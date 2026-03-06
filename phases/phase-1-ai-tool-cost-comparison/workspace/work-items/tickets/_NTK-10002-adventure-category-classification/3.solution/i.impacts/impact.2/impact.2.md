# NTK-10002: Impact 2 - svc-trip-catalog (MINOR)

## Service

**svc-trip-catalog** - The service that manages the catalog of available trips, activities, and trip metadata.

## Impact Level

MINOR - A schema extension is required but no core logic changes.

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

### Activity Type to Adventure Category Mapping

The `svc-trip-catalog` team is responsible for ensuring that each trip in the catalog has an `adventure_category` value assigned. The mapping from `activity_type` to available adventure categories is:

- HIKING: DAY_HIKE, OVERNIGHT_HIKE, ALPINE_HIKE
- CLIMBING: SPORT_CLIMBING, TRAD_CLIMBING, BOULDERING
- KAYAKING: FLATWATER_KAYAK, WHITEWATER_KAYAK, SEA_KAYAK
- RAFTING: CLASS_III_RAFTING, CLASS_IV_RAFTING
- CAMPING: FRONTCOUNTRY_CAMPING, BACKCOUNTRY_CAMPING
- MOUNTAIN_BIKING: CROSS_COUNTRY_MTB, DOWNHILL_MTB
- CANYONEERING: SLOT_CANYON, TECHNICAL_CANYON
- SNOWSHOEING: BEGINNER_SNOWSHOE, BACKCOUNTRY_SNOWSHOE
- SKIING: RESORT_SKIING, BACKCOUNTRY_SKIING
- SAFARI: BIRDING_SAFARI, WILDLIFE_PHOTO_SAFARI, NIGHT_SAFARI, GUIDED_NATURE_WALK

### Swagger Spec Update

The Trip API Swagger specification must be updated to include the `adventure_category` field in the Trip response model. The field should be documented with the full list of valid enum values and a description of its purpose.

### Data Migration

Existing trips in the catalog that do not have an `adventure_category` value will need a one-time data migration. The migration should assign the most appropriate category based on the existing `activity_type` and trip metadata. Trips that cannot be automatically classified should be flagged for manual review by the catalog team.
