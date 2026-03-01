# NTK-10003 - Architecture Decision Records

## ADR-1: Orchestrator Pattern in svc-check-in

### Context

The reservation lookup flow requires coordination across 4-5 downstream services. Two approaches were considered for managing this orchestration:

- **Option A**: Orchestration in svc-check-in (service-level orchestrator)
- **Option B**: Orchestration at the API gateway layer (gateway composition)

### Decision

**Option A: Orchestration in svc-check-in.**

### Rationale

- svc-check-in owns the check-in domain and already contains business logic for the registered guest check-in flow. Adding the unregistered flow here keeps domain logic cohesive.
- The orchestration includes conditional branching (partner fallback), parallel execution (safety + gear), and session creation -- logic that is better expressed in application code than gateway configuration.
- API gateway orchestration would create tight coupling between infrastructure configuration and business logic, making the flow harder to test and evolve.
- The gateway remains responsible for cross-cutting concerns (rate limiting, authentication) as appropriate.

### Consequences

- svc-check-in takes on additional complexity and downstream dependencies
- Circuit breaker patterns must be implemented in application code for partner integration fallback
- The svc-check-in team must maintain knowledge of downstream service contracts

---

## ADR-2: Four-Field Identity Verification

### Context

Multiple approaches were considered for verifying unregistered guest identity:

- **Option A**: Email-based verification (confirmation code + email)
- **Option B**: Phone-based verification (confirmation code + phone + SMS OTP)
- **Option C**: Four-field verification (last name + confirmation code + adventure date + participant count)

### Decision

**Option C: Four-field verification.**

### Rationale

- Partner bookings frequently contain the travel agent's email or phone rather than the guest's personal contact information, making Options A and B unreliable for this guest segment.
- The four selected fields are consistently available across all booking sources (direct, partner, gift card).
- The combination provides reasonable security: confirmation code provides the primary secret, while the other three fields prevent casual guessing even if a confirmation code is observed.
- No dependency on SMS infrastructure, which reduces complexity and avoids international SMS delivery issues for future expansion.

### Consequences

- Lower security assurance than OTP-based verification, mitigated by rate limiting and artificial delays
- All four fields must be accurately maintained in reservation data across all booking sources
- Participant count changes (if guests modify their reservation after booking) could cause verification failures -- messaging must guide guests to the service desk in these cases

---

## ADR-3: Temporary Guest Profile Creation

### Context

The kiosk check-in flow requires a guest profile ID for session management, waiver association, and analytics. Two approaches were considered:

- **Option A**: Require full account registration before kiosk access
- **Option B**: Create a temporary guest profile with minimal data

### Decision

**Option B: Temporary guest profile creation.**

### Rationale

- Requiring full registration defeats the purpose of reducing friction for unregistered guests. The current staff-assisted flow is slow precisely because it involves data collection.
- A temporary profile with only last name and reservation ID is sufficient for the check-in flow.
- Temporary profiles enable a post-check-in registration prompt ("Want faster check-in next time? Create an account!") that is more effective than a pre-check-in registration gate.
- Temporary profiles are automatically anonymized after 90 days, satisfying data retention policies.
- If the guest later creates a full account, the temporary profile is merged to preserve check-in history.

### Consequences

- svc-guest-profiles must support a new `TEMPORARY` profile type with reduced required fields
- A background job is needed for 90-day anonymization of unclaimed temporary profiles
- Profile merge logic must handle edge cases (e.g., multiple temporary profiles for the same guest across visits)

---

## ADR-4: Session-Scoped Kiosk Access with 30-Minute Expiry

### Context

Temporary kiosk access must be time-bounded to prevent misuse and ensure kiosk availability. The session duration was debated:

- **Option A**: 15-minute session
- **Option B**: 30-minute session
- **Option C**: No fixed expiry (session ends when check-in completes or guest navigates away)

### Decision

**Option B: 30-minute session.**

### Rationale

- 15 minutes was deemed too short for guests who need to complete digital waiver signing (which includes reading safety information and providing a signature), review gear assignments, and acknowledge the adventure briefing.
- Data from the registered guest kiosk flow shows that 95% of check-ins complete within 12 minutes, but guests completing waivers for the first time take up to 20 minutes.
- A 30-minute window provides comfortable buffer without holding kiosk resources excessively.
- No-expiry sessions create a risk of unattended kiosks remaining in an authenticated state.
- JWT tokens with embedded expiry are self-validating and do not require server-side session lookups for every request.

### Consequences

- Guests who exceed 30 minutes must re-verify (expected to be rare based on usage data)
- Kiosk UI must display a countdown timer when under 5 minutes remain
- One active session per kiosk device prevents session stacking
