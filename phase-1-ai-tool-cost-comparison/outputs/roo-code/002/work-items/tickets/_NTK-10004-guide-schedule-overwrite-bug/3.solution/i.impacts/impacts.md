# NTK-10004: Impact Assessment

## Impacted Components

| Component | Impact Level | Changes Required |
|-----------|-------------|------------------|
| svc-scheduling-orchestrator | PRIMARY | Replace PUT with PATCH semantics; add partial update DTO; add PATCH controller endpoint; deprecate PUT; add optimistic locking retry logic |
| svc-scheduling-orchestrator (data model) | PRIMARY | Add `@Version` field to `DailySchedule` entity; database migration to add `version` column |
| svc-scheduling-orchestrator (API contract) | MEDIUM | Document PATCH endpoint in OpenAPI spec; deprecate undocumented PUT endpoint |
| svc-guide-management | INFORMATIONAL | No changes required. The PATCH endpoint at `/api/v1/guides/{guideId}/schedule` already exists per ticket Comment 5 (Morgan Rivera). Verify it handles partial updates correctly. |
| Database (daily_schedules table) | LOW | Add `version` column (BIGINT, default 0) for optimistic locking |

## Operational Impact

| Impact Area | Before Fix | After Fix |
|-------------|-----------|-----------|
| Guide enrichment data loss | Occurs on every optimization cycle | Eliminated -- PATCH only updates orchestrator-owned fields |
| Concurrent write corruption | Silent data loss (last-write-wins) | Detected and retried via optimistic locking |
| Guide safety data (medical restrictions) | Silently removed by PUT overwrite | Preserved -- orchestrator cannot modify enrichment fields |
| Guide availability exceptions | Lost after optimization | Preserved |
| Guide certifications | Overwritten to null | Preserved |

## Downstream Effects

The following downstream impacts were observed in Elastic logs and are expected to be resolved by the fix:

| Downstream Service | Current Impact | Expected After Fix |
|-------------------|----------------|-------------------|
| Daily assignment generation | Guides incorrectly removed from assignments after losing certifications/skills | Assignments remain stable; certifications preserved |
| Guide Portal | Guides must re-enter lost data after each optimization | Data persists across optimization cycles |
| Operations management | Manual re-assignment required for incorrectly removed guides | No manual intervention needed |

## Non-Impacted Components

- svc-reservations: No changes
- svc-check-in: No changes
- svc-trip-catalog: No changes
- svc-trail-management: No changes
- All other NovaTrek services: No changes
