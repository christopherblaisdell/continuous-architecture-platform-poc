# NTK-10004: Solution Design -- Guide Schedule Overwrite Bug

## Metadata

| Field | Value |
|-------|-------|
| **Ticket** | NTK-10004 |
| **Version** | 1.1 |
| **Status** | DRAFT |
| **Author** | Solution Architecture (AI-assisted) |
| **Created** | 2026-02-28 |
| **Updated** | 2026-03-03 |
| **Classification** | Bug Fix -- Architectural Boundary Violation |

---

## 1. Problem Statement

The svc-scheduling-orchestrator's nightly and on-demand optimization pipeline overwrites guide enrichment data (vacation blocks, medical restrictions, certification notes, group size overrides) stored in the `daily_schedules` table. The root cause is a full entity replacement via PUT semantics that discards fields not in the orchestrator's DTO. A secondary issue exists: no concurrency control prevents race conditions when multiple regions optimize simultaneously.

**Impact**: 15-20 incorrect guide removals per day during peak periods. Safety-critical medical restrictions silently removed. Guide HR complaints escalating. Three regions confirmed affected (Cascadia, Sierra, Appalachian).

---

## 2. Root Cause Summary

| # | Cause | Type | Severity |
|---|-------|------|----------|
| 1 | `SchedulingService.updateSchedule()` uses `scheduleRepository.save(incoming)` which replaces the entire entity, setting guide-owned fields to null | Primary -- Code Bug | Critical |
| 2 | `DailySchedule` entity conflates orchestrator-owned and guide-management-owned fields in a single JPA entity with no ownership boundary | Primary -- Architecture | Critical |
| 3 | No `@Version` or ETag concurrency control; last-write-wins on concurrent updates | Secondary -- Architecture | High |
| 4 | `PUT /api/v1/schedules/{id}` endpoint undocumented in OpenAPI spec | Contributing -- Governance | Medium |

**Evidence chain** (from Elastic logs):
- 4 ERROR events on 2025-02-12 showing enrichment data loss across 3 guides (G-4821, G-5190, G-3302)
- Race window as tight as 47ms (guide G-4821, trace IDs abc-1001-def-2001 and abc-1001-def-2002)
- Data lost includes ROPE_COURSE and ZIPLINE_ADVANCED certifications, WILDLIFE_EXPERT and FIRST_AID_CERTIFIED specializations, SPANISH and PORTUGUESE language skills

**GitLab MR analysis**: No MR addresses this issue. The PUT-based implementation is the original code -- the bug exists since service creation.

---

## 3. Solution Overview

### Phased Approach

| Phase | Sprint | Scope | Risk Addressed |
|-------|--------|-------|----------------|
| **Phase 1** | Sprint 19 | PATCH semantics + partial-update DTO | Primary: data overwrites |
| **Phase 2** | Sprint 20 | @Version optimistic locking + retry | Secondary: race conditions |
| **Phase 3** | Sprint 21 | Monitoring, PUT deprecation, OpenAPI update | Contributing: governance |

### Architecture Decision Records

- **ADR-NTK10004-001**: Switch from PUT to PATCH semantics (PROPOSED)
- **ADR-NTK10004-002**: Add optimistic locking to DailySchedule (PROPOSED)

---

## 4. Data Ownership Model

The core architectural fix is establishing explicit field ownership:

```
+-----------------------------------------------------------+
|                    daily_schedules                         |
+---------------------------+-------------------------------+
|  ORCHESTRATOR-OWNED       |  GUIDE-MANAGEMENT-OWNED       |
|  -----------------------  |  ---------------------------  |
|  guideId                  |  guideNotes                   |
|  tripId                   |  guidePreferences             |
|  startTime                |                               |
|  endTime                  |                               |
|  participantCount         |                               |
|  maxCapacity              |                               |
|  status                   |                               |
|  locationId               |                               |
|  scheduleDate             |                               |
+---------------------------+-------------------------------+
|  SHARED / SYSTEM                                          |
|  -------------------------------------------------------  |
|  id, version, generatedAt, lastModifiedAt, lastModifiedBy |
+-----------------------------------------------------------+
```

The `PatchScheduleDto` enforces this boundary structurally: it contains only orchestrator-owned fields. Guide-management-owned fields cannot be accidentally modified because they do not exist in the DTO.

---

## 5. Affected Services

| Service | Impact Level | Changes Required |
|---------|-------------|-----------------|
| **svc-scheduling-orchestrator** | HIGH | New PATCH endpoint, PatchScheduleDto, @Version field, retry logic |
| **svc-guide-management** | LOW | Monitoring only -- detect enrichment field nullification |
| **API Gateway / OpenAPI** | MEDIUM | Contract update -- add PATCH, deprecate PUT |

---

## 6. Key Design Decisions

1. **PATCH over read-merge-write**: PATCH semantics enforce ownership at the API boundary. Read-merge-write would add latency and rely on fragile merge logic.

2. **@Version over ETag**: JPA `@Version` is simpler and integrates with Hibernate's built-in conflict detection. ETag-based HTTP concurrency is deferred as a future enhancement for external API consumers.

3. **Deprecate PUT, don't remove it immediately**: A sunset period (target: 2026-06-01) allows undiscovered callers to be identified and migrated. Logging + metrics track PUT usage during the transition.

4. **Three-sprint phased rollout**: Phase 1 (PATCH) provides immediate safety relief. Phase 2 (locking) addresses the less frequent concurrency issue. Phase 3 (monitoring/governance) prevents recurrence.

---

## 7. Success Criteria

1. **Zero enrichment data loss** after optimization -- monitored via `guide.enrichment.nullified.count` metric (target: 0)
2. **Concurrent write conflicts detected** -- `schedule.patch.retry` metric shows conflicts are caught, not silent
3. **PUT usage drops to zero** within 2 sprints of PATCH availability
4. **No guide HR complaints** related to lost schedule data post-deployment
5. **15-20 daily incorrect removals reduced to 0**

---

## 8. References

- Investigation: `3.solution/c.current.state/investigations.md`
- Decisions: `3.solution/d.decisions/decisions.md`
- Guidance: `3.solution/g.guidance/guidance.md`
- Risks: `3.solution/r.risks/risks.md`
- Impacts: `3.solution/i.impacts/impacts.md`
- Source code: `source-code/svc-scheduling-orchestrator/src/main/java/com/novatrek/scheduling/service/SchedulingService.java`
