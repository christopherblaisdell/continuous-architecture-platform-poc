# NTK-10002: Assumptions

## A1 Adventure Category Stability

The set of 25 adventure categories is expected to remain relatively stable. New categories may be added at most once or twice per quarter. The classification system is designed for low-frequency updates, not continuous change. If category additions become frequent, the configuration-driven approach should be reevaluated in favor of a database-backed solution.

## A2 Booking Source Field Completeness

All reservations in `svc-reservations` have a populated `booking_source` field. The override logic depends on this field being present and containing one of the known values (PARTNER_API, WALK_IN, WEBSITE, MOBILE_APP, CALL_CENTER). If `booking_source` is null or unrecognized, no override is applied and the standard category classification is used.

## A3 Check-in Kiosk Support for All Patterns

The check-in kiosk hardware and software can support all 3 check-in UI patterns, including the 6-screen Pattern 3 flow with medical clearance form input and map rendering. No kiosk hardware upgrades are required. The mobile check-in client likewise supports all patterns.

## A4 Cached Config Refresh Frequency

A cache TTL of 5 minutes is acceptable for the classification configuration. This means that after a config change is pushed to Spring Cloud Config, it may take up to 5 minutes for all service instances to reflect the update. For urgent changes, the `/actuator/refresh` endpoint can be called manually to force an immediate reload.

## A5 No Retroactive Application

The adventure category classification will apply only to check-ins occurring after the feature is enabled. Historical check-in records will not be retroactively reclassified. Reporting and analytics based on historical data will continue to use the original `activity_type` field.

## A6 Single Category Per Trip

Each trip reservation has exactly one `adventure_category` value. Multi-activity trips (e.g., a trip that includes both hiking and kayaking) are classified under the primary activity. The classification system does not support composite patterns for multi-activity reservations in this iteration.

## A7 Spring Cloud Config Availability

The Spring Cloud Config server is assumed to be available and operational. If the config server is unreachable at service startup, the service will fail to start by default. In production, the last known good configuration should be cached locally as a fallback.

## A8 svc-reservations Passes adventure_category

The `svc-reservations` service will be updated to include the `adventure_category` field in its reservation response payload. This field originates from `svc-trip-catalog` and is stored on the reservation at booking time. The reservation service change is a prerequisite for the check-in classification feature.
