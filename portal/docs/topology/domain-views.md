# Domain Views

Per-domain topology breakdown showing services, databases, and integration patterns for each bounded context.

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
| [svc-reservations](../microservices/svc-reservations.md) | 10 | PostgreSQL 15 | 3 | 7 | 3 | 1 |

### Cross-Domain Integration

**Outbound (this domain calls):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-reservations](../microservices/svc-reservations.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Validate guest identity |
| [svc-reservations](../microservices/svc-reservations.md) | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | Check trip availability |
| [svc-reservations](../microservices/svc-reservations.md) | [svc-payments](../microservices/svc-payments.md) | Process deposit payment |

**Inbound (called by other domains):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-check-in](../microservices/svc-check-in.md) | [svc-reservations](../microservices/svc-reservations.md) | Verify reservation exists |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-reservations](../microservices/svc-reservations.md) | Create reservation |
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | [svc-reservations](../microservices/svc-reservations.md) | Query past bookings |
| [svc-gear-inventory](../microservices/svc-gear-inventory.md) | [svc-reservations](../microservices/svc-reservations.md) | Verify booking |
| [svc-transport-logistics](../microservices/svc-transport-logistics.md) | [svc-reservations](../microservices/svc-reservations.md) | Get booking details |
| [svc-loyalty-rewards](../microservices/svc-loyalty-rewards.md) | [svc-reservations](../microservices/svc-reservations.md) | Verify completed booking |
| [svc-reviews](../microservices/svc-reviews.md) | [svc-reservations](../microservices/svc-reservations.md) | Validate reservation exists and is COMPLETED |

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
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | 7 | PostgreSQL 15 | 4 | 0 | 1 | 0 |

### Cross-Domain Integration

**Outbound (this domain calls):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Validate guest identity |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | Check trip availability |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-reservations](../microservices/svc-reservations.md) | Create reservation |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-payments](../microservices/svc-payments.md) | Process commission |

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
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | [svc-reservations](../microservices/svc-reservations.md) | Query past bookings |
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | [svc-analytics](../microservices/svc-analytics.md) | Get satisfaction scores |

**Inbound (called by other domains):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-check-in](../microservices/svc-check-in.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Validate guest identity |
| [svc-reservations](../microservices/svc-reservations.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Validate guest identity |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Validate guest identity |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Validate guest identity |
| [svc-gear-inventory](../microservices/svc-gear-inventory.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Validate guest |
| [svc-loyalty-rewards](../microservices/svc-loyalty-rewards.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Get member profile |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Retrieve guest medical info and emergency contacts |
| [svc-reviews](../microservices/svc-reviews.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Validate guest identity |

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
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-guide-management](../microservices/svc-guide-management.md) | Check guide availability |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | [svc-guide-management](../microservices/svc-guide-management.md) | Get assigned guide |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | [svc-guide-management](../microservices/svc-guide-management.md) | Identify nearest on-duty guide |

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
| [svc-transport-logistics](../microservices/svc-transport-logistics.md) | 7 | PostgreSQL 15 | 2 | 0 | 1 | 0 |

### Cross-Domain Integration

**Outbound (this domain calls):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-gear-inventory](../microservices/svc-gear-inventory.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Validate guest |
| [svc-gear-inventory](../microservices/svc-gear-inventory.md) | [svc-reservations](../microservices/svc-reservations.md) | Verify booking |
| [svc-gear-inventory](../microservices/svc-gear-inventory.md) | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Check waiver status |
| [svc-transport-logistics](../microservices/svc-transport-logistics.md) | [svc-reservations](../microservices/svc-reservations.md) | Get booking details |
| [svc-transport-logistics](../microservices/svc-transport-logistics.md) | [svc-location-services](../microservices/svc-location-services.md) | Validate pickup location |

**Inbound (called by other domains):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-check-in](../microservices/svc-check-in.md) | [svc-gear-inventory](../microservices/svc-gear-inventory.md) | Verify gear assignment |
| [svc-inventory-procurement](../microservices/svc-inventory-procurement.md) | [svc-gear-inventory](../microservices/svc-gear-inventory.md) | Verify item catalog |

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
| [svc-check-in](../microservices/svc-check-in.md) | 6 | PostgreSQL 15 | 5 | 0 | 2 | 0 |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | 6 | PostgreSQL 15 + Valkey 8 | 5 | 1 | 3 | 3 |

### Cross-Domain Integration

**Outbound (this domain calls):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-check-in](../microservices/svc-check-in.md) | [svc-reservations](../microservices/svc-reservations.md) | Verify reservation exists |
| [svc-check-in](../microservices/svc-check-in.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Validate guest identity |
| [svc-check-in](../microservices/svc-check-in.md) | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | Get adventure category |
| [svc-check-in](../microservices/svc-check-in.md) | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Validate active waiver |
| [svc-check-in](../microservices/svc-check-in.md) | [svc-gear-inventory](../microservices/svc-gear-inventory.md) | Verify gear assignment |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-guide-management](../microservices/svc-guide-management.md) | Check guide availability |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-trail-management](../microservices/svc-trail-management.md) | Verify trail conditions |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-weather](../microservices/svc-weather.md) | Get forecast |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | Get trip details |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-location-services](../microservices/svc-location-services.md) | Check location capacity |

**Inbound (called by other domains):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | Check for affected scheduled trips |

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
| [svc-trail-management](../microservices/svc-trail-management.md) | 9 | PostGIS (PostgreSQL 15) | 3 | 2 | 1 | 1 |
| [svc-trip-catalog](../microservices/svc-trip-catalog.md) | 11 | PostgreSQL 15 | 0 | 4 | 0 | 0 |

### Cross-Domain Integration

**Outbound (this domain calls):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-trail-management](../microservices/svc-trail-management.md) | [svc-weather](../microservices/svc-weather.md) | Correlate weather data |
| [svc-trail-management](../microservices/svc-trail-management.md) | [svc-location-services](../microservices/svc-location-services.md) | Get trail coordinates |
| [svc-trail-management](../microservices/svc-trail-management.md) | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Update trail safety assessment |

**Inbound (called by other domains):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-trail-management](../microservices/svc-trail-management.md) | Verify trail conditions |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | [svc-trail-management](../microservices/svc-trail-management.md) | Identify nearest trails to sighting location |
| [svc-check-in](../microservices/svc-check-in.md) | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | Get adventure category |
| [svc-reservations](../microservices/svc-reservations.md) | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | Check trip availability |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | Get trip details |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | Check trip availability |

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
| [svc-emergency-response](../microservices/svc-emergency-response.md) | 11 | PostgreSQL 15 | 3 | 0 | 4 | 0 |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | 9 | PostgreSQL 15 | 2 | 3 | 2 | 2 |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | 11 | PostgreSQL 15 | 3 | 0 | 5 | 0 |

### Cross-Domain Integration

**Outbound (this domain calls):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-emergency-response](../microservices/svc-emergency-response.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Retrieve guest medical info and emergency contacts |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | [svc-location-services](../microservices/svc-location-services.md) | Get last known guest GPS position |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | [svc-guide-management](../microservices/svc-guide-management.md) | Identify nearest on-duty guide |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Validate guest identity |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | [svc-guide-management](../microservices/svc-guide-management.md) | Get assigned guide |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | [svc-trail-management](../microservices/svc-trail-management.md) | Identify nearest trails to sighting location |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | [svc-weather](../microservices/svc-weather.md) | Get current conditions at sighting location |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | Check for affected scheduled trips |

**Inbound (called by other domains):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-check-in](../microservices/svc-check-in.md) | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Validate active waiver |
| [svc-gear-inventory](../microservices/svc-gear-inventory.md) | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Check waiver status |
| [svc-trail-management](../microservices/svc-trail-management.md) | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Update trail safety assessment |

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
| [svc-analytics](../microservices/svc-analytics.md) | 6 | Oracle Database 19c | 0 | 1 | 0 | 7 |
| [svc-inventory-procurement](../microservices/svc-inventory-procurement.md) | 8 | PostgreSQL 15 | 2 | 0 | 1 | 0 |
| [svc-location-services](../microservices/svc-location-services.md) | 6 | PostGIS (PostgreSQL 15) | 0 | 4 | 0 | 0 |
| [svc-loyalty-rewards](../microservices/svc-loyalty-rewards.md) | 5 | Couchbase 7 | 3 | 0 | 1 | 1 |
| [svc-media-gallery](../microservices/svc-media-gallery.md) | 5 | PostgreSQL 15 + S3-Compatible Object Store | 0 | 0 | 1 | 0 |
| [svc-notifications](../microservices/svc-notifications.md) | 6 | PostgreSQL 15 + Valkey 8 | 0 | 0 | 0 | 14 |
| [svc-payments](../microservices/svc-payments.md) | 13 | PostgreSQL 15 | 0 | 4 | 2 | 0 |
| [svc-reviews](../microservices/svc-reviews.md) | 10 | PostgreSQL 15 | 2 | 0 | 0 | 0 |
| [svc-weather](../microservices/svc-weather.md) | 5 | Valkey 8 + PostgreSQL 15 | 0 | 3 | 1 | 0 |

### Cross-Domain Integration

**Outbound (this domain calls):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-inventory-procurement](../microservices/svc-inventory-procurement.md) | [svc-gear-inventory](../microservices/svc-gear-inventory.md) | Verify item catalog |
| [svc-loyalty-rewards](../microservices/svc-loyalty-rewards.md) | [svc-reservations](../microservices/svc-reservations.md) | Verify completed booking |
| [svc-loyalty-rewards](../microservices/svc-loyalty-rewards.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Get member profile |
| [svc-reviews](../microservices/svc-reviews.md) | [svc-reservations](../microservices/svc-reservations.md) | Validate reservation exists and is COMPLETED |
| [svc-reviews](../microservices/svc-reviews.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Validate guest identity |

**Inbound (called by other domains):**

| Source | Target | Action |
|--------|--------|--------|
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | [svc-analytics](../microservices/svc-analytics.md) | Get satisfaction scores |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-location-services](../microservices/svc-location-services.md) | Check location capacity |
| [svc-transport-logistics](../microservices/svc-transport-logistics.md) | [svc-location-services](../microservices/svc-location-services.md) | Validate pickup location |
| [svc-trail-management](../microservices/svc-trail-management.md) | [svc-location-services](../microservices/svc-location-services.md) | Get trail coordinates |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | [svc-location-services](../microservices/svc-location-services.md) | Get last known guest GPS position |
| [svc-reservations](../microservices/svc-reservations.md) | [svc-payments](../microservices/svc-payments.md) | Process deposit payment |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | [svc-payments](../microservices/svc-payments.md) | Process commission |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-weather](../microservices/svc-weather.md) | Get forecast |
| [svc-trail-management](../microservices/svc-trail-management.md) | [svc-weather](../microservices/svc-weather.md) | Correlate weather data |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | [svc-weather](../microservices/svc-weather.md) | Get current conditions at sighting location |

---

## Data Source

Generated from `architecture/calm/novatrek-topology.json` by `portal/scripts/generate-topology-pages.py`.
