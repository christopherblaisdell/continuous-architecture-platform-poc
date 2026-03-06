# NTK-10003 - Impact 3: svc-safety-compliance

**Impact Level**: MINOR

## Overview

svc-safety-compliance must extend its waiver lookup capability to support queries by `reservation_id` in addition to the existing `guest_id`-based lookup. This enables the orchestrator to check waiver completion status for unregistered guests who do not yet have a fully linked guest profile.

## Changes Required

### Extended Waiver Lookup

**GET /safety-compliance/waivers** -- Add `reservation_id` query parameter.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| guest_id | UUID | No (existing) | Lookup by guest profile ID |
| reservation_id | UUID | No (new) | Lookup by reservation ID |

At least one parameter must be provided. When `reservation_id` is used, the service returns waiver records associated with the reservation rather than a specific guest profile.

### Response Enhancement

The response must include:
- `waiver_complete` (boolean) -- whether the required waiver has been signed
- `waiver_url` (string, nullable) -- URL to the digital waiver form if incomplete; null if already signed

### No Schema Changes

The existing waiver data model already supports reservation-based associations. The change is limited to adding a query parameter and the corresponding repository lookup method.

## Deployment Notes

- Deploy BEFORE svc-check-in (dependency order)
- No database migration required
- No breaking changes to existing API contracts
- Estimated effort: 1 day (Wei Zhang)
