# NTK-10002: Impact 2 - svc-trip-catalog (MINOR)

## Service

**svc-trip-catalog** - The service that manages the catalog of available trips, activities, and trip metadata.

## Impact Level

MINOR - A schema extension is required but no core logic changes.

## Changes Required

### Add adventure_category Field to Trip Schema

The `Trip` entity and corresponding Swagger spec must be extended with a new `adventure_category` field. This field provides the granular classification that replaces the coarse `activity_type` for check-in pattern determination.

**Field specification**:

| Attribute    | Value                                    |
|--------------|------------------------------------------|
| Field name   | adventure_category                       |
| Type         | String (enum)                            |
| Nullable     | Yes (for backward compatibility with existing trips) |
| Max length   | 50                                       |
| Validation   | Must be a valid AdventureCategory enum value if present |
| Enum values  | 25 values (see classification table in solution design) |

### Swagger Specification Update

The following schemas in `svc-trip-catalog.yaml` require modification:

| Schema | Change |
|--------|--------|
| `Trip` | Add `adventure_category` property (nullable string enum) |
| `TripSummary` | Add `adventure_category` property (nullable string enum) |
| `TripCreateRequest` | Add `adventure_category` property (optional) |
| `TripUpdateRequest` | Add `adventure_category` property (optional) |

### Activity Type to Adventure Category Mapping

The `svc-trip-catalog` team is responsible for ensuring that each trip in the catalog has an `adventure_category` value assigned. The mapping from the existing `activity_type` enum (as defined in the Swagger spec) to available adventure categories:

| svc-trip-catalog ActivityType | Available Adventure Categories |
|-------------------------------|-------------------------------|
| HIKING | DAY_HIKE, OVERNIGHT_HIKE, ALPINE_HIKE |
| ROCK_CLIMBING | SPORT_CLIMBING, TRAD_CLIMBING, BOULDERING |
| KAYAKING | FLATWATER_KAYAK, WHITEWATER_KAYAK, SEA_KAYAK |
| RAFTING | CLASS_III_RAFTING, CLASS_IV_RAFTING |
| CAMPING | FRONTCOUNTRY_CAMPING, BACKCOUNTRY_CAMPING |
| MOUNTAIN_BIKING | CROSS_COUNTRY_MTB, DOWNHILL_MTB |
| CANYONEERING | SLOT_CANYON, TECHNICAL_CANYON |
| SNOWSHOEING | BEGINNER_SNOWSHOE, BACKCOUNTRY_SNOWSHOE |
| BACKCOUNTRY_SKIING | RESORT_SKIING, BACKCOUNTRY_SKIING |
| WILDLIFE_SAFARI | BIRDING_SAFARI, WILDLIFE_PHOTO_SAFARI, NIGHT_SAFARI, GUIDED_NATURE_WALK |

NOTE: The svc-trip-catalog `ActivityType` enum uses `ROCK_CLIMBING`, `BACKCOUNTRY_SKIING`, and `WILDLIFE_SAFARI` whereas the ticket classification table uses `CLIMBING`, `SKIING`, and `SAFARI`. The `adventure_category` is a separate, independent field that does not depend on these naming differences. The `activity_type` field is retained unchanged.

### Data Migration

Existing trips in the catalog that do not have an `adventure_category` value will need a one-time data migration:

1. Trips with a clear mapping (e.g., single-category activity types like RAFTING with only CLASS_III_RAFTING and CLASS_IV_RAFTING) can be auto-classified based on trip metadata (difficulty level, duration, gear requirements).
2. Trips that cannot be automatically classified should be flagged for manual review by the catalog team.
3. Until migration is complete, trips without `adventure_category` will trigger the Pattern 3 (Full Service) fallback in svc-check-in, which is the safe default per ADR-NTK10002-002.
