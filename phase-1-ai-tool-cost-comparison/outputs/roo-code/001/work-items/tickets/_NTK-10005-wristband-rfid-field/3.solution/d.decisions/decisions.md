# NTK-10005 - Decisions

## Classification Decision

**Classification: Code-Level Task with Light Architecture Review**

This ticket does not require a full architecture decision record. The change is additive, affects a single service (svc-check-in), introduces no new cross-service interactions, and follows existing patterns already established in the svc-check-in domain.

### Rationale

1. **Single service scope**: Only svc-check-in is modified. No new service-to-service communication patterns, no new event topics, and no new infrastructure components are introduced.

2. **Additive schema change**: Adding an optional, nullable field to an existing schema is backward-compatible. No existing API consumers break. Downstream event consumers using tolerant reader patterns safely ignore the new field.

3. **Existing pattern**: The `WristbandAssignment` sub-schema already contains `rfid_tag` as a required field (see svc-check-in.yaml, `WristbandAssignment` schema). This ticket promotes that data to the top-level `CheckIn` schema for direct lookup, following the same data capture pattern.

4. **No competing architectural approaches**: The implementation path is straightforward -- add a field to the schema, add input validation, add a partial uniqueness database constraint, and add an optional query parameter. There are no trade-offs that require formal architectural deliberation.

### Architecture Review Touchpoints

While no formal MADR ADR is warranted, the following points should be reviewed during the Swagger spec PR before merge:

| Touchpoint | Review Item | Reviewer |
|------------|-------------|----------|
| Schema compatibility | Confirm `rfid_tag` on `CheckIn` is optional and nullable so existing check-ins without RFID remain valid | API Review |
| Uniqueness scope | Confirm uniqueness constraint is scoped to active check-ins only (status not COMPLETED or FAILED) | Data Review |
| Event schema | Confirm check-in domain event includes `rfid_tag` at the top level for downstream consumers | Event Review |
| RFID format | Confirm regex pattern `^[A-F0-9]{8,16}$` matches the hardware team kiosk firmware RFID output | Hardware Team |
| Query parameter interaction | Confirm `GET /check-ins` behavior when both `reservation_id` and `rfid_tag` are provided | API Review |

### Disposition

No MADR ADR created. Ticket routed to the svc-check-in development team for implementation with architecture review at the Swagger specification PR stage.
