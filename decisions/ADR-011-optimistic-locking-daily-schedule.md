# ADR-011: Add Optimistic Locking to DailySchedule Entity

## Status

Proposed

## Date

2026-02-28

## Context and Problem Statement

Concurrent schedule updates (e.g., nightly batch optimization across multiple regions) can produce race conditions where two processes write to the same guide's schedule within milliseconds. With no version control, the last write silently wins, potentially discarding data from the first write even after PATCH semantics are adopted ([ADR-010](ADR-010-patch-semantics-schedule-updates.md)).

How should concurrent write conflicts be detected and handled?

## Decision Drivers

- Concurrent regional optimizations are a normal operational pattern
- Silent data loss is unacceptable, especially for safety-critical guide data
- JPA provides built-in optimistic locking via `@Version`
- The solution should integrate with the existing Spring Data JPA stack

## Considered Options

1. **JPA @Version optimistic locking** — Add a `@Version` field to `DailySchedule`; JPA throws `OptimisticLockException` on stale writes
2. **ETag-based HTTP concurrency** — Return `ETag` header on GET; require `If-Match` header on PUT/PATCH
3. **Pessimistic locking** — Use `SELECT ... FOR UPDATE` to lock rows during optimization

## Decision Outcome

**Chosen Option**: "JPA @Version optimistic locking", because it integrates natively with the existing JPA/Hibernate stack, requires minimal code changes, and detects conflicts without degrading read performance.

### Confirmation

- `@Version private Long version;` field added to `DailySchedule` entity
- Database migration adds `version` column with `DEFAULT 0`
- `OptimisticLockException` is caught in `SchedulingService` and triggers a retry with exponential backoff (max 3 retries)
- Integration tests simulate concurrent writes and verify conflict detection

## Consequences

### Positive

- Concurrent write conflicts are detected deterministically — no more silent last-write-wins
- Minimal code change: one annotation + one column + exception handler
- No performance impact on reads (version check happens only on write)
- Retry logic ensures transient conflicts auto-resolve without manual intervention

### Negative

- Requires a database migration to add the `version` column
- Retry logic adds complexity and must be tested for edge cases (e.g., all 3 retries fail)
- Does not prevent conflicts — only detects them after the fact

### Neutral

- ETag-based concurrency was considered as a complementary measure for external API consumers but is deferred to a future sprint

## More Information

- Origin: [NTK-10004 Solution Design](../phase-1-ai-tool-cost-comparison/workspace/work-items/tickets/_NTK-10004-guide-schedule-overwrite-bug/NTK-10004-solution-design.md)
- Service: [svc-scheduling-orchestrator](../services/svc-scheduling-orchestrator.md)
- Related: [ADR-010 PATCH Semantics](ADR-010-patch-semantics-schedule-updates.md)
