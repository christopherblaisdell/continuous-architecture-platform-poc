# NTK-10003 - Assumptions

## A1: Partner Reservation Data Is Available via Existing Integrations

All three current partner systems (ExploreMore, TrailFinder, WildPass) expose booking verification APIs that accept confirmation code and last name as lookup fields. The svc-partner-integrations service already has adapters for these APIs. No new partner onboarding is required for this feature.

**Risk if invalid**: If a partner does not support verification by these fields, guests booked through that partner will fall back to staff-assisted check-in. This is an acceptable degraded experience but would reduce the percentage of unregistered guests served by the kiosk.

## A2: Temporary Guest Profiles Do Not Require Email or Phone

Temporary guest profiles can be created with only a last name and reservation ID. Email and phone collection is deferred to an optional post-check-in account registration prompt. This is a significant change from the current `GuestService.java` behavior, which requires email for `createGuest()` and uses `findByEmail()` for deduplication. The new `POST /guest-profiles/temporary` endpoint will bypass the email requirement and use reservation_id for deduplication instead.

**Risk if invalid**: If downstream services (safety-compliance, gear-inventory) require email for guest identification, additional adaptation work will be needed.

## A3: Digital Waiver Signing Is Supported on Kiosk Hardware

All base camp kiosks have touchscreen capability sufficient for digital waiver signature capture. The svc-safety-compliance digital waiver flow is compatible with the kiosk browser environment. The existing `GET /waivers` endpoint requires `guest_id` as a required parameter, which will be available from the temporary profile. No hardware upgrades are required.

**Risk if invalid**: If hardware does not support waiver signing, the QR code fallback (complete on personal device) adds complexity. Pre-deployment hardware audit mitigates this.

## A4: Confirmation Codes Are Unique Across All Booking Sources

Reservation confirmation codes are globally unique -- no two reservations (whether booked directly or through partners) share the same confirmation code. Partner confirmation codes are prefixed with a partner identifier (e.g., `EM-` for ExploreMore, `TF-` for TrailFinder, `WP-` for WildPass) that prevents collisions with NovaTrek-native codes. The normalization layer strips these prefixes for storage.

**Risk if invalid**: If collisions occur, the four-field verification (including last_name, adventure_date, participant_count) provides additional disambiguation. Collision probability is extremely low with 8+ character alphanumeric codes.

## A5: Reservation Data Includes Participant Count

All reservation records, including those synced from partner systems, include an accurate participant count field. The current svc-reservations `Reservation` schema has a `participants` array, so count can be derived from array length. Partner-synced reservations are validated for this field during the nightly sync process.

**Risk if invalid**: If participant count is missing or inaccurate for some reservations, the four-field verification would reject legitimate guests. The solution would be to make participant_count optional in the verification flow and compensate with additional verification.

## A6: Initial Rollout Scope Is Limited to North American Base Camps

The first release targets North American base camps only. International locations have additional regulatory requirements for guest identity verification (e.g., passport-based verification in EU locations) that are out of scope for this iteration. International expansion will be addressed in a follow-up ticket.

**Risk if invalid**: If business requires immediate international rollout, additional design work for regulatory compliance would be needed before launch.

## A7: Kiosk Sessions Are Single-Use

Each successful reservation lookup grants a single kiosk session with a 30-minute TTL (stored in Redis). If the session expires before check-in is complete or the guest navigates away, they must re-enter their verification fields to start a new session. Session tokens are not transferable between kiosks. This maps to ADR-NTK10003-004 (session-scoped kiosk access).

**Risk if invalid**: If guests frequently need sessions longer than 30 minutes (e.g., large groups with many waivers), the TTL may need to be configurable per base camp or per group size.

## A8: Existing Rate Limiting Infrastructure Supports Per-Device Rules

The API gateway supports rate limiting rules scoped to specific request attributes (in this case, `kiosk_device_id` from the request body). The rate limit of 5 attempts per kiosk per 15-minute window can be implemented using existing gateway configuration without custom development. Defense-in-depth is provided by application-level Redis rate limiting.

**Risk if invalid**: If the gateway does not support body-parameter-based rate limiting, the rate limit must be implemented entirely at the application level using Redis, which is already part of the design.

## A9: The CheckInController Stub Can Be Replaced Without Breaking Existing Clients

The existing `POST /lookup-reservation` stub in `CheckInController.java` is not yet called by any production client (it returns a placeholder `Map<String,Object>` with "status" = "not implemented"). The stub can be safely removed when the new `ReservationLookupController` is deployed. No API versioning is required.

**Risk if invalid**: If the stub has been integrated by early adopters or internal testing tools, a deprecation period may be needed. This should be verified with the svc-check-in team before deployment.
