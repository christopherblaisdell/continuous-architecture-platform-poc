# NTK-10003 - Implementation Guidance

## Deployment Order

Services MUST be deployed in this order to avoid runtime errors:

1. **svc-reservations** -- New composite search endpoint and index
2. **svc-guest-profiles** -- Temporary profile endpoint and profile_type field
3. **svc-safety-compliance** -- Extended waiver lookup with reservation_id parameter
4. **API Gateway** -- Rate limiting rules for the new endpoint
5. **svc-check-in** -- Orchestrator endpoint (depends on all upstream services)
6. **Kiosk UI** -- New check-in flow (deployed after svc-check-in is confirmed healthy)

## Feature Flag

`KIOSK_UNREGISTERED_CHECKIN_ENABLED` -- boolean, scoped per base camp location, default `false`.

Enable per the phased rollout plan:
- Phase 1 (March 1): Cascade Ridge only
- Phase 2 (March 8): Thunder Peak, Glacier Basin
- Phase 3 (March 15): All base camps

## Rate Limiting Configuration

| Parameter | Value |
|-----------|-------|
| Max attempts per window | 5 |
| Window duration | 15 minutes |
| Scope | Per kiosk device ID |
| Artificial delay on failure | 2 seconds |
| Implementation layers | API Gateway AND svc-check-in application |

## Response Time Budget

| Step | Service | Budget | Notes |
|------|---------|--------|-------|
| Reservation lookup | svc-reservations | 2 seconds | Composite index query |
| Guest profile | svc-guest-profiles | 1 second | Find-or-create |
| Safety + gear (parallel) | svc-safety-compliance + svc-gear-inventory | 3 seconds | Executed concurrently |
| Session creation | JWT + Redis | 1 second | Local computation + Redis write |
| Buffer | -- | 1 second | Network overhead + processing |
| **Total** | | **8 seconds** | Kiosk timeout is 10 seconds |

## Circuit Breaker Configuration (Partner Fallback)

| Parameter | Value |
|-----------|-------|
| Timeout | 30 seconds |
| Error rate threshold | 50% |
| Recovery window | 60 seconds |
| Fallback behavior | Return 404 with service desk messaging |

## JWT Session Token Claims

```json
{
  "sub": "<guest_profile_id>",
  "reservation_id": "<reservation_id>",
  "kiosk_device_id": "<kiosk_device_id>",
  "iat": "<issued_at_timestamp>",
  "exp": "<issued_at + 30 minutes>",
  "scope": "kiosk_checkin"
}
```

## Security Implementation Checklist

- [ ] Verification fields in POST body only (never URL params)
- [ ] PII masked in logs (last 3 characters of last_name only)
- [ ] Rate limiting at API gateway level
- [ ] Rate limiting at svc-check-in application level
- [ ] 2-second artificial delay on failed lookups
- [ ] JWT scoped to kiosk device ID
- [ ] One active session per kiosk (Redis key: `kiosk_session:{device_id}`)
- [ ] All lookup attempts logged for security audit (timestamp, kiosk_id, masked input)
- [ ] Confirmation code normalized to uppercase before query

## Testing Requirements

### Unit Tests
- Orchestration logic with all downstream services mocked
- Input validation: missing fields, invalid date, out-of-range participant count
- Rate limit counter increment and reset behavior
- JWT token generation with correct claims and expiry

### Integration Tests
- svc-check-in -> svc-reservations: valid 4-field lookup, no-match lookup
- svc-check-in -> svc-guest-profiles: temporary profile creation and deduplication
- svc-check-in -> svc-safety-compliance: waiver status by reservation ID
- Partner fallback: successful partner verification, partner timeout, circuit breaker open

### Performance Tests
- 100 concurrent lookup requests with p95 under 5 seconds
- Rate limit enforcement under concurrent load

### Security Tests
- PII masking verification in all log outputs
- Rate limit bypass attempt validation
- Session token scope enforcement (cross-reservation isolation)
