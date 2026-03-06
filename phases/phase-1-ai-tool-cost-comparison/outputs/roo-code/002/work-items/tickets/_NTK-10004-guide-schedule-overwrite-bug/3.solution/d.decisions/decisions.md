# NTK-10004: Architecture Decisions

---

## ADR-NTK10004-001: PATCH Semantics with Data Ownership Boundaries

### Status

Accepted

### Date

2026-03-04

### Context and Problem Statement

The svc-scheduling-orchestrator overwrites guide enrichment data (notes, preferences, certifications, availability exceptions) when it updates schedules after optimization runs. The root cause is full entity replacement via PUT semantics on data the orchestrator does not own. How should the orchestrator update schedules without destroying data managed by svc-guide-management?

### Decision Drivers

- Guide safety is at risk: medical restrictions are silently removed
- Data integrity: production data corruption with no recovery mechanism
- Operational impact: incorrect guide assignments requiring manual intervention
- The fix must be backward-compatible with existing svc-guide-management consumers
- The fix must prevent both the PUT overwrite and concurrent write issues

### Considered Options

1. **PATCH semantics with field-level ownership** -- Orchestrator sends only scheduling-owned fields via PATCH
2. **Read-modify-write with merge** -- Orchestrator reads the full entity, merges its changes, then PUTs the merged result
3. **Table separation** -- Split `daily_schedules` into two tables with distinct ownership

### Decision Outcome

**Chosen Option**: "PATCH semantics with field-level ownership", because it directly addresses the root cause (writing fields the orchestrator does not own), is the simplest to implement given the PATCH endpoint already exists in svc-guide-management, and establishes a clear architectural pattern for data ownership.

#### Confirmation

- `SchedulingService.updateSchedule()` uses PATCH with a partial DTO containing only orchestrator-owned fields
- `ScheduleController.java` exposes a PATCH endpoint; the PUT endpoint is deprecated
- Integration tests verify that enrichment fields survive optimization cycles

### Consequences

#### Positive

- Enrichment fields (guideNotes, guidePreferences, certifications, availability exceptions) are never touched by the orchestrator
- Clear architectural boundary: each service only modifies fields it owns
- Minimal code change: replace `scheduleRepository.save(incoming)` with selective field updates
- PATCH endpoint in svc-guide-management already exists and is tested

#### Negative

- The orchestrator must be aware of which fields it owns (tight coupling to field list)
- If new fields are added to `DailySchedule`, developers must decide ownership at creation time

#### Neutral

- Requires updating the OpenAPI contract to document the PATCH endpoint

### Pros and Cons of the Options

#### PATCH semantics with field-level ownership

- **Good**, because directly prevents overwriting unowned fields
- **Good**, because svc-guide-management already has a PATCH endpoint
- **Good**, because minimal code change required in the orchestrator
- **Neutral**, because requires maintaining a list of orchestrator-owned fields

#### Read-modify-write with merge

- **Good**, because preserves all existing data by reading first
- **Bad**, because introduces a time-of-check to time-of-use (TOCTOU) race condition
- **Bad**, because doubles the number of API calls (GET then PUT) per update
- **Bad**, because the orchestrator still sends fields it does not own

#### Table separation

- **Good**, because provides the strongest data ownership boundary via physical separation
- **Bad**, because requires database migration, schema redesign, and changes to all consumers
- **Bad**, because significantly higher implementation effort and risk
- **Neutral**, because may be warranted as a future architectural improvement

---

## ADR-NTK10004-002: Optimistic Locking via Version Field

### Status

Accepted

### Date

2026-03-04

### Context and Problem Statement

Concurrent regional optimization runs can write to the same guide's schedule simultaneously. Elastic logs confirm a 47ms race window where two PUT requests for guide G-4821 overlapped. Without concurrency control, last-write-wins semantics cause silent data corruption. How should concurrent writes be detected and handled?

### Decision Drivers

- Concurrent optimization across regions is a normal operational pattern
- Race conditions cause silent data loss with no error feedback
- The solution must not serialize all optimization runs (unacceptable performance impact)
- Cross-region guides are the primary at-risk population

### Considered Options

1. **Optimistic locking with @Version** -- Add a JPA `@Version` field to `DailySchedule`
2. **Pessimistic locking** -- Lock the entity row during updates
3. **Event sourcing** -- Emit schedule change events and reconcile

### Decision Outcome

**Chosen Option**: "Optimistic locking with @Version", because it detects concurrent modifications at write time, fails fast with a clear exception, and has minimal performance overhead for the common case (no contention). This is the standard JPA pattern for concurrent write detection.

#### Confirmation

- `DailySchedule` entity has a `@Version` field
- Concurrent write attempts throw `OptimisticLockingFailureException`
- The orchestrator includes retry logic with back-off for version conflicts

### Consequences

#### Positive

- Concurrent overwrites are detected and fail with a clear exception instead of silently succeeding
- Standard JPA pattern with well-understood behavior
- Minimal performance overhead in the non-contention case

#### Negative

- Conflicting updates must be retried, adding complexity to the orchestrator
- Under high contention, retry storms are theoretically possible (mitigated by exponential back-off)

#### Neutral

- Client-facing API should expose the version via `ETag` / `If-Match` headers for future use

### More Information

- Elastic logs: trace IDs abc-1001-def-2001 and abc-1001-def-2002 show a 47ms concurrent write window for guide G-4821
- Ticket Comment 6 (Morgan Rivera): 14 instances of overlapping PUTs within 500ms windows over 30 days
