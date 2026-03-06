# NTK-10005 - Impact Summary

## Impacted Components

| Component | Impact Type | Severity | Details |
|-----------|------------|----------|---------|
| svc-check-in (API schema) | Schema addition | Low | Add optional `rfid_tag` field to `CheckIn` schema; add `rfid_tag` query parameter to `GET /check-ins` endpoint |
| svc-check-in (data model) | Database migration | Low | Add nullable `rfid_tag` column to `check_in_records` table with a partial unique index on active check-ins |
| svc-check-in (event schema) | Event payload change | Low | Add `rfid_tag` field to the check-in domain event published to the event bus |
| svc-check-in (validation) | Business logic | Low | Add RFID format validation (`^[A-F0-9]{8,16}$`) and active uniqueness check |

## Downstream Notification Required

The following services consume check-in events and should be notified of the new field, even though no immediate action is required:

| Consumer Service | Action Required | Notes |
|------------------|----------------|-------|
| svc-guest-experience | Notification only | Will receive `rfid_tag` in event payload; can ignore until trail tracking features are implemented |
| svc-trail-management | Notification only | Will receive `rfid_tag` in event payload; may use for checkpoint tracking in a future phase |

## Non-Impacted Components

All services not listed above are unaffected. The change is additive and backward-compatible. Consumers using tolerant reader patterns will safely ignore the new field.
