# NTK-10003 - Assumptions

## A1: Partner Reservation Data Is Available via Existing Integrations

All three current partner systems (ExploreMore, TrailFinder, WildPass) expose booking verification APIs that accept confirmation code and last name as lookup fields. The svc-partner-integrations service already has adapters for these APIs. No new partner onboarding is required for this feature.

**Risk if invalid**: If a partner does not support verification by these fields, guests booked through that partner will fall back to staff-assisted check-in. This is an acceptable degraded experience.

## A2: Temporary Guest Profiles Do Not Require Email or Phone

Temporary guest profiles can be created with only a last name and reservation ID. Email and phone collection is deferred to an optional post-check-in account registration prompt. This aligns with the minimal data collection principle and avoids blocking check-in on data that may not be available for partner-booked guests.

## A3: Digital Waiver Signing Is Supported on Kiosk Hardware

All base camp kiosks have touchscreen capability sufficient for digital waiver signature capture. The svc-safety-compliance digital waiver flow (released in 2025-Q3) is compatible with the kiosk browser environment. No hardware upgrades are required.

## A4: Confirmation Codes Are Unique Across All Booking Sources

Reservation confirmation codes are globally unique -- no two reservations (whether booked directly or through partners) share the same confirmation code. Partner confirmation codes are prefixed with a partner identifier (e.g., `EM-`, `TF-`, `WP-`) that prevents collisions with NovaTrek-native codes.

## A5: Reservation Data Includes Participant Count

All reservation records, including those synced from partner systems, include an accurate participant count field. This field is used as one of the four identity verification inputs. Partner-synced reservations are validated for this field during the nightly sync process.

## A6: Initial Rollout Scope Is Limited to North American Base Camps

The first release targets North American base camps only. International locations have additional regulatory requirements for guest identity verification (e.g., passport-based verification in EU locations) that are out of scope for this iteration. International expansion will be addressed in a follow-up ticket.

## A7: Kiosk Sessions Are Single-Use

Each successful reservation lookup grants a single kiosk session. If the session expires before check-in is complete (30-minute timeout) or the guest navigates away, they must re-enter their verification fields to start a new session. Session tokens are not transferable between kiosks.

## A8: Existing Rate Limiting Infrastructure Supports Per-Device Rules

The API gateway supports rate limiting rules scoped to specific request attributes (in this case, `kiosk_device_id`). The rate limit of 5 attempts per kiosk per 15-minute window can be implemented using existing gateway configuration without custom development.
