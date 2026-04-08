# Deep Research Prompt: PlantUML and OpenAPI Chunking and Context Injection for GitHub Copilot

## Context for the Research

We are an enterprise architecture team using GitHub Copilot for AI-assisted solution design. Our architecture workspace contains two critical file types that Copilot handles poorly:

1. **OpenAPI YAML specifications** (19 services, each in a separate `.yaml` file, ranging from 50-500+ lines). These define every API contract in the system — endpoints, request/response schemas, security requirements, and `$ref` pointers to shared component schemas. When Copilot chunks these files, endpoint definitions are severed from their referenced schemas, causing the LLM to hallucinate request/response structures.

2. **PlantUML diagrams** (`.puml` files — C4 component diagrams, sequence diagrams, event flow diagrams). These define the system's visual architecture — who calls whom, in what order, with what data. Copilot treats `.puml` files as raw text with no structural understanding, making lexical search the only retrieval mechanism.

We have already identified MCP servers as one approach (OpenAPI MCP servers exist, PlantUML MCP servers may not). **The core question is whether MCP is the only viable approach, or whether there are other mechanisms — native, community, or configuration-based — that improve how Copilot chunks, indexes, and retrieves these specific file types.**

## Prompt

> Research all available mechanisms — native, community, configuration-based, and custom — for improving how GitHub Copilot chunks, indexes, and retrieves OpenAPI YAML specifications and PlantUML `.puml` diagram files. **Do not assume MCP is the only answer.** Explicitly investigate whether there are out-of-the-box, zero-infrastructure options before recommending MCP.
>
> Investigate these specific areas with authoritative citations:
>
> ### 1. Native Copilot Behavior for OpenAPI YAML
>
> - How exactly does Copilot chunk OpenAPI YAML files today? Confirm whether Tree-sitter's YAML grammar is used, and if so, at what granularity (document level, key level, or token window fallback).
> - Does Copilot treat files with an `openapi:` root key differently from generic YAML? Is there any format detection or schema-aware indexing?
> - When Copilot retrieves a fragment of an OpenAPI spec, does it follow `$ref` pointers to resolve referenced schemas, or does it only return the literal text chunk?
> - Does the file extension (`.yaml` vs `.yml` vs `.json`) affect how Copilot indexes OpenAPI specs?
> - If an OpenAPI spec is stored as JSON instead of YAML, does Copilot's JSON Tree-sitter grammar provide better structural chunking than its YAML handling?
>
> ### 2. Native Copilot Behavior for PlantUML (.puml)
>
> - How does Copilot chunk `.puml` files? Is there any Tree-sitter grammar for PlantUML in Copilot's grammar set?
> - Does Copilot recognize PlantUML syntax (e.g., `@startuml` / `@enduml` boundaries, participant declarations, relationship arrows)?
> - For C4 PlantUML diagrams using `!include` directives and C4 macros (`Container`, `Component`, `Rel`), does Copilot resolve the includes or treat them as opaque text?
> - Does naming the file `.puml` vs `.plantuml` vs `.pu` affect indexing behavior?
> - Can Copilot reason about PlantUML diagram structure from raw text (e.g., "which services does svc-check-in call?"), or is it limited to substring matching?
>
> ### 3. Non-MCP Workarounds for OpenAPI
>
> Investigate every approach that does NOT require an MCP server:
>
> - **File decomposition**: Does splitting a monolithic OpenAPI spec into per-endpoint files linked by `$ref` measurably improve retrieval? Are there benchmarks, case studies, or community reports?
> - **Scoped instruction files**: Can a `.instructions.md` with `applyTo: "**/*.yaml"` teach the LLM to always retrieve referenced schemas? Has anyone documented this pattern working in practice?
> - **JSON instead of YAML**: If OpenAPI specs are stored as `.json`, does Copilot's JSON AST parser provide better chunking than YAML's generic fallback? Would converting YAML specs to JSON improve retrieval quality?
> - **Companion Markdown summaries**: Does creating a human-written `README.md` or `SUMMARY.md` alongside each spec — listing endpoints, schemas, and cross-references in natural language — improve Copilot's ability to find the right spec content?
> - **OpenAPI-specific VS Code extensions**: Do any VS Code extensions (Swagger Viewer, OpenAPI Editor, Stoplight Spectral) expose their parsed AST or validation results in a way that Copilot can consume?
> - **Copilot SKILL.md files**: Can a SKILL.md file be created that teaches Copilot how to navigate and interpret OpenAPI specs? Are there examples of spec-aware skills in the community?
> - **AGENTS.md routing**: Does an explicit AGENTS.md entry for the specs directory measurably improve retrieval compared to relying on vector search alone?
>
> ### 4. Non-MCP Workarounds for PlantUML
>
> Investigate every approach that does NOT require an MCP server:
>
> - **Companion Markdown descriptions**: Does writing a plain-language summary of each diagram (participants, relationships, sequence of calls) in a companion `.md` file improve Copilot's ability to answer questions about architecture?
> - **PlantUML-to-text extraction**: Are there tools that parse `.puml` files and extract structured data (list of participants, list of relationships, call sequences) into machine-readable formats (JSON, YAML, Markdown tables)?
> - **Tree-sitter grammars for PlantUML**: Does a community Tree-sitter grammar for PlantUML exist? If so, could it theoretically be contributed to Copilot's grammar set? Has anyone requested this?
> - **VS Code PlantUML extensions**: Do PlantUML VS Code extensions (e.g., `jebbs.plantuml`) expose parsed diagram data via the Language Server Protocol in a way Copilot could use for better retrieval?
> - **File structure conventions**: Does organizing `.puml` files by diagram type (sequence, component, context) with descriptive names improve retrieval?
> - **Embedded comments**: Does adding structured comments inside `.puml` files (e.g., `' @participants: svc-check-in, svc-reservations, svc-guest-profiles`) improve Copilot's lexical search?
> - **SKILL.md for PlantUML**: Can a skill file teach Copilot the PlantUML DSL syntax so it can reason about relationships rather than treating diagrams as opaque text? The `github/awesome-copilot` repo has a PlantUML ASCII skill — does it help with retrieval?
> - **Generated Markdown from diagrams**: Could a CI script parse `.puml` files and generate Markdown summaries (e.g., "Sequence diagram: svc-check-in calls svc-reservations.getReservation(), then calls svc-guest-profiles.getGuest()") that Copilot can index?
>
> ### 5. MCP Server Landscape for OpenAPI and PlantUML
>
> For completeness, inventory MCP-based approaches:
>
> - **OpenAPI MCP servers**: List all known implementations (openapi-mcp, mcp-openapi-schema-explorer, Stainless MCP, others). For each: tools exposed, response format, `$ref` resolution support, maturity, last activity.
> - **PlantUML MCP servers**: Do any exist? Search GitHub, npm, PyPI for "plantuml mcp server", "plantuml-mcp", "mcp plantuml". If none exist, what would one need to do? (Parse `.puml`, extract participants and relationships, expose as tools.)
> - **Generic diagram MCP servers**: Are there MCP servers for diagram formats in general (Mermaid, D2, Structurizr) that could be adapted for PlantUML?
> - **Custom FastMCP feasibility**: How hard would it be to build a PlantUML MCP server using Python's `plantuml` parser or a PlantUML-to-JSON converter?
>
> ### 6. Out-of-the-Box Solutions
>
> Explicitly answer: **are there any zero-configuration, install-and-go solutions** for improving Copilot's handling of OpenAPI or PlantUML?
>
> - GitHub Copilot Enterprise-only features that affect indexing of these formats?
> - Copilot Spaces configurations that prioritize structured files?
> - VS Code extensions that automatically improve Copilot's context for these file types?
> - GitHub-published best practices for repository structure that specifically address OpenAPI or diagram files?
>
> ### 7. Comparative Analysis
>
> For both OpenAPI and PlantUML, rank all discovered approaches by:
>
> | Criterion | Description |
> |-----------|-------------|
> | **Effort** | How much work to implement (hours, days, weeks) |
> | **Infrastructure** | Does it require running a server, or is it static files only? |
> | **Maintenance** | Ongoing effort to keep it working as Copilot evolves |
> | **Retrieval quality improvement** | Estimated impact on LLM's ability to reason correctly about the content |
> | **Team adoption friction** | How much does each architect need to change their workflow? |
>
> ### Source Priority
>
> 1. **GitHub official documentation** (docs.github.com — Copilot indexing, chunking, MCP support)
> 2. **VS Code documentation** (code.visualstudio.com — extension API, language server protocol)
> 3. **Tree-sitter documentation and grammar repositories** (tree-sitter.github.io, GitHub grammar repos)
> 4. **GitHub engineering blog posts** and GitHub Universe/Copilot talk transcripts
> 5. **MCP server repositories** (GitHub search: "openapi mcp", "plantuml mcp", "swagger mcp")
> 6. **Community patterns** (blog posts, GitHub Discussions, Stack Overflow, Reddit r/githubcopilot)
> 7. **PlantUML official documentation** (plantuml.com — file format, syntax, tooling ecosystem)
> 8. **OpenAPI Initiative documentation** (spec.openapis.org — multi-file spec conventions, `$ref` semantics)
>
> ### Output Format
>
> Structure findings as:
>
> 1. **Executive summary** — 3-5 sentence answer: is MCP the only viable approach, or are there effective non-MCP alternatives?
> 2. **OpenAPI approaches** — ranked table of all approaches (non-MCP first, then MCP) with effort/impact/infrastructure assessment
> 3. **PlantUML approaches** — ranked table of all approaches (non-MCP first, then MCP) with effort/impact/infrastructure assessment
> 4. **Out-of-the-box options** — explicit list of zero-configuration solutions (if any exist)
> 5. **Recommended strategy** — which combination of approaches to adopt for each file type
> 6. **Open questions** — what requires hands-on testing vs. what can be determined from documentation
>
> Cite all sources with URLs. Prefer sources from 2024-2026 given the rapid evolution of Copilot's indexing capabilities.
