# ADR-008: Temporary Guest Profile Creation

## Status

Accepted

## Date

2026-01-30

## Context and Problem Statement

The kiosk check-in flow requires a guest profile ID for session management, waiver association, and analytics. Unregistered guests do not have NovaTrek accounts. Should they be required to register, or should the system accommodate them with temporary profiles?

## Decision Drivers

- Reducing friction is the primary goal of the feature
- The staff-assisted flow is slow precisely because it involves data collection
- Post-check-in registration prompts are more effective than pre-check-in registration gates
- Data retention policies require PII cleanup for unclaimed profiles

## Considered Options

1. **Require full account registration** — Guest must register before kiosk access
2. **Temporary guest profile** — Create a minimal profile with only last name and reservation ID

## Decision Outcome

**Chosen Option**: "Temporary guest profile", because requiring full registration defeats the purpose of reducing friction, and a post-check-in registration prompt ("Want faster check-in next time?") is more effective.

### Confirmation

- svc-guest-profiles supports `TEMPORARY` profile type with reduced required fields
- 90-day anonymization job implemented and monitored
- Profile merge logic handles conversion from temporary to full account

## Consequences

### Positive

- Minimal friction — only last name and reservation ID needed
- Enables post-check-in registration prompt with higher conversion potential (35-45% vs 12%)
- Automatic 90-day anonymization satisfies data retention policies
- Profile merge preserves check-in history when guest later creates a full account

### Negative

- svc-guest-profiles must support a new `TEMPORARY` profile type with reduced required fields
- Background anonymization job must be built and monitored
- Profile merge logic must handle edge cases (multiple temporary profiles across visits)

## More Information

- Origin: [NTK-10003 Solution Design](../phase-1-ai-tool-cost-comparison/workspace/work-items/tickets/_NTK-10003-unregistered-guest-self-checkin/NTK-10003-solution-design.md)
- Services: [svc-guest-profiles](../services/svc-guest-profiles.md), [svc-check-in](../services/svc-check-in.md)
