#!/usr/bin/env python3
"""Detect manual edits (drift) in auto-generated Confluence pages.

Compares Confluence page state against the expected CI-published state by:
  1. Checking if the last editor is someone other than the service account
  2. Comparing content hashes between Confluence and the local staging directory

Exit code 0 = no drift; exit code 1 = drift detected or error.

Usage:
    export CONFLUENCE_BASE_URL="https://novatrek.atlassian.net/wiki"
    export CONFLUENCE_USERNAME="architect@example.com"
    export CONFLUENCE_API_TOKEN="ATATT3..."
    export CONFLUENCE_SPACE="ARCH"
    python3 portal/scripts/confluence-drift-check.py [--staging-dir portal/confluence]
"""

import argparse
import base64
import hashlib
import json
import os
import re
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


def get_current_user(base_url, headers):
    """Get the account ID of the authenticated user."""
    result = api_get(base_url, "/rest/api/user/current", headers)
    return result["accountId"]


def get_labeled_pages(base_url, space, label, headers):
    """Fetch all pages in a space with the auto-generated label."""
    pages = []
    start = 0
    limit = 50

    while True:
        path = (
            f"/rest/api/content?spaceKey={space}&type=page"
            f"&limit={limit}&start={start}"
            f"&expand=version,body.storage,history.lastUpdated"
        )
        result = api_get(base_url, path, headers)

        for page in result.get("results", []):
            label_path = f"/rest/api/content/{page['id']}/label"
            label_result = api_get(base_url, label_path, headers)
            page_labels = [lbl["name"] for lbl in label_result.get("results", [])]
            if label in page_labels:
                pages.append(page)

        if len(result.get("results", [])) < limit:
            break
        start += limit

    return pages


def normalize_html(html):
    """Normalize HTML for comparison by stripping whitespace variations."""
    text = re.sub(r'\s+', ' ', html.strip())
    return text


def content_hash(text):
    """SHA-256 hash of normalized content."""
    return hashlib.sha256(normalize_html(text).encode()).hexdigest()


def load_staging_hashes(staging_dir):
    """Build a dict of {page_title: content_hash} from the staging directory.

    Reads the Title header from each markdown file to map to Confluence titles.
    """
    hashes = {}
    if not os.path.isdir(staging_dir):
        return hashes

    for fname in os.listdir(staging_dir):
        if not fname.endswith(".md"):
            continue
        filepath = os.path.join(staging_dir, fname)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract title from mark header
        title_match = re.search(r'^\s*<!--\s*Title:\s*(.+?)\s*-->', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
        else:
            title = fname.replace(".md", "").replace("-", " ").title()

        # Hash the body content (everything after the header block)
        # Strip mark headers for hashing
        body = re.sub(r'<!--\s*(Space|Parent|Title|Label):.*?-->\s*', '', content)
        hashes[title] = content_hash(body)

    return hashes


def check_drift(base_url, space, label, service_account_id, staging_dir, headers):
    """Check all auto-generated pages for drift. Returns list of drift findings."""
    findings = []
    staging_hashes = load_staging_hashes(staging_dir)

    print(f"Fetching pages with label '{label}' in space '{space}'...")
    pages = get_labeled_pages(base_url, space, label, headers)
    print(f"Found {len(pages)} auto-generated pages")
    print(f"Loaded {len(staging_hashes)} staging page hashes")
    print()

    for page in pages:
        title = page["title"]
        page_id = page["id"]
        issues = []

        # Check 1: Last editor
        version = page.get("version", {})
        last_editor_id = version.get("by", {}).get("accountId", "unknown")
        if last_editor_id != service_account_id:
            last_editor_name = version.get("by", {}).get("displayName", "unknown")
            issues.append(f"last edited by {last_editor_name} (not service account)")

        # Check 2: Content hash comparison
        if title in staging_hashes:
            confluence_body = page.get("body", {}).get("storage", {}).get("value", "")
            remote_hash = content_hash(confluence_body)
            local_hash = staging_hashes[title]
            if remote_hash != local_hash:
                issues.append("content hash mismatch (Confluence differs from git source)")
        else:
            issues.append("no matching staging file found")

        if issues:
            findings.append({"title": title, "id": page_id, "issues": issues})

    return findings


def main():
    parser = argparse.ArgumentParser(description="Detect drift in auto-generated Confluence pages")
    parser.add_argument("--staging-dir", default="portal/confluence", help="Path to Confluence staging directory")
    parser.add_argument("--label", default="auto-generated", help="Label identifying auto-generated pages")
    args = parser.parse_args()

    base_url = os.environ.get("CONFLUENCE_BASE_URL")
    username = os.environ.get("CONFLUENCE_USERNAME")
    api_token = os.environ.get("CONFLUENCE_API_TOKEN")
    space = os.environ.get("CONFLUENCE_SPACE", "ARCH")

    if not all([base_url, username, api_token]):
        print("ERROR: Set CONFLUENCE_BASE_URL, CONFLUENCE_USERNAME, and CONFLUENCE_API_TOKEN", file=sys.stderr)
        sys.exit(1)

    headers = make_auth_header(username, api_token)

    print("=== Confluence Drift Check ===")
    print(f"  Space: {space}")
    print(f"  Staging: {args.staging_dir}")
    print()

    try:
        service_account_id = get_current_user(base_url, headers)
        print(f"  Service account: {service_account_id}")
    except urllib.error.HTTPError as e:
        print(f"  ERROR: Authentication failed — {e.code} {e.reason}", file=sys.stderr)
        sys.exit(1)

    findings = check_drift(base_url, space, args.label, service_account_id, args.staging_dir, headers)

    if not findings:
        print("No drift detected. All auto-generated pages match git source.")
        sys.exit(0)

    print(f"DRIFT DETECTED in {len(findings)} page(s):")
    print()
    for finding in findings:
        print(f"  Page: {finding['title']} (id={finding['id']})")
        for issue in finding["issues"]:
            print(f"    - {issue}")
        print()

    sys.exit(1)


if __name__ == "__main__":
    main()
