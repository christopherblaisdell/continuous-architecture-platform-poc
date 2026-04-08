# Deep Research Prompt: Azure AI Search Chunking Mechanics for Architecture File Types

## Context for the Research

We are an enterprise architecture team evaluating whether Azure AI Foundry (specifically Foundry IQ backed by Azure AI Search) would handle our architecture file types better than GitHub Copilot's native workspace indexing. Our workspace contains: OpenAPI YAML specs (19 services, some exceeding 500 lines), AsyncAPI event schemas, YAML metadata files, Markdown architecture decision records (MADR format), Java source code, PlantUML C4 diagrams with `!include` directives, and configuration YAML. We need a file-type-by-file-type understanding of how Azure AI Search chunks, indexes, and retrieves these formats — so we can compare it directly against Copilot's Tree-sitter + Jaccard sliding window approach.

## Prompt

> Research how Azure AI Search handles chunking, indexing, and retrieval for each architecture file type listed below. The core question is: **for each file type, does Azure AI Search provide meaningfully better chunking than GitHub Copilot's generic 60-line sliding window fallback — and what engineering effort is required to achieve that improvement?**
>
> Investigate with authoritative Microsoft Learn documentation, Azure SDK samples, and community experience reports.
>
> ### 1. Azure AI Search Document Cracking and Built-In Chunking
>
> - What file formats does Azure AI Search's built-in document cracking support natively? Specifically: does it crack YAML, Markdown, PlantUML (.puml), or AsyncAPI files — or does it treat them as plain text?
> - What are the available chunking strategies? Document-level, page-level, fixed-size token windows, sentence-based, semantic chunking? What are the defaults?
> - What is the `text-split` cognitive skill? How does it determine chunk boundaries? Is it configurable per file type or only globally?
> - What are the configurable parameters: chunk size (tokens), overlap, separator characters? What are the default values and allowed ranges?
> - Does Azure AI Search have any format-aware chunking for structured text (YAML key hierarchies, Markdown headings, JSON structure) — or is everything treated as flat text after document cracking?
>
> ### 2. Integrated Vectorization Pipeline
>
> - How does Azure AI Search's integrated vectorization work end-to-end: data source → indexer → skillset → vector index?
> - What embedding models are available through Azure OpenAI for vectorization? (text-embedding-ada-002, text-embedding-3-small, text-embedding-3-large — dimensions, pricing, quality differences)
> - Is vectorization automatic or does it require explicit skillset configuration per data source?
> - How does incremental indexing work? If a single YAML file changes, does it re-chunk and re-vectorize just that file or the entire index?
> - What is the latency from file change to updated index availability?
>
> ### 3. Custom Skillsets for Non-Standard File Types
>
> - Can custom skillsets (Azure Functions, custom Web API skills) be used to implement file-type-specific chunking? For example: a skillset that parses OpenAPI YAML and chunks by endpoint definition rather than by token count?
> - What is the skillset pipeline architecture? Can a custom skill receive the raw file content and return structured chunks?
> - What are the constraints: input size limits, output size limits, timeout limits, cold start latency for Azure Functions-based skills?
> - Are there examples or patterns in Microsoft documentation for custom chunking of structured text formats?
> - What does a custom skillset cost? (Azure Functions execution costs, plus the development and maintenance overhead)
>
> ### 4. File-Type-Specific Analysis
>
> For EACH of these file types, document: (a) how Azure AI Search handles it by default, (b) what customization is possible, (c) what engineering effort is required, and (d) whether the result is meaningfully better than a 60-line sliding window with Jaccard similarity scoring.
>
> #### 4a. OpenAPI YAML Specs
> - Does the document cracker parse YAML structure or treat it as plain text?
> - Can a custom skillset resolve `$ref` pointers and produce dereferenced endpoint chunks?
> - How does Azure AI Search handle a 500-line YAML file with deeply nested schemas?
> - Is there an existing Azure cognitive skill or marketplace skill for OpenAPI parsing?
>
> #### 4b. Markdown (ADRs, Solution Designs)
> - Does the document cracker split Markdown by headings (H1/H2/H3)?
> - Is there a Markdown-aware chunking mode that preserves section boundaries?
> - How does it handle MADR format (Status, Context, Decision Drivers, Considered Options, Decision Outcome)?
>
> #### 4c. PlantUML Diagrams (.puml)
> - Does Azure AI Search recognize .puml files at all, or are they treated as unknown text?
> - Can a custom skillset parse PlantUML syntax to extract participants, relationships, and message flows?
> - Would a PlantUML-to-structured-text converter (custom skill) produce better search results than raw .puml indexing?
> - How does Azure AI Search handle `!include` directives — does it follow them or treat them as opaque text?
>
> #### 4d. AsyncAPI Event Specs
> - Same questions as OpenAPI: YAML structure awareness, `$ref` resolution, custom skillset options
>
> #### 4e. YAML Metadata Files (Capabilities, Tickets, Domain Classifications)
> - Small files (<150 lines) — does Azure AI Search chunk these into a single chunk or split them?
> - Does the YAML key hierarchy influence chunk boundaries at all?
>
> #### 4f. Java / TypeScript / Python Source Code
> - Does Azure AI Search have any code-aware chunking (AST-based, function-level)?
> - Or is source code treated as plain text with token-window chunking?
> - How does this compare to Copilot's Tree-sitter AST-aware chunking for programming languages?
>
> #### 4g. Configuration YAML (Small Files)
> - For files under 100 lines, does Azure AI Search produce a single chunk or multiple?
> - What is the minimum chunk size?
>
> #### 4h. Figma Wireframes
> - Figma files are hosted on figma.com, not in git. Can Foundry IQ index external URLs?
> - If Figma design token exports (JSON) are committed to git, how does Azure AI Search chunk JSON files?
>
> ### 5. Retrieval Quality Comparison Points
>
> - What retrieval modes does Azure AI Search support? Keyword, vector, hybrid (keyword + vector), semantic ranking?
> - How does hybrid retrieval compare to Copilot's hybrid retrieval (lexical + semantic)?
> - What is the query latency profile for: keyword search, vector search, hybrid search, semantic re-ranking?
> - Can retrieval be scoped to specific file types or directories (metadata filters)?
> - Does Azure AI Search support "direct file access" (reading a specific file by path) or is everything retrieval-only?
>
> ### 6. Foundry IQ Layer
>
> - Does Foundry IQ add any chunking intelligence beyond what Azure AI Search provides natively?
> - How do Foundry IQ "retrieval instructions" work? Can they be file-type-specific?
> - What "reasoning effort levels" (minimal, low, medium) exist and how do they affect retrieval quality for structured file types?
> - Can Foundry IQ knowledge bases ingest directly from GitHub repositories, or must content be copied to Azure Blob / SharePoint?
> - How does Foundry IQ's MCP endpoint exposure work? Can MCP tools query the index with file-type-specific semantics?
>
> ### 7. Cost Profile
>
> - What Azure AI Search tier is required for integrated vectorization? (Free, Basic, S1, S2, S3)
> - What is the per-document indexing cost (if any)?
> - What is the per-query cost for vector search vs hybrid search?
> - What does a custom skillset pipeline add to the cost (Azure Functions, Azure OpenAI embedding calls)?
> - Provide a rough cost model for indexing ~200 architecture files (specs, ADRs, diagrams, metadata) with weekly refresh.
>
> ### Output Format
>
> Structure the findings as a file-type-by-file-type comparison table, then detailed sections per file type. For each file type, provide:
> 1. Default Azure AI Search behavior (no customization)
> 2. Best achievable behavior (with custom skillsets)
> 3. Engineering effort to achieve the best behavior
> 4. Whether the improvement is meaningful compared to Copilot's 60-line Jaccard window
>
> Cite Microsoft Learn URLs for every factual claim. Flag anything that is undocumented or based on inference rather than documentation.
