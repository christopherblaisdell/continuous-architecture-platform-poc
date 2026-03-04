# Commit Message

```
feat(svc-trail-management): add elevation profile data to trail response [NTK-10001]

Add elevation profile fields to the Trail schema in svc-trail-management
OpenAPI specification (v1.1.0 -> v1.2.0):

- Add max_elevation_m (nullable double) - peak elevation in meters
- Add min_elevation_m (nullable double) - lowest elevation in meters
- Add elevation_profile (nullable array of ElevationDataPoint) - ordered
  elevation measurements along the trail
- Add ElevationDataPoint schema (distance_km, elevation_m)
- Add elevation profile fields to UpdateTrailRequest schema
- Update novatrek-component-overview.puml with elevation data flow

Existing fields elevation_gain_m and elevation_loss_m were already present
in the Trail schema. No changes to those fields were required.

All additions are nullable and backward-compatible. No existing consumers
are affected. No database migration required - elevation data already
exists in the trails table.

Ticket: NTK-10001
Approved design: NTK-10001-solution-design.md v1.0
```
