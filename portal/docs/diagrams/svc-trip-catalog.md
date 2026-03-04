---
tags:
  - diagrams
  - svc-trip-catalog
  - product-catalog
---

# svc-trip-catalog

| | |
|-----------|-------|
| **Service** | svc-trip-catalog |
| **Domain** | Product Catalog |
| **Team** | NovaTrek Platform Engineering |
| **API Version** | 2.4.0 |
| **Base URL** | `https://api.novatrek.example.com/trips/v1` |

---

## Purpose

Central registry for all bookable adventure experiences. Manages the full lifecycle of trip definitions from draft creation through active availability to retirement. Each trip is associated with a specific activity type, difficulty level, and operating region. Provides trip definitions, scheduling, pricing, and availability data consumed by booking, check-in, and scheduling services.

---

## Architecture Decisions

| ADR | Title | Status |
|-----|-------|--------|
| ADR-004 | Configuration-Driven Classification | Accepted |

---

## Integration Points

| Direction | Service | Purpose |
|-----------|---------|---------|
| Called by | svc-check-in | Adventure category lookup for check-in classification |
| Called by | svc-scheduling-orchestrator | Trip definitions and capacity requirements |
| Called by | svc-reservations | Availability for booking creation |
| Calls | svc-guide-management | Guide assignments for scheduled departures |
| Calls | svc-weather | Weather data linked to operating regions |
| Calls | svc-guest-profiles | Guest certification validation against trip requirements |

---

## Key Patterns

- **Adventure Category as Classification Key** — The `adventure_category` field on trip definitions is the input to the check-in classification system. New categories must have corresponding entries in the check-in classification config or guests default to Pattern 3 (Full Service)
- **25 Adventure Categories to 3 Check-In Patterns** — The current category set maps to Basic, Guided, and Full Service check-in workflows via YAML config
- **Availability Engine** — Dedicated component for real-time availability calculation across dates, regions, and party sizes

---

## Diagrams

### Booking Domain Components

Internal component structure of svc-trip-catalog alongside svc-reservations and svc-scheduling-orchestrator. Shows the `TripCatalogController`, `TripCatalogService`, `TripRepository`, and `AvailabilityEngine` components with inter-service communication for availability checks and trip requirement queries.

<figure markdown>
  ![Booking Domain Components](svg/booking-domain-components.svg){ loading=lazy width="100%" }
  <figcaption>Component — Booking domain: trip catalog with availability engine, reservations, scheduling</figcaption>
</figure>

---

## Recent Changes

| Ticket | Change |
|--------|--------|
| NTK-10002 | Adventure category field consumed by check-in classification system |

---

## Technical Debt

- When new adventure categories are added, the check-in classification config must be updated in the same sprint — no automated sync exists
- Consider adding a classification-sync validation step to the trip-catalog deployment pipeline
