#!/usr/bin/env python3
"""Mock JIRA Client - Simulates querying JIRA tickets for NovaTrek Architecture Practice.

This script provides a synthetic JIRA API client that loads ticket data from
a local JSON file and outputs formatted reports. Used for testing AI coding
assistants in a controlled environment.

Usage:
    # Get a specific ticket
    python mock-jira-client.py --ticket NTK-10002

    # List all tickets
    python mock-jira-client.py --list

    # List tickets filtered by status
    python mock-jira-client.py --list --status "New,In Progress"

    # List tickets filtered by priority
    python mock-jira-client.py --list --priority "Critical,High"

Requires: Python 3.10+ (stdlib only, no external dependencies)
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# Resolve mock data path relative to this script
MOCK_DATA_DIR = Path(__file__).parent / "mock-data"
TICKETS_FILE = MOCK_DATA_DIR / "tickets.json"


def load_tickets() -> list[dict]:
    """Load ticket data from the mock-data JSON file."""
    if not TICKETS_FILE.exists():
        print(f"ERROR: Mock data file not found: {TICKETS_FILE}", file=sys.stderr)
        sys.exit(1)
    with open(TICKETS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def format_ticket_detail(ticket: dict) -> str:
    """Format a single ticket as a detailed report (similar to real JIRA API output)."""
    border = "=" * 72
    created = _format_timestamp(ticket.get("created", ""))
    updated = _format_timestamp(ticket.get("updated", ""))
    labels = ", ".join(ticket.get("labels", []))

    lines = [
        border,
        f"  Ticket:     {ticket['key']}",
        f"  Summary:    {ticket['summary']}",
        border,
        f"  Status:     {ticket['status']}",
        f"  Priority:   {ticket['priority']}",
        f"  Assignee:   {ticket.get('assignee', 'Unassigned')}",
        f"  Reporter:   {ticket.get('reporter', 'Unknown')}",
        f"  Sprint:     {ticket.get('sprint', 'Backlog')}",
        f"  Labels:     {labels}",
        f"  Created:    {created}",
        f"  Updated:    {updated}",
        f"  Comments:   {ticket.get('comments_count', 0)}",
        "",
        "  Description:",
        _indent_text(ticket.get("description", "(No description)"), 4),
        border,
    ]
    return "\n".join(lines)


def format_ticket_row(ticket: dict) -> str:
    """Format a single ticket as a table row."""
    key = ticket["key"].ljust(12)
    status = ticket["status"].ljust(16)
    priority = ticket["priority"].ljust(10)
    assignee = (ticket.get("assignee") or "Unassigned").ljust(18)
    summary = ticket["summary"][:50]
    return f"  {key}{status}{priority}{assignee}{summary}"


def print_ticket_table(tickets: list[dict]) -> None:
    """Print a formatted table of tickets."""
    if not tickets:
        print("  No tickets found matching the given filters.")
        return

    header_border = "-" * 110
    header = (
        f"  {'Key'.ljust(12)}{'Status'.ljust(16)}{'Priority'.ljust(10)}"
        f"{'Assignee'.ljust(18)}{'Summary'}"
    )

    print(f"\n  JIRA Tickets ({len(tickets)} results)")
    print(header_border)
    print(header)
    print(header_border)
    for ticket in tickets:
        print(format_ticket_row(ticket))
    print(header_border)
    print()


def filter_tickets(
    tickets: list,
    statuses: Optional[list] = None,
    priorities: Optional[list] = None,
) -> list:
    """Filter tickets by status and/or priority (case-insensitive)."""
    result = tickets
    if statuses:
        status_lower = [s.strip().lower() for s in statuses]
        result = [t for t in result if t["status"].lower() in status_lower]
    if priorities:
        priority_lower = [p.strip().lower() for p in priorities]
        result = [t for t in result if t["priority"].lower() in priority_lower]
    return result


def _format_timestamp(iso_str: str) -> str:
    """Convert ISO timestamp to a human-readable format."""
    if not iso_str:
        return "N/A"
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M UTC")
    except ValueError:
        return iso_str


def _indent_text(text: str, spaces: int) -> str:
    """Indent each line of text by a number of spaces."""
    prefix = " " * spaces
    return "\n".join(f"{prefix}{line}" for line in text.splitlines())


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser with help text."""
    parser = argparse.ArgumentParser(
        prog="mock-jira-client.py",
        description="Mock JIRA Client - Query synthetic JIRA tickets for architecture analysis.",
        epilog="Examples:\n"
               "  python mock-jira-client.py --ticket NTK-10002\n"
               "  python mock-jira-client.py --list --status 'New,In Progress'\n"
               "  python mock-jira-client.py --list --priority Critical",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ticket", metavar="ID", help="Get details for a specific ticket (e.g., NTK-10002)")
    group.add_argument("--list", action="store_true", help="List all tickets (optionally filtered)")
    parser.add_argument("--status", metavar="FILTER", help='Comma-separated status filter (e.g., "New,In Progress")')
    parser.add_argument("--priority", metavar="FILTER", help='Comma-separated priority filter (e.g., "Critical,High")')
    return parser


def main() -> None:
    """Entry point for the mock JIRA client."""
    parser = build_parser()
    args = parser.parse_args()

    tickets = load_tickets()

    if args.ticket:
        # Find the specific ticket
        matches = [t for t in tickets if t["key"].upper() == args.ticket.upper()]
        if not matches:
            print(f"ERROR: Ticket '{args.ticket}' not found in mock data.", file=sys.stderr)
            sys.exit(1)
        print(format_ticket_detail(matches[0]))
    elif args.list:
        # Parse filters
        statuses = args.status.split(",") if args.status else None
        priorities = args.priority.split(",") if args.priority else None
        filtered = filter_tickets(tickets, statuses=statuses, priorities=priorities)
        print_ticket_table(filtered)


if __name__ == "__main__":
    main()
