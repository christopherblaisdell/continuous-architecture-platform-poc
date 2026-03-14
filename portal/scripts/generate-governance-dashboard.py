#!/usr/bin/env python3
"""Generate a governance compliance dashboard from CALM topology data.

Reads the CALM topology and validates each service node against the
NovaTrek organizational architecture standard, producing a portal page
that shows per-service compliance status for each governance rule.

Usage:
    python3 portal/scripts/generate-governance-dashboard.py

Output:
    portal/docs/topology/governance.md
"""

import json
from collections import defaultdict
from pathlib import Path

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
CALM_DIR = WORKSPACE_ROOT / "architecture" / "calm"
META_DIR = WORKSPACE_ROOT / "architecture" / "metadata"
OUTPUT_DIR = WORKSPACE_ROOT / "portal" / "docs" / "topology"

# Rules that fail with error severity (block merge)
ERROR_RULES = ("r1", "r2", "r4", "r6")
# Rules that fail with warning severity only
WARNING_RULES = ("r3", "r5")
# All rule keys
ALL_RULES = ERROR_RULES + WARNING_RULES


def load_calm(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_pci_services():
    pci_path = META_DIR / "pci.yaml"
    if not YAML_AVAILABLE or not pci_path.exists():
        return set()
    with open(pci_path) as f:
        pci = yaml.safe_load(f)
    return set(pci.get("services", []))


def svc_link(svc_id):
    return f"[{svc_id}](../microservices/{svc_id}/)"


def check_result(passed, severity="error"):
    if passed:
        return "PASS"
    return "FAIL" if severity == "error" else "WARN"


def run_governance_checks(topology, pci_services):
    """Run all governance rules against topology and return per-service results."""
    nodes = topology.get("nodes", [])
    relationships = topology.get("relationships", [])

    service_nodes = [n for n in nodes if n.get("node-type") == "service"]
    service_ids = {n["unique-id"] for n in service_nodes}
    db_nodes = {n["unique-id"] for n in nodes if n.get("node-type") == "database"}

    # Build DB ownership map
    db_connections = defaultdict(list)
    for rel in relationships:
        if rel.get("relationship-type") == "connects" and rel["parties"]["target"] in db_nodes:
            db_connections[rel["parties"]["target"]].append(rel["parties"]["source"])

    # Build service connectivity map
    connected = defaultdict(lambda: {"rest_out": 0, "rest_in": 0, "kafka_out": 0, "kafka_in": 0, "jdbc_violations": []})
    for rel in relationships:
        src = rel["parties"]["source"]
        tgt = rel["parties"]["target"]
        proto = rel.get("protocol", "")
        if proto == "JDBC" and src in service_ids and tgt in service_ids:
            connected[src]["jdbc_violations"].append(tgt)
        if src in service_ids and tgt in service_ids:
            if proto == "HTTPS":
                connected[src]["rest_out"] += 1
                connected[tgt]["rest_in"] += 1
            elif proto == "Kafka":
                connected[src]["kafka_out"] += 1
                connected[tgt]["kafka_in"] += 1

    # Build per-service check results
    results = []
    for svc in sorted(service_nodes, key=lambda s: s["unique-id"]):
        sid = svc["unique-id"]
        meta = svc.get("metadata", {})
        domain = meta.get("domain", "")
        team = meta.get("team", "")
        pci_flag = meta.get("pci-in-scope", False)

        # Rule 1: domain metadata present
        r1 = check_result(bool(domain), "error")

        # Rule 2: team metadata present
        r2 = check_result(bool(team), "error")

        # Rule 3: single database ownership
        owned_dbs = [db for db, owners in db_connections.items() if sid in owners]
        r3 = check_result(len(owned_dbs) == 1, "warning")
        r3_detail = ""
        if len(owned_dbs) == 0:
            r3_detail = "no database"
            r3 = "WARN"
        elif len(owned_dbs) > 1:
            r3_detail = f"multiple DBs: {owned_dbs}"
            r3 = "FAIL"

        # Rule 4: no JDBC between services
        jdbc_v = connected[sid]["jdbc_violations"]
        r4 = check_result(len(jdbc_v) == 0, "error")
        r4_detail = f"JDBC to: {jdbc_v}" if jdbc_v else ""

        # Rule 5: not orphaned (has at least one relationship)
        total_rels = sum(v for k, v in connected[sid].items() if k != "jdbc_violations")
        has_db_rel = len(owned_dbs) > 0
        r5 = check_result(total_rels > 0 or has_db_rel, "warning")

        # Rule 6: PCI scope declared if in PCI registry
        if sid in pci_services:
            r6 = check_result(pci_flag, "error")
        else:
            r6 = "N/A"

        results.append({
            "id": sid,
            "domain": domain or "—",
            "team": team or "—",
            "r1": r1,
            "r2": r2,
            "r3": r3,
            "r3_detail": r3_detail,
            "r4": r4,
            "r4_detail": r4_detail,
            "r5": r5,
            "r6": r6,
        })

    return results


def status_icon(status):
    return {"PASS": "✓", "FAIL": "✗", "WARN": "!", "N/A": "—"}.get(status, status)


def rule_summary(results, rule_key):
    counts = {"PASS": 0, "FAIL": 0, "WARN": 0, "N/A": 0}
    for r in results:
        s = r.get(rule_key, "N/A")
        counts[s] = counts.get(s, 0) + 1
    return counts


def write_governance_page(topology, pci_services):
    results = run_governance_checks(topology, pci_services)

    n_services = len(results)
    total_checks = sum(1 for r in results for k in ALL_RULES if r[k] != "N/A")
    total_pass = sum(1 for r in results for k in ALL_RULES if r[k] == "PASS")
    total_fail = sum(1 for r in results for k in ALL_RULES if r[k] == "FAIL")
    total_warn = sum(1 for r in results for k in ALL_RULES if r[k] == "WARN")

    content = """---
tags:
  - topology
  - governance
  - compliance
---

# Architecture Governance Dashboard

Auto-generated from the [CALM topology](../../calm/) — validates every service against the
[NovaTrek Organizational Architecture Standard](../../../architecture/calm/standards/novatrek-org-standard.json).

---

"""

    content += f"""## Compliance Summary

| Metric | Count |
|--------|-------|
| Services assessed | {n_services} |
| Total rule checks | {total_checks} |
| Passing | {total_pass} |
| Failing (error) | {total_fail} |
| Warnings | {total_warn} |

"""

    if total_fail == 0 and total_warn == 0:
        content += "All services are compliant with NovaTrek architecture governance rules.\n\n"
    elif total_fail == 0:
        content += f"No errors. {total_warn} warning(s) require attention.\n\n"
    else:
        content += f"{total_fail} error(s) and {total_warn} warning(s) require attention before merge.\n\n"

    content += "---\n\n"

    content += """## Governance Rules

| Rule | ID | Severity | Description |
|------|----|----------|-------------|
| Domain metadata | novatrek-003 | Error | Every service must declare its bounded context domain |
| Team metadata | novatrek-003 | Error | Every service must declare its owning team |
| Single database | novatrek-001 | Warning | Each service should own exactly one database |
| API-mediated access | novatrek-002 | Error | No JDBC connections between services |
| No orphan services | novatrek-003 | Warning | Every service should participate in at least one relationship |
| PCI scope | novatrek-004 | Error | PCI-scoped services must declare pci-in-scope: true |

---

## Per-Service Compliance

Legend: ✓ Pass | ✗ Fail | ! Warning | — Not applicable

| Service | Domain | R1 Domain | R2 Team | R3 Single DB | R4 API Only | R5 Connected | R6 PCI |
|---------|--------|-----------|---------|--------------|-------------|--------------|--------|
"""

    for r in results:
        link = svc_link(r["id"])
        r3_cell = status_icon(r["r3"])
        if r["r3_detail"]:
            r3_cell += f" ({r['r3_detail']})"
        r4_cell = status_icon(r["r4"])
        if r["r4_detail"]:
            r4_cell += f" ({r['r4_detail']})"

        content += (
            f"| {link} | {r['domain']} "
            f"| {status_icon(r['r1'])} "
            f"| {status_icon(r['r2'])} "
            f"| {r3_cell} "
            f"| {r4_cell} "
            f"| {status_icon(r['r5'])} "
            f"| {status_icon(r['r6'])} |\n"
        )

    content += "\n"

    # Failing services section (error severity only)
    failing = [r for r in results if any(r[k] == "FAIL" for k in ERROR_RULES)]
    # Warning services (warning severity only, excluding errors already captured)
    warnings = [r for r in results if any(r[k] == "WARN" for k in WARNING_RULES)]

    if failing:
        content += "---\n\n## Failures\n\n"
        for r in failing:
            content += f"### {r['id']}\n\n"
            if r["r1"] == "FAIL":
                content += "- **R1 Domain metadata**: missing — add `domain` field to metadata in `domains.yaml`\n"
            if r["r2"] == "FAIL":
                content += "- **R2 Team metadata**: missing — ensure service has a defined owning team\n"
            if r["r3"] == "FAIL":
                content += f"- **R3 Single database**: {r['r3_detail']} — shared databases violate bounded context rules (ADR-010)\n"
            if r["r4"] == "FAIL":
                content += f"- **R4 API-mediated access**: {r['r4_detail']} — replace JDBC cross-service connections with REST API calls\n"
            if r["r6"] == "FAIL":
                content += "- **R6 PCI scope**: service is in `pci.yaml` but missing `pci-in-scope: true` — update `generate-calm.py` PCI services list\n"
            content += "\n"

    if warnings:
        content += "---\n\n## Warnings\n\n"
        for r in warnings:
            if any(r[k] == "WARN" for k in WARNING_RULES):
                content += f"### {r['id']}\n\n"
                if r["r3"] == "WARN":
                    content += f"- **R3 Single database**: {r['r3_detail'] or 'check data-stores.yaml'}\n"
                if r["r5"] == "WARN":
                    content += "- **R5 Connected**: service appears to have no relationships — verify it is modelled in cross-service-calls.yaml\n"
                content += "\n"

    content += """---

## Data Source

Generated from `architecture/calm/novatrek-topology.json` by `portal/scripts/generate-governance-dashboard.py`.

Governance rules defined in `architecture/calm/standards/novatrek-org-standard.json`.

To regenerate:
```bash
python3 scripts/generate-calm.py
python3 portal/scripts/generate-governance-dashboard.py
```
"""

    path = OUTPUT_DIR / "governance.md"
    path.write_text(content, encoding="utf-8")
    print(f"  Generated {path.relative_to(WORKSPACE_ROOT)}")


def main():
    print("Generating governance dashboard from CALM data...")

    topology_path = CALM_DIR / "novatrek-topology.json"
    if not topology_path.exists():
        print(f"ERROR: {topology_path} not found. Run scripts/generate-calm.py first.")
        return

    topology = load_calm(topology_path)
    pci_services = load_pci_services()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    write_governance_page(topology, pci_services)
    print("Done.")


if __name__ == "__main__":
    main()
