# Commit Message for NTK-10001

```
feat(svc-trail-management): add elevation response fields per NTK-10001

Add elevation_gain_meters and elevation_loss_meters as nullable numeric
fields to the Trail response schema in the OpenAPI specification. These
fields are mapped from the existing elevation_gain_m and elevation_loss_m
database columns via the TrailMapper.

Changes:
- svc-trail-management.yaml: Add elevation_gain_meters and
  elevation_loss_meters to Trail schema with nullable annotations,
  descriptions, and examples. Bump API version from 1.1.0 to 1.2.0.
- novatrek-component-overview.puml: Update NTK-10001 annotation on
  svc-trail-management to reflect the new DTO field names.

This is an additive-only change. No existing fields are modified or
removed. No database migration required. Backward compatible with all
existing consumers.

Ticket: NTK-10001
```
