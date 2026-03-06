<!-- CONFLUENCE-PUBLISH -->

# NTK-10005 - Solution Design: Add Wristband RFID Field to Check-In Record

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Date | 2026-03-03 |
| Author | Solution Architecture (AI-Assisted) |
| Status | DRAFT |
| Ticket | NTK-10005 |

## Problem Statement

NovaTrek Adventures is rolling out RFID-enabled wristbands for the 2026 summer season. Each wristband carries two identifiers: a printed alphanumeric code (`wristband_id`, already supported in the system) and an RFID chip identifier (`rfid_tag`, not yet captured at the check-in record level).

The `WristbandAssignment` sub-schema in svc-check-in already captures `rfid_tag` during the wristband assignment step. However, the top-level `CheckIn` schema and the `CheckInRecord` Java entity do not have a direct `rfid_tag` field. The `GET /check-ins` endpoint also lacks an RFID-based query parameter.

Without promoting the `rfid_tag` to the top-level check-in record:

- Kiosks cannot record scanned RFID data at the check-in record level
- Staff cannot look up a guest check-in by scanning their wristband
- Downstream systems receiving check-in events do not get the RFID tag at the top level

## Architecture Classification

**Classification: Code-Level Task (with light architecture review)**

This is NOT a full architecture engagement. The reasoning:

1. **Single service impact**: Only svc-check-in is modified. No new cross-service orchestration, communication patterns, or infrastructure components are introduced.
2. **No new API endpoints**: The change adds a field to existing schemas and a query parameter to an existing endpoint.
3. **No competing architectural approaches**: The change is straightforward -- add a field, add validation, add a uniqueness constraint.
4. **Existing patterns apply**: The `WristbandAssignment` schema already captures `rfid_tag`. This ticket extends that capture to the top-level `CheckIn` record for direct lookup.

**Architecture review is recommended at the Swagger spec change stage** (before merge) to confirm:

- Uniqueness constraint scope (active check-ins only vs. global)
- Downstream event schema compatibility
- RFID format alignment with hardware team specifications

## Solution Overview

Add an optional `rfid_tag` field to the `CheckIn` schema in svc-check-in, the `CheckInRecord` JPA entity, and the check-in event payload. Add an `rfid_tag` query parameter to `GET /check-ins` for RFID-based lookup.

### Changes Summary

| Component | Change | Type |
|-----------|--------|------|
| svc-check-in Swagger spec | Add `rfid_tag` property to `CheckIn` schema | Schema addition |
| svc-check-in Swagger spec | Add `rfid_tag` query parameter to `GET /check-ins` | API enhancement |
| CheckInRecord.java | Add `rfidTag` field with column constraint | Entity change |
| Database | Add partial unique index on `rfid_tag` for active check-ins | DDL migration |
| Event payload | Include `rfid_tag` in check-in domain event | Event schema addition |

## Impacted Components

| Component | Impact Type | Severity |
|-----------|------------|----------|
| svc-check-in | Schema addition, query parameter addition, validation logic | Low |
| Downstream event consumers | New optional field in event payload (tolerant reader pattern) | Informational |

## Changes Required

### 1. Swagger Specification Update

Add to the `CheckIn` schema:

```yaml
rfid_tag:
  type: string
  maxLength: 64
  pattern: '^[A-F0-9]{8,16}$'
  nullable: true
  description: RFID chip identifier from the guest wristband
  example: "A3F7B20145CC"
```

Add to `GET /check-ins` parameters:

```yaml
- name: rfid_tag
  in: query
  required: false
  schema:
    type: string
    pattern: '^[A-F0-9]{8,16}$'
  description: Filter check-ins by RFID wristband tag
```

### 2. JPA Entity Update

Add to `CheckInRecord.java`:

```java
@Column(length = 64)
private String rfidTag;
```

### 3. Database Migration

```sql
ALTER TABLE check_in_records ADD COLUMN rfid_tag VARCHAR(64);

CREATE UNIQUE INDEX idx_rfid_tag_active 
ON check_in_records (rfid_tag) 
WHERE status NOT IN ('COMPLETED', 'FAILED');
```

### 4. Event Payload Update

Include `rfid_tag` as a top-level field in the check-in domain event. Downstream consumers using tolerant reader patterns will ignore the new field until they are ready to use it.

## Validation Rules

| Rule | Detail |
|------|--------|
| Format | Hexadecimal string matching regex `^[A-F0-9]{8,16}$` |
| Max length | 64 characters |
| Nullable | Yes |
| Uniqueness | Unique across active check-ins (status not in COMPLETED, FAILED) |

## Deployment Notes

- Database migration must run before the application deployment
- The schema change is additive and backward-compatible -- no consumer changes required
- Coordinate deployment with kiosk firmware update timeline (May 2026)
- Notify downstream event consumers of the new field in advance, even though no action is required from them

## Related Artifacts

- [Ticket Report](1.requirements/NTK-10005.ticket.report.md)
- [Simple Explanation](2.analysis/simple.explanation.md)
- [Assumptions](3.solution/a.assumptions/assumptions.md)
- [Current State Investigation](3.solution/c.current.state/investigations.md)
- [Decisions](3.solution/d.decisions/decisions.md)
- [Guidance](3.solution/g.guidance/guidance.md)
- [Impacts](3.solution/i.impacts/impacts.md)
- [User Stories](3.solution/s.user.stories/user-stories.md)
