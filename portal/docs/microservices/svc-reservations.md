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

---

## :material-map: Integration Context

<div class="diagram-wrap"><a href="../svg/svc-reservations--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-reservations--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-reservations C4 context diagram</object></div>


| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `reservations` |
| **Primary Tables** | `reservations`, `participants`, `status_history` |
| **Key Features** | Optimistic locking via _rev field | Composite index on (guest_id, trip_date) | Monthly partitioning by reservation_date |
| **Estimated Volume** | ~2,000 new reservations/day |

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
