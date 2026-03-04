---
tags:
  - microservice
  - svc-reservations
  - booking
---

# svc-reservations

**Reservations Service** &nbsp;|&nbsp; <span style="background: #05966915; color: #059669; border: 1px solid #05966940; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">Booking</span> &nbsp;|&nbsp; `v2.4.1` &nbsp;|&nbsp; *NovaTrek Platform Team*

> Manages adventure trip reservations for NovaTrek Adventures.

[:material-api: Swagger UI](../services/api/svc-reservations.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-reservations.yaml){ .md-button }

---

## :material-database: Data Store

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `reservations` |
| **Primary Tables** | `reservations`, `participants`, `status_history` |
| **Key Features** | Optimistic locking via _rev field · Composite index on (guest_id, trip_date) · Monthly partitioning by reservation_date |
| **Estimated Volume** | ~2,000 new reservations/day |

---

## :material-api: Endpoints (8 total)

---

### GET `/reservations` — Search reservations { .endpoint-get }

> Returns a paginated list of reservations matching the given criteria.

[:material-open-in-new: View in Swagger UI](../services/api/svc-reservations.html#/Reservation%20Search/searchReservations){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /reservations
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: searchReservations()

    Svc->>+Repo: findByFilters(criteria)
    Repo->>+DB: SELECT ... WHERE filters
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: Page of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### POST `/reservations` — Create a new reservation { .endpoint-post }

> Creates a new adventure reservation. Validates guest eligibility,

[:material-open-in-new: View in Swagger UI](../services/api/svc-reservations.html#/Reservations/createReservation){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant GP as Guest Profiles
    participant TC as Trip Catalog
    participant Kafka as Event Bus
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: POST /reservations
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: createReservation()

    rect rgba(199, 123, 48, 0.08)
        Note over Svc,TC: Cross-service integration
        Svc->>+GP: Validate guest identity
        GP-->>-Svc: OK
        Svc->>+TC: Check trip availability
        TC-->>-Svc: OK
    end

    Svc->>+Repo: save(entity)
    Repo->>+DB: INSERT INTO ...
    DB-->>-Repo: Created row
    Repo-->>-Svc: Persisted entity

    Svc-)Kafka: reservation.created

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 201 Created
```

---

### GET `/reservations/{reservation_id}` — Get reservation details { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-reservations.html#/Reservations/getReservation){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /reservations/(reservation_id)
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getReservation()

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

### PATCH `/reservations/{reservation_id}` — Update a reservation { .endpoint-patch }

> Partially updates a reservation. Only modifiable fields can be changed.

[:material-open-in-new: View in Swagger UI](../services/api/svc-reservations.html#/Reservations/updateReservation){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: PATCH /reservations/(reservation_id)
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: updateReservation()

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

### DELETE `/reservations/{reservation_id}` — Cancel a reservation { .endpoint-delete }

[:material-open-in-new: View in Swagger UI](../services/api/svc-reservations.html#/Reservations/cancelReservation){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: DELETE /reservations/(reservation_id)
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: cancelReservation()

    Svc->>+Repo: findById(id)
    Repo->>+DB: SELECT ... WHERE id = ?
    DB-->>-Repo: Row
    Repo-->>-Svc: Entity
    Note right of Repo: Returns 404 if not found
    Svc->>+Repo: delete(entity)
    Repo->>+DB: DELETE FROM ... WHERE id = ?
    DB-->>-Repo: OK
    Repo-->>-Svc: void

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 204 No Content
```

---

### GET `/reservations/{reservation_id}/participants` — Get reservation participants { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-reservations.html#/Reservations/getParticipants){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /reservations/(reservation_id)/participants
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getParticipants()

    Svc->>+Repo: findByParent(parentId)
    Repo->>+DB: SELECT ... WHERE parent_id = ?
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: List of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### POST `/reservations/{reservation_id}/participants` — Add a participant to a reservation { .endpoint-post }

[:material-open-in-new: View in Swagger UI](../services/api/svc-reservations.html#/Reservations/addParticipant){ .md-button }

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

    C->>+GW: POST /reservations/(reservation_id)/participants
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: addParticipant()

    rect rgba(199, 123, 48, 0.08)
        Note over Svc,GP: Cross-service integration
        Svc->>+GP: Validate participant
        GP-->>-Svc: OK
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

### PUT `/reservations/{reservation_id}/status` — Transition reservation status { .endpoint-put }

> Explicitly transitions a reservation to a new status.

[:material-open-in-new: View in Swagger UI](../services/api/svc-reservations.html#/Reservation%20Status/transitionStatus){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Kafka as Event Bus
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: PUT /reservations/(reservation_id)/status
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: transitionStatus()

    Svc->>+Repo: findById(id)
    Repo->>+DB: SELECT ... FOR UPDATE
    DB-->>-Repo: Current row
    Repo-->>-Svc: Existing entity
    Note right of Svc: Replace mutable fields
    Svc->>+Repo: save(entity)
    Repo->>+DB: UPDATE ... SET ...
    DB-->>-Repo: Updated row
    Repo-->>-Svc: Updated entity

    Svc-)Kafka: reservation.status_changed

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```
