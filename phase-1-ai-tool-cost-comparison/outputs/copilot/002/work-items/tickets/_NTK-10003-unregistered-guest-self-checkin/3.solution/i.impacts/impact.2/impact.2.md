# NTK-10003 - Impact 2: svc-guest-profiles

**Impact Level**: MODERATE

## Overview

svc-guest-profiles must support the creation and management of temporary guest profiles for unregistered guests who use the kiosk check-in flow. These profiles have a reduced set of required fields and a defined lifecycle that differs from standard registered profiles.

## Current State Analysis

The current `GuestService.java` creates guest profiles with mandatory email for deduplication:

```java
Optional<GuestProfile> existing = guestRepository.findByEmail(guest.getEmail());
```

The `CreateGuestRequest` schema in the OpenAPI spec requires `first_name`, `last_name`, `email`, `date_of_birth`, and `emergency_contact`. None of these fields (except `last_name`) are reliably available for unregistered guests, particularly partner-booked guests.

The `Guest` schema does not include a `profile_type` field. All profiles are implicitly `REGISTERED`.

## Changes Required

### Data Model Extension

Add `profile_type` field to the Guest model:

| Value | Description |
|-------|-------------|
| `REGISTERED` | Full NovaTrek account holder (existing, default for all current records) |
| `TEMPORARY` | Created during unregistered kiosk check-in |
| `COMPANION` | Added as companion to another guest's reservation |

### New Endpoint

**POST /guest-profiles/temporary**

Creates a temporary guest profile with minimal required fields.

Request:

```json
{
  "last_name": "string (required)",
  "reservation_id": "string (required, UUID)"
}
```

Response (201 Created):

```json
{
  "guest_profile_id": "string (UUID)",
  "profile_type": "TEMPORARY",
  "last_name": "string",
  "reservation_id": "string (UUID)",
  "created_at": "string (ISO 8601)"
}
```

### New Service Method

A new `createTemporaryProfile()` method in `GuestService` that:

- Accepts only `last_name` and `reservation_id` as required fields
- Uses `reservation_id` for deduplication (not email)
- Sets `profile_type` to `TEMPORARY`
- Does NOT require email, first_name, date_of_birth, or emergency_contact

### Deduplication Logic

Before creating a new temporary profile, check for existing profiles linked to the same reservation ID. If one exists, return the existing profile instead of creating a duplicate. This handles cases where a guest re-verifies after a session expiry.

### Profile Merge

When a guest with a temporary profile later creates a full NovaTrek account, the temporary profile must be merged:

- Copy check-in history from temporary to registered profile
- Update waiver associations to point to registered profile
- Mark temporary profile as `MERGED` (soft delete, retain for audit)

### Background Job: Temporary Profile Anonymization

- Run daily at 02:00 UTC
- Select all `TEMPORARY` profiles older than 90 days that are not in `MERGED` status
- Anonymize PII fields (replace last_name with hash, clear any optional data)
- Retain anonymized record for aggregate analytics

## Schema Impact

The `Guest` schema in the OpenAPI spec must be extended with:

```yaml
profile_type:
  type: string
  enum: [REGISTERED, TEMPORARY, COMPANION]
  description: Type of guest profile. Defaults to REGISTERED for existing records.
  default: REGISTERED
reservation_id:
  type: string
  format: uuid
  nullable: true
  description: Linked reservation ID for TEMPORARY profiles. Null for REGISTERED profiles.
```

## Deployment Notes

- Deploy BEFORE svc-check-in
- Database migration required for `profile_type` column (add with default value `REGISTERED` for all existing records)
- Database migration required for `reservation_id` column (nullable)
- No breaking changes to existing API contracts (additive fields and new endpoint)
