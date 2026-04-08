# Deep Research Prompt: Figma Wireframe Chunking and Context Injection for GitHub Copilot

## Context for the Research

We are an enterprise architecture team using GitHub Copilot for AI-assisted solution design. Our UI/UX wireframes are created in **Figma** and need to be accessible to the AI agent during architecture work — solution designs reference specific screens, API designs are informed by UI data requirements, and impact assessments need to identify which wireframes are affected by service changes.

The challenge: Copilot's native indexer has no understanding of design tool file formats. We need to determine: (1) what formats Figma content can be exported to or accessed in, (2) how each format is chunked by Copilot's indexer, (3) whether MCP servers or other integration patterns can provide semantic access to Figma designs, and (4) what the architecture team should actually do to make wireframes useful in AI-assisted workflows.

## Prompt

> Research how Figma wireframes and design artifacts can be made accessible to GitHub Copilot's context window for AI-assisted architecture work. The core question is: **what is the most effective way to get Figma design information into an LLM's context so it can reason about UI structure, screen layouts, data requirements, and user flows during architecture analysis?**
>
> Investigate these specific areas with authoritative citations:
>
> ### 1. Figma Export Formats and Their Chunking Properties
>
> - What formats can Figma export to? (SVG, PNG, PDF, JSON via API, Figma `.fig` files, etc.)
> - For each export format, how does a typical LLM tokenizer and AI coding assistant indexer handle it?
>   - **SVG**: Is SVG text parseable by Copilot? Does it retain semantic information (element names, layer hierarchy, text content) or is it just geometry?
>   - **Figma REST API JSON**: What does Figma's API return for a file or frame? How large are typical responses? Is the JSON structure amenable to LLM reasoning (named components, text nodes, layout properties)?
>   - **Figma `.fig` binary format**: Is this parseable by any tool outside Figma? Are there open-source parsers?
>   - **PNG/JPEG/PDF**: Can multimodal LLMs (GPT-4o, Claude Opus 4.6) reason about screenshot images of wireframes? How does image-based reasoning compare to structured data for architecture decisions?
>
> ### 2. Figma MCP Servers and Integrations
>
> - Do Figma MCP servers exist? Search for:
>   - Official Figma MCP server (if any)
>   - Community MCP servers for Figma (npm packages, GitHub repos)
>   - Any Figma plugin or integration that exposes design data via MCP
> - For each MCP server found:
>   - What tools does it expose? (get frame, list components, export image, get design tokens, etc.)
>   - What data format does it return? (JSON structure, image bytes, text descriptions)
>   - Does it respect Copilot's 10KB response limit, or do responses need pagination?
>   - What authentication does it require? (Figma API key, OAuth, etc.)
>   - Is it actively maintained? (last commit date, open issues, stars)
> - Can a Figma MCP server provide **semantic** access to designs — e.g., "what screens show a reservation form?" or "what data fields are displayed on the check-in confirmation screen?" — or is it limited to raw geometry export?
>
> ### 3. Design-to-Code and Design Token Extraction
>
> - How do modern design-to-code tools extract structured information from Figma?
> - Can **Figma design tokens** (colors, typography, spacing, component variants) be exported as JSON/YAML and committed to git? If so, does Copilot index them effectively?
> - Are there tools that extract **component structure** from Figma as a machine-readable manifest (component names, properties, variants, slot definitions)?
> - Can Figma's **auto-layout** and **component properties** be serialized in a format that an LLM can reason about without seeing the visual design?
>
> ### 4. Architecture-Relevant Information in Wireframes
>
> Not all wireframe information matters for architecture work. Determine which aspects of a Figma design are architecturally relevant and how each can be extracted:
>
> - **Data requirements**: Which fields are displayed on each screen? (Drives API schema design)
> - **User flows**: How do screens connect to each other? (Drives service orchestration)
> - **Component hierarchy**: What reusable components exist? (Drives frontend architecture decisions)
> - **State variations**: What states does each screen support (loading, error, empty, populated)? (Drives API error handling requirements)
> - **Text content**: Labels, button text, error messages (Drives internationalization and content management decisions)
>
> ### 5. Practical Patterns for Architecture Teams
>
> - **Pattern A — Screenshot + description**: Export wireframes as images, write companion Markdown files describing the screen's purpose, data requirements, and user flow connections. The Markdown is indexed; the image is referenced.
> - **Pattern B — Figma MCP server**: Real-time access to Figma designs via MCP tools. Agent queries design data on demand.
> - **Pattern C — Design token export**: Export Figma design tokens and component manifests as JSON/YAML, commit to git, let Copilot index the structured data.
> - **Pattern D — Generated documentation**: Use a tool or script to extract Figma frame metadata (names, text content, component usage) into Markdown summaries, committed to git.
> - Which combination of patterns provides the best architecture-relevant context at the lowest maintenance burden?
>
> ### 6. Multimodal LLM Capabilities for Design Reasoning
>
> - Can current multimodal models (GPT-4o, Claude Opus 4.6, Gemini) reason about architecture-relevant properties from wireframe screenshots?
> - What is the quality of LLM reasoning about UI structure from images vs. from structured data (JSON, design tokens)?
> - Does GitHub Copilot support image input in chat or agent mode? If so, can an architect paste a Figma screenshot and get architecture-relevant analysis?
> - Are there documented patterns for combining image-based and structured-data-based design context in AI workflows?
>
> ### 7. Figma Dev Mode and Developer Handoff
>
> - Does Figma's Dev Mode expose structured data that could be piped into an AI workflow?
> - Can Dev Mode annotations (component specs, CSS properties, spacing values) be exported programmatically?
> - Is there a Figma CLI or CI/CD integration that could automate design-to-git exports?
>
> ### Source Priority
>
> 1. **Figma official documentation** (help.figma.com, figma.com/developers, Figma API reference)
> 2. **GitHub official documentation** (docs.github.com — Copilot MCP support, multimodal features)
> 3. **MCP server repositories on GitHub** (search: "figma mcp server", "figma-mcp", "mcp figma")
> 4. **Figma community plugins and integrations** (figma.com/community)
> 5. **Design engineering blog posts** (Figma blog, design system team posts, AI+design workflow articles)
> 6. **AI and design research** (papers on design-to-code, LLM visual reasoning benchmarks)
>
> ### Output Format
>
> Structure findings as:
>
> 1. **Executive summary** — 3-5 sentence answer to the core question
> 2. **Figma export format analysis** — table comparing formats by chunking quality, semantic richness, and maintenance burden
> 3. **MCP server landscape** — inventory of available Figma MCP servers with maturity assessment
> 4. **Recommended pattern** — which combination of approaches the architecture team should adopt, with rationale
> 5. **Implementation sequence** — ordered steps from quickest win to most sophisticated integration
> 6. **Open questions** — what cannot be determined from public sources and requires hands-on testing
>
> Cite all sources with URLs. Prefer sources from 2024-2026 given the rapid evolution of both MCP and Figma's developer platform.
