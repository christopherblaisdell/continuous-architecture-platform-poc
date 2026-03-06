---
title: "NTK-10003 — Unregistered Guest Self-Service Check-in"
description: "Solution design for NTK-10003"
---

# NTK-10003 — Unregistered Guest Self-Service Check-in

| Field | Value |
|-------|-------|
| **Status** | APPROVED |
| **Version** | Date |
| **Author** | Priya Sharma (Solution Architect) |
| **Date** | Date |
| **Ticket** | NTK-10003 |

## Affected Capabilities

| Capability | Impact | Description |
|-----------|--------|-------------|
| [CAP-2.1 Day-of-Adventure Check-In](../capabilities/index.md#cap-21-day-of-adventure-check-in) | enhanced | Check-in flow now supports walk-up guests without prior reservation |
| [CAP-1.1 Guest Identity and Profile Management](../capabilities/index.md#cap-11-guest-identity-and-profile-management) | enhanced | Temporary guest profiles created for unregistered walk-up guests |
| [CAP-1.3 Reservation Management](../capabilities/index.md#cap-13-reservation-management) | enhanced | Just-in-time reservation creation for walk-up guests |

## Affected Services

- [svc-check-in](../microservices/svc-check-in.md)
- [svc-guest-identity](../microservices/svc-guest-identity.md)
- [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md)

## Architecture Decisions

- ADR-006
- ADR-007
- ADR-008
- ADR-009

## Solution Contents

- Requirements
- Analysis
- Decisions
- Impact Assessments (4)
- User Stories
- Implementation Guidance
- Risk Assessment
- Capability Mapping

## Related Solutions

Solutions that share services or capabilities with this design:

| Solution | Shared Capabilities | Shared Services |
|----------|-------------------|-----------------|
| [NTK-10002 — NTK-10002: Adventure Category Classifica](_NTK-10002-adventure-category-classification.md) | CAP-2.1 | svc-check-in |
| [NTK-10004 — NTK-10004: Solution Design — Guide Sched](_NTK-10004-guide-schedule-overwrite-bug.md) | — | svc-scheduling-orchestrator |
| [NTK-10005 — Add Wristband RFID Field to Check-In Rec](_NTK-10005-wristband-rfid-field.md) | CAP-2.1 | svc-check-in |

---


## Problem Statement

Unregistered guests (partner bookings, gift card recipients, companions) cannot use self-service check-in kiosks and must queue for staff-assisted check-in. This results in average wait times of 22 minutes during peak hours, annual staffing costs of approximately $840K for manual check-in support, and a 34% dissatisfaction rate among partner-booked guests.

## Solution Overview

Implement a reservation lookup and identity verification flow in svc-check-in that enables unregistered guests to access the self-service kiosk. The solution uses an **orchestrator pattern** within svc-check-in to coordinate verification across multiple downstream services, with a **graceful fallback** to partner integration systems when direct reservation lookup fails.

The orchestrator performs the following sequence:
1. Verify identity fields against reservation data
2. Find or create a temporary guest profile
3. Check safety waiver and gear assignment status (in parallel)
4. Grant a time-scoped kiosk session

### Architecture Diagram

See: [lookup-orchestration.puml](3.solution/i.impacts/impact.1/lookup-orchestration.puml) for the full sequence diagram.

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

### Step 1: Validate and Normalize Input

- Normalize `confirmation_code` to uppercase
- Validate `adventure_date` is today or within the next 24 hours (early check-in allowed)
- Validate `participant_count` is between 1 and 20

### Step 2: Lookup Reservation (svc-reservations)

- Call `POST /reservations/search` with verification fields
- If found: proceed to Step 3
- If not found: proceed to Step 2a (Partner Fallback)

### Step 2a: Partner Fallback (svc-partner-integrations)

- Call `POST /partner-integrations/verify-booking` with confirmation code and last name
- If partner confirms booking: create reservation record and proceed to Step 3
- If partner lookup fails or is unavailable (circuit breaker open): return 404 to guest

### Step 3: Find or Create Guest Profile (svc-guest-profiles)

- Call `GET /guest-profiles?reservation_id={id}` to check for existing profile
- If no profile exists: call `POST /guest-profiles/temporary` with last name and reservation ID
- Returns `guest_profile_id` for session creation

### Step 4: Parallel Checks (svc-safety-compliance + svc-gear-inventory)

Execute in parallel:

- **svc-safety-compliance**: `GET /safety-compliance/waivers?reservation_id={id}`
  - Returns waiver completion status and digital waiver URL if incomplete
- **svc-gear-inventory**: `GET /gear-inventory/assignments?reservation_id={id}`
  - Returns gear assignment list and pickup locations

### Step 5: Create Kiosk Session

- Generate JWT session token with claims: `guest_profile_id`, `reservation_id`, `kiosk_device_id`
- Set 30-minute expiry
- Store session in Redis with kiosk device ID as secondary key (one active session per kiosk)
- Return aggregated response to kiosk

## Fallback Behavior

If the primary reservation lookup (Step 2) fails to find a match, the orchestrator attempts partner verification before returning a failure:

1. Extract partner identifier from confirmation code prefix (e.g., `EM-` for ExploreMore, `TF-` for TrailFinder, `WP-` for WildPass)
2. Route to the appropriate partner adapter in svc-partner-integrations
3. If partner confirms the booking, svc-reservations creates a synced reservation record for subsequent lookups
4. Circuit breaker configuration: 30-second timeout, 50% error rate threshold, 60-second recovery window
5. If partner integration is unavailable, return 404 with messaging that directs the guest to the service desk with priority queuing

## Security Considerations

| Concern | Mitigation |
|---------|------------|
| Reservation enumeration | Rate limiting: 5 attempts per kiosk per 15-minute window; 2-second artificial delay on failed lookups |
| PII exposure | All verification fields in POST body (never URL params); PII masked in logs (last 3 chars only) |
| Session hijacking | JWT scoped to specific kiosk device ID; 30-minute hard expiry; one active session per kiosk |
| Brute force attacks | Rate limiting at API gateway AND application level (defense in depth); lockout messaging directs to staff |
| Unauthorized data access | Temporary session grants access only to the matched reservation data; no cross-reservation queries permitted |
| Audit compliance | All lookup attempts (success/failure) logged with timestamp, kiosk ID, and masked input fields |

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
| Kiosk UI | New "Check in with Confirmation Code" flow | 3 days | Jordan Park (UX) |

**Total estimated effort**: 14.5 days across teams (parallelizable to ~6 days calendar time)

## Deployment Sequence

Services must be deployed in the following order to avoid runtime errors:

1. **svc-reservations** - New search endpoint must be available before svc-check-in calls it
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
- svc-check-in to svc-safety-compliance: waiver status retrieval by reservation ID
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