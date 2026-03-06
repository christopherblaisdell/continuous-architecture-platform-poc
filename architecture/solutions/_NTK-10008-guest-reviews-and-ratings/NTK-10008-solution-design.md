<!-- PUBLISH -->
# NTK-10008 Solution Design — Guest Reviews and Ratings Platform

| Field | Value |
|-------|-------|
| Ticket | NTK-10008 |
| Version | v1.0 |
| Status | Proposed |
| Author | Solution Architect (AI-Assisted) |
| Date | 2026-03-06 |

## Problem Statement

NovaTrek Adventures has no mechanism for guests to leave reviews or ratings after completing an adventure. The capability gap (CAP-1.7) means the platform lacks social proof — a critical driver of booking conversion in the adventure tourism industry. Without reviews, the trip catalog presents every adventure identically on quality, making it harder for guests to differentiate between trips and for NovaTrek to surface its highest-quality experiences.

## Solution Overview

Introduce a new **svc-reviews** microservice that owns the entire review lifecycle: submission, moderation, aggregation, and public display. Reviews are tied to completed reservations to ensure authenticity — only guests with a verified COMPLETED reservation can submit a review. A moderation pipeline prevents abusive or fraudulent content from appearing publicly.

### Key Design Decisions

1. **New service (svc-reviews)** rather than extending svc-media-gallery or svc-trip-catalog — reviews are a distinct bounded context with their own data model, moderation workflow, and access patterns
2. **Reservation-gated submissions** — preventing fake reviews by requiring a completed reservation link
3. **Asynchronous moderation pipeline** — reviews enter as PENDING_MODERATION and become visible only after approval (automated or manual)
4. **Aggregated rating summaries** — pre-computed per-trip and per-guide summaries cached for catalog display

### Architectural Pattern

```
Guest submits review
       │
       ▼
  svc-reviews
  (validates via svc-reservations + svc-guest-profiles)
       │
       ├─ Store in reviews DB (status: PENDING_MODERATION)
       ├─ Emit review.submitted event
       │
       ▼
  Moderation Pipeline
  (automated content check + manual queue)
       │
       ├─ APPROVED → update aggregates, emit review.approved
       └─ REJECTED → notify guest, log reason
```

## Impacted Components

| Service | Change Type | Impact Level | Owner |
|---------|------------|-------------|-------|
| svc-reviews | NEW SERVICE | PRIMARY | Guest Experience Team |
| svc-trip-catalog | Read integration | LOW | Product Team |
| svc-reservations | Read integration | LOW | Booking Platform Team |
| svc-guest-profiles | Read integration | LOW | Guest Experience Team |
| svc-guide-management | Read integration | LOW | Guide Operations Team |

## Security Considerations

| Threat | Mitigation |
|--------|-----------|
| Fake reviews | Reservation-gated submission; only COMPLETED reservations accepted |
| Review bombing | One review per guest per reservation; rate limiting per guest |
| Abusive content | Moderation pipeline; automated keyword filter + manual queue |
| PII in review text | Content scanning in moderation; rejection of reviews containing PII patterns |
| Enumeration attacks | Generic error messages; rate limiting on submission endpoint |

## Prior Art

- **NTK-10003** (Unregistered Guest Check-In) — established the pattern for cross-service validation flows (reservation lookup + guest identity verification)
- **NTK-10005** (Wristband RFID) — established the pattern for adding nullable fields to existing schemas without breaking consumers
- **ADR-010/ADR-011** — PATCH semantics and optimistic locking patterns reused for review updates

## Deployment Sequence

1. Database migration — create reviews schema and tables
2. Deploy svc-reviews with feature flag disabled
3. Configure event bus topics (review.submitted, review.approved)
4. Enable moderation queue
5. Enable feature flag for review submission
6. Update svc-trip-catalog to display rating summaries

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-03-06 | Initial solution design |
