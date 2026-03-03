# NTK-10005 - Impact Assessment

## Impacted Components

| Component | Impact Type | Severity | Details |
|-----------|------------|----------|---------|
| svc-check-in (API schema) | Schema addition | Low | Add optional `rfid_tag` field to the `CheckIn` response schema. Add optional `rfid_tag` query parameter to the `GET /check-ins` endpoint for RFID-based lookup. |
| svc-check-in (data model) | Database migration | Low | Add nullable `rfid_tag` VARCHAR(64) column to the `check_in_records` table. Create partial unique index `idx_rfid_tag_active` on `rfid_tag` scoped to active check-ins (status not in COMPLETED, FAILED). |
| svc-check-in (event schema) | Event payload change | Low | Add `rfid_tag` field to the check-in domain event published to the event bus. Field is nullable and optional. |
| svc-check-in (validation logic) | Business logic | Low | Add RFID format validation using regex `^[A-F0-9]{8,16}$`. Add active uniqueness check on `rfid_tag` to prevent two active check-ins from sharing the same RFID tag. |
| svc-check-in (query logic) | API behavior | Low | Modify `GET /check-ins` endpoint to support lookup by `rfid_tag` query parameter. Change `reservation_id` from required to conditionally required (at least one of `reservation_id` or `rfid_tag` must be provided). |

## Downstream Notification Required

The following services consume check-in domain events and should be notified of the new field. No immediate code changes are required in these services.

| Consumer Service | Action Required | Notes |
|------------------|----------------|-------|
| svc-trail-management | Notification only | Will receive `rfid_tag` in the event payload. May use it for checkpoint tracking in a future phase. No action required now. |
| svc-guest-experience | Notification only | Will receive `rfid_tag` in the event payload. Can use it for contactless interactions when ready. No action required now. |

## Non-Impacted Components

All services not listed above are unaffected by this change. The modification is additive and backward-compatible. API consumers not using the new `rfid_tag` field will see no behavioral change. Event consumers using tolerant reader patterns will safely ignore the new field.

## Breaking Change Assessment

| Aspect | Breaking | Mitigation |
|--------|----------|------------|
| New optional field in CheckIn response | No | Additive field; existing consumers unaffected |
| New optional query parameter on GET /check-ins | No | Existing queries using reservation_id continue to work |
| reservation_id becomes conditionally required | Potentially | Current consumers always provide reservation_id and will not be affected. Document the change in the API changelog. |
| New field in domain event | No | Tolerant reader pattern; consumers ignore unknown fields |
