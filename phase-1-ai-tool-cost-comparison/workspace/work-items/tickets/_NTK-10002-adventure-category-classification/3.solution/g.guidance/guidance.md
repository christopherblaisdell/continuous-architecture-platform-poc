# NTK-10002: Implementation Guidance

## 1. Classification Configuration (application.yml)

Add the classification mapping to the `svc-check-in` configuration in Spring Cloud Config:

```yaml
novatrek:
  checkin:
    use-category-classification: true  # Feature flag
    default-pattern: 3                 # Fallback for unknown categories
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

Create `ClassificationService.java` in `svc-check-in`:

```java
@Service
public class ClassificationService {

    @Value("${novatrek.checkin.default-pattern:3}")
    private int defaultPattern;

    private final Map<String, Integer> classificationMap;
    private final Map<String, Integer> bookingSourceOverrides;

    // Constructor injection from config properties

    @Cacheable(value = "checkinPattern", key = "#bookingSource + '-' + #adventureCategory")
    public int determinePattern(String bookingSource, String adventureCategory) {
        // 1. Check booking source override first
        if (bookingSourceOverrides.containsKey(bookingSource)) {
            return bookingSourceOverrides.get(bookingSource);
        }
        // 2. Look up category classification
        if (adventureCategory != null && classificationMap.containsKey(adventureCategory)) {
            return classificationMap.get(adventureCategory);
        }
        // 3. Fallback to default (Pattern 3)
        return defaultPattern;
    }
}
```

## 3. Caching

Use Spring `@Cacheable` on the `determinePattern` method. Configure the cache in `CacheConfig.java`:

- Cache name: `checkinPattern`
- TTL: Read from `novatrek.checkin.cache-ttl-seconds` (default 300)
- Eviction: Time-based expiry. Also evicted on `/actuator/refresh` events via a `@CacheEvict` listener.

## 4. Order of Operations in Check-in Flow

The modified check-in flow in `CheckInController` should follow this sequence:

1. Receive `POST /check-ins` with `reservation_id`
2. Call `svc-reservations` to get reservation details (includes `booking_source` and `adventure_category`)
3. Call `classificationService.determinePattern(bookingSource, adventureCategory)`
4. Use the returned pattern to select the appropriate check-in flow
5. Include `determined_pattern` in the response body

## 5. Updating svc-check-in API Response

Add the `determined_pattern` field to the `CheckInResponse` DTO:

```java
public class CheckInResponse {
    // existing fields...
    private int determinedPattern;  // 1, 2, or 3
    private String patternName;     // "Basic", "Gear Required", "Full Service"
}
```

## 6. Testing Guidance

### Unit Tests for ClassificationService

- Test each of the 25 categories returns the correct pattern.
- Test PARTNER_API booking source returns Pattern 1 regardless of category.
- Test WALK_IN booking source returns Pattern 3 regardless of category.
- Test null `adventure_category` returns Pattern 3 (default).
- Test empty string `adventure_category` returns Pattern 3.
- Test unrecognized category value returns Pattern 3.
- Test that booking source override takes precedence over category (e.g., PARTNER_API + BACKCOUNTRY_CAMPING = Pattern 1, not Pattern 3).

### Integration Tests

- End-to-end check-in for a DAY_HIKE reservation: verify only confirmation screen is returned.
- End-to-end check-in for a WHITEWATER_KAYAK reservation: verify gear + safety screens included.
- End-to-end check-in for a BACKCOUNTRY_CAMPING reservation: verify all 6 screens included.
- Verify that toggling the feature flag reverts to legacy `activity_type` behavior.
- Verify that config refresh updates the classification without service restart.
