#!/usr/bin/env python3
"""Mock GitLab Client - Simulates GitLab Merge Request analysis for NovaTrek Architecture Practice.

This script provides a synthetic GitLab API client that loads MR data from
a local JSON file and outputs formatted analysis reports. Used for testing
AI coding assistants in a controlled environment.

Usage:
    # Analyze a specific merge request
    python mock-gitlab-client.py --mr 5001

    # List all merge requests
    python mock-gitlab-client.py --list

    # List MRs filtered by status
    python mock-gitlab-client.py --list --status open

Requires: Python 3.10+ (stdlib only, no external dependencies)
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

# Resolve mock data path relative to this script
MOCK_DATA_DIR = Path(__file__).parent / "mock-data"
MR_FILE = MOCK_DATA_DIR / "merge-requests.json"


def load_merge_requests() -> list:
    """Load merge request data from the mock-data JSON file."""
    if not MR_FILE.exists():
        print(f"ERROR: Mock data file not found: {MR_FILE}", file=sys.stderr)
        sys.exit(1)
    with open(MR_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def format_mr_detail(mr: dict) -> str:
    """Format a single merge request as a detailed analysis report."""
    border = "=" * 72
    approvals = mr.get("approvals", {})
    approved_by = ", ".join(approvals.get("approved_by", [])) or "None"
    files = mr.get("changes", [])

    lines = [
        border,
        f"  Merge Request:  !{mr['id']}",
        f"  Title:          {mr['title']}",
        border,
        f"  Status:         {mr['status'].upper()}",
        f"  Author:         {mr['author']}",
        f"  Source Branch:  {mr['source_branch']}",
        f"  Target Branch:  {mr['target_branch']}",
        f"  Created:        {mr.get('created_at', 'N/A')}",
        f"  Updated:        {mr.get('updated_at', 'N/A')}",
        f"  Related Ticket: {mr.get('ticket_key', 'N/A')}",
        "",
        "  Approval Status:",
        f"    Required:     {approvals.get('required', 0)}",
        f"    Received:     {approvals.get('received', 0)}",
        f"    Approved By:  {approved_by}",
        "",
        f"  File Changes ({len(files)} files):",
        "  " + "-" * 68,
    ]

    for change in files:
        action = change.get("action", "modified").upper()
        adds = change.get("additions", 0)
        dels = change.get("deletions", 0)
        lines.append(f"    [{action:8s}] {change['path']}  (+{adds} / -{dels})")

    # Summary stats
    total_adds = sum(c.get("additions", 0) for c in files)
    total_dels = sum(c.get("deletions", 0) for c in files)
    lines.extend([
        "  " + "-" * 68,
        f"  Total: {len(files)} files changed, +{total_adds} additions, -{total_dels} deletions",
        border,
    ])
    return "\n".join(lines)


def format_mr_row(mr: dict) -> str:
    """Format a merge request as a summary table row."""
    mr_id = f"!{mr['id']}".ljust(8)
    status = mr["status"].upper().ljust(10)
    author = mr["author"].ljust(16)
    files = str(len(mr.get("changes", []))).ljust(6)
    title = mr["title"][:52]
    return f"  {mr_id}{status}{author}{files}{title}"


def print_mr_table(mrs: list) -> None:
    """Print a formatted table of merge requests."""
    if not mrs:
        print("  No merge requests found matching the given filters.")
        return

    header_border = "-" * 100
    header = (
        f"  {'MR'.ljust(8)}{'Status'.ljust(10)}{'Author'.ljust(16)}"
        f"{'Files'.ljust(6)}{'Title'}"
    )

    print(f"\n  GitLab Merge Requests ({len(mrs)} results)")
    print(header_border)
    print(header)
    print(header_border)
    for mr in mrs:
        print(format_mr_row(mr))
    print(header_border)
    print()


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser with help text."""
    parser = argparse.ArgumentParser(
        prog="mock-gitlab-client.py",
        description="Mock GitLab Client - Analyze synthetic merge requests for architecture review.",
        epilog="Examples:\n"
               "  python mock-gitlab-client.py --mr 5001\n"
               "  python mock-gitlab-client.py --list\n"
               "  python mock-gitlab-client.py --list --status open",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--mr", metavar="ID", type=int, help="Analyze a specific merge request by ID (e.g., 5001)")
    group.add_argument("--list", action="store_true", help="List all merge requests")
    parser.add_argument("--status", metavar="STATUS", help='Filter by status: open, merged, closed')
    return parser


def main() -> None:
    """Entry point for the mock GitLab client."""
    parser = build_parser()
    args = parser.parse_args()

    mrs = load_merge_requests()

    if args.mr:
        matches = [m for m in mrs if m["id"] == args.mr]
        if not matches:
            print(f"ERROR: Merge request !{args.mr} not found in mock data.", file=sys.stderr)
            sys.exit(1)
        print(format_mr_detail(matches[0]))
    elif args.list:
        if args.status:
            mrs = [m for m in mrs if m["status"].lower() == args.status.lower()]
        print_mr_table(mrs)


if __name__ == "__main__":
    main()
