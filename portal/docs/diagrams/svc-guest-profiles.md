---
tags:
  - diagrams
  - svc-guest-profiles
  - guest-identity
---

# svc-guest-profiles

| | |
|-----------|-------|
| **Service** | svc-guest-profiles |
| **Domain** | Guest Identity |
| **Team** | Guest Experience Team |
| **API Version** | 1.0.0 |
| **Base URL** | `https://api.novatrek.example.com/guests/v1` |

---

## Purpose

Manages guest identity records including full registered accounts and temporary kiosk profiles. Provides profile CRUD, identity lookup, and profile merge capabilities. Serves as the **system of record for guest identity** across the NovaTrek platform — all services must resolve guest identity through this service rather than maintaining shadow guest records.

---

## Architecture Decisions

| ADR | Title | Status |
|-----|-------|--------|
| ADR-006 | Orchestrator Pattern | Accepted |
| ADR-008 | Temporary Guest Profile | Accepted |

---

## Integration Points

| Direction | Service | Purpose |
|-----------|---------|---------|
| Called by | svc-check-in | Profile lookup, temporary profile creation |
| Called by | svc-reservations | Guest identity validation |
| Called by | svc-loyalty-rewards | Guest tier data |
| Publishes | Kafka `guest.registered` | Consumed by downstream services |

---

## Key Patterns

- **Temporary Profile Lifecycle** — `TEMPORARY` profiles are created with minimal data (last name + reservation ID) and auto-anonymized after 90 days. If the guest later registers, the temporary profile is merged into the full account, preserving check-in history
- **Profile Type Enum** — `REGISTERED`, `TEMPORARY` governs required field validation and retention policies
- **Single Source of Truth** — All services must use svc-guest-profiles for guest identity resolution. No shadow guest records allowed

---

## Diagrams

### Guest Domain Components

Internal component structure of svc-guest-profiles alongside svc-check-in and svc-loyalty-rewards. Shows the `GuestProfileController`, `GuestProfileService`, `CertificationValidator`, `GuestRepository`, and `GuestEventPublisher` components with their inter-service communication via API calls and Kafka events.

<figure markdown>
  ![Guest Domain Components](svg/guest-domain-components.svg){ loading=lazy width="100%" }
  <figcaption>Component — Guest domain: profiles, check-in, and loyalty rewards with Kafka event flows</figcaption>
</figure>

---

## Recent Changes

| Ticket | Change |
|--------|--------|
| NTK-10003 | Added `TEMPORARY` profile type, 90-day anonymization job, profile merge logic |

---

## Technical Debt

- Profile merge edge cases: multiple temporary profiles for the same guest across visits need deduplication logic
- Background anonymization job monitoring and alerting needs operational runbook
- `TEMPORARY` profile type may need additional fields if kiosk features expand
