# Domains

The NovaTrek Adventures platform is decomposed into **9 bounded contexts** (domains), each owning a set of microservices with clearly defined data ownership boundaries.

Click any domain to view its comprehensive detail page including services, data stores, integrations, events, decisions, and capabilities.

## Domain Overview

| Domain | Services | Team | Events Produced | Events Consumed | Capabilities |
|--------|----------|------|-----------------|-----------------|-------------|
| **[Operations](operations.md)** | 2 | NovaTrek Operations Team | 2 | 3 | 2 |
| **[Guest Identity](guest-identity.md)** | 1 | Guest Experience Team | 1 | 0 | 1 |
| **[Booking](booking.md)** | 1 | Booking Platform Team | 2 | 1 | 1 |
| **[Product Catalog](product-catalog.md)** | 2 | Product Team | 0 | 1 | 4 |
| **[Safety](safety.md)** | 3 | Safety and Compliance Team | 3 | 1 | 4 |
| **[Logistics](logistics.md)** | 2 | Logistics Team | 0 | 0 | 3 |
| **[Guide Management](guide-management.md)** | 1 | Guide Operations Team | 0 | 1 | 1 |
| **[External](external.md)** | 1 | Integration Team | 0 | 0 | 2 |
| **[Support](support.md)** | 9 | Various (cross-cutting platform services) | 1 | 15 | 13 |

---

## Service-to-Domain Map

Complete mapping of all microservices to their owning domain.

| Service | Domain | Database Engine |
|---------|--------|----------------|
| [svc-check-in](../microservices/svc-check-in.md) | [Operations](operations.md) | PostgreSQL 15 |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [Operations](operations.md) | PostgreSQL 15 + Valkey 8 |
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | [Guest Identity](guest-identity.md) | PostgreSQL 15 |
| [svc-reservations](../microservices/svc-reservations.md) | [Booking](booking.md) | PostgreSQL 15 |
| [svc-trip-catalog](../microservices/svc-trip-catalog.md) | [Product Catalog](product-catalog.md) | PostgreSQL 15 |
| [svc-trail-management](../microservices/svc-trail-management.md) | [Product Catalog](product-catalog.md) | PostGIS (PostgreSQL 15) |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | [Safety](safety.md) | PostgreSQL 15 |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | [Safety](safety.md) | PostgreSQL 15 |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | [Safety](safety.md) | PostgreSQL 15 |
| [svc-transport-logistics](../microservices/svc-transport-logistics.md) | [Logistics](logistics.md) | PostgreSQL 15 |
| [svc-gear-inventory](../microservices/svc-gear-inventory.md) | [Logistics](logistics.md) | PostgreSQL 15 |
| [svc-guide-management](../microservices/svc-guide-management.md) | [Guide Management](guide-management.md) | PostgreSQL 15 |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [External](external.md) | PostgreSQL 15 |
| [svc-notifications](../microservices/svc-notifications.md) | [Support](support.md) | PostgreSQL 15 + Valkey 8 |
| [svc-payments](../microservices/svc-payments.md) | [Support](support.md) | PostgreSQL 15 |
| [svc-loyalty-rewards](../microservices/svc-loyalty-rewards.md) | [Support](support.md) | Couchbase 7 |
| [svc-media-gallery](../microservices/svc-media-gallery.md) | [Support](support.md) | PostgreSQL 15 + S3-Compatible Object Store |
| [svc-analytics](../microservices/svc-analytics.md) | [Support](support.md) | Oracle Database 19c |
| [svc-weather](../microservices/svc-weather.md) | [Support](support.md) | Valkey 8 + PostgreSQL 15 |
| [svc-location-services](../microservices/svc-location-services.md) | [Support](support.md) | PostGIS (PostgreSQL 15) |
| [svc-inventory-procurement](../microservices/svc-inventory-procurement.md) | [Support](support.md) | PostgreSQL 15 |
| [svc-reviews](../microservices/svc-reviews.md) | [Support](support.md) | PostgreSQL 15 |

---

## Cross-Domain Dependencies

Summary of which domains call which other domains.

| From \ To | **Operations** | **Guest Identity** | **Booking** | **Product Catalog** | **Safety** | **Logistics** | **Guide Management** | **External** | **Support** |
|---|---|---|---|---|---|---|---|---|---|
| **Operations** | — | 1 | 1 | 4 | 2 | 1 | 3 | · | 6 |
| **Guest Identity** | · | — | 1 | · | · | · | · | · | 1 |
| **Booking** | · | 2 | — | 2 | · | · | · | · | 4 |
| **Product Catalog** | · | · | · | — | 2 | · | · | · | 3 |
| **Safety** | · | 3 | · | 2 | — | · | 3 | · | 7 |
| **Logistics** | · | 1 | 2 | · | 1 | — | · | · | 2 |
| **Guide Management** | · | · | · | · | · | · | — | · | · |
| **External** | · | 1 | 2 | 1 | · | · | · | — | 2 |
| **Support** | · | 3 | 2 | · | · | 1 | · | · | — |

---

## Event Flow Summary

| Event | Producer Domain | Consumer Domains |
|-------|----------------|-----------------|
| `reservation.created` | Booking | Operations, Support |
| `reservation.status_changed` | Booking | Support |
| `guest.registered` | Guest Identity | Support |
| `checkin.completed` | Operations | Support |
| `schedule.published` | Operations | Guide Management, Support |
| `payment.processed` | Support | Booking, Support |
| `incident.reported` | Safety | Support |
| `emergency.triggered` | Safety | Operations, Safety, Support |
| `wildlife_alert.issued` | Safety | Operations, Product Catalog, Support |

---

*Generated from `architecture/metadata/` YAML files by `portal/scripts/generate-domain-pages.py`.*
