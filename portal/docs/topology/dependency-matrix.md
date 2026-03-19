# Dependency Matrix

Service-to-service dependency table showing which services call which, and over what protocol.

!!! info "Everything on this portal is entirely fictional"
    NovaTrek Adventures is a completely fictitious company used as a synthetic workspace for the Continuous Architecture Platform proof of concept.

---

## Reading the Matrix

- Each row is a **calling service** (source)
- Each column shows the **protocol used**: REST (synchronous HTTPS) or Kafka (asynchronous event)
- Services are grouped by domain

## Outbound Dependencies (Who Does This Service Call?)

### Booking

**[svc-reservations](../microservices/svc-reservations.md)** calls:

| Target Service | Protocol |
|----------------|----------|
| [svc-analytics](../microservices/svc-analytics.md) | Kafka |
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | HTTPS |
| [svc-notifications](../microservices/svc-notifications.md) | Kafka |
| [svc-payments](../microservices/svc-payments.md) | HTTPS |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | Kafka |
| [svc-trip-catalog](../microservices/svc-trip-catalog.md) | HTTPS |

### External

**[svc-partner-integrations](../microservices/svc-partner-integrations.md)** calls:

| Target Service | Protocol |
|----------------|----------|
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | HTTPS |
| [svc-notifications](../microservices/svc-notifications.md) | Kafka |
| [svc-payments](../microservices/svc-payments.md) | HTTPS |
| [svc-reservations](../microservices/svc-reservations.md) | HTTPS |
| [svc-trip-catalog](../microservices/svc-trip-catalog.md) | HTTPS |

### Guest Identity

**[svc-guest-profiles](../microservices/svc-guest-profiles.md)** calls:

| Target Service | Protocol |
|----------------|----------|
| [svc-analytics](../microservices/svc-analytics.md) | HTTPS, Kafka |
| [svc-loyalty-rewards](../microservices/svc-loyalty-rewards.md) | Kafka |
| [svc-reservations](../microservices/svc-reservations.md) | HTTPS |

### Guide Management

**[svc-guide-management](../microservices/svc-guide-management.md)** — No outbound service dependencies

### Logistics

**[svc-gear-inventory](../microservices/svc-gear-inventory.md)** calls:

| Target Service | Protocol |
|----------------|----------|
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | HTTPS |
| [svc-reservations](../microservices/svc-reservations.md) | HTTPS |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | HTTPS |

**[svc-transport-logistics](../microservices/svc-transport-logistics.md)** calls:

| Target Service | Protocol |
|----------------|----------|
| [svc-location-services](../microservices/svc-location-services.md) | HTTPS |
| [svc-notifications](../microservices/svc-notifications.md) | Kafka |
| [svc-reservations](../microservices/svc-reservations.md) | HTTPS |

### Operations

**[svc-check-in](../microservices/svc-check-in.md)** calls:

| Target Service | Protocol |
|----------------|----------|
| [svc-analytics](../microservices/svc-analytics.md) | Kafka |
| [svc-gear-inventory](../microservices/svc-gear-inventory.md) | HTTPS |
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | HTTPS |
| [svc-notifications](../microservices/svc-notifications.md) | Kafka |
| [svc-reservations](../microservices/svc-reservations.md) | HTTPS |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | HTTPS |
| [svc-trip-catalog](../microservices/svc-trip-catalog.md) | HTTPS |

**[svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md)** calls:

| Target Service | Protocol |
|----------------|----------|
| [svc-analytics](../microservices/svc-analytics.md) | Kafka |
| [svc-guide-management](../microservices/svc-guide-management.md) | HTTPS, Kafka |
| [svc-location-services](../microservices/svc-location-services.md) | HTTPS |
| [svc-notifications](../microservices/svc-notifications.md) | Kafka |
| [svc-trail-management](../microservices/svc-trail-management.md) | HTTPS |
| [svc-trip-catalog](../microservices/svc-trip-catalog.md) | HTTPS |
| [svc-weather](../microservices/svc-weather.md) | HTTPS |

### Product Catalog

**[svc-trail-management](../microservices/svc-trail-management.md)** calls:

| Target Service | Protocol |
|----------------|----------|
| [svc-location-services](../microservices/svc-location-services.md) | HTTPS |
| [svc-notifications](../microservices/svc-notifications.md) | Kafka |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | HTTPS |
| [svc-weather](../microservices/svc-weather.md) | HTTPS |

**[svc-trip-catalog](../microservices/svc-trip-catalog.md)** — No outbound service dependencies

### Safety

**[svc-emergency-response](../microservices/svc-emergency-response.md)** calls:

| Target Service | Protocol |
|----------------|----------|
| [svc-analytics](../microservices/svc-analytics.md) | Kafka |
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | HTTPS |
| [svc-guide-management](../microservices/svc-guide-management.md) | HTTPS |
| [svc-location-services](../microservices/svc-location-services.md) | HTTPS |
| [svc-notifications](../microservices/svc-notifications.md) | Kafka |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Kafka |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | Kafka |

**[svc-safety-compliance](../microservices/svc-safety-compliance.md)** calls:

| Target Service | Protocol |
|----------------|----------|
| [svc-analytics](../microservices/svc-analytics.md) | Kafka |
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | HTTPS |
| [svc-guide-management](../microservices/svc-guide-management.md) | HTTPS |
| [svc-notifications](../microservices/svc-notifications.md) | Kafka |

**[svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md)** calls:

| Target Service | Protocol |
|----------------|----------|
| [svc-analytics](../microservices/svc-analytics.md) | Kafka |
| [svc-notifications](../microservices/svc-notifications.md) | Kafka |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Kafka |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | HTTPS, Kafka |
| [svc-trail-management](../microservices/svc-trail-management.md) | HTTPS, Kafka |
| [svc-weather](../microservices/svc-weather.md) | HTTPS |

### Support

**[svc-analytics](../microservices/svc-analytics.md)** — No outbound service dependencies

**[svc-inventory-procurement](../microservices/svc-inventory-procurement.md)** calls:

| Target Service | Protocol |
|----------------|----------|
| [svc-gear-inventory](../microservices/svc-gear-inventory.md) | HTTPS |
| [svc-notifications](../microservices/svc-notifications.md) | Kafka |
| [svc-payments](../microservices/svc-payments.md) | HTTPS |

**[svc-location-services](../microservices/svc-location-services.md)** — No outbound service dependencies

**[svc-loyalty-rewards](../microservices/svc-loyalty-rewards.md)** calls:

| Target Service | Protocol |
|----------------|----------|
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | HTTPS |
| [svc-notifications](../microservices/svc-notifications.md) | Kafka |
| [svc-payments](../microservices/svc-payments.md) | HTTPS |
| [svc-reservations](../microservices/svc-reservations.md) | HTTPS |

**[svc-media-gallery](../microservices/svc-media-gallery.md)** calls:

| Target Service | Protocol |
|----------------|----------|
| [svc-notifications](../microservices/svc-notifications.md) | Kafka |

**[svc-notifications](../microservices/svc-notifications.md)** — No outbound service dependencies

**[svc-payments](../microservices/svc-payments.md)** calls:

| Target Service | Protocol |
|----------------|----------|
| [svc-notifications](../microservices/svc-notifications.md) | Kafka |
| [svc-reservations](../microservices/svc-reservations.md) | Kafka |

**[svc-reviews](../microservices/svc-reviews.md)** calls:

| Target Service | Protocol |
|----------------|----------|
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | HTTPS |
| [svc-reservations](../microservices/svc-reservations.md) | HTTPS |

**[svc-weather](../microservices/svc-weather.md)** calls:

| Target Service | Protocol |
|----------------|----------|
| [svc-notifications](../microservices/svc-notifications.md) | Kafka |

---

## Coupling Analysis

### Highest Fan-In (Most Depended Upon)

Services with the most inbound dependencies — changes to these services have the widest blast radius.

| Service | Inbound Dependencies | Domain |
|---------|---------------------|--------|
| [svc-notifications](../microservices/svc-notifications.md) | 14 | Support |
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | 8 | Guest Identity |
| [svc-reservations](../microservices/svc-reservations.md) | 8 | Booking |
| [svc-analytics](../microservices/svc-analytics.md) | 7 | Support |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | 5 | Safety |
| [svc-trip-catalog](../microservices/svc-trip-catalog.md) | 4 | Product Catalog |
| [svc-payments](../microservices/svc-payments.md) | 4 | Support |
| [svc-location-services](../microservices/svc-location-services.md) | 4 | Support |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | 3 | Operations |
| [svc-guide-management](../microservices/svc-guide-management.md) | 3 | Guide Management |

### Highest Fan-Out (Most Dependencies)

Services with the most outbound calls — these services are most affected by changes elsewhere.

| Service | Outbound Dependencies | Domain |
|---------|----------------------|--------|
| [svc-check-in](../microservices/svc-check-in.md) | 7 | Operations |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | 7 | Operations |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | 7 | Safety |
| [svc-reservations](../microservices/svc-reservations.md) | 6 | Booking |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | 6 | Safety |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | 5 | External |
| [svc-trail-management](../microservices/svc-trail-management.md) | 4 | Product Catalog |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | 4 | Safety |
| [svc-loyalty-rewards](../microservices/svc-loyalty-rewards.md) | 4 | Support |
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | 3 | Guest Identity |

---

## Data Source

Generated from `architecture/calm/novatrek-topology.json` by `portal/scripts/generate-topology-pages.py`.
