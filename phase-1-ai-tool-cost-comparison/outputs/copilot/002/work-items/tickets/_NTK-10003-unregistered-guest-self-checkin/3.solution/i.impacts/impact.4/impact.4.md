# NTK-10003 - Impact 4: svc-reservations

**Impact Level**: MODERATE

## Overview

svc-reservations must support a new search endpoint that allows looking up reservations by the four identity verification fields used in the kiosk check-in flow. Additionally, the `Reservation` schema must be extended with a `confirmation_code` field that is currently missing from the OpenAPI specification.

## Current State Analysis

The current `GET /reservations` search supports filtering by:

- `guest_id` (UUID)
- `trip_id` (UUID)
- `status` (enum)
- `start_date` / `end_date` (date range)
- Pagination (`page`, `size`)

The following gaps exist:

1. **No `confirmation_code` field** in the `Reservation` schema. The solution design assumes confirmation codes exist, but the spec does not expose them. This field must be added to both the schema and the data model.
2. **No composite search** by last_name + confirmation_code + adventure_date + participant_count. The current search is optimized for `reservation_id` and `guest_id` direct lookups.
3. **No last_name association** in the reservation data. Last name must be resolved via the `guest_id` relationship to svc-guest-profiles, or denormalized onto the reservation for query performance.

## Changes Required

### Schema Extension

Add `confirmation_code` to the `Reservation` schema:

```yaml
confirmation_code:
  type: string
  pattern: '^[A-Za-z0-9]{2,3}-?[A-Za-z0-9]{6,8}$'
  description: |
    Unique reservation confirmation code. For direct bookings, this is an
    8-character alphanumeric code. For partner bookings, includes a partner
    prefix (e.g., EM-A1B2C3D4 for ExploreMore). Case-insensitive; stored
    and queried in uppercase.
  example: "A1B2C3D4"
```

### New Endpoint

**POST /reservations/search**

Searches for a reservation matching all four verification fields. Uses POST to avoid PII in URL query parameters (per security review).

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

Estimated index creation time: may take up to 2 hours on production data volume. Can be created concurrently without table lock on PostgreSQL using `CREATE INDEX CONCURRENTLY`.

### Last Name Resolution

Two approaches for resolving `last_name` in the search query:

1. **Join approach**: Query joins reservation data with participant/guest data to match last name. More normalized, but adds query complexity.
2. **Denormalization approach**: Store the primary guest's last name directly on the reservation record. Simpler queries, but requires sync when the guest updates their name.

Recommendation: Denormalization approach for query performance, with an event listener to update the denormalized field when guest profile changes occur.

## Backward Compatibility

- The `confirmation_code` field addition is additive (nullable for existing records that may lack this data)
- The new `POST /reservations/search` endpoint is entirely new -- no existing consumers affected
- The existing `GET /reservations` search endpoint is unchanged

## Deployment Notes

- Deploy BEFORE svc-check-in
- Database migration: add `confirmation_code` column to reservations table
- Database migration: create composite index (run during off-peak hours, 02:00-04:00 UTC recommended)
- Backfill existing reservations with confirmation codes if not already present in the database (the field may exist in the DB but not in the API spec)
- No breaking changes to existing API contracts (new endpoint and additive schema field)
