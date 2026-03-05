---
tags:
  - microservice
  - svc-payments
  - support
---

# svc-payments

**NovaTrek Payments Service** &nbsp;|&nbsp; <span style="background: #64748b15; color: #64748b; border: 1px solid #64748b40; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">Support</span> &nbsp;|&nbsp; `v1.0.0` &nbsp;|&nbsp; *NovaTrek Platform Team*

> Manages payments, refunds, and billing for adventure bookings at NovaTrek Adventures.

[:material-api: Swagger UI](../services/api/svc-payments.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-payments.yaml){ .md-button }

---

## :material-map: Integration Context

<div class="diagram-wrap"><a href="../svg/svc-payments--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-payments--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-payments C4 context diagram</object></div>


## :material-database: Data Store { #data-store }

### Overview

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `payments` |
| **Tables** | `payments`, `refunds`, `payment_methods`, `daily_summaries` |
| **Estimated Volume** | ~2,500 transactions/day |
| **Connection Pool** | min 10 / max 30 / idle timeout 5min |
| **Backup Strategy** | Continuous WAL archiving, daily base backup, 7-year retention (financial) |

### Key Features

- PCI-DSS compliant token storage (no raw card data)
- Idempotent payment processing via request keys
- Double-entry ledger for financial reconciliation

### Table Reference

#### `payments`

*Payment transaction records with tokenized card references*

| Column | Type | Constraints |
|--------|------|-------------|
| `payment_id` | `UUID` | PK |
| `reservation_id` | `UUID` | NOT NULL |
| `guest_id` | `UUID` | NOT NULL |
| `amount` | `DECIMAL(10,2)` | NOT NULL |
| `currency` | `CHAR(3)` | NOT NULL |
| `payment_method_id` | `UUID` | NOT NULL, FK -> payment_methods |
| `gateway_ref` | `VARCHAR(255)` | NOT NULL |
| `status` | `VARCHAR(20)` | NOT NULL |
| `idempotency_key` | `VARCHAR(64)` | NOT NULL, UNIQUE |
| `created_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_pay_reservation` on `reservation_id`
- `idx_pay_guest` on `guest_id`
- `idx_pay_idempotency` on `idempotency_key` (UNIQUE)
- `idx_pay_status` on `status, created_at DESC`

#### `refunds`

*Refund records linked to original payments*

| Column | Type | Constraints |
|--------|------|-------------|
| `refund_id` | `UUID` | PK |
| `payment_id` | `UUID` | NOT NULL, FK -> payments |
| `amount` | `DECIMAL(10,2)` | NOT NULL |
| `reason` | `TEXT` | NOT NULL |
| `gateway_ref` | `VARCHAR(255)` | NOT NULL |
| `status` | `VARCHAR(20)` | NOT NULL |
| `created_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_refund_payment` on `payment_id`

#### `payment_methods`

*Tokenized payment instruments (no raw card data stored)*

| Column | Type | Constraints |
|--------|------|-------------|
| `method_id` | `UUID` | PK |
| `guest_id` | `UUID` | NOT NULL |
| `token` | `VARCHAR(255)` | NOT NULL (gateway token) |
| `card_last_four` | `CHAR(4)` | NOT NULL |
| `card_brand` | `VARCHAR(20)` | NOT NULL |
| `expiry_month` | `SMALLINT` | NOT NULL |
| `expiry_year` | `SMALLINT` | NOT NULL |
| `is_default` | `BOOLEAN` | NOT NULL, DEFAULT FALSE |

**Indexes:**

- `idx_pm_guest` on `guest_id`


---

## :material-api: Endpoints (5 total)

---

### POST `/payments` -- Process a payment { .endpoint-post }

> Initiates payment processing for a reservation. The payment is authorized and captured based on the selected method.

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Payments/processPayment){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-payments--post-payments.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-payments--post-payments.svg" type="image/svg+xml" style="max-width: 100%;">POST /payments sequence diagram</object></div>

---

### GET `/payments/{payment_id}` -- Retrieve payment details { .endpoint-get }

> Returns full details of a specific payment including processor reference and status history.

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Payments/getPayment){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-payments--get-payments-payment_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-payments--get-payments-payment_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /payments/{payment_id} sequence diagram</object></div>

---

### POST `/payments/{payment_id}/refund` -- Initiate a refund { .endpoint-post }

> Creates a refund for the specified payment. Supports full or partial refunds.

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Refunds/refundPayment){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-payments--post-payments-payment_id-refund.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-payments--post-payments-payment_id-refund.svg" type="image/svg+xml" style="max-width: 100%;">POST /payments/{payment_id}/refund sequence diagram</object></div>

---

### GET `/guests/{guest_id}/payment-history` -- Retrieve payment history for a guest { .endpoint-get }

> Returns paginated payment history for a specific guest, ordered by most recent first.

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Payments/getGuestPaymentHistory){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-payments--get-guests-guest_id-payment-history.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-payments--get-guests-guest_id-payment-history.svg" type="image/svg+xml" style="max-width: 100%;">GET /guests/{guest_id}/payment-history sequence diagram</object></div>

---

### GET `/payments/daily-summary` -- Get daily payment summary { .endpoint-get }

> Returns an aggregated summary of payments processed on a given date, broken down by method and status.

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Reporting/getDailySummary){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-payments--get-payments-daily-summary.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-payments--get-payments-daily-summary.svg" type="image/svg+xml" style="max-width: 100%;">GET /payments/daily-summary sequence diagram</object></div>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Guest Portal](../../applications/web-guest-portal/) | Booking Flow, Reservation Management |
| [Operations Dashboard](../../applications/web-ops-dashboard/) | Analytics Dashboard, Partner Bookings |
| [Adventure App](../../applications/app-guest-mobile/) | My Reservations |

---

## :material-broadcast: Events Published

| Event | Channel | Trigger | Consumers |
|-------|---------|---------|-----------|
| [`payment.processed`](/events/#paymentprocessed) | `novatrek.support.payment.processed` | [`POST /payments`](#post-payments-process-a-payment) | [svc-reservations](../svc-reservations/), [svc-notifications](../svc-notifications/) |
