# Impact Assessment — svc-adventure-tracking (NEW SERVICE)

| Field | Value |
|-------|-------|
| Service | svc-adventure-tracking |
| Impact Level | PRIMARY |
| Change Type | New Service |
| Owner | Safety and Compliance Team |

## Overview

svc-adventure-tracking is a new microservice that owns the full lifecycle of adventure tracking
sessions: activation at adventure start, real-time GPS telemetry ingestion, geofence evaluation,
automated emergency triggering, and telemetry retention for post-incident investigation.

## API Contract

**New OpenAPI spec**: `architecture/specs/svc-adventure-tracking.yaml`

### Endpoints Introduced

| Method | Path | Purpose |
|--------|------|---------|
| POST | /sessions | Activate a tracking session for a completed check-in group |
| GET | /sessions | List active adventure sessions (operations dashboard) |
| GET | /sessions/{session_id} | Get session details including last positions |
| PATCH | /sessions/{session_id} | Update session status (completed, abandoned) |
| GET | /sessions/{session_id}/positions | Retrieve telemetry history for incident investigation |
| POST | /telemetry | Ingest GPS position update from wristband or mobile device |
| GET | /geofences | List geofence boundaries |
| POST | /geofences | Create a geofence boundary for an adventure area |
| GET | /geofences/{geofence_id} | Get geofence definition |
| DELETE | /geofences/{geofence_id} | Delete a geofence boundary |

## Data Model

**Database**: PostgreSQL 15 with TimescaleDB extension

**Schema**: adventure_tracking

**Tables**:

| Table | Type | Purpose |
|-------|------|---------|
| adventure_sessions | Standard relational | Session state, party composition, status |
| tracked_devices | Standard relational | Device-to-session mapping (wristband, mobile, beacon) |
| position_telemetry | TimescaleDB hypertable | High-frequency GPS telemetry (partitioned by time) |
| geofences | Standard relational | Geofence boundary definitions per trip type |

**Key columns — adventure_sessions**:

- `id` (UUID, PK)
- `check_in_id` (UUID, cross-ref svc-check-in)
- `reservation_id` (UUID, cross-ref svc-reservations)
- `trip_id` (UUID, cross-ref svc-trip-catalog)
- `guide_id` (UUID, nullable, cross-ref svc-guide-management)
- `status` (ENUM: active, completed, emergency, abandoned)
- `party_size` (INTEGER)
- `geofence_id` (UUID, nullable, FK to geofences)
- `emergency_incident_id` (UUID, nullable, cross-ref svc-emergency-response)
- `started_at` (TIMESTAMPTZ)
- `ended_at` (TIMESTAMPTZ, nullable)
- `_rev` (TEXT, optimistic locking token)

**Key columns — position_telemetry** (TimescaleDB hypertable, partitioned by `ingested_at`):

- `id` (UUID, PK)
- `session_id` (UUID, FK to adventure_sessions)
- `device_id` (TEXT, wristband RFID or app UUID)
- `latitude` (DOUBLE PRECISION)
- `longitude` (DOUBLE PRECISION)
- `altitude_meters` (DOUBLE PRECISION, nullable)
- `accuracy_meters` (DOUBLE PRECISION, nullable)
- `sos_flag` (BOOLEAN, default false)
- `recorded_at` (TIMESTAMPTZ, client-reported timestamp)
- `ingested_at` (TIMESTAMPTZ, server-stamped, used as hypertable partition key)

**Retention policy**: Compress chunks older than 30 days; archive to Azure Blob Storage after 90 days.

## Authentication Model

Two distinct authentication schemes:

| Scheme | Consumers | Credential | Scope |
|--------|-----------|-----------|-------|
| BearerAuth (JWT) | Operations dashboard, safety officers, svc-check-in | Short-lived JWT from identity provider | All session and geofence endpoints |
| DeviceApiKey | Wristband devices, mobile apps, satellite beacons | Long-lived API key, provisioned at device issuance | POST /telemetry only |

Device API keys are stored hashed. Key rotation is triggered via ops tooling (out of scope for this
service's API — handled by a provisioning workflow).

## Cross-Service Calls Made by svc-adventure-tracking

| Called Service | Endpoint | Purpose | Failure Mode |
|----------------|----------|---------|-------------|
| svc-emergency-response | POST /emergencies | Create emergency on SOS or geofence violation | Retry with exponential backoff; if unreachable, queue for retry and alert safety officer via svc-notifications directly |

## Cross-Service Consumers of svc-adventure-tracking

| Consumer | Endpoint | Purpose |
|----------|----------|---------|
| svc-check-in | POST /sessions | Activate tracking session on ADVENTURE_STARTED |
| Operations dashboard (web-ops-dashboard) | GET /sessions | Live position map |
| svc-safety-compliance | GET /sessions/{id}/positions | Telemetry trail for incident reports |

## Backward Compatibility

This is a new service. There are no existing consumers to maintain backward compatibility with.
