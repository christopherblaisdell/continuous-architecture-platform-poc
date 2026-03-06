# NTK-10004: Implementation Guidance

---

## Phase 1: Immediate Fix (Sprint 19 — Target: 1 week)

### Step 1: Create PatchScheduleDto

```java
package com.novatrek.scheduling.dto;

import com.novatrek.scheduling.model.DailySchedule;
import lombok.Data;
import java.time.LocalTime;
import java.util.UUID;

@Data
public class PatchScheduleDto {
    private UUID guideId;
    private UUID tripId;
    private LocalTime startTime;
    private LocalTime endTime;
    private int participantCount;
    private int maxCapacity;
    private DailySchedule.ScheduleStatus status;
    
    // NOTE: guideNotes and guidePreferences are intentionally EXCLUDED.
    // These fields are owned by svc-guide-management and must never
    // be modified by the scheduling orchestrator.
}
```

### Step 2: Add patchSchedule() to SchedulingService

```java
@Transactional
public DailySchedule patchSchedule(UUID id, PatchScheduleDto patch) {
    DailySchedule existing = scheduleRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("Schedule not found: " + id));
    
    // Only update orchestrator-owned fields
    if (patch.getGuideId() != null) existing.setGuideId(patch.getGuideId());
    if (patch.getTripId() != null) existing.setTripId(patch.getTripId());
    if (patch.getStartTime() != null) existing.setStartTime(patch.getStartTime());
    if (patch.getEndTime() != null) existing.setEndTime(patch.getEndTime());
    if (patch.getParticipantCount() > 0) existing.setParticipantCount(patch.getParticipantCount());
    if (patch.getMaxCapacity() > 0) existing.setMaxCapacity(patch.getMaxCapacity());
    if (patch.getStatus() != null) existing.setStatus(patch.getStatus());
    
    existing.setLastModifiedAt(LocalDateTime.now());
    existing.setLastModifiedBy("scheduling-orchestrator");
    
    // guideNotes and guidePreferences are NOT in PatchScheduleDto,
    // so they remain unchanged on the existing entity
    return scheduleRepository.save(existing);
}
```

### Step 3: Add PATCH Endpoint to ScheduleController

```java
@PatchMapping("/{id}")
public DailySchedule patchSchedule(@PathVariable UUID id,
                                    @Valid @RequestBody PatchScheduleDto patch) {
    return schedulingService.patchSchedule(id, patch);
}
```

### Step 4: Deprecate PUT Endpoint

```java
@Deprecated(since = "3.1.0", forRemoval = true)
@PutMapping("/{id}")
public ResponseEntity<DailySchedule> updateSchedule(@PathVariable UUID id,
                                                      @Valid @RequestBody DailySchedule schedule) {
    log.warn("DEPRECATED: PUT /schedules/{} called. Migrate to PATCH. Caller: {}",
             id, SecurityContextHolder.getContext().getAuthentication().getName());
    DailySchedule result = schedulingService.updateSchedule(id, schedule);
    return ResponseEntity.ok()
            .header("Sunset", "2026-06-01")
            .header("Deprecation", "true")
            .body(result);
}
```

---

## Phase 2: Concurrency Control (Sprint 20 — Target: 1 week)

### Step 5: Add @Version to DailySchedule

```java
@Version
private Long version;
```

### Step 6: Database Migration

```sql
-- V3.1.0__add_version_to_daily_schedules.sql
ALTER TABLE daily_schedules ADD COLUMN version BIGINT DEFAULT 0 NOT NULL;
```

### Step 7: Add Retry Logic for OptimisticLockException

```java
@Transactional
@Retryable(
    retryFor = OptimisticLockException.class,
    maxAttempts = 3,
    backoff = @Backoff(delay = 100, multiplier = 2, maxDelay = 1000)
)
public DailySchedule patchSchedule(UUID id, PatchScheduleDto patch) {
    // ... same as above
}

@Recover
public DailySchedule patchScheduleRecover(OptimisticLockException ex, UUID id, PatchScheduleDto patch) {
    log.error("Failed to update schedule {} after 3 retries due to concurrent modification", id);
    // Write to dead-letter queue for manual review
    deadLetterService.enqueue("schedule-update-failed", id, patch);
    throw new ConflictException("Schedule " + id + " is being modified concurrently. Please retry.", ex);
}
```

---

## Phase 3: Monitoring & Contract (Sprint 21)

### Step 8: Add Monitoring

Application metrics to add:
- `schedule.patch.success` — counter, incremented on each successful PATCH
- `schedule.patch.retry` — counter, incremented on each optimistic lock retry
- `schedule.patch.retry.exhausted` — counter, incremented when all retries fail
- `schedule.put.deprecated.usage` — counter, incremented on each PUT call (for migration tracking)

### Step 9: Update OpenAPI Specification

Add `PATCH /schedules/{id}` to `svc-scheduling-orchestrator.yaml` with the `PatchScheduleDto` schema. Mark `PUT /schedules/{id}` as deprecated with `x-sunset-date: 2026-06-01`.

---

## Testing Checklist

- [ ] Unit: `patchSchedule()` preserves `guideNotes` when not in DTO
- [ ] Unit: `patchSchedule()` preserves `guidePreferences` when not in DTO  
- [ ] Unit: `patchSchedule()` updates `guideId` when provided
- [ ] Unit: `patchSchedule()` handles null DTO fields gracefully
- [ ] Integration: Concurrent PATCH triggers `OptimisticLockException`
- [ ] Integration: Retry succeeds on second attempt after conflict
- [ ] Integration: PUT still works (backward compatibility during deprecation period)
- [ ] E2E: Guide enters vacation block → optimization runs → vacation block persists
- [ ] Performance: PATCH latency is ≤ PUT latency (no regression)
