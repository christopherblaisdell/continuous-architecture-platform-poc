#!/usr/bin/env python3
"""Seed Vikunja with NovaTrek project, capability labels, and tickets.

Reads from architecture/metadata/tickets.yaml and capabilities.yaml to create:
  1. A "NovaTrek Adventures" project
  2. Labels for each L2 capability (e.g., "CAP-1.1: Guest Identity")
  3. Labels for priority levels and statuses
  4. Tasks for each ticket with capability label associations

Prerequisites:
  - Vikunja instance running and accessible
  - API token created via Vikunja UI (Settings > API Tokens)

Usage:
    export VIKUNJA_URL="https://ca-vikunja-prod.<env>.azurecontainerapps.io"
    export VIKUNJA_TOKEN="your-api-token"
    python3 scripts/vikunja-seed.py [--dry-run]
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
TICKETS_PATH = os.path.join(REPO_ROOT, "architecture", "metadata", "tickets.yaml")
CAPABILITIES_PATH = os.path.join(REPO_ROOT, "architecture", "metadata", "capabilities.yaml")

# Vikunja priority mapping (1=low, 2=medium, 3=high, 4=urgent, 5=do first)
PRIORITY_MAP = {
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "Critical": 4,
}

# Label colors for capability domains
DOMAIN_COLORS = {
    "CAP-1": "4fc3f7",  # Guest Experience — light blue
    "CAP-2": "81c784",  # Operations — green
    "CAP-3": "ffb74d",  # Business Support — orange
    "CAP-4": "e57373",  # Safety and Compliance — red
    "CAP-5": "ba68c8",  # Platform Infrastructure — purple
}


def api_request(base_url, token, method, path, data=None):
    """Make an authenticated request to the Vikunja API."""
    url = f"{base_url}/api/v1{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.readable() else ""
        print(f"  API Error: {method} {path} -> {e.code}: {error_body}", file=sys.stderr)
        raise


def load_capabilities():
    """Load L2 capabilities from capabilities.yaml."""
    with open(CAPABILITIES_PATH, "r") as f:
        data = yaml.safe_load(f)

    capabilities = []
    for domain in data.get("domains", []):
        domain_id = domain["id"]
        for cap in domain.get("capabilities", []):
            capabilities.append({
                "id": cap["id"],
                "name": cap["name"],
                "domain_id": domain_id,
                "domain_name": domain["name"],
            })
    return capabilities


def load_tickets():
    """Load tickets from tickets.yaml."""
    with open(TICKETS_PATH, "r") as f:
        data = yaml.safe_load(f)
    return data.get("tickets", [])


def create_project(base_url, token, dry_run):
    """Create the NovaTrek Adventures project."""
    project_data = {
        "title": "NovaTrek Adventures",
        "description": "Architecture ticket tracking for NovaTrek Adventures platform. Source of truth: architecture/metadata/tickets.yaml",
    }

    if dry_run:
        print("  [DRY RUN] Would create project: NovaTrek Adventures")
        return {"id": 0}

    result = api_request(base_url, token, "PUT", "/projects", project_data)
    print(f"  Created project: NovaTrek Adventures (id={result['id']})")
    return result


def create_labels(base_url, token, capabilities, dry_run):
    """Create labels for capabilities, priorities, and statuses."""
    labels = {}

    # Capability labels
    for cap in capabilities:
        domain_id = cap["domain_id"]
        color = DOMAIN_COLORS.get(domain_id, "9e9e9e")
        label_title = f"{cap['id']}: {cap['name']}"

        if dry_run:
            print(f"  [DRY RUN] Would create label: {label_title} (#{color})")
            labels[cap["id"]] = {"id": 0, "title": label_title}
            continue

        result = api_request(base_url, token, "PUT", "/labels", {
            "title": label_title,
            "hex_color": color,
        })
        labels[cap["id"]] = result
        print(f"  Created label: {label_title} (id={result['id']})")

    # Status labels
    status_colors = {
        "New": "90caf9",
        "In Progress": "fff176",
        "Ready for Dev": "a5d6a7",
        "Closed": "bdbdbd",
    }
    for status, color in status_colors.items():
        label_title = f"Status: {status}"
        if dry_run:
            print(f"  [DRY RUN] Would create label: {label_title}")
            labels[f"status:{status}"] = {"id": 0, "title": label_title}
            continue

        result = api_request(base_url, token, "PUT", "/labels", {
            "title": label_title,
            "hex_color": color,
        })
        labels[f"status:{status}"] = result
        print(f"  Created label: {label_title} (id={result['id']})")

    return labels


def import_tickets(base_url, token, project_id, tickets, labels, dry_run):
    """Import tickets as Vikunja tasks."""
    created = 0

    for ticket in tickets:
        key = ticket["key"]
        summary = ticket["summary"]
        priority = PRIORITY_MAP.get(ticket.get("priority", "Medium"), 2)

        # Build description
        desc_parts = [f"**Ticket:** {key}"]
        if ticket.get("user_story"):
            desc_parts.append(f"\n**User Story:**\n{ticket['user_story'].strip()}")
        if ticket.get("components"):
            desc_parts.append(f"\n**Components:** {', '.join(ticket['components'])}")
        if ticket.get("solution"):
            desc_parts.append(f"\n**Solution:** {ticket['solution']}")
        description = "\n".join(desc_parts)

        task_data = {
            "title": f"[{key}] {summary}",
            "description": description,
            "priority": priority,
        }

        if dry_run:
            print(f"  [DRY RUN] Would create task: [{key}] {summary}")
            created += 1
            continue

        result = api_request(base_url, token, "PUT", f"/projects/{project_id}/tasks", task_data)
        task_id = result["id"]
        print(f"  Created task: [{key}] {summary} (id={task_id})")

        # Assign capability labels
        if ticket.get("labels"):
            for label_tag in ticket["labels"]:
                # Check if any capability label matches
                for cap_id, label_data in labels.items():
                    if cap_id.startswith("CAP-") and cap_id.lower().replace("-", "").replace(".", "") in label_tag.lower().replace("-", "").replace(".", ""):
                        try:
                            api_request(base_url, token, "PUT", f"/tasks/{task_id}/labels", {
                                "label_id": label_data["id"],
                            })
                        except urllib.error.HTTPError:
                            pass  # Label assignment failure is non-critical

        # Assign status label
        status = ticket.get("status", "New")
        status_key = f"status:{status}"
        if status_key in labels:
            try:
                api_request(base_url, token, "PUT", f"/tasks/{task_id}/labels", {
                    "label_id": labels[status_key]["id"],
                })
            except urllib.error.HTTPError:
                pass

        created += 1

    return created


def main():
    parser = argparse.ArgumentParser(description="Seed Vikunja with NovaTrek ticket data")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be created without making API calls")
    args = parser.parse_args()

    base_url = os.environ.get("VIKUNJA_URL", "").rstrip("/")
    token = os.environ.get("VIKUNJA_TOKEN", "")

    if not args.dry_run and (not base_url or not token):
        print("ERROR: Set VIKUNJA_URL and VIKUNJA_TOKEN environment variables", file=sys.stderr)
        print("  export VIKUNJA_URL='https://your-vikunja-instance'", file=sys.stderr)
        print("  export VIKUNJA_TOKEN='your-api-token'", file=sys.stderr)
        sys.exit(1)

    print("=== Vikunja Seed: NovaTrek Adventures ===")
    print(f"  Target: {base_url or '(dry-run)'}")
    print(f"  Dry run: {args.dry_run}")
    print()

    # Load metadata
    capabilities = load_capabilities()
    tickets = load_tickets()
    print(f"  Loaded {len(capabilities)} capabilities and {len(tickets)} tickets")
    print()

    # Step 1: Create project
    print("--- Creating project ---")
    project = create_project(base_url, token, args.dry_run)
    project_id = project["id"]
    print()

    # Step 2: Create labels
    print("--- Creating labels ---")
    labels = create_labels(base_url, token, capabilities, args.dry_run)
    print(f"  Total labels: {len(labels)}")
    print()

    # Step 3: Import tickets
    print("--- Importing tickets ---")
    created = import_tickets(base_url, token, project_id, tickets, labels, args.dry_run)
    print()

    print("=== Seed Complete ===")
    print(f"  Project: NovaTrek Adventures")
    print(f"  Labels: {len(labels)}")
    print(f"  Tickets: {created}")


if __name__ == "__main__":
    main()
