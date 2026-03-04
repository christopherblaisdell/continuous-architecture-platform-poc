# NTK-10004: Guide Schedule Overwrite Bug - Solution Design

**Ticket**: NTK-10004 — Guide Schedule Manual Adjustments Lost After Optimization
**Version**: v1.0
**Date**: 2026-03-04
**Status**: Proposed

## 1 Problem Statement

Trail guides at NovaTrek enter schedule information — vacation blocks, training days, medical restrictions, group size overrides, and notes — through the Guide Portal backed by svc-guide-management. When svc-scheduling-orchestrator runs its nightly or on-demand optimization cycle, all manually entered data is silently discarded. This occurs because the orchestrator uses full entity replacement (PUT semantics) when writing optimized schedules back to the database, overwriting fields it does not own.

This is a CRITICAL safety concern: medical restrictions (e.g., "No high-altitude trails until medical clearance") are being silently removed, potentially leading to unsafe guide assignments.

## 2 Root Cause

### Primary: Data Ownership Boundary Violation

The `SchedulingService.updateSchedule()` method in `SchedulingService.java` (lines 54-64) calls `scheduleRepository.save(incoming)` with full entity replacement. The `incoming` entity is deserialized from the API request, which does not include enrichment fields like `guideNotes` and `guidePreferences`. JPA saves the entire entity, setting these fields to null.

The `DailySchedule` JPA entity conflates two distinct data ownership domains:

| Field Group | Owner | Example Fields |
|-------------|-------|----------------|
| Scheduling fields | svc-scheduling-orchestrator | guideId, tripId, startTime, endTime, status |
| Enrichment fields | svc-guide-management | guideNotes, guidePreferences |

### Secondary: No Concurrency Control

The `DailySchedule` entity has no `@Version` annotation. Concurrent optimization runs (e.g., nightly batch across regions) result in last-write-wins with no conflict detection. Elastic logs confirm a 47ms race window between concurrent PUTs for guide G-4821.

### Contributing: Undocumented Endpoint

The `PUT /api/v1/schedules/{id}` endpoint exists only as a Spring Boot controller mapping. It is not documented in the service's OpenAPI contract, bypassing API governance.

## 3 Evidence

### Elastic Logs

Four ERROR entries from 2025-02-12 confirm enrichment data loss:
- Guide G-4821: Lost certifications (ROPE_COURSE, ZIPLINE_ADVANCED)
- Guide G-4821: Concurrent PUT detected within 47ms window
- Guide G-5190: Lost specializations (WILDLIFE_EXPERT, FIRST_AID_CERTIFIED)
- Guide G-3302: Lost language skills (SPANISH, PORTUGUESE)

### Source Code

- `SchedulingService.java` line 62: `scheduleRepository.save(incoming)` — full entity replacement
- `DailySchedule.java`: `guideNotes` and `guidePreferences` fields marked as overwrite-vulnerable
- `ScheduleController.java`: Only PUT endpoint exposed, no PATCH

### GitLab MR History

No MR exists addressing this issue. The PUT-based update was the original implementation.

## 4 Proposed Solution

### 4.1 Switch to PATCH Semantics

Modify `SchedulingService.updateSchedule()` to:
1. Load the existing entity from the database
2. Update ONLY scheduling-owned fields (guideId, tripId, startTime, endTime, status)
3. Preserve all enrichment fields (guideNotes, guidePreferences)
4. Save the merged entity

Create a `DailyScheduleUpdateRequest` DTO containing only scheduling-owned fields to enforce the boundary at the API layer.

### 4.2 Add Optimistic Locking

Add `@Version` annotation to `DailySchedule` entity:
- JPA automatically increments the version on each save
- Concurrent writes with stale versions receive HTTP 409 Conflict
- The optimization pipeline handles 409 with retry-and-merge strategy (max 3 retries, exponential backoff)

### 4.3 Deprecate PUT Endpoint

- Add `@Deprecated` annotation to the existing PUT endpoint
- Internally delegate PUT calls to the PATCH logic for safety
- Log deprecation warnings for migration tracking
- Plan removal after all callers are migrated

### 4.4 Update OpenAPI Contract

Add `PATCH /api/v1/schedules/{id}` to `svc-scheduling-orchestrator.yaml` with proper documentation of field ownership and optimistic locking headers.

## 5 Affected Services

| Service | Impact | Changes |
|---------|--------|---------|
| svc-scheduling-orchestrator | PRIMARY | New PATCH endpoint, deprecate PUT, add @Version, update DTO |
| svc-guide-management | POSITIVE (no code changes) | Enrichment data no longer overwritten |
| Optimization pipeline | MEDIUM | Must use PATCH, handle 409 conflicts with retry |

## 6 Quality Attributes (ISO 25010)

| Attribute | Assessment |
|-----------|------------|
| Reliability | CRITICAL improvement — eliminates silent data loss and data corruption from concurrent writes |
| Functional Suitability | Fixes a correctness defect — enrichment data is preserved as expected |
| Compatibility | Backward-compatible — deprecated PUT delegates to PATCH; no breaking changes |
| Maintainability | Improved — clear data ownership boundary enforced by DTO; field ownership documented |
| Security | Improved — medical safety restrictions no longer silently removed |

## 7 Timeline

| Phase | Sprint | Deliverable |
|-------|--------|-------------|
| Immediate fix | Sprint 19-20 | PATCH endpoint, @Version optimistic locking, deprecate PUT |
| Caller migration | Sprint 20-21 | Migrate all internal PUT consumers to PATCH |
| Monitoring | Sprint 20+ | Enrichment preservation metrics, conflict tracking |
| Entity separation (future) | Sprint 22+ | Consider splitting DailySchedule into separate tables per ownership domain |
