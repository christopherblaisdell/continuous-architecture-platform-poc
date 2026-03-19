#!/usr/bin/env python3
"""Generate Solution Design pages for the NovaTrek Architecture Portal.

Reads solution design folders from architecture/solutions/ and generates:
  - An index page listing all solutions with status, capabilities, and services
  - Per-solution pages with the master document content and cross-links

Capability mappings are derived from capability-changelog.yaml (single source
of truth), NOT from solution capabilities.md files.

Usage:
    python3 portal/scripts/generate-solution-pages.py
"""

import os
import re
import yaml

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SOLUTIONS_DIR = os.path.join(WORKSPACE_ROOT, "architecture", "solutions")
METADATA_DIR = os.path.join(WORKSPACE_ROOT, "architecture", "metadata")
OUTPUT_DIR = os.path.join(WORKSPACE_ROOT, "portal", "docs", "solutions")


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def heading_slug(text):
    """Reproduce MkDocs heading anchor generation."""
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9 -]", "", slug)
    slug = slug.replace(" ", "-")
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def build_cap_names(caps_data):
    """Build a lookup dict: cap_id -> cap_name from capabilities.yaml."""
    names = {}
    for domain in caps_data.get("domains", []):
        for cap in domain.get("capabilities", []):
            names[cap["id"]] = cap.get("name", "")
    return names


def build_changelog_index(changelog_data):
    """Build lookup dicts from capability-changelog.yaml.

    Returns:
        by_solution: {solution_folder: [{"id": ..., "impact": ..., "description": ...}]}
        decisions_by_solution: {solution_folder: [ADR-xxx, ...]}
    """
    by_solution = {}
    decisions_by_solution = {}
    for entry in changelog_data.get("entries", []):
        sol = entry.get("solution", "")
        if not sol:
            continue
        if sol not in by_solution:
            by_solution[sol] = []
            decisions_by_solution[sol] = []
        for cap in entry.get("capabilities", []):
            by_solution[sol].append({
                "id": cap["id"],
                "impact": cap.get("impact", ""),
                "description": cap.get("description", ""),
            })
        for dec in entry.get("decisions", []):
            if dec not in decisions_by_solution[sol]:
                decisions_by_solution[sol].append(dec)
    return by_solution, decisions_by_solution


def parse_solution_metadata(solution_dir, changelog_caps):
    """Extract metadata from a solution folder."""
    folder_name = os.path.basename(solution_dir)

    # Extract ticket ID from folder name: _NTK-XXXXX-slug
    ticket_match = re.match(r"_?(NTK-\d+)", folder_name)
    ticket_id = ticket_match.group(1) if ticket_match else folder_name

    # Find master document
    master_content = ""
    for f in os.listdir(solution_dir):
        if f.endswith("-solution-design.md"):
            with open(os.path.join(solution_dir, f), encoding="utf-8") as fh:
                master_content = fh.read()
            break

    if not master_content:
        return None

    # Parse header table from master doc
    meta = {
        "ticket_id": ticket_id,
        "folder": folder_name,
        "title": "",
        "version": "",
        "status": "",
        "author": "",
        "date": "",
    }

    # Extract title from first H1
    title_match = re.search(r"^#\s+(.+)$", master_content, re.MULTILINE)
    if title_match:
        meta["title"] = title_match.group(1).strip()
        # Remove ticket prefix from title for display
        meta["title"] = re.sub(r"^NTK-\d+\s*[-—]\s*", "", meta["title"])
        meta["title"] = re.sub(r"^Solution Design:\s*", "", meta["title"])

    # Parse header table fields
    for line in master_content.split("\n"):
        line_lower = line.lower()
        if "| version" in line_lower or "| version" in line_lower:
            parts = line.split("|")
            if len(parts) >= 3:
                meta["version"] = parts[2].strip()
        elif "| status" in line_lower:
            parts = line.split("|")
            if len(parts) >= 3:
                meta["status"] = parts[2].strip()
        elif "| author" in line_lower:
            parts = line.split("|")
            if len(parts) >= 3:
                meta["author"] = parts[2].strip()
        elif "| date" in line_lower or "| last updated" in line_lower:
            parts = line.split("|")
            if len(parts) >= 3:
                meta["date"] = parts[2].strip()

    # Capabilities from changelog (single source of truth)
    meta["capabilities"] = changelog_caps.get(folder_name, [])

    # Detect available sections
    meta["has_requirements"] = os.path.isdir(os.path.join(solution_dir, "1.requirements"))
    meta["has_analysis"] = os.path.isdir(os.path.join(solution_dir, "2.analysis"))
    meta["has_decisions"] = os.path.exists(os.path.join(solution_dir, "3.solution", "d.decisions", "decisions.md"))
    meta["has_impacts"] = os.path.isdir(os.path.join(solution_dir, "3.solution", "i.impacts"))
    meta["has_user_stories"] = os.path.exists(os.path.join(solution_dir, "3.solution", "u.user.stories", "user-stories.md"))
    meta["has_guidance"] = os.path.exists(os.path.join(solution_dir, "3.solution", "g.guidance", "guidance.md"))
    meta["has_risks"] = os.path.exists(os.path.join(solution_dir, "3.solution", "r.risks", "risks.md"))

    # Count impact files
    impacts_dir = os.path.join(solution_dir, "3.solution", "i.impacts")
    meta["impact_count"] = 0
    if os.path.isdir(impacts_dir):
        meta["impact_count"] = sum(1 for d in os.listdir(impacts_dir) if d.startswith("impact."))

    meta["master_content"] = master_content

    return meta


def find_related_services(meta, tickets_data):
    """Find services from tickets.yaml for this solution."""
    if not tickets_data:
        return []
    for t in tickets_data.get("tickets", []):
        if t.get("key") == meta["ticket_id"]:
            return t.get("components", [])
    return []


def find_related_decisions(meta, changelog_decisions):
    """Find ADR references from capability-changelog.yaml."""
    return changelog_decisions.get(meta.get("folder", ""), [])


def find_related_solutions(meta, all_solutions, tickets_data):
    """Find related solutions by service or capability overlap."""
    my_folder = meta.get("folder", "")
    my_caps = set(c["id"] for c in meta.get("capabilities", []))
    my_services = set(find_related_services(meta, tickets_data))

    related = []
    for other in all_solutions:
        if other["folder"] == my_folder:
            continue
        other_caps = set(c["id"] for c in other.get("capabilities", []))
        other_services = set(find_related_services(other, tickets_data))

        shared_caps = my_caps & other_caps
        shared_svcs = my_services & other_services

        if shared_caps or shared_svcs:
            related.append({
                "ticket_id": other["ticket_id"],
                "title": other["title"],
                "folder": other["folder"],
                "shared_caps": sorted(shared_caps),
                "shared_services": sorted(shared_svcs),
            })

    return related


def generate_solution_page(meta, tickets_data, changelog_decisions, cap_names, all_solutions=None):
    """Generate a per-solution Markdown page."""
    services = find_related_services(meta, tickets_data)
    decisions = find_related_decisions(meta, changelog_decisions)

    lines = []
    lines.append("---")
    lines.append(f"title: \"{meta['ticket_id']} — {meta['title']}\"")
    lines.append(f"description: \"Solution design for {meta['ticket_id']}\"")
    lines.append("---")
    lines.append("")
    lines.append(f"# {meta['ticket_id']} — {meta['title']}")
    lines.append("")

    # Metadata card
    lines.append("| Field | Value |")
    lines.append("|-------|-------|")
    if meta["status"]:
        lines.append(f"| **Status** | {meta['status']} |")
    if meta["version"]:
        lines.append(f"| **Version** | {meta['version']} |")
    if meta["author"]:
        lines.append(f"| **Author** | {meta['author']} |")
    if meta["date"]:
        lines.append(f"| **Date** | {meta['date']} |")
    lines.append(f"| **Ticket** | {meta['ticket_id']} |")
    lines.append("")

    # Capabilities (from capability-changelog.yaml)
    if meta["capabilities"]:
        lines.append("## Affected Capabilities")
        lines.append("")
        lines.append("| Capability | Impact | Description |")
        lines.append("|-----------|--------|-------------|")
        for cap in meta["capabilities"]:
            cap_id = cap["id"]
            cap_name = cap_names.get(cap_id, "")
            cap_anchor = heading_slug(f"{cap_id} {cap_name}")
            desc = cap.get("description", "")
            display = f"{cap_id} {cap_name}" if cap_name else cap_id
            lines.append(f"| [{display}](../capabilities/index.md#{cap_anchor}) | {cap['impact']} | {desc} |")
        lines.append("")

    # Services
    if services:
        lines.append("## Affected Services")
        lines.append("")
        for svc in services:
            if svc.startswith("svc-"):
                lines.append(f"- [{svc}](../microservices/{svc}.md)")
            else:
                lines.append(f"- {svc}")
        lines.append("")

    # Decisions
    if decisions:
        lines.append("## Architecture Decisions")
        lines.append("")
        for dec in decisions:
            lines.append(f"- {dec}")
        lines.append("")

    # Solution contents inventory
    lines.append("## Solution Contents")
    lines.append("")
    sections = []
    if meta["has_requirements"]:
        sections.append("Requirements")
    if meta["has_analysis"]:
        sections.append("Analysis")
    if meta["has_decisions"]:
        sections.append("Decisions")
    if meta["has_impacts"]:
        sections.append(f"Impact Assessments ({meta['impact_count']})")
    if meta["has_user_stories"]:
        sections.append("User Stories")
    if meta["has_guidance"]:
        sections.append("Implementation Guidance")
    if meta["has_risks"]:
        sections.append("Risk Assessment")
    if meta["capabilities"]:
        sections.append("Capability Mapping")

    for s in sections:
        lines.append(f"- {s}")
    lines.append("")

    # Related Solutions (auto-detected by service or capability overlap)
    if all_solutions:
        related = find_related_solutions(meta, all_solutions, tickets_data)
        if related:
            lines.append("## Related Solutions")
            lines.append("")
            lines.append("Solutions that share services or capabilities with this design:")
            lines.append("")
            lines.append("| Solution | Shared Capabilities | Shared Services |")
            lines.append("|----------|-------------------|-----------------|")
            for r in related:
                caps_str = ", ".join(r["shared_caps"]) if r["shared_caps"] else "—"
                svcs_str = ", ".join(r["shared_services"]) if r["shared_services"] else "—"
                lines.append(f"| [{r['ticket_id']} — {r['title'][:40]}]({r['folder']}.md) | {caps_str} | {svcs_str} |")
            lines.append("")

    # Master document content (skip the header we already rendered)
    content = meta["master_content"]
    # Remove CONFLUENCE-PUBLISH comment
    content = re.sub(r"<!--\s*CONFLUENCE-PUBLISH\s*-->", "", content).strip()
    # Remove the first H1 and the header table (we rendered our own)
    # Find "## " which starts first real section
    section_start = content.find("\n## ")
    if section_start > 0:
        content = content[section_start:]

    lines.append("---")
    lines.append("")
    lines.append(content)

    return "\n".join(lines)


def generate_index_page(solutions, tickets_data, cap_names):
    """Generate the solution designs index page."""
    lines = []
    lines.append("---")
    lines.append("title: Solution Designs")
    lines.append("description: Architecture solution designs for NovaTrek Adventures")
    lines.append("---")
    lines.append("")
    lines.append("# Solution Designs")
    lines.append("")
    lines.append("Architecture solution designs produced through the continuous architecture workflow.")
    lines.append("Each solution maps business requirements to service changes with full capability traceability.")
    lines.append("")

    # Summary stats
    total = len(solutions)
    approved = sum(1 for s in solutions if "APPROVED" in s.get("status", "").upper())
    lines.append(f"**{total}** solution designs | **{approved}** approved")
    lines.append("")

    # Table
    lines.append("| Ticket | Solution | Status | Capabilities | Services |")
    lines.append("|--------|----------|--------|-------------|----------|")
    for s in sorted(solutions, key=lambda x: x["ticket_id"]):
        slug = s["folder"]
        title_short = s["title"][:50] + ("..." if len(s["title"]) > 50 else "")
        status = s.get("status", "—")
        caps = ", ".join(c["id"] for c in s.get("capabilities", []))
        services = find_related_services(s, tickets_data)
        svc_str = ", ".join(services[:3])
        if len(services) > 3:
            svc_str += f" (+{len(services) - 3})"
        lines.append(f"| {s['ticket_id']} | [{title_short}]({slug}.md) | {status} | {caps} | {svc_str} |")
    lines.append("")

    # Capability coverage
    all_caps = {}
    ticket_folder = {s["ticket_id"]: s["folder"] for s in solutions}
    for s in solutions:
        for c in s.get("capabilities", []):
            cap_id = c["id"]
            if cap_id not in all_caps:
                all_caps[cap_id] = []
            all_caps[cap_id].append(s["ticket_id"])

    if all_caps:
        lines.append("## Capability Coverage")
        lines.append("")
        lines.append("Capabilities shaped by solution designs:")
        lines.append("")
        lines.append("| Capability | Solutions |")
        lines.append("|-----------|----------")
        for cap_id in sorted(all_caps.keys()):
            cap_name = cap_names.get(cap_id, "")
            cap_anchor = heading_slug(f"{cap_id} {cap_name}")
            cap_display = f"{cap_id} {cap_name}" if cap_name else cap_id
            cap_link = f"[{cap_display}](../capabilities/index.md#{cap_anchor})"
            ticket_links = []
            for tid in all_caps[cap_id]:
                folder = ticket_folder.get(tid, "")
                if folder:
                    ticket_links.append(f"[{tid}]({folder}.md)")
                else:
                    ticket_links.append(tid)
            lines.append(f"| {cap_link} | {', '.join(ticket_links)} |")
        lines.append("")

    return "\n".join(lines)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load tickets for cross-referencing (services/components)
    tickets_path = os.path.join(METADATA_DIR, "tickets.yaml")
    tickets_data = load_yaml(tickets_path) if os.path.exists(tickets_path) else None

    # Load capability changelog (single source of truth for capability mappings)
    changelog_path = os.path.join(METADATA_DIR, "capability-changelog.yaml")
    changelog_data = load_yaml(changelog_path) if os.path.exists(changelog_path) else {}
    changelog_caps, changelog_decisions = build_changelog_index(changelog_data)

    # Load capability names for anchor generation
    caps_path = os.path.join(METADATA_DIR, "capabilities.yaml")
    caps_data = load_yaml(caps_path) if os.path.exists(caps_path) else {}
    cap_names = build_cap_names(caps_data)

    # Discover and parse solutions
    solutions = []
    if os.path.isdir(SOLUTIONS_DIR):
        for entry in sorted(os.listdir(SOLUTIONS_DIR)):
            sol_dir = os.path.join(SOLUTIONS_DIR, entry)
            if os.path.isdir(sol_dir) and entry.startswith("_NTK-"):
                meta = parse_solution_metadata(sol_dir, changelog_caps)
                if meta:
                    solutions.append(meta)

    # Generate index
    index_content = generate_index_page(solutions, tickets_data, cap_names)
    with open(os.path.join(OUTPUT_DIR, "index.md"), "w", encoding="utf-8") as f:
        f.write(index_content)

    # Generate per-solution pages
    for meta in solutions:
        page_content = generate_solution_page(meta, tickets_data, changelog_decisions, cap_names, all_solutions=solutions)
        page_path = os.path.join(OUTPUT_DIR, f"{meta['folder']}.md")
        with open(page_path, "w", encoding="utf-8") as f:
            f.write(page_content)

    print(f"  Generated {len(solutions)} solution pages + index in portal/docs/solutions/")


if __name__ == "__main__":
    main()
