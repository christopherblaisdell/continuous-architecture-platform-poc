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

---

## :material-database: Data Store

| Property | Detail |
|----------|--------|
| **Engine** | PostGIS (PostgreSQL 15) |
| **Schema** | `trails` |
| **Primary Tables** | `trails`, `waypoints`, `closures`, `condition_reports` |
| **Key Features** | PostGIS geometry columns for trail routes and waypoints | Spatial indexes (GiST) for proximity queries | Time-series condition data with hypertable extension |
| **Estimated Volume** | ~200 condition updates/day, ~5K trail reads/day |

---

## :material-api: Endpoints (9 total)

---

### GET `/trails` -- Search trails { .endpoint-get }

> Search and filter trails by region, difficulty, activity type, and status.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trail-management.html#/Trails/searchTrails){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-trail-management--get-trails.svg" type="image/svg+xml" style="max-width: 100%;">GET /trails sequence diagram</object></div>

---

### POST `/trails` -- Create a new trail { .endpoint-post }

> Registers a new trail in the system. Requires operations or admin role.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trail-management.html#/Trails/createTrail){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-trail-management--post-trails.svg" type="image/svg+xml" style="max-width: 100%;">POST /trails sequence diagram</object></div>

---

### GET `/trails/{trail_id}` -- Get trail details { .endpoint-get }

> Returns complete trail information including metadata, geography, and current status.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trail-management.html#/Trails/getTrail){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-trail-management--get-trails-trail_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /trails/{trail_id} sequence diagram</object></div>

---

### PATCH `/trails/{trail_id}` -- Update trail details { .endpoint-patch }

> Partially updates trail metadata. Does not modify waypoints or closures.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trail-management.html#/Trails/updateTrail){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-trail-management--patch-trails-trail_id.svg" type="image/svg+xml" style="max-width: 100%;">PATCH /trails/{trail_id} sequence diagram</object></div>

---

### GET `/trails/{trail_id}/waypoints` -- List waypoints for a trail { .endpoint-get }

> Returns all waypoints along the trail in sequence order.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trail-management.html#/Waypoints/getTrailWaypoints){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-trail-management--get-trails-trail_id-waypoints.svg" type="image/svg+xml" style="max-width: 100%;">GET /trails/{trail_id}/waypoints sequence diagram</object></div>

---

### POST `/trails/{trail_id}/waypoints` -- Add a waypoint to a trail { .endpoint-post }

> Appends a new waypoint to the trail. Position in sequence can be specified.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trail-management.html#/Waypoints/addWaypoint){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-trail-management--post-trails-trail_id-waypoints.svg" type="image/svg+xml" style="max-width: 100%;">POST /trails/{trail_id}/waypoints sequence diagram</object></div>

---

### GET `/trails/{trail_id}/closures` -- List closures for a trail { .endpoint-get }

> Returns all current and scheduled closures for the specified trail.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trail-management.html#/Closures/getTrailClosures){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-trail-management--get-trails-trail_id-closures.svg" type="image/svg+xml" style="max-width: 100%;">GET /trails/{trail_id}/closures sequence diagram</object></div>

---

### POST `/trails/{trail_id}/closures` -- Create a trail closure { .endpoint-post }

> Records a closure for the trail. Automatically updates trail status to

[:material-open-in-new: View in Swagger UI](../services/api/svc-trail-management.html#/Closures/createTrailClosure){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-trail-management--post-trails-trail_id-closures.svg" type="image/svg+xml" style="max-width: 100%;">POST /trails/{trail_id}/closures sequence diagram</object></div>

---

### GET `/trails/{trail_id}/conditions` -- Get current trail conditions { .endpoint-get }

> Returns the latest condition assessment for the trail, combining data from

[:material-open-in-new: View in Swagger UI](../services/api/svc-trail-management.html#/Conditions/getTrailCurrentConditions){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-trail-management--get-trails-trail_id-conditions.svg" type="image/svg+xml" style="max-width: 100%;">GET /trails/{trail_id}/conditions sequence diagram</object></div>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Guest Portal](../../applications/web-guest-portal/) | Trip Browser |
| [Operations Dashboard](../../applications/web-ops-dashboard/) | Daily Schedule Board, Guide Assignment |
| [Adventure App](../../applications/app-guest-mobile/) | Live Trip Map, Weather and Trail Alerts |
