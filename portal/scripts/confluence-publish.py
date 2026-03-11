#!/usr/bin/env python3
"""Publish Confluence staging files in correct order.

Ensures parent/index pages are published before their children,
preventing mark from creating orphaned placeholder pages.

Usage:
    python3 portal/scripts/confluence-publish.py
    python3 portal/scripts/confluence-publish.py --dry-run
"""

import glob
import os
import subprocess
import sys


WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFLUENCE_DIR = os.path.join(WORKSPACE_ROOT, "portal", "confluence")


def get_mark_cmd():
    """Build the base mark command from environment variables."""
    base_url = os.environ.get("CONFLUENCE_BASE_URL", "")
    username = os.environ.get("CONFLUENCE_USERNAME", "")
    api_token = os.environ.get("CONFLUENCE_API_TOKEN", "")

    if not all([base_url, username, api_token]):
        print("ERROR: CONFLUENCE_BASE_URL, CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN must be set")
        sys.exit(1)

    return [
        "mark",
        "--base-url", base_url,
        "-u", username,
        "-p", api_token,
        "--minor-edit",
        "--ci",
    ]


def sort_files_parent_first(files):
    """Sort files so that index.md / parent pages come before children.

    Order:
      1. Root index.md (home page)
      2. Section index.md files (sorted by depth, shallowest first)
      3. Non-index .md files (sorted by depth, shallowest first)

    This ensures mark processes parent pages before children,
    preventing orphaned placeholder creation.
    """
    root_index = []
    section_indexes = []
    leaf_pages = []

    for f in files:
        rel = os.path.relpath(f, CONFLUENCE_DIR)
        basename = os.path.basename(f)
        depth = rel.count(os.sep)

        if rel == "index.md":
            root_index.append((depth, rel, f))
        elif basename == "index.md":
            section_indexes.append((depth, rel, f))
        else:
            leaf_pages.append((depth, rel, f))

    # Sort each group by depth (shallowest first), then alphabetically
    root_index.sort()
    section_indexes.sort()
    leaf_pages.sort()

    return [f for _, _, f in root_index + section_indexes + leaf_pages]


def publish_files(files, dry_run=False):
    """Publish files one at a time via mark, in order."""
    base_cmd = get_mark_cmd()
    total = len(files)
    success = 0
    failed = []

    for i, filepath in enumerate(files, 1):
        rel = os.path.relpath(filepath, WORKSPACE_ROOT)
        print(f"\n[{i}/{total}] Publishing: {rel}")

        if dry_run:
            cmd = base_cmd + ["--dry-run", "-f", filepath]
        else:
            cmd = base_cmd + ["-f", filepath]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"  FAILED: {result.stderr.strip()}")
            failed.append((rel, result.stderr.strip()))
        else:
            # Extract the URL from mark output
            lines = result.stdout.strip().split("\n")
            url_line = [l for l in lines if l.startswith("http")]
            if url_line:
                print(f"  OK: {url_line[-1]}")
            else:
                print(f"  OK")
            success += 1

        # Print mark's log output
        for line in result.stderr.split("\n"):
            line = line.strip()
            if line and "FATAL" not in line:
                print(f"  {line}")

    print(f"\n{'='*60}")
    print(f"PUBLISH SUMMARY: {success}/{total} succeeded, {len(failed)} failed")
    if failed:
        print("\nFailed pages:")
        for rel, err in failed:
            print(f"  {rel}: {err[:100]}")
    print(f"{'='*60}")

    return len(failed) == 0


def main():
    dry_run = "--dry-run" in sys.argv

    # Find all staging .md files
    pattern = os.path.join(CONFLUENCE_DIR, "**", "*.md")
    all_files = glob.glob(pattern, recursive=True)

    if not all_files:
        print(f"No .md files found in {CONFLUENCE_DIR}")
        sys.exit(1)

    # Sort for correct parent-first ordering
    ordered = sort_files_parent_first(all_files)

    print(f"Found {len(ordered)} pages to publish")
    if dry_run:
        print("DRY RUN — no pages will be created/updated\n")
    else:
        print("Publishing to Confluence...\n")

    # Show planned order
    print("Publish order:")
    for i, f in enumerate(ordered, 1):
        rel = os.path.relpath(f, CONFLUENCE_DIR)
        print(f"  {i:3d}. {rel}")

    print()

    ok = publish_files(ordered, dry_run)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
