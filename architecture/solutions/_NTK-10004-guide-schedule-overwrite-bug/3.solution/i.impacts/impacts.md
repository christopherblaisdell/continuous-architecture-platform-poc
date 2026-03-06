# NTK-10004: Service Impact Assessments

---

## Impact 1: svc-scheduling-orchestrator (PRIMARY — Code Change Required)

### Impact Level: HIGH

### Summary

The scheduling orchestrator is the source of the bug. Its `SchedulingService.updateSchedule()` method must be refactored from full entity replacement (PUT) to partial update (PATCH) semantics. A new PATCH endpoint, partial-update DTO, and optimistic locking must be added.

### Changes Required

#### 1. New DTO: PatchScheduleDto

Create `PatchScheduleDto.java` containing only orchestrator-owned fields:
- `guideId` (UUID)
- `tripId` (UUID)
- `startTime` (LocalTime)
- `endTime` (LocalTime)
- `participantCount` (int)
- `maxCapacity` (int)
- `status` (ScheduleStatus)

Explicitly **excluded** (guide-management-owned):
- `guideNotes`
- `guidePreferences`

#### 2. SchedulingService.java — New patchSchedule() Method

```java
@Transactional
public DailySchedule patchSchedule(UUID id, PatchScheduleDto patch) {
    DailySchedule existing = scheduleRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("Schedule not found: " + id));
    
    if (patch.getGuideId() != null) existing.setGuideId(patch.getGuideId());
    if (patch.getTripId() != null) existing.setTripId(patch.getTripId());
    if (patch.getStartTime() != null) existing.setStartTime(patch.getStartTime());
    if (patch.getEndTime() != null) existing.setEndTime(patch.getEndTime());
    if (patch.getParticipantCount() > 0) existing.setParticipantCount(patch.getParticipantCount());
    if (patch.getMaxCapacity() > 0) existing.setMaxCapacity(patch.getMaxCapacity());
    if (patch.getStatus() != null) existing.setStatus(patch.getStatus());
    
    existing.setLastModifiedAt(LocalDateTime.now());
    existing.setLastModifiedBy("scheduling-orchestrator");
    return scheduleRepository.save(existing);
}
```

#### 3. ScheduleController.java — New PATCH Endpoint

```java
@PatchMapping("/{id}")
public DailySchedule patchSchedule(@PathVariable UUID id,
                                    @Valid @RequestBody PatchScheduleDto patch) {
    return schedulingService.patchSchedule(id, patch);
}
```

#### 4. DailySchedule.java — Add @Version

```java
@Version
private Long version;
```

#### 5. Deprecate PUT Endpoint

Add `@Deprecated` annotation and `Sunset` response header to the existing PUT endpoint. Log a WARNING when PUT is used to track migration.

### Testing Requirements

- Unit test: `patchSchedule()` preserves `guideNotes` and `guidePreferences`
- Unit test: `patchSchedule()` updates only provided fields
- Integration test: concurrent PATCH throws `OptimisticLockException` and retries
- Regression test: existing GET endpoints return full entity including enrichment fields

### Database Migration

```sql
ALTER TABLE daily_schedules ADD COLUMN version BIGINT DEFAULT 0 NOT NULL;
```

---

## Impact 2: svc-guide-management (MINOR — Monitoring Only)

### Impact Level: LOW

### Summary

No code changes required in svc-guide-management. However, monitoring should be added to detect when enrichment fields (`guideNotes`, `guidePreferences`) are set to null by external callers. This provides a safety net in case any undiscovered caller is also using PUT semantics.

### Changes Required

- Add application-level logging when `guideNotes` or `guidePreferences` transition from non-null to null
- Add metric: `guide.enrichment.nullified.count`
- Add alert: trigger when metric exceeds threshold (>0 per hour)

---

## Impact 3: API Gateway / OpenAPI Contract (MEDIUM — Contract Update)

### Impact Level: MEDIUM

### Summary

The `PUT /api/v1/schedules/{id}` endpoint is not documented in the `svc-scheduling-orchestrator.yaml` OpenAPI specification. The new `PATCH /api/v1/schedules/{id}` endpoint must be added to the contract, and the PUT endpoint should be documented as deprecated.

### Changes Required

- Add `PATCH /schedules/{id}` to `svc-scheduling-orchestrator.yaml` with `PatchScheduleDto` schema
- Add `PUT /schedules/{id}` as deprecated with `x-sunset-date` extension
- Update API gateway routing if applicable
