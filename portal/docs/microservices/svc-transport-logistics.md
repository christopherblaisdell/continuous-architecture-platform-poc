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

---

## :material-map: Integration Context

<div class="diagram-wrap"><a href="../svg/svc-transport-logistics--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-transport-logistics--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-transport-logistics C4 context diagram</object></div>


| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `transport` |
| **Primary Tables** | `routes`, `route_schedules`, `transport_requests`, `vehicles` |
| **Key Features** | Time-window optimization for route scheduling | Vehicle capacity tracking with overbooking prevention | GPS coordinate storage for pickup and dropoff points |
| **Estimated Volume** | ~300 transport requests/day |

---

## :material-api: Endpoints (7 total)

---

### GET `/routes` -- List transport routes { .endpoint-get }

> Returns available transport routes with optional filtering by origin, destination, or active status.

[:material-open-in-new: View in Swagger UI](../services/api/svc-transport-logistics.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-transport-logistics--get-routes.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-transport-logistics--get-routes.svg" type="image/svg+xml" style="max-width: 100%;">GET /routes sequence diagram</object></div>

---

### POST `/routes` -- Create a new transport route { .endpoint-post }

[:material-open-in-new: View in Swagger UI](../services/api/svc-transport-logistics.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-transport-logistics--post-routes.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-transport-logistics--post-routes.svg" type="image/svg+xml" style="max-width: 100%;">POST /routes sequence diagram</object></div>

---

### GET `/routes/{route_id}/schedule` -- Get schedule for a transport route { .endpoint-get }

> Returns the daily schedule of departures for a given route, optionally filtered by date range.

[:material-open-in-new: View in Swagger UI](../services/api/svc-transport-logistics.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-transport-logistics--get-routes-route_id-schedule.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-transport-logistics--get-routes-route_id-schedule.svg" type="image/svg+xml" style="max-width: 100%;">GET /routes/{route_id}/schedule sequence diagram</object></div>

---

### POST `/transport-requests` -- Request transport for a reservation { .endpoint-post }

> Creates a transport request linked to an existing reservation

[:material-open-in-new: View in Swagger UI](../services/api/svc-transport-logistics.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-transport-logistics--post-transport-requests.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-transport-logistics--post-transport-requests.svg" type="image/svg+xml" style="max-width: 100%;">POST /transport-requests sequence diagram</object></div>

---

### GET `/transport-requests/{request_id}` -- Get transport request details { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-transport-logistics.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-transport-logistics--get-transport-requests-request_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-transport-logistics--get-transport-requests-request_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /transport-requests/{request_id} sequence diagram</object></div>

---

### GET `/vehicles` -- List fleet vehicles { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-transport-logistics.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-transport-logistics--get-vehicles.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-transport-logistics--get-vehicles.svg" type="image/svg+xml" style="max-width: 100%;">GET /vehicles sequence diagram</object></div>

---

### PATCH `/vehicles/{vehicle_id}` -- Update vehicle information { .endpoint-patch }

[:material-open-in-new: View in Swagger UI](../services/api/svc-transport-logistics.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-transport-logistics--patch-vehicles-vehicle_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-transport-logistics--patch-vehicles-vehicle_id.svg" type="image/svg+xml" style="max-width: 100%;">PATCH /vehicles/{vehicle_id} sequence diagram</object></div>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Operations Dashboard](../../applications/web-ops-dashboard/) | Transport Dispatch |
