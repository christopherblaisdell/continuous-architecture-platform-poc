---
tags:
  - handbook
  - events
  - kafka
  - asyncapi
---

<!-- PUBLISH -->

<div class="hero" markdown>

# Events

<p class="subtitle">How to add and modify domain events — AsyncAPI specs, event catalog metadata, and consumer registration</p>

</div>

NovaTrek uses Apache Kafka for asynchronous inter-service communication. Every domain event is defined in two places: an **AsyncAPI spec** (the schema contract) and the **events catalog** (the integration topology). This guide covers how to add a new event, modify an existing one, and register or remove consumers.

---

## Overview

Events are defined and maintained in:

| File | Purpose |
|---|---|
| `architecture/events/svc-{name}.events.yaml` | AsyncAPI 3.0 spec — message schema, channel, payload for one producer |
| `architecture/metadata/events.yaml` | Event catalog — channels, producers, consumers, triggers for all events |

Both files must be updated together. The AsyncAPI spec defines **what** the event payload looks like; the catalog defines **who** publishes it and **who** subscribes.

```
Architect edits events.yaml + AsyncAPI spec
     │
     ▼
CI runs generate-event-pages.py
  → portal/docs/events-ui/svc-{name}.html  (AsyncAPI UI page)
CI runs generate-microservice-pages.py
  → portal/docs/events/index.md             (Event Catalog page updated)
  → sequence diagrams updated for producers and consumers
```

---

## Adding a New Event

### Step 1 — Update the Event Catalog

Open `architecture/metadata/events.yaml` and add the new event:

```yaml
tracking.session_started:
  channel: novatrek.safety.tracking.session-started
  producer: svc-adventure-tracking
  trigger:
    method: POST
    path: /tracking-sessions
  consumers:
    - svc-analytics
    - svc-notifications
  domain: Safety
  summary: Published when a guest's adventure tracking session begins
```

**Event name convention:** `{entity}.{past_tense_verb}` using dot notation (e.g., `reservation.created`, `checkin.completed`).

**Channel naming convention:** `novatrek.{domain-kebab}.{entity}.{verb-kebab}`

| Part | Example |
|---|---|
| Prefix | `novatrek` |
| Domain (kebab-case) | `guest-identity`, `operations`, `safety`, `booking`, `support` |
| Entity | `checkin`, `reservation`, `guest`, `payment`, `tracking` |
| Verb (past tense) | `completed`, `created`, `registered`, `processed` |

**Required fields:**

| Field | Description |
|---|---|
| `channel` | Kafka topic name — unique across all events |
| `producer` | Service name of the publisher (one producer per event) |
| `trigger.method` | HTTP method of the API call that triggers the event |
| `trigger.path` | API path that triggers the event |
| `consumers` | List of services that subscribe (can be empty) |
| `domain` | Domain label matching an entry in `domains.yaml` |
| `summary` | One-sentence description of when the event fires |

### Step 2 — Create or Update the AsyncAPI Spec

If this is the **producer service's first event**, create a new AsyncAPI spec file:

```
architecture/events/svc-adventure-tracking.events.yaml
```

If the **producer service already publishes other events**, add to its existing spec file.

#### New spec file template

```yaml
asyncapi: 3.0.0
info:
  title: svc-adventure-tracking Events
  version: 1.0.0
  description: Domain events published by the NovaTrek Adventure Tracking Service
  contact:
    name: NovaTrek Safety and Compliance Team

defaultContentType: application/json

channels:
  trackingSessionStarted:
    address: novatrek.safety.tracking.session-started
    messages:
      trackingSessionStarted:
        $ref: '#/components/messages/TrackingSessionStarted'

operations:
  publishTrackingSessionStarted:
    action: send
    channel:
      $ref: '#/channels/trackingSessionStarted'
    summary: Published when a guest's adventure tracking session begins

components:
  messages:
    TrackingSessionStarted:
      name: TrackingSessionStarted
      title: Tracking Session Started
      summary: A guest has started a tracked adventure
      contentType: application/json
      payload:
        $ref: '#/components/schemas/TrackingSessionStartedPayload'

  schemas:
    TrackingSessionStartedPayload:
      type: object
      required:
        - event_id
        - event_type
        - timestamp
        - session_id
        - reservation_id
        - guest_id
      properties:
        event_id:
          type: string
          format: uuid
          description: Unique identifier for this event instance
        event_type:
          type: string
          const: tracking.session_started
        timestamp:
          type: string
          format: date-time
          description: ISO 8601 timestamp when the event occurred
        session_id:
          type: string
          format: uuid
          description: ID of the tracking session
        reservation_id:
          type: string
          format: uuid
          description: ID of the associated reservation
        guest_id:
          type: string
          format: uuid
          description: ID of the guest whose session started
        trip_id:
          type: string
          format: uuid
          description: ID of the booked trip
        adventure_category:
          type: string
          description: Category of the adventure being tracked
        started_at:
          type: string
          format: date-time
          description: When the tracking session began
```

#### Required payload fields (all NovaTrek events)

Every event payload must include these standard envelope fields:

| Field | Type | Description |
|---|---|---|
| `event_id` | `string (uuid)` | Unique identifier for deduplication |
| `event_type` | `string (const)` | The event name (e.g., `tracking.session_started`) |
| `timestamp` | `string (date-time)` | ISO 8601 when the event occurred |

Beyond the envelope, include all entity IDs relevant to the event context (reservation ID, guest ID, etc.).

#### Adding a second event to an existing spec

If the producer service already has an AsyncAPI spec, add a new channel, operation, message, and schema:

```yaml
channels:
  # ... existing channels ...
  trackingSessionEnded:
    address: novatrek.safety.tracking.session-ended
    messages:
      trackingSessionEnded:
        $ref: '#/components/messages/TrackingSessionEnded'

operations:
  # ... existing operations ...
  publishTrackingSessionEnded:
    action: send
    channel:
      $ref: '#/channels/trackingSessionEnded'
    summary: Published when a guest's adventure tracking session ends

components:
  messages:
    # ... existing messages ...
    TrackingSessionEnded:
      # ...
  schemas:
    # ... existing schemas ...
    TrackingSessionEndedPayload:
      # ...
```

---

## Adding a Consumer to an Existing Event

To register a new service as a consumer of an existing event:

### 1. Update `events.yaml`

```yaml
checkin.completed:
  channel: novatrek.operations.checkin.completed
  producer: svc-check-in
  trigger:
    method: POST
    path: /check-ins
  consumers:
    - svc-analytics
    - svc-notifications
    - svc-adventure-tracking     # ← new consumer
  domain: Operations
  summary: Published when a guest completes the check-in process
```

### 2. Update the consumer registration metadata (if applicable)

If `architecture/metadata/consumers.yaml` is used to document what consumers do with events, add the new subscription:

```yaml
svc-adventure-tracking:
  subscribes:
    - event: checkin.completed
      purpose: Automatically start a tracking session when a guest checks in
```

No changes to the AsyncAPI spec are needed — the AsyncAPI spec belongs to the producer, not the consumer.

---

## Modifying an Existing Event

### Modifying the schema (non-breaking — adding fields)

Adding optional fields to an existing event payload is backward compatible. Existing consumers will ignore fields they do not expect.

1. Add the field to the schema in the producer's AsyncAPI spec:

```yaml
    TrackingSessionStartedPayload:
      properties:
        # ... existing fields ...
        guide_id:                    # ← new optional field
          type: string
          format: uuid
          nullable: true
          description: |
            ID of the assigned guide for this adventure.
            Null for self-guided adventures.
```

2. Bump the spec version: `version: 1.1.0`

### Modifying the schema (breaking — changing or removing fields)

Removing or renaming a required field is a breaking change that will break all existing consumers.

Process:
1. Assess all consumers listed in `events.yaml` — each consumer team must be notified
2. Introduce the change with a new event name (e.g., `tracking.session_started.v2`) on a new channel
3. Run both the old and new events in parallel during the migration period
4. After all consumers have migrated, deprecate the old event by adding `deprecated: true` to the catalog entry:

```yaml
tracking.session_started:
  deprecated: true
  summary: "[DEPRECATED — use tracking.session_started.v2] Published when a session begins"
```

5. Remove the old event entry after all consumers confirm they have migrated

### Changing the trigger endpoint

If the API endpoint that triggers the event changes (e.g., path or method changes), update both `events.yaml` and the OpenAPI spec:

```yaml
tracking.session_started:
  trigger:
    method: POST
    path: /tracking-sessions/start    # ← was /tracking-sessions
```

---

## Removing an Event

1. Verify all consumers — check `events.yaml` consumers list
2. Notify all consumer teams; agree on a migration date
3. Mark the event `deprecated: true` in `events.yaml` first (at least one release cycle before removal)
4. After consumer migration is confirmed:
   - Remove the event entry from `events.yaml`
   - Remove the channel, operation, message, and schema from the AsyncAPI spec
   - Remove the AsyncAPI spec file entirely if it was the only event

---

## Running the Generators

After updating events files:

```bash
# Full regeneration
bash portal/scripts/generate-all.sh

# Event pages only (faster)
python3 portal/scripts/generate-event-pages.py

# Microservice pages (needed if integration topology changed)
python3 portal/scripts/generate-microservice-pages.py
```

Review the output:
- `portal/docs/events-ui/svc-{name}.html` — AsyncAPI UI page
- `portal/docs/events/index.md` — updated event catalog

---

## Event Checklist

- [ ] New event added to `architecture/metadata/events.yaml` with all required fields
- [ ] Channel name follows `novatrek.{domain}.{entity}.{verb}` convention
- [ ] AsyncAPI spec created or updated with new channel, operation, message, and schema
- [ ] Standard envelope fields (`event_id`, `event_type`, `timestamp`) present in payload
- [ ] All consumers registered in `events.yaml`
- [ ] Spec version bumped
- [ ] Generators run without errors
- [ ] Event appears in Event Catalog portal page

---

!!! tip "Related guides"
    - [Adding a Service](adding-a-service.md) — when the new event comes from a new service
    - [API Contract Changes](api-contracts.md) — the trigger endpoint needs to be in the OpenAPI spec
    - [Event Catalog](../events/index.md) — portal view of all published events
