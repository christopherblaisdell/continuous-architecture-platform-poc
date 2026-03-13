---
title: Solution Designs
description: Architecture solution designs for NovaTrek Adventures
---

# Solution Designs

Architecture solution designs produced through the continuous architecture workflow.
Each solution maps business requirements to service changes with full capability traceability.

**8** solution designs | **2** approved

| Ticket | Solution | Status | Capabilities | Services |
|--------|----------|--------|-------------|----------|
| NTK-10001 | [Add Elevation Data to Trail Response](_NTK-10001-add-elevation-to-trail-response.md) | APPROVED | CAP-2.4 | svc-trail-management, trail-geo-data |
| NTK-10002 | [NTK-10002: Adventure Category Classification - Sol...](_NTK-10002-adventure-category-classification.md) |  | CAP-2.1, CAP-1.2 | svc-check-in, svc-adventure-catalog |
| NTK-10003 | [Unregistered Guest Self-Service Check-in](_NTK-10003-unregistered-guest-self-checkin.md) | APPROVED | CAP-2.1, CAP-1.1, CAP-1.3 | svc-check-in, svc-guest-identity, svc-scheduling-orchestrator |
| NTK-10004 | [NTK-10004: Solution Design — Guide Schedule Overwr...](_NTK-10004-guide-schedule-overwrite-bug.md) | Assumption | CAP-2.2 | svc-scheduling-orchestrator |
| NTK-10005 | [Add Wristband RFID Field to Check-In Record](_NTK-10005-wristband-rfid-field.md) | DRAFT | CAP-2.1 | svc-check-in |
| NTK-10006 | [NTK-10006 Solution Design — Real-Time Adventure Tr...](_NTK-10006-real-time-adventure-tracking.md) | Proposed | CAP-3.3, CAP-3.2, CAP-2.1 | svc-adventure-tracking, svc-emergency-response, svc-check-in (+2) |
| NTK-10008 | [NTK-10008 Solution Design — Guest Reviews and Rati...](_NTK-10008-guest-reviews-and-ratings.md) | Proposed | CAP-1.7, CAP-1.2 | svc-reviews, svc-reservations, svc-trip-catalog (+1) |
| NTK-10009 | [NTK-10009 Solution Design — Refund and Dispute Man...](_NTK-10009-refund-dispute-management.md) | Proposed | CAP-5.5, CAP-5.4 | svc-payments, svc-reservations, svc-notifications (+1) |

## Capability Coverage

Capabilities shaped by solution designs:

| Capability | Solutions |
|-----------|----------|
| CAP-1.1 | NTK-10003 |
| CAP-1.2 | NTK-10002, NTK-10008 |
| CAP-1.3 | NTK-10003 |
| CAP-1.7 | NTK-10008 |
| CAP-2.1 | NTK-10002, NTK-10003, NTK-10005, NTK-10006 |
| CAP-2.2 | NTK-10004 |
| CAP-2.4 | NTK-10001 |
| CAP-3.2 | NTK-10006 |
| CAP-3.3 | NTK-10006 |
| CAP-5.4 | NTK-10009 |
| CAP-5.5 | NTK-10009 |
