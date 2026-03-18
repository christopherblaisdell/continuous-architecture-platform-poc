---
tags:
  - microservice
  - svc-location-services
  - support
---

# svc-location-services

**NovaTrek Location Services API** &nbsp;|&nbsp; <span style="background: #64748b15; color: #64748b; border: 1px solid #64748b40; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">Support</span> &nbsp;|&nbsp; `v1.2.0` &nbsp;|&nbsp; *NovaTrek Platform Engineering*

> Manages physical locations across the NovaTrek network including base camps,

[:material-api: Swagger UI](../services/api/svc-location-services.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-location-services.yaml){ .md-button }
[:material-rocket-launch: Live Service (Dev)](https://ca-svc-location-services.blackwater-fd4bc06d.eastus2.azurecontainerapps.io/actuator/health){ .md-button }
[:material-microsoft-azure: Azure Portal](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-location-services){ .md-button }
[:material-pipe: CI/CD Pipeline](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/service-ci.yml){ .md-button }
[:material-source-branch: Source Code](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/services/svc-location-services){ .md-button }
[:material-language-java: Technology Stack](../technologies.md){ .md-button }

## :material-truck-delivery: Delivery Status

**Delivery Wave:** 4 -- Guide and Transport Operations

| Stage | Status |
|-------|--------|
| Infrastructure (Bicep) | :white_check_mark: complete |
| Database Schema (Flyway) | :white_check_mark: complete |
| CI Pipeline | :material-circle-outline: not-started |
| CD Pipeline | :material-circle-outline: not-started |
| Deployed to Dev | :white_check_mark: complete |
| Smoke Tested | :white_check_mark: complete |
| Deployed to Prod | :material-circle-outline: not-started |

**Azure Resources (Dev):**

- [:material-microsoft-azure: Container App](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-location-services)
- [:material-database: PostgreSQL Server](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.DBforPostgreSQL/flexibleServers/pg-novatrek-dev-smwd6ded4e3so)
- [:material-text-search: Log Analytics](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.OperationalInsights/workspaces/log-novatrek-dev/logs)

---

## :material-map: Integration Context

<div class="diagram-wrap"><a href="../svg/svc-location-services--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-location-services--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-location-services C4 context diagram</object></div>


## :material-database: Data Store { #data-store }

### Entity Relationship Diagram

<div class="diagram-wrap"><a href="../svg/svc-location-services--erd.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-location-services--erd.svg" type="image/svg+xml" style="max-width: 100%;">svc-location-services entity relationship diagram</object></div>

### Overview

| Property | Detail |
|----------|--------|
| **Engine** | PostGIS (PostgreSQL 15) |
| **Schema** | `locations` |
| **Tables** | `locations`, `capacity_records`, `operating_hours` |
| **Estimated Volume** | ~100 updates/day, ~2K reads/day |
| **Connection Pool** | min 3 / max 10 / idle timeout 10min |
| **Backup Strategy** | Daily pg_dump, 14-day retention |

### Key Features

- PostGIS geometry for geofencing and proximity queries
- Real-time capacity tracking with threshold alerts
- Timezone-aware operating hours management

### Table Reference

#### `locations`

*Adventure locations and facilities with geospatial boundaries*

| Column | Type | Constraints |
|--------|------|-------------|
| `location_id` | `UUID` | PK |
| `name` | `VARCHAR(200)` | NOT NULL |
| `location_type` | `VARCHAR(30)` | NOT NULL |
| `boundary` | `GEOMETRY(Polygon, 4326)` | NOT NULL |
| `center_point` | `GEOMETRY(Point, 4326)` | NOT NULL |
| `max_capacity` | `INTEGER` | NOT NULL |
| `timezone` | `VARCHAR(50)` | NOT NULL |
| `active` | `BOOLEAN` | NOT NULL, DEFAULT TRUE |

**Indexes:**

- `idx_loc_boundary` on `boundary` (GiST spatial)
- `idx_loc_center` on `center_point` (GiST spatial)
- `idx_loc_type` on `location_type`

#### `capacity_records`

*Real-time occupancy tracking for locations*

| Column | Type | Constraints |
|--------|------|-------------|
| `record_id` | `UUID` | PK |
| `location_id` | `UUID` | NOT NULL, FK -> locations |
| `current_count` | `INTEGER` | NOT NULL |
| `recorded_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_cap_loc_time` on `location_id, recorded_at DESC`


---

## :material-api: Endpoints (6 total)

---

### GET `/locations` -- List all locations { .endpoint-get }

> Returns a paginated list of NovaTrek locations with optional filtering by type, region, or status.

[:material-open-in-new: View in Swagger UI](../services/api/svc-location-services.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-location-services--get-locations.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-location-services--get-locations.svg" type="image/svg+xml" style="max-width: 100%;">GET /locations sequence diagram</object></div>

---

### POST `/locations` -- Create a new location { .endpoint-post }

[:material-open-in-new: View in Swagger UI](../services/api/svc-location-services.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-location-services--post-locations.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-location-services--post-locations.svg" type="image/svg+xml" style="max-width: 100%;">POST /locations sequence diagram</object></div>

---

### GET `/locations/{location_id}` -- Get location details { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-location-services.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-location-services--get-locations-location_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-location-services--get-locations-location_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /locations/{location_id} sequence diagram</object></div>

---

### PATCH `/locations/{location_id}` -- Update location details { .endpoint-patch }

[:material-open-in-new: View in Swagger UI](../services/api/svc-location-services.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-location-services--patch-locations-location_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-location-services--patch-locations-location_id.svg" type="image/svg+xml" style="max-width: 100%;">PATCH /locations/{location_id} sequence diagram</object></div>

---

### GET `/locations/{location_id}/capacity` -- Get current capacity utilization { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-location-services.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-location-services--get-locations-location_id-capacity.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-location-services--get-locations-location_id-capacity.svg" type="image/svg+xml" style="max-width: 100%;">GET /locations/{location_id}/capacity sequence diagram</object></div>

---

### GET `/locations/{location_id}/operating-hours` -- Get operating hours for a location { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-location-services.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-location-services--get-locations-location_id-operating-hours.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-location-services--get-locations-location_id-operating-hours.svg" type="image/svg+xml" style="max-width: 100%;">GET /locations/{location_id}/operating-hours sequence diagram</object></div>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Operations Dashboard](../../applications/web-ops-dashboard/) | Daily Schedule Board, Transport Dispatch |
| [Adventure App](../../applications/app-guest-mobile/) | Live Trip Map |
