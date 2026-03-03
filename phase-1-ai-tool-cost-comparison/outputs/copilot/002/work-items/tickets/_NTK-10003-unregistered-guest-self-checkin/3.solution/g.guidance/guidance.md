# NTK-10003 - Implementation Guidance

## Endpoint Implementation

### Controller Layer (svc-check-in)

The existing `CheckInController.java` has a stub `POST /lookup-reservation` that accepts `Map<String,String>` with only `confirmationCode` and `lastName`. This stub must be replaced with a properly typed implementation. Create a dedicated `ReservationLookupController` to maintain separation of concerns from the existing check-in CRUD operations in `CheckInController`.

The existing controller pattern uses `@RestController`, `@RequestMapping`, and returns `ResponseEntity<>`. Follow this same pattern.

```
ReservationLookupController
  -> ReservationLookupService (orchestration logic)
    -> ReservationClient (calls svc-reservations POST /reservations/search)
    -> GuestProfileClient (calls svc-guest-profiles POST /guest-profiles/temporary)
    -> SafetyComplianceClient (calls svc-safety-compliance GET /waivers)
    -> GearInventoryClient (calls svc-gear-inventory GET /gear-assignments)
    -> PartnerIntegrationClient (calls svc-partner-integrations POST /bookings/verify)
```

Remove the stub from `CheckInController.java` after the new controller is in place.

### Request DTO

Replace the raw `Map<String,String>` with a typed DTO:

```java
public class ReservationLookupRequest {
    @NotBlank
    @Size(max = 100)
    private String lastName;

    @NotBlank
    @Size(min = 6, max = 16)
    @Pattern(regexp = "^[A-Za-z0-9\\-]+$")
    private String confirmationCode;

    @NotNull
    private LocalDate adventureDate;

    @NotNull
    @Min(1)
    @Max(20)
    private Integer participantCount;
}
```

### Input Normalization

Apply normalization in the service layer before calling downstream services:

- `confirmation_code`: Convert to uppercase, trim whitespace, strip hyphens (accept both `EM-A1B2C3D4` and `EMA1B2C3D4`)
- `last_name`: Trim whitespace, preserve case for matching (svc-reservations performs case-insensitive comparison via `LOWER()` index)
- `adventure_date`: Reject dates more than 1 day in the future or more than 0 days in the past (check-in is same-day only)
- `participant_count`: Validate positive integer, cap at 20 (maximum group size)

### Parallel Downstream Calls

After the reservation is found and the temporary guest profile is created (sequential, since profile creation depends on reservation data), use `CompletableFuture.allOf()` to parallelize the remaining calls:

```java
CompletableFuture<WaiverStatus> waiverFuture = CompletableFuture
    .supplyAsync(() -> safetyComplianceClient.getWaivers(guestId, reservationId), executor)
    .orTimeout(3, TimeUnit.SECONDS)
    .exceptionally(ex -> { log.warn("WAIVER_CHECK_FAILED", ex); return null; });

CompletableFuture<GearAssignment> gearFuture = CompletableFuture
    .supplyAsync(() -> gearInventoryClient.getAssignments(reservationId), executor)
    .orTimeout(3, TimeUnit.SECONDS)
    .exceptionally(ex -> { log.warn("GEAR_CHECK_FAILED", ex); return null; });

CompletableFuture.allOf(waiverFuture, gearFuture).join();
```

Use a dedicated `ThreadPoolTaskExecutor` (named `kioskLookupExecutor`, 10 threads) to isolate kiosk traffic from staff-facing API calls.

### Per-Service Timeouts

| Service | Timeout | Justification |
|---------|---------|---------------|
| svc-reservations | 2 seconds | Critical path, should be fast with composite index |
| svc-guest-profiles | 1 second | Simple create/lookup, low latency expected |
| svc-safety-compliance | 3 seconds | May aggregate multiple waiver types per reservation |
| svc-gear-inventory | 3 seconds | Inventory check may involve availability calculation |
| svc-partner-integrations | 30 seconds | External partner API latency is unpredictable; circuit breaker protects against hangs |

## Error Handling Strategy

### Downstream Service Failures

| Service | Failure Behavior | User Message |
|---------|-----------------|--------------|
| svc-reservations | Return 404 (cannot proceed without reservation) | "We couldn't find a matching reservation. Please check your details or visit the service desk." |
| svc-guest-profiles | Return 503 (check-in cannot proceed without profile) | "We're experiencing a temporary issue. Please try again or visit the service desk." |
| svc-safety-compliance | Proceed with `waiver_complete: null` and log warning | (No user-facing error; waiver step shown as "pending") |
| svc-gear-inventory | Proceed with `gear_assigned: null` and log warning | (No user-facing error; gear step shown as "confirm at pickup") |
| svc-partner-integrations | Return 404 with staff desk messaging (circuit breaker) | "We couldn't verify your partner booking. Please visit the service desk for priority assistance." |

### Error Response Consistency

All error responses must use the standard NovaTrek error envelope:

```json
{
  "error": "RESERVATION_NOT_FOUND",
  "message": "We couldn't find a matching reservation. Please check your details or visit the service desk.",
  "trace_id": "correlation-id-for-debugging"
}
```

Error codes: `RESERVATION_NOT_FOUND`, `VALIDATION_ERROR`, `RATE_LIMIT_EXCEEDED`, `SERVICE_UNAVAILABLE`, `PARTNER_VERIFICATION_FAILED`.

Do not expose internal service names, stack traces, or downstream error details in client-facing responses.

## Logging and Monitoring

### Structured Log Events

Log the following events with correlation ID (`X-Trace-Id` header). Use the existing SLF4J + structured logging pattern from the codebase.

| Event | Log Level | Fields |
|-------|-----------|--------|
| `LOOKUP_ATTEMPT` | INFO | kiosk_device_id, confirmation_code (last 4 chars only), adventure_date, timestamp |
| `LOOKUP_SUCCESS` | INFO | kiosk_device_id, reservation_id, guest_profile_type, session_expiry |
| `LOOKUP_FAILURE` | WARN | kiosk_device_id, failure_reason (NOT_FOUND, VALIDATION_ERROR), attempt_count |
| `PARTNER_FALLBACK_TRIGGERED` | INFO | kiosk_device_id, partner_id, confirmation_code (last 4 chars) |
| `PARTNER_FALLBACK_FAILURE` | WARN | kiosk_device_id, partner_id, failure_reason |
| `RATE_LIMIT_TRIGGERED` | WARN | kiosk_device_id, attempt_count, window_reset_time |
| `SESSION_CREATED` | INFO | session_id, kiosk_device_id, reservation_id, expiry_time |
| `SESSION_EXPIRED` | INFO | session_id, kiosk_device_id, check_in_completed (boolean) |
| `TEMP_PROFILE_CREATED` | INFO | guest_profile_id, reservation_id, profile_type |

### PII Masking Rules

- `last_name`: Show only last 3 characters (e.g., `***ith` for "Smith")
- `confirmation_code`: Show only last 4 characters (e.g., `****C3D4`)
- `guest_profile_id`: Full value (not PII)
- `reservation_id`: Full value (not PII)
- `email`: Never logged for temporary profiles (not collected)

### Dashboard Metrics

Create a monitoring dashboard with the following metrics:
- Lookup success rate (target: above 85%)
- Lookup latency p50/p95/p99
- Partner fallback trigger rate
- Rate limit trigger frequency per base camp
- Kiosk session completion rate (started vs completed check-in)
- Temporary profile creation rate (daily)

## Rate Limiting Configuration

### API Gateway Rule

```yaml
rate_limit:
  endpoint: POST /check-ins/lookup-reservation
  key: request.body.kiosk_device_id
  limit: 5
  window: 900  # 15 minutes in seconds
  response_code: 429
  response_headers:
    Retry-After: "{remaining_seconds}"
```

### Application-Level Rate Limiting (Defense in Depth)

Implement a secondary rate limit in svc-check-in using Redis:
- Key: `ratelimit:lookup:{kiosk_device_id}`
- Limit: 5 requests per 15-minute sliding window
- On failed lookup: add 2-second artificial delay before returning response
- On rate limit exceeded: return 429 immediately (no artificial delay)

```java
String key = "ratelimit:lookup:" + request.getKioskDeviceId();
Long attempts = redisTemplate.opsForValue().increment(key);
if (attempts == 1) {
    redisTemplate.expire(key, Duration.ofMinutes(15));
}
if (attempts > 5) {
    throw new RateLimitExceededException(key);
}
```

## Database Migration Guidance (svc-reservations)

### Confirmation Code Column

```sql
ALTER TABLE reservations ADD COLUMN confirmation_code VARCHAR(16);
ALTER TABLE reservations ADD COLUMN adventure_date DATE;
```

### Composite Index

```sql
CREATE INDEX CONCURRENTLY idx_reservation_lookup
  ON reservations (confirmation_code, adventure_date, participant_count, LOWER(last_name));
```

Run during off-peak window (02:00-04:00 UTC). `CREATE INDEX CONCURRENTLY` avoids table locks but requires approximately 2 hours on production data volume. Monitor `pg_stat_progress_create_index` for progress.

## Testing Strategy

### Integration Test Priority

1. Happy path: 4-field lookup matches reservation, temporary profile created, waiver and gear status returned
2. Partner fallback: direct lookup returns 404, partner verification succeeds, reservation synced
3. Rate limiting: 6th attempt within 15-minute window returns 429
4. Graceful degradation: svc-safety-compliance timeout returns partial response with null waiver status
5. Session expiry: session token rejected after 30-minute TTL
6. Input normalization: mixed-case confirmation code, hyphenated code, extra whitespace all resolve correctly
