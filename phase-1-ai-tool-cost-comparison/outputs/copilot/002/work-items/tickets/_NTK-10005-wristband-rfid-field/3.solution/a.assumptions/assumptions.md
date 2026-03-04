# NTK-10005 Assumptions

## Assumptions

### A1 Schema Backward Compatibility

The `rfid_tag` field will be added as an optional (nullable) field on the `CheckIn` schema. Existing API consumers that do not send or expect this field will continue to function without modification. This is a backward-compatible, additive schema change.

### A2 RFID Tag Format

The RFID tag value follows the pattern `^[A-F0-9]{8,16}$` as specified in the JIRA ticket acceptance criteria. The ticket report references a different example format (`RFID-A3F7B201`), but the regex constraint from the acceptance criteria takes precedence. This assumption should be validated with the hardware team.

### A3 Uniqueness Scope

The RFID tag uniqueness constraint applies per active check-in only, not globally across all historical check-in records. A wristband RFID tag may be reused across different adventure dates after the previous check-in is completed or cancelled.

### A4 Existing WristbandAssignment RFID Field

The `WristbandAssignment` schema in the current OpenAPI spec already contains an `rfid_tag` field. The ticket is requesting an additional top-level `rfid_tag` field on the `CheckIn` schema itself to support lookup/filtering without navigating the nested wristband structure. The relationship between these two fields must be clarified with the product owner.

### A5 Event Bus Schema

The check-in event published to the event bus will include the `rfid_tag` field. The event schema is assumed to mirror the `CheckIn` API response schema. Downstream consumers will need to be notified of the new optional field, but no consumer changes are required since the field is optional.

### A6 Kiosk Firmware Dependency

The kiosk firmware team is developing their RFID scanning update independently. The API schema change is a prerequisite for the firmware release but does not block any currently deployed functionality.

### A7 No PII Classification

The RFID tag identifier is a hardware identifier assigned to a wristband, not directly to a guest. It is assumed that the RFID tag alone does not constitute personally identifiable information (PII), though it could be correlated with guest identity through the check-in record. Data classification should be confirmed with the security team.
