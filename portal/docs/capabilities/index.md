---
title: Business Capabilities
description: NovaTrek Adventures business capability map with solution traceability
---

# Business Capability Map

The capability map defines WHAT NovaTrek Adventures does as a business,
independent of HOW services implement it. L1 domains group related capabilities.
L2 capabilities map to services. L3 capabilities emerge from solution designs.

## Coverage Summary

| Status | Count | Percentage |
|--------|-------|-----------|
| Implemented | 27 | 79.4% |
| Partial | 3 | 8.8% |
| Not Implemented | 4 | 11.8% |
| **Total L2 Capabilities** | **34** | |

## Capability Health Dashboard

Health metrics derived from the capability changelog. Staleness measures
days since last solution touched a capability. Churn measures how frequently
a capability is modified by solutions.

### Health Summary

| Metric | Value |
|--------|-------|
| Active (last 90 days) | 7 |
| Aging (90-180 days) | 0 |
| Stale (>180 days) | 2 |
| Untouched (no solutions) | 25 |
| High churn (4+ solutions) | 0 |
| Emergent L3 capabilities | 24 |
| Architecture decisions | 21 |

### Per-Capability Health

| Capability | Status | Solutions | Last Touched | Staleness | Churn | L3s | ADRs |
|-----------|--------|-----------|-------------|-----------|-------|-----|------|
| [CAP-1.1 Guest Identity and Profile Management](#cap-11-guest-identity-and-profile-management) | IMPLEMENTED | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-1.2 Adventure Discovery and Browsing](#cap-12-adventure-discovery-and-browsing) | IMPLEMENTED | 2 | 2026-03-06 | ACTIVE | MODERATE | 2 | 5 |
| [CAP-1.3 Reservation Management](#cap-13-reservation-management) | IMPLEMENTED | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-1.4 Loyalty and Rewards](#cap-14-loyalty-and-rewards) | IMPLEMENTED | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-1.5 Guest Communications](#cap-15-guest-communications) | IMPLEMENTED | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-1.6 Trip Media and Memories](#cap-16-trip-media-and-memories) | IMPLEMENTED | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-1.7 Reviews and Feedback](#cap-17-reviews-and-feedback) | IMPLEMENTED | 1 | 2026-03-06 | ACTIVE | LOW | 5 | 3 |
| [CAP-1.8 Personalized Recommendations](#cap-18-personalized-recommendations) | NOT IMPLEMENTED | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-2.1 Day-of-Adventure Check-In](#cap-21-day-of-adventure-check-in) | IMPLEMENTED | 3 | 2026-03-20 | ACTIVE | MODERATE | 5 | 3 |
| [CAP-2.2 Schedule Planning and Optimization](#cap-22-schedule-planning-and-optimization) | IMPLEMENTED | 1 | 2025-02-05 | STALE | LOW | 2 | 2 |
| [CAP-2.3 Guide Assignment and Management](#cap-23-guide-assignment-and-management) | IMPLEMENTED | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-2.4 Trail Operations](#cap-24-trail-operations) | IMPLEMENTED | 1 | 2025-02-01 | STALE | LOW | 1 | 0 |
| [CAP-2.5 Transport Coordination](#cap-25-transport-coordination) | IMPLEMENTED | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-3.1 Waiver and Compliance Management](#cap-31-waiver-and-compliance-management) | IMPLEMENTED | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-3.2 Incident Reporting and Response](#cap-32-incident-reporting-and-response) | IMPLEMENTED | 1 | 2026-03-20 | ACTIVE | LOW | 2 | 1 |
| [CAP-3.3 Emergency Response Coordination](#cap-33-emergency-response-coordination) | IMPLEMENTED | 1 | 2026-03-20 | ACTIVE | LOW | 2 | 1 |
| [CAP-3.4 Wildlife and Environmental Monitoring](#cap-34-wildlife-and-environmental-monitoring) | IMPLEMENTED | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-3.5 Weather Monitoring and Alerting](#cap-35-weather-monitoring-and-alerting) | IMPLEMENTED | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-4.1 Gear Inventory and Tracking](#cap-41-gear-inventory-and-tracking) | IMPLEMENTED | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-4.2 Procurement and Vendor Management](#cap-42-procurement-and-vendor-management) | IMPLEMENTED | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-4.3 Location and Capacity Management](#cap-43-location-and-capacity-management) | IMPLEMENTED | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-4.4 Vehicle Fleet Management](#cap-44-vehicle-fleet-management) | IMPLEMENTED | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-4.5 Facility and Venue Management](#cap-45-facility-and-venue-management) | NOT IMPLEMENTED | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-5.1 Payment Processing](#cap-51-payment-processing) | IMPLEMENTED | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-5.2 Trip Pricing and Yield Management](#cap-52-trip-pricing-and-yield-management) | PARTIAL | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-5.3 Analytics and Business Intelligence](#cap-53-analytics-and-business-intelligence) | IMPLEMENTED | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-5.4 Financial Reporting and Reconciliation](#cap-54-financial-reporting-and-reconciliation) | PARTIAL | 1 | 2026-03-06 | ACTIVE | LOW | 1 | 3 |
| [CAP-5.5 Refund and Dispute Management](#cap-55-refund-and-dispute-management) | IMPLEMENTED | 1 | 2026-03-06 | ACTIVE | LOW | 4 | 3 |
| [CAP-6.1 Third-Party Booking Channels](#cap-61-third-party-booking-channels) | IMPLEMENTED | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-6.2 Affiliate and Commission Management](#cap-62-affiliate-and-commission-management) | PARTIAL | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-6.3 Channel Rate Parity Management](#cap-63-channel-rate-parity-management) | NOT IMPLEMENTED | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-7.1 Notification Delivery (Multi-Channel)](#cap-71-notification-delivery-multi-channel) | IMPLEMENTED | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-7.2 Geospatial and Location Services](#cap-72-geospatial-and-location-services) | IMPLEMENTED | 0 | — | UNTOUCHED | NONE | 0 | 0 |
| [CAP-7.3 Search and Discovery Engine](#cap-73-search-and-discovery-engine) | NOT IMPLEMENTED | 0 | — | UNTOUCHED | NONE | 0 | 0 |

## Domain Overview

| Domain | L2 Capabilities | Implemented | Partial | Gaps |
|--------|----------------|-------------|---------|------|
| [CAP-1 Guest Experience](#cap-1-guest-experience) | 8 | 7 | 0 | 1 (Personalized Recommendations) |
| [CAP-2 Adventure Operations](#cap-2-adventure-operations) | 5 | 5 | 0 | 0 |
| [CAP-3 Safety and Risk](#cap-3-safety-and-risk) | 5 | 5 | 0 | 0 |
| [CAP-4 Resource Management](#cap-4-resource-management) | 5 | 4 | 0 | 1 (Facility and Venue Management) |
| [CAP-5 Revenue and Finance](#cap-5-revenue-and-finance) | 5 | 3 | 2 | 0 |
| [CAP-6 Partner Ecosystem](#cap-6-partner-ecosystem) | 3 | 1 | 1 | 1 (Channel Rate Parity Management) |
| [CAP-7 Platform Services](#cap-7-platform-services) | 3 | 2 | 0 | 1 (Search and Discovery Engine) |

## CAP-1 Guest Experience

*Capabilities that directly serve guest-facing journeys from discovery through post-adventure engagement*

### CAP-1.1 Guest Identity and Profile Management

**Status:** IMPLEMENTED

Create, verify, merge, and manage guest identity records

**Services:** [svc-guest-profiles](../microservices/svc-guest-profiles.md)

### CAP-1.2 Adventure Discovery and Browsing

**Status:** IMPLEMENTED

Search, filter, and browse available adventures and trails

**Services:** [svc-trip-catalog](../microservices/svc-trip-catalog.md), [svc-trail-management](../microservices/svc-trail-management.md)

#### Solution Timeline

| Date | Ticket | Impact | Summary |
|------|--------|--------|---------|
| 2025-02-10 | [NTK-10002](../solutions/_NTK-10002-adventure-category-classification.md) | enhanced | Configuration-driven adventure category classification for check-in UI patterns |
| 2026-03-06 | [NTK-10008](../solutions/_NTK-10008-guest-reviews-and-ratings.md) | enhanced | Guest reviews and ratings platform with moderation pipeline |

#### Emergent L3 Capabilities

- **Adventure Category Taxonomy** — YAML-driven classification of 25 adventure types into 3 check-in patterns
- **Social Proof on Trip Pages** — Trip detail pages show average rating, review count, and rating distribution

### CAP-1.3 Reservation Management

**Status:** IMPLEMENTED

Create, modify, cancel, and look up adventure reservations

**Services:** [svc-reservations](../microservices/svc-reservations.md)

### CAP-1.4 Loyalty and Rewards

**Status:** IMPLEMENTED

Points earning, tier progression, and reward redemption

**Services:** [svc-loyalty-rewards](../microservices/svc-loyalty-rewards.md)

### CAP-1.5 Guest Communications

**Status:** IMPLEMENTED

Multi-channel notifications (email, SMS, push) for guest interactions

**Services:** [svc-notifications](../microservices/svc-notifications.md)

### CAP-1.6 Trip Media and Memories

**Status:** IMPLEMENTED

Photo and video capture, storage, and sharing for completed adventures

**Services:** [svc-media-gallery](../microservices/svc-media-gallery.md)

### CAP-1.7 Reviews and Feedback

**Status:** IMPLEMENTED

Guest trip reviews, ratings, and social proof for adventure selection

**Services:** [svc-reviews](../microservices/svc-reviews.md)

#### Solution Timeline

| Date | Ticket | Impact | Summary |
|------|--------|--------|---------|
| 2026-03-06 | [NTK-10008](../solutions/_NTK-10008-guest-reviews-and-ratings.md) | new | Guest reviews and ratings platform with moderation pipeline |

#### Emergent L3 Capabilities

- **Reservation-Gated Review Submission** — Reviews authenticated via COMPLETED reservation status — prevents fake reviews
- **Moderation Pipeline** — Reviews enter PENDING_MODERATION and require approval (automated or manual) before publication
- **Aggregated Rating Summaries** — Pre-computed per-trip and per-guide average ratings with distribution histograms
- **Category Ratings** — Optional per-category breakdown (safety, guide quality, value, scenery, difficulty accuracy)
- **Community Curation** — Helpful vote mechanism allows guests to surface the most useful reviews

### CAP-1.8 Personalized Recommendations

**Status:** NOT IMPLEMENTED

AI-driven adventure suggestions based on guest history, preferences, and behavior

**Priority:** MEDIUM
**Gap Rationale:** Increases average booking value; currently flat catalog with no personalization

## CAP-2 Adventure Operations

*Capabilities supporting day-of-adventure execution from check-in through adventure completion*

### CAP-2.1 Day-of-Adventure Check-In

**Status:** IMPLEMENTED

Guest arrival processing, identity verification, wristband assignment, safety briefing

**Services:** [svc-check-in](../microservices/svc-check-in.md)

#### Solution Timeline

| Date | Ticket | Impact | Summary |
|------|--------|--------|---------|
| 2025-02-08 | [NTK-10005](../solutions/_NTK-10005-wristband-rfid-field.md) | enhanced | Add RFID wristband field to check-in record for adventure tracking |
| 2025-02-10 | [NTK-10002](../solutions/_NTK-10002-adventure-category-classification.md) | enhanced | Configuration-driven adventure category classification for check-in UI patterns |
| 2026-03-20 | [NTK-10006](../solutions/_NTK-10006-real-time-adventure-tracking.md) | enhanced | Real-time GPS tracking of active adventure guests with automated emergency alerting |

#### Emergent L3 Capabilities

- **Pattern-Based Check-In Flows** — Three distinct check-in UI patterns (Basic, Guided, Full Service) driven by adventure category
- **Safe Default Classification** — Unknown or unmapped categories default to Pattern 3 (Full Service) for safety
- **Wristband RFID Capture** — Optional RFID tag ID (hex, 8-16 chars) validated and stored at check-in with uniqueness constraint
- **Tracking Session Initiation at Check-In** — checkin.completed event triggers svc-adventure-tracking to create session linked to wristband RFID
- **Tracking Verification Gate** — Pattern 2/3 adventures require confirmed tracking session before guest departure (ADR-005 safety-first)

### CAP-2.2 Schedule Planning and Optimization

**Status:** IMPLEMENTED

Daily schedule creation, slot management, and capacity optimization

**Services:** [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md)

#### Solution Timeline

| Date | Ticket | Impact | Summary |
|------|--------|--------|---------|
| 2025-02-05 | [NTK-10004](../solutions/_NTK-10004-guide-schedule-overwrite-bug.md) | fixed | Fix concurrent schedule update overwrites with optimistic locking |

#### Emergent L3 Capabilities

- **Optimistic Locking on Daily Schedule** — Version-based concurrency control (_rev field) prevents concurrent overwrites
- **PATCH Semantics for Schedule Updates** — Field-level merge replaces full entity replacement on schedule endpoints

### CAP-2.3 Guide Assignment and Management

**Status:** IMPLEMENTED

Guide roster, certification tracking, adventure assignment, and availability

**Services:** [svc-guide-management](../microservices/svc-guide-management.md)

### CAP-2.4 Trail Operations

**Status:** IMPLEMENTED

Trail condition monitoring, elevation data, difficulty classification

**Services:** [svc-trail-management](../microservices/svc-trail-management.md)

#### Solution Timeline

| Date | Ticket | Impact | Summary |
|------|--------|--------|---------|
| 2025-02-01 | [NTK-10001](../solutions/_NTK-10001-add-elevation-to-trail-response.md) | enhanced | Add elevation profile data to trail API response |

#### Emergent L3 Capabilities

- **Elevation Profile Data** — Structured elevation gain, loss, and distance-indexed profile points in trail API response

### CAP-2.5 Transport Coordination

**Status:** IMPLEMENTED

Vehicle dispatch, route planning, and guest transport scheduling

**Services:** [svc-transport-logistics](../microservices/svc-transport-logistics.md)

## CAP-3 Safety and Risk

*Capabilities ensuring guest and staff safety throughout all adventure operations*

### CAP-3.1 Waiver and Compliance Management

**Status:** IMPLEMENTED

Digital waiver collection, age verification, regulatory compliance tracking

**Services:** [svc-safety-compliance](../microservices/svc-safety-compliance.md)

### CAP-3.2 Incident Reporting and Response

**Status:** IMPLEMENTED

Incident logging, investigation workflow, and regulatory reporting

**Services:** [svc-safety-compliance](../microservices/svc-safety-compliance.md), [svc-adventure-tracking](../microservices/svc-adventure-tracking.md)

#### Solution Timeline

| Date | Ticket | Impact | Summary |
|------|--------|--------|---------|
| 2026-03-20 | [NTK-10006](../solutions/_NTK-10006-real-time-adventure-tracking.md) | enhanced | Real-time GPS tracking of active adventure guests with automated emergency alerting |

#### Emergent L3 Capabilities

- **Automated Incident Creation from Tracking Anomalies** — svc-safety-compliance subscribes to tracking.anomaly.detected and creates incident records automatically
- **GPS-Enriched Incident Records** — Incident reports include precise GPS coordinates and anomaly context from tracking session

### CAP-3.3 Emergency Response Coordination

**Status:** IMPLEMENTED

Emergency protocol activation, rescue dispatch, and communication coordination

**Services:** [svc-safety-compliance](../microservices/svc-safety-compliance.md), [svc-emergency-response](../microservices/svc-emergency-response.md), [svc-adventure-tracking](../microservices/svc-adventure-tracking.md)

#### Solution Timeline

| Date | Ticket | Impact | Summary |
|------|--------|--------|---------|
| 2026-03-20 | [NTK-10006](../solutions/_NTK-10006-real-time-adventure-tracking.md) | enhanced | Real-time GPS tracking of active adventure guests with automated emergency alerting |

#### Emergent L3 Capabilities

- **GPS-Triggered Emergency Dispatch** — Anomaly detection in svc-adventure-tracking auto-creates emergencies via svc-emergency-response with precise GPS location
- **Real-Time Location in Emergency Context** — Rescue teams receive last-known GPS position and can track live updates during response

### CAP-3.4 Wildlife and Environmental Monitoring

**Status:** IMPLEMENTED

Wildlife sighting reporting, trail closure triggers, environmental risk assessment

**Services:** [svc-safety-compliance](../microservices/svc-safety-compliance.md), [svc-trail-management](../microservices/svc-trail-management.md)

### CAP-3.5 Weather Monitoring and Alerting

**Status:** IMPLEMENTED

Weather condition tracking, severe weather alerts, and adventure cancellation triggers

**Services:** [svc-weather](../microservices/svc-weather.md)

## CAP-4 Resource Management

*Capabilities for managing physical assets, inventory, and facilities*

### CAP-4.1 Gear Inventory and Tracking

**Status:** IMPLEMENTED

Equipment checkout, return tracking, maintenance scheduling

**Services:** [svc-gear-inventory](../microservices/svc-gear-inventory.md)

### CAP-4.2 Procurement and Vendor Management

**Status:** IMPLEMENTED

Purchase orders, vendor relationships, and supply chain management

**Services:** [svc-inventory-procurement](../microservices/svc-inventory-procurement.md)

### CAP-4.3 Location and Capacity Management

**Status:** IMPLEMENTED

Venue capacity tracking, geospatial boundaries, location metadata

**Services:** [svc-location-services](../microservices/svc-location-services.md)

### CAP-4.4 Vehicle Fleet Management

**Status:** IMPLEMENTED

Vehicle inventory, maintenance scheduling, utilization tracking

**Services:** [svc-transport-logistics](../microservices/svc-transport-logistics.md)

### CAP-4.5 Facility and Venue Management

**Status:** NOT IMPLEMENTED

Facility maintenance, venue reservations, and infrastructure management

**Priority:** LOW
**Gap Rationale:** Currently handled informally through svc-location-services

## CAP-5 Revenue and Finance

*Capabilities for payment processing, pricing, financial reporting, and revenue optimization*

### CAP-5.1 Payment Processing

**Status:** IMPLEMENTED

Payment authorization, capture, and settlement across payment methods

**Services:** [svc-payments](../microservices/svc-payments.md)

### CAP-5.2 Trip Pricing and Yield Management

**Status:** PARTIAL

Dynamic pricing, seasonal rates, and demand-based yield optimization

**Services:** [svc-trip-catalog](../microservices/svc-trip-catalog.md)

### CAP-5.3 Analytics and Business Intelligence

**Status:** IMPLEMENTED

Operational dashboards, booking trends, revenue analytics

**Services:** [svc-analytics](../microservices/svc-analytics.md)

### CAP-5.4 Financial Reporting and Reconciliation

**Status:** PARTIAL

Revenue reporting, payment reconciliation, tax calculation

**Services:** [svc-payments](../microservices/svc-payments.md)

#### Solution Timeline

| Date | Ticket | Impact | Summary |
|------|--------|--------|---------|
| 2026-03-06 | [NTK-10009](../solutions/_NTK-10009-refund-dispute-management.md) | enhanced | Structured refund dispute workflows with policy engine and tiered escalation |

#### Emergent L3 Capabilities

- **Dispute Audit Trail** — All resolution decisions include policy evaluation, resolver identity, justification, and outcome

### CAP-5.5 Refund and Dispute Management

**Status:** IMPLEMENTED

Refund processing, chargeback management, dispute resolution workflows

**Services:** [svc-payments](../microservices/svc-payments.md)

#### Solution Timeline

| Date | Ticket | Impact | Summary |
|------|--------|--------|---------|
| 2026-03-06 | [NTK-10009](../solutions/_NTK-10009-refund-dispute-management.md) | enhanced | Structured refund dispute workflows with policy engine and tiered escalation |

#### Emergent L3 Capabilities

- **Dispute Lifecycle Management** — Full dispute lifecycle (OPENED, UNDER_REVIEW, ESCALATED, RESOLVED) with audit trail
- **YAML-Driven Refund Policy Engine** — Codified cancellation windows and refund percentages evaluated automatically per ADR-004 pattern
- **Three-Tier Escalation** — Auto-approve (policy-eligible), agent review (edge cases), manager escalation (high-value)
- **Chargeback Ingestion** — Payment processor chargeback webhooks create dispute records auto-escalated to manager tier

## CAP-6 Partner Ecosystem

*Capabilities for managing third-party partnerships, booking channels, and commission structures*

### CAP-6.1 Third-Party Booking Channels

**Status:** IMPLEMENTED

OTA integrations, partner API gateway, booking ingestion

**Services:** [svc-partner-integrations](../microservices/svc-partner-integrations.md)

### CAP-6.2 Affiliate and Commission Management

**Status:** PARTIAL

Commission calculation, partner payout, and affiliate tracking

**Services:** [svc-partner-integrations](../microservices/svc-partner-integrations.md)

### CAP-6.3 Channel Rate Parity Management

**Status:** NOT IMPLEMENTED

Ensuring consistent pricing across direct and partner booking channels

**Priority:** MEDIUM
**Gap Rationale:** Partners may undercut direct pricing; no parity enforcement

## CAP-7 Platform Services

*Shared infrastructure capabilities consumed by multiple domain services*

### CAP-7.1 Notification Delivery (Multi-Channel)

**Status:** IMPLEMENTED

Email, SMS, push notification delivery with template management

**Services:** [svc-notifications](../microservices/svc-notifications.md)

### CAP-7.2 Geospatial and Location Services

**Status:** IMPLEMENTED

Geocoding, geofencing, distance calculation, and map tile serving

**Services:** [svc-location-services](../microservices/svc-location-services.md)

### CAP-7.3 Search and Discovery Engine

**Status:** NOT IMPLEMENTED

Cross-entity full-text search with relevance ranking and faceted filtering

**Priority:** MEDIUM
**Gap Rationale:** No cross-entity search or relevance ranking exists
