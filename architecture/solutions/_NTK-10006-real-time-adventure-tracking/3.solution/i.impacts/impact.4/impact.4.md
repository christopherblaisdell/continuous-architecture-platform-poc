<!-- PUBLISH -->
# Impact Assessment 4: svc-location-services (ENHANCED)

| Field | Value |
|-------|-------|
| Service | svc-location-services |
| Domain | Support |
| Change Type | Enhanced — geofence data source |
| Impact Level | LOW |
| Owner | Various |

## Overview

svc-location-services already has PostGIS with geospatial capabilities (boundary polygons, center points, GiST spatial indexes). The service becomes the authoritative source for geofence boundary data consumed by svc-adventure-tracking.

## API Contract Changes

No new endpoints required. The existing location data model already includes `boundary` (Polygon) and `center_point` (Point) fields. svc-adventure-tracking reads geofence boundaries either:

1. Via existing GET /locations endpoints (if geofences are modeled as locations), or
2. Via a new GET /geofences endpoint if geofence boundaries are separated from location records

The preferred approach is option 1 — model trail boundaries, restricted zones, and assembly points as location records with their boundary polygons. This reuses the existing PostGIS infrastructure without schema changes.

## Data Model Impact

No new tables. Existing `locations` table already supports:
- `boundary` (Polygon geometry) — stores the geofence polygon
- `center_point` (Point geometry) — stores the location center
- Location types already include `RANGER_STATION` and `HEADQUARTERS` — add `TRAIL_BOUNDARY`, `RESTRICTED_ZONE`, `ASSEMBLY_POINT` to the type enum

## Cross-Service Integration

| Consumer | Endpoint | Purpose |
|----------|----------|---------|
| svc-adventure-tracking | GET /locations?type=TRAIL_BOUNDARY | Load geofence boundaries for position evaluation |

## Quality Attributes

| Attribute | Assessment |
|-----------|-----------|
| Performance | Geofence queries are infrequent (loaded at session start, cached in tracking service) — no volume concern |
| Compatibility | Extending the location type enum is backward compatible (additive change) |
