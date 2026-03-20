<!-- PUBLISH -->

# Impact Assessment: svc-emergency-response

| | |
|-----------|-------|
| **Ticket** | NTK-10006 |
| **Service** | svc-emergency-response |
| **Domain** | Safety |
| **Team** | Safety and Compliance Team |
| **Change Type** | No API Changes — New Integration Consumer |

## Summary

svc-emergency-response already has a complete OpenAPI spec that fully supports the NTK-10006 integration. No API contract changes are required. The service gains a new caller (svc-adventure-tracking) that uses the existing `POST /emergencies` endpoint to trigger emergencies from GPS anomaly detection.

## API Contract Changes

None. The existing `EmergencyRequest` schema already accepts:
- `guest_id` (UUID)
- `reservation_id` (UUID)
- `type` (enum: sos, medical, weather, wildlife, equipment_failure, lost_party)
- `severity` (enum: low, medium, high, critical)
- `location` (GeoLocation with latitude, longitude, altitude, accuracy, source)
- `reported_by` (string — will be "svc-adventure-tracking" for automated triggers)

The `GeoLocation.source` enum already includes `gps` and `wristband_nfc`, which are the sources svc-adventure-tracking will use.

## New Integration Point

| Caller | Method | Path | Trigger |
|--------|--------|------|---------|
| svc-adventure-tracking | POST | /emergencies | Anomaly detected (geofence violation, SOS, signal loss, inactivity) |

The `type` field maps to anomaly types:
- Geofence violation → `lost_party`
- SOS button → `sos`
- Signal loss → `lost_party` (severity escalated if prolonged)
- Inactivity → `medical` (precautionary)

## Event Impact

The `emergency.triggered` event published by svc-emergency-response already has consumers configured in events.yaml:
- svc-notifications (emergency alerts)
- svc-scheduling-orchestrator (guide awareness)
- svc-safety-compliance (incident logging)
- svc-analytics (reporting)

No event schema changes required.

## Risk

Minimal. The only consideration is increased call volume to `POST /emergencies` if anomaly detection thresholds are too sensitive. Configurable thresholds in svc-adventure-tracking mitigate this (false positive management is the caller's responsibility).
