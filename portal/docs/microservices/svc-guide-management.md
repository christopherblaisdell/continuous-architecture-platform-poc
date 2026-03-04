---
tags:
  - microservice
  - svc-guide-management
  - guide-management
---

# svc-guide-management

**NovaTrek Guide Management Service** &nbsp;|&nbsp; <span style="background: #4f46e515; color: #4f46e5; border: 1px solid #4f46e540; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">Guide Management</span> &nbsp;|&nbsp; `v2.4.0` &nbsp;|&nbsp; *NovaTrek Platform Engineering*

> Manages adventure guides for NovaTrek Adventures, including guide profiles,

[:material-api: Swagger UI](../services/api/svc-guide-management.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-guide-management.yaml){ .md-button }

---

## :material-database: Data Store

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `guides` |
| **Primary Tables** | `guides`, `certifications`, `guide_schedules`, `availability_windows`, `ratings` |
| **Key Features** | Certification expiry tracking with automated alerts · Availability window overlap detection constraints · Weighted rating aggregation with recency bias |
| **Estimated Volume** | ~100 schedule updates/day, ~500 availability queries/day |

---

## :material-api: Endpoints (12 total)

---

### GET `/guides` — Search guides with filters { .endpoint-get }

> Returns a paginated list of guides matching the specified filter criteria.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Guides/searchGuides){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /guides
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: searchGuides()

    Svc->>+Repo: findByFilters(criteria)
    Repo->>+DB: SELECT ... WHERE filters
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: Page of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### POST `/guides` — Create a new guide profile { .endpoint-post }

> Registers a new adventure guide in the system.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Guides/createGuide){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: POST /guides
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: createGuide()

    Svc->>+Repo: save(entity)
    Repo->>+DB: INSERT INTO ...
    DB-->>-Repo: Created row
    Repo-->>-Svc: Persisted entity

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 201 Created
```

---

### GET `/guides/{guide_id}` — Get guide by ID { .endpoint-get }

> Retrieves the full profile for a specific guide.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Guides/getGuide){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /guides/(guide_id)
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getGuide()

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

### PATCH `/guides/{guide_id}` — Update guide profile { .endpoint-patch }

> Partially updates a guide profile. Only provided fields are modified.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Guides/updateGuide){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: PATCH /guides/(guide_id)
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: updateGuide()

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

### GET `/guides/{guide_id}/certifications` — List guide certifications { .endpoint-get }

> Returns all certifications held by the specified guide.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Certifications/getGuideCertifications){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /guides/(guide_id)/certifications
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getGuideCertifications()

    Svc->>+Repo: findByParent(parentId)
    Repo->>+DB: SELECT ... WHERE parent_id = ?
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: List of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### POST `/guides/{guide_id}/certifications` — Add a certification to a guide { .endpoint-post }

> Records a new certification for the specified guide.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Certifications/addGuideCertification){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: POST /guides/(guide_id)/certifications
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: addGuideCertification()

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

### GET `/guides/{guide_id}/schedule` — Get upcoming trip assignments { .endpoint-get }

> Returns the guide's upcoming scheduled trip assignments.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Scheduling/getGuideSchedule){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /guides/(guide_id)/schedule
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getGuideSchedule()

    Svc->>+Repo: findByParent(parentId)
    Repo->>+DB: SELECT ... WHERE parent_id = ?
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: List of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### GET `/guides/{guide_id}/availability` — Get guide availability windows { .endpoint-get }

> Returns the availability windows configured for this guide.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Availability/getGuideAvailability){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /guides/(guide_id)/availability
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getGuideAvailability()

    Svc->>+Repo: findByParent(parentId)
    Repo->>+DB: SELECT ... WHERE parent_id = ?
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: List of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### POST `/guides/{guide_id}/availability` — Set availability windows { .endpoint-post }

> Creates or updates availability windows for the guide.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Availability/setGuideAvailability){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: POST /guides/(guide_id)/availability
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: setGuideAvailability()

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

### GET `/guides/{guide_id}/ratings` — Get guest ratings and reviews { .endpoint-get }

> Returns paginated guest ratings and reviews for the specified guide.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Ratings/getGuideRatings){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /guides/(guide_id)/ratings
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getGuideRatings()

    Svc->>+Repo: findByParent(parentId)
    Repo->>+DB: SELECT ... WHERE parent_id = ?
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: List of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### POST `/guides/{guide_id}/ratings` — Submit a guest rating { .endpoint-post }

> Records a guest rating and optional review for a guide.

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Ratings/submitGuideRating){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: POST /guides/(guide_id)/ratings
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: submitGuideRating()

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

### GET `/guides/available` — Find available guides for a date, activity, and region { .endpoint-get }

> Searches for guides who are available on the specified date, hold relevant

[:material-open-in-new: View in Swagger UI](../services/api/svc-guide-management.html#/Availability/findAvailableGuides){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /guides/available
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: findAvailableGuides()

    Svc->>+Repo: findByFilters(criteria)
    Repo->>+DB: SELECT ... WHERE filters
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: Page of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```
