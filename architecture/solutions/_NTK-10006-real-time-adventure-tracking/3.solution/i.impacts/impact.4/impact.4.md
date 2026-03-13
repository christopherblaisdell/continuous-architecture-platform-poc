# Impact Assessment — svc-safety-compliance

| Field | Value |
|-------|-------|
| Service | svc-safety-compliance |
| Impact Level | LOW |
| Change Type | Read integration — incident reports gain GPS telemetry reference |
| Owner | Safety and Compliance Team |

## Overview

svc-safety-compliance manages incident records, waiver compliance, and regulatory reporting.
When an incident is raised from a tracking-triggered emergency, the incident record can now
include a reference to the svc-adventure-tracking session, enabling compliance officers to
attach the GPS position history to the incident report.

## API Contract Changes

### Existing Schema: IncidentReport — Extended

The `IncidentReport` schema gains one new optional field:

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `tracking_session_id` | UUID | Yes | Reference to the svc-adventure-tracking session for GPS telemetry retrieval. Populated when the incident originated from an automated tracking trigger. Null for incidents created manually. |

### Workflow Change (No API Change)

When a compliance officer opens an incident report that has a `tracking_session_id`, the
operations portal displays a link to the telemetry trail:
`GET /tracking/v1/sessions/{tracking_session_id}/positions`

This is a read-only query from the portal; no new svc-safety-compliance API endpoints are
added.

## Data Model Changes

One nullable column added to the incident reports table:
- `tracking_session_id` (UUID, nullable)

## Backward Compatibility

The `tracking_session_id` field is nullable and additive. Existing incident reports without
a tracking session are unaffected. Existing API consumers that do not use this field are
unaffected.
