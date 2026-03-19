#!/usr/bin/env python3
"""Generate Domain detail pages for the NovaTrek Architecture Portal.

Reads architecture metadata YAML files to generate:
  - A domain overview index page (portal/docs/domains/index.md)
  - One detail page per domain (portal/docs/domains/{slug}.md)

Each domain page includes:
  - Team ownership
  - Services table with data store and API endpoint counts
  - Data ownership boundaries
  - Bounded context rules (domain-specific)
  - Cross-domain integration map (outbound + inbound)
  - Domain events (produced and consumed)
  - Related architecture decisions (ADRs)
  - Related business capabilities
  - Topology diagram link
  - Links to all microservice pages

Usage:
    python3 portal/scripts/generate-domain-pages.py
"""

import os
import re
import yaml

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
METADATA_DIR = os.path.join(WORKSPACE_ROOT, "architecture", "metadata")
SPECS_DIR = os.path.join(WORKSPACE_ROOT, "architecture", "specs")
OUTPUT_DIR = os.path.join(WORKSPACE_ROOT, "portal", "docs", "domains")


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def slug(domain_name):
    """Convert domain name to URL-safe slug."""
    return domain_name.lower().replace(" ", "-")


def count_endpoints(svc_name):
    """Count REST endpoints from an OpenAPI spec."""
    spec_path = os.path.join(SPECS_DIR, f"{svc_name}.yaml")
    if not os.path.exists(spec_path):
        return 0
    spec = load_yaml(spec_path)
    count = 0
    for path_item in (spec.get("paths") or {}).values():
        for method in ("get", "post", "put", "patch", "delete", "head", "options"):
            if method in path_item:
                count += 1
    return count


# -- Domain team assignments (mirrors domains.yaml + copilot-instructions) --
DOMAIN_TEAMS = {
    "Operations": "NovaTrek Operations Team",
    "Guest Identity": "Guest Experience Team",
    "Booking": "Booking Platform Team",
    "Product Catalog": "Product Team",
    "Safety": "Safety and Compliance Team",
    "Logistics": "Logistics Team",
    "Guide Management": "Guide Operations Team",
    "External": "Integration Team",
    "Support": "Various (cross-cutting platform services)",
}

DOMAIN_DESCRIPTIONS = {
    "Operations": "Day-of-adventure workflows including guest check-in, schedule management, and real-time operational coordination. This domain orchestrates the core guest experience on the day of their adventure.",
    "Guest Identity": "Guest identity resolution, profile management, certifications, and medical information. The single source of truth for all guest identity data across the platform.",
    "Booking": "Reservation lifecycle management from creation through completion, including participant management, insurance add-ons, and status tracking.",
    "Product Catalog": "Adventure products, trip definitions, trail data, and the classification system that drives check-in UI patterns and safety workflows.",
    "Safety": "Guest and staff safety including waiver management, incident reporting, emergency response coordination, and wildlife/environmental monitoring.",
    "Logistics": "Physical asset management covering gear inventory, equipment tracking, transport coordination, and vehicle dispatch.",
    "Guide Management": "Guide assignment, certification tracking, availability management, and preference handling for adventure staffing.",
    "External": "Third-party booking channel integrations, partner API gateway, and external system connectivity.",
    "Support": "Cross-cutting platform services including notifications, payments, loyalty rewards, analytics, weather, location services, media gallery, procurement, and reviews.",
}

# Map ADRs to the primary services/domains they affect
ADR_SERVICE_MAP = {
    "ADR-003": ["svc-trail-management"],
    "ADR-004": ["svc-check-in", "svc-trip-catalog"],
    "ADR-005": ["svc-check-in"],
    "ADR-006": ["svc-check-in"],
    "ADR-007": ["svc-guest-profiles", "svc-check-in"],
    "ADR-008": ["svc-guest-profiles"],
    "ADR-009": ["svc-check-in"],
    "ADR-010": ["svc-scheduling-orchestrator"],
    "ADR-011": ["svc-scheduling-orchestrator"],
    "ADR-012": [],  # Platform-wide
    "ADR-013": [],  # Platform-wide
}

ADR_TITLES = {
    "ADR-001": "AI Toolchain Selection",
    "ADR-002": "Documentation Publishing Platform",
    "ADR-003": "Nullable Elevation Fields",
    "ADR-004": "Configuration-Driven Classification",
    "ADR-005": "Pattern 3 Default Fallback",
    "ADR-006": "Orchestrator Pattern for Check-In",
    "ADR-007": "Four-Field Identity Verification",
    "ADR-008": "Temporary Guest Profile",
    "ADR-009": "Session-Scoped Kiosk Access",
    "ADR-010": "PATCH Semantics for Schedule Updates",
    "ADR-011": "Optimistic Locking for Daily Schedule",
    "ADR-012": "TDD/BDD Hybrid Test Methodology",
    "ADR-013": "Spring Cloud Contract Testing",
}

# Bounded context rules specific to each domain
DOMAIN_RULES = {
    "Operations": [
        "[svc-check-in](../microservices/svc-check-in.md) is the designated **orchestrator** for all day-of-adventure workflows ([ADR-006](../decisions/ADR-006-orchestrator-pattern-checkin.md))",
        "[svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) **owns the schedule lifecycle** — other services MUST NOT mutate schedule data directly",
        "Schedule updates use **PATCH semantics** with optimistic locking to prevent data overwrites ([ADR-010](../decisions/ADR-010-patch-semantics-schedule-updates.md), [ADR-011](../decisions/ADR-011-optimistic-locking-daily-schedule.md))",
    ],
    "Guest Identity": [
        "Guest identity resolution **always flows through** [svc-guest-profiles](../microservices/svc-guest-profiles.md) — services MUST NOT maintain shadow guest records",
        "PII is encrypted at rest (AES-256) with GDPR-compliant retention policies",
        "Identity verification uses **four-field matching** ([ADR-007](../decisions/ADR-007-four-field-identity-verification.md))",
        "Temporary guest profiles have a 90-day TTL with merge-on-return semantics ([ADR-008](../decisions/ADR-008-temporary-guest-profile.md))",
    ],
    "Booking": [
        "Reservations use **optimistic locking** via `_rev` field to prevent concurrent update conflicts",
        "Reservation status transitions are event-sourced via `reservation.status_changed` Kafka events",
    ],
    "Product Catalog": [
        "Adventure classification is **configuration-driven** via YAML — no hardcoded constants ([ADR-004](../decisions/ADR-004-configuration-driven-classification.md))",
        "Trail elevation data may be null; all consumers must handle gracefully ([ADR-003](../decisions/ADR-003-nullable-elevation-fields.md))",
        "Unknown adventure categories MUST default to **Pattern 3** (Full Service) for safety ([ADR-005](../decisions/ADR-005-pattern3-default-fallback.md))",
    ],
    "Safety": [
        "Safety waivers are **legally binding** — digital signatures verified via DocuSign API",
        "All incidents are logged and propagated as domain events for analytics and notification",
        "Emergency response coordinates with guest profiles (medical info), location services (GPS), and guide management (nearest responder)",
    ],
    "Logistics": [
        "Gear assignments require validated guest identity and confirmed reservation before checkout",
        "Waiver status is checked before safety-critical gear can be issued",
    ],
    "Guide Management": [
        "Guide availability and preferences are **read-only** to [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator.md) — mutations only through this domain",
        "Guide certifications determine which adventure categories they can lead",
    ],
    "External": [
        "Partner bookings flow through the same reservation pipeline as direct bookings — partners call svc-partner-integrations which delegates to svc-reservations",
        "Commission processing is handled via svc-payments",
    ],
    "Support": [
        "Notification delivery is **multi-channel** (email via SendGrid, SMS via Twilio, push via Firebase)",
        "Payment processing integrates with external fraud detection before authorization",
        "Analytics events flow via Kafka consumers — [svc-analytics](../microservices/svc-analytics.md) subscribes to all domain events",
        "All support services are consumed by other domains but do not own core business data",
    ],
}

# Data ownership entries per domain
DATA_OWNERSHIP = {
    "Operations": [
        ("Check-in records", "svc-check-in", "svc-analytics, svc-notifications"),
        ("Daily schedules", "svc-scheduling-orchestrator", "svc-guide-management (read), svc-check-in (read)"),
    ],
    "Guest Identity": [
        ("Guest profiles", "svc-guest-profiles", "All services (read-only via API)"),
        ("Guest certifications", "svc-guest-profiles", "svc-safety-compliance, svc-guide-management"),
        ("Medical info", "svc-guest-profiles", "svc-emergency-response (read-only)"),
    ],
    "Booking": [
        ("Reservations", "svc-reservations", "svc-check-in, svc-scheduling-orchestrator, svc-partner-integrations"),
        ("Participants", "svc-reservations", "svc-check-in"),
    ],
    "Product Catalog": [
        ("Adventure catalog", "svc-trip-catalog", "svc-check-in, svc-reservations, svc-partner-integrations"),
        ("Trail data", "svc-trail-management", "svc-trip-catalog, svc-safety-compliance, svc-scheduling-orchestrator"),
    ],
    "Safety": [
        ("Waivers", "svc-safety-compliance", "svc-check-in (read-only for validation), svc-gear-inventory"),
        ("Safety incidents", "svc-safety-compliance", "svc-analytics, svc-notifications"),
        ("Emergency records", "svc-emergency-response", "svc-analytics, svc-notifications"),
        ("Wildlife sightings", "svc-wildlife-tracking", "svc-trail-management, svc-scheduling-orchestrator"),
    ],
    "Logistics": [
        ("Gear inventory", "svc-gear-inventory", "svc-check-in (read), svc-inventory-procurement"),
        ("Transport requests", "svc-transport-logistics", "svc-notifications"),
    ],
    "Guide Management": [
        ("Guide preferences", "svc-guide-management", "svc-scheduling-orchestrator (read-only)"),
        ("Guide certifications", "svc-guide-management", "svc-safety-compliance"),
        ("Guide availability", "svc-guide-management", "svc-scheduling-orchestrator, svc-emergency-response"),
    ],
    "External": [
        ("Partner bookings", "svc-partner-integrations", "svc-reservations (via delegation)"),
        ("Partner credentials", "svc-partner-integrations", "None"),
    ],
    "Support": [
        ("Notification log", "svc-notifications", "svc-analytics"),
        ("Payment records", "svc-payments", "svc-reservations, svc-analytics"),
        ("Loyalty points", "svc-loyalty-rewards", "svc-guest-profiles (read)"),
        ("Media assets", "svc-media-gallery", "svc-analytics"),
        ("Analytics events", "svc-analytics", "Internal (no external readers)"),
        ("Weather cache", "svc-weather", "svc-scheduling-orchestrator, svc-trail-management"),
        ("Location data", "svc-location-services", "svc-transport-logistics, svc-emergency-response, svc-trail-management"),
        ("Procurement orders", "svc-inventory-procurement", "svc-gear-inventory"),
        ("Guest reviews", "svc-reviews", "svc-trip-catalog, svc-analytics"),
    ],
}


def build_svc_to_domain(domains_data):
    """Build service -> domain name mapping."""
    mapping = {}
    for domain_name, info in domains_data.items():
        for svc in info.get("services", []):
            mapping[svc] = domain_name
    return mapping


def build_cross_domain_integrations(cross_calls, svc_to_domain, domain_services):
    """Build outbound and inbound cross-domain integrations for a domain."""
    # Label -> service name mapping
    label_to_svc = {
        "Reservations": "svc-reservations",
        "Guest Profiles": "svc-guest-profiles",
        "Trip Catalog": "svc-trip-catalog",
        "Trail Mgmt": "svc-trail-management",
        "Safety Compliance": "svc-safety-compliance",
        "Gear Inventory": "svc-gear-inventory",
        "Guide Mgmt": "svc-guide-management",
        "Weather Svc": "svc-weather",
        "Location Svc": "svc-location-services",
        "Payments Svc": "svc-payments",
        "Notifications": "svc-notifications",
        "Analytics": "svc-analytics",
    }

    outbound = []
    inbound = []

    for svc, endpoints in cross_calls.items():
        svc_domain = svc_to_domain.get(svc, "")
        for endpoint, calls in endpoints.items():
            for call in calls:
                target_svc = label_to_svc.get(call.get("label", ""), "")
                target_domain = svc_to_domain.get(target_svc, "")

                if not target_svc or target_domain == svc_domain:
                    continue  # skip intra-domain and external

                if svc in domain_services:
                    outbound.append({
                        "source": svc,
                        "target": target_svc,
                        "target_domain": target_domain,
                        "action": call.get("action", ""),
                        "async": call.get("async", False),
                    })
                elif target_svc in domain_services:
                    inbound.append({
                        "source": svc,
                        "source_domain": svc_domain,
                        "target": target_svc,
                        "action": call.get("action", ""),
                        "async": call.get("async", False),
                    })

    return outbound, inbound


def find_domain_events(events_data, domain_services, svc_to_domain):
    """Find events produced and consumed by a domain's services."""
    produced = []
    consumed = []

    for event_name, event in events_data.items():
        producer = event.get("producer", "")
        consumers = event.get("consumers", [])

        if producer in domain_services:
            produced.append({
                "name": event_name,
                "channel": event.get("channel", ""),
                "summary": event.get("summary", ""),
                "consumers": consumers,
            })

        for c in consumers:
            if c in domain_services:
                consumed.append({
                    "name": event_name,
                    "channel": event.get("channel", ""),
                    "summary": event.get("summary", ""),
                    "producer": producer,
                    "producer_domain": svc_to_domain.get(producer, ""),
                })

    return produced, consumed


def find_domain_adrs(domain_services):
    """Find ADRs relevant to a domain based on service mapping."""
    adrs = []
    for adr_id, services in ADR_SERVICE_MAP.items():
        if not services:
            continue  # platform-wide, skip
        for svc in services:
            if svc in domain_services:
                adrs.append(adr_id)
                break
    return sorted(set(adrs))


def find_domain_capabilities(caps_data, domain_services):
    """Find capabilities served by this domain's services."""
    results = []
    for domain in caps_data.get("domains", []):
        for cap in domain.get("capabilities", []):
            cap_services = cap.get("services", [])
            overlap = set(cap_services) & domain_services
            if overlap:
                results.append({
                    "id": cap["id"],
                    "name": cap["name"],
                    "status": cap.get("status", "unknown"),
                    "description": cap.get("description", ""),
                    "services": list(overlap),
                })
    return results


def generate_domain_page(domain_name, domains_data, data_stores, cross_calls,
                         events_data, caps_data, svc_to_domain):
    """Generate a comprehensive domain detail page."""
    info = domains_data[domain_name]
    services = info.get("services", [])
    domain_services_set = set(services)
    team = DOMAIN_TEAMS.get(domain_name, "Unknown")
    description = DOMAIN_DESCRIPTIONS.get(domain_name, "")
    domain_slug = slug(domain_name)
    color = info.get("color", "#333")

    lines = []
    lines.append(f"# {domain_name} Domain\n")
    lines.append(f"**Team:** {team}  ")
    lines.append(f"**Services:** {len(services)}  ")
    lines.append(f"**Domain color:** {color}\n")
    lines.append(f"{description}\n")

    # ------------------------------------------------------------------
    # Topology Diagram
    # ------------------------------------------------------------------
    lines.append("---\n")
    lines.append("## Topology\n")
    svg_file = f"topology-{domain_slug}.svg"
    lines.append('<div class="diagram-wrap">')
    lines.append(f'  <a href="../../topology/svg/{svg_file}" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>')
    lines.append(f'  <object data="../../topology/svg/{svg_file}" type="image/svg+xml" style="max-width: 100%;">')
    lines.append(f"    {domain_name} Service Topology C4 Diagram")
    lines.append("  </object>")
    lines.append("</div>\n")

    # ------------------------------------------------------------------
    # Services Table
    # ------------------------------------------------------------------
    lines.append("---\n")
    lines.append("## Services\n")
    lines.append("| Service | Database Engine | Schema | Tables | API Endpoints |")
    lines.append("|---------|----------------|--------|--------|---------------|")
    for svc in services:
        ds = data_stores.get(svc, {})
        engine = ds.get("engine", "—")
        schema_name = ds.get("schema", "—")
        tables = ds.get("tables", [])
        table_count = len(tables)
        endpoint_count = count_endpoints(svc)
        lines.append(
            f"| [{svc}](../microservices/{svc}.md) | {engine} | `{schema_name}` "
            f"| {table_count} | {endpoint_count} |"
        )
    lines.append("")

    # ------------------------------------------------------------------
    # Data Ownership
    # ------------------------------------------------------------------
    ownership = DATA_OWNERSHIP.get(domain_name, [])
    if ownership:
        lines.append("---\n")
        lines.append("## Data Ownership\n")
        lines.append("Every data entity has exactly one owning service. Other services access it read-only through APIs.\n")
        lines.append("| Data Entity | Owning Service | Read Access |")
        lines.append("|-------------|---------------|-------------|")
        for entity, owner, readers in ownership:
            lines.append(f"| {entity} | [{owner}](../microservices/{owner}.md) | {readers} |")
        lines.append("")

    # ------------------------------------------------------------------
    # Data Store Details
    # ------------------------------------------------------------------
    lines.append("---\n")
    lines.append("## Data Stores\n")
    for svc in services:
        ds = data_stores.get(svc, {})
        if not ds:
            continue
        lines.append(f"### {svc}\n")
        lines.append(f"- **Engine:** {ds.get('engine', '—')}")
        lines.append(f"- **Schema:** `{ds.get('schema', '—')}`")
        tables = ds.get("tables", [])
        if tables:
            lines.append(f"- **Tables:** {', '.join(f'`{t}`' for t in tables)}")
        features = ds.get("features", [])
        if features:
            lines.append(f"- **Features:**")
            for feat in features:
                lines.append(f"    - {feat}")
        volume = ds.get("volume")
        if volume:
            lines.append(f"- **Volume:** {volume}")
        backup = ds.get("backup")
        if backup:
            lines.append(f"- **Backup:** {backup}")
        lines.append("")

    # ------------------------------------------------------------------
    # Bounded Context Rules
    # ------------------------------------------------------------------
    rules = DOMAIN_RULES.get(domain_name, [])
    if rules:
        lines.append("---\n")
        lines.append("## Bounded Context Rules\n")
        lines.append("These rules are non-negotiable for this domain.\n")
        for i, rule in enumerate(rules, 1):
            lines.append(f"{i}. {rule}")
        lines.append("")

    # ------------------------------------------------------------------
    # Cross-Domain Integrations
    # ------------------------------------------------------------------
    outbound, inbound = build_cross_domain_integrations(
        cross_calls, svc_to_domain, domain_services_set
    )

    lines.append("---\n")
    lines.append("## Cross-Domain Integration\n")

    if outbound:
        lines.append("### Outbound (this domain calls)\n")
        lines.append("| Source | Target | Target Domain | Action | Async |")
        lines.append("|--------|--------|--------------|--------|-------|")
        seen = set()
        for call in outbound:
            key = (call["source"], call["target"], call["action"])
            if key in seen:
                continue
            seen.add(key)
            async_label = "Yes" if call["async"] else "No"
            lines.append(
                f'| [{call["source"]}](../microservices/{call["source"]}.md) '
                f'| [{call["target"]}](../microservices/{call["target"]}.md) '
                f'| {call["target_domain"]} '
                f'| {call["action"]} | {async_label} |'
            )
        lines.append("")
    else:
        lines.append("### Outbound\n")
        lines.append("No outbound cross-domain calls.\n")

    if inbound:
        lines.append("### Inbound (called by other domains)\n")
        lines.append("| Source | Source Domain | Target | Action | Async |")
        lines.append("|--------|-------------|--------|--------|-------|")
        seen = set()
        for call in inbound:
            key = (call["source"], call["target"], call["action"])
            if key in seen:
                continue
            seen.add(key)
            async_label = "Yes" if call["async"] else "No"
            lines.append(
                f'| [{call["source"]}](../microservices/{call["source"]}.md) '
                f'| {call["source_domain"]} '
                f'| [{call["target"]}](../microservices/{call["target"]}.md) '
                f'| {call["action"]} | {async_label} |'
            )
        lines.append("")
    else:
        lines.append("### Inbound\n")
        lines.append("No inbound cross-domain calls.\n")

    # ------------------------------------------------------------------
    # Domain Events
    # ------------------------------------------------------------------
    produced, consumed = find_domain_events(events_data, domain_services_set, svc_to_domain)

    lines.append("---\n")
    lines.append("## Domain Events\n")

    if produced:
        lines.append("### Events Produced\n")
        lines.append("| Event | Channel | Producer | Summary |")
        lines.append("|-------|---------|----------|---------|")
        for ev in produced:
            consumers_str = ", ".join(ev["consumers"])
            lines.append(
                f'| `{ev["name"]}` | `{ev["channel"]}` '
                f'| [{events_data[ev["name"]]["producer"]}](../microservices/{events_data[ev["name"]]["producer"]}.md) '
                f'| {ev["summary"]} |'
            )
        lines.append("")
        lines.append("**Consumers of these events:**\n")
        for ev in produced:
            consumer_links = ", ".join(
                f'[{c}](../microservices/{c}.md)' for c in ev["consumers"]
            )
            lines.append(f'- `{ev["name"]}` → {consumer_links}')
        lines.append("")

    if consumed:
        lines.append("### Events Consumed\n")
        lines.append("| Event | Channel | Producer | Producer Domain | Consuming Service |")
        lines.append("|-------|---------|----------|----------------|-------------------|")
        seen = set()
        for ev in consumed:
            # Find which of our services consume this
            for svc in services:
                if svc in events_data[ev["name"]].get("consumers", []):
                    key = (ev["name"], svc)
                    if key in seen:
                        continue
                    seen.add(key)
                    lines.append(
                        f'| `{ev["name"]}` | `{ev["channel"]}` '
                        f'| [{ev["producer"]}](../microservices/{ev["producer"]}.md) '
                        f'| {ev["producer_domain"]} '
                        f'| [{svc}](../microservices/{svc}.md) |'
                    )
        lines.append("")

    if not produced and not consumed:
        lines.append("No domain events produced or consumed by this domain.\n")

    # ------------------------------------------------------------------
    # Related Architecture Decisions
    # ------------------------------------------------------------------
    adrs = find_domain_adrs(domain_services_set)
    if adrs:
        lines.append("---\n")
        lines.append("## Architecture Decisions\n")
        lines.append("ADRs that directly constrain or shape this domain.\n")
        lines.append("| ADR | Title |")
        lines.append("|-----|-------|")
        for adr_id in adrs:
            title = ADR_TITLES.get(adr_id, adr_id)
            filename = f"{adr_id}-{title.lower().replace(' ', '-').replace('/', '-')}"
            # Use the actual filenames from decisions/
            adr_slug = adr_id.lower()
            lines.append(f"| [{adr_id}](../decisions/{adr_id}-{slug_from_title(title)}.md) | {title} |")
        lines.append("")

    # ------------------------------------------------------------------
    # Business Capabilities
    # ------------------------------------------------------------------
    capabilities = find_domain_capabilities(caps_data, domain_services_set)
    if capabilities:
        lines.append("---\n")
        lines.append("## Business Capabilities\n")
        lines.append("Capabilities served by this domain's services.\n")
        lines.append("| ID | Capability | Status | Description |")
        lines.append("|----|-----------|--------|-------------|")
        for cap in capabilities:
            status_label = cap["status"].upper().replace("-", " ")
            lines.append(
                f'| {cap["id"]} | {cap["name"]} | {status_label} | {cap["description"]} |'
            )
        lines.append("")

    # ------------------------------------------------------------------
    # Quick Links
    # ------------------------------------------------------------------
    lines.append("---\n")
    lines.append("## Quick Links\n")
    lines.append(f"- [Domain Topology View](../topology/domain-views.md#{domain_slug})")
    for svc in services:
        lines.append(f"- [{svc} Microservice Page](../microservices/{svc}.md)")
    lines.append(f"- [Event Catalog](../events/index.md)")
    lines.append(f"- [Business Capabilities](../capabilities/index.md)")
    lines.append("")

    # ------------------------------------------------------------------
    # Data Source Footer
    # ------------------------------------------------------------------
    lines.append("---\n")
    lines.append("*Generated from `architecture/metadata/` YAML files by `portal/scripts/generate-domain-pages.py`.*\n")

    return "\n".join(lines)


def slug_from_title(title):
    """Convert ADR title to filename slug."""
    # Map known titles to actual filenames
    mapping = {
        "Nullable Elevation Fields": "nullable-elevation-fields",
        "Configuration-Driven Classification": "configuration-driven-classification",
        "Pattern 3 Default Fallback": "pattern3-default-fallback",
        "Orchestrator Pattern for Check-In": "orchestrator-pattern-checkin",
        "Four-Field Identity Verification": "four-field-identity-verification",
        "Temporary Guest Profile": "temporary-guest-profile",
        "Session-Scoped Kiosk Access": "session-scoped-kiosk-access",
        "PATCH Semantics for Schedule Updates": "patch-semantics-schedule-updates",
        "Optimistic Locking for Daily Schedule": "optimistic-locking-daily-schedule",
        "TDD/BDD Hybrid Test Methodology": "test-methodology-tdd-bdd-hybrid",
        "Spring Cloud Contract Testing": "spring-cloud-contract-testing",
        "AI Toolchain Selection": "ai-toolchain-selection",
        "Documentation Publishing Platform": "documentation-publishing-platform",
    }
    return mapping.get(title, title.lower().replace(" ", "-"))


def generate_index_page(domains_data, data_stores, events_data, caps_data, svc_to_domain):
    """Generate the domain overview index page."""
    lines = []
    lines.append("# Domains\n")
    lines.append("The NovaTrek Adventures platform is decomposed into **9 bounded contexts** (domains), each owning a set of microservices with clearly defined data ownership boundaries.\n")
    lines.append("Click any domain to view its comprehensive detail page including services, data stores, integrations, events, decisions, and capabilities.\n")

    # ------------------------------------------------------------------
    # System Overview Diagram
    # ------------------------------------------------------------------
    lines.append("## System Overview\n")
    lines.append('<div class="diagram-wrap">')
    lines.append('  <a href="../topology/svg/topology-domain-overview.svg" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>')
    lines.append('  <object data="../topology/svg/topology-domain-overview.svg" type="image/svg+xml" style="max-width: 100%;">')
    lines.append("    NovaTrek Domain Overview C4 Diagram")
    lines.append("  </object>")
    lines.append("</div>\n")

    # ------------------------------------------------------------------
    # Domain Gallery — visual card per domain
    # ------------------------------------------------------------------
    domain_colors = {
        "Operations":       {"strong": "#2563eb", "light": "#DBEAFE"},
        "Guest Identity":   {"strong": "#7c3aed", "light": "#EDE9FE"},
        "Booking":          {"strong": "#059669", "light": "#D1FAE5"},
        "Product Catalog":  {"strong": "#d97706", "light": "#FEF3C7"},
        "Safety":           {"strong": "#dc2626", "light": "#FEE2E2"},
        "Logistics":        {"strong": "#0891b2", "light": "#CFFAFE"},
        "Guide Management": {"strong": "#4f46e5", "light": "#E0E7FF"},
        "External":         {"strong": "#9333ea", "light": "#F3E8FF"},
        "Support":          {"strong": "#64748b", "light": "#F1F5F9"},
    }

    lines.append("---\n")
    lines.append("## Domain Gallery\n")
    lines.append("Each domain's service topology. Click a diagram to explore the domain in detail.\n")

    for domain_name in domains_data:
        info = domains_data[domain_name]
        services = info.get("services", [])
        domain_services_set = set(services)
        team = DOMAIN_TEAMS.get(domain_name, "Unknown")
        description = DOMAIN_DESCRIPTIONS.get(domain_name, "")
        domain_slug_str = slug(domain_name)
        colors = domain_colors.get(domain_name, {"strong": "#616161", "light": "#F5F5F5"})

        produced, consumed = find_domain_events(events_data, domain_services_set, svc_to_domain)
        capabilities = find_domain_capabilities(caps_data, domain_services_set)

        svg_file = f"topology-{domain_slug_str}.svg"

        lines.append(f'<div style="border: 2px solid {colors["strong"]}; border-radius: 8px; margin-bottom: 1.5em; overflow: hidden;">')
        lines.append(f'  <div style="background: {colors["strong"]}; color: white; padding: 0.6em 1em; display: flex; justify-content: space-between; align-items: center;">')
        lines.append(f'    <strong style="font-size: 1.2em;"><a href="{domain_slug_str}" style="color: white; text-decoration: none;">{domain_name}</a></strong>')
        lines.append(f'    <span style="font-size: 0.85em; opacity: 0.9;">{team}</span>')
        lines.append(f'  </div>')
        lines.append(f'  <div style="padding: 0.8em 1em 0.4em;">')
        lines.append(f'    <p style="margin: 0 0 0.5em; font-size: 0.9em; color: #555;">{description}</p>')
        lines.append(f'    <p style="margin: 0 0 0.5em; font-size: 0.85em;">')
        lines.append(f'      <strong>{len(services)}</strong> services &nbsp;|&nbsp; ')
        lines.append(f'      <strong>{len(produced)}</strong> events produced &nbsp;|&nbsp; ')
        lines.append(f'      <strong>{len(consumed)}</strong> events consumed &nbsp;|&nbsp; ')
        lines.append(f'      <strong>{len(capabilities)}</strong> capabilities')
        lines.append(f'    </p>')
        lines.append(f'  </div>')
        lines.append(f'  <div style="padding: 0 1em 1em;">')
        lines.append(f'    <object data="../topology/svg/{svg_file}" type="image/svg+xml" style="max-width: 100%;">')
        lines.append(f"      {domain_name} Service Topology")
        lines.append(f"    </object>")
        lines.append(f'  </div>')
        lines.append(f'</div>\n')

    lines.append("")

    # Summary table
    lines.append("---\n")
    lines.append("## Domain Overview\n")
    lines.append("| Domain | Services | Team | Events Produced | Events Consumed | Capabilities |")
    lines.append("|--------|----------|------|-----------------|-----------------|-------------|")

    for domain_name in domains_data:
        info = domains_data[domain_name]
        services = info.get("services", [])
        domain_services_set = set(services)
        team = DOMAIN_TEAMS.get(domain_name, "Unknown")
        domain_slug_str = slug(domain_name)

        produced, consumed = find_domain_events(events_data, domain_services_set, svc_to_domain)
        capabilities = find_domain_capabilities(caps_data, domain_services_set)

        lines.append(
            f"| **[{domain_name}]({domain_slug_str}.md)** "
            f"| {len(services)} "
            f"| {team} "
            f"| {len(produced)} "
            f"| {len(consumed)} "
            f"| {len(capabilities)} |"
        )
    lines.append("")

    # Service-to-domain mapping
    lines.append("---\n")
    lines.append("## Service-to-Domain Map\n")
    lines.append("Complete mapping of all microservices to their owning domain.\n")
    lines.append("| Service | Domain | Database Engine |")
    lines.append("|---------|--------|----------------|")
    for domain_name in domains_data:
        for svc in domains_data[domain_name].get("services", []):
            ds = data_stores.get(svc, {})
            engine = ds.get("engine", "—")
            domain_slug_str = slug(domain_name)
            lines.append(
                f"| [{svc}](../microservices/{svc}.md) | [{domain_name}]({domain_slug_str}.md) | {engine} |"
            )
    lines.append("")

    # Cross-domain integration heatmap (simplified)
    lines.append("---\n")
    lines.append("## Cross-Domain Dependencies\n")
    lines.append("Summary of which domains call which other domains.\n")

    all_domains = list(domains_data.keys())
    # Build dependency matrix
    dep_matrix = {}
    cross_calls = load_yaml(os.path.join(METADATA_DIR, "cross-service-calls.yaml"))
    label_to_svc = {
        "Reservations": "svc-reservations",
        "Guest Profiles": "svc-guest-profiles",
        "Trip Catalog": "svc-trip-catalog",
        "Trail Mgmt": "svc-trail-management",
        "Safety Compliance": "svc-safety-compliance",
        "Gear Inventory": "svc-gear-inventory",
        "Guide Mgmt": "svc-guide-management",
        "Weather Svc": "svc-weather",
        "Location Svc": "svc-location-services",
        "Payments Svc": "svc-payments",
        "Notifications": "svc-notifications",
        "Analytics": "svc-analytics",
    }

    for svc, endpoints in cross_calls.items():
        source_domain = svc_to_domain.get(svc, "")
        for endpoint, calls in endpoints.items():
            for call in calls:
                target_svc = label_to_svc.get(call.get("label", ""), "")
                target_domain = svc_to_domain.get(target_svc, "")
                if source_domain and target_domain and source_domain != target_domain:
                    key = (source_domain, target_domain)
                    dep_matrix[key] = dep_matrix.get(key, 0) + 1

    lines.append("| From \\ To | " + " | ".join(f"**{d}**" for d in all_domains) + " |")
    lines.append("|" + "---|" * (len(all_domains) + 1))
    for src in all_domains:
        cells = []
        for tgt in all_domains:
            if src == tgt:
                cells.append("—")
            else:
                count = dep_matrix.get((src, tgt), 0)
                if count > 0:
                    cells.append(str(count))
                else:
                    cells.append("·")
        lines.append(f"| **{src}** | " + " | ".join(cells) + " |")
    lines.append("")

    # Event flow summary
    lines.append("---\n")
    lines.append("## Event Flow Summary\n")
    lines.append("| Event | Producer Domain | Consumer Domains |")
    lines.append("|-------|----------------|-----------------|")
    for event_name, event in events_data.items():
        producer = event.get("producer", "")
        producer_domain = svc_to_domain.get(producer, "")
        consumer_domains = sorted(set(
            svc_to_domain.get(c, "") for c in event.get("consumers", [])
        ) - {""})
        lines.append(
            f"| `{event_name}` | {producer_domain} | {', '.join(consumer_domains)} |"
        )
    lines.append("")

    # Footer
    lines.append("---\n")
    lines.append("*Generated from `architecture/metadata/` YAML files by `portal/scripts/generate-domain-pages.py`.*\n")

    return "\n".join(lines)


def main():
    print("Generating domain pages...")

    # Load all metadata
    domains_data = load_yaml(os.path.join(METADATA_DIR, "domains.yaml"))
    data_stores = load_yaml(os.path.join(METADATA_DIR, "data-stores.yaml"))
    cross_calls = load_yaml(os.path.join(METADATA_DIR, "cross-service-calls.yaml"))
    events_data = load_yaml(os.path.join(METADATA_DIR, "events.yaml"))
    caps_data = load_yaml(os.path.join(METADATA_DIR, "capabilities.yaml"))

    svc_to_domain = build_svc_to_domain(domains_data)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generate index page
    index_content = generate_index_page(domains_data, data_stores, events_data, caps_data, svc_to_domain)
    index_path = os.path.join(OUTPUT_DIR, "index.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_content)
    print(f"  wrote {index_path}")

    # Generate per-domain pages
    for domain_name in domains_data:
        content = generate_domain_page(
            domain_name, domains_data, data_stores, cross_calls,
            events_data, caps_data, svc_to_domain
        )
        page_path = os.path.join(OUTPUT_DIR, f"{slug(domain_name)}.md")
        with open(page_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  wrote {page_path}")

    print(f"Done — generated {1 + len(domains_data)} domain pages in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
