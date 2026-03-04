# NTK-10003 - Impact 1: svc-check-in

**Impact Level**: PRIMARY -- This service receives the largest change scope.

## Overview

svc-check-in is the orchestrating service for the unregistered guest self-service check-in flow. It receives the enhanced `POST /check-ins/lookup-reservation` endpoint and contains all orchestration logic for coordinating verification across downstream services.

## Current State Analysis

The existing `CheckInController.java` contains a stub implementation of `POST /lookup-reservation` (lines 34-41) that:

- Accepts a raw `Map<String, String>` with only `confirmationCode` and `lastName`
- Lacks input validation (no `@Valid` annotation, no typed request DTO)
- Does not include `adventure_date`, `participant_count`, or `kiosk_device_id`
- Returns a plain `CheckInRecord` rather than the enriched session response
- Delegates to `checkInService.lookupReservation()` which likely returns `Optional<CheckInRecord>`

This stub must be replaced with the full orchestration implementation.

## Changes Required

### Endpoint Replacement

- Replace the existing stub `POST /check-ins/lookup-reservation` with a fully typed endpoint
- Create a dedicated `ReservationLookupRequest` DTO with `@Valid` annotations for all five fields
- Create a `ReservationLookupResponse` DTO for the enriched session response

### New Components

| Component | Purpose |
|-----------|---------|
| `ReservationLookupController` | HTTP layer: request validation, response mapping, error handling |
| `ReservationLookupService` | Orchestration logic: sequencing downstream calls, parallel execution, fallback handling |
| `KioskSessionManager` | JWT token generation (30-min expiry), Redis session storage, one-session-per-kiosk enforcement |
| `LookupRateLimiter` | Application-level rate limiting via Redis (defense in depth alongside API gateway) |

### New Service Clients

| Client | Target Service | Purpose | Timeout |
|--------|----------------|---------|---------|
| `ReservationSearchClient` | svc-reservations | Search reservations by four verification fields | 2s |
| `TemporaryGuestProfileClient` | svc-guest-profiles | Create or find temporary guest profiles | 1s |
| `WaiverStatusClient` | svc-safety-compliance | Check waiver completion by reservation_id | 3s |
| `GearAssignmentClient` | svc-gear-inventory | Retrieve gear assignments by reservation_id | 3s |
| `PartnerVerificationClient` | svc-partner-integrations | Fallback booking verification with circuit breaker | 30s |

### Configuration Changes

| Property | Value | Purpose |
|----------|-------|---------|
| `kiosk.session.expiry-minutes` | 30 | JWT session duration |
| `kiosk.lookup.rate-limit.max-attempts` | 5 | Max attempts per kiosk per window |
| `kiosk.lookup.rate-limit.window-seconds` | 900 | Rate limit window (15 min) |
| `kiosk.lookup.failure-delay-ms` | 2000 | Artificial delay on failed lookups |
| `partner.circuit-breaker.timeout-ms` | 30000 | Partner integration timeout |
| `partner.circuit-breaker.error-threshold` | 0.5 | Circuit breaker error rate trigger |
| `partner.circuit-breaker.recovery-window-ms` | 60000 | Circuit breaker recovery window |
| `feature.kiosk-unregistered-checkin.enabled` | false | Feature flag (per base camp) |

### Dependencies Added

- Redis (for session storage and rate limiting counters)
- HTTP clients for svc-reservations, svc-guest-profiles, svc-safety-compliance, svc-gear-inventory, svc-partner-integrations

## API Contract Change

### Before (current stub)

```
POST /check-ins/lookup-reservation
Content-Type: application/json

{"confirmationCode": "A1B2C3D4", "lastName": "Smith"}
```

### After (full implementation)

```
POST /check-ins/lookup-reservation
Content-Type: application/json

{
  "last_name": "Smith",
  "confirmation_code": "A1B2C3D4",
  "adventure_date": "2026-03-01",
  "participant_count": 2,
  "kiosk_device_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

This is a breaking change to the stub request format. Since the stub is not in production use (no consumers), backwards compatibility is not required.

## Deployment Notes

- svc-check-in must be deployed LAST in the deployment sequence (after all upstream services)
- Feature flag defaults to `false`; enable per base camp according to phased rollout plan
- Redis must be provisioned/verified in each base camp environment before deployment
