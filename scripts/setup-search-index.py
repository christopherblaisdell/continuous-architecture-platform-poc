#!/usr/bin/env python3
"""
Create Azure AI Search index, data source, and indexer for architecture content.

This script configures:
1. A data source pointing to the blob storage container
2. A search index with fields for content, metadata, and vector embeddings
3. An indexer that extracts and indexes content from blobs

Usage:
    python3 scripts/setup-search-index.py          # Create everything
    python3 scripts/setup-search-index.py --reset   # Delete and recreate
"""

import argparse
import subprocess
import sys
import json
import urllib.request
import urllib.error

RESOURCE_GROUP = "rg-novatrek-ai-poc"
INDEX_NAME = "architecture-content-index"
DATA_SOURCE_NAME = "architecture-blob-source"
INDEXER_NAME = "architecture-content-indexer"
CONTAINER_NAME = "architecture-content"


def get_search_endpoint():
    """Get the AI Search endpoint."""
    result = subprocess.run(
        ["az", "search", "service", "list",
         "--resource-group", RESOURCE_GROUP,
         "--query", "[0].name", "--output", "tsv"],
        capture_output=True, text=True, check=True
    )
    name = result.stdout.strip()
    if not name:
        print("ERROR: No search service found in resource group", RESOURCE_GROUP)
        sys.exit(1)
    return f"https://{name}.search.windows.net"


def get_search_admin_key():
    """Get the AI Search admin key."""
    # Get search service name first
    result = subprocess.run(
        ["az", "search", "service", "list",
         "--resource-group", RESOURCE_GROUP,
         "--query", "[0].name", "--output", "tsv"],
        capture_output=True, text=True, check=True
    )
    service_name = result.stdout.strip()

    result = subprocess.run(
        ["az", "search", "admin-key", "show",
         "--resource-group", RESOURCE_GROUP,
         "--service-name", service_name,
         "--query", "primaryKey", "--output", "tsv"],
        capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def get_storage_connection_string():
    """Get the storage account connection string."""
    result = subprocess.run(
        ["az", "storage", "account", "list",
         "--resource-group", RESOURCE_GROUP,
         "--query", "[0].name", "--output", "tsv"],
        capture_output=True, text=True, check=True
    )
    account_name = result.stdout.strip()

    result = subprocess.run(
        ["az", "storage", "account", "show-connection-string",
         "--resource-group", RESOURCE_GROUP,
         "--name", account_name,
         "--query", "connectionString", "--output", "tsv"],
        capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def api_call(endpoint, admin_key, method, path, body=None):
    """Make a REST call to the Azure AI Search API."""
    url = f"{endpoint}{path}?api-version=2024-07-01"
    headers = {
        "Content-Type": "application/json",
        "api-key": admin_key,
    }

    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as response:
            if response.status in (200, 201, 204):
                if response.status == 204:
                    return {}
                return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        if e.code == 404 and method == "DELETE":
            return {}  # Already deleted
        print(f"  API Error {e.code}: {error_body[:500]}")
        raise


def create_data_source(endpoint, admin_key, connection_string):
    """Create a blob data source for the indexer."""
    print("--- Creating data source ---")
    body = {
        "name": DATA_SOURCE_NAME,
        "type": "azureblob",
        "credentials": {
            "connectionString": connection_string
        },
        "container": {
            "name": CONTAINER_NAME
        },
        "dataDeletionDetectionPolicy": {
            "@odata.type": "#Microsoft.Azure.Search.SoftDeleteColumnDeletionDetectionPolicy",
            "softDeleteColumnName": "IsDeleted",
            "softDeleteMarkerValue": "true"
        }
    }
    api_call(endpoint, admin_key, "PUT", f"/datasources/{DATA_SOURCE_NAME}", body)
    print(f"  Data source '{DATA_SOURCE_NAME}' created")


def create_index(endpoint, admin_key):
    """Create the search index with fields for architecture content."""
    print("--- Creating search index ---")
    body = {
        "name": INDEX_NAME,
        "fields": [
            {
                "name": "id",
                "type": "Edm.String",
                "key": True,
                "filterable": True
            },
            {
                "name": "content",
                "type": "Edm.String",
                "searchable": True,
                "retrievable": True,
                "analyzer": "standard.lucene"
            },
            {
                "name": "metadata_storage_path",
                "type": "Edm.String",
                "filterable": True,
                "retrievable": True
            },
            {
                "name": "metadata_storage_name",
                "type": "Edm.String",
                "filterable": True,
                "retrievable": True,
                "searchable": True
            },
            {
                "name": "metadata_storage_content_type",
                "type": "Edm.String",
                "filterable": True,
                "retrievable": True
            },
            {
                "name": "metadata_storage_last_modified",
                "type": "Edm.DateTimeOffset",
                "filterable": True,
                "sortable": True,
                "retrievable": True
            },
            {
                "name": "metadata_storage_size",
                "type": "Edm.Int64",
                "filterable": True,
                "retrievable": True
            },
            {
                "name": "file_type",
                "type": "Edm.String",
                "filterable": True,
                "facetable": True,
                "retrievable": True
            }
        ],
        "semantic": {
            "configurations": [
                {
                    "name": "architecture-semantic-config",
                    "prioritizedFields": {
                        "titleField": {
                            "fieldName": "metadata_storage_name"
                        },
                        "prioritizedContentFields": [
                            {
                                "fieldName": "content"
                            }
                        ]
                    }
                }
            ]
        }
    }
    api_call(endpoint, admin_key, "PUT", f"/indexes/{INDEX_NAME}", body)
    print(f"  Index '{INDEX_NAME}' created with semantic config")


def create_indexer(endpoint, admin_key):
    """Create an indexer that populates the index from blob storage."""
    print("--- Creating indexer ---")
    body = {
        "name": INDEXER_NAME,
        "dataSourceName": DATA_SOURCE_NAME,
        "targetIndexName": INDEX_NAME,
        "parameters": {
            "maxFailedItems": 10,
            "configuration": {
                "parsingMode": "default",
                "dataToExtract": "contentAndMetadata",
                "indexStorageMetadataOnlyForOversizedDocuments": True
            }
        },
        "fieldMappings": [
            {
                "sourceFieldName": "metadata_storage_path",
                "targetFieldName": "id",
                "mappingFunction": {
                    "name": "base64Encode"
                }
            }
        ]
    }
    api_call(endpoint, admin_key, "PUT", f"/indexers/{INDEXER_NAME}", body)
    print(f"  Indexer '{INDEXER_NAME}' created")


def run_indexer(endpoint, admin_key):
    """Trigger the indexer to run immediately."""
    print("--- Running indexer ---")
    api_call(endpoint, admin_key, "POST", f"/indexers/{INDEXER_NAME}/run")
    print("  Indexer run triggered")


def get_indexer_status(endpoint, admin_key):
    """Get the indexer status."""
    result = api_call(endpoint, admin_key, "GET", f"/indexers/{INDEXER_NAME}/status")
    last_result = result.get("lastResult") or {}
    status = last_result.get("status", "not yet run")
    doc_count = last_result.get("itemsProcessed", 0)
    error_count = last_result.get("itemsFailed", 0)
    print(f"  Status: {status}, Documents: {doc_count}, Errors: {error_count}")
    return result


def delete_all(endpoint, admin_key):
    """Delete indexer, index, and data source."""
    print("--- Deleting existing resources ---")
    for resource_type, name in [
        ("indexers", INDEXER_NAME),
        ("indexes", INDEX_NAME),
        ("datasources", DATA_SOURCE_NAME)
    ]:
        try:
            api_call(endpoint, admin_key, "DELETE", f"/{resource_type}/{name}")
            print(f"  Deleted {resource_type}/{name}")
        except urllib.error.HTTPError:
            print(f"  {resource_type}/{name} not found (OK)")


def test_search(endpoint, admin_key, query="check-in orchestration"):
    """Run a test search query."""
    print(f"\n--- Test search: '{query}' ---")
    body = {
        "search": query,
        "queryType": "semantic",
        "semanticConfiguration": "architecture-semantic-config",
        "top": 3,
        "select": "metadata_storage_name,content",
    }
    result = api_call(endpoint, admin_key, "POST", f"/indexes/{INDEX_NAME}/docs/search", body)
    hits = result.get("value", [])
    print(f"  Found {len(hits)} results:")
    for hit in hits:
        name = hit.get("metadata_storage_name", "unknown")
        score = hit.get("@search.score", 0)
        content_preview = hit.get("content", "")[:200]
        print(f"    - {name} (score: {score:.2f})")
        print(f"      {content_preview}...")
    return hits


def main():
    parser = argparse.ArgumentParser(description="Set up Azure AI Search index for architecture content")
    parser.add_argument("--reset", action="store_true", help="Delete and recreate all resources")
    parser.add_argument("--test", action="store_true", help="Run test queries only")
    parser.add_argument("--status", action="store_true", help="Check indexer status only")
    args = parser.parse_args()

    endpoint = get_search_endpoint()
    admin_key = get_search_admin_key()
    print(f"Search endpoint: {endpoint}")

    if args.status:
        get_indexer_status(endpoint, admin_key)
        return

    if args.test:
        test_search(endpoint, admin_key, "check-in orchestration pattern")
        test_search(endpoint, admin_key, "ADR-005 default fallback pattern 3")
        test_search(endpoint, admin_key, "svc-check-in events produced")
        return

    if args.reset:
        delete_all(endpoint, admin_key)

    connection_string = get_storage_connection_string()

    create_data_source(endpoint, admin_key, connection_string)
    create_index(endpoint, admin_key)
    create_indexer(endpoint, admin_key)
    run_indexer(endpoint, admin_key)

    print("\n--- Checking indexer status ---")
    get_indexer_status(endpoint, admin_key)

    print("\nSearch index setup complete.")
    print(f"Index: {INDEX_NAME}")
    print(f"Endpoint: {endpoint}")
    print("\nWait 30-60 seconds for indexing, then run:")
    print("  python3 scripts/setup-search-index.py --test")


if __name__ == "__main__":
    main()
