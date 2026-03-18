---
hide:
  - toc
tags:
  - actors
  - catalog
---

<div class="hero" markdown>

# Actor Catalog

<p class="subtitle">All Actors Across the NovaTrek Enterprise</p>
<span class="version-badge">22 Actors &middot; 11 External Systems &middot; 3 Frontend Applications &middot; 5 Humans &middot; 3 Infrastructures</span>

</div>

This catalog lists every actor that interacts with the NovaTrek platform: people, frontend applications, internal microservices, external systems, and infrastructure components. Each actor links to its detailed page where available.

---

## :material-account: Humans

| Actor | Domain | Description | Interacts With |
|-------|--------|-------------|----------------|
| **Adventure Guide** | Guide Management | Certified outdoor guides who lead adventure trips, manage guest safety, and report incidents. | [Adventure App](../applications/app-guest-mobile/), [Operations Dashboard](../applications/web-ops-dashboard/) |
| **Guest** | Guest Identity | NovaTrek customer who books, checks in for, and participates in adventure trips. | [Guest Portal](../applications/web-guest-portal/), [Adventure App](../applications/app-guest-mobile/) |
| **Operations Staff** | Operations | On-site NovaTrek employees who manage daily operations including check-in, scheduling, gear assignment, and incident response. | [Operations Dashboard](../applications/web-ops-dashboard/) |
| **Software Developer** | Engineering | Implements approved architecture designs in service source code, writes tests, and proposes API contract updates via pull request when implementation reveals contract gaps. | [Operations Dashboard](../applications/web-ops-dashboard/) |
| **Solution Architect** | Architecture | Owns architecture metadata, API contracts, solution designs, decisions, and diagrams. Proposes and documents architectural changes to the NovaTrek platform. | [Operations Dashboard](../applications/web-ops-dashboard/) |

---

## :material-application: Frontend Applications

| Application | Display Name | Domain | Technology | Team | Description |
|-------------|-------------|--------|------------|------|-------------|
| [app-guest-mobile](../applications/app-guest-mobile/) | Adventure App | Guest Identity | React Native | Guest Experience Team | Native mobile application for guests to self check-in, view live trip maps, receive weather alerts, upload photos, and earn loyalty points. |
| [web-guest-portal](../applications/web-guest-portal/) | Guest Portal | Guest Identity | React SPA | Guest Experience Team | Public-facing web application for guests to browse trips, book reservations, manage profiles, sign waivers, and view trip media. |
| [web-ops-dashboard](../applications/web-ops-dashboard/) | Operations Dashboard | Operations | React SPA | NovaTrek Operations Team | Internal web application for operations staff to manage check-ins, daily schedules, guide assignments, safety incidents, and partner bookings. |

---

## :material-server-network: Infrastructures

| Component | Technology | Domain | Description |
|-----------|------------|--------|-------------|
| **API Gateway** | Azure API Management | Platform | Central API Gateway that routes all external requests to backend microservices. Handles authentication, rate limiting, and TLS termination. |
| **Event Bus** | Apache Kafka | Platform | Apache Kafka cluster used for asynchronous event-driven communication between microservices. All domain events flow through dedicated Kafka topics. |
| **Object Store** | Azure Blob Storage | Platform | Cloud object storage for media assets including trip photos, guide profile images, and waiver documents. |

---

## :material-cloud: External Systems

| System | Technology | Domain | PCI | Description |
|--------|------------|--------|-----|-------------|
| **DocuSign API** | DocuSign eSignature REST API | Safety |  | Electronic signature platform used for legally-binding adventure liability waivers and safety acknowledgments. |
| **Firebase Cloud Messaging** | Firebase FCM | Support |  | Push notification delivery service for real-time alerts to guest mobile devices (weather warnings, check-in reminders, schedule changes). |
| **Fraud Detection API** | REST API | Support | :material-shield-lock: PCI | Third-party fraud prevention service that scores payment transactions for risk before authorization. |
| **Google Maps Platform** | Google Maps REST API | Logistics |  | Geolocation and mapping service used for trail positioning, location tracking, and capacity management at adventure sites. |
| **IDVerify API** | REST API | Guest Identity |  | Identity verification service used during check-in to validate guest identity against government-issued IDs. |
| **OpenWeather API** | OpenWeather REST API | Support |  | Weather data provider delivering current conditions, forecasts, and severe weather alerts for trail and adventure locations. |
| **Payment Gateway** | Stripe | Support | :material-shield-lock: PCI | PCI-certified payment processing gateway that handles credit card authorization, capture, and refund transactions. |
| **SendGrid API** | SendGrid REST API | Support |  | Transactional email delivery service for reservation confirmations, waiver requests, and loyalty point notifications. |
| **Snowflake Data Cloud** | Snowflake SQL API | Support |  | Cloud data warehouse used for business intelligence, analytics aggregation, and historical trend analysis across all NovaTrek domains. |
| **Stripe API** | Stripe REST API | Support | :material-shield-lock: PCI | Payment platform API for processing charges, managing payment methods, and handling disputes. |
| **Twilio API** | Twilio REST API | Support |  | SMS and messaging service for check-in reminders, schedule updates, and emergency notifications to guests and guides. |

---

## :material-hexagon-multiple: Internal Microservices

| Service | Domain | Description |
|---------|--------|-------------|
| [svc-reservations](../microservices/svc-reservations/) | Booking | See [microservice page](../microservices/svc-reservations/) for full details |
| [svc-partner-integrations](../microservices/svc-partner-integrations/) | External | See [microservice page](../microservices/svc-partner-integrations/) for full details |
| [svc-guest-profiles](../microservices/svc-guest-profiles/) | Guest Identity | See [microservice page](../microservices/svc-guest-profiles/) for full details |
| [svc-guide-management](../microservices/svc-guide-management/) | Guide Management | See [microservice page](../microservices/svc-guide-management/) for full details |
| [svc-gear-inventory](../microservices/svc-gear-inventory/) | Logistics | See [microservice page](../microservices/svc-gear-inventory/) for full details |
| [svc-transport-logistics](../microservices/svc-transport-logistics/) | Logistics | See [microservice page](../microservices/svc-transport-logistics/) for full details |
| [svc-check-in](../microservices/svc-check-in/) | Operations | See [microservice page](../microservices/svc-check-in/) for full details |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator/) | Operations | See [microservice page](../microservices/svc-scheduling-orchestrator/) for full details |
| [svc-trail-management](../microservices/svc-trail-management/) | Product Catalog | See [microservice page](../microservices/svc-trail-management/) for full details |
| [svc-trip-catalog](../microservices/svc-trip-catalog/) | Product Catalog | See [microservice page](../microservices/svc-trip-catalog/) for full details |
| [svc-emergency-response](../microservices/svc-emergency-response/) | Safety | See [microservice page](../microservices/svc-emergency-response/) for full details |
| [svc-safety-compliance](../microservices/svc-safety-compliance/) | Safety | See [microservice page](../microservices/svc-safety-compliance/) for full details |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking/) | Safety | See [microservice page](../microservices/svc-wildlife-tracking/) for full details |
| [svc-analytics](../microservices/svc-analytics/) | Support | See [microservice page](../microservices/svc-analytics/) for full details |
| [svc-inventory-procurement](../microservices/svc-inventory-procurement/) | Support | See [microservice page](../microservices/svc-inventory-procurement/) for full details |
| [svc-location-services](../microservices/svc-location-services/) | Support | See [microservice page](../microservices/svc-location-services/) for full details |
| [svc-loyalty-rewards](../microservices/svc-loyalty-rewards/) | Support | See [microservice page](../microservices/svc-loyalty-rewards/) for full details |
| [svc-media-gallery](../microservices/svc-media-gallery/) | Support | See [microservice page](../microservices/svc-media-gallery/) for full details |
| [svc-notifications](../microservices/svc-notifications/) | Support | See [microservice page](../microservices/svc-notifications/) for full details |
| [svc-payments](../microservices/svc-payments/) | Support | See [microservice page](../microservices/svc-payments/) for full details |
| [svc-reviews](../microservices/svc-reviews/) | Support | See [microservice page](../microservices/svc-reviews/) for full details |
| [svc-weather](../microservices/svc-weather/) | Support | See [microservice page](../microservices/svc-weather/) for full details |

---

## Actor Details

### API Gateway

- **Type:** Infrastructure
- **Domain:** Platform
- **Description:** Central API Gateway that routes all external requests to backend microservices. Handles authentication, rate limiting, and TLS termination.
- **Technology:** Azure API Management

### Adventure Guide

- **Type:** Human
- **Domain:** Guide Management
- **Description:** Certified outdoor guides who lead adventure trips, manage guest safety, and report incidents.

### DocuSign API

- **Type:** External System
- **Domain:** Safety
- **Description:** Electronic signature platform used for legally-binding adventure liability waivers and safety acknowledgments.
- **Technology:** DocuSign eSignature REST API

**Referenced by:**

- [svc-safety-compliance](../microservices/svc-safety-compliance/)

### Event Bus

- **Type:** Infrastructure
- **Domain:** Platform
- **Description:** Apache Kafka cluster used for asynchronous event-driven communication between microservices. All domain events flow through dedicated Kafka topics.
- **Technology:** Apache Kafka

**Referenced by:**

- [svc-guest-profiles](../microservices/svc-guest-profiles/)
- [svc-reservations](../microservices/svc-reservations/)

### Firebase Cloud Messaging

- **Type:** External System
- **Domain:** Support
- **Description:** Push notification delivery service for real-time alerts to guest mobile devices (weather warnings, check-in reminders, schedule changes).
- **Technology:** Firebase FCM

**Referenced by:**

- [svc-notifications](../microservices/svc-notifications/)

### Fraud Detection API

- **Type:** External System
- **Domain:** Support
- **Description:** Third-party fraud prevention service that scores payment transactions for risk before authorization.
- **Technology:** REST API
- **Compliance:** :material-shield-lock: PCI DSS scope

**Referenced by:**

- [svc-payments](../microservices/svc-payments/)

### Google Maps Platform

- **Type:** External System
- **Domain:** Logistics
- **Description:** Geolocation and mapping service used for trail positioning, location tracking, and capacity management at adventure sites.
- **Technology:** Google Maps REST API

**Referenced by:**

- [svc-location-services](../microservices/svc-location-services/)
- [svc-media-gallery](../microservices/svc-media-gallery/)
- [svc-transport-logistics](../microservices/svc-transport-logistics/)

### Guest

- **Type:** Human
- **Domain:** Guest Identity
- **Description:** NovaTrek customer who books, checks in for, and participates in adventure trips.

### IDVerify API

- **Type:** External System
- **Domain:** Guest Identity
- **Description:** Identity verification service used during check-in to validate guest identity against government-issued IDs.
- **Technology:** REST API

**Referenced by:**

- [svc-guest-profiles](../microservices/svc-guest-profiles/)

### Object Store

- **Type:** Infrastructure
- **Domain:** Platform
- **Description:** Cloud object storage for media assets including trip photos, guide profile images, and waiver documents.
- **Technology:** Azure Blob Storage

**Referenced by:**

- [svc-media-gallery](../microservices/svc-media-gallery/)

### OpenWeather API

- **Type:** External System
- **Domain:** Support
- **Description:** Weather data provider delivering current conditions, forecasts, and severe weather alerts for trail and adventure locations.
- **Technology:** OpenWeather REST API

**Referenced by:**

- [svc-weather](../microservices/svc-weather/)

### Operations Staff

- **Type:** Human
- **Domain:** Operations
- **Description:** On-site NovaTrek employees who manage daily operations including check-in, scheduling, gear assignment, and incident response.

### Payment Gateway

- **Type:** External System
- **Domain:** Support
- **Description:** PCI-certified payment processing gateway that handles credit card authorization, capture, and refund transactions.
- **Technology:** Stripe
- **Compliance:** :material-shield-lock: PCI DSS scope

**Referenced by:**

- [svc-payments](../microservices/svc-payments/)

### SendGrid API

- **Type:** External System
- **Domain:** Support
- **Description:** Transactional email delivery service for reservation confirmations, waiver requests, and loyalty point notifications.
- **Technology:** SendGrid REST API

**Referenced by:**

- [svc-notifications](../microservices/svc-notifications/)

### Snowflake Data Cloud

- **Type:** External System
- **Domain:** Support
- **Description:** Cloud data warehouse used for business intelligence, analytics aggregation, and historical trend analysis across all NovaTrek domains.
- **Technology:** Snowflake SQL API

**Referenced by:**

- [svc-analytics](../microservices/svc-analytics/)

### Software Developer

- **Type:** Human
- **Domain:** Engineering
- **Description:** Implements approved architecture designs in service source code, writes tests, and proposes API contract updates via pull request when implementation reveals contract gaps.

### Solution Architect

- **Type:** Human
- **Domain:** Architecture
- **Description:** Owns architecture metadata, API contracts, solution designs, decisions, and diagrams. Proposes and documents architectural changes to the NovaTrek platform.

### Stripe API

- **Type:** External System
- **Domain:** Support
- **Description:** Payment platform API for processing charges, managing payment methods, and handling disputes.
- **Technology:** Stripe REST API
- **Compliance:** :material-shield-lock: PCI DSS scope

### Twilio API

- **Type:** External System
- **Domain:** Support
- **Description:** SMS and messaging service for check-in reminders, schedule updates, and emergency notifications to guests and guides.
- **Technology:** Twilio REST API

**Referenced by:**

- [svc-notifications](../microservices/svc-notifications/)

### app-guest-mobile

- **Type:** Frontend Application
- **Domain:** Guest Identity
- **Description:** Native mobile application for guests to self check-in, view live trip maps, receive weather alerts, upload photos, and earn loyalty points.
- **Technology:** React Native
- **Team:** Guest Experience Team

**Referenced by:**

- [svc-check-in](../microservices/svc-check-in/)
- [svc-emergency-response](../microservices/svc-emergency-response/)
- [svc-gear-inventory](../microservices/svc-gear-inventory/)
- [svc-guest-profiles](../microservices/svc-guest-profiles/)
- [svc-location-services](../microservices/svc-location-services/)
- [svc-loyalty-rewards](../microservices/svc-loyalty-rewards/)
- [svc-media-gallery](../microservices/svc-media-gallery/)
- [svc-notifications](../microservices/svc-notifications/)
- [svc-payments](../microservices/svc-payments/)
- [svc-reservations](../microservices/svc-reservations/)
- [svc-safety-compliance](../microservices/svc-safety-compliance/)
- [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator/)
- [svc-trail-management](../microservices/svc-trail-management/)
- [svc-trip-catalog](../microservices/svc-trip-catalog/)
- [svc-weather](../microservices/svc-weather/)
- [svc-wildlife-tracking](../microservices/svc-wildlife-tracking/)

### web-guest-portal

- **Type:** Frontend Application
- **Domain:** Guest Identity
- **Description:** Public-facing web application for guests to browse trips, book reservations, manage profiles, sign waivers, and view trip media.
- **Technology:** React SPA
- **Team:** Guest Experience Team

**Referenced by:**

- [svc-guest-profiles](../microservices/svc-guest-profiles/)
- [svc-loyalty-rewards](../microservices/svc-loyalty-rewards/)
- [svc-media-gallery](../microservices/svc-media-gallery/)
- [svc-notifications](../microservices/svc-notifications/)
- [svc-payments](../microservices/svc-payments/)
- [svc-reservations](../microservices/svc-reservations/)
- [svc-safety-compliance](../microservices/svc-safety-compliance/)
- [svc-trail-management](../microservices/svc-trail-management/)
- [svc-trip-catalog](../microservices/svc-trip-catalog/)
- [svc-weather](../microservices/svc-weather/)

### web-ops-dashboard

- **Type:** Frontend Application
- **Domain:** Operations
- **Description:** Internal web application for operations staff to manage check-ins, daily schedules, guide assignments, safety incidents, and partner bookings.
- **Technology:** React SPA
- **Team:** NovaTrek Operations Team

**Referenced by:**

- [svc-analytics](../microservices/svc-analytics/)
- [svc-check-in](../microservices/svc-check-in/)
- [svc-emergency-response](../microservices/svc-emergency-response/)
- [svc-gear-inventory](../microservices/svc-gear-inventory/)
- [svc-guest-profiles](../microservices/svc-guest-profiles/)
- [svc-guide-management](../microservices/svc-guide-management/)
- [svc-inventory-procurement](../microservices/svc-inventory-procurement/)
- [svc-location-services](../microservices/svc-location-services/)
- [svc-notifications](../microservices/svc-notifications/)
- [svc-partner-integrations](../microservices/svc-partner-integrations/)
- [svc-payments](../microservices/svc-payments/)
- [svc-reservations](../microservices/svc-reservations/)
- [svc-safety-compliance](../microservices/svc-safety-compliance/)
- [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator/)
- [svc-trail-management](../microservices/svc-trail-management/)
- [svc-transport-logistics](../microservices/svc-transport-logistics/)
- [svc-weather](../microservices/svc-weather/)
- [svc-wildlife-tracking](../microservices/svc-wildlife-tracking/)

### svc-analytics

- **Type:** Internal Microservice
- **Domain:** Support
- **Details:** [svc-analytics Microservice Page](../microservices/svc-analytics/)

### svc-check-in

- **Type:** Internal Microservice
- **Domain:** Operations
- **Details:** [svc-check-in Microservice Page](../microservices/svc-check-in/)

### svc-emergency-response

- **Type:** Internal Microservice
- **Domain:** Safety
- **Details:** [svc-emergency-response Microservice Page](../microservices/svc-emergency-response/)

### svc-gear-inventory

- **Type:** Internal Microservice
- **Domain:** Logistics
- **Details:** [svc-gear-inventory Microservice Page](../microservices/svc-gear-inventory/)

### svc-guest-profiles

- **Type:** Internal Microservice
- **Domain:** Guest Identity
- **Details:** [svc-guest-profiles Microservice Page](../microservices/svc-guest-profiles/)

### svc-guide-management

- **Type:** Internal Microservice
- **Domain:** Guide Management
- **Details:** [svc-guide-management Microservice Page](../microservices/svc-guide-management/)

### svc-inventory-procurement

- **Type:** Internal Microservice
- **Domain:** Support
- **Details:** [svc-inventory-procurement Microservice Page](../microservices/svc-inventory-procurement/)

### svc-location-services

- **Type:** Internal Microservice
- **Domain:** Support
- **Details:** [svc-location-services Microservice Page](../microservices/svc-location-services/)

### svc-loyalty-rewards

- **Type:** Internal Microservice
- **Domain:** Support
- **Details:** [svc-loyalty-rewards Microservice Page](../microservices/svc-loyalty-rewards/)

### svc-media-gallery

- **Type:** Internal Microservice
- **Domain:** Support
- **Details:** [svc-media-gallery Microservice Page](../microservices/svc-media-gallery/)

### svc-notifications

- **Type:** Internal Microservice
- **Domain:** Support
- **Details:** [svc-notifications Microservice Page](../microservices/svc-notifications/)

### svc-partner-integrations

- **Type:** Internal Microservice
- **Domain:** External
- **Details:** [svc-partner-integrations Microservice Page](../microservices/svc-partner-integrations/)

### svc-payments

- **Type:** Internal Microservice
- **Domain:** Support
- **Details:** [svc-payments Microservice Page](../microservices/svc-payments/)

### svc-reservations

- **Type:** Internal Microservice
- **Domain:** Booking
- **Details:** [svc-reservations Microservice Page](../microservices/svc-reservations/)

### svc-reviews

- **Type:** Internal Microservice
- **Domain:** Support
- **Details:** [svc-reviews Microservice Page](../microservices/svc-reviews/)

### svc-safety-compliance

- **Type:** Internal Microservice
- **Domain:** Safety
- **Details:** [svc-safety-compliance Microservice Page](../microservices/svc-safety-compliance/)

### svc-scheduling-orchestrator

- **Type:** Internal Microservice
- **Domain:** Operations
- **Details:** [svc-scheduling-orchestrator Microservice Page](../microservices/svc-scheduling-orchestrator/)

### svc-trail-management

- **Type:** Internal Microservice
- **Domain:** Product Catalog
- **Details:** [svc-trail-management Microservice Page](../microservices/svc-trail-management/)

### svc-transport-logistics

- **Type:** Internal Microservice
- **Domain:** Logistics
- **Details:** [svc-transport-logistics Microservice Page](../microservices/svc-transport-logistics/)

### svc-trip-catalog

- **Type:** Internal Microservice
- **Domain:** Product Catalog
- **Details:** [svc-trip-catalog Microservice Page](../microservices/svc-trip-catalog/)

### svc-weather

- **Type:** Internal Microservice
- **Domain:** Support
- **Details:** [svc-weather Microservice Page](../microservices/svc-weather/)

### svc-wildlife-tracking

- **Type:** Internal Microservice
- **Domain:** Safety
- **Details:** [svc-wildlife-tracking Microservice Page](../microservices/svc-wildlife-tracking/)
