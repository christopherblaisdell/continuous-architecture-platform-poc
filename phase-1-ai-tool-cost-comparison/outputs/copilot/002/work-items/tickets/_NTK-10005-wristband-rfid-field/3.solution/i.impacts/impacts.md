# NTK-10005: Impact Assessment

## Impact Summary

This change has a **low** overall impact. It is an additive, backward-compatible schema extension scoped primarily to `svc-check-in`.

## Affected Services

### svc-check-in (Primary)

- **Schema change**: New optional `rfid_tag` field on `CheckIn` and `CheckInCreate` schemas
- **API change**: New `rfid_tag` query parameter on `GET /check-ins`
- **Database change**: New nullable column with conditional unique index
- **Event change**: Check-in events will include the new field when present
- **Risk level**: Low -- additive change, no existing behavior modified

### Downstream Event Consumers (Informational)

The following services consume check-in events and will receive the new `rfid_tag` field:

- **svc-guest-experience**: Will receive RFID data in check-in events. No action required unless they choose to use it for contactless interactions.
- **svc-trail-management**: Will receive RFID data in check-in events. No action required unless they choose to use it for on-trail tracking.

These services are NOT required to change. The new field is additive and will be ignored by consumers that do not process it.

## API Contract Impact

- **Breaking changes**: None. The new field is optional in requests and nullable in responses.
- **Versioning**: No version bump required. This is a backward-compatible, minor enhancement.
- **Consumer action needed**: None required. Consumers may optionally begin using the field.

## Data Impact

- **New storage**: One additional nullable VARCHAR(64) column per check-in record
- **Storage estimate**: Negligible -- approximately 64 bytes per record at most
- **Migration**: Additive column, online migration with no downtime expected
