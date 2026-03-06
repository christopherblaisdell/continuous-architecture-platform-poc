# NTK-10003 - Implementation Guidance

## Endpoint Implementation

### Controller Layer (svc-check-in)

The new `POST /check-ins/lookup-reservation` endpoint should be implemented in a dedicated `ReservationLookupController` rather than adding to the existing `CheckInController`. This maintains separation of concerns between the registered check-in flow and the unregistered guest lookup flow.

The existing stub in `CheckInController.java` (lines 34-41) should be removed once the new controller is in place.

```
ReservationLookupController
  -> ReservationLookupService (orchestration logic)
    -> ReservationSearchClient (calls svc-reservations)
    -> TemporaryGuestProfileClient (calls svc-guest-profiles)
    -> WaiverStatusClient (calls svc-safety-compliance)
    -> GearAssignmentClient (calls svc-gear-inventory)
    -> PartnerVerificationClient (calls svc-partner-integrations)
```

### Input Normalization

- `confirmation_code`: Convert to uppercase, trim whitespace, strip hyphens (accept both `EM-A1B2C3D4` and `EMA1B2C3D4`)
- `last_name`: Trim whitespace, preserve case for submission (svc-reservations should perform case-insensitive comparison using `LOWER()` function index)
- `adventure_date`: Validate ISO 8601 format, reject dates more than 1 day in the future or in the past
- `kiosk_device_id`: Validate UUID format

### Request DTO

Replace the raw `Map<String, String>` in the current stub with a typed request DTO:

```java
public class ReservationLookupRequest {
    @NotBlank @Size(max = 100)
    private String lastName;

    @NotBlank @Pattern(regexp = "^[A-Za-z0-9-]{6,12}$")
    private String confirmationCode;

    @NotNull
    private LocalDate adventureDate;

    @NotNull @Min(1) @Max(20)
    private Integer participantCount;

    @NotNull
    private UUID kioskDeviceId;
}
```

### Parallel Downstream Calls

Use `CompletableFuture.allOf()` to parallelize the svc-safety-compliance and svc-gear-inventory calls in Step 4. These calls are independent and should not block each other.

Set individual call timeouts:

| Service | Timeout | Failure Behavior |
|---------|---------|-----------------|
| svc-reservations | 2 seconds | Return 404 (cannot proceed without reservation) |
| svc-guest-profiles | 1 second | Return 503 (cannot proceed without profile) |
| svc-safety-compliance | 3 seconds | Proceed with `waiver_complete: null`, log warning |
| svc-gear-inventory | 3 seconds | Proceed with `gear_assigned: null`, log warning |
| svc-partner-integrations | 30 seconds | Return 404 with staff desk messaging (circuit breaker protects against cascading failure) |

### Circuit Breaker for Partner Integration

Configure circuit breaker on the partner integration client:

- Timeout: 30 seconds (partner APIs are external and slower)
- Error threshold: 50% error rate opens the circuit
- Recovery window: 60 seconds before half-open state
- When circuit is open: skip partner fallback immediately, return 404 with staff desk messaging

## Error Handling Strategy

### Downstream Service Failures

| Service | Failure Behavior |
|---------|-----------------|
| svc-reservations | Return 404 (cannot proceed without reservation) |
| svc-guest-profiles | Return 503 (check-in cannot proceed without profile) |
| svc-safety-compliance | Proceed with `waiver_complete: null` and log warning; guest can complete waiver manually on kiosk |
| svc-gear-inventory | Proceed with `gear_assigned: null` and log warning; gear can be confirmed at pickup counter |
| svc-partner-integrations | Return 404 with staff desk messaging (circuit breaker protects against cascading failure) |

### Error Response Consistency

All error responses must use the standard NovaTrek error envelope:

```json
{
  "error": "ERROR_CODE",
  "message": "User-friendly message",
  "trace_id": "correlation-id-for-debugging"
}
```

Do not expose internal service names, stack traces, or downstream error details in client-facing responses.

## Logging and Monitoring

### Structured Log Events

Log the following events with correlation ID (`X-Trace-Id` header):

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

### PII Masking Rules

- `last_name`: Show only last 3 characters (e.g., `***ith` for "Smith")
- `confirmation_code`: Show only last 4 characters (e.g., `****C3D4`)
- `guest_profile_id`: Full value (not PII)
- `reservation_id`: Full value (not PII)

### Dashboard Metrics

Create a monitoring dashboard with the following metrics:

- Lookup success rate (target: above 85%)
- Lookup latency p50/p95/p99
- Partner fallback trigger rate
- Rate limit trigger frequency per base camp
- Kiosk session completion rate (started vs completed check-in)
- Temporary profile creation rate

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

## svc-guest-profiles Temporary Profile Implementation

### New Service Method

Create a `createTemporaryProfile()` method in `GuestService` that bypasses the existing email deduplication:

- Accept `last_name` and `reservation_id` only
- Deduplicate by `reservation_id` (return existing TEMPORARY profile if one exists for this reservation)
- Set `profile_type = TEMPORARY`
- Do NOT set email, first_name, date_of_birth, or emergency_contact

### Anonymization Job

Implement a scheduled job (Spring `@Scheduled` or equivalent):

- Run daily at 02:00 UTC
- Query: `SELECT * FROM guest_profiles WHERE profile_type = 'TEMPORARY' AND created_at < NOW() - INTERVAL '90 days' AND profile_type != 'MERGED'`
- Action: Replace `last_name` with SHA-256 hash, clear any other PII fields
- Retain anonymized record for aggregate analytics
- Log job execution results (count anonymized, count skipped, errors)

## svc-reservations Composite Search

### Index Creation

```sql
CREATE INDEX CONCURRENTLY idx_reservations_verification_lookup
ON reservations (
  confirmation_code,
  adventure_date,
  participant_count,
  LOWER(last_name)
);
```

Use `CONCURRENTLY` to avoid table locks during creation. Run during off-peak hours. Monitor index creation progress in `pg_stat_progress_create_index`.

### Confirmation Code Normalization

Store all confirmation codes in uppercase. On query, normalize the input to uppercase before matching. Strip hyphens from both stored and queried values for consistent matching.
