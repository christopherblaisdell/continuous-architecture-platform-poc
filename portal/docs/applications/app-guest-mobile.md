---
tags:
  - application
  - app-guest-mobile
  - mobile
---

# app-guest-mobile

**NovaTrek Adventure App** &nbsp;|&nbsp; <span style="background: #05966915; color: #059669; border: 1px solid #05966940; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">:material-cellphone: Mobile</span> &nbsp;|&nbsp; *Guest Experience Team*

> Native mobile app for on-trip guest experiences including self check-in, live maps, photo sharing, and real-time weather and trail alerts.

## :material-language-typescript: Tech Stack

**React Native 0.74, TypeScript, Expo**

---

## :material-cellphone: Screens (7 total)

This application interacts with **14 microservices** across 7 screens.

| Screen | Services | Description |
|--------|----------|-------------|
| [Self Check-In](#self-check-in) | `svc-check-in`, `svc-gear-inventory`, `svc-guest-profiles`, `svc-reservations`, `svc-safety-compliance` | Guest self-service check-in with QR code scan, identity verification, waiver con... |
| [Live Trip Map](#live-trip-map) | `svc-location-services`, `svc-scheduling-orchestrator`, `svc-trail-management`, `svc-weather` | Real-time interactive map showing current trail position, nearby waypoints, weat... |
| [Photo Upload](#photo-upload) | `svc-media-gallery`, `svc-notifications` + Google Maps Platform, Object Store | Capture and upload adventure photos with GPS metadata, auto-tagging, and instant... |
| [My Reservations](#my-reservations) | `svc-payments`, `svc-reservations`, `svc-trip-catalog` | View upcoming and past reservations with trip details, payment history, and modi... |
| [Weather and Trail Alerts](#weather-and-trail-alerts) | `svc-notifications`, `svc-trail-management`, `svc-weather` + OpenWeather API | Push-notification-driven alerts for severe weather, trail closures, and safety a... |
| [Digital Wristband](#digital-wristband) | `svc-check-in`, `svc-gear-inventory` | Display NFC-enabled digital wristband for tap-to-verify at activity stations and... |
| [Earn Loyalty Points](#earn-loyalty-points) | `svc-guest-profiles`, `svc-loyalty-rewards`, `svc-reservations` | View point earnings after trip completion, tier progress, and available redempti... |

---

---

### Self Check-In

> Guest self-service check-in with QR code scan, identity verification, waiver confirmation, and wristband activation.

**API Dependencies:**

| Method | Endpoint | Service | Purpose |
|--------|----------|---------|---------|
| GET | [GET `/reservations/{reservation_id}`](../microservices/svc-reservations/#get-reservationsreservation_id-get-reservation-details) | `svc-reservations` | Lookup reservation by QR |
| GET | [GET `/guests/{guest_id}`](../microservices/svc-guest-profiles/#get-guestsguest_id-get-guest-profile) | `svc-guest-profiles` | Verify guest identity |
| GET | [GET `/waivers`](../microservices/svc-safety-compliance/#get-waivers-list-waivers-by-guest) | `svc-safety-compliance` | Validate waiver status |
| POST | [POST `/check-ins`](../microservices/svc-check-in/#post-check-ins-initiate-check-in-for-a-participant) | `svc-check-in` | Create check-in record |
| GET | [GET `/gear-assignments/{assignment_id}`](../microservices/svc-gear-inventory/#get-gear-assignmentsassignment_id-get-gear-assignment-details) | `svc-gear-inventory` | Confirm gear assignment |

<div style="overflow-x: auto; width: 100%;"><object data="../svg/app-guest-mobile--self-check-in.svg" type="image/svg+xml" style="max-width: 100%;">Self Check-In user journey diagram</object></div>

---

### Live Trip Map

> Real-time interactive map showing current trail position, nearby waypoints, weather overlay, and group location.

**API Dependencies:**

| Method | Endpoint | Service | Purpose |
|--------|----------|---------|---------|
| GET | [GET `/locations`](../microservices/svc-location-services/#get-locations-list-all-locations) | `svc-location-services` | Get nearby locations |
| GET | [GET `/trails/{trail_id}`](../microservices/svc-trail-management/#get-trailstrail_id-get-trail-details) | `svc-trail-management` | Get trail waypoints |
| GET | [GET `/trails/{trail_id}/conditions`](../microservices/svc-trail-management/#get-trailstrail_idconditions-get-current-trail-conditions) | `svc-trail-management` | Get trail conditions |
| GET | [GET `/weather/current`](../microservices/svc-weather/#get-weathercurrent-get-current-weather-conditions) | `svc-weather` | Get current weather |
| GET | [GET `/daily-schedules/{schedule_id}`](../microservices/svc-scheduling-orchestrator/) | `svc-scheduling-orchestrator` | Get group schedule |

<div style="overflow-x: auto; width: 100%;"><object data="../svg/app-guest-mobile--live-trip-map.svg" type="image/svg+xml" style="max-width: 100%;">Live Trip Map user journey diagram</object></div>

---

### Photo Upload

> Capture and upload adventure photos with GPS metadata, auto-tagging, and instant sharing.

**API Dependencies:**

| Method | Endpoint | Service | Purpose |
|--------|----------|---------|---------|
| POST | [POST `/media`](../microservices/svc-media-gallery/#post-media-upload-a-media-item) | `svc-media-gallery` | Upload photo |
| -- | *Object Store* | External | Store binary file |
| -- | *Google Maps Platform* | External | Reverse geocode GPS |
| POST | [POST `/media/{media_id}/share`](../microservices/svc-media-gallery/#post-mediamedia_idshare-create-a-shareable-link-for-a-media-item) | `svc-media-gallery` | Create share link |
| POST | [POST `/notifications`](../microservices/svc-notifications/#post-notifications-send-a-notification) | `svc-notifications` | Send share notification |

<div style="overflow-x: auto; width: 100%;"><object data="../svg/app-guest-mobile--photo-upload.svg" type="image/svg+xml" style="max-width: 100%;">Photo Upload user journey diagram</object></div>

---

### My Reservations

> View upcoming and past reservations with trip details, payment history, and modification options.

**API Dependencies:**

| Method | Endpoint | Service | Purpose |
|--------|----------|---------|---------|
| GET | [GET `/reservations`](../microservices/svc-reservations/#get-reservations-search-reservations) | `svc-reservations` | List my reservations |
| GET | [GET `/trips/{trip_id}`](../microservices/svc-trip-catalog/#get-tripstrip_id-get-trip-details) | `svc-trip-catalog` | Get trip details |
| GET | [GET `/payments/{payment_id}`](../microservices/svc-payments/#get-paymentspayment_id-retrieve-payment-details) | `svc-payments` | Get payment details |

<div style="overflow-x: auto; width: 100%;"><object data="../svg/app-guest-mobile--my-reservations.svg" type="image/svg+xml" style="max-width: 100%;">My Reservations user journey diagram</object></div>

---

### Weather and Trail Alerts

> Push-notification-driven alerts for severe weather, trail closures, and safety advisories.

**API Dependencies:**

| Method | Endpoint | Service | Purpose |
|--------|----------|---------|---------|
| GET | [GET `/weather/alerts`](../microservices/svc-weather/#get-weatheralerts-get-active-weather-alerts-for-a-region) | `svc-weather` | Get weather alerts |
| GET | [GET `/trails/{trail_id}/conditions`](../microservices/svc-trail-management/#get-trailstrail_idconditions-get-current-trail-conditions) | `svc-trail-management` | Get trail closures |
| -- | *OpenWeather API* | External | Fetch severe alerts |
| POST | [POST `/notifications`](../microservices/svc-notifications/#post-notifications-send-a-notification) | `svc-notifications` | Receive push notification |

<div style="overflow-x: auto; width: 100%;"><object data="../svg/app-guest-mobile--weather-and-trail-alerts.svg" type="image/svg+xml" style="max-width: 100%;">Weather and Trail Alerts user journey diagram</object></div>

---

### Digital Wristband

> Display NFC-enabled digital wristband for tap-to-verify at activity stations and equipment pickup.

**API Dependencies:**

| Method | Endpoint | Service | Purpose |
|--------|----------|---------|---------|
| GET | [GET `/check-ins/{check_in_id}`](../microservices/svc-check-in/#get-check-inscheck_in_id-get-check-in-details) | `svc-check-in` | Get check-in status |
| GET | [GET `/gear-assignments/{assignment_id}`](../microservices/svc-gear-inventory/#get-gear-assignmentsassignment_id-get-gear-assignment-details) | `svc-gear-inventory` | Verify gear assignment |

<div style="overflow-x: auto; width: 100%;"><object data="../svg/app-guest-mobile--digital-wristband.svg" type="image/svg+xml" style="max-width: 100%;">Digital Wristband user journey diagram</object></div>

---

### Earn Loyalty Points

> View point earnings after trip completion, tier progress, and available redemption offers.

**API Dependencies:**

| Method | Endpoint | Service | Purpose |
|--------|----------|---------|---------|
| GET | [GET `/members/{guest_id}/balance`](../microservices/svc-loyalty-rewards/#get-membersguest_idbalance-get-loyalty-member-balance-and-tier-info) | `svc-loyalty-rewards` | Get member balance |
| POST | [POST `/members/{guest_id}/earn`](../microservices/svc-loyalty-rewards/#post-membersguest_idearn-award-points-to-a-member) | `svc-loyalty-rewards` | Earn points |
| GET | [GET `/reservations`](../microservices/svc-reservations/#get-reservations-search-reservations) | `svc-reservations` | Get completed bookings |
| GET | [GET `/guests/{guest_id}`](../microservices/svc-guest-profiles/#get-guestsguest_id-get-guest-profile) | `svc-guest-profiles` | Get guest profile |

<div style="overflow-x: auto; width: 100%;"><object data="../svg/app-guest-mobile--earn-loyalty-points.svg" type="image/svg+xml" style="max-width: 100%;">Earn Loyalty Points user journey diagram</object></div>
