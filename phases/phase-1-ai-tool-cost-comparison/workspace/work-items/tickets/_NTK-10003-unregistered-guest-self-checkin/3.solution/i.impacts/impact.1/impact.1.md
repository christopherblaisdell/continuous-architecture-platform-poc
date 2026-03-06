# NTK-10003 - Impact 1: svc-check-in

**Impact Level**: PRIMARY -- This service receives the largest change scope.

## Overview

svc-check-in is the orchestrating service for the unregistered guest self-service check-in flow. It receives the new `POST /check-ins/lookup-reservation` endpoint and contains all orchestration logic for coordinating verification across downstream services.

## Changes Required

### New Endpoint

- `POST /check-ins/lookup-reservation` -- Accepts verification fields, orchestrates downstream calls, returns kiosk session token with check-in status

### New Components

| Component | Purpose |
|-----------|---------|
| `ReservationLookupController` | HTTP layer: request validation, response mapping |
| `ReservationLookupService` | Orchestration logic: sequencing downstream calls, parallel execution, fallback handling |
| `KioskSessionManager` | JWT token generation, Redis session storage, session expiry management |
| `LookupRateLimiter` | Application-level rate limiting (defense in depth alongside API gateway) |

### New Service Clients

| Client | Target Service | Purpose |
|--------|----------------|---------|
| `ReservationSearchClient` | svc-reservations | Search reservations by verification fields |
| `TemporaryGuestProfileClient` | svc-guest-profiles | Create or find temporary guest profiles |
| `WaiverStatusClient` | svc-safety-compliance | Check waiver completion by reservation ID |
| `GearAssignmentClient` | svc-gear-inventory | Retrieve gear assignments by reservation ID |
| `PartnerVerificationClient` | svc-partner-integrations | Fallback booking verification |

### Configuration Changes

| Property | Value | Purpose |
|----------|-------|---------|
| `kiosk.session.expiry-minutes` | 30 | JWT session duration |
| `kiosk.lookup.rate-limit.max-attempts` | 5 | Max attempts per kiosk per window |
| `kiosk.lookup.rate-limit.window-seconds` | 900 | Rate limit window (15 min) |
| `kiosk.lookup.failure-delay-ms` | 2000 | Artificial delay on failed lookups |
| `partner.circuit-breaker.timeout-ms` | 30000 | Partner integration timeout |
| `partner.circuit-breaker.error-threshold` | 0.5 | Circuit breaker error rate trigger |
| `feature.kiosk-unregistered-checkin.enabled` | false | Feature flag (per base camp) |

### Dependencies Added

- Redis (for session storage and rate limiting counters)
- svc-reservations, svc-guest-profiles, svc-safety-compliance, svc-gear-inventory, svc-partner-integrations (HTTP clients)

## Deployment Notes

- svc-check-in must be deployed LAST in the deployment sequence (after all upstream services)
- Feature flag defaults to `false`; enable per base camp according to phased rollout plan
- Redis must be provisioned/verified in each base camp environment before deployment
