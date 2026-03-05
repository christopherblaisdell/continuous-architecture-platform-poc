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

# --- svc-payments ---
CROSS_SERVICE_CALLS[("svc-payments", "POST", "/payments")] = [
    ("FD", "Fraud Detection API", "Screen transaction", False, None),
    ("ExtPay", "Stripe API", "Process payment", False, None),
    ("Ntfy", "Notifications", "Send payment receipt", True, ("POST", "/notifications")),
]
CROSS_SERVICE_CALLS[("svc-payments", "POST", "/payments/{payment_id}/refund")] = [
    ("ExtPay", "Stripe API", "Process refund", False, None),
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
# C4 Context Diagram Generation
# ============================================================

def _safe_alias(name):
    """Create a valid PlantUML alias from a service or system name."""
    return re.sub(r'[^a-zA-Z0-9]', '_', name)


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

    L = []
    L.append("@startuml")
    L.append("!include <c4/C4_Container>")
    L.append("")
    L.append("LAYOUT_WITH_LEGEND()")
    L.append("LAYOUT_TOP_DOWN()")
    L.append("")
    L.append(f'title {svc_name} — Integration Context')
    L.append("")

    # Frontend applications at the top
    for app in app_names:
        app_title = APP_TITLES.get(app, app)
        app_type = "Web App" if app.startswith("web-") else "Mobile App"
        a = _safe_alias(app)
        L.append(f'Person({a}, "{app_title}", "{app_type}", $link="/applications/{app}/")')

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
        L.append(f'    Container({_safe_alias(peer)}, "{peer}", "Java / Spring Boot", "{peer_domain}", $link="/microservices/{peer}/")')

    # Outbound peer services inside the boundary
    for peer in sorted(outbound_svcs.keys()):
        if peer in inbound_svcs:
            continue  # already added
        peer_domain, _ = get_domain_info(peer)
        L.append(f'    Container({_safe_alias(peer)}, "{peer}", "Java / Spring Boot", "{peer_domain}", $link="/microservices/{peer}/")')

    L.append("}")
    L.append("")

    # External systems outside boundary
    for ext in sorted(outbound_ext.keys()):
        L.append(f'System_Ext({_safe_alias(ext)}, "{ext}", "Third-party service")')
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
        L.append(f'Rel({_safe_alias(peer)}, {svc_alias}, "{label}", "HTTPS")')

    # Relationships — database
    if ds:
        L.append(f'Rel({svc_alias}, {db_alias}, "Reads/Writes", "SQL/TCP")')

    # Relationships — outbound services
    for peer in sorted(outbound_svcs.keys()):
        actions = sorted(outbound_svcs[peer])
        label = actions[0] if len(actions) == 1 else f"{len(actions)} calls"
        L.append(f'Rel({svc_alias}, {_safe_alias(peer)}, "{label}", "HTTPS")')

    # Relationships — external systems
    for ext in sorted(outbound_ext.keys()):
        actions = sorted(outbound_ext[ext])
        label = actions[0] if len(actions) == 1 else ", ".join(actions[:2])
        L.append(f'Rel({svc_alias}, {_safe_alias(ext)}, "{label}", "HTTPS")')

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

    # Title
    title_text = f"{method} {path}"
    L.append(f"title {title_text}\\n{summary}")
    L.append("")

    # Participants - clickable
    L.append('participant "Client" as Client')
    L.append('participant "API Gateway" as GW #DBEAFE')
    L.append(f'participant "{svc_name}" as Svc [[/microservices/{svc_name}/]] #E8F4F8')

    declared = set()
    for call in (ext_calls or []):
        alias, label, action = call[0], call[1], call[2]
        target_ep = call[4] if len(call) > 4 else None
        if alias in declared:
            continue
        declared.add(alias)
        target_svc = label_to_svc_name(label)
        if target_svc:
            L.append(f'participant "{label}" as {alias} [[/microservices/{target_svc}/]] #FFF8F0')
        elif label == "Event Bus":
            L.append(f'queue "Kafka" as {alias} #F0E6FF')
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
            if target_svc:
                anchor = ""
                if target_ep:
                    anchor = endpoint_anchor(target_svc, target_ep[0], target_ep[1])
                L.append(f"Svc -> {alias} : [[/microservices/{target_svc}/{anchor} {action}]]")
            else:
                L.append(f"Svc -> {alias} : {action}")
            L.append(f"activate {alias} #DBEAFE")
            L.append(f"{alias} --> Svc : OK")
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
            f'<div style="overflow-x: auto; width: 100%;">'
            f'<object data="../svg/{c4_svg}" type="image/svg+xml" '
            f'style="max-width: 100%;">{svc_name} C4 context diagram</object></div>'
        )
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("## :material-database: Data Store")
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
                f'<div style="overflow-x: auto; width: 100%;">'
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

    total_ep = sum(s[2] for s in all_services)
    print(f"\n  Generated {len(all_pumls)} PUML files ({total_ep} endpoint + {len(all_services)} C4 context)")

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

    print()
    print(f"  Done! {len(all_services)} service pages, {total_ep} endpoint diagrams")
    print(f"  PUML: {PUML_DIR}/")
    print(f"  SVGs: {SVG_DIR}/")
    print(f"  Pages: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
