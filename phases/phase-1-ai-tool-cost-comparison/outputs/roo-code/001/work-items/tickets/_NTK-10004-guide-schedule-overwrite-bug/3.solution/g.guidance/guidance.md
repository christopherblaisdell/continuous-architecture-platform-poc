# NTK-10004: Implementation Guidance

## 1. Immediate Fix: Switch to PATCH Semantics (Sprint 19/20)

### 1.1 Create ScheduleUpdateRequest DTO

Create a new DTO that contains ONLY the fields owned by the scheduling orchestrator:

```java
public class ScheduleUpdateRequest {
    private UUID guideId;
    private UUID tripId;
    private LocalTime startTime;
    private LocalTime endTime;
    private int participantCount;
    private int maxCapacity;
    private DailySchedule.ScheduleStatus status;
}
```

IMPORTANT: This DTO intentionally EXCLUDES `guideNotes` and `guidePreferences`. Those fields are owned by svc-guide-management and must not be mutable through the scheduling orchestrator.

### 1.2 Modify SchedulingService.updateSchedule()

Replace the current full-entity replacement with a selective field update:

```java
@Transactional
public DailySchedule updateSchedule(UUID id, ScheduleUpdateRequest request) {
    DailySchedule existing = scheduleRepository.findById(id)
        .orElseThrow(() -> new RuntimeException("Schedule not found: " + id));

    // Update ONLY orchestrator-owned fields
    if (request.getGuideId() != null) existing.setGuideId(request.getGuideId());
    if (request.getTripId() != null) existing.setTripId(request.getTripId());
    if (request.getStartTime() != null) existing.setStartTime(request.getStartTime());
    if (request.getEndTime() != null) existing.setEndTime(request.getEndTime());
    if (request.getParticipantCount() > 0) existing.setParticipantCount(request.getParticipantCount());
    if (request.getMaxCapacity() > 0) existing.setMaxCapacity(request.getMaxCapacity());
    if (request.getStatus() != null) existing.setStatus(request.getStatus());

    existing.setLastModifiedAt(LocalDateTime.now());
    existing.setLastModifiedBy("scheduling-orchestrator");

    // guideNotes and guidePreferences are NEVER touched
    return scheduleRepository.save(existing);
}
```

### 1.3 Add PATCH Endpoint to ScheduleController

```java
@PatchMapping("/{id}")
public DailySchedule patchSchedule(@PathVariable UUID id,
                                   @Valid @RequestBody ScheduleUpdateRequest request) {
    return schedulingService.updateSchedule(id, request);
}
```

### 1.4 Deprecate or Remove PUT Endpoint

Mark the existing `PUT /{id}` endpoint as deprecated. In a follow-up sprint, remove it entirely to prevent regression.

## 2. Add Optimistic Locking (Sprint 19/20)

### 2.1 Add Version Field to DailySchedule Entity

```java
@Version
private Long version;
```

This single annotation enables JPA optimistic locking. Hibernate will automatically increment the version on each update and throw `OptimisticLockException` if a concurrent update is detected.

### 2.2 Database Migration

```sql
ALTER TABLE daily_schedules ADD COLUMN version BIGINT DEFAULT 0;
```

### 2.3 Handle Conflict Responses

Add exception handling in the controller for `OptimisticLockException`:

```java
@ExceptionHandler(OptimisticLockException.class)
@ResponseStatus(HttpStatus.CONFLICT)
public ErrorResponse handleOptimisticLock(OptimisticLockException ex) {
    return new ErrorResponse("SCHEDULE_CONFLICT",
        "Schedule was modified by another process. Read the latest version and retry.");
}
```

### 2.4 Retry Strategy

The optimization pipeline should implement exponential backoff retry when receiving a 409 Conflict:

- Max retries: 3
- Initial delay: 100ms
- Backoff multiplier: 2x
- On final failure: Log error and alert operations team

## 3. Document the Endpoint in OpenAPI (Sprint 20)

The `PATCH /api/v1/schedules/{id}` endpoint must be added to the `svc-scheduling-orchestrator.yaml` OpenAPI specification. The undocumented PUT endpoint should be removed from the spec or marked as deprecated.

## 4. Monitoring and Alerting

### Immediate

- Add alert on `guideNotes`/`guidePreferences` nullification: application-level check that logs a WARNING when enrichment fields transition from non-null to null
- Track concurrent write frequency: monitor for overlapping writes within configurable time windows

### Post-Fix

- Monitor `OptimisticLockException` count to track conflict frequency
- Alert if conflict rate exceeds a configurable threshold (indicates high contention)

## 5. Testing Guidance

| Test Case | Expected Result |
|-----------|----------------|
| PATCH schedule with guideId and tripId | Fields updated; guideNotes and guidePreferences unchanged |
| PATCH schedule while guideNotes has content | guideNotes preserved after patch |
| Concurrent PATCH on same schedule | Second request receives HTTP 409 Conflict |
| Retry after 409 with fresh version | Update succeeds |
| PUT endpoint (if still exposed) | Returns HTTP 405 or deprecated warning |
