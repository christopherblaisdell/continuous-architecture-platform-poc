# NTK-10005 - Implementation Guidance

## Overview

This ticket is classified as a code-level task with light architecture review. The following guidance is provided for the svc-check-in development team implementing the change.

## Schema Changes

### 1. Add rfid_tag to CheckIn Schema in svc-check-in.yaml

Add the following optional property to the `CheckIn` schema in the OpenAPI specification:

```yaml
rfid_tag:
  type: string
  maxLength: 64
  pattern: '^[A-F0-9]{8,16}$'
  nullable: true
  description: >-
    RFID chip identifier from the guest wristband. Populated during wristband
    assignment. Null for adventures that do not use wristband tracking.
  example: "A3F7B20145CC"
```

IMPORTANT: This field should NOT be added to `CheckInCreate`. The RFID tag is captured during the wristband assignment step of the check-in workflow, not at initial check-in creation.

### 2. Add rfid_tag Query Parameter to GET /check-ins

Add a new optional query parameter alongside the existing `reservation_id`:

```yaml
- name: rfid_tag
  in: query
  required: false
  schema:
    type: string
    pattern: '^[A-F0-9]{8,16}$'
  description: Filter check-ins by RFID wristband tag
```

When `rfid_tag` is provided, `reservation_id` should become optional. This is a minor contract change that should be coordinated with API consumers. The endpoint should support three lookup modes:

- By `reservation_id` only (current behavior, unchanged)
- By `rfid_tag` only (new)
- By both `reservation_id` and `rfid_tag` (new, returns intersection)

At least one of the two parameters must be provided. Return HTTP 400 if neither is specified.

### 3. Entity and Database Changes

Add to `CheckInRecord.java`:

```java
@Column(length = 64)
private String rfidTag;
```

Create a Flyway/Liquibase migration to add the column and a partial unique index:

```sql
ALTER TABLE check_in_records ADD COLUMN rfid_tag VARCHAR(64);

CREATE UNIQUE INDEX idx_rfid_tag_active 
ON check_in_records (rfid_tag) 
WHERE status NOT IN ('COMPLETED', 'FAILED');
```

The partial unique index ensures that no two active check-ins share the same RFID tag while allowing reuse of tags after check-in completion.

### 4. Event Schema Update

When publishing check-in domain events to the event bus, include `rfid_tag` as a top-level field in the event payload. Downstream consumers using tolerant reader patterns will safely ignore the new field until they choose to consume it.

## Validation Rules

| Rule | Detail |
|------|--------|
| Format | Hexadecimal string matching regex `^[A-F0-9]{8,16}$` |
| Max length | 64 characters |
| Nullable | Yes -- null is valid for adventures without wristband tracking |
| Uniqueness | Unique across active check-ins (status not in COMPLETED, FAILED) |
| Duplicate rejection | Return HTTP 409 with a clear error message identifying the conflicting check-in |

## Testing Guidance

| Test Case | Expected Result |
|-----------|----------------|
| POST check-in, then assign wristband with RFID | Check-in record includes rfid_tag after assignment |
| GET check-in by ID | Response includes rfid_tag if present |
| GET check-ins filtered by rfid_tag | Returns matching active check-in records |
| POST wristband assignment with duplicate active RFID | HTTP 409 conflict with clear error message |
| POST wristband assignment after previous check-in completed | Succeeds; RFID tag reuse is allowed |
| POST wristband assignment with invalid RFID format | HTTP 400 with validation error |
| Check-in event published | Event payload includes rfid_tag field |
| GET check-ins with no parameters | HTTP 400 requiring at least reservation_id or rfid_tag |

## Architecture Review Checkpoints

The following items should be confirmed during the architecture review of the implementation PR:

1. The Swagger specification change is valid OpenAPI 3.0 syntax
2. The uniqueness constraint scope matches Assumption A2 (active check-ins only)
3. The RFID format regex matches the hardware team kiosk firmware specification
4. Downstream event consumers have been notified of the new field
5. The query parameter interaction between `reservation_id` and `rfid_tag` is clearly documented

## Deployment Sequencing

1. Database migration runs first (adds nullable column and partial unique index)
2. Application deployment follows (new field, validation, query parameter)
3. Notify downstream event consumers of new field in event payload
4. Coordinate with kiosk firmware team for May 2026 rollout
