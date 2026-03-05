---
tags:
  - microservice
  - svc-partner-integrations
  - external
---

# svc-partner-integrations

**NovaTrek Partner Integrations Service** &nbsp;|&nbsp; <span style="background: #9333ea15; color: #9333ea; border: 1px solid #9333ea40; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">External</span> &nbsp;|&nbsp; `v1.0.0` &nbsp;|&nbsp; *NovaTrek Partnerships Team*

> Manages third-party partner relationships and bookings from travel agents,

[:material-api: Swagger UI](../services/api/svc-partner-integrations.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-partner-integrations.yaml){ .md-button }

---

## :material-database: Data Store

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `partners` |
| **Primary Tables** | `partners`, `partner_bookings`, `commission_records`, `reconciliation_log` |
| **Key Features** | Partner API key management with rotation policy | Commission calculation engine with tiered rates | Idempotency keys for booking creation |
| **Estimated Volume** | ~400 partner bookings/day |

---

## :material-api: Endpoints (7 total)

---

### POST `/partner-bookings` -- External partner creates a booking { .endpoint-post }

> Allows an authenticated partner to submit a booking request. Creates

[:material-open-in-new: View in Swagger UI](../services/api/svc-partner-integrations.html#/Partner%20Bookings/createPartnerBooking){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-partner-integrations--post-partner-bookings.svg" type="image/svg+xml" style="max-width: 100%;">POST /partner-bookings sequence diagram</object></div>

---

### GET `/partner-bookings/{booking_id}` -- Get partner booking details { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-partner-integrations.html#/Partner%20Bookings/getPartnerBooking){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-partner-integrations--get-partner-bookings-booking_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /partner-bookings/{booking_id} sequence diagram</object></div>

---

### PATCH `/partner-bookings/{booking_id}` -- Update a partner booking { .endpoint-patch }

[:material-open-in-new: View in Swagger UI](../services/api/svc-partner-integrations.html#/Partner%20Bookings/updatePartnerBooking){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-partner-integrations--patch-partner-bookings-booking_id.svg" type="image/svg+xml" style="max-width: 100%;">PATCH /partner-bookings/{booking_id} sequence diagram</object></div>

---

### POST `/partner-bookings/{booking_id}/confirm` -- Confirm a pending partner booking { .endpoint-post }

> Confirms availability and finalizes the partner booking. Triggers

[:material-open-in-new: View in Swagger UI](../services/api/svc-partner-integrations.html#/Partner%20Bookings/confirmPartnerBooking){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-partner-integrations--post-partner-bookings-booking_id-confirm.svg" type="image/svg+xml" style="max-width: 100%;">POST /partner-bookings/{booking_id}/confirm sequence diagram</object></div>

---

### GET `/partners` -- List registered partners { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-partner-integrations.html#/Partners/listPartners){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-partner-integrations--get-partners.svg" type="image/svg+xml" style="max-width: 100%;">GET /partners sequence diagram</object></div>

---

### POST `/partners` -- Register a new partner { .endpoint-post }

[:material-open-in-new: View in Swagger UI](../services/api/svc-partner-integrations.html#/Partners/registerPartner){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-partner-integrations--post-partners.svg" type="image/svg+xml" style="max-width: 100%;">POST /partners sequence diagram</object></div>

---

### GET `/partners/{partner_id}/commission-report` -- Get commission report for a partner { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-partner-integrations.html#/Partners/getCommissionReport){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-partner-integrations--get-partners-partner_id-commission-report.svg" type="image/svg+xml" style="max-width: 100%;">GET /partners/{partner_id}/commission-report sequence diagram</object></div>
