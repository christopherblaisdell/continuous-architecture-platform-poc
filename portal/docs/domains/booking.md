# Booking Domain

**Team:** Booking Platform Team  
**Services:** 1  
**Domain color:** #059669

Reservation lifecycle management from creation through completion, including participant management, insurance add-ons, and status tracking.

---

## Topology

<div class="diagram-wrap">
  <a href="../../topology/svg/topology-booking.svg" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>
  <object data="../../topology/svg/topology-booking.svg" type="image/svg+xml" style="max-width: 100%;">
    Booking Service Topology C4 Diagram
  </object>
</div>

---

## Services

| Service | Database Engine | Schema | Tables | API Endpoints |
|---------|----------------|--------|--------|---------------|
| [svc-reservations](../microservices/svc-reservations.md) | PostgreSQL 15 | `reservations` | 3 | 8 |

---

## Data Ownership

Every data entity has exactly one owning service. Other services access it read-only through APIs.

| Data Entity | Owning Service | Read Access |
|-------------|---------------|-------------|
| Reservations | [svc-reservations](../microservices/svc-reservations.md) | svc-check-in, svc-scheduling-orchestrator, svc-partner-integrations |
| Participants | [svc-reservations](../microservices/svc-reservations.md) | svc-check-in |

---

## Data Stores

### svc-reservations

- **Engine:** PostgreSQL 15
- **Schema:** `reservations`
- **Tables:** `reservations`, `participants`, `status_history`
- **Features:**
    - Optimistic locking via _rev field
    - Composite index on (guest_id, trip_date)
    - Monthly partitioning by reservation_date
- **Volume:** ~2,000 new reservations/day
- **Backup:** Continuous WAL archiving, daily base backup, 30-day PITR

---

## Bounded Context Rules

These rules are non-negotiable for this domain.

1. Reservations use **optimistic locking** via `_rev` field to prevent concurrent update conflicts
2. Reservation status transitions are event-sourced via `reservation.status_changed` Kafka events

---

## Cross-Domain Integration

### Outbound (this domain calls)

| Source | Target | Target Domain | Action | Async |
|--------|--------|--------------|--------|-------|
| [svc-reservations](../microservices/svc-reservations.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Guest Identity | Validate guest identity | No |
| [svc-reservations](../microservices/svc-reservations.md) | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | Product Catalog | Check trip availability | No |
| [svc-reservations](../microservices/svc-reservations.md) | [svc-payments](../microservices/svc-payments.md) | Support | Process deposit payment | No |
| [svc-reservations](../microservices/svc-reservations.md) | [svc-notifications](../microservices/svc-notifications.md) | Support | Send booking confirmation | Yes |
| [svc-reservations](../microservices/svc-reservations.md) | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | Product Catalog | Verify availability | No |
| [svc-reservations](../microservices/svc-reservations.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Guest Identity | Validate participant | No |
| [svc-reservations](../microservices/svc-reservations.md) | [svc-notifications](../microservices/svc-notifications.md) | Support | Send status update | Yes |
| [svc-reservations](../microservices/svc-reservations.md) | [svc-notifications](../microservices/svc-notifications.md) | Support | Send insurance confirmation | Yes |

### Inbound (called by other domains)

| Source | Source Domain | Target | Action | Async |
|--------|-------------|--------|--------|-------|
| [svc-check-in](../microservices/svc-check-in.md) | Operations | [svc-reservations](../microservices/svc-reservations.md) | Verify reservation exists | No |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | External | [svc-reservations](../microservices/svc-reservations.md) | Create reservation | No |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | External | [svc-reservations](../microservices/svc-reservations.md) | Confirm reservation | No |
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Guest Identity | [svc-reservations](../microservices/svc-reservations.md) | Query past bookings | No |
| [svc-gear-inventory](../microservices/svc-gear-inventory.md) | Logistics | [svc-reservations](../microservices/svc-reservations.md) | Verify booking | No |
| [svc-transport-logistics](../microservices/svc-transport-logistics.md) | Logistics | [svc-reservations](../microservices/svc-reservations.md) | Get booking details | No |
| [svc-loyalty-rewards](../microservices/svc-loyalty-rewards.md) | Support | [svc-reservations](../microservices/svc-reservations.md) | Verify completed booking | No |
| [svc-reviews](../microservices/svc-reviews.md) | Support | [svc-reservations](../microservices/svc-reservations.md) | Validate reservation exists and is COMPLETED | No |

---

## Domain Events

### Events Produced

| Event | Channel | Producer | Summary |
|-------|---------|----------|---------|
| `reservation.created` | `novatrek.booking.reservation.created` | [svc-reservations](../microservices/svc-reservations.md) | Published when a new reservation is confirmed |
| `reservation.status_changed` | `novatrek.booking.reservation.status-changed` | [svc-reservations](../microservices/svc-reservations.md) | Published when a reservation status transitions |

**Consumers of these events:**

- `reservation.created` → [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md), [svc-analytics](../microservices/svc-analytics.md)
- `reservation.status_changed` → [svc-notifications](../microservices/svc-notifications.md), [svc-analytics](../microservices/svc-analytics.md)

### Events Consumed

| Event | Channel | Producer | Producer Domain | Consuming Service |
|-------|---------|----------|----------------|-------------------|
| `payment.processed` | `novatrek.support.payment.processed` | [svc-payments](../microservices/svc-payments.md) | Support | [svc-reservations](../microservices/svc-reservations.md) |

---

## Business Capabilities

Capabilities served by this domain's services.

| ID | Capability | Status | Description |
|----|-----------|--------|-------------|
| CAP-1.3 | Reservation Management | IMPLEMENTED | Create, modify, cancel, and look up adventure reservations |

---

## Quick Links

- [Domain Topology View](../topology/domain-views.md#booking)
- [svc-reservations Microservice Page](../microservices/svc-reservations.md)
- [Event Catalog](../events/index.md)
- [Business Capabilities](../capabilities/index.md)

---

*Generated from `architecture/metadata/` YAML files by `portal/scripts/generate-domain-pages.py`.*
