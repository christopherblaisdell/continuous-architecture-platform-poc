# Guest Identity Domain

**Team:** Guest Experience Team  
**Services:** 1  
**Domain color:** #7c3aed

Guest identity resolution, profile management, certifications, and medical information. The single source of truth for all guest identity data across the platform.

---

## Topology

<div class="diagram-wrap">
  <a href="../../topology/svg/topology-guest-identity.svg" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>
  <object data="../../topology/svg/topology-guest-identity.svg" type="image/svg+xml" style="max-width: 100%;">
    Guest Identity Service Topology C4 Diagram
  </object>
</div>

---

## Services

| Service | Database Engine | Schema | Tables | API Endpoints |
|---------|----------------|--------|--------|---------------|
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | PostgreSQL 15 | `guests` | 5 | 9 |

---

## Data Ownership

Every data entity has exactly one owning service. Other services access it read-only through APIs.

| Data Entity | Owning Service | Read Access |
|-------------|---------------|-------------|
| Guest profiles | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | All services (read-only via API) |
| Guest certifications | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | svc-safety-compliance, svc-guide-management |
| Medical info | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | svc-emergency-response (read-only) |

---

## Data Stores

### svc-guest-profiles

- **Engine:** PostgreSQL 15
- **Schema:** `guests`
- **Tables:** `guest_profiles`, `certifications`, `medical_info`, `emergency_contacts`, `adventure_history`
- **Features:**
    - PII encrypted at rest (AES-256)
    - Composite index on (last_name, date_of_birth)
    - Soft delete with GDPR data retention policy
- **Volume:** ~800 new profiles/day peak season
- **Backup:** Continuous WAL archiving, daily base backup, 90-day PITR (GDPR)

---

## Bounded Context Rules

These rules are non-negotiable for this domain.

1. Guest identity resolution **always flows through** [svc-guest-profiles](../microservices/svc-guest-profiles.md) — services MUST NOT maintain shadow guest records
2. PII is encrypted at rest (AES-256) with GDPR-compliant retention policies
3. Identity verification uses **four-field matching** ([ADR-007](../decisions/ADR-007-four-field-identity-verification.md))
4. Temporary guest profiles have a 90-day TTL with merge-on-return semantics ([ADR-008](../decisions/ADR-008-temporary-guest-profile.md))

---

## Cross-Domain Integration

### Outbound (this domain calls)

| Source | Target | Target Domain | Action | Async |
|--------|--------|--------------|--------|-------|
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | [svc-reservations](../microservices/svc-reservations.md) | Booking | Query past bookings | No |
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | [svc-analytics](../microservices/svc-analytics.md) | Support | Get satisfaction scores | No |

### Inbound (called by other domains)

| Source | Source Domain | Target | Action | Async |
|--------|-------------|--------|--------|-------|
| [svc-check-in](../microservices/svc-check-in.md) | Operations | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Validate guest identity | No |
| [svc-reservations](../microservices/svc-reservations.md) | Booking | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Validate guest identity | No |
| [svc-reservations](../microservices/svc-reservations.md) | Booking | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Validate participant | No |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | External | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Validate guest identity | No |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Safety | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Validate guest identity | No |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Safety | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Get guest contact info | No |
| [svc-gear-inventory](../microservices/svc-gear-inventory.md) | Logistics | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Validate guest | No |
| [svc-loyalty-rewards](../microservices/svc-loyalty-rewards.md) | Support | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Get member profile | No |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | Safety | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Retrieve guest medical info and emergency contacts | No |
| [svc-reviews](../microservices/svc-reviews.md) | Support | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Validate guest identity | No |

---

## Domain Events

### Events Produced

| Event | Channel | Producer | Summary |
|-------|---------|----------|---------|
| `guest.registered` | `novatrek.guest-identity.guest.registered` | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Published when a new guest profile is created |

**Consumers of these events:**

- `guest.registered` → [svc-loyalty-rewards](../microservices/svc-loyalty-rewards.md), [svc-analytics](../microservices/svc-analytics.md)

---

## Architecture Decisions

ADRs that directly constrain or shape this domain.

| ADR | Title |
|-----|-------|
| [ADR-007](../decisions/ADR-007-four-field-identity-verification.md) | Four-Field Identity Verification |
| [ADR-008](../decisions/ADR-008-temporary-guest-profile.md) | Temporary Guest Profile |

---

## Business Capabilities

Capabilities served by this domain's services.

| ID | Capability | Status | Description |
|----|-----------|--------|-------------|
| CAP-1.1 | Guest Identity and Profile Management | IMPLEMENTED | Create, verify, merge, and manage guest identity records |

---

## Quick Links

- [Domain Topology View](../topology/domain-views.md#guest-identity)
- [svc-guest-profiles Microservice Page](../microservices/svc-guest-profiles.md)
- [Event Catalog](../events/index.md)
- [Business Capabilities](../capabilities/index.md)

---

*Generated from `architecture/metadata/` YAML files by `portal/scripts/generate-domain-pages.py`.*
