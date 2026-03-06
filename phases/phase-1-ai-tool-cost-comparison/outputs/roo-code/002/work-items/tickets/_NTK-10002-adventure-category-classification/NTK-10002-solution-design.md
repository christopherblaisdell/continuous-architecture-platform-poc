<!-- CONFLUENCE-PUBLISH -->

# NTK-10002: Adventure Category Classification - Solution Design

| Field        | Value                          |
|--------------|--------------------------------|
| **Version**  | 1.8                            |
| **Date**     | 2026-03-04                     |
| **Status**   | APPROVED                       |
| **Author**   | Solution Architecture (AI-Assisted) |
| **Ticket**   | NTK-10002                      |

---

## 1. Problem Statement

NovaTrek's check-in service (`svc-check-in`) currently determines the guest check-in UI experience using the `activity_type` field from the trip reservation. There are 10 activity types, but they are too coarse to accurately classify the check-in requirements. This results in two failure modes:

1. **Over-servicing**: Guests on simple activities (day hikes, bouldering) are presented with unnecessary gear pickup and guide meetup screens, adding friction and confusion.
2. **Under-servicing**: Guests on complex activities (backcountry camping, technical canyoneering) receive an insufficient check-in flow that skips critical safety steps like medical clearance and transport coordination.

Guest satisfaction scores for the check-in experience have declined for 3 consecutive quarters. Operational staff report that manual interventions are required in approximately 15% of check-ins to correct the flow.

## 2. Solution Overview

Introduce an **adventure category classification** system that replaces the coarse `activity_type`-based check-in determination with a granular, 25-category classification mapped to 3 distinct check-in UI patterns. The classification is configuration-driven, cached in memory, and supports booking source overrides.

### Key Design Principles

- **Configuration over code**: The category-to-pattern mapping is defined in YAML configuration, not hardcoded.
- **Safety-first defaults**: Unknown or unmapped categories default to Pattern 3 (Full Service).
- **Override precedence**: Booking source overrides are evaluated before category classification.
- **Backward compatible**: The existing `activity_type` field is retained; `adventure_category` is additive.

## 3. Classification Table

| Adventure Category       | Activity Type    | Check-in Pattern | Pattern Name   |
|--------------------------|------------------|------------------|----------------|
| DAY_HIKE                 | HIKING           | 1                | Basic          |
| OVERNIGHT_HIKE           | HIKING           | 2                | Gear Required  |
| ALPINE_HIKE              | HIKING           | 3                | Full Service   |
| SPORT_CLIMBING           | CLIMBING         | 2                | Gear Required  |
| TRAD_CLIMBING            | CLIMBING         | 3                | Full Service   |
| BOULDERING               | CLIMBING         | 1                | Basic          |
| FLATWATER_KAYAK          | KAYAKING         | 2                | Gear Required  |
| WHITEWATER_KAYAK         | KAYAKING         | 3                | Full Service   |
| SEA_KAYAK                | KAYAKING         | 2                | Gear Required  |
| CLASS_III_RAFTING         | RAFTING          | 2                | Gear Required  |
| CLASS_IV_RAFTING          | RAFTING          | 3                | Full Service   |
| FRONTCOUNTRY_CAMPING     | CAMPING          | 2                | Gear Required  |
| BACKCOUNTRY_CAMPING      | CAMPING          | 3                | Full Service   |
| CROSS_COUNTRY_MTB        | MOUNTAIN_BIKING  | 2                | Gear Required  |
| DOWNHILL_MTB             | MOUNTAIN_BIKING  | 3                | Full Service   |
| SLOT_CANYON               | CANYONEERING     | 2                | Gear Required  |
| TECHNICAL_CANYON          | CANYONEERING     | 3                | Full Service   |
| BEGINNER_SNOWSHOE        | SNOWSHOEING      | 1                | Basic          |
| BACKCOUNTRY_SNOWSHOE     | SNOWSHOEING      | 2                | Gear Required  |
| RESORT_SKIING            | SKIING           | 1                | Basic          |
| BACKCOUNTRY_SKIING       | SKIING           | 3                | Full Service   |
| BIRDING_SAFARI           | SAFARI           | 1                | Basic          |
| WILDLIFE_PHOTO_SAFARI    | SAFARI           | 1                | Basic          |
| NIGHT_SAFARI             | SAFARI           | 2                | Gear Required  |
| GUIDED_NATURE_WALK       | SAFARI           | 1                | Basic          |

## 4. Booking Source Override Rules

| Booking Source | Override Pattern | Reason                                                  |
|----------------|------------------|---------------------------------------------------------|
| PARTNER_API    | Pattern 1        | Partners coordinate gear and guides independently       |
| WALK_IN        | Pattern 3        | Walk-in guests require full onboarding and safety review|
| WEBSITE        | None             | Standard category classification applies                |
| MOBILE_APP     | None             | Standard category classification applies                |
| CALL_CENTER    | None             | Standard category classification applies                |

Override evaluation occurs BEFORE category classification. If a booking source has an override, the category lookup is skipped entirely.

## 5. Pattern Definitions

### Pattern 1 - Basic

- Single confirmation screen
- Guest confirms name, reservation ID, and trip date
- Estimated kiosk time: 30 seconds
- No gear pickup, no guide meetup, no additional steps

### Pattern 2 - Gear Required

- Screen 1: Confirmation (same as Pattern 1)
- Screen 2: Gear pickup checklist with barcode scanning for each item
- Screen 3: Safety briefing acknowledgment with digital signature
- Estimated kiosk time: 3-5 minutes

### Pattern 3 - Full Service

- Screen 1: Confirmation (same as Pattern 1)
- Screen 2: Gear pickup checklist with barcode scanning
- Screen 3: Guide introduction with guide photo, name, and contact info
- Screen 4: Transport coordination with departure time, pickup location map
- Screen 5: Medical clearance form (pre-filled from reservation if available)
- Screen 6: Final summary with all check-in details and emergency contact info
- Estimated kiosk time: 8-12 minutes

## 6. Impacted Components

| Component         | Impact Level | Changes Required                                           |
|--------------------|--------------|------------------------------------------------------------|
| svc-check-in       | PRIMARY      | New ClassificationService, modified check-in flow, new config, API response enhancement |
| svc-trip-catalog   | MINOR        | Add `adventure_category` field to Trip schema, Swagger spec update |
| svc-reservations   | MINOR        | Pass `adventure_category` through to check-in requests     |

## 7. Source Code Analysis

Analysis of the current `AdventureCategoryClassifier.java` in svc-check-in reveals several critical gaps:

### Current Code Issues

| Issue | Current Behavior | Required Behavior |
|-------|-----------------|-------------------|
| Hardcoded categories | Categories defined in static `Set` constants (`PATTERN_1_CATEGORIES`, `PATTERN_2_CATEGORIES`, `PATTERN_3_CATEGORIES`) | Configuration-driven via Spring Cloud Config YAML |
| Category mismatch | Code uses categories like `SCENIC_OVERLOOK`, `BIRD_WATCHING`, `FISHING_BASIC`, `ZIP_LINE` that do NOT match the 25 approved adventure categories | Must use the 25 categories defined in the classification table (Section 3) |
| Unsafe default | Unknown categories default to `PATTERN_1` (Basic) at line 74 | Unknown categories MUST default to `PATTERN_3` (Full Service) per ADR-NTK10002-002 |
| No caching layer | Categories are read from in-memory constants; no config refresh mechanism | Spring `@Cacheable` with configurable TTL for config-driven lookups |
| No feature flag | No ability to toggle between legacy and new classification | Feature flag `novatrek.checkin.use-category-classification` required |

### CRITICAL Safety Concern

The current default to Pattern 1 for unknown categories (line 74: `return UiPattern.PATTERN_1`) means that a guest booked for an unrecognized high-risk activity would receive only a confirmation screen -- bypassing gear verification, safety briefing, guide meetup, and medical clearance. This is the primary motivator for ADR-NTK10002-002 mandating Pattern 3 as the fallback.

### Activity Type Naming Discrepancy

The svc-trip-catalog Swagger spec uses different `ActivityType` enum values than the ticket's classification table:

| Ticket Uses | svc-trip-catalog Uses |
|-------------|----------------------|
| CLIMBING | ROCK_CLIMBING |
| SKIING | BACKCOUNTRY_SKIING |
| SAFARI | WILDLIFE_SAFARI |

This naming discrepancy must be reconciled when implementing the `adventure_category` field on the Trip schema. The `adventure_category` is a separate, more granular field that sits alongside the existing `activity_type`.

## 8. Service Interaction Changes

### Current Service Interactions

```
Guest -> svc-check-in: POST /check-ins (reservation_id)
svc-check-in -> svc-reservations: GET reservation (reads activity_type)
svc-check-in: Hardcoded two-tier classification by activity_type
svc-check-in -> Guest: Check-in response (no pattern info)
```

### Proposed Service Interactions

```
Guest -> svc-check-in: POST /check-ins (reservation_id)
svc-check-in -> svc-reservations: GET reservation (reads booking_source + adventure_category)
svc-check-in -> ClassificationService: determinePattern(bookingSource, adventureCategory)
ClassificationService -> Spring Cloud Config: Load classification mapping (cached, TTL 5 min)
svc-check-in -> Guest: Check-in response (includes determined_pattern, pattern_name)
```

No new service-to-service network calls are introduced. The `ClassificationService` is an internal component within `svc-check-in`. The `svc-reservations` call already exists; the only change is reading `adventure_category` in addition to `activity_type`.

## 9. Data Model Changes

### svc-trip-catalog Trip Schema

The `Trip` schema must be extended with an `adventure_category` field:

```yaml
adventure_category:
  type: string
  nullable: true
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
  description: >-
    Granular adventure classification used for check-in pattern determination.
    More specific than activity_type. Null for legacy trips not yet classified.
  example: "WHITEWATER_KAYAK"
```

### svc-check-in CheckIn Response

Add two new fields to the `CheckIn` schema:

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

## 10. Deployment Notes

- **Phased rollout**: Deploy classification config first, then enable the feature via feature flag (`novatrek.checkin.use-category-classification=true`).
- **Backward compatible**: When the feature flag is disabled, the existing `activity_type`-based logic remains active.
- **Rollback**: Disable the feature flag to revert to previous behavior instantly. No data migration required.
- **Monitoring**: Add metrics for pattern distribution (`checkin.pattern.determined` counter with pattern tag) to verify classification accuracy post-deployment.

## 11. Testing Strategy

- **Unit tests**: Test `ClassificationService` with all 25 categories to verify correct pattern mapping.
- **Unit tests**: Test booking source override logic for PARTNER_API and WALK_IN.
- **Unit tests**: Test fallback behavior for null, empty, and unrecognized categories.
- **Integration tests**: End-to-end check-in flow for each pattern, verifying correct screens are rendered.
- **Integration tests**: Verify that config refresh updates the classification mapping without restart.
- **Performance tests**: Validate that classification lookup adds less than 1ms to check-in request latency.

## 12. Version History

| Version | Date       | Changes                                                              |
|---------|------------|----------------------------------------------------------------------|
| 1.0     | 2024-08-22 | Initial solution design with classification table and pattern defs   |
| 1.2     | 2024-08-26 | Added performance section, cache strategy, addressed dev lead review |
| 1.4     | 2024-08-29 | Added booking source override table and decision flow diagram        |
| 1.6     | 2024-09-03 | Final editorial corrections, product owner approval                  |
| 1.7     | 2026-03-03 | Added source code analysis, service interaction changes, API contract ADR |
| 1.8     | 2026-03-04 | Enhanced with activity type naming discrepancy analysis, data model changes, deployment notes |

## 13. Related Artifacts

- [Ticket Report](1.requirements/NTK-10002.ticket.report.md)
- [Simple Explanation](2.analysis/simple.explanation.md)
- [Assumptions](3.solution/a.assumptions/assumptions.md)
- [Decisions](3.solution/d.decisions/decisions.md)
- [Guidance](3.solution/g.guidance/guidance.md)
- [Impact 1 - svc-check-in](3.solution/i.impacts/impact.1/impact.1.md)
- [Impact 2 - svc-trip-catalog](3.solution/i.impacts/impact.2/impact.2.md)
- [Risks](3.solution/r.risks/risks.md)
- [User Stories](3.solution/u.user.stories/user-stories.md)
