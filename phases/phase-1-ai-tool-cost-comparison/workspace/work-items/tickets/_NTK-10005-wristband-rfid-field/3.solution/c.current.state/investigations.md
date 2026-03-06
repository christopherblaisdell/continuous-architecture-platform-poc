# NTK-10005 - Current State Investigation

## Investigation Summary

The investigation focused on the current svc-check-in service schema, its Swagger specification, and the Java source code to determine the scope of changes required for adding RFID tag support to the check-in record.

## Current Schema Analysis

### Swagger Specification (svc-check-in.yaml)

The current `WristbandAssignment` schema **already includes** an `rfid_tag` field:

```yaml
WristbandAssignment:
  type: object
  required: [wristband_id, color, rfid_tag]
  properties:
    wristband_id:
      type: string
    color:
      type: string
      enum: [RED, BLUE, GREEN, YELLOW, ORANGE, PURPLE]
    rfid_tag:
      type: string
      example: "RFID-A3F7B201"
    assigned_at:
      type: string
      format: date-time
```

The `WristbandAssignmentRequest` also includes `rfid_tag` as a required field.

However, the top-level `CheckIn` schema does NOT have a direct `rfid_tag` field. The RFID tag is only accessible through the nested `wristband` property (`CheckIn.wristband.rfid_tag`).

### Java Source Code (CheckInRecord.java)

The `CheckInRecord` entity has a `wristbandId` field but no `rfid_tag` or `rfidTag` field:

```java
private String wristbandId;
```

This confirms the gap: the data model stores `wristbandId` but not the RFID tag separately on the check-in record itself.

### API Endpoint Analysis

The `GET /check-ins` endpoint currently supports filtering by `reservation_id` only. There is no query parameter for looking up check-ins by `rfid_tag`.

## Gap Analysis

| Aspect | Current State | Desired State |
|--------|--------------|---------------|
| CheckIn schema - rfid_tag | Not present (only in nested WristbandAssignment) | Direct optional field on CheckIn |
| CheckInRecord entity | No rfidTag field | New rfidTag column with uniqueness constraint |
| GET /check-ins query params | Only reservation_id | Add rfid_tag filter |
| Event payload | No rfid_tag at top level | Include rfid_tag in check-in event |

## Conclusion

The primary work is adding an `rfid_tag` field to the `CheckIn` schema (API response and Java entity) and adding a query parameter to the list endpoint. The `WristbandAssignment` sub-schema already captures the RFID tag during wristband assignment; this ticket extends that capture to the top-level check-in record for direct lookup without traversing the wristband assignment.
