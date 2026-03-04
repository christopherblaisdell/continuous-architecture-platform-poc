---
tags:
  - diagrams
  - svc-scheduling-orchestrator
  - scheduling
---

# svc-scheduling-orchestrator

| | |
|-----------|-------|
| **Service** | svc-scheduling-orchestrator |
| **Domain** | Scheduling |
| **Team** | NovaTrek Platform Engineering |
| **API Version** | 3.0.1 |
| **Base URL** | `https://api.novatrek.example.com/scheduling/v1` |

---

## Purpose

Central orchestration service for NovaTrek trip scheduling. Coordinates guide availability (svc-guide-management), trail conditions (svc-trail-management), weather forecasts (svc-weather), trip definitions (svc-trip-catalog), and location capacity (svc-location-services) to produce optimized schedules and resolve conflicts. Acts as the single source of truth for schedule-related conflict resolution.

---

## Architecture Decisions

| ADR | Title | Status |
|-----|-------|--------|
| ADR-010 | PUT to PATCH Semantics | Proposed |
| ADR-011 | Optimistic Locking for Daily Schedule | Proposed |

---

## Integration Points

| Direction | Service | Purpose |
|-----------|---------|---------|
| Calls | svc-guide-management | Guide availability, certifications, preferences |
| Calls | svc-trail-management | Trail conditions, closures, elevation data |
| Calls | svc-weather | Weather forecasts for scheduling windows |
| Calls | svc-trip-catalog | Trip definitions, capacity requirements |
| Calls | svc-location-services | Location capacity constraints |
| Called by | svc-reservations | Schedule availability queries |
| Publishes | Kafka `schedule.optimized` | Consumed by downstream scheduling consumers |

---

## Key Patterns

- **Data Ownership Boundary** — Owns schedule optimization fields (assigned guide, trip slot, route). Guide-owned fields (guideNotes, guidePreferences, medical restrictions) must never be modified by the orchestrator. Enforced via PATCH semantics with `PatchScheduleDto`
- **Optimistic Concurrency** — Nightly batch optimization runs concurrently across regions. JPA `@Version` on `DailySchedule` detects race conditions with retry+backoff (max 3 retries)
- **Asynchronous Optimization** — Schedule requests return a request ID for polling; optimization runs asynchronously
- **Multi-Factor Conflict Resolution** — Resolves guide availability, trail closure, and severe weather conflicts with automatic fallback alternatives

---

## Diagrams

### Scheduling Orchestration Flow

Admin-driven schedule optimization sequence showing the full data gathering loop (trip requirements, guide availability, trail conditions, weather forecasts), conflict detection and resolution for four conflict types, and the admin approval workflow.

<figure markdown>
  ![Scheduling Orchestration Flow](svg/scheduling-orchestration-flow.svg){ loading=lazy width="100%" }
  <figcaption>Sequence — Multi-service schedule optimization with conflict resolution</figcaption>
</figure>

---

### Booking Domain Components

Internal component structure showing svc-scheduling-orchestrator alongside svc-reservations and svc-trip-catalog. Illustrates the ConflictResolver component, ScheduleEventPublisher, and inter-service dependencies.

<figure markdown>
  ![Booking Domain Components](svg/booking-domain-components.svg){ loading=lazy width="100%" }
  <figcaption>Component — Booking domain: scheduling orchestrator, reservations, trip catalog</figcaption>
</figure>

---

## Recent Changes

| Ticket | Change |
|--------|--------|
| NTK-10004 | Root cause: PUT overwrites guide data. Fix: PATCH semantics + optimistic locking |

---

## Technical Debt

- **PUT endpoint deprecation** — Existing PUT endpoint must be deprecated with sunset header and migrated off by all callers
- **Retry exhaustion handling** — If all 3 optimistic lock retries fail, current behavior is to log an error. Needs alerting and operational runbook
- **ETag-based concurrency** — Deferred as complementary measure for external API consumers
- **47ms race window** — Elastic logs confirm concurrent writes for guide G-4821. Monitoring should track conflict frequency post-fix
