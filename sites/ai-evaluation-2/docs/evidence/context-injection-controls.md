<!-- CONFLUENCE-PUBLISH -->

# Controlling What Copilot Sees: The Context Injection Pipeline

## Why This Matters

GitHub Copilot does not ingest an entire repository into its context window. It selects, prioritizes, and truncates content through a multi-layered pipeline. Understanding this pipeline is critical for architecture teams because **what the LLM sees determines what it knows** — and what it knows determines the quality of its architecture analysis, solution designs, and ADR authoring.

This page distills findings from deep research into the controllable surfaces of Copilot's context injection pipeline. The focus is practical: what can an architecture team configure, optimize, or work around?

## Context Window Budget

Modern models advertise large context windows (up to 400,000 tokens), but Copilot reserves approximately 30-35% exclusively for output generation. A model with a 400,000-token window has a maximum prompt input of roughly 128,000 tokens. This reservation is an immutable system parameter — architects cannot override it.

When the remaining input budget is under pressure from competing sources, Copilot applies a **deterministic priority hierarchy**. Lower-priority sources are silently truncated:

| Priority | Source | Description |
|----------|--------|-------------|
| 1 (highest) | System instructions and rules | Copilot system prompt + custom instructions (`copilot-instructions.md`, scoped `.instructions.md`, organization-level instructions) |
| 2 | Explicit user context | Content attached via `#file`, `#selection` — treated as hard requirements |
| 3 | Tool and MCP results | Output from invoked tools, terminal commands, MCP servers |
| 4 | Active editor and proximity | Currently focused file, cursor position, visible viewport |
| 5 | Retrieved semantic context | RAG results from workspace indexing (`@workspace`, `#codebase`) — dynamically sized based on remaining budget |
| 6 | Conversation history | Previous chat turns — frequently compressed or truncated in long sessions |
| 7 (lowest) | Implicit open tabs | Background files open in the IDE but not focused — first to be evicted |

### Key Implication

Explicit `#file` references consume budget before semantic retrieval runs. If an architect forces five large files into context, there may be no room left for `@workspace` to retrieve related specs or ADRs. Use `#file` surgically, not liberally.

## Instruction File Constraints

Custom instruction files are the primary mechanism for teaching Copilot about the architecture domain. Understanding their limits prevents silent degradation.

### Composition Model

Instructions are composed **additively**, not selectively. All matching instruction files from all tiers are concatenated:

1. **Personal instructions** (VS Code `github.copilot.chat.codeGeneration.instructions` setting) — highest conflict priority
2. **Repository instructions** (`.github/copilot-instructions.md`) — overrides organization defaults
3. **Organization instructions** (GitHub.com admin dashboard) — lowest conflict priority
4. **Scoped instructions** (`.github/instructions/**/*.instructions.md`) — injected when `applyTo` glob matches the active file

Because all matching files are concatenated, instruction bloat directly reduces the token budget available for workspace retrieval.

### Size Limits and Degradation

| Threshold | Behavior |
|-----------|----------|
| Under ~500 lines | Reliable adherence — instructions are followed consistently |
| 500-1,000 lines | Generally effective but attention to deeply nested rules begins to weaken |
| Over ~1,000 lines | Non-deterministic degradation — rules buried deep in the file may be ignored ("lost in the middle" phenomenon) |
| PR Code Review | Hard limit: only the first **4,000 characters** of instruction files are read. Content beyond this cutoff is permanently excluded from automated reviews. |

### Mitigation: Scoped Instructions with `applyTo`

The `applyTo` YAML frontmatter in scoped instruction files acts as a **deterministic pre-filter outside the LLM**. Instead of loading a 1,000-line global rulebook and hoping the model reads all of it, scoped files ensure only relevant rules enter the token budget:

```yaml
---
applyTo: "architecture/specs/**/*.yaml"
---
# OpenAPI Spec Review Rules
...
```

This is the most effective strategy for working within instruction file limits. The architecture team's current setup (1,172-line `copilot-instructions.md`) is at risk of degradation and would benefit from decomposing domain-specific rules into scoped files.

## File Structure Optimization

### Markdown: Heading-Aware Chunking

Copilot's indexing pipeline uses format-aware chunking for Markdown files. Instead of splitting at arbitrary token counts, it splits at **heading boundaries** (H1, H2, H3). The chunker also performs **semantic anchoring** — prepending the parent heading hierarchy to each chunk's metadata, so a retrieved chunk retains its broader context.

**What this means for architecture documents:**

- ADRs with clear H2 sections (Context, Decision, Consequences) produce clean, self-contained chunks
- Long documents without headings are arbitrarily sliced, often breaking the connection between a concept and its explanation
- Deeply nested, well-structured heading hierarchies produce the highest retrieval precision

### YAML and Code: Divergent Chunking Quality

Copilot's Tree-sitter AST parsing provides excellent structural chunking for **programming languages** — Java, TypeScript, Python, Go, Rust. Methods are chunked at class and function boundaries, preserving parent-child relationships. The target chunk size is approximately 50-1,000 characters, with recursive decomposition for oversized AST nodes.

However, **YAML, Markdown, and JSON files receive significantly worse treatment**. While Tree-sitter grammars exist for these formats in the open-source ecosystem, Copilot's deployment does not use them for semantic chunking. Instead, these files fall back to two generic mechanisms:

- **Local (IDE)**: A 60-line sliding window scored by Jaccard similarity (token overlap) against the currently active code. No structural awareness.
- **Remote (cloud RAG)**: Standard embedding token windows (512-1,024 tokens). No respect for YAML key hierarchy, `$ref` pointers, or Markdown heading boundaries.

This creates a severe blind spot for architecture workspaces:

| File Type | What Copilot Does | What Gets Broken |
|-----------|-------------------|-------------------|
| **OpenAPI YAML** | Chunks by 60-line windows or token count | Endpoint definitions severed from their `$ref` component schemas. Response schemas orphaned from parent path definitions. |
| **Markdown ADRs** | Sequential token chunking | A `## Decision` section retrieved without its preceding `## Context` or following `## Consequences`. The LLM generates suggestions that ignore documented constraints. |
| **AsyncAPI YAML** | Same generic chunking | Event schemas separated from their channel definitions and message examples. |
| **Figma designs** | Not in git — hosted on figma.com. Binary `.fig` bypassed by indexer. SVGs explicitly excluded (`**/*.svg` pattern). Screenshots usable only via manual multimodal attachment but suffer from "state obfuscation" (cannot reveal interactive states, permissions, or async loading). | Copilot cannot index external content. Requires tripartite hybrid: (1) CI/CD design token export to git for ambient awareness, (2) Figma MCP server for real-time frame queries, (3) Figma Code Connect to map design components to repository code. |
| **PlantUML** | Raw text tokenization | No community Tree-sitter grammar in use. Diagram relationships are lexically searched, not structurally understood. |

!!! warning "No Custom Chunking Configuration Exists"
    GitHub Copilot (Individual, Business, and Enterprise) does not expose any configuration for chunking strategy. There are no VS Code settings, `.copilot/` directory conventions, or Enterprise admin controls that modify how the indexer slices files. The `applyTo` frontmatter in instruction files controls **when instructions are injected**, not how files are **parsed or chunked**. No competitor platform (Cursor, Windsurf, Claude Code) offers this either — it is a universal limitation of the current generation of AI coding assistants.

### File Size Matters

| Size | Retrieval Impact | Agent Mode Impact |
|------|-----------------|-------------------|
| Small, focused files | High retrieval precision — each file represents a coherent concept | Fast edits — agent mode rewrites whole files |
| Large monolithic files | Vector embedding density diluted — harder to match specific queries | Severe performance bottleneck — agent defaults to whole-file rewriting, causing timeouts and context exhaustion |

**Recommendation:** Favor many small, focused files over few large ones. An architecture workspace with one spec per service (19 files) outperforms a single combined spec file.

### File Naming for Retrieval

Descriptive file names significantly improve retrieval via Copilot's lexical (grep/glob) search layer, which augments the semantic vector search. `svc-check-in-openapi.yaml` is instantly matchable by keyword queries; `spec.yaml` is not. Research confirms that hybrid retrieval (lexical + semantic) outperforms either approach alone. Naming conventions are essentially free metadata that improves both search layers.

### File Decomposition for YAML

Because Copilot's chunker does not understand YAML hierarchy, **physical file boundaries are the only reliable chunk boundaries** for declarative files. For large OpenAPI specs:

- Split paths into separate files, linked by `$ref` from a master `openapi.yaml`
- Keep component schemas in dedicated files under `components/schemas/`
- Target: no single YAML file should exceed ~150 lines, ensuring the entire file fits within a single embedding chunk

The architecture workspace already follows one-spec-per-service (good). Review whether individual spec files exceed the 150-line threshold and consider further decomposition if so.

## MCP as a Custom Chunking Layer

The chunking limitations above are **entirely bypassed by the Model Context Protocol**. Instead of relying on Copilot's generic indexer to understand OpenAPI structure, an MCP server can parse the spec semantically and return exactly the data requested.

### How It Works

An OpenAPI MCP server parses YAML specifications and exposes each endpoint as a discrete tool. When the LLM needs to understand `POST /check-in`, it calls the MCP tool rather than searching the raw YAML. The server returns the complete endpoint definition — path, parameters, request body, response schemas, security requirements — as a single, semantically whole unit.

Existing implementations:

- **openapi-mcp** and **mcp-openapi-schema-explorer** — parse OpenAPI specs and expose endpoints as tools
- **Stainless MCP** — converts OpenAPI specs into MCP servers automatically
- **@figma/mcp-server (official)** — maintained by Figma; exposes `get_design_context`, `search_design_system`, `get_variable_defs`, and bidirectional write tools; leverages Code Connect when configured; requires paid Dev/Full seat on Organization/Enterprise plan
- **@yhy2001/figma-mcp-server** — community server optimized for AI coding assistants with Smart Layout Detection (translates absolute coordinates to Flexbox/Grid CSS) and L1/L2 caching to reduce API rate limiting
- **antonytm/figma-mcp-server** — WebSocket bridge to Figma desktop plugin; bypasses REST API read-only limits but requires running Figma desktop during session
- **mcp-vector-search** — provides independent AST-aware chunking with its own vector store, bypassing the IDE's native limitations

### MCP vs Native Retrieval

MCP tool responses and native workspace retrieval are **additive**, not competing. When both are available, the agent's orchestration layer decides which source to query based on the prompt. MCP responses are more token-efficient because they return only the exact data requested, rather than adjacent chunks of irrelevant content.

However, MCP responses are subject to the **10KB truncation limit** documented below. MCP servers for architecture data must be designed with this constraint from the start.

### When to Use MCP vs Native Indexing

| Data Type | Recommended Approach | Rationale |
|-----------|---------------------|----------|
| Java source code | Native indexing | AST-aware chunking works well for code |
| Markdown ADRs and docs | Native indexing + heading structure | Heading-aware chunking is adequate if documents are well-structured |
| Small YAML metadata files | Native indexing | Files under ~150 lines fit in a single chunk |
| Large OpenAPI specs | MCP server | Native chunker destroys endpoint-schema relationships |
| Figma wireframes | MCP server (Figma API) + design token export + Code Connect | Designs hosted on figma.com, not in git. Tripartite hybrid recommended: (1) export design tokens as JSON/YAML to git via CI/CD for ambient indexing, (2) deploy Figma MCP server for targeted frame queries, (3) configure Code Connect to map design components to code. SVGs are explicitly excluded from Copilot's workspace indexing. Raw REST API JSON exceeds token budgets and uses absolute coordinates that drain LLM reasoning capacity. |
| PlantUML diagrams | Scoped instruction + native indexing | Lexical search on diagram text is adequate; no structural parsing available |

## Retrieval Ranking Signals

When Copilot performs workspace retrieval (implicit in agent mode, explicit via `@workspace`), ranking is driven by multiple signals:

| Signal | Effect | How to Leverage |
|--------|--------|-----------------|
| **Active file and cursor position** | Highest weight — the file and code block at the cursor are prioritized | Open the most relevant file before prompting |
| **Visible viewport** | Code currently on screen ranks higher than hidden code in the same file | Scroll to the relevant section before asking |
| **Temporal recency** | Recently edited or opened files get a temporary boost | Click through related files before prompting to "prime" the context |
| **AST symbol references** | If the cursor is in a function that imports from another file, that file is boosted | Let import chains guide context naturally |
| **Semantic similarity** | Vector embedding match between query and indexed chunks | Use precise terminology in prompts — match the vocabulary in your specs and ADRs |

### `#codebase` vs `@workspace`

These are not synonymous:

- **`#codebase`**: Pure semantic vector search against the full workspace index. Finds content by mathematical meaning, not keywords.
- **`@workspace`**: A chat participant that combines semantic search with editor signals (active file, recent edits, open tabs). More context-aware but more biased toward what is currently open.

For architecture queries that need to search across the entire repository (e.g., "which services use this event?"), `#codebase` is more thorough. For queries anchored to the current file (e.g., "what does this spec imply for the check-in service?"), `@workspace` is more contextually relevant.

## Agent Mode Context Management

In agent mode, context is not a static injection — it is a dynamic, evolving state machine.

### Initialization

Agent mode starts with a **summarized workspace structure** — a token-efficient map of the repository — not the full codebase. The agent then decides which files to read based on the user's prompt.

### Iterative Discovery

The agent discovers context through tool calls (`read_file`, `semantic_search`, `grep_search`). Files that are read or modified enter the agent's **Working Set** — a focused mental model of relevant files.

### Long Session Management

Extended sessions (20+ tool calls) face context pressure as tool outputs, terminal results, and reasoning accumulate. Copilot addresses this with:

- **History summarization**: Older conversation turns are compressed into behavioral milestones
- **Time Traveling Stream Rules (TTSR)**: Mid-stream injection of the original goal and rule reminders to prevent attention decay
- **Checkpoints**: Each `edit_file` call creates a rollback point — undoing resets context to a clean state

### Practical Implication

For complex architecture sessions, the agent does not lose sight of domain rules if they are in instruction files (Priority 1). But retrieved context from earlier in the session may be summarized away. If the agent needs to reference a specific spec or ADR throughout a long session, use `#file` to anchor it explicitly.

## Content Exclusion

### Enterprise Content Exclusion

Enterprise-tier content exclusion policies use glob patterns to make files invisible to Copilot:

- Blocked from inline completions
- Blocked from chat context
- Blocked from PR code review
- Immune to `#file` override — even explicit references cannot force excluded files into context

### Known Gaps

| Gap | Risk Level | Mitigation |
|-----|-----------|------------|
| **Agent mode bypass**: Content exclusion policies are not enforced in agent mode or Copilot CLI | HIGH for regulated environments | Use `.gitignore` as a secondary barrier; configure VS Code `"github.copilot.enable"` settings per file type |
| **LSP semantic leakage**: Copilot can infer structure of excluded files through Language Server Protocol metadata (type information, hover definitions from imports) | MEDIUM | Awareness only — no mitigation available |

## Copilot Spaces (Replaced Knowledge Bases)

GitHub deprecated Copilot Knowledge Bases in November 2025, replacing them with **Copilot Spaces**.

Spaces are centralized, shareable context collections that aggregate cross-repository code, Markdown, JSON, issues, and PR histories. When invoked, Spaces provide **strict grounding** — directing the LLM to reason within the curated content, reducing hallucination.

### Limitation

Spaces are restricted to **GitHub-hosted content**. External systems (Confluence, SharePoint, Jira) cannot be mounted into a Space. Accessing external data still requires MCP servers — and MCP results are subject to the truncation limits below.

## MCP Server Design Constraints

When MCP servers return data to Copilot, the results are subject to severe constraints that architecture teams must design around:

| Constraint | Detail | Impact |
|-----------|--------|--------|
| **10KB hard truncation** | MCP response text is truncated to 10KB before it reaches the agent. No warning is provided — the LLM receives broken JSON or incomplete content. | MCP servers must return concise, pre-filtered responses — not raw API dumps |
| **HTTP 413 death loops** | In extended sessions, accumulated tool history exceeds HTTP payload limits, triggering 413 errors that are themselves appended to history, causing infinite retry loops | Keep responses small; design for pagination |
| **"Unreadable file" fallback** | Very large responses are treated as attached files, causing the LLM to respond "I cannot read it" | Never return more than a few KB per tool call |

### MCP Server Design Rules for Copilot

1. **Paginate**: Return 10-25 items per call with a cursor token. Let the agent iterate.
2. **Strip metadata**: Remove internal IDs, stack traces, and telemetry. Return only semantically relevant content.
3. **Summarize first**: Provide a summary view, then let the agent request detail for specific items.
4. **Limit toolsets**: Restrict exposed tools to minimize system prompt bloat from unused tool schemas.

## Actionable Recommendations

Based on two rounds of deep research (context injection pipeline and chunking control), the architecture team should consider these optimizations:

| # | Action | Effort | Impact |
|---|--------|--------|--------|
| 1 | **Decompose `copilot-instructions.md`** into scoped files with `applyTo` globs — keep global file under 500 lines, move domain-specific rules to path-scoped files | MEDIUM | Prevents instruction truncation and attention degradation |
| 2 | **Structure all Markdown with consistent headings** — H1 for document title, H2 for major sections, H3 for subsections | LOW | Improves chunking boundaries and semantic anchoring |
| 3 | **Keep specs as separate files per service** (already done) — never combine into monolithic files. Review for 150-line threshold. | LOW | Already optimal — validate no spec exceeds the threshold |
| 4 | **Add scoped instruction for OpenAPI directory** — instruct the LLM to always retrieve both endpoint and `$ref` component schemas when analyzing specs | LOW | Mitigates hallucination from fragmented YAML chunking |
| 5 | **Design MCP servers with 10KB response limit** — paginate, summarize, strip metadata | HIGH (at MCP build time) | Prevents silent data corruption and session death loops |
| 6 | **Evaluate OpenAPI MCP server** for the 19-service spec collection — exposes endpoints as discrete tools, bypassing YAML chunking entirely | MEDIUM | Eliminates the worst chunking blind spot |
| 7 | **Prime context before prompting** — open relevant files and scroll to relevant sections before typing a query | LOW | Leverages editor signal boosting at zero cost |
| 8 | **Use `#file` sparingly** — prefer `@workspace` or `#codebase` for discovery; use `#file` only when you know exactly which file the LLM needs | LOW | Prevents budget cannibalization |
| 9 | **Evaluate Copilot Spaces** for cross-repository architecture standards that multiple teams need | MEDIUM | Provides strict grounding without requiring every consumer to clone the architecture repo |
| 10 | **Adopt AGENTS.md** as the repository routing standard — explicit map of workspace topology directing the AI to the correct directories and MCP tools for each file type | LOW | Reduces blind vector search; 60,000+ repos already use this standard |
| 11 | **Enforce descriptive file naming** — include domain, service, and asset type in filenames (e.g., `adr-004-payment-gateway-retry-logic.md` not `adr-004.md`) | LOW | Improves lexical search layer that augments semantic retrieval |

---

**Research sources:**

- [Deep Research — Context Injection Pipeline](../research/deep-research-results-context-injection.md) (April 2026, 55 authoritative sources)
- [Deep Research — Chunking Control by File Type](../research/deep-research-results-chunking-control.md) (April 2026, 57 authoritative sources)
- [Deep Research — Figma Wireframe Chunking](../research/deep-research-results-figma-chunking.md) (April 2026, 51 sources)

**See also:**

- [Build vs Leverage](build-vs-leverage.md) — Why native capabilities replace custom RAG
- [DD-01: Context and Configuration](../decisions/dd-01-context-configuration.md) — How the three options handle domain knowledge injection
- [Copilot Rollout Roadmap](../framework/copilot-rollout-roadmap.md) — Practical deployment plan incorporating these findings
