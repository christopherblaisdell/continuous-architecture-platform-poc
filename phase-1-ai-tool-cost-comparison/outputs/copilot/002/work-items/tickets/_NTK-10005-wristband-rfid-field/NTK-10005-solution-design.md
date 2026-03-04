# NTK-10005 Solution Design

**Ticket**: NTK-10005 — Add Wristband RFID Field to Check-In Record
**Version**: v1.0
**Date**: 2026-03-04
**Status**: Proposed

## 1 Problem Statement

NovaTrek is rolling out RFID-enabled wristbands for the 2026 summer season. Check-in kiosks will be equipped with RFID readers to scan wristbands automatically, replacing manual entry. The current svc-check-in API does not have a top-level RFID field on the check-in record, and the GET endpoint does not support filtering by RFID tag. This prevents kiosks from associating scanned RFID data with check-in records and prevents staff from looking up guests by wristband scan.

## 2 Architecture Classification

### Classification: Architecturally Relevant — Minor Schema Enhancement

This ticket is **architecturally relevant** but represents a **low-complexity, additive change**. The architectural relevance stems from:

- **API contract modification**: Adding a new field to the `CheckIn` schema and a new query parameter to the GET endpoint changes the published API contract
- **Event schema impact**: The check-in event published to the event bus will include the new field, affecting all downstream consumers
- **Data model change**: A new column with a uniqueness constraint is added to the check-in data store

However, the change is **low risk** because:

- All modifications are additive and optional (nullable field, optional query parameter)
- No existing fields are modified or removed
- No cross-service data ownership boundaries are violated — svc-check-in owns the check-in record
- No new service dependencies are introduced

### Recommendation

This ticket can proceed through normal development with architecture review of the OpenAPI spec change. A full solution design cycle is not required, but the schema change should be reviewed to ensure consistency between the top-level `rfid_tag` and the existing nested `wristband.rfid_tag` field.

## 3 Current State

The `WristbandAssignment` schema already defines an `rfid_tag` field that is populated during the wristband assignment step of check-in. However:

- The RFID tag is only available after wristband assignment (a later step in the check-in flow)
- The `CheckIn` schema does not expose `rfid_tag` at the top level
- The `GET /check-ins` endpoint only supports filtering by `reservation_id`
- The `CheckInCreate` schema does not accept `rfid_tag`

See `3.solution/c.current.state/investigations.md` for detailed analysis.

## 4 Proposed Solution

### 4.1 Schema Changes

Add an optional `rfid_tag` field to:
- `CheckIn` schema (top-level, nullable)
- `CheckInCreate` schema (optional input)

Add an `rfid_tag` query parameter to:
- `GET /check-ins` endpoint

### 4.2 Validation

- Regex pattern: `^[A-F0-9]{8,16}$`
- Maximum length: 64 characters
- Uniqueness: Enforced per active check-in (status not in COMPLETE, CANCELLED)

### 4.3 Data Consistency

When a wristband is assigned via `POST /check-ins/{id}/wristband-assignment`:
- If `CheckIn.rfid_tag` is already set, validate it matches `WristbandAssignmentRequest.rfid_tag`
- If `CheckIn.rfid_tag` is null, populate it from the assignment request

### 4.4 Event Bus

The check-in event payload will include the top-level `rfid_tag` field. This is an additive change to the event schema.

## 5 Affected Services

| Service | Impact | Severity |
|---------|--------|----------|
| svc-check-in | Schema change, new query parameter, validation logic | Medium |
| Event consumers | New optional field in event payload | Low |
| Kiosk firmware | Will send rfid_tag in requests (external dependency) | Low |

## 6 Decisions

See `3.solution/d.decisions/decisions.md` for the full MADR decision record on RFID field placement.

## 7 Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Data inconsistency between top-level and nested RFID fields | Medium | Medium | Enforce consistency validation during wristband assignment |
| RFID format mismatch with hardware | Low | Medium | Validate regex pattern with hardware team before implementation |
| Timeline pressure from May firmware deadline | Low | High | Prioritize this change in the next sprint |

## 8 Quality Attributes (ISO 25010)

| Attribute | Assessment |
|-----------|------------|
| Functional Suitability | Meets stated requirements for RFID capture and lookup |
| Compatibility | Backward-compatible additive change; no breaking changes |
| Reliability | Uniqueness constraint prevents duplicate RFID assignment conflicts |
| Maintainability | Two RFID fields (top-level and nested) introduce minor maintenance overhead |
| Security | RFID tag is a hardware identifier, not PII; data classification should be confirmed |
