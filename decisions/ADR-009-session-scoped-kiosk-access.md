# ADR-009: Session-Scoped Kiosk Access with 30-Minute Expiry

## Status

Accepted

## Date

2026-02-05

## Context and Problem Statement

Temporary kiosk access must be time-bounded to prevent misuse and ensure kiosk availability for other guests. What is the appropriate session duration?

## Decision Drivers

- 95% of registered guest check-ins complete within 12 minutes
- First-time waiver completion takes up to 20 minutes
- Kiosk availability must not be blocked by abandoned sessions
- JWT tokens with embedded expiry are self-validating (no server-side lookup per request)

## Considered Options

1. **15-minute session** — Tight, efficient
2. **30-minute session** — Comfortable buffer
3. **No fixed expiry** — Session ends on completion or navigation away

## Decision Outcome

**Chosen Option**: "30-minute session", because it provides comfortable buffer for first-time waiver completion while preventing indefinite kiosk occupation.

### Confirmation

- JWT issued with 30-minute `exp` claim
- One active session per kiosk device enforced
- Kiosk UI displays countdown timer when under 5 minutes remain
- Integration tests verify session expiry and re-verification flow

## Consequences

### Positive

- 30 minutes comfortably covers even the slowest check-in scenarios (waiver + gear + briefing)
- JWT with embedded expiry is self-validating — no per-request session lookup needed
- One active session per kiosk device prevents session stacking

### Negative

- Guests exceeding 30 minutes must re-verify (expected to be rare)
- Kiosk UI must display countdown timer when under 5 minutes remain

## More Information

- Origin: [NTK-10003 Solution Design](../phase-1-ai-tool-cost-comparison/workspace/work-items/tickets/_NTK-10003-unregistered-guest-self-checkin/NTK-10003-solution-design.md)
- Service: [svc-check-in](../services/svc-check-in.md)
