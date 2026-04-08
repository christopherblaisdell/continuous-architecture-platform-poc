<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2620588704/File-Type+Chunking+Strategy+for+GitHub+Copilot -->

# File-Type Chunking Strategy for GitHub Copilot

## The Problem

GitHub Copilot does not index all file types equally. Programming languages (Java, Python, TypeScript) receive AST-aware chunking via Tree-sitter — methods, classes, and functions are parsed into semantically whole units. But the architecture practice works primarily with **declarative and documentation formats** — OpenAPI YAML, Markdown ADRs, AsyncAPI event specs, PlantUML diagrams, Figma wireframes — which receive generic, structure-unaware chunking.

This means the files that matter most for architecture work are the files that Copilot handles worst.

Copilot exposes **no configuration** for chunking behavior. There are no VS Code settings, no `.copilot/` directory conventions, and no Enterprise admin controls that modify how the indexer slices files. This is a universal limitation — Cursor, Windsurf, and Claude Code have the same constraint.

This strategy defines **four workaround mechanisms** that together produce file-type-aware context delivery without requiring any change to Copilot's internal indexer. The approach is practical: each mechanism is deployable today using existing Copilot features.

### Evidence Base

This strategy is grounded in two rounds of deep research (112 authoritative sources total):

- [Deep Research — Context Injection Pipeline](../research/deep-research-results-context-injection.md) (April 2026, 55 sources)
- [Deep Research — Chunking Control by File Type](../research/deep-research-results-chunking-control.md) (April 2026, 57 sources)
- [Controlling What Copilot Sees](../evidence/context-injection-controls.md) — distilled evidence page

## Executive Summary

Copilot's native indexer chunks programming languages well but handles YAML, Markdown, and design files poorly — exactly the file types architecture teams rely on most. No configuration exists to change this behavior in any AI coding platform. This strategy defines four workaround mechanisms that together produce file-type-aware context delivery:

| Strategy | What It Does | Effort | Impact | When |
|----------|-------------|--------|--------|------|
| **1. File Decomposition** | Use physical file boundaries as chunk boundaries — keep YAML files under ~150 lines so each file fits in a single embedding chunk | LOW-MEDIUM | HIGH for YAML | Now |
| **2. Scoped Instructions** | Tell the LLM to actively retrieve missing context (e.g., "always fetch both endpoint and schema") — compensates for fragmented chunking at the reasoning layer | LOW | MEDIUM-HIGH | Now |
| **3. MCP Servers** | Replace native chunking entirely for specific file types — an OpenAPI MCP server returns complete endpoint definitions instead of raw YAML fragments | MEDIUM-HIGH | HIGH | Phase 4 |
| **4. AGENTS.md Routing** | Provide an explicit workspace map so the agent navigates to the right directories and tools instead of relying on blind vector search | LOW | MEDIUM | Now |

Three of the four strategies are deployable immediately with zero infrastructure. The MCP server strategy (highest impact for OpenAPI specs and Figma wireframes) requires evaluation and configuration but builds on existing open-source implementations.

The [Implementation Sequencing](#implementation-sequencing) section at the end provides a 10-step ordered plan aligned with the [Copilot Rollout Roadmap](copilot-rollout-roadmap.md).

---

## File-Type Decision Matrix

This is the primary reference artifact. For any architecture file type, look up the recommended delivery strategy and specific actions.

| File Type | Native Chunking Quality | Primary Strategy | Secondary Strategy | Target State |
|-----------|------------------------|-----------------|-------------------|-------------|
| **Java / TypeScript / Python source code** | HIGH — AST-aware, method-level boundaries | Native indexing (no action needed) | — | Already optimal |
| **Markdown ADRs and solution designs** | MEDIUM — heading-aware chunking, but no semantic anchoring for deeply nested sections | Heading structure discipline | Scoped instruction for ADR conventions | Enforce H1/H2/H3 hierarchy; ensure each H2 section is self-contained |
| **OpenAPI YAML specs (small, <150 lines)** | LOW — Tree-sitter parses YAML at key-value level but has no OpenAPI-specific awareness; no `$ref` resolution | File decomposition (keep under 150 lines) + scoped instruction | CLI bundling as validation layer | Already at one-spec-per-service; validate line counts |
| **OpenAPI YAML specs (large, >150 lines)** | VERY LOW — endpoint definitions severed from `$ref` schemas; Tree-sitter YAML grammar is purely syntactic, not semantic | **CLI bundling** (`swagger-cli bundle --dereference`) to produce a flattened artifact for Copilot ingestion | Scoped instruction + MCP server for dynamic queries | Run `swagger-cli bundle` in CI/pre-commit to generate flattened spec alongside modular source files — see [deep research results](../research/deep-research-results-puml-openapi-chunking.md) |
| **AsyncAPI event specs** | LOW — same generic chunking as OpenAPI | File decomposition + scoped instruction | MCP server (future) | Keep each event spec under 150 lines; instruct LLM to retrieve channel + schema together |
| **YAML metadata files (capabilities, tickets, domains)** | LOW — 60-line windows break key hierarchies | File decomposition (keep under 150 lines) | Descriptive file naming | Already small and focused; validate line counts |
| **PlantUML diagrams (.puml)** | LOW — no Tree-sitter grammar in Copilot (community grammars `lyndsysimon/tree-sitter-plantuml`, `Decodetalkers/tree_sitter_plantuml` exist but are abandoned/experimental and not integrated; Tree-sitter grammar org is not accepting new submissions); `!include` directives and C4 macros are opaque; falls back to `FixedWindowJaccardMatcher` 60-line sliding window with Jaccard similarity scoring | **CI/CD companion Markdown generation** — parse `.puml` files and generate structured summaries (participants, relationships, call flows) that Copilot indexes with near-perfect accuracy | Structured embedded comments (`' @participants:`) + `@startjson` embedded adjacency lists + scoped instruction + jebbs.plantuml LSP enrichment (active file only) + PlantUML MCP server (Infobip) for diagram generation/validation | Deploy companion generation script in CI; add structured comment conventions; embed `@startjson` service adjacency data; evaluate Infobip MCP for interactive use — see deep research results ([combined](../research/deep-research-results-puml-openapi-chunking.md), [dedicated](../research/deep-research-results-plantuml-chunking.md)) |
| **Figma wireframes** | NONE — binary `.fig` format is not indexable; SVGs are explicitly excluded from Copilot indexing (`**/*.svg` pattern); screenshots require manual attachment and suffer from state obfuscation; Figma designs are stored on figma.com, not in git | **Tripartite hybrid**: (1) CI/CD design token export to git (ambient awareness), (2) Figma Code Connect (maps components to code), (3) Figma MCP server (real-time frame queries via URL) | Companion Markdown descriptions as interim fallback | Deploy design token export first (Tier 2), then MCP server (Tier 3), then Code Connect — see [deep research results](../research/deep-research-results-figma-chunking.md) |
| **Configuration YAML (adventure-classification, test-standards)** | LOW — 60-line windows | File decomposition if >150 lines | Scoped instruction | Most config files are already small |
| **Confluence-migrated Markdown** | MEDIUM — heading-aware if properly structured | Post-migration heading cleanup | Scoped instruction for migrated content conventions | Ensure Pandoc output has clean heading hierarchy |

### How to Read This Matrix

- **Native Chunking Quality**: How well Copilot's built-in indexer handles this file type without intervention. HIGH means the indexer produces semantically coherent chunks; NONE means the indexer destroys the file's meaningful structure.
- **Primary Strategy**: The most effective mitigation. Do this first.
- **Secondary Strategy**: An additional layer that improves quality beyond the primary strategy.
- **Target State**: What "done" looks like for this file type.

---

## Strategy 1: File Decomposition

### Principle

Because Copilot's chunker does not understand YAML hierarchy or JSON structure, **physical file boundaries are the only reliable chunk boundaries** for non-code files. A file under ~150 lines fits within a single embedding chunk, ensuring the entire file is retrieved as a unit.

### When to Apply

Any YAML, JSON, or Markdown file exceeding 150 lines that cannot be served by an MCP server.

### Decomposition Patterns

#### OpenAPI Specs

Large monolithic specs should be split using YAML `$ref` pointers:

```
architecture/specs/svc-reservations/
  openapi.yaml              ← master file with info, servers, security
  paths/
    reservations.yaml       ← /reservations endpoints
    reservations-id.yaml    ← /reservations/{id} endpoints
    availability.yaml       ← /availability endpoints
  components/
    schemas/
      reservation.yaml      ← Reservation schema
      availability.yaml     ← Availability schema
      error.yaml             ← Error response schema
```

The master `openapi.yaml` uses `$ref: "./paths/reservations.yaml"` to link path definitions, and each path file uses `$ref: "./components/schemas/reservation.yaml"` for schema references. Each file stays under 150 lines. The complete spec is reconstructible by any OpenAPI tool, and Copilot retrieves each file as a coherent unit.

#### OpenAPI CLI Bundling (Complementary to Decomposition)

File decomposition is ideal for human authoring, but it is **actively detrimental to LLM retrieval** because Copilot's native indexer cannot follow `$ref` pointers across files. The solution is to decouple the authoring format from the ingestion format by generating a flattened artifact:

```bash
# In CI or pre-commit hook — generate a fully dereferenced spec
swagger-cli bundle -o api-bundled.yaml --dereference -t yaml api-main.yaml
```

The bundled file replaces every `$ref` with the literal YAML object it references, producing a single monolithic document where endpoints and their schemas are physically adjacent. Copilot indexes this flattened artifact, eliminating `$ref` hallucination entirely. The modular source files remain for human engineering and Git conflict mitigation.

**Key insight from [deep research](../research/deep-research-results-puml-openapi-chunking.md):** CLI bundling is the #1 ranked non-MCP approach for OpenAPI — higher impact than scoped instructions, AGENTS.md, or companion Markdown, and requires zero infrastructure (just a CI hook).

#### Markdown Documents

Long documents should be decomposed by section, with a parent index page:

```
architecture/solutions/_NTK-10020-redesign/
  NTK-10020-solution-design.md    ← master document with section links
  3.solution/
    i.impacts/
      impact.1.md                  ← svc-reservations impact (focused)
      impact.2.md                  ← svc-check-in impact (focused)
      impact.3.md                  ← svc-notifications impact (focused)
```

Each impact assessment is a self-contained document that Copilot can retrieve whole.

#### YAML Metadata

Split large metadata files by domain or concept:

```
architecture/metadata/
  capabilities-operations.yaml     ← Operations domain capabilities
  capabilities-booking.yaml        ← Booking domain capabilities
  capabilities-safety.yaml         ← Safety domain capabilities
```

Rather than one 500-line `capabilities.yaml`.

### Current State Assessment

The architecture workspace already uses one-spec-per-service (19 files). The next step is to **audit line counts** across all YAML and Markdown files and identify candidates that exceed the 150-line threshold.

### Effort and Impact

| Aspect | Assessment |
|--------|-----------|
| Effort | LOW to MEDIUM — mechanical file splitting, no logic changes |
| Impact | HIGH for YAML — transforms chunking from fragmented to whole-file |
| Risk | LOW — `$ref` is a standard OpenAPI mechanism; file splitting does not change semantics |
| Reversibility | Full — files can be recombined at any time |

---

## Strategy 2: Scoped Instructions as Retrieval Compensators

### Principle

When the chunker fragments a file, the LLM does not know it received an incomplete picture. A scoped instruction file can tell the LLM to **actively retrieve the missing context** before generating analysis. This does not fix the chunking — it compensates for it at the reasoning layer.

### When to Apply

Any file type where chunking regularly separates related content that the LLM needs together. Most valuable for YAML specs where endpoints and schemas are split across chunks.

### Scoped Instruction Examples

#### OpenAPI Spec Retrieval Instruction

```yaml
---
applyTo: "architecture/specs/**/*.yaml"
---
```

```markdown
# OpenAPI Spec Analysis Rules

When analyzing an OpenAPI specification:

1. **Always retrieve the complete endpoint definition** — the path, all parameters,
   request body schema, and all response schemas (including error responses).
   YAML files may be retrieved in fragments. If you see a `$ref` pointer,
   retrieve the referenced file before generating analysis.

2. **Never analyze an endpoint without its schemas.** If you have a path definition
   but not the component schema it references, retrieve the schema file first.

3. **Check for related endpoints.** If analyzing `POST /reservations`, also check
   whether `GET /reservations/{id}`, `PATCH /reservations/{id}`, and
   `DELETE /reservations/{id}` exist — they share schemas and understanding
   one endpoint often requires understanding the full resource lifecycle.

4. **Cross-reference with the service's AsyncAPI spec** (if one exists in
   `architecture/events/`) to understand what events this endpoint triggers.
```

#### ADR Context Instruction

```yaml
---
applyTo: "decisions/ADR-*.md"
---
```

```markdown
# ADR Analysis Rules

When referencing or analyzing an Architecture Decision Record:

1. **Read the full ADR** — never rely on just the Decision section. The Context,
   Decision Drivers, and Consequences sections are equally important.

2. **Check for supersession.** If the ADR's Status says "Superseded by ADR-XXX",
   retrieve and read the superseding ADR before providing analysis.

3. **Check for related ADRs.** ADRs frequently reference other ADRs in their
   Context section. Retrieve referenced ADRs to understand the full decision chain.
```

#### PlantUML Diagram Instruction

```yaml
---
applyTo: "**/*.puml"
---
```

```markdown
# PlantUML Diagram Rules

When analyzing or modifying PlantUML diagrams:

1. **Cross-reference with the OpenAPI spec** for any service referenced in the
   diagram. The spec is the source of truth for endpoint names, parameters,
   and response schemas.

2. **Check the C4 model conventions** in the architecture standards before
   modifying diagram structure.

3. **Verify cross-service calls** against `architecture/metadata/cross-service-calls.yaml`
   to ensure the diagram accurately reflects documented integration points.
```

### How Scoped Instructions Work with Chunking

Scoped instructions use `applyTo` glob patterns in their YAML frontmatter. When an architect opens a file matching the glob, the instruction is injected at **Priority 1** (system instructions) — the highest tier in Copilot's context hierarchy. This means the retrieval compensation rule is always present when the LLM processes the matching file type, regardless of how that file was chunked.

The critical distinction: `applyTo` controls **when instructions are injected**, not how files are chunked. The chunker still produces fragments. But the instruction tells the LLM to go fetch the missing pieces before reasoning — effectively reconstructing the whole from the parts.

### Effort and Impact

| Aspect | Assessment |
|--------|-----------|
| Effort | LOW — a few hundred lines of instruction files |
| Impact | MEDIUM to HIGH — compensates for fragmented retrieval at zero infrastructure cost |
| Risk | LOW — additive only, does not change any existing behavior |
| Reversibility | Instant — delete the instruction file |

---

## Strategy 3: MCP Servers as Semantic Chunking Layers

### Principle

The Model Context Protocol allows an external server to **replace Copilot's native chunking entirely** for specific data types. Instead of relying on the indexer to understand OpenAPI YAML structure, an MCP server parses the spec semantically and returns exactly the data the LLM requested — a complete endpoint definition, a full schema, a cross-service dependency graph — as a single, coherent response.

### When to Apply

File types where native chunking is destructive **and** the content has well-defined semantic units that a parser can extract. The strongest candidates are structured data formats with established parsers (OpenAPI, AsyncAPI) and design tools with REST APIs (Figma).

### Architecture Pattern

```
Architect asks: "What does POST /check-in expect?"
    │
    ├── Without MCP: Copilot searches raw YAML chunks
    │     → Retrieves lines 45-105 of svc-check-in spec
    │     → Endpoint definition present, but $ref schemas are in lines 200-280
    │     → LLM hallucinates the request body structure
    │
    └── With MCP: Copilot calls openapi-mcp tool
          → Server parses the full spec, extracts POST /check-in
          → Returns complete endpoint: path + parameters + request body
            + all referenced schemas + response codes
          → LLM reasons over the complete picture
```

### MCP Server Candidates

| Server | Data Type | How It Helps | Maturity |
|--------|-----------|-------------|----------|
| **openapi-mcp** | OpenAPI YAML | Exposes each endpoint as a tool; returns complete path + schema | Active open-source project |
| **mcp-openapi-schema-explorer** | OpenAPI YAML | Browse and search OpenAPI specs as interactive tools | Active open-source project |
| **Stainless MCP** | OpenAPI YAML | Automatically converts any OpenAPI spec into an MCP server | Commercial; active development |
| **@figma/mcp-server (official)** | Figma designs | Exposes `get_design_context`, `search_design_system`, `get_variable_defs`, and bidirectional write tools. Leverages Code Connect if configured. Requires paid Dev or Full seat on Organization/Enterprise plan. | Production-ready; maintained by Figma |
| **@yhy2001/figma-mcp-server** | Figma designs | Community server optimized for AI coding assistants. Smart Layout Detection translates absolute coordinates into Flexbox/Grid CSS before returning payload. L1 memory + L2 disk caching reduces API calls. | Active open-source project |
| **antonytm/figma-mcp-server** | Figma designs | WebSocket bridge to Figma desktop plugin — bypasses REST API read-only limits for free-tier users. Requires Figma desktop app running during session. | Active but higher operational friction |
| **AWS Labs OpenAPI MCP** | OpenAPI YAML | Dynamically generates MCP tools from OpenAPI specs; handles `$ref` dereferencing natively before transmitting to LLM | Active open-source (AWS Labs) |
| **Specbridge** | OpenAPI YAML | Converts complex OpenAPI specs into callable MCP tools | Active open-source project |
| **Infobip PlantUML MCP** | PlantUML diagrams | Exposes `generate_plantuml_diagram`, `encode_plantuml`, `decode_plantuml`. Supports `!include` directives and C4 macros natively. Structured syntax validation errors enable LLM self-correction via `plantuml_error_handling` prompt. | Active open-source; [Infobip developers blog](https://www.infobip.com/developers/blog/how-i-built-an-open-source-plantuml-mcp-server-without-writing-a-single-line-of-code) |
| **@brainstack/plantuml-mcp** | PlantUML diagrams | npm-based MCP server for diagram generation with custom corporate branding and multiple output formats | Active npm package |
| **junqing258/plantuml-mcp** | PlantUML diagrams | Validates syntax, extracts source from PNG/SVG metadata, generates diagrams | Active open-source project |
| **kwhrkzk/plantuml-validator-mcp-server** | PlantUML diagrams | Dedicated syntax validation for PlantUML code; MCPHub certified | Active open-source project |
| **Custom FastMCP (read-only)** | PlantUML diagrams | Purpose-built Python server exposing `list_diagrams(domain)`, `get_diagram_source(file_path)` (resolves `!include` directives), `get_service_dependencies(service_name)`. Fills the retrieval gap that rendering-focused MCP servers do not address. | Would need to be built (est. 3-5 days) |
| **mcp-vector-search** | Any file type | Independent AST-aware chunking with its own vector store | Experimental |
| **Custom FastMCP** | AsyncAPI, YAML metadata | Purpose-built server for architecture metadata queries | Would need to be built |

### MCP Design Constraints for Copilot

All MCP servers must be designed within Copilot's hard constraints:

| Constraint | Limit | Design Rule |
|-----------|-------|------------|
| Response size | 10KB hard truncation (silent) | Return one endpoint per call, not the full spec. Target responses under 5KB. |
| Extended sessions | HTTP 413 from accumulated history | Paginate list operations (10-25 items per page with cursor) |
| Tool schema bloat | Each tool's schema consumes system prompt tokens | Limit to 10-15 tools per server; combine related queries into parameterized tools |
| Startup time | MCP server must be running before Copilot can use it | Use `stdio` transport for local servers (auto-started by VS Code) |

### Implementation Approach: OpenAPI MCP Server

The highest-value MCP implementation for this workspace is an OpenAPI server for the 19 service specs. A phased approach:

**Phase 1 — Evaluate existing implementations (1-2 days)**

Test `openapi-mcp` and `mcp-openapi-schema-explorer` against the architecture workspace specs. Evaluate:

- Does it parse multi-file `$ref` specs correctly?
- Does it return complete endpoint definitions within the 10KB limit?
- Does it handle the 19-service spec collection without excessive tool schema bloat?
- Does it integrate with VS Code's MCP configuration (`.vscode/mcp.json`)?

**Phase 2 — Configure or build (2-5 days)**

If an existing server works: configure it for the workspace, add to `.vscode/mcp.json`, document usage in the scoped instruction file.

If no existing server fits: build a custom FastMCP server in Python. The architecture workspace already has Python tooling. The server loads all specs at startup, parses them with `pyyaml`, and exposes parameterized tools:

- `get_endpoint(service, method, path)` — returns complete endpoint definition + referenced schemas
- `list_endpoints(service)` — returns endpoint summaries (name, method, path, description)
- `search_schemas(query)` — searches across all service schemas by keyword
- `get_cross_service_calls(service)` — returns integration points from metadata YAML

**Phase 3 — Team onboarding (1 day)**

Add MCP server to `.vscode/mcp.json` (version-controlled). Every architect who clones the repo gets the MCP server configuration automatically. Add usage guidance to the onboarding instruction file.

### Effort and Impact

| Aspect | Assessment |
|--------|-----------|
| Effort | MEDIUM to HIGH — 3-8 days depending on whether existing implementations fit |
| Impact | HIGH — eliminates the worst chunking blind spot (YAML spec fragmentation) |
| Risk | MEDIUM — MCP is a rapidly evolving standard; server implementations may need updates |
| Reversibility | Full — remove MCP server config, native indexing continues working |

---

## Strategy 4: AGENTS.md as a Repository Routing Layer

### Principle

AGENTS.md is an emerging standard (adopted by 60,000+ repositories) that provides an explicit topology map for AI agents. Instead of relying on blind vector search to discover where relevant files live, the agent reads AGENTS.md to understand the workspace structure — which directories contain specs, which contain source code, which contain ADRs, and which MCP tools to use for each.

### When to Apply

Any repository where the AI agent needs to navigate between different file types that live in different directories and require different retrieval strategies.

### How It Improves Chunking Outcomes

AGENTS.md does not change how files are chunked. It changes **which files the agent decides to read**. By providing explicit directory-to-purpose mappings, the agent makes better retrieval decisions:

- For an OpenAPI question, go directly to `architecture/specs/` instead of searching the full workspace
- For a prior decision, go to `decisions/` instead of hoping vector search surfaces the right ADR
- For event schemas, go to `architecture/events/` rather than retrieving random YAML metadata files
- When an MCP server is available for a file type, prefer the MCP tool over native file reading

### AGENTS.md Structure for This Workspace

```markdown
# AGENTS.md

## Repository Overview
This is an architecture workspace for evaluating AI toolchains
and managing architecture artifacts for a microservice ecosystem.

## Directory Map

| Directory | Contents | Retrieval Guidance |
|-----------|----------|-------------------|
| `architecture/specs/` | OpenAPI YAML specs (19 services) | Use OpenAPI MCP server if available; otherwise read individual spec files |
| `architecture/events/` | AsyncAPI event specs (8 services) | Read individual event spec files; cross-reference with metadata/events.yaml |
| `architecture/metadata/` | Domain classifications, capabilities, cross-service calls, data stores | Read individual YAML files; these are the source of truth for service topology |
| `architecture/solutions/` | Solution designs organized by ticket | Read the master document first, then drill into subdirectories |
| Figma (external) | Wireframes and UI designs hosted on figma.com | Use Figma MCP server if available; otherwise reference companion Markdown descriptions in `docs/wireframes/` |
| `decisions/` | MADR-format architecture decision records | Read the full ADR — never rely on just the title or decision section |
| `config/` | Configuration YAML (adventure classification, test standards) | Small files; read directly |
| `portal/docs/` | MkDocs documentation portal source | Reference for published documentation; not primary architecture artifacts |
| `source-code/` | Java source code for services | Native indexing is adequate; use standard code navigation |

## MCP Servers

| Server | Purpose | When to Use |
|--------|---------|-------------|
| OpenAPI MCP | Query endpoint definitions with complete schemas | When analyzing API contracts, checking backward compatibility, or designing cross-service integrations |
| Figma MCP | Query wireframe structure, component properties, and design tokens | When referencing UI designs in solution proposals or identifying data requirements from screens |

## Conventions
- One OpenAPI spec per service (never combine specs)
- MADR format for all architecture decisions
- Solution designs follow the folder structure in copilot-instructions.md
```

### Effort and Impact

| Aspect | Assessment |
|--------|-----------|
| Effort | LOW — one file, a few dozen lines |
| Impact | MEDIUM — reduces blind search, improves retrieval targeting |
| Risk | NONE — purely additive; does not change any behavior if the agent ignores it |
| Reversibility | Instant — delete the file |

---

## Cross-Cutting Guidelines

These practices improve chunking outcomes across all file types.

### File Naming Conventions

Descriptive file names improve Copilot's **lexical search layer**, which augments the semantic vector search. Hybrid retrieval (keyword + embedding) outperforms either approach alone. Good file names are essentially free metadata.

| Pattern | Example | Why It Helps |
|---------|---------|-------------|
| Include service name | `svc-check-in-openapi.yaml` | Keyword match on service queries |
| Include asset type | `adr-005-pattern3-default-fallback.md` | Distinguishes ADRs from solution docs by name |
| Include domain | `capabilities-operations.yaml` | Scopes metadata queries by domain |
| Avoid generic names | `spec.yaml`, `data.json`, `config.yaml` | These match every query indiscriminately |

### Markdown Heading Discipline

Copilot's Markdown chunking splits at heading boundaries and anchors each chunk with its parent heading hierarchy. This means well-structured headings produce self-contained chunks:

| Structure | Chunking Result |
|-----------|----------------|
| H1 → H2 → H3 with content under each | Each H2 section is a retrievable unit, anchored to the H1 title |
| Long paragraphs without headings | Arbitrary 512-1,024 token slices with no context about what section they belong to |
| H2 sections that reference content in other H2 sections | Cross-references break — each chunk is retrieved independently |

**Rule:** Every H2 section should be comprehensible in isolation. If understanding a section requires reading a different section, consolidate them or add a brief summary at the top of each.

### `#file` vs `@workspace` vs `#codebase` Usage

How the architect invokes context affects which retrieval path is used:

| Invocation | Retrieval Path | Best For | Token Budget Impact |
|-----------|---------------|---------|-------------------|
| `#file path/to/file` | Direct file injection (Priority 2) | When you know exactly which file the LLM needs | Consumes budget before semantic retrieval runs — use sparingly |
| `@workspace query` | Semantic + editor signals (Priority 5) | Context-aware queries anchored to what you are currently working on | Dynamically sized based on remaining budget |
| `#codebase query` | Pure semantic vector search (Priority 5) | Broad discovery queries across the full repository | Unbiased by currently open files |

**Guideline:** Default to `@workspace` for most queries. Use `#file` only when you need a specific file that semantic search might not surface (e.g., a metadata YAML file with no natural language content). Use `#codebase` when you want to search without bias toward your currently open files.

### Context Priming

Copilot weights currently visible content higher than background files. Before issuing a complex prompt:

1. **Open the most relevant file** — the active editor has the highest retrieval weight
2. **Scroll to the relevant section** — the visible viewport is prioritized over hidden content
3. **Click through related files** — recently opened files get a temporary boost
4. **Let import chains work** — if your cursor is in code that imports from another file, that file is automatically boosted

These actions are free. They take seconds and measurably improve retrieval quality.

### Copilot Spaces for Cross-Repository Content

When architecture standards, shared schemas, or reference documentation live in a different GitHub repository from the workspace, **Copilot Spaces** provide strict grounding without requiring every consumer to clone the source repo.

Spaces aggregate content from multiple GitHub repositories and provide it as curated context. Use cases for the architecture practice:

- Shared architecture standards referenced by multiple team repositories
- Cross-team API specifications that define integration contracts
- Organization-wide ADRs that constrain per-team design decisions

**Limitation:** Spaces only work with GitHub-hosted content. External systems (Confluence, SharePoint, Jira) still require the MCP bridge approach.

---

## Implementation Sequencing

These strategies are not independent — they build on each other and align with the [Copilot Rollout Roadmap](copilot-rollout-roadmap.md) phases.

| Sequence | Strategy | Rollout Phase | Effort | Prerequisite |
|----------|----------|---------------|--------|-------------|
| 1 | **Audit file sizes** — identify all YAML and Markdown files exceeding 150 lines | Phase 3 prep | LOW (hours) | None |
| 2 | **Add scoped instruction files** — OpenAPI retrieval rules, ADR context rules, PlantUML cross-reference rules | Phase 3.2 | LOW (1-2 days) | None |
| 3 | **Create AGENTS.md** — explicit workspace topology map for AI agent navigation | Phase 3.2 | LOW (hours) | None |
| 4 | **Decompose oversized files** — split large specs and metadata using `$ref` pointers and directory structure | Phase 3 | MEDIUM (2-3 days) | Step 1 audit results |
| 5 | **Enforce file naming conventions** — rename generic files, document naming standard | Phase 3 | LOW (hours) | None |
| 6 | **Enforce Markdown heading discipline** — audit and restructure documents without consistent headings; add author guidance to instruction files | Phase 3 | LOW (1-2 days) | None |
| 7 | **Evaluate OpenAPI MCP server** — test existing implementations against workspace specs | Phase 4.2 | MEDIUM (1-2 days) | None (but Steps 1-3 should be done first) |
| 8 | **Deploy OpenAPI MCP server** — configure or build, add to `.vscode/mcp.json`, update AGENTS.md | Phase 4.2 | MEDIUM-HIGH (3-8 days) | Step 7 evaluation |
| 9 | **Evaluate Copilot Spaces** — assess cross-repository architecture content needs | Phase 4.1 | MEDIUM (1-2 days) | Team scaling triggers this |
| 10 | **Figma integration** — deploy design token CI/CD export (Phase 1), evaluate and configure Figma MCP server (Phase 2), set up Code Connect for high-impact components (Phase 3). [Deep research complete](../research/deep-research-results-figma-chunking.md) — recommends tripartite hybrid pattern. | Phase 4.2 | MEDIUM-HIGH (phased rollout) | Figma is the team's wireframing tool |
| 11 | **OpenAPI CLI bundling** — add `swagger-cli bundle --dereference` to CI pipeline to generate flattened specs alongside modular source files. [Deep research complete](../research/deep-research-results-puml-openapi-chunking.md) — ranked #1 non-MCP approach. | Phase 3 | LOW (hours) | Step 1 audit results |
| 12 | **PlantUML companion Markdown generation** — build CI script to parse `.puml` files and generate structured Markdown summaries (participants, relationships, call flows). [Deep research complete](../research/deep-research-results-puml-openapi-chunking.md) — ranked #1 for PlantUML. | Phase 3 | MEDIUM (1-3 days) | None |
| 13 | **Add `@startjson` embedded metadata to PlantUML files** — append native `@startjson` blocks with service adjacency lists to high-value diagrams. Even without a Tree-sitter `.puml` grammar, the localized JSON density gives the LLM unambiguous relationship data when the chunk is retrieved. | Phase 3 | LOW (hours) | None |
| 14 | **Evaluate PlantUML MCP servers** — test Infobip, @brainstack, and junqing258 PlantUML MCP servers for diagram generation, syntax validation, and `!include` resolution. Assess whether a custom read-only FastMCP server is needed for architectural querying (`list_diagrams`, `get_service_dependencies`). | Phase 4.2 | MEDIUM (1-2 days) | Step 12 informs what gaps remain |

### Quick Wins (This Week)

Steps 1, 2, 3, 5, 11, and 13 can be completed immediately with no infrastructure and no risk. CLI bundling (Step 11) is the single highest-impact quick win for OpenAPI — it entirely eliminates `$ref` hallucination with a one-line CI hook. Embedded `@startjson` metadata (Step 13) is the equivalent quick win for PlantUML.

### Medium-Term (Phase 3-4)

Steps 4, 6, 7, 8, and 12 require meaningful effort but address the most severe chunking blind spots. PlantUML companion Markdown generation (Step 12) is the highest-impact item for diagram retrieval quality. The OpenAPI MCP server (Steps 7-8) provides dynamic query power beyond what CLI bundling alone delivers.

!!! note "jebbs.plantuml Extension (Zero-Cost Boost)"
    The **jebbs.plantuml** VS Code extension (3M+ installs) implements a `DocumentSymbolProvider` that parses `.puml` files and exposes participant/actor declarations to Copilot via the Language Server Protocol. This enriches the context window for the **active editor file only** — it does not improve `@workspace` retrieval. The team should ensure this extension is installed. Limitation: the symbol parser uses regex, not AST, so it fails on deeply nested C4 macros.

### As Needed (Triggered by Use Cases)

Steps 9, 10, and 14 are triggered by specific organizational events or evolving requirements. The Figma research (Step 10) has [deep research results](../research/deep-research-results-figma-chunking.md) recommending a tripartite hybrid pattern. PlantUML + OpenAPI research (Steps 11-14) has deep research results ([combined](../research/deep-research-results-puml-openapi-chunking.md), [dedicated PlantUML](../research/deep-research-results-plantuml-chunking.md)) — CLI bundling and companion Markdown generation are recommended before evaluating MCP servers.

### Total Effort

Across all 14 steps: approximately 3-4 weeks of architecture team time, spread across Phases 3 and 4 of the rollout roadmap. Steps 1-6, 11, and 13 (the quick wins) can be completed in a single sprint.

### Long-Term Alternative: Structurizr DSL

The [dedicated PlantUML research](../research/deep-research-results-plantuml-chunking.md) identifies **Structurizr DSL** as a potential long-term paradigm shift. Unlike PlantUML (presentation-based — describes how a diagram looks), Structurizr is model-based — elements are defined once in a central model, and diagram views are generated from it. LLMs excel at generating and reading Structurizr DSL because it is highly structured text with strict C4 rules, lacking the noisy presentation directives that confuse vector embeddings. Structurizr can export views to PlantUML or Mermaid automatically.

This is not recommended for the immediate term (migrating 140+ diagrams is months of effort), but for teams starting fresh with C4 architecture, Structurizr DSL would eliminate the PlantUML chunking problem entirely. **D2** is another modern alternative with actively maintained Tree-sitter grammars (`pleshevskiy/tree-sitter-d2`, `ravsii/tree-sitter-d2`), which would provide vastly superior semantic chunking if integrated.

### Open Questions for Empirical Testing

The dedicated PlantUML research identifies four experiments that would validate assumptions:

1. **Remote RAG chunk size for `.puml` files** — The local 60-line Jaccard window is documented, but the remote semantic indexer's exact token boundary and overlap for unknown file types needs empirical measurement.
2. **LSP symbol weighting** — Does Copilot weight the `DocumentSymbol` data from jebbs.plantuml higher than raw text chunks? Does it persist after the file is closed?
3. **JSON vs Markdown shadow files** — A/B testing to determine whether companion `.json` adjacency lists or `.summary.md` prose yield higher retrieval accuracy.
4. **SVG exclusion override** — Testing whether removing `**/*.svg` from exclusion patterns allows Copilot to index the XML `<text>` nodes inside rendered PlantUML SVGs.

---

**See also:**

- [Controlling What Copilot Sees](../evidence/context-injection-controls.md) — Evidence page with full technical analysis of Copilot's context injection pipeline
- [Copilot Rollout Roadmap](copilot-rollout-roadmap.md) — Practical deployment plan that references this strategy
- [Build vs Leverage](../evidence/build-vs-leverage.md) — Why native capabilities replace custom RAG for most use cases
- [File-Type Handling: A vs C](../evidence/filetype-handling-a-vs-c.md) — Side-by-side comparison of Option A and Option C for each architecture file type
- [DD-01: Context and Configuration](../decisions/dd-01-context-configuration.md) — How the three options handle domain knowledge injection
