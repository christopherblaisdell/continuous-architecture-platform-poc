# Capability Mapping — NTK-10003

## Affected Capabilities

| Capability | Impact | Description |
|-----------|--------|-------------|
| CAP-2.1 Day-of-Adventure Check-In | Enhanced | Check-in flow supports walk-up guests without prior reservation |
| CAP-1.1 Guest Identity and Profile Management | Enhanced | Temporary guest profiles created for unregistered walk-up guests |
| CAP-1.3 Reservation Management | Enhanced | Just-in-time reservation creation for walk-up guests |

## Emergent L3 Capabilities

- **Reservation Lookup Orchestration** — Four-field identity verification (name, confirmation code, date, party size) for kiosk access
- **Session-Scoped Kiosk Access** — JWT-based 30-minute session tokens for kiosk interactions
- **Temporary Guest Profiles** — Minimal-PII temporary profiles that merge when guest registers

## Related Decisions

- ADR-006: Orchestrator Pattern for Check-In
- ADR-007: Four-Field Identity Verification
- ADR-008: Temporary Guest Profile
- ADR-009: Session-Scoped Kiosk Access
