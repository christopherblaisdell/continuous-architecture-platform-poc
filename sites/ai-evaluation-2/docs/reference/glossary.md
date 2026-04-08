# Glossary

This evaluation uses terminology that overlaps across vendors, open-source projects, and marketing materials. This page defines each term precisely as used on this site so that comparisons are grounded in shared definitions.

## Content and Retrieval

**Content**
:   The architecture artifacts themselves — ADRs, OpenAPI specs, PlantUML diagrams, solution designs, YAML metadata. Content lives in files (usually in git repositories or SharePoint). Content is inherently portable: it is just files.

**Workspace Indexing**
:   The process by which an IDE platform (Copilot, Cursor, Windsurf, Claude Code) automatically parses, chunks, embeds, and indexes all files in the currently open workspace. Requires zero configuration. Indexing is per-workspace and per-client — each platform builds its own index from the same source files.

**Platform-Native Indexing**
:   Workspace indexing provided by the AI platform itself as a built-in feature. No infrastructure to provision, no embedding models to select, no vector databases to manage. The platform handles chunking strategy, embedding generation, index refresh, and semantic search internally.

**RAG (Retrieval-Augmented Generation)**
:   A pattern where an AI model's response is grounded in retrieved documents rather than relying solely on training data. The system retrieves relevant content from an index, then passes it to the LLM as context. Both workspace indexing and Foundry IQ implement RAG — the difference is who builds and manages the retrieval pipeline.

**Agentic Retrieval**
:   A Foundry IQ feature where an LLM plans and executes multiple search queries in parallel before synthesizing results. Differs from single-shot RAG (one query, one result set) by using reasoning to decompose complex questions. Microsoft reports 36% higher response quality compared to single-shot retrieval.

**Knowledge Base**
:   A Foundry IQ concept: a configured collection of knowledge sources (SharePoint sites, Azure Blob containers, OneLake paths) with retrieval instructions, chunking rules, and access control policies. Not to be confused with a general-purpose "knowledge base" (a wiki or document collection).

## Customization

**Customizations**
:   The umbrella term for all configuration that shapes how an AI agent behaves in a specific context. Includes instructions, skills, agent definitions, and MCP server configurations. Customizations are declarative (Markdown files checked into the repository), not code.

**Instructions**
:   Markdown files (`.instructions.md`, `copilot-instructions.md`) that provide behavioral guidance to the AI agent. Instructions tell the agent *how to work* in a specific context — coding conventions, domain rules, workflow patterns. They are scoped by glob pattern or folder. Content is plain text and inherently portable; the file naming convention varies by platform.

**Skills**
:   Modular, on-demand workflow packages defined in `SKILL.md` files. A skill bundles procedural knowledge (e.g., "how to create a solution design") with optional supporting files (templates, checklists, scripts). Skills are loaded lazily — the agent reads only the description at startup and pulls the full content when invoked. The SKILL.md format follows an emerging open standard from [agentskills.io](https://agentskills.io).

**Agent Definitions**
:   Configuration files (`.agent.md`) that define specialized agent personas with specific tool restrictions, instructions, and behavioral profiles. Example: a "Solution Architect" agent that can only use architecture tools and follows MADR format. The format is currently Copilot-specific, but the *content* (the behavioral rules) is transferable.

**Knowledge Layer**
:   This term is used inconsistently across the conversation and should be avoided without qualification. It can mean:

    1. **Customization layer** — the set of instruction files, skills, and agent definitions that shape agent behavior (what this evaluation primarily discusses)
    2. **Retrieval layer** — the search index and embedding infrastructure that lets an agent find relevant content (what Foundry IQ provides)
    3. **Content layer** — the actual documents and artifacts being searched (what lives in git or SharePoint)

    When precision matters, use one of the three specific terms above instead.

## Workloads

**Generation Workload**
:   The use of an AI agent to *produce* architecture artifacts — writing ADRs, analyzing OpenAPI specs, creating PlantUML diagrams, drafting solution designs, generating impact assessments. The agent works within a single workspace, using the open files and repository content as context. This is the primary workload evaluated in this pilot.

**Retrieval Workload**
:   The use of an AI system to *find* relevant content across a large corpus — "which prior solutions touch step-up auth and PCI?" across thousands of documents in multiple repositories and formats. Retrieval may span content in git, SharePoint, Confluence, and vendor documentation. This workload has different tool requirements than generation.

**Content Rationalization**
:   The practice of auditing what content actually needs to be searchable, consolidating it into a manageable scope, and migrating it to formats and locations where existing tools can ingest it. The alternative to building infrastructure that searches everything everywhere is to bring the relevant content closer to where the work happens.

## Integration and Portability

**MCP (Model Context Protocol)**
:   An open-source standard (maintained by Anthropic) that lets AI agents call external services — APIs, databases, search indexes, tools — using a standardized protocol. MCP solves "index lock-in" by allowing any compliant client (Copilot, Cursor, Windsurf, Claude Desktop) to query the same external data source. Foundry IQ exposes knowledge bases as MCP endpoints. Copilot consumes MCP servers as tool providers.

**Portability**
:   The ability to move an investment from one platform to another. Three dimensions are relevant:

    | Dimension | What moves | Portable? |
    |-----------|-----------|-----------|
    | **Content portability** | Architecture artifacts (ADRs, specs, diagrams) | Always — these are files in git |
    | **Customization portability** | Instruction files, skills, agent definitions | Content is portable (plain Markdown); format is converging on open standards (SKILL.md, AGENTS.md) but not yet fully standardized |
    | **Index portability** | The search index and embeddings | Not portable — each platform rebuilds its own index from source content. But the source content is portable, so this is a rebuild cost, not a data loss. |

**Lock-in**
:   The cost and friction of switching platforms. Two forms are relevant:

    - **Platform lock-in** — proprietary customization formats that require rewriting when switching IDEs. Mitigated by open standards convergence (SKILL.md, AGENTS.md, MCP).
    - **Index lock-in** — a search index that is only accessible from one vendor's tools. Mitigated by MCP (which can expose any index to any client) and by the fact that indexes are derived from source content (which is portable).

## Platforms Referenced

**GitHub Copilot**
:   SaaS AI coding assistant with built-in workspace indexing, intent-based billing ($39/seat/month), and declarative customization via Markdown files. Used in this evaluation as the platform-native baseline.

**Foundry IQ**
:   A managed knowledge layer (public preview as of April 2026) built on Azure AI Search. Provides knowledge base orchestration, agentic retrieval, custom chunking via skillsets, access control synchronization, and MCP endpoint exposure. Requires provisioning Azure AI Search, a Foundry project, and an LLM deployment.

**Azure AI Search**
:   Microsoft's GA search platform providing full-text, vector, and hybrid search with skillsets, scoring profiles, and indexers. The infrastructure layer underneath Foundry IQ. Foundry IQ adds the knowledge base abstraction and agentic retrieval engine on top.
