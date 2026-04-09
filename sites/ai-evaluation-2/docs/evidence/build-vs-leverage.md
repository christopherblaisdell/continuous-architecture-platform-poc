<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2615148826/Build+vs+Leverage+Custom+RAG+in+Context -->

# Build vs Leverage: Custom RAG in Context

## When Custom RAG Is the Right Answer

Building a custom Retrieval-Augmented Generation (RAG) pipeline is a well-established pattern when **AI is the product**. Organizations whose core business is delivering AI-powered experiences — search engines, recommendation systems, domain-specific copilots sold to customers — rightfully invest in:

- **Vector databases** (Pinecone, Weaviate, Qdrant) for embedding storage and similarity search
- **Chunking and embedding pipelines** to ingest proprietary corpora
- **Prompt orchestration frameworks** (LangChain, LlamaIndex) to compose retrieval with generation
- **Fine-tuned or distilled models** optimized for their specific domain
- **Evaluation harnesses** (RAGAS, custom benchmarks) to measure retrieval precision and answer quality

This investment is justified because the RAG pipeline *is* the product. The engineering team owns every layer, tunes every parameter, and differentiates on retrieval quality.

## When Custom RAG Reinvents the Wheel

The calculus changes entirely when **AI is a tool** — when the goal is to augment developers and architects working inside an IDE, not to ship an AI product to customers.

For IDE-integrated architecture and coding workflows, the custom RAG approach reconstructs capabilities that already exist natively across multiple modern AI coding platforms:

| RAG Pipeline Component | What You Build | Native Platform Equivalent | Platforms That Offer This |
|------------------------|----------------|---------------------------|---------------------------|
| Document ingestion | Chunking scripts, embedding jobs, scheduled re-indexing | Workspace indexing — automatic, incremental, zero-config | Copilot, Cursor, Windsurf, Claude Code |
| Vector store | Pinecone/Weaviate cluster, schema design, capacity planning | Built-in semantic search index (local + cloud) | Copilot, Cursor, Windsurf, Claude Code |
| Retrieval | Similarity search queries, re-ranking, context window assembly | `@workspace` / `@codebase` — single command retrieves relevant files and symbols | Copilot, Cursor, Windsurf, Cline |
| Context injection | Custom prompt templates stitching retrieved chunks into system prompts | Declarative instruction files — no code required | All five (1) |
| Behavior configuration | Prompt engineering, agent routing logic, mode switching | Rules, custom agents, tool restrictions — all workspace-as-code | Copilot, Cursor, Windsurf, Cline |
| Tool integration | MCP server development, function-calling schemas, tool dispatch | Native MCP support, built-in tools, extensible via MCP | All five |
| Multi-agent orchestration | Agent framework (CrewAI, AutoGen), coordination logic, state management | Native sub-agents, automatic tool delegation | Copilot, Windsurf, Cline, Claude Code |
| Evaluation | Custom benchmarks, A/B testing embedding models | Direct observation + git-branched A/B testing of customizations — same IDE, same workflow, immediate feedback | All platforms |

(1) Each platform uses its own file convention — Copilot: `.instructions.md`, `SKILL.md`; Cursor: `.cursor/rules/*.md`; Windsurf: `.windsurf/rules/*.md`, `.windsurf/skills/`; Cline: `.clinerules/*.md`; Claude Code: `CLAUDE.md` with Skills and Subagents — but a cross-platform standard is emerging via `AGENTS.md` (supported by Copilot, Cursor, Windsurf, and Cline) and the open [Agent Skills](https://agentskills.io) specification (originally developed by Anthropic, now under open governance).

### The Infrastructure Tax

Every component in the left column requires:

- **Development effort** to build and integrate
- **Operational overhead** to monitor, scale, and maintain
- **Ongoing cost** for compute, storage, and API calls
- **Expertise** in ML infrastructure that may not exist on the architecture team

Every major AI coding platform — GitHub Copilot, Cursor, Windsurf, Cline, Claude Code — delivers these capabilities as native features. No infrastructure to provision, no pipelines to maintain, no embedding jobs to schedule. The choice between platforms is a selection decision, not a build decision.

## The Core Argument

Custom RAG is the right choice when your organization's competitive advantage depends on retrieval quality and you need full control over every layer of the AI pipeline.

It is the wrong choice when:

1. **The AI platform already indexes your workspace** — all major platforms (Copilot, Cursor, Windsurf, Claude Code) perform workspace indexing automatically and incrementally
2. **Context injection is solved by convention** — every platform supports declarative instruction files that inject domain knowledge without writing code
3. **The team's expertise is architecture, not ML infrastructure** — time spent maintaining embedding pipelines is time not spent on architecture work
4. **The cost model penalizes complexity** — every additional component (vector DB, embedding service, orchestration layer) adds to TCO with no proportional quality gain over native capabilities

## The PlantUML Chunking Argument

A common concern is that a bespoke agent is required to control how specific file types — particularly PlantUML diagrams — are chunked for retrieval. The argument assumes that general-purpose workspace indexing will misparse `.puml` files, producing semantically broken chunks that degrade retrieval quality.

This concern is valid **in the abstract** but irrelevant to the architecture practice's actual workflow:

**The architect already works with PlantUML files inside VS Code.** Every `.puml` source file lives in the workspace alongside the OpenAPI specs, metadata YAML, and markdown documentation that reference them. The AI agent does not need to "retrieve" PlantUML through an embedding pipeline — it reads the files directly from the workspace, exactly as it reads any other source file.

The architecture practice pilot proved this empirically. Using GitHub Copilot (Option A) with zero custom chunking infrastructure:

- **139 PlantUML sequence diagrams** were generated from OpenAPI specs by the AI agent
- The agent **reads, modifies, and creates** `.puml` files using standard file operations — no embedding or retrieval step is involved
- Cross-references between PlantUML diagrams and service documentation are maintained through workspace-relative paths that the agent navigates directly
- The generator script (`portal/scripts/generate-microservice-pages.py`) produces PUML, renders SVGs, and writes markdown pages — all orchestrated by the AI agent operating on workspace files

**Why this matters:** The chunking concern assumes a retrieval-first architecture where PlantUML content must be embedded, stored in a vector database, and retrieved via similarity search before the model can reason about it. In an IDE-native workflow, the model has **direct file access** — it reads the `.puml` file, understands its structure, and operates on it. No chunking. No embeddings. No retrieval pipeline.

This is a concrete example of the broader pattern: concerns about custom RAG pipeline control often assume a retrieval architecture that IDE-native platforms bypass entirely. The files are already there. The agent reads them directly.

## The Pipeline Composition Argument

A related argument holds that a self-managed embedding pipeline enables programmatic composition: retrieved chunks flow through compliance checks, metadata filters, and custom modes before reaching the model. The architect still works in VS Code — the difference is in *where the AI gets its context from* and *what processing happens between retrieval and reasoning*.

The envisioned pipeline looks like:

1. **Retrieve** — query a custom vector DB with metadata filters (service name, document type, recency)
2. **Lint/Validate** — run compliance checks against retrieved chunks before feeding them to the model
3. **Synthesize** — the model reasons over precisely curated, pre-validated context

This is a genuine architectural vision. The question is whether the incremental retrieval quality justifies the engineering investment to build it — and whether platform-native mechanisms already achieve the same outcome through different means.

### What Platform-Native Workflows Already Provide

| Pipeline Step | Custom Embedding Pipeline | Platform-Native Equivalent |
|---------------|---------------------------|---------------------------|
| Scoped retrieval | Metadata-filtered vector query | Directory structure as implicit metadata + scoped `.instructions.md` files that activate context by file path |
| Compliance checks on context | Pre-retrieval validation scripts | Agentic linting at authoring time — the model invokes Spectral, puml-lint, and other validators directly in VS Code, getting immediate feedback before any output is produced |
| Custom modes | Roo Code modes selecting different retrieval strategies | Copilot custom agents with tool restrictions, scoped instructions, and skill definitions — all declarative, all version-controlled |
| Multi-step composition | Programmatic orchestration code (LangChain, custom framework) | Native MCP servers feeding data + sub-agents delegating tasks + skills defining workflows — composable without custom code |

### The Critical Distinction: Retrieval-Time vs Authoring-Time Quality

The custom pipeline model places quality gates **between retrieval and reasoning** — filtering and validating what the model sees. The platform-native model places quality gates **at the point of authoring** — the model invokes linters, reads specs, and validates its own output against workspace artifacts.

Both approaches aim for the same outcome: high-quality, compliant architecture output. The difference is where the quality check happens:

- **Custom pipeline:** Quality is enforced in the retrieval layer (before the model reasons)
- **Platform-native:** Quality is enforced in the agentic loop (while the model reasons)

The pilot evidence suggests the platform-native approach works: 4 solution designs, 14 ADRs, and 139 diagrams were produced with the model reading files directly, invoking linters agentically, and validating output against OpenAPI specs and metadata — no retrieval-layer compliance pipeline required.

### The Engineering Cost

The custom pipeline is not free. Building the retrieval → validation → synthesis chain requires:

- Vector database provisioning and schema design
- Custom chunking and metadata tagging scripts
- Compliance validation logic running against retrieved chunks
- Orchestration framework to chain the steps
- Ongoing maintenance as document schemas, compliance rules, and retrieval requirements evolve

This is a multi-month engineering project requiring ML infrastructure expertise. It produces a retrieval backend that solves a problem the pilot has not demonstrated exists — the 96%+ architecture output quality scores were achieved without any custom retrieval layer.

!!! note "When This Investment Becomes Justified"
    If the architecture practice grows to consume content from multiple repositories, external knowledge bases (Confluence, SharePoint), or unstructured sources where platform-native indexing demonstrably fails, a custom retrieval pipeline becomes justified. Similarly, if retrieval quality becomes a measurable bottleneck, the ability to maintain versioned vector collections, A/B test different chunking strategies and embedding models, and evaluate retrieval against actual query patterns using formal metrics (MRR, NDCG) becomes valuable — but this is search system R&D, not architecture work. It requires labeled evaluation datasets, ML infrastructure expertise, and an experiment tracking framework. Note that A/B testing of *agent behavior* (instructions, custom agents, skills) is already available via git branching — the custom infrastructure is only needed for A/B testing the *embedding and retrieval layer* specifically. The pilot's pragmatic alternative — testing with real architecture scenarios and measuring output quality directly — achieves a similar outcome without that investment. The recommendation is to adopt platform-native indexing now — and build custom retrieval infrastructure only when a concrete retrieval quality problem is observed, not speculatively.

## Cross-Tool Accessibility

A self-managed vector database is accessible from any tool: CLI scripts, web applications, CI/CD pipelines, Slack bots, custom dashboards. Platform-native indexes are locked inside the IDE — you cannot query Copilot's workspace index from a terminal command, a web app, or an automated compliance check running in CI.

**This is a genuine limitation of platform-native indexing.** It is not a theoretical concern or a misunderstanding — it is a real architectural constraint that should be acknowledged directly.

### Relevance to the Architecture Practice Today

The architecture practice pilot workflow is entirely IDE-based. Every activity — ticket analysis, solution design, impact assessment, ADR authoring, diagram generation, portal publishing — happens inside VS Code with the AI agent operating on workspace files. No step in the current workflow requires querying the semantic index from outside the IDE.

Cross-tool access becomes relevant when the practice needs:

| Use Case | Requires Index Access From | Status |
|----------|---------------------------|--------|
| Standards compliance checker in CI | CI/CD pipeline | Not yet needed — agentic linting runs in IDE at authoring time |
| Web-based architecture knowledge base | Web application | Not yet needed — the MkDocs portal serves this role with static content |
| Slack bot answering architecture questions | Chat platform API | Not yet needed — architects use VS Code directly |
| Automated cross-repo dependency analysis | Batch processing job | Not yet needed — the practice operates on a single repository |

None of these use cases exist in the current workflow. Building a cross-tool-accessible vector store to serve speculative future needs is premature infrastructure investment.

### MCP as a Partial Bridge

The Model Context Protocol (MCP) partially addresses this limitation. MCP servers can expose workspace data — file contents, search results, structured metadata — to any MCP-compatible client. If a future use case requires non-IDE access to architecture content:

1. An MCP server exposing the workspace's file contents and metadata already makes that content queryable by external tools
2. If semantic search (not just file access) is needed externally, a lightweight local vector database exposed via MCP provides cross-tool semantic search without a full custom embedding pipeline
3. This hybrid approach — platform-native indexing for IDE workflows plus a targeted MCP-exposed vector store for specific external needs — captures the cross-tool benefit without replacing the entire retrieval layer

!!! tip "The Pragmatic Path"
    Accept the IDE lock-in for now — it costs nothing and the workflow is IDE-native. If a concrete cross-tool use case emerges (e.g., a CI-based compliance checker needs semantic search), build a lightweight MCP-exposed vector store for that specific need. Do not build cross-tool infrastructure speculatively.

## Implications for This Evaluation

This analysis directly informs two evaluation factors:

- **EF-08 Time to Value**: Option A delivers context-aware AI assistance from day one with declarative configuration. Option B requires building and validating the RAG pipeline before productive use begins.
- **EF-09 Operational Complexity**: Option A adds zero infrastructure. Option B adds vector storage, embedding pipelines, and prompt orchestration as ongoing operational responsibilities.

The dedicated decision page [DD-01 Context and Configuration](../decisions/dd-01-context-configuration.md) evaluates how each option handles knowledge injection and behavior customization.

For the argument that these platforms only work for coding and that architecture requires a bespoke solution, see [Architecture Is Not Just Coding](architecture-not-just-coding.md).

For evidence that Azure AI Search does not actually chunk architecture files better than Copilot, see [File-Type Handling: A vs C](filetype-handling-a-vs-c.md).

For how Option D preserves the Foundry model investment without requiring custom RAG infrastructure, see [Option D — Hybrid Architecture](option-d-hybrid-architecture.md).
