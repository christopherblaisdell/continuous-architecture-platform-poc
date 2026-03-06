# NTK-10003 - Impact 1: svc-check-in

**Impact Level**: PRIMARY -- This service receives the largest change scope.

## Overview

svc-check-in is the orchestrating service for the unregistered guest self-service check-in flow. It receives the expanded `POST /check-ins/lookup-reservation` endpoint and contains all orchestration logic for coordinating verification across downstream services.

## Current State

The `CheckInController.java` already contains a `POST /lookup-reservation` stub that accepts a `Map<String, String>` with only `confirmationCode` and `lastName`. The existing stub returns a `CheckInRecord` via `checkInService.lookupReservation()`. This must be replaced with a fully typed request DTO, proper orchestration, and a structured response.

The existing check-in model (`CheckIn` schema) includes `reservation_id`, `participant_guest_id`, `status`, `wristband`, `gear_verified`, and `waiver_verified` fields. The new endpoint must produce a response that bridges the reservation lookup result into this existing check-in model.

## Changes Required

### Endpoint Expansion

- Replace the untyped `Map<String, String>` request body with a `ReservationLookupRequest` DTO containing all 5 fields: `last_name`, `confirmation_code`, `adventure_date`, `participant_count`, `kiosk_device_id`
- Return a `ReservationLookupResponse` DTO with session token, reservation details, check-in status, and participant list

### New Components

| Component | Purpose |
|-----------|---------|
| `ReservationLookupRequest` | Typed request DTO with validation annotations |
| `ReservationLookupResponse` | Structured response with session and check-in status |
| `ReservationLookupService` | Orchestration logic: sequencing downstream calls, parallel execution, fallback handling |
| `KioskSessionManager` | JWT token generation with `kiosk_device_id` claim, Redis session storage, 30-min expiry |
| `LookupRateLimiter` | Application-level rate limiting (defense in depth alongside API gateway) |

### New Service Clients

| Client | Target Service | Purpose |
|--------|----------------|---------|
| `ReservationSearchClient` | svc-reservations | Search reservations by 4 verification fields |
| `TemporaryGuestProfileClient` | svc-guest-profiles | Create or find temporary guest profiles |
| `WaiverStatusClient` | svc-safety-compliance | Check waiver completion by reservation ID |
| `GearAssignmentClient` | svc-gear-inventory | Retrieve gear assignments by reservation ID |
| `PartnerVerificationClient` | svc-partner-integrations | Fallback booking verification with circuit breaker |

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

## API Contract Change

- **Change Type**: Existing endpoint expansion (from 2-field to 5-field request, new response structure)
- **Breaking Change**: Yes for the existing stub (currently returns `CheckInRecord`; will return new `ReservationLookupResponse`). However, the existing stub is not exposed to any consumer yet.
- **New Fields**: session_token, check_in_status, participants in response
- **Removed Fields**: None from public API

## Deployment Notes

- svc-check-in must be deployed LAST in the deployment sequence (after all upstream services)
- Feature flag defaults to `false`; enable per base camp according to phased rollout plan
- Redis must be provisioned and verified in each base camp environment before deployment
