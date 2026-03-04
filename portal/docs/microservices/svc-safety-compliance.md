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
| **Key Features** | Immutable audit log (append-only) · Digital signature verification for waivers · Regulatory compliance retention (7 years) |
| **Estimated Volume** | ~3,000 waiver checks/day |

---

## :material-api: Endpoints (8 total)

---

### GET `/waivers` — List waivers by guest { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Waivers/listWaivers){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /waivers
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: listWaivers()

    Svc->>+Repo: findByFilters(criteria)
    Repo->>+DB: SELECT ... WHERE filters
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: Page of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### POST `/waivers` — Guest signs a safety waiver { .endpoint-post }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Waivers/signWaiver){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant GP as Guest Profiles
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: POST /waivers
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: signWaiver()

    rect rgba(199, 123, 48, 0.08)
        Note over Svc,GP: Cross-service integration
        Svc->>+GP: Validate guest identity
        GP-->>-Svc: OK
    end

    Svc->>+Repo: save(entity)
    Repo->>+DB: INSERT INTO ...
    DB-->>-Repo: Created row
    Repo-->>-Svc: Persisted entity

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 201 Created
```

---

### GET `/waivers/{waiver_id}` — Get a specific waiver { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Waivers/getWaiver){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /waivers/(waiver_id)
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getWaiver()

    Svc->>+Repo: findById(id)
    Repo->>+DB: SELECT ... WHERE id = ?
    DB-->>-Repo: Row
    Repo-->>-Svc: Entity
    Note right of Repo: Returns 404 if not found

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### POST `/incidents` — File an incident report { .endpoint-post }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Incidents/createIncident){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Ntfy as Notifications
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: POST /incidents
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: createIncident()

    Svc->>+Repo: save(entity)
    Repo->>+DB: INSERT INTO ...
    DB-->>-Repo: Created row
    Repo-->>-Svc: Persisted entity

    Svc-)Ntfy: Send safety alert

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 201 Created
```

---

### GET `/incidents/{incident_id}` — Get an incident report { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Incidents/getIncident){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /incidents/(incident_id)
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getIncident()

    Svc->>+Repo: findById(id)
    Repo->>+DB: SELECT ... WHERE id = ?
    DB-->>-Repo: Row
    Repo-->>-Svc: Entity
    Note right of Repo: Returns 404 if not found

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### PATCH `/incidents/{incident_id}` — Update an incident report (add follow-up, change status) { .endpoint-patch }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Incidents/updateIncident){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: PATCH /incidents/(incident_id)
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: updateIncident()

    Svc->>+Repo: findById(id)
    Repo->>+DB: SELECT ... FOR UPDATE
    DB-->>-Repo: Current row
    Repo-->>-Svc: Existing entity
    Note right of Svc: Merge changed fields only
    Svc->>+Repo: save(entity)
    Repo->>+DB: UPDATE ... SET ...
    DB-->>-Repo: Updated row
    Repo-->>-Svc: Updated entity

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### GET `/safety-inspections` — List safety inspections for a location { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Inspections/listSafetyInspections){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /safety-inspections
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: listSafetyInspections()

    Svc->>+Repo: findByFilters(criteria)
    Repo->>+DB: SELECT ... WHERE filters
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: Page of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### POST `/safety-inspections` — Record a safety inspection { .endpoint-post }

[:material-open-in-new: View in Swagger UI](../services/api/svc-safety-compliance.html#/Inspections/createSafetyInspection){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: POST /safety-inspections
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: createSafetyInspection()

    Svc->>+Repo: save(entity)
    Repo->>+DB: INSERT INTO ...
    DB-->>-Repo: Created row
    Repo-->>-Svc: Persisted entity

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 201 Created
```
