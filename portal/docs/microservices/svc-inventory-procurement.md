---
tags:
  - microservice
  - svc-inventory-procurement
  - support
---

# svc-inventory-procurement

**NovaTrek Inventory Procurement API** &nbsp;|&nbsp; <span style="background: #64748b15; color: #64748b; border: 1px solid #64748b40; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">Support</span> &nbsp;|&nbsp; `v2.1.0` &nbsp;|&nbsp; *NovaTrek Platform Engineering*

> Manages purchasing workflows, supplier relationships, and stock replenishment

[:material-api: Swagger UI](../services/api/svc-inventory-procurement.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-inventory-procurement.yaml){ .md-button }

---

## :material-map: Integration Context

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-inventory-procurement--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-inventory-procurement C4 context diagram</object></div>

---

## :material-database: Data Store

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `procurement` |
| **Primary Tables** | `purchase_orders`, `po_line_items`, `suppliers`, `stock_levels`, `stock_adjustments`, `reorder_alerts` |
| **Key Features** | Purchase order approval workflow with state machine | Automatic reorder point calculation based on consumption | Supplier lead time tracking for delivery estimates |
| **Estimated Volume** | ~50 POs/day, ~200 stock adjustments/day |

---

## :material-api: Endpoints (8 total)

---

### POST `/purchase-orders` -- Create a new purchase order { .endpoint-post }

> Initiates a purchase order in DRAFT status. Items reference gear categories from svc-gear-inventory.

[:material-open-in-new: View in Swagger UI](../services/api/svc-inventory-procurement.html){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-inventory-procurement--post-purchase-orders.svg" type="image/svg+xml" style="max-width: 100%;">POST /purchase-orders sequence diagram</object></div>

---

### GET `/purchase-orders/{po_id}` -- Get purchase order details { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-inventory-procurement.html){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-inventory-procurement--get-purchase-orders-po_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /purchase-orders/{po_id} sequence diagram</object></div>

---

### PATCH `/purchase-orders/{po_id}` -- Update purchase order status or line items { .endpoint-patch }

> Supports status transitions: DRAFT->SUBMITTED->APPROVED->SHIPPED->RECEIVED.

[:material-open-in-new: View in Swagger UI](../services/api/svc-inventory-procurement.html){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-inventory-procurement--patch-purchase-orders-po_id.svg" type="image/svg+xml" style="max-width: 100%;">PATCH /purchase-orders/{po_id} sequence diagram</object></div>

---

### GET `/suppliers` -- List all suppliers { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-inventory-procurement.html){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-inventory-procurement--get-suppliers.svg" type="image/svg+xml" style="max-width: 100%;">GET /suppliers sequence diagram</object></div>

---

### POST `/suppliers` -- Register a new supplier { .endpoint-post }

[:material-open-in-new: View in Swagger UI](../services/api/svc-inventory-procurement.html){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-inventory-procurement--post-suppliers.svg" type="image/svg+xml" style="max-width: 100%;">POST /suppliers sequence diagram</object></div>

---

### GET `/stock-levels` -- Query current stock levels { .endpoint-get }

> Returns stock levels filtered by location and/or item category.

[:material-open-in-new: View in Swagger UI](../services/api/svc-inventory-procurement.html){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-inventory-procurement--get-stock-levels.svg" type="image/svg+xml" style="max-width: 100%;">GET /stock-levels sequence diagram</object></div>

---

### POST `/stock-adjustments` -- Record a stock adjustment { .endpoint-post }

> Used for manual corrections, damage write-offs, or receiving shipments outside PO flow.

[:material-open-in-new: View in Swagger UI](../services/api/svc-inventory-procurement.html){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-inventory-procurement--post-stock-adjustments.svg" type="image/svg+xml" style="max-width: 100%;">POST /stock-adjustments sequence diagram</object></div>

---

### GET `/reorder-alerts` -- Get active reorder alerts { .endpoint-get }

> Returns items that have fallen below their configured reorder point and need replenishment.

[:material-open-in-new: View in Swagger UI](../services/api/svc-inventory-procurement.html){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-inventory-procurement--get-reorder-alerts.svg" type="image/svg+xml" style="max-width: 100%;">GET /reorder-alerts sequence diagram</object></div>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Operations Dashboard](../../applications/web-ops-dashboard/) | Inventory Management |
