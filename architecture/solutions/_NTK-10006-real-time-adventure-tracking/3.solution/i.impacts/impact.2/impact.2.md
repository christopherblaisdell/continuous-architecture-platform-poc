# Impact Assessment — svc-check-in

| Field | Value |
|-------|-------|
| Service | svc-check-in |
| Impact Level | MEDIUM |
| Change Type | New outbound integration |
| Owner | NovaTrek Operations Team |

## Overview

svc-check-in gains a new status transition (`ADVENTURE_STARTED`) and an outbound call to
svc-adventure-tracking when that transition is made. No existing check-in API endpoints
or schemas change; this is an additive change.

## API Contract Changes

### Existing Schema: CheckIn — Extended

The `CheckIn` response object gains one new optional field:

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `tracking_session_id` | UUID | Yes | Reference to the svc-adventure-tracking session created when ADVENTURE_STARTED. Null until adventure commences. |

### Status Transition: ADVENTURE_STARTED

A new status value `ADVENTURE_STARTED` is added to the check-in status enum. This status
indicates that the adventure party has departed from base camp and a tracking session has
been activated.

**Status transition rules**:
- `CHECKED_IN` → `ADVENTURE_STARTED` (guide-initiated, via PATCH /check-ins/{id})
- `ADVENTURE_STARTED` → `COMPLETED` (system-initiated when session ends)
- `ADVENTURE_STARTED` is terminal in the context of check-in (no transition back)

### New Outbound Call

When a check-in transitions to `ADVENTURE_STARTED`, svc-check-in calls:

```
POST https://api.novatrek.example.com/tracking/v1/sessions
{
  "check_in_id": "<check-in ID>",
  "reservation_id": "<reservation ID>",
  "trip_id": "<trip ID from reservation>",
  "guide_id": "<guide ID, nullable>",
  "party_size": <number of checked-in participants>,
  "rfid_tag_ids": ["<rfid_1>", "<rfid_2>", ...],
  "geofence_id": null
}
```

The `geofence_id` is null at session creation; safety officers associate geofences to trips
separately using the geofences management API. Future enhancement: pre-populate based on
trip type lookup.

**Failure handling**: If svc-adventure-tracking is unavailable, the ADVENTURE_STARTED
transition still completes in svc-check-in. The tracking session activation is retried
asynchronously. A warning is logged and a non-blocking alert is raised for the operations
team. The absence of a tracking session does not prevent the adventure from proceeding.

## Data Model Changes

No database schema changes are required in svc-check-in beyond:

- Adding `tracking_session_id` (UUID, nullable) column to the check-ins table
- Adding `ADVENTURE_STARTED` to the status enum

## Backward Compatibility

- Existing consumers of the check-in API that do not use `tracking_session_id` are
  unaffected — the field is nullable and new
- The `ADVENTURE_STARTED` status value is additive; existing consumers that enumerate
  status values should treat unknown values gracefully (follow the OpenAPI spec which
  documents all valid values)
- No existing endpoints are removed or modified
