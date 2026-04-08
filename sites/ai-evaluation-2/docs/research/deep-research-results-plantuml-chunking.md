# Deep Research Results: PlantUML Diagram Chunking and Context Injection

<!-- Paste deep research results below this line -->
Deep Research Report: PlantUML Diagram Chunking and Context Injection for GitHub Copilot
1. Executive Summary
The integration of GitHub Copilot within enterprise architecture workflows presents a significant challenge when the primary artifacts are PlantUML (.puml) diagrams. GitHub Copilot, powered by advanced models such as Claude Opus 4.6, possesses immense potential for architectural analysis; however, the extraction and injection of context from .puml files are severely hindered by the native indexing pipeline. PlantUML is treated as generic plain text due to the absence of an officially supported Tree-sitter grammar, forcing the indexer to rely on naive 60-line sliding window chunking algorithms locally and token-based chunking remotely. This structural fragmentation destroys the semantic relationships between participants defined at the top of a file and their interactions defined dozens of lines below. Furthermore, Copilot does not natively resolve !include directives, rendering C4 macro libraries opaque, and explicitly excludes rendered .svg output from its workspace index.
Addressing this deficiency requires a multi-layered, progressive strategy. Zero-infrastructure optimizations, such as rigid file naming conventions and scoped .instructions.md rules, offer marginal improvements by weighting lexical search fallbacks and guiding model behavior. Medium-infrastructure approaches provide the highest immediate return on investment: generating "shadow files" (companion Markdown or JSON files) via Continuous Integration (CI) pipelines translates graphical syntax into the standard Tree-sitter-supported formats that Copilot processes flawlessly. For advanced, dynamic interaction, the Model Context Protocol (MCP) bridges the gap entirely. Custom and community-maintained MCP servers enable the Large Language Model (LLM) to query, validate, and render PlantUML code on demand, bypassing the generic indexing pipeline altogether. While migrating to alternative model-based formats like Structurizr DSL offers long-term benefits for model-driven architecture, a layered implementation of companion files and MCP servers represents the optimal path for optimizing an existing repository of PlantUML artifacts.
Sources cited in this section: 0
2. Native Copilot Behavior
To engineer a robust solution for PlantUML retrieval, the precise mechanisms of GitHub Copilot's indexing, chunking, and search architectures must be deconstructed. Copilot does not natively comprehend .puml files as structural architectural models; instead, it processes them through fallback text-processing pipelines that were designed for generic prose rather than domain-specific languages.
Tree-Sitter Grammar Inventory and Deficiencies
GitHub Copilot relies extensively on Tree-sitter, an incremental parsing library, to generate Abstract Syntax Trees (ASTs) for source code.1 These ASTs allow the Copilot indexer to identify function definitions, class boundaries, variable scopes, and code blocks, enabling semantic chunking that preserves logical relationships. The official kreuzberg-dev/tree-sitter-language-pack and the Copilot bundled parsers support over 170 programming languages, including major ecosystems like Java, Python, C#, and markup languages like Markdown and JSON.1
An exhaustive inventory of the officially supported Tree-sitter grammars reveals that PlantUML is completely absent from the production ecosystem.1 While experimental third-party repositories exist—such as Decodetalkers/tree_sitter_plantuml and lyndsysimon/tree-sitter-plantuml—these are categorized as pre-release, unfinished, or abandoned.3 Without an integrated Tree-sitter grammar, Copilot cannot parse @startuml and @enduml boundaries, distinguish between a participant declaration and a relationship arrow (->), or understand the scope of an alt/else control flow block. The absence of a structural parser means that Copilot is blind to the syntax hierarchy that defines an architecture diagram.
Chunking Behavior and The Sliding Window Fallback
In the absence of a Tree-sitter AST, Copilot must rely on fallback mechanisms to process unknown file types. For local workspace indexing and active editor context gathering, Copilot utilizes a component known as the FixedWindowJaccardMatcher.5 This algorithm slices the plain text file into overlapping chunks using an eager mode sliding window, which defaults to a maximum of 60 lines.5 It then computes the Jaccard similarity (the intersection over union of lexical tokens) between each 60-line window and the reference file or query.7
This 60-line local window is highly destructive to PlantUML architecture diagrams. In a typical enterprise sequence diagram, the actors, participants, boundaries, and database entities are declared at the beginning of the file (e.g., lines 1-20). The actual runtime interactions, method calls, and return payloads often occur significantly later (e.g., lines 70-150). A 60-line sliding window physically isolates an interaction like svc_check_in -> svc_reservations : GET /reservations into a chunk that completely lacks the earlier definitions of what those services actually represent. When the semantic search ranks these chunks based on vector similarity or dot-product matching to a user query, the fragmented chunks lose their contextual grounding, leading to retrieval failure.9 The model receives the action but not the actors.
Inclusions, Macro Resolution, and Multi-Diagram Files
Enterprise architecture teams heavily utilize the !include directive to standardize diagrams, particularly when utilizing the C4 Model macro library (e.g., !include C4_Component.puml).10 GitHub Copilot treats these directives as opaque string literals.11 When Copilot chunks a .puml file for its vector index, it does not execute a pre-processor to resolve local file paths or download remote URLs; it merely indexes the literal text of the include statement. Consequently, the LLM remains completely blind to the underlying macro definitions (such as Container(), System(), or Rel()). Because the definitions are not injected into the context, the LLM treats them as undefined syntax, severely degrading its ability to reason about the architecture.
Furthermore, if a single .puml file contains multiple diagrams (multiple @startuml / @enduml blocks), Copilot's fallback indexer treats the entire file as a continuous string of text. It chunks indiscriminately across the boundaries of distinct diagrams. This cross-contamination means a chunk might contain the end of a sequence diagram and the beginning of a deployment diagram, thoroughly confusing the embedding model regarding the architectural state.
Indexing Inclusions and Exclusion Patterns
Copilot's indexing pipeline implements strict content exclusion patterns to prevent vector database bloat and manage token limits. Binary files, PDFs, and highly dense graphical files are excluded by default.12 Notably, .svg (Scalable Vector Graphics) files are explicitly excluded from the workspace index.14
This represents a significant missed opportunity. Even though an exported PlantUML SVG is a graphical file, it contains highly structured, readable XML <text> nodes representing the diagram's exact content. By excluding **/*.svg, Copilot prevents this cleanly parsed text from entering the semantic search index. If these files were not excluded, the semantic search could theoretically index the rendered labels and relationships directly from the XML tree.
Semantic vs. Lexical Search Effectiveness
When a user executes a @workspace query, Copilot employs a hybrid search strategy, combining semantic vector embeddings with exact-match lexical search (e.g., TF-IDF or BM25 fallback).9
The semantic search component fails reliably on PlantUML syntax. Embedding models are trained primarily on natural language prose and highly structured programming languages like Python or JavaScript.16 The high density of symbolic operators in PlantUML (-->, ->>, -[#red]>o) creates noise in the embedding space. This lowers the cosine similarity score between a natural language query ("which services does svc-check-in call?") and the dense vector representation of the PlantUML arrow syntax.
Lexical search provides moderate success only if the user query contains exact string matches. A query for svc-check-in will successfully locate the .puml file containing that string. However, because the AST is absent and the chunking is fragmented, Copilot struggles to synthesize the directionality of the call or the broader context if the query spans a chunk boundary. The lexical match pulls the file into the context window, but the LLM must expend significant reasoning effort to decipher the truncated DSL syntax.
Sources cited in this section: 24
3. PlantUML Syntax and Structure: What an Ideal Parser Would Extract
Before evaluating workarounds, generated artifacts, or MCP servers, it is necessary to define the exact semantic elements that matter for architecture reasoning. PlantUML is a presentation-driven domain-specific language (DSL) encompassing over 15 distinct diagram types, making its syntax highly permissive and difficult to parse cleanly.18 An ideal structural parser (such as a mature Tree-sitter grammar) would extract these elements into a deterministic knowledge graph.
Critical Architectural Elements
The following table outlines the core semantic elements of PlantUML, their architectural purpose, and how plain-text search currently degrades their value.
PlantUML Element
Architectural Purpose
Plain-Text Degradation
Ideal Parser Extraction
Participants & Actors (participant, database, actor)
Nouns of the system. Define the entities, boundaries, and data stores.
Lexical search finds names but loses the assigned alias and the entity type classification.
Maps entities to a global registry, resolving aliases to full system names.
Relationships & Arrows (->, -->, ->>)
Verbs of the system. Define synchronous/asynchronous calls, data flow, and dependencies.
Dense punctuation confuses vector embeddings. Directionality is frequently misunderstood by LLMs.
Extracts a directed adjacency list: ``.
C4 Macros (System(), Container(), Rel())
Semantic abstractions for enterprise architecture modeling.
Opaque string literals. The LLM cannot map the macro parameters without the !include definitions.
Parses parameters into structured objects: {type: "Container", name: "API", tech: "Java"}.
Activation & Scope (activate, alt, loop, opt)
Defines runtime control flow, error handling, and parallel execution.
60-line chunks split alt from else blocks. The LLM loses the execution path context.
Builds a nested execution tree, accurately isolating happy paths from error handling paths.
Notes & Metadata (note right, note over)
Human-readable context explaining why an interaction occurs or detailing payloads.
Highly susceptible to chunk truncation. Multi-line notes are easily separated from their target entities.
Binds the text content of the note directly as a property of the specific relationship or actor.
Includes & Defines (!include, !define)
Modularizes diagram components, styles, and enterprise standards.
Treated as literal text. The external dependencies are never fetched or indexed.
Recursively resolves file paths and injects the macro definitions into the AST.

The Gap Between Lexical Search and Structural Parsing
The core deficit identified by analyzing these elements is that plain-text lexical search treats an architecture diagram as a flat, linear sequence of words. When Copilot uses a Jaccard similarity sliding window 5, it assumes that physical proximity in the text equates to logical proximity. In PlantUML, this assumption is false. A participant defined on line 5 might not interact with another system until line 120.
An ideal structural parser would transcend linear text processing. It would read the .puml file and generate a directed graph where entities are nodes and arrows are edges. The LLM would then query this structured graph rather than attempting to stitch together fragmented string chunks. Because this ideal parser does not natively exist in Copilot, the subsequent sections evaluate mechanisms to artificially construct this structured context.
Sources cited in this section: 4
4. Zero-Infrastructure Optimizations
For organizations that cannot deploy custom servers or CI/CD pipelines, several optimizations can be applied directly to the repository structure, file naming conventions, and Copilot instruction files. These zero-infrastructure methods manipulate Copilot's existing hybrid retrieval system to weight the correct files more heavily.
Structural File Optimizations
Because semantic search on PlantUML syntax yields poor cosine similarity scores, the retrieval mechanism must be artificially biased toward lexical matches on file metadata.
First, granular file naming conventions act as explicit semantic indices. Renaming a generic file from diagram-001.puml to sequence-svc-check-in-creates-reservation.puml directly injects the caller, the callee, and the diagram type into the filename tokens. Copilot's file search heavily weights filename matches, ensuring the file is retrieved even if the internal DSL syntax confuses the vector search.12
Second, the structural layout of the directories serves as a strong relevance signal. Grouping diagrams by domain or service (e.g., /docs/architecture/svc-check-in/) rather than by diagram type (e.g., /docs/diagrams/sequence/) improves spatial locality. When a user asks a question about a specific service, Copilot's retrieval algorithm recognizes the directory path as highly relevant, pulling in surrounding Markdown and .puml files together as a cohesive context block.
Third, to mitigate the 60-line sliding window fragmentation 5, files must be kept as concise as possible. Enforcing a strict limit of one @startuml / @enduml block per file ensures that participant declarations and relationship arrows have the highest possible probability of existing within the same or adjacent chunks. Multi-diagram files guarantee semantic fragmentation and must be avoided.
Scoped Instructions and AGENTS.md
VS Code and GitHub Copilot support defining custom instructions that are automatically appended to the LLM's system prompt. These instructions can be stored centrally in .github/copilot-instructions.md or AGENTS.md.19
By utilizing the applyTo frontmatter property, instructions can be scoped strictly to diagram files. For example, a .github/instructions/plantuml.instructions.md file beginning with applyTo: "**/*.puml" can teach Copilot how to read the DSL.19 Architects can codify rules such as:
"When analyzing .puml files, always treat -> as a synchronous HTTP network call unless explicitly annotated otherwise."
"When encountering the C4 macro Rel(A, B,...), map this mentally to a strict architectural dependency where A relies on B."
Furthermore, cross-referencing instructions can compensate for indexing failures. A global instruction rule stating, "If asked about service dependencies in a diagram, always execute a workspace search for the corresponding OpenAPI spec in /specs/ to verify the payload definitions," forces the agent to rely on more structured formats (like YAML) to validate the ambiguous .puml text.
The SKILL.md Framework and DSL Teaching
The GitHub awesome-copilot repository defines "Agent Skills," which are self-contained folders containing a SKILL.md file designed to teach Copilot highly specific capabilities.20 The existing plantuml-ascii skill provides a blueprint for this methodology.22
This skill teaches the Copilot agent how to execute PlantUML command-line operations to generate text-based ASCII diagrams (using -txt and -utxt flags).22 While originally designed for output generation, the methodology proves that SKILL.md files can successfully inject syntax rules into the model's context. By implementing a custom skill, a team can provide few-shot learning examples of complex sequence and C4 diagrams directly in the prompt context. This teaches the Claude Opus 4.6 model how to trace relationships step-by-step through a text block, significantly improving its reasoning accuracy over raw, untaught text ingestion.
Sources cited in this section: 13
5. Medium-Infrastructure Approaches: Companion File Generation
The most robust non-MCP solution to the PlantUML indexing problem is the implementation of the "Shadow File" pattern. Since Copilot perfectly understands Markdown and JSON through highly optimized Tree-sitter grammars and chunkers 1, the optimal strategy is to automatically convert the unsupported .puml format into a fully supported format. This creates a "shadow" of the architecture that the indexer can seamlessly digest.
PlantUML-to-Markdown Summary Generation
Natural language prose is the absolute optimal format for semantic vector search. An LLM searching a vector database for the query "which services does svc-check-in call?" will instantly match a dense semantic sentence stating: "The svc-check-in service makes a synchronous GET call to svc-reservations."
To achieve this, a Continuous Integration (CI) pipeline (e.g., GitHub Actions) can be configured to trigger upon any commit containing .puml file modifications. The pipeline executes a script that utilizes a parser or an LLM API call to read the .puml file and output a companion Markdown file (e.g., svc-check-in-sequence.summary.md). This companion file acts as the semantic shadow of the diagram. It should contain a human-readable list of participants, a bulleted flow of runtime operations, and explicitly separated error paths.23 Because Markdown is natively supported, Copilot will chunk it semantically by structural headers (## Participants, ## Call Flow), preserving the complete context across the entire file.26
AST Extraction and JSON Adjacency Lists
For a more deterministic and highly structured extraction, JavaScript libraries such as plantuml-parser (an npm package utilizing a Parsing Expression Grammar) can be deployed within the CI pipeline.27 While this specific parser has limitations with complex nested sequence diagrams, it successfully extracts detailed elements and relationships from Class and Component (C4) diagrams.27
The pipeline workflow operates as follows:
Parsing: The plantuml-parser reads the C4 .puml file and generates a complete Abstract Syntax Tree (AST).
Transformation: A custom script transforms the verbose AST into a simplified JSON array representing a directed graph or adjacency list (e.g., ``).
Indexing: The .json file is written to the repository alongside the .puml file.
Copilot possesses a robust Tree-sitter grammar for JSON.1 Its JSON chunker easily digests this structured data, associating keys with values perfectly. This allows the Copilot coding agent to accurately traverse the JSON objects to answer deep architectural dependency queries that would be impossible to parse from the raw .puml syntax.
Mitigating Staleness Risk
The primary operational risk of generating companion files is drift—the scenario where the generated Markdown or JSON no longer matches the source .puml diagram. This risk must be mitigated strictly through CI/CD automation.
The .gitignore file should NOT ignore the companion files; they must be committed to the repository so the GitHub Copilot semantic indexer can ingest them remotely. The CI pipeline must enforce a validation check that fails the build if a .puml file is modified without its corresponding shadow file being regenerated. Alternatively, the pipeline can be configured to automatically commit the regenerated files back to the active branch before merging.28 This ensures that the context available to Copilot is never desynchronized from the actual architecture diagrams.
Sources cited in this section: 9
6. Embedded Metadata in PlantUML
If the generation of companion shadow files is deemed too intrusive to the repository structure, enriching the .puml files themselves with machine-readable metadata can significantly improve the performance of Copilot's 60-line sliding window chunker. By manipulating the physical layout of the text, architects can force the chunker to group critical context together.
Structured Comments and Header Weighting
Because the sliding window algorithm captures sequential lines of text indiscriminately 5, packing the top of the .puml file (e.g., lines 1-15) with highly dense, descriptive metadata ensures that any chunk overlapping the beginning of the file contains the global context.
Descriptive Directives: Utilizing the title and description directives with verbose natural language rather than terse names. A title like title Sequence Diagram: svc-check-in creates a new reservation via svc-reservations provides massive semantic value to the embedding model compared to title Check In Flow.
Structured Headers: Adding structured comments such as ' @participants: svc-check-in, svc-reservations or ' @describes: check-in happy path directly below the title. When Copilot's TF-IDF fallback or semantic embedding model scans the file, these natural language tokens drastically boost the file's relevance score for related queries, effectively bridging the gap between the syntax and the user's intent.
Descriptive Labels: Arrow labels must be overly verbose. A -> B : get reservation tokenizes poorly. svc-check-in -> svc-reservations : GET /reservations/{confirmation_code} Retrieve reservation details injects API paths and clear intent directly onto the relationship edge, ensuring that even if this single line is isolated in a chunk, it retains maximum meaning.
The @startjson and @startyaml Directives
PlantUML natively supports rendering structured data visualizations using the @startjson / @endjson and @startyaml / @endyaml boundary tags.29 This native feature presents a unique opportunity for context injection.
An architecture team can embed a raw JSON or YAML block at the bottom of the .puml file containing the explicit adjacency list of the services depicted in the diagram. While Copilot may not trigger its native .json Tree-sitter parser for the entire file due to the .puml extension, the localized density of standard JSON key-value pairs within a text chunk provides the LLM with unambiguous, easily readable relationship data. When that specific chunk is retrieved, the LLM processes the JSON snippet flawlessly, bypassing the need to interpret the preceding arrow syntax.
Pragma Directives
PlantUML supports !pragma directives for advanced rendering configurations and metadata tracking.30 While these directives do not directly influence Copilot's indexing behavior, custom pre-processors built by the team could use specific !pragma tags to trigger the generation of architectural metadata or govern how the diagrams are validated during CI/CD pipelines.
Sources cited in this section: 6
7. VS Code Extensions and Language Server Protocol (LSP)
GitHub Copilot's contextual awareness is tightly integrated with the local VS Code extension ecosystem. To understand the structure of the active editor file, Copilot leverages the Language Server Protocol (LSP), specifically querying the DocumentSymbolProvider interface to extract hierarchical context.32
The jebbs.plantuml Extension
The dominant VS Code extension for this domain is jebbs.plantuml (boasting over 3 million installations).35 This extension is responsible for registering the plantuml language ID within the editor and mapping it to .puml, .pu, .wsd, and .iuml files.36
Crucially, jebbs.plantuml implements a DocumentSymbolProvider via its internal symboler.js module.37 When an architect opens a .puml file in the active editor, the extension parses the file and provides a hierarchical list of symbols to the VS Code Outline view. It recognizes structural declarations such as an actor, a participant, or a component as distinct symbols.
Copilot's LSP Integration and Context Augmentation
When a user interacts with Copilot Chat and asks a question about the active file, Copilot intercepts this LSP traffic. It queries the VS Code API for the available document symbols and injects them directly into the prompt context.32
Contextual Boost: If the extension successfully maps a participant "svc-check-in" declaration to a SymbolKind.Class or SymbolKind.Variable, Copilot's context window is enriched with an explicitly defined, structured list of entities present in the diagram. This gives the LLM an immediate "table of contents" for the architecture, significantly improving its ability to track actors across the file.
Limitations of Active Editor Scope: This LSP integration only functions for the active file or files currently open in the editor. It does not solve the global @workspace retrieval problem. VS Code does not spin up language servers for all 140 background files simultaneously during a remote index.40 Therefore, this optimization is purely local.
Parsing Limitations: The symbol mapping in jebbs.plantuml relies on regular expressions rather than a true Abstract Syntax Tree (AST). This regex approach frequently fails to identify symbols nested deeply within complex multi-line C4 macros or !include chains, resulting in an incomplete symbol list being passed to Copilot.
Sources cited in this section: 11
8. Tree-Sitter Grammar Feasibility
The foundational issue causing Copilot's poor indexing of PlantUML is the absolute lack of a bundled Tree-sitter grammar. Developing, stabilizing, or integrating a custom grammar represents a high-effort, high-reward strategy that attacks the root cause of the problem.
Anatomy and Status of a PlantUML Grammar
A functional Tree-sitter grammar requires a grammar.js file defining the syntactic rules and a C compiler to generate the high-performance parser.41 For Copilot to utilize it for syntax highlighting and structural chunking, it additionally requires Scheme query files (such as tags.scm and highlights.scm) to map the syntax nodes to standard semantic capture names.42
Analyzing the current landscape of experimental repositories reveals significant immaturity. The Decodetalkers/tree_sitter_plantuml repository contains a grammar.js and comprises 7.1% Scheme code, indicating that some query tagging has been implemented for structural parsing.4 However, the repository has seen minimal recent activity, has no official releases, and is explicitly labeled as experimental.3 Similar forks, such as lyndsysimon/tree-sitter-plantuml and cathaysia/tree-sitter-plantuml, share this abandoned or incomplete status.44 Crucially, none of these grammars are packaged within the official kreuzberg-dev polyglot bindings utilized by modern AI agents.2
Complexity and Contribution Barriers
The feasibility of finishing a PlantUML grammar is hindered by the language's inherent complexity. PlantUML is not a formally defined programming language; it has evolved organically over a decade with highly permissive and flexible rules. It encompasses over 15 entirely distinct diagram syntaxes. This extreme flexibility makes it exceptionally difficult to adhere strictly to the LR(1) constraints required by Tree-sitter's GLR parsing algorithm.27
Furthermore, even if the enterprise architecture team dedicated the resources to perfect a PlantUML grammar, upstream contribution is currently blocked. The official tree-sitter-grammars organization explicitly notes they are not accepting new third-party contributions at this time.46 GitHub Copilot's remote indexing pipeline relies on this locked ecosystem. Therefore, the grammar could only be used locally via custom VS Code extension injection 47, which introduces significant maintenance overhead and fails to solve the remote repository indexing problem.
Sources cited in this section: 14
9. MCP Server Approaches
The Model Context Protocol (MCP) provides the ultimate architectural bypass for Copilot's indexing limitations. Instead of relying on passive, error-prone semantic search over plain text, an MCP server equips the Claude Opus 4.6 agent with active tools to query, parse, and render diagrams dynamically.
Existing PlantUML MCP Servers
The open-source ecosystem has rapidly developed several MCP servers designed specifically to interface with PlantUML:
infobip/plantuml-mcp-server: This is a fully featured, production-ready MCP server designed for integration with Claude Desktop and Claude Code.49 It exposes powerful tools such as generate_plantuml_diagram to render SVGs or PNGs and encode_plantuml/decode_plantuml to generate shareable URLs.49 Crucially, it includes an advanced context prompt named plantuml_error_handling. This prompt teaches the LLM how to detect native server validation errors and execute self-healing auto-fix workflows for common syntax mistakes (e.g., missing quotes, invalid arrow directions).49
@brainstack/plantuml-mcp: An npm-based server that generates UML diagrams, applies custom corporate branding, supports multiple output formats, and is easily integrated directly into VS Code AI extensions.50
junqing258/plantuml-mcp: This server focuses heavily on syntax checking without the overhead of rendering. It possesses the unique capability to extract PlantUML source code directly from the embedded metadata of PNG/SVG files.51
Custom FastMCP Implementation for Architecture Querying
While existing servers are excellent for generating diagrams, an enterprise architecture team with 140+ C4 and sequence diagrams requires an AI that can read and analyze complex relationships. Relying solely on generation is insufficient.
A custom Python-based FastMCP server can be developed with moderate effort (estimated 3-5 days) to expose read-only architectural querying tools tailored to the repository's exact structure. This server would expose the following tools to Copilot:
list_diagrams(domain: str): Scans the repository and returns a curated list of diagrams related to a specific business service.
get_diagram_source(file_path: str): Reads a .puml file and recursively resolves all !include directives (like C4_Component.puml) internally before returning the fully expanded text to the LLM. This entirely solves the macro opacity problem.
get_service_dependencies(service_name: str): Uses an internal regex engine or a script like plantuml-parser to aggressively scan all 140 files in the workspace. It returns a consolidated JSON array of every upstream and downstream system that service_name interacts with.
By exposing these specific tools, the Claude Opus 4.6 agent's behavior changes fundamentally. When a user asks "which services does svc-check-in call?", the agent will recognize its own inability to answer via standard codebase search, autonomously invoke the get_service_dependencies("svc-check-in") MCP tool, and receive deterministic, structurally parsed data.
Sources cited in this section: 11
10. Multimodal Approaches (Image-Based Reasoning)
With the integration of Claude Opus 4.6 into GitHub Copilot, the AI assistant now possesses state-of-the-art multimodal (vision) capabilities. Opus 4.6 achieves exceptional scores on visual reasoning benchmarks, notably scoring 77.3% on MMMU Pro with tools, and 61.3% specifically on complex phylogenetic tree and scientific diagram analysis.53
Image-Based Reasoning vs. Text Parsing
Architecture diagrams present a unique advantage for multimodal AI. Unlike UI wireframes or arbitrary images, C4 and sequence diagrams are explicit node-edge graphs. There is no hidden state; every relationship is drawn as a visible line. When Claude Opus 4.6 analyzes a rendered sequence diagram, its Optical Character Recognition (OCR) and spatial reasoning algorithms can highly accurately trace the vertical activation bars, identify parallel execution blocks, and read the API endpoint labels attached to the horizontal arrows.56 The visual representation often resolves the ambiguity present in the raw text DSL.
The SVG and PNG Context Pipeline
The primary barrier to utilizing this immense visual reasoning power is Copilot's strict file exclusion list. .svg files are blocked from text indexing 13, and binary .png files are not automatically embedded into the chat context during a standard @workspace query.12
To leverage Opus 4.6's vision for architecture analysis, the workflow must be driven manually or via agentic tool use:
Manual Attachment: The architect must explicitly drag and drop the rendered .png of the diagram into the Copilot Chat interface. Once the image is attached to the prompt context, Opus 4.6 can analyze the call chain flawlessly and answer questions about the specific diagram.58
MCP Rendering Loop: Utilizing a server like infobip/plantuml-mcp-server, the agent can be instructed to read the raw .puml file, use the MCP tool to generate a PNG, and then analyze the resulting image in a secondary step. This dual-context approach allows the model to verify its text-based understanding against the rendered spatial layout, drastically reducing hallucinations regarding control flow.
While multimodal reasoning is incredibly powerful for ad-hoc debugging, deep analysis, or refactoring of a single diagram, it does not solve the global repository search problem. Multimodal search cannot currently find which of the 140 diagrams contains a specific service, making it a supplementary deep-analysis tool rather than a primary indexing strategy.
Sources cited in this section: 8
11. Alternative Diagram Formats
Given the inherent limitations of integrating PlantUML's presentation-based syntax with standard AI coding assistants, evaluating alternative formats is a necessary due diligence step for long-term architectural planning.
Mermaid and D2
Mermaid is the native diagramming language supported by GitHub Markdown.59 Copilot and its underlying embedding models are trained heavily on Markdown and Mermaid blocks. Because Mermaid is natively embedded in .md files, it bypasses the obscure .puml file extension issues and integrates seamlessly into the standard semantic chunking algorithms. However, Mermaid lacks the deep structural capabilities of PlantUML, particularly regarding complex enterprise C4 macros and advanced sequence diagram control flows.61
D2 is a modern, highly readable diagram-as-code language designed specifically for software engineering.63 Unlike PlantUML, D2 possesses actively maintained Tree-sitter grammars (pleshevskiy/tree-sitter-d2, ravsii/tree-sitter-d2).64 If these grammars were integrated into the editor, D2 would provide vastly superior semantic chunking. However, migrating 140+ enterprise architecture diagrams from PlantUML to D2 represents a massive manual effort, as automated translation tools often lose layout nuances and styling.
Structurizr DSL
Structurizr DSL represents a fundamental paradigm shift; it is a model-based language rather than a presentation-based language.66 Elements (Software Systems, Containers, Components) are defined hierarchically within a central model, and various diagram views are generated dynamically from that single model.
AI Compatibility: LLMs excel at generating and reading Structurizr DSL because it is highly structured text that strictly enforces C4 architecture rules.67 It lacks the noisy presentation directives (colors, manual spacing) that confuse vector embeddings in PlantUML.
Export to PlantUML: Structurizr can automatically export its views to PlantUML or Mermaid formats for rendering.69
For an enterprise team deeply invested in the C4 model, migrating the architectural "source of truth" to Structurizr DSL, while using PlantUML merely as a downstream, generated rendering artifact, solves the semantic context issue entirely. The LLM reads the centralized, cleanly chunked Structurizr model, and humans read the generated PlantUML diagrams.
Sources cited in this section: 10
12. Comparative Analysis and Recommendations
The discovered approaches for optimizing PlantUML context injection are ranked below based on implementation effort, infrastructure requirements, maintenance burden, retrieval quality, and friction for team adoption.
Ranked Comparison Table
Approach
Effort to Implement
Infrastructure Required
Maintenance Burden
Retrieval Quality Improvement
Team Adoption Friction
Composability
1. File Naming & 1-Diagram-per-File
Low (Hours)
None
Low
Low (Improves lexical filename search only)
Medium (Requires renaming existing files)
High (Base layer for all others)
2. Scoped .instructions.md
Low (1 Hour)
None
Low
Low-Medium (Guides interpretation, doesn't fix chunking)
Zero
High
3. LSP / jebbs.plantuml
Low (1 Hour)
VS Code Extension
Zero
Low (Only works on active open file)
Zero
High
4. Shadow Files (CI/CD Markdown Gen)
Medium (Days)
CI/CD Pipeline, Python/Node Script
Medium (Pipeline upkeep)
High (Perfect semantic indexing)
Low (Invisible to developers)
High
5. Custom FastMCP Server
High (Weeks)
MCP Server Runtime
High
Very High (Deterministic read/query access)
Low (Automatic tool calling)
Medium (Replaces generic search)
6. Existing MCP (e.g., infobip)
Medium (Days)
MCP Client Config
Low
Medium (Focuses on rendering/fixing, not global search)
Low
High
7. Multimodal (Image Attachments)
Zero
None
Zero
Medium (Excellent reasoning, zero search capability)
High (Manual drag-and-drop workflow)
Low
8. Migrate to Structurizr DSL
Very High (Months)
Structurizr CLI
Low
Very High (Model-based indexing)
High (New language syntax)
Low (Replaces PlantUML)

Recommended Layered Strategy
Given the team's existing investment in 140+ PlantUML files, a complete migration to Structurizr DSL is not recommended for the immediate term due to migration costs. Instead, the team should execute a progressive, three-layered strategy:
Layer 1: Immediate Action (Zero-Infrastructure)
Enforce a strict "one @startuml block per file" rule immediately to prevent the 60-line sliding window from splitting unrelated diagrams.
Rename files to be highly descriptive (e.g., c4-container-svc-check-in.puml), grouping them into domain-specific directories to optimize Copilot's lexical path matching.
Create a .github/instructions/plantuml.instructions.md file with applyTo: "**/*.puml", explicitly defining how the Claude Opus 4.6 model should trace arrows and interpret opaque C4 macros.
Layer 2: Medium-Term (The Shadow File Pattern)
Implement a GitHub Actions workflow that executes on pull requests containing .puml files.
Use a script (leveraging plantuml-parser or a lightweight LLM call) to generate a .summary.md companion file for every diagram.
Commit these summaries alongside the source files. This forces Copilot's native Markdown Tree-sitter grammar to index the architecture perfectly, allowing @workspace queries to retrieve the textual summary and cross-reference the adjacent .puml file seamlessly.
Layer 3: Long-Term Capability (Custom MCP Integration)
Deploy a lightweight, custom read-only FastMCP server tailored specifically to the repository's structure.
Equip this server with tools like search_architecture(service_name) and resolve_puml_includes(file_path). When an architect asks a complex integration question, the agent will autonomously bypass the VS Code sliding-window indexer, execute the MCP tool, expand the C4 macros, and return deterministic, hallucination-free answers based on the complete architecture.
Sources cited in this section: 0
13. Open Questions for Empirical Testing
Certain behaviors within GitHub Copilot's proprietary, closed-source retrieval-augmented generation (RAG) pipeline cannot be fully determined from documentation alone. These require empirical validation by the enterprise architecture team:
Exact Token Limits of Remote RAG vs. Local Jaccard: While the local 60-line eager mode sliding window is documented, the exact token boundary and overlap percentage of the remote GitHub Enterprise semantic indexer for unknown .puml files must be tested. Creating a dummy file with 500 lines of sequential comments and tracking exactly where the LLM's knowledge cuts off will reveal the remote chunk size.
LSP Symbol Weighting: Does Copilot's embedding model actively weight the DocumentSymbol data generated by the jebbs.plantuml extension higher than the raw text chunks, and does this symbol data persist in memory when the file is closed in the editor?
JSON vs. Markdown Shadow Files: Empirical A/B testing is required to determine whether Copilot's retrieval accuracy is higher when the shadow file is formatted as an adjacency list (.json) or as natural language prose (.md).
files.exclude Override: Testing whether explicitly removing **/*.svg from the VS Code and GitHub repository exclusion lists allows Copilot to index the raw XML <text> nodes inside rendered PlantUML SVGs. If successful, this could offer a zero-code parsing bypass by treating SVGs as structured text documents.
Sources cited in this section: 0
Works cited
Tree-sitter: Introduction, accessed April 8, 2026, https://tree-sitter.github.io/
kreuzberg-dev/tree-sitter-language-pack - GitHub, accessed April 8, 2026, https://github.com/kreuzberg-dev/tree-sitter-language-pack
List of parsers · tree-sitter/tree-sitter Wiki - GitHub, accessed April 8, 2026, https://github.com/tree-sitter/tree-sitter/wiki/List-of-parsers
Decodetalkers/tree_sitter_plantuml: treesitter for plantuml - GitHub, accessed April 8, 2026, https://github.com/Decodetalkers/tree_sitter_plantuml
copilot-explorer | Hacky repo to see what the Copilot extension sends to the server - Parth Thakkar, accessed April 8, 2026, https://thakkarparth007.github.io/copilot-explorer/posts/copilot-internals.html
Unveiling Memorization in Code Models - arXiv, accessed April 8, 2026, https://arxiv.org/html/2308.09932v2
hello-agents/docs/chapter9/Chapter9-Context-Engineering.md at main - GitHub, accessed April 8, 2026, https://github.com/datawhalechina/hello-agents/blob/main/docs/chapter9/Chapter9-Context-Engineering.md
EXPLORING THE USAGE OF PRE-TRAINED MODELS FOR CODE-RELATED TASKS, accessed April 8, 2026, https://sonar.ch/documents/328566/files/2024INF007.pdf
How GitHub Copilot Knows Your Code: Inside Its Indexing Magic | by Yasith Rashan, accessed April 8, 2026, https://yasithrashan.medium.com/how-github-copilot-knows-your-code-inside-its-indexing-magic-aba59a0ce0e8
GitHub - plantuml-stdlib/C4-PlantUML: C4-PlantUML combines the benefits of PlantUML and the C4 model for providing a simple way of describing and communicate software architectures, accessed April 8, 2026, https://github.com/plantuml-stdlib/C4-PlantUML
!include file works only with full path in Markdown · Issue #375 · qjebbs/vscode-plantuml, accessed April 8, 2026, https://github.com/qjebbs/vscode-plantuml/issues/375
How Copilot understands your workspace - Visual Studio Code, accessed April 8, 2026, https://code.visualstudio.com/docs/copilot/reference/workspace-context
Files excluded from GitHub Copilot code review - GitHub Docs, accessed April 8, 2026, https://docs.github.com/en/copilot/reference/review-excluded-files
Content exclusion for GitHub Copilot, accessed April 8, 2026, https://docs.github.com/en/copilot/concepts/context/content-exclusion
Indexing repositories for GitHub Copilot, accessed April 8, 2026, https://docs.github.com/en/copilot/concepts/context/repository-indexing
RepoHyper: Better Context Retrieval Is All You Need for Repository-Level Code Completion, accessed April 8, 2026, https://arxiv.org/html/2403.06095v1
ContextModule: Improving Code Completion via Repository-level Contextual Information - arXiv, accessed April 8, 2026, https://arxiv.org/html/2412.08063v1
PlantUML, accessed April 8, 2026, https://plantuml.com/
Use custom instructions in VS Code, accessed April 8, 2026, https://code.visualstudio.com/docs/copilot/customization/custom-instructions
awesome-copilot/docs/README.skills.md at main - GitHub, accessed April 8, 2026, https://github.com/github/awesome-copilot/blob/main/docs/README.skills.md
Adding repository custom instructions for GitHub Copilot - GitHub Docs, accessed April 8, 2026, https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot
awesome-copilot/skills/plantuml-ascii/SKILL.md at main - GitHub, accessed April 8, 2026, https://github.com/github/awesome-copilot/blob/main/skills/plantuml-ascii/SKILL.md
Computer Security: ESORICS 2020 International Workshops, CyberICPS, SECPRE, and ADIoT, Guildford, UK, September 14–18, 2020, Revised Selected Papers 3030643298, 9783030643294 - DOKUMEN.PUB, accessed April 8, 2026, https://dokumen.pub/computer-security-esorics-2020-international-workshops-cybericps-secpre-and-adiot-guildford-uk-september-1418-2020-revised-selected-papers-3030643298-9783030643294.html
Multi-Vector AI Jailbreak: Simulation Protocols to Obfuscated Surveillance Systems, accessed April 8, 2026, https://www.lumenova.ai/ai-experiments/multi-vector-ai-jailbreak-simulation-protocols/
Ransomware and Artificial Intelligence: A Comprehensive Systematic Review of Reviews - arXiv, accessed April 8, 2026, https://arxiv.org/pdf/2603.13734
What chunking strategies work best for document indexing? - Milvus, accessed April 8, 2026, https://milvus.io/ai-quick-reference/what-chunking-strategies-work-best-for-document-indexing
plantuml-parser - NPM, accessed April 8, 2026, https://www.npmjs.com/package/plantuml-parser
Generate Plantuml · Actions · GitHub Marketplace, accessed April 8, 2026, https://github.com/marketplace/actions/generate-plantuml
Display JSON Data - PlantUML, accessed April 8, 2026, https://plantuml.com/json
Recent changes - PlantUML, accessed April 8, 2026, https://plantuml.com/changes
py2puml · PyPI, accessed April 8, 2026, https://pypi.org/project/py2puml/
VS Code API | Visual Studio Code Extension API, accessed April 8, 2026, https://code.visualstudio.com/api/references/vscode-api
accessed April 8, 2026, https://raw.githubusercontent.com/theia-ide/theia/master/packages/plugin/src/theia.d.ts
GitHub - tennashi/lsp_spec_ja: LSP 仕様の日本語訳, accessed April 8, 2026, https://github.com/tennashi/lsp_spec_ja
PlantUML - Visual Studio Marketplace, accessed April 8, 2026, https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml
vscode-plantuml/package.json at master - GitHub, accessed April 8, 2026, https://github.com/qjebbs/vscode-plantuml/blob/master/package.json
Previews shows "No valid diagram found here!" all the time (startup issue) #140 - GitHub, accessed April 8, 2026, https://github.com/qjebbs/vscode-plantuml/issues/140
Add document symbol hierarchy on a vscode extension - Stack Overflow, accessed April 8, 2026, https://stackoverflow.com/questions/64304186/add-document-symbol-hierarchy-on-a-vscode-extension
Use tools with agents - Visual Studio Code, accessed April 8, 2026, https://code.visualstudio.com/docs/copilot/agents/agent-tools
Language Server Protocol: Get Symbol Information of inner functions/classes, accessed April 8, 2026, https://stackoverflow.com/questions/66084817/language-server-protocol-get-symbol-information-of-inner-functions-classes
Writing the Grammar - Tree-sitter, accessed April 8, 2026, https://tree-sitter.github.io/tree-sitter/creating-parsers/3-writing-the-grammar.html
Understanding Tree-sitter Predicates and Directives | by Lince Mathew - Medium, accessed April 8, 2026, https://medium.com/@linz07m/understanding-tree-sitter-predicates-and-directives-9c27ac62ecfe
Tree-sitter Language Bundle for Emacs - GitHub, accessed April 8, 2026, https://github.com/emacs-tree-sitter/tree-sitter-langs
lyndsysimon/tree-sitter-plantuml - GitHub, accessed April 8, 2026, https://github.com/lyndsysimon/tree-sitter-plantuml
cathaysia/tree-sitter-plantuml: [WIP] - GitHub, accessed April 8, 2026, https://github.com/cathaysia/tree-sitter-plantuml
Tree-sitter Grammars - GitHub, accessed April 8, 2026, https://github.com/tree-sitter-grammars
[FEATURE]: Support custom tree-sitter parsers via config for custom languages · Issue #18587 · anomalyco/opencode - GitHub, accessed April 8, 2026, https://github.com/anomalyco/opencode/issues/18587
How to actually include modules for custom grammars? #885 - GitHub, accessed April 8, 2026, https://github.com/nvim-treesitter/nvim-treesitter/discussions/885
infobip/plantuml-mcp-server - GitHub, accessed April 8, 2026, https://github.com/infobip/plantuml-mcp-server
@brainstack/plantuml-mcp - npm, accessed April 8, 2026, https://www.npmjs.com/package/@brainstack/plantuml-mcp
PlantUML MCP Server - LobeHub, accessed April 8, 2026, https://lobehub.com/mcp/junqing258-plantuml-mcp
junqing258/plantuml-mcp - GitHub, accessed April 8, 2026, https://github.com/junqing258/plantuml-mcp
Claude Opus 4.6 System Card - Anthropic, accessed April 8, 2026, https://www-cdn.anthropic.com/14e4fb01875d2a69f646fa5e574dea2b1c0ff7b5.pdf
Claude Opus 4.6 - AI Model Catalog | Microsoft Foundry Models, accessed April 8, 2026, https://ai.azure.com/catalog/models/claude-opus-4-6
Claude Opus 4.6 - Anthropic, accessed April 8, 2026, https://www.anthropic.com/claude/opus
Benchmarking and Mechanistic Analysis of Vision-Language Models for Cross-Depiction Assembly Instruction Alignment - arXiv, accessed April 8, 2026, https://arxiv.org/html/2604.00913v1
Architectural Advances and Performance Benchmarks of Large Language Models in Light of Anthropic's Claude Opus 4.6 - Preprints.org, accessed April 8, 2026, https://www.preprints.org/manuscript/202602.0537
GitHub Copilot deep dive: Model selection, prompting techniques & agent mode - YouTube, accessed April 8, 2026, https://www.youtube.com/watch?v=0Oz-WQi51aU
GitHub Copilot for Diagrams, Humans for Architectural Decisions 🗺️ · community · Discussion #191247, accessed April 8, 2026, https://github.com/orgs/community/discussions/191247
PlantUML vs Mermaid? : r/ExperiencedDevs - Reddit, accessed April 8, 2026, https://www.reddit.com/r/ExperiencedDevs/comments/1k7ki6k/plantuml_vs_mermaid/
mermaid vs plantuml (and integration in github) · mermaid-js · Discussion #4204, accessed April 8, 2026, https://github.com/orgs/mermaid-js/discussions/4204
UML in the Age of AI: Why Modeling Matters More Than Ever | by Jeremy JEANNE - Medium, accessed April 8, 2026, https://medium.com/@jyjeanne/uml-in-the-age-of-ai-why-modeling-matters-more-than-ever-f50c7e41eb08
Home | D2 Documentation, accessed April 8, 2026, https://d2lang.com/
Overview | D2 Documentation, accessed April 8, 2026, https://d2lang.com/tour/extensions/
ravsii/tree-sitter-d2 - GitHub, accessed April 8, 2026, https://github.com/ravsii/tree-sitter-d2
Structurizr, accessed April 8, 2026, https://structurizr.com/dsl
AI | Structurizr, accessed April 8, 2026, https://docs.structurizr.com/ai
gjalla vs Structurizr: Which Architecture Tool Fits Your Team?, accessed April 8, 2026, https://gjalla.io/blog/blog/gjalla-vs-structurizr/
4. Create with DSL, export to PlantUML/Mermaid - Structurizr, accessed April 8, 2026, https://docs.structurizr.com/getting-started/export-diagrams-as-code
