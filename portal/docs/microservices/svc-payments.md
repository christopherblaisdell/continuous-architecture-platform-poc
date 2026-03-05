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

## :material-database: Data Store

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `payments` |
| **Primary Tables** | `payments`, `refunds`, `payment_methods`, `daily_summaries` |
| **Key Features** | PCI-DSS compliant token storage (no raw card data) | Idempotent payment processing via request keys | Double-entry ledger for financial reconciliation |
| **Estimated Volume** | ~2,500 transactions/day |

---

## :material-api: Endpoints (5 total)

---

### POST `/payments` -- Process a payment { .endpoint-post }

> Initiates payment processing for a reservation. The payment is authorized and captured based on the selected method.

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Payments/processPayment){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-payments--post-payments.svg" type="image/svg+xml" style="max-width: 100%;">POST /payments sequence diagram</object></div>

---

### GET `/payments/{payment_id}` -- Retrieve payment details { .endpoint-get }

> Returns full details of a specific payment including processor reference and status history.

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Payments/getPayment){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-payments--get-payments-payment_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /payments/{payment_id} sequence diagram</object></div>

---

### POST `/payments/{payment_id}/refund` -- Initiate a refund { .endpoint-post }

> Creates a refund for the specified payment. Supports full or partial refunds.

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Refunds/refundPayment){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-payments--post-payments-payment_id-refund.svg" type="image/svg+xml" style="max-width: 100%;">POST /payments/{payment_id}/refund sequence diagram</object></div>

---

### GET `/guests/{guest_id}/payment-history` -- Retrieve payment history for a guest { .endpoint-get }

> Returns paginated payment history for a specific guest, ordered by most recent first.

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Payments/getGuestPaymentHistory){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-payments--get-guests-guest_id-payment-history.svg" type="image/svg+xml" style="max-width: 100%;">GET /guests/{guest_id}/payment-history sequence diagram</object></div>

---

### GET `/payments/daily-summary` -- Get daily payment summary { .endpoint-get }

> Returns an aggregated summary of payments processed on a given date, broken down by method and status.

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Reporting/getDailySummary){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-payments--get-payments-daily-summary.svg" type="image/svg+xml" style="max-width: 100%;">GET /payments/daily-summary sequence diagram</object></div>
