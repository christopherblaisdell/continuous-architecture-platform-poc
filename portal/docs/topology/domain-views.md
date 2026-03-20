# Domain Views

Per-domain topology breakdown showing services, databases, and integration patterns for each bounded context.

!!! info "Everything on this portal is entirely fictional"
    NovaTrek Adventures is a completely fictitious company used as a synthetic workspace for the Continuous Architecture Platform proof of concept.

---

## Booking

**Team:** Booking Platform Team

### Topology

<div class="diagram-wrap">
  <a href="../svg/topology-booking.svg" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>
  <object data="../svg/topology-booking.svg" type="image/svg+xml" style="max-width: 100%;">
    Booking Service Topology C4 Diagram
  </object>
</div>

### Services

| Service | Interfaces | Database | REST Out | REST In | Events Out | Events In |
|---------|------------|----------|----------|---------|------------|----------|
| [svc-reservations](../microservices/svc-reservations.md) | 10 | PostgreSQL 15 | 4 | 7 | 3 | 1 |

### Cross-Domain Integration

**Outbound (this domain calls):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-reservations](../microservices/svc-reservations.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | — |
| [svc-reservations](../microservices/svc-reservations.md) | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | — |
| [svc-reservations](../microservices/svc-reservations.md) | [svc-payments](../microservices/svc-payments.md) | — |
| [svc-reservations](../microservices/svc-reservations.md) | [svc-notifications](../microservices/svc-notifications.md) | — |

**Inbound (called by other domains):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-check-in](../microservices/svc-check-in.md) | [svc-reservations](../microservices/svc-reservations.md) | — |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-reservations](../microservices/svc-reservations.md) | — |
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | [svc-reservations](../microservices/svc-reservations.md) | — |
| [svc-gear-inventory](../microservices/svc-gear-inventory.md) | [svc-reservations](../microservices/svc-reservations.md) | — |
| [svc-transport-logistics](../microservices/svc-transport-logistics.md) | [svc-reservations](../microservices/svc-reservations.md) | — |
| [svc-loyalty-rewards](../microservices/svc-loyalty-rewards.md) | [svc-reservations](../microservices/svc-reservations.md) | — |
| [svc-reviews](../microservices/svc-reviews.md) | [svc-reservations](../microservices/svc-reservations.md) | — |

---

## External

**Team:** Integration Team

### Topology

<div class="diagram-wrap">
  <a href="../svg/topology-external.svg" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>
  <object data="../svg/topology-external.svg" type="image/svg+xml" style="max-width: 100%;">
    External Service Topology C4 Diagram
  </object>
</div>

### Services

| Service | Interfaces | Database | REST Out | REST In | Events Out | Events In |
|---------|------------|----------|----------|---------|------------|----------|
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | 7 | PostgreSQL 15 | 5 | 0 | 0 | 0 |

### Cross-Domain Integration

**Outbound (this domain calls):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | — |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | — |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-reservations](../microservices/svc-reservations.md) | — |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-payments](../microservices/svc-payments.md) | — |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-notifications](../microservices/svc-notifications.md) | — |

---

## Guest Identity

**Team:** Guest Experience Team

### Topology

<div class="diagram-wrap">
  <a href="../svg/topology-guest-identity.svg" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>
  <object data="../svg/topology-guest-identity.svg" type="image/svg+xml" style="max-width: 100%;">
    Guest Identity Service Topology C4 Diagram
  </object>
</div>

### Services

| Service | Interfaces | Database | REST Out | REST In | Events Out | Events In |
|---------|------------|----------|----------|---------|------------|----------|
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | 10 | PostgreSQL 15 | 2 | 8 | 2 | 0 |

### Cross-Domain Integration

**Outbound (this domain calls):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | [svc-reservations](../microservices/svc-reservations.md) | — |
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | [svc-analytics](../microservices/svc-analytics.md) | — |

**Inbound (called by other domains):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-check-in](../microservices/svc-check-in.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | — |
| [svc-reservations](../microservices/svc-reservations.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | — |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | — |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | — |
| [svc-gear-inventory](../microservices/svc-gear-inventory.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | — |
| [svc-loyalty-rewards](../microservices/svc-loyalty-rewards.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | — |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | — |
| [svc-reviews](../microservices/svc-reviews.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | — |

---

## Guide Management

**Team:** Guide Operations Team

### Topology

<div class="diagram-wrap">
  <a href="../svg/topology-guide-management.svg" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>
  <object data="../svg/topology-guide-management.svg" type="image/svg+xml" style="max-width: 100%;">
    Guide Management Service Topology C4 Diagram
  </object>
</div>

### Services

| Service | Interfaces | Database | REST Out | REST In | Events Out | Events In |
|---------|------------|----------|----------|---------|------------|----------|
| [svc-guide-management](../microservices/svc-guide-management.md) | 12 | PostgreSQL 15 | 0 | 3 | 0 | 1 |

### Cross-Domain Integration

**Inbound (called by other domains):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-guide-management](../microservices/svc-guide-management.md) | — |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | [svc-guide-management](../microservices/svc-guide-management.md) | — |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | [svc-guide-management](../microservices/svc-guide-management.md) | — |

---

## Logistics

**Team:** Logistics Team

### Topology

<div class="diagram-wrap">
  <a href="../svg/topology-logistics.svg" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>
  <object data="../svg/topology-logistics.svg" type="image/svg+xml" style="max-width: 100%;">
    Logistics Service Topology C4 Diagram
  </object>
</div>

### Services

| Service | Interfaces | Database | REST Out | REST In | Events Out | Events In |
|---------|------------|----------|----------|---------|------------|----------|
| [svc-gear-inventory](../microservices/svc-gear-inventory.md) | 12 | PostgreSQL 15 | 3 | 2 | 0 | 0 |
| [svc-transport-logistics](../microservices/svc-transport-logistics.md) | 7 | PostgreSQL 15 | 3 | 0 | 0 | 0 |

### Cross-Domain Integration

**Outbound (this domain calls):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-gear-inventory](../microservices/svc-gear-inventory.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | — |
| [svc-gear-inventory](../microservices/svc-gear-inventory.md) | [svc-reservations](../microservices/svc-reservations.md) | — |
| [svc-gear-inventory](../microservices/svc-gear-inventory.md) | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | — |
| [svc-transport-logistics](../microservices/svc-transport-logistics.md) | [svc-reservations](../microservices/svc-reservations.md) | — |
| [svc-transport-logistics](../microservices/svc-transport-logistics.md) | [svc-location-services](../microservices/svc-location-services.md) | — |
| [svc-transport-logistics](../microservices/svc-transport-logistics.md) | [svc-notifications](../microservices/svc-notifications.md) | — |

**Inbound (called by other domains):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-check-in](../microservices/svc-check-in.md) | [svc-gear-inventory](../microservices/svc-gear-inventory.md) | — |
| [svc-inventory-procurement](../microservices/svc-inventory-procurement.md) | [svc-gear-inventory](../microservices/svc-gear-inventory.md) | — |

---

## Operations

**Team:** NovaTrek Operations Team

### Topology

<div class="diagram-wrap">
  <a href="../svg/topology-operations.svg" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>
  <object data="../svg/topology-operations.svg" type="image/svg+xml" style="max-width: 100%;">
    Operations Service Topology C4 Diagram
  </object>
</div>

### Services

| Service | Interfaces | Database | REST Out | REST In | Events Out | Events In |
|---------|------------|----------|----------|---------|------------|----------|
| [svc-check-in](../microservices/svc-check-in.md) | 6 | PostgreSQL 15 | 6 | 0 | 2 | 0 |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | 6 | PostgreSQL 15 + Valkey 8 | 7 | 1 | 2 | 3 |

### Cross-Domain Integration

**Outbound (this domain calls):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-check-in](../microservices/svc-check-in.md) | [svc-reservations](../microservices/svc-reservations.md) | — |
| [svc-check-in](../microservices/svc-check-in.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | — |
| [svc-check-in](../microservices/svc-check-in.md) | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | — |
| [svc-check-in](../microservices/svc-check-in.md) | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | — |
| [svc-check-in](../microservices/svc-check-in.md) | [svc-notifications](../microservices/svc-notifications.md) | — |
| [svc-check-in](../microservices/svc-check-in.md) | [svc-gear-inventory](../microservices/svc-gear-inventory.md) | — |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-guide-management](../microservices/svc-guide-management.md) | — |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-trail-management](../microservices/svc-trail-management.md) | — |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-weather](../microservices/svc-weather.md) | — |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | — |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-notifications](../microservices/svc-notifications.md) | — |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-location-services](../microservices/svc-location-services.md) | — |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-analytics](../microservices/svc-analytics.md) | — |

**Inbound (called by other domains):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | — |

---

## Product Catalog

**Team:** Product Team

### Topology

<div class="diagram-wrap">
  <a href="../svg/topology-product-catalog.svg" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>
  <object data="../svg/topology-product-catalog.svg" type="image/svg+xml" style="max-width: 100%;">
    Product Catalog Service Topology C4 Diagram
  </object>
</div>

### Services

| Service | Interfaces | Database | REST Out | REST In | Events Out | Events In |
|---------|------------|----------|----------|---------|------------|----------|
| [svc-trail-management](../microservices/svc-trail-management.md) | 9 | PostGIS (PostgreSQL 15) | 4 | 2 | 0 | 1 |
| [svc-trip-catalog](../microservices/svc-trip-catalog.md) | 11 | PostgreSQL 15 | 0 | 4 | 0 | 0 |

### Cross-Domain Integration

**Outbound (this domain calls):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-trail-management](../microservices/svc-trail-management.md) | [svc-weather](../microservices/svc-weather.md) | — |
| [svc-trail-management](../microservices/svc-trail-management.md) | [svc-location-services](../microservices/svc-location-services.md) | — |
| [svc-trail-management](../microservices/svc-trail-management.md) | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | — |
| [svc-trail-management](../microservices/svc-trail-management.md) | [svc-notifications](../microservices/svc-notifications.md) | — |

**Inbound (called by other domains):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-trail-management](../microservices/svc-trail-management.md) | — |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | [svc-trail-management](../microservices/svc-trail-management.md) | — |
| [svc-check-in](../microservices/svc-check-in.md) | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | — |
| [svc-reservations](../microservices/svc-reservations.md) | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | — |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | — |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | — |

---

## Safety

**Team:** Safety and Compliance Team

### Topology

<div class="diagram-wrap">
  <a href="../svg/topology-safety.svg" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>
  <object data="../svg/topology-safety.svg" type="image/svg+xml" style="max-width: 100%;">
    Safety Service Topology C4 Diagram
  </object>
</div>

### Services

| Service | Interfaces | Database | REST Out | REST In | Events Out | Events In |
|---------|------------|----------|----------|---------|------------|----------|
| [svc-emergency-response](../microservices/svc-emergency-response.md) | 11 | PostgreSQL 15 | 5 | 0 | 4 | 0 |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | 9 | PostgreSQL 15 | 3 | 5 | 2 | 1 |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | 11 | PostgreSQL 15 | 5 | 0 | 4 | 0 |

### Cross-Domain Integration

**Outbound (this domain calls):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-emergency-response](../microservices/svc-emergency-response.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | — |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | [svc-location-services](../microservices/svc-location-services.md) | — |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | [svc-guide-management](../microservices/svc-guide-management.md) | — |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | [svc-notifications](../microservices/svc-notifications.md) | — |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | — |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | [svc-notifications](../microservices/svc-notifications.md) | — |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | [svc-guide-management](../microservices/svc-guide-management.md) | — |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | [svc-trail-management](../microservices/svc-trail-management.md) | — |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | [svc-weather](../microservices/svc-weather.md) | — |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | [svc-notifications](../microservices/svc-notifications.md) | — |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | — |

**Inbound (called by other domains):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-check-in](../microservices/svc-check-in.md) | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | — |
| [svc-gear-inventory](../microservices/svc-gear-inventory.md) | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | — |
| [svc-trail-management](../microservices/svc-trail-management.md) | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | — |

---

## Support

**Team:** Support Services Team

### Topology

<div class="diagram-wrap">
  <a href="../svg/topology-support.svg" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>
  <object data="../svg/topology-support.svg" type="image/svg+xml" style="max-width: 100%;">
    Support Service Topology C4 Diagram
  </object>
</div>

### Services

| Service | Interfaces | Database | REST Out | REST In | Events Out | Events In |
|---------|------------|----------|----------|---------|------------|----------|
| [svc-analytics](../microservices/svc-analytics.md) | 6 | Oracle Database 19c | 0 | 2 | 0 | 6 |
| [svc-inventory-procurement](../microservices/svc-inventory-procurement.md) | 8 | PostgreSQL 15 | 3 | 0 | 0 | 0 |
| [svc-location-services](../microservices/svc-location-services.md) | 6 | PostGIS (PostgreSQL 15) | 0 | 4 | 0 | 0 |
| [svc-loyalty-rewards](../microservices/svc-loyalty-rewards.md) | 5 | Couchbase 7 | 4 | 0 | 0 | 1 |
| [svc-media-gallery](../microservices/svc-media-gallery.md) | 5 | PostgreSQL 15 + S3-Compatible Object Store | 1 | 0 | 0 | 0 |
| [svc-notifications](../microservices/svc-notifications.md) | 6 | PostgreSQL 15 + Valkey 8 | 0 | 14 | 0 | 7 |
| [svc-payments](../microservices/svc-payments.md) | 13 | PostgreSQL 15 | 1 | 4 | 2 | 0 |
| [svc-reviews](../microservices/svc-reviews.md) | 10 | PostgreSQL 15 | 2 | 0 | 0 | 0 |
| [svc-weather](../microservices/svc-weather.md) | 5 | Valkey 8 + PostgreSQL 15 | 1 | 3 | 0 | 0 |

### Cross-Domain Integration

**Outbound (this domain calls):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-inventory-procurement](../microservices/svc-inventory-procurement.md) | [svc-gear-inventory](../microservices/svc-gear-inventory.md) | — |
| [svc-loyalty-rewards](../microservices/svc-loyalty-rewards.md) | [svc-reservations](../microservices/svc-reservations.md) | — |
| [svc-loyalty-rewards](../microservices/svc-loyalty-rewards.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | — |
| [svc-reviews](../microservices/svc-reviews.md) | [svc-reservations](../microservices/svc-reservations.md) | — |
| [svc-reviews](../microservices/svc-reviews.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | — |

**Inbound (called by other domains):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-analytics](../microservices/svc-analytics.md) | — |
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | [svc-analytics](../microservices/svc-analytics.md) | — |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-location-services](../microservices/svc-location-services.md) | — |
| [svc-transport-logistics](../microservices/svc-transport-logistics.md) | [svc-location-services](../microservices/svc-location-services.md) | — |
| [svc-trail-management](../microservices/svc-trail-management.md) | [svc-location-services](../microservices/svc-location-services.md) | — |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | [svc-location-services](../microservices/svc-location-services.md) | — |
| [svc-check-in](../microservices/svc-check-in.md) | [svc-notifications](../microservices/svc-notifications.md) | — |
| [svc-reservations](../microservices/svc-reservations.md) | [svc-notifications](../microservices/svc-notifications.md) | — |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-notifications](../microservices/svc-notifications.md) | — |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-notifications](../microservices/svc-notifications.md) | — |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | [svc-notifications](../microservices/svc-notifications.md) | — |
| [svc-transport-logistics](../microservices/svc-transport-logistics.md) | [svc-notifications](../microservices/svc-notifications.md) | — |
| [svc-trail-management](../microservices/svc-trail-management.md) | [svc-notifications](../microservices/svc-notifications.md) | — |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | [svc-notifications](../microservices/svc-notifications.md) | — |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | [svc-notifications](../microservices/svc-notifications.md) | — |
| [svc-reservations](../microservices/svc-reservations.md) | [svc-payments](../microservices/svc-payments.md) | — |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-payments](../microservices/svc-payments.md) | — |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-weather](../microservices/svc-weather.md) | — |
| [svc-trail-management](../microservices/svc-trail-management.md) | [svc-weather](../microservices/svc-weather.md) | — |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | [svc-weather](../microservices/svc-weather.md) | — |

---

## Data Source

Generated from `architecture/calm/novatrek-topology.json` by `portal/scripts/generate-topology-pages.py`.
