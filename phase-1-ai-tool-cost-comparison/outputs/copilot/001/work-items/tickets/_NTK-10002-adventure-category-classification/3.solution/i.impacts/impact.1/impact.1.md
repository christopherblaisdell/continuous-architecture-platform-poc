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

### Replacement of AdventureCategoryClassifier

The existing `AdventureCategoryClassifier.java` contains hardcoded category sets with categories that do not match the approved 25-category classification table (e.g., `SCENIC_OVERLOOK`, `BIRD_WATCHING`, `FISHING_BASIC`). This class also defaults unknown categories to Pattern 1 (Basic), which poses a safety risk. The new `ClassificationService` replaces this component entirely, reading from Spring Cloud Config YAML and defaulting to Pattern 3 (Full Service).

### Modified Check-in Flow

The existing `CheckInController.createCheckIn()` method currently reads `activity_type` from the reservation and uses the hardcoded two-tier mapping. This will be modified to:

1. Retrieve `booking_source` and `adventure_category` from the reservation (via `svc-reservations`)
2. Call `ClassificationService.determinePattern()` to get the correct pattern
3. Route to the appropriate check-in flow based on the determined pattern
4. When the feature flag is disabled, fall back to the existing `activity_type` logic

### New Configuration File

A new section in `application.yml` defines the classification mapping, booking source overrides, default fallback pattern, and cache TTL. See the guidance document for the full YAML structure.

### API Response Change

The `POST /check-ins` response will include two new optional fields:

```json
{
  "check_in_id": "chk-12345",
  "reservation_id": "res-67890",
  "status": "INITIATED",
  "determined_pattern": 2,
  "pattern_name": "Gear Required",
  "screens_presented": ["confirmation", "gear_pickup", "safety_briefing"]
}
```

The `determined_pattern` and `pattern_name` fields are additive and do not break existing consumers.

## Decision Flow

See the classification flow diagram in `classification-flow.puml` for a visual representation of the pattern determination logic.

## Metrics

New metrics to add:

- `checkin.pattern.determined` (counter, tagged by pattern) - tracks pattern distribution
- `checkin.classification.fallback.count` (counter) - tracks how often the fallback to Pattern 3 is triggered
- `checkin.classification.override.count` (counter, tagged by booking source) - tracks override usage
