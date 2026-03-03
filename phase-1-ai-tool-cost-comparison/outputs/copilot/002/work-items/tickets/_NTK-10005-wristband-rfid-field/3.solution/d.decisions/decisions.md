# NTK-10005: Classification Decision

## Status

Proposed

## Date

2026-03-03

## Context and Problem Statement

NTK-10005 requests adding an `rfid_tag` field to the check-in record schema and supporting RFID-based lookups. The question is whether this ticket represents an architecturally significant change or a routine code-level task.

## Classification

**Classification: Code-Level Task (Not Architecturally Significant)**

## Reasoning

### Factors Supporting Code-Level Classification

1. **Additive schema change**: Adding an optional field to an existing schema is a non-breaking, backward-compatible change. It does not alter the service boundary, introduce new service dependencies, or change the interaction pattern between services.

2. **No new service interactions**: The change is scoped entirely to `svc-check-in`. No new inter-service calls, protocols, or coordination mechanisms are introduced.

3. **Existing pattern**: The `WristbandAssignment` schema already contains an `rfid_tag` field. This ticket extends the same pattern to make RFID data accessible earlier in the check-in flow and queryable.

4. **No infrastructure changes**: No new databases, message queues, caches, or deployment topology changes are required.

5. **No quality attribute impact**: The change does not materially affect system performance, scalability, security posture, or availability characteristics.

### Factors That Were Considered But Do Not Elevate to Architectural

1. **Downstream event consumers**: While downstream services will receive the new field, it is additive and does not require them to change. This is a standard schema evolution scenario, not an architectural concern.

2. **Uniqueness constraint**: A unique index on `rfid_tag` per active check-in is a data-layer implementation detail, not an architectural decision.

3. **Query endpoint enhancement**: Adding a filter parameter to an existing endpoint is a routine API enhancement.

## Recommendation

This ticket should proceed as a standard development task. No Architecture Decision Record is required. The implementation team should:
- Add the optional `rfid_tag` field to the `CheckIn` schema
- Add `rfid_tag` query parameter to `GET /check-ins`
- Validate format and uniqueness per active check-in
- Ensure the field propagates in check-in events

Standard code review and API contract review processes are sufficient governance for this change.
