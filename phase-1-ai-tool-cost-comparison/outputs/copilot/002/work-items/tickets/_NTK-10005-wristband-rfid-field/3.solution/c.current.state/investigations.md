# NTK-10005 Current State Investigations

## Current State of RFID in svc-check-in

### OpenAPI Spec Analysis

The current `svc-check-in.yaml` (version 1.0.0) was reviewed. Key findings:

1. **WristbandAssignment schema** (line ~265 in svc-check-in.yaml): Already contains an `rfid_tag` field as a required property alongside `wristband_id` and `color`. This field is used during the wristband assignment step of check-in.

2. **WristbandAssignmentRequest schema** (line ~280): Also contains `rfid_tag` as a required field in the assignment request payload.

3. **CheckIn schema** (line ~195): Does NOT have a top-level `rfid_tag` field. The RFID tag is only accessible through the nested `wristband` property (which references `WristbandAssignment`).

4. **GET /check-ins endpoint** (line ~52): Currently supports filtering by `reservation_id` only. There is no `rfid_tag` query parameter for lookup by RFID tag.

5. **POST /check-ins endpoint** (line ~22): The `CheckInCreate` schema does not include `rfid_tag`. RFID tags are only captured during the subsequent wristband assignment step.

### Identified Gaps

| Gap | Description |
|-----|-------------|
| No top-level RFID field on CheckIn | RFID tag is nested under `wristband.rfid_tag`, making direct filtering impractical |
| No RFID query parameter on GET | Cannot look up check-ins by RFID tag scan |
| RFID captured late in flow | RFID tag is only recorded during wristband assignment, not at initial check-in |
| No validation pattern | The existing `rfid_tag` field in `WristbandAssignment` has no regex pattern constraint |
| No uniqueness constraint | No mechanism to prevent duplicate RFID tags across active check-ins |

### Event Bus Impact

The check-in service publishes events to the event bus. The `CheckIn` schema is the basis for these events. Adding a top-level `rfid_tag` field to `CheckIn` would automatically propagate the field to event consumers. This is an additive change and should not break existing consumers.

### Downstream Service Dependencies

Based on the spec description, the following services consume check-in data:
- **svc-reservations**: Referenced for booking validation during check-in
- **svc-safety-compliance**: Referenced for waiver validation
- **svc-gear-inventory**: Referenced for gear assignment
- **svc-guest-profiles**: Referenced for participant identity

These services are consumers of check-in data but would only be affected if they process the event payload fields explicitly. Since `rfid_tag` is additive and optional, no breaking changes are expected.
