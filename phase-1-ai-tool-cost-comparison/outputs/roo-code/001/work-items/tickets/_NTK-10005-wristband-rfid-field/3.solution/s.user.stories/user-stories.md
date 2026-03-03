# NTK-10005 - User Stories

## US-1: RFID Wristband Scan at Check-In Kiosk

**As a** guest checking in for an adventure at a self-service kiosk,
**I want** the kiosk to scan my RFID wristband automatically,
**so that** I do not have to manually type the printed wristband code and my check-in is faster and error-free.

### Acceptance Criteria

- The kiosk scans the RFID wristband and the tag value is recorded as part of my check-in
- If scanning fails, I can still enter the printed wristband code manually
- The check-in confirmation screen shows that my wristband was successfully scanned

## US-2: Staff Lookup by RFID Tag

**As a** NovaTrek staff member at a check-in station,
**I want** to look up a guest check-in record by scanning their wristband,
**so that** I can quickly find their information without asking for their name or reservation number.

### Acceptance Criteria

- Scanning a wristband at the staff terminal returns the associated check-in record
- If no active check-in is found for the scanned RFID tag, a clear message is displayed
- The lookup returns only active check-ins (completed or cancelled check-ins are not returned)

## US-3: Downstream RFID Data for Trail Safety

**As a** trail safety coordinator,
**I want** the RFID tag to be included in check-in notifications sent to downstream systems,
**so that** contactless wristband readers at trail checkpoints can verify guest progress and location.

### Acceptance Criteria

- The check-in notification includes the RFID tag when one has been captured
- If no RFID tag was captured (for adventures without wristband tracking), the notification is still sent without it
- The RFID tag in the notification matches the tag stored in the check-in record

## US-4: Duplicate Wristband Prevention

**As a** check-in system operator,
**I want** the system to reject duplicate RFID tags across active check-ins,
**so that** two guests cannot accidentally have the same wristband assigned, which would cause tracking confusion and safety issues.

### Acceptance Criteria

- If an RFID tag is already associated with an active check-in, a new assignment with the same tag is rejected
- The rejection message clearly identifies the conflict
- Once a check-in is completed or cancelled, the RFID tag becomes available for reassignment to a new guest
