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
| [ADR-006](../decisions/ADR-006-orchestrator-pattern-checkin.md) | Orchestrator Pattern | Accepted | Multi-service orchestration for unregistered guest lookup lives here |
| [ADR-007](../decisions/ADR-007-four-field-identity-verification.md) | Four-Field Identity Verification | Accepted | Kiosk verification via last name + confirmation + date + count |
| [ADR-008](../decisions/ADR-008-temporary-guest-profile.md) | Temporary Guest Profile | Accepted | Creates minimal temporary profiles for unregistered guests |
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

## Key Patterns

- **Adventure Category Classification**: Maps 25 adventure categories to 3 check-in UI patterns (Basic, Guided, Full Service) via configuration-driven YAML. See [ADR-004](../decisions/ADR-004-configuration-driven-classification.md).
- **Unregistered Guest Orchestration**: Multi-service fan-out pattern with conditional partner fallback and parallel safety/gear checks. See [ADR-006](../decisions/ADR-006-orchestrator-pattern-checkin.md) and [orchestration diagram](../phase-1-ai-tool-cost-comparison/workspace/work-items/tickets/_NTK-10003-unregistered-guest-self-checkin/3.solution/i.impacts/impact.1/lookup-orchestration.puml).
- **Kiosk Session Management**: JWT-based 30-minute sessions with one-active-per-device enforcement.

---

## Recent Changes

| Ticket | Change | Date |
|--------|--------|------|
| NTK-10002 | Added adventure category classification system (3 UI patterns) | Phase 1 |
| NTK-10003 | Added unregistered guest self-service check-in flow | Phase 1 |
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
