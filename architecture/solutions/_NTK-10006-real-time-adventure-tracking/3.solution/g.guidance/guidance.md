# Implementation Guidance — NTK-10006

> This document is for the development team implementing svc-adventure-tracking.
> It describes HOW to build the solution. For WHY decisions were made, see decisions.md.
> For WHAT changes architecturally, see the impact assessments.

## Device Telemetry Ingest Pattern

The `POST /telemetry` endpoint is the high-frequency write path. Design it for minimal
processing latency:

1. Authenticate the device API key (hash comparison against stored hash)
2. Resolve the active session for the device ID (cache this mapping in Redis; session is
   looked up once at activation and invalidated when session ends)
3. Write the position record to the `position_telemetry` hypertable
4. Update the `last_position` on the `tracked_devices` record (in-place update)
5. Evaluate geofence and SOS flag (synchronous, fast path)
6. If emergency trigger conditions met, call svc-emergency-response asynchronously
   (do not block the 202 response)
7. Return 202 with `ingested: true` and `emergency_triggered: false` (or true)

The emergency call is async to ensure the device receives a fast acknowledgment even if
svc-emergency-response is temporarily slow.

## TimescaleDB Hypertable Configuration

Create the `position_telemetry` hypertable with a 1-day chunk interval:

```sql
CREATE TABLE position_telemetry (
    id UUID NOT NULL,
    session_id UUID NOT NULL REFERENCES adventure_sessions(id),
    device_id TEXT NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    altitude_meters DOUBLE PRECISION,
    accuracy_meters DOUBLE PRECISION,
    sos_flag BOOLEAN NOT NULL DEFAULT false,
    recorded_at TIMESTAMPTZ NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

SELECT create_hypertable('position_telemetry', 'ingested_at', chunk_time_interval => INTERVAL '1 day');

-- Compression after 30 days
ALTER TABLE position_telemetry SET (
    timescaledb.compress,
    timescaledb.compress_orderby = 'ingested_at DESC',
    timescaledb.compress_segmentby = 'session_id'
);

SELECT add_compression_policy('position_telemetry', INTERVAL '30 days');
```

## Geofence Evaluation

Use the PostGIS extension on the same PostgreSQL instance for geofence point-in-polygon evaluation:

```sql
-- Check if a point is outside the geofence polygon
SELECT NOT ST_Contains(
    ST_GeomFromGeoJSON(geofences.polygon_geojson),
    ST_SetSRID(ST_MakePoint($longitude, $latitude), 4326)
) AS is_outside
FROM geofences
WHERE id = $geofence_id;
```

For circular geofences, use `ST_DWithin` with the great-circle distance.

## Optimistic Locking on Adventure Sessions

The `_rev` field is a UUID generated on each write. Before updating session status:

1. Read the current `_rev`
2. Include `_rev` in the UPDATE WHERE clause
3. If rows affected is 0, return 409 Conflict

```sql
UPDATE adventure_sessions
SET status = $new_status, ended_at = $ended_at, _rev = gen_random_uuid()
WHERE id = $session_id AND _rev = $client_rev;
```

## Device API Key Storage

Store device API keys as bcrypt hashes (cost factor 10). The key is shown once at
provisioning time (wristband issuance) and cannot be retrieved thereafter.

```
api_keys table:
  id UUID PK
  device_id TEXT UNIQUE
  key_hash TEXT (bcrypt)
  created_at TIMESTAMPTZ
  last_used_at TIMESTAMPTZ
  revoked_at TIMESTAMPTZ nullable
```

On ingest: bcrypt compare the raw key from the header against `key_hash` where
`device_id` matches and `revoked_at IS NULL`.

## Staleness Alert

A scheduled job (every 5 minutes) queries:

```sql
SELECT session_id, MAX(ingested_at) as last_seen
FROM position_telemetry
WHERE ingested_at > NOW() - INTERVAL '1 day'
GROUP BY session_id
HAVING MAX(ingested_at) < NOW() - INTERVAL '15 minutes'
```

Any active session with no telemetry in 15 minutes triggers a safety officer notification
via svc-notifications. This is a warning, not an emergency — guides sometimes enter
coverage gaps.
