# Vector Database / RAG Feasibility Analysis for AI-Assisted Architecture Practice

| | |
|-----------|-------|
| **Author** | Christopher Blaisdell |
| **Date** | 2026-03-14 |
| **Status** | RESEARCH COMPLETE |
| **Relates To** | [ADR-001: AI Toolchain Selection](../decisions/ADR-001-ai-toolchain-selection.md) |
| **Phase** | Phase 1 - AI Tool Cost Comparison |
| **See Also** | [Context Window Utilization Analysis](CONTEXT-WINDOW-UTILIZATION-ANALYSIS.md), [Deep Research: Copilot vs Kong+Roo Economics](DEEP-RESEARCH-1.md) |

---

## Executive Summary

This analysis evaluates the feasibility of creating a vector database over the entire workspace to enable AI coding assistants (specifically Roo Code) to perform semantic search automatically, and whether Kong AI Gateway could accomplish this via a VS Code plugin.

**Key findings:**

1. A workspace-wide vector database is **technically feasible** and well-suited for this architecture workspace. The most practical implementation is a local MCP server backed by ChromaDB or LanceDB.
2. Kong AI Gateway is **the wrong tool for this problem** -- it is an API gateway, not an embedding/retrieval system. It operates at the wrong layer of the stack.
3. GitHub Copilot **already implements this pattern** natively via its `@workspace` semantic indexing and Tool RAG architecture (see [DEEP-RESEARCH-1.md](DEEP-RESEARCH-1.md) for details).
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

Roo Code supports Model Context Protocol (MCP) servers, which act as tool providers the agent can invoke autonomously during reasoning. The architecture:

1. **Index the workspace** -- Chunk all files (Markdown, YAML, Java, OpenAPI specs, ADRs, solution designs, event schemas) and generate embeddings using an embedding model (OpenAI `text-embedding-3-small` or a local model via Ollama such as `nomic-embed-text`)
2. **Store in a local vector DB** -- ChromaDB, LanceDB, Qdrant, or FAISS. All run locally with no cloud dependency
3. **Expose via an MCP server** -- A small Python or Node MCP server that accepts `search(query)` tool calls and returns the top-k relevant chunks with source file paths and line numbers
4. **Configure Roo Code** -- Register the MCP server in Roo Code's configuration. The agent can then call `search()` as a tool during any task

Existing open-source MCP servers that implement this pattern:

| Project | Backend | Description |
|---------|---------|-------------|
| `mcp-server-qdrant` | Qdrant | Semantic search over indexed documents |
| `mcp-server-memory` | Various | Persistent memory with vector retrieval |
| `code-index-mcp` | ChromaDB | Purpose-built for codebase indexing |

### Approach B: VS Code Extension with Built-in RAG

Several VS Code extensions embed workspaces into vector stores natively:

- **Continue.dev** -- Open-source AI assistant with a `@codebase` context provider that indexes the workspace into a local vector DB and makes it queryable from AI chat
- **Cursor** -- Has native codebase indexing, but is a separate editor, not a VS Code plugin

### Why This Workspace Is an Ideal Candidate

| Factor | Rationale |
|--------|-----------|
| High text density | ~90% of workspace is Markdown, YAML, and OpenAPI specs -- semantically rich and highly embeddable |
| Cross-referencing is the core challenge | Tickets reference ADRs, which reference specs, which reference solutions. Semantic search bridges these relationships |
| Volume exceeds context windows | 19 OpenAPI specs + 11 ADRs + event schemas + capability metadata + solution designs exceeds any single context window |
| Repetitive lookup patterns | Architecture tasks frequently require "which services touch this capability?" or "what ADRs constrain this design?" -- ideal for retrieval |

### Implementation Challenges

| Challenge | Impact | Mitigation |
|-----------|--------|------------|
| **Chunking strategy** | Naive line-based chunking destroys YAML structure and Markdown section boundaries. Splitting mid-section produces low-quality embeddings | Format-aware chunking: split Markdown by H2 headers, YAML by top-level keys, OpenAPI by path+operation |
| **Index staleness** | Changed files must be re-embedded. Stale embeddings return outdated context | File watcher (`inotify` / `fswatch`) with incremental re-indexing on save |
| **Embedding cost** | ~2,000+ files in workspace. Initial indexing with OpenAI embeddings: ~$0.01-0.05. Ongoing: negligible (only changed files) | Use local embedding model (Ollama + `nomic-embed-text`) for $0 compute cost |
| **Retrieval quality** | Vector similarity alone misses structural relationships (e.g., "which services call svc-check-in?" requires graph traversal, not just semantic similarity) | Supplement with keyword/metadata filters. Consider hybrid search (vector + BM25) |
| **Context budget** | Retrieved chunks consume tokens from the LLM's context window. Over-retrieval crowds out the agent's working memory | Limit to top-5 chunks per query. Include source path + line range, not full files |
| **Agent trust calibration** | The agent must learn when to query the vector DB vs. reading files directly. Over-reliance on retrieval can miss recent unindexed changes | Document the tool's limitations in the MCP server description. Use file reads for known paths |

### Effort Estimate

| Component | Effort | Notes |
|-----------|--------|-------|
| Chunking pipeline (Python) | 1-2 days | Format-aware splitters for Markdown, YAML, Java |
| Embedding + ChromaDB storage | 0.5 day | Well-documented, minimal code |
| MCP server wrapper | 0.5-1 day | Standard MCP protocol implementation |
| File watcher for incremental re-index | 0.5 day | `watchdog` Python library or `fswatch` |
| Testing and tuning | 1-2 days | Chunk size, overlap, top-k calibration |
| **Total** | **3-6 days** | Weekend-to-sprint depending on quality bar |

---

## Question 2: Could Kong AI Gateway Accomplish This?

### Answer: No -- Wrong Layer of the Stack

Kong AI Gateway is an **API gateway** that sits between clients and LLM inference providers. It provides:

- Traffic management (rate limiting, load balancing, retries across AI providers)
- AI Proxy (unified API to route requests to OpenAI, Anthropic, Azure OpenAI)
- Prompt engineering (template management, prompt decoration, guardrails)
- Observability (logging, cost tracking, token counting per request)
- Multi-provider failover (if OpenAI is down, route to Anthropic)

### Gap Analysis

| Required Capability | Kong AI Provides | Gap |
|---------------------|-----------------|-----|
| Generate embeddings from workspace files | Nothing -- Kong does not generate embeddings | Complete miss |
| Store vectors and perform similarity search | Nothing -- Kong has no storage layer | Complete miss |
| Chunk documents with format awareness | Nothing -- Kong operates on API requests, not documents | Complete miss |
| Integrate with VS Code editor and file system | Nothing -- Kong is a server-side gateway | Complete miss |
| Perform semantic search over code/docs | Nothing -- Kong proxies LLM API calls | Complete miss |
| Watch filesystem for changes and re-index | Nothing -- Kong has no filesystem access | Complete miss |

### Where Kong AI Would Fit

Kong AI becomes relevant only **after** a vector DB + retrieval pipeline already exists, as an operational layer to:

- Route embedding API calls through a managed gateway
- Load-balance between embedding providers (OpenAI vs. Cohere vs. local)
- Track cost of embedding + LLM inference calls centrally
- Apply rate limits to prevent runaway indexing costs in a team setting

This is useful at scale (50+ developers, thousands of daily embedding requests) but irrelevant for the POC or small-team architecture practice.

### Analogy

Using Kong AI to build a workspace search engine is like using an nginx reverse proxy to build a search engine. It can route traffic to a search engine, but it cannot *be* the search engine.

---

## Comparison: How Each Tool Handles Workspace Knowledge

| Capability | GitHub Copilot | Roo Code (Current) | Roo Code + Vector MCP | Continue.dev |
|------------|---------------|--------------------|-----------------------|-------------|
| Semantic workspace indexing | Built-in (`@workspace`) | None -- file reads only | Via MCP server | Built-in (`@codebase`) |
| Embedding model | Proprietary (server-side) | N/A | Configurable (OpenAI / local) | Configurable |
| Vector storage | Server-side (GitHub infrastructure) | N/A | Local (ChromaDB / LanceDB) | Local |
| Incremental re-indexing | Automatic (background) | N/A | Requires file watcher | Automatic |
| Query interface | `@workspace` chat participant | N/A | MCP tool call | `@codebase` chat participant |
| Context budget management | Managed (top-k retrieval, auto-compaction) | Manual (file reads fill context) | Semi-managed (configurable top-k) | Managed |
| Cost | Included in subscription | N/A | Embedding cost only (~$0) if local | Free (open source) |
| Setup effort | Zero | N/A | 3-6 days | Extension install + indexing time |

---

## Recommendation for Solution Architecture Practice

### Current State

The NovaTrek architecture workspace is an excellent demonstration of why semantic retrieval matters for architecture practices. With 19 service specs, 11 ADRs, 34 capabilities, event schemas, solution designs, and a growing solution backlog, the knowledge graph has already exceeded what any architect (human or AI) can hold in working memory. The Phase 1 comparison ([Context Window Utilization Analysis](CONTEXT-WINDOW-UTILIZATION-ANALYSIS.md)) demonstrated that Roo Code's brute-force context approach wastes tokens on redundant metadata, while Copilot's built-in RAG provides inherently better knowledge retrieval.

### Recommended Architecture

**Short term (current practice): Use GitHub Copilot as the primary AI assistant.**

Copilot's native `@workspace` semantic indexing already implements the vector DB + RAG pattern described above, with zero setup cost and zero ongoing maintenance. For an architecture practice generating interconnected documentation artifacts, this is the highest-value, lowest-friction option. The context window analysis and cost comparison both support this conclusion.

**Medium term (if Roo Code access is needed): Deploy a local MCP server with ChromaDB.**

If the practice needs Roo Code for specific capabilities (e.g., uncensored model access, OpenRouter flexibility, or multi-provider cost optimization), build the MCP vector server as described in Approach A. This closes the retrieval gap between Roo Code and Copilot. Prioritize:

1. Format-aware Markdown/YAML chunking (critical for this workspace's content mix)
2. Local embeddings via Ollama to eliminate per-query cost
3. Incremental re-indexing on file save to prevent staleness

**Long term (team scale): Evaluate Continue.dev as a unified layer.**

If the architecture practice scales beyond a single architect, Continue.dev offers a middle path -- open-source, local-first, with built-in codebase indexing and support for multiple LLM backends. It avoids vendor lock-in to either GitHub or OpenRouter while providing the RAG capability natively.

### What NOT to Do

- **Do not invest in Kong AI Gateway** for this purpose. Kong solves API traffic management at enterprise scale, not workspace knowledge retrieval. It adds operational complexity with no retrieval capability.
- **Do not build a custom RAG pipeline from scratch** when existing tools (Copilot's `@workspace`, Continue.dev's `@codebase`, or pre-built MCP servers) already solve the problem. The chunking/embedding/retrieval loop is well-understood infrastructure -- not a differentiator for an architecture practice.
- **Do not rely solely on vector similarity** for architecture queries. Many architecture questions are structural ("what services depend on svc-guest-profiles?") rather than semantic ("tell me about guest identity"). The existing YAML metadata files (`capabilities.yaml`, `tickets.yaml`, `capability-changelog.yaml`) with the ticket-client.py tool handle structural queries better than any vector DB. Use both.

### Decision Framework

| Scenario | Recommended Tool | Rationale |
|----------|-----------------|-----------|
| Single architect, maximum simplicity | GitHub Copilot (`@workspace`) | Zero setup, built-in RAG, included in subscription |
| Need Roo Code + workspace search | Custom MCP server + ChromaDB | 3-6 day build, closes Copilot's RAG advantage |
| Team of 3-5 architects | Continue.dev + Ollama | Open source, local-first, multi-backend support |
| Enterprise (50+ developers) | Copilot Enterprise or custom platform | Server-side indexing at scale, centralized governance |

---

## Implementation Plan

A detailed implementation plan for the recommended architecture (MCP server + ChromaDB + Kong AI Gateway) is available at [WORKSPACE-VECTOR-DB-KONG-AI-IMPLEMENTATION-PLAN.md](WORKSPACE-VECTOR-DB-KONG-AI-IMPLEMENTATION-PLAN.md).

---

## References

- [Context Window Utilization Analysis](CONTEXT-WINDOW-UTILIZATION-ANALYSIS.md) -- Empirical comparison of context management between Roo Code and Copilot
- [Deep Research: Copilot vs Kong+Roo Economics](DEEP-RESEARCH-1.md) -- Token economics, semantic indexing architecture, and cost modeling
- [ADR-001: AI Toolchain Selection](../decisions/ADR-001-ai-toolchain-selection.md) -- Original toolchain decision
- [Cost Measurement Methodology](../phases/phase-1-ai-tool-cost-comparison/COST-MEASUREMENT-METHODOLOGY.md) -- Phase 1 cost comparison framework
- MCP Specification: https://spec.modelcontextprotocol.io/
- ChromaDB: https://www.trychroma.com/
- Continue.dev: https://continue.dev/
