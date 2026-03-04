# NTK-10002: Impact 1 - svc-check-in (PRIMARY)

## Service

**svc-check-in** - The primary check-in service responsible for managing guest check-in flows at kiosks and mobile devices.

## Impact Level

PRIMARY - This service receives the majority of changes for this ticket.

## Changes Required

### New Component: ClassificationService

A new service class `ClassificationService` replaces the existing hardcoded `AdventureCategoryClassifier`. This component is responsible for:

- Loading the adventure category classification mapping from Spring Cloud Config YAML
- Evaluating booking source override rules (PARTNER_API -> Pattern 1, WALK_IN -> Pattern 3)
- Determining the correct check-in UI pattern (1, 2, or 3) for a given reservation
- Defaulting to Pattern 3 (Full Service) for null, empty, or unrecognized categories
- Caching classification results using Spring `@Cacheable` with configurable TTL

### Retire AdventureCategoryClassifier

The existing `AdventureCategoryClassifier.java` with its hardcoded `Set` constants and unsafe Pattern 1 default must be replaced. The categories in the current code (`SCENIC_OVERLOOK`, `BIRD_WATCHING`, `FISHING_BASIC`, `ZIP_LINE`, etc.) do not match the 25 approved adventure categories from the ticket requirements.

### Modified Check-in Flow

The existing `CheckInController.createCheckIn()` method currently reads `activity_type` from the reservation and uses a hardcoded two-tier mapping. This will be modified to:

1. Retrieve `booking_source` and `adventure_category` from the reservation (via `svc-reservations`)
2. Call `ClassificationService.determinePattern()` to get the correct pattern
3. Route to the appropriate check-in flow based on the determined pattern
4. When the feature flag `novatrek.checkin.use-category-classification` is disabled, fall back to the existing `activity_type` logic

### New Configuration File

A new section in `application.yml` defines the classification mapping, booking source overrides, default fallback pattern, and cache TTL. See the guidance document for the full YAML structure.

### API Response Change

The `POST /check-ins` response will include two new additive fields:

```json
{
  "check_in_id": "chk-12345",
  "reservation_id": "res-67890",
  "status": "COMPLETED",
  "determined_pattern": 2,
  "pattern_name": "Gear Required"
}
```

The `determined_pattern` and `pattern_name` fields are additive and do not break existing consumers using tolerant reader patterns.

### Swagger Specification Update

The `CheckIn` schema in `svc-check-in.yaml` must be updated with the two new response fields. The `CheckInCreate` schema is unchanged.

## Metrics

New metrics to add:

| Metric | Type | Tags | Purpose |
|--------|------|------|---------|
| `checkin.pattern.determined` | Counter | pattern (1,2,3) | Track pattern distribution |
| `checkin.classification.fallback.count` | Counter | - | Track how often fallback to Pattern 3 is triggered |
| `checkin.classification.override.count` | Counter | booking_source | Track booking source override usage |
