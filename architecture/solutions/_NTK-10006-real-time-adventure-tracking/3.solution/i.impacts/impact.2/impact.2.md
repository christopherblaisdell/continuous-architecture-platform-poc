<!-- PUBLISH -->

# Impact Assessment: svc-check-in

| | |
|-----------|-------|
| **Ticket** | NTK-10006 |
| **Service** | svc-check-in |
| **Domain** | Operations |
| **Team** | NovaTrek Operations Team |
| **Change Type** | Minor Enhancement |

## Summary

svc-check-in's role as the operations orchestrator (ADR-006) is extended to include tracking session awareness. The check-in completion flow gains a new optional response field (`tracking_session_id`) and the `checkin.completed` Kafka event payload must include `wristband_nfc_id`.

## API Contract Changes

**Modified response schema — CheckIn:**

| Field | Type | Change | Nullable |
|-------|------|--------|----------|
| tracking_session_id | string (UUID) | NEW — added | Yes (null until tracking session confirmed) |

This is a backward-compatible addition. Existing consumers that do not expect this field will ignore it.

**No new endpoints.** svc-check-in does not call svc-adventure-tracking directly (ADR-014: event-driven initiation).

## Event Schema Changes

**`checkin.completed` event payload — verify or extend:**

The event must include `wristband_nfc_id` so that svc-adventure-tracking can correlate the check-in to the GPS wristband. If NTK-10005 already added this field to the event payload, no change is needed. If the event currently omits it, the schema must be extended:

| Field | Type | Status |
|-------|------|--------|
| wristband_nfc_id | string | Verify present; add if missing (backward-compatible optional field) |

## Behavioral Changes

| Scenario | Current Behavior | New Behavior |
|----------|-----------------|-------------|
| Check-in completion | Publishes `checkin.completed` event; returns CheckIn response | Same, but response includes `tracking_session_id` once confirmed by tracking service |
| Pattern 2/3 adventure departure | No tracking verification | Ops dashboard shows tracking status; staff verify active tracking before guest departs |
| svc-adventure-tracking unavailable | N/A | Check-in proceeds normally (degraded mode); ops staff alerted to use manual tracking |

## Data Model Changes

None. The `tracking_session_id` is a denormalized reference stored on the CheckIn record for convenience but is not a foreign key (svc-check-in does not own tracking data).

## Risk

Low. The only change is an optional response field and event schema verification. No new synchronous dependencies are added to svc-check-in.
