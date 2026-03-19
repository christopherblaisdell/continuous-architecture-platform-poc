# ADR-007: Four-Field Identity Verification for Unregistered Guests

## Status

Accepted

## Date

2025-01-28

## Context and Problem Statement

Unregistered guests arriving at a self-service kiosk (NTK-10003) need to be matched to their reservation without having a pre-registered account. The system must verify the guest's identity with sufficient confidence to allow check-in while avoiding excessive friction at the kiosk. What verification fields should be required to look up and confirm a reservation?

## Decision Drivers

- Security: verification must prevent one guest from checking in under another guest's reservation
- User experience: guests should be able to complete verification quickly using information they already know
- Operational complexity: the verification approach must work without staff assistance at the kiosk
- Data availability: verification fields must exist in the reservation data returned by svc-reservations

## Considered Options

1. **Four-field verification** -- last name + confirmation code + adventure date + participant count
2. **Confirmation code only** -- single-field lookup using the booking confirmation code
3. **Confirmation code + ID scan** -- confirmation code plus government-issued ID scan at the kiosk

## Decision Outcome

**Chosen Option**: "Four-field verification", because it balances security with usability. The combination of four fields provides sufficient entropy to prevent accidental or intentional reservation mismatches, while all four values are readily available to the guest (printed on their booking confirmation email). No additional hardware (ID scanner) is required at the kiosk.

### Confirmation

- `POST /check-ins/self-service/unregistered` request body requires: `last_name`, `confirmation_code`, `adventure_date`, `participant_count`
- svc-reservations lookup validates all four fields; returns 404 if any field does not match
- Failed verification attempts are logged with rate limiting to prevent enumeration

## Consequences

### Positive

- All four verification fields are printed on the standard booking confirmation email -- no guest needs to memorize extra credentials
- No additional kiosk hardware required (unlike ID scanning)
- Four-field combination provides strong collision resistance -- guessing all four correctly is impractical
- Rate limiting on failed attempts prevents brute-force enumeration of confirmation codes

### Negative

- Guests who forget their confirmation code or participant count cannot self-serve -- they must go to a staffed desk
- Requires svc-reservations to support a multi-field lookup endpoint (new API contract addition)
- Does not provide government-level identity assurance for high-risk adventure categories

### Neutral

- For Pattern 3 (Full Service) adventures, staff-assisted check-in may still perform additional identity verification at their discretion

## Pros and Cons of the Options

### Four-field verification

- **Good**, because strong collision resistance without extra hardware
- **Good**, because all fields are available on the booking confirmation
- **Good**, because no staff assistance needed
- **Neutral**, because requires a new lookup endpoint on svc-reservations
- **Bad**, because guests without their confirmation details must fall back to staffed check-in

### Confirmation code only

- **Good**, because minimal friction -- single field entry
- **Bad**, because confirmation codes alone may not have sufficient entropy to prevent accidental matches
- **Bad**, because a forwarded confirmation email gives any recipient full check-in access

### Confirmation code + ID scan

- **Good**, because strongest identity assurance -- government-issued ID
- **Bad**, because requires ID scanning hardware at every kiosk
- **Bad**, because international guests may have IDs in formats the scanner cannot parse
- **Bad**, because adds significant operational complexity and hardware maintenance cost

## More Information

- Origin: NTK-10003 Solution Design (unregistered guest self-service check-in)
- Services: svc-check-in (consumer), svc-reservations (lookup provider)
- Related: [ADR-006 Orchestrator Pattern](ADR-006-orchestrator-pattern-checkin.md), [ADR-008 Temporary Guest Profile](ADR-008-temporary-guest-profile.md)
- Note: svc-reservations spec currently lacks a `confirmation_code` field -- this must be added as part of the implementation
