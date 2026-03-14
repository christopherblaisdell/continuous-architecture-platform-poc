# Vector DB / RAG Feasibility Analysis

| | |
|-----------|-------|
| **Author** | Christopher Blaisdell |
| **Date** | 2026-03-14 |
| **Status** | RESEARCH COMPLETE |
| **Relates To** | ADR-001: AI Toolchain Selection (`decisions/ADR-001-ai-toolchain-selection.md`) |
| **Phase** | Phase 1 - AI Tool Cost Comparison |
| **See Also** | Context Window Utilization Analysis (`research/CONTEXT-WINDOW-UTILIZATION-ANALYSIS.md`), Deep Research: Copilot vs Kong+Roo Economics (`research/DEEP-RESEARCH-1.md`) |

---

## Executive Summary

This analysis evaluates the feasibility of creating a vector database over the entire workspace to enable AI coding assistants (specifically Roo Code) to perform semantic search automatically, and whether Kong AI Gateway could accomplish this via a VS Code plugin.

**Key findings:**

1. A workspace-wide vector database is **technically feasible** and well-suited for this architecture workspace. The most practical implementation is a local MCP server backed by ChromaDB or LanceDB.
2. Kong AI Gateway is **the wrong tool for this problem** -- it is an API gateway, not an embedding/retrieval system. It operates at the wrong layer of the stack.
3. GitHub Copilot **already implements this pattern** natively via its `@workspace` semantic indexing and Tool RAG architecture.
4. For Roo Code, the open-source **Continue.dev** extension provides the closest existing implementation with local codebase indexing.

---

## Research Questions

1. Can a vector database be created from the entire VS Code workspace and give Roo Code automatic query access?
2. Could a VS Code plugin accomplish this with Kong AI Gateway?

---

## Question 1: Vector Database for Roo Code Workspace Search

### Answer: Yes -- Technically Feasible, Moderate Effort

There are two viable approaches to give Roo Code automatic semantic search over the full workspace.

### Approach A: MCP Server with Local Vector DB (Recommended)

Roo Code supports Model Context Protocol (MCP) servers, which act as tool providers the agent can invoke autonomously during reasoning:

1. **Index the workspace** -- Chunk all files (Markdown, YAML, Java, OpenAPI specs, ADRs, solution designs, event schemas) and generate embeddings
2. **Store in a local vector DB** -- ChromaDB, LanceDB, Qdrant, or FAISS
3. **Expose via an MCP server** -- A small Python or Node MCP server that accepts `search(query)` tool calls and returns the top-k relevant chunks with source file paths
4. **Configure Roo Code** -- Register the MCP server; the agent calls `search()` as a tool during any task

### Approach B: VS Code Extension with Built-in RAG

- **Continue.dev** -- Open-source AI assistant with a `@codebase` context provider that indexes the workspace into a local vector DB
- **Cursor** -- Has native codebase indexing, but is a separate editor, not a VS Code plugin

### Why This Workspace Is an Ideal Candidate

| Factor | Rationale |
|--------|-----------|
| High text density | ~90% of workspace is Markdown, YAML, and OpenAPI specs — semantically rich |
| Cross-referencing is the core challenge | Tickets reference ADRs, which reference specs, which reference solutions |
| Volume exceeds context windows | 19 OpenAPI specs + 11 ADRs + event schemas + capabilities + solutions |
| Repetitive lookup patterns | "Which services touch this capability?" — ideal for retrieval |

### Implementation Challenges

| Challenge | Mitigation |
|-----------|------------|
| Naive chunking destroys YAML/Markdown structure | Format-aware chunking: split Markdown by H2, YAML by top-level keys, OpenAPI by path+operation |
| Index staleness after file changes | File watcher (`watchdog`) with incremental re-indexing on save |
| Retrieval misses structural relationships | Supplement with metadata filters; use the existing `ticket-client.py` for structural queries |

---

## Question 2: Could Kong AI Gateway Accomplish This?

### Answer: No -- Wrong Layer of the Stack

Kong AI Gateway is an **API gateway** that routes requests between clients and LLM providers. It does not:

- Generate embeddings from workspace files
- Store vectors or perform similarity search
- Chunk documents
- Integrate with the VS Code file system
- Watch the filesystem for changes

### Where Kong AI Gateway Does Fit

Kong AI becomes relevant **after** a vector DB + retrieval pipeline exists, as an operational layer to:

- Route embedding API calls through a managed gateway
- Track cost of embedding + LLM inference calls centrally
- Apply rate limits to prevent runaway indexing costs
- Provide multi-provider failover (OpenAI → Cohere → Ollama)

This is useful at team scale but not required for a single-architect POC.

### Analogy

Using Kong AI to build a workspace search engine is like using an nginx reverse proxy to build a search engine. It can route traffic to a search engine, but it cannot *be* the search engine.

---

## Tool Comparison

| Capability | GitHub Copilot | Roo Code (Current) | Roo Code + Vector MCP | Continue.dev |
|------------|---------------|--------------------|-----------------------|-------------|
| Semantic workspace indexing | Built-in (`@workspace`) | None | Via MCP server | Built-in (`@codebase`) |
| Embedding model | Proprietary (server-side) | N/A | Configurable | Configurable |
| Vector storage | Server-side (GitHub) | N/A | Local (ChromaDB) | Local |
| Incremental re-indexing | Automatic | N/A | Requires file watcher | Automatic |
| Cost | Included | N/A | ~$0 if local (Ollama) | Free |
| Setup effort | Zero | N/A | 3-6 days | Extension install |

---

## Recommendation for Solution Architecture Practice

**Short term: Use GitHub Copilot as the primary AI assistant.** Copilot's `@workspace` semantic indexing already implements the vector DB + RAG pattern with zero setup and zero maintenance.

**Medium term (if Roo Code is needed): Deploy a local MCP server with ChromaDB.** See the [implementation plan](vector-db-implementation-plan.md) for the full design. Prioritize format-aware Markdown/YAML chunking and local embeddings via Ollama.

**Long term (team scale): Evaluate Continue.dev.** Open-source, local-first, built-in codebase indexing, multiple LLM backends.

### What NOT to Do

- **Do not invest in Kong AI Gateway** for retrieval. It adds operational complexity with no retrieval capability.
- **Do not build a custom RAG pipeline from scratch** when Copilot's `@workspace`, Continue.dev's `@codebase`, or pre-built MCP servers already solve the problem.
- **Do not rely solely on vector similarity** for architecture queries. Many architecture questions are structural. The existing YAML metadata + `ticket-client.py` handle structural queries better than any vector DB.

---

## Decision Framework

| Scenario | Recommended Tool | Rationale |
|----------|-----------------|-----------|
| Single architect, maximum simplicity | GitHub Copilot (`@workspace`) | Zero setup, built-in RAG |
| Need Roo Code + workspace search | Custom MCP server + ChromaDB | 3-6 day build |
| Team of 3-5 architects | Continue.dev + Ollama | Open source, local-first |
| Enterprise (50+ developers) | Copilot Enterprise | Server-side indexing at scale |

---

## References

- [Workspace Vector DB Implementation Plan](vector-db-implementation-plan.md)
- [Phase 2 Next Steps](phase-2-next-steps.md)
- Context Window Utilization Analysis (`research/CONTEXT-WINDOW-UTILIZATION-ANALYSIS.md`)
- Deep Research: Copilot vs Kong+Roo Economics (`research/DEEP-RESEARCH-1.md`)
