# NTK-10005 - Decisions

## Classification Decision

**Classification: Code-Level Task with Light Architecture Review**

This ticket does not require a full architecture decision record. The change is additive, affects a single service, introduces no new cross-service interactions, and follows existing patterns established in the svc-check-in domain.

### Rationale

1. **Single service scope**: Only svc-check-in is modified. No new service-to-service communication, no new event topics, no new infrastructure components.
2. **Additive schema change**: Adding an optional field to an existing schema is backward-compatible. No existing consumers break.
3. **Existing pattern**: The `WristbandAssignment` sub-schema already contains `rfid_tag` as a required field. This ticket promotes it to the top-level `CheckIn` schema for direct lookup convenience, following the same data pattern.
4. **No competing architectural approaches**: The implementation path is straightforward -- add a field, add validation, add a uniqueness constraint, add a query parameter.

### Architecture Review Touchpoints

While no formal ADR is warranted, the following points should be reviewed before the implementation PR is merged:

| Touchpoint | Review Item | Reviewer | Priority |
|------------|-------------|----------|----------|
| Schema compatibility | Confirm `rfid_tag` on `CheckIn` is optional and nullable so existing check-ins without RFID remain valid | API Review | High |
| Uniqueness scope | Confirm uniqueness constraint is scoped to active check-ins only (status not COMPLETED, FAILED, CANCELLED) | Data Review | High |
| RFID format | Confirm regex pattern `^[A-F0-9]{8,16}$` matches hardware team kiosk firmware output. Note: existing `WristbandAssignment` example uses `RFID-A3F7B201` which includes a prefix not matched by this regex. | Hardware Team | High |
| Event schema | Confirm check-in domain event includes `rfid_tag` at top level for downstream consumers | Event Review | Medium |
| Query parameter interaction | Confirm that when `rfid_tag` query param is provided to `GET /check-ins`, `reservation_id` becomes optional (breaking change to current required constraint) | API Review | Medium |

### Disposition

No MADR ADR created. Routed to svc-check-in development team for implementation with architecture review at the Swagger spec PR stage.

### Open Items

| ID | Item | Owner | Status |
|----|------|-------|--------|
| OI-1 | RFID format discrepancy: existing WristbandAssignment example has `RFID-` prefix but proposed regex does not allow it | Hardware Team / Architecture | Open |
| OI-2 | Confirm whether `reservation_id` should become optional on `GET /check-ins` when `rfid_tag` is provided | API Review | Open |
| OI-3 | Confirm downstream event consumers (svc-guest-experience, svc-trail-management) use tolerant reader patterns | Integration Team | Open |
