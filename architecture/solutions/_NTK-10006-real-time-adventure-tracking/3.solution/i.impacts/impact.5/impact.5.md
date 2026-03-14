<!-- PUBLISH -->
# Impact Assessment 5: svc-check-in (UNCHANGED)

| Field | Value |
|-------|-------|
| Service | svc-check-in |
| Domain | Operations |
| Change Type | None — existing event contract is sufficient |
| Impact Level | NONE |
| Owner | NovaTrek Operations Team |

## Overview

svc-check-in requires zero code changes for NTK-10006. The `checkin.completed` event already carries all fields needed to activate tracking:

| Event Field | Source | Used By svc-adventure-tracking |
|-------------|--------|-------------------------------|
| check_in_id | svc-check-in | Reference only |
| reservation_id | svc-check-in | Link to reservation lifecycle |
| guest_id | svc-check-in | Guest identity for tracking session |
| trip_id | svc-check-in | Trip reference for geofence lookup |
| adventure_category | svc-check-in | Determines tracking frequency tier |
| check_in_pattern | svc-check-in | Maps to tracking frequency (1=60s, 2=30s, 3=10s) |
| rfid_tag | svc-check-in (NTK-10005) | Physical wristband identity for GPS correlation |

The NTK-10005 solution (wristband RFID field) specifically added `rfid_tag` to the check-in record and the checkin.completed event "for adventure tracking" — this was the deliberate precursor to NTK-10006.

## Why No Changes

ADR-013 documents the decision to use event-driven tracking activation. svc-adventure-tracking subscribes to the existing event — the producer (svc-check-in) does not need to know about the new consumer. This is the correct application of loose coupling via events across domain boundaries.
