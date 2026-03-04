# NTK-10002: User Stories

## US-001: Adventure-Appropriate Check-in Experience

**As a** guest arriving for an adventure,
**I want** the check-in process to match the complexity of my booked activity,
**So that** I complete all necessary preparation steps without being slowed down by steps I do not need.

### Acceptance Criteria

- A guest booked for a simple day hike sees only a confirmation screen and is checked in within 30 seconds.
- A guest booked for a whitewater kayaking trip sees confirmation, gear pickup verification, and a safety briefing.
- A guest booked for a backcountry camping expedition sees the full check-in flow including gear pickup, guide meetup, transport coordination, and medical clearance.
- The check-in experience is determined automatically based on the specific adventure category of the booking.

---

## US-002: Simplified Check-in for Partner Bookings

**As a** guest who booked through a NovaTrek partner organization,
**I want** a simplified check-in experience,
**So that** I am not asked to repeat gear and guide coordination steps that my partner has already handled on my behalf.

### Acceptance Criteria

- A guest who booked through a partner always receives the basic confirmation-only check-in, regardless of their adventure type.
- The partner booking status is recognized automatically without the guest needing to explain their situation.

---

## US-003: Full Service Check-in for Walk-in Guests

**As a** walk-in guest who has not booked in advance,
**I want** to receive the full check-in experience,
**So that** I complete all necessary safety preparation, gear verification, and guide coordination before my activity.

### Acceptance Criteria

- A walk-in guest always receives the full check-in flow, including gear pickup, guide meetup, transport details, and medical clearance.
- The full flow applies regardless of the adventure type the walk-in guest selects, because walk-in guests have not completed any pre-trip preparation.

---

## US-004: Safe Default for Unknown Activities

**As a** guest booked for a newly introduced adventure type,
**I want** the system to provide the most thorough check-in experience when it does not recognize my activity,
**So that** I do not miss any critical safety steps due to a classification gap.

### Acceptance Criteria

- If the system does not recognize my adventure category, I receive the full check-in flow with all safety and preparation steps.
- I am never sent on a high-risk activity without completing gear verification and safety briefing, even if my activity was recently added and not yet classified.

---

## US-005: Adjustable Classification Rules

**As an** operations manager,
**I want** to be able to request adjustments to which adventures receive which check-in experience,
**So that** the check-in process can evolve as new adventure types are introduced or business needs change.

### Acceptance Criteria

- Changes to the adventure classification rules go through a review process before taking effect.
- Updated rules take effect within minutes without requiring a system restart or guest-facing downtime.
- The current classification rules are auditable and traceable through version control history.
