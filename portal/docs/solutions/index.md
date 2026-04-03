---
title: Solution Designs
description: Architecture solution designs for NovaTrek Adventures
---

# Solution Designs

Architecture solution designs produced through the continuous architecture workflow.
Each solution maps business requirements to service changes with full capability traceability.

**7** solution designs | **1** approved

| Ticket | Solution | Status | Capabilities | Services |
|--------|----------|--------|-------------|----------|
| [NTK-10001](../tickets/NTK-10001.md) | [Add Elevation Data to Trail Response](_NTK-10001-add-elevation-to-trail-response.md) | APPROVED | [CAP-2.4](../capabilities/index.md#cap-24-trail-operations) | [svc-trail-management](../microservices/svc-trail-management.md), trail-geo-data |
| [NTK-10002](../tickets/NTK-10002.md) | [NTK-10002: Adventure Category Classification - Sol...](_NTK-10002-adventure-category-classification.md) |  | [CAP-2.1](../capabilities/index.md#cap-21-day-of-adventure-check-in), [CAP-1.2](../capabilities/index.md#cap-12-adventure-discovery-and-browsing) | [svc-check-in](../microservices/svc-check-in.md), [svc-trip-catalog](../microservices/svc-trip-catalog.md) |
| [NTK-10004](../tickets/NTK-10004.md) | [NTK-10004: Solution Design — Guide Schedule Overwr...](_NTK-10004-guide-schedule-overwrite-bug.md) | Assumption | [CAP-2.2](../capabilities/index.md#cap-22-schedule-planning-and-optimization) | [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) |
| [NTK-10005](../tickets/NTK-10005.md) | [Add Wristband RFID Field to Check-In Record](_NTK-10005-wristband-rfid-field.md) | DRAFT | [CAP-2.1](../capabilities/index.md#cap-21-day-of-adventure-check-in) | [svc-check-in](../microservices/svc-check-in.md) |
| [NTK-10006](../tickets/NTK-10006.md) | [NTK-10006 Solution Design — Real-Time Adventure Tr...](_NTK-10006-real-time-adventure-tracking.md) |  | [CAP-3.3](../capabilities/index.md#cap-33-emergency-response-coordination), [CAP-3.2](../capabilities/index.md#cap-32-incident-reporting-and-response), [CAP-2.1](../capabilities/index.md#cap-21-day-of-adventure-check-in) | [svc-adventure-tracking](../microservices/svc-adventure-tracking.md), [svc-emergency-response](../microservices/svc-emergency-response.md), [svc-check-in](../microservices/svc-check-in.md) (+2) |
| [NTK-10008](../tickets/NTK-10008.md) | [NTK-10008 Solution Design — Guest Reviews and Rati...](_NTK-10008-guest-reviews-and-ratings.md) | Proposed | [CAP-1.7](../capabilities/index.md#cap-17-reviews-and-feedback), [CAP-1.2](../capabilities/index.md#cap-12-adventure-discovery-and-browsing) | [svc-reviews](../microservices/svc-reviews.md), [svc-reservations](../microservices/svc-reservations.md), [svc-trip-catalog](../microservices/svc-trip-catalog.md) (+1) |
| [NTK-10009](../tickets/NTK-10009.md) | [NTK-10009 Solution Design — Refund and Dispute Man...](_NTK-10009-refund-dispute-management.md) | Proposed | [CAP-5.5](../capabilities/index.md#cap-55-refund-and-dispute-management), [CAP-5.4](../capabilities/index.md#cap-54-financial-reporting-and-reconciliation) | [svc-payments](../microservices/svc-payments.md), [svc-reservations](../microservices/svc-reservations.md), [svc-notifications](../microservices/svc-notifications.md) (+1) |

## Capability Coverage

Capabilities shaped by solution designs:

| Capability | Solutions |
|-----------|----------|
| [CAP-1.2 Adventure Discovery and Browsing](../capabilities/index.md#cap-12-adventure-discovery-and-browsing) | [NTK-10002](_NTK-10002-adventure-category-classification.md), [NTK-10008](_NTK-10008-guest-reviews-and-ratings.md) |
| [CAP-1.7 Reviews and Feedback](../capabilities/index.md#cap-17-reviews-and-feedback) | [NTK-10008](_NTK-10008-guest-reviews-and-ratings.md) |
| [CAP-2.1 Day-of-Adventure Check-In](../capabilities/index.md#cap-21-day-of-adventure-check-in) | [NTK-10002](_NTK-10002-adventure-category-classification.md), [NTK-10005](_NTK-10005-wristband-rfid-field.md), [NTK-10006](_NTK-10006-real-time-adventure-tracking.md) |
| [CAP-2.2 Schedule Planning and Optimization](../capabilities/index.md#cap-22-schedule-planning-and-optimization) | [NTK-10004](_NTK-10004-guide-schedule-overwrite-bug.md) |
| [CAP-2.4 Trail Operations](../capabilities/index.md#cap-24-trail-operations) | [NTK-10001](_NTK-10001-add-elevation-to-trail-response.md) |
| [CAP-3.2 Incident Reporting and Response](../capabilities/index.md#cap-32-incident-reporting-and-response) | [NTK-10006](_NTK-10006-real-time-adventure-tracking.md) |
| [CAP-3.3 Emergency Response Coordination](../capabilities/index.md#cap-33-emergency-response-coordination) | [NTK-10006](_NTK-10006-real-time-adventure-tracking.md) |
| [CAP-5.4 Financial Reporting and Reconciliation](../capabilities/index.md#cap-54-financial-reporting-and-reconciliation) | [NTK-10009](_NTK-10009-refund-dispute-management.md) |
| [CAP-5.5 Refund and Dispute Management](../capabilities/index.md#cap-55-refund-and-dispute-management) | [NTK-10009](_NTK-10009-refund-dispute-management.md) |
