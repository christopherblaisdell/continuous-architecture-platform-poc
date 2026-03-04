# svc-reservations — Service Architecture Page

| | |
|-----------|-------|
| **Service** | svc-reservations |
| **Domain** | Booking |
| **API Version** | 1.0.0 |
| **Base URL** | `https://api.novatrek.example.com/reservations/v1` |
| **Last Updated** | 2026-03-03 |

---

## Purpose

Manages the full lifecycle of adventure reservations — creation, modification, cancellation, and participant management. Serves as the system of record for booking data consumed by check-in, scheduling, and guest-facing applications.

---

## Architecture Decisions

| ADR | Title | Status | Impact |
|-----|-------|--------|--------|
| [ADR-006](../decisions/ADR-006-orchestrator-pattern-checkin.md) | Orchestrator Pattern | Accepted | Queried by svc-check-in for reservation lookup during unregistered guest flow |
| [ADR-007](../decisions/ADR-007-four-field-identity-verification.md) | Four-Field Identity Verification | Accepted | Must maintain accurate last name, confirmation code, adventure date, and participant count for kiosk verification |

---

## Integration Points

| Direction | Service | Purpose |
|-----------|---------|---------|
| ← Called by | svc-check-in | Reservation + participant lookup for check-in |
| ← Called by | svc-scheduling-orchestrator | Trip scheduling and capacity data |
| ← Called by | svc-trip-catalog | Availability consumed for booking creation |
| Calls → | svc-guest-profiles | Guest identity validation on booking |

---

## Sequence Diagrams

### Reservation Booking Flow

<object data="diagrams/reservation-booking-flow.svg" type="image/svg+xml" style="width: 100%; max-width: 100%; overflow-x: auto;">Reservation Booking Flow diagram</object>

### Partner Booking Flow

<object data="diagrams/partner-booking-flow.svg" type="image/svg+xml" style="width: 100%; max-width: 100%; overflow-x: auto;">Partner Booking Flow diagram</object>

---

## Key Patterns

- **Multi-Source Bookings**: Reservations originate from direct bookings, partner integrations (travel agents), and gift card redemptions. All booking sources populate the four verification fields required by [ADR-007](../decisions/ADR-007-four-field-identity-verification.md).
- **Participant Count Accuracy**: Participant count is a verification field — changes after booking must be reflected accurately to prevent kiosk verification failures.

---

## Recent Changes

| Ticket | Change | Date |
|--------|--------|------|
| NTK-10002 | Adventure category field used by check-in classification system | Phase 1 |
| NTK-10003 | Reservation lookup endpoint consumed by unregistered guest flow | Phase 1 |

---

## Source Code

- [svc-reservations](../phase-1-ai-tool-cost-comparison/workspace/source-code/svc-reservations/)
- [OpenAPI Spec](../phase-1-ai-tool-cost-comparison/workspace/corporate-services/services/svc-reservations.yaml)

---

## Technical Debt and Open Questions

- No known architectural debt from Phase 1 work
- Participant count change propagation should be verified end-to-end with kiosk verification flow
