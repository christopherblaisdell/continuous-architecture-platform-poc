# NTK-10005 - Implementation Guidance

## Overview

This ticket is classified as a code-level task with light architecture review. The following guidance is provided for the development team implementing the change.

## Schema Changes

### 1. Add rfid_tag to CheckIn Schema (svc-check-in.yaml)

Add the following optional property to the `CheckIn` schema properties:

```yaml
rfid_tag:
  type: string
  maxLength: 64
  pattern: '^[A-F0-9]{8,16}$'
  nullable: true
  description: >-
    RFID chip identifier from the guest wristband. Populated when a wristband
    is assigned during the check-in process. Null for adventures without
    wristband tracking or before wristband assignment.
  example: "A3F7B20145CC"
```

IMPORTANT: This field should NOT be added to the `CheckInCreate` schema. The RFID tag is captured during the wristband assignment step (`POST /check-ins/{check_in_id}/wristband-assignment`), not at initial check-in creation.

### 2. Add rfid_tag Query Parameter to GET /check-ins

Add a new optional query parameter to the `GET /check-ins` endpoint:

```yaml
- name: rfid_tag
  in: query
  required: false
  schema:
    type: string
    pattern: '^[A-F0-9]{8,16}$'
  description: Filter check-ins by RFID wristband tag
```

Note: When `rfid_tag` is provided, `reservation_id` should become optional. Currently `reservation_id` is marked as required. This is a minor breaking change to the API contract that must be coordinated with consumers. Consider making both parameters optional with server-side validation that at least one is provided.

### 3. Entity and Database Changes

Add to `CheckInRecord.java`:

```java
@Column(name = "rfid_tag", length = 64)
private String rfidTag;
```

Database migration (Flyway or Liquibase):

```sql
-- Add nullable rfid_tag column
ALTER TABLE check_in_records ADD COLUMN rfid_tag VARCHAR(64);

-- Add partial unique index scoped to active check-ins
CREATE UNIQUE INDEX idx_rfid_tag_active 
ON check_in_records (rfid_tag) 
WHERE rfid_tag IS NOT NULL 
AND status NOT IN ('COMPLETED', 'FAILED', 'CANCELLED');
```

The partial index ensures:
- Only non-null RFID tags are subject to uniqueness constraint
- RFID tags can be reused once a check-in is completed, failed, or cancelled
- Completed historical records do not block new wristband assignments

### 4. Event Schema Update

When publishing check-in domain events to the event bus, include `rfid_tag` as a top-level field in the event payload alongside existing fields. Downstream consumers using tolerant reader patterns will ignore the new field until they are ready to use it.

```json
{
  "event_type": "check-in.completed",
  "check_in_id": "uuid",
  "reservation_id": "uuid",
  "participant_guest_id": "uuid",
  "wristband_id": "WB-2026-08-14-0342",
  "rfid_tag": "A3F7B20145CC",
  "status": "COMPLETE",
  "timestamp": "2026-06-15T09:30:00Z"
}
```

## Validation Rules

| Rule | Value | Notes |
|------|-------|-------|
| Format | Hexadecimal matching `^[A-F0-9]{8,16}$` | Confirm with hardware team |
| Max length | 64 characters | Allows for future format expansion |
| Nullable | Yes | Wristband tracking not required for all adventures |
| Uniqueness | Unique across active check-ins | Partial unique index |

## Testing Guidance

| Test Case | Expected Result |
|-----------|----------------|
| POST check-in without rfid_tag | Success; rfid_tag is null in response |
| Assign wristband with valid rfid_tag | Success; rfid_tag appears on CheckIn response |
| GET check-in by ID | Returns rfid_tag when present |
| GET check-ins filtered by rfid_tag | Returns matching active check-in |
| Assign wristband with duplicate rfid_tag (active) | 409 Conflict |
| Assign wristband with rfid_tag from completed check-in | Success (tag reuse allowed) |
| Assign wristband with invalid rfid_tag format | 400 Bad Request |
| Check-in event published with rfid_tag | Event payload includes rfid_tag field |
| Check-in event published without rfid_tag | Event payload has rfid_tag as null |

## Architecture Review Checkpoints

The following should be confirmed during architecture review of the implementation PR:

1. The Swagger spec change is valid OpenAPI 3.0 syntax
2. The uniqueness constraint scope matches Assumption A2 (active check-ins only)
3. The RFID format regex matches the hardware team specification (flag existing `RFID-` prefix discrepancy)
4. The `GET /check-ins` endpoint parameter changes are backward-compatible or coordinated with consumers
5. Downstream event consumers are notified of the new field

## Deployment Sequence

1. Database migration runs first (add column and index)
2. Application deployment with new schema, validation, and event changes
3. Notify downstream event consumers
4. Coordinate with kiosk firmware team for May 2026 deployment
