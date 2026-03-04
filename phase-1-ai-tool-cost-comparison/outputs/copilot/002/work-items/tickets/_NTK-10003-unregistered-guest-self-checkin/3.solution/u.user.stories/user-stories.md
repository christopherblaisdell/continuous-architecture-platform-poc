# NTK-10003 - User Stories

## US-1: Unregistered Guest Kiosk Check-In

**As an** unregistered guest arriving at a NovaTrek base camp,
**I want to** check in at a self-service kiosk using my booking confirmation details,
**so that** I can complete the check-in process without waiting in line for staff assistance.

### Acceptance Criteria

1. Given I am at a kiosk, when I enter my confirmation code, last name, adventure date, and participant count, then the system locates my reservation and begins the check-in flow.
2. Given the system locates my reservation, when I proceed, then a guest profile is created for me automatically without requiring an email address or account creation.
3. Given my reservation is found, when the check-in flow begins, then the kiosk displays my adventure details (trip name, time, guide assignment, meeting point) and any outstanding waiver requirements.
4. Given I have outstanding waivers, when I am prompted on the kiosk, then I can digitally sign the required waivers before completing check-in.
5. Given I complete check-in, when the process finishes, then I receive a wristband assignment and a confirmation screen with a summary of my adventure details.

---

## US-2: Partner-Booked Guest Verification

**As a** guest who booked through a third-party partner (travel agency, hotel concierge),
**I want to** check in at a self-service kiosk using my partner-issued confirmation code,
**so that** I can check in without needing to visit the staff desk to have my booking manually located.

### Acceptance Criteria

1. Given my booking was made through a partner, when my confirmation code is not found in the NovaTrek reservation system, then the system automatically queries partner integration records.
2. Given the partner system confirms my booking, when the lookup succeeds, then I see the same check-in flow as a direct-booked guest.
3. Given the partner system is unavailable or does not recognize my confirmation code, when the lookup fails, then the kiosk displays a message directing me to the staff desk for manual assistance.
4. Given the partner lookup takes longer than expected, when the system is still waiting, then the kiosk displays a progress indicator rather than timing out silently.

---

## US-3: Gift Card Recipient First-Time Check-In

**As a** guest who received a NovaTrek adventure as a gift,
**I want to** check in using the confirmation code from my gift voucher,
**so that** I can start my adventure without needing the original purchaser to be present.

### Acceptance Criteria

1. Given I have a gift voucher confirmation code, when I enter it at the kiosk with my own last name (which may differ from the purchaser), then the system matches using the confirmation code, adventure date, and participant count.
2. Given the last name on the reservation does not match my last name, when the confirmation code, adventure date, and participant count all match, then the system initiates a staff-assisted verification rather than denying access.
3. Given a temporary profile is created for me, when I complete check-in, then my profile is associated with my reservation for the duration of the adventure.

---

## US-4: Protection Against Misuse at Kiosks

**As a** NovaTrek operations manager,
**I want** the kiosk lookup to be rate-limited and restricted to prevent enumeration attacks,
**so that** guest reservation data is protected from unauthorized access even though the kiosk is in a public area.

### Acceptance Criteria

1. Given a kiosk device, when more than 5 lookup attempts are made within 15 minutes, then the kiosk displays a rate-limiting message and directs the user to the staff desk.
2. Given a failed lookup attempt, when the system responds, then it does not reveal whether the confirmation code exists but the other fields were wrong (generic "not found" message).
3. Given a successful lookup, when the system creates a session, then the session expires after a configured timeout (default 15 minutes) if the check-in is not completed.
4. Given the session expires, when the guest returns to the kiosk, then they must repeat the full lookup process.

---

## US-5: Operations Staff Visibility Into Unregistered Check-Ins

**As a** NovaTrek base camp operations staff member,
**I want to** see which guests checked in through the unregistered kiosk flow versus the registered flow,
**so that** I can identify guests who may need additional assistance and monitor adoption of the self-service channel.

### Acceptance Criteria

1. Given guests are checking in, when I view the daily check-in dashboard, then I can filter by check-in channel (registered app, unregistered kiosk, staff-assisted).
2. Given the daily activity log, when I review it, then I can see the count of temporary profiles created, rate limit events triggered, and partner fallback lookups performed.
3. Given a guest checked in via the unregistered kiosk flow, when I view their check-in record, then it clearly indicates `profile_type: TEMPORARY` and the session that was used.
