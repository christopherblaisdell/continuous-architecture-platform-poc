# NTK-10005: Implementation Guidance

## Overview

This document provides implementation guidance for adding the `rfid_tag` field to the check-in record schema in `svc-check-in`.

## Implementation Steps

### Step 1 - Schema Update

Add an optional `rfid_tag` field to the `CheckIn` schema in the OpenAPI specification:
- Type: `string`
- Max length: 64 characters
- Nullable: true
- Description: RFID chip identifier from scanned wristband, available before formal wristband assignment step
- Example: `"RFID-A3F7B201"`

### Step 2 - Database Migration

Add an `rfid_tag` column to the `check_ins` table:
- Column type: `VARCHAR(64)`, nullable
- Create a conditional unique index on `rfid_tag` where check-in status is not in (`COMPLETE`, `CANCELLED`) to enforce uniqueness per active check-in
- Index the column for query performance on the lookup endpoint

### Step 3 - API Endpoint Changes

**POST /check-ins**: Accept optional `rfid_tag` in the `CheckInCreate` request body for scenarios where RFID scanning happens at initial check-in.

**GET /check-ins**: Add `rfid_tag` as an optional query parameter for looking up check-ins by scanned wristband.

**GET /check-ins/{id}**: No changes needed -- the response already includes the full `CheckIn` schema.

### Step 4 - Validation

Implement input validation for the `rfid_tag` field:
- Format validation: Apply configurable regex pattern (initial: `^[A-F0-9]{8,16}$` or the `RFID-` prefixed variant as agreed with the hardware team)
- Length validation: Maximum 64 characters
- Uniqueness validation: Reject duplicate RFID values among active (non-completed, non-cancelled) check-ins

### Step 5 - Event Schema

Ensure the `rfid_tag` field is included in the check-in event payload published to the event bus. Since the event payload is derived from the `CheckIn` schema, this should happen automatically once the schema is updated.

### Step 6 - Testing

- Unit tests for RFID format validation
- Unit tests for uniqueness constraint enforcement
- Integration tests for RFID query parameter on `GET /check-ins`
- Contract tests to verify event payload includes `rfid_tag`
- Backward compatibility tests to ensure check-ins without RFID continue to work

## Dependencies

- Coordinate with kiosk firmware team on final RFID tag format/pattern
- Notify downstream service teams (svc-guest-experience, svc-trail-management) about the new field in check-in events

## Timeline Considerations

- API change must be deployed before kiosk firmware update (May 2026)
- Target completion: April 2026 to allow buffer for integration testing
