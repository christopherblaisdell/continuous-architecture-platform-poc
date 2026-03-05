# Plan: Add Frontend Applications to the Architecture Portal

**Date:** 2026-03-04
**Status:** Draft

---

## Overview

Add three frontend applications to the NovaTrek Architecture Portal alongside the existing 19 microservice pages:

| Application | Type | Audience | Naming Convention |
|-------------|------|----------|-------------------|
| **NovaTrek Guest Portal** | Web (React SPA) | Guests (public) | `web-guest-portal` |
| **NovaTrek Operations Dashboard** | Web (Angular) | Staff / Park Ops | `web-ops-dashboard` |
| **NovaTrek Adventure App** | Mobile (React Native) | Guests (on-trip) | `app-guest-mobile` |

---

## 1. Page Naming

Each frontend gets a deep-dive page following the existing naming pattern:

| Page File | Nav Label | URL Path |
|-----------|-----------|----------|
| `applications/web-guest-portal.md` | web-guest-portal | `/applications/web-guest-portal/` |
| `applications/web-ops-dashboard.md` | web-ops-dashboard | `/applications/web-ops-dashboard/` |
| `applications/app-guest-mobile.md` | app-guest-mobile | `/applications/app-guest-mobile/` |
| `applications/index.md` | (section index) | `/applications/` |

**Rationale:** The `web-` and `app-` prefixes distinguish websites from mobile apps at a glance — analogous to how `svc-` prefixes distinguish backend services.

---

## 2. Portal Organization

### New nav section in `mkdocs.yml`

```yaml
nav:
  - Home: index.md
  - Service Catalog: services/index.md
  - Design Standards: ...
  - Applications:                              # NEW — sits between Microservices and Tags
    - applications/index.md
    - web-guest-portal: applications/web-guest-portal.md
    - web-ops-dashboard: applications/web-ops-dashboard.md
    - app-guest-mobile: applications/app-guest-mobile.md
  - Microservice Pages: ...
  - Tags: tags.md
```

### Directory structure

```
portal/docs/applications/
  index.md                     # Application gallery (like microservices/index.md)
  web-guest-portal.md          # Deep-dive page
  web-ops-dashboard.md         # Deep-dive page
  app-guest-mobile.md          # Deep-dive page
  puml/                        # PlantUML source files (user journey diagrams)
  svg/                         # Rendered SVG diagrams
```

This mirrors the `microservices/` directory structure.

---

## 3. Page Content Structure

Each application page follows this template:

### Header

- Application name, type badge (Web / Mobile), tech stack, owning team
- Links to design system / Figma (placeholder)

### Screen / Feature Inventory

Instead of API endpoints, frontend pages list **screens or features** as the primary unit:

| Section | Microservice Equivalent |
|---------|------------------------|
| Screens / Features | Endpoints |
| User Journey Diagrams | Sequence Diagrams |
| API Dependencies | Cross-Service Calls |
| Client-Side State | Data Store |

### User Journey Sequence Diagrams

PlantUML sequence diagrams showing the **full user journey** through UI to backend:

```
User -> Browser/App -> API Gateway -> svc-A -> DB
                                   -> svc-B -> DB
                                   -> svc-C -> External API
```

These are more complex than microservice diagrams because each user action typically fans out across multiple backend services.

### API Dependency Table

A table showing every microservice endpoint the application consumes:

| Endpoint | Service | Purpose | Link |
|----------|---------|---------|------|
| GET /trips | svc-trip-catalog | Browse adventures | [deep link] |
| POST /reservations | svc-reservations | Book a trip | [deep link] |

---

## 4. Application Definitions

### web-guest-portal (Guest Portal Website)

**Tech:** React 18, TypeScript, Vite, Tailwind CSS
**Audience:** Public guests — browsing, booking, account management
**Key Screens:**

| Screen | Services Called | User Journey Complexity |
|--------|----------------|------------------------|
| Trip Browser | svc-trip-catalog, svc-trail-management, svc-weather, svc-media-gallery | 4 services |
| Booking Flow | svc-trip-catalog, svc-guest-profiles, svc-reservations, svc-payments | 4 services |
| Guest Profile | svc-guest-profiles, svc-loyalty-rewards, svc-reservations | 3 services |
| Reservation Management | svc-reservations, svc-payments, svc-notifications | 3 services |
| Loyalty Dashboard | svc-loyalty-rewards, svc-guest-profiles | 2 services |
| Waiver Signing | svc-safety-compliance, svc-guest-profiles | 2 services + DocuSign |
| Trip Gallery | svc-media-gallery, svc-reservations | 2 services |

### web-ops-dashboard (Operations Dashboard)

**Tech:** Angular 17, TypeScript, PrimeNG, NgRx
**Audience:** NovaTrek staff — scheduling, check-in management, safety oversight
**Key Screens:**

| Screen | Services Called | User Journey Complexity |
|--------|----------------|------------------------|
| Daily Schedule Board | svc-scheduling-orchestrator, svc-guide-management, svc-weather, svc-trail-management, svc-location-services | 5 services |
| Check-In Station | svc-check-in, svc-reservations, svc-guest-profiles, svc-gear-inventory, svc-safety-compliance | 5 services |
| Guide Assignment | svc-guide-management, svc-scheduling-orchestrator, svc-trail-management | 3 services |
| Safety Incident Board | svc-safety-compliance, svc-guest-profiles, svc-notifications, svc-guide-management | 4 services |
| Inventory Management | svc-gear-inventory, svc-inventory-procurement | 2 services |
| Transport Dispatch | svc-transport-logistics, svc-location-services, svc-reservations | 3 services + Google Maps |
| Analytics Dashboard | svc-analytics, svc-reservations, svc-payments | 3 services |
| Partner Bookings | svc-partner-integrations, svc-reservations, svc-payments | 3 services |

### app-guest-mobile (NovaTrek Adventure App)

**Tech:** React Native 0.74, TypeScript, Expo
**Audience:** Guests — on-trip experience, real-time updates, check-in
**Key Screens:**

| Screen | Services Called | User Journey Complexity |
|--------|----------------|------------------------|
| Self Check-In | svc-check-in, svc-reservations, svc-guest-profiles, svc-safety-compliance, svc-gear-inventory | 5 services |
| Live Trip Map | svc-location-services, svc-trail-management, svc-weather, svc-scheduling-orchestrator | 4 services |
| Photo Upload | svc-media-gallery (+ Object Store), svc-notifications | 2 services + S3 + Google Maps |
| My Reservations | svc-reservations, svc-payments, svc-trip-catalog | 3 services |
| Weather & Trail Alerts | svc-weather, svc-trail-management, svc-notifications | 3 services + OpenWeather |
| Digital Wristband | svc-check-in, svc-gear-inventory | 2 services |
| Earn Loyalty Points | svc-loyalty-rewards, svc-reservations, svc-guest-profiles | 3 services |

---

## 5. Linking Strategy

### A. Application pages link TO microservice pages (deep links)

Every API dependency in an application page links to the specific endpoint section on the microservice page using existing deep-link anchors:

```markdown
[POST /reservations](../microservices/svc-reservations/#post-reservations-create-a-new-reservation)
```

### B. User journey diagrams link TO microservice pages

PlantUML participant boxes for backend services link to their microservice page (same pattern as cross-service calls today):

```plantuml
participant "svc-reservations" as Res [[/microservices/svc-reservations/]]
```

And API calls within the journey link to the specific endpoint:

```plantuml
App -> Res : [[/microservices/svc-reservations/#post-reservations-create-a-new-reservation Create reservation]]
```

### C. Microservice pages link BACK to consuming applications

Add a new section to each generated microservice page: **"Consuming Applications"**

| Application | Screens Using This Service |
|-------------|---------------------------|
| [web-guest-portal](../applications/web-guest-portal/) | Trip Browser, Booking Flow |
| [app-guest-mobile](../applications/app-guest-mobile/) | Self Check-In, My Reservations |

This creates **bidirectional navigation** between frontends and backends.

### D. Application index links TO all three apps

The `applications/index.md` gallery page links to each application page, similar to how `microservices/index.md` links to each service.

### E. Cross-linking between applications

Where user journeys span multiple applications (e.g., guest books on web, checks in on mobile), the application pages cross-link to each other.

---

## 6. Generator Changes

Extend `generate-microservice-pages.py` (or create a companion `generate-application-pages.py`) with:

### New data structures

```python
APPLICATIONS = {
    "web-guest-portal": {
        "title": "NovaTrek Guest Portal",
        "type": "Web",
        "tech": "React 18, TypeScript, Vite, Tailwind CSS",
        "team": "Guest Experience Team",
        "screens": { ... },       # screen name -> list of (svc, method, path) calls
    },
    ...
}

# Reverse index: svc_name -> [(app_name, screen_name), ...]
APP_CONSUMERS = {}   # built from APPLICATIONS at startup
```

### New diagram style

User journey diagrams differ from endpoint diagrams:

- **Actor** is a Person (stick figure), not a Client box
- **Frontend** is a participant (Browser or Mobile device)
- The journey flows through **multiple services sequentially** to fulfill one user action
- External 3rd-party services appear as gray participants (same as today)
- Each step shows the HTTP method + path for traceability

### New section in microservice page generator

After the endpoint diagrams, add:

```markdown
## Consuming Applications

| Application | Type | Screens |
|------------|------|---------|
| [Guest Portal](../applications/web-guest-portal/) | Web | Trip Browser, Booking Flow |
```

---

## 7. Implementation Steps

1. Define `APPLICATIONS` data structure with all screens and their API dependencies
2. Define `APP_CONSUMERS` reverse-index (auto-built from APPLICATIONS)
3. Create `generate-application-pages.py` generator script
4. Generate PlantUML user journey diagrams for each screen
5. Generate application deep-dive pages with screen inventory + journey diagrams + API dependency tables
6. Generate `applications/index.md` gallery page
7. Update microservice page generator to add "Consuming Applications" section using `APP_CONSUMERS`
8. Add `Applications` nav section to `mkdocs.yml`
9. Regenerate all pages (microservices + applications)
10. Build and deploy

---

## 8. Open Questions

- Should user journey diagrams show **every** API call in the flow, or group related calls into a single "integration block"?
- Should the mobile app pages include platform-specific details (iOS vs Android) or stay platform-agnostic?
- Should we add a **System Context (C4 Level 1)** diagram to the portal home page showing all 3 applications, 19 services, and external dependencies in one view?
