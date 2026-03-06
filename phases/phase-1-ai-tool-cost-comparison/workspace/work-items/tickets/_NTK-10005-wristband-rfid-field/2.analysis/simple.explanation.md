# NTK-10005 - Simple Explanation

## What is this about?

NovaTrek Adventures is rolling out new wristbands that have a small electronic chip inside them — similar to how a hotel key card works, but worn on your wrist. When a guest checks in for an adventure, a staff member or kiosk scans the wristband, and the system remembers which wristband belongs to which guest.

## Why do we need this?

Right now, each wristband has a printed code on it that staff have to read and type in manually. The new wristbands have an RFID chip (like a contactless credit card) that can be scanned instantly by a reader. This is faster, avoids typos, and also allows the park to track where guests are during an adventure for safety purposes — for example, if a guest hasn't returned from a trail by the expected time, park staff can check their last known location.

## What changes?

We need to add one new field — the RFID tag number — to the check-in system. When a guest checks in, the kiosk or staff terminal scans the wristband and records both the old printed code (which already works) and the new RFID tag. Everything else about the check-in process stays the same.

## Who is affected?

- **Guests**: No change to their experience — the wristband just gets scanned instead of typed
- **Staff**: Check-in is slightly faster since RFID scanning replaces manual entry
- **Downstream systems**: Services that receive check-in data (like guest experience tracking and trail management) will now get the RFID tag too, enabling contactless interactions throughout the day

## Is this a big change?

No. This is a small, additive schema change to a single service (svc-check-in). It adds an optional field — nothing existing breaks. The main consideration is making sure downstream services that consume check-in events are aware of the new field, even though they don't need to do anything immediately.

---

## Architecture Classification

**Classification: Code-Level Task (with light architecture review)**

**Reasoning:**

This ticket is predominantly a **code-level task**, not a full architecture engagement:

1. **Single service impact**: Only svc-check-in is modified. No new cross-service orchestration, no new service-to-service communication patterns, no new Kafka events or topics — just an additive field on an existing schema.

2. **No new API endpoints**: The change adds a field to existing schemas and a query parameter filter to an existing endpoint. No new endpoints, services, or infrastructure components.

3. **No architectural decisions required**: There are no competing architectural approaches to evaluate. The change is straightforward: add a field, add validation, add a uniqueness constraint.

4. **Existing patterns apply**: The svc-check-in service already has a `WristbandAssignment` schema with an `rfid_tag` field. The ticket is asking for the RFID tag to also appear on the `CheckIn` record itself for direct lookup. This follows existing patterns.

**Architecture touchpoints that warrant light review:**
- Confirm the uniqueness constraint scope (per active check-in vs global) — this affects index design
- Confirm downstream event schema compatibility — additive fields should be safe, but verify consumers use tolerant readers
- Confirm the RFID format matches what the hardware team's kiosk firmware will send

**Recommendation**: Route to the svc-check-in development team with architecture review at the Swagger spec change stage (before merge). No full solution design is needed.
