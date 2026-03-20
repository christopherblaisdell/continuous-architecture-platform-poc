<!-- PUBLISH -->

# Impact Assessment: svc-safety-compliance

| | |
|-----------|-------|
| **Ticket** | NTK-10006 |
| **Service** | svc-safety-compliance |
| **Domain** | Safety |
| **Team** | Safety and Compliance Team |
| **Change Type** | New Event Consumer |

## Summary

svc-safety-compliance gains a new Kafka event consumer for `tracking.anomaly.detected`. When an anomaly is detected (geofence violation, SOS, signal loss), svc-safety-compliance auto-creates an incident record with GPS coordinates — enriching the audit trail beyond what manual incident reports provide.

## API Contract Changes

None. The existing `POST /incidents` endpoint and `Incident` schema already support the required fields. The new event consumer creates incidents internally using the same logic.

## Event Changes

**New event consumed:**

| Event | Channel | Action |
|-------|---------|--------|
| tracking.anomaly.detected | novatrek.safety.tracking.anomaly.detected | Auto-create incident record with GPS location, anomaly type, and session metadata |

**Field mapping:**

| Event Field | Incident Field |
|-------------|---------------|
| guest_id | guest_id |
| session_id | (stored in incident description as reference) |
| type (geofence_violation, sos, signal_loss, inactivity) | category (mapped to existing incident types) |
| severity | severity |
| location.latitude, location.longitude | location_id (resolved via svc-location-services) |

## Data Model Changes

None. The existing `incidents` table and `audit_log` table accommodate auto-created incidents. The `reported_by` field will contain "svc-adventure-tracking (automated)" to distinguish from manual reports.

## Regulatory Compliance

The 7-year retention policy on the `audit_log` table applies to tracking-generated incidents as well. Each auto-created incident is logged to the audit trail with full GPS coordinates and anomaly context, satisfying insurance tracking mandates.

## Risk

Low. The only risk is duplicate incident creation if both svc-adventure-tracking (via `POST /emergencies`) and svc-safety-compliance (via event consumption) attempt to create incidents for the same anomaly. Mitigation: svc-safety-compliance checks for existing incidents by session_id + anomaly timestamp before creating.
