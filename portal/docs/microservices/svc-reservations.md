---
tags:
  - microservice
  - svc-reservations
  - booking
---

# svc-reservations

**Reservations Service** &nbsp;|&nbsp; <span style="background: #05966915; color: #059669; border: 1px solid #05966940; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">Booking</span> &nbsp;|&nbsp; `v2.4.1` &nbsp;|&nbsp; *NovaTrek Platform Team*

> Manages adventure trip reservations for NovaTrek Adventures.

[:material-api: Swagger UI](../services/api/svc-reservations.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-reservations.yaml){ .md-button }
[:material-pipe: CI/CD Pipeline](https://github.com/christopherblaisdell/continuous-architecture-platform-poc-2/actions/workflows/service-svc-reservations.yml){ .md-button }
[:material-source-branch: Source Code](https://github.com/christopherblaisdell/continuous-architecture-platform-poc-2/tree/main/services/svc-reservations){ .md-button }
[:material-language-java: Technology Stack](../technologies.md){ .md-button }

## :material-truck-delivery: Delivery Status

**Delivery Wave:** 2 -- Booking and Payments

| Stage | Status |
|-------|--------|
| Infrastructure (Bicep) | :material-circle-outline: not-started |
| Database Schema (Flyway) | :material-circle-outline: not-started |
| CI Pipeline | :material-circle-outline: not-started |
| CD Pipeline | :material-circle-outline: not-started |
| Deployed to Dev | :material-circle-outline: not-started |
| Smoke Tested | :material-circle-outline: not-started |
| Deployed to Prod | :material-circle-outline: not-started |

**Azure Resources (Dev):**

- [:material-database: PostgreSQL Server](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.DBforPostgreSQL/flexibleServers/psql-novatrek-dev)
- [:material-text-search: Log Analytics](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.OperationalInsights/workspaces/log-novatrek-dev/logs)

---

## :material-map: Integration Context

<div class="diagram-wrap"><a href="../svg/svc-reservations--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-reservations--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-reservations C4 context diagram</object></div>


## :material-database: Data Store { #data-store }

### Entity Relationship Diagram

<div class="diagram-wrap"><a href="../svg/svc-reservations--erd.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-reservations--erd.svg" type="image/svg+xml" style="max-width: 100%;">svc-reservations entity relationship diagram</object></div>

### Overview

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `reservations` |
| **Tables** | `reservations`, `participants`, `status_history` |
| **Estimated Volume** | ~2,000 new reservations/day |
| **Connection Pool** | min 10 / max 40 / idle timeout 10min |
| **Backup Strategy** | Continuous WAL archiving, daily base backup, 30-day PITR |

### Key Features

- Optimistic locking via _rev field
- Composite index on (guest_id, trip_date)
- Monthly partitioning by reservation_date

### Table Reference

#### `reservations`

*Core reservation records for adventure bookings*

| Column | Type | Constraints |
|--------|------|-------------|
| `reservation_id` | `UUID` | PK |
| `guest_id` | `UUID` | NOT NULL |
| `trip_id` | `UUID` | NOT NULL |
| `confirmation_code` | `VARCHAR(12)` | NOT NULL, UNIQUE |
| `status` | `VARCHAR(20)` | NOT NULL, DEFAULT 'confirmed' |
| `trip_date` | `DATE` | NOT NULL |
| `party_size` | `INTEGER` | NOT NULL, CHECK (> 0) |
| `total_amount` | `DECIMAL(10,2)` | NOT NULL |
| `currency` | `CHAR(3)` | NOT NULL, DEFAULT 'USD' |
| `_rev` | `INTEGER` | NOT NULL, DEFAULT 1 |
| `created_at` | `TIMESTAMPTZ` | NOT NULL |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_res_guest_date` on `guest_id, trip_date`
- `idx_res_trip_date` on `trip_id, trip_date`
- `idx_res_confirmation` on `confirmation_code` (UNIQUE)
- `idx_res_status` on `status`

#### `participants`

*Individual participants linked to a reservation*

| Column | Type | Constraints |
|--------|------|-------------|
| `participant_id` | `UUID` | PK |
| `reservation_id` | `UUID` | NOT NULL, FK -> reservations |
| `guest_id` | `UUID` | NOT NULL |
| `role` | `VARCHAR(20)` | NOT NULL, DEFAULT 'guest' |
| `waiver_signed` | `BOOLEAN` | NOT NULL, DEFAULT FALSE |
| `created_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_part_reservation` on `reservation_id`
- `idx_part_guest` on `guest_id`

#### `status_history`

*Audit trail of reservation status transitions*

| Column | Type | Constraints |
|--------|------|-------------|
| `history_id` | `UUID` | PK |
| `reservation_id` | `UUID` | NOT NULL, FK -> reservations |
| `old_status` | `VARCHAR(20)` | NULL |
| `new_status` | `VARCHAR(20)` | NOT NULL |
| `changed_by` | `VARCHAR(100)` | NOT NULL |
| `reason` | `TEXT` | NULL |
| `changed_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT NOW() |

**Indexes:**

- `idx_hist_reservation` on `reservation_id, changed_at DESC`


---

## :material-lightbulb: Solutions Affecting This Service

| Ticket | Solution | Capabilities | Date |
|--------|----------|-------------|------|
| NTK-10008 | [Guest Reviews and Ratings Platform](../solutions/_NTK-10008-guest-reviews-and-ratings.md) | `CAP-1.7`, `CAP-1.2` | 2026-03-06 |
| NTK-10009 | [Refund and Dispute Management Workflows](../solutions/_NTK-10009-refund-dispute-management.md) | `CAP-5.5`, `CAP-5.4` | 2026-03-06 |

---

## :material-api: Endpoints (8 total)

---

### GET `/reservations` -- Search reservations { .endpoint-get }

> Returns a paginated list of reservations matching the given criteria.

[:material-open-in-new: View in Swagger UI](../services/api/svc-reservations.html#/Reservation%20Search/searchReservations){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-reservations--get-reservations.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-reservations--get-reservations.svg" type="image/svg+xml" style="max-width: 100%;">GET /reservations sequence diagram</object></div>

---

### POST `/reservations` -- Create a new reservation { .endpoint-post }

> Creates a new adventure reservation. Validates guest eligibility,

[:material-open-in-new: View in Swagger UI](../services/api/svc-reservations.html#/Reservations/createReservation){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-reservations--post-reservations.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-reservations--post-reservations.svg" type="image/svg+xml" style="max-width: 100%;">POST /reservations sequence diagram</object></div>

---

### GET `/reservations/{reservation_id}` -- Get reservation details { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-reservations.html#/Reservations/getReservation){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-reservations--get-reservations-reservation_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-reservations--get-reservations-reservation_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /reservations/{reservation_id} sequence diagram</object></div>

---

### PATCH `/reservations/{reservation_id}` -- Update a reservation { .endpoint-patch }

> Partially updates a reservation. Only modifiable fields can be changed.

[:material-open-in-new: View in Swagger UI](../services/api/svc-reservations.html#/Reservations/updateReservation){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-reservations--patch-reservations-reservation_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-reservations--patch-reservations-reservation_id.svg" type="image/svg+xml" style="max-width: 100%;">PATCH /reservations/{reservation_id} sequence diagram</object></div>

---

### DELETE `/reservations/{reservation_id}` -- Cancel a reservation { .endpoint-delete }

[:material-open-in-new: View in Swagger UI](../services/api/svc-reservations.html#/Reservations/cancelReservation){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-reservations--delete-reservations-reservation_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-reservations--delete-reservations-reservation_id.svg" type="image/svg+xml" style="max-width: 100%;">DELETE /reservations/{reservation_id} sequence diagram</object></div>

---

### GET `/reservations/{reservation_id}/participants` -- Get reservation participants { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-reservations.html#/Reservations/getParticipants){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-reservations--get-reservations-reservation_id-participants.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-reservations--get-reservations-reservation_id-participants.svg" type="image/svg+xml" style="max-width: 100%;">GET /reservations/{reservation_id}/participants sequence diagram</object></div>

---

### POST `/reservations/{reservation_id}/participants` -- Add a participant to a reservation { .endpoint-post }

[:material-open-in-new: View in Swagger UI](../services/api/svc-reservations.html#/Reservations/addParticipant){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-reservations--post-reservations-reservation_id-participants.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-reservations--post-reservations-reservation_id-participants.svg" type="image/svg+xml" style="max-width: 100%;">POST /reservations/{reservation_id}/participants sequence diagram</object></div>

---

### PUT `/reservations/{reservation_id}/status` -- Transition reservation status { .endpoint-put }

> Explicitly transitions a reservation to a new status.

[:material-open-in-new: View in Swagger UI](../services/api/svc-reservations.html#/Reservation%20Status/transitionStatus){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-reservations--put-reservations-reservation_id-status.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-reservations--put-reservations-reservation_id-status.svg" type="image/svg+xml" style="max-width: 100%;">PUT /reservations/{reservation_id}/status sequence diagram</object></div>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Guest Portal](../../applications/web-guest-portal/) | Booking Flow, Guest Profile, Reservation Management, Trip Gallery |
| [Operations Dashboard](../../applications/web-ops-dashboard/) | Check-In Station, Transport Dispatch, Analytics Dashboard, Partner Bookings |
| [Adventure App](../../applications/app-guest-mobile/) | Self Check-In, My Reservations, Earn Loyalty Points |

---

## :material-broadcast: Events Published

| Event | Channel | Trigger | Consumers |
|-------|---------|---------|-----------|
| [`reservation.created`](/events/#reservationcreated) | `novatrek.booking.reservation.created` | [`POST /reservations`](#post-reservations-create-a-new-reservation) | [svc-scheduling-orchestrator](../svc-scheduling-orchestrator/), [svc-analytics](../svc-analytics/) |
| [`reservation.status_changed`](/events/#reservationstatus_changed) | `novatrek.booking.reservation.status-changed` | [`PUT /reservations/{reservation_id}/status`](#put-reservationsreservation_idstatus-transition-reservation-status) | [svc-notifications](../svc-notifications/), [svc-analytics](../svc-analytics/) |

---

## :material-broadcast-off: Events Consumed

| Event | Producer | Channel |
|-------|----------|---------|
| [`payment.processed`](/events/#paymentprocessed) | [svc-payments](../svc-payments/) | `novatrek.support.payment.processed` |
