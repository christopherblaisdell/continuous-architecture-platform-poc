# NTK-10002: Implementation Guidance

## 1. Classification Configuration (application.yml)

Add the classification mapping to the `svc-check-in` configuration in Spring Cloud Config:

```yaml
novatrek:
  checkin:
    use-category-classification: true  # Feature flag
    default-pattern: 3                 # Fallback for unknown categories (ADR-NTK10002-002)
    cache-ttl-seconds: 300             # 5-minute cache TTL
    classification:
      DAY_HIKE: 1
      OVERNIGHT_HIKE: 2
      ALPINE_HIKE: 3
      SPORT_CLIMBING: 2
      TRAD_CLIMBING: 3
      BOULDERING: 1
      FLATWATER_KAYAK: 2
      WHITEWATER_KAYAK: 3
      SEA_KAYAK: 2
      CLASS_III_RAFTING: 2
      CLASS_IV_RAFTING: 3
      FRONTCOUNTRY_CAMPING: 2
      BACKCOUNTRY_CAMPING: 3
      CROSS_COUNTRY_MTB: 2
      DOWNHILL_MTB: 3
      SLOT_CANYON: 2
      TECHNICAL_CANYON: 3
      BEGINNER_SNOWSHOE: 1
      BACKCOUNTRY_SNOWSHOE: 2
      RESORT_SKIING: 1
      BACKCOUNTRY_SKIING: 3
      BIRDING_SAFARI: 1
      WILDLIFE_PHOTO_SAFARI: 1
      NIGHT_SAFARI: 2
      GUIDED_NATURE_WALK: 1
    booking-source-overrides:
      PARTNER_API: 1
      WALK_IN: 3
```

## 2. ClassificationService Implementation

Create `ClassificationService.java` to replace the existing `AdventureCategoryClassifier.java`:

```java
@Service
public class ClassificationService {

    @Value("${novatrek.checkin.default-pattern:3}")
    private int defaultPattern;

    private final Map<String, Integer> classificationMap;
    private final Map<String, Integer> bookingSourceOverrides;

    public ClassificationService(
            @Value("#{${novatrek.checkin.classification}}") Map<String, Integer> classificationMap,
            @Value("#{${novatrek.checkin.booking-source-overrides}}") Map<String, Integer> bookingSourceOverrides) {
        this.classificationMap = new ConcurrentHashMap<>(classificationMap);
        this.bookingSourceOverrides = new ConcurrentHashMap<>(bookingSourceOverrides);
    }

    @Cacheable(value = "checkinPattern", key = "#bookingSource + '-' + #adventureCategory")
    public int determinePattern(String bookingSource, String adventureCategory) {
        // 1. Check booking source override first
        if (bookingSource != null && bookingSourceOverrides.containsKey(bookingSource)) {
            return bookingSourceOverrides.get(bookingSource);
        }
        // 2. Look up category classification
        if (adventureCategory != null && classificationMap.containsKey(adventureCategory)) {
            return classificationMap.get(adventureCategory);
        }
        // 3. Fallback to default (Pattern 3 - Full Service)
        return defaultPattern;
    }
}
```

CRITICAL: The existing `AdventureCategoryClassifier.java` must be retired. It has two problems:
1. Uses hardcoded categories that do not match the 25 approved categories
2. Defaults to Pattern 1 (Basic) for unknowns -- this is an unsafe default that violates ADR-NTK10002-002

## 3. Caching Configuration

Use Spring `@Cacheable` on the `determinePattern` method. Configure the cache in `CacheConfig.java`:

- Cache name: `checkinPattern`
- TTL: Read from `novatrek.checkin.cache-ttl-seconds` (default 300 = 5 minutes)
- Eviction: Time-based expiry. Also evicted on `/actuator/refresh` events via a `@CacheEvict` listener.

## 4. Order of Operations in Check-in Flow

The modified check-in flow in `CheckInController` should follow this sequence:

1. Receive `POST /check-ins` with `reservation_id`
2. Call `svc-reservations` to get reservation details (includes `booking_source` and `adventure_category`)
3. Check feature flag `novatrek.checkin.use-category-classification`
   - If disabled: use legacy `activity_type` classification
   - If enabled: call `classificationService.determinePattern(bookingSource, adventureCategory)`
4. Use the returned pattern to select the appropriate check-in flow
5. Include `determined_pattern` and `pattern_name` in the response body

## 5. API Response Enhancement

Add two new fields to the `CheckIn` response schema in the Swagger spec:

```yaml
determined_pattern:
  type: integer
  enum: [1, 2, 3]
  description: Check-in UI pattern determined by the classification system
  example: 2
pattern_name:
  type: string
  enum: ["Basic", "Gear Required", "Full Service"]
  description: Human-readable name of the determined check-in pattern
  example: "Gear Required"
```

## 6. svc-trip-catalog Schema Extension

Add `adventure_category` to the Trip, TripSummary, TripCreateRequest, and TripUpdateRequest schemas. The field is a nullable string enum with 25 values. See the impact.2 document for the full field specification and data migration guidance.

## 7. Testing Guidance

### Unit Tests for ClassificationService

- Test each of the 25 categories returns the correct pattern
- Test PARTNER_API booking source returns Pattern 1 regardless of category
- Test WALK_IN booking source returns Pattern 3 regardless of category
- Test null `adventure_category` returns Pattern 3 (default)
- Test empty string `adventure_category` returns Pattern 3
- Test unrecognized category value returns Pattern 3
- Test that booking source override takes precedence (e.g., PARTNER_API + BACKCOUNTRY_CAMPING = Pattern 1)

### Integration Tests

- End-to-end check-in for a DAY_HIKE reservation: verify only confirmation screen
- End-to-end check-in for a WHITEWATER_KAYAK reservation: verify gear + safety screens
- End-to-end check-in for a BACKCOUNTRY_CAMPING reservation: verify all 6 screens
- Verify that toggling the feature flag reverts to legacy `activity_type` behavior
- Verify that config refresh updates the classification without service restart

## 8. Feature Flag Rollout

1. Deploy with `novatrek.checkin.use-category-classification=false` (feature off)
2. Verify classification config loads correctly via metrics and logs
3. Enable the feature flag in a single region for canary testing
4. Monitor `checkin.pattern.determined` metric distribution for expected ratios
5. Monitor `checkin.classification.fallback.count` for unexpected unmapped categories
6. Roll out to all regions after validation
