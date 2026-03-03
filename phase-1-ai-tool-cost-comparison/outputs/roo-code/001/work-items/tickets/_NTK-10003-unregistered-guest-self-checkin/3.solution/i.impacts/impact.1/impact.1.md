# NTK-10003: Impact 1 - svc-check-in (PRIMARY)

## Service

**svc-check-in** -- Primary check-in service, orchestrator for the unregistered guest flow.

## Impact Level

PRIMARY -- This service contains the new endpoint and all orchestration logic.

## Changes Required

### New Endpoint

`POST /check-ins/self-service/unregistered` -- Reservation lookup and identity verification for unregistered guests at self-service kiosks.

### New Components

| Component | Responsibility |
|-----------|---------------|
| `ReservationLookupController` | REST controller for the new endpoint; input validation; rate limit check delegation |
| `ReservationLookupService` | Orchestration logic: calls svc-reservations, svc-guest-profiles, svc-safety-compliance, svc-gear-inventory; partner fallback; response aggregation |
| `KioskSessionManager` | JWT session token generation with kiosk device ID claim; Redis session storage; one-session-per-kiosk enforcement |
| `RateLimitService` | Redis-backed sliding window rate limiter (5 attempts per kiosk per 15-minute window); 2-second artificial delay on failed lookups |
| `ReservationClient` | HTTP client for svc-reservations composite search |
| `GuestProfileClient` | HTTP client for svc-guest-profiles temporary profile creation |
| `SafetyComplianceClient` | HTTP client for svc-safety-compliance waiver lookup |
| `GearInventoryClient` | HTTP client for svc-gear-inventory assignment lookup |
| `PartnerIntegrationClient` | HTTP client with circuit breaker for svc-partner-integrations fallback |

### Modified Components

| Component | Change |
|-----------|--------|
| `CheckInController` | Existing `/lookup-reservation` endpoint deprecated in favor of new `/self-service/unregistered` |

### Infrastructure Dependencies

- **Redis**: Required for rate limiting counters and kiosk session storage
- **Circuit breaker**: Resilience4j or similar for partner integration fallback (30s timeout, 50% error threshold)

## Estimated Effort

5 days (Dev Patel, svc-check-in Lead)
