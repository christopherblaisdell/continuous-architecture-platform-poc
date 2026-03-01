# NTK-10005 - Impact Summary

## Impacted Components

| Component | Impact Type | Severity | Details |
|-----------|------------|----------|---------|
| svc-check-in | Schema addition | Low | Add optional `rfid_tag` field to `CheckIn` schema; add query parameter for lookup by RFID |

## Non-Impacted Components

All other services are unaffected. Downstream consumers of check-in events will receive a new optional field but are not required to process it.
