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

---

## :material-database: Data Store

| Property | Detail |
|----------|--------|
| **Engine** | PostgreSQL 15 |
| **Schema** | `gear` |
| **Primary Tables** | `gear_items`, `gear_packages`, `gear_assignments`, `maintenance_records`, `inventory_levels` |
| **Key Features** | RFID tag tracking via unique identifiers | Scheduled maintenance alerts with cron triggers | Location-based inventory partitioning |
| **Estimated Volume** | ~1,500 assignments/day peak season |

---

## :material-api: Endpoints (12 total)

---

### GET `/gear-items` -- Search gear inventory { .endpoint-get }

> Returns a paginated list of gear items matching the provided filters.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Items/searchGearItems){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-gear-inventory--get-gear-items.svg" type="image/svg+xml" style="max-width: 100%;">GET /gear-items sequence diagram</object></div>

---

### POST `/gear-items` -- Add new inventory item { .endpoint-post }

> Registers a new piece of gear in the inventory system.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Items/addGearItem){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-gear-inventory--post-gear-items.svg" type="image/svg+xml" style="max-width: 100%;">POST /gear-items sequence diagram</object></div>

---

### GET `/gear-items/{item_id}` -- Get gear item details { .endpoint-get }

> Returns full details for a single gear item including current status and maintenance schedule.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Items/getGearItem){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-gear-inventory--get-gear-items-item_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /gear-items/{item_id} sequence diagram</object></div>

---

### PATCH `/gear-items/{item_id}` -- Update gear item { .endpoint-patch }

> Partially updates a gear item record. Only provided fields are modified.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Items/updateGearItem){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-gear-inventory--patch-gear-items-item_id.svg" type="image/svg+xml" style="max-width: 100%;">PATCH /gear-items/{item_id} sequence diagram</object></div>

---

### GET `/gear-packages` -- List gear packages { .endpoint-get }

> Returns all predefined gear bundles, optionally filtered by activity type.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Packages/listGearPackages){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-gear-inventory--get-gear-packages.svg" type="image/svg+xml" style="max-width: 100%;">GET /gear-packages sequence diagram</object></div>

---

### GET `/gear-packages/{package_id}` -- Get gear package details { .endpoint-get }

> Returns full details for a gear package including the list of included items and pricing.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Packages/getGearPackage){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-gear-inventory--get-gear-packages-package_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /gear-packages/{package_id} sequence diagram</object></div>

---

### POST `/gear-assignments` -- Assign gear to a participant { .endpoint-post }

> Creates a gear assignment linking inventory items to a trip participant.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Assignments/createGearAssignment){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-gear-inventory--post-gear-assignments.svg" type="image/svg+xml" style="max-width: 100%;">POST /gear-assignments sequence diagram</object></div>

---

### GET `/gear-assignments/{assignment_id}` -- Get gear assignment details { .endpoint-get }

> Returns full details of a gear assignment including item list and return status.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Assignments/getGearAssignment){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-gear-inventory--get-gear-assignments-assignment_id.svg" type="image/svg+xml" style="max-width: 100%;">GET /gear-assignments/{assignment_id} sequence diagram</object></div>

---

### DELETE `/gear-assignments/{assignment_id}` -- Return gear (close assignment) { .endpoint-delete }

> Marks gear as returned and closes the assignment. Accepts optional

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Gear%20Assignments/returnGearAssignment){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-gear-inventory--delete-gear-assignments-assignment_id.svg" type="image/svg+xml" style="max-width: 100%;">DELETE /gear-assignments/{assignment_id} sequence diagram</object></div>

---

### PUT `/gear-items/{item_id}/maintenance` -- Log a maintenance event { .endpoint-put }

> Records a maintenance event (inspection, repair, or part replacement) for a gear item and updates its condition and next-due date.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Maintenance/logMaintenanceEvent){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-gear-inventory--put-gear-items-item_id-maintenance.svg" type="image/svg+xml" style="max-width: 100%;">PUT /gear-items/{item_id}/maintenance sequence diagram</object></div>

---

### GET `/gear-items/{item_id}/maintenance-history` -- Get maintenance history { .endpoint-get }

> Returns the chronological maintenance history for a specific gear item.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Maintenance/getMaintenanceHistory){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-gear-inventory--get-gear-items-item_id-maintenance-history.svg" type="image/svg+xml" style="max-width: 100%;">GET /gear-items/{item_id}/maintenance-history sequence diagram</object></div>

---

### GET `/inventory-levels` -- Get stock levels by location and category { .endpoint-get }

> Returns current inventory counts broken down by location and gear category, including available, assigned, and in-maintenance tallies.

[:material-open-in-new: View in Swagger UI](../services/api/svc-gear-inventory.html#/Inventory%20Levels/getInventoryLevels){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-gear-inventory--get-inventory-levels.svg" type="image/svg+xml" style="max-width: 100%;">GET /inventory-levels sequence diagram</object></div>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Operations Dashboard](../../applications/web-ops-dashboard/) | Check-In Station, Inventory Management |
| [Adventure App](../../applications/app-guest-mobile/) | Self Check-In, Digital Wristband |
