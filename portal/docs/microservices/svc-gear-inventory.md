---
tags:
  - microservice
  - svc-gear-inventory
  - logistics
---

# svc-gear-inventory

**NovaTrek Adventures - Gear Inventory Service** &nbsp;|&nbsp; <span style="background: #0891b215; color: #0891b2; border: 1px solid #0891b240; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">Logistics</span> &nbsp;|&nbsp; `v2.4.0` &nbsp;|&nbsp; *NovaTrek Platform Engineering*

> Manages rental equipment inventory, gear packages, guest assignments,

[:material-api: Swagger UI](../services/api/svc-gear-inventory.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-gear-inventory.yaml){ .md-button }
[:material-pipe: CI/CD Pipeline](https://github.com/christopherblaisdell/continuous-architecture-platform-poc-2/actions/workflows/service-svc-gear-inventory.yml){ .md-button }
[:material-source-branch: Source Code](https://github.com/christopherblaisdell/continuous-architecture-platform-poc-2/tree/main/services/svc-gear-inventory){ .md-button }
[:material-language-java: Technology Stack](../technologies.md){ .md-button }

## :material-truck-delivery: Delivery Status

**Delivery Wave:** 3 -- Day-of-Adventure Operations

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

<div class="diagram-wrap"><a href="../svg/svc-gear-inventory--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-gear-inventory--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-gear-inventory C4 context diagram</object></div>


## :material-database: Data Store { #data-store }

### Entity Relationship Diagram

<div class="diagram-wrap"><a href="../svg/svc-gear-inventory--erd.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-gear-inventory--erd.svg" type="image/svg+xml" style="max-width: 100%;">svc-gear-inventory entity relationship diagram</object></div>

### Overview

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `gear` |
| **Tables** | `gear_items`, `gear_packages`, `gear_assignments`, `maintenance_records`, `inventory_levels` |
| **Estimated Volume** | ~1,500 assignments/day peak season |
| **Connection Pool** | min 5 / max 20 / idle timeout 10min |
| **Backup Strategy** | Daily pg_dump, 30-day retention |

### Key Features

- RFID tag tracking via unique identifiers
- Scheduled maintenance alerts with cron triggers
- Location-based inventory partitioning

### Table Reference

#### `gear_items`

*Individual gear items tracked by RFID tag*

| Column | Type | Constraints |
|--------|------|-------------|
| `item_id` | `UUID` | PK |
| `rfid_tag` | `VARCHAR(64)` | NOT NULL, UNIQUE |
| `gear_type` | `VARCHAR(50)` | NOT NULL |
| `size` | `VARCHAR(20)` | NULL |
| `condition` | `VARCHAR(20)` | NOT NULL, DEFAULT 'good' |
| `location_id` | `UUID` | NOT NULL |
| `last_inspected` | `DATE` | NULL |
| `acquired_date` | `DATE` | NOT NULL |

**Indexes:**

- `idx_gear_rfid` on `rfid_tag` (UNIQUE)
- `idx_gear_type_loc` on `gear_type, location_id`
- `idx_gear_condition` on `condition`

#### `gear_assignments`

*Gear lent to guests for specific check-ins*

| Column | Type | Constraints |
|--------|------|-------------|
| `assignment_id` | `UUID` | PK |
| `check_in_id` | `UUID` | NOT NULL |
| `item_id` | `UUID` | NOT NULL, FK -> gear_items |
| `assigned_at` | `TIMESTAMPTZ` | NOT NULL |
| `returned_at` | `TIMESTAMPTZ` | NULL |
| `condition_on_return` | `VARCHAR(20)` | NULL |

**Indexes:**

- `idx_assign_checkin` on `check_in_id`
- `idx_assign_item` on `item_id`
- `idx_assign_outstanding` on `returned_at` (WHERE returned_at IS NULL)

#### `maintenance_records`

*Maintenance and inspection history for gear items*

| Column | Type | Constraints |
|--------|------|-------------|
| `record_id` | `UUID` | PK |
| `item_id` | `UUID` | NOT NULL, FK -> gear_items |
| `maintenance_type` | `VARCHAR(30)` | NOT NULL |
| `performed_by` | `VARCHAR(100)` | NOT NULL |
| `notes` | `TEXT` | NULL |
| `performed_at` | `TIMESTAMPTZ` | NOT NULL |
| `next_due` | `DATE` | NULL |

**Indexes:**

- `idx_maint_item` on `item_id, performed_at DESC`
- `idx_maint_due` on `next_due`


---

## :material-api: Endpoints (12 total)

---

### GET `/gear-items` -- Search gear inventory { .endpoint-get }

> Returns a paginated list of gear items matching the provided filters.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Items/searchGearItems){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-gear-inventory--get-gear-items.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-gear-inventory--get-gear-items.svg" type="image/svg+xml" style="max-width: 100%;">GET /gear-items sequence diagram</object></div>

---

### POST `/gear-items` -- Add new inventory item { .endpoint-post }

> Registers a new piece of gear in the inventory system.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Items/addGearItem){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-gear-inventory--post-gear-items.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-gear-inventory--post-gear-items.svg" type="image/svg+xml" style="max-width: 100%;">POST /gear-items sequence diagram</object></div>

---

### GET `/gear-items/{item_id}` -- Get gear item details { .endpoint-get }

> Returns full details for a single gear item including current status and maintenance schedule.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Items/getGearItem){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-gear-inventory--get-gear-items-item_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-gear-inventory--get-gear-items-item_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /gear-items/{item_id} sequence diagram</object></div>

---

### PATCH `/gear-items/{item_id}` -- Update gear item { .endpoint-patch }

> Partially updates a gear item record. Only provided fields are modified.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Items/updateGearItem){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-gear-inventory--patch-gear-items-item_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-gear-inventory--patch-gear-items-item_id.svg" type="image/svg+xml" style="max-width: 100%;">PATCH /gear-items/{item_id} sequence diagram</object></div>

---

### GET `/gear-packages` -- List gear packages { .endpoint-get }

> Returns all predefined gear bundles, optionally filtered by activity type.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Packages/listGearPackages){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-gear-inventory--get-gear-packages.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-gear-inventory--get-gear-packages.svg" type="image/svg+xml" style="max-width: 100%;">GET /gear-packages sequence diagram</object></div>

---

### GET `/gear-packages/{package_id}` -- Get gear package details { .endpoint-get }

> Returns full details for a gear package including the list of included items and pricing.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Packages/getGearPackage){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-gear-inventory--get-gear-packages-package_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-gear-inventory--get-gear-packages-package_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /gear-packages/{package_id} sequence diagram</object></div>

---

### POST `/gear-assignments` -- Assign gear to a participant { .endpoint-post }

> Creates a gear assignment linking inventory items to a trip participant.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Assignments/createGearAssignment){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-gear-inventory--post-gear-assignments.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-gear-inventory--post-gear-assignments.svg" type="image/svg+xml" style="max-width: 100%;">POST /gear-assignments sequence diagram</object></div>

---

### GET `/gear-assignments/{assignment_id}` -- Get gear assignment details { .endpoint-get }

> Returns full details of a gear assignment including item list and return status.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Assignments/getGearAssignment){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-gear-inventory--get-gear-assignments-assignment_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-gear-inventory--get-gear-assignments-assignment_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /gear-assignments/{assignment_id} sequence diagram</object></div>

---

### DELETE `/gear-assignments/{assignment_id}` -- Return gear (close assignment) { .endpoint-delete }

> Marks gear as returned and closes the assignment. Accepts optional

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Assignments/returnGearAssignment){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-gear-inventory--delete-gear-assignments-assignment_id.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-gear-inventory--delete-gear-assignments-assignment_id.svg" type="image/svg+xml" style="max-width: 100%;">DELETE /gear-assignments/{assignment_id} sequence diagram</object></div>

---

### PUT `/gear-items/{item_id}/maintenance` -- Log a maintenance event { .endpoint-put }

> Records a maintenance event (inspection, repair, or part replacement) for a gear item and updates its condition and next-due date.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Maintenance/logMaintenanceEvent){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-gear-inventory--put-gear-items-item_id-maintenance.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-gear-inventory--put-gear-items-item_id-maintenance.svg" type="image/svg+xml" style="max-width: 100%;">PUT /gear-items/{item_id}/maintenance sequence diagram</object></div>

---

### GET `/gear-items/{item_id}/maintenance-history` -- Get maintenance history { .endpoint-get }

> Returns the chronological maintenance history for a specific gear item.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Maintenance/getMaintenanceHistory){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-gear-inventory--get-gear-items-item_id-maintenance-history.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-gear-inventory--get-gear-items-item_id-maintenance-history.svg" type="image/svg+xml" style="max-width: 100%;">GET /gear-items/{item_id}/maintenance-history sequence diagram</object></div>

---

### GET `/inventory-levels` -- Get stock levels by location and category { .endpoint-get }

> Returns current inventory counts broken down by location and gear category, including available, assigned, and in-maintenance tallies.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Inventory%20Levels/getInventoryLevels){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-gear-inventory--get-inventory-levels.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-gear-inventory--get-inventory-levels.svg" type="image/svg+xml" style="max-width: 100%;">GET /inventory-levels sequence diagram</object></div>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Operations Dashboard](../../applications/web-ops-dashboard/) | Check-In Station, Inventory Management |
| [Adventure App](../../applications/app-guest-mobile/) | Self Check-In, Digital Wristband |
