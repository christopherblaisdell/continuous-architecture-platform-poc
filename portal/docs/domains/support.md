# Support Domain

**Team:** Various (cross-cutting platform services)  
**Services:** 9  
**Domain color:** #64748b

Cross-cutting platform services including notifications, payments, loyalty rewards, analytics, weather, location services, media gallery, procurement, and reviews.

---

## Topology

<div class="diagram-wrap">
  <a href="../../topology/svg/topology-support.svg" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>
  <object data="../../topology/svg/topology-support.svg" type="image/svg+xml" style="max-width: 100%;">
    Support Service Topology C4 Diagram
  </object>
</div>

---

## Services

| Service | Database Engine | Schema | Tables | API Endpoints |
|---------|----------------|--------|--------|---------------|
| [svc-notifications](../microservices/svc-notifications.md) | PostgreSQL 15 + Valkey 8 | `notifications` | 4 | 6 |
| [svc-payments](../microservices/svc-payments.md) | PostgreSQL 15 | `payments` | 6 | 12 |
| [svc-loyalty-rewards](../microservices/svc-loyalty-rewards.md) | Couchbase 7 | `loyalty` | 4 | 5 |
| [svc-media-gallery](../microservices/svc-media-gallery.md) | PostgreSQL 15 + S3-Compatible Object Store | `media` | 3 | 5 |
| [svc-analytics](../microservices/svc-analytics.md) | Oracle Database 19c | `ANALYTICS` | 6 | 6 |
| [svc-weather](../microservices/svc-weather.md) | Valkey 8 + PostgreSQL 15 | `weather` | 3 | 5 |
| [svc-location-services](../microservices/svc-location-services.md) | PostGIS (PostgreSQL 15) | `locations` | 3 | 6 |
| [svc-inventory-procurement](../microservices/svc-inventory-procurement.md) | PostgreSQL 15 | `procurement` | 6 | 8 |
| [svc-reviews](../microservices/svc-reviews.md) | PostgreSQL 15 | `reviews` | 3 | 10 |

---

## Data Ownership

Every data entity has exactly one owning service. Other services access it read-only through APIs.

| Data Entity | Owning Service | Read Access |
|-------------|---------------|-------------|
| Notification log | [svc-notifications](../microservices/svc-notifications.md) | svc-analytics |
| Payment records | [svc-payments](../microservices/svc-payments.md) | svc-reservations, svc-analytics |
| Loyalty points | [svc-loyalty-rewards](../microservices/svc-loyalty-rewards.md) | svc-guest-profiles (read) |
| Media assets | [svc-media-gallery](../microservices/svc-media-gallery.md) | svc-analytics |
| Analytics events | [svc-analytics](../microservices/svc-analytics.md) | Internal (no external readers) |
| Weather cache | [svc-weather](../microservices/svc-weather.md) | svc-scheduling-orchestrator, svc-trail-management |
| Location data | [svc-location-services](../microservices/svc-location-services.md) | svc-transport-logistics, svc-emergency-response, svc-trail-management |
| Procurement orders | [svc-inventory-procurement](../microservices/svc-inventory-procurement.md) | svc-gear-inventory |
| Guest reviews | [svc-reviews](../microservices/svc-reviews.md) | svc-trip-catalog, svc-analytics |

---

## Data Stores

### svc-notifications

- **Engine:** PostgreSQL 15 + Valkey 8
- **Schema:** `notifications`
- **Tables:** `notifications`, `templates`, `delivery_log`, `channel_preferences`
- **Features:**
    - Valkey queue for async delivery processing
    - Template versioning with rollback support
    - Multi-channel delivery: email, SMS, push, in-app
- **Volume:** ~15,000 notifications/day
- **Backup:** Daily pg_dump, 30-day retention

### svc-payments

- **Engine:** PostgreSQL 15
- **Schema:** `payments`
- **Tables:** `payments`, `refunds`, `payment_methods`, `daily_summaries`, `disputes`, `refund_policy_evaluations`
- **Features:**
    - PCI-DSS compliant token storage (no raw card data)
    - Idempotent payment processing via request keys
    - Double-entry ledger for financial reconciliation
- **Volume:** ~2,500 transactions/day
- **Backup:** Continuous WAL archiving, daily base backup, 7-year retention (financial)

### svc-loyalty-rewards

- **Engine:** Couchbase 7
- **Schema:** `loyalty`
- **Tables:** `members`, `point_transactions`, `tiers`, `redemptions`
- **Features:**
    - Document-oriented member profiles with flexible reward schemas
    - N1QL queries for tier recalculation and point aggregation
    - Sub-document operations for atomic point balance updates
- **Volume:** ~1,000 transactions/day
- **Backup:** XDCR to standby cluster, daily cbbackupmgr

### svc-media-gallery

- **Engine:** PostgreSQL 15 + S3-Compatible Object Store
- **Schema:** `media`
- **Tables:** `media_items`, `share_links`, `albums`
- **Features:**
    - S3-compatible storage for photos and videos
    - Presigned URLs for secure direct upload and download
    - Automatic thumbnail generation on upload
- **Volume:** ~500 uploads/day peak season
- **Backup:** Daily pg_dump, S3 cross-region replication

### svc-analytics

- **Engine:** Oracle Database 19c
- **Schema:** `ANALYTICS`
- **Tables:** `BOOKING_METRICS`, `REVENUE_METRICS`, `UTILIZATION_METRICS`, `SATISFACTION_SCORES`, `SAFETY_METRICS`, `GUIDE_PERFORMANCE`
- **Features:**
    - Oracle Partitioning for time-series data (range partitioning by month)
    - Materialized views with fast refresh for real-time dashboards
    - Oracle Advanced Analytics (DBMS_PREDICTIVE_ANALYTICS) for trend forecasting
- **Volume:** ~50K metric inserts/day (event-driven)
- **Backup:** Oracle RMAN incremental backup, 90-day retention

### svc-weather

- **Engine:** Valkey 8 + PostgreSQL 15
- **Schema:** `weather`
- **Tables:** `weather_stations`, `forecast_cache`, `alert_history`
- **Features:**
    - Valkey TTL cache for current conditions (5-min TTL)
    - External weather API response caching and aggregation
    - Severe weather alert deduplication
- **Volume:** ~10K weather reads/day, ~100 external API fetches/day
- **Backup:** Daily pg_dump, 7-day retention (cache data is ephemeral)

### svc-location-services

- **Engine:** PostGIS (PostgreSQL 15)
- **Schema:** `locations`
- **Tables:** `locations`, `capacity_records`, `operating_hours`
- **Features:**
    - PostGIS geometry for geofencing and proximity queries
    - Real-time capacity tracking with threshold alerts
    - Timezone-aware operating hours management
- **Volume:** ~100 updates/day, ~2K reads/day
- **Backup:** Daily pg_dump, 14-day retention

### svc-inventory-procurement

- **Engine:** PostgreSQL 15
- **Schema:** `procurement`
- **Tables:** `purchase_orders`, `po_line_items`, `suppliers`, `stock_levels`, `stock_adjustments`, `reorder_alerts`
- **Features:**
    - Purchase order approval workflow with state machine
    - Automatic reorder point calculation based on consumption
    - Supplier lead time tracking for delivery estimates
- **Volume:** ~50 POs/day, ~200 stock adjustments/day
- **Backup:** Daily pg_dump, 30-day retention

### svc-reviews

- **Engine:** PostgreSQL 15
- **Schema:** `reviews`
- **Tables:** `reviews`, `review_helpful_votes`, `rating_aggregates`
- **Features:**
    - Reservation-gated review submission (cross-ref svc-reservations)
    - Optimistic locking on review records (_rev field)
    - Pre-computed rating aggregates per trip and per guide
    - Full-text search on review body via tsvector index
- **Volume:** ~500 reviews/day, ~50,000 reads/day
- **Backup:** Daily pg_dump, 30-day retention

---

## Bounded Context Rules

These rules are non-negotiable for this domain.

1. Notification delivery is **multi-channel** (email via SendGrid, SMS via Twilio, push via Firebase)
2. Payment processing integrates with external fraud detection before authorization
3. Analytics events flow via Kafka consumers — [svc-analytics](../microservices/svc-analytics.md) subscribes to all domain events
4. All support services are consumed by other domains but do not own core business data

---

## Cross-Domain Integration

### Outbound (this domain calls)

| Source | Target | Target Domain | Action | Async |
|--------|--------|--------------|--------|-------|
| [svc-loyalty-rewards](../microservices/svc-loyalty-rewards.md) | [svc-reservations](../microservices/svc-reservations.md) | Booking | Verify completed booking | No |
| [svc-loyalty-rewards](../microservices/svc-loyalty-rewards.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Guest Identity | Get member profile | No |
| [svc-inventory-procurement](../microservices/svc-inventory-procurement.md) | [svc-gear-inventory](../microservices/svc-gear-inventory.md) | Logistics | Verify item catalog | No |
| [svc-reviews](../microservices/svc-reviews.md) | [svc-reservations](../microservices/svc-reservations.md) | Booking | Validate reservation exists and is COMPLETED | No |
| [svc-reviews](../microservices/svc-reviews.md) | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Guest Identity | Validate guest identity | No |

### Inbound (called by other domains)

| Source | Source Domain | Target | Action | Async |
|--------|-------------|--------|--------|-------|
| [svc-check-in](../microservices/svc-check-in.md) | Operations | [svc-notifications](../microservices/svc-notifications.md) | Send check-in confirmation | Yes |
| [svc-reservations](../microservices/svc-reservations.md) | Booking | [svc-payments](../microservices/svc-payments.md) | Process deposit payment | No |
| [svc-reservations](../microservices/svc-reservations.md) | Booking | [svc-notifications](../microservices/svc-notifications.md) | Send booking confirmation | Yes |
| [svc-reservations](../microservices/svc-reservations.md) | Booking | [svc-notifications](../microservices/svc-notifications.md) | Send status update | Yes |
| [svc-reservations](../microservices/svc-reservations.md) | Booking | [svc-notifications](../microservices/svc-notifications.md) | Send insurance confirmation | Yes |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | Operations | [svc-weather](../microservices/svc-weather.md) | Get forecast | No |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | Operations | [svc-notifications](../microservices/svc-notifications.md) | Notify assigned guides | Yes |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | Operations | [svc-location-services](../microservices/svc-location-services.md) | Check location capacity | No |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | Operations | [svc-analytics](../microservices/svc-analytics.md) | Log optimization metrics | Yes |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | Operations | [svc-notifications](../microservices/svc-notifications.md) | Notify affected parties | Yes |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | External | [svc-payments](../microservices/svc-payments.md) | Process commission | No |
| [svc-partner-integrations](../microservices/svc-partner-integrations.md) | External | [svc-notifications](../microservices/svc-notifications.md) | Send partner confirmation | Yes |
| [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Guest Identity | [svc-analytics](../microservices/svc-analytics.md) | Get satisfaction scores | No |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Safety | [svc-notifications](../microservices/svc-notifications.md) | Send waiver copy | Yes |
| [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Safety | [svc-notifications](../microservices/svc-notifications.md) | Send safety alert | Yes |
| [svc-transport-logistics](../microservices/svc-transport-logistics.md) | Logistics | [svc-location-services](../microservices/svc-location-services.md) | Validate pickup location | No |
| [svc-transport-logistics](../microservices/svc-transport-logistics.md) | Logistics | [svc-notifications](../microservices/svc-notifications.md) | Send transport details | Yes |
| [svc-trail-management](../microservices/svc-trail-management.md) | Product Catalog | [svc-weather](../microservices/svc-weather.md) | Correlate weather data | No |
| [svc-trail-management](../microservices/svc-trail-management.md) | Product Catalog | [svc-location-services](../microservices/svc-location-services.md) | Get trail coordinates | No |
| [svc-trail-management](../microservices/svc-trail-management.md) | Product Catalog | [svc-notifications](../microservices/svc-notifications.md) | Alert park rangers | Yes |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | Safety | [svc-location-services](../microservices/svc-location-services.md) | Get last known guest GPS position | No |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | Safety | [svc-notifications](../microservices/svc-notifications.md) | Send emergency alerts to staff and guests | Yes |
| [svc-emergency-response](../microservices/svc-emergency-response.md) | Safety | [svc-notifications](../microservices/svc-notifications.md) | Notify dispatched rescue team | Yes |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | Safety | [svc-weather](../microservices/svc-weather.md) | Get current conditions at sighting location | No |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | Safety | [svc-notifications](../microservices/svc-notifications.md) | Alert operations staff and active guides | Yes |

---

## Domain Events

### Events Produced

| Event | Channel | Producer | Summary |
|-------|---------|----------|---------|
| `payment.processed` | `novatrek.support.payment.processed` | [svc-payments](../microservices/svc-payments.md) | Published when a payment is successfully processed |

**Consumers of these events:**

- `payment.processed` → [svc-reservations](../microservices/svc-reservations.md), [svc-notifications](../microservices/svc-notifications.md)

### Events Consumed

| Event | Channel | Producer | Producer Domain | Consuming Service |
|-------|---------|----------|----------------|-------------------|
| `reservation.created` | `novatrek.booking.reservation.created` | [svc-reservations](../microservices/svc-reservations.md) | Booking | [svc-analytics](../microservices/svc-analytics.md) |
| `reservation.status_changed` | `novatrek.booking.reservation.status-changed` | [svc-reservations](../microservices/svc-reservations.md) | Booking | [svc-notifications](../microservices/svc-notifications.md) |
| `reservation.status_changed` | `novatrek.booking.reservation.status-changed` | [svc-reservations](../microservices/svc-reservations.md) | Booking | [svc-analytics](../microservices/svc-analytics.md) |
| `guest.registered` | `novatrek.guest-identity.guest.registered` | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Guest Identity | [svc-loyalty-rewards](../microservices/svc-loyalty-rewards.md) |
| `guest.registered` | `novatrek.guest-identity.guest.registered` | [svc-guest-profiles](../microservices/svc-guest-profiles.md) | Guest Identity | [svc-analytics](../microservices/svc-analytics.md) |
| `checkin.completed` | `novatrek.operations.checkin.completed` | [svc-check-in](../microservices/svc-check-in.md) | Operations | [svc-notifications](../microservices/svc-notifications.md) |
| `checkin.completed` | `novatrek.operations.checkin.completed` | [svc-check-in](../microservices/svc-check-in.md) | Operations | [svc-analytics](../microservices/svc-analytics.md) |
| `schedule.published` | `novatrek.operations.schedule.published` | [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) | Operations | [svc-notifications](../microservices/svc-notifications.md) |
| `payment.processed` | `novatrek.support.payment.processed` | [svc-payments](../microservices/svc-payments.md) | Support | [svc-notifications](../microservices/svc-notifications.md) |
| `incident.reported` | `novatrek.safety.incident.reported` | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Safety | [svc-notifications](../microservices/svc-notifications.md) |
| `incident.reported` | `novatrek.safety.incident.reported` | [svc-safety-compliance](../microservices/svc-safety-compliance.md) | Safety | [svc-analytics](../microservices/svc-analytics.md) |
| `emergency.triggered` | `novatrek.safety.emergency.triggered` | [svc-emergency-response](../microservices/svc-emergency-response.md) | Safety | [svc-notifications](../microservices/svc-notifications.md) |
| `emergency.triggered` | `novatrek.safety.emergency.triggered` | [svc-emergency-response](../microservices/svc-emergency-response.md) | Safety | [svc-analytics](../microservices/svc-analytics.md) |
| `wildlife_alert.issued` | `novatrek.safety.wildlife-alert.issued` | [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | Safety | [svc-notifications](../microservices/svc-notifications.md) |
| `wildlife_alert.issued` | `novatrek.safety.wildlife-alert.issued` | [svc-wildlife-tracking](../microservices/svc-wildlife-tracking.md) | Safety | [svc-analytics](../microservices/svc-analytics.md) |

---

## Business Capabilities

Capabilities served by this domain's services.

| ID | Capability | Status | Description |
|----|-----------|--------|-------------|
| CAP-1.4 | Loyalty and Rewards | IMPLEMENTED | Points earning, tier progression, and reward redemption |
| CAP-1.5 | Guest Communications | IMPLEMENTED | Multi-channel notifications (email, SMS, push) for guest interactions |
| CAP-1.6 | Trip Media and Memories | IMPLEMENTED | Photo and video capture, storage, and sharing for completed adventures |
| CAP-1.7 | Reviews and Feedback | IMPLEMENTED | Guest trip reviews, ratings, and social proof for adventure selection |
| CAP-3.5 | Weather Monitoring and Alerting | IMPLEMENTED | Weather condition tracking, severe weather alerts, and adventure cancellation triggers |
| CAP-4.2 | Procurement and Vendor Management | IMPLEMENTED | Purchase orders, vendor relationships, and supply chain management |
| CAP-4.3 | Location and Capacity Management | IMPLEMENTED | Venue capacity tracking, geospatial boundaries, location metadata |
| CAP-5.1 | Payment Processing | IMPLEMENTED | Payment authorization, capture, and settlement across payment methods |
| CAP-5.3 | Analytics and Business Intelligence | IMPLEMENTED | Operational dashboards, booking trends, revenue analytics |
| CAP-5.4 | Financial Reporting and Reconciliation | PARTIAL | Revenue reporting, payment reconciliation, tax calculation |
| CAP-5.5 | Refund and Dispute Management | IMPLEMENTED | Refund processing, chargeback management, dispute resolution workflows |
| CAP-7.1 | Notification Delivery (Multi-Channel) | IMPLEMENTED | Email, SMS, push notification delivery with template management |
| CAP-7.2 | Geospatial and Location Services | IMPLEMENTED | Geocoding, geofencing, distance calculation, and map tile serving |

---

## Quick Links

- [Domain Topology View](../topology/domain-views.md#support)
- [svc-notifications Microservice Page](../microservices/svc-notifications.md)
- [svc-payments Microservice Page](../microservices/svc-payments.md)
- [svc-loyalty-rewards Microservice Page](../microservices/svc-loyalty-rewards.md)
- [svc-media-gallery Microservice Page](../microservices/svc-media-gallery.md)
- [svc-analytics Microservice Page](../microservices/svc-analytics.md)
- [svc-weather Microservice Page](../microservices/svc-weather.md)
- [svc-location-services Microservice Page](../microservices/svc-location-services.md)
- [svc-inventory-procurement Microservice Page](../microservices/svc-inventory-procurement.md)
- [svc-reviews Microservice Page](../microservices/svc-reviews.md)
- [Event Catalog](../events/index.md)
- [Business Capabilities](../capabilities/index.md)

---

*Generated from `architecture/metadata/` YAML files by `portal/scripts/generate-domain-pages.py`.*
