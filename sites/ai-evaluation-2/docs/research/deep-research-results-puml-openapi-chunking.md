# Deep Research Results: PlantUML and OpenAPI Chunking and Context Injection

<!-- Paste deep research results below this line -->
Architectural Integration Strategies for Copilot: Optimizing OpenAPI and PlantUML Retrieval Context
Executive Summary
The orchestration of Large Language Models (LLMs) within enterprise architecture workspaces demands precise context retrieval, particularly for structured specifications and visual diagramming languages. As organizations transition toward AI-assisted solution design, tools like GitHub Copilot are frequently deployed to analyze complex system architectures. However, an exhaustive analysis of GitHub Copilot's indexing capabilities reveals significant limitations in its native handling of multi-file OpenAPI YAML specifications and PlantUML (.puml) diagrams. When presented with fragmented OpenAPI contracts or opaque diagrammatic domain-specific languages (DSLs), the underlying retrieval mechanisms often sever critical contextual links, prompting the LLM to hallucinate architectural structures.
The central inquiry of this research is whether Model Context Protocol (MCP) servers represent the sole viable approach for resolving this context fragmentation. The evidence demonstrates conclusively that they are not. Highly effective, zero-infrastructure alternatives exist and can be deployed immediately to rectify Copilot's indexing behaviors. For OpenAPI, the implementation of build-time specification flattening via CLI bundling, combined with path-specific instruction files, provides near-perfect retrieval quality without the operational overhead of maintaining an MCP server infrastructure. For PlantUML, leveraging Continuous Integration (CI) pipelines to extract diagram definitions into companion Markdown summaries completely circumvents Copilot's lack of native semantic parsing for .puml files. While MCP servers offer dynamic, tool-based interactions and represent the most robust long-term architecture for specialized tool integration, configuration-based workarounds and file decomposition strategies present immediate, highly effective solutions with minimal adoption friction. This report details the precise mechanisms of Copilot's native parsing, evaluates non-MCP and MCP-based strategies, and provides a comprehensive ranking of all available optimization paradigms.
1. Native Copilot Behavior for OpenAPI YAML
To accurately engineer context injection strategies for GitHub Copilot, it is first necessary to dissect its native indexing, parsing, and retrieval mechanisms. Copilot relies heavily on Tree-sitter, a highly optimized parser generator tool and incremental parsing library.1 Tree-sitter builds a concrete syntax tree for a source file and efficiently updates that syntax tree as the source file is edited, operating fast enough to parse on every keystroke.1
Tree-sitter Chunking and YAML Granularity
GitHub Copilot utilizes Tree-sitter grammars to map the structural boundaries of source code across a repository. This structural mapping allows the semantic search index to chunk documents logically—based on code blocks, functions, or objects—rather than splitting them at arbitrary character counts or line breaks.2 When a repository is indexed, Copilot's file system listeners trigger re-indexing of files, computing a vector embedding for each chunk.4 When a developer interacts with Copilot Chat, the system performs a linear scan, computing the dot product similarity between the user's natural language query and each chunk embedding, ranking the results in descending order of similarity.4
For YAML files, Tree-sitter parsing operates at the key-value structural level.5 In the context of an OpenAPI specification, the parser recognizes document-level boundaries, systematically mapping top-level keys such as paths, components, schemas, and security. Copilot indexes these blocks as discrete fragments. When a developer queries a specific endpoint, the vector search algorithm retrieves the chunk containing that endpoint and injects it into the LLM context window. However, Tree-sitter's YAML grammar provides purely syntactic, not semantic, comprehension.1 The parser successfully identifies a deeply nested YAML object but lacks the domain-specific logic to interpret an OpenAPI contract.
Root Key Detection and Format Awareness
A critical limitation in Copilot's native behavior is the absence of format-specific detection for OpenAPI. When Copilot ingests a YAML file, it does not treat files possessing an openapi: 3.0.0 or swagger: "2.0" root key differently from generic configuration YAML files. There is no schema-aware indexing triggered by this root key. The Linguist library, which underlies much of GitHub's language detection, categorizes the file simply as YAML.6 Consequently, Copilot does not inherently apply OpenAPI-specific reasoning rules, such as understanding the implicit relationship between an HTTP method defined under a path and the corresponding response schema defined in a separate components block. The retrieval engine views the specification purely as a collection of generic YAML nodes, leading to fragmented context when related nodes are located in different chunks or different files entirely.
The Fragmentation of $ref Pointers and Contextual Severance
The most severe degradation in LLM reasoning occurs due to Copilot's inability to resolve JSON Reference ($ref) pointers across a multi-file architecture.7 Modern enterprise architecture teams frequently decompose monolithic OpenAPI specifications into highly modular structures, resulting in dozens of discrete .yaml files (e.g., separating endpoint definitions from shared component schemas).
When Copilot's vector search retrieves a chunk containing an endpoint definition, it captures the literal string value of the reference (for example, $ref: '../common/schemas/ErrorResponse.yaml'). The native semantic indexing mechanism does not execute active file traversal to fetch the contents of the target path.7 The $ref pointer acts as a dead end. Because the endpoint chunk is severed from its referenced schema, the LLM is supplied with an incomplete graph. Faced with a missing schema definition for the ErrorResponse, the LLM will rely on its pre-training data to probabilistically generate the structure, leading to severe architectural hallucinations where the AI invents request and response payloads that do not match the actual system contract. This contextual severance fundamentally cripples Copilot's utility for multi-file OpenAPI workspaces.
File Extensions, AST Parsing, and the YAML versus JSON Paradigm
The file extension applied to the specification—whether .yaml, .yml, or .json—dictates which specific Tree-sitter grammar Copilot invokes during the indexing phase. While .yaml and .yml are parsed identically, formatting an OpenAPI specification as .json introduces a subtle shift in parsing dynamics.
Tree-sitter's JSON parser is historically one of its most widely utilized and heavily optimized grammars, designed to handle deeply nested Abstract Syntax Trees (ASTs) with extreme precision.1 When an OpenAPI specification is stored as JSON, the chunking mechanism may demonstrate slightly improved boundary detection for massive, deeply nested objects, ensuring that a complex schema is indexed as a single, cohesive chunk rather than being improperly fragmented. However, this parsing optimization does not address the fundamental architectural challenge: the $ref severance issue. Transitioning from YAML to JSON offers marginal improvements in structural chunking within a single file but entirely fails to bridge the cross-file contextual divide.9 The LLM remains blind to external file references, rendering the JSON conversion an inadequate solution for multi-file specifications.
2. Native Copilot Behavior for PlantUML (.puml)
PlantUML files represent a highly unique challenge for code-oriented LLM assistants. While PlantUML utilizes a formal domain-specific language (DSL) to define architecture, Copilot's ability to natively parse, index, and interpret this syntax is profoundly constrained, leading to substantial degradation in retrieval quality for visual architecture files.
Tree-sitter Grammar Support and Parsing Fallbacks
Currently, there is no official Tree-sitter grammar for PlantUML included in the core language suite supported by GitHub Copilot.1 The official Tree-sitter repository prioritizes mainstream programming languages such as C++, Rust, Go, Python, and JavaScript.10 Although the open-source community has developed specialized grammars for PlantUML—most notably the lyndsysimon/tree-sitter-plantuml repository and the plantuml/language-grammar project intended for IDE integration and GitHub Linguist support 11—these external grammars have not been integrated into the native Copilot semantic indexing engine.
Consequently, Copilot cannot parse .puml files into a concrete syntax tree. It cannot distinguish between a class definition, a state transition, or a sequence arrow at the programmatic level. Instead, the indexing engine falls back to treating the .puml file as raw, unstructured text. Copilot generates vector embeddings for these files based on arbitrary character windows or line counts rather than structural boundaries.4
Syntax Recognition, Boundaries, and Opaqueness
Because PlantUML files are treated as raw text, Copilot relies entirely on generic lexical and vector-based text retrieval. The system processes the text linearly and does not possess intrinsic semantic awareness of fundamental PlantUML boundaries, such as the @startuml and @enduml declarations. Similarly, it does not inherently understand participant declarations, actors, or relationship arrows (->, -->, <|--) as architectural constructs. It views them merely as sequences of ASCII characters.
This parsing limitation becomes acutely problematic when architecture teams utilize C4 model abstractions. The C4 model for software architecture is frequently implemented in PlantUML via standard library macros (e.g., Container, System_Ext, Rel, Person) which are imported using !include directives.14 When Copilot scans a .puml file containing these C4 macros, it perceives the macros as opaque alphanumeric strings. It does not resolve the !include directive, nor does it understand the underlying definition of a Rel macro.
For instance, if a diagram dictates Rel(svc_check_in, svc_reservations, "Calls", "HTTPS"), Copilot does not parse this as an edge between two discrete system nodes. If an engineer prompts Copilot with the question, "Which services does svc-check-in call?", Copilot must rely entirely on a dot-product similarity search for the tokens "svc-check-in" and "call".4 If the raw text is retrieved successfully, the LLM may deduce the relationship through basic natural language pattern matching. However, the system cannot traverse the !include path to understand the properties of the imported elements, nor can it reliably reconstruct the holistic graph topology from raw macros.
Naming Conventions and Text Reasoning
The choice of file extension (.puml, .plantuml, .pu, or .wsd) does not fundamentally alter the underlying parsing mechanics within the Copilot ecosystem.15 All these extensions are recognized as PlantUML by the underlying Linguist heuristics for the purpose of basic syntax highlighting in the GitHub UI, but for semantic search, they are all processed through the same generic text embedding pipeline.16
The LLM's capacity to deduce architectural structure from raw PlantUML text is entirely dependent on the proximity of the tokens within the text chunk that happens to be retrieved. It operates via substring pattern matching rather than deterministic graph-based semantic analysis. Therefore, complex nested relationships, hidden dependencies, or sequence flows that span hundreds of lines will routinely exceed the limits of the retrieved text chunk, resulting in incomplete or entirely hallucinated architectural representations within the Copilot Chat interface. Copilot cannot "reason" about the diagram; it can only regurgitate and probabilistically complete the textual patterns it retrieves.
3. Non-MCP Workarounds for OpenAPI
Before introducing the operational complexity and maintenance overhead of a Model Context Protocol server, enterprise architecture teams can implement a series of high-impact, zero-infrastructure configurations. These non-MCP workarounds dramatically optimize Copilot's comprehension of OpenAPI specifications by aligning the codebase structure with the LLM's optimal retrieval patterns.
Build-Time File Flattening (The Optimal Approach)
The most definitive non-MCP solution to the $ref pointer fragmentation issue is specification flattening, frequently referred to as bundling or dereferencing. While file decomposition (splitting a monolithic OpenAPI spec into per-endpoint files) is highly advantageous for human developers and Git conflict mitigation, it is actively detrimental to LLM retrieval algorithms. To resolve this tension, teams must decouple the authoring format from the LLM ingestion format.
By utilizing established CLI tools such as swagger-cli bundle or oapi-codegen preprocessors, a monolithic, fully dereferenced OpenAPI specification can be generated automatically.18 The process involves executing a bundling command (e.g., swagger-cli bundle -o api-bundled.yaml --dereference -t yaml api-main.yaml).18 This tool traverses the primary specification, follows every $ref pointer across the file system, and replaces the pointer with the literal YAML object it references, outputting a massive, unified document.21
When this command is incorporated into a local build script or a Continuous Integration (CI) pre-commit hook, the repository will contain both the modular files for human engineering and the flattened artifact for machine ingestion. When Copilot indexes the workspace, the bundled file is embedded. Consequently, when the LLM retrieves an endpoint chunk from the bundled file, the complete request and response schemas are guaranteed to be physically adjacent within the same document context. This approach entirely eliminates LLM hallucination of payloads because the contextual severance has been repaired at the source code level prior to indexing.
Scoped Instruction Files (.instructions.md)
GitHub Copilot supports granular, persistent behavioral modifications via custom instruction files.22 By placing a specific .instructions.md file within the .github/instructions/ directory and utilizing the applyTo YAML frontmatter property, architects can enforce rigid retrieval and generation rules specifically for OpenAPI files.24
An effective .instructions.md tailored for OpenAPI architecture might utilize the following configuration:

YAML


---
applyTo: "**/*.yaml"
---
# OpenAPI Architecture Directives
You are an enterprise API architect. When analyzing these OpenAPI specifications, you must recognize that they represent a modular, multi-file architecture. 
1. You must rigorously attempt to resolve all `$ref` pointers. 
2. If an endpoint references a schema in another file, you must actively utilize your workspace file-reading capabilities to open the referenced file.
3. Inspect the exact schema definition in the referenced file and use those precise properties in your code generation. 
4. Never fabricate or hallucinate schema properties. If you cannot find the schema, state that it is missing.


While this approach explicitly commands the LLM to traverse references, its effectiveness is strictly bound by the agent's tool-use compliance and the context window's capacity. In complex, multi-turn interactions, the LLM may still fail to execute the secondary file read operation, making this a secondary enhancement mechanism rather than a guaranteed standalone cure.26 However, because it requires zero infrastructure and minimal effort, it should be deployed universally.
Companion Markdown Summaries
LLMs possess an exceptional, native aptitude for parsing and reasoning over natural language documents. Generating a companion Markdown file—such as a SUMMARY.md or README.md—alongside the OpenAPI specifications provides a highly indexable semantic map of the API.27 This document should detail the API contracts, list all endpoints, and explicitly describe the core schemas and cross-references in plain English.
Because Copilot indexes Markdown with near-perfect semantic accuracy, the vector search will prioritize retrieving this plain-language summary when a developer asks architectural questions.28 The summary acts as a translation layer, supplying the LLM with the necessary overarching context without forcing it to parse the fragmented, multi-file YAML ASTs directly. While highly effective for retrieval quality, this approach incurs a high maintenance burden if the documentation is not strictly synchronized with the underlying API specifications.27
VS Code LSP-to-MCP Bridges and Extension Integration
A highly advanced, infrastructure-free approach involves leveraging existing Visual Studio Code extensions and their native Language Server Protocol (LSP) capabilities. Certain VS Code extensions, such as Stoplight Spectral (vscode-spectral), are specifically designed to provide linting, validation, and AST parsing for OpenAPI v2 and v3 documents.29
Historically, Copilot could not directly access the rich, parsed AST data generated by these external extensions. However, community tools such as the lsp-mcp-bridge extension by Sehej Jain have emerged to bridge this gap.31 This extension intercepts the intelligence generated by standard VS Code language servers and exposes it directly to Copilot.31 When the LSP-MCP bridge is active alongside an OpenAPI language server, Copilot gains the ability to execute tools like lsp_definition, lsp_references, and lsp_workspace_symbols.31 The LLM can dynamically request definitions across files, effectively outsourcing the cross-file $ref resolution to Spectral's dedicated OpenAPI parser rather than relying on its own flawed vector search. This transforms a standard VS Code extension into an interactive context provider.
AGENTS.md Routing and SKILL.md Frameworks
The deployment of an AGENTS.md file in the root of the API specifications directory provides a predictable, standardized anchor for the Copilot coding agent.33 Adopted by over 60,000 open-source projects, AGENTS.md functions as an instruction manual specifically for the LLM, declaring the exact architectural paradigms, build steps, and conventions in use.34
However, reliance on manual context files must be carefully managed. An ETH Zurich study highlighted that LLM-generated context files can actually reduce task success rates by approximately 3% due to token overhead and increased reasoning complexity, while highly curated, human-written files provide a marginal 4% performance gain.35 Therefore, the AGENTS.md file must be meticulously curated to prevent token bloat.
To complement AGENTS.md, teams can leverage SKILL.md frameworks. A custom skill—similar to the openapi-to-application-code skill found in the GitHub Awesome Copilot repository—can be created to dictate exactly how the LLM should parse the enterprise's specific OpenAPI directory structure.36 Skills allow the bundling of helper scripts and reference data, which are loaded on-demand.37 This enables the LLM to invoke specific parsing behaviors only when directly interacting with the API specifications, optimizing the context window for other tasks.
4. Non-MCP Workarounds for PlantUML
To overcome the lack of native Tree-sitter parsing and semantic awareness for .puml files, enterprise teams must implement strategies that convert opaque diagrammatic syntax into highly indexable, standard text structures that align with the LLM's core competencies.
CI/CD PlantUML-to-Text Extraction
The most resilient and automated workaround for the PlantUML context deficit is the automated translation of diagram logic into LLM-optimized textual formats. PlantUML inherently supports data export, and external utilities can parse the underlying structure.38 Integrating tools like mkdocs-puml, custom Python parsers, or the plantuml.jar command-line interface into the CI/CD pipeline or as local pre-commit hooks ensures that the repository always contains an LLM-readable analog of the visual diagram.39
A CI script can systematically parse the .puml files, isolate the participant, actor, component, and relationship lines, and dynamically generate a structured Markdown file.41 For example, the script could generate a diagram-summary.md artifact containing the following structured data:
Diagram Target: Checkout Orchestration Sequence
Identified Participants: svc-cart, svc-payment, db-orders
Execution Flow: svc-cart invokes svc-payment.process(), which subsequently persists to db-orders and returns an HTTP 200 success code.
Because Copilot indexes Markdown files with near-perfect semantic accuracy and robust chunking boundaries, this automatically generated companion file acts as the ultimate architectural source of truth for the LLM.28 It completely bypasses the need for the LLM to parse the raw .puml text or decipher C4 macros, allowing Copilot to accurately answer complex architectural queries based entirely on the extracted Markdown summary.
Structured Embedded Comments
To optimize lexical retrieval within the .puml files themselves, architects should adopt a strict convention of including structured, natural-language comment blocks at the apex of every diagram file.42

Code snippet


' @architecture-summary
' This sequence diagram illustrates the user check-in orchestration process.
' Primary actors: MobileClient, WebFrontend.
' Core microservices invoked: svc-check-in, svc-reservations.
' Flow: The client authenticates, calls check-in, which subsequently updates the reservation state.


By embedding plain-language summaries directly into the file, the vector embeddings generated by Copilot will capture the semantic intent and architectural reality of the diagram.4 When an engineer queries the chat interface about the check-in architecture, the dot-product similarity search will effortlessly locate this comment block, supplying the LLM with a highly accurate summary even if the subsequent PlantUML syntax is too complex or opaque for the agent to parse.
VS Code PlantUML Extensions
While native VS Code extensions such as qjebbs/vscode-plantuml provide comprehensive local rendering, diagram previews, and syntax highlighting, they do not inherently expose their internal Abstract Syntax Trees to GitHub Copilot's context window.16 However, if these extensions are utilized in tandem with the previously discussed lsp-mcp-bridge 31, and if the extension implements standard LSP definitions for its symbols, Copilot may gain peripheral access to the workspace symbols defined within the diagrams. Regardless of LSP bridging, simply having the extension active and the .puml file open in the editor significantly increases the file's weighting in Copilot's immediate context window, slightly improving the probability of successful substring matching.
The PlantUML-ASCII SKILL.md Framework
The open-source community has developed specialized SKILL.md frameworks specifically designed to augment Copilot's capacity to handle diagrammatic languages. A premier example is the plantuml-ascii skill located within the GitHub Awesome Copilot repository.37
This skill acts as an expert instruction set, teaching the agent how to read, interpret, and generate text-based diagrams. By downloading this skill into the repository's .github/skills/ directory, Copilot is granted explicit, progressive disclosure rules regarding PlantUML syntax.37 The skill defines allowed tools (such as Bash, Write, and Read capabilities) and instructs the agent on converting PlantUML diagrams into ASCII art or processing markdown files containing embedded .puml blocks.44
Furthermore, skills like the architecture-blueprint-generator can be utilized to automatically detect architectural patterns and maintain consistency across the codebase.46 When invoked, these skills utilize a defined operational loop (often referred to as a "Plan-Do-Analyze" or PDA loop) 47, instructing the LLM to selectively read specific reference documentation, parse the necessary codebase files, and output a validated architectural response. While the LLM may still struggle with highly complex graphical topologies, the implementation of these specialized skills significantly elevates its baseline comprehension of PlantUML syntax and C4 modeling abstractions.48
5. MCP Server Landscape for OpenAPI and PlantUML
While the aforementioned non-MCP strategies offer immediate and highly effective remediation, the Model Context Protocol (MCP) standardizes how AI agents interface with external data streams, APIs, and complex file systems. Deploying an MCP server represents the most robust, dynamic, and architecturally sound solution for long-term tool integration, albeit at the cost of operational infrastructure and maintenance overhead.
OpenAPI MCP Servers
The ecosystem surrounding OpenAPI MCP servers is rapidly maturing, driven by the critical enterprise need to seamlessly integrate LLMs with complex, multi-file REST APIs.
AWS Labs OpenAPI MCP Server: This official, open-source server is explicitly designed to dynamically generate MCP tools and resources directly from OpenAPI specifications.50 It permits the LLM to interact with the API documentation as if it were a live, queryable database. When deployed, the agent can call tools to dynamically fetch schemas and endpoint definitions. This entirely resolves the $ref fragmentation issue, as the server handles the dereferencing natively before transmitting the payload to the LLM context window.
Open-WebUI Bridges (mcpo): The open-source community provides sophisticated transport bridges designed to convert existing OpenAPI specifications into MCP tool servers on the fly.52 Tools such as openapi-mcp-server act as automatic translators, exposing RESTful endpoints and schema definitions directly to the Copilot agent's context window without requiring bespoke integration logic.
Specbridge: This utility is explicitly engineered to convert complex OpenAPI specifications into callable MCP tools, dramatically streamlining the ingestion of multi-file enterprise APIs.53 It ensures that the LLM interacts with a standardized, unified representation of the API contract.
PlantUML MCP Servers
The landscape for PlantUML MCP servers is highly active and directly addresses the syntax parsing void present in Copilot's native architecture.
Infobip PlantUML MCP Server: This comprehensive server exposes explicit tools for advanced diagram management.54 It provides generate_plantuml_diagram, encode_plantuml, and decode_plantuml tools. Crucially, it natively supports advanced PlantUML features, including external libraries and !include directives, making it exceptionally suited for resolving the opaqueness of C4 architectures.54 It also features robust error handling, supplying the LLM with structured syntax validation errors to enable autonomous self-correction workflows during diagram generation.55
junqing258 / plantuml-mcp: Another robust implementation that validates PlantUML syntax, extracts source code directly from PNG/SVG metadata, and generates diagrams.56 This offers the LLM a rich set of interactive capabilities, transforming opaque image assets back into parseable code.
kwhrkzk / plantuml-validator-mcp-server: A specialized server, officially certified by MCPHub, dedicated exclusively to validating PlantUML code syntax.57 This is highly useful for ensuring LLM-generated diagrams are syntactically sound before committing them to the repository.
Generic Diagram Servers and Custom FastMCP Feasibility
Beyond PlantUML-specific solutions, generic diagram servers such as the FlowZap MCP Server demonstrate the viability of exposing domain-specific diagramming languages to AI agents.58 FlowZap converts text-based code into visual workflows and exposes its syntax via a flowzap_get_syntax tool, allowing the LLM to learn the language on demand.58
For enterprise teams with unique architectural requirements, developing a custom MCP server utilizing frameworks like Python's FastMCP is highly feasible and requires relatively minimal engineering effort. A custom server could wrap the official Java plantuml.jar or Python's plantuml library, exposing a single, highly specialized tool to the LLM, such as parse_architecture_graph(file_path). The underlying Python script would read the .puml file, resolve local !include macros recursively, and return a structured JSON representation of the nodes and edges directly to the LLM. While this requires running a local or containerized Python daemon, it offers absolute control over how internal C4 macros are interpreted and transmitted to Copilot.
6. Out-of-the-Box Solutions
Before implementing custom CI scripts or standing up permanent MCP server infrastructure, enterprise architecture teams should verify whether any zero-configuration, out-of-the-box mechanisms native to the GitHub ecosystem can satisfy their contextual requirements.
GitHub Copilot Enterprise Knowledge Bases
For organizations subscribed to the GitHub Copilot Enterprise tier, the "Knowledge Bases" feature offers a powerful, out-of-the-box semantic enhancement.27 Knowledge bases allow administrators to aggregate specific, high-value repositories—such as architecture documentation, Markdown wikis, and structured text—into a unified, highly indexed vector database.28
While Copilot Enterprise Knowledge Bases do not execute real-time code logic or parse complex non-standard file types, they expertly index Markdown, text, YAML, and JSON.28 By structuring architectural guidelines, API contracts, and system topologies clearly within these supported formats and attaching the Knowledge Base to the Copilot Chat session, the LLM gains immediate, deep context regarding the system's design principles without requiring local workspace indexing. It is crucial to note, however, that while .yaml is fully supported, raw .puml files are not explicitly prioritized for semantic extraction, reinforcing the necessity for Markdown companion files.60
Copilot Chat @workspace Enhancements
Recent updates to the Visual Studio Code Copilot Chat extension have significantly refined the @workspace context provider.61 The indexing algorithm now performs more aggressive similarity scoring on locally cached files. Ensuring that all 19 OpenAPI YAML files and associated C4 diagrams are actively loaded in the IDE's file explorer (or simply open in background tabs) temporarily elevates their weighting in the LLM's context window.62 Furthermore, the aforementioned implementation of .github/copilot-instructions.md (repository-wide instructions) requires zero infrastructure. Simply dropping a Markdown file detailing API naming conventions, the use of C4 abstraction layers, and the expectation for thorough architectural analysis immediately alters the system prompt fed to the LLM upon every chat initialization.22
7. Comparative Analysis
To provide a definitive decision matrix for enterprise architecture teams, all discovered approaches have been ranked based on Implementation Effort, Infrastructure Requirements, Maintenance Overhead, Retrieval Quality Improvement, and Team Adoption Friction.
Table 1: OpenAPI Integration Strategies Ranked
Strategy
Effort
Infrastructure
Maintenance
Retrieval Quality Improvement
Adoption Friction
1. CLI Bundling (Flattening)
Low (1-2 hours)
None (Local CLI/CI hook)
Low
Critical/High - Entirely solves $ref hallucination by ensuring physical adjacency of endpoints and schemas.
Zero (runs silently in the background)
2. .instructions.md (applyTo)
Very Low (<1 hour)
None (Static File)
Low
Moderate - Prompts LLM to actively traverse references, but remains reliant on non-deterministic agent compliance.
Zero
3. AWS Labs OpenAPI MCP
Medium (1-2 days)
Yes (Local Server/Docker)
Medium
High - Enables dynamic schema fetching and strict, deterministic resolution.
Low (transparent to end-users)
4. lsp-mcp-bridge + Spectral
Low (Plugin Install)
None (VS Code Extension)
Low
High - Outsources deep AST traversal to the Language Server Protocol.
Low (requires explicit extension installation)
5. Companion MD Summaries
High (Ongoing)
None (Static Files)
High
High - Perfect natural language retrieval affinity.
High (requires manual writing and synchronization)
6. AGENTS.md Routing
Very Low (<1 hour)
None (Static File)
Low
Low - Improves general repository focus but structurally fails to solve $ref breakage.
Zero

Analysis: CLI Bundling represents the indisputable optimal strategy for OpenAPI. It perfectly aligns the codebase with the LLM's chunking behavior by presenting a unified document, requiring no external servers or complex prompting. While the AWS Labs MCP server is highly capable, the infrastructure overhead makes it a secondary choice compared to the simplicity of flattening.
Table 2: PlantUML Integration Strategies Ranked
Strategy
Effort
Infrastructure
Maintenance
Retrieval Quality Improvement
Adoption Friction
1. CI/CD Extracted Markdown
Medium (1-3 days)
None (CI Script)
Low
Critical/High - Transforms opaque, unparseable DSL syntax into native, highly-indexed LLM text.
Zero (automated via pipeline)
2. Structured File Comments
Low (Convention)
None (Static File)
Medium
High - Guarantees a high semantic vector hit rate by embedding natural language summaries directly in the file.
Medium (requires enforcing team discipline)
3. Infobip PlantUML MCP
Medium (1-2 days)
Yes (Local Server/Docker)
Medium
Critical/High - Provides full !include macro support, syntax validation, and visual rendering.
Low
4. plantuml-ascii SKILL.md
Low (File Copy)
None (Static File)
Low
Moderate - Improves base syntax comprehension, but the LLM may still struggle with complex graphical topologies.
Low
5. Custom FastMCP Server
High (1-2 weeks)
Yes (Local Server)
High
High - Allows absolute custom logic for interpreting proprietary C4 macros.
Medium

Analysis: PlantUML's lack of native AST support necessitates translation. The CI/CD Extracted Markdown approach is the most resilient, leveraging the LLM's inherent strength in parsing structured text. The Infobip MCP server is an exceptionally strong alternative for teams willing to accept the infrastructure requirements, offering deep integration with C4 macros and !include directives.
8. Recommended Strategy
Based on this exhaustive analysis of Copilot's indexing behaviors, AST generation, and available ecosystem tools, it is definitively established that MCP is not the only viable approach. In fact, for immediate operational impact with minimal architectural overhead, configuration-based and workflow-based alternatives prove vastly superior. The recommended dual-pronged strategy for the enterprise architecture workspace is as follows:
For OpenAPI Specifications: Do not deploy an MCP server initially. Instead, implement Build-Time File Flattening utilizing tools such as swagger-cli bundle.18 Integrate this command into the CI pipeline or a standard pre-commit hook to silently generate a compiled openapi-bundled.yaml file. Copilot's Tree-sitter mechanism will seamlessly index this flattened artifact, guaranteeing that the LLM has immediate, unfragmented access to all $ref components within a single document context. Supplement this flattening process by placing a scoped .instructions.md file using applyTo: "**/*.yaml" to explicitly govern how the LLM generates and validates API code.22
For PlantUML Diagrams: Implement CI/CD PlantUML-to-Text Extraction. Relying on the LLM to parse raw .puml syntax—especially when obscured by nested C4 !include macros—is computationally inefficient and highly prone to hallucination. Develop a lightweight script (e.g., utilizing Python or mkdocs-puml) that parses the diagram files upon commit and generates companion Markdown summaries outlining the nodes, boundaries, and relationships.39 Copilot will ingest these Markdown summaries with near-perfect semantic accuracy, completely circumventing the absence of a native Tree-sitter grammar for PlantUML. To empower developers with diagram generation and syntax validation capabilities directly within the IDE, evaluate the Infobip PlantUML MCP Server as a secondary phase.54
9. Open Questions
While the recommended strategy relies on the proven, documented behaviors of the GitHub Copilot ecosystem, several variables require empirical testing within the specific enterprise environment to ensure optimal deployment:
Context Window Token Constraints and Degradation: When swagger-cli bundle flattens 19 OpenAPI services into a single monolithic file, will the resulting artifact exceed the active token limit of the Copilot chat context window? If the bundled file surpasses the optimal token threshold (often leading to the "lost-in-the-middle" recall degradation phenomenon), the LLM may begin ignoring critical schema details. Empirical testing must determine if specs should be bundled per-domain rather than globally to maintain high attention fidelity.
LSP-MCP Bridge Stability: The lsp-mcp-bridge extension presents a revolutionary method for exposing the Spectral VS Code extension's AST to Copilot.29 However, as a community-driven open-source tool, its stability, latency overhead, and compatibility with upcoming native Copilot API updates must be rigorously benchmarked in an enterprise sandbox environment before widespread rollout.
Cross-Contamination of Indexed Artifacts: When generating flattened OpenAPI files and companion Markdown summaries alongside the original source code, will Copilot's semantic search return duplicate, conflicting results? The architecture team must test whether adding the original modular files to a .copilotignore file (if supported by the specific Copilot tier) or utilizing strict .instructions.md prompt directives is necessary to force the LLM to read only the optimized, generated artifacts, thereby preventing vector search pollution.
Works cited
Tree-sitter: Introduction, accessed April 8, 2026, https://tree-sitter.github.io/
Indexing repositories for GitHub Copilot, accessed April 8, 2026, https://docs.github.com/copilot/concepts/indexing-repositories-for-copilot-chat
Indexing repositories for GitHub Copilot, accessed April 8, 2026, https://docs.github.com/en/copilot/concepts/context/repository-indexing
How GitHub Copilot Knows Your Code: Inside Its Indexing Magic | by Yasith Rashan, accessed April 8, 2026, https://yasithrashan.medium.com/how-github-copilot-knows-your-code-inside-its-indexing-magic-aba59a0ce0e8
Security overview · tree-sitter-grammars/tree-sitter-yaml · GitHub, accessed April 8, 2026, https://github.com/tree-sitter-grammars/tree-sitter-yaml/security
GitHub language support - GitHub Enterprise Cloud Docs, accessed April 8, 2026, https://docs.github.com/enterprise-cloud@latest/get-started/learning-about-github/github-language-support
smartlyio/oats: typescript from openapi3 spec - GitHub, accessed April 8, 2026, https://github.com/smartlyio/oats
tree-sitter repositories - GitHub, accessed April 8, 2026, https://github.com/orgs/tree-sitter/repositories
Leveraging Large Language Models with Retrieval-Augmented Generation for Automated API Service Composition - OuluREPO, accessed April 8, 2026, https://oulurepo.oulu.fi/bitstream/10024/57261/1/nbnfioulu-202506194778.pdf
tree-sitter/tree-sitter: An incremental parsing system for programming tools - GitHub, accessed April 8, 2026, https://github.com/tree-sitter/tree-sitter
List of parsers · tree-sitter/tree-sitter Wiki - GitHub, accessed April 8, 2026, https://github.com/tree-sitter/tree-sitter/wiki/List-of-parsers
lyndsysimon/tree-sitter-plantuml - GitHub, accessed April 8, 2026, https://github.com/lyndsysimon/tree-sitter-plantuml
Formal grammar definition for the PlantUML language, designed for syntax parsing, validation, and editor integration - GitHub, accessed April 8, 2026, https://github.com/plantuml/language-grammar
GitHub - plantuml-stdlib/C4-PlantUML: C4-PlantUML combines the benefits of PlantUML and the C4 model for providing a simple way of describing and communicate software architectures, accessed April 8, 2026, https://github.com/plantuml-stdlib/C4-PlantUML
GitHub - AlDanial/cloc: cloc counts blank lines, comment lines, and physical lines of source code in many programming languages., accessed April 8, 2026, https://github.com/aldanial/cloc
linguist/vendor/README.md at main - GitHub, accessed April 8, 2026, https://github.com/github-linguist/linguist/blob/main/vendor/README.md
gabeins/zed-plantuml: PlantUML support for Zed - GitHub, accessed April 8, 2026, https://github.com/gabeins/zed-plantuml
AWS CloudFormation | Noise | Page 4, accessed April 8, 2026, https://noise.getoto.net/tag/aws-cloudformation/page/4/
Suggestions for structuring/organisation in larger projects · Issue #249 · oapi-codegen/oapi-codegen - GitHub, accessed April 8, 2026, https://github.com/oapi-codegen/oapi-codegen/issues/249
agno-agi/docs: Docs for Agno: build multi-agent systems that learn. - GitHub, accessed April 8, 2026, https://github.com/agno-agi/docs
Understanding API-First Development - Tanzu - VMware Blogs, accessed April 8, 2026, https://blogs.vmware.com/tanzu/understanding-api-first-development/
Your first custom instructions - GitHub Docs, accessed April 8, 2026, https://docs.github.com/en/copilot/tutorials/customization-library/custom-instructions/your-first-custom-instructions
Use custom instructions in VS Code, accessed April 8, 2026, https://code.visualstudio.com/docs/copilot/customization/custom-instructions
Adding repository custom instructions for GitHub Copilot - GitHub Docs, accessed April 8, 2026, https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot
GitHub Copilot Instructions: Setup Guide - Code To Cloud, accessed April 8, 2026, https://codetocloud.io/blog/github-copilot-instructions
Improving GitHub Copilot Responses by Designing Better Context | by Somnath - Medium, accessed April 8, 2026, https://medium.com/@somnath.2301/improving-github-copilot-responses-by-designing-better-context-604f333e2145
Technical documentation: Best practices for software teams and AI-powered solutions, accessed April 8, 2026, https://xenoss.io/blog/technical-documentation-best-practices-for-software-teams-and-ai-powered-solutions
GitHub Server Knowledge connector overview - Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/microsoft-365/copilot/connectors/github-server-knowledge-overview
stoplightio/vscode-spectral: VS Code extension bringing the awesome Spectral JSON/YAML linter with OpenAPI/AsyncAPI support - GitHub, accessed April 8, 2026, https://github.com/stoplightio/vscode-spectral
GitHub - stoplightio/spectral: A flexible JSON/YAML linter for creating automated style guides, with baked in support for OpenAPI (v3.1, v3.0, and v2.0), Arazzo v1.0, as well as AsyncAPI v2.x., accessed April 8, 2026, https://github.com/stoplightio/spectral
Allow Copilot to browse large Codebases intelligently and efficiently : r/vscode - Reddit, accessed April 8, 2026, https://www.reddit.com/r/vscode/comments/1nb2jjt/allow_copilot_to_browse_large_codebases/
Extension that converts any language server into an MCP for Copilot to use - Reddit, accessed April 8, 2026, https://www.reddit.com/r/GithubCopilot/comments/1nb14vs/extension_that_converts_any_language_server_into/
Custom agents configuration - GitHub Docs, accessed April 8, 2026, https://docs.github.com/en/copilot/reference/custom-agents-configuration
AGENTS.md, accessed April 8, 2026, https://agents.md/
How to Build Your AGENTS.md (2026): The Context File That Makes AI Coding Agents Actually Work | Augment Code, accessed April 8, 2026, https://www.augmentcode.com/guides/how-to-build-agents-md
Creating agent skills for GitHub Copilot CLI, accessed April 8, 2026, https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-skills
awesome-copilot/docs/README.skills.md at main - GitHub, accessed April 8, 2026, https://github.com/github/awesome-copilot/blob/main/docs/README.skills.md
linkml generate - linkml documentation, accessed April 8, 2026, https://linkml.io/linkml/cli/generate.html
GitHub - mkdocs/catalog: :trophy: A list of awesome MkDocs projects and plugins., accessed April 8, 2026, https://github.com/mkdocs/catalog
Quick Start Guide to PlantUML, accessed April 8, 2026, https://plantuml.com/starting
plantuml - Skill | Smithery, accessed April 8, 2026, https://smithery.ai/skills/SpillwaveSolutions/plantuml
Support for yaml references · Issue #683 - GitHub, accessed April 8, 2026, https://github.com/plantuml/plantuml/issues/683
How to edit Markdown + UML in Visual Studio Code - freeCodeCamp, accessed April 8, 2026, https://www.freecodecamp.org/news/inserting-uml-in-markdown-using-vscode/
awesome-copilot/skills/plantuml-ascii/SKILL.md at main - GitHub, accessed April 8, 2026, https://github.com/github/awesome-copilot/blob/main/skills/plantuml-ascii/SKILL.md
GitHub - SpillwaveSolutions/plantuml: A Plantuml Claude Skill that can generate images and help you create Plantuml digrams from source code. It can also extract plantuml diagrams from a markdown file and then generate each of those to images and create a new markdown file with image links to those diagrams., accessed April 8, 2026, https://github.com/SpillwaveSolutions/plantuml
awesome-copilot/skills/architecture-blueprint-generator/SKILL.md at ..., accessed April 8, 2026, https://github.com/github/awesome-copilot/blob/main/skills/architecture-blueprint-generator/SKILL.md
Claude Code Skills Deep Dive Part 1 | by Rick Hightower | Spillwave Solutions - Medium, accessed April 8, 2026, https://medium.com/spillwave-solutions/claude-code-skills-deep-dive-part-1-82b572ad9450
C4Sharp (C4S) is a .net library for building C4 Model diagrams. - GitHub, accessed April 8, 2026, https://github.com/8T4/c4sharp
agent-toolkit/skills/c4-architecture/README.md at main - GitHub, accessed April 8, 2026, https://github.com/softaworks/agent-toolkit/blob/main/skills/c4-architecture/README.md
OpenAPI MCP Server - Open Source at AWS, accessed April 8, 2026, https://awslabs.github.io/mcp/servers/openapi-mcp-server
accessed December 31, 1969, https://awslabs.github.io/mcp/servers/openapi-mcp-server/
open-webui/openapi-servers: OpenAPI Tool Servers - GitHub, accessed April 8, 2026, https://github.com/open-webui/openapi-servers
modelcontextprotocol/servers: Model Context Protocol Servers - GitHub, accessed April 8, 2026, https://github.com/modelcontextprotocol/servers
infobip/plantuml-mcp-server · GitHub - GitHub, accessed April 8, 2026, https://github.com/infobip/plantuml-mcp-server
How I built an open-source PlantUML MCP server without writing a single line of code - Infobip Developers Hub, accessed April 8, 2026, https://www.infobip.com/developers/blog/how-i-built-an-open-source-plantuml-mcp-server-without-writing-a-single-line-of-code
junqing258/plantuml-mcp - GitHub, accessed April 8, 2026, https://github.com/junqing258/plantuml-mcp
kwhrkzk/plantuml-validator-mcp-server - GitHub, accessed April 8, 2026, https://github.com/kwhrkzk/plantuml-validator-mcp-server
FlowZap MCP Server Documentation for AI Agents, accessed April 8, 2026, https://flowzap.xyz/docs/mcp
Knowledge sources summary - Microsoft Copilot Studio, accessed April 8, 2026, https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio
Upload files as a knowledge source - Microsoft Copilot Studio, accessed April 8, 2026, https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-add-file-upload
GitHub Copilot - Arm Learning Paths, accessed April 8, 2026, https://learn.arm.com/install-guides/github-copilot/
Enhance GitHub Copilot to Utilize Context from Multiple Open Windows in VS Code #6792, accessed April 8, 2026, https://github.com/microsoft/vscode-copilot-release/issues/6792
