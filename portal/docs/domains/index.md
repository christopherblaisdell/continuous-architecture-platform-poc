# Domains

The NovaTrek Adventures platform is decomposed into **9 bounded contexts** (domains), each owning a set of microservices with clearly defined data ownership boundaries.

Click any domain to view its comprehensive detail page including services, data stores, integrations, events, decisions, and capabilities.

## System Overview

<div class="diagram-wrap">
  <a href="../topology/svg/topology-domain-overview.svg" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>
  <object data="../topology/svg/topology-domain-overview.svg" type="image/svg+xml" style="max-width: 100%;">
    NovaTrek Domain Overview C4 Diagram
  </object>
</div>

---

## Domain Gallery

Each domain's service topology. Click a diagram to explore the domain in detail.

<div style="border: 2px solid #2563eb; border-radius: 8px; margin-bottom: 1.5em; overflow: hidden;">
  <div style="background: #2563eb; color: white; padding: 0.6em 1em; display: flex; justify-content: space-between; align-items: center;">
    <strong style="font-size: 1.2em;"><a href="operations" style="color: white; text-decoration: none;">Operations</a></strong>
    <span style="font-size: 0.85em; opacity: 0.9;">NovaTrek Operations Team</span>
  </div>
  <div style="padding: 0.8em 1em 0.4em;">
    <p style="margin: 0 0 0.5em; font-size: 0.9em; color: #555;">Day-of-adventure workflows including guest check-in, schedule management, and real-time operational coordination. This domain orchestrates the core guest experience on the day of their adventure.</p>
    <p style="margin: 0 0 0.5em; font-size: 0.85em;">
      <strong>2</strong> services &nbsp;|&nbsp; 
      <strong>2</strong> events produced &nbsp;|&nbsp; 
      <strong>3</strong> events consumed &nbsp;|&nbsp; 
      <strong>2</strong> capabilities
    </p>
  </div>
  <div style="padding: 0 1em 1em;">
    <object data="../topology/svg/topology-operations.svg" type="image/svg+xml" style="max-width: 100%;">
      Operations Service Topology
    </object>
  </div>
</div>

<div style="border: 2px solid #7c3aed; border-radius: 8px; margin-bottom: 1.5em; overflow: hidden;">
  <div style="background: #7c3aed; color: white; padding: 0.6em 1em; display: flex; justify-content: space-between; align-items: center;">
    <strong style="font-size: 1.2em;"><a href="guest-identity" style="color: white; text-decoration: none;">Guest Identity</a></strong>
    <span style="font-size: 0.85em; opacity: 0.9;">Guest Experience Team</span>
  </div>
  <div style="padding: 0.8em 1em 0.4em;">
    <p style="margin: 0 0 0.5em; font-size: 0.9em; color: #555;">Guest identity resolution, profile management, certifications, and medical information. The single source of truth for all guest identity data across the platform.</p>
    <p style="margin: 0 0 0.5em; font-size: 0.85em;">
      <strong>1</strong> services &nbsp;|&nbsp; 
      <strong>1</strong> events produced &nbsp;|&nbsp; 
      <strong>0</strong> events consumed &nbsp;|&nbsp; 
      <strong>1</strong> capabilities
    </p>
  </div>
  <div style="padding: 0 1em 1em;">
    <object data="../topology/svg/topology-guest-identity.svg" type="image/svg+xml" style="max-width: 100%;">
      Guest Identity Service Topology
    </object>
  </div>
</div>

<div style="border: 2px solid #059669; border-radius: 8px; margin-bottom: 1.5em; overflow: hidden;">
  <div style="background: #059669; color: white; padding: 0.6em 1em; display: flex; justify-content: space-between; align-items: center;">
    <strong style="font-size: 1.2em;"><a href="booking" style="color: white; text-decoration: none;">Booking</a></strong>
    <span style="font-size: 0.85em; opacity: 0.9;">Booking Platform Team</span>
  </div>
  <div style="padding: 0.8em 1em 0.4em;">
    <p style="margin: 0 0 0.5em; font-size: 0.9em; color: #555;">Reservation lifecycle management from creation through completion, including participant management, insurance add-ons, and status tracking.</p>
    <p style="margin: 0 0 0.5em; font-size: 0.85em;">
      <strong>1</strong> services &nbsp;|&nbsp; 
      <strong>2</strong> events produced &nbsp;|&nbsp; 
      <strong>1</strong> events consumed &nbsp;|&nbsp; 
      <strong>1</strong> capabilities
    </p>
  </div>
  <div style="padding: 0 1em 1em;">
    <object data="../topology/svg/topology-booking.svg" type="image/svg+xml" style="max-width: 100%;">
      Booking Service Topology
    </object>
  </div>
</div>

<div style="border: 2px solid #d97706; border-radius: 8px; margin-bottom: 1.5em; overflow: hidden;">
  <div style="background: #d97706; color: white; padding: 0.6em 1em; display: flex; justify-content: space-between; align-items: center;">
    <strong style="font-size: 1.2em;"><a href="product-catalog" style="color: white; text-decoration: none;">Product Catalog</a></strong>
    <span style="font-size: 0.85em; opacity: 0.9;">Product Team</span>
  </div>
  <div style="padding: 0.8em 1em 0.4em;">
    <p style="margin: 0 0 0.5em; font-size: 0.9em; color: #555;">Adventure products, trip definitions, trail data, and the classification system that drives check-in UI patterns and safety workflows.</p>
    <p style="margin: 0 0 0.5em; font-size: 0.85em;">
      <strong>2</strong> services &nbsp;|&nbsp; 
      <strong>0</strong> events produced &nbsp;|&nbsp; 
      <strong>1</strong> events consumed &nbsp;|&nbsp; 
      <strong>4</strong> capabilities
    </p>
  </div>
  <div style="padding: 0 1em 1em;">
    <object data="../topology/svg/topology-product-catalog.svg" type="image/svg+xml" style="max-width: 100%;">
      Product Catalog Service Topology
    </object>
  </div>
</div>

<div style="border: 2px solid #dc2626; border-radius: 8px; margin-bottom: 1.5em; overflow: hidden;">
  <div style="background: #dc2626; color: white; padding: 0.6em 1em; display: flex; justify-content: space-between; align-items: center;">
    <strong style="font-size: 1.2em;"><a href="safety" style="color: white; text-decoration: none;">Safety</a></strong>
    <span style="font-size: 0.85em; opacity: 0.9;">Safety and Compliance Team</span>
  </div>
  <div style="padding: 0.8em 1em 0.4em;">
    <p style="margin: 0 0 0.5em; font-size: 0.9em; color: #555;">Guest and staff safety including waiver management, incident reporting, emergency response coordination, and wildlife/environmental monitoring.</p>
    <p style="margin: 0 0 0.5em; font-size: 0.85em;">
      <strong>3</strong> services &nbsp;|&nbsp; 
      <strong>3</strong> events produced &nbsp;|&nbsp; 
      <strong>1</strong> events consumed &nbsp;|&nbsp; 
      <strong>4</strong> capabilities
    </p>
  </div>
  <div style="padding: 0 1em 1em;">
    <object data="../topology/svg/topology-safety.svg" type="image/svg+xml" style="max-width: 100%;">
      Safety Service Topology
    </object>
  </div>
</div>

<div style="border: 2px solid #0891b2; border-radius: 8px; margin-bottom: 1.5em; overflow: hidden;">
  <div style="background: #0891b2; color: white; padding: 0.6em 1em; display: flex; justify-content: space-between; align-items: center;">
    <strong style="font-size: 1.2em;"><a href="logistics" style="color: white; text-decoration: none;">Logistics</a></strong>
    <span style="font-size: 0.85em; opacity: 0.9;">Logistics Team</span>
  </div>
  <div style="padding: 0.8em 1em 0.4em;">
    <p style="margin: 0 0 0.5em; font-size: 0.9em; color: #555;">Physical asset management covering gear inventory, equipment tracking, transport coordination, and vehicle dispatch.</p>
    <p style="margin: 0 0 0.5em; font-size: 0.85em;">
      <strong>2</strong> services &nbsp;|&nbsp; 
      <strong>0</strong> events produced &nbsp;|&nbsp; 
      <strong>0</strong> events consumed &nbsp;|&nbsp; 
      <strong>3</strong> capabilities
    </p>
  </div>
  <div style="padding: 0 1em 1em;">
    <object data="../topology/svg/topology-logistics.svg" type="image/svg+xml" style="max-width: 100%;">
      Logistics Service Topology
    </object>
  </div>
</div>

<div style="border: 2px solid #4f46e5; border-radius: 8px; margin-bottom: 1.5em; overflow: hidden;">
  <div style="background: #4f46e5; color: white; padding: 0.6em 1em; display: flex; justify-content: space-between; align-items: center;">
    <strong style="font-size: 1.2em;"><a href="guide-management" style="color: white; text-decoration: none;">Guide Management</a></strong>
    <span style="font-size: 0.85em; opacity: 0.9;">Guide Operations Team</span>
  </div>
  <div style="padding: 0.8em 1em 0.4em;">
    <p style="margin: 0 0 0.5em; font-size: 0.9em; color: #555;">Guide assignment, certification tracking, availability management, and preference handling for adventure staffing.</p>
    <p style="margin: 0 0 0.5em; font-size: 0.85em;">
      <strong>1</strong> services &nbsp;|&nbsp; 
      <strong>0</strong> events produced &nbsp;|&nbsp; 
      <strong>1</strong> events consumed &nbsp;|&nbsp; 
      <strong>1</strong> capabilities
    </p>
  </div>
  <div style="padding: 0 1em 1em;">
    <object data="../topology/svg/topology-guide-management.svg" type="image/svg+xml" style="max-width: 100%;">
      Guide Management Service Topology
    </object>
  </div>
</div>

<div style="border: 2px solid #9333ea; border-radius: 8px; margin-bottom: 1.5em; overflow: hidden;">
  <div style="background: #9333ea; color: white; padding: 0.6em 1em; display: flex; justify-content: space-between; align-items: center;">
    <strong style="font-size: 1.2em;"><a href="external" style="color: white; text-decoration: none;">External</a></strong>
    <span style="font-size: 0.85em; opacity: 0.9;">Integration Team</span>
  </div>
  <div style="padding: 0.8em 1em 0.4em;">
    <p style="margin: 0 0 0.5em; font-size: 0.9em; color: #555;">Third-party booking channel integrations, partner API gateway, and external system connectivity.</p>
    <p style="margin: 0 0 0.5em; font-size: 0.85em;">
      <strong>1</strong> services &nbsp;|&nbsp; 
      <strong>0</strong> events produced &nbsp;|&nbsp; 
      <strong>0</strong> events consumed &nbsp;|&nbsp; 
      <strong>2</strong> capabilities
    </p>
  </div>
  <div style="padding: 0 1em 1em;">
    <object data="../topology/svg/topology-external.svg" type="image/svg+xml" style="max-width: 100%;">
      External Service Topology
    </object>
  </div>
</div>

<div style="border: 2px solid #64748b; border-radius: 8px; margin-bottom: 1.5em; overflow: hidden;">
  <div style="background: #64748b; color: white; padding: 0.6em 1em; display: flex; justify-content: space-between; align-items: center;">
    <strong style="font-size: 1.2em;"><a href="support" style="color: white; text-decoration: none;">Support</a></strong>
    <span style="font-size: 0.85em; opacity: 0.9;">Various (cross-cutting platform services)</span>
  </div>
  <div style="padding: 0.8em 1em 0.4em;">
    <p style="margin: 0 0 0.5em; font-size: 0.9em; color: #555;">Cross-cutting platform services including notifications, payments, loyalty rewards, analytics, weather, location services, media gallery, procurement, and reviews.</p>
    <p style="margin: 0 0 0.5em; font-size: 0.85em;">
      <strong>9</strong> services &nbsp;|&nbsp; 
      <strong>1</strong> events produced &nbsp;|&nbsp; 
      <strong>15</strong> events consumed &nbsp;|&nbsp; 
      <strong>13</strong> capabilities
    </p>
  </div>
  <div style="padding: 0 1em 1em;">
    <object data="../topology/svg/topology-support.svg" type="image/svg+xml" style="max-width: 100%;">
      Support Service Topology
    </object>
  </div>
</div>


---

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
