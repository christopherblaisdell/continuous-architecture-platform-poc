#!/usr/bin/env python3
"""Generate Business Capability pages for the NovaTrek Architecture Portal.

Reads capabilities.yaml and capability-changelog.yaml to generate:
  - A capability map index page with L1 domain summaries and coverage stats
  - Per-domain sections with L2 capability detail and solution timeline

Usage:
    python3 portal/scripts/generate-capability-pages.py
"""

import os
import yaml

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
METADATA_DIR = os.path.join(WORKSPACE_ROOT, "architecture", "metadata")
OUTPUT_DIR = os.path.join(WORKSPACE_ROOT, "portal", "docs", "capabilities")


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def status_badge(status):
    """Return a text label for capability status."""
    mapping = {
        "implemented": "IMPLEMENTED",
        "partial": "PARTIAL",
        "not-implemented": "NOT IMPLEMENTED",
    }
    return mapping.get(status, status.upper())


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    caps_data = load_yaml(os.path.join(METADATA_DIR, "capabilities.yaml"))
    changelog_path = os.path.join(METADATA_DIR, "capability-changelog.yaml")
    changelog_data = load_yaml(changelog_path) if os.path.exists(changelog_path) else {}

    # Build changelog index: cap_id -> [entries]
    changelog_by_cap = {}
    for entry in changelog_data.get("entries", []):
        for cap in entry.get("capabilities", []):
            cap_id = cap["id"]
            if cap_id not in changelog_by_cap:
                changelog_by_cap[cap_id] = []
            changelog_by_cap[cap_id].append({
                "ticket": entry["ticket"],
                "date": str(entry.get("date", "")),
                "summary": entry.get("summary", ""),
                "solution": entry.get("solution", ""),
                "impact": cap.get("impact", ""),
                "description": cap.get("description", ""),
                "l3_capabilities": cap.get("l3_capabilities", []),
                "decisions": entry.get("decisions", []),
            })

    # Compute stats
    total_l2 = 0
    implemented = 0
    partial = 0
    not_impl = 0

    for domain in caps_data.get("domains", []):
        for cap in domain.get("capabilities", []):
            total_l2 += 1
            st = cap.get("status", "")
            if st == "implemented":
                implemented += 1
            elif st == "partial":
                partial += 1
            elif st == "not-implemented":
                not_impl += 1

    lines = []
    lines.append("---")
    lines.append("title: Business Capabilities")
    lines.append("description: NovaTrek Adventures business capability map with solution traceability")
    lines.append("---")
    lines.append("")
    lines.append("# Business Capability Map")
    lines.append("")
    lines.append("The capability map defines WHAT NovaTrek Adventures does as a business,")
    lines.append("independent of HOW services implement it. L1 domains group related capabilities.")
    lines.append("L2 capabilities map to services. L3 capabilities emerge from solution designs.")
    lines.append("")

    # Coverage summary
    pct = round(implemented / total_l2 * 100, 1) if total_l2 else 0
    lines.append("## Coverage Summary")
    lines.append("")
    lines.append("| Status | Count | Percentage |")
    lines.append("|--------|-------|-----------|")
    lines.append(f"| Implemented | {implemented} | {pct}% |")
    lines.append(f"| Partial | {partial} | {round(partial / total_l2 * 100, 1) if total_l2 else 0}% |")
    lines.append(f"| Not Implemented | {not_impl} | {round(not_impl / total_l2 * 100, 1) if total_l2 else 0}% |")
    lines.append(f"| **Total L2 Capabilities** | **{total_l2}** | |")
    lines.append("")

    # Domain overview table
    lines.append("## Domain Overview")
    lines.append("")
    lines.append("| Domain | L2 Capabilities | Implemented | Partial | Gaps |")
    lines.append("|--------|----------------|-------------|---------|------|")
    for domain in caps_data.get("domains", []):
        d_id = domain["id"]
        d_name = domain["name"]
        caps = domain.get("capabilities", [])
        d_impl = sum(1 for c in caps if c.get("status") == "implemented")
        d_part = sum(1 for c in caps if c.get("status") == "partial")
        d_gaps = sum(1 for c in caps if c.get("status") == "not-implemented")
        gap_names = [c["name"] for c in caps if c.get("status") == "not-implemented"]
        gap_str = ", ".join(gap_names) if gap_names else "—"
        lines.append(f"| {d_id} {d_name} | {len(caps)} | {d_impl} | {d_part} | {d_gaps} ({gap_str}) |" if d_gaps else
                      f"| {d_id} {d_name} | {len(caps)} | {d_impl} | {d_part} | 0 |")
    lines.append("")

    # Per-domain detail
    for domain in caps_data.get("domains", []):
        d_id = domain["id"]
        d_name = domain["name"]
        d_desc = domain.get("description", "")

        lines.append(f"## {d_id} {d_name}")
        lines.append("")
        if d_desc:
            lines.append(f"*{d_desc}*")
            lines.append("")

        for cap in domain.get("capabilities", []):
            c_id = cap["id"]
            c_name = cap["name"]
            c_status = status_badge(cap.get("status", ""))
            c_desc = cap.get("description", "")
            services = cap.get("services", [])

            lines.append(f"### {c_id} {c_name}")
            lines.append("")
            lines.append(f"**Status:** {c_status}")
            lines.append("")
            if c_desc:
                lines.append(c_desc)
                lines.append("")

            if services:
                svc_links = []
                for svc in services:
                    if svc.startswith("svc-"):
                        svc_links.append(f"[{svc}](../microservices/{svc}.md)")
                    else:
                        svc_links.append(svc)
                lines.append(f"**Services:** {', '.join(svc_links)}")
                lines.append("")

            if cap.get("status") == "not-implemented":
                if cap.get("priority"):
                    lines.append(f"**Priority:** {cap['priority'].upper()}")
                if cap.get("gap_rationale"):
                    lines.append(f"**Gap Rationale:** {cap['gap_rationale']}")
                lines.append("")

            # Solution timeline from changelog
            timeline = changelog_by_cap.get(c_id, [])
            if timeline:
                lines.append("#### Solution Timeline")
                lines.append("")
                lines.append("| Date | Ticket | Impact | Summary |")
                lines.append("|------|--------|--------|---------|")
                for entry in sorted(timeline, key=lambda x: x["date"]):
                    solution = entry.get("solution", "")
                    ticket = entry["ticket"]
                    if solution:
                        lines.append(f"| {entry['date']} | [{ticket}](../solutions/{solution}.md) | {entry['impact']} | {entry['summary']} |")
                    else:
                        lines.append(f"| {entry['date']} | {ticket} | {entry['impact']} | {entry['summary']} |")
                lines.append("")

                # L3 capabilities
                all_l3 = []
                for entry in timeline:
                    all_l3.extend(entry.get("l3_capabilities", []))
                if all_l3:
                    lines.append("#### Emergent L3 Capabilities")
                    lines.append("")
                    for l3 in all_l3:
                        lines.append(f"- **{l3['name']}** — {l3.get('description', '')}")
                    lines.append("")

    # Write the page
    with open(os.path.join(OUTPUT_DIR, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  Generated capability map page ({total_l2} L2 capabilities, {len(changelog_by_cap)} with history)")


if __name__ == "__main__":
    main()
