# Commit Message for NTK-10001

```
feat(svc-trail-management): add elevation loss data to trail API responses

NTK-10001: Add Elevation Profile Data to Trail Response

Add `elevation_loss_m` field to Trail, CreateTrailRequest, and
UpdateTrailRequest schemas in svc-trail-management OpenAPI spec.
Enhance existing `elevation_gain_m` field with description.
Update component overview diagram to reflect new elevation data flow.

Changes:
- corporate-services/services/svc-trail-management.yaml
  - Trail schema: add `elevation_loss_m` (number, double, nullable)
  - Trail schema: add description to existing `elevation_gain_m`
  - CreateTrailRequest: add `elevation_loss_m` field
  - UpdateTrailRequest: add `elevation_loss_m` field
- corporate-services/diagrams/Components/novatrek-component-overview.puml
  - Add NTK-10001 note on svc-trail-management component
  - Update scheduling→trails dependency label to include elevation data

Approved solution design: NTK-10001-solution-design.md (v1.0, APPROVED)
Backward compatible: Yes (additive fields only, nullable)
Database migration: None required (data exists in trails table)
```
