# Architecture Decisions — NTK-10008

## ADR-NTK10008-001: Dedicated Reviews Microservice

### Status

Accepted

### Date

2026-03-06

### Context and Problem Statement

Guest reviews and ratings need a home in the NovaTrek architecture. Reviews have distinct data models (ratings, moderation status, helpful votes), access patterns (high read, moderate write), and lifecycle (submission, moderation, publication). The question is whether to add reviews to an existing service or create a dedicated microservice.

### Decision Drivers

- Domain cohesion — reviews are a distinct bounded context with their own lifecycle
- Independent scalability — read-heavy workload (catalog browsing) vs. moderate writes (review submission)
- Team ownership — Guest Experience Team owns guest-facing quality features
- Data isolation — review data should not be co-located with catalog or media data
- Deployment independence — moderation workflow changes should not require redeploying the trip catalog

### Considered Options

**Option 1: New svc-reviews microservice** (SELECTED)

- (+) Clean bounded context with dedicated data store
- (+) Independent scaling for high-read rating summary queries
- (+) Guest Experience Team owns the full review lifecycle
- (+) Moderation workflow changes deploy independently
- (-) Additional service to operate and monitor
- (-) Cross-service calls needed for reservation validation

**Option 2: Extend svc-trip-catalog with review endpoints**

- (+) No new service to deploy; reviews co-located with trip data
- (+) Rating summaries are local queries (no cross-service aggregation)
- (-) Violates single responsibility — catalog manages product data, not user-generated content
- (-) Moderation workflow couples to catalog deployment
- (-) Product Team inherits ownership of a guest experience feature

**Option 3: Extend svc-media-gallery to include reviews**

- (+) Media gallery already handles user-generated content
- (-) Very different data models — binary media vs. structured text + ratings
- (-) Different access patterns and moderation workflows
- (-) Forces coupling between photo sharing and review features

### Decision Outcome

Selected **Option 1: New svc-reviews microservice**. Reviews are a distinct domain with their own lifecycle, access patterns, and team ownership. The additional operational cost of a new service is justified by the clean separation of concerns and deployment independence.

### Consequences

**Positive**: Clean bounded context; independent deployment; Guest Experience Team owns end-to-end.

**Negative**: Additional service to monitor; cross-service calls for reservation and guest validation add latency to submission flow.

**Neutral**: Follows the established NovaTrek pattern of service-per-bounded-context.

---

## ADR-NTK10008-002: Reservation-Gated Review Submission

### Status

Accepted

### Date

2026-03-06

### Context and Problem Statement

Review platforms face integrity challenges from fake reviews, competitor sabotage, and incentivized reviews. NovaTrek must ensure that published reviews reflect genuine guest experiences. The question is how to verify review authenticity.

### Decision Drivers

- Review integrity — only real guests should leave reviews
- Friction minimization — verification should not create excessive barriers
- Scalability — approach must work without manual verification
- Compatibility — must work with existing reservation and check-in data

### Considered Options

**Option 1: Reservation-gated submission** (SELECTED)

- (+) Strong authenticity guarantee — reservation must exist and be COMPLETED
- (+) Zero additional guest friction — reservation_id is known from the booking
- (+) Scales automatically with booking volume
- (+) Compatible with existing svc-reservations API
- (-) Guests who experienced an adventure without a reservation (comp tickets, staff) cannot review
- (-) Requires svc-reservations to expose COMPLETED status reliably

**Option 2: Email verification**

- (+) Low friction
- (-) Email addresses can be fabricated; weak authenticity signal
- (-) Does not prove the guest actually completed the adventure

**Option 3: Post-check-in token**

- (+) Strongest proof of attendance (guest was physically present)
- (-) Requires svc-check-in to issue review tokens — new contract
- (-) Guests who lose the token cannot review
- (-) Adds complexity to the check-in flow

### Decision Outcome

Selected **Option 1: Reservation-gated submission**. The combination of a valid reservation_id in COMPLETED status provides sufficient authenticity. Comp ticket and staff reviews can be handled as a future enhancement (internal review submission without reservation).

### Consequences

**Positive**: Strong integrity with zero additional guest friction.

**Negative**: Comp ticket recipients cannot review until an alternative path is built.

**Neutral**: Requires svc-reservations to reliably expose COMPLETED status, which is expected per the existing API contract.

---

## ADR-NTK10008-003: Moderation-First Publishing Model

### Status

Accepted

### Date

2026-03-06

### Context and Problem Statement

User-generated content on a brand-owned platform carries reputational risk. Abusive, defamatory, or PII-containing reviews must be intercepted before public display. The question is whether reviews should be published immediately or require moderation first.

### Decision Drivers

- Brand safety — NovaTrek controls the platform and has reputational exposure
- Guest experience — long moderation delays frustrate reviewers
- Legal compliance — defamatory content must be interceptable
- Operational cost — manual moderation does not scale infinitely

### Considered Options

**Option 1: Moderation-first (PENDING_MODERATION default)** (SELECTED)

- (+) No abusive content reaches public display
- (+) PII detection before publication
- (+) Legal protection — publisher has reviewed content
- (-) Delay between submission and publication (target: 4 hours)
- (-) Requires moderation staff or automated tooling

**Option 2: Publish-first with retroactive moderation**

- (+) Reviews appear instantly — better guest experience
- (-) Abusive or PII-containing content visible to other guests before moderation
- (-) Legal and reputational risk during the exposure window
- (-) Requires rapid content monitoring infrastructure

### Decision Outcome

Selected **Option 1: Moderation-first**. Brand safety and legal compliance outweigh the delay cost. Target moderation turnaround is 4 hours, with automated keyword filtering to auto-approve clean reviews and route flagged content to manual review.

### Consequences

**Positive**: Zero exposure to abusive content; legal defensibility.

**Negative**: Publication delay; requires moderation operations.

**Neutral**: Standard practice for brand-owned UGC platforms in travel and hospitality.
