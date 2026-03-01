# Assumptions - NTK-10004: Guide Schedule Overwrite Bug

## Status Legend

- CONFIRMED: Validated through code review, log analysis, or reproduction
- INVESTIGATING: Evidence suggests this is true but not yet fully validated

---

## Assumption 1: Orchestrator Uses Full Replacement Semantics

**Status**: CONFIRMED

svc-scheduling-orchestrator calls `PUT /api/v1/guides/{guideId}/schedule` after each optimization cycle, replacing the entire schedule document. This was confirmed through source code review of the `GuideScheduleTransformer` class and corroborated by Elastic log analysis showing PUT requests with complete document payloads that lack manually-entered fields.

## Assumption 2: Manual Adjustments Share the Same Document

**Status**: CONFIRMED

svc-guide-management stores both optimized schedule data (trail assignments, shifts) and manual adjustments (availability exceptions, notes, group size overrides) in the same DynamoDB document under the `guide-schedules` table. There is no separation between orchestrator-owned fields and guide-owned fields at the storage level.

## Assumption 3: Concurrent Regional Optimization Creates Race Conditions

**Status**: INVESTIGATING

When multiple regions trigger optimization simultaneously (as happens during the nightly batch at 02:00 UTC), guides who are assigned to cross-region trails may have their schedule documents updated by multiple optimization processes. Elastic logs show 14 instances of overlapping PUTs within 500ms windows over 30 days, but it has not yet been confirmed whether these caused observable data corruption beyond the already-known overwrite issue.

## Assumption 4: No Revision or Concurrency Control Exists

**Status**: INVESTIGATING

Initial code review of svc-guide-management suggests no optimistic locking or conditional writes are implemented on the schedule document. The PUT endpoint does not check for `If-Match` headers or document revision fields. This needs validation through the full API specification and DynamoDB table configuration to confirm that conditional expressions are not applied at the data layer.
