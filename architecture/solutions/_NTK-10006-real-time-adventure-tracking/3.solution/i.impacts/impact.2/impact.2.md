<!-- PUBLISH -->
# Impact Assessment 2: svc-emergency-response (NEW)

| Field | Value |
|-------|-------|
| Service | svc-emergency-response |
| Domain | Safety |
| Change Type | New service |
| Impact Level | PRIMARY |
| Owner | NovaTrek Safety and Compliance Team |

## Overview

svc-emergency-response manages the full emergency lifecycle: from detection through dispatch through resolution. It receives emergency triggers from svc-adventure-tracking (SOS, geofence breaches) and svc-weather (severe weather alerts), dispatches rescue teams, coordinates notifications, and maintains an audit trail.

## API Contract

Existing OpenAPI specification: `architecture/specs/svc-emergency-response.yaml` (v1.0.0) — already defined in the architecture metadata.

### Key Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | /emergencies | Create emergency (from SOS, geofence breach, weather) |
| PATCH | /emergencies/{id} | Update status through lifecycle |
| GET | /emergencies/{id}/timeline | Append-only audit trail |
| POST | /dispatch | Dispatch rescue team to emergency |
| GET | /rescue-teams | List teams with availability |
| GET | /emergency-contacts/{guest_id} | Guest emergency contacts |

## Data Model

Already defined in `architecture/metadata/data-stores.yaml`:

| Table | Purpose | Volume |
|-------|---------|--------|
| emergencies | Emergency records with location and status | ~50/month peak season |
| emergency_timeline | Append-only event log per emergency | ~500 entries/month |
| dispatch_records | Team-to-emergency assignments with ETA | ~50/month |
| rescue_teams | Team roster with certifications and region | ~10 static |
| emergency_contacts | Cached guest emergency contacts | ~5,000 |

**Database:** PostgreSQL 15 with optimistic locking (_rev) on emergencies.

## Event Integration

### Consumes

| Event | Source | Action |
|-------|--------|--------|
| sos.triggered | svc-adventure-tracking | Create emergency (SOS type) |
| geofence.breach | svc-adventure-tracking | Create emergency (GEOFENCE_BREACH type) |
| weather alert (WARNING/EMERGENCY) | svc-weather | Create area-wide emergency if evacuation needed |
| wildlife-alert.issued (evacuate) | svc-wildlife-tracking | Create emergency (WILDLIFE type) |

### Produces

| Event | Channel | Trigger |
|-------|---------|---------|
| emergency.triggered | novatrek.safety.emergency.triggered | Emergency created |
| emergency.resolved | novatrek.safety.emergency.resolved | Emergency resolved |

## Cross-Service Dependencies

| Target Service | Integration | Direction |
|---------------|-------------|-----------|
| svc-adventure-tracking | GET /tracking-sessions (affected guests) | Outbound (read) |
| svc-guest-profiles | GET /guests/{id} (identity, medical info) | Outbound (read) |
| svc-notifications | POST /notifications, POST /notifications/bulk | Outbound (emergency alerts) |
| svc-safety-compliance | POST /incidents (create incident record) | Outbound |

## Quality Attributes

| Attribute | Assessment |
|-----------|-----------|
| Reliability | CRITICAL — emergency creation and dispatch must never fail silently; circuit breaker + retry for all outbound calls |
| Performance | Emergency creation to first notification must complete within 60 seconds (SLA) |
| Security | Emergency records contain PII (guest identity, location) — standard PII protections apply |
| Maintainability | Emergency types and severity mappings are extensible enums |
