# Impact Assessment — svc-reviews (NEW SERVICE)

| Field | Value |
|-------|-------|
| Service | svc-reviews |
| Impact Level | PRIMARY |
| Change Type | New Service |
| Owner | Guest Experience Team |

## Overview

svc-reviews is a new microservice that owns the full review lifecycle: submission, moderation, aggregation, and public display. This is the primary deliverable of NTK-10008.

## Data Model

**Database**: PostgreSQL 15

**Schema**: reviews

**Tables**:

| Table | Purpose |
|-------|---------|
| reviews | Guest reviews with ratings, text, moderation status |
| review_helpful_votes | One-per-guest helpful vote tracking |
| rating_aggregates | Pre-computed per-entity (trip/guide) rating summaries |

**Key columns on reviews table**:

- `id` (UUID, PK)
- `reservation_id` (UUID, FK cross-ref svc-reservations, UNIQUE with guest_id)
- `guest_id` (UUID, cross-ref svc-guest-profiles)
- `trip_id` (UUID, cross-ref svc-trip-catalog)
- `guide_id` (UUID, nullable, cross-ref svc-guide-management)
- `overall_rating` (INTEGER, 1-5)
- `category_ratings` (JSONB — safety, guide_quality, value_for_money, scenery, difficulty_accuracy)
- `title` (VARCHAR 200)
- `body` (TEXT, max 5000 chars)
- `moderation_status` (ENUM: PENDING_MODERATION, APPROVED, REJECTED, FLAGGED)
- `helpful_count` (INTEGER, default 0)
- `_rev` (INTEGER, optimistic locking version)
- `created_at`, `updated_at` (TIMESTAMPTZ)

**Indexes**:

- `(trip_id, moderation_status)` — trip page queries
- `(guide_id, moderation_status)` — guide rating queries
- `(guest_id, reservation_id)` — uniqueness enforcement
- `(moderation_status, created_at)` — moderation queue ordering

## API Endpoints

See `architecture/specs/svc-reviews.yaml` for the full OpenAPI specification.

| Method | Path | Purpose |
|--------|------|---------|
| POST | /reviews | Submit a review |
| GET | /reviews | List reviews (filtered) |
| GET | /reviews/{review_id} | Get single review |
| PATCH | /reviews/{review_id} | Update review (guest edit or moderation) |
| DELETE | /reviews/{review_id} | Soft-delete review |
| POST | /reviews/{review_id}/helpful | Mark review as helpful |
| GET | /trips/{trip_id}/rating-summary | Trip rating aggregate |
| GET | /guides/{guide_id}/rating-summary | Guide rating aggregate |
| GET | /moderation/queue | Moderation queue |
| POST | /moderation/{review_id}/decide | Approve or reject |

## Cross-Service Dependencies

| Dependency | Purpose | Call Pattern |
|-----------|---------|-------------|
| svc-reservations | Validate reservation exists and is COMPLETED | Synchronous GET on submission |
| svc-guest-profiles | Validate guest identity | Synchronous GET on submission |
| svc-trip-catalog | Validate trip exists (optional) | Synchronous GET on submission |
| svc-guide-management | Validate guide exists (optional) | Synchronous GET on submission |

## Events Produced

| Event | Trigger | Consumers |
|-------|---------|-----------|
| review.submitted | Review created | Moderation pipeline |
| review.approved | Review passes moderation | svc-trip-catalog (cache invalidation), svc-analytics |
| review.rejected | Review rejected | svc-notifications (guest notification) |

## Configuration

| Property | Default | Description |
|----------|---------|-------------|
| reviews.moderation.auto-approve.enabled | true | Enable keyword-based auto-approval |
| reviews.moderation.flagged-keywords | (list) | Keywords that route to manual review |
| reviews.submission.rate-limit | 5/hour/guest | Max submissions per guest per hour |
| reviews.aggregate.refresh-interval | 300s | Rating summary recalculation interval |
| reviews.feature-flag.enabled | false | Master feature flag for review submission |

## Deployment Notes

- Deploy database migration FIRST (create schema + tables + indexes)
- Deploy svc-reviews with feature flag disabled
- Configure event bus topics before enabling the feature flag
- Enable moderation queue dashboard access for moderators
- Enable feature flag per location (phased rollout)
