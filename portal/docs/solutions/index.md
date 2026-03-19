---
title: Solution Designs
description: Architecture solution designs for NovaTrek Adventures
---

# Solution Designs

Architecture solution designs produced through the continuous architecture workflow.
Each solution maps business requirements to service changes with full capability traceability.

**6** solution designs | **1** approved

| Ticket | Solution | Status | Capabilities | Services |
|--------|----------|--------|-------------|----------|
| NTK-10001 | [Add Elevation Data to Trail Response](_NTK-10001-add-elevation-to-trail-response.md) | APPROVED | CAP-2.4 | svc-trail-management, trail-geo-data |
| NTK-10002 | [NTK-10002: Adventure Category Classification - Sol...](_NTK-10002-adventure-category-classification.md) |  | CAP-2.1, CAP-1.2 | svc-check-in, svc-adventure-catalog |
| NTK-10004 | [NTK-10004: Solution Design — Guide Schedule Overwr...](_NTK-10004-guide-schedule-overwrite-bug.md) | Assumption | CAP-2.2 | svc-scheduling-orchestrator |
| NTK-10005 | [Add Wristband RFID Field to Check-In Record](_NTK-10005-wristband-rfid-field.md) | DRAFT | CAP-2.1 | svc-check-in |
| NTK-10008 | [NTK-10008 Solution Design — Guest Reviews and Rati...](_NTK-10008-guest-reviews-and-ratings.md) | Proposed | CAP-1.7, CAP-1.2 | svc-reviews, svc-reservations, svc-trip-catalog (+1) |
| NTK-10009 | [NTK-10009 Solution Design — Refund and Dispute Man...](_NTK-10009-refund-dispute-management.md) | Proposed | CAP-5.5, CAP-5.4 | svc-payments, svc-reservations, svc-notifications (+1) |

## Capability Coverage

Capabilities shaped by solution designs:

| Capability | Solutions |
|-----------|----------
| [CAP-1.2 Adventure Discovery and Browsing](../capabilities/index.md#cap-12-adventure-discovery-and-browsing) | [NTK-10002](_NTK-10002-adventure-category-classification.md), [NTK-10008](_NTK-10008-guest-reviews-and-ratings.md) |
| [CAP-1.7 Reviews and Feedback](../capabilities/index.md#cap-17-reviews-and-feedback) | [NTK-10008](_NTK-10008-guest-reviews-and-ratings.md) |
| [CAP-2.1 Day-of-Adventure Check-In](../capabilities/index.md#cap-21-day-of-adventure-check-in) | [NTK-10002](_NTK-10002-adventure-category-classification.md), [NTK-10005](_NTK-10005-wristband-rfid-field.md) |
| [CAP-2.2 Schedule Planning and Optimization](../capabilities/index.md#cap-22-schedule-planning-and-optimization) | [NTK-10004](_NTK-10004-guide-schedule-overwrite-bug.md) |
| [CAP-2.4 Trail Operations](../capabilities/index.md#cap-24-trail-operations) | [NTK-10001](_NTK-10001-add-elevation-to-trail-response.md) |
| [CAP-5.4 Financial Reporting and Reconciliation](../capabilities/index.md#cap-54-financial-reporting-and-reconciliation) | [NTK-10009](_NTK-10009-refund-dispute-management.md) |
| [CAP-5.5 Refund and Dispute Management](../capabilities/index.md#cap-55-refund-and-dispute-management) | [NTK-10009](_NTK-10009-refund-dispute-management.md) |
