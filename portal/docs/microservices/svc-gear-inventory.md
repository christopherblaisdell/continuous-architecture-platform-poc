---
tags:
  - microservice
  - svc-gear-inventory
  - logistics
---

# svc-gear-inventory

**NovaTrek Adventures - Gear Inventory Service** &nbsp;|&nbsp; <span style="background: #0891b215; color: #0891b2; border: 1px solid #0891b240; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">Logistics</span> &nbsp;|&nbsp; `v2.4.0` &nbsp;|&nbsp; *NovaTrek Platform Engineering*

> Manages rental equipment inventory, gear packages, guest assignments,

[:material-api: Swagger UI](../services/api/svc-gear-inventory.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-gear-inventory.yaml){ .md-button }

---

## :material-database: Data Store

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `gear` |
| **Primary Tables** | `gear_items`, `gear_packages`, `gear_assignments`, `maintenance_records`, `inventory_levels` |
| **Key Features** | RFID tag tracking via unique identifiers · Scheduled maintenance alerts with cron triggers · Location-based inventory partitioning |
| **Estimated Volume** | ~1,500 assignments/day peak season |

---

## :material-api: Endpoints (12 total)

---

### GET `/gear-items` — Search gear inventory { .endpoint-get }

> Returns a paginated list of gear items matching the provided filters.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Items/searchGearItems){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /gear-items
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: searchGearItems()

    Svc->>+Repo: findByFilters(criteria)
    Repo->>+DB: SELECT ... WHERE filters
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: Page of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### POST `/gear-items` — Add new inventory item { .endpoint-post }

> Registers a new piece of gear in the inventory system.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Items/addGearItem){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: POST /gear-items
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: addGearItem()

    Svc->>+Repo: save(entity)
    Repo->>+DB: INSERT INTO ...
    DB-->>-Repo: Created row
    Repo-->>-Svc: Persisted entity

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 201 Created
```

---

### GET `/gear-items/{item_id}` — Get gear item details { .endpoint-get }

> Returns full details for a single gear item including current status and maintenance schedule.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Items/getGearItem){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /gear-items/(item_id)
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getGearItem()

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

### PATCH `/gear-items/{item_id}` — Update gear item { .endpoint-patch }

> Partially updates a gear item record. Only provided fields are modified.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Items/updateGearItem){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: PATCH /gear-items/(item_id)
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: updateGearItem()

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

### GET `/gear-packages` — List gear packages { .endpoint-get }

> Returns all predefined gear bundles, optionally filtered by activity type.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Packages/listGearPackages){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /gear-packages
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: listGearPackages()

    Svc->>+Repo: findByFilters(criteria)
    Repo->>+DB: SELECT ... WHERE filters
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: Page of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### GET `/gear-packages/{package_id}` — Get gear package details { .endpoint-get }

> Returns full details for a gear package including the list of included items and pricing.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Packages/getGearPackage){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /gear-packages/(package_id)
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getGearPackage()

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

### POST `/gear-assignments` — Assign gear to a participant { .endpoint-post }

> Creates a gear assignment linking inventory items to a trip participant.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Assignments/createGearAssignment){ .md-button }

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

    C->>+GW: POST /gear-assignments
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: createGearAssignment()

    rect rgba(199, 123, 48, 0.08)
        Note over Svc,GP: Cross-service integration
        Svc->>+GP: Validate guest
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

### GET `/gear-assignments/{assignment_id}` — Get gear assignment details { .endpoint-get }

> Returns full details of a gear assignment including item list and return status.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Assignments/getGearAssignment){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /gear-assignments/(assignment_id)
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getGearAssignment()

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

### DELETE `/gear-assignments/{assignment_id}` — Return gear (close assignment) { .endpoint-delete }

> Marks gear as returned and closes the assignment. Accepts optional

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Assignments/returnGearAssignment){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: DELETE /gear-assignments/(assignment_id)
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: returnGearAssignment()

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

### PUT `/gear-items/{item_id}/maintenance` — Log a maintenance event { .endpoint-put }

> Records a maintenance event (inspection, repair, or part replacement) for a gear item and updates its condition and next-due date.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Maintenance/logMaintenanceEvent){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: PUT /gear-items/(item_id)/maintenance
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: logMaintenanceEvent()

    Svc->>+Repo: findById(id)
    Repo->>+DB: SELECT ... FOR UPDATE
    DB-->>-Repo: Current row
    Repo-->>-Svc: Existing entity
    Note right of Svc: Replace mutable fields
    Svc->>+Repo: save(entity)
    Repo->>+DB: UPDATE ... SET ...
    DB-->>-Repo: Updated row
    Repo-->>-Svc: Updated entity

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### GET `/gear-items/{item_id}/maintenance-history` — Get maintenance history { .endpoint-get }

> Returns the chronological maintenance history for a specific gear item.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Maintenance/getMaintenanceHistory){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /gear-items/(item_id)/maintenance-history
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getMaintenanceHistory()

    Svc->>+Repo: findByParent(parentId)
    Repo->>+DB: SELECT ... WHERE parent_id = ?
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: List of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### GET `/inventory-levels` — Get stock levels by location and category { .endpoint-get }

> Returns current inventory counts broken down by location and gear category, including available, assigned, and in-maintenance tallies.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Inventory%20Levels/getInventoryLevels){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /inventory-levels
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getInventoryLevels()

    Svc->>+Repo: findByFilters(criteria)
    Repo->>+DB: SELECT ... WHERE filters
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: Page of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```
