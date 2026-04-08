# Deep Research Prompt: Controlling Chunking by File Type in GitHub Copilot

## Context for the Research

We are an enterprise architecture team using GitHub Copilot with a workspace containing diverse file types: OpenAPI YAML specs (19 services), AsyncAPI event schemas, YAML metadata files, Markdown architecture decision records, Java source code, PlantUML diagrams, Excalidraw JSON wireframes, and MkDocs configuration. We need to understand whether and how we can control how different file types are chunked, parsed, and injected into the AI context — because a 500-line OpenAPI spec has very different semantic boundaries than a Markdown ADR or a Java class.

## Prompt

> Research whether GitHub Copilot (and the broader AI coding assistant ecosystem) allows users or teams to control how different file types are chunked, parsed, and injected into the LLM context window. The core question is: **can we define custom chunking strategies per file type, and if not natively, what workarounds or emerging standards exist?**
>
> Investigate these specific areas with authoritative sources:
>
> ### 1. GitHub Copilot's Native File-Type-Aware Chunking
>
> - How does Copilot's Tree-sitter-based chunking handle different file types? Which languages/formats have AST-aware chunking vs. falling back to generic token-window chunking?
> - Specifically: does Copilot have Tree-sitter grammars for YAML, JSON, Markdown, PlantUML, or only for programming languages (Java, Python, TypeScript, etc.)?
> - For YAML files (OpenAPI specs, AsyncAPI schemas, Kubernetes manifests) — does Copilot chunk at the YAML document level, key hierarchy level, or just by token count?
> - For Markdown files (ADRs, solution designs, documentation) — does Copilot chunk at heading boundaries (H1/H2/H3) or by raw token count?
> - Is there any way to influence chunking behavior through file structure, naming conventions, or metadata?
>
> ### 2. Custom Chunking Configuration
>
> - Does Copilot (Individual, Business, or Enterprise) expose any configuration for chunking strategy — per file type, per directory, or globally?
> - Does any AI coding platform (Cursor, Windsurf, Cline, Claude Code) allow users to define custom chunking rules?
> - Are there `.copilot/`, `.github/copilot/`, or VS Code settings (`github.copilot.*`) that affect how files are parsed or chunked?
> - Can `.instructions.md` files or `copilot-instructions.md` influence how Copilot processes (not just responds to) workspace files?
>
> ### 3. Workarounds and Patterns
>
> - **File decomposition**: If Copilot's chunking is opaque, does splitting large files (e.g., breaking a 2000-line OpenAPI spec into per-endpoint files) measurably improve retrieval precision?
> - **Summary files**: Does creating human-authored summary files (e.g., `README.md` in each directory, `_index.yaml` manifests) help Copilot's retrieval find the right content faster?
> - **Structured headings**: For Markdown files, does using consistent heading hierarchies (H1 = document title, H2 = sections, H3 = subsections) create better chunk boundaries than flat documents?
> - **YAML structure**: For YAML files, does nesting depth, anchor usage, multi-document YAML (`---` separators), or key ordering affect chunking quality?
> - **File naming conventions**: Does naming files descriptively (e.g., `svc-check-in-openapi.yaml` vs. `spec.yaml`) improve retrieval ranking?
>
> ### 4. MCP as a Custom Chunking Layer
>
> - Can an MCP server act as a custom chunking/retrieval layer — where instead of relying on Copilot's native indexing, the architect queries an MCP tool that applies domain-specific chunking (e.g., chunk OpenAPI specs by endpoint, chunk ADRs by decision section)?
> - Are there existing MCP servers or patterns that implement custom retrieval with file-type-specific chunking?
> - How does MCP tool response content interact with Copilot's native retrieval — do they compete for context space, or are they additive?
>
> ### 5. Enterprise and Organization-Level Controls
>
> - Does GitHub Copilot Enterprise offer any organization-level configuration for indexing behavior — file type priorities, excluded paths, custom parsers?
> - Do Copilot Knowledge Bases (if they exist) allow custom chunking configuration?
> - Is there a GitHub roadmap item, feature request, or public RFC for user-configurable chunking?
>
> ### 6. Emerging Standards and Community Patterns
>
> - Are there community-developed patterns (blog posts, GitHub discussions, conference talks) for optimizing repository structure for AI retrieval?
> - Does the `AGENTS.md` or Agent Skills specification include any provisions for declaring how files should be parsed?
> - Are there academic papers or industry reports analyzing the impact of file structure on AI coding assistant retrieval quality?
> - What does the Tree-sitter grammar ecosystem look like for non-programming formats (YAML, Markdown, TOML, PlantUML)?
>
> ### Source Priority
>
> 1. **GitHub official documentation** (docs.github.com, github.blog, GitHub Changelog)
> 2. **VS Code documentation** (code.visualstudio.com)
> 3. **GitHub engineering blog posts** and GitHub Universe/Copilot talk transcripts
> 4. **Tree-sitter documentation and grammar repositories** (tree-sitter.github.io, github.com/tree-sitter)
> 5. **Competitor platform documentation** (Cursor, Windsurf, Cline, Claude Code) for comparison
> 6. **Community patterns** (GitHub Discussions, Stack Overflow, dev.to, technical blogs)
> 7. **Academic papers** on code retrieval, RAG chunking strategies, structural parsing
>
> ### Output Format
>
> For each question area, provide:
> - **Answer** based on available evidence
> - **Source URLs** with publication dates
> - **Confidence level**: HIGH (official docs/engineering blog), MEDIUM (talks/community with evidence), LOW (inference/speculation)
> - **Actionable recommendation** for an architecture team structuring a 1,000-file workspace
>
> ### Exclusions
>
> Do NOT cover:
> - Embedding model internals (already researched)
> - Vector database comparisons
> - Self-managed RAG pipeline design
> - Pricing/billing models
> - General "what is Copilot" introductions
