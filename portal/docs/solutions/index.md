---
title: Solution Designs
description: Architecture solution designs for NovaTrek Adventures
---

# Solution Designs

Architecture solution designs produced through the continuous architecture workflow.
Each solution maps business requirements to service changes with full capability traceability.

**5** solution designs | **2** approved

| Ticket | Solution | Status | Capabilities | Services |
|--------|----------|--------|-------------|----------|
| NTK-10001 | [Add Elevation Data to Trail Response](_NTK-10001-add-elevation-to-trail-response.md) | APPROVED | CAP-2.4 | svc-trail-management, trail-geo-data |
| NTK-10002 | [NTK-10002: Adventure Category Classification - Sol...](_NTK-10002-adventure-category-classification.md) |  | CAP-2.1, CAP-1.2 | svc-check-in, svc-adventure-catalog |
| NTK-10003 | [Unregistered Guest Self-Service Check-in](_NTK-10003-unregistered-guest-self-checkin.md) | APPROVED | CAP-2.1, CAP-1.1, CAP-1.3 | svc-check-in, svc-guest-identity, svc-scheduling-orchestrator |
| NTK-10004 | [NTK-10004: Solution Design — Guide Schedule Overwr...](_NTK-10004-guide-schedule-overwrite-bug.md) | Assumption | CAP-2.2 | svc-scheduling-orchestrator |
| NTK-10005 | [Add Wristband RFID Field to Check-In Record](_NTK-10005-wristband-rfid-field.md) | DRAFT | CAP-2.1 | svc-check-in |

## Capability Coverage

Capabilities shaped by solution designs:

| Capability | Solutions |
|-----------|----------|
| CAP-1.1 | NTK-10003 |
| CAP-1.2 | NTK-10002 |
| CAP-1.3 | NTK-10003 |
| CAP-2.1 | NTK-10002, NTK-10003, NTK-10005 |
| CAP-2.2 | NTK-10004 |
| CAP-2.4 | NTK-10001 |
