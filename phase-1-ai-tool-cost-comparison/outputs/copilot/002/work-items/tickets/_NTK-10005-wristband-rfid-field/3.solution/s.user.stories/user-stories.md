# NTK-10005 User Stories

## US-1 Guest RFID Wristband Scan at Kiosk

**As a** guest checking in for an adventure,
**I want to** scan my RFID wristband at the check-in kiosk,
**so that** the kiosk automatically records my wristband identifier without manual entry.

### Acceptance Criteria

- The kiosk displays a prompt to scan the RFID wristband
- After scanning, the kiosk confirms the RFID tag has been recorded
- If scanning fails, the guest can still enter the wristband code manually
- The check-in proceeds normally regardless of whether RFID scanning was used

## US-2 Staff Lookup by RFID Scan

**As a** park staff member,
**I want to** scan a guest's wristband with an RFID reader to view their check-in details,
**so that** I can quickly identify the guest and their adventure assignment without asking for their name or reservation number.

### Acceptance Criteria

- Scanning a wristband returns the associated check-in record
- If no active check-in is found for the RFID tag, a clear "not found" message is displayed
- The lookup returns the same check-in details as a search by reservation ID

## US-3 Guest Contactless Interactions During Adventure

**As a** guest on an adventure,
**I want** my RFID wristband to be recognized by park systems throughout the day,
**so that** I can access facilities and receive personalized services without carrying additional identification.

### Acceptance Criteria

- Downstream park systems can retrieve the RFID tag from the check-in event
- The RFID tag remains associated with the check-in for the duration of the adventure
- After the adventure is complete, the RFID tag association is released for future reuse

## US-4 Operations Duplicate RFID Prevention

**As a** check-in operations manager,
**I want** the system to reject duplicate RFID tag assignments for active check-ins,
**so that** each wristband is uniquely associated with one guest at a time, preventing tracking confusion.

### Acceptance Criteria

- If an RFID tag is already assigned to an active check-in, a new check-in with the same RFID tag is rejected
- The rejection message clearly identifies the conflict
- Once a check-in is completed or cancelled, the RFID tag becomes available for reassignment
