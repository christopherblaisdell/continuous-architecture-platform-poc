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

---

## :material-map: Integration Context

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-trip-catalog--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-trip-catalog C4 context diagram</object></div>

<p style="text-align: right; margin-top: -0.5em;"><a href="../svg/svc-trip-catalog--c4-context.svg" target="_blank" title="Open diagram in full screen">:material-fullscreen: View full screen</a></p>

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `catalog` |
| **Primary Tables** | `trips`, `trip_schedules`, `pricing_tiers`, `requirements`, `regions`, `activity_types` |
| **Key Features** | Full-text search index on trip name and description | Materialized view for availability calendar | JSONB columns for flexible requirement definitions |
| **Estimated Volume** | ~50 catalog updates/day, ~10K availability reads/day |

---

## :material-api: Endpoints (11 total)

---

### GET `/trips` -- Search trips with filters { .endpoint-get }

> Returns a paginated list of trips matching the specified filter criteria.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trip-catalog.html#/Trips/searchTrips){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-trip-catalog--get-trips.svg" type="image/svg+xml" style="max-width: 100%;">GET /trips sequence diagram</object></div>

<p style="text-align: right; margin-top: -0.5em;"><a href="../svg/svc-trip-catalog--get-trips.svg" target="_blank" title="Open diagram in full screen">:material-fullscreen: View full screen</a></p>

---

### POST `/trips` -- Create a new trip definition { .endpoint-post }

> Creates a new trip in DRAFT status. The trip must be explicitly

[:material-open-in-new: View in Swagger UI](../services/api/svc-trip-catalog.html#/Trips/createTrip){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-trip-catalog--post-trips.svg" type="image/svg+xml" style="max-width: 100%;">POST /trips sequence diagram</object></div>

<p style="text-align: right; margin-top: -0.5em;"><a href="../svg/svc-trip-catalog--post-trips.svg" target="_blank" title="Open diagram in full screen">:material-fullscreen: View full screen</a></p>

---

### GET `/trips/{trip_id}` -- Get trip details { .endpoint-get }

> Returns the full trip definition including all metadata.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trip-catalog.html#/Trips/getTripById){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-trip-catalog--get-trips-trip_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /trips/{trip_id} sequence diagram</object></div>

<p style="text-align: right; margin-top: -0.5em;"><a href="../svg/svc-trip-catalog--get-trips-trip_id.svg" target="_blank" title="Open diagram in full screen">:material-fullscreen: View full screen</a></p>

---

### PATCH `/trips/{trip_id}` -- Update trip details { .endpoint-patch }

> Partially updates a trip definition. Only provided fields are modified.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trip-catalog.html#/Trips/updateTrip){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-trip-catalog--patch-trips-trip_id.svg" type="image/svg+xml" style="max-width: 100%;">PATCH /trips/{trip_id} sequence diagram</object></div>

<p style="text-align: right; margin-top: -0.5em;"><a href="../svg/svc-trip-catalog--patch-trips-trip_id.svg" target="_blank" title="Open diagram in full screen">:material-fullscreen: View full screen</a></p>

---

### GET `/trips/{trip_id}/schedule` -- Get scheduled departures { .endpoint-get }

> Returns all scheduled departures for a trip, optionally filtered

[:material-open-in-new: View in Swagger UI](../services/api/svc-trip-catalog.html#/Schedule/getTripSchedule){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-trip-catalog--get-trips-trip_id-schedule.svg" type="image/svg+xml" style="max-width: 100%;">GET /trips/{trip_id}/schedule sequence diagram</object></div>

<p style="text-align: right; margin-top: -0.5em;"><a href="../svg/svc-trip-catalog--get-trips-trip_id-schedule.svg" target="_blank" title="Open diagram in full screen">:material-fullscreen: View full screen</a></p>

---

### POST `/trips/{trip_id}/schedule` -- Add a scheduled departure { .endpoint-post }

> Adds a new departure date and time for this trip. The trip must be

[:material-open-in-new: View in Swagger UI](../services/api/svc-trip-catalog.html#/Schedule/addScheduledDeparture){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-trip-catalog--post-trips-trip_id-schedule.svg" type="image/svg+xml" style="max-width: 100%;">POST /trips/{trip_id}/schedule sequence diagram</object></div>

<p style="text-align: right; margin-top: -0.5em;"><a href="../svg/svc-trip-catalog--post-trips-trip_id-schedule.svg" target="_blank" title="Open diagram in full screen">:material-fullscreen: View full screen</a></p>

---

### GET `/trips/{trip_id}/pricing` -- Get pricing tiers { .endpoint-get }

> Returns all pricing tiers configured for the specified trip.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trip-catalog.html#/Pricing/getTripPricing){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-trip-catalog--get-trips-trip_id-pricing.svg" type="image/svg+xml" style="max-width: 100%;">GET /trips/{trip_id}/pricing sequence diagram</object></div>

<p style="text-align: right; margin-top: -0.5em;"><a href="../svg/svc-trip-catalog--get-trips-trip_id-pricing.svg" target="_blank" title="Open diagram in full screen">:material-fullscreen: View full screen</a></p>

---

### PUT `/trips/{trip_id}/pricing` -- Replace pricing tiers { .endpoint-put }

> Replaces all pricing tiers for the trip. At minimum, a STANDARD tier

[:material-open-in-new: View in Swagger UI](../services/api/svc-trip-catalog.html#/Pricing/updateTripPricing){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-trip-catalog--put-trips-trip_id-pricing.svg" type="image/svg+xml" style="max-width: 100%;">PUT /trips/{trip_id}/pricing sequence diagram</object></div>

<p style="text-align: right; margin-top: -0.5em;"><a href="../svg/svc-trip-catalog--put-trips-trip_id-pricing.svg" target="_blank" title="Open diagram in full screen">:material-fullscreen: View full screen</a></p>

---

### GET `/trips/{trip_id}/requirements` -- Get trip requirements { .endpoint-get }

> Returns gear, certification, and fitness requirements for the trip.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trip-catalog.html#/Requirements/getTripRequirements){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-trip-catalog--get-trips-trip_id-requirements.svg" type="image/svg+xml" style="max-width: 100%;">GET /trips/{trip_id}/requirements sequence diagram</object></div>

<p style="text-align: right; margin-top: -0.5em;"><a href="../svg/svc-trip-catalog--get-trips-trip_id-requirements.svg" target="_blank" title="Open diagram in full screen">:material-fullscreen: View full screen</a></p>

---

### GET `/regions` -- List operating regions { .endpoint-get }

> Returns all regions where NovaTrek operates adventure trips.

[:material-open-in-new: View in Swagger UI](../services/api/svc-trip-catalog.html#/Reference%20Data/listRegions){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-trip-catalog--get-regions.svg" type="image/svg+xml" style="max-width: 100%;">GET /regions sequence diagram</object></div>

<p style="text-align: right; margin-top: -0.5em;"><a href="../svg/svc-trip-catalog--get-regions.svg" target="_blank" title="Open diagram in full screen">:material-fullscreen: View full screen</a></p>

---

### GET `/activity-types` -- List available activity types { .endpoint-get }

> Returns the enumerated list of supported activity types with

[:material-open-in-new: View in Swagger UI](../services/api/svc-trip-catalog.html#/Reference%20Data/listActivityTypes){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-trip-catalog--get-activity-types.svg" type="image/svg+xml" style="max-width: 100%;">GET /activity-types sequence diagram</object></div>

<p style="text-align: right; margin-top: -0.5em;"><a href="../svg/svc-trip-catalog--get-activity-types.svg" target="_blank" title="Open diagram in full screen">:material-fullscreen: View full screen</a></p>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Guest Portal](../../applications/web-guest-portal/) | Trip Browser, Booking Flow |
| [Adventure App](../../applications/app-guest-mobile/) | My Reservations |
