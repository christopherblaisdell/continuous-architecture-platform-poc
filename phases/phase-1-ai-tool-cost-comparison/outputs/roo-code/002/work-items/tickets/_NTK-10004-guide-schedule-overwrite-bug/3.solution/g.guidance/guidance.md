# NTK-10004: Implementation Guidance

## Phase 1: Immediate Fix (Sprint 19/20)

### 1. Switch Orchestrator from PUT to PATCH

Modify `SchedulingService.updateSchedule()` to update only scheduling-owned fields:

```java
@Transactional
public DailySchedule updateSchedule(UUID id, ScheduleUpdateDto update) {
    DailySchedule existing = scheduleRepository.findById(id)
            .orElseThrow(() -> new ScheduleNotFoundException(id));
    
    // Only update orchestrator-owned fields
    if (update.getGuideId() != null) existing.setGuideId(update.getGuideId());
    if (update.getTripId() != null) existing.setTripId(update.getTripId());
    if (update.getStartTime() != null) existing.setStartTime(update.getStartTime());
    if (update.getEndTime() != null) existing.setEndTime(update.getEndTime());
    if (update.getStatus() != null) existing.setStatus(update.getStatus());
    
    // NEVER touch guideNotes, guidePreferences - those are owned by svc-guide-management
    existing.setLastModifiedAt(LocalDateTime.now());
    existing.setLastModifiedBy("scheduling-orchestrator");
    
    return scheduleRepository.save(existing);
}
```

### 2. Create Partial Update DTO

Create `ScheduleUpdateDto` containing ONLY orchestrator-owned fields:

```java
public class ScheduleUpdateDto {
    private UUID guideId;
    private UUID tripId;
    private LocalTime startTime;
    private LocalTime endTime;
    private DailySchedule.ScheduleStatus status;
    // NO guideNotes, NO guidePreferences
}
```

### 3. Add PATCH Endpoint

Add to `ScheduleController.java`:

```java
@PatchMapping("/{id}")
public DailySchedule patchSchedule(@PathVariable UUID id,
                                    @Valid @RequestBody ScheduleUpdateDto update) {
    return schedulingService.updateSchedule(id, update);
}
```

Deprecate the existing PUT endpoint with `@Deprecated` annotation and a response header warning consumers.

### 4. Add Optimistic Locking

Add to `DailySchedule.java`:

```java
@Version
private Long version;
```

This will cause concurrent writes to throw `OptimisticLockingFailureException`. Add retry logic in the orchestrator:

```java
@Retryable(value = OptimisticLockingFailureException.class, 
           maxAttempts = 3, 
           backoff = @Backoff(delay = 100, multiplier = 2))
public DailySchedule updateScheduleWithRetry(UUID id, ScheduleUpdateDto update) {
    return updateSchedule(id, update);
}
```

## Phase 2: Architectural Improvement (Sprint 21+)

### 5. Define Data Ownership Contracts

Document field ownership in the OpenAPI spec and entity annotations:

| Field | Owner | Can Be Set By |
|-------|-------|---------------|
| guideId, tripId, startTime, endTime, status | svc-scheduling-orchestrator | Orchestrator PATCH |
| guideNotes, guidePreferences | svc-guide-management | Guide Portal, Guide API |
| lastModifiedAt, lastModifiedBy | System | Either service |
| version | System | JPA managed |

### 6. Add PATCH to OpenAPI Contract

Document the new PATCH endpoint in `svc-scheduling-orchestrator.yaml`. Deprecate the undocumented PUT endpoint.

### 7. Add Data Loss Detection

Add application-level monitoring:

```java
@EventListener
public void onScheduleUpdate(ScheduleUpdateEvent event) {
    if (event.getPreviousGuideNotes() != null && event.getCurrentGuideNotes() == null) {
        log.warn("ALERT: guideNotes nullified for schedule {}", event.getScheduleId());
        metrics.counter("schedule.enrichment.nullified", "field", "guideNotes").increment();
    }
}
```

## Testing Guidance

| Test Case | Expected Result |
|-----------|----------------|
| PATCH with scheduling fields only | Enrichment fields preserved |
| Concurrent PATCH from two regions | One succeeds, other gets OptimisticLockingFailureException |
| Retry after version conflict | Second attempt succeeds with updated version |
| PUT endpoint (deprecated) | Returns 200 with deprecation warning header |
| PATCH with enrichment fields | Fields ignored or rejected (400) |

## Deployment Sequence

1. Add `@Version` field with database migration (add `version` column, default 0)
2. Deploy PATCH endpoint alongside existing PUT
3. Update orchestrator to call PATCH instead of PUT
4. Monitor for version conflicts and enrichment nullification alerts
5. After validation period, deprecate PUT endpoint with sunset header
