# Current State Investigation - NTK-10004: Guide Schedule Overwrite Bug

## Investigation Status: CONFIRMED -- Root Cause Identified

Last updated: 2026-03-04

---

## 1. Evidence Gathering: Elastic Log Analysis

### 1.1 ERROR-Level Logs (svc-scheduling-orchestrator)

Query: `python3 scripts/mock-elastic-searcher.py --service svc-scheduling-orchestrator --level ERROR`

Four ERROR entries found showing guide enrichment data loss:

| Timestamp | Guide ID | Data Lost | Concurrent Window | Trace ID |
|-----------|----------|-----------|-------------------|----------|
| 2025-02-12 08:14:32.441Z | G-4821 | Certifications: ROPE_COURSE, ZIPLINE_ADVANCED | -- | abc-1001-def-2001 |
| 2025-02-12 08:14:32.489Z | G-4821 | (concurrent PUT detected) | 47ms | abc-1001-def-2002 |
| 2025-02-12 09:15:44.887Z | G-5190 | Specializations: WILDLIFE_EXPERT, FIRST_AID_CERTIFIED | -- | abc-1003-def-4001 |
| 2025-02-12 13:05:18.441Z | G-3302 | Language skills: SPANISH, PORTUGUESE | -- | abc-1005-def-4002 |

All four entries share the message pattern: "Guide enrichment data overwritten during concurrent schedule update" and the API path: `PUT /guides/{guideId}/schedule`.

### 1.2 Error Timeline Analysis

The errors on 2025-02-12 follow a clear pattern:

1. **08:14:32.441Z** -- Guide G-4821 loses ROPE_COURSE and ZIPLINE_ADVANCED certifications via PUT
2. **08:14:32.489Z** -- 47ms later, a second concurrent PUT for the same guide confirms a race condition
3. **09:15:44.887Z** -- Guide G-5190 loses WILDLIFE_EXPERT and FIRST_AID_CERTIFIED specializations
4. **13:05:18.441Z** -- Guide G-3302 loses SPANISH and PORTUGUESE language skills

The 47ms gap between the two G-4821 entries confirms concurrent optimization runs writing to the same guide simultaneously.

### 1.3 Causal Chain

Based on the ticket report comments (Sam Patel, 2026-02-14), the downstream impact is:
- Guide G-4821 lost ROPE_COURSE certification -> removed from rope course assignment
- Guide G-3302 lost SPANISH/PORTUGUESE -> removed from bilingual tour assignment
- Guide Maria Torres lost medical altitude restriction -> safety concern
- Guide Jake Moreno lost vacation block Feb 22-28 -> received conflicting assignment

---

## 2. Source Code Analysis: svc-scheduling-orchestrator

### 2.1 SchedulingService.java -- The Bug

File: `SchedulingService.java` lines 52-64

The `updateSchedule()` method performs **full entity replacement**:

```java
// BUG: NTK-10004 - This PUT replaces the entire entity, overwriting guide enrichments
@Transactional
public DailySchedule updateSchedule(UUID id, DailySchedule incoming) {
    if (!scheduleRepository.existsById(id)) {
        throw new RuntimeException("Schedule not found: " + id);
    }
    // Full entity replacement - this is the bug!
    // The incoming entity from API clients does NOT include guideNotes/guidePreferences
    incoming.setId(id);
    incoming.setLastModifiedAt(LocalDateTime.now());
    incoming.setLastModifiedBy("scheduling-orchestrator");
    return scheduleRepository.save(incoming);
}
```

`scheduleRepository.save(incoming)` persists the entire `DailySchedule` entity. Since `incoming` was deserialized from the API request body -- which does not include `guideNotes` or `guidePreferences` -- those fields are set to `null` and overwrite the existing values.

### 2.2 DailySchedule.java -- Data Model

The entity has two fields explicitly marked as vulnerable:

```java
// GETS OVERWRITTEN by NTK-10004 bug - guide-management enriches this field
@Column(columnDefinition = "TEXT")
private String guideNotes;

// GETS OVERWRITTEN by NTK-10004 bug - guide-management enriches this field
@Column(columnDefinition = "TEXT")
private String guidePreferences;
```

These fields are enriched by svc-guide-management but live in the same JPA entity and database table (`daily_schedules`) as scheduling-owned fields.

### 2.3 No Concurrency Control

The `DailySchedule` entity has:
- No `@Version` annotation (JPA optimistic locking absent)
- No `ETag` / `If-Match` support
- `lastModifiedAt` set manually but not used for conflict detection

Result: concurrent PUT requests follow last-write-wins with no error or warning.

---

## 3. GitLab MR History

Query: `python3 scripts/mock-gitlab-client.py --list`

| MR | Status | Author | Files | Title |
|----|--------|--------|-------|-------|
| !5001 | MERGED | alex.chen | 3 | feat: Add elevation data to trail response |
| !5002 | OPEN | maya.rodriguez | 8 | feat: Adventure category classification system |
| !5003 | OPEN | alex.chen | 12 | feat: Unregistered guest self-service check-in |

**Finding**: No MR exists for svc-scheduling-orchestrator addressing the overwrite bug. The PUT-based `updateSchedule()` method is the original implementation -- the bug was introduced at initial service creation, not by a subsequent change. No PATCH alternative was ever implemented.

---

## 4. Root Cause Analysis -- CONFIRMED

### Primary Root Cause: Architectural Data Ownership Boundary Violation

This is NOT just a code bug. It is an **architectural boundary violation**. The svc-scheduling-orchestrator uses full entity replacement (PUT semantics) on a shared data structure, overwriting fields it does not own. The `DailySchedule` entity conflates two distinct ownership domains:

| Field Group | Owner | Mutated By | Example Fields |
|-------------|-------|------------|----------------|
| Scheduling fields | svc-scheduling-orchestrator | Optimization pipeline | guideId, tripId, startTime, endTime, status |
| Enrichment fields | svc-guide-management | Guide Portal, enrichment API | guideNotes, guidePreferences |

When the orchestrator calls `scheduleRepository.save(incoming)`, the `incoming` entity has `guideNotes = null` and `guidePreferences = null` because the API caller does not send those fields. JPA persists the entire entity, replacing existing enrichment data with nulls.

### Secondary Root Cause: Absent Concurrency Control

No optimistic locking exists on the `DailySchedule` entity. Concurrent regional optimization runs can overwrite each other's results. Elastic logs confirm a 47ms race window for guide G-4821.

### Contributing Factor: Undocumented Internal Endpoint

The `PUT /api/v1/schedules/{id}` endpoint is not in the service's OpenAPI contract (`svc-scheduling-orchestrator.yaml`). It exists only as a Spring Boot controller mapping, bypassing API gateway governance and contract-first design review.

---

## 5. Impact Assessment

| Impact Category | Severity | Description |
|----------------|----------|-------------|
| Guide Safety | CRITICAL | Medical restrictions silently removed (altitude limits, equipment restrictions) |
| Operational | HIGH | Incorrect guide assignments; manual re-assignment required |
| Guide Retention | MEDIUM | Guides escalating to HR about repeated data loss |
| Data Integrity | HIGH | Production data corruption with no recovery mechanism |
| Compliance | MEDIUM | Safety certifications must be maintained per operational policies |
