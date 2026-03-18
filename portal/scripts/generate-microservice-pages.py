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
import shutil
import subprocess
import unicodedata
import yaml
from urllib.parse import quote

# Paths
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPECS_DIR = os.path.join(WORKSPACE_ROOT, "architecture", "specs")
OUTPUT_DIR = os.path.join(WORKSPACE_ROOT, "portal", "docs", "microservices")
PUML_DIR = os.path.join(OUTPUT_DIR, "puml")
SVG_DIR = os.path.join(OUTPUT_DIR, "svg")
OVERRIDE_DIR = os.path.join(WORKSPACE_ROOT, "architecture", "diagrams", "endpoints")

# -- Metadata loaded from YAML files (architecture/metadata/) --
# Architects edit YAML, commit, push -- CI rebuilds automatically.
# No need to edit this Python file for metadata changes.
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from load_metadata import (  # noqa: E402
    DOMAINS, ALL_SERVICES, LABEL_TO_SVC,
    PCI_SERVICES, PCI_EXTERNALS, PCI_DATA_FLOWS, is_pci_flow,
    DATA_STORES, CROSS_SERVICE_CALLS,
    EVENT_CATALOG, EVENTS_BY_PRODUCER, EVENTS_BY_CONSUMER,
    APP_CONSUMERS, APP_TITLES, ACTORS, ACTOR_SERVICE_USAGE,
    SOLUTIONS_BY_SERVICE,
    DELIVERY_STATUS, DELIVERY_WAVES,
    PIPELINE_REPO_URL, PIPELINE_AZURE, PIPELINE_PORTAL_LINKS,
    PIPELINE_PER_SERVICE, PIPELINE_GLOBAL,
    get_service_light_color,
)

# ── Infrastructure Colors (fixed, not domain-dependent) ──
COLOR_DATABASE   = "#FEF9C3"   # yellow-100 — data at rest
COLOR_CACHE      = "#FECDD3"   # rose-200  — hot/fast data
COLOR_EVENT_BUS  = "#F5F3FF"   # violet-50 — async events
COLOR_GATEWAY    = "#E0F2FE"   # sky-100   — API entry point
COLOR_EXTERNAL   = "#F3F4F6"   # gray-100  — outside boundary
COLOR_PCI        = "#FEE2E2"   # red-100   — PCI compliance

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

    # Layout hints — arrange peer services in columns to prevent horizontal sprawl
    all_peers = []
    for peer in sorted(inbound_svcs.keys()):
        all_peers.append(_safe_alias(peer))
    for peer in sorted(outbound_svcs.keys()):
        if peer not in inbound_svcs:
            all_peers.append(_safe_alias(peer))
    if len(all_peers) > 4:
        L.append("")
        L.append("' Layout hints: stack peers in columns")
        col_size = max(2, (len(all_peers) + 2) // 3)  # ~3 columns
        for i in range(len(all_peers) - col_size):
            L.append(f'Lay_D({all_peers[i]}, {all_peers[i + col_size]})')

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
# ERD (Entity Relationship Diagram) Generation
# ============================================================

def _parse_fk(constraints_str):
    """Extract FK target table from a constraints string like 'NOT NULL, FK -> check_ins'."""
    if "FK ->" in constraints_str:
        parts = constraints_str.split("FK ->")
        target = parts[-1].strip()
        return target
    return None


def build_erd_puml(svc_name, ds):
    """Generate a PlantUML ERD from data-stores metadata."""
    table_details = ds.get("table_details", {})
    if not table_details:
        return None

    engine = ds.get("engine", "PostgreSQL")
    schema = ds.get("schema", svc_name)
    is_document = "couchbase" in engine.lower()

    L = []
    L.append("@startuml")
    L.append("!theme plain")
    L.append("skinparam linetype ortho")
    L.append("skinparam roundcorner 8")
    L.append("skinparam defaultFontName Inter, Helvetica, Arial, sans-serif")
    L.append("skinparam defaultFontSize 12")
    L.append("skinparam titleFontSize 16")
    L.append("skinparam titleFontStyle bold")
    L.append("")
    L.append("skinparam class {")
    L.append("  BackgroundColor #FAFBFC")
    L.append("  BorderColor #D1D5DB")
    L.append("  HeaderBackgroundColor #E5E7EB")
    L.append("  FontColor #1F2937")
    L.append("  AttributeFontSize 11")
    L.append("}")
    L.append("")

    label = "collections" if is_document else "tables"
    L.append(f'title {svc_name} ERD\\n<size:12>{engine} -- schema: {schema} ({len(table_details)} {label})</size>')
    L.append("")

    # Track FK relationships: (from_table, to_table, from_col)
    fk_relations = []

    for tbl_name, tbl_info in table_details.items():
        columns = tbl_info.get("columns", [])
        alias = re.sub(r'[^a-zA-Z0-9]', '_', tbl_name)

        L.append(f'entity "{tbl_name}" as {alias} {{')

        # Separate PK columns from others
        for col in columns:
            col_name = col[0] if isinstance(col, (list, tuple)) else col.get("name", "")
            col_type = col[1] if isinstance(col, (list, tuple)) else col.get("type", "")
            col_constraints = ""
            if isinstance(col, (list, tuple)):
                col_constraints = (col[2] if len(col) > 2 else "") or ""
            else:
                col_constraints = col.get("constraints", "") or ""

            is_pk = "PK" in col_constraints
            fk_target = _parse_fk(col_constraints)

            if fk_target:
                fk_relations.append((tbl_name, fk_target, col_name))

            # Build constraint annotation
            annot_parts = []
            if is_pk:
                annot_parts.append("PK")
            if fk_target:
                annot_parts.append("FK")
            if "NOT NULL" in col_constraints and not is_pk:
                annot_parts.append("NN")
            if "UNIQUE" in col_constraints and not is_pk:
                annot_parts.append("UQ")

            annot = " ".join(annot_parts)
            marker = "* " if is_pk else "  "
            annot_str = f" <<{annot}>>" if annot else ""

            if is_pk:
                L.append(f"  {marker}{col_name} : {col_type}{annot_str}")
            else:
                L.append(f"  {marker}{col_name} : {col_type}{annot_str}")

        L.append("}")
        L.append("")

    # Render FK relationships
    for from_tbl, to_tbl, col_name in fk_relations:
        from_alias = re.sub(r'[^a-zA-Z0-9]', '_', from_tbl)
        to_alias = re.sub(r'[^a-zA-Z0-9]', '_', to_tbl)
        # Only draw if target table exists in this service's schema
        if to_tbl in table_details:
            L.append(f'{from_alias} }}|--|| {to_alias} : {col_name}')

    L.append("")
    L.append("@enduml")
    return "\n".join(L)


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

    # Skinparam — neutral defaults; per-participant colors set inline
    L.append("skinparam backgroundColor #FEFEFE")
    L.append("skinparam shadowing false")
    L.append('skinparam defaultFontName "Segoe UI"')
    L.append("skinparam sequence {")
    L.append(f"    ArrowColor {method_color}")
    L.append("    ParticipantBorderColor #374151")
    L.append("    ParticipantBackgroundColor #F9FAFB")
    L.append("    LifeLineBorderColor #6B7280")
    L.append("    BoxBorderColor #94A3B8")
    L.append("    BoxBackgroundColor #F8FAFC")
    L.append("    NoteBorderColor #64748B")
    L.append("    NoteBackgroundColor #F8FAFC")
    L.append("}")
    L.append("")

    # Parent breadcrumb
    L.append(f'header [[/microservices/{svc_name}/#integration-context \u2B06 {svc_name} Integration Context]]')
    L.append("")

    # Title
    title_text = f"{method} {path}"
    L.append(f"title {title_text}\\n{summary}")
    L.append("")

    # Participants - clickable, colored by domain
    L.append(f'participant "Client" as Client [[/applications/]]')
    L.append(f'participant "API Gateway" as GW [[/actors/#api-gateway]] {COLOR_GATEWAY}')
    svc_bg = COLOR_PCI if svc_name in PCI_SERVICES else get_service_light_color(svc_name)
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
            color = COLOR_PCI if target_svc in PCI_SERVICES else get_service_light_color(target_svc)
            L.append(f'participant "{label}" as {alias} [[/microservices/{target_svc}/]] {color}')
        elif label == "Event Bus":
            L.append(f'queue "Kafka" as {alias} [[/actors/#event-bus]] {COLOR_EVENT_BUS}')
        elif label in PCI_EXTERNALS:
            actor_link = actor_anchor(label)
            L.append(f'participant "{label}" as {alias} [[/actors/#{actor_link}]] {COLOR_PCI}')
        else:
            actor_link = actor_anchor(label)
            if label in ACTORS:
                L.append(f'participant "{label}" as {alias} [[/actors/#{actor_link}]] {COLOR_EXTERNAL}')
            else:
                L.append(f'participant "{label}" as {alias} {COLOR_EXTERNAL}')

    L.append(f'database "{db_label}" as DB [[/microservices/{svc_name}/#data-store]] {COLOR_DATABASE}')
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
            act_color = get_service_light_color(target_svc) if target_svc else COLOR_EXTERNAL
            L.append(f"activate {alias} {act_color}")
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
            L.append(f"activate DB {COLOR_DATABASE}")
            L.append(f"DB --> Svc : {_r['one']}")
            L.append("deactivate DB")
            L.append("note right of DB : Returns 404 if not found")
        elif is_sub_resource(path):
            L.append(f"Svc -> DB : {_q['by_parent']}")
            L.append(f"activate DB {COLOR_DATABASE}")
            L.append(f"DB --> Svc : {_r['set']}")
            L.append("deactivate DB")
        else:
            L.append(f"Svc -> DB : {_q['filter']}")
            L.append(f"activate DB {COLOR_DATABASE}")
            L.append(f"DB --> Svc : {_r['page']}")
            L.append("deactivate DB")

    elif method == "POST":
        if is_sub_resource(path):
            L.append(f"Svc -> DB : {_q['chk_par']}")
            L.append(f"activate DB {COLOR_DATABASE}")
            L.append(f"DB --> Svc : {_r['parent']}")
            L.append("deactivate DB")
            L.append("note right of DB : 404 if parent not found")
            L.append("")
        L.append(f"Svc -> DB : {_q['insert']}")
        L.append(f"activate DB {COLOR_DATABASE}")
        L.append(f"DB --> Svc : {_r['created']}")
        L.append("deactivate DB")

    elif method in ("PUT", "PATCH"):
        L.append(f"Svc -> DB : {_q['lock']}")
        L.append(f"activate DB {COLOR_DATABASE}")
        L.append(f"DB --> Svc : {_r['current']}")
        L.append("deactivate DB")
        note = _merge_note if method == "PATCH" else _replace_note
        L.append(f"note right of Svc : {note}")
        L.append("")
        L.append(f"Svc -> DB : {_q['update']}")
        L.append(f"activate DB {COLOR_DATABASE}")
        L.append(f"DB --> Svc : {_r['updated']}")
        L.append("deactivate DB")

    elif method == "DELETE":
        L.append(f"Svc -> DB : {_q['by_id']}")
        L.append(f"activate DB {COLOR_DATABASE}")
        L.append(f"DB --> Svc : {_r['one']}")
        L.append("deactivate DB")
        L.append("note right of DB : Returns 404 if not found")
        L.append("")
        L.append(f"Svc -> DB : {_q['delete']}")
        L.append(f"activate DB {COLOR_DATABASE}")
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

    # -- Deployment & Operations buttons --
    delivery = DELIVERY_STATUS.get(svc_name, {})
    delivery_url = delivery.get("url")
    if delivery_url:
        lines.append(
            f"[:material-rocket-launch: Live Service (Dev)]({delivery_url}/actuator/health)"
            "{ .md-button }"
        )

    sub_id = PIPELINE_AZURE.get("subscription_id", "")
    rg = PIPELINE_AZURE.get("resource_groups", {}).get("dev", "")
    ca_pattern = PIPELINE_AZURE.get("container_app_pattern", "ca-{service-name}")
    ca_name = ca_pattern.replace("{service-name}", svc_name)
    if sub_id and rg and delivery_url:
        ca_link = PIPELINE_PORTAL_LINKS.get("container_app", "").format(
            subscription_id=sub_id, rg=rg, name=ca_name,
        )
        lines.append(
            f"[:material-microsoft-azure: Azure Portal]({ca_link})"
            "{ .md-button }"
        )

    if PIPELINE_REPO_URL:
        ci_pattern = PIPELINE_PER_SERVICE.get("ci-workflow-pattern", "")
        ci_workflow = ci_pattern.replace("{service-name}", svc_name)
        actions_url = f"{PIPELINE_REPO_URL}/actions/workflows/{ci_workflow}"
        lines.append(
            f"[:material-pipe: CI/CD Pipeline]({actions_url})"
            "{ .md-button }"
        )

        source_pattern = PIPELINE_PER_SERVICE.get("source-path-pattern", "")
        source_path = source_pattern.replace("{service-name}", svc_name)
        source_url = f"{PIPELINE_REPO_URL}/tree/main/{source_path}"
        lines.append(
            f"[:material-source-branch: Source Code]({source_url})"
            "{ .md-button }"
        )

    lines.append(
        "[:material-language-java: Technology Stack](../technologies.md)"
        "{ .md-button }"
    )

    lines.append("")

    # -- Delivery Status section --
    if delivery:
        stages = delivery.get("stages", {})
        wave_num = delivery.get("wave")
        wave_info = DELIVERY_WAVES.get(wave_num, {})
        wave_name = wave_info.get("name", f"Wave {wave_num}")

        lines.append("## :material-truck-delivery: Delivery Status")
        lines.append("")
        lines.append(f"**Delivery Wave:** {wave_num} -- {wave_name}")
        lines.append("")

        # Stage progress table — split into deployment and pipeline sections
        deploy_method = stages.get("deploy-method", "manual")
        lines.append("| Stage | Status |")
        lines.append("|-------|--------|")

        deploy_stage_labels = {
            "bicep-module": "Infrastructure (Bicep)",
            "db-schema": "Database Schema (Flyway)",
            "deployed-dev": "Deployed to Dev",
            "smoke-tested": "Smoke Tested",
            "deployed-prod": "Deployed to Prod",
        }
        for stage_key, stage_label in deploy_stage_labels.items():
            status = stages.get(stage_key, "not-started")
            if status == "complete":
                icon = ":white_check_mark:"
            elif status == "in-progress":
                icon = ":construction:"
            else:
                icon = ":material-circle-outline:"
            lines.append(f"| {stage_label} | {icon} {status} |")
        lines.append("")

        # Pipeline maturity
        ci_status = stages.get("ci-pipeline", "not-started")
        cd_status = stages.get("cd-pipeline", "not-started")
        if ci_status != "complete" or cd_status != "complete":
            if deploy_method == "manual":
                lines.append(
                    "!!! info \"Deployment Method\"\n"
                    "    This service was deployed manually via Azure CLI. "
                    "Automated CI/CD pipelines are not yet configured."
                )
            else:
                lines.append("| CI Pipeline | {} {} |".format(
                    ":white_check_mark:" if ci_status == "complete" else ":material-circle-outline:",
                    ci_status))
                lines.append("| CD Pipeline | {} {} |".format(
                    ":white_check_mark:" if cd_status == "complete" else ":material-circle-outline:",
                    cd_status))
        else:
            lines.append("")
            lines.append("| Pipeline | Status |")
            lines.append("|----------|--------|")
            lines.append(f"| CI Pipeline | :white_check_mark: complete |")
            lines.append(f"| CD Pipeline | :white_check_mark: complete |")
        lines.append("")

        # Azure resource links
        if sub_id and rg:
            lines.append("**Azure Resources (Dev):**")
            lines.append("")
            if delivery_url:
                lines.append(
                    f"- [:material-microsoft-azure: Container App]"
                    f"({PIPELINE_PORTAL_LINKS.get('container_app', '').format(subscription_id=sub_id, rg=rg, name=ca_name)})"
                )
            pg_name = PIPELINE_AZURE.get("postgresql", {}).get("dev", "")
            if pg_name:
                lines.append(
                    f"- [:material-database: PostgreSQL Server]"
                    f"({PIPELINE_PORTAL_LINKS.get('postgresql', '').format(subscription_id=sub_id, rg=rg, name=pg_name)})"
                )
            log_name = PIPELINE_AZURE.get("log_analytics", {}).get("dev", "")
            if log_name:
                lines.append(
                    f"- [:material-text-search: Log Analytics]"
                    f"({PIPELINE_PORTAL_LINKS.get('log_analytics', '').format(subscription_id=sub_id, rg=rg, name=log_name)})"
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
    lines.append("## :material-database: Data Store { #data-store }")
    lines.append("")

    # ERD diagram
    erd_svg = f"{svc_name}--erd.svg"
    if erd_svg in svg_files:
        lines.append("### Entity Relationship Diagram")
        lines.append("")
        lines.append(
            f'<div class="diagram-wrap">'
            f'<a href="../svg/{erd_svg}" target="_blank" class="diagram-expand" title="Open in new tab">\u2922</a>'
            f'<object data="../svg/{erd_svg}" type="image/svg+xml" '
            f'style="max-width: 100%;">{svc_name} entity relationship diagram</object></div>'
        )
        lines.append("")

    if ds:
        lines.append("### Overview")
        lines.append("")
        tables_fmt = ", ".join(f"`{t}`" for t in ds.get("tables", []))
        lines.append("| Property | Detail |")
        lines.append("|----------|--------|")
        lines.append(f"| **Engine** | {ds.get('engine', 'N/A')} |")
        lines.append(f"| **Schema** | `{ds.get('schema', 'N/A')}` |")
        lines.append(f"| **Tables** | {tables_fmt} |")
        lines.append(f"| **Estimated Volume** | {ds.get('volume', 'N/A')} |")
        cp = ds.get("connection_pool")
        if cp:
            lines.append(f"| **Connection Pool** | min {cp['min']} / max {cp['max']} / idle timeout {cp['idle_timeout']} |")
        backup = ds.get("backup")
        if backup:
            lines.append(f"| **Backup Strategy** | {backup} |")
        lines.append("")

        # Key features
        features = ds.get("features", [])
        if features:
            lines.append("### Key Features")
            lines.append("")
            for feat in features:
                lines.append(f"- {feat}")
            lines.append("")

        # Table details
        table_details = ds.get("table_details", {})
        if table_details:
            lines.append("### Table Reference")
            lines.append("")
            for tbl_name, tbl_info in table_details.items():
                tbl_desc = tbl_info.get("description", "")
                lines.append(f"#### `{tbl_name}`")
                lines.append("")
                if tbl_desc:
                    lines.append(f"*{tbl_desc}*")
                    lines.append("")
                columns = tbl_info.get("columns", [])
                if columns:
                    lines.append("| Column | Type | Constraints |")
                    lines.append("|--------|------|-------------|")
                    for col in columns:
                        col_name, col_type, col_constraints = col[0], col[1], col[2] if len(col) > 2 else ""
                        lines.append(f"| `{col_name}` | `{col_type}` | {col_constraints} |")
                    lines.append("")
                indexes = tbl_info.get("indexes", [])
                if indexes:
                    lines.append("**Indexes:**")
                    lines.append("")
                    for idx in indexes:
                        idx_name = idx[0]
                        idx_cols = idx[1]
                        idx_note = idx[2] if len(idx) > 2 else ""
                        note_str = f" ({idx_note})" if idx_note else ""
                        lines.append(f"- `{idx_name}` on `{idx_cols}`{note_str}")
                    lines.append("")
    else:
        lines.append("*Data store information not yet documented.*")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Solutions Affecting This Service
    solutions = SOLUTIONS_BY_SERVICE.get(svc_name, [])
    if solutions:
        lines.append("## :material-lightbulb: Solutions Affecting This Service")
        lines.append("")
        lines.append("| Ticket | Solution | Capabilities | Date |")
        lines.append("|--------|----------|-------------|------|")
        for sol in solutions:
            ticket = sol["ticket"]
            folder = sol["folder"]
            summary = sol["summary"]
            caps = ", ".join(f"`{c}`" for c in sol["capabilities"]) if sol["capabilities"] else "--"
            date = sol["date"] or "--"
            lines.append(
                f"| {ticket} "
                f"| [{summary}](../solutions/{folder}.md) "
                f"| {caps} "
                f"| {date} |"
            )
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
    lines.append(
        "All services are built on the same "
        "[technology stack](../technologies.md) — Java 21, Spring Boot 3.3.5, "
        "PostgreSQL 15, deployed to Azure Container Apps."
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
        lines.append("| Service | Version | Endpoints | Status | Page |")
        lines.append("|---------|---------|-----------|--------|------|")

        for svc_name, title, ep_count, version in sorted(svcs):
            delivery = DELIVERY_STATUS.get(svc_name, {})
            dev_deployed = delivery.get("stages", {}).get("deployed-dev", "not-started")
            if dev_deployed == "complete":
                status_badge = ":white_check_mark: Deployed"
            elif dev_deployed == "in-progress":
                status_badge = ":construction: In Progress"
            else:
                wave_num = delivery.get("wave", "?")
                status_badge = f":material-circle-outline: Wave {wave_num}"
            lines.append(
                f"| **{title}**<br><small>`{svc_name}`</small> "
                f"| `{version}` "
                f"| {ep_count} endpoints "
                f"| {status_badge} "
                f"| [:material-arrow-right: Open]({svc_name}.md)" + "{ .md-button } |"
            )

        lines.append("")

    return "\n".join(lines)


# ============================================================
# Event Catalog Page Generation
# ============================================================

EVENTS_DIR = os.path.join(WORKSPACE_ROOT, "architecture", "events")
EVENTS_OUTPUT_DIR = os.path.join(WORKSPACE_ROOT, "portal", "docs", "events")


def build_event_flow_puml():
    """Generate a PlantUML diagram showing all event producers, Kafka, and consumers."""
    L = []
    L.append("@startuml")
    L.append("!theme plain")
    L.append("top to bottom direction")
    L.append("skinparam backgroundColor #FAFAFA")
    L.append("skinparam defaultFontName Inter")
    L.append("skinparam defaultFontSize 12")
    L.append("skinparam roundCorner 8")
    L.append("skinparam componentStyle rectangle")
    L.append("skinparam rectangleBorderColor transparent")
    L.append("skinparam rectangleBackgroundColor transparent")
    L.append("title NovaTrek Event Flow")
    L.append("")

    # Collect unique producers and consumers
    producers = set()
    consumers = set()
    for evt_name, evt in EVENT_CATALOG.items():
        producers.add(evt["producer"])
        for c in evt["consumers"]:
            consumers.add(c)

    sorted_producers = sorted(producers)
    sorted_consumers = sorted(consumers)
    cols = 4

    def _emit_grid(items, prefix, group_label):
        """Emit components in nested row containers for grid layout."""
        L.append(f'package "{group_label}" {{')
        rows = [items[i:i + cols] for i in range(0, len(items), cols)]
        for row_idx, row in enumerate(rows):
            L.append(f'  rectangle "row{row_idx}" as {prefix}row{row_idx} {{')
            for svc in row:
                _, color = get_domain_info(svc)
                alias = prefix + svc.replace("-", "_")
                L.append(f'    component "{svc}" as {alias} [[/microservices/{svc}/]] {color}')
            L.append("  }")
        L.append("}")
        L.append("")

    _emit_grid(sorted_producers, "p_", "Producers")

    # Kafka in the middle
    L.append('queue "Kafka Event Bus" as kafka #F0E6FF')
    L.append("")

    _emit_grid(sorted_consumers, "c_", "Consumers")

    # Draw arrows from producers to Kafka (down)
    for evt_name, evt in sorted(EVENT_CATALOG.items()):
        p_alias = "p_" + evt["producer"].replace("-", "_")
        L.append(f'{p_alias} --> kafka : {evt_name}')

    L.append("")

    # Draw arrows from Kafka to consumers (down)
    drawn = set()
    for evt_name, evt in sorted(EVENT_CATALOG.items()):
        for c in evt["consumers"]:
            c_alias = "c_" + c.replace("-", "_")
            key = (evt_name, c_alias)
            if key not in drawn:
                drawn.add(key)
                L.append(f'kafka --> {c_alias} : {evt_name}')

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
    events_dir = os.path.join(WORKSPACE_ROOT, "architecture", "events")
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
    override_count = 0

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
            override_path = os.path.join(OVERRIDE_DIR, f"{fname}.puml")
            puml_path = os.path.join(PUML_DIR, f"{fname}.puml")
            if os.path.isfile(override_path):
                # Architect-crafted override takes precedence
                shutil.copy2(override_path, puml_path)
                override_count += 1
            else:
                with open(puml_path, "w") as f:
                    f.write(puml_content)
            all_pumls.append(puml_path)

        all_services.append((svc_name, title, len(endpoints), version, domain))

    # Generate ERD diagrams for each service
    erd_count = 0
    for svc_name, _, _, _, _ in all_services:
        ds = DATA_STORES.get(svc_name, {})
        erd_puml = build_erd_puml(svc_name, ds)
        if erd_puml:
            erd_path = os.path.join(PUML_DIR, f"{svc_name}--erd.puml")
            with open(erd_path, "w") as f:
                f.write(erd_puml)
            all_pumls.append(erd_path)
            erd_count += 1

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
    override_msg = f" ({override_count} architect overrides)" if override_count else ""
    print(f"\n  Generated {len(all_pumls)} PUML files ({total_ep} endpoint + {erd_count} ERD + {len(all_services)} C4 context + 1 enterprise + 1 event flow){override_msg}")

    # Copy theme.puml so architect overrides can resolve !include ../theme.puml
    theme_src = os.path.join(WORKSPACE_ROOT, "architecture", "diagrams", "theme.puml")
    if os.path.isfile(theme_src):
        shutil.copy2(theme_src, os.path.join(OUTPUT_DIR, "theme.puml"))

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
    os.makedirs(EVENTS_OUTPUT_DIR, exist_ok=True)
    event_catalog_page = generate_event_catalog_page()
    event_catalog_path = os.path.join(EVENTS_OUTPUT_DIR, "index.md")
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
    print(f"  Events: {EVENTS_OUTPUT_DIR}/")
    print(f"  Actors: {ACTORS_DIR}/")


if __name__ == "__main__":
    main()
