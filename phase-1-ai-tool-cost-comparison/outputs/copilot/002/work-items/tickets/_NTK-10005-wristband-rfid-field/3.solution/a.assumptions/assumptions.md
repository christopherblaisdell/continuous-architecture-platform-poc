# NTK-10005: Assumptions

## Assumptions

### A1 - Existing WristbandAssignment Schema Already Contains rfid_tag

The current `WristbandAssignment` schema in `svc-check-in.yaml` already includes an `rfid_tag` field as a required property. The ticket report references adding `rfid_tag` to both `CheckIn` and `WristbandAssignment` schemas, but the OpenAPI spec shows `rfid_tag` already exists on `WristbandAssignment`. The actual gap is:
- The top-level `CheckIn` schema does not have a standalone `rfid_tag` field for direct query/filter access
- The `GET /api/v1/checkins` endpoint does not support filtering by `rfid_tag`

### A2 - RFID Tag Format

The RFID tag follows the pattern shown in the existing spec example: `"RFID-A3F7B201"`. The JIRA ticket mentions a regex pattern `^[A-F0-9]{8,16}$`, but the existing spec example uses a prefix format. We assume the validation pattern will be finalized during implementation but the field type is `string` with a max length of 64 characters.

### A3 - Backward Compatibility Required

The new field must be optional/nullable so that existing check-in records without RFID data continue to function. Adventures that do not use wristband tracking should not be affected.

### A4 - No New Service Dependencies

This change is scoped to `svc-check-in` only. Downstream services that consume check-in events will receive the new field but are not required to process it immediately.

### A5 - Uniqueness Constraint Scope

The RFID uniqueness constraint applies per active check-in only (not globally across all historical records). Once a check-in is completed or cancelled, the RFID tag can be reused.

### A6 - Kiosk Firmware Dependency

The kiosk firmware update that enables RFID scanning is independently managed by the hardware team. The API change needs to be available before the firmware release in May 2026 but does not depend on it.
