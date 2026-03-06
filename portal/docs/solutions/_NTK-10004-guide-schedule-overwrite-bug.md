---
title: "NTK-10004 — NTK-10004: Solution Design — Guide Schedule Overwrite Bug"
description: "Solution design for NTK-10004"
---

# NTK-10004 — NTK-10004: Solution Design — Guide Schedule Overwrite Bug

| Field | Value |
|-------|-------|
| **Status** | Assumption |
| **Ticket** | NTK-10004 |

## Affected Capabilities

| Capability | Impact |
|-----------|--------|
| [CAP-2.2 Schedule Planning and Optimization](../capabilities/index.md#cap-22) | Fixed |

## Affected Services

- [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md)

## Architecture Decisions

- ADR-010
- ADR-011

## Solution Contents

- Requirements
- Analysis
- Decisions
- Impact Assessments (0)
- Implementation Guidance
- Risk Assessment
- Capability Mapping

---


## Metadata

| Field | Value |
|-------|-------|
| **Ticket** | NTK-10004 |
| **Version** | 1.0 |
| **Status** | DRAFT |
| **Author** | Solution Architecture (AI-assisted) |
| **Created** | 2026-02-28 |
| **Classification** | Bug Fix — Medium Complexity |

---

## 1. Problem Statement

The svc-scheduling-orchestrator's nightly and on-demand optimization pipeline overwrites guide enrichment data (vacation blocks, medical restrictions, certification notes, group size overrides) stored in the `daily_schedules` table. The root cause is a full entity replacement via PUT semantics that discards fields not in the orchestrator's DTO. A secondary issue exists: no concurrency control prevents race conditions when multiple regions optimize simultaneously.

**Impact**: 15-20 incorrect guide removals per day during peak periods. Safety-critical medical restrictions silently removed. Guide HR complaints escalating.

---

## 2. Root Cause Summary

| # | Cause | Type | Severity |
|---|-------|------|----------|
| 1 | `SchedulingService.updateSchedule()` uses `scheduleRepository.save(incoming)` which replaces the entire entity, setting guide-owned fields to null | Primary — Code Bug | Critical |
| 2 | `DailySchedule` entity conflates orchestrator-owned and guide-management-owned fields in a single JPA entity with no ownership boundary | Primary — Architecture | Critical |
| 3 | No `@Version` or ETag concurrency control; last-write-wins on concurrent updates | Secondary — Architecture | High |
| 4 | `PUT /api/v1/schedules/{id}` endpoint undocumented in OpenAPI spec | Contributing — Governance | Medium |

See: [investigations.md](../c.current.state/investigations.md) for full evidence chain.

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

See: [decisions.md](../d.decisions/decisions.md)

---

## 4. Affected Services

| Service | Impact Level | Changes Required |
|---------|-------------|-----------------|
| **svc-scheduling-orchestrator** | HIGH | New PATCH endpoint, PatchScheduleDto, @Version field, retry logic |
| **svc-guide-management** | LOW | Monitoring only — detect enrichment field nullification |
| **API Gateway / OpenAPI** | MEDIUM | Contract update — add PATCH, deprecate PUT |

See: [impacts.md](../i.impacts/impacts.md)

---

## 5. Data Ownership Model

The core architectural fix is establishing explicit field ownership:

```
┌─────────────────────────────────────────────────────────┐
│                    daily_schedules                       │
├─────────────────────────┬───────────────────────────────┤
│  ORCHESTRATOR-OWNED     │  GUIDE-MANAGEMENT-OWNED       │
│  ─────────────────────  │  ───────────────────────────  │
│  guideId                │  guideNotes                   │
│  tripId                 │  guidePreferences             │
│  startTime              │                               │
│  endTime                │                               │
│  participantCount       │                               │
│  maxCapacity            │                               │
│  status                 │                               │
│  locationId             │                               │
│  scheduleDate           │                               │
├─────────────────────────┴───────────────────────────────┤
│  SHARED / SYSTEM                                         │
│  ─────────────────────────────────────────────────────── │
│  id, version, generatedAt, lastModifiedAt, lastModifiedBy│
└─────────────────────────────────────────────────────────┘
```

The `PatchScheduleDto` enforces this boundary structurally: it contains only orchestrator-owned fields. Guide-management-owned fields cannot be accidentally modified because they do not exist in the DTO.

---

## 6. Key Design Decisions

1. **PATCH over read-merge-write**: PATCH semantics enforce ownership at the API boundary. Read-merge-write would add latency and rely on fragile merge logic.

2. **@Version over ETag**: JPA `@Version` is simpler and integrates with Hibernate's built-in conflict detection. ETag-based HTTP concurrency is deferred as a future enhancement for external API consumers.

3. **Deprecate PUT, don't remove it immediately**: A sunset period allows undiscovered callers to be identified and migrated. Logging + metrics track PUT usage during the transition.

4. **Three-sprint phased rollout**: Phase 1 (PATCH) provides immediate safety relief. Phase 2 (locking) addresses the less frequent concurrency issue. Phase 3 (monitoring/governance) prevents recurrence.

---

## 7. Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Incomplete field ownership mapping | Medium | High | Full entity audit before implementation |
| Optimistic lock retry exhaustion | Low | Medium | Dead-letter queue + alerting |
| Undiscovered PUT callers | Medium | Medium | Observation period with structured logging |
| Historical data unrecoverable | High | Medium | Guide notification campaign post-deploy |

See: [risks.md](../r.risks/risks.md)

---

## 8. Assumptions

| # | Assumption | Status | Validation |
|---|-----------|--------|------------|
| A1 | Orchestrator uses full replacement (PUT) semantics | CONFIRMED | Source code review of SchedulingService.java |
| A2 | Manual adjustments share the same database entity | CONFIRMED | DailySchedule.java entity inspection |
| A3 | Concurrent regional optimization creates race conditions | CONFIRMED | Elastic logs: 47ms race window for G-4821 |
| A4 | No revision or concurrency control exists | CONFIRMED | No @Version annotation in DailySchedule entity |

See: [assumptions.md](../a.assumptions/assumptions.md)

---

## 9. Implementation Guidance

Detailed implementation steps with code samples are provided in [guidance.md](../g.guidance/guidance.md), including:
- `PatchScheduleDto` class definition
- `patchSchedule()` service method
- PATCH controller endpoint
- PUT deprecation pattern
- Database migration SQL
- `@Retryable` configuration for optimistic lock conflicts
- Testing checklist (9 test cases)

---

## 10. Success Criteria

1. **Zero enrichment data loss** after optimization — monitored via `guide.enrichment.nullified.count` metric (target: 0)
2. **Concurrent write conflicts detected** — `schedule.patch.retry` metric shows conflicts are caught, not silent
3. **PUT usage drops to zero** within 2 sprints of PATCH availability
4. **No guide HR complaints** related to lost schedule data post-deployment
5. **15-20 daily incorrect removals reduced to 0**