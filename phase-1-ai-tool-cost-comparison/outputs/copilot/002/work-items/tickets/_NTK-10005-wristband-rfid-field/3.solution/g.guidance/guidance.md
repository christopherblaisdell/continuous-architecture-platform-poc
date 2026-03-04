# NTK-10005 Implementation Guidance

## Overview

This guidance covers the implementation steps for adding the `rfid_tag` field to the svc-check-in service. The change is additive and backward-compatible.

## Step 1 Update OpenAPI Specification

Add the following to the `CheckIn` schema in `svc-check-in.yaml`:

```yaml
rfid_tag:
  type: string
  nullable: true
  pattern: '^[A-F0-9]{8,16}$'
  maxLength: 64
  description: >
    RFID chip identifier from the guest wristband. Nullable for adventures
    that do not use wristband tracking. Must be unique across active check-ins.
  example: "A3F7B2010E4D"
```

Add `rfid_tag` to the `CheckInCreate` schema as an optional field:

```yaml
rfid_tag:
  type: string
  nullable: true
  pattern: '^[A-F0-9]{8,16}$'
  maxLength: 64
  description: Optional RFID tag scanned at kiosk during check-in creation
```

Add an `rfid_tag` query parameter to the `GET /check-ins` endpoint:

```yaml
- name: rfid_tag
  in: query
  required: false
  schema:
    type: string
    pattern: '^[A-F0-9]{8,16}$'
  description: Filter check-ins by RFID wristband tag
```

## Step 2 Database Schema Migration

Add an `rfid_tag` column to the `check_ins` table:

```sql
ALTER TABLE check_ins ADD COLUMN rfid_tag VARCHAR(64) NULL;
CREATE UNIQUE INDEX idx_check_ins_rfid_tag_active
  ON check_ins (rfid_tag)
  WHERE status NOT IN ('COMPLETE', 'CANCELLED') AND rfid_tag IS NOT NULL;
```

The partial unique index enforces uniqueness only among active check-ins, allowing RFID tag reuse after previous check-ins are completed.

## Step 3 Service Layer Changes

- Add `rfid_tag` field to the `CheckIn` entity/domain model
- Add regex validation (`^[A-F0-9]{8,16}$`) in the service layer before persistence
- Add uniqueness check: query active check-ins for the given `rfid_tag` before creating a new check-in. Return HTTP 409 if a duplicate is found
- Add `rfid_tag` to the check-in event payload published to the event bus

## Step 4 Consistency Between Top-Level and Nested RFID

When a wristband is assigned via `POST /check-ins/{id}/wristband-assignment`, if the `CheckIn` record already has a top-level `rfid_tag`, validate that it matches the `rfid_tag` in the `WristbandAssignmentRequest`. If they differ, return HTTP 409 with a clear error message.

If the top-level `rfid_tag` is null at the time of wristband assignment, populate it from the `WristbandAssignmentRequest.rfid_tag`.

## Step 5 Testing

- Unit tests for RFID regex validation
- Unit tests for uniqueness constraint (active check-ins only)
- Integration tests for the new query parameter on GET /check-ins
- Contract tests verifying backward compatibility (existing consumers without `rfid_tag` continue to function)
- Verify event schema includes the new field

## Step 6 Consumer Notification

Notify downstream event consumers about the new optional `rfid_tag` field in the check-in event payload. No consumer changes are required since the field is optional, but teams should be aware for future integration planning.
