# Current State Investigation - NTK-10004: Guide Schedule Overwrite Bug

## Investigation Status: CONFIRMED - Root Cause Identified

Last updated: 2026-03-04

---

## 1 Evidence Gathering: Elastic Log Analysis

### 1.1 ERROR-Level Logs (svc-scheduling-orchestrator)

Query: `python3 scripts/mock-elastic-searcher.py --service svc-scheduling-orchestrator --level ERROR`

Four ERROR entries found showing guide enrichment data loss:

| Timestamp | Guide ID | Data Lost | Concurrent Window | Trace ID |
|-----------|----------|-----------|-------------------|----------|
| 2025-02-12 08:14:32.441Z | G-4821 | Certifications: ROPE_COURSE, ZIPLINE_ADVANCED | - | abc-1001-def-2001 |
| 2025-02-12 08:14:32.489Z | G-4821 | (concurrent PUT detected) | 47ms | abc-1001-def-2002 |
| 2025-02-12 09:15:44.887Z | G-5190 | Specializations: WILDLIFE_EXPERT, FIRST_AID_CERTIFIED | - | abc-1003-def-4001 |
| 2025-02-12 13:05:18.441Z | G-3302 | Language skills: SPANISH, PORTUGUESE | - | abc-1005-def-4002 |

All four entries share the message pattern: "Guide enrichment data overwritten during concurrent schedule update" and the API path: `PUT /guides/{guideId}/schedule`.

### 1.2 Causal Chain Confirmed

The error log timestamps directly correlate with downstream operational failures:

- Guide G-4821 lost ROPE_COURSE certification at 08:14 -> was removed from ROPE_COURSE assignment by the daily assignment process
- Guide G-3302 lost SPANISH/PORTUGUESE language skills at 13:05 -> was removed from BILINGUAL_TOUR assignment

This establishes the causal chain: enrichment data loss -> incorrect guide qualification checks -> improper assignment removals.

---

## 2 Source Code Analysis: svc-scheduling-orchestrator

### 2.1 SchedulingService.java - The Bug

File: `source-code/svc-scheduling-orchestrator/src/main/java/com/novatrek/scheduling/service/SchedulingService.java`

The `updateSchedule()` method (lines 54-64) performs **full entity replacement**:

```java
@Transactional
public DailySchedule updateSchedule(UUID id, DailySchedule incoming) {
    if (!scheduleRepository.existsById(id)) {
        throw new RuntimeException("Schedule not found: " + id);
    }
    // Full entity replacement - this is the bug!
    incoming.setId(id);
    incoming.setLastModifiedAt(LocalDateTime.now());
    incoming.setLastModifiedBy("scheduling-orchestrator");
    return scheduleRepository.save(incoming);
}
```

`scheduleRepository.save(incoming)` persists the entire `DailySchedule` entity. Since `incoming` was deserialized from the API request body — which does not include `guideNotes` or `guidePreferences` — those fields are set to `null` and overwrite the existing values.

### 2.2 DailySchedule.java - Data Model

The entity has two fields explicitly vulnerable to overwrite:

- `guideNotes` (TEXT column) — enriched by svc-guide-management
- `guidePreferences` (TEXT column) — enriched by svc-guide-management

These fields live in the same JPA entity and database table (`daily_schedules`) as scheduling-owned fields like `guideId`, `tripId`, `startTime`, `endTime`, and `status`.

### 2.3 ScheduleController.java - No PATCH Endpoint

The controller only exposes PUT — no PATCH endpoint exists. There is no merge logic, no field-level ownership check, and no concurrency control (no `@Version`, no `If-Match` ETag support).

### 2.4 No Version Control on Entity

The `DailySchedule` entity has no `@Version` annotation (JPA optimistic locking). The `lastModifiedAt` field is set manually but not used for conflict detection. Concurrent PUT requests result in last-write-wins semantics with no error or warning.

---

## 3 GitLab MR History

Query: `python3 scripts/mock-gitlab-client.py --list`

| MR | Status | Author | Files | Title |
|----|--------|--------|-------|-------|
| !5001 | MERGED | alex.chen | 3 | feat: Add elevation data to trail response |
| !5002 | OPEN | maya.rodriguez | 8 | feat: Adventure category classification system |
| !5003 | OPEN | alex.chen | 12 | feat: Unregistered guest self-service check-in |

**Finding**: No MR exists for svc-scheduling-orchestrator that addresses the overwrite bug. The PUT-based `updateSchedule()` method is the original implementation — the bug was introduced at initial service creation, not by a subsequent change.

---

## 4 Root Cause Analysis - CONFIRMED

### Primary Root Cause: Data Ownership Boundary Violation

The svc-scheduling-orchestrator performs **full entity replacement** (PUT semantics) on the `daily_schedules` table, overwriting fields it does not own. The `DailySchedule` JPA entity conflates two distinct ownership domains:

| Field Group | Owner | Mutated By | Example Fields |
|-------------|-------|------------|----------------|
| Scheduling fields | svc-scheduling-orchestrator | Optimization pipeline | guideId, tripId, startTime, endTime, status |
| Enrichment fields | svc-guide-management | Guide Portal, enrichment pipeline | guideNotes, guidePreferences |

**This is not merely a code bug — it is an architectural data ownership violation.** The scheduling service treats a shared data structure as exclusively its own.

### Secondary Root Cause: Absent Concurrency Control

No optimistic locking exists on the `DailySchedule` entity. When multiple optimization runs execute concurrently, guides assigned to cross-region trails can have their schedules overwritten by the last writer. Elastic logs confirm a 47ms race window for guide G-4821.

### Contributing Factor: Undocumented Internal Endpoint

The `PUT /api/v1/schedules/{id}` endpoint is not in the service's OpenAPI contract. It exists only as a Spring Boot controller mapping, bypassing API gateway governance and contract-first design review.

---

## 5 Impact Assessment

| Impact Category | Severity | Description |
|----------------|----------|-------------|
| Guide Safety | CRITICAL | Medical restrictions are silently removed |
| Operational | HIGH | Incorrect guide assignment removals during peak periods |
| Guide Retention | MEDIUM | Guides escalating to HR about repeated data loss |
| Data Integrity | HIGH | Production data corruption with no recovery mechanism |
| Compliance | MEDIUM | Safety certifications must be maintained per operational policies |
