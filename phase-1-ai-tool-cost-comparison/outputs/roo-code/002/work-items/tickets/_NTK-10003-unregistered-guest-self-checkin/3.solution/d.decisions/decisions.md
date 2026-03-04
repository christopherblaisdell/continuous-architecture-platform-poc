# NTK-10003 - Architecture Decision Records

---

## ADR-NTK10003-001: Orchestrator Pattern in svc-check-in

### Status
Accepted

### Date
2026-01-29

### Context and Problem Statement
The unregistered guest reservation lookup flow requires coordination across 4-5 downstream services. The flow includes conditional branching (partner fallback), parallel execution (safety + gear checks), and session creation. What coordination pattern should be used?

### Decision Drivers
- Domain cohesion: check-in domain logic should be co-located
- Synchronous request-response required for kiosk interaction
- 8-second end-to-end response time budget requires deterministic flow control
- Conditional logic complexity: partner fallback requires sequential branching

### Considered Options
1. **Orchestration in svc-check-in** -- Central orchestrator coordinates all downstream calls
2. **Choreography via events** -- Each service reacts to events; no central coordinator
3. **Hybrid** -- Event-driven for async steps, orchestrated for synchronous verification

### Decision Outcome
**Chosen Option**: "Orchestration in svc-check-in", because the flow requires conditional branching (partner fallback), sequential dependency resolution, strict response time budgets, and synchronous request-response semantics.

### Consequences
#### Positive
- Complex branching and parallel execution are testable and debuggable in application code
- Deterministic flow control enables precise per-step timeout budgets (2s + 1s + 3s + 1s + 1s = 8s)
- API gateway remains clean -- handles only rate limiting, authentication, and routing

#### Negative
- svc-check-in takes on 5 new downstream dependencies
- Circuit breaker patterns must be implemented for partner integration fallback

---

## ADR-NTK10003-002: Four-Field Identity Verification

### Status
Accepted

### Date
2026-01-29

### Context and Problem Statement
Unregistered guests at self-service kiosks must be verified against their reservation. The verification mechanism must work across all booking sources (direct, partner, gift card) while providing reasonable security.

### Decision Drivers
- Partner bookings often have the travel agent's email/phone, not the guest's
- All four fields must be consistently available across all booking sources
- No dependency on external SMS/email infrastructure

### Considered Options
1. **Email-based verification** -- Confirmation code + email address
2. **Phone-based verification** -- Confirmation code + phone + SMS OTP
3. **Four-field verification** -- Last name + confirmation code + adventure date + participant count

### Decision Outcome
**Chosen Option**: "Four-field verification", because the selected fields are consistently available across all booking sources and do not depend on external infrastructure.

### Consequences
#### Positive
- Reliable across all booking sources -- no dependency on guest email/phone accuracy
- No SMS infrastructure dependency (avoids international delivery issues)
- Confirmation code provides primary secret; other fields prevent casual guessing

#### Negative
- Lower security assurance than OTP-based verification (mitigated by rate limiting and artificial delays)
- Participant count changes after booking could cause verification failures

---

## ADR-NTK10003-003: Temporary Guest Profile Creation

### Status
Accepted

### Date
2026-01-30

### Context and Problem Statement
The kiosk check-in flow requires a guest profile ID for session management, waiver association, and analytics. Unregistered guests do not have NovaTrek accounts. Should they register, or should the system create temporary profiles?

### Decision Drivers
- Reducing friction is the primary goal
- Post-check-in registration prompts achieve higher conversion (35-45%) than upfront gates (12%)
- Data retention policies require PII cleanup for unclaimed profiles

### Considered Options
1. **Require full account registration** -- Guest must register before kiosk access
2. **Temporary guest profile** -- Create minimal profile with only last name and reservation ID

### Decision Outcome
**Chosen Option**: "Temporary guest profile", because requiring full registration defeats the purpose of reducing friction, and a post-check-in registration prompt is more effective for conversion.

### Consequences
#### Positive
- Minimal friction -- only last name and reservation ID needed
- Enables post-check-in registration with higher conversion potential
- 90-day anonymization satisfies data retention policies
- Profile merge preserves history when guest later creates full account

#### Negative
- svc-guest-profiles must support TEMPORARY profile type with reduced required fields
- Background anonymization job must be built and monitored

---

## ADR-NTK10003-004: Session-Scoped Kiosk Access with 30-Minute Expiry

### Status
Accepted

### Date
2026-02-05

### Context and Problem Statement
Temporary kiosk access must be time-bounded to prevent misuse and ensure kiosk availability. What session duration is appropriate?

### Decision Drivers
- 95% of registered guest check-ins complete within 12 minutes
- First-time waiver completion takes up to 20 minutes
- JWT tokens with embedded expiry are self-validating

### Considered Options
1. **15-minute session** -- Tight, efficient
2. **30-minute session** -- Comfortable buffer for first-time waiver completion
3. **No fixed expiry** -- Session ends on completion

### Decision Outcome
**Chosen Option**: "30-minute session", because it provides comfortable buffer for first-time waiver completion while preventing indefinite kiosk occupation.

### Consequences
#### Positive
- Covers even the slowest check-in scenarios (waiver + gear + briefing)
- JWT with embedded expiry is self-validating -- no per-request session lookup
- One active session per kiosk device prevents session stacking

#### Negative
- Guests exceeding 30 minutes must re-verify (expected to be rare)
- Kiosk UI must display countdown timer when under 5 minutes remain
