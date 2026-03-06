#!/usr/bin/env python3
"""
NovaTrek ticket-client.py — YAML-based ticket query CLI.

Reads architecture/metadata/tickets.yaml and supports filtering by
capability, service, status, priority, and free-text search.

Usage:
    python3 scripts/ticket-client.py --list
    python3 scripts/ticket-client.py --list --status "New"
    python3 scripts/ticket-client.py --list --capability CAP-2.1
    python3 scripts/ticket-client.py --list --service svc-check-in
    python3 scripts/ticket-client.py --list --priority Critical
    python3 scripts/ticket-client.py --list --query "wristband"
    python3 scripts/ticket-client.py --ticket NTK-10003
"""

import argparse
import os
import sys

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def find_tickets_file():
    """Locate tickets.yaml relative to the script or workspace root."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(script_dir, "..", "architecture", "metadata", "tickets.yaml"),
        os.path.join(os.getcwd(), "architecture", "metadata", "tickets.yaml"),
    ]
    for path in candidates:
        resolved = os.path.normpath(path)
        if os.path.isfile(resolved):
            return resolved
    print("ERROR: Could not find architecture/metadata/tickets.yaml", file=sys.stderr)
    sys.exit(1)


def load_tickets(path):
    """Load and return the tickets list from YAML."""
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("tickets", [])


def filter_tickets(tickets, status=None, capability=None, service=None, priority=None, query=None):
    """Apply filters to the ticket list."""
    results = tickets

    if status:
        status_lower = status.lower()
        results = [t for t in results if t.get("status", "").lower() == status_lower]

    if priority:
        priority_lower = priority.lower()
        results = [t for t in results if t.get("priority", "").lower() == priority_lower]

    if capability:
        cap_upper = capability.upper()
        results = [
            t for t in results
            if any(c.get("id", "").upper() == cap_upper for c in t.get("capabilities", []))
        ]

    if service:
        svc_lower = service.lower()
        results = [
            t for t in results
            if svc_lower in [c.lower() for c in t.get("components", [])]
        ]

    if query:
        query_lower = query.lower()
        results = [
            t for t in results
            if query_lower in t.get("summary", "").lower()
            or query_lower in t.get("key", "").lower()
            or query_lower in (t.get("user_story") or "").lower()
            or any(query_lower in label.lower() for label in t.get("labels", []))
        ]

    return results


def print_ticket_list(tickets):
    """Print a summary table of tickets."""
    if not tickets:
        print("No tickets found.")
        return

    # Header
    print(f"{'Key':<12} {'Priority':<10} {'Status':<16} {'Summary'}")
    print("-" * 80)

    for t in tickets:
        key = t.get("key", "")
        priority = t.get("priority", "")
        status = t.get("status", "")
        summary = t.get("summary", "")
        print(f"{key:<12} {priority:<10} {status:<16} {summary}")

    print(f"\n{len(tickets)} ticket(s) found.")


def print_ticket_detail(ticket):
    """Print full detail for a single ticket."""
    print(f"Key:        {ticket.get('key', '')}")
    print(f"Summary:    {ticket.get('summary', '')}")
    print(f"Status:     {ticket.get('status', '')}")
    print(f"Priority:   {ticket.get('priority', '')}")
    print(f"Assignee:   {ticket.get('assignee') or 'Unassigned'}")
    print(f"Reporter:   {ticket.get('reporter', '')}")
    print(f"Sprint:     {ticket.get('sprint') or 'Backlog'}")
    print(f"Created:    {ticket.get('created', '')}")
    print(f"Updated:    {ticket.get('updated', '')}")

    components = ticket.get("components", [])
    if components:
        print(f"Components: {', '.join(components)}")

    labels = ticket.get("labels", [])
    if labels:
        print(f"Labels:     {', '.join(labels)}")

    solution = ticket.get("solution")
    if solution:
        print(f"Solution:   architecture/solutions/{solution}/")

    capabilities = ticket.get("capabilities", [])
    if capabilities:
        print("\nCapabilities:")
        for cap in capabilities:
            print(f"  - {cap.get('id', '')} ({cap.get('impact', '')})")

    decisions = ticket.get("decisions", [])
    if decisions:
        print(f"\nDecisions:  {', '.join(decisions)}")

    new_services = ticket.get("new_services", [])
    if new_services:
        print(f"\nNew Services: {', '.join(new_services)}")

    user_story = ticket.get("user_story", "").strip()
    if user_story:
        print("\nUser Story:")
        for line in user_story.split("\n"):
            print(f"  {line}")


def main():
    parser = argparse.ArgumentParser(
        description="NovaTrek ticket query CLI (reads architecture/metadata/tickets.yaml)"
    )
    parser.add_argument("--list", action="store_true", help="List tickets (with optional filters)")
    parser.add_argument("--ticket", type=str, help="Show detail for a specific ticket (e.g., NTK-10003)")
    parser.add_argument("--status", type=str, help="Filter by status (e.g., New, 'In Progress', 'Ready for Dev')")
    parser.add_argument("--capability", type=str, help="Filter by capability ID (e.g., CAP-2.1)")
    parser.add_argument("--service", type=str, help="Filter by service component (e.g., svc-check-in)")
    parser.add_argument("--priority", type=str, help="Filter by priority (Critical, High, Medium, Low)")
    parser.add_argument("--query", type=str, help="Free-text search across summary, labels, user story")

    args = parser.parse_args()

    if not args.list and not args.ticket:
        parser.print_help()
        sys.exit(1)

    tickets_path = find_tickets_file()
    tickets = load_tickets(tickets_path)

    if args.ticket:
        ticket_key = args.ticket.upper()
        match = next((t for t in tickets if t.get("key", "").upper() == ticket_key), None)
        if match:
            print_ticket_detail(match)
        else:
            print(f"Ticket {ticket_key} not found.", file=sys.stderr)
            sys.exit(1)
    elif args.list:
        filtered = filter_tickets(
            tickets,
            status=args.status,
            capability=args.capability,
            service=args.service,
            priority=args.priority,
            query=args.query,
        )
        print_ticket_list(filtered)


if __name__ == "__main__":
    main()
