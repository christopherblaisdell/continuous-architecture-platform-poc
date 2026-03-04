<!-- CONFLUENCE-PUBLISH -->

# NTK-10005 - Solution Design: Add Wristband RFID Field to Check-In Record

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Date | 2026-03-04 |
| Author | Solution Architecture (AI-Assisted) |
| Status | DRAFT |
| Ticket | NTK-10005 |

## Problem Statement

NovaTrek Adventures is rolling out RFID-enabled wristbands for the 2026 summer season. Each wristband carries two identifiers: a printed alphanumeric code (`wristband_id`, already supported in the check-in system) and an RFID chip identifier (`rfid_tag`, not yet captured at the check-in record level).

The `WristbandAssignment` sub-schema in svc-check-in already has an `rfid_tag` field (required during wristband assignment). However, the top-level `CheckIn` schema does not expose `rfid_tag` directly. This means:

- Kiosks cannot record scanned RFID data at the check-in record level
- Staff cannot look up a guest's check-in by scanning their wristband (no RFID-based query parameter on `GET /check-ins`)
- Downstream event consumers do not receive `rfid_tag` at the top level of check-in events

The kiosk firmware supporting RFID scanning ships in May 2026. The API schema change must be deployed before that date.

## Architecture Classification

**Classification: Code-Level Task (with light architecture review)**

This is NOT a full architecture engagement. The reasoning:

1. **Single service impact** -- Only svc-check-in is modified. No new cross-service orchestration, communication patterns, or infrastructure components are introduced.
2. **No new API endpoints** -- The change adds a field to existing schemas and a query parameter to an existing endpoint.
3. **No competing architectural approaches** -- The implementation path is straightforward: add a field, add validation, add a uniqueness constraint.
4. **Existing patterns apply** -- The `WristbandAssignment` schema already captures `rfid_tag`. This ticket extends that capture to the top-level `CheckIn` record for direct lookup.

**Architecture review is recommended at the Swagger spec change stage** (before merge) to confirm:
- Uniqueness constraint scope (active check-ins only vs global)
- Downstream event schema compatibility (tolerant reader verification)
- RFID format alignment with hardware team specifications (existing example `RFID-A3F7B201` includes a prefix not matched by the proposed regex `^[A-F0-9]{8,16}$`)

## Solution Overview

Add an optional `rfid_tag` field to the `CheckIn` schema in svc-check-in. Add an `rfid_tag` query parameter to `GET /check-ins` for RFID-based lookup. Include `rfid_tag` in the check-in domain event for downstream consumers.

### Changes Summary

| Component | Change | Type | Severity |
|-----------|--------|------|----------|
| svc-check-in Swagger spec | Add `rfid_tag` property to `CheckIn` schema | Schema addition | Low |
| svc-check-in Swagger spec | Add `rfid_tag` query parameter to `GET /check-ins` | API enhancement | Low |
| CheckInRecord.java | Add `rfidTag` field with column constraint | Entity change | Low |
| Database | Add nullable column `rfid_tag` with partial unique index on active check-ins | DDL migration | Low |
| Event payload | Include `rfid_tag` in check-in domain event | Event schema addition | Low |
| GET /check-ins contract | Make `reservation_id` optional when `rfid_tag` is provided | Contract change | Medium |

## Impacted Components

| Component | Impact Type | Severity |
|-----------|------------|----------|
| svc-check-in | Schema addition, query parameter addition, validation logic, database migration | Low |
| Downstream event consumers (svc-guest-experience, svc-trail-management) | New optional field in event payload (informational; no action required) | Informational |

## Changes Required

### 1. Swagger Specification Update

Add to the `CheckIn` schema:

```yaml
rfid_tag:
  type: string
  maxLength: 64
  pattern: '^[A-F0-9]{8,16}$'
  nullable: true
  description: >-
    RFID chip identifier from the guest wristband. Populated when a wristband
    is assigned during the check-in process. Null for adventures without
    wristband tracking or before wristband assignment.
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
@Column(name = "rfid_tag", length = 64)
private String rfidTag;
```

### 3. Database Migration

```sql
ALTER TABLE check_in_records ADD COLUMN rfid_tag VARCHAR(64);

CREATE UNIQUE INDEX idx_rfid_tag_active 
ON check_in_records (rfid_tag) 
WHERE rfid_tag IS NOT NULL 
AND status NOT IN ('COMPLETED', 'FAILED', 'CANCELLED');
```

### 4. Event Payload Update

Include `rfid_tag` as a top-level field in the check-in domain event. Downstream consumers using tolerant reader patterns will ignore the new field until they are ready to use it.

## Validation Rules

| Rule | Value |
|------|-------|
| Format | Hexadecimal string matching regex `^[A-F0-9]{8,16}$` |
| Max length | 64 characters |
| Nullable | Yes |
| Uniqueness | Unique across active check-ins (status not in COMPLETED, FAILED, CANCELLED) |

## Open Items

| ID | Item | Owner | Status |
|----|------|-------|--------|
| OI-1 | Confirm RFID format with hardware team. Existing `WristbandAssignment` example uses `RFID-A3F7B201` (with prefix) but proposed regex `^[A-F0-9]{8,16}$` does not allow prefixes. | Hardware Team | Open |
| OI-2 | Confirm whether `reservation_id` should become optional on `GET /check-ins` when `rfid_tag` is provided. | API Review | Open |
| OI-3 | Verify downstream event consumers use tolerant reader patterns. | Integration Team | Open |

## Deployment Notes

- Database migration must run before the application deployment
- The schema change is additive and backward-compatible -- no consumer changes required
- Coordinate deployment with kiosk firmware update timeline (May 2026)
- Notify downstream event consumers of the new field before deployment, even though no action is required from them

## Related Artifacts

- [Ticket Report](1.requirements/NTK-10005.ticket.report.md)
- [Simple Explanation](2.analysis/simple.explanation.md)
- [Assumptions](3.solution/a.assumptions/assumptions.md)
- [Current State Investigation](3.solution/c.current.state/investigations.md)
- [Decisions](3.solution/d.decisions/decisions.md)
- [Guidance](3.solution/g.guidance/guidance.md)
- [Impacts](3.solution/i.impacts/impacts.md)
- [User Stories](3.solution/s.user.stories/user-stories.md)
