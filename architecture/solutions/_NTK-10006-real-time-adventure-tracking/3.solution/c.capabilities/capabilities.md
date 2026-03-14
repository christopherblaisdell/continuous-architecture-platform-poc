<!-- PUBLISH -->
# NTK-10006 Capabilities

This document summarizes the capability changes for the Real-Time Adventure Tracking and Emergency Alerting solution. The authoritative capability data is recorded in `architecture/metadata/capability-changelog.yaml`.

## Affected Capabilities

### CAP-2.1 — Day-of-Adventure Check-In (Enhanced)

Check-in completion now serves as the trigger event for real-time tracking activation. The existing `checkin.completed` event (which already carries `rfid_tag` from NTK-10005) is consumed by svc-adventure-tracking to create a tracking session. No changes to svc-check-in itself are required — the event contract is already sufficient.

**L3 Capabilities Emerging:**
- **Tracking Session Activation** — Check-in completion automatically initiates GPS tracking based on adventure classification pattern

### CAP-3.2 — Incident Reporting and Response (Enhanced)

Incidents can now be auto-generated from tracking system events (SOS triggers, geofence breaches) in addition to manual reporting. svc-emergency-response creates structured incident records with precise GPS coordinates, reducing the time from event to documented incident.

**L3 Capabilities Emerging:**
- **Automated Incident Generation from Tracking Events** — SOS signals and geofence breaches create incident records with GPS coordinates without manual intervention
- **Location-Enriched Incident Records** — Every tracking-generated incident includes precise latitude, longitude, altitude, and nearest landmark

### CAP-3.3 — Emergency Response Coordination (Enhanced)

Emergency response now includes a full lifecycle: detection (SOS, geofence breach, weather alert) through dispatch (nearest rescue team assignment) through resolution (timeline tracking, multi-channel notifications). svc-emergency-response orchestrates the response workflow with real-time location data from svc-adventure-tracking.

**L3 Capabilities Emerging:**
- **SOS-Triggered Emergency Response** — Wristband SOS button or mobile app SOS initiates full emergency workflow with automatic dispatch
- **Proximity-Based Rescue Dispatch** — Nearest available rescue team is identified using geospatial distance calculation
- **Weather-Triggered Evacuation Coordination** — Severe weather alerts automatically identify affected guests and initiate evacuation notifications
- **Emergency Response Timeline** — Every emergency maintains an append-only timeline (triggered, dispatched, acknowledged, en_route, on_scene, resolved) for audit and insurance compliance
- **Multi-Channel Emergency Notification** — URGENT notifications sent simultaneously via SMS, push, and in-app channels to guides, staff, and emergency contacts

### CAP-7.2 — Geospatial and Location Services (Enhanced)

svc-location-services gains geofence evaluation responsibilities. Trail boundaries and restricted zones are evaluated against real-time guest positions to detect breaches.

**L3 Capabilities Emerging:**
- **Real-Time Geofence Evaluation** — Active guest positions checked against trail boundaries, restricted zones, and emergency assembly points

## New Capabilities

No new L1 or L2 capabilities are introduced. All changes enhance existing capabilities with L3 features that emerge from the real-time tracking and emergency alerting infrastructure.

## Summary

| Capability | Impact | L3 Count |
|-----------|--------|----------|
| CAP-2.1 | Enhanced | 1 |
| CAP-3.2 | Enhanced | 2 |
| CAP-3.3 | Enhanced | 5 |
| CAP-7.2 | Enhanced | 1 |
| **Total** | | **9** |
