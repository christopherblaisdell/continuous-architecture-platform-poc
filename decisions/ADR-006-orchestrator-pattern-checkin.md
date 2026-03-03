# ADR-006: Orchestrator Pattern in svc-check-in

## Status

Accepted

## Date

2026-01-29

## Context and Problem Statement

The unregistered guest reservation lookup flow requires coordination across 4-5 downstream services (svc-reservations, svc-guest-profiles, svc-safety-compliance, svc-gear-inventory, and optionally svc-partner-integrations). The flow includes conditional branching (partner fallback), parallel execution (safety + gear checks), and session creation. Where should this orchestration logic live?

## Decision Drivers

- Domain cohesion: check-in domain logic should be co-located
- Testability: orchestration logic with branching and parallelism must be unit-testable
- Separation of concerns: API gateway should handle cross-cutting concerns, not business logic
- Team ownership: svc-check-in team already owns the registered guest check-in flow

## Considered Options

1. **Orchestration in svc-check-in** — Service-level orchestrator
2. **Orchestration at API gateway** — Gateway composition

## Decision Outcome

**Chosen Option**: "Orchestration in svc-check-in", because it keeps domain logic cohesive within the service that owns the check-in flow, enables proper unit testing of conditional branching and parallel execution, and keeps the API gateway focused on cross-cutting concerns.

### Confirmation

- Orchestration logic implemented in `UnregisteredCheckInOrchestrator` class within svc-check-in
- Unit tests cover all branching paths (partner fallback, parallel safety + gear)
- API gateway routes only — no business logic

## Consequences

### Positive

- Domain logic remains cohesive in the service that already owns registered guest check-in
- Complex branching (partner fallback) and parallel execution (safety + gear) are expressed in application code, making them testable and debuggable
- API gateway remains clean — handles only rate limiting, authentication, and routing

### Negative

- svc-check-in takes on additional complexity and 5 new downstream dependencies
- Circuit breaker patterns must be implemented in application code for partner integration fallback
- The svc-check-in team must maintain knowledge of downstream service contracts

## More Information

- Origin: [NTK-10003 Solution Design](../phase-1-ai-tool-cost-comparison/workspace/work-items/tickets/_NTK-10003-unregistered-guest-self-checkin/NTK-10003-solution-design.md)
- Services: [svc-check-in](../services/svc-check-in.md), [svc-reservations](../services/svc-reservations.md), [svc-guest-profiles](../services/svc-guest-profiles.md)
- Orchestration diagram: [lookup-orchestration.puml](../phase-1-ai-tool-cost-comparison/workspace/work-items/tickets/_NTK-10003-unregistered-guest-self-checkin/3.solution/i.impacts/impact.1/lookup-orchestration.puml)
