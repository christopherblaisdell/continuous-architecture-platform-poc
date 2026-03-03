# NTK-10005: User Stories

## US-1: Guest Scans Wristband at Kiosk

**As a** guest arriving for an adventure,
**I want to** tap my RFID wristband on the kiosk scanner during check-in,
**so that** my wristband is automatically registered without manually typing the code.

### Acceptance Criteria
- The kiosk displays a "Tap your wristband" prompt during check-in
- After tapping, the RFID tag is captured and the check-in proceeds
- If the RFID is already in use for another active check-in, the guest sees a clear error message

## US-2: Staff Looks Up Guest by Wristband Scan

**As a** park staff member,
**I want to** scan a guest's wristband to pull up their check-in record,
**so that** I can quickly assist with questions or issues without asking for booking details.

### Acceptance Criteria
- Staff can search for a check-in record using the RFID tag value
- The search returns the matching active check-in with guest and reservation details

## US-3: Guest Checks In Without RFID Wristband

**As a** guest whose wristband does not have an RFID chip (legacy band),
**I want to** still be able to check in using the manual wristband code entry,
**so that** the new RFID feature does not prevent me from checking in.

### Acceptance Criteria
- Check-in works normally when no RFID tag is provided
- The RFID field is optional and does not block the check-in flow

## US-4: Downstream Service Receives RFID Data

**As a** park experience coordinator,
**I want** the guest's RFID tag included in check-in notifications,
**so that** other park systems can offer contactless interactions throughout the adventure.

### Acceptance Criteria
- Check-in event notifications include the RFID tag when present
- Downstream systems that do not use RFID are unaffected
