# NTK-10005 - Implementation Guidance

## Overview

This ticket is a code-level task with light architecture review. The following guidance is provided for the development team implementing the change.

## Schema Changes

### 1. Add rfid_tag to CheckIn Schema (svc-check-in.yaml)

Add the following optional property to the `CheckIn` schema:

```yaml
rfid_tag:
  type: string
  maxLength: 64
  pattern: '^[A-F0-9]{8,16}$'
  nullable: true
  description: RFID chip identifier from the guest wristband. Null for adventures without wristband tracking.
  example: "A3F7B20145CC"
```

This field should NOT be added to `CheckInCreate` -- the RFID tag is captured during wristband assignment, not at initial check-in creation.

### 2. Add rfid_tag Query Parameter to GET /check-ins

Add a new optional query parameter alongside `reservation_id`:

```yaml
- name: rfid_tag
  in: query
  required: false
  schema:
    type: string
    pattern: '^[A-F0-9]{8,16}$'
  description: Filter check-ins by RFID wristband tag
```

Note: When `rfid_tag` is provided, `reservation_id` should become optional (currently required). This is a minor breaking change to the API contract that should be coordinated with consumers.

### 3. Entity and Database Changes

Add to `CheckInRecord.java`:

```java
@Column(length = 64)
private String rfidTag;
```

Add a partial unique index scoped to active check-ins:

```sql
CREATE UNIQUE INDEX idx_rfid_tag_active 
ON check_in_records (rfid_tag) 
WHERE status NOT IN ('COMPLETED', 'FAILED');
```

### 4. Event Schema

When publishing check-in events to the event bus, include `rfid_tag` as a top-level field in the event payload. Downstream consumers using tolerant reader patterns will ignore the new field until they are ready to use it.

## Validation Rules

- Format: Hexadecimal string matching regex `^[A-F0-9]{8,16}$`
- Max length: 64 characters
- Nullable: Yes (wristband tracking is not required for all adventures)
- Uniqueness: Unique across active check-ins (status not in COMPLETED, FAILED)

## Testing Guidance

- Verify POST check-in with and without RFID tag
- Verify GET check-in returns rfid_tag when present
- Verify GET check-ins filters by rfid_tag
- Verify duplicate RFID tag rejection for active check-ins
- Verify RFID tag reuse after check-in completion
- Verify event payload includes rfid_tag
- Verify format validation rejects invalid RFID patterns

## Architecture Review Checkpoints

The following should be confirmed during architecture review of the implementation PR:

1. The Swagger spec change is valid OpenAPI 3.0 syntax
2. The uniqueness constraint scope matches Assumption A2 (active check-ins only)
3. The RFID format regex matches the hardware team's specification
4. Downstream event consumers are notified of the new field (even if no action is required)
