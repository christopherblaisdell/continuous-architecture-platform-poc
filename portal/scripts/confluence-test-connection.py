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

    headers = {"Authorization": f"Basic {creds}", "Accept": "application/json"}

    tests = [
        ("Confluence v2 spaces", "https://novatrek.atlassian.net/wiki/api/v2/spaces"),
        ("Confluence v1 space", "https://novatrek.atlassian.net/wiki/rest/api/space"),
        ("Confluence content", "https://novatrek.atlassian.net/wiki/rest/api/content"),
        ("Jira myself", "https://novatrek.atlassian.net/rest/api/3/myself"),
        ("Jira serverInfo", "https://novatrek.atlassian.net/rest/api/3/serverInfo"),
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
