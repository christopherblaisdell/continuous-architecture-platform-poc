#!/usr/bin/env python3
"""Test Confluence API connectivity and list spaces."""
import urllib.request
import json
import base64
import os
import sys


def main():
    user = os.environ.get("CONFLUENCE_USERNAME", "")
    token = os.environ.get("CONFLUENCE_API_TOKEN", "")

    if not user or not token:
        print("ERROR: CONFLUENCE_USERNAME and CONFLUENCE_API_TOKEN must be set")
        sys.exit(1)

    creds = base64.b64encode(f"{user}:{token}".encode()).decode()

    base_url = os.environ.get("CONFLUENCE_BASE_URL", "https://christopherblaisdell.atlassian.net/wiki")
    # Derive site root (without /wiki) for Jira endpoints
    site_root = base_url.replace("/wiki", "")
    print(f"Using base URL: {base_url}")

    headers = {"Authorization": f"Basic {creds}", "Accept": "application/json"}

    tests = [
        ("Confluence v2 spaces", f"{base_url}/api/v2/spaces"),
        ("Confluence v1 space", f"{base_url}/rest/api/space"),
        ("Confluence content", f"{base_url}/rest/api/content"),
        ("Jira myself", f"{site_root}/rest/api/3/myself"),
        ("Jira serverInfo", f"{site_root}/rest/api/3/serverInfo"),
    ]

    any_ok = False
    for label, url in tests:
        req = urllib.request.Request(url, headers=headers)
        try:
            resp = urllib.request.urlopen(req)
            data = resp.read()[:300].decode()
            print(f"OK  {label}: {data[:200]}")
            any_ok = True
        except urllib.error.HTTPError as e:
            body = e.read()[:300].decode("utf-8", errors="replace")
            print(f"{e.code} {label}: {body[:200]}")

    if not any_ok:
        print("\nNo endpoints reachable. Confluence may not be activated on this site.")
        sys.exit(1)
    print("\nAt least one endpoint is reachable.")


if __name__ == "__main__":
    main()
