# NTK-10003 - User Stories

## US-001: Self-Service Check-in with Confirmation Code

**As an** unregistered guest arriving for a NovaTrek adventure,
**I want** to check in at a self-service kiosk using my confirmation code and personal details,
**So that** I can complete check-in without waiting in the staff-assisted queue.

### Acceptance Criteria

- I can select "Check in with Confirmation Code" on the kiosk welcome screen
- I enter my last name, confirmation code, adventure date, and participant count
- Upon successful verification, the kiosk displays my adventure details and guides me through the check-in steps
- The entire self-service process takes less than 5 minutes

---

## US-002: Partner-Booked Guest Self-Service

**As a** guest who booked through a NovaTrek travel partner (ExploreMore, TrailFinder, WildPass),
**I want** the kiosk to recognize my partner booking,
**So that** I receive the same self-service check-in experience as directly-booked guests.

### Acceptance Criteria

- If my reservation is not found through direct lookup, the system automatically checks with my booking partner
- I do not need to know whether my booking was direct or through a partner -- the kiosk handles this transparently
- If the partner system is unavailable, I am directed to the service desk with a priority queue message

---

## US-003: Digital Waiver Completion at Kiosk

**As an** unregistered guest who has not completed a safety waiver,
**I want** to sign the required safety waiver on the kiosk touchscreen during check-in,
**So that** I can complete all required safety steps in one place without additional paperwork.

### Acceptance Criteria

- If my waiver is incomplete, the kiosk displays the digital waiver signing interface
- I can read the waiver terms and sign with my finger on the kiosk touchscreen
- After signing, my waiver status is updated and I can continue the check-in process
- The signed waiver is associated with my temporary profile for record-keeping

---

## US-004: Staff Awareness of Kiosk Activity

**As a** check-in staff member at a base camp,
**I want** to see when an unregistered guest abandons the kiosk self-service flow or is directed to the service desk,
**So that** I can proactively assist them and avoid making them re-explain their situation.

### Acceptance Criteria

- My staff dashboard shows real-time kiosk activity including guests who were directed to the service desk
- If a guest was directed to me after a failed kiosk lookup, I can see what they already attempted
- I can quickly look up the guest by confirmation code to continue their check-in manually

---

## US-005: Post Check-in Registration Prompt

**As an** unregistered guest who has completed self-service check-in,
**I want** to be offered the option to create a NovaTrek account,
**So that** my next visit has an even faster check-in experience.

### Acceptance Criteria

- After completing check-in, the kiosk displays a registration prompt: "Want faster check-in next time?"
- I can choose to register with my email address or skip for now
- If I register, my check-in history from this visit is linked to my new account
- If I skip, my temporary profile is retained and anonymized after 90 days

---

## US-006: Secure Rate-Limited Kiosk Access

**As a** NovaTrek security administrator,
**I want** the kiosk self-service lookup to be rate-limited and audited,
**So that** the system is protected against reservation enumeration attacks and all access attempts are traceable.

### Acceptance Criteria

- Each kiosk allows a maximum of 5 lookup attempts per 15-minute window
- Failed lookups include a 2-second delay before responding
- All lookup attempts (successful and failed) are logged with kiosk ID and masked input fields
- If the rate limit is exceeded, the kiosk displays a message directing the guest to the service desk
