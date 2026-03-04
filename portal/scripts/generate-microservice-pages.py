#!/usr/bin/env python3
"""Generate Microservice Pages for the NovaTrek Architecture Portal.

Creates a deep-dive page for each of the 19 NovaTrek microservices with:
  - Service metadata and description
  - Data store documentation
  - Internal sequence diagrams for EVERY endpoint (Mermaid)
  - Direct links to Swagger UI for each endpoint
  - Cross-service integration flows where applicable

Usage:
    python3 portal/scripts/generate-microservice-pages.py
"""

import os
import yaml
from urllib.parse import quote

# ────────────────────────────────────────────────────────────
# Paths
# ────────────────────────────────────────────────────────────

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPECS_DIR = os.path.join(WORKSPACE_ROOT, "portal", "docs", "specs")
OUTPUT_DIR = os.path.join(WORKSPACE_ROOT, "portal", "docs", "microservices")

# ────────────────────────────────────────────────────────────
# Mermaid Theme — NovaTrek Corporate Palette
# ────────────────────────────────────────────────────────────

MERMAID_THEME = (
    "%%{init: {'theme': 'base', 'themeVariables': {"
    "'primaryColor': '#1a2744', "
    "'primaryTextColor': '#fff', "
    "'primaryBorderColor': '#c77b30', "
    "'lineColor': '#475569', "
    "'secondaryColor': '#dbeafe', "
    "'tertiaryColor': '#fff7ed', "
    "'noteBkgColor': '#fef3e7', "
    "'noteTextColor': '#1e293b', "
    "'noteBorderColor': '#c77b30', "
    "'actorBkg': '#1a2744', "
    "'actorTextColor': '#fff', "
    "'actorBorder': '#c77b30', "
    "'activationBkgColor': '#dbeafe', "
    "'activationBorderColor': '#3b82f6', "
    "'signalColor': '#1e293b', "
    "'signalTextColor': '#1e293b'"
    "}}}%%"
)

# ────────────────────────────────────────────────────────────
# Domain Configuration
# ────────────────────────────────────────────────────────────

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

# ────────────────────────────────────────────────────────────
# Data Store Metadata (Synthetic — NovaTrek Adventures)
# ────────────────────────────────────────────────────────────

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
        "engine": "PostgreSQL 15 + Redis 7",
        "schema": "scheduling",
        "tables": ["schedule_requests", "daily_schedules", "schedule_conflicts", "optimization_runs"],
        "features": [
            "Optimistic locking per ADR-011",
            "Redis for schedule lock cache and optimization queue",
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
        "engine": "PostgreSQL 15 + Redis 7",
        "schema": "notifications",
        "tables": ["notifications", "templates", "delivery_log", "channel_preferences"],
        "features": [
            "Redis queue for async delivery processing",
            "Template versioning with rollback support",
            "Multi-channel delivery: email, SMS, push, in-app",
        ],
        "volume": "~15,000 notifications/day",
    },
    "svc-analytics": {
        "engine": "TimescaleDB (PostgreSQL 15)",
        "schema": "analytics",
        "tables": ["booking_metrics", "revenue_metrics", "utilization_metrics", "satisfaction_scores", "safety_metrics", "guide_performance"],
        "features": [
            "TimescaleDB hypertables for time-series aggregation",
            "Continuous aggregates for real-time dashboards",
            "30-day raw retention, 2-year aggregate retention",
        ],
        "volume": "~50K metric inserts/day (event-driven)",
    },
    "svc-loyalty-rewards": {
        "engine": "PostgreSQL 15",
        "schema": "loyalty",
        "tables": ["members", "point_transactions", "tiers", "redemptions"],
        "features": [
            "Points balance with optimistic locking for concurrency",
            "Tier recalculation triggers on point thresholds",
            "Point expiry date tracking and automated cleanup",
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
        "engine": "Redis 7 + PostgreSQL 15",
        "schema": "weather",
        "tables": ["weather_stations", "forecast_cache", "alert_history"],
        "features": [
            "Redis TTL cache for current conditions (5-min TTL)",
            "External weather API response caching and aggregation",
            "Severe weather alert deduplication",
        ],
        "volume": "~10K weather reads/day, ~100 external API fetches/day",
    },
}

# ────────────────────────────────────────────────────────────
# Cross-Service Integration Map
# Key: (service, HTTP method, path) -> [(alias, label, action, is_async)]
# ────────────────────────────────────────────────────────────

CROSS_SERVICE_CALLS = {}

# -- svc-check-in --
CROSS_SERVICE_CALLS[("svc-check-in", "POST", "/check-ins")] = [
    ("Res", "Reservations", "Verify reservation exists", False),
    ("Safety", "Safety Compliance", "Validate active waiver", False),
]
CROSS_SERVICE_CALLS[("svc-check-in", "POST", "/check-ins/{check_in_id}/gear-verification")] = [
    ("Gear", "Gear Inventory", "Verify gear assignment", False),
]

# -- svc-reservations --
CROSS_SERVICE_CALLS[("svc-reservations", "POST", "/reservations")] = [
    ("GP", "Guest Profiles", "Validate guest identity", False),
    ("TC", "Trip Catalog", "Check trip availability", False),
    ("Kafka", "Event Bus", "reservation.created", True),
]
CROSS_SERVICE_CALLS[("svc-reservations", "PUT", "/reservations/{reservation_id}")] = [
    ("TC", "Trip Catalog", "Verify availability", False),
]
CROSS_SERVICE_CALLS[("svc-reservations", "POST", "/reservations/{reservation_id}/participants")] = [
    ("GP", "Guest Profiles", "Validate participant", False),
]
CROSS_SERVICE_CALLS[("svc-reservations", "PUT", "/reservations/{reservation_id}/status")] = [
    ("Kafka", "Event Bus", "reservation.status_changed", True),
]

# -- svc-scheduling-orchestrator --
CROSS_SERVICE_CALLS[("svc-scheduling-orchestrator", "POST", "/schedule-requests")] = [
    ("GM", "Guide Mgmt", "Check guide availability", False),
    ("TM", "Trail Mgmt", "Verify trail conditions", False),
    ("WX", "Weather Svc", "Get forecast", False),
    ("TC", "Trip Catalog", "Get trip details", False),
]
CROSS_SERVICE_CALLS[("svc-scheduling-orchestrator", "POST", "/schedule-optimization")] = [
    ("GM", "Guide Mgmt", "Get all available guides", False),
    ("LS", "Location Svc", "Check location capacity", False),
]
CROSS_SERVICE_CALLS[("svc-scheduling-orchestrator", "POST", "/schedule-conflicts/resolve")] = [
    ("GM", "Guide Mgmt", "Reassign guide", False),
]

# -- svc-partner-integrations --
CROSS_SERVICE_CALLS[("svc-partner-integrations", "POST", "/partner-bookings")] = [
    ("Res", "Reservations", "Create reservation", False),
]
CROSS_SERVICE_CALLS[("svc-partner-integrations", "POST", "/partner-bookings/{booking_id}/confirm")] = [
    ("Res", "Reservations", "Confirm reservation", False),
    ("Pay", "Payments Svc", "Process commission", False),
]

# -- svc-guest-profiles --
CROSS_SERVICE_CALLS[("svc-guest-profiles", "POST", "/guests")] = [
    ("Kafka", "Event Bus", "guest.registered", True),
]
CROSS_SERVICE_CALLS[("svc-guest-profiles", "GET", "/guests/{guest_id}/adventure-history")] = [
    ("Res", "Reservations", "Query past bookings", False),
]

# -- svc-payments --
CROSS_SERVICE_CALLS[("svc-payments", "POST", "/payments")] = [
    ("ExtPay", "Payment Gateway", "Process payment", False),
]
CROSS_SERVICE_CALLS[("svc-payments", "POST", "/payments/{payment_id}/refund")] = [
    ("ExtPay", "Payment Gateway", "Process refund", False),
]

# -- svc-notifications --
CROSS_SERVICE_CALLS[("svc-notifications", "POST", "/notifications")] = [
    ("ExtMsg", "Email/SMS Provider", "Deliver message", True),
]
CROSS_SERVICE_CALLS[("svc-notifications", "POST", "/notifications/bulk")] = [
    ("ExtMsg", "Email/SMS Provider", "Deliver bulk messages", True),
]

# -- svc-safety-compliance --
CROSS_SERVICE_CALLS[("svc-safety-compliance", "POST", "/waivers")] = [
    ("GP", "Guest Profiles", "Validate guest identity", False),
]
CROSS_SERVICE_CALLS[("svc-safety-compliance", "POST", "/incidents")] = [
    ("Ntfy", "Notifications", "Send safety alert", True),
]

# -- svc-gear-inventory --
CROSS_SERVICE_CALLS[("svc-gear-inventory", "POST", "/gear-assignments")] = [
    ("GP", "Guest Profiles", "Validate guest", False),
]

# -- svc-transport-logistics --
CROSS_SERVICE_CALLS[("svc-transport-logistics", "POST", "/transport-requests")] = [
    ("LS", "Location Svc", "Validate pickup location", False),
]

# -- svc-loyalty-rewards --
CROSS_SERVICE_CALLS[("svc-loyalty-rewards", "POST", "/members/{guest_id}/earn")] = [
    ("Res", "Reservations", "Verify completed booking", False),
]
CROSS_SERVICE_CALLS[("svc-loyalty-rewards", "POST", "/members/{guest_id}/redeem")] = [
    ("Pay", "Payments Svc", "Process reward credit", False),
]

# -- svc-media-gallery --
CROSS_SERVICE_CALLS[("svc-media-gallery", "POST", "/media")] = [
    ("S3", "Object Store", "Upload binary file", False),
]
CROSS_SERVICE_CALLS[("svc-media-gallery", "POST", "/media/{media_id}/share")] = [
    ("Ntfy", "Notifications", "Send share link", True),
]

# -- svc-inventory-procurement --
CROSS_SERVICE_CALLS[("svc-inventory-procurement", "POST", "/purchase-orders")] = [
    ("GI", "Gear Inventory", "Verify item catalog", False),
]

# -- svc-weather --
CROSS_SERVICE_CALLS[("svc-weather", "GET", "/weather/current")] = [
    ("ExtWx", "Weather API", "Fetch current conditions", False),
]
CROSS_SERVICE_CALLS[("svc-weather", "GET", "/weather/forecast")] = [
    ("ExtWx", "Weather API", "Fetch multi-day forecast", False),
]
CROSS_SERVICE_CALLS[("svc-weather", "GET", "/weather/alerts")] = [
    ("ExtWx", "Weather API", "Fetch active alerts", False),
]

# -- svc-trail-management --
CROSS_SERVICE_CALLS[("svc-trail-management", "POST", "/trails/{trail_id}/conditions")] = [
    ("WX", "Weather Svc", "Correlate weather data", False),
]


# ============================================================
# Helper Functions
# ============================================================

def get_domain_info(svc_name):
    """Return (domain_name, domain_color) for a service."""
    for domain, info in DOMAINS.items():
        if svc_name in info["services"]:
            return domain, info["color"]
    return "Support", "#64748b"


def extract_endpoints(spec):
    """Extract all endpoints from an OpenAPI spec."""
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
    """Extract short database name for Mermaid participant."""
    if "TimescaleDB" in engine:
        return "TimescaleDB"
    if "PostGIS" in engine:
        return "PostGIS"
    if engine.startswith("Redis"):
        return "Redis"
    if "PostgreSQL" in engine:
        return "PostgreSQL"
    return engine.split()[0]


def has_path_param_at_end(path):
    """Check if path ends with a path parameter like /{id}."""
    parts = path.strip("/").split("/")
    return parts[-1].startswith("{") and parts[-1].endswith("}")


def is_sub_resource(path):
    """Check if path accesses a sub-resource under a parameterized parent."""
    parts = path.strip("/").split("/")
    if len(parts) >= 3:
        has_mid_param = any(p.startswith("{") for p in parts[1:-1])
        end_not_param = not parts[-1].startswith("{")
        return has_mid_param and end_not_param
    return False


def sanitize_mermaid(text):
    """Remove characters that break Mermaid syntax."""
    return (text
        .replace("#", "")
        .replace("<", "")
        .replace(">", "")
        .replace("{", "(")
        .replace("}", ")")
        .replace('"', "'")
        .replace(";", ","))


def path_display(path):
    """Convert path to display format for Mermaid messages."""
    return sanitize_mermaid(path)


def success_status(method):
    """Return expected success HTTP status code."""
    if method == "POST":
        return "201 Created"
    if method == "DELETE":
        return "204 No Content"
    return "200 OK"


def svc_method_name(method, path, operation_id):
    """Generate a service-layer method call description."""
    if operation_id:
        return sanitize_mermaid(operation_id) + "()"
    if method == "GET":
        if has_path_param_at_end(path):
            return "getById(id)"
        return "search(filters)"
    elif method == "POST":
        return "create(body)"
    elif method == "PUT":
        return "update(id, body)"
    elif method == "PATCH":
        return "patch(id, fields)"
    elif method == "DELETE":
        return "delete(id)"
    return "handle(request)"


# ============================================================
# Mermaid Diagram Generation
# ============================================================

def build_diagram(svc_name, method, path, summary, db_engine, ext_calls, operation_id=""):
    """Generate a Mermaid sequence diagram for one endpoint."""

    db_label = get_short_db_name(db_engine)
    disp_path = path_display(path)
    svc_call = svc_method_name(method, path, operation_id)

    lines = [MERMAID_THEME, "sequenceDiagram"]

    # ── Participants (left to right) ──
    lines.append("    participant C as Client")
    lines.append("    participant GW as API Gateway")
    lines.append("    participant Ctrl as Controller")
    lines.append("    participant Svc as Service Layer")

    for alias, label, _, _ in (ext_calls or []):
        lines.append(f"    participant {alias} as {label}")

    lines.append("    participant Repo as Repository")
    lines.append(f"    participant DB as {db_label}")
    lines.append("")

    # ── Request arrival ──
    lines.append(f"    C->>+GW: {method} {disp_path}")
    lines.append("    GW->>+Ctrl: Route request")

    # ── Validation for writes ──
    if method in ("POST", "PUT", "PATCH"):
        lines.append("    Note right of Ctrl: Validate request body")

    # ── Delegate to service layer ──
    lines.append(f"    Ctrl->>+Svc: {svc_call}")

    # ── Cross-service integration (sync) ──
    sync_calls = [c for c in (ext_calls or []) if not c[3]]
    async_calls = [c for c in (ext_calls or []) if c[3]]

    if sync_calls:
        lines.append("")
        lines.append("    rect rgba(199, 123, 48, 0.08)")
        lines.append(f"        Note over Svc,{sync_calls[-1][0]}: Cross-service integration")
        for alias, label, action, _ in sync_calls:
            lines.append(f"        Svc->>+{alias}: {action}")
            lines.append(f"        {alias}-->>-Svc: OK")
        lines.append("    end")

    lines.append("")

    # ── Database operations ──
    if method == "GET":
        if has_path_param_at_end(path):
            lines.append("    Svc->>+Repo: findById(id)")
            lines.append("    Repo->>+DB: SELECT ... WHERE id = ?")
            lines.append("    DB-->>-Repo: Row")
            lines.append("    Repo-->>-Svc: Entity")
            lines.append("    Note right of Repo: Returns 404 if not found")
        elif is_sub_resource(path):
            lines.append("    Svc->>+Repo: findByParent(parentId)")
            lines.append("    Repo->>+DB: SELECT ... WHERE parent_id = ?")
            lines.append("    DB-->>-Repo: ResultSet")
            lines.append("    Repo-->>-Svc: List of results")
        else:
            lines.append("    Svc->>+Repo: findByFilters(criteria)")
            lines.append("    Repo->>+DB: SELECT ... WHERE filters")
            lines.append("    DB-->>-Repo: ResultSet")
            lines.append("    Repo-->>-Svc: Page of results")

    elif method == "POST":
        if is_sub_resource(path):
            lines.append("    Svc->>+Repo: findParent(parentId)")
            lines.append("    Repo->>+DB: SELECT parent")
            lines.append("    DB-->>-Repo: Parent row")
            lines.append("    Repo-->>-Svc: Parent entity")
            lines.append("    Note right of Repo: 404 if parent not found")
        lines.append("    Svc->>+Repo: save(entity)")
        lines.append("    Repo->>+DB: INSERT INTO ...")
        lines.append("    DB-->>-Repo: Created row")
        lines.append("    Repo-->>-Svc: Persisted entity")

    elif method in ("PUT", "PATCH"):
        lines.append("    Svc->>+Repo: findById(id)")
        lines.append("    Repo->>+DB: SELECT ... FOR UPDATE")
        lines.append("    DB-->>-Repo: Current row")
        lines.append("    Repo-->>-Svc: Existing entity")
        note = "Merge changed fields only" if method == "PATCH" else "Replace mutable fields"
        lines.append(f"    Note right of Svc: {note}")
        lines.append("    Svc->>+Repo: save(entity)")
        lines.append("    Repo->>+DB: UPDATE ... SET ...")
        lines.append("    DB-->>-Repo: Updated row")
        lines.append("    Repo-->>-Svc: Updated entity")

    elif method == "DELETE":
        lines.append("    Svc->>+Repo: findById(id)")
        lines.append("    Repo->>+DB: SELECT ... WHERE id = ?")
        lines.append("    DB-->>-Repo: Row")
        lines.append("    Repo-->>-Svc: Entity")
        lines.append("    Note right of Repo: Returns 404 if not found")
        lines.append("    Svc->>+Repo: delete(entity)")
        lines.append("    Repo->>+DB: DELETE FROM ... WHERE id = ?")
        lines.append("    DB-->>-Repo: OK")
        lines.append("    Repo-->>-Svc: void")

    # ── Async events ──
    if async_calls:
        lines.append("")
        for alias, label, action, _ in async_calls:
            lines.append(f"    Svc-){alias}: {action}")

    # ── Response chain ──
    status = success_status(method)
    lines.append("")
    lines.append("    Svc-->>-Ctrl: Result")
    lines.append("    Ctrl-->>-GW: Response")
    lines.append(f"    GW-->>-C: {status}")

    return "\n".join(lines)


# ============================================================
# Page Generation
# ============================================================

def generate_service_page(svc_name, spec):
    """Generate the full Markdown page for one microservice."""

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

    # ── Frontmatter ──
    lines.append("---")
    lines.append("tags:")
    lines.append("  - microservice")
    lines.append(f"  - {svc_name}")
    lines.append(f"  - {domain.lower().replace(' ', '-')}")
    lines.append("---")
    lines.append("")

    # ── Title ──
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

    # ── Description ──
    if desc_first_line:
        lines.append(f"> {desc_first_line}")
        lines.append("")

    # ── Quick links ──
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

    # ── Data Store section ──
    lines.append("## :material-database: Data Store")
    lines.append("")

    if ds:
        tables_fmt = ", ".join(f"`{t}`" for t in ds.get("tables", []))
        features_fmt = " · ".join(ds.get("features", []))

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

    # ── Endpoints section ──
    lines.append(f"## :material-api: Endpoints ({len(endpoints)} total)")
    lines.append("")

    for ep in endpoints:
        method = ep["method"]
        path = ep["path"]
        summary = ep["summary"] or "Endpoint"
        desc = ep["description"]
        op_id = ep["operationId"]
        tags = ep["tags"]
        method_lower = method.lower()

        # Endpoint header with CSS class
        lines.append("---")
        lines.append("")
        lines.append(f"### {method} `{path}` — {summary} {{ .endpoint-{method_lower} }}")
        lines.append("")

        if desc:
            lines.append(f"> {desc}")
            lines.append("")

        # Swagger UI deep link
        tag_encoded = quote(tags[0], safe="") if tags else ""
        anchor = f"#/{tag_encoded}/{op_id}" if tag_encoded and op_id else ""
        swagger_url = f"../services/api/{svc_name}.html{anchor}"
        lines.append(
            f"[:material-open-in-new: View in Swagger UI]({swagger_url})"
            "{ .md-button }"
        )
        lines.append("")

        # Mermaid sequence diagram
        ext_calls = CROSS_SERVICE_CALLS.get((svc_name, method, path), [])
        diagram = build_diagram(
            svc_name, method, path, summary,
            ds.get("engine", "PostgreSQL"), ext_calls, op_id
        )

        lines.append("```mermaid")
        lines.append(diagram)
        lines.append("```")
        lines.append("")

    return "\n".join(lines)


def generate_index_page(all_services):
    """Generate the Microservice Pages landing / index page."""

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
        "Each microservice page provides **internal sequence diagrams** for every "
        "API endpoint, data store documentation, and direct links to the interactive "
        "Swagger UI reference."
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    # Group by domain
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
                f"| [:material-arrow-right: Open]({svc_name}.md){{ .md-button }} |"
            )

        lines.append("")

    return "\n".join(lines)


# ============================================================
# Main
# ============================================================

def main():
    print("Generating NovaTrek Microservice Pages...")
    print(f"  Specs:  {SPECS_DIR}")
    print(f"  Output: {OUTPUT_DIR}")
    print()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_services = []   # (svc_name, title, endpoint_count, version, domain)

    spec_files = sorted(f for f in os.listdir(SPECS_DIR) if f.endswith(".yaml"))

    for spec_file in spec_files:
        svc_name = spec_file.replace(".yaml", "")
        spec_path = os.path.join(SPECS_DIR, spec_file)

        with open(spec_path) as f:
            spec = yaml.safe_load(f)

        endpoints = extract_endpoints(spec)
        title = spec.get("info", {}).get("title", svc_name)
        version = spec.get("info", {}).get("version", "0.0.0")
        domain, _ = get_domain_info(svc_name)

        print(f"  {svc_name}: {len(endpoints)} endpoints")

        page = generate_service_page(svc_name, spec)
        with open(os.path.join(OUTPUT_DIR, f"{svc_name}.md"), "w") as f:
            f.write(page)

        all_services.append((svc_name, title, len(endpoints), version, domain))

    # Index page
    index_page = generate_index_page(all_services)
    with open(os.path.join(OUTPUT_DIR, "index.md"), "w") as f:
        f.write(index_page)

    total_ep = sum(s[2] for s in all_services)
    print()
    print(f"  Generated {len(all_services)} service pages with {total_ep} endpoint diagrams")
    print(f"  Index: {os.path.join(OUTPUT_DIR, 'index.md')}")
    print("  Done!")


if __name__ == "__main__":
    main()
