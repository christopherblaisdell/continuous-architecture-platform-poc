<!-- PUBLISH -->

# NTK-10003 - Solution Design: Unregistered Guest Self-Service Check-in

| Field | Value |
|-------|-------|
| Version | 1.9 |
| Date | 2026-02-25 |
| Author | Priya Sharma (Solution Architect) |
| Status | APPROVED |
| Ticket | NTK-10003 |
| Reviewers | Marcus Chen (Security), Dev Patel (svc-check-in), Lisa Nakamura (svc-guest-profiles), Sam Okonkwo (svc-reservations), Rachel Torres (QA) |

## Problem Statement

Unregistered guests (partner bookings, gift card recipients, companions) cannot use self-service check-in kiosks and must queue for staff-assisted check-in. This results in average wait times of 22 minutes during peak hours, annual staffing costs of approximately $840K for manual check-in support, and a 34% dissatisfaction rate among partner-booked guests. Only 12% of unregistered guests who check in via staff assistance convert to registered NovaTrek accounts, compared to an industry benchmark of 35-45% for self-service flows with account creation prompts.

## Solution Overview

Implement a reservation lookup and identity verification flow in svc-check-in that enables unregistered guests to access the self-service kiosk. The solution uses an **orchestrator pattern** within svc-check-in to coordinate verification across multiple downstream services, with a **graceful fallback** to partner integration systems when direct reservation lookup fails.

The orchestrator performs the following sequence:

1. Validate and normalize input fields
2. Look up reservation by four verification fields (svc-reservations)
3. If not found, attempt partner fallback verification (svc-partner-integrations)
4. Find or create a temporary guest profile (svc-guest-profiles)
5. Check safety waiver and gear assignment status in parallel (svc-safety-compliance + svc-gear-inventory)
6. Grant a time-scoped kiosk session (JWT, 30-minute expiry)

### Architecture Diagrams

- Component diagram: See [ntk10003-unregistered-checkin-components.puml](../../corporate-services/diagrams/Components/ntk10003-unregistered-checkin-components.puml)
- Sequence diagram: See [ntk10003-unregistered-checkin-sequence.puml](../../corporate-services/diagrams/Sequence/ntk10003-unregistered-checkin-sequence.puml)

## Source Code Analysis

### Current State of POST /check-ins/lookup-reservation (CheckInController.java)

The existing `POST /lookup-reservation` endpoint in `CheckInController.java` is a minimal stub that:

- Accepts a raw `Map<String, String>` with only `confirmationCode` and `lastName` (line 36-41)
- Lacks input validation (no `@Valid` annotation, no request DTO)
- Does not include `adventure_date`, `participant_count`, or `kiosk_device_id` fields
- Returns a plain `CheckInRecord` rather than the enriched session response

This implementation must be replaced with the full orchestration flow described in this design.

### Current State of GuestService.java (svc-guest-profiles)

The `GuestService.createGuest()` method (line 31-41) requires email for duplicate detection:

```
Optional<GuestProfile> existing = guestRepository.findByEmail(guest.getEmail());
```

Temporary guest profiles cannot provide email (partner bookings have the agent's email, not the guest's). A new `createTemporaryProfile()` method is needed that:

- Accepts only `last_name` and `reservation_id` as required fields
- Uses `reservation_id` for deduplication instead of email
- Sets `profile_type` to `TEMPORARY`

### svc-safety-compliance API Gap

The current `GET /waivers` endpoint requires `guest_id` as a required query parameter. The unregistered guest flow needs lookup by `reservation_id`, since the guest may not have an established profile at the time of waiver verification. The endpoint must support `reservation_id` as an alternative query parameter.

### svc-reservations API Gap

The current `Reservation` schema does not include a `confirmation_code` field. The `GET /reservations` search supports filtering by `guest_id`, `trip_id`, `status`, and date range, but not by confirmation code or last name. A new composite search endpoint (`POST /reservations/search`) is required to support the four-field verification lookup.

## New Endpoint Specification

### POST /check-ins/lookup-reservation

**Service**: svc-check-in

**Purpose**: Verify an unregistered guest's identity against a reservation and grant temporary kiosk access for self-service check-in.

#### Request Schema

```json
{
  "last_name": "string (required, 1-100 chars)",
  "confirmation_code": "string (required, 8 chars alphanumeric, case-insensitive)",
  "adventure_date": "string (required, ISO 8601 date: YYYY-MM-DD)",
  "participant_count": "integer (required, 1-20)",
  "kiosk_device_id": "string (required, UUID of the kiosk terminal)"
}
```

#### Response Schema - Success (200 OK)

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

#### Response Schema - Failure (404 Not Found)

```json
{
  "error": "RESERVATION_NOT_FOUND",
  "message": "We couldn't find a matching reservation. Please verify your details or visit the service desk for assistance.",
  "remaining_attempts": "integer (attempts left in rate limit window)"
}
```

#### Response Schema - Rate Limited (429 Too Many Requests)

```json
{
  "error": "RATE_LIMIT_EXCEEDED",
  "message": "Too many attempts. Please visit the service desk for assistance.",
  "retry_after_seconds": "integer"
}
```

## Orchestration Flow

### Step 1 Validate and Normalize Input

- Normalize `confirmation_code` to uppercase, strip hyphens
- Validate `adventure_date` is today or within the next 24 hours
- Validate `participant_count` is between 1 and 20
- Validate `kiosk_device_id` is a valid UUID
- Check rate limit for the kiosk device

### Step 2 Lookup Reservation (svc-reservations)

- Call `POST /reservations/search` with all four verification fields
- All four fields must match for a successful lookup
- If found: proceed to Step 3
- If not found: proceed to Step 2a (Partner Fallback)

### Step 2a Partner Fallback (svc-partner-integrations)

- Extract partner identifier from confirmation code prefix (e.g., `EM-` for ExploreMore, `TF-` for TrailFinder, `WP-` for WildPass)
- Call `POST /partner-integrations/verify-booking` with confirmation code and last name
- If partner confirms booking: create a synced reservation record in svc-reservations, then proceed to Step 3
- If partner lookup fails or is unavailable (circuit breaker open): apply 2-second artificial delay, then return 404 to guest
- Circuit breaker configuration: 30-second timeout, 50% error rate threshold, 60-second recovery window

### Step 3 Find or Create Guest Profile (svc-guest-profiles)

- Call `GET /guest-profiles?reservation_id={id}` to check for existing profile
- If no profile exists: call `POST /guest-profiles/temporary` with `last_name` and `reservation_id`
- Returns `guest_profile_id` for session creation

### Step 4 Parallel Checks (svc-safety-compliance + svc-gear-inventory)

Execute in parallel using `CompletableFuture.allOf()`:

- **svc-safety-compliance**: `GET /safety-compliance/waivers?reservation_id={id}`
  - Returns waiver completion status and digital waiver URL if incomplete
  - If service is unavailable: proceed with `waiver_complete: null` and log warning
- **svc-gear-inventory**: `GET /gear-inventory/assignments?reservation_id={id}`
  - Returns gear assignment list and pickup locations
  - If service is unavailable: proceed with `gear_assigned: null` and log warning

### Step 5 Create Kiosk Session

- Generate JWT session token with claims: `guest_profile_id`, `reservation_id`, `kiosk_device_id`
- Set 30-minute expiry (configurable via `kiosk.session.expiry-minutes`)
- Store session in Redis with kiosk device ID as secondary key (one active session per kiosk)
- Return aggregated response to kiosk

## Security Considerations

| Concern | Mitigation |
|---------|------------|
| Reservation enumeration | Rate limiting: 5 attempts per kiosk per 15-minute window; 2-second artificial delay on failed lookups |
| PII exposure | All verification fields in POST body (never URL params); PII masked in logs (last 3 chars only) |
| Session hijacking | JWT scoped to specific kiosk device ID; 30-minute hard expiry; one active session per kiosk |
| Brute force attacks | Rate limiting at API gateway AND application level (defense in depth); lockout messaging directs to staff |
| Unauthorized data access | Temporary session grants access only to matched reservation data; no cross-reservation queries permitted |
| Audit compliance | All lookup attempts (success/failure) logged with timestamp, kiosk ID, and masked input fields |

## Impacted Components

| Service | Change Type | Estimated Effort | Owner |
|---------|-------------|-------------------|-------|
| svc-check-in | New orchestration logic, replace stub endpoint, session management | 5 days | Dev Patel |
| svc-reservations | New composite search endpoint, confirmation_code field, index creation | 2 days | Sam Okonkwo |
| svc-guest-profiles | New temporary profile endpoint, profile_type field, dedup by reservation_id | 3 days | Lisa Nakamura |
| svc-safety-compliance | Extend waiver lookup to support reservation_id query | 1 day | Wei Zhang |
| svc-gear-inventory | No changes (existing endpoint supports reservation_id) | 0 days | -- |
| svc-partner-integrations | No changes (existing verify-booking endpoint) | 0 days | -- |
| API Gateway | Rate limiting rule for new endpoint | 0.5 days | Platform Team |
| Kiosk UI | New "Check in with Confirmation Code" flow | 3 days | Jordan Park (UX) |

**Total estimated effort**: 14.5 days across teams (parallelizable to approximately 6 days calendar time)

## Deployment Sequence

Services must be deployed in the following order to avoid runtime errors:

1. **svc-reservations** - New search endpoint and confirmation_code field must be available first
2. **svc-guest-profiles** - Temporary profile endpoint must be available before svc-check-in calls it
3. **svc-safety-compliance** - Extended waiver lookup must be available before svc-check-in calls it
4. **API Gateway** - Rate limiting rules for the new endpoint
5. **svc-check-in** - Orchestrator endpoint (deployed last, depends on all upstream services)
6. **Kiosk UI** - New check-in flow (deployed after svc-check-in is confirmed healthy)

### Phased Rollout Plan

| Phase | Date | Scope | Success Criteria |
|-------|------|-------|-----------------|
| Phase 1 | 2026-03-01 | Cascade Ridge base camp | p95 latency under 5s, error rate under 1%, minimum 20 successful check-ins |
| Phase 2 | 2026-03-08 | Thunder Peak, Glacier Basin | Sustained metrics from Phase 1, no critical incidents |
| Phase 3 | 2026-03-15 | All remaining base camps | Full rollout for spring peak season |

Feature flag: `KIOSK_UNREGISTERED_CHECKIN_ENABLED` (per base camp location, default: `false`)

## Testing Strategy

### Unit Tests

- Orchestration logic with mocked downstream services
- Input validation and normalization
- Rate limiting counter behavior
- JWT session token generation and validation

### Integration Tests

- svc-check-in to svc-reservations: reservation lookup with valid and invalid inputs
- svc-check-in to svc-guest-profiles: temporary profile creation and deduplication
- svc-check-in to svc-safety-compliance: waiver status retrieval by reservation_id
- Partner fallback flow with simulated partner responses

### End-to-End Tests

- Full kiosk check-in flow (requires kiosk emulator environment)
- Rate limiting verification across multiple kiosks
- Session expiry and cleanup
- Concurrent lookup requests (target: 100 concurrent, p95 under 5 seconds)

### Security Tests

- PII masking verification in all log outputs
- Rate limit bypass attempt validation
- Session token scope enforcement
- Cross-reservation data isolation

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-23 | Priya Sharma | Initial draft with problem statement and proposed approach |
| 1.1 | 2026-01-24 | Priya Sharma | Added security considerations based on Marcus Chen review |
| 1.2 | 2026-01-27 | Priya Sharma | Incorporated UX wireframe references from Jordan Park |
| 1.3 | 2026-01-28 | Priya Sharma | Added endpoint specification and orchestration flow |
| 1.4 | 2026-01-29 | Priya Sharma | Parallelized safety compliance and gear inventory calls per Dev Patel feedback |
| 1.5 | 2026-01-30 | Priya Sharma | Added temporary guest profile details from Lisa Nakamura |
| 1.6 | 2026-02-03 | Priya Sharma | Added reservation search index details from Sam Okonkwo |
| 1.7 | 2026-02-05 | Priya Sharma | Security approval incorporated (v1.6 review by Marcus Chen) |
| 1.8 | 2026-02-20 | Priya Sharma | Added phased rollout plan and feature flag strategy |
| 1.9 | 2026-02-25 | Solution Architecture | Source code analysis: identified gaps in CheckInController stub, GuestService email dependency, waiver API contract, and reservation schema. Added confirmation_code field requirement for svc-reservations. Updated deployment sequence. |
