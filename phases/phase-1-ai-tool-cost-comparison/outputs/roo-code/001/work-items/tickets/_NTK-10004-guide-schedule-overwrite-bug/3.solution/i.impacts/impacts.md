# NTK-10004: Impact Assessment

## Impacted Components

| Component | Impact Level | Changes Required |
|-----------|-------------|-----------------|
| svc-scheduling-orchestrator | PRIMARY | Replace PUT with PATCH semantics in `SchedulingService.updateSchedule()`. Create new `ScheduleUpdateRequest` DTO. Add `@Version` optimistic locking to `DailySchedule` entity. Add PATCH endpoint to `ScheduleController`. Deprecate/remove PUT endpoint. Add database migration for version column. |
| svc-scheduling-orchestrator (OpenAPI) | MODERATE | Add `PATCH /api/v1/schedules/{id}` to the service OpenAPI contract. Remove or deprecate the undocumented PUT endpoint. |
| svc-guide-management | INFORMATIONAL | No code changes required. This service is the data owner of `guideNotes` and `guidePreferences`. The fix ensures its data is no longer overwritten by the orchestrator. Verify that the guide-management PATCH endpoint for schedule updates works correctly. |
| Optimization pipeline | MODERATE | The nightly and on-demand optimization pipelines must be updated to call the new PATCH endpoint instead of PUT. Add retry logic with exponential backoff for HTTP 409 Conflict responses from optimistic locking. |
| Database (daily_schedules table) | LOW | Add `version BIGINT DEFAULT 0` column for optimistic locking. Non-breaking additive migration. |

## Operational Impact

| Category | Before Fix | After Fix |
|----------|-----------|-----------|
| Guide data loss | Enrichment data silently overwritten on every optimization cycle | Enrichment data preserved; only orchestrator-owned fields updated |
| Concurrent conflicts | Last write wins silently | Detected via optimistic locking; second writer receives HTTP 409 and retries |
| Audit trail | No visibility into who changed what | `lastModifiedBy` field identifies the modifying service; version field tracks revision count |
| Safety compliance | Medical restrictions silently removed | Medical restrictions preserved across optimization cycles |

## Data Recovery

Existing data that was lost prior to the fix cannot be automatically recovered. A manual process is required:

1. Identify guides who have logged complaints about lost data (tracked in ticket comments)
2. Have those guides re-enter their availability exceptions, notes, and preferences through the Guide Portal
3. After the fix is deployed, verify that the re-entered data survives the next optimization cycle

## Non-Impacted Components

All services not listed above are unaffected. The fix is internal to the scheduling orchestrator and its interaction with the daily_schedules data store. No API changes are visible to external consumers (kiosks, mobile apps).
