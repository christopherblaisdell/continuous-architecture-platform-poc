#!/usr/bin/env python3
"""Generate Microservice Pages for the NovaTrek Architecture Portal.

Creates a deep-dive page for each of the 19 NovaTrek microservices with:
  - Service metadata and description
  - Data store documentation
  - PlantUML sequence diagrams for EVERY endpoint (rendered as clickable SVGs)
  - Direct links to Swagger UI for each endpoint
  - Cross-service integration flows where applicable

Usage:
    python3 portal/scripts/generate-microservice-pages.py
"""

import os
import re
import subprocess
import unicodedata
import yaml
from urllib.parse import quote

# Paths
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPECS_DIR = os.path.join(WORKSPACE_ROOT, "portal", "docs", "specs")
OUTPUT_DIR = os.path.join(WORKSPACE_ROOT, "portal", "docs", "microservices")
PUML_DIR = os.path.join(OUTPUT_DIR, "puml")
SVG_DIR = os.path.join(OUTPUT_DIR, "svg")

# Domain Configuration
DOMAINS = {
    "Operations": {
        "color": "#2563eb",
        "services": ["svc-check-in", "svc-scheduling-orchestrator"],
    },
    "Guest Identity": {
        "color": "#7c3aed",
        "services": ["svc-guest-profiles"],
    },
    "Booking": {
        "color": "#059669",
        "services": ["svc-reservations"],
    },
    "Product Catalog": {
        "color": "#d97706",
        "services": ["svc-trip-catalog", "svc-trail-management"],
    },
    "Safety": {
        "color": "#dc2626",
        "services": ["svc-safety-compliance"],
    },
    "Logistics": {
        "color": "#0891b2",
        "services": ["svc-transport-logistics", "svc-gear-inventory"],
    },
    "Guide Management": {
        "color": "#4f46e5",
        "services": ["svc-guide-management"],
    },
    "External": {
        "color": "#9333ea",
        "services": ["svc-partner-integrations"],
    },
    "Support": {
        "color": "#64748b",
        "services": [
            "svc-notifications", "svc-payments", "svc-loyalty-rewards",
            "svc-media-gallery", "svc-analytics", "svc-weather",
            "svc-location-services", "svc-inventory-procurement",
        ],
    },
}

ALL_SERVICES = set()
for _info in DOMAINS.values():
    ALL_SERVICES.update(_info["services"])

LABEL_TO_SVC = {
    "Reservations": "svc-reservations",
    "Guest Profiles": "svc-guest-profiles",
    "Trip Catalog": "svc-trip-catalog",
    "Trail Mgmt": "svc-trail-management",
    "Guide Mgmt": "svc-guide-management",
    "Weather Svc": "svc-weather",
    "Location Svc": "svc-location-services",
    "Gear Inventory": "svc-gear-inventory",
    "Payments Svc": "svc-payments",
    "Notifications": "svc-notifications",
    "Safety Compliance": "svc-safety-compliance",
    "Analytics": "svc-analytics",
}

# PCI DSS Compliance Configuration
PCI_SERVICES = {"svc-payments"}  # Services operating within PCI compliance scope
PCI_EXTERNALS = {"Payment Gateway", "Stripe API", "Fraud Detection API"}
# Directional pairs where PCI-sensitive data (card numbers, tokens) flows
PCI_DATA_FLOWS = {
    ("svc-reservations", "svc-payments"),
    ("svc-partner-integrations", "svc-payments"),
    ("svc-loyalty-rewards", "svc-payments"),
    ("svc-inventory-procurement", "svc-payments"),
    ("svc-payments", "Payment Gateway"),
    ("svc-payments", "Stripe API"),
    ("svc-payments", "Fraud Detection API"),
}

def is_pci_flow(from_name, to_name):
    """Check whether a relationship carries PCI-sensitive data."""
    return (from_name, to_name) in PCI_DATA_FLOWS

DATA_STORES = {
    "svc-check-in": {
        "engine": "PostgreSQL 15",
        "schema": "checkin",
        "tables": ["check_ins", "gear_verifications", "wristband_assignments"],
        "features": [
            "Indexes on reservation_id and check_in_date",
            "TTL-based cleanup of stale check-ins (older than 24h)",
            "Composite unique constraint on (reservation_id, participant_id)",
        ],
        "volume": "~5,000 check-ins/day peak season",
    },
    "svc-reservations": {
        "engine": "PostgreSQL 15",
        "schema": "reservations",
        "tables": ["reservations", "participants", "status_history"],
        "features": [
            "Optimistic locking via _rev field",
            "Composite index on (guest_id, trip_date)",
            "Monthly partitioning by reservation_date",
        ],
        "volume": "~2,000 new reservations/day",
    },
    "svc-scheduling-orchestrator": {
        "engine": "PostgreSQL 15 + Valkey 8",
        "schema": "scheduling",
        "tables": ["schedule_requests", "daily_schedules", "schedule_conflicts", "optimization_runs"],
        "features": [
            "Optimistic locking per ADR-011",
            "Valkey for schedule lock cache and optimization queue",
            "JSONB columns for constraint parameters",
        ],
        "volume": "~500 schedule requests/day",
    },
    "svc-guest-profiles": {
        "engine": "PostgreSQL 15",
        "schema": "guests",
        "tables": ["guest_profiles", "certifications", "medical_info", "emergency_contacts", "adventure_history"],
        "features": [
            "PII encrypted at rest (AES-256)",
            "Composite index on (last_name, date_of_birth)",
            "Soft delete with GDPR data retention policy",
        ],
        "volume": "~800 new profiles/day peak season",
    },
    "svc-trip-catalog": {
        "engine": "PostgreSQL 15",
        "schema": "catalog",
        "tables": ["trips", "trip_schedules", "pricing_tiers", "requirements", "regions", "activity_types"],
        "features": [
            "Full-text search index on trip name and description",
            "Materialized view for availability calendar",
            "JSONB columns for flexible requirement definitions",
        ],
        "volume": "~50 catalog updates/day, ~10K availability reads/day",
    },
    "svc-trail-management": {
        "engine": "PostGIS (PostgreSQL 15)",
        "schema": "trails",
        "tables": ["trails", "waypoints", "closures", "condition_reports"],
        "features": [
            "PostGIS geometry columns for trail routes and waypoints",
            "Spatial indexes (GiST) for proximity queries",
            "Time-series condition data with hypertable extension",
        ],
        "volume": "~200 condition updates/day, ~5K trail reads/day",
    },
    "svc-safety-compliance": {
        "engine": "PostgreSQL 15",
        "schema": "safety",
        "tables": ["waivers", "incidents", "safety_inspections", "audit_log"],
        "features": [
            "Immutable audit log (append-only)",
            "Digital signature verification for waivers",
            "Regulatory compliance retention (7 years)",
        ],
        "volume": "~3,000 waiver checks/day",
    },
    "svc-gear-inventory": {
        "engine": "PostgreSQL 15",
        "schema": "gear",
        "tables": ["gear_items", "gear_packages", "gear_assignments", "maintenance_records", "inventory_levels"],
        "features": [
            "RFID tag tracking via unique identifiers",
            "Scheduled maintenance alerts with cron triggers",
            "Location-based inventory partitioning",
        ],
        "volume": "~1,500 assignments/day peak season",
    },
    "svc-transport-logistics": {
        "engine": "PostgreSQL 15",
        "schema": "transport",
        "tables": ["routes", "route_schedules", "transport_requests", "vehicles"],
        "features": [
            "Time-window optimization for route scheduling",
            "Vehicle capacity tracking with overbooking prevention",
            "GPS coordinate storage for pickup and dropoff points",
        ],
        "volume": "~300 transport requests/day",
    },
    "svc-guide-management": {
        "engine": "PostgreSQL 15",
        "schema": "guides",
        "tables": ["guides", "certifications", "guide_schedules", "availability_windows", "ratings"],
        "features": [
            "Certification expiry tracking with automated alerts",
            "Availability window overlap detection constraints",
            "Weighted rating aggregation with recency bias",
        ],
        "volume": "~100 schedule updates/day, ~500 availability queries/day",
    },
    "svc-partner-integrations": {
        "engine": "PostgreSQL 15",
        "schema": "partners",
        "tables": ["partners", "partner_bookings", "commission_records", "reconciliation_log"],
        "features": [
            "Partner API key management with rotation policy",
            "Commission calculation engine with tiered rates",
            "Idempotency keys for booking creation",
        ],
        "volume": "~400 partner bookings/day",
    },
    "svc-payments": {
        "engine": "PostgreSQL 15",
        "schema": "payments",
        "tables": ["payments", "refunds", "payment_methods", "daily_summaries"],
        "features": [
            "PCI-DSS compliant token storage (no raw card data)",
            "Idempotent payment processing via request keys",
            "Double-entry ledger for financial reconciliation",
        ],
        "volume": "~2,500 transactions/day",
    },
    "svc-notifications": {
        "engine": "PostgreSQL 15 + Valkey 8",
        "schema": "notifications",
        "tables": ["notifications", "templates", "delivery_log", "channel_preferences"],
        "features": [
            "Valkey queue for async delivery processing",
            "Template versioning with rollback support",
            "Multi-channel delivery: email, SMS, push, in-app",
        ],
        "volume": "~15,000 notifications/day",
    },
    "svc-analytics": {
        "engine": "Oracle Database 19c",
        "schema": "ANALYTICS",
        "tables": ["BOOKING_METRICS", "REVENUE_METRICS", "UTILIZATION_METRICS", "SATISFACTION_SCORES", "SAFETY_METRICS", "GUIDE_PERFORMANCE"],
        "features": [
            "Oracle Partitioning for time-series data (range partitioning by month)",
            "Materialized views with fast refresh for real-time dashboards",
            "Oracle Advanced Analytics (DBMS_PREDICTIVE_ANALYTICS) for trend forecasting",
        ],
        "volume": "~50K metric inserts/day (event-driven)",
    },
    "svc-loyalty-rewards": {
        "engine": "Couchbase 7",
        "schema": "loyalty",
        "tables": ["members", "point_transactions", "tiers", "redemptions"],
        "features": [
            "Document-oriented member profiles with flexible reward schemas",
            "N1QL queries for tier recalculation and point aggregation",
            "Sub-document operations for atomic point balance updates",
        ],
        "volume": "~1,000 transactions/day",
    },
    "svc-media-gallery": {
        "engine": "PostgreSQL 15 + S3-Compatible Object Store",
        "schema": "media",
        "tables": ["media_items", "share_links", "albums"],
        "features": [
            "S3-compatible storage for photos and videos",
            "Presigned URLs for secure direct upload and download",
            "Automatic thumbnail generation on upload",
        ],
        "volume": "~500 uploads/day peak season",
    },
    "svc-location-services": {
        "engine": "PostGIS (PostgreSQL 15)",
        "schema": "locations",
        "tables": ["locations", "capacity_records", "operating_hours"],
        "features": [
            "PostGIS geometry for geofencing and proximity queries",
            "Real-time capacity tracking with threshold alerts",
            "Timezone-aware operating hours management",
        ],
        "volume": "~100 updates/day, ~2K reads/day",
    },
    "svc-inventory-procurement": {
        "engine": "PostgreSQL 15",
        "schema": "procurement",
        "tables": ["purchase_orders", "po_line_items", "suppliers", "stock_levels", "stock_adjustments", "reorder_alerts"],
        "features": [
            "Purchase order approval workflow with state machine",
            "Automatic reorder point calculation based on consumption",
            "Supplier lead time tracking for delivery estimates",
        ],
        "volume": "~50 POs/day, ~200 stock adjustments/day",
    },
    "svc-weather": {
        "engine": "Valkey 8 + PostgreSQL 15",
        "schema": "weather",
        "tables": ["weather_stations", "forecast_cache", "alert_history"],
        "features": [
            "Valkey TTL cache for current conditions (5-min TTL)",
            "External weather API response caching and aggregation",
            "Severe weather alert deduplication",
        ],
        "volume": "~10K weather reads/day, ~100 external API fetches/day",
    },
}

# Pre-loaded endpoint summaries: (svc_name, METHOD, /path) -> summary
ALL_ENDPOINT_SUMMARIES = {}


def heading_slug(method, path, summary):
    """Reproduce MkDocs heading anchor from: ### METHOD `/path` -- Summary"""
    text = f"{method} {path} -- {summary}"
    text = unicodedata.normalize('NFKD', text)
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)


def endpoint_anchor(target_svc, target_method, target_path):
    """Get the MkDocs heading anchor for a specific endpoint on a target service."""
    summary = ALL_ENDPOINT_SUMMARIES.get((target_svc, target_method, target_path), "")
    if not summary:
        return ""
    return "#" + heading_slug(target_method, target_path, summary)


# Cross-Service Integration Map
# Each entry: (alias, label, action, is_async, (target_method, target_path) or None)
CROSS_SERVICE_CALLS = {}

# --- svc-check-in ---
CROSS_SERVICE_CALLS[("svc-check-in", "POST", "/check-ins")] = [
    ("Res", "Reservations", "Verify reservation exists", False, ("GET", "/reservations/{reservation_id}")),
    ("GP", "Guest Profiles", "Validate guest identity", False, ("GET", "/guests/{guest_id}")),
    ("TC", "Trip Catalog", "Get adventure category", False, ("GET", "/trips/{trip_id}")),
    ("Safety", "Safety Compliance", "Validate active waiver", False, ("GET", "/waivers")),
    ("Ntfy", "Notifications", "Send check-in confirmation", True, ("POST", "/notifications")),
]
CROSS_SERVICE_CALLS[("svc-check-in", "POST", "/check-ins/{check_in_id}/gear-verification")] = [
    ("Gear", "Gear Inventory", "Verify gear assignment", False, ("GET", "/gear-assignments/{assignment_id}")),
    ("Safety", "Safety Compliance", "Log gear verification", False, ("POST", "/incidents")),
]

# --- svc-reservations ---
CROSS_SERVICE_CALLS[("svc-reservations", "POST", "/reservations")] = [
    ("GP", "Guest Profiles", "Validate guest identity", False, ("GET", "/guests/{guest_id}")),
    ("TC", "Trip Catalog", "Check trip availability", False, ("GET", "/trips/{trip_id}")),
    ("Pay", "Payments Svc", "Process deposit payment", False, ("POST", "/payments")),
    ("Kafka", "Event Bus", "reservation.created", True, None),
    ("Ntfy", "Notifications", "Send booking confirmation", True, ("POST", "/notifications")),
]
CROSS_SERVICE_CALLS[("svc-reservations", "PUT", "/reservations/{reservation_id}")] = [
    ("TC", "Trip Catalog", "Verify availability", False, ("GET", "/trips/{trip_id}")),
]
CROSS_SERVICE_CALLS[("svc-reservations", "POST", "/reservations/{reservation_id}/participants")] = [
    ("GP", "Guest Profiles", "Validate participant", False, ("GET", "/guests/{guest_id}")),
]
CROSS_SERVICE_CALLS[("svc-reservations", "PUT", "/reservations/{reservation_id}/status")] = [
    ("Kafka", "Event Bus", "reservation.status_changed", True, None),
    ("Ntfy", "Notifications", "Send status update", True, ("POST", "/notifications")),
]

# --- svc-scheduling-orchestrator ---
CROSS_SERVICE_CALLS[("svc-scheduling-orchestrator", "POST", "/schedule-requests")] = [
    ("GM", "Guide Mgmt", "Check guide availability", False, ("GET", "/guides/{guide_id}/availability")),
    ("TM", "Trail Mgmt", "Verify trail conditions", False, ("GET", "/trails/{trail_id}/conditions")),
    ("WX", "Weather Svc", "Get forecast", False, ("GET", "/weather/forecast")),
    ("TC", "Trip Catalog", "Get trip details", False, ("GET", "/trips/{trip_id}")),
    ("Ntfy", "Notifications", "Notify assigned guides", True, ("POST", "/notifications")),
]
CROSS_SERVICE_CALLS[("svc-scheduling-orchestrator", "POST", "/schedule-optimization")] = [
    ("GM", "Guide Mgmt", "Get all available guides", False, ("GET", "/guides/available")),
    ("LS", "Location Svc", "Check location capacity", False, ("GET", "/locations/{location_id}/capacity")),
    ("TC", "Trip Catalog", "Get trip requirements", False, ("GET", "/trips/{trip_id}")),
    ("AN", "Analytics", "Log optimization metrics", True, ("POST", "/events")),
]
CROSS_SERVICE_CALLS[("svc-scheduling-orchestrator", "POST", "/schedule-conflicts/resolve")] = [
    ("GM", "Guide Mgmt", "Reassign guide", False, ("PATCH", "/guides/{guide_id}")),
    ("Ntfy", "Notifications", "Notify affected parties", True, ("POST", "/notifications")),
]

# --- svc-partner-integrations ---
CROSS_SERVICE_CALLS[("svc-partner-integrations", "POST", "/partner-bookings")] = [
    ("GP", "Guest Profiles", "Validate guest identity", False, ("GET", "/guests/{guest_id}")),
    ("TC", "Trip Catalog", "Check trip availability", False, ("GET", "/trips/{trip_id}")),
    ("Res", "Reservations", "Create reservation", False, ("POST", "/reservations")),
]
CROSS_SERVICE_CALLS[("svc-partner-integrations", "POST", "/partner-bookings/{booking_id}/confirm")] = [
    ("Res", "Reservations", "Confirm reservation", False, ("PUT", "/reservations/{reservation_id}/status")),
    ("Pay", "Payments Svc", "Process commission", False, ("POST", "/payments")),
    ("Ntfy", "Notifications", "Send partner confirmation", True, ("POST", "/notifications")),
]

# --- svc-guest-profiles ---
CROSS_SERVICE_CALLS[("svc-guest-profiles", "POST", "/guests")] = [
    ("ExtID", "IDVerify API", "Verify identity document", False, None),
    ("Kafka", "Event Bus", "guest.registered", True, None),
]
CROSS_SERVICE_CALLS[("svc-guest-profiles", "GET", "/guests/{guest_id}/adventure-history")] = [
    ("Res", "Reservations", "Query past bookings", False, ("GET", "/reservations")),
    ("AN", "Analytics", "Get satisfaction scores", False, ("GET", "/events")),
]

# --- svc-payments --- (PCI scope)
CROSS_SERVICE_CALLS[("svc-payments", "POST", "/payments")] = [
    ("FD", "Fraud Detection API", "Screen transaction", False, None),
    ("PGW", "Payment Gateway", "Tokenize & route payment", False, None),
    ("Ntfy", "Notifications", "Send payment receipt", True, ("POST", "/notifications")),
]
CROSS_SERVICE_CALLS[("svc-payments", "POST", "/payments/{payment_id}/refund")] = [
    ("PGW", "Payment Gateway", "Process refund via gateway", False, None),
    ("Ntfy", "Notifications", "Send refund confirmation", True, ("POST", "/notifications")),
]

# --- svc-notifications ---
CROSS_SERVICE_CALLS[("svc-notifications", "POST", "/notifications")] = [
    ("SG", "SendGrid API", "Deliver email", True, None),
    ("TW", "Twilio API", "Deliver SMS", True, None),
    ("FCM", "Firebase Cloud Messaging", "Send push notification", True, None),
]
CROSS_SERVICE_CALLS[("svc-notifications", "POST", "/notifications/bulk")] = [
    ("SG", "SendGrid API", "Deliver bulk emails", True, None),
    ("TW", "Twilio API", "Deliver bulk SMS", True, None),
    ("FCM", "Firebase Cloud Messaging", "Send bulk push notifications", True, None),
]

# --- svc-safety-compliance ---
CROSS_SERVICE_CALLS[("svc-safety-compliance", "POST", "/waivers")] = [
    ("GP", "Guest Profiles", "Validate guest identity", False, ("GET", "/guests/{guest_id}")),
    ("DS", "DocuSign API", "Verify digital signature", False, None),
    ("Ntfy", "Notifications", "Send waiver copy", True, ("POST", "/notifications")),
]
CROSS_SERVICE_CALLS[("svc-safety-compliance", "POST", "/incidents")] = [
    ("GP", "Guest Profiles", "Get guest contact info", False, ("GET", "/guests/{guest_id}")),
    ("GM", "Guide Mgmt", "Get assigned guide", False, ("GET", "/guides/{guide_id}")),
    ("Ntfy", "Notifications", "Send safety alert", True, ("POST", "/notifications")),
]

# --- svc-gear-inventory ---
CROSS_SERVICE_CALLS[("svc-gear-inventory", "POST", "/gear-assignments")] = [
    ("GP", "Guest Profiles", "Validate guest", False, ("GET", "/guests/{guest_id}")),
    ("Res", "Reservations", "Verify booking", False, ("GET", "/reservations/{reservation_id}")),
    ("Safety", "Safety Compliance", "Check waiver status", False, ("GET", "/waivers")),
]

# --- svc-transport-logistics ---
CROSS_SERVICE_CALLS[("svc-transport-logistics", "POST", "/transport-requests")] = [
    ("Res", "Reservations", "Get booking details", False, ("GET", "/reservations/{reservation_id}")),
    ("LS", "Location Svc", "Validate pickup location", False, ("GET", "/locations/{location_id}")),
    ("ExtMap", "Google Maps Platform", "Calculate optimal route", False, None),
    ("Ntfy", "Notifications", "Send transport details", True, ("POST", "/notifications")),
]

# --- svc-loyalty-rewards ---
CROSS_SERVICE_CALLS[("svc-loyalty-rewards", "POST", "/members/{guest_id}/earn")] = [
    ("Res", "Reservations", "Verify completed booking", False, ("GET", "/reservations/{reservation_id}")),
    ("GP", "Guest Profiles", "Get member profile", False, ("GET", "/guests/{guest_id}")),
    ("Ntfy", "Notifications", "Send earn confirmation", True, ("POST", "/notifications")),
]
CROSS_SERVICE_CALLS[("svc-loyalty-rewards", "POST", "/members/{guest_id}/redeem")] = [
    ("GP", "Guest Profiles", "Get member profile", False, ("GET", "/guests/{guest_id}")),
    ("Pay", "Payments Svc", "Process reward credit", False, ("POST", "/payments")),
    ("Ntfy", "Notifications", "Send redemption confirmation", True, ("POST", "/notifications")),
]

# --- svc-media-gallery ---
CROSS_SERVICE_CALLS[("svc-media-gallery", "POST", "/media")] = [
    ("S3", "Object Store", "Upload binary file", False, None),
    ("ExtMap", "Google Maps Platform", "Reverse geocode GPS metadata", False, None),
]
CROSS_SERVICE_CALLS[("svc-media-gallery", "POST", "/media/{media_id}/share")] = [
    ("Ntfy", "Notifications", "Send share link", True, ("POST", "/notifications")),
]

# --- svc-inventory-procurement ---
CROSS_SERVICE_CALLS[("svc-inventory-procurement", "POST", "/purchase-orders")] = [
    ("GI", "Gear Inventory", "Verify item catalog", False, ("GET", "/gear-items")),
    ("Pay", "Payments Svc", "Process PO payment", False, ("POST", "/payments")),
    ("Ntfy", "Notifications", "Notify procurement team", True, ("POST", "/notifications")),
]

# --- svc-weather ---
CROSS_SERVICE_CALLS[("svc-weather", "GET", "/weather/current")] = [
    ("ExtWx", "OpenWeather API", "Fetch current conditions", False, None),
]
CROSS_SERVICE_CALLS[("svc-weather", "GET", "/weather/forecast")] = [
    ("ExtWx", "OpenWeather API", "Fetch multi-day forecast", False, None),
]
CROSS_SERVICE_CALLS[("svc-weather", "GET", "/weather/alerts")] = [
    ("ExtWx", "OpenWeather API", "Fetch active alerts", False, None),
    ("Ntfy", "Notifications", "Distribute severe weather alerts", True, ("POST", "/notifications")),
]

# --- svc-trail-management ---
CROSS_SERVICE_CALLS[("svc-trail-management", "POST", "/trails/{trail_id}/conditions")] = [
    ("WX", "Weather Svc", "Correlate weather data", False, ("GET", "/weather/current")),
    ("LS", "Location Svc", "Get trail coordinates", False, ("GET", "/locations/{location_id}")),
    ("Safety", "Safety Compliance", "Update trail safety assessment", False, ("POST", "/incidents")),
    ("Ntfy", "Notifications", "Alert park rangers", True, ("POST", "/notifications")),
]

# --- svc-location-services ---
CROSS_SERVICE_CALLS[("svc-location-services", "POST", "/locations")] = [
    ("ExtMap", "Google Maps Platform", "Geocode address", False, None),
]

# --- svc-analytics ---
CROSS_SERVICE_CALLS[("svc-analytics", "POST", "/events")] = [
    ("ExtBI", "Snowflake Data Cloud", "Export aggregated metrics", True, None),
]


# ============================================================
# Event Catalog
# ============================================================

EVENT_CATALOG = {
    "reservation.created": {
        "channel": "novatrek.booking.reservation.created",
        "producer": "svc-reservations",
        "trigger": ("POST", "/reservations"),
        "consumers": ["svc-scheduling-orchestrator", "svc-analytics"],
        "domain": "Booking",
        "summary": "Published when a new reservation is confirmed",
    },
    "reservation.status_changed": {
        "channel": "novatrek.booking.reservation.status-changed",
        "producer": "svc-reservations",
        "trigger": ("PUT", "/reservations/{reservation_id}/status"),
        "consumers": ["svc-notifications", "svc-analytics"],
        "domain": "Booking",
        "summary": "Published when a reservation status transitions",
    },
    "guest.registered": {
        "channel": "novatrek.guest-identity.guest.registered",
        "producer": "svc-guest-profiles",
        "trigger": ("POST", "/guests"),
        "consumers": ["svc-loyalty-rewards", "svc-analytics"],
        "domain": "Guest Identity",
        "summary": "Published when a new guest profile is created",
    },
    "checkin.completed": {
        "channel": "novatrek.operations.checkin.completed",
        "producer": "svc-check-in",
        "trigger": ("POST", "/check-ins"),
        "consumers": ["svc-analytics", "svc-notifications"],
        "domain": "Operations",
        "summary": "Published when a guest completes the check-in process",
    },
    "schedule.published": {
        "channel": "novatrek.operations.schedule.published",
        "producer": "svc-scheduling-orchestrator",
        "trigger": ("POST", "/schedule-requests"),
        "consumers": ["svc-guide-management", "svc-notifications"],
        "domain": "Operations",
        "summary": "Published when a daily schedule is finalized",
    },
    "payment.processed": {
        "channel": "novatrek.support.payment.processed",
        "producer": "svc-payments",
        "trigger": ("POST", "/payments"),
        "consumers": ["svc-reservations", "svc-notifications"],
        "domain": "Support",
        "summary": "Published when a payment is successfully processed",
    },
    "incident.reported": {
        "channel": "novatrek.safety.incident.reported",
        "producer": "svc-safety-compliance",
        "trigger": ("POST", "/incidents"),
        "consumers": ["svc-notifications", "svc-analytics"],
        "domain": "Safety",
        "summary": "Published when a safety incident is reported",
    },
}

# Derived lookups
EVENTS_BY_PRODUCER = {}
EVENTS_BY_CONSUMER = {}
for _evt_name, _evt_info in EVENT_CATALOG.items():
    EVENTS_BY_PRODUCER.setdefault(_evt_info["producer"], []).append(_evt_name)
    for _consumer in _evt_info["consumers"]:
        EVENTS_BY_CONSUMER.setdefault(_consumer, []).append(_evt_name)


# ============================================================
# Consuming Applications (reverse index for bidirectional links)
# ============================================================

APP_CONSUMERS = {
    "svc-trip-catalog": [
        ("web-guest-portal", "Trip Browser"),
        ("web-guest-portal", "Booking Flow"),
        ("app-guest-mobile", "My Reservations"),
    ],
    "svc-trail-management": [
        ("web-guest-portal", "Trip Browser"),
        ("web-ops-dashboard", "Daily Schedule Board"),
        ("web-ops-dashboard", "Guide Assignment"),
        ("app-guest-mobile", "Live Trip Map"),
        ("app-guest-mobile", "Weather and Trail Alerts"),
    ],
    "svc-weather": [
        ("web-guest-portal", "Trip Browser"),
        ("web-ops-dashboard", "Daily Schedule Board"),
        ("app-guest-mobile", "Live Trip Map"),
        ("app-guest-mobile", "Weather and Trail Alerts"),
    ],
    "svc-media-gallery": [
        ("web-guest-portal", "Trip Browser"),
        ("web-guest-portal", "Trip Gallery"),
        ("app-guest-mobile", "Photo Upload"),
    ],
    "svc-guest-profiles": [
        ("web-guest-portal", "Booking Flow"),
        ("web-guest-portal", "Guest Profile"),
        ("web-guest-portal", "Waiver Signing"),
        ("web-ops-dashboard", "Check-In Station"),
        ("web-ops-dashboard", "Safety Incident Board"),
        ("app-guest-mobile", "Self Check-In"),
        ("app-guest-mobile", "Earn Loyalty Points"),
    ],
    "svc-reservations": [
        ("web-guest-portal", "Booking Flow"),
        ("web-guest-portal", "Guest Profile"),
        ("web-guest-portal", "Reservation Management"),
        ("web-guest-portal", "Trip Gallery"),
        ("web-ops-dashboard", "Check-In Station"),
        ("web-ops-dashboard", "Transport Dispatch"),
        ("web-ops-dashboard", "Analytics Dashboard"),
        ("web-ops-dashboard", "Partner Bookings"),
        ("app-guest-mobile", "Self Check-In"),
        ("app-guest-mobile", "My Reservations"),
        ("app-guest-mobile", "Earn Loyalty Points"),
    ],
    "svc-payments": [
        ("web-guest-portal", "Booking Flow"),
        ("web-guest-portal", "Reservation Management"),
        ("web-ops-dashboard", "Analytics Dashboard"),
        ("web-ops-dashboard", "Partner Bookings"),
        ("app-guest-mobile", "My Reservations"),
    ],
    "svc-loyalty-rewards": [
        ("web-guest-portal", "Guest Profile"),
        ("web-guest-portal", "Loyalty Dashboard"),
        ("app-guest-mobile", "Earn Loyalty Points"),
    ],
    "svc-notifications": [
        ("web-guest-portal", "Reservation Management"),
        ("web-guest-portal", "Waiver Signing"),
        ("web-guest-portal", "Trip Gallery"),
        ("web-ops-dashboard", "Safety Incident Board"),
        ("app-guest-mobile", "Photo Upload"),
        ("app-guest-mobile", "Weather and Trail Alerts"),
    ],
    "svc-safety-compliance": [
        ("web-guest-portal", "Waiver Signing"),
        ("web-ops-dashboard", "Check-In Station"),
        ("web-ops-dashboard", "Safety Incident Board"),
        ("app-guest-mobile", "Self Check-In"),
    ],
    "svc-check-in": [
        ("web-ops-dashboard", "Check-In Station"),
        ("app-guest-mobile", "Self Check-In"),
        ("app-guest-mobile", "Digital Wristband"),
    ],
    "svc-gear-inventory": [
        ("web-ops-dashboard", "Check-In Station"),
        ("web-ops-dashboard", "Inventory Management"),
        ("app-guest-mobile", "Self Check-In"),
        ("app-guest-mobile", "Digital Wristband"),
    ],
    "svc-scheduling-orchestrator": [
        ("web-ops-dashboard", "Daily Schedule Board"),
        ("web-ops-dashboard", "Guide Assignment"),
        ("app-guest-mobile", "Live Trip Map"),
    ],
    "svc-guide-management": [
        ("web-ops-dashboard", "Daily Schedule Board"),
        ("web-ops-dashboard", "Guide Assignment"),
        ("web-ops-dashboard", "Safety Incident Board"),
    ],
    "svc-location-services": [
        ("web-ops-dashboard", "Daily Schedule Board"),
        ("web-ops-dashboard", "Transport Dispatch"),
        ("app-guest-mobile", "Live Trip Map"),
    ],
    "svc-transport-logistics": [
        ("web-ops-dashboard", "Transport Dispatch"),
    ],
    "svc-inventory-procurement": [
        ("web-ops-dashboard", "Inventory Management"),
    ],
    "svc-analytics": [
        ("web-ops-dashboard", "Analytics Dashboard"),
    ],
    "svc-partner-integrations": [
        ("web-ops-dashboard", "Partner Bookings"),
    ],
}

APP_TITLES = {
    "web-guest-portal": "Guest Portal",
    "web-ops-dashboard": "Operations Dashboard",
    "app-guest-mobile": "Adventure App",
}


# ============================================================
# Actor Catalog
# ============================================================

ACTORS = {
    # ── Human Actors ──
    "Guest": {
        "type": "Human",
        "description": "NovaTrek customer who books, checks in for, and participates in adventure trips.",
        "interacts_with": ["web-guest-portal", "app-guest-mobile"],
        "domain": "Guest Identity",
    },
    "Operations Staff": {
        "type": "Human",
        "description": "On-site NovaTrek employees who manage daily operations including check-in, scheduling, gear assignment, and incident response.",
        "interacts_with": ["web-ops-dashboard"],
        "domain": "Operations",
    },
    "Adventure Guide": {
        "type": "Human",
        "description": "Certified outdoor guides who lead adventure trips, manage guest safety, and report incidents.",
        "interacts_with": ["app-guest-mobile", "web-ops-dashboard"],
        "domain": "Guide Management",
    },

    # ── Frontend Applications ──
    "web-guest-portal": {
        "type": "Frontend Application",
        "description": "Public-facing web application for guests to browse trips, book reservations, manage profiles, sign waivers, and view trip media.",
        "technology": "React SPA",
        "team": "Guest Experience Team",
        "domain": "Guest Identity",
    },
    "web-ops-dashboard": {
        "type": "Frontend Application",
        "description": "Internal web application for operations staff to manage check-ins, daily schedules, guide assignments, safety incidents, and partner bookings.",
        "technology": "React SPA",
        "team": "NovaTrek Operations Team",
        "domain": "Operations",
    },
    "app-guest-mobile": {
        "type": "Frontend Application",
        "description": "Native mobile application for guests to self check-in, view live trip maps, receive weather alerts, upload photos, and earn loyalty points.",
        "technology": "React Native",
        "team": "Guest Experience Team",
        "domain": "Guest Identity",
    },

    # ── Infrastructure ──
    "API Gateway": {
        "type": "Infrastructure",
        "description": "Central API Gateway that routes all external requests to backend microservices. Handles authentication, rate limiting, and TLS termination.",
        "technology": "Azure API Management",
        "domain": "Platform",
    },
    "Event Bus": {
        "type": "Infrastructure",
        "description": "Apache Kafka cluster used for asynchronous event-driven communication between microservices. All domain events flow through dedicated Kafka topics.",
        "technology": "Apache Kafka",
        "domain": "Platform",
    },
    "Object Store": {
        "type": "Infrastructure",
        "description": "Cloud object storage for media assets including trip photos, guide profile images, and waiver documents.",
        "technology": "Azure Blob Storage",
        "domain": "Platform",
    },

    # ── External Systems ──
    "Payment Gateway": {
        "type": "External System",
        "description": "PCI-certified payment processing gateway that handles credit card authorization, capture, and refund transactions.",
        "technology": "Stripe",
        "pci": True,
        "domain": "Support",
    },
    "Stripe API": {
        "type": "External System",
        "description": "Payment platform API for processing charges, managing payment methods, and handling disputes.",
        "technology": "Stripe REST API",
        "pci": True,
        "domain": "Support",
    },
    "Fraud Detection API": {
        "type": "External System",
        "description": "Third-party fraud prevention service that scores payment transactions for risk before authorization.",
        "technology": "REST API",
        "pci": True,
        "domain": "Support",
    },
    "DocuSign API": {
        "type": "External System",
        "description": "Electronic signature platform used for legally-binding adventure liability waivers and safety acknowledgments.",
        "technology": "DocuSign eSignature REST API",
        "domain": "Safety",
    },
    "IDVerify API": {
        "type": "External System",
        "description": "Identity verification service used during check-in to validate guest identity against government-issued IDs.",
        "technology": "REST API",
        "domain": "Guest Identity",
    },
    "Google Maps Platform": {
        "type": "External System",
        "description": "Geolocation and mapping service used for trail positioning, location tracking, and capacity management at adventure sites.",
        "technology": "Google Maps REST API",
        "domain": "Logistics",
    },
    "OpenWeather API": {
        "type": "External System",
        "description": "Weather data provider delivering current conditions, forecasts, and severe weather alerts for trail and adventure locations.",
        "technology": "OpenWeather REST API",
        "domain": "Support",
    },
    "Firebase Cloud Messaging": {
        "type": "External System",
        "description": "Push notification delivery service for real-time alerts to guest mobile devices (weather warnings, check-in reminders, schedule changes).",
        "technology": "Firebase FCM",
        "domain": "Support",
    },
    "SendGrid API": {
        "type": "External System",
        "description": "Transactional email delivery service for reservation confirmations, waiver requests, and loyalty point notifications.",
        "technology": "SendGrid REST API",
        "domain": "Support",
    },
    "Twilio API": {
        "type": "External System",
        "description": "SMS and messaging service for check-in reminders, schedule updates, and emergency notifications to guests and guides.",
        "technology": "Twilio REST API",
        "domain": "Support",
    },
    "Snowflake Data Cloud": {
        "type": "External System",
        "description": "Cloud data warehouse used for business intelligence, analytics aggregation, and historical trend analysis across all NovaTrek domains.",
        "technology": "Snowflake SQL API",
        "domain": "Support",
    },
}

# Build reverse index: which services reference which actors
ACTOR_SERVICE_USAGE = {}
for (_caller, _method, _path), _targets in CROSS_SERVICE_CALLS.items():
    for _t in _targets:
        _label = _t[1]
        if _label in ACTORS:
            ACTOR_SERVICE_USAGE.setdefault(_label, set()).add(_caller)

# Add services from APP_CONSUMERS
for _svc, _apps in APP_CONSUMERS.items():
    for _app_name, _ in _apps:
        if _app_name in ACTORS:
            ACTOR_SERVICE_USAGE.setdefault(_app_name, set()).add(_svc)


# ============================================================
# C4 Context Diagram Generation
# ============================================================

def _safe_alias(name):
    """Create a valid PlantUML alias from a service or system name."""
    return re.sub(r'[^a-zA-Z0-9]', '_', name)


def build_enterprise_c4_puml():
    """Build an enterprise-level C4 Container diagram showing ALL services.

    Groups services by domain inside System_Boundary elements, shows the
    three frontend applications as Person elements, external third-party
    systems as System_Ext, and inter-domain relationships as aggregated arrows.
    """
    # Collect all edges
    svc_to_domain = {}
    for domain, info in DOMAINS.items():
        for svc in info["services"]:
            svc_to_domain[svc] = domain

    # Service-to-service edges
    svc_edges = {}       # (from_svc, to_svc) -> count
    ext_edges = {}       # (from_svc, ext_label) -> count
    ext_labels = set()

    for (caller, method, path), targets in CROSS_SERVICE_CALLS.items():
        for entry in targets:
            label = entry[1]
            target_svc = label_to_svc_name(label)
            if target_svc:
                key = (caller, target_svc)
                svc_edges[key] = svc_edges.get(key, 0) + 1
            elif label not in ("Event Bus", "Object Store"):
                key = (caller, label)
                ext_edges[key] = ext_edges.get(key, 0) + 1
                ext_labels.add(label)

    # Aggregate to domain-level relationships to avoid spaghetti
    # Exclude PCI service edges from domain aggregation (they get their own arrows)
    domain_edges = {}  # (from_domain, to_domain) -> total_count
    for (f, t), cnt in svc_edges.items():
        if f in PCI_SERVICES or t in PCI_SERVICES:
            continue  # handled as direct PCI arrows below
        fd = svc_to_domain.get(f, "Support")
        td = svc_to_domain.get(t, "Support")
        if fd != td:
            key = (fd, td)
            domain_edges[key] = domain_edges.get(key, 0) + cnt

    # App-to-service edges (aggregated to domain)
    app_domain_edges = {}  # (app, domain) -> count
    for svc, consumers in APP_CONSUMERS.items():
        domain = svc_to_domain.get(svc, "Support")
        for app_name, _ in consumers:
            key = (app_name, domain)
            app_domain_edges[key] = app_domain_edges.get(key, 0) + 1

    L = []
    L.append("@startuml")
    L.append("!include <c4/C4_Container>")
    L.append("")
    L.append("LAYOUT_WITH_LEGEND()")
    L.append("LAYOUT_TOP_DOWN()")
    L.append("")
    L.append('AddRelTag("pci", $lineColor="#DC2626", $textColor="#DC2626", $legendText="PCI Data Flow")')
    L.append("")
    L.append("title NovaTrek Adventures — Enterprise Architecture")
    L.append("")

    # Frontend applications as Person elements
    app_order = ["web-guest-portal", "web-ops-dashboard", "app-guest-mobile"]
    for app in app_order:
        app_title = APP_TITLES.get(app, app)
        app_type = "Web App" if app.startswith("web-") else "Mobile App"
        L.append(f'Person({_safe_alias(app)}, "{app_title}", "{app_type}", $link="/applications/{app}/")')
    L.append("")

    # Domain boundaries with services
    domain_order = [
        "Operations", "Guest Identity", "Booking", "Product Catalog",
        "Safety", "Logistics", "Guide Management", "External", "Support",
    ]

    for domain_name in domain_order:
        info = DOMAINS[domain_name]
        svcs = info["services"]
        boundary_alias = _safe_alias(domain_name)
        L.append(f'System_Boundary({boundary_alias}, "{domain_name}") {{')
        for svc in svcs:
            if svc in PCI_SERVICES:
                continue  # rendered inside PCI Zone instead
            svc_title = svc.replace("svc-", "").replace("-", " ").title()
            L.append(f'    Container({_safe_alias(svc)}, "{svc}", "Java / Spring Boot", "{svc_title}", $link="/microservices/{svc}/#integration-context")')
        L.append("}")
        L.append("")

    # PCI Zone boundary (separate, visually distinct)
    L.append('System_Boundary(PCI_Zone, "PCI DSS Compliance Zone") {')
    for svc in sorted(PCI_SERVICES):
        svc_title = svc.replace("svc-", "").replace("-", " ").title()
        L.append(f'    Container({_safe_alias(svc)}, "{svc}", "Java / Spring Boot", "{svc_title} (PCI scope)", $link="/microservices/{svc}/#integration-context")')
    L.append("}")
    L.append("")

    # External systems (add Payment Gateway explicitly)
    all_ext = ext_labels | {"Payment Gateway"}
    for ext in sorted(all_ext):
        ext_anchor_val = actor_anchor(ext)
        if ext in PCI_EXTERNALS:
            L.append(f'System_Ext({_safe_alias(ext)}, "{ext}", "PCI-certified third-party", $link="/actors/#{ext_anchor_val}")')
        else:
            L.append(f'System_Ext({_safe_alias(ext)}, "{ext}", "Third-party service", $link="/actors/#{ext_anchor_val}")')
    L.append("")

    # Relationships: apps to domains
    for app in app_order:
        app_alias = _safe_alias(app)
        targets = sorted(set(d for (a, d) in app_domain_edges if a == app))
        for domain_name in targets:
            # Link to first service in that domain as representative
            first_svc = DOMAINS[domain_name]["services"][0]
            count = app_domain_edges[(app, domain_name)]
            L.append(f'Rel({app_alias}, {_safe_alias(first_svc)}, "{count} screens", "HTTPS")')

    L.append("")

    # Relationships: inter-domain (aggregated), with PCI tags
    for (fd, td), cnt in sorted(domain_edges.items()):
        from_svc = DOMAINS[fd]["services"][0]
        to_svc = DOMAINS[td]["services"][0]
        L.append(f'Rel({_safe_alias(from_svc)}, {_safe_alias(to_svc)}, "{cnt} calls", "HTTPS")')

    L.append("")

    # Direct PCI service-level edges (not aggregated to domain)
    for (f, t), cnt in sorted(svc_edges.items()):
        if f not in PCI_SERVICES and t not in PCI_SERVICES:
            continue
        pci = is_pci_flow(f, t)
        tag_attr = ', $tags="pci"' if pci else ""
        L.append(f'Rel({_safe_alias(f)}, {_safe_alias(t)}, "{cnt} calls", "HTTPS"{tag_attr})')

    L.append("")

    # Relationships: services to external systems (service-level, not domain-level)
    for (svc, ext), cnt in sorted(ext_edges.items()):
        pci = is_pci_flow(svc, ext)
        tag_attr = ', $tags="pci"' if pci else ""
        L.append(f'Rel({_safe_alias(svc)}, {_safe_alias(ext)}, "Integrates", "HTTPS"{tag_attr})')

    # Payment Gateway to Stripe API (PCI)
    L.append(f'Rel({_safe_alias("Payment Gateway")}, {_safe_alias("Stripe API")}, "Process card txn", "HTTPS", $tags="pci")')

    L.append("")
    L.append("@enduml")

    return "\n".join(L)


def build_c4_context_puml(svc_name):
    """Build a C4 Container-level context diagram for a microservice.

    Shows the service at the center with:
      - Its database
      - Services it calls (outbound)
      - Services that call it (inbound)
      - External third-party systems
      - Consuming frontend applications
    """
    domain, color = get_domain_info(svc_name)
    ds = DATA_STORES.get(svc_name, {})

    # Collect outbound relationships: services and externals this svc calls
    outbound_svcs = {}   # svc_name -> set of action descriptions
    outbound_ext = {}    # ext_label -> set of action descriptions
    for (caller, method, path), targets in CROSS_SERVICE_CALLS.items():
        if caller != svc_name:
            continue
        for entry in targets:
            label = entry[1]
            action = entry[2]
            target_svc = label_to_svc_name(label)
            if target_svc:
                outbound_svcs.setdefault(target_svc, set()).add(action)
            elif label not in ("Event Bus", "Object Store"):
                outbound_ext.setdefault(label, set()).add(action)

    # Collect inbound relationships: services that call this svc
    inbound_svcs = {}  # svc_name -> set of action descriptions
    for (caller, method, path), targets in CROSS_SERVICE_CALLS.items():
        for entry in targets:
            label = entry[1]
            target_svc = label_to_svc_name(label)
            if target_svc == svc_name and caller != svc_name:
                action = entry[2]
                inbound_svcs.setdefault(caller, set()).add(action)

    # Consuming applications
    apps = APP_CONSUMERS.get(svc_name, [])
    app_names = sorted(set(a for a, _ in apps))

    # Determine if this diagram involves any PCI flows
    has_pci = svc_name in PCI_SERVICES or any(
        is_pci_flow(peer, svc_name) for peer in inbound_svcs
    ) or any(
        is_pci_flow(svc_name, peer) for peer in outbound_svcs
    ) or any(
        is_pci_flow(svc_name, ext) for ext in outbound_ext
    )

    L = []
    L.append("@startuml")
    L.append("!include <c4/C4_Container>")
    L.append("")
    L.append("LAYOUT_WITH_LEGEND()")
    L.append("LAYOUT_TOP_DOWN()")
    if has_pci:
        L.append("")
        L.append('AddRelTag("pci", $lineColor="#DC2626", $textColor="#DC2626", $legendText="PCI Data Flow")')
    L.append("")
    L.append(f'header [[/microservices/ \u2B06 All Microservices]]')
    L.append("")
    L.append(f'title {svc_name} — Integration Context')
    L.append("")

    # Frontend applications at the top
    for app in app_names:
        app_title = APP_TITLES.get(app, app)
        app_type = "Web App" if app.startswith("web-") else "Mobile App"
        a = _safe_alias(app)
        L.append(f'Person({a}, "{app_title}", "{app_type}", $link="/applications/{app}/#service-dependencies")')

    L.append("")

    # The service itself (center)
    svc_title = svc_name.replace("svc-", "").replace("-", " ").title()
    L.append(f'System_Boundary(boundary, "NovaTrek Platform") {{')
    L.append(f'    Container({_safe_alias(svc_name)}, "{svc_name}", "Java / Spring Boot", "{svc_title} Service", $link="/microservices/{svc_name}/")')

    # Database
    if ds:
        engine = ds.get("engine", "PostgreSQL 15")
        schema = ds.get("schema", "")
        db_alias = f"{_safe_alias(svc_name)}_db"
        L.append(f'    ContainerDb({db_alias}, "{engine}", "{schema} schema", "Primary data store", $link="/microservices/{svc_name}/#data-store")')

    # Inbound peer services inside the boundary
    for peer in sorted(inbound_svcs.keys()):
        peer_domain, _ = get_domain_info(peer)
        L.append(f'    Container({_safe_alias(peer)}, "{peer}", "Java / Spring Boot", "{peer_domain}", $link="/microservices/{peer}/#integration-context")')

    # Outbound peer services inside the boundary
    for peer in sorted(outbound_svcs.keys()):
        if peer in inbound_svcs:
            continue  # already added
        peer_domain, _ = get_domain_info(peer)
        L.append(f'    Container({_safe_alias(peer)}, "{peer}", "Java / Spring Boot", "{peer_domain}", $link="/microservices/{peer}/#integration-context")')

    L.append("}")
    L.append("")

    # External systems outside boundary
    for ext in sorted(outbound_ext.keys()):
        ext_anchor = actor_anchor(ext)
        if ext in PCI_EXTERNALS:
            L.append(f'System_Ext({_safe_alias(ext)}, "{ext}", "PCI-certified third-party", $link="/actors/#{ext_anchor}")')
        else:
            L.append(f'System_Ext({_safe_alias(ext)}, "{ext}", "Third-party service", $link="/actors/#{ext_anchor}")')
    L.append("")

    # Relationships — apps to this service
    svc_alias = _safe_alias(svc_name)
    for app in app_names:
        a = _safe_alias(app)
        L.append(f'Rel({a}, {svc_alias}, "Uses API", "HTTPS")')

    # Relationships — inbound services
    for peer in sorted(inbound_svcs.keys()):
        actions = sorted(inbound_svcs[peer])
        label = actions[0] if len(actions) == 1 else f"{len(actions)} calls"
        pci_tag = ', $tags="pci"' if is_pci_flow(peer, svc_name) else ""
        L.append(f'Rel({_safe_alias(peer)}, {svc_alias}, "{label}", "HTTPS"{pci_tag})')

    # Relationships — database
    if ds:
        L.append(f'Rel({svc_alias}, {db_alias}, "Reads/Writes", "SQL/TCP")')

    # Relationships — outbound services
    for peer in sorted(outbound_svcs.keys()):
        actions = sorted(outbound_svcs[peer])
        label = actions[0] if len(actions) == 1 else f"{len(actions)} calls"
        pci_tag = ', $tags="pci"' if is_pci_flow(svc_name, peer) else ""
        L.append(f'Rel({svc_alias}, {_safe_alias(peer)}, "{label}", "HTTPS"{pci_tag})')

    # Relationships — external systems
    for ext in sorted(outbound_ext.keys()):
        actions = sorted(outbound_ext[ext])
        label = actions[0] if len(actions) == 1 else ", ".join(actions[:2])
        pci_tag = ', $tags="pci"' if is_pci_flow(svc_name, ext) else ""
        L.append(f'Rel({svc_alias}, {_safe_alias(ext)}, "{label}", "HTTPS"{pci_tag})')

    L.append("")
    L.append("@enduml")

    return "\n".join(L)


# ============================================================
# Helper Functions
# ============================================================

def get_domain_info(svc_name):
    for domain, info in DOMAINS.items():
        if svc_name in info["services"]:
            return domain, info["color"]
    return "Support", "#64748b"


def extract_endpoints(spec):
    endpoints = []
    for path, path_item in spec.get("paths", {}).items():
        for method in ["get", "post", "put", "patch", "delete"]:
            if method in path_item:
                op = path_item[method]
                desc_raw = (op.get("description") or "").strip()
                desc_line = desc_raw.split("\n")[0].strip()[:200] if desc_raw else ""
                endpoints.append({
                    "method": method.upper(),
                    "path": path,
                    "summary": op.get("summary", ""),
                    "description": desc_line,
                    "operationId": op.get("operationId", ""),
                    "tags": op.get("tags", []),
                })
    return endpoints


def get_short_db_name(engine):
    if "Oracle" in engine:
        return "Oracle"
    if "Couchbase" in engine:
        return "Couchbase"
    if "TimescaleDB" in engine:
        return "TimescaleDB"
    if "PostGIS" in engine:
        return "PostGIS"
    if engine.startswith("Valkey"):
        return "Valkey + PG"
    if engine.startswith("Redis"):
        return "Redis + PG"
    if "PostgreSQL" in engine and "Valkey" in engine:
        return "PG + Valkey"
    if "PostgreSQL" in engine and "Redis" in engine:
        return "PG + Redis"
    if "PostgreSQL" in engine:
        return "PostgreSQL"
    return engine.split()[0]


def has_path_param_at_end(path):
    parts = path.strip("/").split("/")
    return parts[-1].startswith("{") and parts[-1].endswith("}")


def is_sub_resource(path):
    parts = path.strip("/").split("/")
    if len(parts) >= 3:
        has_mid_param = any(p.startswith("{") for p in parts[1:-1])
        end_not_param = not parts[-1].startswith("{")
        return has_mid_param and end_not_param
    return False


def success_status(method):
    if method == "POST":
        return "201 Created"
    if method == "DELETE":
        return "204 No Content"
    return "200 OK"


def svc_method_name(method, path, operation_id):
    if operation_id:
        return operation_id + "()"
    if method == "GET":
        return "getById(id)" if has_path_param_at_end(path) else "search(filters)"
    elif method == "POST":
        return "create(body)"
    elif method == "PUT":
        return "update(id, body)"
    elif method == "PATCH":
        return "patch(id, fields)"
    elif method == "DELETE":
        return "delete(id)"
    return "handle(request)"


def label_to_svc_name(label):
    return LABEL_TO_SVC.get(label, None)


def make_puml_filename(svc_name, method, path):
    clean = path.strip("/").replace("/", "-").replace("{", "").replace("}", "")
    return f"{svc_name}--{method.lower()}-{clean}"


# ============================================================
# PlantUML Diagram Generation
# ============================================================

METHOD_COLORS = {
    "GET": "#2563eb",
    "POST": "#059669",
    "PUT": "#c77b30",
    "PATCH": "#7c3aed",
    "DELETE": "#dc2626",
}


def build_puml(svc_name, method, path, summary, db_engine, ext_calls,
               operation_id="", tags=None):
    method_color = METHOD_COLORS.get(method, "#475569")
    db_label = get_short_db_name(db_engine)
    tag = (tags or [""])[0]
    fname = make_puml_filename(svc_name, method, path)

    L = []
    L.append(f"@startuml {fname}")
    L.append("")

    # Skinparam
    L.append("skinparam backgroundColor #FEFEFE")
    L.append("skinparam shadowing false")
    L.append('skinparam defaultFontName "Segoe UI"')
    L.append("skinparam sequence {")
    L.append(f"    ArrowColor {method_color}")
    L.append("    ParticipantBorderColor #2E86AB")
    L.append("    ParticipantBackgroundColor #E8F4F8")
    L.append("    LifeLineBorderColor #A23B72")
    L.append("    BoxBorderColor #F18F01")
    L.append("    BoxBackgroundColor #FFF8F0")
    L.append("    NoteBorderColor #c77b30")
    L.append("    NoteBackgroundColor #FEF3E7")
    L.append("}")
    L.append("")

    # Parent breadcrumb
    L.append(f'header [[/microservices/{svc_name}/#integration-context \u2B06 {svc_name} Integration Context]]')
    L.append("")

    # Title
    title_text = f"{method} {path}"
    L.append(f"title {title_text}\\n{summary}")
    L.append("")

    # Participants - clickable
    L.append(f'participant "Client" as Client [[/applications/]]')
    L.append(f'participant "API Gateway" as GW [[/actors/#api-gateway]] #DBEAFE')
    svc_bg = "#FFE0E0" if svc_name in PCI_SERVICES else "#E8F4F8"
    L.append(f'participant "{svc_name}" as Svc [[/microservices/{svc_name}/]] {svc_bg}')

    declared = set()
    for call in (ext_calls or []):
        alias, label, action = call[0], call[1], call[2]
        target_ep = call[4] if len(call) > 4 else None
        if alias in declared:
            continue
        declared.add(alias)
        target_svc = label_to_svc_name(label)
        if target_svc:
            color = "#FFE0E0" if target_svc in PCI_SERVICES else "#FFF8F0"
            L.append(f'participant "{label}" as {alias} [[/microservices/{target_svc}/]] {color}')
        elif label == "Event Bus":
            L.append(f'queue "Kafka" as {alias} [[/actors/#event-bus]] #F0E6FF')
        elif label in PCI_EXTERNALS:
            actor_link = actor_anchor(label)
            L.append(f'participant "{label}" as {alias} [[/actors/#{actor_link}]] #FFE0E0')
        else:
            actor_link = actor_anchor(label)
            if label in ACTORS:
                L.append(f'participant "{label}" as {alias} [[/actors/#{actor_link}]] #F5F5F5')
            else:
                L.append(f'participant "{label}" as {alias} #F5F5F5')

    L.append(f'database "{db_label}" as DB #FCE4EC')
    L.append("")

    # Swagger link note
    tag_enc = quote(tag, safe="") if tag else ""
    anchor = f"#/{tag_enc}/{operation_id}" if tag_enc and operation_id else ""
    swagger_url = f"/services/api/{svc_name}.html{anchor}"
    L.append("note over Svc")
    L.append(f"  [[{swagger_url} View in Swagger UI]]")
    L.append("end note")
    L.append("")

    # Request flow
    L.append(f"Client -> GW : {method} {path}")
    L.append(f"activate GW {method_color}")
    L.append("GW -> Svc : route request")
    L.append(f"activate Svc {method_color}")
    L.append("")

    if method in ("POST", "PUT", "PATCH"):
        L.append("note right of Svc : Validate request body")
        L.append("")

    # Cross-service calls (sync)
    sync_calls = [c for c in (ext_calls or []) if not c[3]]
    async_calls = [c for c in (ext_calls or []) if c[3]]

    if sync_calls:
        L.append("== Cross-Service Integration ==")
        L.append("")
        for call in sync_calls:
            alias, label, action = call[0], call[1], call[2]
            target_ep = call[4] if len(call) > 4 else None
            target_svc = label_to_svc_name(label)
            # Determine if this call carries PCI data
            pci_target = target_svc if target_svc else label
            pci_arrow = "-[#DC2626]>" if is_pci_flow(svc_name, pci_target) else "->"
            pci_return = "--[#DC2626]>" if is_pci_flow(svc_name, pci_target) else "-->"
            if target_svc:
                anchor = ""
                if target_ep:
                    anchor = endpoint_anchor(target_svc, target_ep[0], target_ep[1])
                L.append(f"Svc {pci_arrow} {alias} : [[/microservices/{target_svc}/{anchor} {action}]]")
            else:
                L.append(f"Svc {pci_arrow} {alias} : {action}")
            L.append(f"activate {alias} #DBEAFE")
            L.append(f"{alias} {pci_return} Svc : OK")
            L.append(f"deactivate {alias}")
            L.append("")

    # Database operation labels (adapt for document vs relational databases)
    _doc = "Couchbase" in db_engine
    _q = {
        "by_id":     "GET document by key"            if _doc else "SELECT ... WHERE id = ?",
        "by_parent": "N1QL: SELECT WHERE parent_id"   if _doc else "SELECT ... WHERE parent_id = ?",
        "filter":    "N1QL: SELECT WHERE filters"     if _doc else "SELECT ... WHERE filters",
        "chk_par":   "GET parent document by key"     if _doc else "SELECT parent WHERE id = ?",
        "insert":    "INSERT document"                if _doc else "INSERT INTO ...",
        "lock":      "GET document (CAS read)"        if _doc else "SELECT ... FOR UPDATE",
        "update":    "UPSERT document (CAS write)"    if _doc else "UPDATE ... SET ...",
        "delete":    "REMOVE document"                if _doc else "DELETE FROM ... WHERE id = ?",
    }
    _r = {
        "one":     "Document"     if _doc else "Row",
        "set":     "Document set" if _doc else "ResultSet",
        "page":    "Document set" if _doc else "Page of results",
        "parent":  "Document"     if _doc else "Parent row",
        "created": "Document"     if _doc else "Created row",
        "current": "Document"     if _doc else "Current row",
        "updated": "Document"     if _doc else "Updated row",
    }
    _merge_note = "Sub-document mutation for changed fields" if _doc else "Merge changed fields only"
    _replace_note = "Replace document content" if _doc else "Replace mutable fields"

    # Database operations
    L.append("== Database ==")
    L.append("")

    if method == "GET":
        if has_path_param_at_end(path):
            L.append(f"Svc -> DB : {_q['by_id']}")
            L.append("activate DB #FCE4EC")
            L.append(f"DB --> Svc : {_r['one']}")
            L.append("deactivate DB")
            L.append("note right of DB : Returns 404 if not found")
        elif is_sub_resource(path):
            L.append(f"Svc -> DB : {_q['by_parent']}")
            L.append("activate DB #FCE4EC")
            L.append(f"DB --> Svc : {_r['set']}")
            L.append("deactivate DB")
        else:
            L.append(f"Svc -> DB : {_q['filter']}")
            L.append("activate DB #FCE4EC")
            L.append(f"DB --> Svc : {_r['page']}")
            L.append("deactivate DB")

    elif method == "POST":
        if is_sub_resource(path):
            L.append(f"Svc -> DB : {_q['chk_par']}")
            L.append("activate DB #FCE4EC")
            L.append(f"DB --> Svc : {_r['parent']}")
            L.append("deactivate DB")
            L.append("note right of DB : 404 if parent not found")
            L.append("")
        L.append(f"Svc -> DB : {_q['insert']}")
        L.append("activate DB #FCE4EC")
        L.append(f"DB --> Svc : {_r['created']}")
        L.append("deactivate DB")

    elif method in ("PUT", "PATCH"):
        L.append(f"Svc -> DB : {_q['lock']}")
        L.append("activate DB #FCE4EC")
        L.append(f"DB --> Svc : {_r['current']}")
        L.append("deactivate DB")
        note = _merge_note if method == "PATCH" else _replace_note
        L.append(f"note right of Svc : {note}")
        L.append("")
        L.append(f"Svc -> DB : {_q['update']}")
        L.append("activate DB #FCE4EC")
        L.append(f"DB --> Svc : {_r['updated']}")
        L.append("deactivate DB")

    elif method == "DELETE":
        L.append(f"Svc -> DB : {_q['by_id']}")
        L.append("activate DB #FCE4EC")
        L.append(f"DB --> Svc : {_r['one']}")
        L.append("deactivate DB")
        L.append("note right of DB : Returns 404 if not found")
        L.append("")
        L.append(f"Svc -> DB : {_q['delete']}")
        L.append("activate DB #FCE4EC")
        L.append("DB --> Svc : OK")
        L.append("deactivate DB")

    L.append("")

    # Async events
    if async_calls:
        L.append("== Async Events ==")
        L.append("")
        for call in async_calls:
            alias, label, action = call[0], call[1], call[2]
            target_ep = call[4] if len(call) > 4 else None
            target_svc = label_to_svc_name(label)
            if target_svc and target_ep:
                anchor = endpoint_anchor(target_svc, target_ep[0], target_ep[1])
                L.append(f"Svc ->> {alias} : [[/microservices/{target_svc}/{anchor} {action}]]")
            elif label == "Event Bus" and action in EVENT_CATALOG:
                slug = re.sub(r'[^\w\s-]', '', action).strip().lower().replace(' ', '-')
                L.append(f"Svc ->> {alias} : [[/events/#{slug} {action}]]")
            else:
                L.append(f"Svc ->> {alias} : {action}")
        L.append("")

    # Response
    status = success_status(method)
    L.append(f"Svc --> GW : {status}")
    L.append("deactivate Svc")
    L.append(f"GW --> Client : {status}")
    L.append("deactivate GW")
    L.append("")
    L.append("@enduml")

    return "\n".join(L)


# ============================================================
# Page Generation
# ============================================================

def generate_service_page(svc_name, spec, svg_files):
    info = spec.get("info", {})
    title = info.get("title", svc_name)
    version = info.get("version", "0.0.0")
    description = (info.get("description") or "").strip()
    desc_first_line = description.split("\n")[0].strip() if description else ""
    owner = info.get("contact", {}).get("name", "NovaTrek Engineering")

    domain, color = get_domain_info(svc_name)
    ds = DATA_STORES.get(svc_name, {})
    endpoints = extract_endpoints(spec)

    lines = []

    lines.append("---")
    lines.append("tags:")
    lines.append("  - microservice")
    lines.append(f"  - {svc_name}")
    lines.append(f"  - {domain.lower().replace(' ', '-')}")
    lines.append("---")
    lines.append("")

    lines.append(f"# {svc_name}")
    lines.append("")
    badge_style = (
        f"background: {color}15; color: {color}; "
        f"border: 1px solid {color}40; padding: 0.15rem 0.6rem; "
        f"border-radius: 1rem; font-size: 0.8rem; font-weight: 600;"
    )
    lines.append(
        f'**{title}** &nbsp;|&nbsp; '
        f'<span style="{badge_style}">{domain}</span> '
        f'&nbsp;|&nbsp; `v{version}` &nbsp;|&nbsp; *{owner}*'
    )
    lines.append("")

    if desc_first_line:
        lines.append(f"> {desc_first_line}")
        lines.append("")

    lines.append(
        f"[:material-api: Swagger UI](../services/api/{svc_name}.html)"
        "{ .md-button .md-button--primary }"
    )
    lines.append(
        f"[:material-file-download: Download OpenAPI Spec](../specs/{svc_name}.yaml)"
        "{ .md-button }"
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    # C4 Context Diagram
    c4_svg = f"{svc_name}--c4-context.svg"
    if c4_svg in svg_files:
        lines.append("## :material-map: Integration Context")
        lines.append("")
        lines.append(
            f'<div class="diagram-wrap">'
            f'<a href="../svg/{c4_svg}" target="_blank" class="diagram-expand" title="Open in new tab">\u2922</a>'
            f'<object data="../svg/{c4_svg}" type="image/svg+xml" '
            f'style="max-width: 100%;">{svc_name} C4 context diagram</object></div>'
        )
        lines.append("")
        lines.append("")
    if ds:
        tables_fmt = ", ".join(f"`{t}`" for t in ds.get("tables", []))
        features_fmt = " | ".join(ds.get("features", []))
        lines.append("| Property | Detail |")
        lines.append("|----------|--------|")
        lines.append(f"| **Engine** | {ds.get('engine', 'N/A')} |")
        lines.append(f"| **Schema** | `{ds.get('schema', 'N/A')}` |")
        lines.append(f"| **Primary Tables** | {tables_fmt} |")
        lines.append(f"| **Key Features** | {features_fmt} |")
        lines.append(f"| **Estimated Volume** | {ds.get('volume', 'N/A')} |")
    else:
        lines.append("*Data store information not yet documented.*")

    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append(f"## :material-api: Endpoints ({len(endpoints)} total)")
    lines.append("")

    for ep in endpoints:
        method = ep["method"]
        path = ep["path"]
        summary = ep["summary"] or "Endpoint"
        desc = ep["description"]
        op_id = ep["operationId"]
        tags_list = ep["tags"]
        method_lower = method.lower()

        lines.append("---")
        lines.append("")
        lines.append(f"### {method} `{path}` -- {summary} " + "{ .endpoint-" + method_lower + " }")
        lines.append("")

        if desc:
            lines.append(f"> {desc}")
            lines.append("")

        tag_encoded = quote(tags_list[0], safe="") if tags_list else ""
        anchor = f"#/{tag_encoded}/{op_id}" if tag_encoded and op_id else ""
        swagger_url = f"../services/api/{svc_name}.html{anchor}"
        lines.append(
            f"[:material-open-in-new: View in Swagger UI]({swagger_url})"
            "{ .md-button }"
        )
        lines.append("")

        svg_filename = make_puml_filename(svc_name, method, path) + ".svg"
        if svg_filename in svg_files:
            lines.append(
                f'<div class="diagram-wrap">'
                f'<a href="../svg/{svg_filename}" target="_blank" class="diagram-expand" title="Open in new tab">\u2922</a>'
                f'<object data="../svg/{svg_filename}" type="image/svg+xml" '
                f'style="max-width: 100%;">'
                f'{method} {path} sequence diagram</object>'
                f'</div>'
            )
        else:
            lines.append(f"*Diagram not available for {method} {path}*")

        lines.append("")

    # Consuming Applications section
    consumers = APP_CONSUMERS.get(svc_name, [])
    if consumers:
        lines.append("---")
        lines.append("")
        lines.append("## :material-cellphone-link: Consuming Applications")
        lines.append("")
        lines.append("| Application | Screens Using This Service |")
        lines.append("|-------------|---------------------------|")
        by_app = {}
        for app_name, screen_name in consumers:
            by_app.setdefault(app_name, []).append(screen_name)
        for app_name, screen_list in by_app.items():
            title = APP_TITLES.get(app_name, app_name)
            screens_str = ", ".join(screen_list)
            lines.append(f"| [{title}](../../applications/{app_name}/) | {screens_str} |")
        lines.append("")

    # Events Published section
    published_events = EVENTS_BY_PRODUCER.get(svc_name, [])
    if published_events:
        lines.append("---")
        lines.append("")
        lines.append("## :material-broadcast: Events Published")
        lines.append("")
        lines.append("| Event | Channel | Trigger | Consumers |")
        lines.append("|-------|---------|---------|-----------|")
        for evt_name in published_events:
            evt = EVENT_CATALOG[evt_name]
            trigger_method, trigger_path = evt["trigger"]
            trigger_summary = ALL_ENDPOINT_SUMMARIES.get(
                (svc_name, trigger_method, trigger_path), ""
            )
            if trigger_summary:
                anchor = "#" + heading_slug(trigger_method, trigger_path, trigger_summary)
                trigger_link = f"[`{trigger_method} {trigger_path}`]({anchor})"
            else:
                trigger_link = f"`{trigger_method} {trigger_path}`"
            consumer_links = []
            for c in evt["consumers"]:
                consumer_links.append(f"[{c}](../{c}/)")
            consumers_str = ", ".join(consumer_links)
            evt_slug = re.sub(r'[^\w\s-]', '', evt_name).strip().lower().replace(' ', '-')
            lines.append(
                f"| [`{evt_name}`](/events/#{evt_slug}) "
                f"| `{evt['channel']}` "
                f"| {trigger_link} "
                f"| {consumers_str} |"
            )
        lines.append("")

    # Events Consumed section
    consumed_events = EVENTS_BY_CONSUMER.get(svc_name, [])
    if consumed_events:
        lines.append("---")
        lines.append("")
        lines.append("## :material-broadcast-off: Events Consumed")
        lines.append("")
        lines.append("| Event | Producer | Channel |")
        lines.append("|-------|----------|---------|")
        for evt_name in consumed_events:
            evt = EVENT_CATALOG[evt_name]
            producer = evt["producer"]
            evt_slug = re.sub(r'[^\w\s-]', '', evt_name).strip().lower().replace(' ', '-')
            lines.append(
                f"| [`{evt_name}`](/events/#{evt_slug}) "
                f"| [{producer}](../{producer}/) "
                f"| `{evt['channel']}` |"
            )
        lines.append("")

    return "\n".join(lines)


def generate_index_page(all_services):
    total_endpoints = sum(s[2] for s in all_services)

    lines = []
    lines.append("---")
    lines.append("hide:")
    lines.append("  - toc")
    lines.append("tags:")
    lines.append("  - microservice")
    lines.append("---")
    lines.append("")
    lines.append('<div class="hero" markdown>')
    lines.append("")
    lines.append("# Microservice Pages")
    lines.append("")
    lines.append(
        '<p class="subtitle">'
        "Deep-Dive Architecture Documentation for Every NovaTrek Service"
        "</p>"
    )
    lines.append("")
    lines.append(
        f'<span class="version-badge">'
        f"{len(all_services)} Services &middot; {total_endpoints} Endpoints"
        f"</span>"
    )
    lines.append("")
    lines.append("</div>")
    lines.append("")
    lines.append(
        "Each microservice page provides **PlantUML sequence diagrams** for every "
        "API endpoint with clickable links to other services and Swagger UI, "
        "data store documentation, and direct links to the interactive API reference."
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    # Enterprise C4 diagram
    lines.append("## Enterprise Architecture")
    lines.append("")
    lines.append(
        '<div class="diagram-wrap">'
        '<a href="svg/enterprise-c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">\u2922</a>'
        '<object data="svg/enterprise-c4-context.svg" type="image/svg+xml" '
        'style="width:100%;max-width:1400px"></object></div>'
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    domain_order = [
        "Operations", "Guest Identity", "Booking", "Product Catalog",
        "Safety", "Logistics", "Guide Management", "External", "Support",
    ]

    by_domain = {}
    for svc_name, title, ep_count, version, domain in all_services:
        by_domain.setdefault(domain, []).append((svc_name, title, ep_count, version))

    for domain_name in domain_order:
        svcs = by_domain.get(domain_name, [])
        if not svcs:
            continue

        lines.append(f"## {domain_name}")
        lines.append("")
        lines.append("| Service | Version | Endpoints | Page |")
        lines.append("|---------|---------|-----------|------|")

        for svc_name, title, ep_count, version in sorted(svcs):
            lines.append(
                f"| **{title}**<br><small>`{svc_name}`</small> "
                f"| `{version}` "
                f"| {ep_count} endpoints "
                f"| [:material-arrow-right: Open]({svc_name}.md)" + "{ .md-button } |"
            )

        lines.append("")

    return "\n".join(lines)


# ============================================================
# Event Catalog Page Generation
# ============================================================

EVENTS_DIR = os.path.join(WORKSPACE_ROOT, "portal", "docs", "events")


def build_event_flow_puml():
    """Generate a PlantUML diagram showing all event producers, Kafka, and consumers."""
    L = []
    L.append("@startuml")
    L.append("!theme plain")
    L.append("skinparam backgroundColor #FAFAFA")
    L.append("skinparam defaultFontName Inter")
    L.append("skinparam defaultFontSize 12")
    L.append("skinparam roundCorner 8")
    L.append("skinparam componentStyle rectangle")
    L.append("title NovaTrek Event Flow")
    L.append("")

    # Collect unique producers and consumers
    producers = set()
    consumers = set()
    for evt_name, evt in EVENT_CATALOG.items():
        producers.add(evt["producer"])
        for c in evt["consumers"]:
            consumers.add(c)

    # Declare producers (left side)
    L.append("rectangle \"Producers\" {")
    for p in sorted(producers):
        _, color = get_domain_info(p)
        L.append(f'  component "{p}" as {p.replace("-", "_")} [[/microservices/{p}/]] {color}')
    L.append("}")
    L.append("")

    # Kafka in the middle
    L.append('queue "Kafka Event Bus" as kafka #F0E6FF')
    L.append("")

    # Declare consumers (right side)
    L.append("rectangle \"Consumers\" {")
    for c in sorted(consumers):
        _, color = get_domain_info(c)
        L.append(f'  component "{c}" as {c.replace("-", "_")} [[/microservices/{c}/]] {color}')
    L.append("}")
    L.append("")

    # Draw arrows from producers to Kafka
    for evt_name, evt in sorted(EVENT_CATALOG.items()):
        p_alias = evt["producer"].replace("-", "_")
        L.append(f'{p_alias} -right-> kafka : {evt_name}')

    L.append("")

    # Draw arrows from Kafka to consumers
    drawn = set()
    for evt_name, evt in sorted(EVENT_CATALOG.items()):
        for c in evt["consumers"]:
            c_alias = c.replace("-", "_")
            key = (evt_name, c_alias)
            if key not in drawn:
                drawn.add(key)
                L.append(f'kafka -right-> {c_alias} : {evt_name}')

    L.append("")
    L.append("@enduml")
    return "\n".join(L)


def generate_event_catalog_page():
    """Generate the Event Catalog index page."""
    lines = []
    lines.append("---")
    lines.append("hide:")
    lines.append("  - toc")
    lines.append("tags:")
    lines.append("  - events")
    lines.append("  - kafka")
    lines.append("---")
    lines.append("")
    lines.append('<div class="hero" markdown>')
    lines.append("")
    lines.append("# Event Catalog")
    lines.append("")
    lines.append(
        '<p class="subtitle">'
        "Domain Events Published and Consumed Across NovaTrek Services"
        "</p>"
    )
    lines.append("")
    lines.append(
        f'<span class="version-badge">'
        f"{len(EVENT_CATALOG)} Events &middot; "
        f"{len(EVENTS_BY_PRODUCER)} Producers &middot; "
        f"{len(EVENTS_BY_CONSUMER)} Consumers"
        f"</span>"
    )
    lines.append("")
    lines.append("</div>")
    lines.append("")
    lines.append(
        "The NovaTrek platform uses **Apache Kafka** as its event bus for "
        "asynchronous inter-service communication. Each event is published to a "
        "dedicated channel and consumed by one or more downstream services."
    )
    lines.append("")

    # Event flow diagram
    lines.append("---")
    lines.append("")
    lines.append("## Event Flow Overview")
    lines.append("")
    lines.append(
        '<div class="diagram-wrap">'
        '<a href="../microservices/svg/event-flow.svg" target="_blank" class="diagram-expand" title="Open in new tab">\u2922</a>'
        '<object data="../microservices/svg/event-flow.svg" type="image/svg+xml" '
        'style="width:100%;max-width:1400px"></object></div>'
    )
    lines.append("")

    # Group events by domain
    lines.append("---")
    lines.append("")

    domain_order = [
        "Operations", "Guest Identity", "Booking", "Product Catalog",
        "Safety", "Logistics", "Guide Management", "External", "Support",
    ]

    by_domain = {}
    for evt_name, evt in EVENT_CATALOG.items():
        by_domain.setdefault(evt["domain"], []).append((evt_name, evt))

    for domain_name in domain_order:
        events = by_domain.get(domain_name, [])
        if not events:
            continue

        lines.append(f"## {domain_name}")
        lines.append("")
        lines.append("| Event | Channel | Producer | Consumers | Schema |")
        lines.append("|-------|---------|----------|-----------|--------|")

        for evt_name, evt in sorted(events):
            producer = evt["producer"]
            consumer_links = ", ".join(
                f"[{c}](../microservices/{c}/)" for c in evt["consumers"]
            )
            lines.append(
                f"| **{evt_name}** "
                f"| `{evt['channel']}` "
                f"| [{producer}](../microservices/{producer}/) "
                f"| {consumer_links} "
                f"| [:material-code-json:](../events-ui/{producer}.html \"View event schema\") |"
            )
        lines.append("")

    # Individual event detail sections (for deep-link anchors)
    lines.append("---")
    lines.append("")
    lines.append("## Event Details")
    lines.append("")

    for evt_name in sorted(EVENT_CATALOG.keys()):
        evt = EVENT_CATALOG[evt_name]
        lines.append(f"### {evt_name}")
        lines.append("")
        trigger_method, trigger_path = evt["trigger"]
        trigger_summary = ALL_ENDPOINT_SUMMARIES.get(
            (evt["producer"], trigger_method, trigger_path), ""
        )
        if trigger_summary:
            anchor = "#" + heading_slug(trigger_method, trigger_path, trigger_summary)
            trigger_link = f"[`{trigger_method} {trigger_path}`](../microservices/{evt['producer']}/{anchor})"
        else:
            trigger_link = f"`{trigger_method} {trigger_path}`"

        lines.append(f"- **Channel:** `{evt['channel']}`")
        lines.append(f"- **Producer:** [{evt['producer']}](../microservices/{evt['producer']}/)")
        lines.append(f"- **Trigger:** {trigger_link}")
        lines.append(f"- **Domain:** {evt['domain']}")
        lines.append(f"- **Description:** {evt['summary']}")
        lines.append(f"- **Schema:** [:material-code-json: View Event Schema](../events-ui/{evt['producer']}.html)")
        lines.append("")
        lines.append("**Consumers:**")
        lines.append("")
        for c in evt["consumers"]:
            lines.append(f"- [{c}](../microservices/{c}/)")
        lines.append("")

    # AsyncAPI specs reference
    lines.append("---")
    lines.append("")
    lines.append("## AsyncAPI Specifications")
    lines.append("")
    lines.append(
        "Each producing service has an AsyncAPI 3.0 specification file "
        "describing its published events in detail."
    )
    lines.append("")
    lines.append("| Service | Spec File | Interactive Viewer |")
    lines.append("|---------|-----------|-------------------|")
    events_dir = os.path.join(WORKSPACE_ROOT, "portal", "docs", "events")
    if os.path.isdir(events_dir):
        for fname in sorted(os.listdir(events_dir)):
            if fname.endswith(".events.yaml"):
                svc = fname.replace(".events.yaml", "")
                lines.append(
                    f"| [{svc}](../microservices/{svc}/) "
                    f"| [`{fname}`](../events/{fname}) "
                    f"| [:material-code-json: View Schema](../events-ui/{svc}.html) |"
                )
    lines.append("")

    return "\n".join(lines)


ACTORS_DIR = os.path.join(WORKSPACE_ROOT, "portal", "docs", "actors")


def actor_anchor(name):
    """Generate MkDocs-compatible anchor from an actor name."""
    text = unicodedata.normalize('NFKD', name)
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)


def generate_actors_page():
    """Generate the Actor Catalog index page."""
    lines = []
    lines.append("---")
    lines.append("hide:")
    lines.append("  - toc")
    lines.append("tags:")
    lines.append("  - actors")
    lines.append("  - catalog")
    lines.append("---")
    lines.append("")
    lines.append('<div class="hero" markdown>')
    lines.append("")
    lines.append("# Actor Catalog")
    lines.append("")
    lines.append(
        '<p class="subtitle">'
        "All Actors Across the NovaTrek Enterprise"
        "</p>"
    )

    # Count by type
    type_counts = {}
    for a in ACTORS.values():
        t = a["type"]
        type_counts[t] = type_counts.get(t, 0) + 1
    badge_parts = " &middot; ".join(f"{v} {k}s" for k, v in sorted(type_counts.items()))
    lines.append(f'<span class="version-badge">{len(ACTORS)} Actors &middot; {badge_parts}</span>')
    lines.append("")
    lines.append("</div>")
    lines.append("")
    lines.append(
        "This catalog lists every actor that interacts with the NovaTrek platform: "
        "people, frontend applications, internal microservices, external systems, and infrastructure components. "
        "Each actor links to its detailed page where available."
    )
    lines.append("")

    # Group actors by type, maintaining order
    type_order = ["Human", "Frontend Application", "Infrastructure", "External System"]
    by_type = {}
    for name, info in ACTORS.items():
        by_type.setdefault(info["type"], []).append((name, info))

    # Icon per type
    type_icon = {
        "Human": ":material-account:",
        "Frontend Application": ":material-application:",
        "Infrastructure": ":material-server-network:",
        "External System": ":material-cloud:",
    }

    for actor_type in type_order:
        actors = by_type.get(actor_type, [])
        if not actors:
            continue
        icon = type_icon.get(actor_type, "")
        lines.append("---")
        lines.append("")
        lines.append(f"## {icon} {actor_type}s")
        lines.append("")

        if actor_type == "Human":
            lines.append("| Actor | Domain | Description | Interacts With |")
            lines.append("|-------|--------|-------------|----------------|")
            for name, info in sorted(actors):
                interactions = ", ".join(
                    f"[{APP_TITLES.get(i, i)}](../applications/{i}/)" for i in info.get("interacts_with", [])
                )
                lines.append(f"| **{name}** | {info['domain']} | {info['description']} | {interactions} |")
            lines.append("")

        elif actor_type == "Frontend Application":
            lines.append("| Application | Display Name | Domain | Technology | Team | Description |")
            lines.append("|-------------|-------------|--------|------------|------|-------------|")
            for name, info in sorted(actors):
                display = APP_TITLES.get(name, name)
                lines.append(
                    f"| [{name}](../applications/{name}/) | {display} | {info['domain']} "
                    f"| {info.get('technology', '')} | {info.get('team', '')} | {info['description']} |"
                )
            lines.append("")

        elif actor_type == "Infrastructure":
            lines.append("| Component | Technology | Domain | Description |")
            lines.append("|-----------|------------|--------|-------------|")
            for name, info in sorted(actors):
                lines.append(
                    f"| **{name}** | {info.get('technology', '')} "
                    f"| {info['domain']} | {info['description']} |"
                )
            lines.append("")

        elif actor_type == "External System":
            lines.append("| System | Technology | Domain | PCI | Description |")
            lines.append("|--------|------------|--------|-----|-------------|")
            for name, info in sorted(actors):
                pci_badge = ":material-shield-lock: PCI" if info.get("pci") else ""
                lines.append(
                    f"| **{name}** | {info.get('technology', '')} "
                    f"| {info['domain']} | {pci_badge} | {info['description']} |"
                )
            lines.append("")

    # Internal Microservices section (from DOMAINS, not ACTORS dict)
    lines.append("---")
    lines.append("")
    lines.append("## :material-hexagon-multiple: Internal Microservices")
    lines.append("")
    lines.append("| Service | Domain | Description |")
    lines.append("|---------|--------|-------------|")
    all_svcs = set()
    for domain_name, domain_info in sorted(DOMAINS.items()):
        for svc in sorted(domain_info["services"]):
            all_svcs.add(svc)
            lines.append(
                f"| [{svc}](../microservices/{svc}/) | {domain_name} "
                f"| See [microservice page](../microservices/{svc}/) for full details |"
            )
    lines.append("")

    # Detail sections for deep-link anchors (one H3 per actor)
    lines.append("---")
    lines.append("")
    lines.append("## Actor Details")
    lines.append("")

    for name, info in sorted(ACTORS.items()):
        lines.append(f"### {name}")
        lines.append("")
        lines.append(f"- **Type:** {info['type']}")
        lines.append(f"- **Domain:** {info['domain']}")
        lines.append(f"- **Description:** {info['description']}")
        if info.get("technology"):
            lines.append(f"- **Technology:** {info['technology']}")
        if info.get("pci"):
            lines.append("- **Compliance:** :material-shield-lock: PCI DSS scope")
        if info.get("team"):
            lines.append(f"- **Team:** {info['team']}")

        # Show which services reference this actor
        usage = ACTOR_SERVICE_USAGE.get(name, set())
        if usage:
            lines.append("")
            lines.append("**Referenced by:**")
            lines.append("")
            for svc in sorted(usage):
                lines.append(f"- [{svc}](../microservices/{svc}/)")
        lines.append("")

    # Internal services detail
    for svc in sorted(all_svcs):
        domain, color = get_domain_info(svc)
        lines.append(f"### {svc}")
        lines.append("")
        lines.append(f"- **Type:** Internal Microservice")
        lines.append(f"- **Domain:** {domain}")
        lines.append(f"- **Details:** [{svc} Microservice Page](../microservices/{svc}/)")
        lines.append("")

    return "\n".join(lines)


# ============================================================
# Main
# ============================================================

def main():
    print("Generating NovaTrek Microservice Pages (PlantUML SVGs)...")
    print(f"  Specs:  {SPECS_DIR}")
    print(f"  Output: {OUTPUT_DIR}")
    print()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(PUML_DIR, exist_ok=True)
    os.makedirs(SVG_DIR, exist_ok=True)

    spec_files = sorted(f for f in os.listdir(SPECS_DIR) if f.endswith(".yaml"))

    # Pre-load all endpoint summaries for cross-service deep linking
    for spec_file in spec_files:
        svc_name = spec_file.replace(".yaml", "")
        with open(os.path.join(SPECS_DIR, spec_file)) as f:
            spec = yaml.safe_load(f)
        for path, path_item in spec.get("paths", {}).items():
            for method in ["get", "post", "put", "patch", "delete"]:
                if method in path_item:
                    summary = path_item[method].get("summary", "")
                    ALL_ENDPOINT_SUMMARIES[(svc_name, method.upper(), path)] = summary

    all_pumls = []
    all_services = []

    for spec_file in spec_files:
        svc_name = spec_file.replace(".yaml", "")
        spec_path = os.path.join(SPECS_DIR, spec_file)

        with open(spec_path) as f:
            spec = yaml.safe_load(f)

        endpoints = extract_endpoints(spec)
        title = spec.get("info", {}).get("title", svc_name)
        version = spec.get("info", {}).get("version", "0.0.0")
        domain, _ = get_domain_info(svc_name)
        ds = DATA_STORES.get(svc_name, {})

        print(f"  {svc_name}: {len(endpoints)} endpoints")

        for ep in endpoints:
            puml_content = build_puml(
                svc_name, ep["method"], ep["path"], ep["summary"],
                ds.get("engine", "PostgreSQL"),
                CROSS_SERVICE_CALLS.get((svc_name, ep["method"], ep["path"]), []),
                ep["operationId"],
                ep["tags"],
            )
            fname = make_puml_filename(svc_name, ep["method"], ep["path"])
            puml_path = os.path.join(PUML_DIR, f"{fname}.puml")
            with open(puml_path, "w") as f:
                f.write(puml_content)
            all_pumls.append(puml_path)

        all_services.append((svc_name, title, len(endpoints), version, domain))

    # Generate C4 context diagrams for each service
    for svc_name, _, _, _, _ in all_services:
        c4_puml = build_c4_context_puml(svc_name)
        c4_path = os.path.join(PUML_DIR, f"{svc_name}--c4-context.puml")
        with open(c4_path, "w") as f:
            f.write(c4_puml)
        all_pumls.append(c4_path)

    # Generate enterprise rollup C4 diagram
    enterprise_puml = build_enterprise_c4_puml()
    enterprise_path = os.path.join(PUML_DIR, "enterprise-c4-context.puml")
    with open(enterprise_path, "w") as f:
        f.write(enterprise_puml)
    all_pumls.append(enterprise_path)

    # Generate event flow diagram
    event_flow_puml = build_event_flow_puml()
    event_flow_path = os.path.join(PUML_DIR, "event-flow.puml")
    with open(event_flow_path, "w") as f:
        f.write(event_flow_puml)
    all_pumls.append(event_flow_path)

    total_ep = sum(s[2] for s in all_services)
    print(f"\n  Generated {len(all_pumls)} PUML files ({total_ep} endpoint + {len(all_services)} C4 context + 1 enterprise + 1 event flow)")

    # Render all PUMLs to SVG
    print("  Rendering SVGs with PlantUML...")
    result = subprocess.run(
        ["plantuml", "-tsvg", "-o", SVG_DIR] + all_pumls,
        capture_output=True, text=True, timeout=300,
    )
    if result.returncode != 0:
        print(f"  WARNING: PlantUML returned {result.returncode}")
        if result.stderr:
            print(f"  stderr: {result.stderr[:500]}")

    svg_files = set(f for f in os.listdir(SVG_DIR) if f.endswith(".svg"))
    print(f"  Rendered {len(svg_files)} SVGs")

    # Generate Markdown pages
    print("  Generating Markdown pages...")
    for spec_file in spec_files:
        svc_name = spec_file.replace(".yaml", "")
        spec_path = os.path.join(SPECS_DIR, spec_file)

        with open(spec_path) as f:
            spec = yaml.safe_load(f)

        page = generate_service_page(svc_name, spec, svg_files)
        with open(os.path.join(OUTPUT_DIR, f"{svc_name}.md"), "w") as f:
            f.write(page)

    index_page = generate_index_page(all_services)
    with open(os.path.join(OUTPUT_DIR, "index.md"), "w") as f:
        f.write(index_page)

    # Generate Event Catalog page
    os.makedirs(EVENTS_DIR, exist_ok=True)
    event_catalog_page = generate_event_catalog_page()
    event_catalog_path = os.path.join(EVENTS_DIR, "index.md")
    with open(event_catalog_path, "w") as f:
        f.write(event_catalog_page)
    print(f"  Event Catalog: {event_catalog_path}")

    # Generate Actor Catalog page
    os.makedirs(ACTORS_DIR, exist_ok=True)
    actors_page = generate_actors_page()
    actors_path = os.path.join(ACTORS_DIR, "index.md")
    with open(actors_path, "w") as f:
        f.write(actors_page)
    print(f"  Actor Catalog: {actors_path}")

    print()
    print(f"  Done! {len(all_services)} service pages, {total_ep} endpoint diagrams, 1 event catalog, 1 actor catalog")
    print(f"  PUML: {PUML_DIR}/")
    print(f"  SVGs: {SVG_DIR}/")
    print(f"  Pages: {OUTPUT_DIR}/")
    print(f"  Events: {EVENTS_DIR}/")
    print(f"  Actors: {ACTORS_DIR}/")


if __name__ == "__main__":
    main()
