---
hide:
  - navigation
  - toc
---

<div class="hero" markdown>

# NovaTrek Architecture Portal

<p class="subtitle">Living Architecture for Adventure Operations</p>

<span class="version-badge"><a href="microservices/">19 Services</a> &middot; <a href="events/">7 Events</a> &middot; <a href="actors/">39 Actors</a> &middot; <a href="decisions/">11 ADRs</a></span>

</div>

<div class="home-section" markdown>

## Explore the Platform

<div class="portal-grid" markdown>

<a href="microservices/" class="portal-card" markdown>
<span class="card-icon">:material-hexagon-multiple:</span>

### Microservices

19 services with 139 interactive sequence diagrams, C4 context views, data store documentation, and Swagger UI for every endpoint.
</a>

<a href="applications/" class="portal-card" markdown>
<span class="card-icon">:material-application:</span>

### Applications

3 frontend applications — Guest Portal, Operations Dashboard, and Adventure App — with screen-level architecture flows.
</a>

<a href="events/" class="portal-card" markdown>
<span class="card-icon">:material-lightning-bolt:</span>

### Event Catalog

7 domain events across 6 producers with AsyncAPI specs, event flow diagrams, and interactive schema viewers.
</a>

<a href="actors/" class="portal-card" markdown>
<span class="card-icon">:material-account-group:</span>

### Actor Catalog

39 actors across the enterprise — people, apps, services, external systems, and infrastructure — all cross-linked.
</a>

<a href="services/" class="portal-card" markdown>
<span class="card-icon">:material-file-tree:</span>

### Service Catalog

Consolidated inventory with domain ownership, API contracts, dependencies, and OpenAPI specifications.
</a>

<a href="standards/" class="portal-card" markdown>
<span class="card-icon">:material-draw:</span>

### Design Standards

arc42 templates, C4 model notation, MADR decision records, ISO 25010 quality attributes, and ADR templates.
</a>

<a href="roadmap/" class="portal-card" markdown>
<span class="card-icon">:material-road-variant:</span>

### Platform Roadmap

Future initiatives including CALM automated governance, test methodology, Azure implementation, and cross-linking strategy.
</a>

</div>

</div>

---

<div class="home-section" markdown>

## Architecture at a Glance

<div class="portal-grid portal-grid--wide" markdown>

<div class="portal-card portal-card--flat" markdown>

### :material-domain: Service Domains

| Domain | Services |
|--------|----------|
| Operations | [svc-check-in](microservices/svc-check-in/), [svc-scheduling-orchestrator](microservices/svc-scheduling-orchestrator/) |
| Guest Identity | [svc-guest-profiles](microservices/svc-guest-profiles/) |
| Booking | [svc-reservations](microservices/svc-reservations/) |
| Product Catalog | [svc-trip-catalog](microservices/svc-trip-catalog/), [svc-trail-management](microservices/svc-trail-management/) |
| Safety | [svc-safety-compliance](microservices/svc-safety-compliance/) |
| Logistics | [svc-transport-logistics](microservices/svc-transport-logistics/), [svc-gear-inventory](microservices/svc-gear-inventory/) |
| Guide Management | [svc-guide-management](microservices/svc-guide-management/) |
| External | [svc-partner-integrations](microservices/svc-partner-integrations/) |
| Support | [svc-notifications](microservices/svc-notifications/), [svc-payments](microservices/svc-payments/), [svc-loyalty-rewards](microservices/svc-loyalty-rewards/), [svc-media-gallery](microservices/svc-media-gallery/), [svc-analytics](microservices/svc-analytics/), [svc-weather](microservices/svc-weather/), [svc-location-services](microservices/svc-location-services/), [svc-inventory-procurement](microservices/svc-inventory-procurement/) |

</div>

<div class="portal-card portal-card--flat" markdown>

### :material-transit-connection-variant: Key Integration Patterns

- **Synchronous REST** within bounded contexts for real-time reads
- **[Apache Kafka](actors/#event-bus)** event bus for cross-domain async communication
- **[API Gateway](actors/#api-gateway)** as the single entry point for all external traffic
- **Saga/orchestrator pattern** for multi-service workflows (check-in, scheduling)
- **CQRS** separation in analytics and reporting paths

### :material-shield-check: Safety Classification

| Pattern | Risk | Check-in |
|---------|------|----------|
| Pattern 1 (Basic) | Low | Self-service |
| Pattern 2 (Guided) | Medium | Guide-assisted |
| Pattern 3 (Full Service) | High | Staff-assisted |

Unknown categories default to **Pattern 3** ([ADR-005](decisions/ADR-005-pattern3-default-fallback.md)).

</div>

</div>

</div>

---

<div class="home-section" markdown>

## Enterprise Architecture

<div class="diagram-wrap">
<a href="microservices/svg/enterprise-c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>
<object data="microservices/svg/enterprise-c4-context.svg" type="image/svg+xml" style="width:100%;max-width:1200px;display:block;margin:0 auto"></object>
</div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/architecture/specs" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from all OpenAPI specs + cross-service-calls.yaml</a>

</div>

---

<div class="home-section" markdown>

## Recent Decisions

| ADR | Title | Status |
|-----|-------|--------|
| [ADR-011](../decisions/ADR-011-optimistic-locking-daily-schedule.md) | Optimistic Locking for Daily Schedule | Accepted |
| [ADR-010](../decisions/ADR-010-patch-semantics-schedule-updates.md) | PATCH Semantics for Schedule Updates | Accepted |
| [ADR-009](../decisions/ADR-009-session-scoped-kiosk-access.md) | Session-Scoped Kiosk Access | Accepted |
| [ADR-008](../decisions/ADR-008-temporary-guest-profile.md) | Temporary Guest Profile | Accepted |
| [ADR-007](../decisions/ADR-007-four-field-identity-verification.md) | Four-Field Identity Verification | Accepted |
| [ADR-006](../decisions/ADR-006-orchestrator-pattern-checkin.md) | Orchestrator Pattern for Check-in | Accepted |

[View all 11 decisions :material-arrow-right:](../decisions/README.md){ .md-button }

</div>
