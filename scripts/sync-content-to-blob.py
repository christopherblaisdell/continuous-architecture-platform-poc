#!/usr/bin/env python3
"""
Sync high-value architecture content to Azure Blob Storage for AI Search indexing.

Reads from the local workspace and uploads to the 'architecture-content' container
in the configured storage account. Files are organized by type for targeted indexing.

Usage:
    python3 scripts/sync-content-to-blob.py                    # Sync all content
    python3 scripts/sync-content-to-blob.py --dry-run           # Preview what would be uploaded
    python3 scripts/sync-content-to-blob.py --type specs        # Sync only OpenAPI specs
"""

import argparse
import subprocess
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
CONTAINER_NAME = "architecture-content"
RESOURCE_GROUP = "rg-novatrek-ai-poc"

# Content manifest: type → (source glob, blob prefix, description)
CONTENT_TYPES = {
    "specs": {
        "patterns": ["architecture/specs/svc-*.yaml"],
        "prefix": "specs/",
        "description": "OpenAPI specifications (19 services)",
        "priority": "HIGH",
    },
    "decisions": {
        "patterns": ["decisions/ADR-*.md"],
        "prefix": "decisions/",
        "description": "Architecture Decision Records",
        "priority": "HIGH",
    },
    "solutions": {
        "patterns": ["architecture/solutions/*/*.md", "architecture/solutions/*/*/*.md",
                     "architecture/solutions/*/*/*/*.md"],
        "prefix": "solutions/",
        "description": "Solution design documents",
        "priority": "HIGH",
        "preserve_path": True,
    },
    "metadata": {
        "patterns": ["architecture/metadata/*.yaml"],
        "prefix": "metadata/",
        "description": "Capabilities, events, tickets, cross-service calls",
        "priority": "HIGH",
    },
    "events": {
        "patterns": ["architecture/events/*.yaml"],
        "prefix": "events/",
        "description": "AsyncAPI event specifications",
        "priority": "MEDIUM",
    },
    "config": {
        "patterns": ["config/*.yaml"],
        "prefix": "config/",
        "description": "Adventure classification and test standards",
        "priority": "MEDIUM",
    },
    "diagrams": {
        "patterns": [".enriched-puml/*.md"],
        "prefix": "diagrams/",
        "description": "Enriched PlantUML diagrams (sequence, C4, ERD, event-flow)",
        "priority": "HIGH",
    },
    # copilot-instructions.md excluded — too large for single-document indexing
    # Content is covered by the individual ADRs, specs, and metadata files
}


def get_storage_account_name():
    """Retrieve the storage account name from the resource group."""
    result = subprocess.run(
        ["az", "storage", "account", "list",
         "--resource-group", RESOURCE_GROUP,
         "--query", "[0].name", "--output", "tsv"],
        capture_output=True, text=True, check=True
    )
    name = result.stdout.strip()
    if not name:
        print("ERROR: No storage account found in resource group", RESOURCE_GROUP)
        sys.exit(1)
    return name


def get_storage_key(account_name):
    """Retrieve the storage account key."""
    result = subprocess.run(
        ["az", "storage", "account", "keys", "list",
         "--resource-group", RESOURCE_GROUP,
         "--account-name", account_name,
         "--query", "[0].value", "--output", "tsv"],
        capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def resolve_files(patterns):
    """Resolve glob patterns relative to workspace root."""
    files = []
    for pattern in patterns:
        matched = list(WORKSPACE_ROOT.glob(pattern))
        files.extend(sorted(matched))
    return files


def upload_file(local_path, blob_name, account_name, account_key, dry_run=False):
    """Upload a single file to blob storage."""
    if dry_run:
        print(f"  [DRY RUN] {local_path.relative_to(WORKSPACE_ROOT)} → {blob_name}")
        return True

    result = subprocess.run(
        ["az", "storage", "blob", "upload",
         "--account-name", account_name,
         "--account-key", account_key,
         "--container-name", CONTAINER_NAME,
         "--name", blob_name,
         "--file", str(local_path),
         "--overwrite", "true",
         "--output", "none"],
        capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        print(f"  ERROR uploading {blob_name}: {result.stderr.strip()}")
        return False
    return True


def sync_content(content_types=None, dry_run=False):
    """Sync content to blob storage."""
    if not dry_run:
        account_name = get_storage_account_name()
        account_key = get_storage_key(account_name)
        print(f"Storage account: {account_name}")
    else:
        account_name = "<dry-run>"
        account_key = "<dry-run>"
        print("[DRY RUN MODE]")

    print(f"Container: {CONTAINER_NAME}")
    print()

    types_to_sync = content_types or list(CONTENT_TYPES.keys())
    total_files = 0
    total_uploaded = 0

    for type_name in types_to_sync:
        if type_name not in CONTENT_TYPES:
            print(f"WARNING: Unknown content type '{type_name}', skipping")
            continue

        config = CONTENT_TYPES[type_name]
        files = resolve_files(config["patterns"])

        print(f"--- {type_name} ({config['description']}) [{config['priority']}] ---")
        print(f"    Found {len(files)} files")

        for f in files:
            rel_path = f.relative_to(WORKSPACE_ROOT)
            if config.get("preserve_path"):
                blob_name = f"{config['prefix']}{rel_path}"
            else:
                blob_name = f"{config['prefix']}{rel_path.name}"
            total_files += 1

            if upload_file(f, blob_name, account_name, account_key, dry_run):
                total_uploaded += 1

        print()

    print("=" * 60)
    print(f"Total: {total_uploaded}/{total_files} files {'would be ' if dry_run else ''}uploaded")
    print("=" * 60)

    return total_uploaded == total_files


def main():
    parser = argparse.ArgumentParser(description="Sync architecture content to Azure Blob Storage")
    parser.add_argument("--dry-run", action="store_true", help="Preview without uploading")
    parser.add_argument("--type", dest="content_type", help="Sync only a specific content type")
    args = parser.parse_args()

    content_types = [args.content_type] if args.content_type else None

    success = sync_content(content_types=content_types, dry_run=args.dry_run)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
