# svc-trip-catalog — Service Architecture Page

| | |
|-----------|-------|
| **Service** | svc-trip-catalog |
| **Domain** | Product Catalog |
| **Team** | NovaTrek Platform Engineering |
| **API Version** | 2.4.0 |
| **Base URL** | `https://api.novatrek.example.com/trips/v1` |
| **Last Updated** | 2026-03-03 |

---

## Purpose

Central registry for all bookable adventure experiences. Manages the full lifecycle of trip definitions from draft creation through active availability to retirement. Each trip is associated with a specific activity type, difficulty level, and operating region. Provides trip definitions, scheduling, pricing, and availability data consumed by booking, check-in, and scheduling services.

---

## Architecture Decisions

| ADR | Title | Status | Impact |
|-----|-------|--------|--------|
| [ADR-004](../decisions/ADR-004-configuration-driven-classification.md) | Configuration-Driven Classification | Accepted | Adventure categories defined here are mapped to check-in patterns via Spring Cloud Config in svc-check-in |

---

## Integration Points

| Direction | Service | Purpose |
|-----------|---------|---------|
| ← Called by | svc-check-in | Adventure category lookup for check-in classification |
| ← Called by | svc-scheduling-orchestrator | Trip definitions and capacity requirements |
| ← Called by | svc-reservations | Availability consumed for booking creation |
| Calls → | svc-guide-management | Guide assignments for scheduled departures |
| Calls → | svc-weather | Weather data linked to operating regions |
| Calls → | svc-guest-profiles | Guest certification validation against trip requirements |

---

## Sequence Diagrams

### Reservation Booking Flow

Shows how the trip catalog is queried during the booking process for trip search, details, and eligibility validation.

<object data="diagrams/reservation-booking-flow.svg" type="image/svg+xml" style="width: 100%; max-width: 100%; overflow-x: auto;">Reservation Booking Flow diagram</object>

---

## Key Patterns

- **Adventure Category as Classification Key**: The `adventure_category` field on trip definitions is the input to the check-in classification system. New categories added here must have corresponding entries in the check-in classification config — otherwise, guests default to Pattern 3 (Full Service) per [ADR-005](../decisions/ADR-005-pattern3-default-fallback.md).
- **25 Adventure Categories → 3 Check-In Patterns**: The current category set maps to Basic, Guided, and Full Service check-in workflows via YAML config.

---

## Recent Changes

| Ticket | Change | Date |
|--------|--------|------|
| NTK-10002 | Adventure category field consumed by check-in classification system | Phase 1 |

---

## Source Code

- [svc-trip-catalog](../phase-1-ai-tool-cost-comparison/workspace/source-code/svc-trip-catalog/)
- [OpenAPI Spec](../phase-1-ai-tool-cost-comparison/workspace/corporate-services/services/svc-trip-catalog.yaml)

---

## Technical Debt and Open Questions

- When new adventure categories are added, the check-in classification config must be updated in the same sprint — no automated sync exists
- Consider adding a classification-sync validation step to the trip-catalog deployment pipeline (Phase 3 candidate)
