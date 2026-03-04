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
| **Key Features** | PCI-DSS compliant token storage (no raw card data) · Idempotent payment processing via request keys · Double-entry ledger for financial reconciliation |
| **Estimated Volume** | ~2,500 transactions/day |

---

## :material-api: Endpoints (5 total)

---

### POST `/payments` — Process a payment { .endpoint-post }

> Initiates payment processing for a reservation. The payment is authorized and captured based on the selected method.

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Payments/processPayment){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant ExtPay as Payment Gateway
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: POST /payments
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: processPayment()

    rect rgba(199, 123, 48, 0.08)
        Note over Svc,ExtPay: Cross-service integration
        Svc->>+ExtPay: Process payment
        ExtPay-->>-Svc: OK
    end

    Svc->>+Repo: save(entity)
    Repo->>+DB: INSERT INTO ...
    DB-->>-Repo: Created row
    Repo-->>-Svc: Persisted entity

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 201 Created
```

---

### GET `/payments/{payment_id}` — Retrieve payment details { .endpoint-get }

> Returns full details of a specific payment including processor reference and status history.

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Payments/getPayment){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /payments/(payment_id)
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getPayment()

    Svc->>+Repo: findById(id)
    Repo->>+DB: SELECT ... WHERE id = ?
    DB-->>-Repo: Row
    Repo-->>-Svc: Entity
    Note right of Repo: Returns 404 if not found

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### POST `/payments/{payment_id}/refund` — Initiate a refund { .endpoint-post }

> Creates a refund for the specified payment. Supports full or partial refunds.

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Refunds/refundPayment){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant ExtPay as Payment Gateway
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: POST /payments/(payment_id)/refund
    GW->>+Ctrl: Route request
    Note right of Ctrl: Validate request body
    Ctrl->>+Svc: refundPayment()

    rect rgba(199, 123, 48, 0.08)
        Note over Svc,ExtPay: Cross-service integration
        Svc->>+ExtPay: Process refund
        ExtPay-->>-Svc: OK
    end

    Svc->>+Repo: findParent(parentId)
    Repo->>+DB: SELECT parent
    DB-->>-Repo: Parent row
    Repo-->>-Svc: Parent entity
    Note right of Repo: 404 if parent not found
    Svc->>+Repo: save(entity)
    Repo->>+DB: INSERT INTO ...
    DB-->>-Repo: Created row
    Repo-->>-Svc: Persisted entity

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 201 Created
```

---

### GET `/guests/{guest_id}/payment-history` — Retrieve payment history for a guest { .endpoint-get }

> Returns paginated payment history for a specific guest, ordered by most recent first.

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Payments/getGuestPaymentHistory){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /guests/(guest_id)/payment-history
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getGuestPaymentHistory()

    Svc->>+Repo: findByParent(parentId)
    Repo->>+DB: SELECT ... WHERE parent_id = ?
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: List of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```

---

### GET `/payments/daily-summary` — Get daily payment summary { .endpoint-get }

> Returns an aggregated summary of payments processed on a given date, broken down by method and status.

[:material-open-in-new: View in Swagger UI](../services/api/svc-payments.html#/Reporting/getDailySummary){ .md-button }

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a2744', 'primaryTextColor': '#fff', 'primaryBorderColor': '#c77b30', 'lineColor': '#475569', 'secondaryColor': '#dbeafe', 'tertiaryColor': '#fff7ed', 'noteBkgColor': '#fef3e7', 'noteTextColor': '#1e293b', 'noteBorderColor': '#c77b30', 'actorBkg': '#1a2744', 'actorTextColor': '#fff', 'actorBorder': '#c77b30', 'activationBkgColor': '#dbeafe', 'activationBorderColor': '#3b82f6', 'signalColor': '#1e293b', 'signalTextColor': '#1e293b'}}}%%
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant Ctrl as Controller
    participant Svc as Service Layer
    participant Repo as Repository
    participant DB as PostgreSQL

    C->>+GW: GET /payments/daily-summary
    GW->>+Ctrl: Route request
    Ctrl->>+Svc: getDailySummary()

    Svc->>+Repo: findByFilters(criteria)
    Repo->>+DB: SELECT ... WHERE filters
    DB-->>-Repo: ResultSet
    Repo-->>-Svc: Page of results

    Svc-->>-Ctrl: Result
    Ctrl-->>-GW: Response
    GW-->>-C: 200 OK
```
