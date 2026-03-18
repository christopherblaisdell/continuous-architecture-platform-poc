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
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from load_metadata import diagram_source_badge  # noqa: E402

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
CALM_DIR = WORKSPACE_ROOT / "architecture" / "calm"
OUTPUT_DIR = WORKSPACE_ROOT / "portal" / "docs" / "topology"

# Domain colors for Mermaid styling
DOMAIN_COLORS = {
    "Operations": "#1B5E20",
    "Guest Identity": "#0D47A1",
    "Booking": "#E65100",
    "Product Catalog": "#4A148C",
    "Safety": "#B71C1C",
    "Logistics": "#006064",
    "Guide Management": "#33691E",
    "External": "#37474F",
    "Support": "#4E342E",
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


def generate_domain_overview(topology):
    """Generate a domain-level Mermaid diagram (domains as nodes, aggregated edges)."""
    _, _, svc_domain, domains, rest_edges, kafka_edges = _extract_topology_data(topology)

    # Aggregate edges to domain-to-domain level
    domain_rest = defaultdict(int)
    domain_kafka = defaultdict(int)
    for src, tgt in rest_edges:
        src_d = svc_domain[src]
        tgt_d = svc_domain[tgt]
        if src_d != tgt_d:
            domain_rest[(src_d, tgt_d)] += 1
    for src, tgt in kafka_edges:
        src_d = svc_domain[src]
        tgt_d = svc_domain[tgt]
        if src_d != tgt_d:
            domain_kafka[(src_d, tgt_d)] += 1

    # Also count intra-domain edges for the node labels
    intra_rest = defaultdict(int)
    intra_kafka = defaultdict(int)
    for src, tgt in rest_edges:
        src_d = svc_domain[src]
        tgt_d = svc_domain[tgt]
        if src_d == tgt_d:
            intra_rest[src_d] += 1
    for src, tgt in kafka_edges:
        src_d = svc_domain[src]
        tgt_d = svc_domain[tgt]
        if src_d == tgt_d:
            intra_kafka[src_d] += 1

    lines = ["```mermaid", "flowchart TB"]
    lines.append("")

    # Domain nodes with service counts
    for domain in sorted(domains.keys()):
        safe = domain.replace(" ", "_")
        n_svcs = len(domains[domain])
        svc_word = "service" if n_svcs == 1 else "services"
        intra = intra_rest[domain] + intra_kafka[domain]
        intra_note = f"\\n{intra} internal connections" if intra > 0 else ""
        lines.append(f"    {safe}[\"{domain}\\n{n_svcs} {svc_word}{intra_note}\"]")
    lines.append("")

    # Cross-domain REST edges with counts
    lines.append("    %% Cross-domain REST calls")
    for (src_d, tgt_d), count in sorted(domain_rest.items()):
        src_safe = src_d.replace(" ", "_")
        tgt_safe = tgt_d.replace(" ", "_")
        lines.append(f"    {src_safe} -->|{count} REST| {tgt_safe}")
    lines.append("")

    # Cross-domain Kafka edges with counts
    lines.append("    %% Cross-domain event flows")
    for (src_d, tgt_d), count in sorted(domain_kafka.items()):
        src_safe = src_d.replace(" ", "_")
        tgt_safe = tgt_d.replace(" ", "_")
        lines.append(f"    {src_safe} -.->|{count} events| {tgt_safe}")
    lines.append("")

    # Styling
    lines.append("    %% Styling")
    for domain in domains:
        safe = domain.replace(" ", "_")
        color = DOMAIN_COLORS.get(domain, "#616161")
        lines.append(f"    style {safe} fill:{color}20,stroke:{color},stroke-width:2px,color:#fff")

    lines.append("```")
    return "\n".join(lines)


def generate_domain_diagram(topology, target_domain):
    """Generate a Mermaid diagram for a single domain showing its services and cross-domain connections."""
    _, _, svc_domain, domains, rest_edges, kafka_edges = _extract_topology_data(topology)

    domain_svc_ids = {s["unique-id"] for s in domains[target_domain]}

    # Find all edges involving this domain's services
    relevant_rest = [(s, t) for s, t in rest_edges if s in domain_svc_ids or t in domain_svc_ids]
    relevant_kafka = [(s, t) for s, t in kafka_edges if s in domain_svc_ids or t in domain_svc_ids]

    # Collect external services that connect to this domain, grouped by their domain
    external_svcs = set()
    for s, t in relevant_rest + relevant_kafka:
        if s not in domain_svc_ids:
            external_svcs.add(s)
        if t not in domain_svc_ids:
            external_svcs.add(t)

    external_by_domain = defaultdict(set)
    for sid in external_svcs:
        external_by_domain[svc_domain[sid]].add(sid)

    lines = ["```mermaid", "flowchart TB"]
    lines.append("")

    # Target domain subgraph
    safe_target = target_domain.replace(" ", "_")
    lines.append(f"    subgraph {safe_target}[\"{target_domain}\"]")
    for svc in sorted(domains[target_domain], key=lambda s: s["unique-id"]):
        sid = svc["unique-id"]
        lines.append(f"        {sid}[\"{short_name(sid)}\"]")
    lines.append("    end")
    lines.append("")

    # External domain subgraphs
    for ext_domain in sorted(external_by_domain.keys()):
        safe_ext = ext_domain.replace(" ", "_")
        lines.append(f"    subgraph {safe_ext}[\"{ext_domain}\"]")
        for sid in sorted(external_by_domain[ext_domain]):
            lines.append(f"        {sid}[\"{short_name(sid)}\"]")
        lines.append("    end")
        lines.append("")

    # REST edges
    if relevant_rest:
        lines.append("    %% REST calls")
        for src, tgt in sorted(relevant_rest):
            lines.append(f"    {src} --> {tgt}")
        lines.append("")

    # Kafka edges
    if relevant_kafka:
        lines.append("    %% Event flows")
        for src, tgt in sorted(relevant_kafka):
            lines.append(f"    {src} -.-> {tgt}")
        lines.append("")

    # Styling
    lines.append("    %% Styling")
    target_color = DOMAIN_COLORS.get(target_domain, "#616161")
    lines.append(f"    style {safe_target} fill:{target_color}15,stroke:{target_color},stroke-width:2px")
    for ext_domain in external_by_domain:
        safe_ext = ext_domain.replace(" ", "_")
        color = DOMAIN_COLORS.get(ext_domain, "#616161")
        lines.append(f"    style {safe_ext} fill:{color}08,stroke:{color},stroke-width:1px,stroke-dasharray: 5 5")

    lines.append("```")
    return "\n".join(lines)


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


def write_system_map_page(topology):
    """Write the system map page with domain-level overview and links to per-domain detail."""
    overview = generate_domain_overview(topology)
    _, _, svc_domain, domains, rest_edges, kafka_edges = _extract_topology_data(topology)

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

    content = f"""# System Map

Domain-level topology for NovaTrek Adventures — {n_services} services across {n_domains} domains.

!!! info "Everything on this portal is entirely fictional"
    NovaTrek Adventures is a completely fictitious company used as a synthetic workspace for the Continuous Architecture Platform proof of concept.

---

## Domain Overview

Each node represents a domain (bounded context) containing one or more microservices. Arrows show **cross-domain** communication — internal connections within a domain are noted on each node.

**Solid arrows** = synchronous REST calls (HTTPS)
**Dashed arrows** = asynchronous event flows (Kafka)

{overview}
{diagram_source_badge(
    'architecture/calm/novatrek-topology.json',
    'https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/calm/novatrek-topology.json',
)}

---

## Domains

Click a domain to see its service-level topology diagram with individual service connections.

| Domain | Services | REST Out | Events Out |
|--------|----------|----------|------------|
{domain_table_rows}
---

## Legend

| Element | Meaning |
|---------|---------|
| Domain node | Bounded context containing one or more services |
| Solid arrow with count | Cross-domain synchronous REST calls |
| Dashed arrow with count | Cross-domain asynchronous Kafka events |
| Internal connections note | Intra-domain service-to-service calls |

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


def write_domain_views_page(topology):
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

        # Per-domain topology diagram
        domain_diagram = generate_domain_diagram(topology, domain)
        content += "### Topology\n\n"
        content += "**Solid arrows** = REST calls  |  **Dashed arrows** = Kafka events  |  "
        content += "Dashed border = external domain\n\n"
        content += domain_diagram
        content += "\n"
        content += diagram_source_badge(
            "architecture/calm/novatrek-topology.json",
            "https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/calm/novatrek-topology.json",
        )
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

    write_index_page(topology)
    write_system_map_page(topology)
    write_dependency_matrix_page(topology)
    write_domain_views_page(topology)

    print(f"Done — {4} pages written to {OUTPUT_DIR.relative_to(WORKSPACE_ROOT)}")


if __name__ == "__main__":
    main()
