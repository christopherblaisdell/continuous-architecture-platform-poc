#!/usr/bin/env python3
"""
RAG Proxy: Chat Completions proxy with Azure AI Search context injection.

Receives standard OpenAI Chat Completions requests (from Copilot BYOK),
queries Azure AI Search for relevant architecture content, injects the
results into the system message, and forwards to Azure OpenAI.

This implements Architecture C from BYOK-CONTEXT-INJECTION-PLAN.md.
It serves as the immediate working implementation while the Foundry Agent
(Architecture B) is developed.

Usage:
    # Start the proxy server
    python3 scripts/rag-proxy.py

    # Configure Copilot BYOK to point to the proxy
    # baseUrl: http://localhost:8081/openai/v1

Environment variables:
    AZURE_OPENAI_ENDPOINT     - Azure OpenAI endpoint URL
    AZURE_OPENAI_API_KEY      - Azure OpenAI API key
    AZURE_SEARCH_ENDPOINT     - Azure AI Search endpoint URL
    AZURE_SEARCH_API_KEY      - Azure AI Search admin key
    AZURE_SEARCH_INDEX        - Search index name (default: architecture-content-index)
    RAG_PROXY_PORT            - Proxy port (default: 8081)
    RAG_TOP_K                 - Number of search results to inject (default: 5)
"""

import http.server
import json
import os
import sys
import urllib.error
import urllib.request
from urllib.parse import urlparse, parse_qs

# Configuration from environment
OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY", "")
SEARCH_ENDPOINT = os.environ.get("AZURE_SEARCH_ENDPOINT", "")
SEARCH_API_KEY = os.environ.get("AZURE_SEARCH_API_KEY", "")
SEARCH_INDEX = os.environ.get("AZURE_SEARCH_INDEX", "architecture-content-index")
PROXY_PORT = int(os.environ.get("RAG_PROXY_PORT", "8081"))
TOP_K = int(os.environ.get("RAG_TOP_K", "5"))

# Context injection template
CONTEXT_PREFIX = """[ARCHITECTURE CONTEXT — Retrieved from NovaTrek architecture knowledge base]
The following architecture documents are relevant to your query. Use them to ground your response.
Cite the source file when referencing specific information.

"""

CONTEXT_SUFFIX = """
[END ARCHITECTURE CONTEXT]

"""


def search_architecture(query):
    """Query Azure AI Search for relevant architecture content."""
    if not SEARCH_ENDPOINT or not SEARCH_API_KEY:
        return []

    url = f"{SEARCH_ENDPOINT}/indexes/{SEARCH_INDEX}/docs/search?api-version=2024-07-01"
    body = {
        "search": query,
        "queryType": "semantic",
        "semanticConfiguration": "architecture-semantic-config",
        "top": TOP_K,
        "select": "metadata_storage_name,content",
    }

    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("api-key", SEARCH_API_KEY)

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("value", [])
    except urllib.error.HTTPError as e:
        print(f"[RAG] Search error {e.code}: {e.read().decode('utf-8')[:200]}", file=sys.stderr)
        return []
    except (urllib.error.URLError, OSError) as e:
        print(f"[RAG] Search exception: {e}", file=sys.stderr)
        return []


def extract_query(messages):
    """Extract the user's query from the messages array for search."""
    # Use the last user message as the search query
    for msg in reversed(messages):
        if msg.get("role") == "user":
            content = msg.get("content", "")
            if isinstance(content, list):
                # Handle multimodal content
                for part in content:
                    if isinstance(part, dict) and part.get("type") == "text":
                        return part.get("text", "")
            return str(content)
    return ""


def build_context_block(search_results):
    """Build the context injection block from search results."""
    if not search_results:
        return ""

    context = CONTEXT_PREFIX
    for i, hit in enumerate(search_results, 1):
        name = hit.get("metadata_storage_name", "unknown")
        content = hit.get("content", "")
        score = hit.get("@search.score", 0)

        # Truncate content to avoid overwhelming the context window
        max_chunk = 2000
        if len(content) > max_chunk:
            content = content[:max_chunk] + "... [truncated]"

        context += f"--- Source {i}: {name} (relevance: {score:.2f}) ---\n"
        context += f"{content}\n\n"

    context += CONTEXT_SUFFIX
    return context


def inject_context(messages, context_block):
    """Inject the context block into the messages array."""
    if not context_block:
        return messages

    enriched = list(messages)

    # Find or create system message
    if enriched and enriched[0].get("role") == "system":
        enriched[0] = dict(enriched[0])
        enriched[0]["content"] = enriched[0].get("content", "") + "\n\n" + context_block
    else:
        enriched.insert(0, {"role": "system", "content": context_block})

    return enriched


def forward_to_openai(path, _headers, body):
    """Forward the enriched request to Azure OpenAI."""
    # Reconstruct the URL for Azure OpenAI
    # Incoming: /openai/v1/chat/completions or /openai/deployments/{model}/chat/completions
    # Forward to: {OPENAI_ENDPOINT}openai/deployments/gpt-4o/chat/completions?api-version=...

    parsed = urlparse(path)
    query_params = parse_qs(parsed.query)

    # Determine the target path
    target_path = parsed.path
    if "/v1/chat/completions" in target_path:
        # Copilot BYOK sends to /openai/v1/chat/completions
        # Route to the gpt-4o deployment
        model = body.get("model", "gpt-4o")
        target_path = f"/openai/deployments/{model}/chat/completions"

    api_version = query_params.get("api-version", ["2024-10-01-preview"])[0]
    url = f"{OPENAI_ENDPOINT.rstrip('/')}{target_path}?api-version={api_version}"

    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("api-key", OPENAI_API_KEY)

    try:
        with urllib.request.urlopen(req) as response:
            response_body = response.read()
            return response.status, dict(response.headers), response_body
    except urllib.error.HTTPError as e:
        error_body = e.read()
        return e.code, dict(e.headers) if hasattr(e, 'headers') else {}, error_body


class RAGProxyHandler(http.server.BaseHTTPRequestHandler):
    """HTTP handler for the RAG proxy."""

    def do_GET(self):
        """Handle GET — return models list for Copilot discovery."""
        if "/models" in self.path:
            response = {
                "object": "list",
                "data": [
                    {
                        "id": "gpt-4o",
                        "object": "model",
                        "created": 1700000000,
                        "owned_by": "azure-novatrek-rag",
                    }
                ]
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        """Handle POST — intercept chat completions, inject context, forward."""
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)

        try:
            body = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error": "Invalid JSON"}')
            return

        messages = body.get("messages", [])

        # Extract query and search for relevant context
        query = extract_query(messages)
        if query:
            print(f"[RAG] Query: {query[:100]}...", file=sys.stderr)
            search_results = search_architecture(query)
            print(f"[RAG] Found {len(search_results)} results", file=sys.stderr)

            # Build and inject context
            context_block = build_context_block(search_results)
            body["messages"] = inject_context(messages, context_block)

        # Forward to Azure OpenAI
        status, resp_headers, resp_body = forward_to_openai(
            self.path, dict(self.headers), body
        )

        self.send_response(status)
        for key, value in resp_headers.items():
            if key.lower() not in ("transfer-encoding", "connection", "content-length"):
                self.send_header(key, value)
        self.send_header("Content-Length", str(len(resp_body)))
        self.end_headers()
        self.wfile.write(resp_body)

    def log_message(self, fmt, *args):  # noqa: A002
        """Log to stderr with timestamp."""
        print(f"[RAG Proxy] {args[0]}", file=sys.stderr)


def main():
    """Start the RAG proxy server."""
    missing = []
    if not OPENAI_ENDPOINT:
        missing.append("AZURE_OPENAI_ENDPOINT")
    if not OPENAI_API_KEY:
        missing.append("AZURE_OPENAI_API_KEY")
    if not SEARCH_ENDPOINT:
        missing.append("AZURE_SEARCH_ENDPOINT")
    if not SEARCH_API_KEY:
        missing.append("AZURE_SEARCH_API_KEY")

    if missing:
        print(f"ERROR: Missing environment variables: {', '.join(missing)}", file=sys.stderr)
        print("\nSet them with:", file=sys.stderr)
        print("  export AZURE_OPENAI_ENDPOINT=https://oai-novatrek-poc.openai.azure.com/", file=sys.stderr)
        print("  export AZURE_OPENAI_API_KEY=<key>", file=sys.stderr)
        print("  export AZURE_SEARCH_ENDPOINT=https://srch-novatrek-poc.search.windows.net", file=sys.stderr)
        print("  export AZURE_SEARCH_API_KEY=<key>", file=sys.stderr)
        sys.exit(1)

    server = http.server.HTTPServer(("0.0.0.0", PROXY_PORT), RAGProxyHandler)
    print(f"RAG Proxy listening on http://localhost:{PROXY_PORT}", file=sys.stderr)
    print(f"OpenAI backend: {OPENAI_ENDPOINT}", file=sys.stderr)
    print(f"Search backend: {SEARCH_ENDPOINT}", file=sys.stderr)
    print(f"Search index: {SEARCH_INDEX}", file=sys.stderr)
    print(f"Top K results: {TOP_K}", file=sys.stderr)
    print(f"\nConfigure Copilot BYOK baseUrl: http://localhost:{PROXY_PORT}/openai/v1", file=sys.stderr)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down RAG proxy", file=sys.stderr)
        server.server_close()


if __name__ == "__main__":
    main()
