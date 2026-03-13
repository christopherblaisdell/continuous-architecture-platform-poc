# Impact Assessment — svc-emergency-response

| Field | Value |
|-------|-------|
| Service | svc-emergency-response |
| Impact Level | LOW |
| Change Type | New consumer integration (programmatic calls from svc-adventure-tracking) |
| Owner | Safety and Compliance Team |

## Overview

svc-emergency-response already has an API contract and dispatch workflow. This solution
adds a new programmatic consumer: svc-adventure-tracking calls `POST /emergencies` when
an SOS signal or geofence violation is detected. No changes to the svc-emergency-response
API contract or data model are required.

## API Contract Changes

None. The existing `POST /emergencies` endpoint is consumed as-is.

### Existing Endpoint: POST /emergencies

svc-adventure-tracking calls this endpoint with the following field population:

| Field | Value |
|-------|-------|
| `source` | `system` (automated trigger from tracking service) |
| `trigger_type` | `sos_signal` or `geofence_violation` |
| `location.latitude` | Last known latitude from position telemetry |
| `location.longitude` | Last known longitude from position telemetry |
| `guest_ids` | Guest IDs of all party members from the tracking session |
| `tracking_session_id` | Reference to the svc-adventure-tracking session |
| `severity` | `critical` for SOS; `high` for geofence violation (before safety officer review) |

NOTE: If the `POST /emergencies` request body schema does not currently support
`tracking_session_id` or `source: system`, the schema requires a minor additive extension.
See the svc-emergency-response OpenAPI spec for current field definitions. This is a
backward-compatible addition (new nullable fields).

## Data Model Changes

None in svc-emergency-response. The `tracking_session_id` field is added as an optional
metadata field to the Emergency schema if not already present.

## Integration Point

The integration is one-directional: svc-adventure-tracking → svc-emergency-response.
svc-emergency-response does not call back to svc-adventure-tracking.

The emergency incident ID returned by `POST /emergencies` is stored in the
adventure session record (`emergency_incident_id` on `adventure_sessions`) by
svc-adventure-tracking for cross-reference.

## Backward Compatibility

All changes to svc-emergency-response are additive (new optional request body fields).
Existing callers of `POST /emergencies` (human-initiated SOS via ops dashboard) are
unaffected.
