#!/usr/bin/env python3
"""
Foundry IQ Proxy: Translates OpenAI Chat Completions API to Azure AI Search
Knowledge Base retrieve API.

Receives standard Chat Completions requests (from Copilot BYOK), forwards
the user query to the Foundry IQ knowledge base (agentic retrieval), and
returns the grounded answer in Chat Completions response format.

This implements Architecture B from BYOK-CONTEXT-INJECTION-PLAN.md.

Usage:
    python3 scripts/foundry-proxy.py

    # Configure Copilot BYOK to point to:
    # baseUrl: http://localhost:8082/openai/v1

Environment variables:
    AZURE_SEARCH_ENDPOINT     - Azure AI Search endpoint (e.g., https://srch-novatrek-poc.search.windows.net)
    AZURE_SEARCH_API_KEY      - Azure AI Search admin key
    KNOWLEDGE_BASE_NAME       - Knowledge base name (default: architecture-knowledge-base)
    FOUNDRY_PROXY_PORT        - Proxy port (default: 8082)
"""

import http.server
import json
import os
import sys
import time
import urllib.error
import urllib.request

SEARCH_ENDPOINT = os.environ.get("AZURE_SEARCH_ENDPOINT", "")
SEARCH_API_KEY = os.environ.get("AZURE_SEARCH_API_KEY", "")
KB_NAME = os.environ.get("KNOWLEDGE_BASE_NAME", "architecture-knowledge-base")
PROXY_PORT = int(os.environ.get("FOUNDRY_PROXY_PORT", "8082"))
API_VERSION = "2025-11-01-preview"


def extract_query(messages):
    """Extract the last user message as the query."""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            content = msg.get("content", "")
            if isinstance(content, list):
                for part in content:
                    if isinstance(part, dict) and part.get("type") == "text":
                        return part.get("text", "")
            return str(content)
    return ""


def retrieve_from_kb(query):
    """Call the Foundry IQ knowledge base retrieve API."""
    url = (
        f"{SEARCH_ENDPOINT}/knowledgebases('{KB_NAME}')"
        f"/retrieve?api-version={API_VERSION}"
    )
    body = {
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": query}]}
        ]
    }

    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("api-key", SEARCH_API_KEY)

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"[Foundry] Retrieve error {e.code}: {error_body[:300]}", file=sys.stderr)
        return {"error": e.code, "body": error_body}
    except (urllib.error.URLError, OSError) as e:
        print(f"[Foundry] Retrieve exception: {e}", file=sys.stderr)
        return {"error": 502, "body": str(e)}


def extract_answer(retrieve_result):
    """Extract the answer text from a retrieve response."""
    if "error" in retrieve_result:
        return f"Error querying knowledge base: {retrieve_result.get('body', 'unknown error')}"

    for resp in retrieve_result.get("response", []):
        for content in resp.get("content", []):
            if content.get("type") == "text":
                return content.get("text", "")
    return "No relevant architecture content found for this query."


def extract_citations(retrieve_result):
    """Extract source citations from retrieve activity."""
    citations = []
    activity = retrieve_result.get("activity", [])
    if isinstance(activity, list):
        for act in activity:
            if isinstance(act, dict):
                for ref in act.get("references", []):
                    if isinstance(ref, dict):
                        citations.append(ref.get("title", ref.get("id", "unknown")))
    elif isinstance(activity, dict):
        for ref in activity.get("references", []):
            if isinstance(ref, dict):
                citations.append(ref.get("title", ref.get("id", "unknown")))
    return citations


def to_chat_completion(answer, model="gpt-4o"):
    """Wrap the answer in a Chat Completions response envelope."""
    return {
        "id": f"foundry-{int(time.time())}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": answer,
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        },
    }


class FoundryProxyHandler(http.server.BaseHTTPRequestHandler):
    """Translates Chat Completions → Foundry IQ retrieve."""

    def do_GET(self):
        """Handle GET — models list for Copilot discovery."""
        if "/models" in self.path:
            response = {
                "object": "list",
                "data": [
                    {
                        "id": "gpt-4o",
                        "object": "model",
                        "created": 1700000000,
                        "owned_by": "novatrek-foundry-iq",
                    }
                ],
            }
            self._send_json(200, response)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        """Handle POST — translate chat completions to retrieve."""
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)

        try:
            body = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Invalid JSON"})
            return

        messages = body.get("messages", [])
        query = extract_query(messages)

        if not query:
            self._send_json(400, {"error": "No user message found"})
            return

        print(f"[Foundry] Query: {query[:120]}", file=sys.stderr)

        # Call Foundry IQ knowledge base
        result = retrieve_from_kb(query)
        answer = extract_answer(result)
        citations = extract_citations(result)

        if citations:
            print(f"[Foundry] Citations: {', '.join(citations[:5])}", file=sys.stderr)

        model = body.get("model", "gpt-4o")
        response = to_chat_completion(answer, model)
        self._send_json(200, response)

    def _send_json(self, status, data):
        """Send a JSON response."""
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"[Foundry Proxy] {args[0]}", file=sys.stderr)


def main():
    if not SEARCH_ENDPOINT or not SEARCH_API_KEY:
        print("ERROR: Set AZURE_SEARCH_ENDPOINT and AZURE_SEARCH_API_KEY", file=sys.stderr)
        sys.exit(1)

    server = http.server.HTTPServer(("0.0.0.0", PROXY_PORT), FoundryProxyHandler)
    print(f"Foundry IQ Proxy listening on port {PROXY_PORT}", file=sys.stderr)
    print(f"Knowledge base: {KB_NAME}", file=sys.stderr)
    print(f"Search endpoint: {SEARCH_ENDPOINT}", file=sys.stderr)
    print(f"Configure BYOK baseUrl: http://localhost:{PROXY_PORT}/openai/v1", file=sys.stderr)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down", file=sys.stderr)
        server.shutdown()


if __name__ == "__main__":
    main()
