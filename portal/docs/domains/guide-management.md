# Guide Management Domain

**Team:** Guide Operations Team  
**Services:** 1  
**Domain color:** #4f46e5

Guide assignment, certification tracking, availability management, and preference handling for adventure staffing.

---

## Topology

<div class="diagram-wrap">
  <a href="../../topology/svg/topology-guide-management.svg" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>
  <object data="../../topology/svg/topology-guide-management.svg" type="image/svg+xml" style="max-width: 100%;">
    Guide Management Service Topology C4 Diagram
  </object>
</div>

---

## Services

| Service | Database Engine | Schema | Tables | API Endpoints |
|---------|----------------|--------|--------|---------------|
| [svc-guide-management](../microservices/svc-guide-management.md) | PostgreSQL 15 | `guides` | 5 | 12 |

---

## Data Ownership

Every data entity has exactly one owning service. Other services access it read-only through APIs.

| Data Entity | Owning Service | Read Access |
|-------------|---------------|-------------|
| Guide preferences | [svc-guide-management](../microservices/svc-guide-management.md) | svc-scheduling-orchestrator (read-only) |
| Guide certifications | [svc-guide-management](../microservices/svc-guide-management.md) | svc-safety-compliance |
| Guide availability | [svc-guide-management](../microservices/svc-guide-management.md) | svc-scheduling-orchestrator, svc-emergency-response |

---

## Data Stores

### svc-guide-management

- **Engine:** PostgreSQL 15
- **Schema:** `guides`
- **Tables:** `guides`, `certifications`, `guide_schedules`, `availability_windows`, `ratings`
- **Features:**
    - Certification expiry tracking with automated alerts
    - Availability window overlap detection constraints
    - Weighted rating aggregation with recency bias
- **Volume:** ~100 schedule updates/day, ~500 availability queries/day
- **Backup:** Daily pg_dump, 30-day retention

---

## Bounded Context Rules

These rules are non-negotiable for this domain.

1. Guide availability and preferences are **read-only** to [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) — mutations only through this domain
2. Guide certifications determine which adventure categories they can lead

---

## Cross-Domain Integration

### Outbound

No outbound cross-domain calls.

### Inbound (called by other domains)

| Source | Source Domain | Target | Action | Async |
|--------|-------------|--------|--------|-------|
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | Operations | [svc-guide-management](../microservices/svc-guide-management.md) | Check guide availability | No |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | Operations | [svc-guide-management](../microservices/svc-guide-management.md) | Get all available guides | No |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | Operations | [svc-guide-management](../microservices/svc-guide-management.md) | Reassign guide | No |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Safety | [svc-guide-management](../microservices/svc-guide-management.md) | Get assigned guide | No |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | Safety | [svc-guide-management](../microservices/svc-guide-management.md) | Identify nearest on-duty guide | No |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | Safety | [svc-guide-management](../microservices/svc-guide-management.md) | Check guide availability for rescue | No |

---

## Domain Events

### Events Consumed

| Event | Channel | Producer | Producer Domain | Consuming Service |
|-------|---------|----------|----------------|-------------------|
| `schedule.published` | `novatrek.operations.schedule.published` | [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | Operations | [svc-guide-management](../microservices/svc-guide-management.md) |

---

## Business Capabilities

Capabilities served by this domain's services.

| ID | Capability | Status | Description |
|----|-----------|--------|-------------|
| CAP-2.3 | Guide Assignment and Management | IMPLEMENTED | Guide roster, certification tracking, adventure assignment, and availability |

---

## Quick Links

- [Domain Topology View](../topology/domain-views.md#guide-management)
- [svc-guide-management Microservice Page](../microservices/svc-guide-management.md)
- [Event Catalog](../events/index.md)
- [Business Capabilities](../capabilities/index.md)

---

*Generated from `architecture/metadata/` YAML files by `portal/scripts/generate-domain-pages.py`.*
