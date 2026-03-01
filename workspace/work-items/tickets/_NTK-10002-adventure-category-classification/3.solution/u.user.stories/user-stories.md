# NTK-10002: User Stories

## US-001: Determine Check-in Pattern from Adventure Category

**As a** check-in kiosk,
**I want to** determine the correct UI pattern based on the guest's adventure category,
**So that** guests see the check-in flow appropriate to the complexity of their booked activity.

### Acceptance Criteria

- Given a reservation with adventure_category = DAY_HIKE, when check-in is initiated, then Pattern 1 (Basic) is returned with only the confirmation screen.
- Given a reservation with adventure_category = WHITEWATER_KAYAK, when check-in is initiated, then Pattern 3 (Full Service) is returned with all 6 screens.
- Given a reservation with adventure_category = FLATWATER_KAYAK, when check-in is initiated, then Pattern 2 (Gear Required) is returned with confirmation, gear pickup, and safety briefing screens.
- The determined pattern is included in the POST /check-ins response as `determined_pattern`.

---

## US-002: Simplified Check-in for Partner Bookings

**As a** guest who booked through a NovaTrek partner,
**I want to** receive a simplified check-in experience regardless of my adventure type,
**So that** I am not asked to complete gear and guide steps that my partner organization has already handled.

### Acceptance Criteria

- Given a reservation with booking_source = PARTNER_API and adventure_category = BACKCOUNTRY_CAMPING, when check-in is initiated, then Pattern 1 (Basic) is returned.
- Given a reservation with booking_source = PARTNER_API and adventure_category = TECHNICAL_CANYON, when check-in is initiated, then Pattern 1 (Basic) is returned.
- The booking source override takes precedence over the category classification in all cases.

---

## US-003: Full Service Check-in for Walk-in Guests

**As a** walk-in guest who has not booked in advance,
**I want to** receive the full-service check-in experience,
**So that** I complete all necessary safety steps, gear verification, and guide coordination before my activity.

### Acceptance Criteria

- Given a reservation with booking_source = WALK_IN and adventure_category = DAY_HIKE, when check-in is initiated, then Pattern 3 (Full Service) is returned.
- Given a reservation with booking_source = WALK_IN and adventure_category = BOULDERING, when check-in is initiated, then Pattern 3 (Full Service) is returned.
- The WALK_IN override applies regardless of the adventure category, even for categories that would normally map to Pattern 1.

---

## US-004: View and Update Classification Mapping

**As an** operations manager,
**I want to** view the current category-to-pattern classification mapping and request updates through configuration,
**So that** the check-in behavior can be adjusted as new adventure categories are introduced or business requirements change.

### Acceptance Criteria

- The classification mapping is stored in a YAML configuration file in Spring Cloud Config.
- Changes to the mapping file are version-controlled and require a pull request review before merge.
- After a configuration change is merged, the mapping can be refreshed without restarting the service by calling the /actuator/refresh endpoint.
- The current active mapping can be verified through the service health or info actuator endpoint.
