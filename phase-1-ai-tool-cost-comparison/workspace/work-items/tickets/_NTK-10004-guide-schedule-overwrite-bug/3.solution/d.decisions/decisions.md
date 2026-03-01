# NTK-10004: Architecture Decisions

---

## ADR-NTK10004-001: Switch from PUT to PATCH Semantics for Schedule Updates

### Status

Proposed

### Date

2026-02-28

### Context and Problem Statement

The svc-scheduling-orchestrator uses `PUT /api/v1/schedules/{id}` to persist optimized schedule data. This replaces the entire `DailySchedule` entity, including fields owned by svc-guide-management (guideNotes, guidePreferences). This full-replacement behavior silently destroys guide-entered data on every optimization cycle, creating safety risks (lost medical restrictions), operational disruption (15-20 incorrect guide removals per day), and guide frustration.

How should the scheduling orchestrator persist its optimization results without overwriting data it does not own?

### Decision Drivers

- Guide safety: medical restrictions and certification notes must never be silently removed
- Data ownership: each service should only modify fields it is responsible for
- Minimal disruption: the fix should not require changes to svc-guide-management or the database schema
- Backward compatibility: existing API clients should not break

### Considered Options

1. **PATCH semantics** — Add a PATCH endpoint that accepts only orchestrator-owned fields; use a partial-update DTO
2. **Read-merge-write** — Before saving, read the existing entity and merge incoming fields with preserved fields
3. **Document separation** — Split `daily_schedules` into two tables with different owners, joined at read time

### Decision Outcome

**Chosen Option**: "PATCH semantics", because it establishes a clear data ownership boundary at the API level with minimal implementation scope and no schema changes.

#### Confirmation

- New `PatchScheduleDto` contains only orchestrator-owned fields
- `PATCH /api/v1/schedules/{id}` endpoint added to ScheduleController
- Existing PUT endpoint deprecated with sunset header
- Integration tests verify guideNotes/guidePreferences survive a PATCH call

### Consequences

#### Positive

- Guide enrichment data is structurally preserved — the orchestrator physically cannot overwrite fields not in the DTO
- Clear API contract makes data ownership boundaries explicit
- No database migration or schema change required
- Existing GET endpoints continue to return the full entity unchanged

#### Negative

- Requires a new DTO class (`PatchScheduleDto`) and endpoint, adding code surface area
- PUT endpoint must be deprecated and eventually removed, requiring migration of any other callers
- Does not address the secondary concurrency issue (see ADR-NTK10004-002)

#### Neutral

- Read-merge-write was rejected because it adds latency (extra SELECT before UPDATE) and still allows accidental overwrites if the merge logic is incorrect

### Pros and Cons of the Options

#### PATCH semantics

- **Good**, because structurally prevents overwriting non-owned fields
- **Good**, because minimal implementation scope (new DTO + endpoint)
- **Good**, because follows REST best practices for partial updates
- **Neutral**, because requires clients to switch from PUT to PATCH
- **Bad**, because does not solve concurrency (separate ADR)

#### Read-merge-write

- **Good**, because no new endpoint needed — existing PUT becomes merge-aware
- **Bad**, because adds latency (extra SELECT per update)
- **Bad**, because merge logic is fragile — any new field requires merge rule updates
- **Bad**, because obscures data ownership in code rather than in contract

#### Document separation

- **Good**, because strongest data ownership guarantee — physically separate tables
- **Bad**, because requires database migration, schema redesign, and changes to all consumers
- **Bad**, because join-at-read-time adds query complexity
- **Bad**, because highest implementation effort relative to the immediate problem

### More Information

- Root cause analysis: `3.solution/c.current.state/investigations.md`, Section 5
- Source code: `SchedulingService.java`, `updateSchedule()` method
- Elastic evidence: 4 ERROR logs, 2 WARN logs confirming data loss pattern

---

## ADR-NTK10004-002: Add Optimistic Locking to DailySchedule Entity

### Status

Proposed

### Date

2026-02-28

### Context and Problem Statement

Concurrent schedule updates (e.g., nightly batch optimization across multiple regions) can produce race conditions where two processes write to the same guide's schedule within milliseconds. Elastic logs confirm a 47ms race window for guide G-4821. With no version control, the last write silently wins, potentially discarding data from the first write even after PATCH semantics are adopted (ADR-NTK10004-001).

How should concurrent write conflicts be detected and handled?

### Decision Drivers

- Concurrent regional optimizations are a normal operational pattern
- Silent data loss is unacceptable, especially for safety-critical guide data
- JPA provides built-in optimistic locking via `@Version`
- The solution should integrate with the existing Spring Data JPA stack

### Considered Options

1. **JPA @Version optimistic locking** — Add a `@Version` field to `DailySchedule`; JPA throws `OptimisticLockException` on stale writes
2. **ETag-based HTTP concurrency** — Return `ETag` header on GET; require `If-Match` header on PUT/PATCH
3. **Pessimistic locking** — Use `SELECT ... FOR UPDATE` to lock rows during optimization

### Decision Outcome

**Chosen Option**: "JPA @Version optimistic locking", because it integrates natively with the existing JPA/Hibernate stack, requires minimal code changes, and detects conflicts without degrading read performance.

#### Confirmation

- `@Version private Long version;` field added to `DailySchedule` entity
- Database migration adds `version` column with `DEFAULT 0`
- `OptimisticLockException` is caught in `SchedulingService` and triggers a retry with exponential backoff (max 3 retries)
- Integration tests simulate concurrent writes and verify conflict detection

### Consequences

#### Positive

- Concurrent write conflicts are detected deterministically — no more silent last-write-wins
- Minimal code change: one annotation + one column + exception handler
- No performance impact on reads (version check happens only on write)
- Retry logic ensures transient conflicts auto-resolve without manual intervention

#### Negative

- Requires a database migration to add the `version` column
- Retry logic adds complexity and must be tested for edge cases (e.g., all 3 retries fail)
- Does not prevent conflicts — only detects them after the fact

#### Neutral

- ETag-based concurrency was considered as a complementary measure for external API consumers but is deferred to a future sprint

### More Information

- Elastic log evidence: Guide G-4821, two PUTs within 47ms (trace IDs abc-1001-def-2001, abc-1001-def-2002)
- JPA optimistic locking reference: Hibernate ORM documentation, Section 5.5
