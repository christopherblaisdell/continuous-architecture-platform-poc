# NTK-10005 - Simple Explanation

## What is this about

NovaTrek Adventures is upgrading to new wristbands that contain a small electronic chip -- similar to how a contactless credit card or hotel key card works. These are called RFID (Radio Frequency Identification) wristbands. When guests check in for an adventure, a reader at the kiosk or staff station can instantly scan the wristband instead of someone having to read and type in a printed code.

## Why do we need this

Today, each wristband has a printed alphanumeric code (the `wristband_id`) that staff must manually read and type into the system during check-in. This is slow and prone to typos. The new RFID-enabled wristbands have a chip inside that can be scanned instantly by a reader. The system needs a place to store this scanned RFID tag value so that:

- Check-in is faster and more accurate (scan instead of type)
- Staff can look up any guest by scanning their wristband instead of asking for a name or reservation number
- The park can track guest location during adventures for safety purposes (e.g., a guest who has not returned from a trail by the expected time)

## What changes

One new data field -- the RFID tag identifier -- needs to be added to the check-in record in svc-check-in. The system already captures a printed wristband code; this adds the electronic chip identifier alongside it. The check-in process itself does not change. The field is optional, so adventures that do not use wristband tracking continue to work as before.

## Who is affected

- **Guests**: No visible change -- the wristband is simply scanned instead of manually entered
- **Check-in staff**: Slightly faster workflow since RFID scanning replaces manual code entry
- **Downstream systems**: Services that consume check-in events (such as trail management and guest experience) will receive the new RFID tag in the event data, enabling future contactless interactions

## Is this a big change

No. This is a small, additive change to a single service. It adds one optional field to existing schemas. Nothing that currently works will break. The main consideration is coordinating the deployment with the kiosk firmware update timeline (May 2026) and notifying downstream event consumers about the new field.

---

## Architecture Classification

**Classification: Code-Level Task (with light architecture review)**

**Reasoning:**

This ticket is a code-level task, not a full architecture engagement:

1. **Single service impact**: Only svc-check-in is modified. No new cross-service orchestration, no new service-to-service communication patterns, and no new infrastructure components are introduced.

2. **No new API endpoints**: The change adds a field to existing schemas and a query parameter to an existing endpoint. No new endpoints or services are created.

3. **No competing architectural approaches**: The implementation path is straightforward -- add a field, add validation, add a uniqueness constraint. There are no architectural trade-offs requiring a formal decision record.

4. **Existing patterns apply**: The `WristbandAssignment` sub-schema in svc-check-in already contains an `rfid_tag` field. This ticket promotes that data to the top-level `CheckIn` schema for direct lookup convenience, following the same pattern.

**Architecture touchpoints warranting light review:**

- Confirm uniqueness constraint scope (active check-ins only vs. global)
- Confirm downstream event schema compatibility (additive field safe with tolerant readers)
- Confirm RFID format regex aligns with the hardware team kiosk firmware specification

**Recommendation**: Route to the svc-check-in development team for implementation. Architecture review at the Swagger/OpenAPI spec change stage (before merge) is sufficient.
