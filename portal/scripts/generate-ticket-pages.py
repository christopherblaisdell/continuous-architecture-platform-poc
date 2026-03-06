#!/usr/bin/env python3
"""Generate Ticket (User Story) pages for the NovaTrek Architecture Portal.

Reads tickets.yaml and capability-changelog.yaml to generate:
  - An index page listing all tickets with status, priority, and capability mapping
  - Per-ticket detail pages with user stories, services, and cross-links

Capability mappings for solved tickets are derived from capability-changelog.yaml
(single source of truth). Unsolved tickets use planned_capabilities from tickets.yaml.

Usage:
    python3 portal/scripts/generate-ticket-pages.py
"""

import os
import yaml

import re


WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
METADATA_DIR = os.path.join(WORKSPACE_ROOT, "architecture", "metadata")
OUTPUT_DIR = os.path.join(WORKSPACE_ROOT, "portal", "docs", "tickets")


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


def build_changelog_by_ticket(changelog_data):
    """Build lookup dicts from capability-changelog.yaml indexed by ticket key.

    Returns:
        caps_by_ticket: {ticket_key: [{"id": ..., "impact": ..., "description": ...}]}
        decisions_by_ticket: {ticket_key: [ADR-xxx, ...]}
    """
    caps_by_ticket = {}
    decisions_by_ticket = {}
    for entry in changelog_data.get("entries", []):
        ticket = entry.get("ticket", "")
        if not ticket:
            continue
        if ticket not in caps_by_ticket:
            caps_by_ticket[ticket] = []
            decisions_by_ticket[ticket] = []
        for cap in entry.get("capabilities", []):
            caps_by_ticket[ticket].append({
                "id": cap["id"],
                "impact": cap.get("impact", ""),
                "description": cap.get("description", ""),
            })
        for dec in entry.get("decisions", []):
            if dec not in decisions_by_ticket[ticket]:
                decisions_by_ticket[ticket].append(dec)
    return caps_by_ticket, decisions_by_ticket


def get_ticket_capabilities(ticket, caps_by_ticket):
    """Get capabilities for a ticket: from changelog if solved, from planned_capabilities if not."""
    key = ticket["key"]
    if ticket.get("solution") and key in caps_by_ticket:
        return caps_by_ticket[key]
    # Unsolved tickets: use planned_capabilities
    return ticket.get("planned_capabilities", [])


def get_ticket_decisions(ticket, decisions_by_ticket):
    """Get decisions for a ticket from the changelog."""
    return decisions_by_ticket.get(ticket["key"], [])


def priority_sort_key(priority):
    order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    return order.get(priority, 9)


def generate_ticket_page(ticket, caps_by_ticket, decisions_by_ticket, cap_names):
    """Generate a per-ticket Markdown page."""
    key = ticket["key"]
    summary = ticket.get("summary", "")
    status = ticket.get("status", "")
    priority = ticket.get("priority", "")
    assignee = ticket.get("assignee") or "Unassigned"
    reporter = ticket.get("reporter", "")
    components = ticket.get("components", [])
    capabilities = get_ticket_capabilities(ticket, caps_by_ticket)
    decisions = get_ticket_decisions(ticket, decisions_by_ticket)
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
        is_planned = not ticket.get("solution")
        cap_label = "Planned Capabilities" if is_planned else "Affected Capabilities"
        lines.append(f"## {cap_label}")
        lines.append("")
        lines.append("| Capability | Impact |")
        lines.append("|-----------|--------|")
        for cap in capabilities:
            cap_id = cap["id"]
            cap_name = cap_names.get(cap_id, "")
            cap_anchor = heading_slug(f"{cap_id} {cap_name}")
            display = f"{cap_id} {cap_name}" if cap_name else cap_id
            impact = cap.get("impact", "")
            lines.append(f"| [{display}](../capabilities/index.md#{cap_anchor}) | {impact} |")
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


def generate_index_page(tickets, caps_by_ticket):
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
    lines.append("Capability mappings for solved tickets are derived from the")
    lines.append("[Capability Changelog](../capabilities/index.md) (single source of truth).")
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
            t_caps = get_ticket_capabilities(t, caps_by_ticket)
            caps = ", ".join(c["id"] for c in t_caps)
            sol = "[View](../solutions/{}.md)".format(t["solution"]) if t.get("solution") else "—"
            lines.append(f"| [{key}]({key}.md) | {summary} | {status} | {caps} | {sol} |")
        lines.append("")

    return "\n".join(lines)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    tickets_data = load_yaml(os.path.join(METADATA_DIR, "tickets.yaml"))
    tickets = tickets_data.get("tickets", [])

    # Load capability changelog (single source of truth for solved tickets)
    changelog_path = os.path.join(METADATA_DIR, "capability-changelog.yaml")
    changelog_data = load_yaml(changelog_path) if os.path.exists(changelog_path) else {}
    caps_by_ticket, decisions_by_ticket = build_changelog_by_ticket(changelog_data)

    # Load capability names for anchor generation
    caps_path = os.path.join(METADATA_DIR, "capabilities.yaml")
    caps_data = load_yaml(caps_path) if os.path.exists(caps_path) else {}
    cap_names = build_cap_names(caps_data)

    # Generate index
    index_content = generate_index_page(tickets, caps_by_ticket)
    with open(os.path.join(OUTPUT_DIR, "index.md"), "w", encoding="utf-8") as f:
        f.write(index_content)

    # Generate per-ticket pages
    for ticket in tickets:
        page_content = generate_ticket_page(ticket, caps_by_ticket, decisions_by_ticket, cap_names)
        page_path = os.path.join(OUTPUT_DIR, f"{ticket['key']}.md")
        with open(page_path, "w", encoding="utf-8") as f:
            f.write(page_content)

    print(f"  Generated {len(tickets)} ticket pages + index in portal/docs/tickets/")


if __name__ == "__main__":
    main()
