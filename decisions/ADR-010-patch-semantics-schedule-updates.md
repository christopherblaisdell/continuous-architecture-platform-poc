# ADR-010: Switch from PUT to PATCH Semantics for Schedule Updates

## Status

Proposed

## Date

2026-02-28

## Context and Problem Statement

The svc-scheduling-orchestrator uses `PUT /api/v1/schedules/{id}` to persist optimized schedule data. This replaces the entire `DailySchedule` entity, including fields owned by svc-guide-management (guideNotes, guidePreferences). This full-replacement behavior silently destroys guide-entered data on every optimization cycle, creating safety risks (lost medical restrictions), operational disruption (15-20 incorrect guide removals per day), and guide frustration.

How should the scheduling orchestrator persist its optimization results without overwriting data it does not own?

## Decision Drivers

- Guide safety: medical restrictions and certification notes must never be silently removed
- Data ownership: each service should only modify fields it is responsible for
- Minimal disruption: the fix should not require changes to svc-guide-management or the database schema
- Backward compatibility: existing API clients should not break

## Considered Options

1. **PATCH semantics** — Add a PATCH endpoint that accepts only orchestrator-owned fields; use a partial-update DTO
2. **Read-merge-write** — Before saving, read the existing entity and merge incoming fields with preserved fields
3. **Document separation** — Split `daily_schedules` into two tables with different owners, joined at read time

## Decision Outcome

**Chosen Option**: "PATCH semantics", because it establishes a clear data ownership boundary at the API level with minimal implementation scope and no schema changes.

### Confirmation

- New `PatchScheduleDto` contains only orchestrator-owned fields
- `PATCH /api/v1/schedules/{id}` endpoint added to ScheduleController
- Existing PUT endpoint deprecated with sunset header
- Integration tests verify guideNotes/guidePreferences survive a PATCH call

## Consequences

### Positive

- Guide enrichment data is structurally preserved — the orchestrator physically cannot overwrite fields not in the DTO
- Clear API contract makes data ownership boundaries explicit
- No database migration or schema change required
- Existing GET endpoints continue to return the full entity unchanged

### Negative

- Requires a new DTO class (`PatchScheduleDto`) and endpoint, adding code surface area
- PUT endpoint must be deprecated and eventually removed, requiring migration of any other callers
- Does not address the secondary concurrency issue (see [ADR-011](ADR-011-optimistic-locking-daily-schedule.md))

### Neutral

- Read-merge-write was rejected because it adds latency (extra SELECT before UPDATE) and still allows accidental overwrites if the merge logic is incorrect

## Pros and Cons of the Options

### PATCH semantics

- **Good**, because structurally prevents overwriting non-owned fields
- **Good**, because minimal implementation scope (new DTO + endpoint)
- **Good**, because follows REST best practices for partial updates
- **Neutral**, because requires clients to switch from PUT to PATCH
- **Bad**, because does not solve concurrency (separate ADR)

### Read-merge-write

- **Good**, because no new endpoint needed — existing PUT becomes merge-aware
- **Bad**, because adds latency (extra SELECT per update)
- **Bad**, because merge logic is fragile — any new field requires merge rule updates
- **Bad**, because obscures data ownership in code rather than in contract

### Document separation

- **Good**, because strongest data ownership guarantee — physically separate tables
- **Bad**, because requires database migration, schema redesign, and changes to all consumers
- **Bad**, because join-at-read-time adds query complexity
- **Bad**, because highest implementation effort relative to the immediate problem

## More Information

- Origin: [NTK-10004 Solution Design](../phase-1-ai-tool-cost-comparison/workspace/work-items/tickets/_NTK-10004-guide-schedule-overwrite-bug/NTK-10004-solution-design.md)
- Service: [svc-scheduling-orchestrator](../services/svc-scheduling-orchestrator.md)
- Root cause analysis: [investigations.md](../phase-1-ai-tool-cost-comparison/workspace/work-items/tickets/_NTK-10004-guide-schedule-overwrite-bug/3.solution/c.current.state/investigations.md)
- Related: [ADR-011 Optimistic Locking](ADR-011-optimistic-locking-daily-schedule.md)
