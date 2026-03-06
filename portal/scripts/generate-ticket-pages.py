#!/usr/bin/env python3
"""Generate Ticket (User Story) pages for the NovaTrek Architecture Portal.

Reads tickets.yaml and generates:
  - An index page listing all tickets with status, priority, and capability mapping
  - Per-ticket detail pages with user stories, services, and cross-links

Usage:
    python3 portal/scripts/generate-ticket-pages.py
"""

import os
import yaml

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
METADATA_DIR = os.path.join(WORKSPACE_ROOT, "architecture", "metadata")
OUTPUT_DIR = os.path.join(WORKSPACE_ROOT, "portal", "docs", "tickets")


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def priority_sort_key(priority):
    order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    return order.get(priority, 9)


def generate_ticket_page(ticket):
    """Generate a per-ticket Markdown page."""
    key = ticket["key"]
    summary = ticket.get("summary", "")
    status = ticket.get("status", "")
    priority = ticket.get("priority", "")
    assignee = ticket.get("assignee") or "Unassigned"
    reporter = ticket.get("reporter", "")
    components = ticket.get("components", [])
    capabilities = ticket.get("capabilities", [])
    decisions = ticket.get("decisions", [])
    user_story = ticket.get("user_story", "").strip()
    solution = ticket.get("solution")
    new_services = ticket.get("new_services", [])
    labels = ticket.get("labels", [])

    lines = []
    lines.append("---")
    lines.append(f"title: \"{key} — {summary}\"")
    lines.append(f"description: \"{summary}\"")
    lines.append("---")
    lines.append("")
    lines.append(f"# {key} — {summary}")
    lines.append("")

    # Metadata table
    lines.append("| Field | Value |")
    lines.append("|-------|-------|")
    lines.append(f"| **Status** | {status} |")
    lines.append(f"| **Priority** | {priority} |")
    lines.append(f"| **Assignee** | {assignee} |")
    lines.append(f"| **Reporter** | {reporter} |")
    if ticket.get("sprint"):
        lines.append(f"| **Sprint** | {ticket['sprint']} |")
    if ticket.get("created"):
        lines.append(f"| **Created** | {ticket['created']} |")
    if ticket.get("updated"):
        lines.append(f"| **Updated** | {ticket['updated']} |")
    lines.append("")

    # User story
    if user_story:
        lines.append("## User Story")
        lines.append("")
        lines.append(f"> {user_story.replace(chr(10), chr(10) + '> ')}")
        lines.append("")

    # Solution link
    if solution:
        lines.append("## Solution Design")
        lines.append("")
        lines.append(f"[View Solution Design](../solutions/{solution}.md)")
        lines.append("")

    # Capabilities
    if capabilities:
        lines.append("## Affected Capabilities")
        lines.append("")
        lines.append("| Capability | Impact |")
        lines.append("|-----------|--------|")
        for cap in capabilities:
            cap_id = cap["id"]
            impact = cap.get("impact", "")
            lines.append(f"| [{cap_id}](../capabilities/index.md#{cap_id.lower().replace('.', '')}) | {impact} |")
        lines.append("")

    # Components / Services
    if components:
        lines.append("## Affected Services")
        lines.append("")
        for svc in components:
            if svc.startswith("svc-"):
                lines.append(f"- [{svc}](../microservices/{svc}.md)")
            else:
                lines.append(f"- {svc}")
        lines.append("")

    # New services
    if new_services:
        lines.append("## New Services Required")
        lines.append("")
        for svc in new_services:
            lines.append(f"- **{svc}**")
        lines.append("")

    # Decisions
    if decisions:
        lines.append("## Architecture Decisions")
        lines.append("")
        for dec in decisions:
            lines.append(f"- {dec}")
        lines.append("")

    # Labels
    if labels:
        lines.append("## Labels")
        lines.append("")
        lines.append(", ".join(f"`{l}`" for l in labels))
        lines.append("")

    return "\n".join(lines)


def generate_index_page(tickets):
    """Generate the tickets index page."""
    lines = []
    lines.append("---")
    lines.append("title: User Stories and Tickets")
    lines.append("description: NovaTrek Adventures architecture ticket registry")
    lines.append("---")
    lines.append("")
    lines.append("# User Stories and Tickets")
    lines.append("")
    lines.append("Architecture ticket registry with capability traceability.")
    lines.append("Each ticket tracks affected services, capabilities, and links to its solution design.")
    lines.append("")

    # Summary stats
    total = len(tickets)
    with_solution = sum(1 for t in tickets if t.get("solution"))
    lines.append(f"**{total}** tickets | **{with_solution}** with solution designs")
    lines.append("")

    # By priority grouping
    for priority_label in ["Critical", "High", "Medium", "Low"]:
        group = [t for t in tickets if t.get("priority", "") == priority_label]
        if not group:
            continue

        lines.append(f"## {priority_label} Priority")
        lines.append("")
        lines.append("| Ticket | Summary | Status | Capabilities | Solution |")
        lines.append("|--------|---------|--------|-------------|----------|")
        for t in group:
            key = t["key"]
            summary = t.get("summary", "")[:55]
            status = t.get("status", "")
            caps = ", ".join(c["id"] for c in t.get("capabilities", []))
            sol = "[View](../solutions/{}.md)".format(t["solution"]) if t.get("solution") else "—"
            lines.append(f"| [{key}]({key}.md) | {summary} | {status} | {caps} | {sol} |")
        lines.append("")

    return "\n".join(lines)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    tickets_data = load_yaml(os.path.join(METADATA_DIR, "tickets.yaml"))
    tickets = tickets_data.get("tickets", [])

    # Generate index
    index_content = generate_index_page(tickets)
    with open(os.path.join(OUTPUT_DIR, "index.md"), "w", encoding="utf-8") as f:
        f.write(index_content)

    # Generate per-ticket pages
    for ticket in tickets:
        page_content = generate_ticket_page(ticket)
        page_path = os.path.join(OUTPUT_DIR, f"{ticket['key']}.md")
        with open(page_path, "w", encoding="utf-8") as f:
            f.write(page_content)

    print(f"  Generated {len(tickets)} ticket pages + index in portal/docs/tickets/")


if __name__ == "__main__":
    main()
