# NTK-10003: Impact 4 - svc-reservations (MODERATE)

## Service

**svc-reservations** -- Manages reservation lifecycle, booking data, and reservation search.

## Impact Level

MODERATE -- New composite search endpoint and database index required.

## Changes Required

### New Endpoint

`POST /reservations/search` -- Composite search endpoint for reservation lookup by four verification fields.

**Request Schema**:
```json
{
  "last_name": "string (required, case-insensitive match)",
  "confirmation_code": "string (required, normalized to uppercase)",
  "adventure_date": "string (required, ISO 8601 date)",
  "participant_count": "integer (required)"
}
```

**Response**: Standard Reservation response if all four fields match a single reservation. Returns 404 if no match or multiple ambiguous matches.

### Database Index

A composite index is required to support the four-field lookup without full table scans:

```sql
CREATE INDEX idx_reservation_lookup 
ON reservations (
    UPPER(confirmation_code), 
    UPPER(last_name), 
    adventure_date, 
    participant_count
);
```

Per Sam Okonkwo (svc-reservations Lead), the current search indexes are optimized for `reservation_id` and `guest_id` lookups. The composite index for the four-field search requires approximately 2 days of work.

### Confirmation Code Normalization

Confirmation codes are 8-character alphanumeric, case-insensitive. The search endpoint must normalize to uppercase before querying. Partner-prefixed codes (e.g., `EM-A1B2C3D4`) should be accepted with or without the hyphenated prefix.

### Security Considerations

- The search endpoint must use POST (not GET) to keep PII out of URL parameters and access logs
- Response must not reveal which specific field failed to match (prevent enumeration)
- Rate limiting is handled by the calling service (svc-check-in) and API gateway, not by svc-reservations itself

## Estimated Effort

2 days (Sam Okonkwo, svc-reservations Lead)
