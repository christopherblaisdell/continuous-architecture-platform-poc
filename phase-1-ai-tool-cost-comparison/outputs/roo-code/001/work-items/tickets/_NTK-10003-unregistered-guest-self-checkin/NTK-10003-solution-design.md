<!-- CONFLUENCE-PUBLISH -->

# NTK-10003 - Solution Design: Unregistered Guest Self-Service Check-in

| Field | Value |
|-------|-------|
| Version | 1.9 |
| Status | APPROVED |
| Author | Priya Sharma (Solution Architect) |
| Last Updated | 2026-03-03 |
| Reviewers | Marcus Chen (Security), Dev Patel (svc-check-in), Lisa Nakamura (svc-guest-profiles), Sam Okonkwo (svc-reservations), Rachel Torres (QA) |

## Problem Statement

Unregistered guests (partner bookings, gift card recipients, companions) cannot use self-service check-in kiosks and must queue for staff-assisted check-in. This results in average wait times of 22 minutes during peak hours, annual staffing costs of approximately $840K for manual check-in support, and a 34% dissatisfaction rate among partner-booked guests.

## Solution Overview

Implement a reservation lookup and identity verification flow in svc-check-in that enables unregistered guests to access the self-service kiosk. The solution uses an **orchestrator pattern** within svc-check-in to coordinate verification across multiple downstream services, with a **graceful fallback** to partner integration systems when direct reservation lookup fails.

### Proposed New Endpoint

**POST /check-ins/self-service/unregistered** (previously `/check-ins/lookup-reservation`)

The orchestrator performs the following sequence:

1. Validate and normalize input fields
2. Verify identity fields against reservation data (svc-reservations)
3. If not found, attempt partner fallback (svc-partner-integrations)
4. Find or create a temporary guest profile (svc-guest-profiles)
5. Check safety waiver and gear assignment status in parallel (svc-safety-compliance + svc-gear-inventory)
6. Grant a time-scoped kiosk session (30-minute JWT)

### Request Schema

```json
{
  "last_name": "string (required, 1-100 chars)",
  "confirmation_code": "string (required, 8 chars alphanumeric, case-insensitive)",
  "adventure_date": "string (required, ISO 8601 date: YYYY-MM-DD)",
  "participant_count": "integer (required, 1-20)",
  "kiosk_device_id": "string (required, UUID of the kiosk terminal)"
}
```

### Response Schema - Success (200 OK)

```json
{
  "session_token": "string (JWT, 30-minute expiry)",
  "reservation_id": "string (UUID)",
  "guest_profile_id": "string (UUID, temporary or matched profile)",
  "adventure_name": "string",
  "adventure_date": "string (ISO 8601)",
  "check_in_status": {
    "waiver_complete": "boolean",
    "waiver_url": "string (nullable, URL for digital waiver if incomplete)",
    "gear_assigned": "boolean",
    "gear_items": [
      {
        "item_type": "string",
        "size": "string",
        "pickup_location": "string"
      }
    ]
  },
  "participants": [
    {
      "name": "string",
      "role": "string (PRIMARY | COMPANION)"
    }
  ]
}
```

### Error Responses

| Status | Error Code | Description |
|--------|-----------|-------------|
| 404 | RESERVATION_NOT_FOUND | No matching reservation found after primary and partner fallback |
| 429 | RATE_LIMIT_EXCEEDED | 5 attempts per kiosk per 15-minute window exceeded |
| 400 | VALIDATION_ERROR | Input validation failure (invalid date, malformed confirmation code) |
| 503 | SERVICE_UNAVAILABLE | Critical downstream service unavailable |

## Orchestration Flow

### Step 1: Validate and Normalize Input

- Normalize `confirmation_code` to uppercase, strip hyphens
- Validate `adventure_date` is today or within the next 24 hours
- Validate `participant_count` is between 1 and 20
- Check rate limit for the kiosk device ID

### Step 2: Lookup Reservation (svc-reservations)

- Call `POST /reservations/search` with the four verification fields
- All four fields must match (last name case-insensitive, confirmation code normalized)
- If found: proceed to Step 3
- If not found: proceed to Step 2a (Partner Fallback)

### Step 2a: Partner Fallback (svc-partner-integrations)

- Extract partner identifier from confirmation code prefix (EM-, TF-, WP-)
- Call `POST /partner-integrations/verify-booking` with confirmation code and last name
- If partner confirms: create synced reservation record, proceed to Step 3
- If unavailable (circuit breaker open): return 404 directing guest to staff desk

### Step 3: Find or Create Guest Profile (svc-guest-profiles)

- Call `GET /guest-profiles?reservation_id={id}` to check for existing profile
- If no profile exists: call `POST /guest-profiles/temporary` with last name and reservation ID
- Returns `guest_profile_id` for session creation

### Step 4: Parallel Checks (svc-safety-compliance + svc-gear-inventory)

Execute in parallel using `CompletableFuture.allOf()`:

- **svc-safety-compliance**: `GET /safety-compliance/waivers?reservation_id={id}` -- waiver status and URL
- **svc-gear-inventory**: `GET /gear-inventory/assignments?reservation_id={id}` -- gear list and pickup locations

### Step 5: Create Kiosk Session

- Generate JWT with claims: `guest_profile_id`, `reservation_id`, `kiosk_device_id`
- 30-minute expiry
- Store in Redis with kiosk device ID as secondary key (one active session per kiosk)
- Return aggregated response

## Source Code Analysis

The existing `CheckInController.java` has a basic `POST /check-ins/lookup-reservation` endpoint (lines 35-43) that accepts only `confirmationCode` and `lastName`. This implementation:

- Uses a simple `Map<String, String>` request body instead of a typed DTO
- Does not perform input validation or normalization
- Does not include the four-field verification required by security review
- Does not implement rate limiting, session management, or downstream orchestration

The new implementation will replace this with a fully orchestrated endpoint using the `ReservationLookupController` and `ReservationLookupService` classes per the guidance document.

## Security Considerations

| Concern | Mitigation |
|---------|------------|
| Reservation enumeration | Rate limiting: 5 attempts per kiosk per 15-minute window; 2-second artificial delay on failed lookups |
| PII exposure | All verification fields in POST body (never URL params); PII masked in logs |
| Session hijacking | JWT scoped to specific kiosk device ID; 30-minute hard expiry; one active session per kiosk |
| Brute force attacks | Rate limiting at API gateway AND application level (defense in depth) |
| Unauthorized data access | Temporary session grants access only to matched reservation data |
| Audit compliance | All lookup attempts logged with timestamp, kiosk ID, and masked input fields |

## Impacted Components

| Service | Change Type | Estimated Effort | Owner |
|---------|-------------|-------------------|-------|
| svc-check-in | New endpoint, orchestration logic, session management | 5 days | Dev Patel |
| svc-reservations | New composite search endpoint, index creation | 2 days | Sam Okonkwo |
| svc-guest-profiles | New temporary profile creation endpoint, profile type field | 3 days | Lisa Nakamura |
| svc-safety-compliance | Extend waiver lookup to support reservation_id query | 1 day | Wei Zhang |
| svc-gear-inventory | No changes (existing endpoint supports reservation_id) | 0 days | -- |
| svc-partner-integrations | No changes (existing verify-booking endpoint) | 0 days | -- |
| API Gateway | Rate limiting rule for new endpoint | 0.5 days | Platform Team |
| Kiosk UI | New "Check in with Confirmation Code" flow | 3 days | Jordan Park |

## Deployment Sequence

1. **svc-reservations** -- New search endpoint available first
2. **svc-guest-profiles** -- Temporary profile endpoint available
3. **svc-safety-compliance** -- Extended waiver lookup available
4. **API Gateway** -- Rate limiting rules deployed
5. **svc-check-in** -- Orchestrator endpoint (depends on all upstream)
6. **Kiosk UI** -- New check-in flow (after svc-check-in confirmed healthy)

### Phased Rollout

| Phase | Date | Scope | Success Criteria |
|-------|------|-------|-----------------|
| Phase 1 | 2026-03-01 | Cascade Ridge base camp | p95 latency under 5s, error rate under 1%, minimum 20 successful check-ins |
| Phase 2 | 2026-03-08 | Thunder Peak, Glacier Basin | Sustained metrics, no critical incidents |
| Phase 3 | 2026-03-15 | All remaining base camps | Full rollout for spring peak season |

Feature flag: `KIOSK_UNREGISTERED_CHECKIN_ENABLED` (per base camp location, default: false)

## Related Artifacts

- [Ticket Report](1.requirements/NTK-10003.ticket.report.md)
- [Decisions](3.solution/d.decisions/decisions.md)
- [Guidance](3.solution/g.guidance/guidance.md)
- [Impact 1 - svc-check-in](3.solution/i.impacts/impact.1/impact.1.md)
- [Impact 2 - svc-guest-profiles](3.solution/i.impacts/impact.2/impact.2.md)
- [Impact 3 - svc-safety-compliance](3.solution/i.impacts/impact.3/impact.3.md)
- [Impact 4 - svc-reservations](3.solution/i.impacts/impact.4/impact.4.md)
- [Risks](3.solution/r.risks/risks.md)
- [User Stories](3.solution/u.user.stories/user-stories.md)
- [C4 Component Diagram](corporate-services/diagrams/Components/ntk10003-unregistered-checkin-components.puml)
- [Sequence Diagram](corporate-services/diagrams/Sequence/unregistered-guest-checkin-flow.puml)
