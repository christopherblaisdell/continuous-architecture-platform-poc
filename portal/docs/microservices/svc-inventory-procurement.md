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
[:material-rocket-launch: Live Service (Dev)](https://ca-svc-inventory-procurement.blackwater-fd4bc06d.eastus2.azurecontainerapps.io/actuator/health){ .md-button }
[:material-microsoft-azure: Azure Portal](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-inventory-procurement){ .md-button }
[:material-pipe: CI/CD Pipeline](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/service-ci.yml){ .md-button }
[:material-source-branch: Source Code](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/services/svc-inventory-procurement){ .md-button }
[:material-language-java: Technology Stack](../technologies.md){ .md-button }

## :material-truck-delivery: Delivery Status

**Delivery Wave:** 6 -- External Integrations

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

- [:material-microsoft-azure: Container App](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-inventory-procurement)
- [:material-database: PostgreSQL Server](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.DBforPostgreSQL/flexibleServers/pg-novatrek-dev-smwd6ded4e3so)
- [:material-text-search: Log Analytics](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.OperationalInsights/workspaces/log-novatrek-dev/logs)

---

## :material-map: Integration Context

<div class="diagram-wrap"><a href="../svg/svc-inventory-procurement--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-inventory-procurement--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-inventory-procurement C4 context diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-inventory-procurement.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-inventory-procurement.yaml` + `cross-service-calls.yaml`</a>


## :material-database: Data Store { #data-store }

### Entity Relationship Diagram

<div class="diagram-wrap"><a href="../svg/svc-inventory-procurement--erd.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-inventory-procurement--erd.svg" type="image/svg+xml" style="max-width: 100%;">svc-inventory-procurement entity relationship diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/data-stores.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/metadata/data-stores.yaml`</a>

### Overview

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `procurement` |
| **Tables** | `purchase_orders`, `po_line_items`, `suppliers`, `stock_levels`, `stock_adjustments`, `reorder_alerts` |
| **Estimated Volume** | ~50 POs/day, ~200 stock adjustments/day |
| **Connection Pool** | min 3 / max 10 / idle timeout 10min |
| **Backup Strategy** | Daily pg_dump, 30-day retention |

### Key Features

- Purchase order approval workflow with state machine
- Automatic reorder point calculation based on consumption
- Supplier lead time tracking for delivery estimates

### Table Reference

#### `purchase_orders`

*Purchase orders with approval state machine*

| Column | Type | Constraints |
|--------|------|-------------|
| `po_id` | `UUID` | PK |
| `supplier_id` | `UUID` | NOT NULL, FK -> suppliers |
| `status` | `VARCHAR(20)` | NOT NULL, DEFAULT 'draft' |
| `total_amount` | `DECIMAL(10,2)` | NOT NULL |
| `currency` | `CHAR(3)` | NOT NULL, DEFAULT 'USD' |
| `approved_by` | `VARCHAR(100)` | NULL |
| `submitted_at` | `TIMESTAMPTZ` | NULL |
| `approved_at` | `TIMESTAMPTZ` | NULL |
| `created_at` | `TIMESTAMPTZ` | NOT NULL |

**Indexes:**

- `idx_po_supplier` on `supplier_id`
- `idx_po_status` on `status`

#### `suppliers`

*Approved suppliers with performance tracking*

| Column | Type | Constraints |
|--------|------|-------------|
| `supplier_id` | `UUID` | PK |
| `name` | `VARCHAR(200)` | NOT NULL |
| `contact_email` | `VARCHAR(255)` | NOT NULL |
| `lead_time_days` | `INTEGER` | NOT NULL |
| `rating` | `DECIMAL(3,2)` | NULL |
| `active` | `BOOLEAN` | NOT NULL, DEFAULT TRUE |

**Indexes:**

- `idx_supplier_active` on `active`

#### `stock_levels`

*Current stock quantities with reorder thresholds*

| Column | Type | Constraints |
|--------|------|-------------|
| `stock_id` | `UUID` | PK |
| `item_type` | `VARCHAR(50)` | NOT NULL |
| `location_id` | `UUID` | NOT NULL |
| `quantity_on_hand` | `INTEGER` | NOT NULL |
| `reorder_point` | `INTEGER` | NOT NULL |
| `reorder_quantity` | `INTEGER` | NOT NULL |
| `last_counted_at` | `TIMESTAMPTZ` | NULL |

**Indexes:**

- `idx_stock_item_loc` on `item_type, location_id` (UNIQUE)
- `idx_stock_reorder` on `quantity_on_hand` (WHERE quantity_on_hand <= reorder_point)


---

## :material-api: Endpoints (8 total)

---

### POST `/purchase-orders` -- Create a new purchase order { .endpoint-post }

> Initiates a purchase order in DRAFT status. Items reference gear categories from svc-gear-inventory.

[:material-open-in-new: View in Swagger UI](../services/api/svc-inventory-procurement.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-inventory-procurement--post-purchase-orders.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-inventory-procurement--post-purchase-orders.svg" type="image/svg+xml" style="max-width: 100%;">POST /purchase-orders sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-inventory-procurement.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-inventory-procurement.yaml`</a>

---

### GET `/purchase-orders/{po_id}` -- Get purchase order details { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-inventory-procurement.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-inventory-procurement--get-purchase-orders-po_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-inventory-procurement--get-purchase-orders-po_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /purchase-orders/{po_id} sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-inventory-procurement.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-inventory-procurement.yaml`</a>

---

### PATCH `/purchase-orders/{po_id}` -- Update purchase order status or line items { .endpoint-patch }

> Supports status transitions: DRAFT->SUBMITTED->APPROVED->SHIPPED->RECEIVED.

[:material-open-in-new: View in Swagger UI](../services/api/svc-inventory-procurement.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-inventory-procurement--patch-purchase-orders-po_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-inventory-procurement--patch-purchase-orders-po_id.svg" type="image/svg+xml" style="max-width: 100%;">PATCH /purchase-orders/{po_id} sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-inventory-procurement.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-inventory-procurement.yaml`</a>

---

### GET `/suppliers` -- List all suppliers { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-inventory-procurement.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-inventory-procurement--get-suppliers.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-inventory-procurement--get-suppliers.svg" type="image/svg+xml" style="max-width: 100%;">GET /suppliers sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-inventory-procurement.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-inventory-procurement.yaml`</a>

---

### POST `/suppliers` -- Register a new supplier { .endpoint-post }

[:material-open-in-new: View in Swagger UI](../services/api/svc-inventory-procurement.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-inventory-procurement--post-suppliers.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-inventory-procurement--post-suppliers.svg" type="image/svg+xml" style="max-width: 100%;">POST /suppliers sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-inventory-procurement.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-inventory-procurement.yaml`</a>

---

### GET `/stock-levels` -- Query current stock levels { .endpoint-get }

> Returns stock levels filtered by location and/or item category.

[:material-open-in-new: View in Swagger UI](../services/api/svc-inventory-procurement.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-inventory-procurement--get-stock-levels.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-inventory-procurement--get-stock-levels.svg" type="image/svg+xml" style="max-width: 100%;">GET /stock-levels sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-inventory-procurement.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-inventory-procurement.yaml`</a>

---

### POST `/stock-adjustments` -- Record a stock adjustment { .endpoint-post }

> Used for manual corrections, damage write-offs, or receiving shipments outside PO flow.

[:material-open-in-new: View in Swagger UI](../services/api/svc-inventory-procurement.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-inventory-procurement--post-stock-adjustments.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-inventory-procurement--post-stock-adjustments.svg" type="image/svg+xml" style="max-width: 100%;">POST /stock-adjustments sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-inventory-procurement.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-inventory-procurement.yaml`</a>

---

### GET `/reorder-alerts` -- Get active reorder alerts { .endpoint-get }

> Returns items that have fallen below their configured reorder point and need replenishment.

[:material-open-in-new: View in Swagger UI](../services/api/svc-inventory-procurement.html){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-inventory-procurement--get-reorder-alerts.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-inventory-procurement--get-reorder-alerts.svg" type="image/svg+xml" style="max-width: 100%;">GET /reorder-alerts sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-inventory-procurement.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-inventory-procurement.yaml`</a>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Operations Dashboard](../../applications/web-ops-dashboard/) | Inventory Management |
