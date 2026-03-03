# NTK-10003 - Architecture Decision Records

---

## ADR-NTK10003-001: Orchestrator Pattern in svc-check-in

### Status

Accepted

### Date

2026-01-29

### Context and Problem Statement

The unregistered guest reservation lookup flow requires coordination across 4-5 downstream services (svc-reservations, svc-guest-profiles, svc-safety-compliance, svc-gear-inventory, and optionally svc-partner-integrations). The flow includes conditional branching (partner fallback), parallel execution (safety + gear checks), and synchronous session creation. What coordination pattern should be used?

### Decision Drivers

- Domain cohesion: check-in domain logic should be co-located
- Testability: orchestration logic with branching and parallelism must be unit-testable
- Separation of concerns: API gateway should handle cross-cutting concerns, not business logic
- Team ownership: svc-check-in team already owns the registered guest check-in flow and the existing `POST /lookup-reservation` stub
- Conditional logic complexity: partner fallback requires sequential decision branching
- Response time budget: 8-second end-to-end target requires deterministic flow control

### Considered Options

1. **Orchestration in svc-check-in** - Central orchestrator coordinates all downstream calls with explicit flow control
2. **Choreography via events** - Each service reacts to events published by the previous step; no central coordinator
3. **Hybrid** - Event-driven for async steps (profile creation, analytics), orchestrated for synchronous verification flow

### Decision Outcome

**Chosen Option**: "Orchestration in svc-check-in", because the flow requires conditional branching (partner fallback), sequential dependency resolution (reservation must be found before profile lookup), strict response time budgets (8 seconds), and synchronous request-response semantics for the kiosk interaction.

### Consequences

#### Positive

- Domain logic remains cohesive in the service that already owns registered guest check-in
- Complex branching (partner fallback) and parallel execution (safety + gear) are expressed in application code, making them testable and debuggable
- API gateway remains clean -- handles only rate limiting, authentication, and routing
- Deterministic flow control enables precise timeout budgets per step: reservation lookup (2s) + guest profile (1s) + parallel safety/gear (3s) + session creation (1s) + buffer (1s) = 8s total
- Existing `POST /lookup-reservation` stub in CheckInController.java provides a foundation to extend

#### Negative

- svc-check-in takes on additional complexity and 5 new downstream dependencies
- Circuit breaker patterns must be implemented in application code for partner integration fallback
- The svc-check-in team must maintain knowledge of downstream service contracts

### Pros and Cons of the Options

#### Orchestration in svc-check-in

- **Good**, because explicit flow control supports conditional branching (partner fallback) and parallel execution
- **Good**, because synchronous request-response matches kiosk interaction model (guest waits for result)
- **Good**, because per-step timeouts enable precise response budget management
- **Neutral**, because adds 5 downstream dependencies to svc-check-in
- **Bad**, because single point of failure if svc-check-in is down

#### Choreography via events

- **Good**, because services are fully decoupled; no central coordinator to maintain
- **Bad**, because conditional branching (partner fallback) is difficult to express in event chains
- **Bad**, because response time is unpredictable -- each event hop adds latency and the kiosk requires synchronous response
- **Bad**, because error handling and compensation logic is distributed across services, making debugging difficult

#### Hybrid

- **Good**, because separates synchronous verification from asynchronous post-processing
- **Neutral**, because adds infrastructure complexity (event bus for post-processing, HTTP for verification)
- **Bad**, because the verification flow (the critical path) still requires orchestration

---

## ADR-NTK10003-002: Four-Field Identity Verification

### Status

Accepted

### Date

2026-01-29

### Context and Problem Statement

Unregistered guests at self-service kiosks must be verified against their reservation before gaining kiosk access. The verification mechanism must work reliably across all booking sources (direct, partner, gift card) while providing reasonable security against unauthorized access.

The existing `POST /lookup-reservation` endpoint in CheckInController.java currently accepts only two fields (`confirmationCode` and `lastName`). The security review by Marcus Chen requires stronger verification without depending on email or phone infrastructure.

### Decision Drivers

- Partner bookings often have the travel agent's email/phone, not the guest's
- All four fields must be consistently available across all booking sources
- Security must be sufficient without being burdensome (this is a kiosk, not a bank)
- No dependency on external SMS/email infrastructure
- Confirmation codes are 8-character alphanumeric per svc-reservations team

### Considered Options

1. **Email-based verification** - Confirmation code + email address
2. **Phone-based verification** - Confirmation code + phone + SMS OTP
3. **Four-field verification** - Last name + confirmation code + adventure date + participant count

### Decision Outcome

**Chosen Option**: "Four-field verification", because the four selected fields are consistently available across all booking sources and do not depend on external infrastructure.

### Consequences

#### Positive

- Reliable across all booking sources -- no dependency on guest email/phone accuracy
- No SMS infrastructure dependency (avoids international SMS delivery issues)
- Confirmation code provides primary secret; other fields prevent casual guessing
- All four fields confirmed available in the NovaTrek reservation data model and partner sync data

#### Negative

- Lower security assurance than OTP-based verification (mitigated by rate limiting and 2-second artificial delays on failure)
- Participant count changes after booking could cause verification failures (mitigated by using original booking count)
- Requires all fields to be accurately maintained across reservation data sources
- Requires a new `POST /reservations/search` endpoint and composite database index in svc-reservations

---

## ADR-NTK10003-003: Temporary Guest Profile Creation

### Status

Accepted

### Date

2026-01-30

### Context and Problem Statement

The kiosk check-in flow requires a guest profile ID for session management, waiver association, and analytics. Unregistered guests do not have NovaTrek accounts. The current `GuestService.createGuest()` method in svc-guest-profiles requires an email address and performs duplicate detection by email. The `CreateGuestRequest` schema requires `first_name`, `last_name`, `email`, `date_of_birth`, and `emergency_contact` -- fields that may not be available for partner-booked or gift-card guests.

Should unregistered guests be required to register, or should the system accommodate them with temporary profiles?

### Decision Drivers

- Reducing friction is the primary goal of the feature
- The staff-assisted flow is slow precisely because it involves data collection
- Post-check-in registration prompts are more effective than pre-check-in registration gates (12% vs 35-45% expected conversion)
- Data retention policies require PII cleanup for unclaimed profiles

### Considered Options

1. **Require full account registration** - Guest must register before kiosk access (requires email, DOB, emergency contact per current schema)
2. **Temporary guest profile** - Create a minimal profile with only last name and reservation ID via a new `POST /guest-profiles/temporary` endpoint

### Decision Outcome

**Chosen Option**: "Temporary guest profile", because requiring full registration defeats the purpose of reducing friction, and a post-check-in registration prompt ("Want faster check-in next time?") is more effective.

### Consequences

#### Positive

- Minimal friction -- only last name and reservation ID needed
- Enables post-check-in registration prompt with higher conversion potential
- Automatic 90-day anonymization satisfies data retention policies
- Profile merge preserves check-in history when guest later creates a full account

#### Negative

- svc-guest-profiles must support a new `TEMPORARY` profile type with reduced required fields (bypassing email/DOB/emergency contact requirements)
- Background anonymization job must be built and monitored
- Profile merge logic must handle edge cases (multiple temporary profiles across visits)
- Deduplication must switch from email-based (current) to reservation_id-based for temporary profiles

---

## ADR-NTK10003-004: Session-Scoped Kiosk Access with 30-Minute Expiry

### Status

Accepted

### Date

2026-02-05

### Context and Problem Statement

Temporary kiosk access must be time-bounded to prevent misuse and ensure kiosk availability for other guests. What is the appropriate session duration?

### Decision Drivers

- 95% of registered guest check-ins complete within 12 minutes
- First-time digital waiver completion takes up to 20 minutes
- Kiosk availability must not be blocked by abandoned sessions
- JWT tokens with embedded expiry are self-validating (no server-side lookup per request)
- Security review requires kiosk device ID in JWT claims

### Considered Options

1. **15-minute session** - Tight, efficient
2. **30-minute session** - Comfortable buffer for first-time waiver completion
3. **No fixed expiry** - Session ends on completion or navigation away

### Decision Outcome

**Chosen Option**: "30-minute session", because it provides comfortable buffer for first-time waiver completion while preventing indefinite kiosk occupation.

### Consequences

#### Positive

- 30 minutes comfortably covers even the slowest check-in scenarios (waiver + gear + briefing)
- JWT with embedded expiry is self-validating -- no per-request session lookup needed
- One active session per kiosk device prevents session stacking

#### Negative

- Guests exceeding 30 minutes must re-verify (expected to be rare)
- Kiosk UI must display countdown timer when under 5 minutes remain
