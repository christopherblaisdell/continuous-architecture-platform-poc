---
title: "NTK-10006 — NTK-10006 Solution Design — Real-Time Adventure Tracking and Emergency Alerting System"
description: "Solution design for NTK-10006"
---

# NTK-10006 — NTK-10006 Solution Design — Real-Time Adventure Tracking and Emergency Alerting System

| Field | Value |
|-------|-------|
| **Status** | Proposed |
| **Version** | v1.0 |
| **Author** | Solution Architect (AI-Assisted) |
| **Date** | 2026-03-14 |
| **Ticket** | NTK-10006 |

## Affected Capabilities

| Capability | Impact | Description |
|-----------|--------|-------------|
| [CAP-2.1 Day-of-Adventure Check-In](../capabilities/index.md#cap-21-day-of-adventure-check-in) | enhanced | Check-in completion triggers tracking session activation via checkin.completed event |
| [CAP-3.2 Incident Reporting and Response](../capabilities/index.md#cap-32-incident-reporting-and-response) | enhanced | Incidents auto-generated from SOS triggers and geofence breaches with precise GPS coordinates |
| [CAP-3.3 Emergency Response Coordination](../capabilities/index.md#cap-33-emergency-response-coordination) | enhanced | Full emergency lifecycle with SOS detection, proximity-based rescue dispatch, and multi-channel alerting |
| [CAP-7.2 Geospatial and Location Services](../capabilities/index.md#cap-72-geospatial-and-location-services) | enhanced | svc-location-services provides geofence boundaries for real-time position evaluation |

## Affected Services

- [svc-adventure-tracking](../microservices/svc-adventure-tracking.md)
- [svc-emergency-response](../microservices/svc-emergency-response.md)
- [svc-check-in](../microservices/svc-check-in.md)
- [svc-notifications](../microservices/svc-notifications.md)
- [svc-safety-compliance](../microservices/svc-safety-compliance.md)

## Architecture Decisions

- ADR-012
- ADR-013
- ADR-014

## Solution Contents

- Requirements
- Analysis
- Decisions
- Impact Assessments (5)
- User Stories
- Risk Assessment
- Capability Mapping

## Related Solutions

Solutions that share services or capabilities with this design:

| Solution | Shared Capabilities | Shared Services |
|----------|-------------------|-----------------|
| [NTK-10002 — NTK-10002: Adventure Category Classifica](_NTK-10002-adventure-category-classification.md) | CAP-2.1 | svc-check-in |
| [NTK-10003 — Unregistered Guest Self-Service Check-in](_NTK-10003-unregistered-guest-self-checkin.md) | CAP-2.1 | svc-check-in |
| [NTK-10005 — Add Wristband RFID Field to Check-In Rec](_NTK-10005-wristband-rfid-field.md) | CAP-2.1 | svc-check-in |
| [NTK-10009 — NTK-10009 Solution Design — Refund and D](_NTK-10009-refund-dispute-management.md) | — | svc-notifications |

---


## Problem Statement

NovaTrek Adventures has no real-time visibility into guest locations during active adventures. When a guest encounters an emergency (injury, getting lost, severe weather), there is no automated system to determine their position or coordinate rescue. This creates three critical gaps:

1. **Safety gap** — Rescue response begins with manual location discovery, wasting critical minutes
2. **Compliance gap** — Insurance mandates require GPS tracking records for guided and full-service adventures, and this data does not exist
3. **Coordination gap** — Weather events and wildlife alerts require manual assessment of affected guests with no systematic way to identify who is in the danger zone

The RFID wristband infrastructure from NTK-10005 provides the physical identity token; this solution builds the tracking and emergency response systems on top of that foundation.

## Solution Overview

Two new services address the problem with clear separation of concerns:

**svc-adventure-tracking** (Operations domain) — High-throughput GPS position ingestion service. Receives position updates from wristband devices, maintains tracking sessions linked to guest check-ins, evaluates positions against geofences, and provides a live streaming API for the operations dashboard.

**svc-emergency-response** (Safety domain) — High-reliability emergency lifecycle manager. Receives emergency triggers from tracking (SOS, geofence breaches) and weather systems, dispatches rescue teams based on proximity and certification, coordinates multi-channel notifications, and maintains an append-only audit timeline.

### Architectural Pattern

```
Wristband GPS                    svc-weather
    │                                 │
    ▼                                 │ weather.alert event
POST /positions                       │
    │                                 ▼
svc-adventure-tracking ──event──> svc-emergency-response
    │    │    │                       │    │    │
    │    │    │                       │    │    │
    │    │    └─ geofence.breach ─────┘    │    │
    │    │                                 │    │
    │    └─── sos.triggered ───────────────┘    │
    │                                           │
    ▼                                           ▼
SSE /live-stream                    POST /notifications (URGENT)
    │                                    │
    ▼                                    ▼
web-ops-dashboard              Guide + Ops + Emergency Contacts
(live tracking map)
```

### Event Flow: Check-In to Tracking

```
Guest completes check-in
    │
    ▼
svc-check-in emits: checkin.completed
  { guest_id, reservation_id, rfid_tag, adventure_category, check_in_pattern }
    │
    ▼
svc-adventure-tracking consumes event
    │
    ├─ Creates TrackingSession (ACTIVE)
    ├─ Sets frequency: Pattern 1→60s, Pattern 2→30s, Pattern 3→10s
    └─ Loads geofences for trail_id from svc-location-services
    │
    ▼
Wristband begins transmitting GPS at configured frequency
    │
    ▼
POST /positions (per update) or POST /positions/batch (buffered)
    │
    ├─ Store position
    ├─ Evaluate geofence
    ├─ Broadcast via SSE /live-stream
    └─ If SOS=true → trigger emergency workflow
```

### Event Flow: SOS Emergency

```
Guest presses SOS (5-second hold)
    │
    ▼
POST /positions { sos: true, latitude, longitude, rfid_tag }
    │
    ▼
svc-adventure-tracking
    ├─ Emits: sos.triggered { session_id, guest_id, latitude, longitude }
    │
    ▼
svc-emergency-response
    ├─ Creates Emergency (TRIGGERED, type=SOS, severity=CRITICAL)
    ├─ Identifies nearest AVAILABLE rescue team (geospatial proximity + certifications)
    ├─ Creates Dispatch (ETA calculated)
    ├─ Appends timeline: TRIGGERED → DISPATCHED
    ├─ Emits: emergency.triggered
    │
    ▼
svc-notifications
    ├─ URGENT SMS + PUSH to assigned guide
    ├─ URGENT IN_APP to operations staff
    ├─ URGENT SMS to emergency contacts
    └─ URGENT SMS + PUSH to rescue team
```

## Impacted Components

| Service | Change Type | Impact Level | Owner |
|---------|------------|-------------|-------|
| svc-adventure-tracking | NEW service | PRIMARY | NovaTrek Operations Team |
| svc-emergency-response | NEW service (spec exists) | PRIMARY | Safety and Compliance Team |
| svc-notifications | New templates + event consumer | MEDIUM | Various |
| svc-location-services | Geofence data source (enum extension) | LOW | Various |
| svc-check-in | No change (existing event sufficient) | NONE | NovaTrek Operations Team |
| svc-weather | No change (existing alerts sufficient) | NONE | Various |
| svc-reservations | No change (existing event sufficient) | NONE | Booking Platform Team |

## Security Considerations

| Threat | Mitigation |
|--------|-----------|
| GPS position data is PII | Encryption at rest, access logging, 90-day retention limit, right-to-deletion support |
| Spoofed position reports | RFID tag validation against active tracking sessions; bearer token authentication on all endpoints |
| Unauthorized tracking access | Role-based access — only SAFETY_OFFICER and OPS_STAFF roles can view live tracking |
| Emergency notification interception | URGENT notifications via encrypted channels (HTTPS for push, TLS for SMS via Twilio) |
| Denial of service via position flooding | Rate limiting on POST /positions per RFID tag (max 1 update per second) |

## Prior Art

| Solution | Relationship |
|----------|-------------|
| **NTK-10005** (Wristband RFID Field) | Direct precursor — added rfid_tag to check-in record and checkin.completed event specifically for tracking |
| **NTK-10002** (Adventure Classification) | Established Pattern 1/2/3 classification system reused for tracking frequency tiers (ADR-004) |
| **NTK-10003** (Unregistered Guest Check-In) | Established svc-check-in as orchestrator (ADR-006); check-in completion is the tracking trigger |
| **ADR-005** (Pattern 3 Default Fallback) | Safety-first principle applied to tracking: unknown categories get Pattern 3 frequency |

## Key Design Decisions

| ADR | Decision | Rationale |
|-----|----------|-----------|
| ADR-012 | Two new services (not one combined, not extending existing) | Separation of concerns: high-throughput tracking vs. high-reliability emergency response; domain boundary alignment |
| ADR-013 | Event-driven tracking activation via checkin.completed | Zero coupling to svc-check-in; event already carries all required data; at-least-once delivery guarantees |
| ADR-014 | Pattern-based tracking frequency with Pattern 3 default | Risk-proportionate tracking; configuration-driven (ADR-004 consistency); safety-first default (ADR-005 consistency) |

## Deployment Sequence

1. Deploy svc-adventure-tracking with PostgreSQL + PostGIS database
2. Deploy svc-emergency-response (or verify existing spec is deployed)
3. Seed geofence boundaries in svc-location-services for all active trails
4. Create emergency notification templates in svc-notifications
5. Configure svc-adventure-tracking to consume checkin.completed events
6. Configure svc-emergency-response to consume sos.triggered and geofence.breach events
7. Configure svc-notifications to consume emergency.triggered events
8. Enable live-stream SSE endpoint and connect web-ops-dashboard
9. Validate end-to-end SOS flow in staging with test wristbands

## Wireframe Reference

Operations dashboard live tracking map: `architecture/wireframes/web-ops-dashboard/live-tracking.excalidraw`

## Quality Attributes

| Attribute (ISO 25010) | Assessment |
|----------------------|-----------|
| **Functional Suitability** | All 10 acceptance criteria from the ticket report are addressed by the solution |
| **Performance Efficiency** | svc-adventure-tracking handles 50,000 position updates/day with sub-100ms acknowledgment; SSE stream for real-time dashboard updates |
| **Reliability** | svc-emergency-response uses circuit breaker + retry for all outbound calls; at-least-once event delivery; dashboard fallback for notification failures |
| **Security** | PII classification for position data; encryption at rest; role-based access; rate limiting; RFID validation |
| **Compatibility** | Zero changes to svc-check-in, svc-weather, svc-reservations; additive-only changes to svc-location-services and svc-notifications |
| **Maintainability** | Tracking frequency configurable via YAML; emergency types extensible via enum; geofence boundaries managed as data, not code |