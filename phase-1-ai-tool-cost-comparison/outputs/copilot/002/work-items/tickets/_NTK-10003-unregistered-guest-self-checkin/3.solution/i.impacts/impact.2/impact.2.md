# NTK-10003 - Impact 2: svc-guest-profiles

**Impact Level**: MODERATE

## Overview

svc-guest-profiles must support the creation and management of temporary guest profiles for unregistered guests who use the kiosk check-in flow. These profiles have a reduced set of required fields and a defined lifecycle that differs from standard registered profiles.

## Current State

The `GuestService.java` performs duplicate detection by email (`guestRepository.findByEmail()`) and requires email for all profile creation. The `CreateGuestRequest` schema requires `first_name`, `last_name`, `email`, `date_of_birth`, and `emergency_contact`. None of these fields besides `last_name` are reliably available for unregistered guests, particularly those booked through travel partners.

The `Guest` schema does not include a `profile_type` discriminator. All profiles are implicitly `REGISTERED`.

## Changes Required

### Data Model Extension

Add `profile_type` field to the Guest model:

| Value | Description |
|-------|-------------|
| `REGISTERED` | Full NovaTrek account holder (existing, default for existing records) |
| `TEMPORARY` | Created during unregistered kiosk check-in |
| `COMPANION` | Added as companion to another guest's reservation |

### New Endpoint

**POST /guest-profiles/temporary**

Creates a temporary guest profile with minimal required fields, bypassing the standard email/DOB/emergency-contact requirements.

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
  "created_at": "string (ISO 8601)"
}
```

### Extended Query Parameter

Add `reservation_id` as a query parameter to `GET /guests`:

| Current | New |
|---------|-----|
| `?q=`, `?email=`, `?status=`, `?certification_type=` | Same + `?reservation_id={UUID}` |

### Deduplication Logic

Before creating a new temporary profile, check for existing profiles linked to the same reservation ID. If one exists, return the existing profile instead of creating a duplicate. This handles cases where a guest re-verifies after a session expiry.

This requires a new lookup path separate from the existing email-based `findByEmail()` deduplication.

### Profile Merge

When a guest with a temporary profile later creates a full NovaTrek account, the temporary profile must be merged:
- Copy check-in history from temporary to registered profile
- Update waiver associations to point to registered profile
- Mark temporary profile as `MERGED` (soft delete, retain for audit)

### Background Job: Temporary Profile Anonymization

- Run daily at 02:00 UTC
- Select all `TEMPORARY` profiles older than 90 days that are not in `MERGED` status
- Anonymize PII fields (replace last_name with hash, clear any collected data)
- Retain anonymized record for aggregate analytics

## Deployment Notes

- Deploy BEFORE svc-check-in
- Database migration required for `profile_type` column (add with default value `REGISTERED` for existing records)
- No breaking changes to existing API contracts (new endpoint and additive query parameter only)
