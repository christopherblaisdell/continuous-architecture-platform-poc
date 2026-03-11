#!/usr/bin/env python3
"""Verify Confluence content matches the local staging directory.

Round-trip verification: after publishing via `mark`, this script pulls
content back from Confluence and validates that pages exist with correct
titles, parents, labels, headings, and attachments.

Usage:
    python3 portal/scripts/confluence-verify.py \
        --base-url "https://novatrek.atlassian.net/wiki" \
        --username "architect@example.com" \
        --api-token "ATATT3..." \
        --space "ARCH"
"""

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFLUENCE_DIR = os.path.join(WORKSPACE_ROOT, "portal", "confluence")


# ---------------------------------------------------------------------------
# Confluence REST API helpers
# ---------------------------------------------------------------------------

def make_auth_header(username, api_token):
    credentials = base64.b64encode(f"{username}:{api_token}".encode()).decode()
    return {"Authorization": f"Basic {credentials}", "Content-Type": "application/json"}


def api_get(base_url, path, headers):
    url = f"{base_url}{path}"
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def get_all_pages(base_url, space, headers):
    """Fetch all pages in a space with body, ancestors, labels, and children expanded."""
    pages = []
    start = 0
    limit = 50
    while True:
        path = (
            f"/rest/api/content?spaceKey={space}&type=page"
            f"&expand=body.storage,ancestors,metadata.labels,children.attachment"
            f"&limit={limit}&start={start}"
        )
        result = api_get(base_url, path, headers)
        pages.extend(result.get("results", []))
        if len(result.get("results", [])) < limit:
            break
        start += limit
    return pages


def get_attachments(base_url, page_id, headers):
    """Fetch attachment list for a page."""
    path = f"/rest/api/content/{page_id}/child/attachment?limit=100"
    result = api_get(base_url, path, headers)
    return [att["title"] for att in result.get("results", [])]


# ---------------------------------------------------------------------------
# Staging file parser
# ---------------------------------------------------------------------------

def parse_staging_file(filepath):
    """Extract mark headers and content from a staging Markdown file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    info = {
        "filepath": filepath,
        "space": None,
        "parent": None,
        "title": None,
        "labels": [],
        "headings": [],
        "images": [],
    }

    for line in content.split("\n"):
        m = re.match(r"<!--\s*Space:\s*(.+?)\s*-->", line)
        if m:
            info["space"] = m.group(1)
        m = re.match(r"<!--\s*Parent:\s*(.+?)\s*-->", line)
        if m:
            info["parent"] = m.group(1)
        m = re.match(r"<!--\s*Title:\s*(.+?)\s*-->", line)
        if m:
            info["title"] = m.group(1)
        m = re.match(r"<!--\s*Label:\s*(.+?)\s*-->", line)
        if m:
            info["labels"] = [lbl.strip() for lbl in m.group(1).split(",")]

    # Extract Markdown headings (H1-H3)
    for m in re.finditer(r"^(#{1,3})\s+(.+)$", content, re.MULTILINE):
        level = len(m.group(1))
        text = m.group(2).strip()
        info["headings"].append((level, text))

    # Extract image references
    for m in re.finditer(r"!\[.*?\]\((.+?)\)", content):
        info["images"].append(m.group(1))

    return info


def load_all_staging_files(staging_dir=None):
    """Recursively load all staging Markdown files."""
    base_dir = staging_dir or CONFLUENCE_DIR
    staging = {}
    for root, _dirs, files in os.walk(base_dir):
        for fname in files:
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(root, fname)
            info = parse_staging_file(fpath)
            if info["title"]:
                staging[info["title"]] = info
    return staging


# ---------------------------------------------------------------------------
# XHTML heading extractor
# ---------------------------------------------------------------------------

class HeadingExtractor(HTMLParser):
    """Extract headings from Confluence Storage Format (XHTML)."""

    def __init__(self):
        super().__init__()
        self._in_heading = False
        self._heading_level = 0
        self._heading_text = ""
        self.headings = []

    def handle_starttag(self, tag, attrs):
        m = re.match(r"h([1-6])", tag)
        if m:
            self._in_heading = True
            self._heading_level = int(m.group(1))
            self._heading_text = ""

    def handle_endtag(self, tag):
        if re.match(r"h[1-6]", tag) and self._in_heading:
            self._in_heading = False
            text = self._heading_text.strip()
            if text:
                self.headings.append((self._heading_level, text))

    def handle_data(self, data):
        if self._in_heading:
            self._heading_text += data


def extract_xhtml_headings(xhtml):
    """Extract headings from Confluence Storage Format body."""
    parser = HeadingExtractor()
    try:
        parser.feed(xhtml)
    except Exception:
        pass
    return parser.headings


# ---------------------------------------------------------------------------
# Verification checks
# ---------------------------------------------------------------------------

class VerificationReport:
    def __init__(self):
        self.checks = 0
        self.passed = 0
        self.warnings = 0
        self.failures = 0
        self.details = []

    def ok(self, msg):
        self.checks += 1
        self.passed += 1

    def warn(self, msg):
        self.checks += 1
        self.warnings += 1
        self.details.append(f"  WARNING: {msg}")

    def fail(self, msg):
        self.checks += 1
        self.failures += 1
        self.details.append(f"  FAIL: {msg}")

    def section(self, title):
        self.details.append(f"\n=== {title} ===")

    def summary(self):
        lines = ["\n" + "=" * 60]
        lines.append("CONFLUENCE VERIFICATION REPORT")
        lines.append("=" * 60)
        for d in self.details:
            lines.append(d)
        lines.append("")
        lines.append("-" * 60)
        lines.append(f"Checks: {self.checks}  Passed: {self.passed}  Warnings: {self.warnings}  Failures: {self.failures}")
        if self.failures == 0:
            lines.append("RESULT: ALL CHECKS PASSED")
        else:
            lines.append(f"RESULT: {self.failures} FAILURE(S) DETECTED")
        lines.append("=" * 60)
        return "\n".join(lines)


def verify_structural(staging, confluence_pages, report):
    """Check every staging file has a Confluence page and vice versa."""
    report.section("Structural Verification")

    confluence_titles = {p["title"] for p in confluence_pages}
    staging_titles = set(staging.keys())

    missing = staging_titles - confluence_titles
    orphaned = confluence_titles - staging_titles

    for title in sorted(missing):
        report.fail(f"MISSING from Confluence: '{title}' (staged at {staging[title]['filepath']})")

    for title in sorted(orphaned):
        report.warn(f"ORPHANED in Confluence (no staging file): '{title}'")

    matched = staging_titles & confluence_titles
    report.ok(f"{len(matched)} pages matched by title")
    if missing:
        report.fail(f"{len(missing)} staging pages missing from Confluence")
    else:
        report.ok("All staging pages found in Confluence")

    return matched


def verify_hierarchy(staging, confluence_pages, matched_titles, report):
    """Check parent-child relationships match."""
    report.section("Hierarchy Verification")

    page_by_title = {p["title"]: p for p in confluence_pages}
    mismatches = 0

    for title in sorted(matched_titles):
        expected_parent = staging[title]["parent"]
        page = page_by_title.get(title)
        if not page:
            continue

        ancestors = page.get("ancestors", [])
        if ancestors:
            actual_parent = ancestors[-1].get("title", "")
        else:
            actual_parent = "(root)"

        if expected_parent and actual_parent != expected_parent:
            report.fail(f"Parent mismatch for '{title}': expected '{expected_parent}', got '{actual_parent}'")
            mismatches += 1

    if mismatches == 0:
        report.ok(f"All {len(matched_titles)} parent relationships correct")
    else:
        report.fail(f"{mismatches} parent hierarchy mismatches")


def verify_labels(staging, confluence_pages, matched_titles, report):
    """Check all expected labels are present on each page."""
    report.section("Label Verification")

    page_by_title = {p["title"]: p for p in confluence_pages}
    missing_labels = 0

    for title in sorted(matched_titles):
        expected = set(staging[title]["labels"])
        page = page_by_title.get(title)
        if not page:
            continue

        labels_data = page.get("metadata", {}).get("labels", {}).get("results", [])
        actual = {lbl["name"] for lbl in labels_data}

        diff = expected - actual
        if diff:
            report.fail(f"Missing labels on '{title}': {', '.join(sorted(diff))}")
            missing_labels += 1

    if missing_labels == 0:
        report.ok(f"All labels correct across {len(matched_titles)} pages")
    else:
        report.fail(f"{missing_labels} pages with missing labels")


def verify_content(staging, confluence_pages, matched_titles, report):
    """Check key headings from staging appear in Confluence XHTML."""
    report.section("Content Verification (Headings)")

    page_by_title = {p["title"]: p for p in confluence_pages}
    content_issues = 0

    for title in sorted(matched_titles):
        page = page_by_title.get(title)
        if not page:
            continue

        body_xhtml = page.get("body", {}).get("storage", {}).get("value", "")
        if not body_xhtml:
            report.warn(f"Empty body for '{title}'")
            content_issues += 1
            continue

        confluence_headings = extract_xhtml_headings(body_xhtml)
        confluence_heading_texts = {h[1].lower() for h in confluence_headings}

        staging_h1h2 = [(lvl, text) for lvl, text in staging[title]["headings"] if lvl <= 2]

        for lvl, text in staging_h1h2:
            if text.lower() not in confluence_heading_texts:
                report.warn(f"Heading missing in '{title}': H{lvl} '{text}'")
                content_issues += 1

    if content_issues == 0:
        report.ok(f"All H1/H2 headings verified across {len(matched_titles)} pages")
    else:
        report.warn(f"{content_issues} heading discrepancies (may be due to mark transformation)")


def verify_attachments(staging, confluence_pages, matched_titles, base_url, headers, report):
    """Check that referenced images are uploaded as attachments."""
    report.section("Attachment Verification")

    page_by_title = {p["title"]: p for p in confluence_pages}
    attachment_issues = 0
    pages_checked = 0

    for title in sorted(matched_titles):
        expected_images = staging[title]["images"]
        if not expected_images:
            continue

        page = page_by_title.get(title)
        if not page:
            continue

        pages_checked += 1
        try:
            actual_attachments = get_attachments(base_url, page["id"], headers)
        except urllib.error.HTTPError:
            report.warn(f"Could not fetch attachments for '{title}'")
            continue

        actual_set = {a.lower() for a in actual_attachments}

        for img_path in expected_images:
            img_name = os.path.basename(img_path).lower()
            # Skip external URLs
            if img_path.startswith("http://") or img_path.startswith("https://"):
                continue
            if img_name not in actual_set:
                report.warn(f"Missing attachment on '{title}': {img_name}")
                attachment_issues += 1

    if attachment_issues == 0:
        report.ok(f"Attachment check passed for {pages_checked} pages with images")
    else:
        report.warn(f"{attachment_issues} missing attachments across {pages_checked} pages")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Verify Confluence content matches staging directory")
    parser.add_argument("--base-url", default=os.environ.get("CONFLUENCE_BASE_URL", ""), help="Confluence base URL")
    parser.add_argument("--username", default=os.environ.get("CONFLUENCE_USERNAME", ""), help="Service account email")
    parser.add_argument("--api-token", default=os.environ.get("CONFLUENCE_API_TOKEN", ""), help="Confluence API token")
    parser.add_argument("--space", default=os.environ.get("CONFLUENCE_SPACE", "ARCH"), help="Confluence space key")
    parser.add_argument("--staging-dir", default=CONFLUENCE_DIR, help="Path to staging directory")
    args = parser.parse_args()

    if not args.base_url or not args.username or not args.api_token:
        print("ERROR: --base-url, --username, --api-token required (or set CONFLUENCE_BASE_URL, CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN env vars)")
        sys.exit(1)

    staging_dir = args.staging_dir

    headers = make_auth_header(args.username, args.api_token)

    print("Loading staging files...")
    staging = load_all_staging_files(staging_dir)
    print(f"  Found {len(staging)} staging pages")

    print("Fetching Confluence pages...")
    try:
        confluence_pages = get_all_pages(args.base_url, args.space, headers)
    except urllib.error.HTTPError as e:
        print(f"ERROR: Failed to connect to Confluence — {e.code} {e.reason}", file=sys.stderr)
        sys.exit(1)
    print(f"  Found {len(confluence_pages)} Confluence pages")

    report = VerificationReport()

    # 1. Structural check
    matched = verify_structural(staging, confluence_pages, report)

    if not matched:
        print(report.summary())
        sys.exit(1)

    # 2. Hierarchy check
    verify_hierarchy(staging, confluence_pages, matched, report)

    # 3. Labels check
    verify_labels(staging, confluence_pages, matched, report)

    # 4. Content headings check
    verify_content(staging, confluence_pages, matched, report)

    # 5. Attachment check
    verify_attachments(staging, confluence_pages, matched, args.base_url, headers, report)

    print(report.summary())
    sys.exit(1 if report.failures > 0 else 0)


if __name__ == "__main__":
    main()
