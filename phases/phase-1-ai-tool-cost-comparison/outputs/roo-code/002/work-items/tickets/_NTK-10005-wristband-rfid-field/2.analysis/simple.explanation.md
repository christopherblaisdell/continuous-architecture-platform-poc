# NTK-10005 - Simple Explanation

## What is this about

NovaTrek Adventures is introducing new wristbands with a built-in electronic chip for the 2026 summer season. These wristbands work like contactless credit cards -- a reader device can scan them instantly without touching. Each wristband has two identifiers: a printed code on the outside (already supported) and an internal RFID chip identifier (not yet captured in the check-in system).

## Why do we need this

Today, staff must read the printed code on each wristband and type it into the system manually during check-in. This is slow and prone to typing errors. With the new RFID-enabled wristbands, a kiosk or staff terminal can scan the wristband in under a second. Beyond speed, the RFID tag also enables park-wide contactless tracking for safety -- if a guest has not returned from a trail by the expected time, staff can check their last known checkpoint location using RFID readers positioned along the trail.

## What changes

One new data field -- the RFID tag identifier -- needs to be added to the check-in system. When a guest checks in, the kiosk or staff terminal scans the wristband and records both the printed code and the RFID tag. The system also needs to allow staff to look up a check-in record by scanning a wristband (RFID-based search). Everything else about the check-in process stays the same.

## Who is affected

- **Guests**: No change to their experience. The wristband is scanned instead of having its code typed, making check-in slightly faster.
- **Check-in staff**: Faster wristband processing. Staff can also scan a wristband to look up a guest instead of searching by name or reservation number.
- **Trail safety coordinators**: Downstream systems that track guests during adventures will receive the RFID tag, enabling future contactless checkpoint tracking.
- **Downstream system teams**: Services consuming check-in events will see a new optional field. No immediate action is required from those teams.

## Is this a big change

No. This is a small, additive change to a single service (svc-check-in). It adds an optional field to an existing schema. Nothing existing breaks. The main coordination item is notifying downstream teams about the new field in the check-in event payload, and confirming the RFID format matches what the hardware team's kiosk firmware will send.

---

## Architecture Classification

**Classification: Code-Level Task (with light architecture review)**

**Reasoning:**

This ticket is predominantly a code-level task, not a full architecture engagement:

1. **Single service impact**: Only svc-check-in is modified. No new cross-service orchestration, communication patterns, event topics, or infrastructure components are introduced.

2. **No new API endpoints**: The change adds a field to existing schemas and a query parameter filter to an existing endpoint. No new endpoints or services are created.

3. **No architectural decisions required**: There are no competing architectural approaches to evaluate. The implementation path is clear: add a field, add validation, add a uniqueness constraint, add a query parameter.

4. **Existing patterns apply**: The `WristbandAssignment` sub-schema in svc-check-in already has an `rfid_tag` field. This ticket promotes that field to the top-level `CheckIn` schema for direct lookup convenience, following the same established pattern.

**Architecture touchpoints requiring review before merge:**

- Confirm the uniqueness constraint scope (active check-ins only vs global) -- this affects database index design
- Confirm downstream event schema compatibility -- additive fields should be safe under tolerant reader patterns, but this should be verified
- Confirm the RFID format regex (`^[A-F0-9]{8,16}$`) matches the hardware team's kiosk firmware output specification

**Recommendation**: Route to the svc-check-in development team for implementation. Architecture review is recommended at the Swagger spec PR stage, before merge.
