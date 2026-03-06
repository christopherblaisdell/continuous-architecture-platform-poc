# NTK-10003: Impact 2 - svc-guest-profiles (MODERATE)

## Service

**svc-guest-profiles** -- Manages guest identity, profile data, and account lifecycle.

## Impact Level

MODERATE -- New endpoint and data model extension required.

## Changes Required

### New Endpoint

`POST /guest-profiles/temporary` -- Creates a minimal temporary guest profile for unregistered kiosk check-in.

**Request Schema**:
```json
{
  "last_name": "string (required)",
  "reservation_id": "string (UUID, required)"
}
```

**Response**: Standard GuestProfile response with `profile_type: "TEMPORARY"`.

### Data Model Extension

Add `profile_type` field to the guest profile model:

| Field | Type | Values | Default |
|-------|------|--------|---------|
| profile_type | String (enum) | REGISTERED, TEMPORARY, COMPANION | REGISTERED |

### Deduplication Logic

Before creating a new temporary profile, check if one already exists for the given `reservation_id`. If found, return the existing profile. This prevents accumulation of duplicate temporary profiles from repeated kiosk attempts.

### Profile Merge

When a guest with a TEMPORARY profile later creates a full REGISTERED account, the merge process must:

1. Transfer check-in history from the temporary profile to the registered profile
2. Transfer waiver associations
3. Mark the temporary profile as MERGED (not deleted, for audit trail)
4. Link the merged profile ID to the registered profile for reference

### Anonymization Background Job

Temporary profiles that are not merged within 90 days must be anonymized:

- Replace `last_name` with SHA-256 hash
- Clear any other PII fields
- Set `profile_type` to ANONYMIZED
- Retain aggregated analytics data (check-in counts, adventure types)

## Estimated Effort

3 days (Lisa Nakamura, svc-guest-profiles Lead)
