# Implementation Plan: Workspace-Wide Vector Database with Kong AI Gateway

| | |
|-----------|-------|
| **Author** | Christopher Blaisdell |
| **Date** | 2026-03-14 |
| **Status** | PROPOSED |
| **Relates To** | [Vector DB / RAG Feasibility Analysis](VECTOR-DB-RAG-FEASIBILITY-ANALYSIS.md) |
| **Phase** | Phase 2 - AI Workflow Enhancement |
| **See Also** | [Context Window Utilization Analysis](CONTEXT-WINDOW-UTILIZATION-ANALYSIS.md), [Deep Research: Copilot vs Kong+Roo Economics](DEEP-RESEARCH-1.md) |

---

## Executive Summary

This plan describes how to build a workspace-wide vector database that indexes the entire NovaTrek architecture workspace and exposes it to AI coding assistants (Roo Code, Copilot, Continue.dev) via MCP protocol, with Kong AI Gateway managing all LLM and embedding API traffic for cost control, observability, prompt injection of retrieved context, and multi-provider failover.

**The key insight:** Kong AI Gateway cannot *be* the vector database or retrieval engine, but it is the correct place to manage the AI API traffic that powers the system. The architecture places each component in its proper layer:

| Layer | Component | Responsibility |
|-------|-----------|----------------|
| **Storage** | ChromaDB (local) | Vector storage, similarity search, metadata filtering |
| **Indexing** | Python chunking pipeline | Format-aware document splitting, embedding generation |
| **Retrieval** | MCP Server (Python) | Query interface for AI agents via MCP protocol |
| **AI Gateway** | Kong AI Gateway | Route embedding + LLM calls, cost tracking, prompt decoration, guardrails |
| **Inference** | OpenAI / Anthropic / Ollama | Embedding models + LLM reasoning |
| **Client** | Roo Code / VS Code | AI assistant consuming the MCP tool |

---

## Architecture

### System Context (C4 Level 1)

```
                    +------------------+
                    |    Architect      |
                    |  (VS Code User)  |
                    +--------+---------+
                             |
                    +--------v---------+
                    |    Roo Code /    |
                    |  Continue.dev /  |
                    |     Copilot      |
                    +--------+---------+
                             | MCP Protocol
                    +--------v---------+
                    | MCP Vector Server|
                    |  (Python, local) |
                    +---+----+----+----+
                        |    |    |
            +-----------+    |    +------------+
            |                |                 |
   +--------v-------+  +----v--------+  +-----v----------+
   |   ChromaDB     |  | Kong AI GW  |  |  File Watcher  |
   | (local vector  |  | (API proxy) |  |  (fswatch /    |
   |   database)    |  +----+--------+  |   watchdog)    |
   +----------------+       |           +----------------+
                        +---+---+
                        |       |
               +--------v+  +--v----------+
               | Embedding|  | LLM Inference|
               | Provider |  | Provider     |
               | (OpenAI/ |  | (Anthropic/  |
               |  Ollama) |  |  OpenAI)     |
               +----------+  +-------------+
```

### Data Flow

**Indexing Flow (background, on file change):**

```
File saved in workspace
  -> File watcher detects change
  -> Chunking pipeline splits file (format-aware)
  -> Chunks sent to Kong AI Gateway /embeddings endpoint
  -> Kong routes to embedding provider (OpenAI or Ollama)
  -> Kong logs: model, tokens, cost, latency
  -> Embedding vectors returned
  -> ChromaDB upserts vectors with metadata (file path, line range, content type)
```

**Query Flow (on-demand, during AI agent reasoning):**

```
AI agent calls MCP tool: search("which services call svc-guest-profiles?")
  -> MCP server embeds query via Kong AI Gateway /embeddings
  -> MCP server queries ChromaDB for top-k similar chunks
  -> MCP server returns ranked results with file paths + content snippets
  -> AI agent uses retrieved context in its reasoning
  -> AI agent's LLM call routes through Kong AI Gateway /chat/completions
  -> Kong logs: full request cost, latency, model, token counts
```

### Kong AI Gateway's Role (Specifically)

Kong AI does not perform retrieval. It provides five critical infrastructure services for this pipeline:

| Service | How Kong AI Delivers It |
|---------|------------------------|
| **Unified embedding API** | Kong's AI Proxy plugin exposes a single `/embeddings` endpoint. Backend can be switched between OpenAI, Cohere, or local Ollama without changing any client code |
| **Cost tracking** | Every embedding call and every LLM inference call passes through Kong. The AI Observability plugin logs token counts, model name, latency, and estimated cost per request. This gives exact cost-per-index-run and cost-per-query metrics |
| **Prompt decoration** | Kong's AI Prompt Decorator plugin can inject a system prompt prefix into every LLM call (e.g., "You have access to a workspace vector search tool. Use it before reading files manually."). This steers agent behavior without modifying the AI assistant's configuration |
| **Rate limiting** | Kong's Rate Limiting plugin prevents runaway re-indexing from consuming excessive embedding API quota (e.g., max 1,000 embedding requests per minute) |
| **Multi-provider failover** | If OpenAI's embedding endpoint is down, Kong automatically routes to the fallback provider (Cohere or local Ollama) with no client-side changes |

---

## Component Design

### Component 1: Chunking Pipeline

**Purpose:** Split workspace files into semantically meaningful chunks suitable for embedding.

**Location:** `scripts/vector-db/chunker.py`

**Format-aware chunking rules:**

| File Type | Chunking Strategy | Expected Chunk Size |
|-----------|------------------|-------------------|
| Markdown (`.md`) | Split by H2 (`##`) headers. Each section becomes one chunk. Front matter (title, metadata table) stays attached to the first chunk | 200-1500 tokens |
| YAML — OpenAPI specs | Split by path + operation. Each `paths./endpoint.method` block becomes one chunk. `info` and `components/schemas` are separate chunks | 100-800 tokens |
| YAML — metadata files | Split by top-level key. Each capability, ticket, or event definition becomes one chunk | 50-400 tokens |
| AsyncAPI (`.yaml`) | Split by channel. Each channel + message schema becomes one chunk | 100-500 tokens |
| Java (`.java`) | Split by class method. Each method (with its Javadoc) becomes one chunk. Class-level annotations and imports stay with the first chunk | 100-1000 tokens |
| PlantUML (`.puml`) | Entire file as one chunk (these are small) | 50-200 tokens |
| ADR (`.md`) | Split by MADR section (Context, Decision Drivers, Options, Outcome, Consequences) | 100-500 tokens |

**Metadata per chunk:**

```python
{
    "file_path": "architecture/specs/svc-check-in.yaml",
    "file_type": "openapi",
    "chunk_type": "endpoint",           # endpoint | schema | section | method | definition
    "section_heading": "POST /check-ins",
    "line_start": 45,
    "line_end": 98,
    "service": "svc-check-in",          # extracted from path or spec content
    "domain": "Operations",             # from DOMAINS mapping
    "last_modified": "2026-03-12T14:30:00Z"
}
```

**Implementation:**

```python
# scripts/vector-db/chunker.py

import os
import yaml
import re
from dataclasses import dataclass
from typing import Generator
from pathlib import Path

@dataclass
class Chunk:
    content: str
    file_path: str
    file_type: str
    chunk_type: str
    section_heading: str
    line_start: int
    line_end: int
    metadata: dict

SKIP_DIRS = {'.git', 'node_modules', '.venv', 'site', '__pycache__', '.mypy_cache'}
SKIP_FILES = {'.DS_Store', '.gitignore', '.env'}

def chunk_markdown(file_path: str, content: str) -> Generator[Chunk, None, None]:
    """Split Markdown by H2 headers."""
    lines = content.split('\n')
    current_section = []
    current_heading = "Preamble"
    section_start = 1

    for i, line in enumerate(lines, 1):
        if line.startswith('## ') and current_section:
            yield Chunk(
                content='\n'.join(current_section),
                file_path=file_path,
                file_type='markdown',
                chunk_type='section',
                section_heading=current_heading,
                line_start=section_start,
                line_end=i - 1,
                metadata={}
            )
            current_section = [line]
            current_heading = line.lstrip('# ').strip()
            section_start = i
        else:
            current_section.append(line)

    if current_section:
        yield Chunk(
            content='\n'.join(current_section),
            file_path=file_path,
            file_type='markdown',
            chunk_type='section',
            section_heading=current_heading,
            line_start=section_start,
            line_end=len(lines),
            metadata={}
        )

def chunk_openapi(file_path: str, content: str) -> Generator[Chunk, None, None]:
    """Split OpenAPI YAML by path+operation."""
    try:
        spec = yaml.safe_load(content)
    except yaml.YAMLError:
        yield Chunk(
            content=content,
            file_path=file_path,
            file_type='openapi',
            chunk_type='full_file',
            section_heading=os.path.basename(file_path),
            line_start=1,
            line_end=content.count('\n') + 1,
            metadata={}
        )
        return

    # Info block
    if 'info' in spec:
        info_yaml = yaml.dump({'info': spec['info']}, default_flow_style=False)
        yield Chunk(
            content=info_yaml,
            file_path=file_path,
            file_type='openapi',
            chunk_type='info',
            section_heading=spec.get('info', {}).get('title', 'API Info'),
            line_start=1,
            line_end=1,
            metadata={'service': _extract_service(file_path)}
        )

    # Each path+operation
    for path, methods in (spec.get('paths') or {}).items():
        for method, operation in methods.items():
            if method.startswith('x-'):
                continue
            op_yaml = yaml.dump(
                {path: {method: operation}},
                default_flow_style=False
            )
            summary = operation.get('summary', f'{method.upper()} {path}')
            yield Chunk(
                content=op_yaml,
                file_path=file_path,
                file_type='openapi',
                chunk_type='endpoint',
                section_heading=f'{method.upper()} {path} -- {summary}',
                line_start=1,
                line_end=1,
                metadata={'service': _extract_service(file_path)}
            )

    # Schemas
    schemas = (spec.get('components') or {}).get('schemas') or {}
    for name, schema in schemas.items():
        schema_yaml = yaml.dump({name: schema}, default_flow_style=False)
        yield Chunk(
            content=schema_yaml,
            file_path=file_path,
            file_type='openapi',
            chunk_type='schema',
            section_heading=f'Schema: {name}',
            line_start=1,
            line_end=1,
            metadata={'service': _extract_service(file_path)}
        )

def chunk_java(file_path: str, content: str) -> Generator[Chunk, None, None]:
    """Split Java by method boundaries."""
    # Simplified: split on method-level patterns
    lines = content.split('\n')
    method_pattern = re.compile(
        r'^\s+(public|private|protected)\s+\S+\s+\w+\s*\('
    )
    current_block = []
    block_start = 1
    current_heading = os.path.basename(file_path)

    for i, line in enumerate(lines, 1):
        if method_pattern.match(line) and current_block:
            yield Chunk(
                content='\n'.join(current_block),
                file_path=file_path,
                file_type='java',
                chunk_type='method',
                section_heading=current_heading,
                line_start=block_start,
                line_end=i - 1,
                metadata={}
            )
            current_block = [line]
            current_heading = line.strip()
            block_start = i
        else:
            current_block.append(line)

    if current_block:
        yield Chunk(
            content='\n'.join(current_block),
            file_path=file_path,
            file_type='java',
            chunk_type='method',
            section_heading=current_heading,
            line_start=block_start,
            line_end=len(lines),
            metadata={}
        )

def _extract_service(file_path: str) -> str:
    """Extract service name from file path."""
    parts = Path(file_path).parts
    for part in parts:
        if part.startswith('svc-'):
            return part
    stem = Path(file_path).stem
    if stem.startswith('svc-'):
        return stem
    return ''

def chunk_workspace(workspace_root: str) -> Generator[Chunk, None, None]:
    """Walk workspace and yield all chunks."""
    for dirpath, dirnames, filenames in os.walk(workspace_root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for filename in filenames:
            if filename in SKIP_FILES:
                continue

            file_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(file_path, workspace_root)

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except (PermissionError, IsADirectoryError):
                continue

            if not content.strip():
                continue

            ext = Path(filename).suffix.lower()

            if ext == '.md':
                yield from chunk_markdown(rel_path, content)
            elif ext in ('.yaml', '.yml'):
                # Detect OpenAPI vs plain YAML
                if 'openapi:' in content[:500]:
                    yield from chunk_openapi(rel_path, content)
                else:
                    # Plain YAML: single chunk
                    yield Chunk(
                        content=content,
                        file_path=rel_path,
                        file_type='yaml',
                        chunk_type='full_file',
                        section_heading=filename,
                        line_start=1,
                        line_end=content.count('\n') + 1,
                        metadata={}
                    )
            elif ext == '.java':
                yield from chunk_java(rel_path, content)
            elif ext in ('.puml', '.plantuml'):
                yield Chunk(
                    content=content,
                    file_path=rel_path,
                    file_type='plantuml',
                    chunk_type='full_file',
                    section_heading=filename,
                    line_start=1,
                    line_end=content.count('\n') + 1,
                    metadata={}
                )
```

### Component 2: ChromaDB Vector Store

**Purpose:** Store embeddings locally with metadata filtering and similarity search.

**Location:** `scripts/vector-db/store.py`

**Why ChromaDB:**

| Criterion | ChromaDB | LanceDB | Qdrant | FAISS |
|-----------|----------|---------|--------|-------|
| Local-first (no server needed) | Yes (persistent mode) | Yes | Needs Docker | Yes |
| Metadata filtering | Yes | Yes | Yes | No |
| Python SDK quality | Excellent | Good | Good | Minimal |
| Incremental upsert | Yes (by ID) | Yes | Yes | Manual |
| Hybrid search (vector + keyword) | Yes (with `where_document`) | No | Yes | No |
| Disk footprint | <100 MB for this workspace | <50 MB | ~200 MB (Docker) | <50 MB |
| Setup complexity | `pip install chromadb` | `pip install lancedb` | Docker container | `pip install faiss-cpu` |

**Implementation:**

```python
# scripts/vector-db/store.py

import chromadb
import hashlib
from pathlib import Path

DB_PATH = ".vector-db"
COLLECTION_NAME = "novatrek-workspace"

def get_collection():
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

def chunk_id(file_path: str, line_start: int, section_heading: str) -> str:
    """Deterministic ID for upsert idempotency."""
    raw = f"{file_path}:{line_start}:{section_heading}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

def upsert_chunks(chunks, embeddings):
    """Upsert chunk embeddings into ChromaDB."""
    collection = get_collection()
    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:
        ids.append(chunk_id(chunk.file_path, chunk.line_start, chunk.section_heading))
        documents.append(chunk.content)
        metadatas.append({
            "file_path": chunk.file_path,
            "file_type": chunk.file_type,
            "chunk_type": chunk.chunk_type,
            "section_heading": chunk.section_heading,
            "line_start": chunk.line_start,
            "line_end": chunk.line_end,
            **chunk.metadata
        })

    # ChromaDB handles batching internally
    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )

def query(embedding, top_k=5, where_filter=None):
    """Query ChromaDB for similar chunks."""
    collection = get_collection()
    kwargs = {
        "query_embeddings": [embedding],
        "n_results": top_k,
        "include": ["documents", "metadatas", "distances"]
    }
    if where_filter:
        kwargs["where"] = where_filter

    return collection.query(**kwargs)

def delete_by_file(file_path: str):
    """Remove all chunks for a file (before re-indexing)."""
    collection = get_collection()
    collection.delete(where={"file_path": file_path})

def get_stats():
    """Return collection statistics."""
    collection = get_collection()
    return {
        "total_chunks": collection.count(),
        "collection": COLLECTION_NAME
    }
```

### Component 3: Kong AI Gateway (Docker)

**Purpose:** Central proxy for all embedding and LLM API calls. Provides cost tracking, rate limiting, prompt decoration, and multi-provider failover.

**Location:** Added to `docker-compose.yml`

**Docker Compose addition:**

```yaml
  # ---------------------------------------------------------------------------
  # Kong AI Gateway (manages embedding + LLM API traffic)
  # ---------------------------------------------------------------------------
  kong:
    image: kong/kong-gateway:3.9
    container_name: novatrek-kong-ai
    environment:
      KONG_DATABASE: "off"
      KONG_DECLARATIVE_CONFIG: /etc/kong/kong.yml
      KONG_PROXY_LISTEN: "0.0.0.0:8000"
      KONG_ADMIN_LISTEN: "0.0.0.0:8001"
      KONG_LOG_LEVEL: info
    ports:
      - "8000:8000"   # Proxy (AI API calls go here)
      - "8001:8001"   # Admin API
    volumes:
      - ./config/kong/kong.yml:/etc/kong/kong.yml:ro
    healthcheck:
      test: ["CMD", "kong", "health"]
      interval: 10s
      timeout: 5s
      retries: 5
```

**Kong declarative config (`config/kong/kong.yml`):**

```yaml
_format_version: "3.0"

services:
  # ===== Embedding Provider: OpenAI =====
  - name: openai-embeddings
    url: https://api.openai.com/v1
    routes:
      - name: embeddings-route
        paths:
          - /ai/embeddings
        strip_path: true
    plugins:
      - name: ai-proxy
        config:
          route_type: llm/v1/embeddings
          auth:
            header_name: Authorization
            header_value: "Bearer ${OPENAI_API_KEY}"
          model:
            provider: openai
            name: text-embedding-3-small
      - name: rate-limiting
        config:
          minute: 500
          policy: local
      - name: ai-prompt-decorator
        config:
          prepend:
            - role: system
              content: >
                You are indexing an architecture workspace for the NovaTrek
                Adventures platform. Embeddings are used for semantic search
                over OpenAPI specs, ADRs, solution designs, and service metadata.

  # ===== Embedding Provider: Ollama (local fallback) =====
  - name: ollama-embeddings
    url: http://host.docker.internal:11434/v1
    routes:
      - name: embeddings-local-route
        paths:
          - /ai/embeddings/local
        strip_path: true
    plugins:
      - name: rate-limiting
        config:
          minute: 1000
          policy: local

  # ===== LLM Inference: Anthropic (for Roo Code RAG-augmented calls) =====
  - name: anthropic-chat
    url: https://api.anthropic.com/v1
    routes:
      - name: chat-route
        paths:
          - /ai/chat
        strip_path: true
    plugins:
      - name: ai-proxy
        config:
          route_type: llm/v1/chat
          auth:
            header_name: x-api-key
            header_value: "${ANTHROPIC_API_KEY}"
          model:
            provider: anthropic
            name: claude-sonnet-4-20250514
      - name: rate-limiting
        config:
          minute: 100
          policy: local
      - name: ai-prompt-decorator
        config:
          prepend:
            - role: system
              content: >
                You have access to a workspace vector search tool via MCP.
                When investigating architecture questions, query the vector
                database before reading files directly. The workspace contains
                19 microservice OpenAPI specs, 11 ADRs, event schemas, and
                solution designs for the NovaTrek Adventures platform.

  # ===== LLM Inference: OpenAI (fallback) =====
  - name: openai-chat
    url: https://api.openai.com/v1
    routes:
      - name: chat-fallback-route
        paths:
          - /ai/chat/openai
        strip_path: true
    plugins:
      - name: ai-proxy
        config:
          route_type: llm/v1/chat
          auth:
            header_name: Authorization
            header_value: "Bearer ${OPENAI_API_KEY}"
          model:
            provider: openai
            name: gpt-4.1
      - name: rate-limiting
        config:
          minute: 100
          policy: local
```

**What Kong AI tracks for every request:**

```
{
  "request.model": "text-embedding-3-small",
  "request.provider": "openai",
  "response.tokens.input": 1523,
  "response.tokens.output": 0,
  "response.latency_ms": 142,
  "response.cost_usd": 0.0000305,
  "consumer": "vector-indexer",
  "route": "embeddings-route",
  "timestamp": "2026-03-14T15:30:42Z"
}
```

### Component 4: Embedding Client (via Kong AI)

**Purpose:** Generate embeddings by calling Kong AI Gateway's unified `/ai/embeddings` endpoint.

**Location:** `scripts/vector-db/embedder.py`

```python
# scripts/vector-db/embedder.py

import os
import requests
from typing import Optional

KONG_BASE_URL = os.environ.get("KONG_AI_URL", "http://localhost:8000")

def embed_texts(texts: list[str], provider: str = "openai") -> list[list[float]]:
    """Generate embeddings via Kong AI Gateway."""
    if provider == "local":
        url = f"{KONG_BASE_URL}/ai/embeddings/local"
        payload = {
            "model": "nomic-embed-text",
            "input": texts
        }
    else:
        url = f"{KONG_BASE_URL}/ai/embeddings"
        payload = {
            "model": "text-embedding-3-small",
            "input": texts
        }

    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()

    data = response.json()
    return [item["embedding"] for item in data["data"]]

def embed_query(query: str, provider: str = "openai") -> list[float]:
    """Embed a single query string."""
    return embed_texts([query], provider=provider)[0]
```

### Component 5: MCP Server

**Purpose:** Expose vector search as an MCP tool that Roo Code (and other MCP-compatible clients) can call autonomously.

**Location:** `scripts/vector-db/mcp_server.py`

**MCP Tool Definition:**

```json
{
  "name": "workspace_search",
  "description": "Semantic search across the entire NovaTrek architecture workspace. Searches OpenAPI specs, ADRs, solution designs, event schemas, capability metadata, and Java source code. Returns the top-k most relevant chunks with file paths and line numbers. Use this BEFORE reading files to find relevant context efficiently.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
      },
      "top_k": {
        "type": "integer",
        "default": 5,
        "description": "Number of results to return (1-20)"
      },
      "file_type": {
        "type": "string",
        "enum": ["markdown", "openapi", "yaml", "java", "plantuml"],
        "description": "Optional filter to restrict search to a specific file type"
      },
      "service": {
        "type": "string",
        "description": "Optional filter to restrict search to a specific service (e.g., 'svc-check-in')"
      }
    },
    "required": ["query"]
  }
}
```

**Implementation:**

```python
# scripts/vector-db/mcp_server.py

import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from store import query as vector_query, get_stats
from embedder import embed_query

app = Server("novatrek-workspace-search")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="workspace_search",
            description=(
                "Semantic search across the entire NovaTrek architecture workspace. "
                "Searches OpenAPI specs, ADRs, solution designs, event schemas, "
                "capability metadata, and Java source code. Returns the top-k most "
                "relevant chunks with file paths and line numbers. "
                "Use this BEFORE reading files to find relevant context efficiently."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language search query"
                    },
                    "top_k": {
                        "type": "integer",
                        "default": 5,
                        "description": "Number of results to return (1-20)"
                    },
                    "file_type": {
                        "type": "string",
                        "enum": ["markdown", "openapi", "yaml", "java", "plantuml"],
                        "description": "Optional: restrict to file type"
                    },
                    "service": {
                        "type": "string",
                        "description": "Optional: restrict to service (e.g., svc-check-in)"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="workspace_index_stats",
            description="Get statistics about the workspace vector index",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "workspace_search":
        query_text = arguments["query"]
        top_k = min(arguments.get("top_k", 5), 20)

        # Build metadata filter
        where_filter = {}
        if "file_type" in arguments:
            where_filter["file_type"] = arguments["file_type"]
        if "service" in arguments:
            where_filter["service"] = arguments["service"]

        # Embed query via Kong AI Gateway
        query_embedding = embed_query(query_text)

        # Search ChromaDB
        results = vector_query(
            embedding=query_embedding,
            top_k=top_k,
            where_filter=where_filter if where_filter else None
        )

        # Format results
        output_lines = [f"## Search Results for: \"{query_text}\"\n"]
        for i, (doc, meta, dist) in enumerate(zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        )):
            score = 1 - dist  # cosine distance to similarity
            output_lines.append(
                f"### Result {i+1} (similarity: {score:.3f})\n"
                f"**File:** {meta['file_path']} "
                f"(lines {meta['line_start']}-{meta['line_end']})\n"
                f"**Type:** {meta['file_type']} / {meta['chunk_type']}\n"
                f"**Section:** {meta['section_heading']}\n\n"
                f"```\n{doc[:500]}{'...' if len(doc) > 500 else ''}\n```\n"
            )

        return [TextContent(type="text", text='\n'.join(output_lines))]

    elif name == "workspace_index_stats":
        stats = get_stats()
        return [TextContent(
            type="text",
            text=json.dumps(stats, indent=2)
        )]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())
```

### Component 6: File Watcher (Incremental Re-indexing)

**Purpose:** Detect file changes and re-index only the modified files.

**Location:** `scripts/vector-db/watcher.py`

```python
# scripts/vector-db/watcher.py

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

from chunker import chunk_markdown, chunk_openapi, chunk_java, SKIP_DIRS
from embedder import embed_texts
from store import upsert_chunks, delete_by_file

WATCH_EXTENSIONS = {'.md', '.yaml', '.yml', '.java', '.puml'}

class WorkspaceHandler(FileSystemEventHandler):
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root

    def on_modified(self, event):
        if event.is_directory:
            return
        self._reindex(event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return
        self._reindex(event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        rel_path = str(Path(event.src_path).relative_to(self.workspace_root))
        delete_by_file(rel_path)

    def _reindex(self, abs_path: str):
        path = Path(abs_path)
        if path.suffix not in WATCH_EXTENSIONS:
            return
        if any(skip in path.parts for skip in SKIP_DIRS):
            return

        rel_path = str(path.relative_to(self.workspace_root))

        try:
            content = path.read_text(encoding='utf-8', errors='ignore')
        except (PermissionError, FileNotFoundError):
            return

        if not content.strip():
            return

        # Delete old chunks for this file
        delete_by_file(rel_path)

        # Re-chunk
        if path.suffix == '.md':
            chunks = list(chunk_markdown(rel_path, content))
        elif path.suffix in ('.yaml', '.yml') and 'openapi:' in content[:500]:
            chunks = list(chunk_openapi(rel_path, content))
        elif path.suffix == '.java':
            chunks = list(chunk_java(rel_path, content))
        else:
            return

        if not chunks:
            return

        # Embed via Kong AI
        texts = [c.content for c in chunks]
        embeddings = embed_texts(texts)

        # Upsert
        upsert_chunks(chunks, embeddings)
        print(f"Re-indexed {rel_path}: {len(chunks)} chunks")

def watch(workspace_root: str):
    handler = WorkspaceHandler(workspace_root)
    observer = Observer()
    observer.schedule(handler, workspace_root, recursive=True)
    observer.start()
    print(f"Watching {workspace_root} for changes...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```

### Component 7: Index Runner (Full Re-index)

**Purpose:** One-shot full workspace indexing.

**Location:** `scripts/vector-db/index.py`

```python
# scripts/vector-db/index.py

import sys
import time
from chunker import chunk_workspace
from embedder import embed_texts
from store import upsert_chunks, get_stats

BATCH_SIZE = 50  # Chunks per embedding API call

def index_workspace(workspace_root: str):
    print(f"Indexing workspace: {workspace_root}")
    start = time.time()

    all_chunks = list(chunk_workspace(workspace_root))
    print(f"Chunked {len(all_chunks)} chunks from workspace")

    # Batch embed
    for i in range(0, len(all_chunks), BATCH_SIZE):
        batch = all_chunks[i:i + BATCH_SIZE]
        texts = [c.content for c in batch]
        embeddings = embed_texts(texts)
        upsert_chunks(batch, embeddings)
        print(f"  Indexed batch {i//BATCH_SIZE + 1}/{(len(all_chunks) + BATCH_SIZE - 1)//BATCH_SIZE}")

    elapsed = time.time() - start
    stats = get_stats()
    print(f"Done. {stats['total_chunks']} chunks indexed in {elapsed:.1f}s")

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    index_workspace(root)
```

---

## Roo Code MCP Configuration

Add to Roo Code's MCP settings (`.roo/mcp.json` or via Roo Code settings UI):

```json
{
  "mcpServers": {
    "novatrek-workspace": {
      "command": "python3",
      "args": ["scripts/vector-db/mcp_server.py"],
      "env": {
        "KONG_AI_URL": "http://localhost:8000"
      }
    }
  }
}
```

Once configured, Roo Code will see `workspace_search` and `workspace_index_stats` as available tools and can call them autonomously during any task.

---

## Directory Structure

```
scripts/vector-db/
├── README.md                 # Setup and usage instructions
├── requirements.txt          # Python dependencies
├── chunker.py                # Format-aware document chunking
├── store.py                  # ChromaDB vector storage (supports Qdrant backend)
├── embedder.py               # Embedding client (via Kong AI Gateway)
├── mcp_server.py             # MCP server for Roo Code integration
├── watcher.py                # File watcher for incremental re-indexing
├── reindex-file.py           # Single-file re-indexer (called by VS Code extension)
├── index.py                  # Full workspace indexer
└── test_chunker.py           # Unit tests for chunking logic

config/kong/
└── kong.yml                  # Kong AI Gateway declarative configuration

.vscode/
└── tasks.json                # Auto-start watcher on workspace open

.githooks/
├── post-merge                # Auto-reindex after git pull
└── post-checkout             # Auto-reindex after branch switch

.vector-db/                   # ChromaDB persistent storage (gitignored)
```

---

## Dependencies

**Python (`scripts/vector-db/requirements.txt`):**

```
chromadb>=0.5,<1.0
mcp>=1.0,<2.0
watchdog>=4.0,<5.0
requests>=2.31,<3.0
pyyaml>=6.0,<7.0
```

**Docker:**

- Kong Gateway 3.9+ (from `kong/kong-gateway:3.9`)
- Ollama (optional, for local embeddings): `docker run -d -p 11434:11434 ollama/ollama`

**API Keys (in `.env`):**

```bash
export OPENAI_API_KEY=sk-...          # For text-embedding-3-small
export ANTHROPIC_API_KEY=sk-ant-...    # For Claude (if routing LLM calls through Kong)
```

---

## Implementation Phases

### Phase A: Foundation (Day 1-2)

| Step | Task | Validation |
|------|------|------------|
| A.1 | Create `scripts/vector-db/` directory and `requirements.txt` | `pip install -r requirements.txt` succeeds |
| A.2 | Implement `chunker.py` with Markdown + YAML + Java splitters | Unit test: chunk a sample OpenAPI spec, verify endpoint-level splitting |
| A.3 | Implement `store.py` with ChromaDB persistent storage | Unit test: upsert 10 chunks, query by embedding, verify top-k results |
| A.4 | Implement `embedder.py` with direct OpenAI calls (no Kong yet) | Verify: embed a test string, get 1536-dim vector back |
| A.5 | Implement `index.py` full workspace indexer | Run against workspace, verify chunk count and ChromaDB stats |
| A.6 | Add `.vector-db/` to `.gitignore` | Verify directory not tracked |

**Milestone:** Full workspace indexed into local ChromaDB. Can query from Python REPL.

### Phase B: MCP Server (Day 2-3)

| Step | Task | Validation |
|------|------|------------|
| B.1 | Implement `mcp_server.py` with `workspace_search` and `workspace_index_stats` tools | MCP inspector tool: connect and list tools |
| B.2 | Configure Roo Code MCP connection (`.roo/mcp.json`) | Roo Code shows "novatrek-workspace" in MCP server list |
| B.3 | Test end-to-end: ask Roo Code "which services handle guest check-in?" and verify it calls `workspace_search` | Agent log shows MCP tool call + relevant results |
| B.4 | Tune top-k and chunk size based on retrieval quality | Manual review of 10 test queries |

**Milestone:** Roo Code can autonomously search the workspace vector DB during any task.

### Phase C: Kong AI Gateway (Day 3-4)

| Step | Task | Validation |
|------|------|------------|
| C.1 | Add Kong to `docker-compose.yml` | `docker compose up kong` starts successfully |
| C.2 | Create `config/kong/kong.yml` with embedding routes | `curl http://localhost:8001/services` returns configured services |
| C.3 | Update `embedder.py` to route through Kong (`http://localhost:8000/ai/embeddings`) | Embeddings still work; Kong access log shows requests |
| C.4 | Add AI Prompt Decorator plugin for agent steering | LLM calls via Kong include injected system prompt |
| C.5 | Add Rate Limiting plugin | Verify 429 response when exceeding limit |
| C.6 | Add cost tracking (AI Observability or custom logging plugin) | Kong logs show token counts and estimated cost per request |
| C.7 | Configure Ollama as local fallback | When OpenAI key removed, embeddings still work via Ollama route |

**Milestone:** All AI API traffic flows through Kong with observability, cost tracking, and rate limiting.

### Phase D: File Watching + Polish (Day 4-5)

| Step | Task | Validation |
|------|------|------------|
| D.1 | Implement `watcher.py` with watchdog | Modify a YAML file, verify ChromaDB re-indexes within 5 seconds |
| D.2 | Add Makefile targets for common operations | `make vector-index`, `make vector-watch`, `make vector-stats` |
| D.3 | Write `scripts/vector-db/README.md` with setup and usage instructions | New team member can set up from scratch following README |
| D.4 | Add unit tests for chunker edge cases (empty files, malformed YAML, deeply nested Markdown) | All tests pass |
| D.5 | Performance test: time full re-index, measure query latency | Full index < 60s, query latency < 500ms |

**Milestone:** Production-ready system with automatic re-indexing and developer documentation.

### Phase E: Optimization (Day 5-6, optional)

| Step | Task | Validation |
|------|------|------------|
| E.1 | Add hybrid search (vector + BM25 keyword matching) | Structural queries ("services calling svc-check-in") return better results |
| E.2 | Add chunk overlap (50-token overlap between adjacent chunks) | Boundary-spanning concepts are not lost |
| E.3 | Add file-type boosting (weight OpenAPI specs higher for API queries) | API-related queries prioritize spec content |
| E.4 | Export Kong cost metrics to a dashboard | Weekly cost report for embedding + LLM calls |
| E.5 | Configure Continue.dev as alternative MCP client | Continue.dev can also query the same vector DB |

---

## Makefile Additions

```makefile
# ===========================================================================
# Vector Database (Workspace Search)
# ===========================================================================

vector-index: ## Full re-index of workspace into vector DB
	python3 scripts/vector-db/index.py .

vector-watch: ## Watch workspace and re-index on file changes
	python3 scripts/vector-db/watcher.py

vector-stats: ## Show vector DB statistics
	python3 -c "from scripts.vector_db.store import get_stats; import json; print(json.dumps(get_stats(), indent=2))"

vector-search: ## Search vector DB: make vector-search Q="your query"
	python3 -c "from scripts.vector_db.embedder import embed_query; from scripts.vector_db.store import query; import json; r=query(embed_query('$(Q)')); [print(f'{m[\"file_path\"]}:{m[\"line_start\"]} ({m[\"section_heading\"]})') for m in r['metadatas'][0]]"

kong-up: ## Start Kong AI Gateway
	docker compose up kong -d

kong-logs: ## Tail Kong AI Gateway logs
	docker compose logs kong -f

kong-routes: ## List Kong AI routes
	curl -s http://localhost:8001/routes | python3 -m json.tool
```

---

## Cost Projections

### Initial Full Index

| Metric | OpenAI Embeddings | Local Ollama |
|--------|-------------------|-------------|
| Estimated chunks | ~3,000-5,000 | Same |
| Avg tokens per chunk | ~300 | Same |
| Total tokens | ~1,000,000-1,500,000 | Same |
| Embedding cost | $0.01-0.03 | $0.00 |
| Time (API) | 30-60 seconds | 2-5 minutes |

### Daily Operations (Incremental)

| Metric | OpenAI Embeddings | Local Ollama |
|--------|-------------------|-------------|
| Files modified per day | ~20-50 | Same |
| Chunks re-indexed | ~100-300 | Same |
| Daily embedding cost | < $0.001 | $0.00 |
| Query cost per search | ~$0.000002 | $0.00 |

### Kong AI Gateway Overhead

| Metric | Value |
|--------|-------|
| Docker image size | ~150 MB |
| Memory usage | ~128-256 MB |
| CPU overhead per request | < 1 ms (proxy latency) |
| Added latency per request | 2-5 ms |

### Total Monthly Cost

| Configuration | Monthly Cost |
|---------------|-------------|
| OpenAI embeddings + Kong (local Docker) | ~$0.50 - $1.00 |
| Ollama local embeddings + Kong (local Docker) | $0.00 (compute only) |
| For comparison: GitHub Copilot (includes @workspace RAG) | $39.00/month |

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| ChromaDB data corruption on crash | Low | Medium | `.vector-db/` is ephemeral -- full re-index recovers in < 60 seconds |
| Stale embeddings return wrong context | Medium | Medium | File watcher for auto-reindex; `vector-index` Makefile target for manual rebuild |
| Kong AI Gateway adds complexity for solo architect | Medium | Low | Kong is optional -- `embedder.py` can call OpenAI directly by setting `KONG_AI_URL=""` |
| Chunking splits critical context across boundaries | Medium | Medium | 50-token overlap in Phase E; tune chunk boundaries for domain-specific patterns |
| Roo Code ignores MCP tool (doesn't call `workspace_search`) | Low | High | MCP tool description explicitly instructs "use this BEFORE reading files"; add to Roo Code system prompt |
| OpenAI API rate limits during bulk re-index | Low | Low | Kong rate limiting prevents bursts; batch size of 50 stays well under limits |
| Embedding model version change alters vector space | Low | High | Re-index entire workspace when embedding model changes (< 60 seconds) |

---

## Multi-Architect Deployment

### Per-Architect Resource Model

Every component in this plan runs locally. Each architect who opens the workspace gets their own independent instance:

| Component | Per-architect? | Why |
|-----------|---------------|-----|
| ChromaDB (`.vector-db/`) | Yes -- local disk | ChromaDB runs as an embedded library, not a server. Each architect's checkout has its own `.vector-db/` directory (gitignored). No shared state |
| File watcher | Yes -- local process | Each architect runs `make vector-watch` in their VS Code terminal. It watches their working copy for changes |
| Kong AI Gateway | Yes or shared | If running locally via Docker Compose (`make kong-up`), each architect runs their own. Could be shared via a team-hosted instance |
| MCP server | Yes -- local process | Roo Code spawns the MCP server as a child process (configured in `.roo/mcp.json`). It runs per VS Code window |
| Embeddings | Shared API key | All architects hit the same OpenAI/Ollama endpoint (via Kong or directly). Cost is pooled |

### Practical Workflow Per Architect

```
Architect opens VS Code
  -> Roo Code auto-starts MCP server (from .roo/mcp.json config)
  -> MCP server connects to local ChromaDB

First time (or after git pull with many changes):
  -> Run: make vector-index          # ~60 seconds, full re-index

Ongoing:
  -> Run: make vector-watch          # background, re-indexes on save
  -> (Or: VS Code task that auto-starts watcher on workspace open)
```

### Scaling to Multiple Architects

The core limitation is that every architect maintains their own local vector DB. Three approaches address this:

#### Approach A: VS Code Task Auto-Start (Low Effort)

Add a `.vscode/tasks.json` task that auto-runs the watcher on workspace open. Each architect still has a local DB, but the watcher starts automatically with no manual step.

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Vector DB: Watch for Changes",
      "type": "shell",
      "command": "python3",
      "args": ["scripts/vector-db/watcher.py"],
      "isBackground": true,
      "problemMatcher": [],
      "runOptions": {
        "runOn": "folderOpen"
      },
      "presentation": {
        "reveal": "silent",
        "panel": "dedicated"
      }
    },
    {
      "label": "Vector DB: Full Re-index",
      "type": "shell",
      "command": "python3",
      "args": ["scripts/vector-db/index.py", "."],
      "problemMatcher": [],
      "presentation": {
        "reveal": "always"
      }
    }
  ]
}
```

**Effort:** 30 minutes. **Trade-off:** Still per-architect, still needs initial index after clone.

#### Approach B: Git Hook Indexing (Low Effort)

Add `post-checkout` and `post-merge` git hooks that trigger a full re-index after every `git pull` or branch switch. Combined with the file watcher for live changes.

```bash
#!/bin/sh
# .githooks/post-merge
# Auto-reindex vector DB after git pull

if [ -d "scripts/vector-db" ] && command -v python3 >/dev/null 2>&1; then
    echo "Re-indexing workspace vector DB..."
    python3 scripts/vector-db/index.py . &
fi
```

```bash
#!/bin/sh
# .githooks/post-checkout
# Auto-reindex vector DB after branch switch

# Only run for branch checkouts (flag=1), not file checkouts (flag=0)
if [ "$3" = "1" ] && [ -d "scripts/vector-db" ] && command -v python3 >/dev/null 2>&1; then
    echo "Re-indexing workspace vector DB..."
    python3 scripts/vector-db/index.py . &
fi
```

Configure git to use the hooks directory:

```bash
git config core.hooksPath .githooks
```

**Effort:** 1 hour. **Trade-off:** Adds ~60 seconds (background) to every pull. Still local per architect.

#### Approach C: Shared Qdrant Server (Medium Effort)

Replace embedded ChromaDB with a team-hosted Qdrant instance. All architects query the same index. A CI job re-indexes on every push to `main`.

```yaml
# Addition to docker-compose.yml (or team-hosted VM)
  qdrant:
    image: qdrant/qdrant:v1.12
    container_name: novatrek-qdrant
    ports:
      - "6333:6333"   # REST API
      - "6334:6334"   # gRPC
    volumes:
      - qdrant-data:/qdrant/storage
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/healthz"]
      interval: 10s
      timeout: 5s
      retries: 5
```

CI job (GitHub Actions):

```yaml
# .github/workflows/vector-index.yml
name: Reindex Vector DB
on:
  push:
    branches: [main]
    paths:
      - 'architecture/**'
      - 'decisions/**'
      - 'portal/docs/**'
      - 'config/**'
      - 'services/**'

jobs:
  reindex:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r scripts/vector-db/requirements.txt
      - run: python3 scripts/vector-db/index.py .
        env:
          QDRANT_URL: ${{ vars.QDRANT_URL }}
          KONG_AI_URL: ${{ vars.KONG_AI_URL }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

The `store.py` module would need a backend switch:

```python
BACKEND = os.environ.get("VECTOR_BACKEND", "chromadb")  # chromadb | qdrant

if BACKEND == "qdrant":
    from qdrant_client import QdrantClient
    client = QdrantClient(url=os.environ.get("QDRANT_URL", "http://localhost:6333"))
else:
    import chromadb
    client = chromadb.PersistentClient(path=".vector-db")
```

**Effort:** 1-2 days. **Trade-off:** Requires network access and shared infrastructure. Single source of truth -- no per-architect index staleness.

### Multi-Architect Recommendation

| Scenario | Approach | Why |
|----------|----------|-----|
| Solo architect (current state) | A + B | VS Code task auto-starts watcher; git hooks rebuild after pulls. Zero manual steps after initial setup |
| Team of 2-5 architects | A + B | Same as solo. Local DBs are acceptable when each architect's workspace diverges (feature branches) |
| Team of 5+ or CI-driven workflows | C | Shared Qdrant eliminates "every architect maintains their own DB" problem. CI-driven indexing guarantees freshness on `main` |

---

## VS Code Extension Analysis

### Could This Be a VS Code Extension?

**Yes.** VS Code's extension API provides every primitive needed:

| Requirement | VS Code Extension API |
|-------------|----------------------|
| Watch file changes | `vscode.workspace.onDidSaveTextDocument`, `vscode.workspace.onDidCreateFiles`, `vscode.workspace.onDidDeleteFiles` |
| Read workspace files | `vscode.workspace.fs.readFile`, `vscode.workspace.findFiles` |
| Background processing | Extension activation on workspace open (`onStartupFinished`) |
| Status bar feedback | `vscode.window.createStatusBarItem` -- show "Indexed 3,412 chunks" |
| Configuration | `package.json` contributes settings -- embedding provider, Kong URL, chunk size |
| MCP server hosting | Extension can spawn the MCP server as a child process, or expose tools directly |
| Shared state across windows | `globalState` for cross-window persistence |

A VS Code extension would eliminate every manual step:

- No `make vector-index` -- the extension auto-indexes on activation
- No `make vector-watch` -- file events are native to the extension lifecycle
- No `.roo/mcp.json` manual config -- the extension registers the MCP server automatically
- No separate terminal process -- everything runs inside the extension host

### Should It Be a VS Code Extension?

**For a solo architect or small team: No. For a distributable product: Yes.**

#### Arguments FOR a VS Code Extension

| Advantage | Why it matters |
|-----------|---------------|
| **Zero-touch setup** | Install extension, open workspace, done. No pip install, no Docker, no Makefile targets, no background terminals |
| **Native file watching** | VS Code's file system events are more reliable than `watchdog` -- they fire for git operations, refactors, and external tools that modify files |
| **UX integration** | Status bar showing index health, progress notifications during re-index, command palette commands (`>Workspace Search: Reindex`, `>Workspace Search: Query`) |
| **Per-workspace activation** | Extension activates only for workspaces that need it (via `activationEvents`). No wasted resources |
| **Portable** | Any architect installs the extension from the marketplace (or a `.vsix` file). No Python environment, no requirements.txt compatibility issues |
| **Lifecycle management** | Extension deactivates cleanly when VS Code closes -- no orphaned watcher processes |

#### Arguments AGAINST a VS Code Extension

| Disadvantage | Why it matters more |
|-------------|-------------------|
| **Development effort is 3-5x higher** | A VS Code extension requires TypeScript, webpack bundling, extension manifest, activation events, contribution points, state management. The Python scripts in this plan are ~400 lines total. An equivalent extension is ~1,500-2,500 lines of TypeScript + build config |
| **Dependency bundling is painful** | ChromaDB is a Python library. A VS Code extension runs in Node.js. Options: (a) bundle a ChromaDB Python subprocess, (b) use a JavaScript vector DB like `vectra` or `hnswlib-node`, (c) HTTP calls to a ChromaDB server in Docker. None are as clean as `pip install chromadb` |
| **Embedding model integration** | The extension would need to either bundle an embedding model (huge), call an external API (requires API key config in VS Code settings), or shell out to Python/Ollama. The Python script approach handles this natively |
| **Testing and debugging** | Extension debugging requires launching a separate VS Code Extension Development Host. Python scripts can be tested with `pytest` in 2 seconds |
| **Maintenance burden** | VS Code API changes between versions. Extension marketplace publishing has review requirements. Python scripts just work |
| **Already solved by Continue.dev** | Continue.dev already IS this VS Code extension -- open source, local codebase indexing, multiple LLM backends. Building a custom extension duplicates their work |

#### What a Custom Extension Gives You That Continue.dev Doesn't

| Requirement | Continue.dev | Custom Extension |
|------------|-------------|-----------------|
| Workspace-wide semantic search | Yes (`@codebase`) | Yes |
| Format-aware chunking (OpenAPI, YAML) | Partial -- generic chunking | Full control |
| Kong AI Gateway routing | No | Yes |
| Cost tracking per query | No | Yes (via Kong) |
| MCP tool exposure for Roo Code | No -- Continue.dev is its own chat | Yes |
| NovaTrek-specific metadata enrichment | No | Yes |

The only unique value a custom extension provides over Continue.dev is **Kong AI integration** and **MCP tool exposure for Roo Code**.

### Recommended Hybrid Path: Thin Extension Wrapper

If extension-level UX is desired, build a **thin VS Code extension wrapper** around the existing Python scripts rather than rewriting everything in TypeScript:

```
VS Code Extension (TypeScript, ~200 lines)
  |-- onStartupFinished -> spawn `python3 scripts/vector-db/index.py`
  |-- onDidSaveTextDocument -> spawn `python3 scripts/vector-db/reindex-file.py <path>`
  |-- Status bar item -> reads `.vector-db/stats.json`
  |-- Command: "Reindex Workspace" -> spawns full `index.py`
  +-- Extension settings -> Kong URL, embedding provider, top-k

Python scripts (unchanged from this plan)
  |-- chunker.py, store.py, embedder.py -> actual work
  |-- mcp_server.py -> Roo Code integration
  +-- index.py, watcher.py -> invoked by extension
```

This gives:

- Extension UX (auto-start, status bar, command palette)
- Python implementation (ChromaDB native, easy to test, ~400 lines)
- No webpack/bundling complexity for the heavy logic
- Extension is a thin shell -- trivial to maintain

### Extension Decision Matrix

| If you are... | Do this | Why |
|---------------|---------|-----|
| Solo architect wanting RAG now | **Use the Python scripts from this plan** | Working in days, not weeks. `make vector-index && make vector-watch` is 2 commands |
| Solo architect who wants polish | **Install Continue.dev** | Zero development. `@codebase` works out of the box |
| Building for a team of 3-5 | **Python scripts + thin extension wrapper** | Auto-start eliminates "forgot to run the watcher" failure mode. Kong routing gives cost visibility |
| Building a product for distribution | **Full VS Code extension** | Only if packaging for dozens of users who cannot be expected to run Python scripts |

### Updated Implementation Phase (Phase F)

If the thin extension wrapper is pursued, add after Phase E:

### Phase F: VS Code Extension Wrapper (Day 6-7, optional)

| Step | Task | Validation |
|------|------|------------|
| F.1 | Scaffold VS Code extension with `yo code` generator | Extension loads in Extension Development Host |
| F.2 | Add `onStartupFinished` activation that spawns `python3 scripts/vector-db/watcher.py` as a child process | Opening workspace starts watcher automatically |
| F.3 | Add `onDidSaveTextDocument` handler that calls `python3 scripts/vector-db/reindex-file.py <path>` | Saving a file triggers re-index within 2 seconds |
| F.4 | Add status bar item that shows chunk count from `.vector-db/stats.json` | Status bar displays "Vector DB: 3,412 chunks" |
| F.5 | Add command palette: "Workspace Search: Full Reindex" | Command triggers `index.py` with progress notification |
| F.6 | Add extension settings for Kong URL and embedding provider | Settings appear under "Workspace Search" in VS Code settings |
| F.7 | Package as `.vsix` for team distribution | `vsce package` produces installable file |

**Milestone:** Zero-touch vector DB lifecycle -- opens with workspace, updates on save, no manual commands needed.

---

## Success Criteria

| Criterion | Measurement |
|-----------|-------------|
| Full workspace indexed | `vector-stats` reports > 2,500 chunks |
| Query relevance | Top-3 results contain the answer for 80%+ of test queries |
| Query latency | < 500 ms end-to-end (embed query + search + format results) |
| Incremental re-index | Changed file re-indexed within 5 seconds of save |
| Kong observability | Every embedding and LLM call logged with token count and cost |
| Agent adoption | Roo Code calls `workspace_search` in > 50% of multi-file investigation tasks |
| Zero manual context | Architect does not need to manually paste file contents or explain workspace structure |

---

## References

- [Vector DB / RAG Feasibility Analysis](VECTOR-DB-RAG-FEASIBILITY-ANALYSIS.md) -- Feasibility assessment and tool comparison
- [Context Window Utilization Analysis](CONTEXT-WINDOW-UTILIZATION-ANALYSIS.md) -- Why better retrieval matters
- [Deep Research: Copilot vs Kong+Roo Economics](DEEP-RESEARCH-1.md) -- Token economics and RAG architecture comparison
- Kong AI Gateway Docs: https://docs.konghq.com/gateway/latest/ai-gateway/
- ChromaDB Docs: https://docs.trychroma.com/
- MCP Specification: https://spec.modelcontextprotocol.io/
- Ollama: https://ollama.ai/
