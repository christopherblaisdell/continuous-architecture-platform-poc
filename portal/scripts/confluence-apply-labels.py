#!/usr/bin/env python3
"""Apply labels to all Confluence pages based on staging file metadata.

mark CLI doesn't apply labels when --minor-edit is used, so this script
applies them via the REST API after publishing.

Usage:
    python3 portal/scripts/confluence-apply-labels.py
"""

import glob
import json
import os
import re
import sys
import urllib.request
import urllib.error


WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFLUENCE_DIR = os.path.join(WORKSPACE_ROOT, "portal", "confluence")


def get_config():
    base_url = os.environ.get("CONFLUENCE_BASE_URL", "")
    username = os.environ.get("CONFLUENCE_USERNAME", "")
    api_token = os.environ.get("CONFLUENCE_API_TOKEN", "")
    space = os.environ.get("CONFLUENCE_SPACE", "ARCH")
    if not all([base_url, username, api_token]):
        print("ERROR: Set CONFLUENCE_BASE_URL, CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN")
        sys.exit(1)
    return base_url, username, api_token, space


def make_headers(username, api_token):
    import base64
    creds = base64.b64encode(f"{username}:{api_token}".encode()).decode()
    return {
        "Authorization": f"Basic {creds}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def get_all_pages(base_url, space, headers):
    """Fetch all pages in the space."""
    pages = {}
    start = 0
    while True:
        url = f"{base_url}/rest/api/content?spaceKey={space}&limit=100&start={start}&expand=metadata.labels"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
        for page in data["results"]:
            existing_labels = {r["name"] for r in page.get("metadata", {}).get("labels", {}).get("results", [])}
            pages[page["title"]] = {"id": page["id"], "labels": existing_labels}
        if len(data["results"]) < 100:
            break
        start += 100
    return pages


def add_labels(base_url, page_id, labels, headers):
    """Add labels to a page via REST API."""
    url = f"{base_url}/rest/api/content/{page_id}/label"
    body = json.dumps([{"prefix": "global", "name": label} for label in labels]).encode()
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        return resp.status


def parse_labels_from_staging():
    """Read all staging .md files and extract label metadata."""
    page_labels = {}
    for filepath in glob.glob(os.path.join(CONFLUENCE_DIR, "**", "*.md"), recursive=True):
        title = None
        labels = set()
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                m = re.match(r"<!-- Title: (.+?) -->", line)
                if m:
                    title = m.group(1)
                m = re.match(r"<!-- Label: (.+?) -->", line)
                if m:
                    # Labels can be comma-separated on one line
                    for label in m.group(1).split(","):
                        label = label.strip()
                        if label:
                            labels.add(label)
                if not line.startswith("<!--"):
                    break
        if title and labels:
            page_labels[title] = labels
    return page_labels


def main():
    base_url, username, api_token, space = get_config()
    headers = make_headers(username, api_token)

    print("Reading labels from staging files...")
    staging_labels = parse_labels_from_staging()
    print(f"  {len(staging_labels)} pages have label metadata")

    print("Fetching pages from Confluence...")
    pages = get_all_pages(base_url, space, headers)
    print(f"  {len(pages)} pages found in space {space}")

    applied = 0
    skipped = 0

    for title, desired_labels in sorted(staging_labels.items()):
        page = pages.get(title)
        if not page:
            print(f"  SKIP: Page '{title}' not found in Confluence")
            skipped += 1
            continue

        missing = desired_labels - page["labels"]
        if not missing:
            continue

        try:
            add_labels(base_url, page["id"], missing, headers)
            applied += 1
            print(f"  OK: '{title}' +{len(missing)} labels: {', '.join(sorted(missing))}")
        except urllib.error.HTTPError as e:
            print(f"  FAIL: '{title}': {e.code} {e.reason}")

    print(f"\nDone: {applied} pages updated, {skipped} skipped")


if __name__ == "__main__":
    main()
