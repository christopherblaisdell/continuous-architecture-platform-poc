# Workspace Vector DB Implementation Plan

| | |
|-----------|-------|
| **Author** | Christopher Blaisdell |
| **Date** | 2026-03-14 |
| **Status** | PROPOSED |
| **Relates To** | [Vector DB / RAG Feasibility Analysis](vector-db-rag-feasibility.md) |
| **Phase** | Phase 2 - AI Workflow Enhancement |
| **Full Detail** | Full Implementation Plan (`research/WORKSPACE-VECTOR-DB-KONG-AI-IMPLEMENTATION-PLAN.md`) |

---

## Executive Summary

This plan describes how to build a workspace-wide vector database that indexes the entire NovaTrek architecture workspace and exposes it to AI coding assistants via MCP protocol, with Kong AI Gateway managing embedding and LLM API traffic.

**Key insight:** Kong AI Gateway cannot *be* the vector database, but it is the correct place to manage the AI API traffic that powers the system.

| Layer | Component | Responsibility |
|-------|-----------|----------------|
| Storage | ChromaDB (local) | Vector storage, similarity search, metadata filtering |
| Indexing | Python chunking pipeline | Format-aware document splitting, embedding generation |
| Retrieval | MCP Server (Python) | Query interface for AI agents via MCP protocol |
| AI Gateway | Kong AI Gateway | Route embedding + LLM calls, cost tracking, prompt decoration |
| Inference | OpenAI / Anthropic / Ollama | Embedding models + LLM reasoning |
| Client | Roo Code / VS Code | AI assistant consuming the MCP tool |

---

## Architecture Overview

### Data Flow

**Indexing (on file change):**

```
File saved in workspace
  -> File watcher detects change
  -> Chunking pipeline splits file (format-aware)
  -> Chunks sent to embedding provider (via Kong AI or direct Ollama)
  -> Embedding vectors stored in ChromaDB with metadata
```

**Query (during AI agent reasoning):**

```
AI agent calls MCP tool: search("which services call svc-guest-profiles?")
  -> MCP server embeds query
  -> MCP server queries ChromaDB for top-k similar chunks
  -> Returns ranked results with file paths + content snippets
  -> AI agent uses retrieved context in its reasoning
```

### Kong AI Gateway Role

Kong does not perform retrieval. It provides infrastructure for the pipeline:

| Service | Value |
|---------|-------|
| Unified embedding API | Single `/embeddings` endpoint; backend switchable between OpenAI/Cohere/Ollama |
| Cost tracking | Every embedding + LLM call logged with tokens, model, latency, cost |
| Prompt decoration | Injects system prompt: "Use workspace_search before reading files manually" |
| Rate limiting | Prevents runaway re-indexing from consuming embedding API quota |
| Multi-provider failover | If OpenAI is down, route to Ollama automatically |

---

## Implementation Phases

| Phase | Name | Duration | Output |
|-------|------|----------|--------|
| A | Chunking pipeline | 1-2 days | `scripts/vector-db/chunker.py` |
| B | ChromaDB setup | 0.5 day | `scripts/vector-db/store.py` |
| C | File watcher | 0.5 day | `scripts/vector-db/watcher.py` |
| D | MCP server | 0.5-1 day | `scripts/vector-db/mcp_server.py` |
| E | Kong AI Gateway config | 0.5-1 day | `config/kong/ai-plugin.yaml` |
| F | VS Code extension wrapper | 1-2 days (optional) | `.vscode/extensions/workspace-search/` |

**Total effort:** 3-6 days (4-8 with optional extension)

---

## Format-Aware Chunking Strategy

| File Type | Strategy | Expected Chunk Size |
|-----------|----------|-------------------|
| Markdown (`.md`) | Split by H2 (`##`) headers | 200-1500 tokens |
| OpenAPI specs | Split by path + operation | 100-800 tokens |
| YAML metadata files | Split by top-level key | 50-400 tokens |
| AsyncAPI (`.yaml`) | Split by channel | 100-500 tokens |
| Java (`.java`) | Split by class method | 100-1000 tokens |
| ADR (`.md`) | Split by MADR section | 100-500 tokens |

---

## How the Vector DB Gets Updated

**Local file watcher (primary — no check-in required):**

The `watcher.py` script uses the Python `watchdog` library to monitor the workspace filesystem. When any file is saved — including uncommitted files in the working tree — it triggers incremental re-indexing of only the changed file. Re-index completes within 5 seconds of save.

**CI-triggered indexing (supplementary — on push to main):**

A GitHub Actions workflow triggers a full re-index on push to main. This publishes a shared team baseline. Individual architects still use local watcher for day-to-day work.

**Key point:** An architect does not need to commit or check in anything to get their work indexed. The local watcher indexes on save, before any commit. This addresses the concern that "each architect must check in every item they want to chunk."

---

## VS Code Plugin: Should It Be Built?

The short answer: not from scratch, and not as the primary delivery vehicle.

### Reasons Not to Build a Full VS Code Extension

| Reason | Detail |
|--------|--------|
| Already solved by Continue.dev | Continue.dev already IS this extension — open source, local codebase indexing, multiple LLM backends |
| Development effort 3-5x higher | Extension requires TypeScript, webpack, manifest, activation events. Python scripts are ~400 lines. Extension equivalent is ~1,500-2,500 lines |
| Dependency bundling is painful | ChromaDB is Python. VS Code extensions run in Node.js. Integration requires subprocess management |
| Testing overhead | Extension debugging requires VS Code Extension Development Host. Python scripts test in 2 seconds with pytest |

### Recommended: Thin Extension Wrapper

If VS Code integration UX is desired, build a thin wrapper (~200 lines TypeScript) that calls the existing Python scripts:

```
VS Code Extension (TypeScript, ~200 lines)
  |-- onStartupFinished -> spawn python3 scripts/vector-db/index.py
  |-- onDidSaveTextDocument -> spawn python3 scripts/vector-db/reindex-file.py <path>
  |-- Status bar item -> reads .vector-db/stats.json
  |-- Command: "Reindex Workspace" -> spawns full index.py
  +-- Extension settings -> Kong URL, embedding provider, top-k

Python scripts (unchanged)
  |-- chunker.py, store.py, embedder.py -> actual work
  |-- mcp_server.py -> Roo Code integration
  +-- index.py, watcher.py -> invoked by extension
```

This gives extension UX (auto-start, status bar, command palette) without rewriting the implementation in TypeScript.

### Extension Decision Matrix

| Situation | Recommendation | Reason |
|-----------|---------------|--------|
| Solo architect wanting RAG now | Python scripts from this plan | Working in days, not weeks |
| Solo architect who wants polish | Install Continue.dev | Zero development, `@codebase` works out of the box |
| Team of 3-5 architects | Python scripts + thin extension wrapper | Auto-start eliminates manual watcher maintenance |
| Building for broad distribution | Full VS Code extension | Only if packaging for users who cannot run Python |

---

## Success Criteria

| Criterion | Measurement |
|-----------|-------------|
| Full workspace indexed | `vector-stats` reports > 2,500 chunks |
| Query relevance | Top-3 results contain the answer for 80%+ of test queries |
| Query latency | < 500 ms end-to-end |
| Incremental re-index | Changed file re-indexed within 5 seconds of save |
| Kong observability | Every embedding and LLM call logged with token count and cost |
| Agent adoption | Roo Code calls `workspace_search` in > 50% of multi-file tasks |

---

## References

- Full Implementation Plan (`research/WORKSPACE-VECTOR-DB-KONG-AI-IMPLEMENTATION-PLAN.md`) — Complete technical detail, code samples, Kong plugin config
- [Vector DB / RAG Feasibility Analysis](vector-db-rag-feasibility.md) — Feasibility and tool comparison
- [Phase 2 Next Steps](phase-2-next-steps.md) — Decision point and action items
