# NTK-10003 - User Stories

## US-1: Unregistered Guest Kiosk Check-in

**As an** unregistered guest arriving at a NovaTrek base camp,
**I want to** check in at the self-service kiosk using my reservation confirmation code,
**So that** I can complete check-in quickly without waiting in the staff-assisted queue.

### Acceptance Criteria

- Given I am at the kiosk welcome screen, when I select "Check in with Confirmation Code", then a form requesting last name, confirmation code, adventure date, and participant count is displayed
- Given I enter all four fields correctly, when I submit the form, then I am granted a temporary kiosk session and see my reservation details, waiver status, and gear assignments
- Given I enter incorrect information, when I submit the form, then I see a generic error message and the number of remaining attempts
- Given my session is active, when I complete check-in, then I receive a check-in confirmation with adventure briefing details and gear pickup location

---

## US-2: Partner-Booked Guest Verification

**As a** guest who booked through a travel partner (ExploreMore, TrailFinder, or WildPass),
**I want to** verify my identity and access the self-service kiosk even if my booking is not yet synced to NovaTrek,
**So that** I have the same check-in experience as guests who booked directly.

### Acceptance Criteria

- Given my partner booking has not been synced to NovaTrek's reservation system, when I enter my partner confirmation code at the kiosk, then the system automatically checks with the booking partner for verification
- Given the partner confirms my booking, when the verification succeeds, then my reservation is synced to NovaTrek and I proceed with kiosk check-in
- Given the partner system is unavailable, when the fallback fails, then I see a message directing me to the service desk with priority queuing
- Given my partner booking has already been synced (via nightly sync), when I enter my details, then the direct lookup succeeds without requiring the partner fallback

---

## US-3: Gift Card Recipient First-Time Check-in

**As a** gift card recipient checking in for my first NovaTrek adventure,
**I want to** use the kiosk without needing to create a NovaTrek account first,
**So that** I can start my experience without unnecessary registration steps.

### Acceptance Criteria

- Given I received a reservation confirmation code via email from the gift card purchase, when I enter my details at the kiosk, then the system finds my reservation and creates a temporary guest profile for me
- Given I completed check-in with a temporary profile, when I finish my adventure, then I am prompted to create a full NovaTrek account to preserve my check-in history and earn rewards
- Given I choose not to create an account, when I leave, then my temporary profile is retained for 90 days (for analytics) and then anonymized

---

## US-4: Protection Against Misuse

**As a** base camp manager,
**I want** the self-service kiosk to limit repeated failed verification attempts,
**So that** the system is protected against misuse and guests who cannot verify are directed to staff assistance.

### Acceptance Criteria

- Given a kiosk has received multiple failed lookup attempts, when further attempts are made, then the kiosk displays a message directing the guest to the service desk for assistance
- Given a lookup attempt fails, when the response is returned, then there is a brief delay before the failure is displayed to discourage rapid repeated attempts
- Given a guest has difficulty verifying, when they reach the attempt limit, then they know exactly where to go for in-person help
- Given any lookup activity occurs, when reviewed by operations, then all attempts are traceable for security audit purposes

---

## US-5: Operations Staff Check-in Analytics

**As** operations staff at a base camp,
**I want to** see analytics that differentiate between kiosk check-ins (registered and unregistered) and staff-assisted check-ins,
**So that** I can measure the impact of the self-service kiosk for unregistered guests and optimize staffing levels.

### Acceptance Criteria

- Given check-ins have been processed, when I view the check-in analytics dashboard, then I see separate counts for: registered-guest kiosk, unregistered-guest kiosk, and staff-assisted check-ins
- Given the analytics data is available, when I filter by date range and base camp, then I see average check-in times and completion rates for each check-in channel
- Given the kiosk self-service option is enabled, when I compare pre-launch and post-launch periods, then I can measure the reduction in staff-assisted check-in volume
- Given a guest abandons the kiosk check-in flow, when I view the dashboard, then I see the abandonment recorded with the step where the guest exited
