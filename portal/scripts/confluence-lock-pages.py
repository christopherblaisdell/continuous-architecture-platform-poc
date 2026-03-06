#!/usr/bin/env python3
"""Lock Confluence pages to prevent manual edits.

Sets edit restrictions on all pages with a specified label in a Confluence
space, so only the CI service account can modify them. This is Layer 1 of
the 4-layer drift prevention strategy.

Usage:
    python3 portal/scripts/confluence-lock-pages.py \
        --base-url "https://novatrek.atlassian.net/wiki" \
        --username "architect@example.com" \
        --api-token "ATATT3..." \
        --space "ARCH" \
        --label "auto-generated"
"""

import argparse
import base64
import json
import sys
import urllib.request
import urllib.error


def make_auth_header(username, api_token):
    """Create Basic auth header for Confluence Cloud REST API."""
    credentials = base64.b64encode(f"{username}:{api_token}".encode()).decode()
    return {"Authorization": f"Basic {credentials}", "Content-Type": "application/json"}


def api_get(base_url, path, headers):
    """Perform GET request to Confluence REST API."""
    url = f"{base_url}{path}"
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def api_put(base_url, path, headers, data):
    """Perform PUT request to Confluence REST API."""
    url = f"{base_url}{path}"
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, headers=headers, method="PUT")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def get_current_user(base_url, headers):
    """Get the account ID of the authenticated user."""
    result = api_get(base_url, "/rest/api/user/current", headers)
    return result["accountId"]


def get_pages_by_label(base_url, space, label, headers):
    """Fetch all pages in a space with a given label, handling pagination."""
    pages = []
    start = 0
    limit = 50

    while True:
        path = f"/rest/api/content?spaceKey={space}&type=page&limit={limit}&start={start}"
        result = api_get(base_url, path, headers)

        for page in result.get("results", []):
            # Fetch labels for this page
            label_path = f"/rest/api/content/{page['id']}/label"
            label_result = api_get(base_url, label_path, headers)
            page_labels = [lbl["name"] for lbl in label_result.get("results", [])]
            if label in page_labels:
                pages.append({"id": page["id"], "title": page["title"]})

        if len(result.get("results", [])) < limit:
            break
        start += limit

    return pages


def set_edit_restriction(base_url, page_id, account_id, headers):
    """Set edit restriction on a page so only the service account can modify it."""
    path = f"/rest/api/content/{page_id}/restriction"
    data = [
        {
            "operation": "update",
            "restrictions": {
                "user": {
                    "results": [{"type": "known", "accountId": account_id}],
                    "start": 0,
                    "limit": 1,
                    "size": 1,
                }
            },
        }
    ]
    return api_put(base_url, path, headers, data)


def main():
    parser = argparse.ArgumentParser(description="Lock Confluence pages to prevent manual edits")
    parser.add_argument("--base-url", required=True, help="Confluence base URL (e.g., https://novatrek.atlassian.net/wiki)")
    parser.add_argument("--username", required=True, help="Service account email")
    parser.add_argument("--api-token", required=True, help="Confluence API token")
    parser.add_argument("--space", required=True, help="Confluence space key")
    parser.add_argument("--label", required=True, help="Only lock pages with this label")
    parser.add_argument("--dry-run", action="store_true", help="List pages without locking")
    args = parser.parse_args()

    headers = make_auth_header(args.username, args.api_token)

    print("=== Confluence Page Lock ===")
    print(f"  Space: {args.space}")
    print(f"  Label: {args.label}")
    print()

    # Get service account ID
    try:
        account_id = get_current_user(args.base_url, headers)
        print(f"  Service account: {account_id}")
    except urllib.error.HTTPError as e:
        print(f"  ERROR: Failed to authenticate — {e.code} {e.reason}", file=sys.stderr)
        sys.exit(1)

    # Find all pages with the target label
    print(f"  Scanning for pages with label '{args.label}'...")
    pages = get_pages_by_label(args.base_url, args.space, args.label, headers)
    print(f"  Found {len(pages)} pages")
    print()

    if not pages:
        print("  No pages to lock.")
        return

    # Lock each page
    locked = 0
    failed = 0
    for page in pages:
        if args.dry_run:
            print(f"  [DRY RUN] Would lock: {page['title']} (id={page['id']})")
            locked += 1
            continue

        try:
            set_edit_restriction(args.base_url, page["id"], account_id, headers)
            print(f"  Locked: {page['title']}")
            locked += 1
        except urllib.error.HTTPError as e:
            print(f"  FAILED: {page['title']} — {e.code} {e.reason}", file=sys.stderr)
            failed += 1

    print()
    print(f"  Locked: {locked}")
    if failed:
        print(f"  Failed: {failed}")
        sys.exit(1)


if __name__ == "__main__":
    main()
