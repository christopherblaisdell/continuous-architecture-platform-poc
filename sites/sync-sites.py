#!/usr/bin/env python3
"""
Sync shared documentation files to site-specific directories.

Reads sites/manifest.yaml and copies source files to each target site,
applying per-site link rewrites. This ensures all sites stay in sync
with the authoritative source files in docs/.

Usage:
    python3 sites/sync-sites.py           # sync all sites
    python3 sites/sync-sites.py --check   # dry-run: report drift without writing
"""

import argparse
import os
import sys

import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "manifest.yaml")


def load_manifest():
    with open(MANIFEST_PATH, "r") as f:
        return yaml.safe_load(f)


def apply_rewrites(content, rewrites):
    for old, new in rewrites.items():
        content = content.replace(old, new)
    return content


def sync_sites(check_only=False):
    manifest = load_manifest()
    sites = manifest["sites"]
    pages = manifest["pages"]
    link_rewrites = manifest.get("link_rewrites", {})

    synced = 0
    drifted = 0
    errors = 0

    for page in pages:
        source_path = os.path.join(REPO_ROOT, page["source"])
        if not os.path.exists(source_path):
            print(f"  ERROR: source not found: {page['source']}")
            errors += 1
            continue

        with open(source_path, "r") as f:
            source_content = f.read()

        for target in page["targets"]:
            site_name = target["site"]
            site_config = sites[site_name]
            dest_path = os.path.join(REPO_ROOT, site_config["docs_dir"], target["dest"])

            # Apply site-specific link rewrites
            rewrites = link_rewrites.get(site_name, {})
            transformed = apply_rewrites(source_content, rewrites)

            # Check if destination exists and matches
            if os.path.exists(dest_path):
                with open(dest_path, "r") as f:
                    existing = f.read()
                if existing == transformed:
                    synced += 1
                    continue
                else:
                    drifted += 1
                    if check_only:
                        print(f"  DRIFT: {page['source']} -> {site_name}/{target['dest']}")
                        continue
                    else:
                        print(f"  UPDATE: {page['source']} -> {site_name}/{target['dest']}")
            else:
                drifted += 1
                if check_only:
                    print(f"  MISSING: {site_name}/{target['dest']}")
                    continue
                else:
                    print(f"  CREATE: {page['source']} -> {site_name}/{target['dest']}")

            # Write the transformed file
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(dest_path, "w") as f:
                f.write(transformed)
            synced += 1

    return synced, drifted, errors


def main():
    parser = argparse.ArgumentParser(description="Sync shared docs to site directories")
    parser.add_argument("--check", action="store_true", help="Dry-run: report drift without writing")
    args = parser.parse_args()

    print(f"{'Checking' if args.check else 'Syncing'} sites from {MANIFEST_PATH}")
    synced, drifted, errors = sync_sites(check_only=args.check)

    if args.check:
        print(f"\nResult: {synced} in sync, {drifted} drifted, {errors} errors")
        if drifted > 0 or errors > 0:
            print("Run 'python3 sites/sync-sites.py' to fix drift.")
            sys.exit(1)
    else:
        print(f"\nResult: {synced + drifted} synced, {errors} errors")
        if errors > 0:
            sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
