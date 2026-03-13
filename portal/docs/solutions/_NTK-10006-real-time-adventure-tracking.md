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
| **Date** | 2026-03-13 |
| **Ticket** | NTK-10006 |

## Affected Capabilities

| Capability | Impact | Description |
|-----------|--------|-------------|
| [CAP-3.3 Emergency Response Coordination](../capabilities/index.md#cap-33-emergency-response-coordination) | enhanced | Emergency response now triggered automatically by GPS signals (SOS button activation and geofence boundary violations) via svc-adventure-tracking; no longer dependent solely on radio reports from guides |
| [CAP-3.2 Incident Reporting and Response](../capabilities/index.md#cap-32-incident-reporting-and-response) | enhanced | Incident reports in svc-safety-compliance now link to GPS telemetry sessions in svc-adventure-tracking; compliance officers can retrieve the full position history for insurance investigations and regulatory reporting |
| [CAP-2.1 Day-of-Adventure Check-In](../capabilities/index.md#cap-21-day-of-adventure-check-in) | enhanced | svc-check-in extended with ADVENTURE_STARTED status transition that activates a tracking session in svc-adventure-tracking; tracking is now part of the check-in departure workflow |

## Affected Services

- [svc-adventure-tracking](../microservices/svc-adventure-tracking.md)
- [svc-emergency-response](../microservices/svc-emergency-response.md)
- [svc-check-in](../microservices/svc-check-in.md)
- [svc-notifications](../microservices/svc-notifications.md)
- [svc-safety-compliance](../microservices/svc-safety-compliance.md)

## Architecture Decisions

- ADR-NTK10006-001
- ADR-NTK10006-002
- ADR-NTK10006-003

## Solution Contents

- Requirements
- Analysis
- Decisions
- Impact Assessments (4)
- Implementation Guidance
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

NovaTrek Adventures has no mechanism to track the real-time position of guests
during active adventures. When a guest becomes lost, injured, or separated from
their group, safety officers have no visibility into where the party is located.
Rescue dispatch relies entirely on verbal reports from guides using radio — a
single point of failure with no automated escalation and no GPS evidence trail
for insurance investigations.

The gap spans two capabilities: CAP-3.3 (Emergency Response Coordination) lacks
automated triggering from field signals, and CAP-3.2 (Incident Reporting) lacks
GPS telemetry linked to incident records. CAP-2.1 (Multi-Channel Check-In) also
requires extension to activate tracking sessions when adventures commence.

## Solution Overview

Introduce a new **svc-adventure-tracking** microservice that:

1. Maintains an adventure session per check-in group from departure to return
2. Ingests real-time GPS telemetry from wristband RFID devices and mobile apps
3. Enforces configurable geofence boundaries per trip type
4. Automatically triggers emergency incidents in svc-emergency-response when
   an SOS signal is received or a geofence boundary is violated
5. Provides live position data to the operations dashboard

The existing **svc-emergency-response** already has the API contract and dispatch
workflow. This solution connects the field signal pipeline to that existing
emergency infrastructure.

### Key Design Decisions

1. **New dedicated service** rather than extending svc-check-in or svc-safety-compliance —
   telemetry ingestion has distinct operational characteristics (high-frequency writes,
   device authentication, time-series retention) that justify isolation
2. **Check-in as the session trigger** — svc-check-in calls svc-adventure-tracking
   when adventure status transitions to ADVENTURE_STARTED; tracking follows check-in
3. **Device API key authentication** separate from human JWT tokens — wristband devices
   cannot hold rotating JWT credentials; long-lived per-device keys with narrow scope
4. **Geofence-based automatic escalation** — human-in-the-loop is too slow for safety;
   boundary violations trigger automated emergency creation in svc-emergency-response

### Architectural Flow

```
[Wristband / Mobile] ──telemetry──► svc-adventure-tracking
                                           │
                              ┌────────────┴───────────────┐
                              │                            │
                    (SOS or geofence              (normal update)
                     violation)                         │
                              │                    Store position
                              ▼                    Update last position
                   svc-emergency-response
                              │
                    Create emergency incident
                    Dispatch rescue resources
                              │
                              ▼
                    svc-notifications
                    (multi-channel alert to
                     safety officers + guide)

svc-check-in ──ADVENTURE_STARTED──► svc-adventure-tracking (start session)
```

## Impacted Components

| Service | Change Type | Impact Level | Owner |
|---------|------------|-------------|-------|
| svc-adventure-tracking | NEW SERVICE | PRIMARY | Safety and Compliance Team |
| svc-check-in | Integration — outbound call added | MEDIUM | NovaTrek Operations Team |
| svc-emergency-response | Integration — now called programmatically by tracking | LOW | Safety and Compliance Team |
| svc-notifications | No API change — already called by svc-emergency-response | NONE | Various |
| svc-safety-compliance | Read integration — incident reports link to session telemetry | LOW | Safety and Compliance Team |

## Security Considerations

| Threat | Mitigation |
|--------|-----------|
| Device spoofing | Per-device API keys provisioned at wristband issuance; keys stored hashed; rotation procedure defined |
| GPS coordinate tampering | Server-side geofence evaluation — client cannot suppress a violation by omitting coordinates |
| SOS suppression | Device transmits SOS flag in payload; missing telemetry for a session triggers a separate staleness alert |
| PII in telemetry | Guest ID is resolved server-side from device ID; telemetry payload contains only device ID and coordinates |
| Unauthorized access to live positions | BearerAuth (JWT) required for all session read endpoints; safety officer role required |
| Telemetry replay attack | Positions with `recorded_at` more than 30 minutes in the past are rejected |

## Prior Art

- **NTK-10005** (Wristband RFID) — established the `rfid_tag_id` field on check-in records
  that this solution uses as device identifiers for session correlation
- **NTK-10003** (Unregistered Guest Check-In) — established session-scoped JWT tokens for
  kiosk interactions; the device API key pattern in this solution is analogous
- **NTK-10004** (Guide Schedule Overwrite) — established optimistic locking (`_rev`) pattern
  reused on `AdventureSession` to prevent concurrent status transition conflicts
- **ADR-005** (Safety Defaults) — the unknown-category-defaults-to-Pattern-3 rule is extended
  here: unknown geofence boundaries default to the widest defined boundary for the trip type

## Related Services

- **svc-location-services** — provides geospatial location metadata (base camps, trail
  boundaries) that safety teams reference when configuring geofences; not called at runtime
- **svc-weather** — severe weather alerts can trigger adventure suspension independently;
  this solution does not integrate with svc-weather but both feed svc-safety-compliance

## Deployment Sequence

1. Provision TimescaleDB extension on PostgreSQL for `position_telemetry` hypertable
2. Create `adventure_tracking` database schema and tables
3. Provision per-device API keys for existing wristband inventory
4. Deploy svc-adventure-tracking with feature flag `TRACKING_ENABLED=false`
5. Configure geofence boundaries for all active trip types
6. Enable feature flag; verify telemetry ingestion in staging
7. Update svc-check-in to call `POST /sessions` on ADVENTURE_STARTED event
8. Monitor emergency trigger rate and false positive rate for 14 days before enabling
   automatic SOS triggers in production

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-03-13 | Initial solution design |