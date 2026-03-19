# ADR-006: Orchestrator Pattern for Self-Service Check-In

## Status

Accepted

## Date

2025-01-28

## Context and Problem Statement

The unregistered guest check-in flow (NTK-10003) requires coordinating calls across four services: svc-check-in, svc-reservations, svc-guest-profiles, and svc-safety-compliance. A guest arriving at the kiosk without a pre-registered account must have their reservation looked up, a temporary profile created, waiver status verified, and check-in initiated -- all within a single user-facing interaction. How should this multi-service coordination be orchestrated?

## Decision Drivers

- Consistency guarantees: the check-in flow must either complete fully or roll back cleanly -- partial check-ins create safety gaps
- Error handling: failures at any step must produce actionable feedback to the guest and operational staff
- Operational visibility: administrators need to trace the full check-in flow across services for troubleshooting
- Latency: the kiosk interaction must complete within a few seconds to maintain guest satisfaction

## Considered Options

1. **Orchestration** -- svc-check-in acts as the central coordinator, making synchronous calls to each downstream service in sequence
2. **Choreography** -- services communicate via events on Kafka; each service reacts to the previous step's completion event
3. **Hybrid** -- synchronous orchestration for the critical path (reservation lookup, profile creation, check-in), async events for non-critical side effects (notifications, analytics)

## Decision Outcome

**Chosen Option**: "Orchestration", because the self-service check-in flow is a user-facing, latency-sensitive operation where the guest is waiting at the kiosk. Synchronous orchestration through svc-check-in provides deterministic sequencing, clear error attribution, and the ability to return a coherent response to the kiosk within a single request-response cycle.

### Confirmation

- svc-check-in owns the `POST /check-ins/self-service/unregistered` endpoint that coordinates the full flow
- Each downstream call (reservation lookup, profile creation, waiver check) has explicit error handling with guest-friendly messages
- Distributed tracing via correlation ID propagated through all service calls

## Consequences

### Positive

- Single point of orchestration simplifies debugging -- the full flow is visible in svc-check-in logs
- Error handling is centralized: each step's failure produces a specific, actionable kiosk message
- Consistent with svc-check-in's existing role as the day-of-adventure workflow coordinator
- Correlation ID propagation enables end-to-end tracing across all four services

### Negative

- svc-check-in becomes a coupling point -- changes to downstream service contracts require svc-check-in updates
- Synchronous call chain means the flow's total latency is the sum of all service call latencies
- Temporary increase in svc-check-in's complexity as new orchestration logic is added

### Neutral

- Non-critical side effects (analytics events, notification dispatch) may still use async events, but the core flow remains synchronous

## Pros and Cons of the Options

### Orchestration

- **Good**, because deterministic flow sequencing with clear error attribution at each step
- **Good**, because single request-response cycle for the kiosk -- no polling or callbacks needed
- **Good**, because consistent with svc-check-in's established role as operations coordinator
- **Neutral**, because adds orchestration logic to svc-check-in
- **Bad**, because creates temporal coupling -- all four services must be available simultaneously

### Choreography

- **Good**, because loose coupling -- each service reacts independently to events
- **Bad**, because eventual consistency is unacceptable for a user-facing kiosk flow
- **Bad**, because error handling becomes distributed -- no single service can report a coherent failure to the guest
- **Bad**, because debugging requires correlating events across four service logs

### Hybrid

- **Good**, because balances consistency for critical steps with decoupling for side effects
- **Neutral**, because adds complexity of maintaining both sync and async patterns
- **Bad**, because the critical path is still synchronous, negating the primary choreography benefit

## More Information

- Origin: NTK-10003 Solution Design (unregistered guest self-service check-in)
- Services: svc-check-in (orchestrator), svc-reservations, svc-guest-profiles, svc-safety-compliance
- Related: [ADR-007 Four-Field Identity Verification](ADR-007-four-field-identity-verification.md), [ADR-008 Temporary Guest Profile](ADR-008-temporary-guest-profile.md)
