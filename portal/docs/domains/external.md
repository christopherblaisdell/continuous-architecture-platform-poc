# External Domain

**Team:** Integration Team  
**Services:** 1  
**Domain color:** #9333ea

Third-party booking channel integrations, partner API gateway, and external system connectivity.

---

## Topology

<div class="diagram-wrap">
  <a href="../../topology/svg/topology-external.svg" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>
  <object data="../../topology/svg/topology-external.svg" type="image/svg+xml" style="max-width: 100%;">
    External Service Topology C4 Diagram
  </object>
</div>

---

## Services

| Service | Database Engine | Schema | Tables | API Endpoints |
|---------|----------------|--------|--------|---------------|
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | PostgreSQL 15 | `partners` | 4 | 7 |

---

## Data Ownership

Every data entity has exactly one owning service. Other services access it read-only through APIs.

| Data Entity | Owning Service | Read Access |
|-------------|---------------|-------------|
| Partner bookings | [svc-partner-integrations](../microservices/svc-partner-integrations.md) | svc-reservations (via delegation) |
| Partner credentials | [svc-partner-integrations](../microservices/svc-partner-integrations.md) | None |

---

## Data Stores

### svc-partner-integrations

- **Engine:** PostgreSQL 15
- **Schema:** `partners`
- **Tables:** `partners`, `partner_bookings`, `commission_records`, `reconciliation_log`
- **Features:**
    - Partner API key management with rotation policy
    - Commission calculation engine with tiered rates
    - Idempotency keys for booking creation
- **Volume:** ~400 partner bookings/day
- **Backup:** Daily pg_dump, 30-day retention

---

## Bounded Context Rules

These rules are non-negotiable for this domain.

1. Partner bookings flow through the same reservation pipeline as direct bookings — partners call svc-partner-integrations which delegates to svc-reservations
2. Commission processing is handled via svc-payments

---

## Cross-Domain Integration

### Outbound (this domain calls)

| Source | Target | Target Domain | Action | Async |
|--------|--------|--------------|--------|-------|
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Guest Identity | Validate guest identity | No |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | Product Catalog | Check trip availability | No |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-reservations](../microservices/svc-reservations.md) | Booking | Create reservation | No |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-reservations](../microservices/svc-reservations.md) | Booking | Confirm reservation | No |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-payments](../microservices/svc-payments.md) | Support | Process commission | No |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-notifications](../microservices/svc-notifications.md) | Support | Send partner confirmation | Yes |

### Inbound

No inbound cross-domain calls.

---

## Domain Events

No domain events produced or consumed by this domain.

---

## Business Capabilities

Capabilities served by this domain's services.

| ID | Capability | Status | Description |
|----|-----------|--------|-------------|
| CAP-6.1 | Third-Party Booking Channels | IMPLEMENTED | OTA integrations, partner API gateway, booking ingestion |
| CAP-6.2 | Affiliate and Commission Management | PARTIAL | Commission calculation, partner payout, and affiliate tracking |

---

## Quick Links

- [Domain Topology View](../topology/domain-views.md#external)
- [svc-partner-integrations Microservice Page](../microservices/svc-partner-integrations.md)
- [Event Catalog](../events/index.md)
- [Business Capabilities](../capabilities/index.md)

---

*Generated from `architecture/metadata/` YAML files by `portal/scripts/generate-domain-pages.py`.*
