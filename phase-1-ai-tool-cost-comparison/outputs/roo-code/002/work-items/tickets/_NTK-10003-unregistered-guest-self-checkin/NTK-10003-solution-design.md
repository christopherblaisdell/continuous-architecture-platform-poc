<!-- CONFLUENCE-PUBLISH -->

# NTK-10003 - Solution Design: Unregistered Guest Self-Service Check-in

| Field | Value |
|-------|-------|
| Version | 1.9 |
| Status | APPROVED |
| Author | Solution Architecture (AI-Assisted), based on Priya Sharma v1.8 |
| Last Updated | 2026-03-04 |
| Ticket | NTK-10003 |

## Problem Statement

Unregistered guests (partner bookings, gift card recipients, companions) cannot use self-service check-in kiosks and must queue for staff-assisted check-in. This results in average wait times of 22 minutes during peak hours, annual staffing costs of approximately $840K, and a 34% dissatisfaction rate among partner-booked guests.

## Solution Overview

Implement a reservation lookup and identity verification flow in svc-check-in that enables unregistered guests to access the self-service kiosk. The solution uses an **orchestrator pattern** within svc-check-in to coordinate verification across multiple downstream services, with a **graceful fallback** to partner integration systems when direct reservation lookup fails.

### Orchestration Sequence

1. Verify identity fields against reservation data (svc-reservations)
2. Partner fallback if direct lookup fails (svc-partner-integrations)
3. Find or create a temporary guest profile (svc-guest-profiles)
4. Check safety waiver and gear assignment status in parallel (svc-safety-compliance, svc-gear-inventory)
5. Grant a time-scoped kiosk session (JWT, 30-minute expiry, stored in Redis)

## New Endpoint

### POST /check-ins/lookup-reservation

**Service**: svc-check-in

#### Request Schema

```json
{
  "last_name": "string (required, 1-100 chars)",
  "confirmation_code": "string (required, 8 chars alphanumeric, case-insensitive)",
  "adventure_date": "string (required, ISO 8601 date)",
  "participant_count": "integer (required, 1-20)",
  "kiosk_device_id": "string (required, UUID)"
}
```

#### Response Schema - Success (200 OK)

```json
{
  "session_token": "string (JWT, 30-minute expiry)",
  "reservation_id": "string (UUID)",
  "guest_profile_id": "string (UUID, temporary or matched)",
  "adventure_name": "string",
  "adventure_date": "string (ISO 8601)",
  "check_in_status": {
    "waiver_complete": "boolean",
    "waiver_url": "string (nullable)",
    "gear_assigned": "boolean",
    "gear_items": [{"item_type": "string", "size": "string", "pickup_location": "string"}]
  },
  "participants": [{"name": "string", "role": "PRIMARY | COMPANION"}]
}
```

#### Error Responses

- **404 Not Found**: Reservation not matched. Deliberately vague messaging to prevent enumeration.
- **429 Too Many Requests**: Rate limit exceeded. Returns `retry_after_seconds`.

## Architecture Decisions

| ADR | Decision | Rationale |
|-----|----------|-----------|
| ADR-NTK10003-001 | Orchestrator pattern in svc-check-in | Synchronous kiosk flow requires deterministic branching and 8-second response budget |
| ADR-NTK10003-002 | Four-field identity verification | Fields available across all booking sources; no SMS/email dependency |
| ADR-NTK10003-003 | Temporary guest profiles | Reduces friction; post-check-in registration achieves higher conversion |
| ADR-NTK10003-004 | 30-minute session with JWT | Covers slowest check-in scenarios; self-validating tokens |

See [Decisions](3.solution/d.decisions/decisions.md) for full MADR-formatted ADRs.

## Impacted Components

| Service | Impact Level | Changes | Effort | Owner |
|---------|-------------|---------|--------|-------|
| svc-check-in | PRIMARY | New endpoint, orchestrator, session manager, rate limiter | 5 days | Dev Patel |
| svc-reservations | MODERATE | New composite search endpoint, database index | 2 days | Sam Okonkwo |
| svc-guest-profiles | MODERATE | Temporary profile endpoint, profile_type field, merge logic | 3 days | Lisa Nakamura |
| svc-safety-compliance | MINOR | Extended waiver lookup with reservation_id parameter | 1 day | Wei Zhang |
| svc-gear-inventory | NONE | Existing endpoint supports reservation_id | 0 days | -- |
| svc-partner-integrations | NONE | Existing verify-booking endpoint | 0 days | -- |
| API Gateway | MINOR | Rate limiting rule for new endpoint | 0.5 days | Platform Team |

**Total**: 14.5 days across teams (parallelizable to approximately 6 calendar days)

## Security

| Concern | Mitigation |
|---------|------------|
| Reservation enumeration | Rate limiting (5 per kiosk per 15 min) + 2-second delay on failures |
| PII exposure | POST body only; PII masked in logs (last 3 chars) |
| Session hijacking | JWT scoped to kiosk device ID; 30-minute hard expiry; one session per kiosk |
| Brute force | Defense-in-depth rate limiting (gateway + application) |
| Unauthorized data access | Session grants access only to matched reservation data |
| Audit compliance | All attempts logged with timestamp, kiosk ID, masked inputs |

## Phased Rollout

| Phase | Date | Scope | Success Criteria |
|-------|------|-------|-----------------|
| Phase 1 | 2026-03-01 | Cascade Ridge | p95 under 5s, error rate under 1%, min 20 successful check-ins |
| Phase 2 | 2026-03-08 | Thunder Peak, Glacier Basin | Sustained Phase 1 metrics |
| Phase 3 | 2026-03-15 | All base camps | Full rollout for spring peak season |

Feature flag: `KIOSK_UNREGISTERED_CHECKIN_ENABLED` (per base camp, default `false`)

## Architecture Diagrams

- [C4 Component Diagram](../../corporate-services/diagrams/Components/ntk10003-unregistered-checkin-components.puml)
- [Sequence Diagram](../../corporate-services/diagrams/Sequence/ntk10003-unregistered-checkin-flow.puml)

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
