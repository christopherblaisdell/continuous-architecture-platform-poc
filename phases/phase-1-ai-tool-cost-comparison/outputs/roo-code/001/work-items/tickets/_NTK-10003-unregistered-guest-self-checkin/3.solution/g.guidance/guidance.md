# NTK-10003 - Implementation Guidance

## Endpoint Implementation

### Controller Layer (svc-check-in)

Create a dedicated `ReservationLookupController` for the new endpoint rather than extending the existing `CheckInController`. This maintains separation of concerns between registered and unregistered guest flows.

```
ReservationLookupController
  -> ReservationLookupService (orchestration logic)
    -> ReservationClient (calls svc-reservations)
    -> GuestProfileClient (calls svc-guest-profiles)
    -> SafetyComplianceClient (calls svc-safety-compliance)
    -> GearInventoryClient (calls svc-gear-inventory)
    -> PartnerIntegrationClient (calls svc-partner-integrations)
```

The existing `CheckInController.lookupReservation()` method (lines 35-43) should be deprecated. It uses a simple `Map<String, String>` with only two fields and does not meet the four-field verification or security requirements.

### Input Normalization

- `confirmation_code`: Convert to uppercase, trim whitespace, strip hyphens (accept both `EM-A1B2C3D4` and `EMA1B2C3D4`)
- `last_name`: Trim whitespace, preserve case for matching (svc-reservations performs case-insensitive comparison)
- `adventure_date`: Validate ISO 8601 format, reject dates more than 1 day in the future or in the past

### Parallel Downstream Calls

Use `CompletableFuture.allOf()` to parallelize the svc-safety-compliance and svc-gear-inventory calls in Step 4. These calls are independent and should not block each other.

Set individual call timeouts:

| Service | Timeout | Reason |
|---------|---------|--------|
| svc-reservations | 2 seconds | Primary lookup, must be fast |
| svc-guest-profiles | 1 second | Simple profile lookup/creation |
| svc-safety-compliance | 3 seconds | Waiver queries may involve document lookup |
| svc-gear-inventory | 3 seconds | Gear assignment queries |
| svc-partner-integrations | 30 seconds | External partner APIs have higher latency |

## Error Handling Strategy

### Downstream Service Failures

| Service | Failure Behavior |
|---------|-----------------|
| svc-reservations | Return 404 (cannot proceed without reservation) |
| svc-guest-profiles | Return 503 (check-in cannot proceed without profile) |
| svc-safety-compliance | Proceed with `waiver_complete: null` and log warning; guest completes waiver on kiosk |
| svc-gear-inventory | Proceed with `gear_assigned: null` and log warning; gear confirmed at pickup |
| svc-partner-integrations | Return 404 with staff desk messaging (circuit breaker protects against cascading failure) |

### Error Response Consistency

All error responses use the standard NovaTrek error envelope. Never expose internal service names, stack traces, or downstream error details in client-facing responses.

## Logging and Monitoring

### Structured Log Events

| Event | Log Level | Fields |
|-------|-----------|--------|
| `LOOKUP_ATTEMPT` | INFO | kiosk_device_id, confirmation_code (last 4 chars only), adventure_date |
| `LOOKUP_SUCCESS` | INFO | kiosk_device_id, reservation_id, guest_profile_type, session_expiry |
| `LOOKUP_FAILURE` | WARN | kiosk_device_id, failure_reason (NOT_FOUND, VALIDATION_ERROR), attempt_count |
| `PARTNER_FALLBACK_TRIGGERED` | INFO | kiosk_device_id, partner_id |
| `PARTNER_FALLBACK_FAILURE` | WARN | kiosk_device_id, partner_id, failure_reason |
| `RATE_LIMIT_TRIGGERED` | WARN | kiosk_device_id, attempt_count, window_reset_time |
| `SESSION_CREATED` | INFO | session_id, kiosk_device_id, reservation_id, expiry_time |

### PII Masking Rules

- `last_name`: Show only last 3 characters (e.g., `***ith` for "Smith")
- `confirmation_code`: Show only last 4 characters (e.g., `****C3D4`)
- `guest_profile_id` and `reservation_id`: Full value (not PII)

### Dashboard Metrics

- Lookup success rate (target: above 85%)
- Lookup latency p50/p95/p99
- Partner fallback trigger rate
- Rate limit trigger frequency per base camp
- Kiosk session completion rate

## Rate Limiting Configuration

### API Gateway Rule

```yaml
rate_limit:
  endpoint: POST /check-ins/self-service/unregistered
  key: request.body.kiosk_device_id
  limit: 5
  window: 900  # 15 minutes
  response_code: 429
```

### Application-Level Rate Limiting (Defense in Depth)

Redis-backed secondary rate limit in svc-check-in:
- Key: `ratelimit:lookup:{kiosk_device_id}`
- Limit: 5 requests per 15-minute sliding window
- On failed lookup: add 2-second artificial delay before returning response
- On rate limit exceeded: return 429 immediately (no artificial delay)
