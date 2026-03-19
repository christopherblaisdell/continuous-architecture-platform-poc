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
<span class="version-badge">29 Actors &middot; 18 External Systems &middot; 3 Frontend Applications &middot; 5 Humans &middot; 3 Infrastructures</span>

</div>

This catalog lists every actor that interacts with the NovaTrek platform: people, frontend applications, internal microservices, external systems, and infrastructure components. Each card uses the same C4 model shapes and domain color scheme as the architecture diagrams.

---

## Humans

<div class="actor-grid">
<a class="actor-card" href="#adventure-guide" style="--actor-border: #4f46e5; --actor-bg: #E0E7FF;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Ccircle%20cx%3D%2224%22%20cy%3D%2212%22%20r%3D%228%22%20fill%3D%22%23E0E7FF%22%2F%3E%3Cpath%20d%3D%22M8%2044%20C8%2030%2016%2024%2024%2024%20C32%2024%2040%2030%2040%2044%22%20fill%3D%22%23E0E7FF%22%20stroke%3D%22none%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">Adventure Guide</span><span class="actor-desc">Certified outdoor guides who lead adventure trips, manage guest safety, and report incidents.</span><span class="actor-domain">Guide Management</span></a>
<a class="actor-card" href="#guest" style="--actor-border: #7c3aed; --actor-bg: #EDE9FE;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Ccircle%20cx%3D%2224%22%20cy%3D%2212%22%20r%3D%228%22%20fill%3D%22%23EDE9FE%22%2F%3E%3Cpath%20d%3D%22M8%2044%20C8%2030%2016%2024%2024%2024%20C32%2024%2040%2030%2040%2044%22%20fill%3D%22%23EDE9FE%22%20stroke%3D%22none%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">Guest</span><span class="actor-desc">NovaTrek customer who books, checks in for, and participates in adventure trips.</span><span class="actor-domain">Guest Identity</span></a>
<a class="actor-card" href="#operations-staff" style="--actor-border: #2563eb; --actor-bg: #DBEAFE;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Ccircle%20cx%3D%2224%22%20cy%3D%2212%22%20r%3D%228%22%20fill%3D%22%23DBEAFE%22%2F%3E%3Cpath%20d%3D%22M8%2044%20C8%2030%2016%2024%2024%2024%20C32%2024%2040%2030%2040%2044%22%20fill%3D%22%23DBEAFE%22%20stroke%3D%22none%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">Operations Staff</span><span class="actor-desc">On-site NovaTrek employees who manage daily operations including check-in, scheduling, gear assignment, and incident response.</span><span class="actor-domain">Operations</span></a>
<a class="actor-card" href="#software-developer" style="--actor-border: #475569; --actor-bg: #F1F5F9;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Ccircle%20cx%3D%2224%22%20cy%3D%2212%22%20r%3D%228%22%20fill%3D%22%23F1F5F9%22%2F%3E%3Cpath%20d%3D%22M8%2044%20C8%2030%2016%2024%2024%2024%20C32%2024%2040%2030%2040%2044%22%20fill%3D%22%23F1F5F9%22%20stroke%3D%22none%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">Software Developer</span><span class="actor-desc">Implements approved architecture designs in service source code, writes tests, and proposes API contract updates via pull request when implementation reveals contract gaps.</span><span class="actor-domain">Engineering</span></a>
<a class="actor-card" href="#solution-architect" style="--actor-border: #1a2744; --actor-bg: #E2E8F0;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Ccircle%20cx%3D%2224%22%20cy%3D%2212%22%20r%3D%228%22%20fill%3D%22%23E2E8F0%22%2F%3E%3Cpath%20d%3D%22M8%2044%20C8%2030%2016%2024%2024%2024%20C32%2024%2040%2030%2040%2044%22%20fill%3D%22%23E2E8F0%22%20stroke%3D%22none%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">Solution Architect</span><span class="actor-desc">Owns architecture metadata, API contracts, solution designs, decisions, and diagrams. Proposes and documents architectural changes to the NovaTrek platform.</span><span class="actor-domain">Architecture</span></a>
</div>

---

## Frontend Applications

<div class="actor-grid">
<a class="actor-card" href="../applications/app-guest-mobile/" style="--actor-border: #7c3aed; --actor-bg: #EDE9FE;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%2232%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%23EDE9FE%22%20stroke%3D%22%237c3aed%22%20stroke-width%3D%221.5%22%2F%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%228%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%237c3aed%22%20opacity%3D%220.25%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">app-guest-mobile</span><span class="actor-tech">[React Native]</span><span class="actor-desc">Native mobile application for guests to self check-in, view live trip maps, receive weather alerts, upload photos, and earn loyalty points.</span><span class="actor-domain">Guest Identity</span></a>
<a class="actor-card" href="../applications/web-guest-portal/" style="--actor-border: #7c3aed; --actor-bg: #EDE9FE;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%2232%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%23EDE9FE%22%20stroke%3D%22%237c3aed%22%20stroke-width%3D%221.5%22%2F%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%228%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%237c3aed%22%20opacity%3D%220.25%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">web-guest-portal</span><span class="actor-tech">[React SPA]</span><span class="actor-desc">Public-facing web application for guests to browse trips, book reservations, manage profiles, sign waivers, and view trip media.</span><span class="actor-domain">Guest Identity</span></a>
<a class="actor-card" href="../applications/web-ops-dashboard/" style="--actor-border: #2563eb; --actor-bg: #DBEAFE;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%2232%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%23DBEAFE%22%20stroke%3D%22%232563eb%22%20stroke-width%3D%221.5%22%2F%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%228%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%232563eb%22%20opacity%3D%220.25%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">web-ops-dashboard</span><span class="actor-tech">[React SPA]</span><span class="actor-desc">Internal web application for operations staff to manage check-ins, daily schedules, guide assignments, safety incidents, and partner bookings.</span><span class="actor-domain">Operations</span></a>
</div>

---

## Infrastructure

<div class="actor-grid">
<a class="actor-card" href="#api-gateway" style="--actor-border: #374151; --actor-bg: #F3F4F6;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cellipse%20cx%3D%2224%22%20cy%3D%2212%22%20rx%3D%2218%22%20ry%3D%226%22%20fill%3D%22%23F3F4F6%22%20stroke%3D%22%23374151%22%20stroke-width%3D%221.5%22%2F%3E%3Crect%20x%3D%226%22%20y%3D%2212%22%20width%3D%2236%22%20height%3D%2224%22%20fill%3D%22%23F3F4F6%22%20stroke%3D%22%23374151%22%20stroke-width%3D%221.5%22%2F%3E%3Cellipse%20cx%3D%2224%22%20cy%3D%2236%22%20rx%3D%2218%22%20ry%3D%226%22%20fill%3D%22%23F3F4F6%22%20stroke%3D%22%23374151%22%20stroke-width%3D%221.5%22%2F%3E%3Cellipse%20cx%3D%2224%22%20cy%3D%2212%22%20rx%3D%2218%22%20ry%3D%226%22%20fill%3D%22%23F3F4F6%22%20stroke%3D%22none%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">API Gateway</span><span class="actor-tech">[Azure API Management]</span><span class="actor-desc">Central API Gateway that routes all external requests to backend microservices. Handles authentication, rate limiting, and TLS termination.</span><span class="actor-domain">Platform</span></a>
<a class="actor-card" href="#event-bus" style="--actor-border: #374151; --actor-bg: #F3F4F6;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cellipse%20cx%3D%2224%22%20cy%3D%2212%22%20rx%3D%2218%22%20ry%3D%226%22%20fill%3D%22%23F3F4F6%22%20stroke%3D%22%23374151%22%20stroke-width%3D%221.5%22%2F%3E%3Crect%20x%3D%226%22%20y%3D%2212%22%20width%3D%2236%22%20height%3D%2224%22%20fill%3D%22%23F3F4F6%22%20stroke%3D%22%23374151%22%20stroke-width%3D%221.5%22%2F%3E%3Cellipse%20cx%3D%2224%22%20cy%3D%2236%22%20rx%3D%2218%22%20ry%3D%226%22%20fill%3D%22%23F3F4F6%22%20stroke%3D%22%23374151%22%20stroke-width%3D%221.5%22%2F%3E%3Cellipse%20cx%3D%2224%22%20cy%3D%2212%22%20rx%3D%2218%22%20ry%3D%226%22%20fill%3D%22%23F3F4F6%22%20stroke%3D%22none%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">Event Bus</span><span class="actor-tech">[Apache Kafka]</span><span class="actor-desc">Apache Kafka cluster used for asynchronous event-driven communication between microservices. All domain events flow through dedicated Kafka topics.</span><span class="actor-domain">Platform</span></a>
<a class="actor-card" href="#object-store" style="--actor-border: #374151; --actor-bg: #F3F4F6;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cellipse%20cx%3D%2224%22%20cy%3D%2212%22%20rx%3D%2218%22%20ry%3D%226%22%20fill%3D%22%23F3F4F6%22%20stroke%3D%22%23374151%22%20stroke-width%3D%221.5%22%2F%3E%3Crect%20x%3D%226%22%20y%3D%2212%22%20width%3D%2236%22%20height%3D%2224%22%20fill%3D%22%23F3F4F6%22%20stroke%3D%22%23374151%22%20stroke-width%3D%221.5%22%2F%3E%3Cellipse%20cx%3D%2224%22%20cy%3D%2236%22%20rx%3D%2218%22%20ry%3D%226%22%20fill%3D%22%23F3F4F6%22%20stroke%3D%22%23374151%22%20stroke-width%3D%221.5%22%2F%3E%3Cellipse%20cx%3D%2224%22%20cy%3D%2212%22%20rx%3D%2218%22%20ry%3D%226%22%20fill%3D%22%23F3F4F6%22%20stroke%3D%22none%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">Object Store</span><span class="actor-tech">[Azure Blob Storage]</span><span class="actor-desc">Cloud object storage for media assets including trip photos, guide profile images, and waiver documents.</span><span class="actor-domain">Platform</span></a>
</div>

---

## External Systems

<div class="actor-grid">
<a class="actor-card" href="#currency-exchange-api" style="--actor-border: #64748b; --actor-bg: #F1F5F9;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%2232%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%23F1F5F9%22%20stroke%3D%22%2364748b%22%20stroke-width%3D%221.5%22%20stroke-dasharray%3D%224%202%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">Currency Exchange API</span><span class="actor-tech">[REST API]</span><span class="actor-desc">Real-time foreign currency exchange rate provider for converting international guest payments to the base operating currency.</span><span class="actor-domain">Support</span></a>
<a class="actor-card" href="#docusign-api" style="--actor-border: #dc2626; --actor-bg: #FEE2E2;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%2232%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%23FEE2E2%22%20stroke%3D%22%23dc2626%22%20stroke-width%3D%221.5%22%20stroke-dasharray%3D%224%202%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">DocuSign API</span><span class="actor-tech">[DocuSign eSignature REST API]</span><span class="actor-desc">Electronic signature platform used for legally-binding adventure liability waivers and safety acknowledgments.</span><span class="actor-domain">Safety</span></a>
<a class="actor-card" href="#firebase-cloud-messaging" style="--actor-border: #64748b; --actor-bg: #F1F5F9;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%2232%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%23F1F5F9%22%20stroke%3D%22%2364748b%22%20stroke-width%3D%221.5%22%20stroke-dasharray%3D%224%202%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">Firebase Cloud Messaging</span><span class="actor-tech">[Firebase FCM]</span><span class="actor-desc">Push notification delivery service for real-time alerts to guest mobile devices (weather warnings, check-in reminders, schedule changes).</span><span class="actor-domain">Support</span></a>
<a class="actor-card" href="#fleet-gps-tracking-api" style="--actor-border: #0891b2; --actor-bg: #CFFAFE;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%2232%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%23CFFAFE%22%20stroke%3D%22%230891b2%22%20stroke-width%3D%221.5%22%20stroke-dasharray%3D%224%202%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">Fleet GPS Tracking API</span><span class="actor-tech">[REST API / WebSocket]</span><span class="actor-desc">Vehicle telematics and GPS tracking platform providing real-time location, speed, and ETA data for NovaTrek transport fleet vehicles including shuttles, vans, and boats.</span><span class="actor-domain">Logistics</span></a>
<a class="actor-card" href="#fraud-detection-api" style="--actor-border: #64748b; --actor-bg: #F1F5F9;"><span class="actor-pci">PCI</span><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%2232%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%23F1F5F9%22%20stroke%3D%22%2364748b%22%20stroke-width%3D%221.5%22%20stroke-dasharray%3D%224%202%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">Fraud Detection API</span><span class="actor-tech">[REST API]</span><span class="actor-desc">Third-party fraud prevention service that scores payment transactions for risk before authorization.</span><span class="actor-domain">Support</span></a>
<a class="actor-card" href="#google-maps-platform" style="--actor-border: #0891b2; --actor-bg: #CFFAFE;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%2232%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%23CFFAFE%22%20stroke%3D%22%230891b2%22%20stroke-width%3D%221.5%22%20stroke-dasharray%3D%224%202%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">Google Maps Platform</span><span class="actor-tech">[Google Maps REST API]</span><span class="actor-desc">Geolocation and mapping service used for trail positioning, location tracking, and capacity management at adventure sites.</span><span class="actor-domain">Logistics</span></a>
<a class="actor-card" href="#idverify-api" style="--actor-border: #7c3aed; --actor-bg: #EDE9FE;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%2232%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%23EDE9FE%22%20stroke%3D%22%237c3aed%22%20stroke-width%3D%221.5%22%20stroke-dasharray%3D%224%202%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">IDVerify API</span><span class="actor-tech">[REST API]</span><span class="actor-desc">Identity verification service used during check-in to validate guest identity against government-issued IDs.</span><span class="actor-domain">Guest Identity</span></a>
<a class="actor-card" href="#instagram-graph-api" style="--actor-border: #64748b; --actor-bg: #F1F5F9;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%2232%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%23F1F5F9%22%20stroke%3D%22%2364748b%22%20stroke-width%3D%221.5%22%20stroke-dasharray%3D%224%202%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">Instagram Graph API</span><span class="actor-tech">[Instagram Graph REST API]</span><span class="actor-desc">Meta social media API enabling guests to share adventure trip photos and stories directly from the NovaTrek media gallery to their Instagram accounts.</span><span class="actor-domain">Support</span></a>
<a class="actor-card" href="#national-parks-permit-api" style="--actor-border: #d97706; --actor-bg: #FEF3C7;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%2232%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%23FEF3C7%22%20stroke%3D%22%23d97706%22%20stroke-width%3D%221.5%22%20stroke-dasharray%3D%224%202%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">National Parks Permit API</span><span class="actor-tech">[REST API]</span><span class="actor-desc">Government parks and forestry service API for submitting trail access permits, validating permit status, and receiving seasonal trail closure notifications.</span><span class="actor-domain">Product Catalog</span></a>
<a class="actor-card" href="#openweather-api" style="--actor-border: #64748b; --actor-bg: #F1F5F9;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%2232%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%23F1F5F9%22%20stroke%3D%22%2364748b%22%20stroke-width%3D%221.5%22%20stroke-dasharray%3D%224%202%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">OpenWeather API</span><span class="actor-tech">[OpenWeather REST API]</span><span class="actor-desc">Weather data provider delivering current conditions, forecasts, and severe weather alerts for trail and adventure locations.</span><span class="actor-domain">Support</span></a>
<a class="actor-card" href="#payment-gateway" style="--actor-border: #64748b; --actor-bg: #F1F5F9;"><span class="actor-pci">PCI</span><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%2232%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%23F1F5F9%22%20stroke%3D%22%2364748b%22%20stroke-width%3D%221.5%22%20stroke-dasharray%3D%224%202%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">Payment Gateway</span><span class="actor-tech">[Stripe]</span><span class="actor-desc">PCI-certified payment processing gateway that handles credit card authorization, capture, and refund transactions.</span><span class="actor-domain">Support</span></a>
<a class="actor-card" href="#search-and-rescue-dispatch-api" style="--actor-border: #dc2626; --actor-bg: #FEE2E2;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%2232%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%23FEE2E2%22%20stroke%3D%22%23dc2626%22%20stroke-width%3D%221.5%22%20stroke-dasharray%3D%224%202%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">Search and Rescue Dispatch API</span><span class="actor-tech">[REST API]</span><span class="actor-desc">Regional search and rescue coordination API for dispatching emergency response teams to backcountry locations during safety incidents.</span><span class="actor-domain">Safety</span></a>
<a class="actor-card" href="#sendgrid-api" style="--actor-border: #64748b; --actor-bg: #F1F5F9;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%2232%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%23F1F5F9%22%20stroke%3D%22%2364748b%22%20stroke-width%3D%221.5%22%20stroke-dasharray%3D%224%202%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">SendGrid API</span><span class="actor-tech">[SendGrid REST API]</span><span class="actor-desc">Transactional email delivery service for reservation confirmations, waiver requests, and loyalty point notifications.</span><span class="actor-domain">Support</span></a>
<a class="actor-card" href="#snowflake-data-cloud" style="--actor-border: #64748b; --actor-bg: #F1F5F9;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%2232%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%23F1F5F9%22%20stroke%3D%22%2364748b%22%20stroke-width%3D%221.5%22%20stroke-dasharray%3D%224%202%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">Snowflake Data Cloud</span><span class="actor-tech">[Snowflake SQL API]</span><span class="actor-desc">Cloud data warehouse used for business intelligence, analytics aggregation, and historical trend analysis across all NovaTrek domains.</span><span class="actor-domain">Support</span></a>
<a class="actor-card" href="#stripe-api" style="--actor-border: #64748b; --actor-bg: #F1F5F9;"><span class="actor-pci">PCI</span><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%2232%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%23F1F5F9%22%20stroke%3D%22%2364748b%22%20stroke-width%3D%221.5%22%20stroke-dasharray%3D%224%202%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">Stripe API</span><span class="actor-tech">[Stripe REST API]</span><span class="actor-desc">Payment platform API for processing charges, managing payment methods, and handling disputes.</span><span class="actor-domain">Support</span></a>
<a class="actor-card" href="#supplier-procurement-portal" style="--actor-border: #0891b2; --actor-bg: #CFFAFE;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%2232%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%23CFFAFE%22%20stroke%3D%22%230891b2%22%20stroke-width%3D%221.5%22%20stroke-dasharray%3D%224%202%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">Supplier Procurement Portal</span><span class="actor-tech">[REST API]</span><span class="actor-desc">External supplier ordering platform for procuring adventure gear, safety equipment, and consumable supplies from approved NovaTrek vendors.</span><span class="actor-domain">Logistics</span></a>
<a class="actor-card" href="#travel-insurance-api" style="--actor-border: #059669; --actor-bg: #D1FAE5;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%2232%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%23D1FAE5%22%20stroke%3D%22%23059669%22%20stroke-width%3D%221.5%22%20stroke-dasharray%3D%224%202%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">Travel Insurance API</span><span class="actor-tech">[REST API]</span><span class="actor-desc">Third-party travel insurance provider for quoting and binding adventure trip insurance policies based on activity risk level and participant profile.</span><span class="actor-domain">Booking</span></a>
<a class="actor-card" href="#twilio-api" style="--actor-border: #64748b; --actor-bg: #F1F5F9;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Crect%20x%3D%224%22%20y%3D%228%22%20width%3D%2240%22%20height%3D%2232%22%20rx%3D%224%22%20ry%3D%224%22%20fill%3D%22%23F1F5F9%22%20stroke%3D%22%2364748b%22%20stroke-width%3D%221.5%22%20stroke-dasharray%3D%224%202%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">Twilio API</span><span class="actor-tech">[Twilio REST API]</span><span class="actor-desc">SMS and messaging service for check-in reminders, schedule updates, and emergency notifications to guests and guides.</span><span class="actor-domain">Support</span></a>
</div>

---

## Internal Microservices

<div class="actor-grid">
<a class="actor-card" href="../microservices/svc-reservations/" style="--actor-border: #059669; --actor-bg: #D1FAE5;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cpolygon%20points%3D%2224%2C4%2044%2C14%2044%2C34%2024%2C44%204%2C34%204%2C14%22%20fill%3D%22%23D1FAE5%22%20stroke%3D%22%23059669%22%20stroke-width%3D%221.5%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">svc-reservations</span><span class="actor-domain">Booking</span></a>
<a class="actor-card" href="../microservices/svc-partner-integrations/" style="--actor-border: #9333ea; --actor-bg: #F3E8FF;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cpolygon%20points%3D%2224%2C4%2044%2C14%2044%2C34%2024%2C44%204%2C34%204%2C14%22%20fill%3D%22%23F3E8FF%22%20stroke%3D%22%239333ea%22%20stroke-width%3D%221.5%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">svc-partner-integrations</span><span class="actor-domain">External</span></a>
<a class="actor-card" href="../microservices/svc-guest-profiles/" style="--actor-border: #7c3aed; --actor-bg: #EDE9FE;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cpolygon%20points%3D%2224%2C4%2044%2C14%2044%2C34%2024%2C44%204%2C34%204%2C14%22%20fill%3D%22%23EDE9FE%22%20stroke%3D%22%237c3aed%22%20stroke-width%3D%221.5%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">svc-guest-profiles</span><span class="actor-domain">Guest Identity</span></a>
<a class="actor-card" href="../microservices/svc-guide-management/" style="--actor-border: #4f46e5; --actor-bg: #E0E7FF;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cpolygon%20points%3D%2224%2C4%2044%2C14%2044%2C34%2024%2C44%204%2C34%204%2C14%22%20fill%3D%22%23E0E7FF%22%20stroke%3D%22%234f46e5%22%20stroke-width%3D%221.5%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">svc-guide-management</span><span class="actor-domain">Guide Management</span></a>
<a class="actor-card" href="../microservices/svc-gear-inventory/" style="--actor-border: #0891b2; --actor-bg: #CFFAFE;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cpolygon%20points%3D%2224%2C4%2044%2C14%2044%2C34%2024%2C44%204%2C34%204%2C14%22%20fill%3D%22%23CFFAFE%22%20stroke%3D%22%230891b2%22%20stroke-width%3D%221.5%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">svc-gear-inventory</span><span class="actor-domain">Logistics</span></a>
<a class="actor-card" href="../microservices/svc-transport-logistics/" style="--actor-border: #0891b2; --actor-bg: #CFFAFE;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cpolygon%20points%3D%2224%2C4%2044%2C14%2044%2C34%2024%2C44%204%2C34%204%2C14%22%20fill%3D%22%23CFFAFE%22%20stroke%3D%22%230891b2%22%20stroke-width%3D%221.5%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">svc-transport-logistics</span><span class="actor-domain">Logistics</span></a>
<a class="actor-card" href="../microservices/svc-check-in/" style="--actor-border: #2563eb; --actor-bg: #DBEAFE;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cpolygon%20points%3D%2224%2C4%2044%2C14%2044%2C34%2024%2C44%204%2C34%204%2C14%22%20fill%3D%22%23DBEAFE%22%20stroke%3D%22%232563eb%22%20stroke-width%3D%221.5%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">svc-check-in</span><span class="actor-domain">Operations</span></a>
<a class="actor-card" href="../microservices/svc-scheduling-orchestrator/" style="--actor-border: #2563eb; --actor-bg: #DBEAFE;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cpolygon%20points%3D%2224%2C4%2044%2C14%2044%2C34%2024%2C44%204%2C34%204%2C14%22%20fill%3D%22%23DBEAFE%22%20stroke%3D%22%232563eb%22%20stroke-width%3D%221.5%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">svc-scheduling-orchestrator</span><span class="actor-domain">Operations</span></a>
<a class="actor-card" href="../microservices/svc-trail-management/" style="--actor-border: #d97706; --actor-bg: #FEF3C7;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cpolygon%20points%3D%2224%2C4%2044%2C14%2044%2C34%2024%2C44%204%2C34%204%2C14%22%20fill%3D%22%23FEF3C7%22%20stroke%3D%22%23d97706%22%20stroke-width%3D%221.5%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">svc-trail-management</span><span class="actor-domain">Product Catalog</span></a>
<a class="actor-card" href="../microservices/svc-trip-catalog/" style="--actor-border: #d97706; --actor-bg: #FEF3C7;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cpolygon%20points%3D%2224%2C4%2044%2C14%2044%2C34%2024%2C44%204%2C34%204%2C14%22%20fill%3D%22%23FEF3C7%22%20stroke%3D%22%23d97706%22%20stroke-width%3D%221.5%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">svc-trip-catalog</span><span class="actor-domain">Product Catalog</span></a>
<a class="actor-card" href="../microservices/svc-emergency-response/" style="--actor-border: #dc2626; --actor-bg: #FEE2E2;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cpolygon%20points%3D%2224%2C4%2044%2C14%2044%2C34%2024%2C44%204%2C34%204%2C14%22%20fill%3D%22%23FEE2E2%22%20stroke%3D%22%23dc2626%22%20stroke-width%3D%221.5%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">svc-emergency-response</span><span class="actor-domain">Safety</span></a>
<a class="actor-card" href="../microservices/svc-safety-compliance/" style="--actor-border: #dc2626; --actor-bg: #FEE2E2;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cpolygon%20points%3D%2224%2C4%2044%2C14%2044%2C34%2024%2C44%204%2C34%204%2C14%22%20fill%3D%22%23FEE2E2%22%20stroke%3D%22%23dc2626%22%20stroke-width%3D%221.5%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">svc-safety-compliance</span><span class="actor-domain">Safety</span></a>
<a class="actor-card" href="../microservices/svc-wildlife-tracking/" style="--actor-border: #dc2626; --actor-bg: #FEE2E2;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cpolygon%20points%3D%2224%2C4%2044%2C14%2044%2C34%2024%2C44%204%2C34%204%2C14%22%20fill%3D%22%23FEE2E2%22%20stroke%3D%22%23dc2626%22%20stroke-width%3D%221.5%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">svc-wildlife-tracking</span><span class="actor-domain">Safety</span></a>
<a class="actor-card" href="../microservices/svc-analytics/" style="--actor-border: #64748b; --actor-bg: #F1F5F9;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cpolygon%20points%3D%2224%2C4%2044%2C14%2044%2C34%2024%2C44%204%2C34%204%2C14%22%20fill%3D%22%23F1F5F9%22%20stroke%3D%22%2364748b%22%20stroke-width%3D%221.5%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">svc-analytics</span><span class="actor-domain">Support</span></a>
<a class="actor-card" href="../microservices/svc-inventory-procurement/" style="--actor-border: #64748b; --actor-bg: #F1F5F9;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cpolygon%20points%3D%2224%2C4%2044%2C14%2044%2C34%2024%2C44%204%2C34%204%2C14%22%20fill%3D%22%23F1F5F9%22%20stroke%3D%22%2364748b%22%20stroke-width%3D%221.5%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">svc-inventory-procurement</span><span class="actor-domain">Support</span></a>
<a class="actor-card" href="../microservices/svc-location-services/" style="--actor-border: #64748b; --actor-bg: #F1F5F9;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cpolygon%20points%3D%2224%2C4%2044%2C14%2044%2C34%2024%2C44%204%2C34%204%2C14%22%20fill%3D%22%23F1F5F9%22%20stroke%3D%22%2364748b%22%20stroke-width%3D%221.5%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">svc-location-services</span><span class="actor-domain">Support</span></a>
<a class="actor-card" href="../microservices/svc-loyalty-rewards/" style="--actor-border: #64748b; --actor-bg: #F1F5F9;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cpolygon%20points%3D%2224%2C4%2044%2C14%2044%2C34%2024%2C44%204%2C34%204%2C14%22%20fill%3D%22%23F1F5F9%22%20stroke%3D%22%2364748b%22%20stroke-width%3D%221.5%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">svc-loyalty-rewards</span><span class="actor-domain">Support</span></a>
<a class="actor-card" href="../microservices/svc-media-gallery/" style="--actor-border: #64748b; --actor-bg: #F1F5F9;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cpolygon%20points%3D%2224%2C4%2044%2C14%2044%2C34%2024%2C44%204%2C34%204%2C14%22%20fill%3D%22%23F1F5F9%22%20stroke%3D%22%2364748b%22%20stroke-width%3D%221.5%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">svc-media-gallery</span><span class="actor-domain">Support</span></a>
<a class="actor-card" href="../microservices/svc-notifications/" style="--actor-border: #64748b; --actor-bg: #F1F5F9;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cpolygon%20points%3D%2224%2C4%2044%2C14%2044%2C34%2024%2C44%204%2C34%204%2C14%22%20fill%3D%22%23F1F5F9%22%20stroke%3D%22%2364748b%22%20stroke-width%3D%221.5%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">svc-notifications</span><span class="actor-domain">Support</span></a>
<a class="actor-card" href="../microservices/svc-payments/" style="--actor-border: #64748b; --actor-bg: #F1F5F9;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cpolygon%20points%3D%2224%2C4%2044%2C14%2044%2C34%2024%2C44%204%2C34%204%2C14%22%20fill%3D%22%23F1F5F9%22%20stroke%3D%22%2364748b%22%20stroke-width%3D%221.5%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">svc-payments</span><span class="actor-domain">Support</span></a>
<a class="actor-card" href="../microservices/svc-reviews/" style="--actor-border: #64748b; --actor-bg: #F1F5F9;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cpolygon%20points%3D%2224%2C4%2044%2C14%2044%2C34%2024%2C44%204%2C34%204%2C14%22%20fill%3D%22%23F1F5F9%22%20stroke%3D%22%2364748b%22%20stroke-width%3D%221.5%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">svc-reviews</span><span class="actor-domain">Support</span></a>
<a class="actor-card" href="../microservices/svc-weather/" style="--actor-border: #64748b; --actor-bg: #F1F5F9;"><span class="c4-icon" style="background-image:url(&quot;data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cpolygon%20points%3D%2224%2C4%2044%2C14%2044%2C34%2024%2C44%204%2C34%204%2C14%22%20fill%3D%22%23F1F5F9%22%20stroke%3D%22%2364748b%22%20stroke-width%3D%221.5%22%2F%3E%3C%2Fsvg%3E&quot;);"></span><span class="actor-name">svc-weather</span><span class="actor-domain">Support</span></a>
</div>

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

### Currency Exchange API

- **Type:** External System
- **Domain:** Support
- **Description:** Real-time foreign currency exchange rate provider for converting international guest payments to the base operating currency.
- **Technology:** REST API

**Referenced by:**

- [svc-payments](../microservices/svc-payments/)

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

### Fleet GPS Tracking API

- **Type:** External System
- **Domain:** Logistics
- **Description:** Vehicle telematics and GPS tracking platform providing real-time location, speed, and ETA data for NovaTrek transport fleet vehicles including shuttles, vans, and boats.
- **Technology:** REST API / WebSocket

**Referenced by:**

- [svc-transport-logistics](../microservices/svc-transport-logistics/)

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

### Instagram Graph API

- **Type:** External System
- **Domain:** Support
- **Description:** Meta social media API enabling guests to share adventure trip photos and stories directly from the NovaTrek media gallery to their Instagram accounts.
- **Technology:** Instagram Graph REST API

**Referenced by:**

- [svc-media-gallery](../microservices/svc-media-gallery/)

### National Parks Permit API

- **Type:** External System
- **Domain:** Product Catalog
- **Description:** Government parks and forestry service API for submitting trail access permits, validating permit status, and receiving seasonal trail closure notifications.
- **Technology:** REST API

**Referenced by:**

- [svc-trail-management](../microservices/svc-trail-management/)

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

### Search and Rescue Dispatch API

- **Type:** External System
- **Domain:** Safety
- **Description:** Regional search and rescue coordination API for dispatching emergency response teams to backcountry locations during safety incidents.
- **Technology:** REST API

**Referenced by:**

- [svc-emergency-response](../microservices/svc-emergency-response/)

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

### Supplier Procurement Portal

- **Type:** External System
- **Domain:** Logistics
- **Description:** External supplier ordering platform for procuring adventure gear, safety equipment, and consumable supplies from approved NovaTrek vendors.
- **Technology:** REST API

**Referenced by:**

- [svc-inventory-procurement](../microservices/svc-inventory-procurement/)

### Travel Insurance API

- **Type:** External System
- **Domain:** Booking
- **Description:** Third-party travel insurance provider for quoting and binding adventure trip insurance policies based on activity risk level and participant profile.
- **Technology:** REST API

**Referenced by:**

- [svc-reservations](../microservices/svc-reservations/)

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
