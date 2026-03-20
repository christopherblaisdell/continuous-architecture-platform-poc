<!-- PUBLISH -->

# Impact Assessment: svc-adventure-tracking (NEW SERVICE)

| | |
|-----------|-------|
| **Ticket** | NTK-10006 |
| **Service** | svc-adventure-tracking |
| **Domain** | Safety |
| **Team** | Safety and Compliance Team |
| **Change Type** | New Service |

## Summary

New service responsible for real-time GPS location tracking of guests during active adventures. Manages tracking session lifecycle, ingests GPS coordinates from wristband hardware, monitors geofence boundaries, detects anomalies, and triggers emergency response when safety thresholds are breached.

## API Contract

New OpenAPI spec to be created at `architecture/specs/svc-adventure-tracking.yaml`.

**Endpoints:**

| Method | Path | Purpose |
|--------|------|---------|
| POST | /tracking-sessions | Create tracking session (internal, from checkin.completed) |
| GET | /tracking-sessions | List sessions with filters (status, date, adventure_category) |
| GET | /tracking-sessions/{id} | Get session details with latest location |
| PATCH | /tracking-sessions/{id} | Update session status (end, pause) |
| POST | /tracking-sessions/{id}/locations | Ingest GPS coordinate from wristband |
| GET | /tracking-sessions/{id}/locations | Get location history |
| GET | /tracking-sessions/active | All active sessions with latest coordinates (ops dashboard) |
| POST | /geofences | Create geofence boundary |
| GET | /geofences | List geofences |
| GET | /geofences/{id} | Get geofence details |

## Data Model

**Schema:** `tracking`
**Engine:** PostgreSQL 15

| Table | Key Columns | Volume |
|-------|------------|--------|
| tracking_sessions | session_id (PK), wristband_nfc_id (UNIQUE while active), reservation_id, guest_id, adventure_category, trail_id, status, started_at, ended_at, _rev | ~500 active at peak |
| location_updates | update_id (PK), session_id (FK), latitude, longitude, altitude_meters, accuracy_meters, source, recorded_at | ~1,000/min peak; 1-year retention |
| geofences | geofence_id (PK), trail_id, name, boundary_polygon (JSONB), active | ~50 (one per trail) |
| anomaly_events | anomaly_id (PK), session_id (FK), type, severity, detected_at, resolved_at, emergency_id (FK nullable) | Low volume — anomalies are exceptional |

**Indexes Required:**
- `idx_session_wristband` — UNIQUE on (wristband_nfc_id) WHERE status = 'active'
- `idx_location_session_time` — (session_id, recorded_at DESC) for location history queries
- `idx_location_recorded_at` — for time-series partitioning and retention cleanup
- `idx_session_status` — for active session listing

**Partitioning:** `location_updates` should be time-partitioned by month on `recorded_at` for query performance and retention management.

## Events Published

| Event | Channel | Payload |
|-------|---------|---------|
| tracking.session.started | novatrek.safety.tracking.session.started | session_id, guest_id, reservation_id, wristband_nfc_id, adventure_category, started_at |
| tracking.session.ended | novatrek.safety.tracking.session.ended | session_id, guest_id, ended_at, duration_minutes, location_count |
| tracking.location.updated | novatrek.safety.tracking.location.updated | session_id, latitude, longitude, accuracy_meters, recorded_at |
| tracking.anomaly.detected | novatrek.safety.tracking.anomaly.detected | anomaly_id, session_id, guest_id, type, severity, location, detected_at |

## Events Consumed

| Event | Channel | Action |
|-------|---------|--------|
| checkin.completed | novatrek.operations.checkin.completed | Create tracking session linked to wristband_nfc_id |

## Cross-Service Calls (Outbound)

| Target | Method | Path | Purpose |
|--------|--------|------|---------|
| svc-emergency-response | POST | /emergencies | Trigger emergency on anomaly detection |
| svc-location-services | GET | /trails/{id}/boundary | Retrieve geofence boundary polygon |
| svc-check-in | GET | /check-ins?rfid_tag={tag} | Resolve wristband to guest identity (fallback if event payload incomplete) |

## Infrastructure

| Resource | Specification |
|----------|--------------|
| Azure Container App | 0.25 CPU, 0.5Gi memory, min 0 / max 4 replicas |
| Azure Database for PostgreSQL Flexible Server | Shared with NovaTrek cluster |
| Kafka topics | 4 new topics (tracking.session.started, .ended, .location.updated, .anomaly.detected) |
| WebSocket | /ws/tracking endpoint for real-time map (requires sticky sessions or external WebSocket gateway) |
