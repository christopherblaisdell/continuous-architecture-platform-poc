# NTK-10005 - Current State Investigation

## Investigation Summary

This investigation examines the current state of the svc-check-in service schema, its OpenAPI specification, and the Java source code to determine the scope of changes required for adding RFID tag support to the check-in record.

## Data Sources

- **JIRA Ticket**: NTK-10005 retrieved via `python3 scripts/mock-jira-client.py --ticket NTK-10005`
- **OpenAPI Specification**: `corporate-services/services/svc-check-in.yaml` (version 1.0.0)
- **Java Source Code**: `source-code/svc-check-in/src/main/java/com/novatrek/checkin/model/CheckInRecord.java`

## Current Schema Analysis

### OpenAPI Specification - WristbandAssignment Schema

The current `WristbandAssignment` schema already includes an `rfid_tag` field as a required property:

```yaml
WristbandAssignment:
  type: object
  required: [wristband_id, color, rfid_tag]
  properties:
    wristband_id:
      type: string
      example: "WB-2026-08-14-0342"
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

The `WristbandAssignmentRequest` also includes `rfid_tag` as a required field. This means the API already accepts RFID data during the wristband assignment step.

### OpenAPI Specification - CheckIn Schema

The top-level `CheckIn` schema does NOT have a direct `rfid_tag` field. The RFID tag is only accessible through the nested `wristband` property path: `CheckIn.wristband.rfid_tag`. This means clients must traverse the wristband assignment sub-object to access the RFID tag, and there is no way to filter check-ins by RFID tag directly.

### Java Source Code - CheckInRecord Entity

The `CheckInRecord` JPA entity (line 35 in `CheckInRecord.java`) has a `wristbandId` field:

```java
private String wristbandId;
```

There is no `rfidTag` field on the entity. The RFID tag is not persisted as a direct column on the check-in record table.

### API Endpoint Analysis

The `GET /check-ins` endpoint currently supports a single query parameter:

- `reservation_id` (required, UUID format) -- filters check-ins by reservation

There is no `rfid_tag` query parameter. Clients cannot look up a check-in record by scanning a wristband RFID tag.

## Gap Analysis

| Aspect | Current State | Desired State | Gap |
|--------|--------------|---------------|-----|
| CheckIn schema - rfid_tag | Not present at top level; only in nested WristbandAssignment | Direct optional field on CheckIn response | Schema addition needed |
| CheckInRecord entity | No rfidTag field | New rfidTag column with partial uniqueness constraint | Entity and DDL migration needed |
| GET /check-ins query params | Only reservation_id (required) | Add optional rfid_tag filter | API parameter addition needed |
| Check-in event payload | No rfid_tag at top level | Include rfid_tag in domain event | Event schema addition needed |

## Key Findings

1. **Partial support already exists**: The `WristbandAssignment` sub-schema captures `rfid_tag` during the wristband assignment step. The gap is promoting this data to the top-level `CheckIn` record for direct access and lookup.

2. **No new services or endpoints required**: The change is confined to existing schemas and an existing endpoint within svc-check-in.

3. **Backward-compatible change**: Adding an optional, nullable field to the `CheckIn` schema and an optional query parameter to `GET /check-ins` does not break existing API consumers.

## Conclusion

The scope of work is limited to svc-check-in. The change promotes the RFID tag (already captured during wristband assignment) to the top-level check-in record for direct lookup. This is an additive schema change with no cross-service implications beyond event payload updates for downstream consumers.
