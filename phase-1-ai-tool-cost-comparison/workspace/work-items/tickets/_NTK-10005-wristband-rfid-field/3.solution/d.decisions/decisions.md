# NTK-10005 - Decisions

## Classification Decision

**Classification: Code-Level Task with Light Architecture Review**

This ticket does not require a full architecture decision record. The change is additive, affects a single service, introduces no new cross-service interactions, and follows existing patterns already established in the svc-check-in domain.

### Rationale

1. **Single service scope**: Only svc-check-in is modified. No new service-to-service communication, no new event topics, no new infrastructure.
2. **Additive schema change**: Adding an optional field to an existing schema is backward-compatible. No existing consumers break.
3. **Existing pattern**: The `WristbandAssignment` sub-schema already contains `rfid_tag`. This ticket promotes it to the top-level `CheckIn` schema for direct lookup convenience.
4. **No competing architectural approaches**: The implementation path is straightforward -- add a field, add validation, add a uniqueness constraint, add a query parameter.

### Architecture Review Touchpoints

While no formal ADR is warranted, the following points should be reviewed before merge:

| Touchpoint | Review Item | Reviewer |
|------------|-------------|----------|
| Schema compatibility | Confirm `rfid_tag` on `CheckIn` is optional and nullable so existing check-ins without RFID remain valid | API Review |
| Uniqueness scope | Confirm uniqueness constraint is scoped to active check-ins only (status not COMPLETE or CANCELLED) | Data Review |
| Event schema | Confirm check-in domain event includes `rfid_tag` at the top level for downstream consumers | Event Review |
| RFID format | Confirm regex pattern `^[A-F0-9]{8,16}$` matches hardware team output (kiosk firmware ships May 2026) | Hardware Team |

### Disposition

No MADR ADR created. Routed to svc-check-in development team for implementation with architecture review at the Swagger spec PR stage.
