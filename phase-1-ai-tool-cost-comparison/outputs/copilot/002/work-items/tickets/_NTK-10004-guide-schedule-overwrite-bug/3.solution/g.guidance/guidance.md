# NTK-10004: Implementation Guidance

## 1 Immediate Fix: Switch to PATCH Semantics

### 1.1 Modify SchedulingService.updateSchedule()

Replace the full entity replacement with field-level updates on the existing entity:

```java
@Transactional
public DailySchedule updateSchedule(UUID id, DailyScheduleUpdateRequest updateRequest) {
    DailySchedule existing = scheduleRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("Schedule not found: " + id));

    // Update ONLY scheduling-owned fields
    if (updateRequest.getGuideId() != null) {
        existing.setGuideId(updateRequest.getGuideId());
    }
    if (updateRequest.getTripId() != null) {
        existing.setTripId(updateRequest.getTripId());
    }
    if (updateRequest.getStartTime() != null) {
        existing.setStartTime(updateRequest.getStartTime());
    }
    if (updateRequest.getEndTime() != null) {
        existing.setEndTime(updateRequest.getEndTime());
    }
    if (updateRequest.getStatus() != null) {
        existing.setStatus(updateRequest.getStatus());
    }

    // NEVER touch guideNotes or guidePreferences - those are owned by svc-guide-management

    existing.setLastModifiedAt(LocalDateTime.now());
    existing.setLastModifiedBy("scheduling-orchestrator");
    return scheduleRepository.save(existing);
}
```

### 1.2 Create DailyScheduleUpdateRequest DTO

Create a new DTO that contains ONLY scheduling-owned fields:

```java
public class DailyScheduleUpdateRequest {
    private UUID guideId;
    private UUID tripId;
    private LocalTime startTime;
    private LocalTime endTime;
    private DailySchedule.ScheduleStatus status;
    // No guideNotes, no guidePreferences - enforced by DTO boundary
}
```

### 1.3 Add PATCH Endpoint to ScheduleController

```java
@PatchMapping("/{id}")
public DailySchedule patchSchedule(@PathVariable UUID id,
                                   @Valid @RequestBody DailyScheduleUpdateRequest updateRequest) {
    return schedulingService.updateSchedule(id, updateRequest);
}
```

### 1.4 Deprecate PUT Endpoint

Add `@Deprecated` annotation and a response header to warn callers:

```java
@Deprecated
@PutMapping("/{id}")
public DailySchedule updateScheduleLegacy(@PathVariable UUID id,
                                          @Valid @RequestBody DailySchedule schedule) {
    log.warn("Deprecated PUT endpoint called for schedule {}. Migrate to PATCH.", id);
    // Internally delegate to the safe PATCH logic
    return schedulingService.updateSchedule(id, mapToPatchRequest(schedule));
}
```

## 2 Add Optimistic Locking

### 2.1 Add @Version to DailySchedule

```java
@Version
@Column(name = "version")
private Long version;
```

### 2.2 Database Migration

```sql
ALTER TABLE daily_schedules ADD COLUMN version BIGINT NOT NULL DEFAULT 0;
```

### 2.3 Handle Version Conflicts

When JPA detects a version mismatch, it throws `OptimisticLockException`. Handle this in the controller:

```java
@ExceptionHandler(OptimisticLockException.class)
@ResponseStatus(HttpStatus.CONFLICT)
public ErrorResponse handleOptimisticLock(OptimisticLockException ex) {
    return new ErrorResponse("SCHEDULE_CONFLICT",
        "Schedule was modified by another process. Retry with the current version.");
}
```

### 2.4 Optimization Pipeline Retry Logic

The optimization pipeline should handle 409 Conflict responses with a retry strategy:

1. Read the current schedule (with updated version)
2. Re-apply only the scheduling-owned field changes
3. Retry the PATCH request
4. Maximum 3 retries with exponential backoff

## 3 Update OpenAPI Specification

Add the PATCH endpoint to `svc-scheduling-orchestrator.yaml`:

```yaml
/api/v1/schedules/{id}:
  patch:
    operationId: patchSchedule
    summary: Partially update a daily schedule
    description: |
      Updates only scheduling-owned fields on a daily schedule.
      Guide enrichment fields (guideNotes, guidePreferences) are preserved.
      Requires If-Match header with the current entity version for optimistic locking.
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: string
          format: uuid
      - name: If-Match
        in: header
        required: true
        schema:
          type: string
        description: Entity version for optimistic concurrency control
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/DailyScheduleUpdateRequest'
    responses:
      '200':
        description: Schedule updated successfully
      '409':
        description: Version conflict - schedule was modified concurrently
      '404':
        description: Schedule not found
```

## 4 Testing

- **Unit test**: Verify that PATCH preserves `guideNotes` and `guidePreferences` when updating scheduling fields
- **Unit test**: Verify that concurrent PATCH requests with stale versions return 409
- **Integration test**: Simulate the full optimization cycle and verify enrichment data survives
- **Integration test**: Simulate concurrent regional optimizations and verify conflict detection
- **Regression test**: Verify the deprecated PUT endpoint still functions but delegates to PATCH logic

## 5 Monitoring

- Add a metric `schedule.enrichment.preserved` to track successful preservation during updates
- Alert on `guideNotes` or `guidePreferences` transitioning from non-null to null (should never happen after fix)
- Track `schedule.version.conflict.count` to monitor concurrency issues
