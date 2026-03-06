# NTK-10004: Architecture Decisions

---

## ADR-NTK10004-001: PATCH Semantics for Schedule Updates

### Status

Proposed

### Date

2026-03-04

### Context and Problem Statement

The svc-scheduling-orchestrator uses PUT semantics to update guide schedules, replacing the entire entity including fields owned by svc-guide-management. This causes silent data loss of guide enrichment fields (notes, preferences, certifications, availability exceptions). The update mechanism must be changed to preserve fields the orchestrator does not own.

### Decision Drivers

- Guide safety data (medical restrictions, certification records) must not be silently discarded
- The fix must be backward-compatible with existing API consumers
- svc-guide-management and svc-scheduling-orchestrator have distinct data ownership scopes on the same entity
- The solution must be implementable within 1-2 sprints given the severity of the bug

### Considered Options

1. **Switch to PATCH semantics** — Modify the orchestrator to use HTTP PATCH, updating only fields it owns
2. **Read-merge-write pattern** — Read the current entity, merge orchestrator fields, then PUT the complete entity
3. **Split the entity** — Separate scheduling fields and enrichment fields into distinct database tables

### Decision Outcome

**Chosen Option**: "Switch to PATCH semantics", because it directly addresses the data ownership violation, is the simplest to implement, and does not require database schema changes. The read-merge-write pattern is rejected because it introduces a race condition window between read and write.

#### Confirmation

- The orchestrator's `updateSchedule()` method updates only scheduling-owned fields via field-level setters on the existing entity
- A new `PATCH /api/v1/schedules/{id}` endpoint is added to the controller
- Integration tests verify that `guideNotes` and `guidePreferences` survive an optimization cycle

### Consequences

#### Positive

- Guide enrichment data is preserved during optimization cycles
- Clear data ownership boundary: orchestrator updates only what it owns
- PATCH endpoint follows RESTful best practices for partial updates
- No database schema migration required

#### Negative

- The orchestrator must explicitly list which fields it is permitted to update, creating maintenance overhead when new scheduling fields are added
- Existing internal consumers of the PUT endpoint must be migrated to PATCH

#### Neutral

- The PUT endpoint should be deprecated and eventually removed to prevent future misuse

### Pros and Cons of the Options

#### Switch to PATCH semantics

- **Good**, because it directly enforces data ownership boundaries
- **Good**, because it is the simplest implementation (field-level update on existing entity)
- **Good**, because it does not require database changes
- **Bad**, because it requires updating all callers of the PUT endpoint

#### Read-merge-write pattern

- **Good**, because it preserves all existing data through explicit merging
- **Bad**, because it introduces a TOCTOU (time-of-check-to-time-of-use) race condition
- **Bad**, because it is fragile — any new field must be added to the merge logic

#### Split the entity

- **Good**, because it enforces ownership at the database level
- **Good**, because each service has its own table with full control
- **Bad**, because it requires a database migration and data transformation
- **Bad**, because read queries must join two tables, adding complexity
- **Bad**, because implementation scope exceeds the sprint timeline for a high-priority bug fix

### More Information

- Elastic log evidence: 4 ERROR events showing data loss for guides G-4821, G-5190, G-3302
- Source code: `SchedulingService.java` lines 54-64 (full entity replacement)
- Related: ADR-010 (global decision on PATCH semantics for schedule updates)

---

## ADR-NTK10004-002: Optimistic Locking on DailySchedule Entity

### Status

Proposed

### Date

2026-03-04

### Context and Problem Statement

Concurrent schedule optimization runs (nightly batch across multiple regions) can overwrite each other's results for guides assigned to cross-region trails. The `DailySchedule` entity has no concurrency control — the last writer wins silently. Elastic logs confirm a 47ms race window between concurrent PUTs for the same guide.

### Decision Drivers

- Concurrent writes have been observed in production with 14 instances in 30 days
- Guide schedules are a safety-critical resource; silent overwrites create risk
- The solution must not significantly increase write latency for the optimization pipeline
- The solution must be compatible with the PATCH semantics change in ADR-NTK10004-001

### Considered Options

1. **JPA @Version optimistic locking** — Add a version field to the entity; reject writes with stale versions
2. **Database-level pessimistic locking** — Use SELECT FOR UPDATE to serialize writes
3. **Application-level distributed lock** — Use Redis or similar to acquire a per-guide lock before writing

### Decision Outcome

**Chosen Option**: "JPA @Version optimistic locking", because it provides conflict detection without serializing writes, has minimal performance impact, and integrates naturally with the existing JPA/Spring Data stack.

#### Confirmation

- `DailySchedule` entity has a `@Version` annotated field
- Concurrent writes return HTTP 409 Conflict with a clear error message
- The optimization pipeline handles 409 responses with a retry-and-merge strategy

### Consequences

#### Positive

- Concurrent writes are detected and rejected rather than silently lost
- No additional infrastructure required (no Redis, no external lock manager)
- Standard JPA mechanism understood by all Spring developers on the team

#### Negative

- Concurrent writes now fail instead of silently succeeding — the optimization pipeline must handle 409 responses
- Adds a retry path to the optimization code, increasing complexity slightly

#### Neutral

- The version field adds one column to the `daily_schedules` table (integer, auto-incremented by JPA)

### Pros and Cons of the Options

#### JPA @Version optimistic locking

- **Good**, because zero additional infrastructure
- **Good**, because integrates with existing JPA stack
- **Good**, because conflict detection, not prevention — preserves concurrent read performance
- **Bad**, because callers must handle version conflicts (409 responses)

#### Database-level pessimistic locking

- **Good**, because prevents conflicts entirely (serialized writes)
- **Bad**, because increases write latency due to lock contention
- **Bad**, because can cause deadlocks in cross-region optimization scenarios

#### Application-level distributed lock

- **Good**, because provides fine-grained locking per guide
- **Bad**, because introduces Redis or similar infrastructure dependency
- **Bad**, because adds operational complexity (lock expiry, stale locks)

### More Information

- Elastic log evidence: 47ms race window for guide G-4821 (traces abc-1001-def-2001, abc-1001-def-2002)
- Related: ADR-011 (global decision on optimistic locking for daily schedules)
