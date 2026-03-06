# NTK-10005 - Impact Assessment

## Impact Summary

This change is confined to a single service (svc-check-in) with informational notifications to downstream event consumers. No cross-service orchestration changes, no new infrastructure, and no breaking changes to existing consumers.

## Impacted Components

| Component | Impact Type | Severity | Details |
|-----------|------------|----------|---------|
| svc-check-in (API schema) | Schema addition | Low | Add optional `rfid_tag` field to `CheckIn` response schema. Add `rfid_tag` query parameter to `GET /check-ins` endpoint. |
| svc-check-in (request validation) | Business logic | Low | Add RFID format validation (`^[A-F0-9]{8,16}$`) to the wristband assignment flow. Add active uniqueness check before accepting an RFID tag. |
| svc-check-in (data model) | Database migration | Low | Add nullable `rfid_tag` column to `check_in_records` table. Create a partial unique index on `rfid_tag` scoped to active check-ins (WHERE status NOT IN COMPLETED, FAILED, CANCELLED). |
| svc-check-in (event schema) | Event payload change | Low | Add `rfid_tag` field to the check-in domain event published to the event bus. |
| svc-check-in (GET /check-ins contract) | API parameter change | Medium | Making `reservation_id` optional when `rfid_tag` is provided is a minor contract change. Existing consumers that always send `reservation_id` are unaffected, but consumers relying on `reservation_id` being required in the spec may need notification. |

## Downstream Notification Required

The following services consume check-in domain events and should be notified of the new `rfid_tag` field. No code changes are required from any downstream team for this release.

| Consumer Service | Action Required | Timeline | Notes |
|------------------|----------------|----------|-------|
| svc-guest-experience | Notification only | Before deployment | Will receive `rfid_tag` in event payload. Can ignore until RFID-based guest experience features are implemented in a future phase. |
| svc-trail-management | Notification only | Before deployment | Will receive `rfid_tag` in event payload. May use for RFID-based checkpoint tracking at trail waypoints in a future phase. |

## Non-Impacted Components

All services not listed above are unaffected by this change. The modification is additive and backward-compatible. Consumers using tolerant reader or consumer-driven contract patterns will safely ignore the new field.

Specifically NOT impacted:
- svc-reservations (no schema or contract changes)
- svc-guest-profiles (no schema or contract changes)
- svc-safety-compliance (no schema or contract changes)
- svc-gear-inventory (no schema or contract changes)
- All other NovaTrek microservices

## Risk Assessment for Impacts

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Downstream consumer with strict schema validation rejects new event field | Low | Verify tolerant reader patterns before deployment. Notify consumer teams in advance. |
| RFID format mismatch between API regex and kiosk firmware output | Medium | Confirm regex with hardware team before finalizing Swagger spec change. |
| Partial unique index not supported on target database platform | Low | Test migration on staging environment. PostgreSQL supports partial indexes natively. |
