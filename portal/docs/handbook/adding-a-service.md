---
tags:
  - handbook
  - microservices
  - architecture
---

<!-- PUBLISH -->

<div class="hero" markdown>

# Adding a Service

<p class="subtitle">How to register a new microservice — from OpenAPI spec to live portal page</p>

</div>

Adding a new microservice to the NovaTrek platform requires updates to several metadata files and the creation of an OpenAPI spec. This guide walks through every required file in order.

---

## Overview

When you add a new service, you must touch these files:

| File | What to do |
|---|---|
| `architecture/specs/svc-{name}.yaml` | Create the OpenAPI spec (new file) |
| `architecture/metadata/domains.yaml` | Assign the service to a domain |
| `architecture/metadata/data-stores.yaml` | Document the service's database schema |
| `architecture/metadata/cross-service-calls.yaml` | Document any cross-service integrations |
| `architecture/metadata/capabilities.yaml` | Assign capabilities to the service |
| `architecture/metadata/capability-changelog.yaml` | Record the architectural decision to add the service |
| `architecture/metadata/tickets.yaml` | Register the source ticket |
| `portal/mkdocs.yml` | Add the service page to the navigation |

Optionally:
- `architecture/events/*.events.yaml` — if the service publishes domain events
- `architecture/metadata/events.yaml` — if the service is a producer or consumer of events
- `architecture/metadata/consumers.yaml` — if the service consumes events from other services

---

## Step 1 — Create the OpenAPI Spec

Create `architecture/specs/svc-{service-name}.yaml`. Use an existing spec as a starting template (e.g., `architecture/specs/svc-check-in.yaml`).

Required top-level structure:

```yaml
openapi: 3.0.3
info:
  title: NovaTrek {Service Display Name}
  description: |
    One to three sentence description of what this service does,
    which services it coordinates with, and its primary role.
  version: 1.0.0
  contact:
    name: NovaTrek {Team Name} Team
    email: {team}@novatrek.example.com

servers:
  - url: https://api.novatrek.example.com/{service-path}/v1
    description: Production

security:
  - BearerAuth: []

paths:
  # Define all endpoints here
  /{resource}:
    get:
      operationId: list{Resources}
      summary: List all {resources}
      # ...

tags:
  - name: {Primary Resource}
    description: Operations on {primary resource}

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    # Define all request/response schemas

  responses:
    BadRequest:
      description: Invalid request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    Unauthorized:
      description: Missing or invalid authentication token
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    Error:
      type: object
      required: [code, message]
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: object
```

See [API Contract Changes](api-contracts.md) for guidance on writing individual endpoints and schemas.

---

## Step 2 — Assign the Service to a Domain

Open `architecture/metadata/domains.yaml` and add the service to the appropriate domain. If the service does not fit an existing domain, add a new domain block.

```yaml
# Adding to an existing domain
Operations:
  color: '#2563eb'
  light: '#DBEAFE'
  icon: clipboard-check
  services:
    - svc-check-in
    - svc-scheduling-orchestrator
    - svc-adventure-tracking     # ← new service

# Adding a new domain (if needed)
Sustainability:
  color: '#16a34a'
  light: '#DCFCE7'
  icon: leaf
  services:
    - svc-carbon-tracking        # ← new domain + service
```

**Domain selection guidelines:**

| Domain | Purpose |
|---|---|
| Operations | Day-of-adventure execution: check-in, scheduling |
| Guest Identity | Guest profiles and identity |
| Booking | Reservations and availability |
| Product Catalog | Adventures, trips, trails |
| Safety | Compliance, waivers, emergency response |
| Logistics | Transport, gear |
| Guide Management | Guide assignments and preferences |
| External | Partner integrations |
| Support | Cross-cutting: notifications, payments, loyalty, analytics, media, weather, location |

When in doubt, place the service in the domain whose primary responsibility it supports.

---

## Step 3 — Document the Data Store

Add the service's database configuration to `architecture/metadata/data-stores.yaml`:

```yaml
svc-adventure-tracking:
  engine: PostgreSQL 15
  schema: tracking
  tables:
    - tracking_sessions
    - location_pings
  features:
    - Index on guest_id and session_start
    - Partitioned by day for high-volume location data
  volume: ~50,000 pings/day active season
  connection_pool:
    min: 3
    max: 15
    idle_timeout: 10min
  backup: Continuous WAL archiving, daily base backup, 7-day PITR
  table_details:
    tracking_sessions:
      description: Active adventure tracking sessions
      columns:
        - name: session_id
          type: UUID
          constraints: PK, DEFAULT gen_random_uuid()
        - name: reservation_id
          type: UUID
          constraints: NOT NULL
        - name: guest_id
          type: UUID
          constraints: NOT NULL
        - name: started_at
          type: TIMESTAMPTZ
          constraints: NOT NULL, DEFAULT NOW()
        - name: ended_at
          type: TIMESTAMPTZ
          constraints: NULL
        - name: status
          type: VARCHAR(20)
          constraints: NOT NULL, DEFAULT 'active'
        - name: created_at
          type: TIMESTAMPTZ
          constraints: NOT NULL, DEFAULT NOW()
      indexes:
        - name: idx_tracking_guest
          columns: guest_id, started_at DESC
        - name: idx_tracking_reservation
          columns: reservation_id
```

If the service does not have a database (e.g., it is a pure pass-through), omit it from `data-stores.yaml` entirely — the generator skips services with no entry.

See [Database Changes](database-changes.md) for full column and index syntax.

---

## Step 4 — Register Cross-Service Integrations

For every endpoint that calls another service, add an entry to `architecture/metadata/cross-service-calls.yaml`:

```yaml
svc-adventure-tracking:
  POST /tracking-sessions:
    - alias: Res
      label: Reservations
      action: Verify reservation exists and is active
      async: false
      target:
        method: GET
        path: /reservations/{reservation_id}
    - alias: GP
      label: Guest Profiles
      action: Verify guest identity
      async: false
      target:
        method: GET
        path: /guests/{guest_id}
```

**Field reference:**

| Field | Description |
|---|---|
| `alias` | Short label used in sequence diagram participant boxes (2-4 characters) |
| `label` | Full display name for the target service |
| `action` | Verb phrase describing why the call is made |
| `async` | `true` for event publishing, `false` for synchronous REST calls |
| `target.method` | HTTP method of the target endpoint |
| `target.path` | Path on the target service |

---

## Step 5 — Map Capabilities

If the new service introduces new capabilities or enhances existing ones, update `architecture/metadata/capabilities.yaml`:

```yaml
domains:
  - id: CAP-3
    name: Safety and Compliance
    capabilities:
      # ... existing ...
      - id: CAP-3.4
        name: Real-Time Adventure Tracking         # ← new capability
        status: implemented
        services: [svc-adventure-tracking]
        description: GPS-based live location tracking for active adventure participants
```

Then add the capability change to `capability-changelog.yaml` — this is required for every solution that introduces a new service:

```yaml
entries:
  - ticket: NTK-10006
    date: 2026-03-15
    solution: _NTK-10006-real-time-adventure-tracking
    summary: New svc-adventure-tracking service for GPS location monitoring
    capabilities:
      - id: CAP-3.4
        impact: new
        description: New capability providing real-time GPS tracking for active adventure participants
        l3_capabilities:
          - name: Live Location Tracking
            description: GPS coordinates streamed from guest devices during active adventures
```

---

## Step 6 — Add to Portal Navigation

Open `portal/mkdocs.yml` and add the new service to the nav under `Services > Microservices`:

```yaml
nav:
  - Services:
    - Microservices:
      - microservices/index.md
      # ... existing services ...
      - svc-adventure-tracking: microservices/svc-adventure-tracking.md
```

Note: The actual page file (`portal/docs/microservices/svc-adventure-tracking.md`) is generated by `generate-microservice-pages.py`. You only need to add the nav entry.

---

## Step 7 — Run Generators

```bash
bash portal/scripts/generate-all.sh
```

This generates:
- `portal/docs/microservices/svc-{name}.md` — the service deep-dive page
- `portal/docs/services/api/svc-{name}.html` — the Swagger UI page
- Updated sequence diagrams for all services that call the new service

Verify the output:
- `portal/docs/microservices/svc-adventure-tracking.md` exists and has content
- `portal/docs/services/api/svc-adventure-tracking.html` exists
- No generator errors in the console output

---

## Step 8 — Raise the PR

Follow the standard solution design PR process:

```bash
git add .
git commit -m "feat: add svc-adventure-tracking service"
git push -u origin solution/NTK-10006-real-time-adventure-tracking
```

---

## Service Registration Checklist

- [ ] OpenAPI spec created at `architecture/specs/svc-{name}.yaml`
- [ ] Service added to correct domain in `domains.yaml`
- [ ] Database schema documented in `data-stores.yaml` (or consciously omitted for stateless services)
- [ ] Cross-service calls registered in `cross-service-calls.yaml`
- [ ] Capabilities mapped in `capabilities.yaml` and `capability-changelog.yaml`
- [ ] Service added to `portal/mkdocs.yml` nav
- [ ] Generators run without errors
- [ ] New service page renders correctly in local portal build

---

!!! tip "Related guides"
    - [API Contract Changes](api-contracts.md) — writing OpenAPI endpoints and schemas
    - [Database Changes](database-changes.md) — adding the initial schema
    - [Events](events.md) — if the new service produces or consumes domain events
    - [Solution Design](solution-design.md) — the full solution design workflow
    - [Metadata Registry](../standards/metadata-registry/index.md) — full YAML structure reference
