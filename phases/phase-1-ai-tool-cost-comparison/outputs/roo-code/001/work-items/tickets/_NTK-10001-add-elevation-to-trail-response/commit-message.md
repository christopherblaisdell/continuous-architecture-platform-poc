# Commit Message

```
feat(svc-trail-management): add elevation profile data to trail response [NTK-10001]

Add elevation profile fields to the Trail schema in svc-trail-management
OpenAPI specification (v1.1.0 -> v1.2.0):

- Add max_elevation_m (nullable double) to Trail, CreateTrailRequest,
  and UpdateTrailRequest schemas
- Add min_elevation_m (nullable double) to Trail, CreateTrailRequest,
  and UpdateTrailRequest schemas
- Add elevation_profile (nullable array of ElevationDataPoint) to Trail,
  CreateTrailRequest, and UpdateTrailRequest schemas
- Add new ElevationDataPoint schema with distance_from_start_km and
  elevation_m fields

Existing elevation_gain_m and elevation_loss_m fields were already present
in the spec; no changes needed for those.

Update novatrek-component-overview.puml to reflect elevation data flow
from svc-trail-management to svc-scheduling-orchestrator.

All new fields are nullable for backward compatibility. No existing
consumers are affected.

Refs: NTK-10001
Approved-by: Solution Architecture
```
