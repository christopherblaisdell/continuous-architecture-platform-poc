# NTK-10003 - Impact 4: svc-reservations

**Impact Level**: MODERATE

## Overview

svc-reservations must support a new search endpoint that allows looking up reservations by the four identity verification fields used in the kiosk check-in flow. Current search capabilities are optimized for `reservation_id` and `guest_id` lookups; the new composite search requires a new index.

## Changes Required

### New Endpoint

**POST /reservations/search**

Searches for a reservation matching all four verification fields.

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

Estimated index creation time: 2 hours on production data volume (can be created concurrently without table lock on PostgreSQL).

## Deployment Notes

- Deploy BEFORE svc-check-in
- Run index migration during off-peak hours (recommended: 02:00-04:00 UTC)
- No breaking changes to existing API contracts (new endpoint only)
