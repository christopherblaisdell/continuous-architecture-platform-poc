# NTK-10005 - Current State Investigation

## Investigation Summary

This investigation examined the svc-check-in Swagger specification, the JIRA ticket data, and the existing schema structure to determine the scope of changes required for adding RFID tag support to the check-in record.

## Data Sources

| Source | Method | Key Findings |
|--------|--------|--------------|
| JIRA (mock) | `python3 scripts/mock-jira-client.py --ticket NTK-10005` | Ticket status: New, Priority: Medium, Labels: api-enhancement, svc-check-in |
| JIRA (mock) | `python3 scripts/mock-jira-client.py --list --status "New"` | NTK-10005 confirmed as a New ticket alongside NTK-10004 |
| Ticket report | `1.requirements/NTK-10005.ticket.report.md` | Detailed requirements with two identifiers: wristband_id (existing) and rfid_tag (new) |
| Swagger spec | `corporate-services/services/svc-check-in.yaml` | WristbandAssignment already has rfid_tag; CheckIn schema lacks it |

## Current Schema Analysis

### Swagger Specification (svc-check-in.yaml v1.0.0)

The current `WristbandAssignment` schema **already includes** an `rfid_tag` field as a required property:

```yaml
WristbandAssignment:
  type: object
  required: [wristband_id, color, rfid_tag]
  properties:
    wristband_id:
      type: string
      example: "WB-2026-08-14-0342"
    color:
      type: string
      enum: [RED, BLUE, GREEN, YELLOW, ORANGE, PURPLE]
    rfid_tag:
      type: string
      example: "RFID-A3F7B201"
    assigned_at:
      type: string
      format: date-time
```

The `WristbandAssignmentRequest` also includes `rfid_tag` as a required field.

However, the top-level `CheckIn` schema does NOT have a direct `rfid_tag` property. The RFID tag is only accessible through the nested `wristband` property path: `CheckIn.wristband.rfid_tag`.

### CheckIn Schema (Current)

The `CheckIn` schema has the following relevant properties:
- `id`, `reservation_id`, `participant_guest_id`, `status` (all required)
- `wristband` -- references `WristbandAssignment` (which contains `rfid_tag`)
- `gear_verified`, `gear_items`, `waiver_verified`, `waiver_id`
- `checked_in_at`, `checked_in_by`, `completed_at`

No `rfid_tag` at the top level of `CheckIn`.

### API Endpoint Analysis

The `GET /check-ins` endpoint currently supports only one query parameter:
- `reservation_id` (required, uuid format)

There is no query parameter for looking up check-ins by `rfid_tag` or `wristband_id`.

### CheckInCreate Schema

The `CheckInCreate` schema requires: `reservation_id`, `participant_guest_id`, `checked_in_by`. It does NOT include `rfid_tag` or `wristband_id` -- those are captured during the wristband assignment step, not at check-in creation.

## Gap Analysis

| Aspect | Current State | Desired State | Gap Severity |
|--------|--------------|---------------|-------------|
| CheckIn schema - rfid_tag | Not present (only in nested WristbandAssignment) | Direct optional field on CheckIn for lookup convenience | Low |
| CheckInRecord entity | No rfidTag field (inferred from ticket report; Java source has wristbandId only) | New rfidTag column with partial uniqueness constraint | Low |
| GET /check-ins query params | Only reservation_id (required) | Add optional rfid_tag filter | Low |
| Event payload | No rfid_tag at top level of check-in events | Include rfid_tag in check-in domain event | Low |
| RFID format validation | No validation; WristbandAssignment accepts any string | Regex validation `^[A-F0-9]{8,16}$` | Low |

## Existing Pattern Observation

The `WristbandAssignment` example value `RFID-A3F7B201` includes a prefix `RFID-` that does NOT match the proposed regex `^[A-F0-9]{8,16}$`. This discrepancy should be clarified with the hardware team. Either:
- The regex should allow the `RFID-` prefix (e.g., `^(RFID-)?[A-F0-9]{8,16}$`), or
- The existing example in the Swagger spec should be updated to remove the prefix

This is flagged as an open item for architecture review.

## Conclusion

The primary work is adding an `rfid_tag` field to the `CheckIn` schema (API response and Java entity) and adding a query parameter to the list endpoint. The `WristbandAssignment` sub-schema already captures the RFID tag during wristband assignment; this ticket extends that capture to the top-level check-in record for direct lookup without traversing the wristband assignment. The change is additive, backward-compatible, and confined to a single service.
