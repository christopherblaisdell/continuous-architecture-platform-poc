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

## R5: Staff Training and Workflow Adjustment

**Likelihood**: Medium | **Impact**: Low

**Description**: Front desk staff must understand the new kiosk capability to properly assist guests who have difficulty with the self-service flow. Staff also need to be aware of the "priority queuing" process for guests directed from the kiosk after a failed lookup.

**Mitigation**:
- Training materials prepared for each phase of rollout
- Kiosk displays a "Need Help?" button that alerts the nearest staff member
- Staff dashboard shows real-time kiosk activity including guests who abandoned the self-service flow
- Staff check-in UI shows whether a guest has already attempted kiosk check-in (prevents repeat data collection)

**Residual Risk**: Low (with training completed before each phase)
