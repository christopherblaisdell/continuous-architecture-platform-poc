# NTK-10004: Impact Assessment

## Affected Service: svc-scheduling-orchestrator

### API Changes

| Change | Type | Breaking |
|--------|------|----------|
| Add `PATCH /api/v1/schedules/{id}` endpoint | New endpoint | No |
| Deprecate `PUT /api/v1/schedules/{id}` endpoint | Deprecation | No (backward-compatible delegation) |
| Add `version` field to `DailySchedule` response | Additive | No |
| Add `If-Match` header requirement on PATCH | New requirement | No (only applies to new endpoint) |

### Data Model Changes

- New `version` column (BIGINT, NOT NULL, DEFAULT 0) on the `daily_schedules` table
- No changes to existing columns
- No data migration required for existing rows (DEFAULT 0 handles existing records)

### Behavior Changes

| Before | After |
|--------|-------|
| PUT replaces entire entity | PATCH updates only scheduling-owned fields |
| Last write wins silently | Optimistic locking detects concurrent writes |
| Guide enrichment data lost | Guide enrichment data preserved |
| No version tracking | Version incremented on each update |

## Affected Service: svc-guide-management

### Impact

No code changes required in svc-guide-management. The fix is entirely within svc-scheduling-orchestrator. However, svc-guide-management benefits from the fix because its enrichment data (guideNotes, guidePreferences) will no longer be overwritten.

## Downstream Impact

| Service | Impact |
|---------|--------|
| Optimization pipeline | Must handle 409 Conflict responses and implement retry logic |
| Nightly batch job | Must be updated to use PATCH instead of PUT |
| Region manager UI | If it triggers optimization via PUT, must be updated to use PATCH |
| svc-check-in | No impact — reads schedule data, does not write |
| svc-guide-management | Positive impact — enrichment data preserved |

## Safety Impact

| Before | After |
|--------|-------|
| Medical restrictions silently removed | Medical restrictions preserved through optimization |
| Certifications lost during optimization | Certifications preserved |
| Guides assigned to conflicting activities | Guides retain their qualification data for accurate assignment |
