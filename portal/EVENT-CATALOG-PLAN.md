# Event Catalog Plan — NovaTrek Architecture Portal

| | |
|-----------|-------|
| **Author** | Christopher Blaisdell |
| **Created** | 2026-03-05 |
| **Status** | Proposed |
| **Related** | [Microservice Pages Generator](scripts/generate-microservice-pages.py) · [CLOSING-THE-LOOP.md](../CLOSING-THE-LOOP.md) · [copilot-instructions.md](../.github/copilot-instructions.md) |

---

## 1. Problem Statement

The NovaTrek workspace already references domain events in `CROSS_SERVICE_CALLS` (e.g., `reservation.created`, `reservation.status_changed`, `guest.registered`) but they exist only as inline strings in a Python generator script. There is:

- No authoritative event catalog — no single place listing all domain events, their schemas, producers, and consumers
- No event schema definitions — events are mentioned by name without payload structure
- No portal pages for events — the architecture portal documents REST APIs comprehensively (19 services, 139 endpoints, Swagger UI) but events are invisible
- No tooling to validate event contracts — unlike OpenAPI specs that validate REST contracts, event contracts have no source-of-truth file

This is a gap. The copilot-instructions.md states: *"Event-driven integration is preferred between domains; synchronous REST within a domain is acceptable."* If events are the preferred cross-domain integration pattern, they deserve the same documentation rigor as REST APIs.

---

## 2. Decision: AsyncAPI vs JSON Files

### Option A: AsyncAPI Specs (YAML)

[AsyncAPI](https://www.asyncapi.com/) is the event/message equivalent of OpenAPI. It is a structured YAML specification that defines:

- Channels (topics/queues)
- Messages (event payloads with JSON Schema)
- Servers (broker endpoints)
- Bindings (Kafka, RabbitMQ, etc. specific configuration)

**Pros:**

- Industry standard for event-driven architecture documentation (CNCF project)
- Machine-readable — enables code generation, validation, documentation tooling
- Mirrors the OpenAPI pattern already established in the workspace (19 YAML specs in `portal/docs/specs/`)
- AsyncAPI Studio and AsyncAPI Generator can produce interactive documentation (similar to Swagger UI)
- Schema evolution and compatibility checking (forward/backward) can be automated
- Deep linking from microservice pages to event definitions follows the same pattern as Swagger UI links

**Cons:**

- Learning curve for the team (though similar to OpenAPI which is already in use)
- AsyncAPI tooling is less mature than OpenAPI tooling
- Requires maintaining a separate spec per service or a unified spec

### Option B: Plain JSON/YAML Files (Custom Schema)

Define events as simple YAML files with a custom structure — event name, producer, consumers, payload fields.

**Pros:**

- Zero learning curve — just YAML files with whatever structure we define
- Full control over format
- No external tooling dependencies

**Cons:**

- No validation tooling — payload schemas can drift without detection
- No code generation — every integration point is manually maintained
- No interactive documentation tool (no equivalent of Swagger UI)
- Reinventing what AsyncAPI already provides
- Not portable — other teams or tools won't understand our custom format

### Recommendation: AsyncAPI Specs

Use AsyncAPI YAML specs, one per producing service, stored alongside OpenAPI specs. The rationale:

1. **Consistency** — we already use OpenAPI YAML for REST contracts. AsyncAPI YAML for event contracts is the natural parallel.
2. **Tooling** — AsyncAPI Generator can produce an interactive HTML page (like Swagger UI) without custom code.
3. **Schema validation** — JSON Schema in AsyncAPI specs enables automated contract testing.
4. **Industry alignment** — AsyncAPI is the CNCF standard. Using it signals architectural maturity.
5. **Generator integration** — the microservice page generator already reads OpenAPI specs from `portal/docs/specs/`. Reading AsyncAPI specs from the same directory (or a sibling) is a natural extension.

---

## 3. Source Control Structure

### 3.1 File Layout

```
portal/docs/
├── specs/                          # Existing OpenAPI specs (REST)
│   ├── svc-check-in.yaml
│   ├── svc-reservations.yaml
│   └── ... (19 files)
│
├── events/                         # NEW: AsyncAPI specs (Events)
│   ├── svc-check-in.events.yaml
│   ├── svc-reservations.events.yaml
│   ├── svc-guest-profiles.events.yaml
│   ├── svc-scheduling-orchestrator.events.yaml
│   └── ... (one per producing service)
│
├── services/
│   └── api/                        # Existing Swagger UI HTML pages
│       ├── svc-check-in.html
│       └── ...
│
└── events-ui/                      # NEW: Generated AsyncAPI HTML pages
    ├── svc-check-in.events.html
    ├── svc-reservations.events.html
    └── ...
```

### 3.2 Naming Convention

| Artifact | Pattern | Example |
|----------|---------|---------|
| AsyncAPI spec | `{svc-name}.events.yaml` | `svc-reservations.events.yaml` |
| AsyncAPI HTML page | `{svc-name}.events.html` | `svc-reservations.events.html` |
| Event name | `{domain}.{entity}.{past-tense-verb}` | `booking.reservation.created` |
| Channel/topic name | `novatrek.{domain}.{entity}.{verb}` | `novatrek.booking.reservation.created` |

### 3.3 AsyncAPI Spec Structure (Example)

```yaml
asyncapi: 3.0.0
info:
  title: svc-reservations Events
  version: 2.4.1
  description: Domain events published by the NovaTrek Reservations Service
  contact:
    name: Booking Platform Team

defaultContentType: application/json

channels:
  reservationCreated:
    address: novatrek.booking.reservation.created
    messages:
      reservationCreated:
        $ref: '#/components/messages/ReservationCreated'

  reservationStatusChanged:
    address: novatrek.booking.reservation.status-changed
    messages:
      reservationStatusChanged:
        $ref: '#/components/messages/ReservationStatusChanged'

operations:
  publishReservationCreated:
    action: send
    channel:
      $ref: '#/channels/reservationCreated'
    summary: Published when a new reservation is confirmed
    tags:
      - name: booking

  publishReservationStatusChanged:
    action: send
    channel:
      $ref: '#/channels/reservationStatusChanged'
    summary: Published when a reservation status transitions
    tags:
      - name: booking

components:
  messages:
    ReservationCreated:
      name: ReservationCreated
      title: Reservation Created
      summary: A new reservation has been confirmed in the system
      contentType: application/json
      payload:
        $ref: '#/components/schemas/ReservationCreatedPayload'

    ReservationStatusChanged:
      name: ReservationStatusChanged
      title: Reservation Status Changed
      summary: A reservation has transitioned to a new status
      contentType: application/json
      payload:
        $ref: '#/components/schemas/ReservationStatusChangedPayload'

  schemas:
    ReservationCreatedPayload:
      type: object
      required:
        - event_id
        - event_type
        - timestamp
        - reservation_id
        - guest_id
        - trip_id
      properties:
        event_id:
          type: string
          format: uuid
          description: Unique identifier for this event instance
        event_type:
          type: string
          const: reservation.created
        timestamp:
          type: string
          format: date-time
          description: ISO 8601 timestamp when the event occurred
        reservation_id:
          type: string
          format: uuid
        guest_id:
          type: string
          format: uuid
        trip_id:
          type: string
          format: uuid
        trip_date:
          type: string
          format: date
        participant_count:
          type: integer
          minimum: 1
        status:
          type: string
          enum: [CONFIRMED]
        confirmation_code:
          type: string

    ReservationStatusChangedPayload:
      type: object
      required:
        - event_id
        - event_type
        - timestamp
        - reservation_id
        - previous_status
        - new_status
      properties:
        event_id:
          type: string
          format: uuid
        event_type:
          type: string
          const: reservation.status_changed
        timestamp:
          type: string
          format: date-time
        reservation_id:
          type: string
          format: uuid
        previous_status:
          type: string
          enum: [PENDING, CONFIRMED, CHECKED_IN, IN_PROGRESS, COMPLETED, CANCELLED]
        new_status:
          type: string
          enum: [PENDING, CONFIRMED, CHECKED_IN, IN_PROGRESS, COMPLETED, CANCELLED]
        changed_by:
          type: string
          description: User or service that triggered the transition
```

### 3.4 Known Events (from Existing CROSS_SERVICE_CALLS)

These events are already referenced in the generator script and need AsyncAPI specs:

| Event Name | Producer | Trigger Endpoint | Known/Assumed Consumers |
|-----------|----------|-----------------|------------------------|
| `reservation.created` | svc-reservations | `POST /reservations` | svc-scheduling-orchestrator, svc-analytics |
| `reservation.status_changed` | svc-reservations | `PUT /reservations/{id}/status` | svc-notifications, svc-analytics |
| `guest.registered` | svc-guest-profiles | `POST /guests` | svc-loyalty-rewards, svc-analytics |
| `checkin.completed` | svc-check-in | `POST /check-ins` | svc-analytics, svc-notifications (assumed) |
| `schedule.published` | svc-scheduling-orchestrator | `POST /schedule-requests` | svc-guide-management, svc-notifications (assumed) |
| `payment.processed` | svc-payments | `POST /payments` | svc-reservations, svc-notifications (assumed) |
| `incident.reported` | svc-safety-compliance | `POST /incidents` | svc-notifications, svc-analytics (assumed) |

---

## 4. Portal Publishing Plan

### 4.1 Page Architecture

Events should be visible in **three places** in the portal:

#### A. Event Catalog Index Page (New Top-Level Tab)

A new top-level nav tab "Event Catalog" alongside the existing Home, Service Catalog, Design Standards, Applications, Microservice Pages, and Tags tabs.

**Path:** `portal/docs/events/index.md`

**Content:**

- Summary statistics (total events, total producers, total consumers)
- Domain-grouped table of all events (mirroring the microservice index page pattern)
- Each row: event name, channel, producer service (linked), consumer count, link to detail section
- A Mermaid or PlantUML event flow diagram showing all producers, the event bus, and all consumers

**Example layout:**

```
# Event Catalog

19 Events · 8 Producers · 14 Consumers

## Event Flow Overview
[Enterprise event flow diagram — all services, event bus, arrows]

## Booking Events
| Event | Channel | Producer | Consumers | Spec |
|-------|---------|----------|-----------|------|
| Reservation Created | novatrek.booking.reservation.created | svc-reservations | svc-scheduling-orchestrator, svc-analytics | [AsyncAPI] |
| Reservation Status Changed | novatrek.booking.reservation.status-changed | svc-reservations | svc-notifications, svc-analytics | [AsyncAPI] |

## Operations Events
...

## Guest Identity Events
...
```

#### B. Microservice Page Integration (Existing Pages, New Section)

Each microservice page already has sections for Integration Context, Endpoints, and Consuming Applications. Add two new sections:

**"Events Published" section** — appears on producer service pages. For each event:

- Event name and channel
- Trigger description (which endpoint/action causes the event)
- Payload schema summary (key fields only, link to full AsyncAPI spec)
- Link to AsyncAPI HTML page
- List of known consumers (linked to their microservice pages)

**"Events Consumed" section** — appears on consumer service pages. For each consumed event:

- Event name and channel
- Producer service (linked)
- What the consumer does with the event
- Link to the producer's AsyncAPI spec

These sections would be generated by the existing `generate-microservice-pages.py` script, which already reads from data structure dictionaries.

#### C. AsyncAPI Interactive Pages (New, Like Swagger UI)

Generated HTML pages using AsyncAPI tooling, providing an interactive viewer for each service's event specs — the event equivalent of Swagger UI pages.

**Path:** `portal/docs/events-ui/{svc-name}.events.html`

**Linked from:** Microservice pages (button next to "Swagger UI" button), Event Catalog index page

### 4.2 Navigation Structure

```yaml
# Addition to portal/mkdocs.yml nav:
nav:
  - Home: index.md
  - Service Catalog: services/index.md
  - Design Standards: ...
  - Applications: ...
  - Microservice Pages: ...
  - Event Catalog:                          # NEW TAB
    - events/index.md
    - "Booking Events": events/booking.md
    - "Operations Events": events/operations.md
    - "Guest Identity Events": events/guest-identity.md
    # ... one page per domain, or one unified page
  - Tags: tags.md
```

### 4.3 Linking Strategy

| Link Type | From | To | Format |
|-----------|------|----|--------|
| **Event → Producer** | Event catalog row | Microservice page | `/microservices/{svc-name}/` |
| **Event → AsyncAPI UI** | Event catalog row, microservice page button | AsyncAPI HTML page | `/events-ui/{svc-name}.events.html` |
| **Event → Spec download** | Event catalog row, microservice page | Raw YAML file | `/events/{svc-name}.events.yaml` |
| **Producer page → Events published** | "Events Published" section on microservice page | Event catalog entry, AsyncAPI UI | Deep link to event catalog heading |
| **Consumer page → Events consumed** | "Events Consumed" section on microservice page | Producer's event catalog entry | Deep link to producer's event section |
| **Sequence diagram → Event** | Dashed arrow in PlantUML endpoint diagrams | Event catalog entry | PlantUML `[[url]]` clickable link |
| **C4 diagram → Event channel** | Dashed relationship line | Event catalog page | PlantUML `[[url]]` clickable link |

### 4.4 Sequence Diagram Integration

The existing `CROSS_SERVICE_CALLS` already marks event bus interactions with dashed lines (the `True` flag in the tuple indicates async). Currently these render as:

```
CheckIn -[#green,dashed]-> Kafka : reservation.created
```

With the event catalog in place, these arrows should become **clickable links** to the event's entry in the event catalog:

```plantuml
CheckIn -[#green,dashed]-> Kafka : [[/events/#booking-reservationcreated reservation.created]]
```

This change is mechanical — update the PlantUML generation code in `generate_endpoint_puml()` to add `[[url]]` syntax when the call target is the Event Bus.

---

## 5. Generator Integration

### 5.1 New Data Structure: EVENT_CATALOG

Add to `generate-microservice-pages.py`:

```python
EVENT_CATALOG = {
    "reservation.created": {
        "channel": "novatrek.booking.reservation.created",
        "producer": "svc-reservations",
        "trigger": ("POST", "/reservations"),
        "consumers": ["svc-scheduling-orchestrator", "svc-analytics"],
        "domain": "Booking",
        "summary": "Published when a new reservation is confirmed",
    },
    "reservation.status_changed": {
        "channel": "novatrek.booking.reservation.status-changed",
        "producer": "svc-reservations",
        "trigger": ("PUT", "/reservations/{reservation_id}/status"),
        "consumers": ["svc-notifications", "svc-analytics"],
        "domain": "Booking",
        "summary": "Published when a reservation status transitions",
    },
    "guest.registered": {
        "channel": "novatrek.guest-identity.guest.registered",
        "producer": "svc-guest-profiles",
        "trigger": ("POST", "/guests"),
        "consumers": ["svc-loyalty-rewards", "svc-analytics"],
        "domain": "Guest Identity",
        "summary": "Published when a new guest profile is created",
    },
    # ... etc
}
```

### 5.2 Generator Changes

| Change | File | Description |
|--------|------|-------------|
| Add EVENT_CATALOG dict | `generate-microservice-pages.py` | Central event metadata registry |
| Add "Events Published" section | `generate-microservice-pages.py` | Table of events this service produces, rendered after Endpoints section |
| Add "Events Consumed" section | `generate-microservice-pages.py` | Table of events this service consumes, rendered after Events Published |
| Add event deep links to sequence diagrams | `generate-microservice-pages.py` | Make Event Bus arrows clickable to event catalog entries |
| Generate event catalog index page | `generate-microservice-pages.py` (or new script) | Produce `events/index.md` with domain-grouped event tables |
| Generate AsyncAPI HTML pages | New script: `generate-event-pages.py` | Read AsyncAPI YAML specs, produce interactive HTML pages |

### 5.3 Build Pipeline Changes

```bash
# Updated build pipeline
cd portal

# Generate microservice pages (existing — now also generates event sections)
python3 scripts/generate-microservice-pages.py

# Generate event catalog pages (new)
python3 scripts/generate-event-pages.py

# Build MkDocs
/usr/bin/python3 -m mkdocs build

# Copy assets (existing + new)
cp -r docs/services/api site/services/
cp -r docs/specs site/
cp -r docs/microservices/svg site/microservices/
cp -r docs/events site/                     # NEW: AsyncAPI YAML specs
cp -r docs/events-ui site/                  # NEW: AsyncAPI HTML pages
cp staticwebapp.config.json site/

# Deploy
swa deploy site --deployment-token "<token>" --env production
```

---

## 6. AsyncAPI Tooling

### 6.1 HTML Generation

Use the [AsyncAPI React component](https://github.com/asyncapi/asyncapi-react) or the [AsyncAPI Generator](https://github.com/asyncapi/generator) with the HTML template:

```bash
# Install (one-time)
npm install -g @asyncapi/generator

# Generate HTML for each service
for spec in portal/docs/events/*.events.yaml; do
  svc=$(basename "$spec" .events.yaml)
  ag "$spec" @asyncapi/html-template -o "portal/docs/events-ui/" \
    --force-write \
    -p singleFile=true \
    -p outFilename="${svc}.events.html"
done
```

Alternatively, use a self-contained HTML approach similar to `generate-swagger-pages.py` — embed the AsyncAPI spec as JSON in an HTML page that loads the AsyncAPI React component from a CDN. This avoids an npm dependency in the build pipeline.

### 6.2 Validation

```bash
# Validate all AsyncAPI specs (CI step)
npm install -g @asyncapi/cli
for spec in portal/docs/events/*.events.yaml; do
  asyncapi validate "$spec"
done
```

### 6.3 Self-Contained HTML Approach (Preferred)

To match the existing Swagger UI pattern, create a `generate-event-pages.py` script that:

1. Reads each `*.events.yaml` from `portal/docs/events/`
2. Converts to JSON
3. Embeds in an HTML template that loads [AsyncAPI React standalone bundle](https://unpkg.com/@asyncapi/react-component@latest/browser/standalone/index.js)
4. Writes to `portal/docs/events-ui/{svc}.events.html`

This parallels exactly how `generate-swagger-pages.py` works for OpenAPI specs.

---

## 7. Implementation Phases

### Phase 1: Foundation (Event specs + catalog page)

1. Create `portal/docs/events/` directory
2. Write AsyncAPI YAML specs for the 7 known events (from section 3.4)
3. Create `portal/docs/events/index.md` — hand-authored event catalog index page
4. Add "Event Catalog" tab to `portal/mkdocs.yml` nav
5. Add `cp -r docs/events site/` to build pipeline
6. Deploy and verify

### Phase 2: Generator Integration (Microservice page sections)

1. Add `EVENT_CATALOG` dict to `generate-microservice-pages.py`
2. Add "Events Published" and "Events Consumed" sections to generated microservice pages
3. Make Event Bus arrows in sequence diagrams clickable (link to event catalog)
4. Regenerate all 19 microservice pages
5. Deploy and verify

### Phase 3: Interactive Pages (AsyncAPI UI)

1. Create `generate-event-pages.py` script (parallel to `generate-swagger-pages.py`)
2. Generate AsyncAPI HTML pages for each producing service
3. Add "AsyncAPI UI" button to microservice pages (next to Swagger UI button)
4. Add `cp -r docs/events-ui site/` to build pipeline
5. Deploy and verify

### Phase 4: Event Flow Diagrams

1. Add enterprise event flow C4 diagram to event catalog index page
2. Add per-domain event flow diagrams to domain event pages
3. Regenerate and deploy

---

## 8. Copilot Instructions Updates

After implementation, update `.github/copilot-instructions.md` to add:

- `portal/docs/events/` to the Key Locations table
- AsyncAPI spec analysis guidelines (parallel to OpenAPI spec analysis)
- Event naming convention rules
- Event catalog generator usage instructions
- Updated build pipeline with event asset copying

---

## 9. Open Questions

| Question | Options | Recommendation |
|----------|---------|----------------|
| One AsyncAPI spec per service or one unified spec? | Per-service matches OpenAPI pattern | **Per-service** — consistent with existing pattern |
| Should consumer mappings live in AsyncAPI specs or in the generator? | AsyncAPI `x-consumers` extension vs Python dict | **Python dict** for now (like `CROSS_SERVICE_CALLS`), migrate to AsyncAPI extensions later |
| Should we generate the event catalog index page or hand-author it? | Generated = always in sync, hand-authored = more flexible | **Generated** in Phase 2, **hand-authored** in Phase 1 |
| AsyncAPI v2 or v3? | v3 is current but tooling support is still catching up | **v3** — forward-looking, and the self-contained HTML approach avoids tooling gaps |
| Kafka topic naming: `novatrek.{domain}.{entity}.{verb}` or flat? | Hierarchical enables topic-level ACLs and filtering | **Hierarchical** — matches domain-driven design |
| Should event payload schemas reference OpenAPI component schemas? | `$ref` to OpenAPI schemas enables reuse but creates cross-file dependencies | **Copy key fields** into AsyncAPI schemas, document the source OpenAPI schema as a note. Full `$ref` integration is fragile. |
