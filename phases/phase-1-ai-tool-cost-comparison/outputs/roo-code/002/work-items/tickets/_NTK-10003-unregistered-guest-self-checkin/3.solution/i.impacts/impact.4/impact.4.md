# NTK-10003 - Impact 4: svc-reservations

**Impact Level**: MODERATE

## Overview

svc-reservations must support a new composite search endpoint that enables reservation lookup by the four verification fields (last_name, confirmation_code, adventure_date, participant_count) used during unregistered guest kiosk check-in.

## Changes Required

### New Endpoint

**POST /reservations/search**

Performs a composite lookup using all four verification fields. All fields must match for a reservation to be returned.

Request:
```json
{
  "last_name": "string (required, case-insensitive)",
  "confirmation_code": "string (required, 8 chars, normalized to uppercase)",
  "adventure_date": "string (required, ISO 8601 date)",
  "participant_count": "integer (required, 1-20)"
}
```

Response (200 OK):
```json
{
  "reservation_id": "string (UUID)",
  "confirmation_code": "string",
  "adventure_name": "string",
  "adventure_date": "string (ISO 8601)",
  "participant_count": "integer",
  "booking_source": "string (WEBSITE | MOBILE_APP | PARTNER_API | CALL_CENTER | WALK_IN)",
  "primary_guest_last_name": "string",
  "participants": [
    {
      "name": "string",
      "role": "PRIMARY | COMPANION"
    }
  ]
}
```

Response (404 Not Found): Reservation not found for the given combination of fields.

### Database Index

A composite index is required for the search query:

```sql
CREATE INDEX idx_reservation_composite_lookup
ON reservations (
  UPPER(primary_guest_last_name),
  UPPER(confirmation_code),
  adventure_date,
  participant_count
);
```

Per Sam Okonkwo (svc-reservations lead, Comment 8), current search indexes are optimized for `reservation_id` and `guest_id` lookups. The composite index is estimated at 2 days of work.

### Confirmation Code Handling

Confirmation codes are 8-character alphanumeric, case-insensitive. The search endpoint must normalize to uppercase before querying. The composite search must match ALL four fields -- partial matches are not returned to prevent enumeration.

## Deployment Notes

- Deploy BEFORE svc-check-in (dependency order)
- Database migration required for composite index creation
- No breaking changes to existing API contracts
- The POST method is used (not GET) because verification fields include PII (last_name) that must not appear in URL query parameters per security review (Marcus Chen, Comment 3)
- Estimated effort: 2 days (Sam Okonkwo)
