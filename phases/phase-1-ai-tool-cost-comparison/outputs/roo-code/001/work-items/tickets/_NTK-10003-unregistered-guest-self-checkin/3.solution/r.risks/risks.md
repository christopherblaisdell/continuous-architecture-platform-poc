# NTK-10003 - Risks

## R1: Reservation Enumeration Attacks

**Likelihood**: Medium | **Impact**: High

**Description**: Malicious actors could attempt to enumerate valid reservation confirmation codes by submitting systematic lookup requests through the kiosk. Successful enumeration could expose guest names and adventure details.

**Mitigation**:
- Rate limiting: 5 attempts per kiosk per 15-minute window (gateway + application level)
- 2-second artificial delay on failed lookups to slow automated attempts
- Vague error messaging ("We couldn't find a matching reservation") that does not confirm which field was incorrect
- All failed attempts logged for SOC monitoring with alerting on anomalous patterns
- Kiosk-scoped rate limits prevent a single compromised kiosk from being used as an enumeration tool

**Residual Risk**: Low (after mitigations applied)

## R2: Partner Data Inconsistency

**Likelihood**: Medium | **Impact**: Medium

**Description**: Partner booking data may be inconsistent with the reservation record in svc-reservations. Common issues include: different last name spelling, participant count mismatches due to post-booking modifications, and confirmation code format variations. This would cause verification failures for legitimate guests.

**Mitigation**:
- Confirmation code normalization (strip hyphens, uppercase) reduces format-related mismatches
- Partner data sync runs nightly with validation checks and discrepancy reporting
- Error messaging directs guests to staff desk with priority queuing when verification fails
- Dashboard metric tracks partner-booked verification failure rate to identify systemic data quality issues

**Residual Risk**: Low-Medium (data quality is an ongoing operational concern)

## R3: Temporary Profile Accumulation and Cleanup

**Likelihood**: Low | **Impact**: Medium

**Description**: High volumes of temporary guest profiles could accumulate if the 90-day anonymization job fails or if unexpected usage patterns create large numbers of profiles. This could impact svc-guest-profiles query performance and storage costs.

**Mitigation**:
- Deduplication logic prevents multiple temporary profiles for the same reservation
- 90-day anonymization background job with monitoring and alerting on job failures
- Database monitoring for temporary profile table growth
- Manual cleanup procedure documented in runbook

**Residual Risk**: Low

## R4: Kiosk Hardware Limitations

**Likelihood**: Low | **Impact**: Medium

**Description**: Some older kiosk terminals at smaller base camps may not support the digital waiver signature capture flow, which requires a responsive touchscreen with sufficient resolution. If the kiosk cannot render the waiver signing interface, the guest cannot complete check-in.

**Mitigation**:
- Pre-deployment hardware audit at each base camp (included in Phase 1 checklist)
- Graceful degradation: if waiver cannot be completed on kiosk, display QR code for guest to complete waiver on personal mobile device
- Phased rollout starts at Cascade Ridge (newest hardware) to validate before wider deployment
- Hardware upgrade budget identified for base camps that fail the audit

**Residual Risk**: Low (with pre-deployment audit)

## R5: Check-in Load During Peak Arrival Windows

**Likelihood**: Medium | **Impact**: Medium

**Description**: The self-service flow adds network calls to 4-5 downstream services per kiosk check-in. During peak arrival windows (7:00-9:00 AM), high concurrency of kiosk lookups could strain downstream services, particularly svc-reservations (new composite index query) and svc-guest-profiles (temporary profile creation).

**Mitigation**:
- Response time budgets per downstream call (2s + 1s + 3s + 1s = 7s with 1s buffer)
- svc-safety-compliance and svc-gear-inventory calls are parallelized to reduce total latency
- Circuit breaker on partner integration prevents cascading failures
- Performance testing target: 100 concurrent lookups with p95 under 5 seconds
- Phase 1 at lowest-volume base camp validates load patterns before wider rollout

**Residual Risk**: Low-Medium (depends on peak season volumes)

## R6: Compliance Risk for Unregistered Guests

**Likelihood**: Low | **Impact**: High

**Description**: Unregistered guests who check in via kiosk may bypass safety compliance steps if the integration with svc-safety-compliance fails gracefully (waiver_complete returned as null). A guest could proceed to an adventure without completing a mandatory safety waiver.

**Mitigation**:
- If waiver status is unknown (null), the kiosk displays the waiver signing interface as a mandatory step before check-in can be completed
- The check-in flow does not allow final confirmation without either confirmed waiver completion or on-kiosk waiver signing
- Staff check-in dashboard flags guests with incomplete waivers for manual verification at the base camp entrance

**Residual Risk**: Low (with mandatory waiver gating in kiosk flow)
