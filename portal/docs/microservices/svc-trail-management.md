---
tags:
  - microservice
  - svc-trail-management
  - product-catalog
---

# svc-trail-management

**NovaTrek Trail Management Service** &nbsp;|&nbsp; <span style="background: #d9770615; color: #d97706; border: 1px solid #d9770640; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">Product Catalog</span> &nbsp;|&nbsp; `v1.1.0` &nbsp;|&nbsp; *NovaTrek Platform Team*

> Manages trail definitions, waypoints, difficulty ratings, closures, and real-time

[:material-api: Swagger UI](../services/api/svc-trail-management.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-trail-management.yaml){ .md-button }
[:material-rocket-launch: Live Service (Dev)](https://ca-svc-trail-management.blackwater-fd4bc06d.eastus2.azurecontainerapps.io/actuator/health){ .md-button }
[:material-microsoft-azure: Azure Portal](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-trail-management){ .md-button }
[:material-pipe: CI/CD Pipeline](https://github.com/christopherblaisdell/continuous-architecture-platform-poc-2/actions/workflows/service-svc-trail-management.yml){ .md-button }
[:material-source-branch: Source Code](https://github.com/christopherblaisdell/continuous-architecture-platform-poc-2/tree/main/services/svc-trail-management){ .md-button }

## :material-truck-delivery: Delivery Status

**Delivery Wave:** 1 -- Guest Identity and Product Catalog

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

- [:material-microsoft-azure: Container App](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-trail-management)
- [:material-database: PostgreSQL Server](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.DBforPostgreSQL/flexibleServers/psql-novatrek-dev)
- [:material-text-search: Log Analytics](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.OperationalInsights/workspaces/log-novatrek-dev/logs)

---

## :material-map: Integration Context

<div class="diagram-wrap"><a href="../svg/svc-trail-management--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trail-management--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-trail-management C4 context diagram</object></div>


## :material-database: Data Store { #data-store }

### Entity Relationship Diagram

<div class="diagram-wrap"><a href="../svg/svc-trail-management--erd.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trail-management--erd.svg" type="image/svg+xml" style="max-width: 100%;">svc-trail-management entity relationship diagram</object></div>

### Overview

| Property | Detail |
|----------|--------|
| **Engine** | PostGIS (PostgreSQL 15) |
| **Schema** | `trails` |
| **Tables** | `trails`, `waypoints`, `closures`, `condition_reports` |
| **Estimated Volume** | ~200 condition updates/day, ~5K trail reads/day |
| **Connection Pool** | min 5 / max 15 / idle timeout 10min |
| **Backup Strategy** | Daily pg_dump with PostGIS extensions, 14-day retention |

### Key Features

- PostGIS geometry columns for trail routes and waypoints
- Spatial indexes (GiST) for proximity queries
- Time-series condition data with hypertable extension

### Table Reference

#### `trails`

*Trail definitions with geospatial route geometry*

| Column | Type | Constraints |
|--------|------|-------------|
| `trail_id` | `UUID` | PK |
| `name` | `VARCHAR(200)` | NOT NULL |
| `difficulty` | `VARCHAR(20)` | NOT NULL |
| `length_km` | `DECIMAL(6,2)` | NOT NULL |
| `elevation_gain_m` | `INTEGER` | NULL |
| `route` | `GEOMETRY(LineString, 4326)` | NOT NULL |
| `status` | `VARCHAR(20)` | NOT NULL, DEFAULT 'open' |
| `region_id` | `UUID` | NOT NULL |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_trail_route` on `route` (GiST spatial)
- `idx_trail_status` on `status`
- `idx_trail_region` on `region_id`

#### `waypoints`

*Points of interest and navigation markers along trails*

| Column | Type | Constraints |
|--------|------|-------------|
| `waypoint_id` | `UUID` | PK |
| `trail_id` | `UUID` | NOT NULL, FK -> trails |
| `name` | `VARCHAR(100)` | NOT NULL |
| `location` | `GEOMETRY(Point, 4326)` | NOT NULL |
| `waypoint_type` | `VARCHAR(30)` | NOT NULL |
| `elevation_m` | `INTEGER` | NULL |
| `sequence_order` | `INTEGER` | NOT NULL |

**Indexes:**

- `idx_wp_trail` on `trail_id, sequence_order`
- `idx_wp_location` on `location` (GiST spatial)

#### `condition_reports`

*Time-series trail condition observations from guides and sensors*

| Column | Type | Constraints |
|--------|------|-------------|
| `report_id` | `UUID` | PK |
| `trail_id` | `UUID` | NOT NULL, FK -> trails |
| `condition` | `VARCHAR(30)` | NOT NULL |
| `details` | `TEXT` | NULL |
| `reported_by` | `VARCHAR(100)` | NOT NULL |
| `reported_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_cond_trail_time` on `trail_id, reported_at DESC`


---

## :material-lightbulb: Solutions Affecting This Service

| Ticket | Solution | Capabilities | Date |
|--------|----------|-------------|------|
| NTK-10001 | [Add Elevation Profile Data to Trail Response](../solutions/_NTK-10001-add-elevation-to-trail-response.md) | `CAP-2.4` | 2025-02-01 |

---

## :material-api: Endpoints (9 total)

---

### GET `/trails` -- Search trails { .endpoint-get }

> Search and filter trails by region, difficulty, activity type, and status.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trail-management.html#/Trails/searchTrails){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-trail-management--get-trails.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trail-management--get-trails.svg" type="image/svg+xml" style="max-width: 100%;">GET /trails sequence diagram</object></div>

---

### POST `/trails` -- Create a new trail { .endpoint-post }

> Registers a new trail in the system. Requires operations or admin role.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trail-management.html#/Trails/createTrail){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-trail-management--post-trails.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trail-management--post-trails.svg" type="image/svg+xml" style="max-width: 100%;">POST /trails sequence diagram</object></div>

---

### GET `/trails/{trail_id}` -- Get trail details { .endpoint-get }

> Returns complete trail information including metadata, geography, and current status.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trail-management.html#/Trails/getTrail){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-trail-management--get-trails-trail_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trail-management--get-trails-trail_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /trails/{trail_id} sequence diagram</object></div>

---

### PATCH `/trails/{trail_id}` -- Update trail details { .endpoint-patch }

> Partially updates trail metadata. Does not modify waypoints or closures.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trail-management.html#/Trails/updateTrail){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-trail-management--patch-trails-trail_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trail-management--patch-trails-trail_id.svg" type="image/svg+xml" style="max-width: 100%;">PATCH /trails/{trail_id} sequence diagram</object></div>

---

### GET `/trails/{trail_id}/waypoints` -- List waypoints for a trail { .endpoint-get }

> Returns all waypoints along the trail in sequence order.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trail-management.html#/Waypoints/getTrailWaypoints){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-trail-management--get-trails-trail_id-waypoints.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trail-management--get-trails-trail_id-waypoints.svg" type="image/svg+xml" style="max-width: 100%;">GET /trails/{trail_id}/waypoints sequence diagram</object></div>

---

### POST `/trails/{trail_id}/waypoints` -- Add a waypoint to a trail { .endpoint-post }

> Appends a new waypoint to the trail. Position in sequence can be specified.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trail-management.html#/Waypoints/addWaypoint){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-trail-management--post-trails-trail_id-waypoints.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trail-management--post-trails-trail_id-waypoints.svg" type="image/svg+xml" style="max-width: 100%;">POST /trails/{trail_id}/waypoints sequence diagram</object></div>

---

### GET `/trails/{trail_id}/closures` -- List closures for a trail { .endpoint-get }

> Returns all current and scheduled closures for the specified trail.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trail-management.html#/Closures/getTrailClosures){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-trail-management--get-trails-trail_id-closures.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trail-management--get-trails-trail_id-closures.svg" type="image/svg+xml" style="max-width: 100%;">GET /trails/{trail_id}/closures sequence diagram</object></div>

---

### POST `/trails/{trail_id}/closures` -- Create a trail closure { .endpoint-post }

> Records a closure for the trail. Automatically updates trail status to

[:material-open-in-new: View in Swagger UI](../services/api/svc-trail-management.html#/Closures/createTrailClosure){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-trail-management--post-trails-trail_id-closures.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trail-management--post-trails-trail_id-closures.svg" type="image/svg+xml" style="max-width: 100%;">POST /trails/{trail_id}/closures sequence diagram</object></div>

---

### GET `/trails/{trail_id}/conditions` -- Get current trail conditions { .endpoint-get }

> Returns the latest condition assessment for the trail, combining data from

[:material-open-in-new: View in Swagger UI](../services/api/svc-trail-management.html#/Conditions/getTrailCurrentConditions){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-trail-management--get-trails-trail_id-conditions.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trail-management--get-trails-trail_id-conditions.svg" type="image/svg+xml" style="max-width: 100%;">GET /trails/{trail_id}/conditions sequence diagram</object></div>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Guest Portal](../../applications/web-guest-portal/) | Trip Browser |
| [Operations Dashboard](../../applications/web-ops-dashboard/) | Daily Schedule Board, Guide Assignment |
| [Adventure App](../../applications/app-guest-mobile/) | Live Trip Map, Weather and Trail Alerts |

---

## :material-broadcast-off: Events Consumed

| Event | Producer | Channel |
|-------|----------|---------|
| [`wildlife_alert.issued`](/events/#wildlife_alertissued) | [svc-wildlife-tracking](../svc-wildlife-tracking/) | `novatrek.safety.wildlife-alert.issued` |
