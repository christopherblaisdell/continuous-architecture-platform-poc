# NTK-10003 - Architecture Decision Records

---

## ADR-NTK10003-001: Orchestrator Pattern in svc-check-in

### Status

Accepted

### Date

2026-01-29

### Context and Problem Statement

The unregistered guest reservation lookup flow requires coordination across 4-5 downstream services (svc-reservations, svc-guest-profiles, svc-safety-compliance, svc-gear-inventory, and optionally svc-partner-integrations). The flow includes conditional branching (partner fallback), parallel execution (safety + gear checks), and session creation. What coordination pattern should be used?

### Decision Drivers

- Domain cohesion: check-in domain logic should be co-located
- Testability: orchestration logic with branching and parallelism must be unit-testable
- Response time budget: 8-second end-to-end target requires deterministic flow control
- Conditional logic complexity: partner fallback requires sequential decision branching
- Team ownership: svc-check-in team already owns the registered guest check-in flow

### Considered Options

1. **Orchestration in svc-check-in** -- Central orchestrator coordinates all downstream calls with explicit flow control
2. **Choreography via events** -- Each service reacts to events; no central coordinator
3. **Hybrid** -- Event-driven for async steps, orchestrated for synchronous verification

### Decision Outcome

**Chosen Option**: "Orchestration in svc-check-in", because the flow requires conditional branching (partner fallback), sequential dependency resolution (reservation must be found before profile lookup), strict response time budgets (8 seconds), and synchronous request-response semantics for the kiosk interaction.

### Consequences

#### Positive

- Domain logic remains cohesive in the service that already owns registered guest check-in
- Complex branching and parallel execution are testable in application code
- API gateway remains clean -- handles only rate limiting, authentication, and routing
- Deterministic flow control enables precise timeout budgets per step

#### Negative

- svc-check-in takes on additional complexity and 5 new downstream dependencies
- Circuit breaker patterns must be implemented for partner integration fallback
- The svc-check-in team must maintain knowledge of downstream service contracts

### Pros and Cons of the Options

#### Orchestration in svc-check-in

- **Good**, because explicit flow control supports conditional branching and parallel execution
- **Good**, because synchronous request-response matches kiosk interaction model
- **Good**, because per-step timeouts enable precise response budget management (2s + 1s + 3s + 1s + 1s = 8s)
- **Neutral**, because adds 5 downstream dependencies to svc-check-in
- **Bad**, because single point of failure if svc-check-in is down

#### Choreography via events

- **Good**, because services are fully decoupled
- **Bad**, because conditional branching is difficult in event chains
- **Bad**, because response time is unpredictable -- kiosk requires synchronous response
- **Bad**, because error handling distributed across services makes debugging difficult

#### Hybrid

- **Good**, because separates synchronous verification from async post-processing
- **Bad**, because the verification flow still requires orchestration, so hybrid adds complexity without simplifying the core problem

---

## ADR-NTK10003-002: Four-Field Identity Verification

### Status

Accepted

### Date

2026-01-29

### Context and Problem Statement

Unregistered guests at self-service kiosks must be verified against their reservation before gaining kiosk access. The verification mechanism must work reliably across all booking sources (direct, partner, gift card) while providing reasonable security.

### Decision Drivers

- Partner bookings often have the travel agent's email/phone, not the guest's
- All four fields must be consistently available across all booking sources
- Security must be sufficient without being burdensome
- No dependency on external SMS/email infrastructure

### Considered Options

1. **Confirmation code only** -- Single-field verification for maximum simplicity
2. **Confirmation code + ID scan** -- Code plus physical document scan at kiosk
3. **Four-field verification** -- Last name + confirmation code + adventure date + participant count

### Decision Outcome

**Chosen Option**: "Four-field verification", because the four selected fields are consistently available across all booking sources, provide adequate security without external infrastructure, and balance convenience with protection against casual guessing.

### Consequences

#### Positive

- Reliable across all booking sources -- no dependency on guest email/phone accuracy
- No SMS infrastructure dependency (avoids international SMS delivery issues)
- Confirmation code provides primary secret; other fields prevent casual guessing
- No hardware requirements beyond the existing kiosk touchscreen

#### Negative

- Lower security assurance than OTP-based or biometric verification (mitigated by rate limiting)
- Participant count changes after booking could cause verification failures
- All fields must be accurately maintained across reservation data sources

---

## ADR-NTK10003-003: Temporary Guest Profile Creation

### Status

Accepted

### Date

2026-01-30

### Context and Problem Statement

The kiosk check-in flow requires a guest profile ID for session management, waiver association, and analytics. Unregistered guests do not have NovaTrek accounts. Should they be required to register, or should the system accommodate them with temporary profiles?

### Decision Drivers

- Reducing friction is the primary goal
- Post-check-in registration prompts are more effective than pre-check-in gates
- Data retention policies require PII cleanup for unclaimed profiles

### Considered Options

1. **Full profile** -- Require full account registration before kiosk access
2. **Ephemeral profile** -- In-memory only, discarded after session
3. **Temporary profile** -- Minimal persistent profile with 90-day TTL and merge capability

### Decision Outcome

**Chosen Option**: "Temporary profile", because requiring full registration defeats the purpose of reducing friction, ephemeral profiles lose data for analytics and audit, and a persistent temporary profile with TTL and merge supports both the immediate need and future account conversion.

### Consequences

#### Positive

- Minimal friction -- only last name and reservation ID needed
- Post-check-in registration prompt achieves higher conversion potential
- 90-day anonymization satisfies data retention policies
- Profile merge preserves check-in history when guest later registers

#### Negative

- svc-guest-profiles must support a new TEMPORARY profile type
- Anonymization background job must be built and monitored
- Profile merge logic must handle edge cases (multiple temporary profiles)

---

## ADR-NTK10003-004: Session-Scoped Kiosk Access with 30-Minute Expiry

### Status

Accepted

### Date

2026-02-05

### Context and Problem Statement

Temporary kiosk access must be time-bounded to prevent misuse and ensure kiosk availability. What is the appropriate session duration?

### Decision Drivers

- 95% of registered guest check-ins complete within 12 minutes
- First-time waiver completion takes up to 20 minutes
- Kiosk availability must not be blocked by abandoned sessions
- JWT tokens with embedded expiry are self-validating

### Considered Options

1. **15-minute session** -- Tight, efficient
2. **30-minute session** -- Comfortable buffer
3. **No fixed expiry** -- Session ends on completion or navigation away

### Decision Outcome

**Chosen Option**: "30-minute session", because it provides comfortable buffer for first-time waiver completion while preventing indefinite kiosk occupation.

### Consequences

#### Positive

- 30 minutes comfortably covers even the slowest check-in scenarios
- JWT with embedded expiry is self-validating -- no per-request session lookup
- One active session per kiosk device prevents session stacking

#### Negative

- Guests exceeding 30 minutes must re-verify (expected to be rare)
- Kiosk UI must display countdown timer when under 5 minutes remain
