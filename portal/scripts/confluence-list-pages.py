#!/usr/bin/env python3
"""List pages in the ARCH Confluence space."""
import urllib.request
import json
import base64
import os
import sys


def main():
    user = os.environ.get("CONFLUENCE_USERNAME", "")
    token = os.environ.get("CONFLUENCE_API_TOKEN", "")
    base_url = os.environ.get("CONFLUENCE_BASE_URL", "https://christopherblaisdell.atlassian.net/wiki")
    space = os.environ.get("CONFLUENCE_SPACE", "ARCH")

    if not user or not token:
        print("ERROR: CONFLUENCE_USERNAME and CONFLUENCE_API_TOKEN must be set")
        sys.exit(1)

    creds = base64.b64encode(f"{user}:{token}".encode()).decode()
    headers = {"Authorization": f"Basic {creds}", "Accept": "application/json"}

    # Space info
    url = f"{base_url}/rest/api/space/{space}?expand=homepage"
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    hp = data.get("homepage", {})
    print(f"Space: {data['name']} (key: {data['key']})")
    print(f"Homepage: {hp.get('title', '?')} (id: {hp.get('id', '?')})")

    # List all pages
    start = 0
    total = 0
    while True:
        url2 = f"{base_url}/rest/api/content?spaceKey={space}&type=page&limit=50&start={start}"
        req2 = urllib.request.Request(url2, headers=headers)
        resp2 = urllib.request.urlopen(req2)
        data2 = json.loads(resp2.read())
        for p in data2["results"]:
            total += 1
            print(f"  {p['id']}: {p['title']}")
        if data2["size"] < 50:
            break
        start += 50

    print(f"\nTotal pages: {total}")


if __name__ == "__main__":
    main()
