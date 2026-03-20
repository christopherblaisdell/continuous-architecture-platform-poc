<!-- PUBLISH -->

# NTK-10006 Decisions

## ADR-014: Event-Driven Tracking Session Initiation

### Status

Proposed

### Date

2026-03-20

### Context and Problem Statement

When a guest completes check-in and receives their GPS-enabled wristband, a tracking session must be created in svc-adventure-tracking. The question is how svc-check-in communicates the check-in completion to the tracking service: synchronously (svc-check-in calls svc-adventure-tracking's API directly) or asynchronously (svc-check-in publishes a Kafka event that svc-adventure-tracking consumes).

This decision affects the coupling between the Operations and Safety domains, the failure behavior of check-in, and the extensibility of the check-in completion trigger.

### Decision Drivers

- **Domain boundary respect** — svc-check-in (Operations) and svc-adventure-tracking (Safety) are in different domains; cross-domain communication should prefer loose coupling (copilot-instructions.md: "Event-driven integration is preferred between domains")
- **Check-in reliability** — check-in is a critical guest-facing operation; adding a synchronous dependency on a new service increases the risk of check-in failures
- **Extensibility** — other services may need to react to check-in completion in the future (analytics, guide notifications); a Kafka event supports multiple consumers without modifying svc-check-in
- **Latency tolerance** — tracking session creation is not time-sensitive to the millisecond; a few seconds of Kafka consumer lag is acceptable
- **Existing pattern** — svc-check-in already publishes `checkin.completed` to Kafka (defined in events.yaml); the event infrastructure exists

### Considered Options

#### Option A: Synchronous REST Call

svc-check-in calls `POST /tracking-sessions` on svc-adventure-tracking directly after completing check-in.

**Pros:**
- Immediate confirmation that tracking session was created
- Simple request/response; easy to debug

**Cons:**
- Tight coupling between Operations and Safety domains — violates domain boundary guidance
- Check-in fails or degrades if svc-adventure-tracking is unavailable
- Each new tracking-related consumer requires a code change in svc-check-in
- Increases svc-check-in's already large blast radius (7 downstream services)

#### Option B: Kafka Event Consumption (Recommended)

svc-adventure-tracking subscribes to the existing `checkin.completed` Kafka event and creates a tracking session asynchronously.

**Pros:**
- Zero coupling between svc-check-in and svc-adventure-tracking — check-in does not know tracking exists
- Check-in reliability is unaffected by tracking service availability
- Extensible: any future service can subscribe to `checkin.completed` without modifying svc-check-in
- Leverages existing event infrastructure (`novatrek.operations.checkin.completed` channel)
- Consistent with ADR-006 (orchestrator pattern) and cross-domain communication guidelines

**Cons:**
- Eventual consistency — tracking session creation may lag by a few seconds
- If check-in event is lost or consumer crashes, session may not be created (requires dead-letter queue and monitoring)
- Debugging requires Kafka tooling, not just HTTP traces

### Decision Outcome

**Option B: Kafka Event Consumption.**

The `checkin.completed` event already exists and carries the required data (guest_id, reservation_id, adventure_category). NTK-10005 added `wristband_nfc_id` to the check-in record, which must be included in the event payload. svc-adventure-tracking subscribes to this event and creates a tracking session without any modification to svc-check-in's code.

### Consequences

**Positive:**
- svc-check-in's blast radius does not increase (stays at 7 downstream)
- Tracking can be deployed and rolled back independently
- Other consumers (analytics, guide app) can subscribe to the same event

**Negative:**
- Tracking session creation is eventually consistent (expected lag: 1-3 seconds)
- Dead-letter queue and alerting required for failed event consumption

**Neutral:**
- The `checkin.completed` event schema must be verified to include `wristband_nfc_id` — if it does not, the schema must be extended (backward-compatible: new optional field)
