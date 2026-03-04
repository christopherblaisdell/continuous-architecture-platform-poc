---
tags:
  - microservice
  - svc-scheduling-orchestrator
  - operations
---

# svc-scheduling-orchestrator

**NovaTrek Scheduling Orchestrator API** &nbsp;|&nbsp; <span style="background: #2563eb15; color: #2563eb; border: 1px solid #2563eb40; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">Operations</span> &nbsp;|&nbsp; `v3.0.1` &nbsp;|&nbsp; *NovaTrek Platform Engineering*

> Central orchestration service for NovaTrek trip scheduling. Coordinates guide

[:material-api: Swagger UI](../services/api/svc-scheduling-orchestrator.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-scheduling-orchestrator.yaml){ .md-button }

---

## :material-database: Data Store

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 + Redis 7 |
| **Schema** | `scheduling` |
| **Primary Tables** | `schedule_requests`, `daily_schedules`, `schedule_conflicts`, `optimization_runs` |
| **Key Features** | Optimistic locking per ADR-011 · Redis for schedule lock cache and optimization queue · JSONB columns for constraint parameters |
| **Estimated Volume** | ~500 schedule requests/day |

---

## :material-api: Endpoints (5 total)

---

### POST `/schedule-requests` — Request optimal schedule for a trip { .endpoint-post }

> Submits a scheduling request that evaluates preferred dates against

[:material-open-in-new: View in Swagger UI](../services/api/svc-scheduling-orchestrator.html){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant GM as Guide Mgmt
    participant TM as Trail Mgmt
    participant WX as Weather Svc
    participant TC as Trip Catalog
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: POST /schedule-requests
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: createScheduleRequest()

    rect rgba(199, 123, 48, 0.08)
        Note over Svc,TC: Cross-service integration
        Svc->>+GM: Check guide availability
        GM-->>-Svc: OK
        Svc->>+TM: Verify trail conditions
        TM-->>-Svc: OK
        Svc->>+WX: Get forecast
        WX-->>-Svc: OK
        Svc->>+TC: Get trip details
        TC-->>-Svc: OK
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

### GET `/schedule-requests/{request_id}` — Get schedule request status and result { .endpoint-get }

> Poll this endpoint to retrieve the status and, once complete, the

[:material-open-in-new: View in Swagger UI](../services/api/svc-scheduling-orchestrator.html){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /schedule-requests/(request_id)
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getScheduleRequest()

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

### GET `/schedule-optimization` — Run synchronous schedule optimization { .endpoint-get }

> Performs a real-time scheduling optimization for a specific trip and

[:material-open-in-new: View in Swagger UI](../services/api/svc-scheduling-orchestrator.html){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /schedule-optimization
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getScheduleOptimization()

    Svc->>+Repo: findByFilters(criteria)
    Repo->>+DB: SELECT ... WHERE filters
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: Page of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### GET `/schedule-conflicts` — List scheduling conflicts { .endpoint-get }

> Returns active scheduling conflicts for a given date and/or region.

[:material-open-in-new: View in Swagger UI](../services/api/svc-scheduling-orchestrator.html){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /schedule-conflicts
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: listScheduleConflicts()

    Svc->>+Repo: findByFilters(criteria)
    Repo->>+DB: SELECT ... WHERE filters
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: Page of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### POST `/schedule-conflicts/resolve` — Resolve a scheduling conflict { .endpoint-post }

> Applies a resolution to an identified scheduling conflict. The resolution

[:material-open-in-new: View in Swagger UI](../services/api/svc-scheduling-orchestrator.html){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant GM as Guide Mgmt
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: POST /schedule-conflicts/resolve
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: resolveScheduleConflict()

    rect rgba(199, 123, 48, 0.08)
        Note over Svc,GM: Cross-service integration
        Svc->>+GM: Reassign guide
        GM-->>-Svc: OK
    end

    Svc->>+Repo: save(entity)
    Repo->>+DB: INSERT INTO ...
    DB-->>-Repo: Created row
    Repo-->>-Svc: Persisted entity

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 201 Created
```
