# NTK-10003 - Impact 1: svc-check-in

**Impact Level**: PRIMARY

## Overview

svc-check-in is the orchestration hub for the unregistered guest self-service check-in flow. It receives the kiosk verification request, coordinates downstream service calls, manages rate limiting, and creates the temporary kiosk session.

## Changes Required

### New Endpoint

**POST /check-ins/lookup-reservation** -- Accepts verification fields (last_name, confirmation_code, adventure_date, participant_count, kiosk_device_id) and returns a JWT session token with reservation details.

### New Components

| Component | Responsibility |
|-----------|---------------|
| LookupReservationController | REST controller for the new endpoint; input validation and normalization |
| ReservationLookupOrchestrator | Coordinates the 5-step verification flow with conditional branching and parallel execution |
| KioskSessionManager | Creates and manages JWT sessions scoped to kiosk device IDs; stores sessions in Redis |
| RateLimitFilter | Enforces 5 attempts per kiosk per 15-minute window with 2-second artificial delay on failures |

### Orchestration Flow

1. Rate limit check (short-circuit on exceeded)
2. Input validation and normalization (uppercase confirmation code, date validation)
3. Reservation lookup via svc-reservations (with partner fallback)
4. Guest profile find-or-create via svc-guest-profiles
5. Parallel: waiver check (svc-safety-compliance) + gear check (svc-gear-inventory)
6. JWT session creation with 30-minute expiry

### Response Time Budget

| Step | Budget | Service |
|------|--------|---------|
| Reservation lookup | 2 seconds | svc-reservations |
| Guest profile | 1 second | svc-guest-profiles |
| Safety + gear (parallel) | 3 seconds | svc-safety-compliance, svc-gear-inventory |
| Session creation | 1 second | Local + Redis |
| Buffer | 1 second | -- |
| **Total** | **8 seconds** | |

### Estimated Effort

5 days (Dev Patel, svc-check-in lead)
