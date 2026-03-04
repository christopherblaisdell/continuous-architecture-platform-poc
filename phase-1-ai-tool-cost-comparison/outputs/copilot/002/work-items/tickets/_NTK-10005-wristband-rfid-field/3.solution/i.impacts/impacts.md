# NTK-10005 Impact Assessment

## Affected Service: svc-check-in

### API Contract Changes

| Change | Type | Breaking |
|--------|------|----------|
| Add `rfid_tag` field to `CheckIn` schema | Additive | No |
| Add `rfid_tag` field to `CheckInCreate` schema | Additive | No |
| Add `rfid_tag` query parameter to `GET /check-ins` | Additive | No |

All changes are additive and optional. Existing consumers that do not send or consume the `rfid_tag` field will continue to function without modification.

### Data Model Changes

- New nullable `rfid_tag` column on the `check_ins` table
- Partial unique index on `rfid_tag` for active check-ins only
- No changes to existing columns or constraints

### Event Schema Changes

The check-in event published to the event bus will include a new optional `rfid_tag` field. This is an additive change. Downstream consumers using schema-tolerant deserialization (ignoring unknown fields) will not be affected.

### Downstream Service Impact

| Service | Impact | Action Required |
|---------|--------|-----------------|
| svc-reservations | None | No changes needed |
| svc-safety-compliance | None | No changes needed |
| svc-gear-inventory | None | No changes needed |
| svc-guest-profiles | None | No changes needed |
| svc-analytics | Low | May want to consume rfid_tag for tracking analytics in the future |
| svc-notifications | None | No changes needed |

### Integration Points

| Integration | Impact |
|-------------|--------|
| Check-in event bus | New optional field in event payload |
| Kiosk firmware | Will send rfid_tag in check-in creation requests (firmware update scheduled for May) |
| RFID scanner hardware | No API impact; hardware integration is handled by kiosk firmware |

### Risk Summary

- **Low risk**: All changes are additive and backward-compatible
- **Data consistency**: Two locations for RFID data (top-level and nested under wristband) require synchronization logic
- **Timeline dependency**: API change must be deployed before kiosk firmware update in May 2026
