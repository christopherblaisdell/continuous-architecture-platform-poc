# NTK-10003 - Risks

## R1: Reservation Enumeration Attacks

**Likelihood**: Medium | **Impact**: High

**Description**: Malicious actors could attempt to enumerate valid reservation confirmation codes by submitting systematic lookup requests through the kiosk. Successful enumeration could expose guest names and adventure details.

**Mitigation**:

- Rate limiting: 5 attempts per kiosk per 15-minute window at both API gateway and application level (defense in depth)
- 2-second artificial delay on failed lookups to slow automated attempts
- Vague error messaging ("We couldn't find a matching reservation") that does not confirm which field was incorrect
- All failed attempts logged with correlation ID for SOC monitoring with alerting on anomalous patterns
- Kiosk-scoped rate limits prevent a single compromised kiosk from being used as an enumeration tool
- Confirmation code entropy (8 alphanumeric characters, approximately 2.8 trillion possible values) makes systematic enumeration impractical

**Residual Risk**: Low (after mitigations applied)

## R2: Partner Data Inconsistency

**Likelihood**: Medium | **Impact**: Medium

**Description**: Partner booking data may be inconsistent with the reservation record in svc-reservations. Common issues include: different last name spelling, participant count mismatches due to post-booking modifications, and confirmation code format variations. This would cause verification failures for legitimate guests.

**Evidence**: The current svc-reservations OpenAPI spec does not include a `confirmation_code` field, suggesting that partner confirmation code synchronization may not yet be formalized. This increases the risk of data format inconsistencies.

**Mitigation**:

- Confirmation code normalization (strip hyphens, uppercase) reduces format-related mismatches
- Partner data sync runs nightly with validation checks and discrepancy reporting
- Error messaging directs guests to staff desk with priority queuing when verification fails
- Dashboard metric tracks partner-booked verification failure rate to identify systemic data quality issues
- Partner fallback path in the orchestrator provides a secondary verification mechanism

**Residual Risk**: Low-Medium (data quality is an ongoing operational concern)

## R3: Temporary Profile Accumulation

**Likelihood**: Low | **Impact**: Medium

**Description**: High volumes of temporary guest profiles could accumulate if the 90-day anonymization job fails or if unexpected usage patterns create large numbers of profiles. This could impact svc-guest-profiles query performance and storage costs.

**Mitigation**:

- Deduplication logic prevents multiple temporary profiles for the same reservation
- 90-day anonymization background job with monitoring and alerting on job failures
- Database monitoring for temporary profile table growth rate
- Manual cleanup procedure documented in operations runbook

**Residual Risk**: Low

## R4: Downstream Service Cascading Failures

**Likelihood**: Low | **Impact**: High

**Description**: The orchestrator in svc-check-in depends on 4-5 downstream services. If multiple services experience latency or failures simultaneously, the orchestrator could exhaust its thread pool or connection pool, causing cascading failures that affect registered guest check-in as well.

**Mitigation**:

- Per-service timeouts prevent any single downstream service from blocking the entire flow (2s + 1s + 3s = 6s total, within 8s budget)
- Circuit breaker on partner integration with automatic recovery
- Graceful degradation for non-critical services: waiver and gear checks return null on failure rather than blocking check-in
- Bulkhead pattern: separate thread pools for lookup-reservation and regular check-in flows to prevent cross-contamination
- svc-check-in health check endpoint monitors downstream dependency health

**Residual Risk**: Low (with proper timeout and bulkhead configuration)

## R5: Session Token Misuse

**Likelihood**: Low | **Impact**: Medium

**Description**: If a session JWT is intercepted (e.g., by observing the kiosk screen), it could theoretically be used from another device to access the guest's reservation data during the 30-minute window.

**Mitigation**:

- JWT includes `kiosk_device_id` claim; requests from other devices are rejected
- One active session per kiosk device (Redis enforcement); new sessions invalidate existing ones
- 30-minute hard expiry limits the exposure window
- Session grants read-only access to the matched reservation; no write operations possible without additional authorization

**Residual Risk**: Low

## R6: Staff Process Change Resistance

**Likelihood**: Medium | **Impact**: Low

**Description**: Front desk staff must understand the new kiosk capability to properly assist guests who have difficulty with the self-service flow. Staff also need to be aware of the "priority queuing" process for guests directed from the kiosk after a failed lookup.

**Mitigation**:

- Training materials prepared for each phase of rollout
- Kiosk displays a "Need Help?" button that alerts the nearest staff member
- Staff dashboard shows real-time kiosk activity including guests who abandoned the self-service flow
- Staff check-in UI shows whether a guest has already attempted kiosk check-in (prevents repeat data collection)
- Phased rollout provides opportunity to refine staff processes before full deployment

**Residual Risk**: Low (with training completed before each phase)
