# Logistics Domain

**Team:** Logistics Team  
**Services:** 2  
**Domain color:** #0891b2

Physical asset management covering gear inventory, equipment tracking, transport coordination, and vehicle dispatch.

---

## Topology

<div class="diagram-wrap">
  <a href="../../topology/svg/topology-logistics.svg" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>
  <object data="../../topology/svg/topology-logistics.svg" type="image/svg+xml" style="max-width: 100%;">
    Logistics Service Topology C4 Diagram
  </object>
</div>

---

## Services

| Service | Database Engine | Schema | Tables | API Endpoints |
|---------|----------------|--------|--------|---------------|
| [svc-transport-logistics](../microservices/svc-transport-logistics.md) | PostgreSQL 15 | `transport` | 4 | 7 |
| [svc-gear-inventory](../microservices/svc-gear-inventory.md) | PostgreSQL 15 | `gear` | 5 | 12 |

---

## Data Ownership

Every data entity has exactly one owning service. Other services access it read-only through APIs.

| Data Entity | Owning Service | Read Access |
|-------------|---------------|-------------|
| Gear inventory | [svc-gear-inventory](../microservices/svc-gear-inventory.md) | svc-check-in (read), svc-inventory-procurement |
| Transport requests | [svc-transport-logistics](../microservices/svc-transport-logistics.md) | svc-notifications |

---

## Data Stores

### svc-transport-logistics

- **Engine:** PostgreSQL 15
- **Schema:** `transport`
- **Tables:** `routes`, `route_schedules`, `transport_requests`, `vehicles`
- **Features:**
    - Time-window optimization for route scheduling
    - Vehicle capacity tracking with overbooking prevention
    - GPS coordinate storage for pickup and dropoff points
- **Volume:** ~300 transport requests/day
- **Backup:** Daily pg_dump, 14-day retention

### svc-gear-inventory

- **Engine:** PostgreSQL 15
- **Schema:** `gear`
- **Tables:** `gear_items`, `gear_packages`, `gear_assignments`, `maintenance_records`, `inventory_levels`
- **Features:**
    - RFID tag tracking via unique identifiers
    - Scheduled maintenance alerts with cron triggers
    - Location-based inventory partitioning
- **Volume:** ~1,500 assignments/day peak season
- **Backup:** Daily pg_dump, 30-day retention

---

## Bounded Context Rules

These rules are non-negotiable for this domain.

1. Gear assignments require validated guest identity and confirmed reservation before checkout
2. Waiver status is checked before safety-critical gear can be issued

---

## Cross-Domain Integration

### Outbound (this domain calls)

| Source | Target | Target Domain | Action | Async |
|--------|--------|--------------|--------|-------|
| [svc-gear-inventory](../microservices/svc-gear-inventory.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Guest Identity | Validate guest | No |
| [svc-gear-inventory](../microservices/svc-gear-inventory.md) | [svc-reservations](../microservices/svc-reservations.md) | Booking | Verify booking | No |
| [svc-gear-inventory](../microservices/svc-gear-inventory.md) | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Safety | Check waiver status | No |
| [svc-transport-logistics](../microservices/svc-transport-logistics.md) | [svc-reservations](../microservices/svc-reservations.md) | Booking | Get booking details | No |
| [svc-transport-logistics](../microservices/svc-transport-logistics.md) | [svc-location-services](../microservices/svc-location-services.md) | Support | Validate pickup location | No |
| [svc-transport-logistics](../microservices/svc-transport-logistics.md) | [svc-notifications](../microservices/svc-notifications.md) | Support | Send transport details | Yes |

### Inbound (called by other domains)

| Source | Source Domain | Target | Action | Async |
|--------|-------------|--------|--------|-------|
| [svc-check-in](../microservices/svc-check-in.md) | Operations | [svc-gear-inventory](../microservices/svc-gear-inventory.md) | Verify gear assignment | No |
| [svc-inventory-procurement](../microservices/svc-inventory-procurement.md) | Support | [svc-gear-inventory](../microservices/svc-gear-inventory.md) | Verify item catalog | No |

---

## Domain Events

No domain events produced or consumed by this domain.

---

## Business Capabilities

Capabilities served by this domain's services.

| ID | Capability | Status | Description |
|----|-----------|--------|-------------|
| CAP-2.5 | Transport Coordination | IMPLEMENTED | Vehicle dispatch, route planning, and guest transport scheduling |
| CAP-4.1 | Gear Inventory and Tracking | IMPLEMENTED | Equipment checkout, return tracking, maintenance scheduling |
| CAP-4.4 | Vehicle Fleet Management | IMPLEMENTED | Vehicle inventory, maintenance scheduling, utilization tracking |

---

## Quick Links

- [Domain Topology View](../topology/domain-views.md#logistics)
- [svc-transport-logistics Microservice Page](../microservices/svc-transport-logistics.md)
- [svc-gear-inventory Microservice Page](../microservices/svc-gear-inventory.md)
- [Event Catalog](../events/index.md)
- [Business Capabilities](../capabilities/index.md)

---

*Generated from `architecture/metadata/` YAML files by `portal/scripts/generate-domain-pages.py`.*
