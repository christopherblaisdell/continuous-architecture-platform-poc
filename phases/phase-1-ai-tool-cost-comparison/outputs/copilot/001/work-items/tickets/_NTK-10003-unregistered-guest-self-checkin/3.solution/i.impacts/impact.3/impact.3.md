# NTK-10003 - Impact 3: svc-safety-compliance

**Impact Level**: LOW

## Overview

svc-safety-compliance currently supports waiver lookup by `guest_id` only. The `GET /waivers` endpoint has `guest_id` as a required query parameter. The unregistered guest flow requires waiver lookup by `reservation_id`, since the guest may not have an established profile at the time of the waiver check or the temporary profile may have been created moments before the waiver query.

## Current State

The existing `GET /waivers` endpoint requires:
- `guest_id` (required, UUID query parameter)
- `status` (optional, WaiverStatus enum)

The `Waiver` schema includes both `guest_id` and `reservation_id` fields, so the data model already supports reservation-based association. The limitation is in the query endpoint, not the data model.

The `WaiverSignRequest` schema already accepts `reservation_id` for waiver creation, so waivers are already linked to reservations at sign time.

## Changes Required

### Extended Query Parameter

**GET /waivers**

Add `reservation_id` as an alternative query parameter:

| Current | New |
|---------|-----|
| `?guest_id={id}` (required) | `?guest_id={id}` OR `?reservation_id={id}` (at least one required) |

When queried by `reservation_id`, the endpoint returns the waiver status for all participants on the reservation. The response schema remains unchanged.

### Digital Waiver Trigger

If no waiver record exists for the reservation, the response should include the digital waiver URL so the kiosk can present it to the guest:

```json
{
  "waiver_complete": false,
  "waiver_url": "https://waivers.novatrek.com/sign/{reservation_id}",
  "participants_pending": ["last_name_1", "last_name_2"]
}
```

### Index Addition

Add a database index on `reservation_id` in the waiver records table to support the new query pattern. Estimated creation time: under 5 minutes on current data volume.

## API Contract Change

- **Change Type**: Additive query parameter
- **Breaking Change**: No (existing `guest_id` queries continue to work unchanged)
- **Backward Compatible**: Yes

## Deployment Notes

- Deploy BEFORE svc-check-in
- No breaking changes to existing API contract (additive query parameter)
- Index migration should be run during low-traffic window
