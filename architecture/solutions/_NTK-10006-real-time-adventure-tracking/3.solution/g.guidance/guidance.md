<!-- PUBLISH -->

# NTK-10006 Implementation Guidance

## Phased Delivery Recommendation

Given the scope (new service + 4 integration points), a phased delivery is recommended:

### Phase A: Core Tracking Service

1. Create `svc-adventure-tracking` OpenAPI spec
2. Scaffold service using `scripts/generate-service-scaffold.py`
3. Implement tracking session CRUD and location ingestion (POST /tracking-sessions/{id}/locations)
4. Implement `checkin.completed` Kafka consumer to auto-create tracking sessions
5. Deploy to Azure Container Apps (follow Wave 0-6 pattern)
6. Add BDD scenarios for tracking session lifecycle

### Phase B: Anomaly Detection and Emergency Integration

1. Implement geofence monitoring (point-in-polygon check against boundary_polygon JSONB)
2. Implement signal-loss detection (background task checking last update timestamp)
3. Implement SOS signal handling
4. Wire anomaly detection to `POST /emergencies` on svc-emergency-response
5. Publish `tracking.anomaly.detected` events to Kafka
6. Add svc-safety-compliance consumer for auto-incident creation
7. Add BDD scenarios for each anomaly type

### Phase C: Ops Dashboard Integration

1. Implement `GET /tracking-sessions/active` for bulk location retrieval
2. Add WebSocket endpoint (`/ws/tracking`) for real-time location streaming
3. Integrate with web-ops-dashboard (reference `live-tracking.excalidraw` wireframe)
4. Add `tracking_session_id` to svc-check-in's CheckIn response schema

## Configuration

Tracking thresholds should be configurable per adventure category in `config/adventure-classification.yaml`:

```yaml
tracking:
  default_update_interval_seconds: 30
  signal_loss_warning_minutes: 5
  signal_loss_emergency_minutes: 15
  geofence_warning_buffer_meters: 50
  geofence_emergency_delay_minutes: 2
  
overrides:
  pattern_1:  # Low-risk: basic self-check-in
    tracking_required: false
    signal_loss_warning_minutes: 10
  pattern_2:  # Medium-risk: guided
    tracking_required: true
    signal_loss_warning_minutes: 5
  pattern_3:  # High-risk: full service  
    tracking_required: true
    signal_loss_warning_minutes: 3
    signal_loss_emergency_minutes: 10
```

## Geofence Implementation

Use PostgreSQL's geometry functions for point-in-polygon checks:

```sql
-- Check if a GPS coordinate is within the geofence boundary
SELECT geofence_id, name 
FROM geofences 
WHERE active = true 
  AND trail_id = :trail_id
  AND NOT ST_Contains(
    ST_GeomFromGeoJSON(boundary_polygon::text),
    ST_SetSRID(ST_MakePoint(:longitude, :latitude), 4326)
  );
```

This requires the PostGIS extension. If PostGIS is not available, a simpler approach is to use Java's `java.awt.geom.Path2D` for in-memory polygon containment checks with the boundary loaded from the JSONB column.

## Data Retention

| Data | Retention | Archive Target |
|------|----------|---------------|
| Location coordinates | 1 year rolling | Azure Blob Storage (cold tier) |
| Tracking sessions | 1 year rolling | Azure Blob Storage (cold tier) |
| Anomaly events | 7 years | Azure Blob Storage (archive tier) |
| Audit log entries | 7 years | Azure Blob Storage (archive tier) |

Implement retention using PostgreSQL table partitioning by month on `location_updates.recorded_at`. A scheduled job drops partitions older than 12 months after archiving to Blob Storage.
