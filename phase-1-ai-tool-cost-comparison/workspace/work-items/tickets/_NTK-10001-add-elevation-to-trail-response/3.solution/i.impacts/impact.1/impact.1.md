# NTK-10001 - Impact 1: svc-trail-management

## Impacted Service

**svc-trail-management**

## What Changes

The Trail response DTO in svc-trail-management will be updated to include two new nullable fields:

- `elevation_gain_meters` (BigDecimal, nullable) - Total elevation gained along the trail in meters
- `elevation_loss_meters` (BigDecimal, nullable) - Total elevation lost along the trail in meters

These fields are mapped from the existing `elevation_gain_m` and `elevation_loss_m` columns in the `trails` database table.

## Affected Endpoints

| Endpoint | Method | Change |
|----------|--------|--------|
| /trails/{trail_id} | GET | Response includes new elevation fields |
| /trails | GET | Each trail object in the collection includes new elevation fields |

## API Contract Change

- **Change Type**: Additive only
- **Breaking Change**: No
- **New Fields**: `elevation_gain_meters`, `elevation_loss_meters`
- **Removed Fields**: None
- **Modified Fields**: None

## Database Impact

No database changes required. The `elevation_gain_m` and `elevation_loss_m` columns already exist in the `trails` table.

## Testing Requirements

- Unit tests for TrailMapper to verify new field mapping
- Unit tests for trail controller to verify fields present in response
- Integration test to confirm end-to-end field population from database to API response
