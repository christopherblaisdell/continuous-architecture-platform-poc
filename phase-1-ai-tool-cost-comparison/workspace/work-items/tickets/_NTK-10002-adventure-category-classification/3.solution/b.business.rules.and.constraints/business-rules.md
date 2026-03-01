# NTK-10002: Business Rules and Constraints

## Classification Mapping Table

Each adventure category is assigned exactly one check-in pattern. This mapping is the authoritative source for determining check-in behavior.

| # | Adventure Category       | Parent Activity Type | Check-in Pattern | Pattern Name   |
|---|--------------------------|----------------------|------------------|----------------|
| 1 | DAY_HIKE                 | HIKING               | 1                | Basic          |
| 2 | OVERNIGHT_HIKE           | HIKING               | 2                | Gear Required  |
| 3 | ALPINE_HIKE              | HIKING               | 3                | Full Service   |
| 4 | SPORT_CLIMBING           | CLIMBING             | 2                | Gear Required  |
| 5 | TRAD_CLIMBING            | CLIMBING             | 3                | Full Service   |
| 6 | BOULDERING               | CLIMBING             | 1                | Basic          |
| 7 | FLATWATER_KAYAK          | KAYAKING             | 2                | Gear Required  |
| 8 | WHITEWATER_KAYAK         | KAYAKING             | 3                | Full Service   |
| 9 | SEA_KAYAK                | KAYAKING             | 2                | Gear Required  |
|10 | CLASS_III_RAFTING         | RAFTING              | 2                | Gear Required  |
|11 | CLASS_IV_RAFTING          | RAFTING              | 3                | Full Service   |
|12 | FRONTCOUNTRY_CAMPING     | CAMPING              | 2                | Gear Required  |
|13 | BACKCOUNTRY_CAMPING      | CAMPING              | 3                | Full Service   |
|14 | CROSS_COUNTRY_MTB        | MOUNTAIN_BIKING      | 2                | Gear Required  |
|15 | DOWNHILL_MTB             | MOUNTAIN_BIKING      | 3                | Full Service   |
|16 | SLOT_CANYON               | CANYONEERING         | 2                | Gear Required  |
|17 | TECHNICAL_CANYON          | CANYONEERING         | 3                | Full Service   |
|18 | BEGINNER_SNOWSHOE        | SNOWSHOEING          | 1                | Basic          |
|19 | BACKCOUNTRY_SNOWSHOE     | SNOWSHOEING          | 2                | Gear Required  |
|20 | RESORT_SKIING            | SKIING               | 1                | Basic          |
|21 | BACKCOUNTRY_SKIING       | SKIING               | 3                | Full Service   |
|22 | BIRDING_SAFARI           | SAFARI               | 1                | Basic          |
|23 | WILDLIFE_PHOTO_SAFARI    | SAFARI               | 1                | Basic          |
|24 | NIGHT_SAFARI             | SAFARI               | 2                | Gear Required  |
|25 | GUIDED_NATURE_WALK       | SAFARI               | 1                | Basic          |

## Booking Source Override Rules

Booking source overrides take precedence over category classification. When a booking source has an override defined, the category lookup is skipped entirely.

| Rule | Booking Source | Override Pattern | Business Justification                            |
|------|----------------|------------------|---------------------------------------------------|
| OVR-1| PARTNER_API    | Pattern 1 (Basic)| Partners manage gear and guide logistics externally|
| OVR-2| WALK_IN        | Pattern 3 (Full Service)| Walk-in guests have no pre-trip preparation |

All other booking sources (WEBSITE, MOBILE_APP, CALL_CENTER) use the standard category classification with no override.

## Fallback Rule

**RULE-FALLBACK-001**: If the `adventure_category` field on a reservation is null, empty, or contains a value not present in the classification table, the system SHALL assign **Pattern 3 (Full Service)**.

**Rationale**: Safety-first principle. It is better to over-service a guest with unnecessary steps than to under-service a guest and skip critical safety procedures.

## Pattern Behavior Specifications

### Pattern 1 - Basic

| Attribute              | Value                          |
|------------------------|--------------------------------|
| Screens                | 1 (Confirmation)               |
| Gear Pickup            | No                             |
| Safety Briefing        | No                             |
| Guide Meetup           | No                             |
| Transport Coordination | No                             |
| Medical Clearance      | No                             |
| Estimated Duration     | 30 seconds                     |

### Pattern 2 - Gear Required

| Attribute              | Value                          |
|------------------------|--------------------------------|
| Screens                | 3 (Confirmation, Gear, Safety) |
| Gear Pickup            | Yes (barcode scan verification)|
| Safety Briefing        | Yes (digital acknowledgment)   |
| Guide Meetup           | No                             |
| Transport Coordination | No                             |
| Medical Clearance      | No                             |
| Estimated Duration     | 3-5 minutes                    |

### Pattern 3 - Full Service

| Attribute              | Value                                       |
|------------------------|---------------------------------------------|
| Screens                | 6 (Confirm, Gear, Guide, Transport, Medical, Summary) |
| Gear Pickup            | Yes (barcode scan verification)             |
| Safety Briefing        | Yes (included in guide meetup)              |
| Guide Meetup           | Yes (guide photo, name, contact)            |
| Transport Coordination | Yes (departure time, pickup map)            |
| Medical Clearance      | Yes (form, pre-filled if available)         |
| Estimated Duration     | 8-12 minutes                                |
