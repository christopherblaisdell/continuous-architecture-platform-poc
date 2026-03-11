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
[:material-pipe: CI/CD Pipeline](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/service-ci.yml){ .md-button }
[:material-source-branch: Source Code](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/services/svc-partner-integrations){ .md-button }
[:material-language-java: Technology Stack](../technologies.md){ .md-button }

## :material-truck-delivery: Delivery Status

**Delivery Wave:** 6 -- External Integrations

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

<div class="diagram-wrap"><a href="../svg/svc-partner-integrations--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-partner-integrations--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-partner-integrations C4 context diagram</object></div>


## :material-database: Data Store { #data-store }

### Entity Relationship Diagram

<div class="diagram-wrap"><a href="../svg/svc-partner-integrations--erd.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-partner-integrations--erd.svg" type="image/svg+xml" style="max-width: 100%;">svc-partner-integrations entity relationship diagram</object></div>

### Overview

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `partners` |
| **Tables** | `partners`, `partner_bookings`, `commission_records`, `reconciliation_log` |
| **Estimated Volume** | ~400 partner bookings/day |
| **Connection Pool** | min 3 / max 10 / idle timeout 10min |
| **Backup Strategy** | Daily pg_dump, 30-day retention |

### Key Features

- Partner API key management with rotation policy
- Commission calculation engine with tiered rates
- Idempotency keys for booking creation

### Table Reference

#### `partners`

*External partner organizations and their API credentials*

| Column | Type | Constraints |
|--------|------|-------------|
| `partner_id` | `UUID` | PK |
| `name` | `VARCHAR(200)` | NOT NULL |
| `api_key_hash` | `VARCHAR(128)` | NOT NULL |
| `commission_rate` | `DECIMAL(4,2)` | NOT NULL |
| `status` | `VARCHAR(20)` | NOT NULL, DEFAULT 'active' |
| `key_rotated_at` | `TIMESTAMPTZ` | NOT NULL |
| `created_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_partner_status` on `status`

#### `partner_bookings`

*Bookings originated from partner channels*

| Column | Type | Constraints |
|--------|------|-------------|
| `booking_id` | `UUID` | PK |
| `partner_id` | `UUID` | NOT NULL, FK -> partners |
| `reservation_id` | `UUID` | NOT NULL |
| `idempotency_key` | `VARCHAR(64)` | NOT NULL, UNIQUE |
| `commission_amount` | `DECIMAL(10,2)` | NOT NULL |
| `created_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_pb_partner` on `partner_id`
- `idx_pb_idempotency` on `idempotency_key` (UNIQUE)
- `idx_pb_reservation` on `reservation_id`


---

## :material-api: Endpoints (7 total)

---

### POST `/partner-bookings` -- External partner creates a booking { .endpoint-post }

> Allows an authenticated partner to submit a booking request. Creates

[:material-open-in-new: View in Swagger UI](../services/api/svc-partner-integrations.html#/Partner%20Bookings/createPartnerBooking){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-partner-integrations--post-partner-bookings.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-partner-integrations--post-partner-bookings.svg" type="image/svg+xml" style="max-width: 100%;">POST /partner-bookings sequence diagram</object></div>

---

### GET `/partner-bookings/{booking_id}` -- Get partner booking details { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-partner-integrations.html#/Partner%20Bookings/getPartnerBooking){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-partner-integrations--get-partner-bookings-booking_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-partner-integrations--get-partner-bookings-booking_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /partner-bookings/{booking_id} sequence diagram</object></div>

---

### PATCH `/partner-bookings/{booking_id}` -- Update a partner booking { .endpoint-patch }

[:material-open-in-new: View in Swagger UI](../services/api/svc-partner-integrations.html#/Partner%20Bookings/updatePartnerBooking){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-partner-integrations--patch-partner-bookings-booking_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-partner-integrations--patch-partner-bookings-booking_id.svg" type="image/svg+xml" style="max-width: 100%;">PATCH /partner-bookings/{booking_id} sequence diagram</object></div>

---

### POST `/partner-bookings/{booking_id}/confirm` -- Confirm a pending partner booking { .endpoint-post }

> Confirms availability and finalizes the partner booking. Triggers

[:material-open-in-new: View in Swagger UI](../services/api/svc-partner-integrations.html#/Partner%20Bookings/confirmPartnerBooking){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-partner-integrations--post-partner-bookings-booking_id-confirm.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-partner-integrations--post-partner-bookings-booking_id-confirm.svg" type="image/svg+xml" style="max-width: 100%;">POST /partner-bookings/{booking_id}/confirm sequence diagram</object></div>

---

### GET `/partners` -- List registered partners { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-partner-integrations.html#/Partners/listPartners){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-partner-integrations--get-partners.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-partner-integrations--get-partners.svg" type="image/svg+xml" style="max-width: 100%;">GET /partners sequence diagram</object></div>

---

### POST `/partners` -- Register a new partner { .endpoint-post }

[:material-open-in-new: View in Swagger UI](../services/api/svc-partner-integrations.html#/Partners/registerPartner){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-partner-integrations--post-partners.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-partner-integrations--post-partners.svg" type="image/svg+xml" style="max-width: 100%;">POST /partners sequence diagram</object></div>

---

### GET `/partners/{partner_id}/commission-report` -- Get commission report for a partner { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-partner-integrations.html#/Partners/getCommissionReport){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-partner-integrations--get-partners-partner_id-commission-report.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-partner-integrations--get-partners-partner_id-commission-report.svg" type="image/svg+xml" style="max-width: 100%;">GET /partners/{partner_id}/commission-report sequence diagram</object></div>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Operations Dashboard](../../applications/web-ops-dashboard/) | Partner Bookings |
