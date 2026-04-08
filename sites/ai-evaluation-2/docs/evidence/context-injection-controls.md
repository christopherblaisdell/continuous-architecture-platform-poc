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

### YAML and Code: AST-Aware Chunking

For structured files (Java, YAML, JSON), Copilot uses Tree-sitter AST parsing. This preserves parent-child relationships — an OpenAPI endpoint definition stays connected to its security schema, and Java methods are chunked along class and method boundaries.

When AST parsing is unavailable, Copilot falls back to **~250-token semantic chunks** (~10-30 lines). This fallback applies to file types without a Tree-sitter grammar.

### File Size Matters

| Size | Retrieval Impact | Agent Mode Impact |
|------|-----------------|-------------------|
| Small, focused files | High retrieval precision — each file represents a coherent concept | Fast edits — agent mode rewrites whole files |
| Large monolithic files | Vector embedding density diluted — harder to match specific queries | Severe performance bottleneck — agent defaults to whole-file rewriting, causing timeouts and context exhaustion |

**Recommendation:** Favor many small, focused files over few large ones. An architecture workspace with one spec per service (19 files) outperforms a single combined spec file.

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

Based on this research, the architecture team should consider these optimizations:

| # | Action | Effort | Impact |
|---|--------|--------|--------|
| 1 | **Decompose `copilot-instructions.md`** into scoped files with `applyTo` globs — keep global file under 500 lines, move domain-specific rules to path-scoped files | MEDIUM | Prevents instruction truncation and attention degradation |
| 2 | **Structure all Markdown with consistent headings** — H1 for document title, H2 for major sections, H3 for subsections | LOW | Improves chunking boundaries and semantic anchoring |
| 3 | **Keep specs as separate files per service** (already done) — never combine into monolithic files | LOW | Already optimal — validate this remains the convention |
| 4 | **Design MCP servers with 10KB response limit** — paginate, summarize, strip metadata | HIGH (at MCP build time) | Prevents silent data corruption and session death loops |
| 5 | **Prime context before prompting** — open relevant files and scroll to relevant sections before typing a query | LOW | Leverages editor signal boosting at zero cost |
| 6 | **Use `#file` sparingly** — prefer `@workspace` or `#codebase` for discovery; use `#file` only when you know exactly which file the LLM needs | LOW | Prevents budget cannibalization |
| 7 | **Evaluate Copilot Spaces** for cross-repository architecture standards that multiple teams need | MEDIUM | Provides strict grounding without requiring every consumer to clone the architecture repo |

---

**Research source:** [Deep Research — Context Injection Pipeline](../research/deep-research-results-context-injection.md) (April 2026, 55 authoritative sources)

**See also:**

- [Build vs Leverage](build-vs-leverage.md) — Why native capabilities replace custom RAG
- [DD-01: Context and Configuration](../decisions/dd-01-context-configuration.md) — How the three options handle domain knowledge injection
- [Copilot Rollout Roadmap](../framework/copilot-rollout-roadmap.md) — Practical deployment plan incorporating these findings
