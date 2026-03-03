# NTK-10004: Service Impact Assessments

---

## Impact 1: svc-scheduling-orchestrator (PRIMARY -- Code Change Required)

### Impact Level: HIGH

### Summary

The scheduling orchestrator is the source of the bug. Its `SchedulingService.updateSchedule()` method must be refactored from full entity replacement (PUT) to partial update (PATCH) semantics. A new PATCH endpoint, partial-update DTO, and optimistic locking must be added.

### Changes Required

1. **New DTO**: `PatchScheduleDto.java` containing only orchestrator-owned fields (guideId, tripId, startTime, endTime, participantCount, maxCapacity, status). Explicitly excludes `guideNotes` and `guidePreferences`.
2. **New service method**: `patchSchedule()` that reads the existing entity and updates only provided fields
3. **New PATCH endpoint**: `PATCH /api/v1/schedules/{id}` accepting `PatchScheduleDto`
4. **PUT deprecation**: Add `@Deprecated`, `Sunset` header, and structured logging to existing PUT
5. **@Version field**: Add JPA optimistic locking to `DailySchedule` entity
6. **Retry logic**: `@Retryable` on `patchSchedule()` for `OptimisticLockException` with exponential backoff

### Database Migration

```sql
ALTER TABLE daily_schedules ADD COLUMN version BIGINT DEFAULT 0 NOT NULL;
```

### Testing Requirements

- Unit tests: PATCH preserves guideNotes and guidePreferences; updates only provided fields
- Integration tests: concurrent PATCH triggers OptimisticLockException and retries
- Regression tests: existing GET endpoints return full entity including enrichment fields

---

## Impact 2: svc-guide-management (MINOR -- Monitoring Only)

### Impact Level: LOW

### Summary

No code changes required in svc-guide-management. However, monitoring should be added to detect when enrichment fields (`guideNotes`, `guidePreferences`) are set to null by external callers. This provides a safety net in case any undiscovered caller is also using PUT semantics.

### Changes Required

- Add application-level logging when `guideNotes` or `guidePreferences` transition from non-null to null
- Add metric: `guide.enrichment.nullified.count`
- Add alert: trigger when metric exceeds threshold (>0 per hour)

---

## Impact 3: API Gateway and OpenAPI Contract (MEDIUM -- Contract Update)

### Impact Level: MEDIUM

### Summary

The `PUT /api/v1/schedules/{id}` endpoint is not documented in the `svc-scheduling-orchestrator.yaml` OpenAPI specification. The new `PATCH /api/v1/schedules/{id}` endpoint must be added to the contract, and the PUT endpoint should be documented as deprecated.

### Changes Required

- Add `PATCH /schedules/{id}` to `svc-scheduling-orchestrator.yaml` with `PatchScheduleDto` schema
- Add `PUT /schedules/{id}` as deprecated with `x-sunset-date: 2026-06-01` extension
- Update API gateway routing if applicable
