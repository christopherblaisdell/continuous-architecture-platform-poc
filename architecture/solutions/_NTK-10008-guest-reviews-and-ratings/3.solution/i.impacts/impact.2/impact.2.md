# Impact Assessment — svc-trip-catalog

| Field | Value |
|-------|-------|
| Service | svc-trip-catalog |
| Impact Level | LOW |
| Change Type | Read integration |
| Owner | Product Team |

## Overview

svc-trip-catalog consumes rating summary data from svc-reviews to display aggregated guest ratings on trip pages. No schema changes or new endpoints are required on svc-trip-catalog itself — the catalog frontend queries the svc-reviews rating summary endpoint directly.

## Integration Points

| Integration | Details |
|-------------|---------|
| Read from svc-reviews | GET /trips/{trip_id}/rating-summary — called by frontend when rendering trip detail pages |
| Event consumption | Subscribe to `review.approved` event for local cache invalidation |

## Changes Required

1. **Frontend integration**: Trip detail pages add a rating summary widget (average stars, review count, link to full reviews)
2. **Cache layer**: Optional local cache of rating summaries with TTL (5 minutes), invalidated on `review.approved` event
3. **No API contract changes** to svc-trip-catalog itself

## Dependencies

- svc-reviews must be deployed and returning rating summaries before the catalog frontend is updated
- Event bus subscription for `review.approved` requires topic configuration

## Deployment Notes

- Deploy AFTER svc-reviews is live and returning data
- Frontend update can be feature-flagged independently
- No database migration required
