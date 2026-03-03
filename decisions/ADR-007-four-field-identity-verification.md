# ADR-007: Four-Field Identity Verification

## Status

Accepted

## Date

2026-01-29

## Context and Problem Statement

Unregistered guests at self-service kiosks must be verified against their reservation before gaining kiosk access. The verification mechanism must work reliably across all booking sources (direct, partner, gift card) while providing reasonable security against unauthorized access.

## Decision Drivers

- Partner bookings often have the travel agent's email/phone, not the guest's
- All verification fields must be consistently available across all booking sources
- Security must be sufficient without being burdensome (this is a kiosk, not a bank)
- No dependency on external SMS/email infrastructure

## Considered Options

1. **Email-based verification** — Confirmation code + email address
2. **Phone-based verification** — Confirmation code + phone + SMS OTP
3. **Four-field verification** — Last name + confirmation code + adventure date + participant count

## Decision Outcome

**Chosen Option**: "Four-field verification", because the four selected fields are consistently available across all booking sources and do not depend on external infrastructure.

### Confirmation

- API contract includes all four fields as required in the verification request
- Integration tests verify successful lookup across direct, partner, and gift card booking sources
- Rate limiting and artificial delays protect against brute-force guessing

## Consequences

### Positive

- Reliable across all booking sources — no dependency on guest email/phone accuracy
- No SMS infrastructure dependency (avoids international SMS delivery issues)
- Confirmation code provides primary secret; other fields prevent casual guessing

### Negative

- Lower security assurance than OTP-based verification (mitigated by rate limiting and artificial delays)
- Participant count changes after booking could cause verification failures
- Requires all fields to be accurately maintained across reservation data sources

## More Information

- Origin: [NTK-10003 Solution Design](../phase-1-ai-tool-cost-comparison/workspace/work-items/tickets/_NTK-10003-unregistered-guest-self-checkin/NTK-10003-solution-design.md)
- Services: [svc-check-in](../services/svc-check-in.md), [svc-reservations](../services/svc-reservations.md)
