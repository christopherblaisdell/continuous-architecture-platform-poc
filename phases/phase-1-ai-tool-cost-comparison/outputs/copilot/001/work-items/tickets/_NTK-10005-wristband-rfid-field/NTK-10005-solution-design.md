# NTK-10005: Add Wristband RFID Field to Check-In Record - Solution Design

## Metadata

| Field | Value |
|-------|-------|
| Ticket | NTK-10005 |
| Title | Add Wristband RFID Field to Check-In Record |
| Status | Draft |
| Author | Solution Architecture |
| Date | 2026-03-03 |
| Classification | Code-Level Task (Not Architecturally Significant) |

## Problem Statement

NovaTrek is deploying RFID-enabled wristbands for the 2026 summer season. Each wristband carries both a printed visual code (`wristband_id`) and an RFID chip identifier (`rfid_tag`). The current check-in system captures the visual code but has no mechanism to:

1. Store the RFID tag at the top level of the check-in record for direct access
2. Look up check-in records by RFID tag (required for kiosk scan-to-lookup workflows)
3. Capture the RFID tag at initial check-in (before the formal wristband assignment step)

The `WristbandAssignment` sub-schema already includes `rfid_tag`, but this is only populated during the wristband assignment step -- too late for kiosk scenarios where RFID scanning initiates the check-in.

## Architectural Classification

**This ticket is classified as a code-level task, not an architecturally significant change.**

Rationale:
- The change is an additive, backward-compatible schema extension
- No new service-to-service interactions are introduced
- No changes to infrastructure, deployment topology, or quality attributes
- The pattern (optional field on an existing schema) is well-established in the codebase
- No Architecture Decision Record is required

## Proposed Solution

### Schema Changes

Add an optional `rfid_tag` field to the `CheckIn` schema:

```yaml
rfid_tag:
  type: string
  maxLength: 64
  nullable: true
  description: RFID chip identifier scanned from the guest wristband
  example: "RFID-A3F7B201"
```

Add `rfid_tag` to the `CheckInCreate` request schema as an optional field to support RFID capture at check-in initiation.

### API Changes

| Endpoint | Change |
|----------|--------|
| `POST /check-ins` | Accept optional `rfid_tag` in request body |
| `GET /check-ins` | Add optional `rfid_tag` query parameter for lookup |
| `GET /check-ins/{id}` | No change (inherits from updated CheckIn schema) |

### Data Model Changes

- Add nullable `rfid_tag` column (`VARCHAR(64)`) to `check_ins` table
- Create conditional unique index on `rfid_tag` for active check-ins only
- Standard online migration with no downtime

### Event Schema

The check-in event published to the event bus will automatically include `rfid_tag` when present, as the event payload is derived from the `CheckIn` schema.

## Service Interactions

No new service interactions are introduced. The change is scoped to `svc-check-in`.

```
[Kiosk] --RFID scan--> [svc-check-in] --event (now includes rfid_tag)--> [Event Bus]
                                                                              |
                                                                    +--------+--------+
                                                                    |                 |
                                                          [svc-guest-experience] [svc-trail-management]
                                                          (no changes needed)    (no changes needed)
```

## Validation Rules

- Format: Configurable regex (initial: `^[A-F0-9]{8,16}$` or agreed prefix format)
- Length: Maximum 64 characters
- Uniqueness: Reject duplicates among active check-ins (status not in COMPLETE, CANCELLED)
- Nullability: Field is optional -- null/absent values are valid

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| RFID format mismatch with hardware | Low | Medium | Coordinate with hardware team on format; use configurable regex |
| Downstream services fail on new field | Very Low | Low | Field is additive; standard JSON deserialization ignores unknown fields |
| Uniqueness constraint causes check-in failures | Low | Medium | Clear error messages; staff override mechanism if needed |

## Timeline

| Milestone | Target Date |
|-----------|------------|
| Schema and API implementation | April 2026 |
| Integration testing with kiosk firmware | May 2026 |
| Production deployment | Before May 2026 kiosk firmware release |

## References

- Ticket report: `1.requirements/NTK-10005.ticket.report.md`
- Service spec: `corporate-services/services/svc-check-in.yaml`
- Analysis: `2.analysis/simple.explanation.md`
