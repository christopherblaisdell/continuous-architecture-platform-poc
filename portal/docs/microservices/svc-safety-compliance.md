---
tags:
  - microservice
  - svc-safety-compliance
  - safety
---

# svc-safety-compliance

**NovaTrek Safety and Compliance Service** &nbsp;|&nbsp; <span style="background: #dc262615; color: #dc2626; border: 1px solid #dc262640; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">Safety</span> &nbsp;|&nbsp; `v1.0.0` &nbsp;|&nbsp; *NovaTrek Safety Operations*

> Manages guest safety waivers, incident reporting, safety inspections, and

[:material-api: Swagger UI](../services/api/svc-safety-compliance.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-safety-compliance.yaml){ .md-button }
[:material-pipe: CI/CD Pipeline](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/service-ci.yml){ .md-button }
[:material-source-branch: Source Code](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/services/svc-safety-compliance){ .md-button }
[:material-language-java: Technology Stack](../technologies.md){ .md-button }

## :material-truck-delivery: Delivery Status

**Delivery Wave:** 3 -- Day-of-Adventure Operations

| Stage | Status |
|-------|--------|
| Infrastructure (Bicep) | :material-circle-outline: not-started |
| Database Schema (Flyway) | :material-circle-outline: not-started |
| CI Pipeline | :material-circle-outline: not-started |
| CD Pipeline | :material-circle-outline: not-started |
| Deployed to Dev | :material-circle-outline: not-started |
| Smoke Tested | :material-circle-outline: not-started |
| Deployed to Prod | :material-circle-outline: not-started |

**Azure Resources (Dev):**

- [:material-database: PostgreSQL Server](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.DBforPostgreSQL/flexibleServers/pg-novatrek-dev-smwd6ded4e3so)
- [:material-text-search: Log Analytics](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.OperationalInsights/workspaces/log-novatrek-dev/logs)

---

## :material-map: Integration Context

<div class="diagram-wrap"><a href="../svg/svc-safety-compliance--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-safety-compliance--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-safety-compliance C4 context diagram</object></div>


## :material-database: Data Store { #data-store }

### Entity Relationship Diagram

<div class="diagram-wrap"><a href="../svg/svc-safety-compliance--erd.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-safety-compliance--erd.svg" type="image/svg+xml" style="max-width: 100%;">svc-safety-compliance entity relationship diagram</object></div>

### Overview

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `safety` |
| **Tables** | `waivers`, `incidents`, `safety_inspections`, `audit_log` |
| **Estimated Volume** | ~3,000 waiver checks/day |
| **Connection Pool** | min 5 / max 20 / idle timeout 10min |
| **Backup Strategy** | Continuous WAL archiving, daily base backup, 7-year retention (regulatory) |

### Key Features

- Immutable audit log (append-only)
- Digital signature verification for waivers
- Regulatory compliance retention (7 years)

### Table Reference

#### `waivers`

*Signed liability waivers with digital signature verification*

| Column | Type | Constraints |
|--------|------|-------------|
| `waiver_id` | `UUID` | PK |
| `guest_id` | `UUID` | NOT NULL |
| `trip_id` | `UUID` | NOT NULL |
| `waiver_type` | `VARCHAR(50)` | NOT NULL |
| `signed_at` | `TIMESTAMPTZ` | NULL |
| `signature_ref` | `VARCHAR(255)` | NULL (DocuSign envelope ID) |
| `status` | `VARCHAR(20)` | NOT NULL, DEFAULT 'pending' |
| `expires_at` | `TIMESTAMPTZ` | NULL |
| `created_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_waiver_guest_trip` on `guest_id, trip_id`
- `idx_waiver_status` on `status`

#### `incidents`

*Safety incident reports with severity classification*

| Column | Type | Constraints |
|--------|------|-------------|
| `incident_id` | `UUID` | PK |
| `trip_id` | `UUID` | NULL |
| `location_id` | `UUID` | NULL |
| `severity` | `VARCHAR(20)` | NOT NULL |
| `description` | `TEXT` | NOT NULL |
| `reported_by` | `VARCHAR(100)` | NOT NULL |
| `reported_at` | `TIMESTAMPTZ` | NOT NULL |
| `resolved_at` | `TIMESTAMPTZ` | NULL |
| `resolution_notes` | `TEXT` | NULL |

**Indexes:**

- `idx_incident_severity` on `severity, reported_at DESC`
- `idx_incident_trip` on `trip_id`

#### `audit_log`

*Immutable append-only audit trail for regulatory compliance*

| Column | Type | Constraints |
|--------|------|-------------|
| `log_id` | `BIGSERIAL` | PK |
| `entity_type` | `VARCHAR(50)` | NOT NULL |
| `entity_id` | `UUID` | NOT NULL |
| `action` | `VARCHAR(20)` | NOT NULL |
| `actor` | `VARCHAR(100)` | NOT NULL |
| `details` | `JSONB` | NOT NULL |
| `logged_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT NOW() |

**Indexes:**

- `idx_audit_entity` on `entity_type, entity_id`
- `idx_audit_time` on `logged_at`


---

## :material-lightbulb: Solutions Affecting This Service

| Ticket | Solution | Capabilities | Date |
|--------|----------|-------------|------|
| NTK-10006 | [Real-Time Adventure Tracking and Emergency Alerting System](../solutions/_NTK-10006-real-time-adventure-tracking.md) | `CAP-2.1`, `CAP-3.2`, `CAP-3.3`, `CAP-7.2` | 2026-03-14 |

---

## :material-api: Endpoints (8 total)

---

### GET `/waivers` -- List waivers by guest { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Waivers/listWaivers){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-safety-compliance--get-waivers.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-safety-compliance--get-waivers.svg" type="image/svg+xml" style="max-width: 100%;">GET /waivers sequence diagram</object></div>

---

### POST `/waivers` -- Guest signs a safety waiver { .endpoint-post }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Waivers/signWaiver){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-safety-compliance--post-waivers.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-safety-compliance--post-waivers.svg" type="image/svg+xml" style="max-width: 100%;">POST /waivers sequence diagram</object></div>

---

### GET `/waivers/{waiver_id}` -- Get a specific waiver { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Waivers/getWaiver){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-safety-compliance--get-waivers-waiver_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-safety-compliance--get-waivers-waiver_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /waivers/{waiver_id} sequence diagram</object></div>

---

### POST `/incidents` -- File an incident report { .endpoint-post }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Incidents/createIncident){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-safety-compliance--post-incidents.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-safety-compliance--post-incidents.svg" type="image/svg+xml" style="max-width: 100%;">POST /incidents sequence diagram</object></div>

---

### GET `/incidents/{incident_id}` -- Get an incident report { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Incidents/getIncident){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-safety-compliance--get-incidents-incident_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-safety-compliance--get-incidents-incident_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /incidents/{incident_id} sequence diagram</object></div>

---

### PATCH `/incidents/{incident_id}` -- Update an incident report (add follow-up, change status) { .endpoint-patch }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Incidents/updateIncident){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-safety-compliance--patch-incidents-incident_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-safety-compliance--patch-incidents-incident_id.svg" type="image/svg+xml" style="max-width: 100%;">PATCH /incidents/{incident_id} sequence diagram</object></div>

---

### GET `/safety-inspections` -- List safety inspections for a location { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Inspections/listSafetyInspections){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-safety-compliance--get-safety-inspections.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-safety-compliance--get-safety-inspections.svg" type="image/svg+xml" style="max-width: 100%;">GET /safety-inspections sequence diagram</object></div>

---

### POST `/safety-inspections` -- Record a safety inspection { .endpoint-post }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Inspections/createSafetyInspection){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-safety-compliance--post-safety-inspections.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-safety-compliance--post-safety-inspections.svg" type="image/svg+xml" style="max-width: 100%;">POST /safety-inspections sequence diagram</object></div>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Guest Portal](../../applications/web-guest-portal/) | Waiver Signing |
| [Operations Dashboard](../../applications/web-ops-dashboard/) | Check-In Station, Safety Incident Board |
| [Adventure App](../../applications/app-guest-mobile/) | Self Check-In |

---

## :material-broadcast: Events Published

| Event | Channel | Trigger | Consumers |
|-------|---------|---------|-----------|
| [`incident.reported`](/events/#incidentreported) | `novatrek.safety.incident.reported` | [`POST /incidents`](#post-incidents-file-an-incident-report) | [svc-notifications](../svc-notifications/), [svc-analytics](../svc-analytics/) |

---

## :material-broadcast-off: Events Consumed

| Event | Producer | Channel |
|-------|----------|---------|
| [`emergency.triggered`](/events/#emergencytriggered) | [svc-emergency-response](../svc-emergency-response/) | `novatrek.safety.emergency.triggered` |
