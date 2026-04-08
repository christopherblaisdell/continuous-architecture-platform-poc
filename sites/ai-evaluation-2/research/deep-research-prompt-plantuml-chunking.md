# Deep Research Prompt: PlantUML Diagram Chunking and Context Injection for GitHub Copilot

## Context for the Research

We are an enterprise architecture team using GitHub Copilot (Pro+ plan with Claude Opus 4.6) for AI-assisted solution design. Our architecture workspace contains approximately 140 PlantUML diagram files (`.puml`) across multiple categories:

- **C4 Component diagrams** — define container and component boundaries using the C4 PlantUML macro library (`!include C4_Component.puml`, `Container()`, `Component()`, `Rel()`)
- **Sequence diagrams** — describe runtime interactions between services, showing method calls, parameters, response payloads, and error paths
- **Event flow diagrams** — show asynchronous event-driven integrations through Kafka topics with producers, consumers, and event schemas
- **System Context diagrams** — high-level views of system boundaries and external actor interactions

These diagrams are the **primary communication artifacts** for architecture decisions. When an architect asks Copilot "which services does svc-check-in call?", the answer is encoded in these `.puml` files. When designing a new API contract, the sequence diagrams define the expected call flows.

**The problem:** GitHub Copilot treats `.puml` files as generic plain text. There is no Tree-sitter grammar for PlantUML in Copilot's indexer, no structural parsing of `@startuml`/`@enduml` boundaries, no resolution of `!include` directives, and no understanding of PlantUML's domain-specific syntax (participants, arrows, activation bars, notes, groups). The indexer applies a generic 60-line sliding window (local) or 512-1024 token embedding window (remote RAG), destroying the semantic relationships between diagram elements.

This means the files that encode the most critical architectural knowledge — who calls whom, with what data, in what order — are the files Copilot understands worst.

## Research Prompt

> Conduct an exhaustive investigation into all available mechanisms — native, community, configuration-based, and custom — for improving how GitHub Copilot chunks, indexes, retrieves, and reasons about PlantUML `.puml` diagram files. This is not limited to MCP. Investigate every layer of the context injection pipeline: file structure, naming conventions, instruction files, VS Code extensions, Tree-sitter grammars, MCP servers, companion file generation, and multimodal approaches. Include authoritative source URLs for every claim.
>
> ### 1. GitHub Copilot's Native Handling of PlantUML Files
>
> Investigate exactly what happens when Copilot encounters a `.puml` file:
>
> - **Tree-sitter grammar inventory**: List every Tree-sitter grammar bundled with VS Code and Copilot. Is there a PlantUML grammar? Check the `tree-sitter-plantuml` repository on GitHub — does it exist? What is its status, maturity, and completeness?
> - **Extension-to-language mapping**: Does VS Code's language detection recognize `.puml`, `.plantuml`, `.pu`, or `.iuml` file extensions? What language ID is assigned? Does this language ID affect Copilot's chunking strategy?
> - **Chunking behavior**: Without a Tree-sitter grammar, what fallback does Copilot use? Confirm whether it is a 60-line sliding window (local Jaccard similarity), a generic token window for remote embeddings, or something else. Cite the source.
> - **Indexing inclusion/exclusion**: Are `.puml` files included in Copilot's workspace index by default? Are they subject to any exclusion patterns similar to `**/*.svg`? Check `files.exclude`, `search.exclude`, and Copilot-specific exclusion lists.
> - **Semantic search effectiveness**: When a user queries `@workspace "which services does svc-check-in call?"`, can Copilot's embedding-based retrieval find the relevant `.puml` sequence diagram? Or does the PlantUML DSL syntax (arrows, participant declarations) confuse the embedding model?
> - **Lexical search effectiveness**: When a user queries with exact terms like `svc-check-in -> svc-reservations`, does Copilot's TF-IDF fallback successfully locate the diagram? How does PlantUML arrow syntax (`->`, `-->`, `->>`, `->o`) affect tokenization?
> - **`!include` resolution**: When a `.puml` file contains `!include C4_Component.puml` or `!include ../common/styles.puml`, does Copilot resolve these includes to provide the macro definitions, or does it treat them as opaque strings?
> - **Multi-diagram files**: If a single `.puml` file contains multiple `@startuml name` / `@enduml` blocks, does Copilot treat each block as a separate unit or chunk across boundaries indiscriminately?
>
> ### 2. PlantUML Syntax and Structure: What an Ideal Parser Would Extract
>
> Before evaluating workarounds, define the semantic elements that matter for architecture reasoning:
>
> - **Participants and actors**: `participant`, `actor`, `boundary`, `control`, `entity`, `database`, `queue`, `collections` declarations — these name the services and systems in the architecture
> - **Relationships**: `->`, `-->`, `->>`, `->o`, `<-`, `<--` arrows with labels — these encode who calls whom and with what message
> - **C4 model elements**: `Person()`, `System()`, `Container()`, `Component()`, `Rel()`, `BiRel()` — macro-based declarations that embed names, descriptions, and technology annotations
> - **Activation and scope**: `activate`, `deactivate`, `group`, `alt`, `loop`, `opt`, `par`, `critical`, `break` — these define control flow and error handling
> - **Notes and metadata**: `note left`, `note right`, `note over`, `hnote` — these carry human-readable context about why calls happen
> - **Stereotypes and tags**: `<<stereotype>>`, `$tag` — used for visual and semantic categorization
> - **`!include` and `!define`**: Macro inclusion and definition — critical for C4 model libraries and shared styles
> - **Diagram title and caption**: `title`, `caption`, `header`, `footer` — these name and describe the diagram's purpose
>
> For each element type: how well does plain-text lexical search work? How much is lost compared to a structural parser?
>
> ### 3. Non-MCP Approaches: File Structure and Naming
>
> Investigate structural optimizations that require no tooling:
>
> - **File naming conventions**: Does naming a file `svc-check-in-create-reservation-sequence.puml` vs `diagram-001.puml` measurably improve Copilot's ability to surface the right diagram? How does Copilot's hybrid retrieval (lexical + semantic) weight the filename vs file content?
> - **One diagram per file**: Does enforcing one `@startuml` / `@enduml` block per file improve chunking compared to multi-diagram files?
> - **Directory organization**: Does grouping diagrams by type (`sequence/`, `component/`, `context/`, `event-flow/`) vs by service (`svc-check-in/`, `svc-reservations/`) affect retrieval? Does the directory path appear in chunk metadata?
> - **File size thresholds**: At what line count does a `.puml` file exceed a single embedding chunk? Is 150 lines still the practical threshold for PlantUML (given that PlantUML lines are typically shorter than YAML or Markdown)?
> - **Companion `README.md` per directory**: Does placing a Markdown summary alongside diagram files (listing each diagram's purpose, participants, and key relationships) improve retrieval?
>
> ### 4. Non-MCP Approaches: Scoped Instructions and AGENTS.md
>
> Investigate instruction-based compensation for poor chunking:
>
> - **Scoped `.instructions.md` for PlantUML**: Can an instruction file with `applyTo: "**/*.puml"` teach Copilot to cross-reference diagrams with OpenAPI specs, metadata YAML, and source code? Has anyone published examples of PlantUML-specific instruction files?
> - **Cross-referencing instructions**: Can instructions tell the LLM "when you find a participant named svc-reservations in a diagram, also retrieve the OpenAPI spec at architecture/specs/svc-reservations-openapi.yaml"? Does this work in practice?
> - **AGENTS.md routing for diagrams**: Does adding an explicit `architecture/diagrams/` entry in AGENTS.md with diagram-type descriptions improve agent navigation compared to relying on vector search?
> - **SKILL.md for PlantUML DSL**: The `github/awesome-copilot` repository documents a PlantUML ASCII skill. Evaluate whether SKILL.md files can teach Copilot to parse PlantUML syntax rather than treating it as plain text. What are the limits of skill-based DSL teaching?
>
> ### 5. Non-MCP Approaches: Companion File Generation
>
> Investigate generated artifacts that make diagram content indexable:
>
> - **PlantUML-to-Markdown summary generation**: Are there tools or scripts that parse `.puml` files and produce structured Markdown summaries? (e.g., "Sequence diagram: svc-check-in calls svc-reservations.getReservation(), then calls svc-guest-profiles.getGuest(). Error path: if reservation not found, return 404.")
> - **PlantUML-to-JSON extraction**: Are there parsers that convert PlantUML into structured JSON or YAML representing participants, relationships, and control flow? Check: `plantuml-parser` (npm), `py-puml-tools`, `plantuml-to-json`, or other open-source tools.
> - **Relationship extraction**: Can an existing tool extract a simple adjacency list from a sequence diagram? (e.g., `[{from: "svc-check-in", to: "svc-reservations", method: "GET", path: "/reservations/{id}"}]`)
> - **CI/CD pipeline integration**: If companion files are generated, how should they be maintained? GitHub Action on `.puml` file changes? Pre-commit hook? What is the maintenance burden?
> - **Staleness risk**: How do generated companion files avoid drifting from the source `.puml`? Can CI enforce that the companion is regenerated when the diagram changes?
>
> ### 6. Non-MCP Approaches: Embedded Metadata in PlantUML
>
> Investigate whether enriching `.puml` files themselves improves retrieval:
>
> - **Structured comments**: Does adding machine-readable comments like `' @participants: svc-check-in, svc-reservations, svc-guest-profiles` or `' @describes: check-in happy path` improve Copilot's lexical and semantic search?
> - **PlantUML `!metadata` or `!pragma` directives**: Does PlantUML have native metadata mechanisms that survive rendering and could aid indexing?
> - **Title and header text**: Does the `title` directive in PlantUML diagrams get weighted more heavily by Copilot's chunker than body content?
> - **Descriptive arrow labels vs terse labels**: Does `svc-check-in -> svc-reservations : GET /reservations/{confirmation_code}\nRetrieve reservation details` index better than `A -> B : get reservation`?
> - **PlantUML JSON/YAML data blocks**: PlantUML supports `@startjson`, `@startyaml` — can these be used to embed structured metadata within diagram files that Copilot's JSON/YAML chunker would recognize?
>
> ### 7. VS Code Extensions and Language Server Protocol
>
> Investigate whether existing VS Code extensions improve Copilot's understanding:
>
> - **jebbs.plantuml extension**: Does this extension expose a Language Server that provides symbol information (document symbols, workspace symbols, go-to-definition) for PlantUML? If so, does Copilot leverage these LSP signals for better retrieval?
> - **PlantUML language ID registration**: When the PlantUML extension registers the `plantuml` language ID, does this change how Copilot chunks the file?
> - **Extension-provided hover/completion data**: Do PlantUML extensions provide hover information or code completions that Copilot could use as additional context signals?
> - **Copilot's LSP integration**: Research documents that Copilot uses LSP signals (type information, hover definitions) for context. Do non-code language servers (PlantUML, Mermaid, Graphviz) provide equivalent signals?
>
> ### 8. Tree-Sitter Grammar Feasibility
>
> Investigate the feasibility of a PlantUML Tree-sitter grammar:
>
> - **Existing Tree-sitter grammars for diagram languages**: Do Tree-sitter grammars exist for Mermaid, Graphviz DOT, D2, or Structurizr DSL? If so, are they used by any AI coding assistant?
> - **PlantUML grammar complexity**: How complex is PlantUML's syntax relative to other Tree-sitter grammars? PlantUML supports 15+ diagram types with distinct syntaxes — is a single grammar feasible?
> - **Contributing to Copilot's grammar set**: Is there a process for contributing a Tree-sitter grammar to GitHub Copilot's bundled set? Has anyone requested PlantUML support via GitHub Community Discussions or VS Code issues?
> - **Timeline and likelihood**: If a grammar were developed, what is the realistic timeline for it to land in Copilot's indexer?
>
> ### 9. MCP Server Approaches
>
> For completeness, inventory MCP-based options:
>
> - **Existing PlantUML MCP servers**: Search GitHub, npm, PyPI for `plantuml mcp`, `puml mcp`, `mcp plantuml`, `mcp-server-plantuml`. List any implementations found with their tools, maturity, and last commit date.
> - **Diagram-agnostic MCP servers**: Are there MCP servers designed for diagram formats in general (Mermaid MCP, Graphviz MCP, Structurizr MCP) that could be adapted for PlantUML?
> - **PlantUML Server integration**: The PlantUML project maintains an HTTP rendering server. Could an MCP server wrap this to provide text-to-SVG rendering directly in Copilot's tool context? Would multimodal analysis of the rendered SVG add value over text parsing?
> - **Custom FastMCP feasibility**: Evaluate the effort to build a Python FastMCP server that:
>   - Parses `.puml` files using regex or an existing parser library
>   - Extracts participants, relationships, and control flow
>   - Exposes tools: `list_diagrams()`, `get_diagram_participants(file)`, `get_relationships(file)`, `search_diagrams(service_name)`, `get_call_chain(from_service, to_service)`
>   - Estimate development time, maintenance burden, and operational requirements
> - **Multimodal MCP pattern**: Could an MCP server render `.puml` to PNG/SVG and return the image alongside extracted text, allowing multimodal models (Claude Opus 4.6, GPT-5.4) to reason visually about diagram layout?
>
> ### 10. Multimodal Approaches (Image-Based Reasoning)
>
> Investigate using rendered diagram images as context:
>
> - **PlantUML rendering to PNG/SVG**: Can rendered diagrams be attached to Copilot Chat for visual reasoning? What is the quality of multimodal LLM understanding of PlantUML sequence diagrams vs component diagrams?
> - **OCR accuracy on PlantUML output**: How reliably do multimodal models extract participant names, arrow labels, and note text from rendered PlantUML diagrams?
> - **State obfuscation in diagrams**: Unlike UI wireframes, architecture diagrams are fully explicit (no hidden state). Does this make multimodal analysis more reliable for diagrams than for UI screenshots?
> - **SVG text extraction**: Since PlantUML's SVG output embeds text as `<text>` elements (not rasterized), can SVG files be treated as semi-structured text? Does Copilot's `**/*.svg` exclusion pattern need to be overridden for architecture diagrams?
> - **Dual context (text + image)**: Is there evidence that providing both the `.puml` source and the rendered image produces better LLM reasoning than either alone?
>
> ### 11. Alternative Diagram Formats
>
> Evaluate whether switching away from PlantUML would solve the problem:
>
> - **Mermaid**: Mermaid is natively rendered by GitHub Markdown. Does Copilot index Mermaid diagrams embedded in `.md` files better than standalone `.puml` files? Is there a Tree-sitter grammar for Mermaid?
> - **Structurizr DSL**: Structurizr uses a dedicated DSL for C4 models. Does any AI coding assistant handle Structurizr DSL better than PlantUML?
> - **D2**: D2 is a modern diagram-as-code language designed for readability. Does Copilot handle D2 files better than PlantUML?
> - **Migration cost**: For a workspace with 140+ PlantUML diagrams, what is the realistic migration effort and risk of switching to an alternative format?
> - **Recommendation**: Given the existing investment in PlantUML, should the team optimize PlantUML handling, migrate to an alternative, or maintain a dual-format approach?
>
> ### 12. Comparative Analysis and Recommendations
>
> Rank ALL discovered approaches by:
>
> | Criterion | Description |
> |-----------|-------------|
> | **Effort to implement** | Hours, days, or weeks of work |
> | **Infrastructure required** | None (file conventions only), VS Code extension, CI pipeline, or running MCP server |
> | **Maintenance burden** | Ongoing work to keep the approach functional as Copilot and PlantUML evolve |
> | **Retrieval quality improvement** | Estimated impact on Copilot's ability to correctly answer architecture questions using diagram content |
> | **Team adoption friction** | How much each architect needs to change their workflow |
> | **Composability** | Does this approach work alongside others, or does it replace them? |
>
> Provide a final recommended strategy as a **layered approach**: which zero-effort optimizations to apply immediately, which medium-effort approaches to add next, and whether MCP is justified as the final layer.
>
> ### Source Priority
>
> 1. **GitHub official documentation** — Copilot indexing, workspace context, chunking behavior, MCP support, file exclusion patterns
> 2. **VS Code documentation** — extension API, language server protocol, language detection, Tree-sitter integration
> 3. **Tree-sitter repositories** — grammar inventory, PlantUML grammar status, contribution process
> 4. **GitHub engineering blog and GitHub Universe talks** — indexing internals, RAG pipeline architecture
> 5. **PlantUML official documentation** — file format specification, syntax reference, `!include` semantics, metadata directives, server API
> 6. **npm / PyPI package registries** — PlantUML parser libraries, MCP server packages
> 7. **GitHub search** — repositories matching "plantuml mcp", "plantuml parser", "plantuml tree-sitter", "plantuml json", "plantuml markdown"
> 8. **Community sources** — GitHub Discussions, Stack Overflow, Reddit r/githubcopilot, blog posts from architecture teams
> 9. **Academic papers** — diagram-to-text extraction, visual language grounding in LLMs
>
> ### Output Format
>
> Structure the findings as:
>
> 1. **Executive Summary** — 5-8 sentence answer: what works today without MCP, what requires MCP, and what does not work at all
> 2. **Native Copilot Behavior** — detailed analysis of how Copilot currently handles PlantUML, with evidence
> 3. **Zero-Infrastructure Optimizations** — approaches requiring only file/naming/instruction changes
> 4. **Medium-Infrastructure Approaches** — companion file generation, CI pipelines, VS Code extensions
> 5. **MCP Server Approaches** — existing and custom MCP server options
> 6. **Multimodal Approaches** — image-based reasoning with rendered diagrams
> 7. **Alternative Format Analysis** — Mermaid, D2, Structurizr comparison
> 8. **Ranked Comparison Table** — all approaches ranked across the six criteria
> 9. **Recommended Layered Strategy** — specific combination of approaches for immediate, medium-term, and long-term adoption
> 10. **Open Questions for Empirical Testing** — what cannot be determined from documentation and requires hands-on validation
>
> Cite ALL sources with full URLs. Prefer sources from 2024-2026. Include the number of sources cited at the end of each major section.
