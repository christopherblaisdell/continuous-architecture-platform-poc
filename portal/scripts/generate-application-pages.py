#!/usr/bin/env python3
"""Generate Application Pages for the NovaTrek Architecture Portal.

Creates a deep-dive page for each frontend application with:
  - Application metadata (tech stack, team, type)
  - Screen inventory with API dependency tables
  - PlantUML user journey sequence diagrams (rendered as clickable SVGs)
  - Bidirectional links to microservice endpoint pages

Also generates an Application Gallery index page.

Usage:
    python3 portal/scripts/generate-application-pages.py
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
OUTPUT_DIR = os.path.join(WORKSPACE_ROOT, "portal", "docs", "applications")
PUML_DIR = os.path.join(OUTPUT_DIR, "puml")
SVG_DIR = os.path.join(OUTPUT_DIR, "svg")

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


# ============================================================
# Application Definitions
# ============================================================

# Each screen has:
#   "description": short text
#   "steps": ordered list of (alias, label, svc_name_or_None, action, method, path_or_None, is_async)
#       - alias: short PlantUML participant alias
#       - label: display label in diagram
#       - svc_name_or_None: microservice name for linking (None = external)
#       - action: arrow label text
#       - method: HTTP method (for deep-link anchor lookup)
#       - path_or_None: API path (for deep-link anchor lookup, None = external)
#       - is_async: True for dashed async arrows

APPLICATIONS = {
    "web-guest-portal": {
        "title": "NovaTrek Guest Portal",
        "type": "Web",
        "type_icon": ":material-web:",
        "tech": "React 18, TypeScript, Vite, Tailwind CSS",
        "team": "Guest Experience Team",
        "color": "#2563eb",
        "description": "Public-facing website where guests browse adventures, make reservations, manage their profiles, and track loyalty rewards.",
        "client_label": "Browser",
        "client_icon": "browser",
        "screens": {
            "Trip Browser": {
                "description": "Search and explore available adventures with trail info, weather forecasts, and photo galleries.",
                "steps": [
                    ("TC", "svc-trip-catalog", "svc-trip-catalog", "Search available trips", "GET", "/trips", False),
                    ("TC", "svc-trip-catalog", "svc-trip-catalog", "Get trip details", "GET", "/trips/{trip_id}", False),
                    ("TM", "svc-trail-management", "svc-trail-management", "Get trail conditions", "GET", "/trails/{trail_id}/conditions", False),
                    ("WX", "svc-weather", "svc-weather", "Get weather forecast", "GET", "/weather/forecast", False),
                    ("MG", "svc-media-gallery", "svc-media-gallery", "Load trip photos", "GET", "/media", False),
                ],
            },
            "Booking Flow": {
                "description": "End-to-end reservation flow from trip selection through payment confirmation.",
                "steps": [
                    ("TC", "svc-trip-catalog", "svc-trip-catalog", "Check trip availability", "GET", "/trips/{trip_id}", False),
                    ("GP", "svc-guest-profiles", "svc-guest-profiles", "Get guest profile", "GET", "/guests/{guest_id}", False),
                    ("Res", "svc-reservations", "svc-reservations", "Create reservation", "POST", "/reservations", False),
                    ("Pay", "svc-payments", "svc-payments", "Process payment", "POST", "/payments", False),
                    ("Stripe", "Stripe API", None, "Charge card", None, None, False),
                ],
            },
            "Guest Profile": {
                "description": "View and edit guest profile, certifications, past adventures, and loyalty tier.",
                "steps": [
                    ("GP", "svc-guest-profiles", "svc-guest-profiles", "Get guest profile", "GET", "/guests/{guest_id}", False),
                    ("GP", "svc-guest-profiles", "svc-guest-profiles", "Get adventure history", "GET", "/guests/{guest_id}/adventure-history", False),
                    ("LR", "svc-loyalty-rewards", "svc-loyalty-rewards", "Get loyalty balance", "GET", "/members/{guest_id}/balance", False),
                    ("Res", "svc-reservations", "svc-reservations", "Get upcoming bookings", "GET", "/reservations", False),
                ],
            },
            "Reservation Management": {
                "description": "View, modify, or cancel existing reservations and process refunds.",
                "steps": [
                    ("Res", "svc-reservations", "svc-reservations", "List reservations", "GET", "/reservations", False),
                    ("Res", "svc-reservations", "svc-reservations", "Get reservation details", "GET", "/reservations/{reservation_id}", False),
                    ("Res", "svc-reservations", "svc-reservations", "Update reservation status", "PUT", "/reservations/{reservation_id}/status", False),
                    ("Pay", "svc-payments", "svc-payments", "Process refund", "POST", "/payments/{payment_id}/refund", False),
                    ("Ntfy", "svc-notifications", "svc-notifications", "Send cancellation notice", "POST", "/notifications", True),
                ],
            },
            "Loyalty Dashboard": {
                "description": "View loyalty points balance, tier status, transaction history, and available rewards.",
                "steps": [
                    ("LR", "svc-loyalty-rewards", "svc-loyalty-rewards", "Get member balance", "GET", "/members/{guest_id}/balance", False),
                    ("LR", "svc-loyalty-rewards", "svc-loyalty-rewards", "Get transaction history", "GET", "/members/{guest_id}/transactions", False),
                    ("GP", "svc-guest-profiles", "svc-guest-profiles", "Get guest profile", "GET", "/guests/{guest_id}", False),
                ],
            },
            "Waiver Signing": {
                "description": "Review and digitally sign safety waivers before trip departure.",
                "steps": [
                    ("SC", "svc-safety-compliance", "svc-safety-compliance", "Get required waivers", "GET", "/waivers", False),
                    ("GP", "svc-guest-profiles", "svc-guest-profiles", "Get guest profile", "GET", "/guests/{guest_id}", False),
                    ("SC", "svc-safety-compliance", "svc-safety-compliance", "Submit signed waiver", "POST", "/waivers", False),
                    ("DS", "DocuSign API", None, "Verify digital signature", None, None, False),
                    ("Ntfy", "svc-notifications", "svc-notifications", "Send waiver copy", "POST", "/notifications", True),
                ],
            },
            "Trip Gallery": {
                "description": "Browse and share photos and videos from past adventures.",
                "steps": [
                    ("MG", "svc-media-gallery", "svc-media-gallery", "List trip media", "GET", "/media", False),
                    ("Res", "svc-reservations", "svc-reservations", "Get reservation details", "GET", "/reservations/{reservation_id}", False),
                    ("MG", "svc-media-gallery", "svc-media-gallery", "Create share link", "POST", "/media/{media_id}/share", False),
                    ("Ntfy", "svc-notifications", "svc-notifications", "Send share notification", "POST", "/notifications", True),
                ],
            },
        },
    },
    "web-ops-dashboard": {
        "title": "NovaTrek Operations Dashboard",
        "type": "Web",
        "type_icon": ":material-monitor-dashboard:",
        "tech": "Angular 17, TypeScript, PrimeNG, NgRx",
        "team": "NovaTrek Operations Team",
        "color": "#dc2626",
        "description": "Internal staff dashboard for managing daily operations including scheduling, check-ins, safety incidents, inventory, and analytics.",
        "client_label": "Browser",
        "client_icon": "browser",
        "screens": {
            "Daily Schedule Board": {
                "description": "View and manage the day's adventure schedule with guide assignments, weather conditions, and trail status.",
                "steps": [
                    ("SO", "svc-scheduling-orchestrator", "svc-scheduling-orchestrator", "Get daily schedules", "GET", "/schedule-optimization", False),
                    ("GM", "svc-guide-management", "svc-guide-management", "Get available guides", "GET", "/guides/available", False),
                    ("WX", "svc-weather", "svc-weather", "Get weather forecast", "GET", "/weather/forecast", False),
                    ("TM", "svc-trail-management", "svc-trail-management", "Get trail conditions", "GET", "/trails/{trail_id}/conditions", False),
                    ("LS", "svc-location-services", "svc-location-services", "Get location capacity", "GET", "/locations/{location_id}/capacity", False),
                ],
            },
            "Check-In Station": {
                "description": "Staff-assisted check-in workflow: verify reservation, validate identity, check waivers, assign gear, and issue wristband.",
                "steps": [
                    ("Res", "svc-reservations", "svc-reservations", "Lookup reservation", "GET", "/reservations/{reservation_id}", False),
                    ("GP", "svc-guest-profiles", "svc-guest-profiles", "Verify guest identity", "GET", "/guests/{guest_id}", False),
                    ("SC", "svc-safety-compliance", "svc-safety-compliance", "Check waiver status", "GET", "/waivers", False),
                    ("CI", "svc-check-in", "svc-check-in", "Create check-in", "POST", "/check-ins", False),
                    ("GI", "svc-gear-inventory", "svc-gear-inventory", "Assign gear package", "POST", "/gear-assignments", False),
                ],
            },
            "Guide Assignment": {
                "description": "Assign guides to scheduled adventures based on certification, availability, and guest preferences.",
                "steps": [
                    ("GM", "svc-guide-management", "svc-guide-management", "List certified guides", "GET", "/guides", False),
                    ("GM", "svc-guide-management", "svc-guide-management", "Check availability", "GET", "/guides/{guide_id}/availability", False),
                    ("SO", "svc-scheduling-orchestrator", "svc-scheduling-orchestrator", "Submit schedule request", "POST", "/schedule-requests", False),
                    ("TM", "svc-trail-management", "svc-trail-management", "Verify trail status", "GET", "/trails/{trail_id}", False),
                ],
            },
            "Safety Incident Board": {
                "description": "Log and manage safety incidents with guest contact, guide notification, and regulatory reporting.",
                "steps": [
                    ("SC", "svc-safety-compliance", "svc-safety-compliance", "List active incidents", "GET", "/incidents/{incident_id}", False),
                    ("SC", "svc-safety-compliance", "svc-safety-compliance", "Log new incident", "POST", "/incidents", False),
                    ("GP", "svc-guest-profiles", "svc-guest-profiles", "Get guest contact info", "GET", "/guests/{guest_id}", False),
                    ("GM", "svc-guide-management", "svc-guide-management", "Get assigned guide", "GET", "/guides/{guide_id}", False),
                    ("Ntfy", "svc-notifications", "svc-notifications", "Send safety alerts", "POST", "/notifications", True),
                ],
            },
            "Inventory Management": {
                "description": "Track gear inventory levels, manage assignments, and create procurement orders.",
                "steps": [
                    ("GI", "svc-gear-inventory", "svc-gear-inventory", "Get inventory levels", "GET", "/gear-items", False),
                    ("GI", "svc-gear-inventory", "svc-gear-inventory", "Check gear assignments", "GET", "/gear-assignments/{assignment_id}", False),
                    ("IP", "svc-inventory-procurement", "svc-inventory-procurement", "Create purchase order", "POST", "/purchase-orders", False),
                ],
            },
            "Transport Dispatch": {
                "description": "Coordinate guest transport with route optimization, vehicle assignment, and real-time tracking.",
                "steps": [
                    ("TL", "svc-transport-logistics", "svc-transport-logistics", "List transport requests", "GET", "/transport-requests/{request_id}", False),
                    ("TL", "svc-transport-logistics", "svc-transport-logistics", "Create transport request", "POST", "/transport-requests", False),
                    ("LS", "svc-location-services", "svc-location-services", "Get pickup locations", "GET", "/locations/{location_id}", False),
                    ("Res", "svc-reservations", "svc-reservations", "Get booking details", "GET", "/reservations/{reservation_id}", False),
                    ("GM", "Google Maps Platform", None, "Calculate optimal route", None, None, False),
                ],
            },
            "Analytics Dashboard": {
                "description": "Business intelligence views for booking trends, revenue, utilization, and guest satisfaction.",
                "steps": [
                    ("AN", "svc-analytics", "svc-analytics", "Get booking metrics", "GET", "/analytics/bookings", False),
                    ("Res", "svc-reservations", "svc-reservations", "Get reservation stats", "GET", "/reservations", False),
                    ("Pay", "svc-payments", "svc-payments", "Get revenue summary", "GET", "/payments/daily-summary", False),
                    ("SF", "Snowflake Data Cloud", None, "Query data warehouse", None, None, False),
                ],
            },
            "Partner Bookings": {
                "description": "Manage partner-originated bookings, commission tracking, and reconciliation.",
                "steps": [
                    ("PI", "svc-partner-integrations", "svc-partner-integrations", "List partner bookings", "GET", "/partner-bookings/{booking_id}", False),
                    ("PI", "svc-partner-integrations", "svc-partner-integrations", "Confirm booking", "POST", "/partner-bookings/{booking_id}/confirm", False),
                    ("Res", "svc-reservations", "svc-reservations", "Get reservation details", "GET", "/reservations/{reservation_id}", False),
                    ("Pay", "svc-payments", "svc-payments", "Get payment status", "GET", "/payments/{payment_id}", False),
                ],
            },
        },
    },
    "app-guest-mobile": {
        "title": "NovaTrek Adventure App",
        "type": "Mobile",
        "type_icon": ":material-cellphone:",
        "tech": "React Native 0.74, TypeScript, Expo",
        "team": "Guest Experience Team",
        "color": "#059669",
        "description": "Native mobile app for on-trip guest experiences including self check-in, live maps, photo sharing, and real-time weather and trail alerts.",
        "client_label": "Mobile App",
        "client_icon": "mobile",
        "screens": {
            "Self Check-In": {
                "description": "Guest self-service check-in with QR code scan, identity verification, waiver confirmation, and wristband activation.",
                "steps": [
                    ("Res", "svc-reservations", "svc-reservations", "Lookup reservation by QR", "GET", "/reservations/{reservation_id}", False),
                    ("GP", "svc-guest-profiles", "svc-guest-profiles", "Verify guest identity", "GET", "/guests/{guest_id}", False),
                    ("SC", "svc-safety-compliance", "svc-safety-compliance", "Validate waiver status", "GET", "/waivers", False),
                    ("CI", "svc-check-in", "svc-check-in", "Create check-in record", "POST", "/check-ins", False),
                    ("GI", "svc-gear-inventory", "svc-gear-inventory", "Confirm gear assignment", "GET", "/gear-assignments/{assignment_id}", False),
                ],
            },
            "Live Trip Map": {
                "description": "Real-time interactive map showing current trail position, nearby waypoints, weather overlay, and group location.",
                "steps": [
                    ("LS", "svc-location-services", "svc-location-services", "Get nearby locations", "GET", "/locations", False),
                    ("TM", "svc-trail-management", "svc-trail-management", "Get trail waypoints", "GET", "/trails/{trail_id}", False),
                    ("TM", "svc-trail-management", "svc-trail-management", "Get trail conditions", "GET", "/trails/{trail_id}/conditions", False),
                    ("WX", "svc-weather", "svc-weather", "Get current weather", "GET", "/weather/current", False),
                    ("SO", "svc-scheduling-orchestrator", "svc-scheduling-orchestrator", "Get group schedule", "GET", "/schedule-requests/{request_id}", False),
                ],
            },
            "Photo Upload": {
                "description": "Capture and upload adventure photos with GPS metadata, auto-tagging, and instant sharing.",
                "steps": [
                    ("MG", "svc-media-gallery", "svc-media-gallery", "Upload photo", "POST", "/media", False),
                    ("S3", "Object Store", None, "Store binary file", None, None, False),
                    ("GM", "Google Maps Platform", None, "Reverse geocode GPS", None, None, False),
                    ("MG", "svc-media-gallery", "svc-media-gallery", "Create share link", "POST", "/media/{media_id}/share", False),
                    ("Ntfy", "svc-notifications", "svc-notifications", "Send share notification", "POST", "/notifications", True),
                ],
            },
            "My Reservations": {
                "description": "View upcoming and past reservations with trip details, payment history, and modification options.",
                "steps": [
                    ("Res", "svc-reservations", "svc-reservations", "List my reservations", "GET", "/reservations", False),
                    ("TC", "svc-trip-catalog", "svc-trip-catalog", "Get trip details", "GET", "/trips/{trip_id}", False),
                    ("Pay", "svc-payments", "svc-payments", "Get payment details", "GET", "/payments/{payment_id}", False),
                ],
            },
            "Weather and Trail Alerts": {
                "description": "Push-notification-driven alerts for severe weather, trail closures, and safety advisories.",
                "steps": [
                    ("WX", "svc-weather", "svc-weather", "Get weather alerts", "GET", "/weather/alerts", False),
                    ("TM", "svc-trail-management", "svc-trail-management", "Get trail closures", "GET", "/trails/{trail_id}/conditions", False),
                    ("ExtWx", "OpenWeather API", None, "Fetch severe alerts", None, None, False),
                    ("Ntfy", "svc-notifications", "svc-notifications", "Receive push notification", "POST", "/notifications", True),
                ],
            },
            "Digital Wristband": {
                "description": "Display NFC-enabled digital wristband for tap-to-verify at activity stations and equipment pickup.",
                "steps": [
                    ("CI", "svc-check-in", "svc-check-in", "Get check-in status", "GET", "/check-ins/{check_in_id}", False),
                    ("GI", "svc-gear-inventory", "svc-gear-inventory", "Verify gear assignment", "GET", "/gear-assignments/{assignment_id}", False),
                ],
            },
            "Earn Loyalty Points": {
                "description": "View point earnings after trip completion, tier progress, and available redemption offers.",
                "steps": [
                    ("LR", "svc-loyalty-rewards", "svc-loyalty-rewards", "Get member balance", "GET", "/members/{guest_id}/balance", False),
                    ("LR", "svc-loyalty-rewards", "svc-loyalty-rewards", "Earn points", "POST", "/members/{guest_id}/earn", False),
                    ("Res", "svc-reservations", "svc-reservations", "Get completed bookings", "GET", "/reservations", False),
                    ("GP", "svc-guest-profiles", "svc-guest-profiles", "Get guest profile", "GET", "/guests/{guest_id}", False),
                ],
            },
        },
    },
}


# ============================================================
# Reverse Index: svc_name -> [(app_name, screen_name), ...]
# ============================================================

def build_app_consumers():
    """Build reverse index from service name to consuming applications/screens."""
    consumers = {}
    for app_name, app in APPLICATIONS.items():
        for screen_name, screen in app["screens"].items():
            for step in screen["steps"]:
                svc = step[2]
                if svc:
                    consumers.setdefault(svc, []).append((app_name, screen_name))
    # Deduplicate
    for svc in consumers:
        consumers[svc] = sorted(set(consumers[svc]))
    return consumers


APP_CONSUMERS = build_app_consumers()


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


def make_puml_filename(app_name, screen_name):
    clean = screen_name.lower().replace(" ", "-").replace("&", "and")
    clean = re.sub(r'[^a-z0-9-]', '', clean)
    return f"{app_name}--{clean}"


def build_journey_puml(app_name, app_info, screen_name, screen):
    """Build a PlantUML user journey sequence diagram for one screen."""
    steps = screen["steps"]
    color = app_info["color"]
    client_label = app_info["client_label"]
    fname = make_puml_filename(app_name, screen_name)

    L = []
    L.append(f"@startuml {fname}")
    L.append("")

    # Skinparam
    L.append("skinparam backgroundColor #FEFEFE")
    L.append("skinparam shadowing false")
    L.append('skinparam defaultFontName "Segoe UI"')
    L.append("skinparam sequence {")
    L.append(f"    ArrowColor {color}")
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
    L.append(f'header [[/applications/{app_name}/#service-dependencies \u2B06 {app_info["title"]} Service Dependencies]]')
    L.append("")

    # Title
    L.append(f"title {screen_name}\\n{app_info['title']}")
    L.append("")

    # Participants
    L.append(f'actor "Guest" as User')
    L.append(f'participant "{client_label}" as App #DBEAFE')
    L.append('participant "API Gateway" as GW #DBEAFE')

    # Collect unique participants in order
    declared = set()
    for step in steps:
        alias, label, svc, action = step[0], step[1], step[2], step[3]
        if alias in declared:
            continue
        declared.add(alias)
        if svc:
            L.append(f'participant "{svc}" as {alias} [[/microservices/{svc}/]] #E8F4F8')
        else:
            L.append(f'participant "{label}" as {alias} #F5F5F5')

    L.append("")

    # User initiates
    L.append(f"User -> App : Open {screen_name}")
    L.append(f"activate App {color}")
    L.append("App -> GW : API request")
    L.append(f"activate GW {color}")
    L.append("")

    # API calls grouped
    L.append("== Backend Integration ==")
    L.append("")

    for step in steps:
        alias, label, svc = step[0], step[1], step[2]
        action, method, path = step[3], step[4], step[5]
        is_async = step[6]

        arrow = "->>" if is_async else "->"
        return_arrow = "-->>" if is_async else "-->"

        if svc and method and path:
            anchor = endpoint_anchor(svc, method, path)
            link_text = f"[[/microservices/{svc}/{anchor} {action}]]"
        elif svc:
            link_text = f"[[/microservices/{svc}/ {action}]]"
        else:
            link_text = action

        L.append(f"GW {arrow} {alias} : {link_text}")
        L.append(f"activate {alias} #DBEAFE")
        L.append(f"{alias} {return_arrow} GW : OK")
        L.append(f"deactivate {alias}")
        L.append("")

    # Response
    L.append("GW --> App : Response")
    L.append("deactivate GW")
    L.append("App --> User : Render screen")
    L.append("deactivate App")
    L.append("")
    L.append("@enduml")

    return "\n".join(L)


# ============================================================
# C4 Context Diagram Generation
# ============================================================

def _safe_alias(name):
    """Create a valid PlantUML alias from a name."""
    return re.sub(r'[^a-zA-Z0-9]', '_', name)


def build_c4_app_puml(app_name, app_info):
    """Build a C4 Container-level context diagram for a frontend application.

    Shows the application at the center with all microservices and
    external systems it connects to.
    """
    title = app_info["title"]
    color = app_info["color"]
    tech = app_info["tech"].split(",")[0]  # e.g. "React 18"
    app_type = app_info["type"]
    screens = app_info["screens"]

    # Collect all unique microservices and external systems
    all_svcs = {}       # svc_name -> set of screen names
    all_externals = {}  # label -> set of screen names

    for screen_name, screen in screens.items():
        for step in screen["steps"]:
            svc = step[2]
            label = step[1]
            if svc:
                all_svcs.setdefault(svc, set()).add(screen_name)
            else:
                all_externals.setdefault(label, set()).add(screen_name)

    L = []
    L.append("@startuml")
    L.append("!include <c4/C4_Container>")
    L.append("")
    L.append("LAYOUT_WITH_LEGEND()")
    L.append("LAYOUT_TOP_DOWN()")
    L.append("")
    L.append(f'header [[/applications/ \u2B06 All Applications]]')
    L.append("")
    L.append(f'title {app_name} — Service Dependencies')
    L.append("")

    # User
    L.append(f'Person(user, "Guest", "NovaTrek customer")')
    L.append("")

    # The application itself
    L.append(f'Container({_safe_alias(app_name)}, "{title}", "{tech}", "{app_type} application", $link="/applications/{app_name}/")')
    L.append("")

    # Backend services inside platform boundary
    L.append('System_Boundary(platform, "NovaTrek Platform") {')
    for svc in sorted(all_svcs.keys()):
        screen_count = len(all_svcs[svc])
        L.append(f'    Container({_safe_alias(svc)}, "{svc}", "Java / Spring Boot", "{screen_count} screens", $link="/microservices/{svc}/#integration-context")')
    L.append("}")
    L.append("")

    # External systems
    for ext in sorted(all_externals.keys()):
        L.append(f'System_Ext({_safe_alias(ext)}, "{ext}", "Third-party service")')
    L.append("")

    # Relationships
    app_alias = _safe_alias(app_name)
    L.append(f'Rel(user, {app_alias}, "Uses", "HTTPS")')
    for svc in sorted(all_svcs.keys()):
        screen_count = len(all_svcs[svc])
        label = f"{screen_count} screens" if screen_count > 1 else "1 screen"
        L.append(f'Rel({app_alias}, {_safe_alias(svc)}, "{label}", "REST/HTTPS")')

    for ext in sorted(all_externals.keys()):
        L.append(f'Rel({app_alias}, {_safe_alias(ext)}, "Uses", "HTTPS")')

    L.append("")
    L.append("@enduml")

    return "\n".join(L)


# ============================================================
# Page Generation
# ============================================================

def generate_app_page(app_name, app_info, svg_files):
    """Generate the deep-dive Markdown page for one application."""
    title = app_info["title"]
    app_type = app_info["type"]
    type_icon = app_info["type_icon"]
    tech = app_info["tech"]
    team = app_info["team"]
    color = app_info["color"]
    description = app_info["description"]
    screens = app_info["screens"]

    lines = []

    # Frontmatter
    lines.append("---")
    lines.append("tags:")
    lines.append("  - application")
    lines.append(f"  - {app_name}")
    lines.append(f"  - {app_type.lower()}")
    lines.append("---")
    lines.append("")

    # Header
    lines.append(f"# {app_name}")
    lines.append("")
    badge_style = (
        f"background: {color}15; color: {color}; "
        f"border: 1px solid {color}40; padding: 0.15rem 0.6rem; "
        f"border-radius: 1rem; font-size: 0.8rem; font-weight: 600;"
    )
    lines.append(
        f'**{title}** &nbsp;|&nbsp; '
        f'<span style="{badge_style}">{type_icon} {app_type}</span> '
        f'&nbsp;|&nbsp; *{team}*'
    )
    lines.append("")
    lines.append(f"> {description}")
    lines.append("")

    # Tech stack
    lines.append("## :material-language-typescript: Tech Stack")
    lines.append("")
    lines.append(f"**{tech}**")
    lines.append("")
    lines.append("---")
    lines.append("")

    # C4 Context Diagram
    c4_svg = f"{app_name}--c4-context.svg"
    if c4_svg in svg_files:
        lines.append("## :material-map: Service Dependencies")
        lines.append("")
        lines.append(
            f'<div style="overflow-x: auto; width: 100%;">'
            f'<object data="../svg/{c4_svg}" type="image/svg+xml" '
            f'style="max-width: 100%;">{app_name} C4 context diagram</object></div>'
        )
        lines.append("")
        lines.append(
            f'<p style="text-align: right; margin-top: -0.5em;">'
            f'<a href="../svg/{c4_svg}" target="_blank" title="Open diagram in full screen">'
            f':material-fullscreen: View full screen</a></p>'
        )
        lines.append("")
        lines.append("---")
        lines.append("")

    # Screen count summary
    total_services = set()
    for screen in screens.values():
        for step in screen["steps"]:
            if step[2]:
                total_services.add(step[2])

    lines.append(f"## {type_icon} Screens ({len(screens)} total)")
    lines.append("")
    lines.append(f"This application interacts with **{len(total_services)} microservices** across {len(screens)} screens.")
    lines.append("")

    # Screen summary table
    lines.append("| Screen | Services | Description |")
    lines.append("|--------|----------|-------------|")
    for screen_name, screen in screens.items():
        svcs = sorted(set(s[2] for s in screen["steps"] if s[2]))
        ext = sorted(set(s[1] for s in screen["steps"] if not s[2]))
        svc_list = ", ".join(f"`{s}`" for s in svcs)
        if ext:
            svc_list += " + " + ", ".join(ext)
        lines.append(f"| [{screen_name}](#{screen_name.lower().replace(' ', '-').replace('&', 'and')}) | {svc_list} | {screen['description'][:80]}... |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Each screen
    for screen_name, screen in screens.items():
        lines.append("---")
        lines.append("")
        lines.append(f"### {screen_name}")
        lines.append("")
        lines.append(f"> {screen['description']}")
        lines.append("")

        # API dependency table
        lines.append("**API Dependencies:**")
        lines.append("")
        lines.append("| Method | Endpoint | Service | Purpose |")
        lines.append("|--------|----------|---------|---------|")
        seen = set()
        for step in screen["steps"]:
            alias, label, svc, action, method, path, is_async = step
            if svc and method and path:
                key = (svc, method, path)
                if key in seen:
                    continue
                seen.add(key)
                anchor = endpoint_anchor(svc, method, path)
                if anchor:
                    link = f"[{method} `{path}`](../../microservices/{svc}/{anchor})"
                else:
                    link = f"[{method} `{path}`](../../microservices/{svc}/)"
                lines.append(f"| {method} | {link} | `{svc}` | {action} |")
            elif not svc:
                lines.append(f"| -- | *{label}* | External | {action} |")
        lines.append("")

        # SVG diagram
        svg_filename = make_puml_filename(app_name, screen_name) + ".svg"
        if svg_filename in svg_files:
            lines.append(
                f'<div style="overflow-x: auto; width: 100%;">'
                f'<object data="../svg/{svg_filename}" type="image/svg+xml" '
                f'style="max-width: 100%;">'
                f'{screen_name} user journey diagram</object>'
                f'</div>'
            )
            lines.append("")
            lines.append(
                f'<p style="text-align: right; margin-top: -0.5em;">'
                f'<a href="../svg/{svg_filename}" target="_blank" title="Open diagram in full screen">'
                f':material-fullscreen: View full screen</a></p>'
            )
        else:
            lines.append(f"*Diagram not available for {screen_name}*")
        lines.append("")

    return "\n".join(lines)


def generate_index_page():
    """Generate the Application Gallery index page."""
    total_screens = sum(len(a["screens"]) for a in APPLICATIONS.values())

    lines = []
    lines.append("---")
    lines.append("hide:")
    lines.append("  - toc")
    lines.append("tags:")
    lines.append("  - application")
    lines.append("---")
    lines.append("")
    lines.append('<div class="hero" markdown>')
    lines.append("")
    lines.append("# Applications")
    lines.append("")
    lines.append(
        '<p class="subtitle">'
        "Frontend Application Architecture for NovaTrek Adventures"
        "</p>"
    )
    lines.append("")
    lines.append(
        f'<span class="version-badge">'
        f"{len(APPLICATIONS)} Applications &middot; {total_screens} Screens"
        f"</span>"
    )
    lines.append("")
    lines.append("</div>")
    lines.append("")
    lines.append(
        "Each application page provides **user journey sequence diagrams** for every "
        "screen, showing the full API call flow from UI through API Gateway to backend "
        "microservices, with clickable links to service endpoints and Swagger UI."
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    # App cards
    lines.append("| Application | Type | Tech Stack | Screens | Page |")
    lines.append("|-------------|------|------------|---------|------|")

    for app_name, app in APPLICATIONS.items():
        screen_count = len(app["screens"])
        lines.append(
            f"| **{app['title']}**<br><small>`{app_name}`</small> "
            f"| {app['type_icon']} {app['type']} "
            f"| {app['tech'].split(',')[0]} "
            f"| {screen_count} screens "
            f"| [:material-arrow-right: Open]({app_name}.md)"
            "{ .md-button } |"
        )

    lines.append("")
    lines.append("---")
    lines.append("")

    # Service coverage matrix
    lines.append("## Service Coverage Matrix")
    lines.append("")
    lines.append("Which microservices are consumed by which applications:")
    lines.append("")

    all_svcs = sorted(APP_CONSUMERS.keys())
    app_names = list(APPLICATIONS.keys())

    lines.append("| Service | " + " | ".join(f"`{a}`" for a in app_names) + " |")
    lines.append("|---------|" + "|".join(["------" for _ in app_names]) + "|")

    for svc in all_svcs:
        row = f"| [`{svc}`](../../microservices/{svc}/) |"
        for app_name in app_names:
            screens = [s for a, s in APP_CONSUMERS[svc] if a == app_name]
            if screens:
                row += f" {len(screens)} screens |"
            else:
                row += " -- |"
        lines.append(row)

    lines.append("")
    return "\n".join(lines)


# ============================================================
# Main
# ============================================================

def main():
    print("Generating NovaTrek Application Pages (PlantUML SVGs)...")
    print(f"  Output: {OUTPUT_DIR}")
    print()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(PUML_DIR, exist_ok=True)
    os.makedirs(SVG_DIR, exist_ok=True)

    # Pre-load all endpoint summaries for deep linking
    spec_files = sorted(f for f in os.listdir(SPECS_DIR) if f.endswith(".yaml"))
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
    total_screens = 0

    for app_name, app_info in APPLICATIONS.items():
        screens = app_info["screens"]
        print(f"  {app_name}: {len(screens)} screens")
        total_screens += len(screens)

        for screen_name, screen in screens.items():
            puml_content = build_journey_puml(app_name, app_info, screen_name, screen)
            fname = make_puml_filename(app_name, screen_name)
            puml_path = os.path.join(PUML_DIR, f"{fname}.puml")
            with open(puml_path, "w") as f:
                f.write(puml_content)
            all_pumls.append(puml_path)

        # C4 context diagram for the application
        c4_puml = build_c4_app_puml(app_name, app_info)
        c4_path = os.path.join(PUML_DIR, f"{app_name}--c4-context.puml")
        with open(c4_path, "w") as f:
            f.write(c4_puml)
        all_pumls.append(c4_path)

    print(f"\n  Generated {len(all_pumls)} PUML files ({total_screens} screen + {len(APPLICATIONS)} C4 context)")

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
    for app_name, app_info in APPLICATIONS.items():
        page = generate_app_page(app_name, app_info, svg_files)
        with open(os.path.join(OUTPUT_DIR, f"{app_name}.md"), "w") as f:
            f.write(page)

    index_page = generate_index_page()
    with open(os.path.join(OUTPUT_DIR, "index.md"), "w") as f:
        f.write(index_page)

    print()
    print(f"  Done! {len(APPLICATIONS)} app pages, {total_screens} screen diagrams")
    print(f"  PUML: {PUML_DIR}/")
    print(f"  SVGs: {SVG_DIR}/")
    print(f"  Pages: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
