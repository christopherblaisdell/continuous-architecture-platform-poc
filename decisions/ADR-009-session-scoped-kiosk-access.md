# ADR-009: Session-Scoped Kiosk Access for Self-Service Check-In

## Status

Accepted

## Date

2025-01-28

## Context and Problem Statement

Self-service kiosks (NTK-10003) are shared terminals in public areas. Once an unregistered guest completes identity verification and begins the check-in flow, the kiosk holds a reference to their temporary profile and reservation. Without session management, the guest's data could remain accessible on the kiosk screen after they walk away, or a subsequent user could resume a previous session. How should kiosk sessions be scoped and secured?

## Decision Drivers

- PII protection: guest data displayed on a kiosk screen must not persist after the session ends
- Session hijacking prevention: a subsequent kiosk user must not be able to access a previous guest's check-in
- Operational simplicity: kiosk terminals are stateless thin clients -- session state must be server-managed
- Timeout behavior: sessions must expire automatically if a guest abandons the kiosk mid-flow

## Considered Options

1. **JWT-based session with 30-minute expiry** -- server issues a short-lived JWT after identity verification; all subsequent kiosk API calls include the token; token expires after 30 minutes or on check-in completion
2. **Server-side session with cookie** -- traditional HTTP session stored server-side, referenced by a session cookie on the kiosk browser
3. **No session** -- each kiosk API call re-verifies identity using the four-field verification; no persistent session state

## Decision Outcome

**Chosen Option**: "JWT-based session with 30-minute expiry", because JWTs are stateless on the server side (no session store to manage), the 30-minute TTL ensures automatic expiry for abandoned sessions, and the token can encode the `guest_id` and `reservation_id` claims to scope all subsequent API calls without re-verification.

### Confirmation

- `POST /check-ins/self-service/unregistered` returns a `session_token` (JWT) on successful identity verification
- JWT contains claims: `guest_id`, `reservation_id`, `kiosk_id`, `exp` (30-minute TTL)
- All subsequent kiosk API calls require `Authorization: Bearer <session_token>`
- Token is invalidated server-side on check-in completion (`POST /check-ins/{id}/complete`)
- Kiosk UI clears local state and token reference on session end or expiry

## Consequences

### Positive

- Automatic 30-minute expiry ensures abandoned sessions do not leave guest data accessible
- Stateless JWT verification -- no server-side session store required, reducing infrastructure complexity
- Token claims scope API access to a specific guest and reservation -- prevents cross-session data leakage
- Kiosk thin-client model preserved -- all session logic is server-side

### Negative

- JWTs cannot be revoked before expiry without a server-side blocklist (mitigated by short 30-minute TTL)
- If a guest's check-in takes longer than 30 minutes (rare edge case), they must re-verify
- Token must be stored in kiosk browser memory (not localStorage) to prevent persistence across sessions

### Neutral

- 30-minute TTL was chosen based on average kiosk interaction time (8-12 minutes) with a safety margin
- The 15-minute cache TTL for profile data (separate from session TTL) prevents stale data from being served during the session

## Pros and Cons of the Options

### JWT-based session with 30-minute expiry

- **Good**, because stateless server-side -- no session store infrastructure needed
- **Good**, because automatic expiry protects abandoned sessions
- **Good**, because token claims scope access to specific guest and reservation
- **Neutral**, because 30-minute TTL balances security with usability
- **Bad**, because token revocation before expiry requires a server-side blocklist

### Server-side session with cookie

- **Good**, because immediate server-side revocation is straightforward
- **Bad**, because requires a shared session store (Redis or similar) across check-in service instances
- **Bad**, because session cookies on shared kiosk terminals create CSRF and persistence risks
- **Bad**, because adds infrastructure dependency for session storage

### No session

- **Good**, because simplest approach -- no session state to manage
- **Bad**, because re-verifying identity on every API call adds latency and friction
- **Bad**, because the four-field verification would need to be repeated for gear pickup, wristband assignment, and every sub-step
- **Bad**, because no mechanism to detect or prevent a different person resuming an abandoned flow

## More Information

- Origin: NTK-10003 Solution Design (unregistered guest self-service check-in)
- Services: svc-check-in (session issuer and validator)
- Related: [ADR-007 Four-Field Identity Verification](ADR-007-four-field-identity-verification.md), [ADR-008 Temporary Guest Profile](ADR-008-temporary-guest-profile.md)
- Security: kiosk JWT tokens MUST be stored in memory only (not localStorage or sessionStorage) to prevent persistence
