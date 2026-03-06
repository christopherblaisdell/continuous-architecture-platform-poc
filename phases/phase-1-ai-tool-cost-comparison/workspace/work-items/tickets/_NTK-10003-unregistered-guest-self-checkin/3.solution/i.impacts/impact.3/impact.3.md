# NTK-10003 - Impact 3: svc-safety-compliance

**Impact Level**: LOW

## Overview

svc-safety-compliance currently supports waiver lookup by `guest_id`. The unregistered guest flow requires waiver lookup by `reservation_id`, since the guest may not have an established profile at the time of the waiver check.

## Changes Required

### Extended Query Parameter

**GET /safety-compliance/waivers**

Add `reservation_id` as an alternative query parameter:

| Current | New |
|---------|-----|
| `?guest_id={id}` | `?guest_id={id}` OR `?reservation_id={id}` |

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

## Deployment Notes

- Deploy BEFORE svc-check-in
- No breaking changes to existing API contract (additive query parameter)
- Index migration should be run during low-traffic window
