# NTK-10003 - Risk Assessment

## RISK-001: Identity Verification Security

**Category**: Security
**Likelihood**: Medium
**Impact**: High

**Description**: The four-field verification (last name, confirmation code, adventure date, participant count) provides reasonable but not strong identity assurance. An attacker with knowledge of a guest's last name and confirmation code could potentially bypass verification by guessing date and participant count.

**Mitigation**:
- Rate limiting: 5 attempts per kiosk per 15-minute window (per kiosk device ID)
- 2-second artificial delay on failed lookups to slow enumeration
- All verification fields submitted via POST body (never URL params) to prevent PII exposure in logs
- PII masked in application logs (last 3 characters of last name only)
- All attempts (success and failure) logged for SOC security monitoring
- Defense-in-depth: rate limiting at both API gateway and application level

## RISK-002: Temporary Profile Data Retention

**Category**: Data/Compliance
**Likelihood**: Low
**Impact**: Medium

**Description**: Temporary guest profiles contain PII (last name) and are linked to reservation data. If the 90-day anonymization job fails or is delayed, PII may be retained beyond the intended retention period, creating compliance risk.

**Mitigation**:
- Automated anonymization job runs daily at 02:00 UTC with monitoring and alerting
- Job failure triggers immediate alert to the platform operations team
- Manual anonymization procedure documented as fallback
- Temporary profiles are created with minimal PII (last name only; no email, phone, or DOB)

## RISK-003: Partner Integration Availability

**Category**: Operational
**Likelihood**: Medium
**Impact**: Medium

**Description**: The partner fallback path depends on svc-partner-integrations being available and the upstream partner APIs (ExploreMore, TrailFinder, WildPass) being responsive. If partner systems are down during peak check-in hours, partner-booked unregistered guests cannot use the kiosk.

**Mitigation**:
- Circuit breaker pattern: 30-second timeout, 50% error rate threshold, 60-second recovery window
- When partner lookup is unavailable, clear messaging directs guest to service desk with priority queuing
- Nightly partner booking sync reduces dependency on real-time partner API calls (most bookings are pre-synced)

## RISK-004: Check-in Load During Peak Hours

**Category**: Operational
**Likelihood**: Medium
**Impact**: Medium

**Description**: Enabling kiosk check-in for unregistered guests increases the load on svc-check-in and downstream services. During peak arrival windows (7:00-9:00 AM), the new endpoint could see high concurrent usage across multiple kiosks.

**Mitigation**:
- Performance target: 100 concurrent lookup requests with p95 under 5 seconds
- Phased rollout: start with Cascade Ridge base camp only (lowest volume), expand after validation
- Feature flag `KIOSK_UNREGISTERED_CHECKIN_ENABLED` per base camp enables gradual rollout
- Safety and gear checks parallelized to reduce sequential latency

## RISK-005: Safety Compliance for Unregistered Guests

**Category**: Compliance
**Likelihood**: Low
**Impact**: Critical

**Description**: Unregistered guests who bypass or skip the waiver signing step during kiosk check-in could participate in adventures without proper safety documentation. The kiosk flow must enforce waiver completion with the same rigor as the staff-assisted flow.

**Mitigation**:
- Waiver completion status is checked in Step 4 of the orchestration flow
- If waiver is incomplete, the kiosk displays the digital waiver URL and blocks check-in completion until signed
- Check-in cannot reach COMPLETE status without waiver_verified = true (existing enforcement in svc-check-in)
- The orchestrator does not create a shortcut around existing safety enforcement logic
