# NovaTrek Domain Model

This page describes the business domain that the NovaTrek architecture serves. Understanding the domain is a prerequisite for producing architecturally sound solution designs.

---

## What NovaTrek Does

NovaTrek Adventures is an outdoor adventure company that operates guided trips — hiking, rock climbing, kayaking, wildlife tours, and 21 other adventure categories. The platform manages the full lifecycle: guests browse and book adventures, check in on the day of their trip, receive safety briefings and gear, and participate in guided experiences.

---

## Service Domains

The platform is decomposed into 9 bounded contexts, each owning a set of microservices.

| Domain | Services | Team | Responsibility |
|--------|----------|------|----------------|
| **[Operations](../domains/operations.md)** | [svc-check-in](../microservices/svc-check-in/), [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator/) | NovaTrek Operations | Day-of-adventure workflows, schedule management |
| **[Guest Identity](../domains/guest-identity.md)** | [svc-guest-profiles](../microservices/svc-guest-profiles/) | Guest Experience | Guest identity resolution, profile management |
| **[Booking](../domains/booking.md)** | [svc-reservations](../microservices/svc-reservations/) | Booking Platform | Reservation lifecycle |
| **[Product Catalog](../domains/product-catalog.md)** | [svc-trip-catalog](../microservices/svc-trip-catalog/), [svc-trail-management](../microservices/svc-trail-management/) | Product | Adventure products and trail data |
| **[Safety](../domains/safety.md)** | [svc-safety-compliance](../microservices/svc-safety-compliance/) | Safety and Compliance | Waivers, safety certifications, compliance |
| **[Logistics](../domains/logistics.md)** | [svc-transport-logistics](../microservices/svc-transport-logistics/), [svc-gear-inventory](../microservices/svc-gear-inventory/) | Logistics | Transport coordination, gear tracking |
| **[Guide Management](../domains/guide-management.md)** | [svc-guide-management](../microservices/svc-guide-management/) | Guide Operations | Guide assignments, certifications, preferences |
| **[External](../domains/external.md)** | [svc-partner-integrations](../microservices/svc-partner-integrations/) | Integration | Third-party booking channels, external systems |
| **[Support](../domains/support.md)** | [svc-notifications](../microservices/svc-notifications/), [svc-payments](../microservices/svc-payments/), [svc-loyalty-rewards](../microservices/svc-loyalty-rewards/), [svc-media-gallery](../microservices/svc-media-gallery/), [svc-analytics](../microservices/svc-analytics/), [svc-weather](../microservices/svc-weather/), [svc-location-services](../microservices/svc-location-services/), [svc-inventory-procurement](../microservices/svc-inventory-procurement/) | Various | Cross-cutting platform services |

---

## Bounded Context Rules

These rules are non-negotiable. Every solution design must respect them.

1. **Services within the same domain** may share data types but MUST communicate via API contracts
2. **Cross-domain communication** MUST go through published API endpoints — never direct database access
3. **Each service owns its data exclusively** — no shared databases between services
4. **Event-driven integration** is preferred between domains; synchronous REST within a domain is acceptable
5. **[svc-check-in](../microservices/svc-check-in/)** is the designated orchestrator for all day-of-adventure workflows
6. **[svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator/)** owns the schedule lifecycle — other services MUST NOT mutate schedule data directly
7. **Guest identity resolution** always flows through [svc-guest-profiles](../microservices/svc-guest-profiles/) — services MUST NOT maintain shadow guest records

---

## Data Ownership

Every data entity has exactly one owning service. Other services access it read-only through APIs.

| Data Entity | Owning Service | Read Access |
|-------------|---------------|-------------|
| Check-in records | [svc-check-in](../microservices/svc-check-in/) | [svc-analytics](../microservices/svc-analytics/), [svc-notifications](../microservices/svc-notifications/) |
| Guest profiles | [svc-guest-profiles](../microservices/svc-guest-profiles/) | All services (read-only via API) |
| Reservations | [svc-reservations](../microservices/svc-reservations/) | [svc-check-in](../microservices/svc-check-in/), [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator/) |
| Daily schedules | [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator/) | [svc-guide-management](../microservices/svc-guide-management/) (read), [svc-check-in](../microservices/svc-check-in/) (read) |
| Guide preferences | [svc-guide-management](../microservices/svc-guide-management/) | [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator/) (read-only) |
| Trail data | [svc-trail-management](../microservices/svc-trail-management/) | [svc-trip-catalog](../microservices/svc-trip-catalog/), [svc-safety-compliance](../microservices/svc-safety-compliance/) |
| Adventure catalog | [svc-trip-catalog](../microservices/svc-trip-catalog/) | [svc-check-in](../microservices/svc-check-in/), [svc-reservations](../microservices/svc-reservations/) |
| Waivers | [svc-safety-compliance](../microservices/svc-safety-compliance/) | [svc-check-in](../microservices/svc-check-in/) (read-only for validation) |

When designing a solution, always verify data ownership boundaries. If your design requires Service A to write data owned by Service B, you have a boundary violation that needs to be resolved — typically through an API call to Service B or an event-driven pattern.

---

## Adventure Classification System

NovaTrek classifies 25 adventure categories into 3 check-in UI patterns. This classification drives safety workflows, gear assignment, and staffing requirements.

| Pattern | Description | Safety Level | Check-in Mode | Examples |
|---------|-------------|-------------|---------------|----------|
| **Pattern 1** (Basic) | Simple self-check-in, minimal equipment | Low risk | Self-service kiosk | Nature walks, bird watching |
| **Pattern 2** (Guided) | Guide-assisted check-in, moderate equipment | Medium risk | Guide-assisted | Hiking, kayaking |
| **Pattern 3** (Full Service) | Full staff-assisted check-in, extensive safety gear | High risk | Staff-assisted | Rock climbing, whitewater rafting |

!!! warning "CRITICAL SAFETY RULE"
    Unknown or unmapped adventure categories MUST default to **Pattern 3 (Full Service)**, never Pattern 1. This ensures maximum safety protocols for any unrecognized activity. This rule is codified in [ADR-005](../decisions/ADR-005-pattern3-default-fallback.md) and is enforced via configuration in [`config/adventure-classification.yaml`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/config/adventure-classification.yaml).

The classification is configuration-driven ([ADR-004](../decisions/ADR-004-configuration-driven-classification.md)), meaning new adventure categories can be added to [`config/adventure-classification.yaml`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/config/adventure-classification.yaml) without code changes. The classification engine reads this YAML at runtime.

---

## Integration Patterns

### Synchronous (REST)

Used for real-time operations within bounded contexts and for cross-domain reads where latency matters:

- Check-in service calling guest profiles to verify identity
- Scheduling orchestrator reading guide availability
- Reservations service looking up trip catalog details

### Asynchronous (Kafka Events)

Used for cross-domain state propagation where eventual consistency is acceptable:

- Check-in completion triggers gear preparation notification
- Reservation confirmation triggers schedule slot allocation
- Safety waiver expiration triggers guest notification

See the [Event Catalog](../events/index.md) for the full list of domain events, producers, and consumers.

### Orchestration vs. Choreography

- **[svc-check-in](../microservices/svc-check-in/)** uses the **orchestrator pattern** for day-of-adventure workflows — it coordinates the sequence of calls to guest profiles, reservations, safety compliance, and gear inventory ([ADR-006](../decisions/ADR-006-orchestrator-pattern-checkin.md))
- **Cross-domain** integration uses **choreography** via Kafka events — no central coordinator; each domain reacts to events independently

---

## Frontend Applications

Three frontend applications consume the microservice APIs:

| Application | Users | Key Screens |
|-------------|-------|-------------|
| **Web Guest Portal** | Guests (pre-trip) | Browse adventures, book trips, manage reservations, pre-check-in |
| **Web Ops Dashboard** | Operations staff | Live adventure tracking, schedule management, incident response |
| **Mobile Guest App** | Guests (day-of) | Day-of check-in, adventure details, real-time updates, photo sharing |

Wireframes for these applications are maintained as Excalidraw files in `architecture/wireframes/`. See [Diagrams and Wireframes](diagrams-and-wireframes.md) for how to edit them.

---

## Key Architecture Decisions

These global decisions constrain the design space. Read them before proposing solutions.

| ADR | Title | Impact |
|-----|-------|--------|
| [ADR-003](../decisions/ADR-003-nullable-elevation-fields.md) | Nullable Elevation Fields | Trail elevation data may be null; consumers must handle gracefully |
| [ADR-004](../decisions/ADR-004-configuration-driven-classification.md) | Configuration-Driven Classification | Adventure categories are YAML-driven, not hardcoded |
| [ADR-005](../decisions/ADR-005-pattern3-default-fallback.md) | Pattern 3 Default Fallback | Unknown categories default to highest safety level |
| [ADR-010](../decisions/ADR-010-patch-semantics-schedule-updates.md) | PATCH Semantics for Schedule Updates | Schedule mutations use PATCH, not PUT (prevents data overwrite) |
| [ADR-011](../decisions/ADR-011-optimistic-locking-daily-schedule.md) | Optimistic Locking for Daily Schedule | `_rev` field with 409 Conflict on mismatch |
| [ADR-012](../decisions/ADR-012-test-methodology-tdd-bdd-hybrid.md) | TDD/BDD Hybrid Test Methodology | Unit/integration via TDD; acceptance via BDD |
| [ADR-013](../decisions/ADR-013-spring-cloud-contract-testing.md) | Spring Cloud Contract Testing | API contracts verified via consumer-driven contract tests |
