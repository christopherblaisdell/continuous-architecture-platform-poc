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

---

## :material-database: Data Store

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `safety` |
| **Primary Tables** | `waivers`, `incidents`, `safety_inspections`, `audit_log` |
| **Key Features** | Immutable audit log (append-only) | Digital signature verification for waivers | Regulatory compliance retention (7 years) |
| **Estimated Volume** | ~3,000 waiver checks/day |

---

## :material-api: Endpoints (8 total)

---

### GET `/waivers` -- List waivers by guest { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Waivers/listWaivers){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-safety-compliance--get-waivers.svg" type="image/svg+xml" style="max-width: 100%;">GET /waivers sequence diagram</object></div>

---

### POST `/waivers` -- Guest signs a safety waiver { .endpoint-post }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Waivers/signWaiver){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-safety-compliance--post-waivers.svg" type="image/svg+xml" style="max-width: 100%;">POST /waivers sequence diagram</object></div>

---

### GET `/waivers/{waiver_id}` -- Get a specific waiver { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Waivers/getWaiver){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-safety-compliance--get-waivers-waiver_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /waivers/{waiver_id} sequence diagram</object></div>

---

### POST `/incidents` -- File an incident report { .endpoint-post }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Incidents/createIncident){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-safety-compliance--post-incidents.svg" type="image/svg+xml" style="max-width: 100%;">POST /incidents sequence diagram</object></div>

---

### GET `/incidents/{incident_id}` -- Get an incident report { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Incidents/getIncident){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-safety-compliance--get-incidents-incident_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /incidents/{incident_id} sequence diagram</object></div>

---

### PATCH `/incidents/{incident_id}` -- Update an incident report (add follow-up, change status) { .endpoint-patch }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Incidents/updateIncident){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-safety-compliance--patch-incidents-incident_id.svg" type="image/svg+xml" style="max-width: 100%;">PATCH /incidents/{incident_id} sequence diagram</object></div>

---

### GET `/safety-inspections` -- List safety inspections for a location { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Inspections/listSafetyInspections){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-safety-compliance--get-safety-inspections.svg" type="image/svg+xml" style="max-width: 100%;">GET /safety-inspections sequence diagram</object></div>

---

### POST `/safety-inspections` -- Record a safety inspection { .endpoint-post }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Inspections/createSafetyInspection){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-safety-compliance--post-safety-inspections.svg" type="image/svg+xml" style="max-width: 100%;">POST /safety-inspections sequence diagram</object></div>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Guest Portal](../applications/web-guest-portal/) | Waiver Signing |
| [Operations Dashboard](../applications/web-ops-dashboard/) | Check-In Station, Safety Incident Board |
| [Adventure App](../applications/app-guest-mobile/) | Self Check-In |
