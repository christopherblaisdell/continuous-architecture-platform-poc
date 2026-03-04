# NTK-10005 Simple Explanation

## What Is This About

NovaTrek is rolling out new wristbands for the 2026 summer season that contain an embedded RFID chip. Today, when guests check in for an adventure, staff manually enter the wristband's printed code. With the new wristbands, check-in kiosks equipped with RFID readers could scan the wristband automatically instead of requiring manual entry.

## What Is the Problem

The check-in system does not currently have a dedicated place to store the RFID chip identifier at the top level of a check-in record. While the wristband assignment sub-record already captures an RFID tag, the main check-in record lacks a direct RFID field for quick lookup, and the GET endpoint does not support filtering by RFID tag. This means kiosks and downstream systems cannot easily locate a guest's check-in by scanning their wristband.

## What Needs to Change

A new optional field called `rfid_tag` needs to be added to the check-in record so that:

- Kiosks can scan a wristband and record the RFID tag value directly during check-in
- Staff or systems can look up a guest's check-in by scanning their wristband (filtering by RFID tag)
- Other NovaTrek services that consume check-in events receive the RFID tag for contactless interactions throughout the adventure

## Who Does This Affect

- **Guests**: Faster, contactless check-in experience at kiosks
- **Park staff**: Reduced manual data entry during check-in
- **Downstream services**: Any service consuming check-in events will see a new optional field in the event payload
- **Kiosk firmware team**: The firmware update (scheduled for May) depends on this schema being available

## Timeline

The RFID-enabled wristbands start shipping to parks in April 2026, and the kiosk firmware update is scheduled for May 2026. The API schema change must be completed before the firmware release.
