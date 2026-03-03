# NTK-10004: Architecture Decisions

---

## ADR-NTK10004-001: PATCH Semantics for Schedule Updates

### Status

Accepted

### Date

2026-03-03

### Context and Problem Statement

The svc-scheduling-orchestrator uses PUT semantics (`scheduleRepository.save(incoming)`) to update guide schedules after optimization. This full entity replacement overwrites fields owned by svc-guide-management -- specifically `guideNotes` and `guidePreferences` -- because the orchestrator DTO does not include those fields. How should the orchestrator update schedules without destroying data it does not own?

### Decision Drivers

- Guide safety data (medical restrictions, certification notes) must not be silently removed
- The fix must be backward-compatible with existing schedule consumers
- The solution must establish a clear data ownership boundary between scheduling and guide-management domains
- Implementation should be achievable within 1-2 sprints

### Considered Options

1. **Switch to PATCH semantics** -- Update only orchestrator-owned fields, preserve all other fields
2. **Read-modify-write pattern** -- Read existing entity, merge incoming fields, write back
3. **Split the entity** -- Separate `daily_schedules` into orchestrator-owned and guide-owned tables

### Decision Outcome

**Chosen Option**: "Switch to PATCH semantics", because it directly addresses the root cause (full entity replacement), establishes a clear ownership boundary at the API level, and can be implemented within 1-2 sprints without schema migration.

#### Confirmation

- `SchedulingService.updateSchedule()` modified to update only scheduling-owned fields
- New `PATCH /api/v1/schedules/{id}` endpoint created with a `ScheduleUpdateRequest` DTO containing only orchestrator-owned fields
- Existing PUT endpoint deprecated or removed
- Integration tests verify that `guideNotes` and `guidePreferences` survive a schedule update

### Consequences

#### Positive

- Enrichment fields are never overwritten by the orchestrator
- Clear API contract defines which fields are mutable by the orchestrator
- Follows HTTP PATCH semantics correctly (partial update)

#### Negative

- Requires a new DTO class for the PATCH request body
- Existing PUT callers must migrate to PATCH (breaking change for internal consumers)

#### Neutral

- The read-modify-write pattern remains available as a fallback if PATCH is insufficient for complex merge scenarios

### Pros and Cons of the Options

#### Switch to PATCH semantics

- **Good**, because directly prevents overwriting non-owned fields
- **Good**, because aligns with HTTP standards (PUT = full replacement, PATCH = partial)
- **Good**, because new DTO explicitly defines the orchestrator ownership boundary
- **Neutral**, because requires migrating existing internal PUT callers

#### Read-modify-write pattern

- **Good**, because preserves all existing data by merging
- **Bad**, because introduces a race condition window between read and write
- **Bad**, because does not solve the concurrency problem (secondary root cause)
- **Bad**, because the orchestrator still sends a full entity, just with merged data

#### Split the entity

- **Good**, because enforces physical data ownership boundaries
- **Bad**, because requires database schema migration
- **Bad**, because requires join logic for reads
- **Bad**, because scope exceeds what is needed for the immediate fix

---

## ADR-NTK10004-002: Optimistic Locking on Daily Schedule Entity

### Status

Accepted

### Date

2026-03-03

### Context and Problem Statement

Concurrent optimization runs across regions can update the same guide schedule simultaneously. With no concurrency control, the last write wins, potentially overwriting a valid optimization result. Elastic logs confirm a 47ms race window between concurrent PUTs for guide G-4821. How should concurrent schedule modifications be handled?

### Decision Drivers

- Concurrent regional optimizations must not corrupt guide schedules
- The solution must detect conflicts rather than silently overwriting
- Integration with JPA/Hibernate is preferred for implementation simplicity
- The solution must not introduce significant latency to the optimization pipeline

### Considered Options

1. **JPA @Version optimistic locking** -- Add a version field to the entity; concurrent writes trigger `OptimisticLockException`
2. **Database-level pessimistic locking** -- Use `SELECT FOR UPDATE` during schedule updates
3. **Application-level distributed lock** -- Use Redis or similar for cross-instance locking

### Decision Outcome

**Chosen Option**: "JPA @Version optimistic locking", because it provides conflict detection with minimal implementation complexity, integrates natively with the existing JPA/Hibernate stack, and does not introduce external dependencies or additional latency.

#### Confirmation

- `DailySchedule` entity includes `@Version private Long version;` field
- `PATCH /api/v1/schedules/{id}` accepts an `If-Match` header containing the version
- `OptimisticLockException` returns HTTP 409 Conflict with retry guidance
- Integration tests verify that concurrent updates to the same schedule produce a conflict error

### Consequences

#### Positive

- Concurrent writes are detected and the second writer receives a clear conflict error
- Native JPA integration -- no external infrastructure required
- Conflict resolution can be handled by retry with backoff

#### Negative

- The failing writer must retry, adding latency to that optimization path
- Retries may fail repeatedly if contention is high (mitigated by exponential backoff)

#### Neutral

- The optimization pipeline needs a retry strategy for version conflicts

### More Information

- Elastic logs: 47ms concurrent write window for guide G-4821 (trace IDs abc-1001-def-2001 and abc-1001-def-2002)
- The `DailySchedule` entity currently has no `@Version` field (confirmed in source code review)
