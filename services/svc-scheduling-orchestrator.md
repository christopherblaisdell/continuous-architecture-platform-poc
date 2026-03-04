# svc-scheduling-orchestrator — Service Architecture Page

| | |
|-----------|-------|
| **Service** | svc-scheduling-orchestrator |
| **Domain** | Scheduling |
| **Team** | NovaTrek Platform Engineering |
| **API Version** | 3.0.1 |
| **Base URL** | `https://api.novatrek.example.com/scheduling/v1` |
| **Last Updated** | 2026-03-03 |

---

## Purpose

Central orchestration service for NovaTrek trip scheduling. Coordinates guide availability (svc-guide-management), trail conditions (svc-trail-management), weather forecasts (svc-weather), trip definitions (svc-trip-catalog), and location capacity (svc-location-services) to produce optimized schedules and resolve conflicts. Acts as the single source of truth for schedule-related conflict resolution.

---

## Architecture Decisions

| ADR | Title | Status | Impact |
|-----|-------|--------|--------|
| [ADR-010](../decisions/ADR-010-patch-semantics-schedule-updates.md) | PUT → PATCH Semantics | Proposed | Switch to partial-update DTO to prevent overwriting guide-owned fields |
| [ADR-011](../decisions/ADR-011-optimistic-locking-daily-schedule.md) | Optimistic Locking | Proposed | Add JPA `@Version` to DailySchedule for concurrent write detection |

---

## Integration Points

| Direction | Service | Purpose |
|-----------|---------|---------|
| Calls → | svc-guide-management | Guide availability, certifications, preferences |
| Calls → | svc-trail-management | Trail conditions, closures |
| Calls → | svc-weather | Weather forecasts for scheduling windows |
| Calls → | svc-trip-catalog | Trip definitions, capacity requirements |
| Calls → | svc-location-services | Location capacity constraints |
| ← Called by | svc-reservations | Schedule availability queries |

---

## Sequence Diagrams

### Scheduling Orchestration Flow

<object data="diagrams/scheduling-orchestration-flow.svg" type="image/svg+xml" style="width: 100%; max-width: 100%; overflow-x: auto;">Scheduling Orchestration Flow diagram</object>

---

## Key Patterns

- **Data Ownership Boundary**: The scheduling orchestrator owns schedule optimization fields (assigned guide, trip slot, route). Guide-owned fields (guideNotes, guidePreferences, medical restrictions) must never be modified by the orchestrator. Enforced via PATCH semantics with `PatchScheduleDto`. See [ADR-010](../decisions/ADR-010-patch-semantics-schedule-updates.md).
- **Optimistic Concurrency**: Nightly batch optimization runs concurrently across regions. JPA `@Version` on `DailySchedule` detects race conditions with retry+backoff (max 3 retries). See [ADR-011](../decisions/ADR-011-optimistic-locking-daily-schedule.md).
- **Asynchronous Optimization**: Schedule requests return a request ID for polling; optimization runs asynchronously.

---

## Recent Changes

| Ticket | Change | Date |
|--------|--------|------|
| NTK-10004 | Root cause: PUT overwrites guide data. Fix: PATCH semantics + optimistic locking | Phase 1 |

---

## Source Code

- [svc-scheduling-orchestrator](../phase-1-ai-tool-cost-comparison/workspace/source-code/svc-scheduling-orchestrator/)
- [OpenAPI Spec](../phase-1-ai-tool-cost-comparison/workspace/corporate-services/services/svc-scheduling-orchestrator.yaml)

---

## Technical Debt and Open Questions

- **PUT endpoint deprecation**: Existing PUT endpoint must be deprecated with sunset header and migrated off by all callers before removal
- **Retry exhaustion handling**: If all 3 optimistic lock retries fail, the current behavior is to log an error — needs alerting and operational runbook
- **ETag-based concurrency**: Deferred to future sprint as complementary measure for external API consumers (per ADR-011 discussion)
- **47ms race window**: Elastic logs confirm concurrent writes for guide G-4821 — monitoring should track conflict frequency post-fix
