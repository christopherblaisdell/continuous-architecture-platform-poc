<!-- CONFLUENCE-PUBLISH -->

# NTK-10004 - Solution Design: Guide Schedule Overwrite Bug

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Date | 2026-03-03 |
| Author | Solution Architecture (AI-Assisted) |
| Status | DRAFT |
| Ticket | NTK-10004 |

## Problem Statement

Guides using the NovaTrek Guide Portal report that their manually entered availability exceptions, training day blocks, medical restrictions, and special notes are disappearing after the svc-scheduling-orchestrator runs its optimization cycle. The root cause is an architectural data ownership boundary violation: the orchestrator uses PUT semantics (full entity replacement) to update guide schedules, overwriting fields it does not own.

This is a safety-critical issue. Medical restrictions (such as altitude limits) are silently removed, leading to guides being assigned to trails they are medically restricted from. The problem affects all regions and has been reported by multiple guides across Cascadia, Sierra, and Appalachian regions.

## Root Cause Summary

### Primary: Data Ownership Boundary Violation

The `SchedulingService.updateSchedule()` method in svc-scheduling-orchestrator (lines 52-64) calls `scheduleRepository.save(incoming)`, which performs a full JPA entity save. The `incoming` entity is deserialized from an API request that does NOT include `guideNotes` or `guidePreferences` (fields owned by svc-guide-management). These fields are set to null and overwrite the existing values.

The `DailySchedule` JPA entity conflates two distinct ownership domains in a single table (`daily_schedules`):

| Field Group | Owner | Example Fields |
|-------------|-------|----------------|
| Scheduling | svc-scheduling-orchestrator | guideId, tripId, startTime, endTime, status |
| Enrichment | svc-guide-management | guideNotes, guidePreferences |

### Secondary: Absent Concurrency Control

The `DailySchedule` entity has no `@Version` field for optimistic locking. Concurrent optimization runs (nightly batch across regions) can race on cross-region guide schedules. Elastic logs confirm a 47ms concurrent write window for guide G-4821 (trace IDs abc-1001-def-2001 and abc-1001-def-2002).

### Contributing Factor: Undocumented Internal Endpoint

The `PUT /api/v1/schedules/{id}` endpoint exists only as a Spring Boot controller mapping and is not documented in the service OpenAPI contract. It bypassed API governance and contract-first design review.

## Evidence Summary

| Source | Finding |
|--------|---------|
| Elastic ERROR logs | 4 data loss events on 2025-02-12 across guides G-4821, G-5190, G-3302. Lost data: certifications, specializations, language skills. |
| Source code review | `SchedulingService.updateSchedule()` performs full entity replacement via `scheduleRepository.save(incoming)` |
| Source code review | `DailySchedule` entity has no `@Version` field; `guideNotes` and `guidePreferences` fields are explicitly commented as vulnerable |
| GitLab MR history | No MR addresses this bug. The PUT implementation is the original code -- the bug was introduced at service creation. |

## Solution

### Immediate Fix (Sprint 19/20)

1. **Switch from PUT to PATCH semantics**: Modify `SchedulingService.updateSchedule()` to use a new `ScheduleUpdateRequest` DTO containing only orchestrator-owned fields. Read the existing entity, update only the DTO fields, and save.

2. **Add PATCH endpoint**: Create `PATCH /api/v1/schedules/{id}` in `ScheduleController`. Deprecate or remove the existing PUT endpoint.

3. **Add optimistic locking**: Add `@Version private Long version;` to the `DailySchedule` entity. Add a database migration for the `version` column. Handle `OptimisticLockException` with HTTP 409 Conflict response.

### Architectural Improvement (Sprint 21+)

4. **Document the endpoint**: Add `PATCH /api/v1/schedules/{id}` to the OpenAPI specification. Remove or deprecate the undocumented PUT.

5. **Define data ownership contracts**: Document which service owns which fields in shared entities.

6. **Consider entity separation**: In a future phase, consider splitting the `daily_schedules` table into `schedule_assignments` (orchestrator-owned) and `guide_schedule_metadata` (guide-management-owned).

## Architecture Decisions

- **ADR-NTK10004-001**: PATCH Semantics for Schedule Updates -- switch from PUT to PATCH to prevent overwriting non-owned fields.
- **ADR-NTK10004-002**: Optimistic Locking on Daily Schedule Entity -- add `@Version` field to detect and prevent concurrent write corruption.

Full MADR-formatted ADRs in [decisions.md](3.solution/d.decisions/decisions.md).

## Related Artifacts

- [Ticket Report](1.requirements/NTK-10004.ticket.report.md)
- [Current State Investigation](3.solution/c.current.state/investigations.md)
- [Assumptions](3.solution/a.assumptions/assumptions.md)
- [Decisions](3.solution/d.decisions/decisions.md)
- [Guidance](3.solution/g.guidance/guidance.md)
- [Impacts](3.solution/i.impacts/impacts.md)
- [Risks](3.solution/r.risks/risks.md)
- [User Stories](3.solution/s.user.stories/user-stories.md)
