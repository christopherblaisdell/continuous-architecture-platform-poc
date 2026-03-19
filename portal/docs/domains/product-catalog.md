# Product Catalog Domain

**Team:** Product Team  
**Services:** 2  
**Domain color:** #d97706

Adventure products, trip definitions, trail data, and the classification system that drives check-in UI patterns and safety workflows.

---

## Topology

<div class="diagram-wrap">
  <a href="../../topology/svg/topology-product-catalog.svg" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>
  <object data="../../topology/svg/topology-product-catalog.svg" type="image/svg+xml" style="max-width: 100%;">
    Product Catalog Service Topology C4 Diagram
  </object>
</div>

---

## Services

| Service | Database Engine | Schema | Tables | API Endpoints |
|---------|----------------|--------|--------|---------------|
| [svc-trip-catalog](../microservices/svc-trip-catalog.md) | PostgreSQL 15 | `catalog` | 6 | 11 |
| [svc-trail-management](../microservices/svc-trail-management.md) | PostGIS (PostgreSQL 15) | `trails` | 4 | 9 |

---

## Data Ownership

Every data entity has exactly one owning service. Other services access it read-only through APIs.

| Data Entity | Owning Service | Read Access |
|-------------|---------------|-------------|
| Adventure catalog | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | svc-check-in, svc-reservations, svc-partner-integrations |
| Trail data | [svc-trail-management](../microservices/svc-trail-management.md) | svc-trip-catalog, svc-safety-compliance, svc-scheduling-orchestrator |

---

## Data Stores

### svc-trip-catalog

- **Engine:** PostgreSQL 15
- **Schema:** `catalog`
- **Tables:** `trips`, `trip_schedules`, `pricing_tiers`, `requirements`, `regions`, `activity_types`
- **Features:**
    - Full-text search index on trip name and description
    - Materialized view for availability calendar
    - JSONB columns for flexible requirement definitions
- **Volume:** ~50 catalog updates/day, ~10K availability reads/day
- **Backup:** Daily pg_dump, 14-day retention

### svc-trail-management

- **Engine:** PostGIS (PostgreSQL 15)
- **Schema:** `trails`
- **Tables:** `trails`, `waypoints`, `closures`, `condition_reports`
- **Features:**
    - PostGIS geometry columns for trail routes and waypoints
    - Spatial indexes (GiST) for proximity queries
    - Time-series condition data with hypertable extension
- **Volume:** ~200 condition updates/day, ~5K trail reads/day
- **Backup:** Daily pg_dump with PostGIS extensions, 14-day retention

---

## Bounded Context Rules

These rules are non-negotiable for this domain.

1. Adventure classification is **configuration-driven** via YAML — no hardcoded constants ([ADR-004](../decisions/ADR-004-configuration-driven-classification.md))
2. Trail elevation data may be null; all consumers must handle gracefully ([ADR-003](../decisions/ADR-003-nullable-elevation-fields.md))
3. Unknown adventure categories MUST default to **Pattern 3** (Full Service) for safety ([ADR-005](../decisions/ADR-005-pattern3-default-fallback.md))

---

## Cross-Domain Integration

### Outbound (this domain calls)

| Source | Target | Target Domain | Action | Async |
|--------|--------|--------------|--------|-------|
| [svc-trail-management](../microservices/svc-trail-management.md) | [svc-weather](../microservices/svc-weather.md) | Support | Correlate weather data | No |
| [svc-trail-management](../microservices/svc-trail-management.md) | [svc-location-services](../microservices/svc-location-services.md) | Support | Get trail coordinates | No |
| [svc-trail-management](../microservices/svc-trail-management.md) | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Safety | Update trail safety assessment | No |
| [svc-trail-management](../microservices/svc-trail-management.md) | [svc-notifications](../microservices/svc-notifications.md) | Support | Alert park rangers | Yes |
| [svc-trail-management](../microservices/svc-trail-management.md) | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Safety | Validate trail safety rating | No |

### Inbound (called by other domains)

| Source | Source Domain | Target | Action | Async |
|--------|-------------|--------|--------|-------|
| [svc-check-in](../microservices/svc-check-in.md) | Operations | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | Get adventure category | No |
| [svc-reservations](../microservices/svc-reservations.md) | Booking | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | Check trip availability | No |
| [svc-reservations](../microservices/svc-reservations.md) | Booking | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | Verify availability | No |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | Operations | [svc-trail-management](../microservices/svc-trail-management.md) | Verify trail conditions | No |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | Operations | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | Get trip details | No |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | Operations | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | Get trip requirements | No |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | External | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | Check trip availability | No |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | Safety | [svc-trail-management](../microservices/svc-trail-management.md) | Identify nearest trails to sighting location | No |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | Safety | [svc-trail-management](../microservices/svc-trail-management.md) | Recommend trail closure for affected corridors | No |

---

## Domain Events

### Events Consumed

| Event | Channel | Producer | Producer Domain | Consuming Service |
|-------|---------|----------|----------------|-------------------|
| `wildlife_alert.issued` | `novatrek.safety.wildlife-alert.issued` | [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | Safety | [svc-trail-management](../microservices/svc-trail-management.md) |

---

## Architecture Decisions

ADRs that directly constrain or shape this domain.

| ADR | Title |
|-----|-------|
| [ADR-003](../decisions/ADR-003-nullable-elevation-fields.md) | Nullable Elevation Fields |
| [ADR-004](../decisions/ADR-004-configuration-driven-classification.md) | Configuration-Driven Classification |

---

## Business Capabilities

Capabilities served by this domain's services.

| ID | Capability | Status | Description |
|----|-----------|--------|-------------|
| CAP-1.2 | Adventure Discovery and Browsing | IMPLEMENTED | Search, filter, and browse available adventures and trails |
| CAP-2.4 | Trail Operations | IMPLEMENTED | Trail condition monitoring, elevation data, difficulty classification |
| CAP-3.4 | Wildlife and Environmental Monitoring | IMPLEMENTED | Wildlife sighting reporting, trail closure triggers, environmental risk assessment |
| CAP-5.2 | Trip Pricing and Yield Management | PARTIAL | Dynamic pricing, seasonal rates, and demand-based yield optimization |

---

## Quick Links

- [Domain Topology View](../topology/domain-views.md#product-catalog)
- [svc-trip-catalog Microservice Page](../microservices/svc-trip-catalog.md)
- [svc-trail-management Microservice Page](../microservices/svc-trail-management.md)
- [Event Catalog](../events/index.md)
- [Business Capabilities](../capabilities/index.md)

---

*Generated from `architecture/metadata/` YAML files by `portal/scripts/generate-domain-pages.py`.*
