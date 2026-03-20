<!-- PUBLISH -->

# NTK-10006 Capabilities

This document summarizes the capability changes introduced by NTK-10006. The single source of truth for capability changes is `architecture/metadata/capability-changelog.yaml`.

## Capabilities Affected

### CAP-3.3 — Emergency Response Coordination (Enhanced)

**Current state:** Emergency protocol activation, rescue dispatch, and communication coordination via svc-safety-compliance.

**After NTK-10006:** Emergency response is triggered automatically by real-time GPS anomaly detection. When svc-adventure-tracking detects a geofence violation, SOS signal, or signal loss, it calls `POST /emergencies` on svc-emergency-response with the guest's precise GPS coordinates. This eliminates the manual step of determining the guest's location before dispatching rescue.

**L3 Capabilities:**
- GPS-Triggered Emergency Dispatch — anomaly detection in svc-adventure-tracking automatically creates an emergency with precise coordinates
- Real-Time Location in Emergency Context — rescue teams receive the guest's last-known GPS position and can track updates during the response

### CAP-3.2 — Incident Reporting and Response (Enhanced)

**Current state:** Manual incident logging via `POST /incidents` on svc-safety-compliance.

**After NTK-10006:** Incidents are auto-created when `tracking.anomaly.detected` events are consumed by svc-safety-compliance. The incident record includes GPS coordinates, anomaly type, and session metadata — providing a richer audit trail than manual reports.

**L3 Capabilities:**
- Automated Incident Creation from Tracking Anomalies — svc-safety-compliance subscribes to `tracking.anomaly.detected` and creates incident records automatically
- GPS-Enriched Incident Records — incident reports include precise location data from the tracking session

### CAP-2.1 — Day-of-Adventure Check-In (Enhanced)

**Current state:** Guest arrival processing, identity verification, wristband assignment, safety briefing.

**After NTK-10006:** Check-in completion triggers a tracking session via the `checkin.completed` Kafka event. The wristband RFID tag (added by NTK-10005) serves as the correlation key between the guest's check-in record and their GPS tracking session. For Pattern 2/3 adventures, tracking activation is verified before the guest departs.

**L3 Capabilities:**
- Tracking Session Initiation at Check-In — `checkin.completed` event triggers svc-adventure-tracking to create a tracking session linked to the guest's wristband
- Tracking Verification Gate — Pattern 2/3 adventures require confirmed tracking session before guest departure (safety-first per ADR-005)
