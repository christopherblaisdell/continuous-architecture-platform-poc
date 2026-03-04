---
tags:
  - microservice
  - svc-partner-integrations
  - external
---

# svc-partner-integrations

**NovaTrek Partner Integrations Service** &nbsp;|&nbsp; <span style="background: #9333ea15; color: #9333ea; border: 1px solid #9333ea40; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">External</span> &nbsp;|&nbsp; `v1.0.0` &nbsp;|&nbsp; *NovaTrek Partnerships Team*

> Manages third-party partner relationships and bookings from travel agents,

[:material-api: Swagger UI](../services/api/svc-partner-integrations.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-partner-integrations.yaml){ .md-button }

---

## :material-database: Data Store

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `partners` |
| **Primary Tables** | `partners`, `partner_bookings`, `commission_records`, `reconciliation_log` |
| **Key Features** | Partner API key management with rotation policy · Commission calculation engine with tiered rates · Idempotency keys for booking creation |
| **Estimated Volume** | ~400 partner bookings/day |

---

## :material-api: Endpoints (7 total)

---

### POST `/partner-bookings` — External partner creates a booking { .endpoint-post }

> Allows an authenticated partner to submit a booking request. Creates

[:material-open-in-new: View in Swagger UI](../services/api/svc-partner-integrations.html#/Partner%20Bookings/createPartnerBooking){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Res as Reservations
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: POST /partner-bookings
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: createPartnerBooking()

    rect rgba(199, 123, 48, 0.08)
        Note over Svc,Res: Cross-service integration
        Svc->>+Res: Create reservation
        Res-->>-Svc: OK
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

### GET `/partner-bookings/{booking_id}` — Get partner booking details { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-partner-integrations.html#/Partner%20Bookings/getPartnerBooking){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /partner-bookings/(booking_id)
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getPartnerBooking()

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

### PATCH `/partner-bookings/{booking_id}` — Update a partner booking { .endpoint-patch }

[:material-open-in-new: View in Swagger UI](../services/api/svc-partner-integrations.html#/Partner%20Bookings/updatePartnerBooking){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: PATCH /partner-bookings/(booking_id)
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: updatePartnerBooking()

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

### POST `/partner-bookings/{booking_id}/confirm` — Confirm a pending partner booking { .endpoint-post }

> Confirms availability and finalizes the partner booking. Triggers

[:material-open-in-new: View in Swagger UI](../services/api/svc-partner-integrations.html#/Partner%20Bookings/confirmPartnerBooking){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Res as Reservations
    participant Pay as Payments Svc
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: POST /partner-bookings/(booking_id)/confirm
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: confirmPartnerBooking()

    rect rgba(199, 123, 48, 0.08)
        Note over Svc,Pay: Cross-service integration
        Svc->>+Res: Confirm reservation
        Res-->>-Svc: OK
        Svc->>+Pay: Process commission
        Pay-->>-Svc: OK
    end

    Svc->>+Repo: findParent(parentId)
    Repo->>+DB: SELECT parent
    DB-->>-Repo: Parent row
    Repo-->>-Svc: Parent entity
    Note right of Repo: 404 if parent not found
    Svc->>+Repo: save(entity)
    Repo->>+DB: INSERT INTO ...
    DB-->>-Repo: Created row
    Repo-->>-Svc: Persisted entity

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 201 Created
```

---

### GET `/partners` — List registered partners { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-partner-integrations.html#/Partners/listPartners){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /partners
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: listPartners()

    Svc->>+Repo: findByFilters(criteria)
    Repo->>+DB: SELECT ... WHERE filters
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: Page of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### POST `/partners` — Register a new partner { .endpoint-post }

[:material-open-in-new: View in Swagger UI](../services/api/svc-partner-integrations.html#/Partners/registerPartner){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: POST /partners
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: registerPartner()

    Svc->>+Repo: save(entity)
    Repo->>+DB: INSERT INTO ...
    DB-->>-Repo: Created row
    Repo-->>-Svc: Persisted entity

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 201 Created
```

---

### GET `/partners/{partner_id}/commission-report` — Get commission report for a partner { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-partner-integrations.html#/Partners/getCommissionReport){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /partners/(partner_id)/commission-report
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getCommissionReport()

    Svc->>+Repo: findByParent(parentId)
    Repo->>+DB: SELECT ... WHERE parent_id = ?
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: List of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```
