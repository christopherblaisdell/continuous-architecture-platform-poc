# NTK-10002: Impact 2 - svc-trip-catalog (MINOR)

## Service

**svc-trip-catalog** -- The service that manages the catalog of available trips, activities, and trip metadata.

## Impact Level

MINOR -- A schema extension is required but no core logic changes.

## Changes Required

### Add adventure_category Field to Trip Schema

The `Trip` entity must be extended with a new `adventure_category` field. This field provides the granular classification that replaces the coarse `activity_type` for check-in pattern determination.

**Field specification**:

| Attribute    | Value                                    |
|--------------|------------------------------------------|
| Field name   | adventure_category                       |
| Type         | String (enum)                            |
| Nullable     | Yes (for backward compatibility)         |
| Max length   | 50                                       |
| Validation   | Must be a valid AdventureCategory enum value if present |

### Swagger Specification Update

The svc-trip-catalog `Trip` schema (currently at version 2.4.0) must be updated to include:

```yaml
adventure_category:
  type: string
  nullable: true
  maxLength: 50
  description: >-
    Granular adventure category for check-in classification. Maps to one of
    three check-in UI patterns. If null, svc-check-in will default to
    Pattern 3 (Full Service).
  enum:
    - DAY_HIKE
    - OVERNIGHT_HIKE
    - ALPINE_HIKE
    - SPORT_CLIMBING
    - TRAD_CLIMBING
    - BOULDERING
    - FLATWATER_KAYAK
    - WHITEWATER_KAYAK
    - SEA_KAYAK
    - CLASS_III_RAFTING
    - CLASS_IV_RAFTING
    - FRONTCOUNTRY_CAMPING
    - BACKCOUNTRY_CAMPING
    - CROSS_COUNTRY_MTB
    - DOWNHILL_MTB
    - SLOT_CANYON
    - TECHNICAL_CANYON
    - BEGINNER_SNOWSHOE
    - BACKCOUNTRY_SNOWSHOE
    - RESORT_SKIING
    - BACKCOUNTRY_SKIING
    - BIRDING_SAFARI
    - WILDLIFE_PHOTO_SAFARI
    - NIGHT_SAFARI
    - GUIDED_NATURE_WALK
  example: "DAY_HIKE"
```

This field should be added to the `Trip`, `TripSummary`, `TripCreateRequest`, and `TripUpdateRequest` schemas.

### Activity Type to Adventure Category Mapping

The svc-trip-catalog team is responsible for ensuring that each trip in the catalog has an `adventure_category` value assigned. The mapping from `activity_type` to available adventure categories is:

- HIKING: DAY_HIKE, OVERNIGHT_HIKE, ALPINE_HIKE
- CLIMBING (ROCK_CLIMBING in catalog): SPORT_CLIMBING, TRAD_CLIMBING, BOULDERING
- KAYAKING: FLATWATER_KAYAK, WHITEWATER_KAYAK, SEA_KAYAK
- RAFTING: CLASS_III_RAFTING, CLASS_IV_RAFTING
- CAMPING: FRONTCOUNTRY_CAMPING, BACKCOUNTRY_CAMPING
- MOUNTAIN_BIKING: CROSS_COUNTRY_MTB, DOWNHILL_MTB
- CANYONEERING: SLOT_CANYON, TECHNICAL_CANYON
- SNOWSHOEING: BEGINNER_SNOWSHOE, BACKCOUNTRY_SNOWSHOE
- BACKCOUNTRY_SKIING: RESORT_SKIING, BACKCOUNTRY_SKIING
- WILDLIFE_SAFARI: BIRDING_SAFARI, WILDLIFE_PHOTO_SAFARI, NIGHT_SAFARI, GUIDED_NATURE_WALK

NOTE: The svc-trip-catalog `ActivityType` enum uses slightly different names (e.g., `ROCK_CLIMBING` instead of `CLIMBING`, `WILDLIFE_SAFARI` instead of `SAFARI`, `BACKCOUNTRY_SKIING` instead of `SKIING`). The adventure category field is independent of the activity type field and both will coexist.

### Data Migration

Existing trips in the catalog that do not have an `adventure_category` value will need a one-time data migration. The migration should assign the most appropriate category based on the existing `activity_type` and trip metadata (difficulty level, duration, gear requirements). Trips that cannot be automatically classified should be flagged for manual review by the catalog team.
