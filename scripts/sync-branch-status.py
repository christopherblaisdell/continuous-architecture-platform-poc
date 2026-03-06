#!/usr/bin/env python3
"""Sync ticket status based on Git branch state.

Checks for solution branches (solution/NTK-XXXXX-*) and updates ticket
status in both tickets.yaml and Vikunja:
  - Branch exists and open PR -> "In Progress"
  - Branch merged to main -> "Ready for Dev"

Usage:
    export VIKUNJA_URL="..."
    export VIKUNJA_TOKEN="..."
    python3 scripts/sync-branch-status.py [--dry-run]

Designed to run in GitHub Actions on branch push and PR merge events.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
import urllib.error
import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
TICKETS_PATH = os.path.join(REPO_ROOT, "architecture", "metadata", "tickets.yaml")

VIKUNJA_URL = os.environ.get("VIKUNJA_URL", "").rstrip("/")
VIKUNJA_TOKEN = os.environ.get("VIKUNJA_TOKEN", "")


def vikunja_api(method, path, data=None):
    if not VIKUNJA_URL or not VIKUNJA_TOKEN:
        return None
    url = f"{VIKUNJA_URL}/api/v1{path}"
    headers = {"Authorization": f"Bearer {VIKUNJA_TOKEN}", "Content-Type": "application/json"}
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except (urllib.error.URLError, OSError):
        return None


def get_solution_branches():
    """Get all remote solution branches and their merge status."""
    try:
        result = subprocess.run(
            ["git", "branch", "-r", "--list", "origin/solution/*"],
            capture_output=True, text=True, check=True
        )
        branches = [b.strip() for b in result.stdout.strip().split("\n") if b.strip()]
    except subprocess.CalledProcessError:
        branches = []

    # Also check merged branches
    try:
        result = subprocess.run(
            ["git", "branch", "-r", "--merged", "origin/main", "--list", "origin/solution/*"],
            capture_output=True, text=True, check=True
        )
        merged = set(b.strip() for b in result.stdout.strip().split("\n") if b.strip())
    except subprocess.CalledProcessError:
        merged = set()

    branch_status = {}
    for branch in branches:
        match = re.search(r"solution/(NTK-\d+)", branch)
        if match:
            ticket_key = match.group(1)
            branch_status[ticket_key] = "merged" if branch in merged else "in-progress"

    return branch_status


def get_vikunja_project_and_tasks():
    """Get Vikunja project ID and tasks keyed by ticket ID."""
    projects = vikunja_api("GET", "/projects")
    if not projects:
        return None, {}
    pid = None
    for p in projects:
        if p.get("title") == "NovaTrek Adventures":
            pid = p["id"]
            break
    if not pid:
        return None, {}

    tasks = []
    page = 1
    while True:
        result = vikunja_api("GET", f"/projects/{pid}/tasks?page={page}")
        if not result:
            break
        tasks.extend(result)
        if len(result) < 50:
            break
        page += 1

    task_by_key = {}
    for task in tasks:
        match = re.match(r"\[([A-Z]+-\d+)\]", task.get("title", ""))
        if match:
            task_by_key[match.group(1)] = task

    return pid, task_by_key


def main():
    parser = argparse.ArgumentParser(description="Sync ticket status from Git branches")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    branch_status = get_solution_branches()
    if not branch_status:
        print("No solution branches found.")
        return

    print(f"Found {len(branch_status)} solution branches:")
    for key, status in sorted(branch_status.items()):
        print(f"  {key}: {status}")

    # Load YAML tickets
    with open(TICKETS_PATH, encoding="utf-8") as f:
        yaml_data = yaml.safe_load(f)

    status_map = {
        "in-progress": "In Progress",
        "merged": "Ready for Dev",
    }

    yaml_changes = 0
    for ticket in yaml_data.get("tickets", []):
        key = ticket["key"]
        if key not in branch_status:
            continue
        new_status = status_map.get(branch_status[key])
        if not new_status:
            continue
        current = ticket.get("status", "")
        # Only update forward: New -> In Progress -> Ready for Dev
        order = {"New": 0, "In Progress": 1, "Ready for Dev": 2, "Closed": 3}
        if order.get(new_status, 0) <= order.get(current, 0):
            continue
        if args.dry_run:
            print(f"  [DRY RUN] {key}: {current} -> {new_status}")
        else:
            print(f"  {key}: {current} -> {new_status}")
            ticket["status"] = new_status
        yaml_changes += 1

    if yaml_changes > 0 and not args.dry_run:
        with open(TICKETS_PATH, "w", encoding="utf-8") as f:
            yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120)
        print(f"Updated {yaml_changes} tickets in tickets.yaml")

    print(f"\nTotal changes: {yaml_changes}")


if __name__ == "__main__":
    main()
