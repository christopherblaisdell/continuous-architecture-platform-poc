---
tags:
  - microservice
  - svc-transport-logistics
  - logistics
---

# svc-transport-logistics

**NovaTrek Transport Logistics API** &nbsp;|&nbsp; <span style="background: #0891b215; color: #0891b2; border: 1px solid #0891b240; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">Logistics</span> &nbsp;|&nbsp; `v1.4.0` &nbsp;|&nbsp; *NovaTrek Platform Engineering*

> Manages shuttle buses, van pickups, and transport coordination between NovaTrek

[:material-api: Swagger UI](../services/api/svc-transport-logistics.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-transport-logistics.yaml){ .md-button }
[:material-rocket-launch: Live Service (Dev)](https://ca-svc-transport-logistics.blackwater-fd4bc06d.eastus2.azurecontainerapps.io/actuator/health){ .md-button }
[:material-microsoft-azure: Azure Portal](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-transport-logistics){ .md-button }
[:material-pipe: CI/CD Pipeline](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/service-ci.yml){ .md-button }
[:material-source-branch: Source Code](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/services/svc-transport-logistics){ .md-button }
[:material-language-java: Technology Stack](../technologies.md){ .md-button }

## :material-truck-delivery: Delivery Status

**Delivery Wave:** 4 -- Guide and Transport Operations

| Stage | Status |
|-------|--------|
| Infrastructure (Bicep) | :white_check_mark: complete |
| Database Schema (Flyway) | :white_check_mark: complete |
| Deployed to Dev | :white_check_mark: complete |
| Smoke Tested | :white_check_mark: complete |
| Deployed to Prod | :material-circle-outline: not-started |


| Pipeline | Status |
|----------|--------|
| CI Pipeline | :white_check_mark: complete |
| CD Pipeline | :white_check_mark: complete |

**Azure Resources (Dev):**

- [:material-microsoft-azure: Container App](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-transport-logistics)
- [:material-database: PostgreSQL Server](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.DBforPostgreSQL/flexibleServers/pg-novatrek-dev-smwd6ded4e3so)
- [:material-text-search: Log Analytics](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.OperationalInsights/workspaces/log-novatrek-dev/logs)

---

## :material-map: Integration Context

<div class="diagram-wrap"><a href="../svg/svc-transport-logistics--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-transport-logistics--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-transport-logistics C4 context diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-transport-logistics.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-transport-logistics.yaml` + `cross-service-calls.yaml`</a>


## :material-database: Data Store { #data-store }

### Entity Relationship Diagram

<div class="diagram-wrap"><a href="../svg/svc-transport-logistics--erd.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-transport-logistics--erd.svg" type="image/svg+xml" style="max-width: 100%;">svc-transport-logistics entity relationship diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/data-stores.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/metadata/data-stores.yaml`</a>

### Overview

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `transport` |
| **Tables** | `routes`, `route_schedules`, `transport_requests`, `vehicles` |
| **Estimated Volume** | ~300 transport requests/day |
| **Connection Pool** | min 3 / max 10 / idle timeout 10min |
| **Backup Strategy** | Daily pg_dump, 14-day retention |

### Key Features

- Time-window optimization for route scheduling
- Vehicle capacity tracking with overbooking prevention
- GPS coordinate storage for pickup and dropoff points

### Table Reference

#### `vehicles`

*Fleet vehicles with capacity and maintenance status*

| Column | Type | Constraints |
|--------|------|-------------|
| `vehicle_id` | `UUID` | PK |
| `registration` | `VARCHAR(20)` | NOT NULL, UNIQUE |
| `vehicle_type` | `VARCHAR(30)` | NOT NULL |
| `capacity` | `INTEGER` | NOT NULL |
| `status` | `VARCHAR(20)` | NOT NULL, DEFAULT 'available' |
| `current_location` | `POINT` | NULL |
| `last_service_date` | `DATE` | NULL |

**Indexes:**

- `idx_vehicle_status` on `status`
- `idx_vehicle_type` on `vehicle_type`

#### `transport_requests`

*Guest and staff transport requests with pickup windows*

| Column | Type | Constraints |
|--------|------|-------------|
| `request_id` | `UUID` | PK |
| `route_id` | `UUID` | NOT NULL, FK -> routes |
| `vehicle_id` | `UUID` | NULL, FK -> vehicles |
| `passenger_count` | `INTEGER` | NOT NULL |
| `pickup_time` | `TIMESTAMPTZ` | NOT NULL |
| `pickup_location` | `POINT` | NOT NULL |
| `dropoff_location` | `POINT` | NOT NULL |
| `status` | `VARCHAR(20)` | NOT NULL |
| `created_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_treq_route` on `route_id`
- `idx_treq_pickup` on `pickup_time`
- `idx_treq_vehicle` on `vehicle_id`


---

## :material-api: Endpoints (7 total)

---

### GET `/routes` -- List transport routes { .endpoint-get }

> Returns available transport routes with optional filtering by origin, destination, or active status.

[:material-open-in-new: View in Swagger UI](../services/api/svc-transport-logistics.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-transport-logistics--get-routes.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-transport-logistics--get-routes.svg" type="image/svg+xml" style="max-width: 100%;">GET /routes sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-transport-logistics.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-transport-logistics.yaml`</a>

---

### POST `/routes` -- Create a new transport route { .endpoint-post }

[:material-open-in-new: View in Swagger UI](../services/api/svc-transport-logistics.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-transport-logistics--post-routes.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-transport-logistics--post-routes.svg" type="image/svg+xml" style="max-width: 100%;">POST /routes sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-transport-logistics.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-transport-logistics.yaml`</a>

---

### GET `/routes/{route_id}/schedule` -- Get schedule for a transport route { .endpoint-get }

> Returns the daily schedule of departures for a given route, optionally filtered by date range.

[:material-open-in-new: View in Swagger UI](../services/api/svc-transport-logistics.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-transport-logistics--get-routes-route_id-schedule.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-transport-logistics--get-routes-route_id-schedule.svg" type="image/svg+xml" style="max-width: 100%;">GET /routes/{route_id}/schedule sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-transport-logistics.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-transport-logistics.yaml`</a>

---

### POST `/transport-requests` -- Request transport for a reservation { .endpoint-post }

> Creates a transport request linked to an existing reservation

[:material-open-in-new: View in Swagger UI](../services/api/svc-transport-logistics.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-transport-logistics--post-transport-requests.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-transport-logistics--post-transport-requests.svg" type="image/svg+xml" style="max-width: 100%;">POST /transport-requests sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-transport-logistics.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-transport-logistics.yaml`</a>

---

### GET `/transport-requests/{request_id}` -- Get transport request details { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-transport-logistics.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-transport-logistics--get-transport-requests-request_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-transport-logistics--get-transport-requests-request_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /transport-requests/{request_id} sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-transport-logistics.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-transport-logistics.yaml`</a>

---

### GET `/vehicles` -- List fleet vehicles { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-transport-logistics.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-transport-logistics--get-vehicles.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-transport-logistics--get-vehicles.svg" type="image/svg+xml" style="max-width: 100%;">GET /vehicles sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-transport-logistics.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-transport-logistics.yaml`</a>

---

### PATCH `/vehicles/{vehicle_id}` -- Update vehicle information { .endpoint-patch }

[:material-open-in-new: View in Swagger UI](../services/api/svc-transport-logistics.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-transport-logistics--patch-vehicles-vehicle_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-transport-logistics--patch-vehicles-vehicle_id.svg" type="image/svg+xml" style="max-width: 100%;">PATCH /vehicles/{vehicle_id} sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-transport-logistics.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-transport-logistics.yaml`</a>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Operations Dashboard](../../applications/web-ops-dashboard/) | Transport Dispatch |
