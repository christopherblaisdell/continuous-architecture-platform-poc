---
tags:
  - application
  - web-guest-portal
  - web
---

# web-guest-portal

**NovaTrek Guest Portal** &nbsp;|&nbsp; <span style="background: #2563eb15; color: #2563eb; border: 1px solid #2563eb40; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">:material-web: Web</span> &nbsp;|&nbsp; *Guest Experience Team*

> Public-facing website where guests browse adventures, make reservations, manage their profiles, and track loyalty rewards.

## :material-language-typescript: Tech Stack

**React 18, TypeScript, Vite, Tailwind CSS**

---

## :material-map: Service Dependencies

<div class="diagram-wrap"><a href="../svg/web-guest-portal--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/web-guest-portal--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">web-guest-portal C4 context diagram</object></div>

---

## :material-web: Screens (7 total)

This application interacts with **10 microservices** across 7 screens.

| Screen | Services | Description |
|--------|----------|-------------|
| [Trip Browser](#trip-browser) | `svc-media-gallery`, `svc-trail-management`, `svc-trip-catalog`, `svc-weather` | Search and explore available adventures with trail info, weather forecasts, and ... |
| [Booking Flow](#booking-flow) | `svc-guest-profiles`, `svc-payments`, `svc-reservations`, `svc-trip-catalog` + Stripe API | End-to-end reservation flow from trip selection through payment confirmation.... |
| [Guest Profile](#guest-profile) | `svc-guest-profiles`, `svc-loyalty-rewards`, `svc-reservations` | View and edit guest profile, certifications, past adventures, and loyalty tier.... |
| [Reservation Management](#reservation-management) | `svc-notifications`, `svc-payments`, `svc-reservations` | View, modify, or cancel existing reservations and process refunds.... |
| [Loyalty Dashboard](#loyalty-dashboard) | `svc-guest-profiles`, `svc-loyalty-rewards` | View loyalty points balance, tier status, transaction history, and available rew... |
| [Waiver Signing](#waiver-signing) | `svc-guest-profiles`, `svc-notifications`, `svc-safety-compliance` + DocuSign API | Review and digitally sign safety waivers before trip departure.... |
| [Trip Gallery](#trip-gallery) | `svc-media-gallery`, `svc-notifications`, `svc-reservations` | Browse and share photos and videos from past adventures.... |

---

---

### Trip Browser

> Search and explore available adventures with trail info, weather forecasts, and photo galleries.

**API Dependencies:**

| Method | Endpoint | Service | Purpose |
|--------|----------|---------|---------|
| GET | [GET `/trips`](../../microservices/svc-trip-catalog/#get-trips-search-trips-with-filters) | `svc-trip-catalog` | Search available trips |
| GET | [GET `/trips/{trip_id}`](../../microservices/svc-trip-catalog/#get-tripstrip_id-get-trip-details) | `svc-trip-catalog` | Get trip details |
| GET | [GET `/trails/{trail_id}/conditions`](../../microservices/svc-trail-management/#get-trailstrail_idconditions-get-current-trail-conditions) | `svc-trail-management` | Get trail conditions |
| GET | [GET `/weather/forecast`](../../microservices/svc-weather/#get-weatherforecast-get-weather-forecast) | `svc-weather` | Get weather forecast |
| GET | [GET `/media`](../../microservices/svc-media-gallery/#get-media-list-media-by-reservation-or-trip) | `svc-media-gallery` | Load trip photos |

<div class="diagram-wrap"><a href="../svg/web-guest-portal--trip-browser.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/web-guest-portal--trip-browser.svg" type="image/svg+xml" style="max-width: 100%;">Trip Browser user journey diagram</object></div>

---

### Booking Flow

> End-to-end reservation flow from trip selection through payment confirmation.

**API Dependencies:**

| Method | Endpoint | Service | Purpose |
|--------|----------|---------|---------|
| GET | [GET `/trips/{trip_id}`](../../microservices/svc-trip-catalog/#get-tripstrip_id-get-trip-details) | `svc-trip-catalog` | Check trip availability |
| GET | [GET `/guests/{guest_id}`](../../microservices/svc-guest-profiles/#get-guestsguest_id-get-guest-profile) | `svc-guest-profiles` | Get guest profile |
| POST | [POST `/reservations`](../../microservices/svc-reservations/#post-reservations-create-a-new-reservation) | `svc-reservations` | Create reservation |
| POST | [POST `/payments`](../../microservices/svc-payments/#post-payments-process-a-payment) | `svc-payments` | Process payment |
| -- | *Stripe API* | External | Charge card |

<div class="diagram-wrap"><a href="../svg/web-guest-portal--booking-flow.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/web-guest-portal--booking-flow.svg" type="image/svg+xml" style="max-width: 100%;">Booking Flow user journey diagram</object></div>

---

### Guest Profile

> View and edit guest profile, certifications, past adventures, and loyalty tier.

**API Dependencies:**

| Method | Endpoint | Service | Purpose |
|--------|----------|---------|---------|
| GET | [GET `/guests/{guest_id}`](../../microservices/svc-guest-profiles/#get-guestsguest_id-get-guest-profile) | `svc-guest-profiles` | Get guest profile |
| GET | [GET `/guests/{guest_id}/adventure-history`](../../microservices/svc-guest-profiles/#get-guestsguest_idadventure-history-get-guest-adventure-history) | `svc-guest-profiles` | Get adventure history |
| GET | [GET `/members/{guest_id}/balance`](../../microservices/svc-loyalty-rewards/#get-membersguest_idbalance-get-loyalty-member-balance-and-tier-info) | `svc-loyalty-rewards` | Get loyalty balance |
| GET | [GET `/reservations`](../../microservices/svc-reservations/#get-reservations-search-reservations) | `svc-reservations` | Get upcoming bookings |

<div class="diagram-wrap"><a href="../svg/web-guest-portal--guest-profile.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/web-guest-portal--guest-profile.svg" type="image/svg+xml" style="max-width: 100%;">Guest Profile user journey diagram</object></div>

---

### Reservation Management

> View, modify, or cancel existing reservations and process refunds.

**API Dependencies:**

| Method | Endpoint | Service | Purpose |
|--------|----------|---------|---------|
| GET | [GET `/reservations`](../../microservices/svc-reservations/#get-reservations-search-reservations) | `svc-reservations` | List reservations |
| GET | [GET `/reservations/{reservation_id}`](../../microservices/svc-reservations/#get-reservationsreservation_id-get-reservation-details) | `svc-reservations` | Get reservation details |
| PUT | [PUT `/reservations/{reservation_id}/status`](../../microservices/svc-reservations/#put-reservationsreservation_idstatus-transition-reservation-status) | `svc-reservations` | Update reservation status |
| POST | [POST `/payments/{payment_id}/refund`](../../microservices/svc-payments/#post-paymentspayment_idrefund-initiate-a-refund) | `svc-payments` | Process refund |
| POST | [POST `/notifications`](../../microservices/svc-notifications/#post-notifications-send-a-notification) | `svc-notifications` | Send cancellation notice |

<div class="diagram-wrap"><a href="../svg/web-guest-portal--reservation-management.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/web-guest-portal--reservation-management.svg" type="image/svg+xml" style="max-width: 100%;">Reservation Management user journey diagram</object></div>

---

### Loyalty Dashboard

> View loyalty points balance, tier status, transaction history, and available rewards.

**API Dependencies:**

| Method | Endpoint | Service | Purpose |
|--------|----------|---------|---------|
| GET | [GET `/members/{guest_id}/balance`](../../microservices/svc-loyalty-rewards/#get-membersguest_idbalance-get-loyalty-member-balance-and-tier-info) | `svc-loyalty-rewards` | Get member balance |
| GET | [GET `/members/{guest_id}/transactions`](../../microservices/svc-loyalty-rewards/#get-membersguest_idtransactions-list-point-transactions-for-a-member) | `svc-loyalty-rewards` | Get transaction history |
| GET | [GET `/guests/{guest_id}`](../../microservices/svc-guest-profiles/#get-guestsguest_id-get-guest-profile) | `svc-guest-profiles` | Get guest profile |

<div class="diagram-wrap"><a href="../svg/web-guest-portal--loyalty-dashboard.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/web-guest-portal--loyalty-dashboard.svg" type="image/svg+xml" style="max-width: 100%;">Loyalty Dashboard user journey diagram</object></div>

---

### Waiver Signing

> Review and digitally sign safety waivers before trip departure.

**API Dependencies:**

| Method | Endpoint | Service | Purpose |
|--------|----------|---------|---------|
| GET | [GET `/waivers`](../../microservices/svc-safety-compliance/#get-waivers-list-waivers-by-guest) | `svc-safety-compliance` | Get required waivers |
| GET | [GET `/guests/{guest_id}`](../../microservices/svc-guest-profiles/#get-guestsguest_id-get-guest-profile) | `svc-guest-profiles` | Get guest profile |
| POST | [POST `/waivers`](../../microservices/svc-safety-compliance/#post-waivers-guest-signs-a-safety-waiver) | `svc-safety-compliance` | Submit signed waiver |
| -- | *DocuSign API* | External | Verify digital signature |
| POST | [POST `/notifications`](../../microservices/svc-notifications/#post-notifications-send-a-notification) | `svc-notifications` | Send waiver copy |

<div class="diagram-wrap"><a href="../svg/web-guest-portal--waiver-signing.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/web-guest-portal--waiver-signing.svg" type="image/svg+xml" style="max-width: 100%;">Waiver Signing user journey diagram</object></div>

---

### Trip Gallery

> Browse and share photos and videos from past adventures.

**API Dependencies:**

| Method | Endpoint | Service | Purpose |
|--------|----------|---------|---------|
| GET | [GET `/media`](../../microservices/svc-media-gallery/#get-media-list-media-by-reservation-or-trip) | `svc-media-gallery` | List trip media |
| GET | [GET `/reservations/{reservation_id}`](../../microservices/svc-reservations/#get-reservationsreservation_id-get-reservation-details) | `svc-reservations` | Get reservation details |
| POST | [POST `/media/{media_id}/share`](../../microservices/svc-media-gallery/#post-mediamedia_idshare-create-a-shareable-link-for-a-media-item) | `svc-media-gallery` | Create share link |
| POST | [POST `/notifications`](../../microservices/svc-notifications/#post-notifications-send-a-notification) | `svc-notifications` | Send share notification |

<div class="diagram-wrap"><a href="../svg/web-guest-portal--trip-gallery.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/web-guest-portal--trip-gallery.svg" type="image/svg+xml" style="max-width: 100%;">Trip Gallery user journey diagram</object></div>
