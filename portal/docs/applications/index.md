---
hide:
  - toc
tags:
  - application
---

<div class="hero" markdown>

# Applications

<p class="subtitle">Frontend Application Architecture for NovaTrek Adventures</p>

<span class="version-badge">3 Applications &middot; 22 Screens</span>

</div>

Each application page provides **user journey sequence diagrams** for every screen, showing the full API call flow from UI through API Gateway to backend microservices, with clickable links to service endpoints and Swagger UI.

---

| Application | Type | Tech Stack | Screens | Page |
|-------------|------|------------|---------|------|
| **NovaTrek Guest Portal**<br><small>`web-guest-portal`</small> | :material-web: Web | React 18 | 7 screens | [:material-arrow-right: Open](web-guest-portal.md){ .md-button } |
| **NovaTrek Operations Dashboard**<br><small>`web-ops-dashboard`</small> | :material-monitor-dashboard: Web | Angular 17 | 8 screens | [:material-arrow-right: Open](web-ops-dashboard.md){ .md-button } |
| **NovaTrek Adventure App**<br><small>`app-guest-mobile`</small> | :material-cellphone: Mobile | React Native 0.74 | 7 screens | [:material-arrow-right: Open](app-guest-mobile.md){ .md-button } |

---

## Service Coverage Matrix

Which microservices are consumed by which applications:

| Service | `web-guest-portal` | `web-ops-dashboard` | `app-guest-mobile` |
|---------|------|------|------|
| [`svc-analytics`](../microservices/svc-analytics/) | -- | 1 screens | -- |
| [`svc-check-in`](../microservices/svc-check-in/) | -- | 1 screens | 2 screens |
| [`svc-gear-inventory`](../microservices/svc-gear-inventory/) | -- | 2 screens | 2 screens |
| [`svc-guest-profiles`](../microservices/svc-guest-profiles/) | 4 screens | 2 screens | 2 screens |
| [`svc-guide-management`](../microservices/svc-guide-management/) | -- | 3 screens | -- |
| [`svc-inventory-procurement`](../microservices/svc-inventory-procurement/) | -- | 1 screens | -- |
| [`svc-location-services`](../microservices/svc-location-services/) | -- | 2 screens | 1 screens |
| [`svc-loyalty-rewards`](../microservices/svc-loyalty-rewards/) | 2 screens | -- | 1 screens |
| [`svc-media-gallery`](../microservices/svc-media-gallery/) | 2 screens | -- | 1 screens |
| [`svc-notifications`](../microservices/svc-notifications/) | 3 screens | 1 screens | 2 screens |
| [`svc-partner-integrations`](../microservices/svc-partner-integrations/) | -- | 1 screens | -- |
| [`svc-payments`](../microservices/svc-payments/) | 2 screens | 2 screens | 1 screens |
| [`svc-reservations`](../microservices/svc-reservations/) | 4 screens | 4 screens | 3 screens |
| [`svc-safety-compliance`](../microservices/svc-safety-compliance/) | 1 screens | 2 screens | 1 screens |
| [`svc-scheduling-orchestrator`](../microservices/svc-scheduling-orchestrator/) | -- | 2 screens | 1 screens |
| [`svc-trail-management`](../microservices/svc-trail-management/) | 1 screens | 2 screens | 2 screens |
| [`svc-transport-logistics`](../microservices/svc-transport-logistics/) | -- | 1 screens | -- |
| [`svc-trip-catalog`](../microservices/svc-trip-catalog/) | 2 screens | -- | 1 screens |
| [`svc-weather`](../microservices/svc-weather/) | 1 screens | 1 screens | 2 screens |
