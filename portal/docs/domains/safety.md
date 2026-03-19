# Safety Domain

**Team:** Safety and Compliance Team  
**Services:** 3  
**Domain color:** #dc2626

Guest and staff safety including waiver management, incident reporting, emergency response coordination, and wildlife/environmental monitoring.

---

## Topology

<div class="diagram-wrap">
  <a href="../../topology/svg/topology-safety.svg" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>
  <object data="../../topology/svg/topology-safety.svg" type="image/svg+xml" style="max-width: 100%;">
    Safety Service Topology C4 Diagram
  </object>
</div>

---

## Services

| Service | Database Engine | Schema | Tables | API Endpoints |
|---------|----------------|--------|--------|---------------|
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | PostgreSQL 15 | `safety` | 4 | 8 |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | PostgreSQL 15 | `emergency` | 5 | 10 |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | PostgreSQL 15 | `wildlife` | 4 | 10 |

---

## Data Ownership

Every data entity has exactly one owning service. Other services access it read-only through APIs.

| Data Entity | Owning Service | Read Access |
|-------------|---------------|-------------|
| Waivers | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | svc-check-in (read-only for validation), svc-gear-inventory |
| Safety incidents | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | svc-analytics, svc-notifications |
| Emergency records | [svc-emergency-response](../microservices/svc-emergency-response.md) | svc-analytics, svc-notifications |
| Wildlife sightings | [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | svc-trail-management, svc-scheduling-orchestrator |

---

## Data Stores

### svc-safety-compliance

- **Engine:** PostgreSQL 15
- **Schema:** `safety`
- **Tables:** `waivers`, `incidents`, `safety_inspections`, `audit_log`
- **Features:**
    - Immutable audit log (append-only)
    - Digital signature verification for waivers
    - Regulatory compliance retention (7 years)
- **Volume:** ~3,000 waiver checks/day
- **Backup:** Continuous WAL archiving, daily base backup, 7-year retention (regulatory)

### svc-emergency-response

- **Engine:** PostgreSQL 15
- **Schema:** `emergency`
- **Tables:** `emergencies`, `emergency_timeline`, `dispatch_records`, `rescue_teams`, `emergency_contacts`
- **Features:**
    - Indexes on guest_id and reservation_id for fast lookup
    - Optimistic locking via _rev column on emergencies table
    - Composite index on (status, severity) for active incident filtering
    - TTL-based archival of resolved emergencies after 90 days
- **Volume:** ~50 emergencies/month (peak season)
- **Backup:** Continuous WAL archiving, daily base backup, 30-day PITR

### svc-wildlife-tracking

- **Engine:** PostgreSQL 15
- **Schema:** `wildlife`
- **Tables:** `sightings`, `wildlife_alerts`, `species`, `habitat_zones`
- **Features:**
    - PostGIS extension for geospatial queries on sighting locations
    - Indexes on species_id and trail_id for sighting lookups
    - Optimistic locking via _rev on wildlife_alerts
    - Automatic alert generation when dangerous species sighted near trails
- **Volume:** ~200 sightings/month peak season
- **Backup:** Daily base backup, 14-day PITR

---

## Bounded Context Rules

These rules are non-negotiable for this domain.

1. Safety waivers are **legally binding** — digital signatures verified via DocuSign API
2. All incidents are logged and propagated as domain events for analytics and notification
3. Emergency response coordinates with guest profiles (medical info), location services (GPS), and guide management (nearest responder)

---

## Cross-Domain Integration

### Outbound (this domain calls)

| Source | Target | Target Domain | Action | Async |
|--------|--------|--------------|--------|-------|
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Guest Identity | Validate guest identity | No |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | [svc-notifications](../microservices/svc-notifications.md) | Support | Send waiver copy | Yes |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Guest Identity | Get guest contact info | No |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | [svc-guide-management](../microservices/svc-guide-management.md) | Guide Management | Get assigned guide | No |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | [svc-notifications](../microservices/svc-notifications.md) | Support | Send safety alert | Yes |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Guest Identity | Retrieve guest medical info and emergency contacts | No |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | [svc-location-services](../microservices/svc-location-services.md) | Support | Get last known guest GPS position | No |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | [svc-guide-management](../microservices/svc-guide-management.md) | Guide Management | Identify nearest on-duty guide | No |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | [svc-notifications](../microservices/svc-notifications.md) | Support | Send emergency alerts to staff and guests | Yes |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | [svc-guide-management](../microservices/svc-guide-management.md) | Guide Management | Check guide availability for rescue | No |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | [svc-notifications](../microservices/svc-notifications.md) | Support | Notify dispatched rescue team | Yes |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | [svc-trail-management](../microservices/svc-trail-management.md) | Product Catalog | Identify nearest trails to sighting location | No |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | [svc-weather](../microservices/svc-weather.md) | Support | Get current conditions at sighting location | No |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | [svc-trail-management](../microservices/svc-trail-management.md) | Product Catalog | Recommend trail closure for affected corridors | No |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | [svc-notifications](../microservices/svc-notifications.md) | Support | Alert operations staff and active guides | Yes |

### Inbound (called by other domains)

| Source | Source Domain | Target | Action | Async |
|--------|-------------|--------|--------|-------|
| [svc-check-in](../microservices/svc-check-in.md) | Operations | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Validate active waiver | No |
| [svc-check-in](../microservices/svc-check-in.md) | Operations | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Log gear verification | No |
| [svc-gear-inventory](../microservices/svc-gear-inventory.md) | Logistics | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Check waiver status | No |
| [svc-trail-management](../microservices/svc-trail-management.md) | Product Catalog | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Update trail safety assessment | No |
| [svc-trail-management](../microservices/svc-trail-management.md) | Product Catalog | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Validate trail safety rating | No |

---

## Domain Events

### Events Produced

| Event | Channel | Producer | Summary |
|-------|---------|----------|---------|
| `incident.reported` | `novatrek.safety.incident.reported` | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Published when a safety incident is reported |
| `emergency.triggered` | `novatrek.safety.emergency.triggered` | [svc-emergency-response](../microservices/svc-emergency-response.md) | Published when a new emergency SOS is triggered by a guest or staff member |
| `wildlife_alert.issued` | `novatrek.safety.wildlife-alert.issued` | [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | Published when a dangerous wildlife alert is issued for trails in a region |

**Consumers of these events:**

- `incident.reported` → [svc-notifications](../microservices/svc-notifications.md), [svc-analytics](../microservices/svc-analytics.md)
- `emergency.triggered` → [svc-notifications](../microservices/svc-notifications.md), [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md), [svc-safety-compliance](../microservices/svc-safety-compliance.md), [svc-analytics](../microservices/svc-analytics.md)
- `wildlife_alert.issued` → [svc-notifications](../microservices/svc-notifications.md), [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md), [svc-trail-management](../microservices/svc-trail-management.md), [svc-analytics](../microservices/svc-analytics.md)

### Events Consumed

| Event | Channel | Producer | Producer Domain | Consuming Service |
|-------|---------|----------|----------------|-------------------|
| `emergency.triggered` | `novatrek.safety.emergency.triggered` | [svc-emergency-response](../microservices/svc-emergency-response.md) | Safety | [svc-safety-compliance](../microservices/svc-safety-compliance.md) |

---

## Business Capabilities

Capabilities served by this domain's services.

| ID | Capability | Status | Description |
|----|-----------|--------|-------------|
| CAP-3.1 | Waiver and Compliance Management | IMPLEMENTED | Digital waiver collection, age verification, regulatory compliance tracking |
| CAP-3.2 | Incident Reporting and Response | IMPLEMENTED | Incident logging, investigation workflow, and regulatory reporting |
| CAP-3.3 | Emergency Response Coordination | IMPLEMENTED | Emergency protocol activation, rescue dispatch, and communication coordination |
| CAP-3.4 | Wildlife and Environmental Monitoring | IMPLEMENTED | Wildlife sighting reporting, trail closure triggers, environmental risk assessment |

---

## Quick Links

- [Domain Topology View](../topology/domain-views.md#safety)
- [svc-safety-compliance Microservice Page](../microservices/svc-safety-compliance.md)
- [svc-emergency-response Microservice Page](../microservices/svc-emergency-response.md)
- [svc-wildlife-tracking Microservice Page](../microservices/svc-wildlife-tracking.md)
- [Event Catalog](../events/index.md)
- [Business Capabilities](../capabilities/index.md)

---

*Generated from `architecture/metadata/` YAML files by `portal/scripts/generate-domain-pages.py`.*
