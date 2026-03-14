<!-- PUBLISH -->
# Impact Assessment 1: svc-adventure-tracking (NEW)

| Field | Value |
|-------|-------|
| Service | svc-adventure-tracking |
| Domain | Operations |
| Change Type | New service |
| Impact Level | PRIMARY |
| Owner | NovaTrek Operations Team |

## Overview

svc-adventure-tracking is a new service that manages real-time GPS tracking of guests on active adventures. It is the primary data ingestion point for GPS position updates from wristband devices.

## API Contract

New OpenAPI specification: `architecture/specs/svc-adventure-tracking.yaml` (v1.0.0)

### Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | /tracking-sessions | List active tracking sessions (dashboard) |
| POST | /tracking-sessions | Create tracking session (from checkin.completed event) |
| GET | /tracking-sessions/{session_id} | Get session details with last position |
| PATCH | /tracking-sessions/{session_id} | Update session status (complete/terminate) |
| GET | /tracking-sessions/{session_id}/positions | Position history (compliance records) |
| POST | /positions | Report a GPS position update |
| POST | /positions/batch | Report buffered position batch |
| GET | /geofences | List geofences |
| POST | /geofences | Create a geofence boundary |
| GET | /live-stream | SSE stream for live position updates |

### Key Schemas

- **TrackingSession** — session lifecycle (ACTIVE, COMPLETED, TERMINATED), links guest to rfid_tag, tracks frequency by pattern
- **PositionReport** — GPS coordinates with accuracy, speed, heading, battery, SOS flag
- **Geofence** — GeoJSON polygon boundaries with type classification and buffer distance

## Data Model

| Table | Purpose | Volume |
|-------|---------|--------|
| tracking_sessions | Active and historical tracking sessions | ~500/day peak |
| positions | GPS position updates (time-series) | ~50,000/day peak |
| geofences | Trail boundaries and restricted zones | ~100 static |

**Database:** PostgreSQL 15 with PostGIS for geospatial queries (geofence evaluation, bounding box filters).

**Retention:** 90 days for position data (insurance compliance), then archived.

## Event Integration

### Consumes

| Event | Source | Action |
|-------|--------|--------|
| checkin.completed | svc-check-in | Create tracking session with rfid_tag, adventure_category, check_in_pattern |
| reservation.status-changed (COMPLETED) | svc-reservations | Terminate tracking session |

### Produces

| Event | Channel | Trigger |
|-------|---------|---------|
| position.updated | novatrek.tracking.position.updated | Every GPS position received |
| geofence.breach | novatrek.tracking.geofence.breach | Guest exits trail boundary |
| sos.triggered | novatrek.tracking.sos.triggered | SOS flag on position report |

## Cross-Service Dependencies

| Target Service | Integration | Direction |
|---------------|-------------|-----------|
| svc-emergency-response | POST /emergencies | Outbound (on SOS or geofence breach) |
| svc-location-services | GET /locations (geofence data) | Outbound (read) |
| svc-notifications | POST /notifications | Outbound (geofence breach alerts) |

## Quality Attributes

| Attribute | Assessment |
|-----------|-----------|
| Performance | Must handle 50,000 position writes/day with sub-100ms acknowledgment |
| Reliability | Position loss is acceptable if buffered and retransmitted; SOS must never be lost |
| Security | Position data is PII — encryption at rest, access logging, role-based access |
| Maintainability | Tracking frequency configurable via YAML — no code change for tuning |
