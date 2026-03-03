# NTK-10003 - Risks

## R1: Reservation Enumeration Attacks

**Likelihood**: Medium | **Impact**: High

**Description**: Malicious actors could attempt to enumerate valid reservation confirmation codes by submitting systematic lookup requests through the kiosk. Successful enumeration could expose guest names and adventure details. The existing `CheckInController.java` stub accepts a raw `Map<String,String>` with no input validation, which means no server-side protection exists in the current codebase.

**Mitigation**:
- Rate limiting: 5 attempts per kiosk per 15-minute window (gateway + application level using Redis sliding window)
- 2-second artificial delay on failed lookups (`Thread.sleep(2000)` in `ReservationLookupService`) to slow automated attempts
- Vague error messaging ("We couldn't find a matching reservation") that does not confirm which field was incorrect
- All failed attempts logged for SOC monitoring with alerting on anomalous patterns using structured log event `LOOKUP_FAILURE`
- Kiosk-scoped rate limits prevent a single compromised kiosk from being used as an enumeration tool
- Replace the existing `Map<String,String>` input with a typed `ReservationLookupRequest` DTO with Bean Validation annotations (`@Size`, `@Pattern`, `@NotNull`) to reject malformed input before it reaches business logic

**Residual Risk**: Low (after mitigations applied)

## R2: Partner Data Inconsistency

**Likelihood**: Medium | **Impact**: Medium

**Description**: Partner booking data may be inconsistent with the reservation record in svc-reservations. Common issues include: different last name spelling, participant count mismatches due to post-booking modifications, and confirmation code format variations (ExploreMore uses `EM-` prefix, TrailFinder uses `TF-`, WildPass uses `WP-`). The `BookingSource` enum in svc-reservations includes `PARTNER_API` but the current schema has no `confirmation_code` field, meaning partner codes have no canonical storage location yet.

**Mitigation**:
- Confirmation code normalization at the svc-check-in layer: strip hyphens, uppercase, trim whitespace (accept both `EM-A1B2C3D4` and `EMA1B2C3D4`)
- Partner data sync runs nightly with validation checks and discrepancy reporting
- Error messaging directs guests to staff desk with priority queuing when verification fails
- Dashboard metric tracks partner-booked verification failure rate to identify systemic data quality issues
- svc-partner-integrations fallback provides a second verification path when nightly sync data is stale

**Residual Risk**: Low-Medium (data quality is an ongoing operational concern)

## R3: Temporary Profile Accumulation and Cleanup

**Likelihood**: Low | **Impact**: Medium

**Description**: High volumes of temporary guest profiles could accumulate if the 90-day anonymization job fails or if unexpected usage patterns create large numbers of profiles. The current `GuestService.java` uses `findByEmail()` for deduplication, but temporary profiles will not have email addresses. This means the existing deduplication mechanism will not prevent duplicate temporary profiles for the same guest across multiple visits.

**Mitigation**:
- Deduplication for temporary profiles keyed on reservation_id (one temporary profile per reservation) rather than email
- `profile_type` field (`REGISTERED` / `TEMPORARY`) added to `Guest` entity enables targeted queries and cleanup
- 90-day anonymization background job with monitoring and alerting on job failures
- Database monitoring for temporary profile table growth with threshold alerts
- Manual cleanup procedure documented in runbook for emergency bulk deletion

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

## R6: Service Dependency Cascade During Peak Check-in

**Likelihood**: Medium | **Impact**: High

**Description**: The orchestration flow in svc-check-in calls up to 5 downstream services (svc-reservations, svc-guest-profiles, svc-safety-compliance, svc-gear-inventory, svc-partner-integrations). During peak morning check-in periods (07:00-09:00), simultaneous kiosk lookups could saturate downstream service connection pools. The current `CheckInController.java` has no circuit breaker or bulkhead pattern implemented.

**Mitigation**:
- Circuit breaker per downstream client (Resilience4j) with failure rate threshold of 50% over 10-call sliding window
- Bulkhead pattern: dedicated thread pool for kiosk lookup requests (10 threads) isolated from staff check-in API
- Per-service timeouts (svc-reservations: 2s, svc-guest-profiles: 1s, svc-safety-compliance: 3s, svc-gear-inventory: 3s, svc-partner-integrations: 30s)
- Graceful degradation for non-critical services (safety-compliance and gear-inventory can return null without blocking check-in)
- Connection pool sizing review for all downstream HTTP clients

**Residual Risk**: Low-Medium (requires load testing to validate thresholds)
