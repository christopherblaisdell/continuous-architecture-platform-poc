# ADR-005: Pattern 3 as Default Fallback for Unknown Categories

## Status

Accepted

## Date

2024-08-19

## Context and Problem Statement

Edge cases exist where the `adventure_category` field may be null, empty, or contain a value not recognized by the classification table. This could occur with legacy reservations predating the feature, or when a new category is added to svc-trip-catalog before the classification config is updated. What should the system do when it encounters an unknown or missing category?

## Decision Drivers

- Guest safety is the highest priority
- Operational staff prefer to over-service rather than under-service
- Unknown categories are expected to occur occasionally during the transition period
- The fallback must be deterministic and predictable

## Considered Options

1. **Default to Pattern 3 (Full Service)** — Safety-first, provide all check-in steps
2. **Default to Pattern 1 (Basic)** — Minimal friction, assume low-complexity
3. **Return an error** — Reject the check-in and require manual classification

## Decision Outcome

**Chosen Option**: "Default to Pattern 3 (Full Service)", because guest safety takes precedence over convenience, and over-servicing creates only minor inconvenience while under-servicing could create safety risks.

### Confirmation

- Unit tests verify fallback to Pattern 3 for null, empty, and unrecognized category values
- `checkin.classification.fallback.count` metric is tracked and alerted on

## Consequences

### Positive

- No guest will miss critical safety steps due to a classification gap
- Operational alignment: confirmed with operations team as the preferred approach
- Deterministic behavior: logs and monitoring clearly show when fallback is triggered

### Negative

- Guests with unmapped low-complexity categories experience an unnecessarily long check-in flow
- May cause minor guest frustration if fallback occurs frequently

### Neutral

- Monitoring via `checkin.classification.fallback.count` metric identifies categories needing mapping

## Pros and Cons of the Options

### Default to Pattern 3 (Full Service)

- **Good**, because no guest misses safety-critical steps
- **Good**, because aligned with operational safety-first principles
- **Neutral**, because adds a few minutes to check-in for misclassified guests
- **Bad**, because may cause minor frustration for simple-activity guests

### Default to Pattern 1 (Basic)

- **Good**, because minimal friction for guests — fastest possible check-in
- **Bad**, because could skip gear verification, safety briefing, or medical clearance for high-risk activities
- **Bad**, because creates safety liability if a guest on a complex activity bypasses safety steps

### Return an error

- **Good**, because forces correct classification before check-in proceeds
- **Bad**, because blocks the guest from checking in — creates a hard failure at the kiosk
- **Bad**, because requires staff intervention for every unmapped category

## More Information

- Origin: [NTK-10002 Solution Design](../phase-1-ai-tool-cost-comparison/workspace/work-items/tickets/_NTK-10002-adventure-category-classification/NTK-10002-solution-design.md)
- Service: [svc-check-in](../services/svc-check-in.md)
- Related: [ADR-004 Configuration-Driven Classification](ADR-004-configuration-driven-classification.md)
