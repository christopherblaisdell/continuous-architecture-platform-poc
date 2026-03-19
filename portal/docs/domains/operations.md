# Operations Domain

**Team:** NovaTrek Operations Team  
**Services:** 2  
**Domain color:** #2563eb

Day-of-adventure workflows including guest check-in, schedule management, and real-time operational coordination. This domain orchestrates the core guest experience on the day of their adventure.

---

## Topology

<div class="diagram-wrap">
  <a href="../../topology/svg/topology-operations.svg" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>
  <object data="../../topology/svg/topology-operations.svg" type="image/svg+xml" style="max-width: 100%;">
    Operations Service Topology C4 Diagram
  </object>
</div>

---

## Services

| Service | Database Engine | Schema | Tables | API Endpoints |
|---------|----------------|--------|--------|---------------|
| [svc-check-in](../microservices/svc-check-in.md) | PostgreSQL 15 | `checkin` | 3 | 5 |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | PostgreSQL 15 + Valkey 8 | `scheduling` | 4 | 5 |

---

## Data Ownership

Every data entity has exactly one owning service. Other services access it read-only through APIs.

| Data Entity | Owning Service | Read Access |
|-------------|---------------|-------------|
| Check-in records | [svc-check-in](../microservices/svc-check-in.md) | svc-analytics, svc-notifications |
| Daily schedules | [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | svc-guide-management (read), svc-check-in (read) |

---

## Data Stores

### svc-check-in

- **Engine:** PostgreSQL 15
- **Schema:** `checkin`
- **Tables:** `check_ins`, `gear_verifications`, `wristband_assignments`
- **Features:**
    - Indexes on reservation_id and check_in_date
    - TTL-based cleanup of stale check-ins (older than 24h)
    - Composite unique constraint on (reservation_id, participant_id)
- **Volume:** ~5,000 check-ins/day peak season
- **Backup:** Continuous WAL archiving, daily base backup, 7-day PITR

### svc-scheduling-orchestrator

- **Engine:** PostgreSQL 15 + Valkey 8
- **Schema:** `scheduling`
- **Tables:** `schedule_requests`, `daily_schedules`, `schedule_conflicts`, `optimization_runs`
- **Features:**
    - Optimistic locking per ADR-011
    - Valkey for schedule lock cache and optimization queue
    - JSONB columns for constraint parameters
- **Volume:** ~500 schedule requests/day
- **Backup:** Continuous WAL archiving, daily base backup, 14-day PITR

---

## Bounded Context Rules

These rules are non-negotiable for this domain.

1. [svc-check-in](../microservices/svc-check-in.md) is the designated **orchestrator** for all day-of-adventure workflows ([ADR-006](../decisions/ADR-006-orchestrator-pattern-checkin.md))
2. [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) **owns the schedule lifecycle** — other services MUST NOT mutate schedule data directly
3. Schedule updates use **PATCH semantics** with optimistic locking to prevent data overwrites ([ADR-010](../decisions/ADR-010-patch-semantics-schedule-updates.md), [ADR-011](../decisions/ADR-011-optimistic-locking-daily-schedule.md))

---

## Cross-Domain Integration

### Outbound (this domain calls)

| Source | Target | Target Domain | Action | Async |
|--------|--------|--------------|--------|-------|
| [svc-check-in](../microservices/svc-check-in.md) | [svc-reservations](../microservices/svc-reservations.md) | Booking | Verify reservation exists | No |
| [svc-check-in](../microservices/svc-check-in.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Guest Identity | Validate guest identity | No |
| [svc-check-in](../microservices/svc-check-in.md) | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | Product Catalog | Get adventure category | No |
| [svc-check-in](../microservices/svc-check-in.md) | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Safety | Validate active waiver | No |
| [svc-check-in](../microservices/svc-check-in.md) | [svc-notifications](../microservices/svc-notifications.md) | Support | Send check-in confirmation | Yes |
| [svc-check-in](../microservices/svc-check-in.md) | [svc-gear-inventory](../microservices/svc-gear-inventory.md) | Logistics | Verify gear assignment | No |
| [svc-check-in](../microservices/svc-check-in.md) | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Safety | Log gear verification | No |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-guide-management](../microservices/svc-guide-management.md) | Guide Management | Check guide availability | No |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-trail-management](../microservices/svc-trail-management.md) | Product Catalog | Verify trail conditions | No |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-weather](../microservices/svc-weather.md) | Support | Get forecast | No |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | Product Catalog | Get trip details | No |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-notifications](../microservices/svc-notifications.md) | Support | Notify assigned guides | Yes |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-guide-management](../microservices/svc-guide-management.md) | Guide Management | Get all available guides | No |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-location-services](../microservices/svc-location-services.md) | Support | Check location capacity | No |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-trip-catalog](../microservices/svc-trip-catalog.md) | Product Catalog | Get trip requirements | No |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-analytics](../microservices/svc-analytics.md) | Support | Log optimization metrics | Yes |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-guide-management](../microservices/svc-guide-management.md) | Guide Management | Reassign guide | No |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | [svc-notifications](../microservices/svc-notifications.md) | Support | Notify affected parties | Yes |

### Inbound

No inbound cross-domain calls.

---

## Domain Events

### Events Produced

| Event | Channel | Producer | Summary |
|-------|---------|----------|---------|
| `checkin.completed` | `novatrek.operations.checkin.completed` | [svc-check-in](../microservices/svc-check-in.md) | Published when a guest completes the check-in process |
| `schedule.published` | `novatrek.operations.schedule.published` | [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | Published when a daily schedule is finalized |

**Consumers of these events:**

- `checkin.completed` → [svc-analytics](../microservices/svc-analytics.md), [svc-notifications](../microservices/svc-notifications.md)
- `schedule.published` → [svc-guide-management](../microservices/svc-guide-management.md), [svc-notifications](../microservices/svc-notifications.md)

### Events Consumed

| Event | Channel | Producer | Producer Domain | Consuming Service |
|-------|---------|----------|----------------|-------------------|
| `reservation.created` | `novatrek.booking.reservation.created` | [svc-reservations](../microservices/svc-reservations.md) | Booking | [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) |
| `emergency.triggered` | `novatrek.safety.emergency.triggered` | [svc-emergency-response](../microservices/svc-emergency-response.md) | Safety | [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) |
| `wildlife_alert.issued` | `novatrek.safety.wildlife-alert.issued` | [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | Safety | [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) |

---

## Architecture Decisions

ADRs that directly constrain or shape this domain.

| ADR | Title |
|-----|-------|
| [ADR-004](../decisions/ADR-004-configuration-driven-classification.md) | Configuration-Driven Classification |
| [ADR-005](../decisions/ADR-005-pattern3-default-fallback.md) | Pattern 3 Default Fallback |
| [ADR-006](../decisions/ADR-006-orchestrator-pattern-checkin.md) | Orchestrator Pattern for Check-In |
| [ADR-007](../decisions/ADR-007-four-field-identity-verification.md) | Four-Field Identity Verification |
| [ADR-009](../decisions/ADR-009-session-scoped-kiosk-access.md) | Session-Scoped Kiosk Access |
| [ADR-010](../decisions/ADR-010-patch-semantics-schedule-updates.md) | PATCH Semantics for Schedule Updates |
| [ADR-011](../decisions/ADR-011-optimistic-locking-daily-schedule.md) | Optimistic Locking for Daily Schedule |

---

## Business Capabilities

Capabilities served by this domain's services.

| ID | Capability | Status | Description |
|----|-----------|--------|-------------|
| CAP-2.1 | Day-of-Adventure Check-In | IMPLEMENTED | Guest arrival processing, identity verification, wristband assignment, safety briefing |
| CAP-2.2 | Schedule Planning and Optimization | IMPLEMENTED | Daily schedule creation, slot management, and capacity optimization |

---

## Quick Links

- [Domain Topology View](../topology/domain-views.md#operations)
- [svc-check-in Microservice Page](../microservices/svc-check-in.md)
- [svc-scheduling-orchestrator Microservice Page](../microservices/svc-scheduling-orchestrator.md)
- [Event Catalog](../events/index.md)
- [Business Capabilities](../capabilities/index.md)

---

*Generated from `architecture/metadata/` YAML files by `portal/scripts/generate-domain-pages.py`.*
