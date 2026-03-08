#!/usr/bin/env python3
"""Delete all pages from a Confluence space (except the space homepage).

This script removes all child pages from a Confluence Cloud space,
effectively resetting the space to a clean state for republishing.

Usage:
    python3 portal/scripts/confluence-delete-space-content.py \
        --base-url "https://novatrek.atlassian.net/wiki" \
        --username "architect@example.com" \
        --api-token "ATATT3..." \
        --space "ARCH"

    # Dry run (list pages without deleting):
    python3 portal/scripts/confluence-delete-space-content.py \
        --base-url "https://novatrek.atlassian.net/wiki" \
        --username "architect@example.com" \
        --api-token "ATATT3..." \
        --space "ARCH" \
        --dry-run
"""

import argparse
import base64
import json
import sys
import time
import urllib.error
import urllib.request


def make_auth_header(username, api_token):
    """Create Basic auth header for Confluence Cloud REST API."""
    credentials = base64.b64encode(f"{username}:{api_token}".encode()).decode()
    return {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json",
    }


def api_get(base_url, path, headers):
    """Perform GET request to Confluence REST API."""
    url = f"{base_url}{path}"
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def api_delete(base_url, path, headers):
    """Perform DELETE request to Confluence REST API."""
    url = f"{base_url}{path}"
    req = urllib.request.Request(url, headers=headers, method="DELETE")
    with urllib.request.urlopen(req) as resp:
        return resp.status


def get_space_homepage_id(base_url, space, headers):
    """Get the homepage ID for a space."""
    result = api_get(base_url, f"/rest/api/space/{space}?expand=homepage", headers)
    return result["homepage"]["id"]


def get_all_pages(base_url, space, headers):
    """Fetch all pages in a space, handling pagination."""
    pages = []
    start = 0
    limit = 50

    while True:
        path = (
            f"/rest/api/content?spaceKey={space}&type=page"
            f"&limit={limit}&start={start}"
            f"&expand=ancestors"
        )
        result = api_get(base_url, path, headers)

        for page in result.get("results", []):
            depth = len(page.get("ancestors", []))
            pages.append({
                "id": page["id"],
                "title": page["title"],
                "depth": depth,
            })

        if len(result.get("results", [])) < limit:
            break
        start += limit

    return pages


def delete_page(base_url, page_id, headers):
    """Delete a single page."""
    path = f"/rest/api/content/{page_id}"
    return api_delete(base_url, path, headers)


def main():
    parser = argparse.ArgumentParser(
        description="Delete all pages from a Confluence space"
    )
    parser.add_argument(
        "--base-url", required=True,
        help="Confluence base URL (e.g., https://novatrek.atlassian.net/wiki)",
    )
    parser.add_argument("--username", required=True, help="Service account email")
    parser.add_argument("--api-token", required=True, help="Confluence API token")
    parser.add_argument("--space", required=True, help="Confluence space key")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="List pages without deleting",
    )
    args = parser.parse_args()

    headers = make_auth_header(args.username, args.api_token)

    print("=== Confluence Space Content Deletion ===")
    print(f"  Space: {args.space}")
    if args.dry_run:
        print("  Mode:  DRY RUN (no pages will be deleted)")
    print()

    # Get the space homepage ID (we keep this page)
    try:
        homepage_id = get_space_homepage_id(args.base_url, args.space, headers)
        print(f"  Space homepage ID: {homepage_id} (will be preserved)")
    except urllib.error.HTTPError as e:
        print(f"  ERROR: Failed to access space — {e.code} {e.reason}", file=sys.stderr)
        sys.exit(1)

    # Get all pages
    print("  Fetching all pages...")
    pages = get_all_pages(args.base_url, args.space, headers)
    print(f"  Found {len(pages)} total pages")

    # Exclude homepage
    pages_to_delete = [p for p in pages if p["id"] != homepage_id]
    print(f"  Pages to delete: {len(pages_to_delete)}")
    print()

    if not pages_to_delete:
        print("  No pages to delete. Space is already clean.")
        return

    # Sort by depth descending — delete deepest pages first to avoid
    # "page has children" errors
    pages_to_delete.sort(key=lambda p: p["depth"], reverse=True)

    deleted = 0
    failed = 0

    for page in pages_to_delete:
        if args.dry_run:
            print(f"  [DRY RUN] Would delete: {page['title']} (id={page['id']}, depth={page['depth']})")
            deleted += 1
            continue

        try:
            delete_page(args.base_url, page["id"], headers)
            print(f"  Deleted: {page['title']} (id={page['id']})")
            deleted += 1
            # Small delay to avoid rate limiting
            time.sleep(0.2)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                # Already deleted (parent deletion cascades to children)
                print(f"  Skipped (already gone): {page['title']}")
                deleted += 1
            else:
                print(
                    f"  FAILED: {page['title']} — {e.code} {e.reason}",
                    file=sys.stderr,
                )
                failed += 1

    print()
    print(f"  Deleted: {deleted}")
    if failed:
        print(f"  Failed: {failed}")
        sys.exit(1)

    print()
    print("  Space content deleted. Ready for republishing.")


if __name__ == "__main__":
    main()
