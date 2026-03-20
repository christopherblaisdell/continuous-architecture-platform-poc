---
title: "NTK-10006 — NTK-10006 Solution Design — Real-Time Adventure Tracking and Emergency Alerting System"
description: "Solution design for NTK-10006"
---

# NTK-10006 — NTK-10006 Solution Design — Real-Time Adventure Tracking and Emergency Alerting System

| Field | Value |
|-------|-------|
| **Ticket** | NTK-10006 |

## Affected Capabilities

| Capability | Impact | Description |
|-----------|--------|-------------|
| [CAP-3.3 Emergency Response Coordination](../capabilities/index.md#cap-33-emergency-response-coordination) | enhanced | Emergency response triggered automatically by GPS anomaly detection with precise guest coordinates |
| [CAP-3.2 Incident Reporting and Response](../capabilities/index.md#cap-32-incident-reporting-and-response) | enhanced | Incidents auto-created from tracking anomalies with GPS-enriched audit data |
| [CAP-2.1 Day-of-Adventure Check-In](../capabilities/index.md#cap-21-day-of-adventure-check-in) | enhanced | Check-in completion triggers GPS tracking session via Kafka event; wristband RFID is correlation key |

## Affected Services

- [svc-adventure-tracking](../microservices/svc-adventure-tracking.md)
- [svc-emergency-response](../microservices/svc-emergency-response.md)
- [svc-check-in](../microservices/svc-check-in.md)
- [svc-notifications](../microservices/svc-notifications.md)
- [svc-safety-compliance](../microservices/svc-safety-compliance.md)

## Architecture Decisions

- ADR-014

## Solution Contents

- Requirements
- Analysis
- Decisions
- Impact Assessments (5)
- User Stories
- Implementation Guidance
- Risk Assessment
- Capability Mapping

## Related Solutions

Solutions that share services or capabilities with this design:

| Solution | Shared Capabilities | Shared Services |
|----------|-------------------|-----------------|
| [NTK-10002 — NTK-10002: Adventure Category Classifica](_NTK-10002-adventure-category-classification.md) | CAP-2.1 | svc-check-in |
| [NTK-10005 — Add Wristband RFID Field to Check-In Rec](_NTK-10005-wristband-rfid-field.md) | CAP-2.1 | svc-check-in |
| [NTK-10009 — NTK-10009 Solution Design — Refund and D](_NTK-10009-refund-dispute-management.md) | — | svc-notifications |

---


## 1. Problem Statement

NovaTrek Adventures lacks real-time visibility into guest locations during active adventures. Safety officers depend on manual radio check-ins and phone calls to locate guests — a process that is unreliable in backcountry areas with limited cell coverage. When emergencies occur, response is delayed by the time required to determine the guest's location.

The ticket requests a GPS tracking system that monitors all active guests in near-real-time, automatically detects emergency conditions (SOS signals, geofence violations, loss of signal), and triggers the existing emergency response workflow with precise location data.

## 2. Prior Art

| Reference | Relevance |
|-----------|-----------|
| NTK-10005 (Wristband RFID Field) | Added `rfid_tag` to the CheckIn schema — the wristband is the key that links a guest to their GPS tracker. This solution depends on NTK-10005. |
| NTK-10002 (Adventure Category Classification) | Established Pattern 1/2/3 UI classification for check-in. Pattern 3 (high-risk) adventures will require mandatory GPS tracking; Pattern 1 (low-risk) adventures may use opt-in tracking. |
| ADR-005 (Pattern 3 Default Fallback) | Safety-first design principle: unknown or unmapped states default to the highest safety level. Applied here: unknown tracking state defaults to "assume emergency." |
| ADR-006 (Orchestrator Pattern for Check-In) | svc-check-in is the operations coordinator for day-of-adventure workflows. Tracking session initiation follows this established pattern. |
| svc-emergency-response spec | Full OpenAPI spec already exists with emergencies, dispatch, rescue teams, timeline, and GeoLocation schema. This solution integrates with it rather than duplicating it. |
| `emergency.triggered` event | Kafka event already defined in `events.yaml` with consumers: svc-notifications, svc-scheduling-orchestrator, svc-safety-compliance, svc-analytics. |
| `live-tracking.excalidraw` wireframe | Operations dashboard wireframe for real-time map view already exists at `architecture/wireframes/web-ops-dashboard/live-tracking.excalidraw`. |

## 3. Proposed Solution

### 3.1 Architecture Overview

The solution introduces one new service (**svc-adventure-tracking**) and integrates it with four existing services. svc-emergency-response already has a complete API spec — no new service is needed for emergency coordination.

```
Guest Wristband (GPS) --> svc-adventure-tracking --> svc-emergency-response
                               |                          |
                               |                          +--> svc-notifications (SMS/push/email)
                               |                          +--> svc-safety-compliance (incident log)
                               |
                               +--> Kafka: tracking.location.updated
                               +--> Kafka: tracking.anomaly.detected
                               +--> Kafka: tracking.session.started
                               +--> Kafka: tracking.session.ended
```

### 3.2 Service Responsibilities

| Service | Role | Data Owned |
|---------|------|-----------|
| **svc-adventure-tracking** (NEW) | GPS ingestion, tracking session lifecycle, geofence monitoring, anomaly detection | Tracking sessions, location history, geofence definitions |
| svc-emergency-response (EXISTING) | Emergency creation, rescue dispatch, timeline, contacts | Emergency records, dispatch records, rescue team status |
| svc-check-in (EXISTING) | Initiates tracking session on check-in completion | Check-in records, wristband assignments |
| svc-notifications (EXISTING) | Delivers emergency alerts across channels | No persistent store |
| svc-safety-compliance (EXISTING) | Receives incident events for audit logging | Incidents, audit log |

### 3.3 Tracking Session Lifecycle

1. **Start** — `checkin.completed` event published by svc-check-in includes `wristband_nfc_id` and `reservation_id`. svc-adventure-tracking consumes this event and creates a tracking session.
2. **Active** — GPS coordinates arrive from wristband hardware at a configurable interval (default: 30 seconds). svc-adventure-tracking stores each location update and publishes `tracking.location.updated` events for the ops dashboard.
3. **Anomaly** — If the guest exits a geofence boundary, stops transmitting for longer than the configurable timeout (default: 5 minutes), or presses the SOS button, svc-adventure-tracking publishes `tracking.anomaly.detected` and calls `POST /emergencies` on svc-emergency-response.
4. **End** — When the adventure concludes (scheduled end time or manual check-out), svc-adventure-tracking closes the tracking session and publishes `tracking.session.ended`. Location history is retained for insurance compliance.

### 3.4 New Service: svc-adventure-tracking

**Domain:** Safety
**Team:** Safety and Compliance Team
**Database:** PostgreSQL 15, schema `tracking`

**Core Endpoints (to be defined in OpenAPI spec):**

| Method | Path | Purpose |
|--------|------|---------|
| POST | /tracking-sessions | Create a tracking session (called internally on checkin.completed) |
| GET | /tracking-sessions | List active tracking sessions with filters |
| GET | /tracking-sessions/{id} | Get tracking session details including latest location |
| PATCH | /tracking-sessions/{id} | Update session status (end, pause) |
| POST | /tracking-sessions/{id}/locations | Ingest GPS location update from wristband |
| GET | /tracking-sessions/{id}/locations | Get location history for a session |
| GET | /tracking-sessions/active | Get all currently active sessions with latest coordinates (ops dashboard) |
| POST | /geofences | Create a geofence boundary for a trail or adventure zone |
| GET | /geofences | List geofences |
| GET | /geofences/{id} | Get geofence details |

**Data Model:**

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| tracking_sessions | Session lifecycle | session_id (PK), wristband_nfc_id, reservation_id, guest_id, adventure_category, trail_id, status (active/ended/emergency), started_at, ended_at, _rev |
| location_updates | GPS coordinate history | update_id (PK), session_id (FK), latitude, longitude, altitude_meters, accuracy_meters, source, recorded_at |
| geofences | Trail boundaries | geofence_id (PK), trail_id, name, boundary_polygon (JSONB), active |
| anomaly_events | Detected anomalies | anomaly_id (PK), session_id (FK), type (geofence_violation/signal_loss/sos/inactivity), severity, detected_at, resolved_at, emergency_id (FK, nullable) |

**Volume Estimates:**
- Active sessions: up to 500 concurrent (peak season)
- Location updates: ~1,000/minute at peak (500 guests x 2 updates/min)
- Location history retention: 1 year rolling, then archived to cold storage
- Audit retention: 7 years (regulatory)

### 3.5 Event Design

**New events published by svc-adventure-tracking:**

| Event | Channel | Trigger | Consumers |
|-------|---------|---------|-----------|
| tracking.session.started | novatrek.safety.tracking.session.started | Tracking session created from checkin.completed | svc-analytics, svc-scheduling-orchestrator |
| tracking.session.ended | novatrek.safety.tracking.session.ended | Adventure concluded, session closed | svc-analytics |
| tracking.location.updated | novatrek.safety.tracking.location.updated | Each GPS coordinate received | web-ops-dashboard (via WebSocket gateway) |
| tracking.anomaly.detected | novatrek.safety.tracking.anomaly.detected | Geofence violation, signal loss, SOS, inactivity | svc-emergency-response, svc-notifications, svc-safety-compliance, svc-analytics |

**Existing event consumed by svc-adventure-tracking:**

| Event | Channel | Producer | Purpose |
|-------|---------|----------|---------|
| checkin.completed | novatrek.operations.checkin.completed | svc-check-in | Triggers tracking session creation |

### 3.6 Integration Points

| Caller | Target | Method | Path | Purpose | Sync/Async |
|--------|--------|--------|------|---------|------------|
| svc-adventure-tracking | svc-emergency-response | POST | /emergencies | Trigger emergency on anomaly detection | Sync (HTTPS) |
| svc-adventure-tracking | svc-location-services | GET | /trails/{id}/boundary | Retrieve geofence boundary for trail | Sync (HTTPS) |
| svc-adventure-tracking | svc-check-in | GET | /check-ins?rfid_tag={tag} | Resolve wristband to guest identity | Sync (HTTPS) |
| web-ops-dashboard | svc-adventure-tracking | GET | /tracking-sessions/active | Live map data for ops dashboard | Sync (HTTPS) |
| web-ops-dashboard | svc-adventure-tracking | WebSocket | /ws/tracking | Real-time location stream for map | Async (WebSocket) |

### 3.7 Safety-First Design Principles

Per ADR-005 (Pattern 3 Default Fallback), the tracking system applies safety-first defaults:

| Scenario | Default Behavior |
|----------|-----------------|
| Unknown adventure category | Mandatory tracking (Pattern 3 equivalent) |
| Signal lost from wristband | After configurable timeout (default 5 min), escalate to anomaly |
| Guest exits geofence | Immediate warning to ops dashboard; auto-escalate after 2 min if no acknowledgment |
| Tracking session not started after check-in | Alert ops staff — do not allow guest to depart without active tracking for Pattern 2/3 adventures |
| svc-adventure-tracking unavailable | svc-check-in logs degraded-mode warning; check-in proceeds with manual tracking fallback (radio check-ins) |

### 3.8 Backward Compatibility

| Change | Impact | Mitigation |
|--------|--------|-----------|
| New `checkin.completed` consumer | No breaking change — Kafka is pub/sub; adding a consumer does not affect the producer | Verify event schema includes wristband_nfc_id (added by NTK-10005) |
| svc-check-in adds tracking status field | New optional field `tracking_session_id` on CheckIn response | Nullable field; existing consumers ignore it |
| New Kafka topics | No impact on existing topics — new channels only | Standard topic creation via infrastructure |

## 4. Quality Attributes (ISO 25010)

| Attribute | Assessment | Notes |
|-----------|-----------|-------|
| **Functional Suitability** | Meets stated requirements — GPS tracking, automated alerting, insurance compliance | Acceptance criteria 1-8 addressed |
| **Performance Efficiency** | 1,000 location updates/minute at peak; 30-second latency target; WebSocket for real-time map | Location_updates table will need time-series partitioning for query performance |
| **Reliability** | Safety-first defaults (ADR-005); graceful degradation when tracking unavailable; anomaly detection with configurable thresholds | Signal loss timeout prevents false negatives |
| **Security** | GPS location is PII — access restricted to ops staff and safety team; audit logging for all location queries; wristband-to-guest resolution only through svc-check-in | Emergency contacts accessible only during active emergencies |
| **Maintainability** | Event-driven decoupling between tracking, emergency response, and notifications; geofence boundaries configured via API not hardcoded | Separate anomaly detection logic from GPS ingestion for testability |
| **Compatibility** | No breaking changes to existing services; new optional fields only; new Kafka topics do not affect existing consumers | checkin.completed event schema must include wristband_nfc_id (NTK-10005 dependency) |

## 5. Decisions

See [3.solution/d.decisions/decisions.md](3.solution/d.decisions/decisions.md) for full MADR-format ADR.

| Decision | Summary |
|----------|---------|
| ADR-014: Event-Driven Tracking Session Initiation | Tracking sessions initiated by consuming `checkin.completed` events (not by synchronous call from svc-check-in) |

## 6. Risks

See [3.solution/r.risks/risks.md](3.solution/r.risks/risks.md) for detailed risk register.

| Risk | Severity | Mitigation |
|------|----------|-----------|
| GPS signal unreliable in deep canyon/forest areas | High | Configurable signal-loss timeout; manual tracking fallback; mesh relay network as future enhancement |
| Location data volume overwhelms database | Medium | Time-series partitioning on location_updates; 1-year rolling retention with cold archive |
| False positive anomalies trigger unnecessary emergencies | Medium | Configurable thresholds per adventure category; human acknowledgment required before full escalation |
| Wristband hardware dependency | High | svc-adventure-tracking is hardware-agnostic (accepts any GPS source via REST API); wristband integration is a hardware concern, not an architecture concern |
| Privacy concerns with continuous GPS tracking | Medium | Data retention policy; guest consent at check-in; location data access restricted to authorized safety staff |

## 7. Impacts

See impact assessments in [3.solution/i.impacts/](3.solution/i.impacts/):

| Service | Change Summary |
|---------|---------------|
| svc-adventure-tracking | NEW SERVICE — full API, data model, event publishing |
| svc-check-in | Add `tracking_session_id` to CheckIn response; ensure `checkin.completed` event includes `wristband_nfc_id` |
| svc-emergency-response | No API changes — existing spec fully supports the integration |
| svc-notifications | No API changes — existing bulk notification API handles emergency alerts |
| svc-safety-compliance | New `tracking.anomaly.detected` event consumer for auto-creating incidents |

## 8. User Stories

See [3.solution/u.user.stories/user-stories.md](3.solution/u.user.stories/user-stories.md) for full user story set.