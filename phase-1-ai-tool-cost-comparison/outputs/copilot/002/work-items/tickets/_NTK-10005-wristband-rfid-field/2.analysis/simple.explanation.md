# NTK-10005: Simple Explanation

## What Is This About

NovaTrek is rolling out new wristbands for the 2026 summer season that contain RFID chips -- small electronic tags that can be read by scanners without physical contact (like a contactless payment card). Each wristband has two identifiers:

1. **A printed code** on the band that guests or staff can read visually (the system already supports this)
2. **An RFID chip identifier** that scanners at kiosks can detect automatically (the system does NOT support this yet)

## What Is the Problem

Today, when a guest checks in at a kiosk, they must manually type in or have staff enter the wristband code. With the new RFID-enabled wristbands, the kiosk could simply scan the wristband -- but the system has no place to store or look up the RFID tag value.

## What Needs to Change

The check-in system needs a new field added to its records to store the RFID tag identifier. This will allow:

- **Kiosks** to scan and record the RFID tag during check-in instead of manual entry
- **Staff** to look up a guest by scanning their wristband
- **Other park systems** to receive the RFID tag when notified about a check-in, enabling contactless interactions throughout the park

## Who Is Affected

- **Guests**: Faster, more convenient check-in experience via tap-to-scan
- **Park staff**: Can scan wristbands instead of manually typing codes
- **Downstream services**: Any service that consumes check-in events will receive the new RFID data

## Timeline

The RFID-enabled wristbands ship to parks in April 2026, and the kiosk firmware update is scheduled for May 2026. The API change needs to be completed before the firmware release.
