# ADR-008: Temporary Guest Profile for Unregistered Check-In

## Status

Accepted

## Date

2025-01-28

## Context and Problem Statement

When an unregistered guest checks in at a self-service kiosk (NTK-10003), a guest profile must be created in svc-guest-profiles to support downstream workflows (wristband assignment, gear verification, safety compliance). However, creating a full guest account for a walkup visitor who may never return introduces data retention concerns and profile management overhead. What type of profile should be created for unregistered guests?

## Decision Drivers

- Data retention compliance: PII collected at the kiosk must be managed according to retention policies
- Profile merge complexity: if the guest later creates a full account, the temporary profile should be mergeable
- Audit trail: safety-critical check-in records must be traceable to a guest identity even after the adventure
- Minimal data collection: only fields strictly necessary for check-in should be required at the kiosk

## Considered Options

1. **Temporary profile** -- a new `TEMPORARY` profile type with minimal required fields and automatic 90-day anonymization
2. **Full profile creation** -- create a standard guest account with all required fields populated at the kiosk
3. **Reservation-linked profile** -- ephemeral identity linked to the reservation record, no standalone guest profile created

## Decision Outcome

**Chosen Option**: "Temporary profile", because it collects only the minimum PII needed for check-in (name from reservation, contact method for emergencies), provides a real `guest_id` for downstream service calls, and automatically anonymizes after 90 days to comply with data retention policies. The `TEMPORARY` status flag enables future profile merge if the guest returns and registers.

### Confirmation

- svc-guest-profiles schema extended with `status` enum: `ACTIVE`, `TEMPORARY`, `ANONYMIZED`
- `POST /guests` accepts `status: TEMPORARY` with relaxed field validation (email not required)
- Background job anonymizes `TEMPORARY` profiles 90 days after creation: replaces PII with hashed placeholders
- Profile merge endpoint `POST /guests/{guest_id}/merge` supports upgrading `TEMPORARY` to `ACTIVE`

## Consequences

### Positive

- Minimal PII collection at the kiosk -- only name and optional emergency contact
- Automatic 90-day anonymization reduces data retention risk without manual intervention
- Real `guest_id` issued, so all downstream services (check-in, gear, wristband) work unchanged
- Profile merge path supports guest conversion -- walkup visitors who later register keep their adventure history

### Negative

- Adds a new `status` field and `TEMPORARY` lifecycle to svc-guest-profiles, increasing schema and validation complexity
- Anonymization job must be implemented and monitored -- a missed run could leave PII past retention window
- Relaxed validation for `TEMPORARY` profiles means some standard fields may be null, requiring null-safe handling in consumers

### Neutral

- The 90-day retention window aligns with existing NovaTrek data retention policies for non-registered participants
- Anonymized profiles retain the `guest_id` and adventure history linkage, but PII fields are replaced with hashed values

## Pros and Cons of the Options

### Temporary profile

- **Good**, because minimal data collection reduces PII exposure and retention risk
- **Good**, because real `guest_id` enables seamless downstream integration
- **Good**, because automatic anonymization enforces retention policy without manual effort
- **Good**, because merge path supports guest conversion to full account
- **Neutral**, because adds `TEMPORARY` lifecycle management to svc-guest-profiles
- **Bad**, because consumers must handle nullable fields on temporary profiles

### Full profile creation

- **Good**, because all downstream services work without modification -- standard profile shape
- **Bad**, because requires collecting extensive PII at the kiosk (email, phone, address) -- high friction for walkup guests
- **Bad**, because creates permanent profiles for one-time visitors, increasing data retention burden
- **Bad**, because no automatic cleanup -- profiles persist indefinitely unless manually deleted

### Reservation-linked profile

- **Good**, because no additional PII stored beyond what is already in the reservation
- **Bad**, because no `guest_id` issued -- downstream services (wristband, gear) that require a guest identity cannot function
- **Bad**, because breaks the architectural constraint that guest identity flows through svc-guest-profiles
- **Bad**, because creates a shadow identity pattern that duplicates guest data in svc-reservations

## More Information

- Origin: NTK-10003 Solution Design (unregistered guest self-service check-in)
- Services: svc-guest-profiles (owner), svc-check-in (consumer)
- Related: [ADR-007 Four-Field Identity Verification](ADR-007-four-field-identity-verification.md), [ADR-009 Session-Scoped Kiosk Access](ADR-009-session-scoped-kiosk-access.md)
- Constraint: Guest identity resolution MUST flow through svc-guest-profiles (bounded context rule)
