# Risks — NTK-10008

## R1: Review Manipulation and Gaming

**Likelihood**: Medium
**Impact**: High

**Description**: Competitors, disgruntled employees, or incentivized parties submit misleading reviews to inflate or deflate trip ratings.

**Mitigation**: Reservation-gated submission (only verified guests). One review per reservation. Moderation pipeline with keyword filtering. Anomaly detection on rating patterns (future phase). Staff-submitted reviews flagged separately.

**Residual Risk**: Low — reservation gating eliminates most attack vectors. Genuine guests with grudges can still leave unfairly low ratings, but this is normal for any review platform.

## R2: Moderation Backlog Under High Volume

**Likelihood**: Medium
**Impact**: Medium

**Description**: Peak season or viral marketing campaigns generate review volumes that exceed moderation capacity, delaying publication.

**Mitigation**: Automated keyword filter auto-approves clean reviews (expected 80-90% auto-approval rate). Flagged reviews route to manual queue. Target moderation SLA: 4 hours for auto-approved, 24 hours for manual.

**Residual Risk**: Low — auto-approval handles the majority. Manual queue is for edge cases.

## R3: PII Exposure in Review Text

**Likelihood**: Medium
**Impact**: High

**Description**: Guests include personal information (phone numbers, email, addresses, guide names) in review text, creating data protection exposure.

**Mitigation**: Moderation pipeline includes PII pattern detection (regex for phone, email, addresses). Flagged reviews route to manual moderation. Reviewers informed via submission guidelines that PII will be removed.

**Residual Risk**: Medium — regex detection is imperfect. Unusual PII formats may pass through automated checks.

## R4: Negative Review Impact on Guide Morale

**Likelihood**: Medium
**Impact**: Low

**Description**: Per-guide rating summaries, if visible to guides, may negatively affect morale. Guides may feel surveilled rather than supported.

**Mitigation**: Guide rating summaries are accessible only to operations management, not directly to guides. Aggregate trends (not individual reviews) used for performance conversations. Positive review highlights shared with guides.

**Residual Risk**: Low — this is an operational and HR concern, not a technical risk.

## R5: Eventual Consistency of Rating Aggregates

**Likelihood**: Low
**Impact**: Low

**Description**: Rating summaries are pre-computed and refreshed periodically (every 5 minutes). During the refresh window, a trip page may show a stale average.

**Mitigation**: 5-minute refresh interval is acceptable for this domain. Event-driven cache invalidation on `review.approved` reduces the typical delay to seconds.

**Residual Risk**: Low — exact-second consistency is not required for review ratings.
