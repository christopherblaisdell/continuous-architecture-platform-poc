<!-- CONFLUENCE-PUBLISH -->

# NTK-10004 - Solution Design: Guide Schedule Overwrite Bug

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Date | 2026-03-04 |
| Author | Solution Architecture (AI-Assisted) |
| Status | DRAFT |
| Ticket | NTK-10004 |
| Priority | HIGH |

## Problem Statement

Guides at NovaTrek report that manually entered data -- availability exceptions, training blocks, medical restrictions, certification notes, and language skills -- disappear after the svc-scheduling-orchestrator runs optimization cycles. This has been confirmed across Cascadia, Sierra, and Appalachian regions.

The root cause is an **architectural data ownership boundary violation**: svc-scheduling-orchestrator uses `PUT` (full entity replacement) semantics when updating guide schedules, overwriting fields it does not own. A secondary issue is the absence of concurrency control, which allows simultaneous regional optimizations to overwrite each other.

This is a CRITICAL safety concern: medical restrictions (e.g., altitude limitations) are silently removed, potentially leading to unsafe guide assignments.

## Root Cause Summary

### Primary: Data Ownership Violation

The `SchedulingService.updateSchedule()` method (lines 52-64) calls `scheduleRepository.save(incoming)` with a `DailySchedule` entity deserialized from the API request. The incoming entity does not contain guide enrichment fields (`guideNotes`, `guidePreferences`), so JPA persists null values that overwrite existing data.

The `DailySchedule` entity conflates two ownership domains in a single table:

| Field Group | Owner | Examples |
|-------------|-------|----------|
| Scheduling fields | svc-scheduling-orchestrator | guideId, tripId, startTime, endTime, status |
| Enrichment fields | svc-guide-management | guideNotes, guidePreferences, certifications |

### Secondary: No Concurrency Control

No `@Version` field, no ETag support, no conditional writes. Concurrent regional optimizations result in last-write-wins with no detection. Elastic logs confirm a 47ms race window for guide G-4821.

### Contributing: Undocumented Endpoint

The `PUT /api/v1/schedules/{id}` endpoint is not in the OpenAPI contract -- it exists only as a Spring Boot controller mapping, bypassing API governance.

## Evidence

| Source | Finding |
|--------|---------|
| Elastic ERROR logs (4 entries, 2025-02-12) | Guide enrichment data overwritten for G-4821, G-5190, G-3302 via PUT requests |
| Elastic concurrent PUT detection | 47ms window between concurrent PUTs for G-4821 (traceIds: abc-1001-def-2001, abc-1001-def-2002) |
| Source code: SchedulingService.java line 57 | `scheduleRepository.save(incoming)` -- full entity replacement with null enrichment fields |
| Source code: DailySchedule.java | `guideNotes` and `guidePreferences` annotated as vulnerable to overwrite |
| Source code: ScheduleController.java | Only PUT endpoint exposed; no PATCH endpoint |
| GitLab MR history | No existing MR addresses this bug; PUT semantics are the original implementation |
| Ticket comments (Sam Patel) | 3 confirmed incidents across 3 regions; HR escalations from affected guides |

## Solution Overview

### Phase 1: Immediate Fix (Sprint 19/20)

1. **Switch from PUT to PATCH semantics**: Modify `SchedulingService.updateSchedule()` to update only orchestrator-owned fields via a partial update DTO
2. **Add PATCH controller endpoint**: New `@PatchMapping("/{id}")` in `ScheduleController.java`
3. **Add optimistic locking**: Add `@Version` to `DailySchedule` entity with retry logic
4. **Deprecate PUT endpoint**: Add deprecation headers; do not remove immediately

### Phase 2: Architectural Improvement (Sprint 21+)

5. **Document data ownership contracts**: Field ownership annotations and OpenAPI spec updates
6. **Add enrichment nullification alerts**: Monitoring for enrichment field transitions to null
7. **Consider table separation**: Split into `schedule_assignments` and `guide_schedule_metadata`

## Architecture Decisions

- **ADR-NTK10004-001**: PATCH semantics with field-level ownership (Accepted)
- **ADR-NTK10004-002**: Optimistic locking via `@Version` field (Accepted)

See [Decisions](3.solution/d.decisions/decisions.md) for full MADR-formatted ADRs.

## Impacted Components

| Component | Impact Level | Change Summary |
|-----------|-------------|----------------|
| svc-scheduling-orchestrator | PRIMARY | PATCH endpoint, partial DTO, optimistic locking, retry logic |
| svc-scheduling-orchestrator (data model) | PRIMARY | `@Version` field, database migration |
| svc-guide-management | INFORMATIONAL | No changes required; PATCH endpoint already exists |

## Related Artifacts

- [Investigation](3.solution/c.current.state/investigations.md)
- [Decisions](3.solution/d.decisions/decisions.md)
- [Guidance](3.solution/g.guidance/guidance.md)
- [Impacts](3.solution/i.impacts/impacts.md)
- [Risks](3.solution/r.risks/risks.md)
- [User Stories](3.solution/s.user.stories/user-stories.md)
