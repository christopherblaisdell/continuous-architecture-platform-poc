# NTK-10003 - Impact 4: svc-reservations

**Impact Level**: MODERATE

## Overview

svc-reservations must support a new search endpoint that allows looking up reservations by the four identity verification fields used in the kiosk check-in flow. The current API only supports search by `guest_id`, `trip_id`, `status`, and date range. The `Reservation` schema does not currently include a `confirmation_code` field.

## Current State

The existing `GET /reservations` endpoint supports:
- `guest_id` (UUID query parameter)
- `trip_id` (UUID query parameter)
- `status` (ReservationStatus enum)
- `start_date` / `end_date` (date range)
- `page` / `size` (pagination)

The `Reservation` schema includes: `id`, `guest_id`, `trip_id`, `status`, `booking_source`, `participants[]`, `gear_package_id`, `special_requirements`, `emergency_contact`, `payment_reference`, `total_amount`, `currency`, `created_at`, `updated_at`, `_rev`. Notably absent: `confirmation_code`, `adventure_date`, `adventure_name`.

The `BookingSource` enum includes `PARTNER_API` which is relevant for partner fallback identification.

## Changes Required

### Schema Extension

Add fields to the `Reservation` schema:
- `confirmation_code`: string, 8 characters alphanumeric, case-insensitive
- `adventure_date`: date, derived from the associated trip schedule
- `adventure_name`: string, denormalized from svc-trip-catalog for display

### New Endpoint

**POST /reservations/search**

Searches for a reservation matching all four verification fields. Uses POST to keep PII (last_name) out of URL query parameters per security review.

Request:
```json
{
  "last_name": "string (required, case-insensitive match)",
  "confirmation_code": "string (required, normalized to uppercase)",
  "adventure_date": "string (required, ISO 8601 date)",
  "participant_count": "integer (required)"
}
```

Response (200 OK):
```json
{
  "reservation_id": "string (UUID)",
  "confirmation_code": "string",
  "adventure_name": "string",
  "adventure_date": "string (ISO 8601)",
  "base_camp": "string",
  "booking_source": "DIRECT | PARTNER",
  "partner_id": "string (nullable)",
  "participants": [
    {
      "name": "string",
      "role": "PRIMARY | COMPANION"
    }
  ]
}
```

Response (404 Not Found): Standard error envelope when no matching reservation is found.

### Composite Index

Create a composite database index on: `(confirmation_code, adventure_date, participant_count, LOWER(last_name))`

This index supports the exact query pattern used by the verification flow. The `LOWER()` function index enables case-insensitive last name matching without full table scans.

Estimated index creation time: 2 hours on production data volume (can be created concurrently without table lock on PostgreSQL using `CREATE INDEX CONCURRENTLY`).

### Confirmation Code Normalization

Per Sam Okonkwo (svc-reservations lead): confirmation codes are 8-character alphanumeric, case-insensitive. The search endpoint should normalize to uppercase before querying. Accept both `EM-A1B2C3D4` and `EMA1B2C3D4` formats (strip hyphens).

## API Contract Change

- **Change Type**: New endpoint, schema extension
- **Breaking Change**: No (new endpoint only, schema additions are additive)
- **Backward Compatible**: Yes

## Deployment Notes

- Deploy BEFORE svc-check-in
- Run index migration during off-peak hours (recommended: 02:00-04:00 UTC)
- Use `CREATE INDEX CONCURRENTLY` to avoid table locks during index creation
- No breaking changes to existing API contracts (new endpoint only)
