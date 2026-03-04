# NTK-10005 Architecture Decisions

## ADR NTK-10005-01 RFID Tag Field Placement on CheckIn Schema

### Status

Proposed

### Date

2026-03-04

### Context and Problem Statement

NTK-10005 requests adding an `rfid_tag` field to support RFID wristband scanning at check-in kiosks. The `WristbandAssignment` schema already contains an `rfid_tag` field, but it is nested within the `CheckIn` schema and only populated during the wristband assignment step (which occurs after initial check-in). The question is whether to add a top-level `rfid_tag` field directly on the `CheckIn` schema or rely on the existing nested field.

### Decision Drivers

- Kiosk firmware requires a direct field on the check-in record for RFID scan association
- The GET /check-ins endpoint needs to support filtering by RFID tag
- Backward compatibility with existing API consumers must be preserved
- The RFID tag may be known at check-in time (scanned at kiosk) before the formal wristband assignment step

### Considered Options

1. Add a top-level optional `rfid_tag` field to the `CheckIn` schema
2. Rely on the existing nested `wristband.rfid_tag` field and add a query parameter that searches the nested structure

### Decision Outcome

**Chosen Option**: "Option 1 — Add a top-level optional rfid_tag field to the CheckIn schema", because it enables straightforward filtering on the GET endpoint, allows RFID capture at initial check-in before wristband assignment, and aligns with the acceptance criteria which specify the field on the check-in record itself.

#### Confirmation

- The updated OpenAPI spec includes the new field with proper type, description, pattern, and nullable annotation
- The GET /check-ins endpoint includes an `rfid_tag` query parameter
- Integration tests validate that the field is optional and does not break existing consumers

### Consequences

#### Positive

- Enables RFID-based check-in lookup without navigating nested objects
- Allows RFID tag capture earlier in the check-in flow (at initial kiosk scan)
- Additive change preserves backward compatibility

#### Negative

- Introduces a potential data duplication between `CheckIn.rfid_tag` and `CheckIn.wristband.rfid_tag` that must be kept consistent
- Requires documentation clarifying the relationship between the two RFID fields

#### Neutral

- Downstream event consumers will see a new optional field in the event payload but do not need to process it immediately

### Pros and Cons of the Options

#### Option 1 Add top-level rfid_tag on CheckIn

- **Good**, because it directly supports RFID filtering on the GET endpoint
- **Good**, because it allows RFID capture at check-in creation time
- **Good**, because it is an additive, backward-compatible change
- **Bad**, because it creates two locations for RFID data (top-level and nested under wristband)

#### Option 2 Reuse nested wristband rfid_tag

- **Good**, because it avoids data duplication
- **Good**, because it uses the existing schema structure
- **Bad**, because RFID is only available after wristband assignment, not at initial check-in
- **Bad**, because filtering by a nested field is more complex and may not be supported by all API gateway tooling

### More Information

- Ticket: NTK-10005
- Current spec: svc-check-in.yaml (version 1.0.0)
- Related: WristbandAssignment schema already defines rfid_tag as a required field
