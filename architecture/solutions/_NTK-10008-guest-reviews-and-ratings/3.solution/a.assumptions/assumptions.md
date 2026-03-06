# Assumptions — NTK-10008

## A1: Reservation Status is Authoritative

**Assumption**: svc-reservations exposes a `status` field on the reservation object that includes a `COMPLETED` state, and this status is reliably updated after adventure completion.

**Risk if invalid**: Reviews cannot be gate-checked against completed adventures; fake review submissions become possible.

**Mitigation**: If no COMPLETED status exists, gate on check-in completion status from svc-check-in instead.

## A2: One Review per Guest per Reservation

**Assumption**: The business requires exactly one review per guest per reservation. Guests who want to update their review edit the existing one rather than submitting a new one.

**Risk if invalid**: Duplicate reviews inflate rating averages.

**Mitigation**: Enforce uniqueness constraint at the database level (guest_id + reservation_id).

## A3: Guide Assignment is Available on Reservation

**Assumption**: The reservation or check-in record includes a reference to the assigned guide, enabling per-guide rating aggregation.

**Risk if invalid**: Guide rating summaries cannot be computed without manual data entry.

**Mitigation**: If guide_id is not on the reservation, query svc-guide-management by adventure date and trip to resolve the assignment.

## A4: Automated Content Moderation is Sufficient for Initial Launch

**Assumption**: A keyword-based content filter combined with manual moderation queue is adequate for launch volume. Machine learning-based moderation is not required in phase 1.

**Risk if invalid**: High volume of reviews overwhelms manual moderation.

**Acceptable degradation**: Reviews take longer to appear (24-48 hours instead of 4 hours). Scale moderation team or introduce ML-based triage in phase 2.

## A5: Rating Display Does Not Require Real-Time Consistency

**Assumption**: Aggregated rating summaries (average, count) can be eventually consistent. A delay of up to 5 minutes between review approval and summary update is acceptable.

**Risk if invalid**: Guests see stale averages. Acceptable for this domain — reviews are not time-critical data.

## A6: Review Text is English-Only at Launch

**Assumption**: Reviews are submitted in English. Multi-language support (translation, language detection) is deferred.

**Risk if invalid**: Non-English reviews bypass keyword-based moderation filters.

**Mitigation**: Flag non-ASCII-heavy reviews for manual moderation.
