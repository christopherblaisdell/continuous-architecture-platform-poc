# NTK-10005 - User Stories

## US-1: RFID Wristband Scan at Check-In Kiosk

**As a** guest checking in for an adventure at a self-service kiosk,
**I want** the kiosk to scan my RFID wristband automatically,
**so that** I do not have to manually enter the wristband code and my check-in is faster and error-free.

### Acceptance Criteria
- The kiosk scans the RFID wristband and the tag value is recorded as part of my check-in
- If scanning fails, I can still enter the printed wristband code manually
- The check-in confirmation screen shows that my wristband was scanned successfully

## US-2: Staff Lookup by Wristband Scan

**As a** NovaTrek staff member at a check-in station,
**I want** to look up a guest's check-in record by scanning their wristband with an RFID reader,
**so that** I can quickly find their information without asking for their name or reservation number.

### Acceptance Criteria
- Scanning a wristband at the staff terminal returns the associated check-in record
- If no active check-in is found for the scanned RFID tag, a clear message is displayed
- The lookup returns only active check-ins (completed or cancelled check-ins are not returned)

## US-3: Downstream RFID Data for Trail Safety

**As a** trail safety coordinator,
**I want** the check-in confirmation to include the RFID tag so downstream safety tracking systems receive it,
**so that** I can use contactless wristband readers at trail checkpoints to verify guest progress and identify guests who may need assistance.

### Acceptance Criteria
- The check-in notification published to downstream systems includes the RFID tag when present
- If no RFID tag was captured (adventures without wristband tracking), the notification is still published without it
- The RFID tag in the notification matches the tag stored in the check-in record

## US-4: Duplicate Wristband Prevention

**As a** check-in system operator,
**I want** the system to reject duplicate RFID tags across active check-ins,
**so that** two guests cannot accidentally have the same wristband assigned, which would cause tracking confusion during adventures.

### Acceptance Criteria
- If an RFID tag is already associated with an active check-in, a new assignment with the same tag is rejected with a clear error
- The rejection message identifies the conflict so the operator can resolve it
- Once a check-in is completed or cancelled, the RFID tag becomes available for reassignment to a different guest

## US-5: Adventures Without Wristband Tracking

**As a** guest on a low-intensity adventure that does not use wristband tracking,
**I want** my check-in to proceed normally without requiring an RFID wristband scan,
**so that** the new tracking feature does not slow down check-in for adventures that do not need it.

### Acceptance Criteria
- Check-in completes successfully when no RFID tag is provided
- The absence of an RFID tag does not affect any other check-in steps (waiver, gear, group assembly)
- The check-in record clearly indicates that no wristband RFID was assigned
