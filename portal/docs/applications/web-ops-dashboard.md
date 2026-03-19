---
tags:
  - application
  - web-ops-dashboard
  - web
---

# web-ops-dashboard

**NovaTrek Operations Dashboard** &nbsp;|&nbsp; <span style="background: #dc262615; color: #dc2626; border: 1px solid #dc262640; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">:material-monitor-dashboard: Web</span> &nbsp;|&nbsp; *NovaTrek Operations Team*

> Internal staff dashboard for managing daily operations including scheduling, check-ins, safety incidents, inventory, and analytics.

## :material-language-typescript: Tech Stack

**Angular 17, TypeScript, PrimeNG, NgRx**

---

## :material-map: Service Dependencies

<div class="diagram-wrap"><a href="../svg/web-ops-dashboard--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/web-ops-dashboard--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">web-ops-dashboard C4 context diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/applications.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from architecture/metadata/applications.yaml</a>

---

## :material-monitor-dashboard: Screens (8 total)

This application interacts with **16 microservices** across 8 screens.

| Screen | Services | Wireframe | Description |
|--------|----------|-----------|-------------|
| [Daily Schedule Board](#daily-schedule-board) | `svc-guide-management`, `svc-location-services`, `svc-scheduling-orchestrator`, `svc-trail-management`, `svc-weather` | [:material-pencil-ruler: View](wireframes/daily-schedule-board/) | View and manage the day's adventure schedule with guide assignments, weather con... |
| [Check-In Station](#check-in-station) | `svc-check-in`, `svc-gear-inventory`, `svc-guest-profiles`, `svc-reservations`, `svc-safety-compliance` | [:material-pencil-ruler: View](wireframes/check-in-station/) | Staff-assisted check-in workflow: verify reservation, validate identity, check w... |
| [Guide Assignment](#guide-assignment) | `svc-guide-management`, `svc-scheduling-orchestrator`, `svc-trail-management` | [:material-pencil-ruler: View](wireframes/guide-assignment/) | Assign guides to scheduled adventures based on certification, availability, and ... |
| [Safety Incident Board](#safety-incident-board) | `svc-guest-profiles`, `svc-guide-management`, `svc-notifications`, `svc-safety-compliance` | [:material-pencil-ruler: View](wireframes/safety-incident-board/) | Log and manage safety incidents with guest contact, guide notification, and regu... |
| [Inventory Management](#inventory-management) | `svc-gear-inventory`, `svc-inventory-procurement` | [:material-pencil-ruler: View](wireframes/inventory-management/) | Track gear inventory levels, manage assignments, and create procurement orders.... |
| [Transport Dispatch](#transport-dispatch) | `svc-location-services`, `svc-reservations`, `svc-transport-logistics` + Google Maps Platform | [:material-pencil-ruler: View](wireframes/transport-dispatch/) | Coordinate guest transport with route optimization, vehicle assignment, and real... |
| [Analytics Dashboard](#analytics-dashboard) | `svc-analytics`, `svc-payments`, `svc-reservations` + Snowflake Data Cloud | [:material-pencil-ruler: View](wireframes/analytics-dashboard/) | Business intelligence views for booking trends, revenue, utilization, and guest ... |
| [Partner Bookings](#partner-bookings) | `svc-partner-integrations`, `svc-payments`, `svc-reservations` | [:material-pencil-ruler: View](wireframes/partner-bookings/) | Manage partner-originated bookings, commission tracking, and reconciliation.... |

---

---

### Daily Schedule Board

> View and manage the day's adventure schedule with guide assignments, weather conditions, and trail status.

:material-pencil-ruler: **[View Wireframe](wireframes/daily-schedule-board/)**

**API Dependencies:**

| Method | Endpoint | Service | Purpose |
|--------|----------|---------|---------|
| GET | [GET `/schedule-optimization`](../../microservices/svc-scheduling-orchestrator/#get-schedule-optimization-run-synchronous-schedule-optimization) | `svc-scheduling-orchestrator` | Get daily schedules |
| GET | [GET `/guides/available`](../../microservices/svc-guide-management/#get-guidesavailable-find-available-guides-for-a-date-activity-and-region) | `svc-guide-management` | Get available guides |
| GET | [GET `/weather/forecast`](../../microservices/svc-weather/#get-weatherforecast-get-weather-forecast) | `svc-weather` | Get weather forecast |
| GET | [GET `/trails/{trail_id}/conditions`](../../microservices/svc-trail-management/#get-trailstrail_idconditions-get-current-trail-conditions) | `svc-trail-management` | Get trail conditions |
| GET | [GET `/locations/{location_id}/capacity`](../../microservices/svc-location-services/#get-locationslocation_idcapacity-get-current-capacity-utilization) | `svc-location-services` | Get location capacity |

<div class="diagram-wrap"><a href="../svg/web-ops-dashboard--daily-schedule-board.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/web-ops-dashboard--daily-schedule-board.svg" type="image/svg+xml" style="max-width: 100%;">Daily Schedule Board user journey diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/applications.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from architecture/metadata/applications.yaml</a>

---

### Check-In Station

> Staff-assisted check-in workflow: verify reservation, validate identity, check waivers, assign gear, and issue wristband.

:material-pencil-ruler: **[View Wireframe](wireframes/check-in-station/)**

**API Dependencies:**

| Method | Endpoint | Service | Purpose |
|--------|----------|---------|---------|
| GET | [GET `/reservations/{reservation_id}`](../../microservices/svc-reservations/#get-reservationsreservation_id-get-reservation-details) | `svc-reservations` | Lookup reservation |
| GET | [GET `/guests/{guest_id}`](../../microservices/svc-guest-profiles/#get-guestsguest_id-get-guest-profile) | `svc-guest-profiles` | Verify guest identity |
| GET | [GET `/waivers`](../../microservices/svc-safety-compliance/#get-waivers-list-waivers-by-guest) | `svc-safety-compliance` | Check waiver status |
| POST | [POST `/check-ins`](../../microservices/svc-check-in/#post-check-ins-initiate-check-in-for-a-participant) | `svc-check-in` | Create check-in |
| POST | [POST `/gear-assignments`](../../microservices/svc-gear-inventory/#post-gear-assignments-assign-gear-to-a-participant) | `svc-gear-inventory` | Assign gear package |

<div class="diagram-wrap"><a href="../svg/web-ops-dashboard--check-in-station.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/web-ops-dashboard--check-in-station.svg" type="image/svg+xml" style="max-width: 100%;">Check-In Station user journey diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/applications.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from architecture/metadata/applications.yaml</a>

---

### Guide Assignment

> Assign guides to scheduled adventures based on certification, availability, and guest preferences.

:material-pencil-ruler: **[View Wireframe](wireframes/guide-assignment/)**

**API Dependencies:**

| Method | Endpoint | Service | Purpose |
|--------|----------|---------|---------|
| GET | [GET `/guides`](../../microservices/svc-guide-management/#get-guides-search-guides-with-filters) | `svc-guide-management` | List certified guides |
| GET | [GET `/guides/{guide_id}/availability`](../../microservices/svc-guide-management/#get-guidesguide_idavailability-get-guide-availability-windows) | `svc-guide-management` | Check availability |
| POST | [POST `/schedule-requests`](../../microservices/svc-scheduling-orchestrator/#post-schedule-requests-request-optimal-schedule-for-a-trip) | `svc-scheduling-orchestrator` | Submit schedule request |
| GET | [GET `/trails/{trail_id}`](../../microservices/svc-trail-management/#get-trailstrail_id-get-trail-details) | `svc-trail-management` | Verify trail status |

<div class="diagram-wrap"><a href="../svg/web-ops-dashboard--guide-assignment.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/web-ops-dashboard--guide-assignment.svg" type="image/svg+xml" style="max-width: 100%;">Guide Assignment user journey diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/applications.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from architecture/metadata/applications.yaml</a>

---

### Safety Incident Board

> Log and manage safety incidents with guest contact, guide notification, and regulatory reporting.

:material-pencil-ruler: **[View Wireframe](wireframes/safety-incident-board/)**

**API Dependencies:**

| Method | Endpoint | Service | Purpose |
|--------|----------|---------|---------|
| GET | [GET `/incidents/{incident_id}`](../../microservices/svc-safety-compliance/#get-incidentsincident_id-get-an-incident-report) | `svc-safety-compliance` | List active incidents |
| POST | [POST `/incidents`](../../microservices/svc-safety-compliance/#post-incidents-file-an-incident-report) | `svc-safety-compliance` | Log new incident |
| GET | [GET `/guests/{guest_id}`](../../microservices/svc-guest-profiles/#get-guestsguest_id-get-guest-profile) | `svc-guest-profiles` | Get guest contact info |
| GET | [GET `/guides/{guide_id}`](../../microservices/svc-guide-management/#get-guidesguide_id-get-guide-by-id) | `svc-guide-management` | Get assigned guide |
| POST | [POST `/notifications`](../../microservices/svc-notifications/#post-notifications-send-a-notification) | `svc-notifications` | Send safety alerts |

<div class="diagram-wrap"><a href="../svg/web-ops-dashboard--safety-incident-board.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/web-ops-dashboard--safety-incident-board.svg" type="image/svg+xml" style="max-width: 100%;">Safety Incident Board user journey diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/applications.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from architecture/metadata/applications.yaml</a>

---

### Inventory Management

> Track gear inventory levels, manage assignments, and create procurement orders.

:material-pencil-ruler: **[View Wireframe](wireframes/inventory-management/)**

**API Dependencies:**

| Method | Endpoint | Service | Purpose |
|--------|----------|---------|---------|
| GET | [GET `/gear-items`](../../microservices/svc-gear-inventory/#get-gear-items-search-gear-inventory) | `svc-gear-inventory` | Get inventory levels |
| GET | [GET `/gear-assignments/{assignment_id}`](../../microservices/svc-gear-inventory/#get-gear-assignmentsassignment_id-get-gear-assignment-details) | `svc-gear-inventory` | Check gear assignments |
| POST | [POST `/purchase-orders`](../../microservices/svc-inventory-procurement/#post-purchase-orders-create-a-new-purchase-order) | `svc-inventory-procurement` | Create purchase order |

<div class="diagram-wrap"><a href="../svg/web-ops-dashboard--inventory-management.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/web-ops-dashboard--inventory-management.svg" type="image/svg+xml" style="max-width: 100%;">Inventory Management user journey diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/applications.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from architecture/metadata/applications.yaml</a>

---

### Transport Dispatch

> Coordinate guest transport with route optimization, vehicle assignment, and real-time tracking.

:material-pencil-ruler: **[View Wireframe](wireframes/transport-dispatch/)**

**API Dependencies:**

| Method | Endpoint | Service | Purpose |
|--------|----------|---------|---------|
| GET | [GET `/transport-requests/{request_id}`](../../microservices/svc-transport-logistics/#get-transport-requestsrequest_id-get-transport-request-details) | `svc-transport-logistics` | List transport requests |
| POST | [POST `/transport-requests`](../../microservices/svc-transport-logistics/#post-transport-requests-request-transport-for-a-reservation) | `svc-transport-logistics` | Create transport request |
| GET | [GET `/locations/{location_id}`](../../microservices/svc-location-services/#get-locationslocation_id-get-location-details) | `svc-location-services` | Get pickup locations |
| GET | [GET `/reservations/{reservation_id}`](../../microservices/svc-reservations/#get-reservationsreservation_id-get-reservation-details) | `svc-reservations` | Get booking details |
| -- | *Google Maps Platform* | External | Calculate optimal route |

<div class="diagram-wrap"><a href="../svg/web-ops-dashboard--transport-dispatch.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/web-ops-dashboard--transport-dispatch.svg" type="image/svg+xml" style="max-width: 100%;">Transport Dispatch user journey diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/applications.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from architecture/metadata/applications.yaml</a>

---

### Analytics Dashboard

> Business intelligence views for booking trends, revenue, utilization, and guest satisfaction.

:material-pencil-ruler: **[View Wireframe](wireframes/analytics-dashboard/)**

**API Dependencies:**

| Method | Endpoint | Service | Purpose |
|--------|----------|---------|---------|
| GET | [GET `/analytics/bookings`](../../microservices/svc-analytics/#get-analyticsbookings-get-booking-analytics-for-a-period) | `svc-analytics` | Get booking metrics |
| GET | [GET `/reservations`](../../microservices/svc-reservations/#get-reservations-search-reservations) | `svc-reservations` | Get reservation stats |
| GET | [GET `/payments/daily-summary`](../../microservices/svc-payments/#get-paymentsdaily-summary-get-daily-payment-summary) | `svc-payments` | Get revenue summary |
| -- | *Snowflake Data Cloud* | External | Query data warehouse |

<div class="diagram-wrap"><a href="../svg/web-ops-dashboard--analytics-dashboard.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/web-ops-dashboard--analytics-dashboard.svg" type="image/svg+xml" style="max-width: 100%;">Analytics Dashboard user journey diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/applications.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from architecture/metadata/applications.yaml</a>

---

### Partner Bookings

> Manage partner-originated bookings, commission tracking, and reconciliation.

:material-pencil-ruler: **[View Wireframe](wireframes/partner-bookings/)**

**API Dependencies:**

| Method | Endpoint | Service | Purpose |
|--------|----------|---------|---------|
| GET | [GET `/partner-bookings/{booking_id}`](../../microservices/svc-partner-integrations/#get-partner-bookingsbooking_id-get-partner-booking-details) | `svc-partner-integrations` | List partner bookings |
| POST | [POST `/partner-bookings/{booking_id}/confirm`](../../microservices/svc-partner-integrations/#post-partner-bookingsbooking_idconfirm-confirm-a-pending-partner-booking) | `svc-partner-integrations` | Confirm booking |
| GET | [GET `/reservations/{reservation_id}`](../../microservices/svc-reservations/#get-reservationsreservation_id-get-reservation-details) | `svc-reservations` | Get reservation details |
| GET | [GET `/payments/{payment_id}`](../../microservices/svc-payments/#get-paymentspayment_id-retrieve-payment-details) | `svc-payments` | Get payment status |

<div class="diagram-wrap"><a href="../svg/web-ops-dashboard--partner-bookings.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/web-ops-dashboard--partner-bookings.svg" type="image/svg+xml" style="max-width: 100%;">Partner Bookings user journey diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/applications.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from architecture/metadata/applications.yaml</a>
