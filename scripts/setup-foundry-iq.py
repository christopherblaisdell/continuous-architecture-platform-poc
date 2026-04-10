#!/usr/bin/env python3
"""
Set up Foundry IQ: Knowledge Source + Knowledge Base on Azure AI Search.

This creates the agentic retrieval pipeline on top of the existing
architecture-content-index. The knowledge base exposes an MCP endpoint
that Foundry Agent Service can connect to.

Usage:
    python3 scripts/setup-foundry-iq.py              # Create everything
    python3 scripts/setup-foundry-iq.py --status      # Check status
    python3 scripts/setup-foundry-iq.py --test        # Run test retrieval
    python3 scripts/setup-foundry-iq.py --delete      # Delete KB + KS
"""

import argparse
import json
import subprocess
import sys
import urllib.error
import urllib.request

RESOURCE_GROUP = "rg-novatrek-ai-poc"
INDEX_NAME = "architecture-content-index"
KNOWLEDGE_SOURCE_NAME = "architecture-knowledge-source"
KNOWLEDGE_BASE_NAME = "architecture-knowledge-base"
API_VERSION = "2025-11-01-preview"


def get_search_endpoint():
    result = subprocess.run(
        ["az", "search", "service", "list",
         "--resource-group", RESOURCE_GROUP,
         "--query", "[0].name", "--output", "tsv"],
        capture_output=True, text=True, check=True
    )
    name = result.stdout.strip()
    if not name:
        print("ERROR: No search service found")
        sys.exit(1)
    return f"https://{name}.search.windows.net"


def get_search_key():
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


def get_openai_endpoint():
    result = subprocess.run(
        ["az", "cognitiveservices", "account", "show",
         "--resource-group", RESOURCE_GROUP,
         "--name", "oai-novatrek-poc",
         "--query", "properties.endpoint", "--output", "tsv"],
        capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def get_openai_key():
    result = subprocess.run(
        ["az", "cognitiveservices", "account", "keys", "list",
         "--resource-group", RESOURCE_GROUP,
         "--name", "oai-novatrek-poc",
         "--query", "key1", "--output", "tsv"],
        capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def api_call(endpoint, key, method, path, body=None):
    """Make a REST call to AI Search using OData URL format."""
    url = f"{endpoint}/{path}?api-version={API_VERSION}"
    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("api-key", key)
    req.add_header("Prefer", "return=representation")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status == 204:
                return None
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        if e.code == 404:
            return None
        print(f"  ERROR {e.code}: {error_body[:500]}")
        return {"error": e.code, "body": error_body}


def create_knowledge_source(endpoint, key):
    """Create a searchIndex knowledge source wrapping our existing index."""
    print(f"Creating knowledge source: {KNOWLEDGE_SOURCE_NAME}")

    # CRITICAL: Use minimal config — only searchIndexName.
    # Adding sourceDataFields, searchFields, or semanticConfigurationName
    # causes "Failed to query search index" errors in agentic retrieval.
    body = {
        "name": KNOWLEDGE_SOURCE_NAME,
        "description": "NovaTrek Adventures architecture content — OpenAPI specs, ADRs, solution designs, metadata YAML, event specs, and configuration files for 19 microservices.",
        "kind": "searchIndex",
        "searchIndexParameters": {
            "searchIndexName": INDEX_NAME
        }
    }

    result = api_call(endpoint, key, "PUT",
                      f"knowledgesources('{KNOWLEDGE_SOURCE_NAME}')", body)
    if result and "error" not in result:
        print(f"  Knowledge source '{KNOWLEDGE_SOURCE_NAME}' created successfully")
    elif result and "error" in result:
        print("  Failed to create knowledge source")
        return False
    return True


def create_knowledge_base(endpoint, key, openai_endpoint, openai_key):
    """Create a knowledge base linking the knowledge source to GPT-4o."""
    print(f"Creating knowledge base: {KNOWLEDGE_BASE_NAME}")

    body = {
        "name": KNOWLEDGE_BASE_NAME,
        "description": "Architecture knowledge base for the NovaTrek Adventures continuous architecture platform.",
        "knowledgeSources": [
            {"name": KNOWLEDGE_SOURCE_NAME}
        ],
        "models": [
            {
                "kind": "azureOpenAI",
                "azureOpenAIParameters": {
                    "resourceUri": openai_endpoint.rstrip("/"),
                    "deploymentId": "gpt-4o",
                    "apiKey": openai_key,
                    "modelName": "gpt-4o"
                }
            }
        ],
        "retrievalReasoningEffort": {"kind": "low"},
        "outputMode": "answerSynthesis",
        "retrievalInstructions": "This knowledge base contains architecture artifacts for NovaTrek Adventures, a fictional outdoor adventure company with 19 microservices. Prioritize OpenAPI specs for API questions, ADRs for design rationale, and solution designs for implementation context.",
        "answerInstructions": "Cite the source document name when answering. Be concise and specific. Reference specific endpoints, fields, or decisions by name."
    }

    result = api_call(endpoint, key, "PUT",
                      f"knowledgebases('{KNOWLEDGE_BASE_NAME}')", body)
    if result and "error" not in result:
        print(f"  Knowledge base '{KNOWLEDGE_BASE_NAME}' created successfully")
        mcp_url = f"{endpoint}/knowledgebases('{KNOWLEDGE_BASE_NAME}')/mcp?api-version={API_VERSION}"
        print(f"  MCP endpoint: {mcp_url}")
    elif result and "error" in result:
        print("  Failed to create knowledge base")
        return False
    return True


def check_status(endpoint, key):
    """List knowledge sources and knowledge bases."""
    print("=== Knowledge Sources ===")
    result = api_call(endpoint, key, "GET", "knowledgesources")
    if result and "value" in result:
        for ks in result["value"]:
            print(f"  - {ks['name']} (type: {ks.get('type', '?')})")
    else:
        print("  (none)")

    print("\n=== Knowledge Bases ===")
    result = api_call(endpoint, key, "GET", "knowledgebases")
    if result and "value" in result:
        for kb in result["value"]:
            print(f"  - {kb['name']}")
            if "knowledgeSources" in kb:
                for ks in kb["knowledgeSources"]:
                    print(f"    → source: {ks['name']}")
            mcp_url = f"{endpoint}/knowledgebases('{kb['name']}')/mcp?api-version={API_VERSION}"
            print(f"    → MCP: {mcp_url}")
    else:
        print("  (none)")


def test_retrieval(endpoint, key):
    """Run a test retrieval query against the knowledge base."""
    print(f"Testing retrieval from: {KNOWLEDGE_BASE_NAME}")

    queries = [
        "What is the check-in orchestration pattern?",
        "What does ADR-005 say about default fallback?",
        "What events does svc-check-in produce?"
    ]

    for query in queries:
        print(f"\n--- Query: {query}")
        body = {
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": query}]}
            ],
            "retrievalReasoningEffort": {"kind": "low"}
        }

        result = api_call(endpoint, key, "POST",
                          f"knowledgebases('{KNOWLEDGE_BASE_NAME}')/retrieve", body)
        if result and "error" not in result:
            # Extract response text
            if "response" in result:
                for resp in result["response"]:
                    if "content" in resp:
                        for c in resp["content"]:
                            if c.get("type") == "text":
                                text = c.get("text", "")
                                print(f"    Answer: {text[:300]}...")
            # Show references if any
            if "activity" in result:
                act = result["activity"]
                if "references" in act:
                    print(f"    References: {len(act['references'])} documents")
                    for ref in act["references"][:3]:
                        print(f"      - {ref.get('title', ref.get('id', '?'))}")
        elif result and "error" in result:
            print(f"    Error: {result['body'][:200]}")
        else:
            print("    No result")


def delete_all(endpoint, key):
    """Delete knowledge base and knowledge source."""
    print(f"Deleting knowledge base: {KNOWLEDGE_BASE_NAME}")
    api_call(endpoint, key, "DELETE", f"knowledgebases('{KNOWLEDGE_BASE_NAME}')")
    print(f"Deleting knowledge source: {KNOWLEDGE_SOURCE_NAME}")
    api_call(endpoint, key, "DELETE", f"knowledgesources('{KNOWLEDGE_SOURCE_NAME}')")
    print("Done")


def main():
    parser = argparse.ArgumentParser(description="Set up Foundry IQ on Azure AI Search")
    parser.add_argument("--status", action="store_true", help="Check status")
    parser.add_argument("--test", action="store_true", help="Run test retrieval")
    parser.add_argument("--delete", action="store_true", help="Delete KB + KS")
    args = parser.parse_args()

    endpoint = get_search_endpoint()
    key = get_search_key()

    if args.status:
        check_status(endpoint, key)
        return

    if args.test:
        test_retrieval(endpoint, key)
        return

    if args.delete:
        delete_all(endpoint, key)
        return

    # Create everything
    openai_endpoint = get_openai_endpoint()
    openai_key = get_openai_key()

    print(f"Search endpoint: {endpoint}")
    print(f"OpenAI endpoint: {openai_endpoint}")
    print(f"Index: {INDEX_NAME}")
    print()

    if not create_knowledge_source(endpoint, key):
        sys.exit(1)

    if not create_knowledge_base(endpoint, key, openai_endpoint, openai_key):
        sys.exit(1)

    print("\n=== Foundry IQ Setup Complete ===")
    mcp_url = f"{endpoint}/knowledgebases('{KNOWLEDGE_BASE_NAME}')/mcp?api-version={API_VERSION}"
    print(f"MCP endpoint: {mcp_url}")
    print(f"\nTest with: python3 scripts/setup-foundry-iq.py --test")


if __name__ == "__main__":
    main()
