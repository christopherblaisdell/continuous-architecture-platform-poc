#!/usr/bin/env python3
"""Bidirectional sync between tickets.yaml and Vikunja.

Synchronization logic:
  - YAML → Vikunja: New tickets in YAML that don't exist in Vikunja are created.
  - Vikunja → YAML: Status and priority changes in Vikunja are pulled back to YAML.
  - Conflict: If both sides changed, Vikunja wins for status/priority (UI is the
    user-facing tool), YAML wins for structural fields (key, components, solution).

Usage:
    export VIKUNJA_URL="https://ca-vikunja-prod.<env>.azurecontainerapps.io"
    export VIKUNJA_TOKEN="your-api-token"
    python3 portal/scripts/sync-tickets.py [--dry-run] [--direction both|push|pull]
"""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
TICKETS_PATH = os.path.join(REPO_ROOT, "architecture", "metadata", "tickets.yaml")

PRIORITY_TO_VIKUNJA = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
VIKUNJA_TO_PRIORITY = {v: k for k, v in PRIORITY_TO_VIKUNJA.items()}

STATUS_LABELS = {"New", "In Progress", "Ready for Dev", "Closed"}


def api_request(base_url, token, method, path, data=None):
    """Make authenticated Vikunja API request."""
    url = f"{base_url}/api/v1{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def get_project_id(base_url, token):
    """Find the NovaTrek Adventures project ID."""
    projects = api_request(base_url, token, "GET", "/projects")
    for project in projects:
        if project["title"] == "NovaTrek Adventures":
            return project["id"]
    return None


def get_vikunja_tasks(base_url, token, project_id):
    """Fetch all tasks from the NovaTrek project."""
    tasks = []
    page = 1
    while True:
        result = api_request(base_url, token, "GET", f"/projects/{project_id}/tasks?page={page}")
        if not result:
            break
        tasks.extend(result)
        if len(result) < 50:
            break
        page += 1
    return tasks


def extract_ticket_key(title):
    """Extract NTK-XXXXX from task title like '[NTK-10001] Summary'."""
    match = re.match(r'\[([A-Z]+-\d+)\]', title)
    return match.group(1) if match else None


def get_task_status_label(task):
    """Extract status from task labels."""
    for label in task.get("labels", []) or []:
        title = label.get("title", "")
        if title.startswith("Status: "):
            return title.replace("Status: ", "")
    return None


def load_yaml_tickets():
    """Load tickets from YAML."""
    with open(TICKETS_PATH, "r") as f:
        data = yaml.safe_load(f)
    return data


def save_yaml_tickets(data):
    """Save tickets back to YAML preserving format."""
    with open(TICKETS_PATH, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120)


def sync_pull(base_url, token, project_id, yaml_data, dry_run):
    """Pull changes from Vikunja → YAML (status, priority)."""
    vikunja_tasks = get_vikunja_tasks(base_url, token, project_id)
    task_by_key = {}
    for task in vikunja_tasks:
        key = extract_ticket_key(task.get("title", ""))
        if key:
            task_by_key[key] = task

    changes = 0
    for ticket in yaml_data.get("tickets", []):
        key = ticket["key"]
        if key not in task_by_key:
            continue

        task = task_by_key[key]

        # Sync status
        vikunja_status = get_task_status_label(task)
        if vikunja_status and vikunja_status != ticket.get("status"):
            if dry_run:
                print(f"  [DRY RUN] {key}: status '{ticket.get('status')}' -> '{vikunja_status}'")
            else:
                print(f"  {key}: status '{ticket.get('status')}' -> '{vikunja_status}'")
                ticket["status"] = vikunja_status
            changes += 1

        # Sync priority
        vikunja_priority_num = task.get("priority", 2)
        vikunja_priority = VIKUNJA_TO_PRIORITY.get(vikunja_priority_num, "Medium")
        if vikunja_priority != ticket.get("priority"):
            if dry_run:
                print(f"  [DRY RUN] {key}: priority '{ticket.get('priority')}' -> '{vikunja_priority}'")
            else:
                print(f"  {key}: priority '{ticket.get('priority')}' -> '{vikunja_priority}'")
                ticket["priority"] = vikunja_priority
            changes += 1

    return changes


def sync_push(base_url, token, project_id, yaml_data, dry_run):
    """Push new tickets from YAML → Vikunja."""
    vikunja_tasks = get_vikunja_tasks(base_url, token, project_id)
    existing_keys = set()
    for task in vikunja_tasks:
        key = extract_ticket_key(task.get("title", ""))
        if key:
            existing_keys.add(key)

    created = 0
    for ticket in yaml_data.get("tickets", []):
        key = ticket["key"]
        if key in existing_keys:
            continue

        summary = ticket["summary"]
        priority = PRIORITY_TO_VIKUNJA.get(ticket.get("priority", "Medium"), 2)

        desc_parts = [f"**Ticket:** {key}"]
        if ticket.get("user_story"):
            desc_parts.append(f"\n**User Story:**\n{ticket['user_story'].strip()}")
        if ticket.get("components"):
            desc_parts.append(f"\n**Components:** {', '.join(ticket['components'])}")
        description = "\n".join(desc_parts)

        if dry_run:
            print(f"  [DRY RUN] Would create: [{key}] {summary}")
        else:
            api_request(base_url, token, "PUT", f"/projects/{project_id}/tasks", {
                "title": f"[{key}] {summary}",
                "description": description,
                "priority": priority,
            })
            print(f"  Created: [{key}] {summary}")
        created += 1

    return created


def main():
    parser = argparse.ArgumentParser(description="Sync tickets between YAML and Vikunja")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without applying")
    parser.add_argument("--direction", choices=["both", "push", "pull"], default="both",
                        help="Sync direction: push (YAML→Vikunja), pull (Vikunja→YAML), both")
    args = parser.parse_args()

    base_url = os.environ.get("VIKUNJA_URL", "").rstrip("/")
    token = os.environ.get("VIKUNJA_TOKEN", "")

    if not base_url or not token:
        print("ERROR: Set VIKUNJA_URL and VIKUNJA_TOKEN environment variables", file=sys.stderr)
        sys.exit(1)

    print("=== Ticket Sync ===")
    print(f"  Vikunja: {base_url}")
    print(f"  Direction: {args.direction}")
    print(f"  Dry run: {args.dry_run}")
    print()

    # Find the project
    project_id = get_project_id(base_url, token)
    if not project_id:
        print("ERROR: 'NovaTrek Adventures' project not found. Run vikunja-seed.py first.", file=sys.stderr)
        sys.exit(1)

    yaml_data = load_yaml_tickets()

    # Pull: Vikunja → YAML
    if args.direction in ("both", "pull"):
        print("--- Pull: Vikunja -> YAML ---")
        pull_changes = sync_pull(base_url, token, project_id, yaml_data, args.dry_run)
        print(f"  Changes: {pull_changes}")
        if pull_changes > 0 and not args.dry_run:
            save_yaml_tickets(yaml_data)
            print(f"  Updated {TICKETS_PATH}")
        print()

    # Push: YAML → Vikunja
    if args.direction in ("both", "push"):
        print("--- Push: YAML -> Vikunja ---")
        push_created = sync_push(base_url, token, project_id, yaml_data, args.dry_run)
        print(f"  Created: {push_created}")
        print()

    print("=== Sync Complete ===")


if __name__ == "__main__":
    main()
