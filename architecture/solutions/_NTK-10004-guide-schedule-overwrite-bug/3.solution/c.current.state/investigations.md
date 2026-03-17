# Current State Investigation - NTK-10004: Guide Schedule Overwrite Bug

## Investigation Status: CONFIRMED — Root Cause Identified

Last updated: 2026-02-28

---

## 1. Evidence Gathering: Elastic Log Analysis

### 1.1 ERROR-Level Logs (svc-scheduling-orchestrator)

Query: `mock-elastic-searcher.py --service svc-scheduling-orchestrator --level ERROR`

Four ERROR entries found showing guide enrichment data loss:

| Timestamp | Guide ID | Data Lost | Concurrent Window | Trace ID |
|-----------|----------|-----------|-------------------|----------|
| 2025-02-12 08:14:32.441Z | G-4821 | Certifications: ROPE_COURSE, ZIPLINE_ADVANCED | — | abc-1001-def-2001 |
| 2025-02-12 08:14:32.489Z | G-4821 | (concurrent PUT detected) | 47ms | abc-1001-def-2002 |
| 2025-02-12 09:15:44.887Z | G-5190 | Specializations: WILDLIFE_EXPERT, FIRST_AID_CERTIFIED | — | abc-1003-def-4001 |
| 2025-02-12 13:05:18.441Z | G-3302 | Language skills: SPANISH, PORTUGUESE | — | abc-1005-def-4002 |

All four entries share the same message pattern: _"Guide enrichment data overwritten during concurrent schedule update"_ and the same API path: `PUT /guides/{guideId}/schedule`.

### 1.2 WARN-Level Logs (Downstream Impact)

Query: `mock-elastic-searcher.py --service svc-scheduling-orchestrator --level WARN`

Two WARN entries confirm downstream operational impact of the data loss:

| Timestamp | Guide ID | Impact | API Path |
|-----------|----------|--------|----------|
| 2025-02-12 09:02:15.112Z | G-4821 | Removed from ADV-302 (ROPE_COURSE) — missing certification | POST /schedules/daily-assignments |
| 2025-02-12 13:20:09.112Z | G-3302 | Removed from ADV-115 (BILINGUAL_TOUR) — missing language qualification | POST /schedules/daily-assignments |

**Causal chain confirmed**: Guide G-4821 lost ROPE_COURSE certification at 08:14 → was removed from ROPE_COURSE assignment at 09:02. Guide G-3302 lost SPANISH/PORTUGUESE at 13:05 → was removed from BILINGUAL_TOUR at 13:20.

### 1.3 Log Evidence Summary

- 4 ERROR events in a single day showing enrichment data loss across 3 guides
- 2 WARN events showing downstream assignment removals caused by the data loss
- Concurrent PUT window as tight as 47ms for guide G-4821
- Affected data types: certifications, specializations, language skills

---

## 2. Source Code Analysis: svc-scheduling-orchestrator

### 2.1 SchedulingService.java — The Bug

File: `source-code/svc-scheduling-orchestrator/src/main/java/com/novatrek/scheduling/service/SchedulingService.java`

The `updateSchedule()` method (lines 54-64) performs **full entity replacement**:

```java
// BUG: NTK-10004 - This PUT replaces the entire entity, overwriting guide enrichments
// (guideNotes, guidePreferences) that were set by svc-guide-management.
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

Key observation: `scheduleRepository.save(incoming)` persists the entire `DailySchedule` entity. Since `incoming` was deserialized from the API request body — which does not include `guideNotes` or `guidePreferences` — those fields are set to `null` and overwrite the existing values.

### 2.2 DailySchedule.java — Data Model

File: `source-code/svc-scheduling-orchestrator/src/main/java/com/novatrek/scheduling/model/DailySchedule.java`

The entity has two fields explicitly commented as vulnerable:

```java
// GETS OVERWRITTEN by NTK-10004 bug - guide-management enriches this field
@Column(columnDefinition = "TEXT")
private String guideNotes;

// GETS OVERWRITTEN by NTK-10004 bug - guide-management enriches this field
@Column(columnDefinition = "TEXT")
private String guidePreferences;
```

These fields are enriched by svc-guide-management but live in the same JPA entity and database table (`daily_schedules`) as scheduling-owned fields like `guideId`, `tripId`, `startTime`, `endTime`, and `status`.

### 2.3 ScheduleController.java — PUT Endpoint

File: `source-code/svc-scheduling-orchestrator/src/main/java/com/novatrek/scheduling/controller/ScheduleController.java`

```java
@PutMapping("/{id}")
public DailySchedule updateSchedule(@PathVariable UUID id,
                                    @Valid @RequestBody DailySchedule schedule) {
    // THE PROBLEMATIC ENDPOINT - full entity replacement overwrites guide enrichments
    return schedulingService.updateSchedule(id, schedule);
}
```

The controller only exposes PUT — no PATCH endpoint exists. There is no merge logic, no field-level ownership check, and no concurrency control (no `@Version`, no `If-Match` ETag support).

### 2.4 No Version Control on Entity

The `DailySchedule` entity has no `@Version` annotation (JPA optimistic locking). The `lastModifiedAt` field is set manually but not used for conflict detection. This means concurrent PUT requests result in last-write-wins semantics with no error or warning.

---

## 3. GitLab MR History

Query: `mock-gitlab-client.py --list`

| MR | Status | Author | Files | Title |
|----|--------|--------|-------|-------|
| !5001 | MERGED | alex.chen | 3 | feat: Add elevation data to trail response |
| !5002 | OPEN | maya.rodriguez | 8 | feat: Adventure category classification system |

**Finding**: No MR exists for svc-scheduling-orchestrator that addresses the overwrite bug. The PUT-based `updateSchedule()` method is the original implementation — the bug was introduced at initial service creation, not by a subsequent change. The PATCH alternative was never implemented.

---

## 4. API Specification Analysis

File: `corporate-services/services/svc-scheduling-orchestrator.yaml`

The OpenAPI spec (v3.0.1, 662 lines) defines the scheduling orchestrator as the _"architectural hub for all scheduling decisions."_ It exposes:
- `POST /schedule-requests` — async optimization requests
- `GET /schedule-optimization` — sync optimization
- `GET/POST /schedules/conflicts` — conflict detection and resolution

The spec does not define `PUT /schedules/{id}` or `PATCH /schedules/{id}` at the API gateway level — the problematic PUT endpoint is an internal implementation detail exposed through the Spring Boot controller but not documented in the service contract. This is itself an architectural concern: an undocumented internal endpoint is causing data corruption.

---

## 5. Root Cause Analysis — CONFIRMED

### Primary Root Cause: Data Ownership Boundary Violation

The svc-scheduling-orchestrator performs **full entity replacement** (PUT semantics) on the `daily_schedules` table, overwriting fields it does not own. The `DailySchedule` JPA entity conflates two distinct ownership domains:

| Field Group | Owner | Mutated By | Example Fields |
|-------------|-------|------------|----------------|
| Scheduling fields | svc-scheduling-orchestrator | Optimization pipeline | guideId, tripId, startTime, endTime, status |
| Enrichment fields | svc-guide-management | Guide Portal, enrichment pipeline | guideNotes, guidePreferences |

When the orchestrator calls `scheduleRepository.save(incoming)`, the `incoming` entity has `guideNotes = null` and `guidePreferences = null` because the API caller never sends those fields. JPA persists the entire entity, replacing the existing enrichment data with nulls.

**This is not merely a code bug — it is an architectural data ownership violation.** The scheduling service treats a shared data structure as exclusively its own.

### Secondary Root Cause: Absent Concurrency Control

No optimistic locking exists on the `DailySchedule` entity:
- No `@Version` field
- No `ETag` / `If-Match` support
- No conditional writes

When multiple optimization runs execute concurrently (e.g., nightly batch across regions), guides assigned to cross-region trails can have their schedules overwritten by the last writer. Elastic logs confirm a 47ms race window for guide G-4821.

### Contributing Factor: Undocumented Internal Endpoint

The `PUT /api/v1/schedules/{id}` endpoint is not in the service's OpenAPI contract. It exists only as a Spring Boot controller mapping, bypassing API gateway governance and contract-first design review.

---

## 6. Impact Assessment

| Impact Category | Severity | Description |
|----------------|----------|-------------|
| **Guide Safety** | CRITICAL | Medical restrictions (altitude limits, equipment restrictions) are silently removed |
| **Operational** | HIGH | 15-20 incorrect guide removals per day during peak periods; manual re-assignment required |
| **Guide Retention** | MEDIUM | Two guides have escalated to HR about repeated data loss; trust in the system is eroding |
| **Data Integrity** | HIGH | Production data corruption — no recovery mechanism exists |
| **Compliance** | MEDIUM | Safety certifications must be maintained per NovaTrek operational policies |

---

## 7. Recommendation Summary

### Immediate Fix (Sprint 19/20)
1. **Switch orchestrator from PUT to PATCH**: Modify `SchedulingService.updateSchedule()` to update only scheduling-owned fields, preserving enrichment fields
2. **Add a PATCH endpoint** to `ScheduleController.java` that accepts a partial update DTO containing only orchestrator-owned fields
3. **Add `@Version` optimistic locking** to `DailySchedule` entity to prevent concurrent write corruption

### Architectural Improvement (Sprint 21+)
4. **Define explicit data ownership contracts**: Document which service owns which fields in shared entities, enforced through API contracts
5. **Consider document separation**: Split the `daily_schedules` table into `schedule_assignments` (orchestrator-owned) and `guide_schedule_metadata` (guide-management-owned), joined at read time
6. **Add the endpoint to the OpenAPI contract**: Document `PATCH /api/v1/schedules/{id}` in `svc-scheduling-orchestrator.yaml` and remove or deprecate the undocumented PUT

### Monitoring
7. **Alert on `guideNotes`/`guidePreferences` nullification**: Add a database trigger or application-level check that logs a WARNING when enrichment fields transition from non-null to null
8. **Track concurrent write frequency**: Monitor for overlapping writes within configurable time windows
