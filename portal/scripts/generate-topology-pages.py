#!/usr/bin/env python3
"""Generate topology visualization pages from CALM architecture data.

Reads the CALM topology JSON files and generates:
  - System map page with Mermaid diagram showing all services grouped by domain
  - Dependency matrix page showing service-to-service dependencies
  - Topology index page with summary statistics

Usage:
    python3 portal/scripts/generate-topology-pages.py
"""

import json
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
CALM_DIR = WORKSPACE_ROOT / "architecture" / "calm"
OUTPUT_DIR = WORKSPACE_ROOT / "portal" / "docs" / "topology"
PUML_DIR = OUTPUT_DIR / "puml"
SVG_DIR = OUTPUT_DIR / "svg"

# Domain colors matching architecture/diagrams/theme.puml
# (strong = border/accent, light = background)
DOMAIN_COLORS = {
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


def load_calm(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def short_name(svc_id):
    """Convert svc-check-in to Check In."""
    return svc_id.replace("svc-", "").replace("-", " ").title()


def svc_link(svc_id):
    """Return markdown link to service page."""
    return f"[{svc_id}](../microservices/{svc_id}.md)"


def _extract_topology_data(topology):
    """Extract services, domains, and edges from topology data."""
    nodes = topology.get("nodes", [])
    relationships = topology.get("relationships", [])

    services = [n for n in nodes if n.get("node-type") == "service"]
    service_ids = {n["unique-id"] for n in services}

    # Map service -> domain
    svc_domain = {}
    domains = defaultdict(list)
    for svc in services:
        domain = svc.get("metadata", {}).get("domain", "Unknown")
        svc_domain[svc["unique-id"]] = domain
        domains[domain].append(svc)

    # Collect service-to-service relationships (deduplicated)
    rest_edges = set()
    kafka_edges = set()
    for rel in relationships:
        src = rel["parties"]["source"]
        tgt = rel["parties"]["target"]
        if src in service_ids and tgt in service_ids:
            proto = rel.get("protocol", "")
            if proto == "HTTPS":
                rest_edges.add((src, tgt))
            elif proto == "Kafka":
                kafka_edges.add((src, tgt))

    return services, service_ids, svc_domain, domains, rest_edges, kafka_edges


def _safe_id(name):
    """Convert a domain name to a valid PlantUML identifier."""
    return name.replace(" ", "_").replace("-", "_")


def generate_domain_overview_svg(topology):
    """Generate a clean hand-laid SVG for the 9-domain overview in a 3x3 grid.

    Bypasses PlantUML entirely so the layout is deterministic and clean.
    Arrows are drawn center-to-center; boxes paint over the midpoints so
    visible arrows appear to start/end at box edges without any math.
    """
    _, _, svc_domain, domains, rest_edges, kafka_edges = _extract_topology_data(topology)

    # Aggregate to domain level
    domain_rest = defaultdict(int)
    domain_kafka = defaultdict(int)
    for src, tgt in rest_edges:
        src_d, tgt_d = svc_domain[src], svc_domain[tgt]
        if src_d != tgt_d:
            domain_rest[(src_d, tgt_d)] += 1
    for src, tgt in kafka_edges:
        src_d, tgt_d = svc_domain[src], svc_domain[tgt]
        if src_d != tgt_d:
            domain_kafka[(src_d, tgt_d)] += 1

    # Fixed 3×3 grid positions (row, col)
    GRID = {
        "External":        (0, 0),
        "Guest Identity":  (0, 1),
        "Booking":         (0, 2),
        "Product Catalog": (1, 0),
        "Operations":      (1, 1),
        "Safety":          (1, 2),
        "Guide Management":(2, 0),
        "Logistics":       (2, 1),
        "Support":         (2, 2),
    }

    # Layout constants
    BOX_W, BOX_H = 210, 80
    COL_GAP, ROW_GAP = 56, 66
    PAD_L, PAD_T = 44, 72   # PAD_T includes space for title

    total_w = PAD_L * 2 + 3 * BOX_W + 2 * COL_GAP
    total_h = PAD_T + 3 * BOX_H + 2 * ROW_GAP + 36
    RADIUS = 10

    def box_xy(domain):
        r, c = GRID[domain]
        return (PAD_L + c * (BOX_W + COL_GAP), PAD_T + r * (BOX_H + ROW_GAP))

    def box_center(domain):
        bx, by = box_xy(domain)
        return (bx + BOX_W // 2, by + BOX_H // 2)

    # Consolidate bidirectional pairs and build edge list
    all_pairs = set(domain_rest.keys()) | set(domain_kafka.keys())
    emitted = set()
    edges = []  # (src, tgt)
    for src_d, tgt_d in sorted(all_pairs):
        pair_key = tuple(sorted([src_d, tgt_d]))
        if pair_key in emitted:
            continue
        emitted.add(pair_key)
        if src_d in GRID and tgt_d in GRID:
            edges.append((src_d, tgt_d))

    out = []
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{total_h}" '
               f'viewBox="0 0 {total_w} {total_h}" role="img" '
               f'aria-label="NovaTrek Adventures domain overview">')
    out.append('<defs>')
    out.append('  <marker id="ah" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">')
    out.append('    <polygon points="0 0,8 3,0 6" fill="#94a3b8"/>')
    out.append('  </marker>')
    out.append('</defs>')
    out.append(f'<rect width="{total_w}" height="{total_h}" fill="white"/>')

    # Title
    out.append(f'<text x="{total_w // 2}" y="42" '
               f'font-family="Segoe UI,Helvetica,sans-serif" font-size="16" '
               f'font-weight="600" text-anchor="middle" fill="#1e293b">'
               f'NovaTrek Adventures &#8212; Domain Overview</text>')

    # Arrows drawn first (boxes will paint over the center portions)
    for src, tgt in edges:
        sx, sy = box_center(src)
        tx, ty = box_center(tgt)
        out.append(f'<line x1="{sx}" y1="{sy}" x2="{tx}" y2="{ty}" '
                   f'stroke="#cbd5e1" stroke-width="1.5" marker-end="url(#ah)"/>')

    # Boxes painted on top
    for domain in GRID:
        colors_d = DOMAIN_COLORS.get(domain, {"strong": "#616161", "light": "#F5F5F5"})
        bx, by = box_xy(domain)
        cx = bx + BOX_W // 2
        n_svcs = len(domains.get(domain, []))
        svc_word = "service" if n_svcs == 1 else "services"
        link_slug = domain.lower().replace(" ", "-")
        link = f"/topology/domain-views/#{link_slug}"

        out.append(f'<a href="{link}" style="text-decoration:none">')
        out.append(f'  <rect x="{bx}" y="{by}" width="{BOX_W}" height="{BOX_H}" '
                   f'rx="{RADIUS}" ry="{RADIUS}" fill="{colors_d["light"]}" '
                   f'stroke="{colors_d["strong"]}" stroke-width="2.5"/>')
        text_y1 = by + BOX_H // 2 - 7
        text_y2 = by + BOX_H // 2 + 13
        out.append(f'  <text x="{cx}" y="{text_y1}" '
                   f'font-family="Segoe UI,Helvetica,sans-serif" font-size="14" '
                   f'font-weight="600" text-anchor="middle" fill="{colors_d["strong"]}">'
                   f'{domain}</text>')
        out.append(f'  <text x="{cx}" y="{text_y2}" '
                   f'font-family="Segoe UI,Helvetica,sans-serif" font-size="11" '
                   f'text-anchor="middle" fill="{colors_d["strong"]}" opacity="0.75">'
                   f'{n_svcs} {svc_word}</text>')
        out.append('</a>')

    # Footer
    out.append(f'<text x="{total_w // 2}" y="{total_h - 10}" '
               f'font-family="Segoe UI,Helvetica,sans-serif" font-size="10" '
               f'text-anchor="middle" fill="#94a3b8">'
               f'Click any domain to explore its services and integrations</text>')

    out.append('</svg>')
    return "\n".join(out)


def generate_domain_overview_puml(topology):
    """Generate a C4 Context PUML for the domain-level overview."""
    _, _, svc_domain, domains, rest_edges, kafka_edges = _extract_topology_data(topology)

    # Aggregate edges to domain-to-domain level
    domain_rest = defaultdict(int)
    domain_kafka = defaultdict(int)
    for src, tgt in rest_edges:
        src_d, tgt_d = svc_domain[src], svc_domain[tgt]
        if src_d != tgt_d:
            domain_rest[(src_d, tgt_d)] += 1
    for src, tgt in kafka_edges:
        src_d, tgt_d = svc_domain[src], svc_domain[tgt]
        if src_d != tgt_d:
            domain_kafka[(src_d, tgt_d)] += 1

    lines = [
        "@startuml",
        "!include <c4/C4_Context>",
        "",
        "LAYOUT_TOP_DOWN()",
        "HIDE_STEREOTYPE()",
        "",
        'AddRelTag("kafka", $lineStyle=DashedLine(), $lineColor="#7c3aed", $textColor="#7c3aed")',
        "",
        "title NovaTrek Adventures — Domain Overview",
        "",
    ]

    # Define per-domain element tags for color differentiation
    for domain in sorted(domains.keys()):
        safe = _safe_id(domain)
        colors = DOMAIN_COLORS.get(domain, {"strong": "#616161", "light": "#F5F5F5"})
        lines.append(
            f'AddElementTag("{safe}", $bgColor="{colors["light"]}",'
            f' $borderColor="{colors["strong"]}",'
            f' $fontColor="{colors["strong"]}")'
        )
    lines.append("")

    # Each domain as a System node with its own color tag
    for domain in sorted(domains.keys()):
        safe = _safe_id(domain)
        n_svcs = len(domains[domain])
        svc_word = "service" if n_svcs == 1 else "services"
        link = domain.lower().replace(" ", "-")
        lines.append(
            f'System({safe}, "{domain}", "{n_svcs} {svc_word}",'
            f' $link="/topology/domain-views/#{link}",'
            f' $tags="{safe}")'
        )

    lines.append("")

    # Consolidate bidirectional edges: if A->B and B->A both exist,
    # merge into a single Rel_Neighbor (bidirectional) to reduce arrow noise.
    all_pairs = set(domain_rest.keys()) | set(domain_kafka.keys())
    emitted = set()  # track (min,max) pairs already written

    for src_d, tgt_d in sorted(all_pairs):
        pair_key = tuple(sorted([src_d, tgt_d]))
        if pair_key in emitted:
            continue
        emitted.add(pair_key)

        src_safe, tgt_safe = _safe_id(src_d), _safe_id(tgt_d)

        # Sum connections in both directions
        rest_fwd = domain_rest.get((src_d, tgt_d), 0)
        rest_rev = domain_rest.get((tgt_d, src_d), 0)
        kafka_fwd = domain_kafka.get((src_d, tgt_d), 0)
        kafka_rev = domain_kafka.get((tgt_d, src_d), 0)
        rest_total = rest_fwd + rest_rev
        kafka_total = kafka_fwd + kafka_rev

        if rest_total > 0 and kafka_total > 0:
            lines.append(f'Rel({src_safe}, {tgt_safe}, "{rest_total} REST + {kafka_total} events", "HTTPS / Kafka")')
        elif rest_total > 0:
            lines.append(f'Rel({src_safe}, {tgt_safe}, "{rest_total} REST calls", "HTTPS")')
        elif kafka_total > 0:
            lines.append(f'Rel({src_safe}, {tgt_safe}, "{kafka_total} events", "Kafka", $tags="kafka")')

    lines.append("")

    # Layout hints: arrange domains in a roughly 3x3 grid
    # Row 1: External, Guest Identity, Booking (entry points)
    # Row 2: Product Catalog, Operations, Safety (core adventure)
    # Row 3: Guide Management, Logistics, Support (supporting)
    lines.append("' Layout hints: 3-row grid")
    lines.append("Lay_R(External, Guest_Identity)")
    lines.append("Lay_R(Guest_Identity, Booking)")
    lines.append("Lay_D(External, Product_Catalog)")
    lines.append("Lay_R(Product_Catalog, Operations)")
    lines.append("Lay_R(Operations, Safety)")
    lines.append("Lay_D(Product_Catalog, Guide_Management)")
    lines.append("Lay_R(Guide_Management, Logistics)")
    lines.append("Lay_R(Logistics, Support)")

    lines.append("")
    lines.append("@enduml")

    return "\n".join(lines)


def generate_domain_detail_puml(topology, target_domain):
    """Generate a C4 Container PUML for a single domain with its services and cross-domain connections."""
    _, _, svc_domain, domains, rest_edges, kafka_edges = _extract_topology_data(topology)

    domain_svc_ids = {s["unique-id"] for s in domains[target_domain]}

    # Find all edges involving this domain's services
    relevant_rest = [(s, t) for s, t in rest_edges if s in domain_svc_ids or t in domain_svc_ids]
    relevant_kafka = [(s, t) for s, t in kafka_edges if s in domain_svc_ids or t in domain_svc_ids]

    # Collect external services grouped by their domain
    external_svcs = set()
    for s, t in relevant_rest + relevant_kafka:
        if s not in domain_svc_ids:
            external_svcs.add(s)
        if t not in domain_svc_ids:
            external_svcs.add(t)

    external_by_domain = defaultdict(set)
    for sid in external_svcs:
        external_by_domain[svc_domain[sid]].add(sid)

    lines = [
        "@startuml",
        "!include <c4/C4_Container>",
        "",
        "LAYOUT_WITH_LEGEND()",
        "LAYOUT_TOP_DOWN()",
        "",
        'AddRelTag("kafka", $lineStyle=DashedLine(), $lineColor="#7c3aed", $textColor="#7c3aed", $legendText="Kafka Events")',
        "",
        'header [[/topology/system-map/ \u2B06 System Map]]',
        f'title {target_domain} — Service Topology',
        "",
    ]

    # Target domain boundary with its services
    safe_target = _safe_id(target_domain)
    lines.append(f'System_Boundary({safe_target}, "{target_domain}") {{')
    for svc in sorted(domains[target_domain], key=lambda s: s["unique-id"]):
        sid = svc["unique-id"]
        safe_svc = _safe_id(sid)
        label = short_name(sid)
        lines.append(
            f'    Container({safe_svc}, "{sid}", "Java / Spring Boot", "{label}",'
            f' $link="/microservices/{sid}/#integration-context")'
        )
    lines.append("}")
    lines.append("")

    # External domain boundaries
    for ext_domain in sorted(external_by_domain.keys()):
        safe_ext = _safe_id(ext_domain)
        lines.append(f'System_Boundary({safe_ext}, "{ext_domain}") {{')
        for sid in sorted(external_by_domain[ext_domain]):
            safe_svc = _safe_id(sid)
            label = short_name(sid)
            lines.append(
                f'    Container({safe_svc}, "{sid}", "Java / Spring Boot", "{label}",'
                f' $link="/microservices/{sid}/#integration-context")'
            )
        lines.append("}")
        lines.append("")

    # REST relationships
    for src, tgt in sorted(relevant_rest):
        src_safe, tgt_safe = _safe_id(src), _safe_id(tgt)
        lines.append(f'Rel({src_safe}, {tgt_safe}, "API call", "HTTPS")')

    # Kafka relationships
    for src, tgt in sorted(relevant_kafka):
        src_safe, tgt_safe = _safe_id(src), _safe_id(tgt)
        lines.append(f'Rel({src_safe}, {tgt_safe}, "Event", "Kafka", $tags="kafka")')

    # Layout hints: stack external domain services vertically to reduce width
    for ext_domain in sorted(external_by_domain.keys()):
        ext_svcs = sorted(external_by_domain[ext_domain])
        for i in range(len(ext_svcs) - 1):
            lines.append(f"Lay_D({_safe_id(ext_svcs[i])}, {_safe_id(ext_svcs[i + 1])})")

    lines.append("")
    lines.append("@enduml")

    return "\n".join(lines)


def render_pumls_to_svg(puml_files):
    """Render PlantUML files to SVG."""
    if not puml_files:
        return
    svg_dir = str(SVG_DIR)
    result = subprocess.run(
        ["plantuml", "-tsvg", "-o", svg_dir] + [str(p) for p in puml_files],
        capture_output=True, text=True, timeout=120, check=False,
    )
    if result.returncode != 0:
        print(f"  WARNING: PlantUML returned {result.returncode}")
        if result.stderr:
            print(f"  stderr: {result.stderr[:500]}")


def svg_embed(svg_filename, alt_text):
    """Return HTML to embed an SVG diagram in the same style as microservice pages."""
    return (
        f'<div class="diagram-wrap">\n'
        f'  <a href="../svg/{svg_filename}" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>\n'
        f'  <object data="../svg/{svg_filename}" type="image/svg+xml" style="max-width: 100%;">\n'
        f"    {alt_text}\n"
        f"  </object>\n"
        f"</div>"
    )


def generate_dependency_matrix(topology):
    """Generate a markdown table showing service-to-service dependencies."""
    nodes = topology.get("nodes", [])
    relationships = topology.get("relationships", [])

    services = sorted(
        [n for n in nodes if n.get("node-type") == "service"],
        key=lambda n: (n.get("metadata", {}).get("domain", ""), n["unique-id"]),
    )
    service_ids = {n["unique-id"] for n in services}

    # Build dependency map: source -> target -> protocols
    deps = defaultdict(lambda: defaultdict(set))
    for rel in relationships:
        src = rel["parties"]["source"]
        tgt = rel["parties"]["target"]
        if src in service_ids and tgt in service_ids and src != tgt:
            proto = rel.get("protocol", "?")
            deps[src][tgt].add(proto)

    return services, deps


def generate_domain_stats(topology):
    """Generate per-domain statistics."""
    nodes = topology.get("nodes", [])
    relationships = topology.get("relationships", [])

    services = [n for n in nodes if n.get("node-type") == "service"]
    service_ids = {n["unique-id"] for n in services}
    domains = defaultdict(list)
    for svc in services:
        domain = svc.get("metadata", {}).get("domain", "Unknown")
        domains[domain].append(svc["unique-id"])

    # Count relationships per domain
    domain_rels = defaultdict(lambda: {"rest": 0, "kafka": 0, "total": 0})
    for rel in relationships:
        src = rel["parties"]["source"]
        if src not in service_ids:
            continue
        src_domain = next(
            (n.get("metadata", {}).get("domain", "?") for n in nodes if n["unique-id"] == src),
            "?",
        )
        proto = rel.get("protocol", "")
        if proto == "HTTPS":
            domain_rels[src_domain]["rest"] += 1
        elif proto == "Kafka":
            domain_rels[src_domain]["kafka"] += 1
        domain_rels[src_domain]["total"] += 1

    return domains, domain_rels


def write_index_page(topology):
    """Write the topology section index page."""
    nodes = topology.get("nodes", [])
    rels = topology.get("relationships", [])

    n_services = sum(1 for n in nodes if n.get("node-type") == "service")
    n_databases = sum(1 for n in nodes if n.get("node-type") == "database")
    n_rest = sum(1 for r in rels if r.get("protocol") == "HTTPS")
    n_kafka = sum(1 for r in rels if r.get("protocol") == "Kafka")
    n_jdbc = sum(1 for r in rels if r.get("protocol") == "JDBC")

    domains, domain_rels = generate_domain_stats(topology)

    content = f"""# System Topology

Auto-generated from the [CALM topology](../calm.md) — the machine-readable architecture model for NovaTrek Adventures.

!!! info "Everything on this portal is entirely fictional"
    NovaTrek Adventures is a completely fictitious company used as a synthetic workspace for the Continuous Architecture Platform proof of concept.

---

## Topology at a Glance

| Metric | Count |
|--------|-------|
| Services | {n_services} |
| Databases | {n_databases} |
| REST integrations | {n_rest} |
| Event flows (Kafka) | {n_kafka} |
| Database connections | {n_jdbc} |
| Total nodes | {len(nodes)} |
| Total relationships | {len(rels)} |

## Domain Summary

| Domain | Services | REST Calls | Event Flows | Total Relationships |
|--------|----------|------------|-------------|---------------------|
"""
    for domain in sorted(domains.keys()):
        svcs = domains[domain]
        stats = domain_rels.get(domain, {"rest": 0, "kafka": 0, "total": 0})
        content += f"| {domain} | {len(svcs)} | {stats['rest']} | {stats['kafka']} | {stats['total']} |\n"

    content += f"""
## Pages

| Page | Description |
|------|-------------|
| [System Map](system-map.md) | Interactive Mermaid diagram showing all {n_services} services grouped by domain with REST and event-driven connections |
| [Dependency Matrix](dependency-matrix.md) | Service-to-service dependency table showing which services call which, and over what protocol |
| [Domain Views](domain-views.md) | Per-domain topology details with service lists, databases, and relationship breakdowns |

## Data Source

All topology data is auto-generated from architecture metadata by `scripts/generate-calm.py` and validated by `scripts/validate-calm.py`. The CALM topology files live in `architecture/calm/`.

The generator reads 6 metadata sources:

- `architecture/metadata/domains.yaml` — service domain assignments
- `architecture/metadata/data-stores.yaml` — database configurations
- `architecture/metadata/cross-service-calls.yaml` — REST integrations
- `architecture/metadata/events.yaml` — Kafka event definitions
- `architecture/metadata/actors.yaml` — actors and frontend applications
- `architecture/specs/*.yaml` — OpenAPI specifications
"""

    path = OUTPUT_DIR / "index.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"  Generated {path.relative_to(WORKSPACE_ROOT)}")


def write_system_map_page(topology, puml_files):
    """Write the system map page with domain-level overview SVG."""
    _, _, _, domains, rest_edges, kafka_edges = _extract_topology_data(topology)

    # Write overview SVG directly (bypasses PlantUML for a clean 3x3 grid)
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    svg_path = SVG_DIR / "topology-domain-overview.svg"
    svg_path.write_text(generate_domain_overview_svg(topology))

    # Still write the PUML for reference/audit, but don't add to render queue
    puml_path = PUML_DIR / "topology-domain-overview.puml"
    PUML_DIR.mkdir(parents=True, exist_ok=True)
    puml_path.write_text(generate_domain_overview_puml(topology))

    n_services = sum(1 for n in topology["nodes"] if n.get("node-type") == "service")
    n_domains = len(set(n.get("metadata", {}).get("domain") for n in topology["nodes"] if n.get("node-type") == "service"))

    # Build domain summary table
    domain_table_rows = ""
    for domain in sorted(domains.keys()):
        n_svcs = len(domains[domain])
        domain_svc_ids = {s["unique-id"] for s in domains[domain]}
        n_rest_out = sum(1 for s, t in rest_edges if s in domain_svc_ids and t not in domain_svc_ids)
        n_kafka_out = sum(1 for s, t in kafka_edges if s in domain_svc_ids and t not in domain_svc_ids)
        slug = domain.lower().replace(" ", "-")
        domain_table_rows += f"| [{domain}](domain-views.md#{slug}) | {n_svcs} | {n_rest_out} | {n_kafka_out} |\n"

    overview_svg = svg_embed("topology-domain-overview.svg", "Domain Overview C4 Diagram")

    content = f"""# System Map

Domain-level topology for NovaTrek Adventures — {n_services} services across {n_domains} domains.

!!! info "Everything on this portal is entirely fictional"
    NovaTrek Adventures is a completely fictitious company used as a synthetic workspace for the Continuous Architecture Platform proof of concept.

---

## Domain Overview

Each node represents a domain (bounded context) containing one or more microservices. Arrows show **cross-domain** communication with connection counts.

{overview_svg}

---

## Domains

Click a domain in the diagram or table to see its service-level topology with individual connections.

| Domain | Services | REST Out | Events Out |
|--------|----------|----------|------------|
{domain_table_rows}
---

## Legend

| Element | Meaning |
|---------|---------|
| Blue box | Domain (bounded context) containing one or more services |
| Solid arrow with label | Synchronous REST calls (count shown) |
| Dashed purple arrow | Asynchronous Kafka events (count shown) |

## How to Read This Diagram

1. **Each box is a domain** — a bounded context owning a group of related microservices
2. **Arrows between domains** show cross-boundary communication with the number of distinct service-to-service connections
3. **High fan-in domains** (many arrows pointing in) provide shared platform capabilities — Guest Identity, Support
4. **Dashed lines** indicate event-driven decoupling — the source domain publishes events without knowing the consumers
5. **Drill down** into any domain via the [Domain Views](domain-views.md) page to see individual service connections

## Data Source

Generated from `architecture/calm/novatrek-topology.json` by `portal/scripts/generate-topology-pages.py`.
"""

    path = OUTPUT_DIR / "system-map.md"
    path.write_text(content)
    print(f"  Generated {path.relative_to(WORKSPACE_ROOT)}")


def write_dependency_matrix_page(topology):
    """Write the dependency matrix page."""
    services, deps = generate_dependency_matrix(topology)

    # Build a compact table with short names
    svc_list = [s["unique-id"] for s in services]
    svc_domains = {s["unique-id"]: s.get("metadata", {}).get("domain", "?") for s in services}

    content = """# Dependency Matrix

Service-to-service dependency table showing which services call which, and over what protocol.

!!! info "Everything on this portal is entirely fictional"
    NovaTrek Adventures is a completely fictitious company used as a synthetic workspace for the Continuous Architecture Platform proof of concept.

---

## Reading the Matrix

- Each row is a **calling service** (source)
- Each column shows the **protocol used**: REST (synchronous HTTPS) or Kafka (asynchronous event)
- Services are grouped by domain

## Outbound Dependencies (Who Does This Service Call?)

"""

    for domain in sorted(set(svc_domains.values())):
        domain_svcs = [s for s in svc_list if svc_domains[s] == domain]
        content += f"### {domain}\n\n"

        for src in domain_svcs:
            targets = deps.get(src, {})
            if not targets:
                content += f"**{svc_link(src)}** — No outbound service dependencies\n\n"
                continue

            content += f"**{svc_link(src)}** calls:\n\n"
            content += "| Target Service | Protocol |\n"
            content += "|----------------|----------|\n"

            for tgt in sorted(targets.keys()):
                protos = ", ".join(sorted(targets[tgt]))
                content += f"| {svc_link(tgt)} | {protos} |\n"

            content += "\n"

    # Fan-in/fan-out analysis
    fan_in = defaultdict(int)
    fan_out = defaultdict(int)
    for src in svc_list:
        targets = deps.get(src, {})
        fan_out[src] = len(targets)
        for tgt in targets:
            fan_in[tgt] += 1

    content += """---

## Coupling Analysis

### Highest Fan-In (Most Depended Upon)

Services with the most inbound dependencies — changes to these services have the widest blast radius.

| Service | Inbound Dependencies | Domain |
|---------|---------------------|--------|
"""
    for svc, count in sorted(fan_in.items(), key=lambda x: -x[1])[:10]:
        content += f"| {svc_link(svc)} | {count} | {svc_domains[svc]} |\n"

    content += """
### Highest Fan-Out (Most Dependencies)

Services with the most outbound calls — these services are most affected by changes elsewhere.

| Service | Outbound Dependencies | Domain |
|---------|----------------------|--------|
"""
    for svc, count in sorted(fan_out.items(), key=lambda x: -x[1])[:10]:
        if count > 0:
            content += f"| {svc_link(svc)} | {count} | {svc_domains[svc]} |\n"

    content += """
---

## Data Source

Generated from `architecture/calm/novatrek-topology.json` by `portal/scripts/generate-topology-pages.py`.
"""

    path = OUTPUT_DIR / "dependency-matrix.md"
    path.write_text(content)
    print(f"  Generated {path.relative_to(WORKSPACE_ROOT)}")


def write_domain_views_page(topology, puml_files):
    """Write per-domain topology details."""
    nodes = topology.get("nodes", [])
    relationships = topology.get("relationships", [])

    services = [n for n in nodes if n.get("node-type") == "service"]
    service_ids = {n["unique-id"] for n in services}
    databases = {n["unique-id"]: n for n in nodes if n.get("node-type") == "database"}

    # Group by domain
    domains = defaultdict(list)
    for svc in services:
        domain = svc.get("metadata", {}).get("domain", "Unknown")
        domains[domain].append(svc)

    # Map database connections
    db_owner = {}
    for rel in relationships:
        if rel.get("relationship-type") == "connects" and rel.get("protocol") == "JDBC":
            tgt = rel["parties"]["target"]
            if tgt in databases:
                db_owner[tgt] = rel["parties"]["source"]

    # Map service relationships
    svc_rels = defaultdict(lambda: {"rest_out": [], "rest_in": [], "kafka_out": [], "kafka_in": []})
    for rel in relationships:
        src = rel["parties"]["source"]
        tgt = rel["parties"]["target"]
        proto = rel.get("protocol", "")
        channel = rel.get("metadata", {}).get("channel", "")
        action = rel.get("metadata", {}).get("action", "")

        if src in service_ids and tgt in service_ids:
            if proto == "HTTPS":
                svc_rels[src]["rest_out"].append({"target": tgt, "action": action})
                svc_rels[tgt]["rest_in"].append({"source": src, "action": action})
            elif proto == "Kafka":
                svc_rels[src]["kafka_out"].append({"target": tgt, "channel": channel})
                svc_rels[tgt]["kafka_in"].append({"source": src, "channel": channel})

    content = """# Domain Views

Per-domain topology breakdown showing services, databases, and integration patterns for each bounded context.

!!! info "Everything on this portal is entirely fictional"
    NovaTrek Adventures is a completely fictitious company used as a synthetic workspace for the Continuous Architecture Platform proof of concept.

---

"""

    for domain in sorted(domains.keys()):
        svcs = sorted(domains[domain], key=lambda s: s["unique-id"])
        content += f"## {domain}\n\n"

        team = svcs[0].get("metadata", {}).get("team", "Unknown") if svcs else "Unknown"
        content += f"**Team:** {team}\n\n"

        # Per-domain topology diagram (C4 PlantUML SVG)
        slug = domain.lower().replace(" ", "-")
        puml_name = f"topology-{slug}.puml"
        svg_name = f"topology-{slug}.svg"
        puml_path = PUML_DIR / puml_name
        puml_path.write_text(generate_domain_detail_puml(topology, domain))
        puml_files.append(puml_path)

        content += "### Topology\n\n"
        content += svg_embed(svg_name, f"{domain} Service Topology C4 Diagram")
        content += "\n\n"

        # Services table
        content += "### Services\n\n"
        content += "| Service | Interfaces | Database | REST Out | REST In | Events Out | Events In |\n"
        content += "|---------|------------|----------|----------|---------|------------|----------|\n"

        for svc in svcs:
            sid = svc["unique-id"]
            n_ifaces = len(svc.get("interfaces", []))
            rels = svc_rels[sid]

            # Find this service's database
            db_name = "—"
            for db_id, owner in db_owner.items():
                if owner == sid:
                    db_node = databases[db_id]
                    engine = db_node.get("metadata", {}).get("engine", "?")
                    db_name = engine
                    break

            content += (
                f"| {svc_link(sid)} | {n_ifaces} | {db_name} "
                f"| {len(set(r['target'] for r in rels['rest_out']))} "
                f"| {len(set(r['source'] for r in rels['rest_in']))} "
                f"| {len(set(r['target'] for r in rels['kafka_out']))} "
                f"| {len(set(r['source'] for r in rels['kafka_in']))} |\n"
            )

        content += "\n"

        # Cross-domain calls
        domain_svc_ids = {s["unique-id"] for s in svcs}
        cross_domain_out = []
        cross_domain_in = []

        for svc in svcs:
            sid = svc["unique-id"]
            for r in svc_rels[sid]["rest_out"]:
                if r["target"] not in domain_svc_ids:
                    cross_domain_out.append({"source": sid, "target": r["target"], "action": r["action"]})
            for r in svc_rels[sid]["rest_in"]:
                if r["source"] not in domain_svc_ids:
                    cross_domain_in.append({"source": r["source"], "target": sid, "action": r["action"]})

        if cross_domain_out or cross_domain_in:
            content += "### Cross-Domain Integration\n\n"

            if cross_domain_out:
                content += "**Outbound (this domain calls):**\n\n"
                content += "| Source | Target | Action |\n"
                content += "|--------|--------|--------|\n"
                seen = set()
                for c in cross_domain_out:
                    key = (c["source"], c["target"])
                    if key not in seen:
                        seen.add(key)
                        content += f"| {svc_link(c['source'])} | {svc_link(c['target'])} | {c['action'] or '—'} |\n"
                content += "\n"

            if cross_domain_in:
                content += "**Inbound (called by other domains):**\n\n"
                content += "| Source | Target | Action |\n"
                content += "|--------|--------|--------|\n"
                seen = set()
                for c in cross_domain_in:
                    key = (c["source"], c["target"])
                    if key not in seen:
                        seen.add(key)
                        content += f"| {svc_link(c['source'])} | {svc_link(c['target'])} | {c['action'] or '—'} |\n"
                content += "\n"

        content += "---\n\n"

    content += """## Data Source

Generated from `architecture/calm/novatrek-topology.json` by `portal/scripts/generate-topology-pages.py`.
"""

    path = OUTPUT_DIR / "domain-views.md"
    path.write_text(content)
    print(f"  Generated {path.relative_to(WORKSPACE_ROOT)}")


def main():
    print("Generating topology pages from CALM data...")

    topology_path = CALM_DIR / "novatrek-topology.json"
    if not topology_path.exists():
        print(f"ERROR: {topology_path} not found. Run scripts/generate-calm.py first.")
        return

    topology = load_calm(topology_path)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PUML_DIR.mkdir(parents=True, exist_ok=True)
    SVG_DIR.mkdir(parents=True, exist_ok=True)

    # Copy theme.puml so PUML files can reference it
    theme_src = WORKSPACE_ROOT / "architecture" / "diagrams" / "theme.puml"
    if theme_src.is_file():
        shutil.copy2(theme_src, PUML_DIR / "theme.puml")

    puml_files = []

    write_index_page(topology)
    write_system_map_page(topology, puml_files)
    write_dependency_matrix_page(topology)
    write_domain_views_page(topology, puml_files)

    # Render all PUMLs to SVG
    if puml_files:
        print(f"  Rendering {len(puml_files)} PUML files to SVG...")
        render_pumls_to_svg(puml_files)
        svg_count = sum(1 for f in SVG_DIR.iterdir() if f.suffix == ".svg")
        print(f"  Rendered {svg_count} SVGs")

    print(f"Done — 4 pages + {len(puml_files)} diagrams written to {OUTPUT_DIR.relative_to(WORKSPACE_ROOT)}")


if __name__ == "__main__":
    main()
