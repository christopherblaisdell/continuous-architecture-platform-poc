# svc-check-in — Service Architecture Page

| | |
|-----------|-------|
| **Service** | svc-check-in |
| **Domain** | Operations |
| **Team** | NovaTrek Operations Team |
| **API Version** | 1.0.0 |
| **Base URL** | `https://api.novatrek.example.com/checkin/v1` |
| **Last Updated** | 2026-03-03 |

---

## Purpose

Handles day-of-adventure check-in workflow including wristband assignment, gear pickup verification, waiver validation, and group assembly. Coordinates with svc-reservations for booking data, svc-safety-compliance for waiver status, and svc-gear-inventory for equipment assignment.

---

## Architecture Decisions

| ADR | Title | Status | Impact |
|-----|-------|--------|--------|
| [ADR-004](../decisions/ADR-004-configuration-driven-classification.md) | Configuration-Driven Classification | Accepted | Category-to-pattern mapping via Spring Cloud Config YAML |
| [ADR-005](../decisions/ADR-005-pattern3-default-fallback.md) | Pattern 3 Default Fallback | Accepted | Unknown categories default to Full Service (safety-first) |
| [ADR-007](../decisions/ADR-007-four-field-identity-verification.md) | Four-Field Identity Verification | Accepted | Kiosk verification via last name + confirmation + date + count |
| [ADR-009](../decisions/ADR-009-session-scoped-kiosk-access.md) | 30-Minute Kiosk Session | Accepted | JWT-based session with 30-minute expiry for kiosk access |

---

## Integration Points

| Direction | Service | Purpose |
|-----------|---------|---------|
| Calls → | svc-reservations | Booking lookup, participant verification |
| Calls → | svc-guest-profiles | Profile lookup/creation, temporary profile creation |
| Calls → | svc-safety-compliance | Waiver validation |
| Calls → | svc-gear-inventory | Equipment assignment and pickup verification |
| Calls → | svc-partner-integrations | Fallback reservation lookup for partner bookings |
| Calls → | svc-trip-catalog | Adventure category lookup for classification |

---

## Sequence Diagrams

### Check-In Process Flow

<object data="diagrams/check-in-process-flow.svg" type="image/svg+xml" style="width: 100%; max-width: 100%; overflow-x: auto;">Check-In Process Flow diagram</object>


<object data="diagrams/lookup-orchestration.svg" type="image/svg+xml" style="width: 100%; max-width: 100%; overflow-x: auto;">Lookup Orchestration diagram</object>

---

## Key Patterns

- **Adventure Category Classification**: Maps 25 adventure categories to 3 check-in UI patterns (Basic, Guided, Full Service) via configuration-driven YAML. See [ADR-004](../decisions/ADR-004-configuration-driven-classification.md).
- **Kiosk Session Management**: JWT-based 30-minute sessions with one-active-per-device enforcement.

---

## Recent Changes

| Ticket | Change | Date |
|--------|--------|------|
| NTK-10002 | Added adventure category classification system (3 UI patterns) | Phase 1 |
| NTK-10005 | Added RFID wristband field to check-in schema | Phase 1 |

---

## Source Code

- [svc-check-in](../phase-1-ai-tool-cost-comparison/workspace/source-code/svc-check-in/)
- [OpenAPI Spec](../phase-1-ai-tool-cost-comparison/workspace/corporate-services/services/svc-check-in.yaml)
- [Component Diagram](../phase-1-ai-tool-cost-comparison/workspace/corporate-services/diagrams/Components/ntk10003-unregistered-checkin-components.puml)

---

## Technical Debt and Open Questions

- Circuit breaker configuration for svc-partner-integrations fallback path needs tuning (timeout, retry limits)
- Classification fallback metric (`checkin.classification.fallback.count`) alert threshold needs calibration after go-live
- PUT-to-PATCH migration for any endpoints that accept full-entity updates (preventive, per [ADR-010](../decisions/ADR-010-patch-semantics-schedule-updates.md) pattern)
