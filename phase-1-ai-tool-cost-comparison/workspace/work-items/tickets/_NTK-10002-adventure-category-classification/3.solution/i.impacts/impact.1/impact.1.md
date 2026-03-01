# NTK-10002: Impact 1 - svc-check-in (PRIMARY)

## Service

**svc-check-in** - The primary check-in service responsible for managing guest check-in flows at kiosks and mobile devices.

## Impact Level

PRIMARY - This service receives the majority of changes for this ticket.

## Changes Required

### New Component: ClassificationService

A new service class `ClassificationService` will be added to `svc-check-in`. This component is responsible for:

- Loading the adventure category classification mapping from Spring Cloud Config
- Evaluating booking source override rules
- Determining the correct check-in UI pattern (1, 2, or 3) for a given reservation
- Caching classification results for performance

### Modified Check-in Flow

The existing `CheckInController.createCheckIn()` method currently reads `activity_type` from the reservation and uses a hardcoded two-tier mapping. This will be modified to:

1. Retrieve `booking_source` and `adventure_category` from the reservation (via `svc-reservations`)
2. Call `ClassificationService.determinePattern()` to get the correct pattern
3. Route to the appropriate check-in flow based on the determined pattern
4. When the feature flag is disabled, fall back to the existing `activity_type` logic

### New Configuration File

A new section in `application.yml` defines the classification mapping, booking source overrides, default fallback pattern, and cache TTL. See the guidance document for the full YAML structure.

### API Change

The `POST /check-ins` response will include a new field:

```json
{
  "check_in_id": "chk-12345",
  "reservation_id": "res-67890",
  "status": "COMPLETED",
  "determined_pattern": 2,
  "pattern_name": "Gear Required",
  "screens_presented": ["confirmation", "gear_pickup", "safety_briefing"]
}
```

The `determined_pattern` and `pattern_name` fields are additive and do not break existing consumers.

## Decision Flow

See the classification flow diagram in [classification-flow.puml](classification-flow.puml) for a visual representation of the pattern determination logic.

## Metrics

New metrics to add:

- `checkin.pattern.determined` (counter, tagged by pattern) - tracks pattern distribution
- `checkin.classification.fallback.count` (counter) - tracks how often the fallback to Pattern 3 is triggered
- `checkin.classification.override.count` (counter, tagged by booking source) - tracks override usage
