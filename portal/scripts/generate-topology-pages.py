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
from collections import defaultdict
from pathlib import Path

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


def generate_system_map(topology):
    """Generate a Mermaid flowchart of the full system topology."""
    nodes = topology.get("nodes", [])
    relationships = topology.get("relationships", [])

    services = [n for n in nodes if n.get("node-type") == "service"]
    service_ids = {n["unique-id"] for n in services}

    # Group services by domain
    domains = defaultdict(list)
    for svc in services:
        domain = svc.get("metadata", {}).get("domain", "Unknown")
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

    # Build Mermaid diagram
    lines = ["```mermaid", "flowchart LR"]

    # Style definitions
    lines.append("")
    lines.append("    %% Domain subgraphs")

    for domain in sorted(domains.keys()):
        svcs = domains[domain]
        safe_domain = domain.replace(" ", "_")
        lines.append(f"    subgraph {safe_domain}[\"{domain}\"]")
        for svc in sorted(svcs, key=lambda s: s["unique-id"]):
            sid = svc["unique-id"]
            label = short_name(sid)
            lines.append(f"        {sid}[\"{label}\"]")
        lines.append("    end")
        lines.append("")

    # REST edges (solid arrows)
    lines.append("    %% REST calls (HTTPS)")
    for src, tgt in sorted(rest_edges):
        lines.append(f"    {src} --> {tgt}")

    lines.append("")

    # Kafka edges (dashed arrows)
    lines.append("    %% Event flows (Kafka)")
    for src, tgt in sorted(kafka_edges):
        lines.append(f"    {src} -.-> {tgt}")

    # Style classes
    lines.append("")
    lines.append("    %% Styling")
    for domain, svcs in domains.items():
        safe_domain = domain.replace(" ", "_")
        color = DOMAIN_COLORS.get(domain, "#616161")
        lines.append(f"    style {safe_domain} fill:{color}15,stroke:{color},stroke-width:2px")

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
    """Write the system map page with Mermaid diagram."""
    mermaid = generate_system_map(topology)

    content = f"""# System Map

Interactive service topology for NovaTrek Adventures — {sum(1 for n in topology['nodes'] if n.get('node-type') == 'service')} services across {len(set(n.get('metadata', {}).get('domain') for n in topology['nodes'] if n.get('node-type') == 'service'))} domains.

!!! info "Everything on this portal is entirely fictional"
    NovaTrek Adventures is a completely fictitious company used as a synthetic workspace for the Continuous Architecture Platform proof of concept.

---

## Full System Topology

**Solid arrows** = synchronous REST calls (HTTPS)
**Dashed arrows** = asynchronous event flows (Kafka)

{mermaid}

---

## Legend

| Element | Meaning |
|---------|---------|
| Solid box | Microservice |
| Colored subgraph | Domain boundary |
| Solid arrow (-->) | Synchronous REST call |
| Dashed arrow (-.->) | Asynchronous Kafka event |

## How to Read This Diagram

1. **Domains** are grouped as colored subgraphs — services within the same subgraph belong to the same bounded context
2. **High fan-in services** (many arrows pointing in) are shared platform services — `Guest Profiles`, `Notifications`, `Reservations`
3. **High fan-out services** (many arrows pointing out) are orchestrators — `Check In`, `Scheduling Orchestrator`, `Emergency Response`
4. **Dashed lines** indicate event-driven decoupling — the source publishes an event without knowing the consumer

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
