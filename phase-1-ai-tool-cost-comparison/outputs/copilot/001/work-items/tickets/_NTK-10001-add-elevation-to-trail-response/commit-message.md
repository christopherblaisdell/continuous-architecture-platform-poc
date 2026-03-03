# Commit Message for NTK-10001

```
feat(svc-trail-management): expose elevation data in trail API responses

NTK-10001: Add Elevation Data Fields to Trail Response

Update svc-trail-management OpenAPI specification to fully document the
elevation_gain_m and elevation_loss_m fields across all trail schemas.
Both fields are nullable per approved decision D1, allowing consumers to
distinguish between "no data available" (null) and "flat trail" (0).
Update component diagram to reflect the elevation data flow.

Changes:
- corporate-services/services/svc-trail-management.yaml
  - Bump version from 1.1.0 to 1.2.0
  - Add changelog entry documenting NTK-10001 changes
  - Trail schema: enhance elevation_gain_m and elevation_loss_m
    descriptions with nullability rationale and DB column mapping
  - Trail schema: add schema-level description referencing NTK-10001
  - CreateTrailRequest: add nullable annotation and description to
    elevation_gain_m (was missing)
  - CreateTrailRequest: enhance elevation_loss_m description
  - UpdateTrailRequest: add nullable annotations and descriptions
    to both elevation fields (were missing)
- corporate-services/diagrams/Components/novatrek-component-overview.puml
  - Update NTK-10001 note to include version reference (v1.2.0)
  - Add trip_catalog to trails dependency for difficulty assessment
  - Add header comment noting NTK-10001 elevation data flow update

Approved design: NTK-10001-solution-design.md (v1.0, APPROVED, 2024-04-15)
Backward compatible: Yes (additive nullable fields only)
Database migration: None required (elevation_gain_m and elevation_loss_m
  columns already exist in trails table, DECIMAL(8,2), nullable)
```
