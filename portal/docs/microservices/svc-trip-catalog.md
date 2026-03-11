---
tags:
  - microservice
  - svc-trip-catalog
  - product-catalog
---

# svc-trip-catalog

**NovaTrek Adventures - Trip Catalog Service** &nbsp;|&nbsp; <span style="background: #d9770615; color: #d97706; border: 1px solid #d9770640; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">Product Catalog</span> &nbsp;|&nbsp; `v2.4.0` &nbsp;|&nbsp; *NovaTrek Platform Engineering*

> Manages adventure trip definitions, scheduling, pricing, and availability

[:material-api: Swagger UI](../services/api/svc-trip-catalog.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-trip-catalog.yaml){ .md-button }
[:material-rocket-launch: Live Service (Dev)](https://ca-svc-trip-catalog.blackwater-fd4bc06d.eastus2.azurecontainerapps.io/actuator/health){ .md-button }
[:material-microsoft-azure: Azure Portal](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-trip-catalog){ .md-button }
[:material-pipe: CI/CD Pipeline](https://github.com/christopherblaisdell/continuous-architecture-platform-poc-2/actions/workflows/service-svc-trip-catalog.yml){ .md-button }
[:material-source-branch: Source Code](https://github.com/christopherblaisdell/continuous-architecture-platform-poc-2/tree/main/services/svc-trip-catalog){ .md-button }
[:material-language-java: Technology Stack](../technologies.md){ .md-button }

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

- [:material-microsoft-azure: Container App](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-trip-catalog)
- [:material-database: PostgreSQL Server](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.DBforPostgreSQL/flexibleServers/psql-novatrek-dev)
- [:material-text-search: Log Analytics](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.OperationalInsights/workspaces/log-novatrek-dev/logs)

---

## :material-map: Integration Context

<div class="diagram-wrap"><a href="../svg/svc-trip-catalog--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trip-catalog--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-trip-catalog C4 context diagram</object></div>


## :material-database: Data Store { #data-store }

### Entity Relationship Diagram

<div class="diagram-wrap"><a href="../svg/svc-trip-catalog--erd.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trip-catalog--erd.svg" type="image/svg+xml" style="max-width: 100%;">svc-trip-catalog entity relationship diagram</object></div>

### Overview

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `catalog` |
| **Tables** | `trips`, `trip_schedules`, `pricing_tiers`, `requirements`, `regions`, `activity_types` |
| **Estimated Volume** | ~50 catalog updates/day, ~10K availability reads/day |
| **Connection Pool** | min 5 / max 25 / idle timeout 10min |
| **Backup Strategy** | Daily pg_dump, 14-day retention |

### Key Features

- Full-text search index on trip name and description
- Materialized view for availability calendar
- JSONB columns for flexible requirement definitions

### Table Reference

#### `trips`

*Master adventure trip catalog entries*

| Column | Type | Constraints |
|--------|------|-------------|
| `trip_id` | `UUID` | PK |
| `name` | `VARCHAR(200)` | NOT NULL |
| `description` | `TEXT` | NOT NULL |
| `adventure_category` | `VARCHAR(50)` | NOT NULL |
| `region_id` | `UUID` | NOT NULL, FK -> regions |
| `difficulty_level` | `SMALLINT` | NOT NULL, CHECK (1-5) |
| `duration_hours` | `DECIMAL(4,1)` | NOT NULL |
| `min_participants` | `INTEGER` | NOT NULL, DEFAULT 1 |
| `max_participants` | `INTEGER` | NOT NULL |
| `base_price` | `DECIMAL(10,2)` | NOT NULL |
| `currency` | `CHAR(3)` | DEFAULT 'USD' |
| `active` | `BOOLEAN` | NOT NULL, DEFAULT TRUE |
| `created_at` | `TIMESTAMPTZ` | NOT NULL |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_trip_category` on `adventure_category`
- `idx_trip_region` on `region_id`
- `idx_trip_search` on `name, description` (GIN (tsvector))

#### `trip_schedules`

*Available dates and time slots for each trip*

| Column | Type | Constraints |
|--------|------|-------------|
| `schedule_id` | `UUID` | PK |
| `trip_id` | `UUID` | NOT NULL, FK -> trips |
| `trip_date` | `DATE` | NOT NULL |
| `start_time` | `TIME` | NOT NULL |
| `available_spots` | `INTEGER` | NOT NULL |
| `booked_spots` | `INTEGER` | NOT NULL, DEFAULT 0 |

**Indexes:**

- `idx_sched_trip_date` on `trip_id, trip_date`
- `idx_sched_avail` on `trip_date, available_spots`

#### `pricing_tiers`

*Dynamic pricing tiers based on season, demand, and group size*

| Column | Type | Constraints |
|--------|------|-------------|
| `tier_id` | `UUID` | PK |
| `trip_id` | `UUID` | NOT NULL, FK -> trips |
| `tier_name` | `VARCHAR(50)` | NOT NULL |
| `multiplier` | `DECIMAL(3,2)` | NOT NULL |
| `effective_from` | `DATE` | NOT NULL |
| `effective_to` | `DATE` | NULL |

**Indexes:**

- `idx_pricing_trip` on `trip_id, effective_from`


---

## :material-lightbulb: Solutions Affecting This Service

| Ticket | Solution | Capabilities | Date |
|--------|----------|-------------|------|
| NTK-10008 | [Guest Reviews and Ratings Platform](../solutions/_NTK-10008-guest-reviews-and-ratings.md) | `CAP-1.7`, `CAP-1.2` | 2026-03-06 |

---

## :material-api: Endpoints (11 total)

---

### GET `/trips` -- Search trips with filters { .endpoint-get }

> Returns a paginated list of trips matching the specified filter criteria.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trip-catalog.html#/Trips/searchTrips){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-trip-catalog--get-trips.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trip-catalog--get-trips.svg" type="image/svg+xml" style="max-width: 100%;">GET /trips sequence diagram</object></div>

---

### POST `/trips` -- Create a new trip definition { .endpoint-post }

> Creates a new trip in DRAFT status. The trip must be explicitly

[:material-open-in-new: View in Swagger UI](../services/api/svc-trip-catalog.html#/Trips/createTrip){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-trip-catalog--post-trips.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trip-catalog--post-trips.svg" type="image/svg+xml" style="max-width: 100%;">POST /trips sequence diagram</object></div>

---

### GET `/trips/{trip_id}` -- Get trip details { .endpoint-get }

> Returns the full trip definition including all metadata.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trip-catalog.html#/Trips/getTripById){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-trip-catalog--get-trips-trip_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trip-catalog--get-trips-trip_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /trips/{trip_id} sequence diagram</object></div>

---

### PATCH `/trips/{trip_id}` -- Update trip details { .endpoint-patch }

> Partially updates a trip definition. Only provided fields are modified.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trip-catalog.html#/Trips/updateTrip){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-trip-catalog--patch-trips-trip_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trip-catalog--patch-trips-trip_id.svg" type="image/svg+xml" style="max-width: 100%;">PATCH /trips/{trip_id} sequence diagram</object></div>

---

### GET `/trips/{trip_id}/schedule` -- Get scheduled departures { .endpoint-get }

> Returns all scheduled departures for a trip, optionally filtered

[:material-open-in-new: View in Swagger UI](../services/api/svc-trip-catalog.html#/Schedule/getTripSchedule){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-trip-catalog--get-trips-trip_id-schedule.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trip-catalog--get-trips-trip_id-schedule.svg" type="image/svg+xml" style="max-width: 100%;">GET /trips/{trip_id}/schedule sequence diagram</object></div>

---

### POST `/trips/{trip_id}/schedule` -- Add a scheduled departure { .endpoint-post }

> Adds a new departure date and time for this trip. The trip must be

[:material-open-in-new: View in Swagger UI](../services/api/svc-trip-catalog.html#/Schedule/addScheduledDeparture){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-trip-catalog--post-trips-trip_id-schedule.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trip-catalog--post-trips-trip_id-schedule.svg" type="image/svg+xml" style="max-width: 100%;">POST /trips/{trip_id}/schedule sequence diagram</object></div>

---

### GET `/trips/{trip_id}/pricing` -- Get pricing tiers { .endpoint-get }

> Returns all pricing tiers configured for the specified trip.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trip-catalog.html#/Pricing/getTripPricing){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-trip-catalog--get-trips-trip_id-pricing.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trip-catalog--get-trips-trip_id-pricing.svg" type="image/svg+xml" style="max-width: 100%;">GET /trips/{trip_id}/pricing sequence diagram</object></div>

---

### PUT `/trips/{trip_id}/pricing` -- Replace pricing tiers { .endpoint-put }

> Replaces all pricing tiers for the trip. At minimum, a STANDARD tier

[:material-open-in-new: View in Swagger UI](../services/api/svc-trip-catalog.html#/Pricing/updateTripPricing){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-trip-catalog--put-trips-trip_id-pricing.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trip-catalog--put-trips-trip_id-pricing.svg" type="image/svg+xml" style="max-width: 100%;">PUT /trips/{trip_id}/pricing sequence diagram</object></div>

---

### GET `/trips/{trip_id}/requirements` -- Get trip requirements { .endpoint-get }

> Returns gear, certification, and fitness requirements for the trip.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trip-catalog.html#/Requirements/getTripRequirements){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-trip-catalog--get-trips-trip_id-requirements.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trip-catalog--get-trips-trip_id-requirements.svg" type="image/svg+xml" style="max-width: 100%;">GET /trips/{trip_id}/requirements sequence diagram</object></div>

---

### GET `/regions` -- List operating regions { .endpoint-get }

> Returns all regions where NovaTrek operates adventure trips.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trip-catalog.html#/Reference%20Data/listRegions){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-trip-catalog--get-regions.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trip-catalog--get-regions.svg" type="image/svg+xml" style="max-width: 100%;">GET /regions sequence diagram</object></div>

---

### GET `/activity-types` -- List available activity types { .endpoint-get }

> Returns the enumerated list of supported activity types with

[:material-open-in-new: View in Swagger UI](../services/api/svc-trip-catalog.html#/Reference%20Data/listActivityTypes){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-trip-catalog--get-activity-types.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-trip-catalog--get-activity-types.svg" type="image/svg+xml" style="max-width: 100%;">GET /activity-types sequence diagram</object></div>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Guest Portal](../../applications/web-guest-portal/) | Trip Browser, Booking Flow |
| [Adventure App](../../applications/app-guest-mobile/) | My Reservations |
