---
hide:
  - toc
tags:
  - microservice
---

<div class="hero" markdown>

# Microservice Pages

<p class="subtitle">Deep-Dive Architecture Documentation for Every NovaTrek Service</p>

<span class="version-badge">23 Services &middot; 186 Endpoints</span>

</div>

Each microservice page provides **PlantUML sequence diagrams** for every API endpoint with clickable links to other services and Swagger UI, data store documentation, and direct links to the interactive API reference.

All services are built on the same [technology stack](../technologies.md) — Java 21, Spring Boot 3.3.5, PostgreSQL 15, deployed to Azure Container Apps.

---

## Enterprise Architecture

<div class="diagram-wrap"><a href="svg/enterprise-c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="svg/enterprise-c4-context.svg" type="image/svg+xml" style="width:100%;max-width:1400px"></object></div>

---

## Operations

| Service | Version | Endpoints | Status | Page |
|---------|---------|-----------|--------|------|
| **NovaTrek Adventure Tracking Service**<br><small>`svc-adventure-tracking`</small> | `1.0.0` | 10 endpoints | :material-circle-outline: Wave ? | [:material-arrow-right: Open](svc-adventure-tracking.md){ .md-button } |
| **NovaTrek Check-In Service**<br><small>`svc-check-in`</small> | `1.0.0` | 5 endpoints | :material-circle-outline: Wave 3 | [:material-arrow-right: Open](svc-check-in.md){ .md-button } |
| **NovaTrek Scheduling Orchestrator API**<br><small>`svc-scheduling-orchestrator`</small> | `3.0.1` | 5 endpoints | :material-circle-outline: Wave 3 | [:material-arrow-right: Open](svc-scheduling-orchestrator.md){ .md-button } |

## Guest Identity

| Service | Version | Endpoints | Status | Page |
|---------|---------|-----------|--------|------|
| **NovaTrek Adventures - Guest Profiles Service**<br><small>`svc-guest-profiles`</small> | `2.4.0` | 9 endpoints | :white_check_mark: Deployed | [:material-arrow-right: Open](svc-guest-profiles.md){ .md-button } |

## Booking

| Service | Version | Endpoints | Status | Page |
|---------|---------|-----------|--------|------|
| **Reservations Service**<br><small>`svc-reservations`</small> | `2.4.1` | 8 endpoints | :material-circle-outline: Wave 2 | [:material-arrow-right: Open](svc-reservations.md){ .md-button } |

## Product Catalog

| Service | Version | Endpoints | Status | Page |
|---------|---------|-----------|--------|------|
| **NovaTrek Trail Management Service**<br><small>`svc-trail-management`</small> | `1.1.0` | 9 endpoints | :white_check_mark: Deployed | [:material-arrow-right: Open](svc-trail-management.md){ .md-button } |
| **NovaTrek Adventures - Trip Catalog Service**<br><small>`svc-trip-catalog`</small> | `2.4.0` | 11 endpoints | :white_check_mark: Deployed | [:material-arrow-right: Open](svc-trip-catalog.md){ .md-button } |

## Safety

| Service | Version | Endpoints | Status | Page |
|---------|---------|-----------|--------|------|
| **NovaTrek Emergency Response Service**<br><small>`svc-emergency-response`</small> | `1.0.0` | 10 endpoints | :material-circle-outline: Wave 6 | [:material-arrow-right: Open](svc-emergency-response.md){ .md-button } |
| **NovaTrek Safety and Compliance Service**<br><small>`svc-safety-compliance`</small> | `1.0.0` | 8 endpoints | :material-circle-outline: Wave 3 | [:material-arrow-right: Open](svc-safety-compliance.md){ .md-button } |
| **NovaTrek Wildlife Tracking Service**<br><small>`svc-wildlife-tracking`</small> | `1.0.0` | 10 endpoints | :material-circle-outline: Wave 6 | [:material-arrow-right: Open](svc-wildlife-tracking.md){ .md-button } |

## Logistics

| Service | Version | Endpoints | Status | Page |
|---------|---------|-----------|--------|------|
| **NovaTrek Adventures - Gear Inventory Service**<br><small>`svc-gear-inventory`</small> | `2.4.0` | 12 endpoints | :material-circle-outline: Wave 3 | [:material-arrow-right: Open](svc-gear-inventory.md){ .md-button } |
| **NovaTrek Transport Logistics API**<br><small>`svc-transport-logistics`</small> | `1.4.0` | 7 endpoints | :material-circle-outline: Wave 4 | [:material-arrow-right: Open](svc-transport-logistics.md){ .md-button } |

## Guide Management

| Service | Version | Endpoints | Status | Page |
|---------|---------|-----------|--------|------|
| **NovaTrek Guide Management Service**<br><small>`svc-guide-management`</small> | `2.4.0` | 12 endpoints | :material-circle-outline: Wave 4 | [:material-arrow-right: Open](svc-guide-management.md){ .md-button } |

## External

| Service | Version | Endpoints | Status | Page |
|---------|---------|-----------|--------|------|
| **NovaTrek Partner Integrations Service**<br><small>`svc-partner-integrations`</small> | `1.0.0` | 7 endpoints | :material-circle-outline: Wave 6 | [:material-arrow-right: Open](svc-partner-integrations.md){ .md-button } |

## Support

| Service | Version | Endpoints | Status | Page |
|---------|---------|-----------|--------|------|
| **NovaTrek Analytics Service**<br><small>`svc-analytics`</small> | `1.3.0` | 6 endpoints | :material-circle-outline: Wave 5 | [:material-arrow-right: Open](svc-analytics.md){ .md-button } |
| **NovaTrek Inventory Procurement API**<br><small>`svc-inventory-procurement`</small> | `2.1.0` | 8 endpoints | :material-circle-outline: Wave 6 | [:material-arrow-right: Open](svc-inventory-procurement.md){ .md-button } |
| **NovaTrek Location Services API**<br><small>`svc-location-services`</small> | `1.2.0` | 6 endpoints | :material-circle-outline: Wave 4 | [:material-arrow-right: Open](svc-location-services.md){ .md-button } |
| **NovaTrek Loyalty Rewards Service**<br><small>`svc-loyalty-rewards`</small> | `1.0.0` | 5 endpoints | :material-circle-outline: Wave 5 | [:material-arrow-right: Open](svc-loyalty-rewards.md){ .md-button } |
| **NovaTrek Media Gallery Service**<br><small>`svc-media-gallery`</small> | `1.0.2` | 5 endpoints | :material-circle-outline: Wave 5 | [:material-arrow-right: Open](svc-media-gallery.md){ .md-button } |
| **NovaTrek Notifications Service**<br><small>`svc-notifications`</small> | `1.0.0` | 6 endpoints | :material-circle-outline: Wave 2 | [:material-arrow-right: Open](svc-notifications.md){ .md-button } |
| **NovaTrek Payments Service**<br><small>`svc-payments`</small> | `1.1.0` | 12 endpoints | :material-circle-outline: Wave 2 | [:material-arrow-right: Open](svc-payments.md){ .md-button } |
| **NovaTrek Reviews Service**<br><small>`svc-reviews`</small> | `1.0.0` | 10 endpoints | :material-circle-outline: Wave ? | [:material-arrow-right: Open](svc-reviews.md){ .md-button } |
| **NovaTrek Weather Service**<br><small>`svc-weather`</small> | `1.0.0` | 5 endpoints | :material-circle-outline: Wave 6 | [:material-arrow-right: Open](svc-weather.md){ .md-button } |
