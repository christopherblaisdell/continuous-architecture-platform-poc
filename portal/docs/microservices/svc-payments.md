---
tags:
  - microservice
  - svc-payments
  - support
---

# svc-payments

**NovaTrek Payments Service** &nbsp;|&nbsp; <span style="background: #64748b15; color: #64748b; border: 1px solid #64748b40; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">Support</span> &nbsp;|&nbsp; `v1.1.0` &nbsp;|&nbsp; *NovaTrek Platform Team*

> Manages payments, refunds, and billing for adventure bookings at NovaTrek Adventures.

[:material-api: Swagger UI](../services/api/svc-payments.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-payments.yaml){ .md-button }
[:material-rocket-launch: Live Service (Dev)](https://ca-svc-payments.blackwater-fd4bc06d.eastus2.azurecontainerapps.io/actuator/health){ .md-button }
[:material-microsoft-azure: Azure Portal](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-payments){ .md-button }
[:material-pipe: CI/CD Pipeline](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/service-ci.yml){ .md-button }
[:material-source-branch: Source Code](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/services/svc-payments){ .md-button }
[:material-language-java: Technology Stack](../technologies.md){ .md-button }

## :material-truck-delivery: Delivery Status

**Delivery Wave:** 2 -- Booking and Payments

| Stage | Status |
|-------|--------|
| Infrastructure (Bicep) | :white_check_mark: complete |
| Database Schema (Flyway) | :white_check_mark: complete |
| Deployed to Dev | :white_check_mark: complete |
| Smoke Tested | :white_check_mark: complete |
| Deployed to Prod | :material-circle-outline: not-started |


| Pipeline | Status |
|----------|--------|
| CI Pipeline | :white_check_mark: complete |
| CD Pipeline | :white_check_mark: complete |

**Azure Resources (Dev):**

- [:material-microsoft-azure: Container App](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-payments)
- [:material-database: PostgreSQL Server](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.DBforPostgreSQL/flexibleServers/pg-novatrek-dev-smwd6ded4e3so)
- [:material-text-search: Log Analytics](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.OperationalInsights/workspaces/log-novatrek-dev/logs)

---

## :material-map: Integration Context

<div class="diagram-wrap"><a href="../svg/svc-payments--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-payments--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-payments C4 context diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-payments.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-payments.yaml` + `cross-service-calls.yaml`</a>


## :material-database: Data Store { #data-store }

### Entity Relationship Diagram

<div class="diagram-wrap"><a href="../svg/svc-payments--erd.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-payments--erd.svg" type="image/svg+xml" style="max-width: 100%;">svc-payments entity relationship diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/data-stores.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/metadata/data-stores.yaml`</a>

### Overview

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `payments` |
| **Tables** | `payments`, `refunds`, `payment_methods`, `daily_summaries`, `disputes`, `refund_policy_evaluations` |
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

## :material-lightbulb: Solutions Affecting This Service

| Ticket | Solution | Capabilities | Date |
|--------|----------|-------------|------|
| NTK-10009 | [Refund and Dispute Management Workflows](../solutions/_NTK-10009-refund-dispute-management.md) | `CAP-5.5`, `CAP-5.4` | 2026-03-06 |

---

## :material-api: Endpoints (12 total)

---

### POST `/payments` -- Process a payment { .endpoint-post }

> Initiates payment processing for a reservation. The payment is authorized and captured based on the selected method.

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Payments/processPayment){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-payments--post-payments.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-payments--post-payments.svg" type="image/svg+xml" style="max-width: 100%;">POST /payments sequence diagram</object></div>
<span class="diagram-source diagram-source--override"><span class="diagram-source-icon">&#x270E;</span> Architect-authored — overrides auto-generated baseline</span>
<span class="diagram-source-subtitle">Source: <a href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/diagrams/endpoints/svc-payments--post-payments.puml"><code>architecture/diagrams/endpoints/svc-payments--post-payments.puml</code></a></span>

---

### GET `/payments/{payment_id}` -- Retrieve payment details { .endpoint-get }

> Returns full details of a specific payment including processor reference and status history.

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Payments/getPayment){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-payments--get-payments-payment_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-payments--get-payments-payment_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /payments/{payment_id} sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-payments.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-payments.yaml`</a>
<span class="diagram-source-subtitle">Auto-generated baseline — shows standard request flow. For detailed behavioral sequences, see the relevant <a href="../solutions/">solution design</a>.</span>

---

### POST `/payments/{payment_id}/refund` -- Initiate a refund { .endpoint-post }

> Creates a refund for the specified payment. Supports full or partial refunds.

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Refunds/refundPayment){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-payments--post-payments-payment_id-refund.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-payments--post-payments-payment_id-refund.svg" type="image/svg+xml" style="max-width: 100%;">POST /payments/{payment_id}/refund sequence diagram</object></div>
<span class="diagram-source diagram-source--override"><span class="diagram-source-icon">&#x270E;</span> Architect-authored — overrides auto-generated baseline</span>
<span class="diagram-source-subtitle">Source: <a href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/diagrams/endpoints/svc-payments--post-payments-payment_id-refund.puml"><code>architecture/diagrams/endpoints/svc-payments--post-payments-payment_id-refund.puml</code></a></span>

---

### GET `/guests/{guest_id}/payment-history` -- Retrieve payment history for a guest { .endpoint-get }

> Returns paginated payment history for a specific guest, ordered by most recent first.

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Payments/getGuestPaymentHistory){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-payments--get-guests-guest_id-payment-history.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-payments--get-guests-guest_id-payment-history.svg" type="image/svg+xml" style="max-width: 100%;">GET /guests/{guest_id}/payment-history sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-payments.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-payments.yaml`</a>
<span class="diagram-source-subtitle">Auto-generated baseline — shows standard request flow. For detailed behavioral sequences, see the relevant <a href="../solutions/">solution design</a>.</span>

---

### GET `/disputes` -- List disputes with optional filters { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Disputes/listDisputes){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-payments--get-disputes.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-payments--get-disputes.svg" type="image/svg+xml" style="max-width: 100%;">GET /disputes sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-payments.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-payments.yaml`</a>
<span class="diagram-source-subtitle">Auto-generated baseline — shows standard request flow. For detailed behavioral sequences, see the relevant <a href="../solutions/">solution design</a>.</span>

---

### POST `/disputes` -- Create a refund dispute { .endpoint-post }

> Opens a dispute for a payment. The system evaluates the refund request against

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Disputes/createDispute){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-payments--post-disputes.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-payments--post-disputes.svg" type="image/svg+xml" style="max-width: 100%;">POST /disputes sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-payments.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-payments.yaml`</a>
<span class="diagram-source-subtitle">Auto-generated baseline — shows standard request flow. For detailed behavioral sequences, see the relevant <a href="../solutions/">solution design</a>.</span>

---

### GET `/disputes/{dispute_id}` -- Retrieve dispute details { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Disputes/getDispute){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-payments--get-disputes-dispute_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-payments--get-disputes-dispute_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /disputes/{dispute_id} sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-payments.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-payments.yaml`</a>
<span class="diagram-source-subtitle">Auto-generated baseline — shows standard request flow. For detailed behavioral sequences, see the relevant <a href="../solutions/">solution design</a>.</span>

---

### PATCH `/disputes/{dispute_id}` -- Update a dispute (assign, add notes, escalate) { .endpoint-patch }

> Supports field-level updates. Requires role matching the dispute tier.

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Disputes/updateDispute){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-payments--patch-disputes-dispute_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-payments--patch-disputes-dispute_id.svg" type="image/svg+xml" style="max-width: 100%;">PATCH /disputes/{dispute_id} sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-payments.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-payments.yaml`</a>
<span class="diagram-source-subtitle">Auto-generated baseline — shows standard request flow. For detailed behavioral sequences, see the relevant <a href="../solutions/">solution design</a>.</span>

---

### POST `/disputes/{dispute_id}/resolve` -- Resolve a dispute with refund decision { .endpoint-post }

> Resolves the dispute with a decision (FULL_REFUND, PARTIAL_REFUND, DENIED).

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Disputes/resolveDispute){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-payments--post-disputes-dispute_id-resolve.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-payments--post-disputes-dispute_id-resolve.svg" type="image/svg+xml" style="max-width: 100%;">POST /disputes/{dispute_id}/resolve sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-payments.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-payments.yaml`</a>
<span class="diagram-source-subtitle">Auto-generated baseline — shows standard request flow. For detailed behavioral sequences, see the relevant <a href="../solutions/">solution design</a>.</span>

---

### POST `/chargebacks` -- Ingest a chargeback notification from payment processor { .endpoint-post }

> Creates a dispute record from an external chargeback notification.

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Disputes/ingestChargeback){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-payments--post-chargebacks.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-payments--post-chargebacks.svg" type="image/svg+xml" style="max-width: 100%;">POST /chargebacks sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-payments.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-payments.yaml`</a>
<span class="diagram-source-subtitle">Auto-generated baseline — shows standard request flow. For detailed behavioral sequences, see the relevant <a href="../solutions/">solution design</a>.</span>

---

### POST `/refund-policy/evaluate` -- Evaluate refund eligibility against policy (dry-run) { .endpoint-post }

> Returns the policy evaluation result without creating a dispute.

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Disputes/evaluateRefundPolicy){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-payments--post-refund-policy-evaluate.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-payments--post-refund-policy-evaluate.svg" type="image/svg+xml" style="max-width: 100%;">POST /refund-policy/evaluate sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-payments.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-payments.yaml`</a>
<span class="diagram-source-subtitle">Auto-generated baseline — shows standard request flow. For detailed behavioral sequences, see the relevant <a href="../solutions/">solution design</a>.</span>

---

### GET `/payments/daily-summary` -- Get daily payment summary { .endpoint-get }

> Returns an aggregated summary of payments processed on a given date, broken down by method and status.

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Reporting/getDailySummary){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-payments--get-payments-daily-summary.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-payments--get-payments-daily-summary.svg" type="image/svg+xml" style="max-width: 100%;">GET /payments/daily-summary sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-payments.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-payments.yaml`</a>
<span class="diagram-source-subtitle">Auto-generated baseline — shows standard request flow. For detailed behavioral sequences, see the relevant <a href="../solutions/">solution design</a>.</span>

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
