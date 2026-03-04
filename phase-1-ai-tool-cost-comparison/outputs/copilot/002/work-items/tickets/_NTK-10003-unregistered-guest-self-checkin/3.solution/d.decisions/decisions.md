# NTK-10003 - Architecture Decision Records

---

## ADR-NTK10003-001: Orchestrator Pattern for Unregistered Guest Check-in

### Status

Accepted

### Date

2026-01-29

### Context and Problem Statement

The unregistered guest reservation lookup flow requires coordination across 4-5 downstream services (svc-reservations, svc-guest-profiles, svc-safety-compliance, svc-gear-inventory, and optionally svc-partner-integrations). The flow includes conditional branching (partner fallback), parallel execution (safety + gear checks), and session creation. What coordination pattern should be used?

### Decision Drivers

- Domain cohesion: check-in domain logic should be co-located in the service that already owns registered guest check-in
- Testability: orchestration logic with branching and parallelism must be unit-testable with mocked dependencies
- Separation of concerns: API gateway should handle cross-cutting concerns (rate limiting, auth), not business logic
- Conditional logic complexity: partner fallback requires sequential decision branching that is difficult to express in event chains
- Response time budget: 8-second end-to-end target requires deterministic flow control with per-step timeouts
- Synchronous interaction model: kiosk guest waits for an immediate answer; eventual consistency is not acceptable

### Considered Options

1. **Orchestration in svc-check-in** -- Central orchestrator coordinates all downstream calls with explicit flow control
2. **Choreography via events** -- Each service reacts to events published by the previous step; no central coordinator
3. **Hybrid** -- Event-driven for async steps (profile creation, analytics), orchestrated for synchronous verification flow

### Decision Outcome

**Chosen Option**: "Orchestration in svc-check-in", because the flow requires conditional branching (partner fallback), sequential dependency resolution (reservation must be found before profile lookup), strict response time budgets (8 seconds), and synchronous request-response semantics for the kiosk interaction.

### Consequences

#### Positive

- Domain logic remains cohesive in the service that already owns registered guest check-in
- Complex branching (partner fallback) and parallel execution (safety + gear) are expressed in application code, making them testable and debuggable
- API gateway remains clean -- handles only rate limiting, authentication, and routing
- Deterministic flow control enables precise timeout budgets per step (2s + 1s + 3s + 1s + 1s buffer = 8s total)
- The existing CheckInController.java already has a stub for `POST /lookup-reservation` (line 34-41), confirming the architectural intent

#### Negative

- svc-check-in takes on additional complexity and 5 new downstream dependencies
- Circuit breaker patterns must be implemented in application code for partner integration fallback
- The svc-check-in team must maintain knowledge of downstream service contracts
- Single point of failure if svc-check-in is down (mitigated by existing redundancy and load balancing)

#### Neutral

- Post-check-in analytics events (e.g., `checkin.completed`) can still be published to Kafka as the existing registered check-in flow does

### Pros and Cons of the Options

#### Orchestration in svc-check-in

- Good, because explicit flow control supports conditional branching (partner fallback) and parallel execution
- Good, because synchronous request-response matches kiosk interaction model (guest waits for result)
- Good, because per-step timeouts enable precise response budget management
- Neutral, because adds 5 downstream dependencies to svc-check-in
- Bad, because single point of failure if svc-check-in is down

#### Choreography via events

- Good, because services are fully decoupled; no central coordinator to maintain
- Good, because adding new steps does not require changes to a central orchestrator
- Bad, because conditional branching (partner fallback) is difficult to express in event chains
- Bad, because response time is unpredictable -- each event hop adds latency and the kiosk requires synchronous response
- Bad, because error handling and compensation logic is distributed across services, making debugging difficult
- Bad, because the kiosk guest cannot wait for eventual consistency

#### Hybrid (orchestrated verification plus event-driven async)

- Good, because separates synchronous verification from asynchronous post-processing
- Neutral, because adds infrastructure complexity (event bus for post-processing, HTTP for verification)
- Bad, because the verification flow (the critical path) still requires orchestration, so the hybrid adds complexity without simplifying the core problem

---

## ADR-NTK10003-002: Four-Field Identity Verification

### Status

Accepted

### Date

2026-01-29

### Context and Problem Statement

Unregistered guests at self-service kiosks must be verified against their reservation before gaining kiosk access. The verification mechanism must work reliably across all booking sources (direct, partner, gift card) while providing reasonable security against unauthorized access. Partner bookings frequently have the travel agent's contact information rather than the guest's, which eliminates email and phone as reliable verification fields.

### Decision Drivers

- Partner bookings often have the travel agent's email/phone, not the guest's -- verification fields must be consistently available regardless of booking source
- Security must be sufficient for a kiosk environment without being burdensome -- this is not a financial transaction
- No dependency on external SMS/email infrastructure for OTP delivery
- All four fields must be present in reservation data across all booking sources (direct, ExploreMore, TrailFinder, WildPass)
- Rate limiting and artificial delays provide supplementary security beyond the verification fields

### Considered Options

1. **Email-based verification** -- Confirmation code + email address
2. **Phone-based verification** -- Confirmation code + phone + SMS OTP
3. **Four-field verification** -- Last name + confirmation code + adventure date + participant count

### Decision Outcome

**Chosen Option**: "Four-field verification", because the four selected fields are consistently available across all booking sources and do not depend on external infrastructure. The confirmation code provides primary secret (8-character alphanumeric); the remaining three fields prevent casual guessing.

### Consequences

#### Positive

- Reliable across all booking sources -- no dependency on guest email/phone accuracy
- No SMS infrastructure dependency (avoids international SMS delivery issues at future international locations)
- Confirmation code provides primary entropic security; other fields prevent casual guessing
- All four fields are naturally known to the guest from their booking confirmation email/document

#### Negative

- Lower security assurance than OTP-based verification (mitigated by rate limiting: 5 attempts per kiosk per 15-minute window, and 2-second artificial delay on failures per security review by Marcus Chen)
- Participant count changes after booking (e.g., companion added or removed) could cause verification failures (mitigated by directing guest to service desk with priority queuing)
- Requires all fields to be accurately synchronized across reservation data sources (mitigated by nightly partner data sync with validation)

#### Neutral

- The 8-character alphanumeric confirmation code provides approximately 2.8 trillion possible values, making enumeration impractical even without rate limiting

---

## ADR-NTK10003-003: Temporary Guest Profile Strategy

### Status

Accepted

### Date

2026-01-30

### Context and Problem Statement

The kiosk check-in flow requires a guest profile ID for session management, waiver association, and analytics tracking. Unregistered guests do not have NovaTrek accounts. Should they be required to register before accessing the kiosk, or should the system accommodate them with temporary profiles?

Source code analysis confirms that the current `GuestService.createGuest()` method requires email for duplicate detection (`guestRepository.findByEmail()`), which is not available for partner-booked guests. A new creation path is needed.

### Decision Drivers

- Reducing check-in friction is the primary goal of the feature -- requiring full registration would negate the benefit
- The staff-assisted check-in flow is slow (22 minutes average) precisely because it involves extensive data collection
- Post-check-in registration prompts ("Want faster check-in next time?") achieve higher conversion rates (35-45%) than pre-check-in registration gates (12%)
- Data retention policies require PII cleanup for unclaimed temporary profiles
- Deduplication must prevent multiple temporary profiles for the same reservation (session re-verification scenario)

### Considered Options

1. **Require full account registration** -- Guest must register before kiosk access
2. **Temporary guest profile** -- Create a minimal profile with only last name and reservation ID; deduplication by reservation_id instead of email

### Decision Outcome

**Chosen Option**: "Temporary guest profile", because requiring full registration defeats the purpose of reducing friction. A minimal profile (last_name + reservation_id) enables the kiosk session while deferring account creation to a post-check-in prompt where conversion rates are higher.

### Consequences

#### Positive

- Minimal friction -- only last name and reservation ID needed (no email required)
- Enables post-check-in registration prompt with higher conversion potential
- Automatic 90-day anonymization satisfies data retention policies
- Profile merge preserves check-in history when guest later creates a full account
- Deduplication by reservation_id prevents duplicate profiles across session re-verifications

#### Negative

- svc-guest-profiles must support a new `TEMPORARY` profile type with reduced required fields, adding complexity to the profile model
- The existing `GuestService.createGuest()` email deduplication path cannot be reused; a new `createTemporaryProfile()` method is needed
- Background anonymization job must be built and monitored (90-day TTL)
- Profile merge logic must handle edge cases (multiple temporary profiles from different reservations, re-verification after merge)

#### Neutral

- The `profile_type` enum (`REGISTERED`, `TEMPORARY`, `COMPANION`) can be extended for future use cases without schema changes

---

## ADR-NTK10003-004: Session-Scoped Kiosk Access with JWT

### Status

Accepted

### Date

2026-02-05

### Context and Problem Statement

Temporary kiosk access must be time-bounded to prevent misuse, ensure kiosk availability for other guests, and scope data access to only the matched reservation. What session mechanism and duration should be used?

### Decision Drivers

- 95% of registered guest check-ins complete within 12 minutes (observed metric)
- First-time waiver completion takes up to 20 minutes (worst case)
- Kiosk availability must not be blocked by abandoned sessions
- JWT tokens with embedded expiry are self-validating without per-request server-side lookup
- Security review (Marcus Chen) requires session scoping to a specific kiosk device ID
- One active session per kiosk prevents session stacking

### Considered Options

1. **15-minute session** -- Tight, efficient, but risks timeout during waiver completion
2. **30-minute session** -- Comfortable buffer for all scenarios
3. **No fixed expiry** -- Session ends on check-in completion or navigation away

### Decision Outcome

**Chosen Option**: "30-minute session with JWT", because it provides comfortable buffer for first-time waiver completion (up to 20 minutes) while preventing indefinite kiosk occupation. JWT with embedded expiry, kiosk device ID claim, and Redis-backed session storage provides defense in depth.

### Consequences

#### Positive

- 30 minutes comfortably covers even the slowest check-in scenarios (waiver + gear + briefing)
- JWT with embedded expiry is self-validating -- no per-request session lookup needed for most operations
- Scoping to kiosk device ID prevents token reuse on other devices
- One active session per kiosk (enforced via Redis secondary key) prevents session stacking
- Redis TTL automatically cleans up expired sessions without a background job

#### Negative

- Guests exceeding 30 minutes must re-verify (expected to be rare based on 95th percentile data)
- Kiosk UI must display countdown timer when under 5 minutes remain to avoid surprise expiry
- Redis dependency added to svc-check-in (already used for caching in other check-in flows)

#### Neutral

- Session duration is configurable via `kiosk.session.expiry-minutes` to allow per-location tuning if needed
