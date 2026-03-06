# NTK-10003 - Impact 3: svc-safety-compliance

**Impact Level**: LOW

## Overview

svc-safety-compliance currently supports waiver lookup by `guest_id` only. The unregistered guest flow requires waiver lookup by `reservation_id`, since the guest may not have an established profile at the time of the initial waiver check.

## Current State Analysis

The current `GET /waivers` endpoint in the OpenAPI spec requires `guest_id` as a required query parameter:

```yaml
parameters:
  - name: guest_id
    in: query
    required: true
    schema:
      type: string
      format: uuid
```

The `Waiver` schema does include a `reservation_id` field, confirming that the relationship between waivers and reservations already exists in the data model. The gap is in the query interface, not the data model.

## Changes Required

### Extended Query Parameter

**GET /safety-compliance/waivers**

Add `reservation_id` as an alternative query parameter. The endpoint should accept either `guest_id` OR `reservation_id`, but at least one must be provided.

| Current | New |
|---------|-----|
| `?guest_id={id}` (required) | `?guest_id={id}` OR `?reservation_id={id}` (at least one required) |

When queried by `reservation_id`, the endpoint returns the waiver status for all participants on the reservation. The response schema remains unchanged (array of Waiver objects).

### Digital Waiver Trigger

If no waiver record exists for the reservation, the response should include a digital waiver URL so the kiosk can present it to the guest:

```json
{
  "waiver_complete": false,
  "waiver_url": "https://waivers.novatrek.example.com/sign/{reservation_id}",
  "participants_pending": ["last_name_1", "last_name_2"]
}
```

### Index Addition

Add a database index on `reservation_id` in the waiver records table to support the new query pattern efficiently. Based on the current `Waiver` schema, this field already exists. Estimated index creation time: under 5 minutes on current data volume.

## Backward Compatibility

This change is fully backward compatible. Existing consumers that query by `guest_id` are unaffected. The `reservation_id` parameter is additive.

## Deployment Notes

- Deploy BEFORE svc-check-in
- No breaking changes to existing API contract (additive query parameter)
- Index migration should be run during low-traffic window to minimize table lock impact
- No new dependencies introduced
