# NTK-10005: Current State Investigation

## Service Analysis - svc-check-in

### Current Schema State

**CheckIn schema** (`svc-check-in.yaml`):
- Contains a `wristband` field that references the `WristbandAssignment` sub-object
- The `WristbandAssignment` schema already includes `rfid_tag` as a required field alongside `wristband_id` and `color`
- There is no top-level `rfid_tag` field on `CheckIn` for direct access or query filtering

**WristbandAssignment schema**:
- `wristband_id` (string) - visual alphanumeric code printed on the band
- `color` (enum) - color-coded for trip group identification
- `rfid_tag` (string) - RFID chip identifier (already present in the spec)
- `assigned_at` (datetime)

**WristbandAssignmentRequest schema**:
- Also already includes `rfid_tag` as a required field in the request body

### Current API Endpoints

| Endpoint | Method | RFID Support |
|----------|--------|-------------|
| `/check-ins` | POST | RFID captured via wristband assignment sub-flow, not at check-in creation |
| `/check-ins` | GET | Filters by `reservation_id` only -- no `rfid_tag` filter |
| `/check-ins/{id}` | GET | Returns `wristband.rfid_tag` if wristband is assigned |
| `/check-ins/{id}/wristband-assignment` | POST | Accepts `rfid_tag` in request body |

### Gap Analysis

1. **Missing query filter**: `GET /check-ins` cannot filter by `rfid_tag`. This is the primary gap for kiosk lookup scenarios.
2. **No standalone RFID field on CheckIn**: The RFID tag is nested inside `wristband` which is only populated after the wristband assignment step. For scenarios where the RFID scan happens at initial check-in, there is no field to capture it early.
3. **Event schema**: The check-in event published to the event bus inherits from the `CheckIn` schema. Adding a top-level field would automatically propagate to downstream consumers.

### Downstream Service Impact

Services that consume check-in events:
- `svc-guest-experience` - would receive RFID data for contactless interactions
- `svc-trail-management` - would receive RFID data for on-trail tracking
- These services would need to be aware of the new field but are not required to act on it immediately (additive, backward-compatible change)
