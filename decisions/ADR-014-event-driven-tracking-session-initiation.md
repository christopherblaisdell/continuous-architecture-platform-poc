# ADR-014: Event-Driven Tracking Session Initiation

## Status

Proposed

## Date

2026-03-20

## Context and Problem Statement

When a guest completes check-in and receives their GPS-enabled wristband (NTK-10005), a tracking session must be created in svc-adventure-tracking. The question is how svc-check-in communicates the check-in completion to the tracking service: synchronously (REST call) or asynchronously (Kafka event consumption).

## Decision Drivers

- Domain boundary respect: svc-check-in (Operations) and svc-adventure-tracking (Safety) are in different domains; event-driven integration is preferred between domains
- Check-in reliability: adding a synchronous dependency on a new service increases check-in failure risk
- Extensibility: other services may need to react to check-in completion in the future
- The `checkin.completed` Kafka event already exists in the event catalog

## Considered Options

### Option A: Synchronous REST Call

svc-check-in calls `POST /tracking-sessions` on svc-adventure-tracking directly.

- Good, because it provides immediate confirmation of session creation
- Bad, because it couples Operations to Safety domain synchronously
- Bad, because check-in fails if svc-adventure-tracking is unavailable
- Bad, because it increases svc-check-in's blast radius (already 7 downstream services)

### Option B: Kafka Event Consumption

svc-adventure-tracking subscribes to the existing `checkin.completed` event.

- Good, because zero coupling between svc-check-in and svc-adventure-tracking
- Good, because check-in reliability is unaffected by tracking service availability
- Good, because it leverages existing event infrastructure
- Good, because other future consumers can subscribe without modifying svc-check-in
- Bad, because tracking session creation is eventually consistent (1-3 second lag)
- Bad, because requires dead-letter queue for failed event consumption

## Decision Outcome

**Option B: Kafka Event Consumption.** svc-adventure-tracking subscribes to `checkin.completed` and creates tracking sessions asynchronously. This is consistent with ADR-006 (orchestrator pattern) and the cross-domain communication guidelines.

## Consequences

### Positive

- svc-check-in's blast radius does not increase
- Tracking can be deployed and rolled back independently
- Other consumers can subscribe to the same event

### Negative

- Tracking session creation is eventually consistent (expected lag: 1-3 seconds)
- Dead-letter queue and alerting required for failed event consumption

### Neutral

- The `checkin.completed` event schema must include `wristband_nfc_id` (added by NTK-10005)
