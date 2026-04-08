# Deep Research Results: Azure AI Search Chunking Mechanics (Pro Mode)

<!-- Paste pro mode deep research results below this line -->


Analytical Evaluation of Azure AI Search Chunking Mechanics for Enterprise Architecture Assets
The architectural evaluation of enterprise repositories requires search and retrieval mechanisms capable of parsing highly structured, hierarchically dependent, and cross-referenced file formats. Traditional retrieval-augmented generation (RAG) models often rely on generic text splitting, such as static token windows or the sliding window approaches employed natively by tools like GitHub Copilot. Copilot utilizes a hybrid approach, combining Tree-sitter Abstract Syntax Tree (AST) parsing for supported programming languages with a generic 60-line sliding window fallback for unsupported plaintext or markup files, scored using Jaccard similarity and dense embeddings.1 The Jaccard similarity coefficient, expressed mathematically as , provides a purely lexical measure of overlap between the query and the chunk, which is then fused with semantic vectors. While sliding windows offer basic contextual proximity, they frequently sever semantic relationships in structured formats like OpenAPI specifications, Markdown Architecture Decision Records (MADRs), and nested configuration files because the arbitrary 60-line boundary lacks structural awareness.
This report provides an exhaustive technical analysis of Azure AI Search and Foundry IQ capabilities compared to generalized code-aware and sliding-window retrieval models. The analysis explores native document cracking, integrated vectorization pipelines, custom skillset extensibility, retrieval quality, and the cost profile associated with indexing a complex enterprise architecture workspace containing diverse file formats.
Azure AI Search Document Cracking and Built-In Chunking Strategies
The foundational layer of any enterprise retrieval system is its ability to ingest raw storage assets, crack the file envelopes, extract the underlying text, and partition that text into semantically viable chunks that conform to the context windows of downstream large language models (LLMs).
Native Document Cracking Capabilities
The Azure AI Search ingestion pipeline relies on built-in blob indexers and the DocumentExtractionSkill to execute document cracking.3 The indexer natively supports an extensive array of file formats, including Microsoft Office formats (DOCX, XLSX, PPTX), PDF, HTML, JSON, CSV, XML, plain text, and Markdown.3
When processing enterprise architecture assets, the native document cracker exhibits distinctly variable behaviors dictated by the file extension and parsing configuration. Markdown files benefit from native structural parsing via the markdownParsingSubmode.5 However, formats such as YAML (which encompasses OpenAPI and AsyncAPI specifications), PlantUML (.puml), and programming source code (Java, TypeScript, Python) do not possess native format-aware crackers in the default indexing tier.3 Consequently, Azure AI Search treats these assets entirely as plain text files.3 When a structured file is relegated to plain text processing, its inherent hierarchical relationships—such as YAML key parent-child dependencies or AST structures in source code—are flattened into continuous, undifferentiated character strings prior to chunking.
Recently, the ecosystem introduced the Azure Content Understanding skill as a sophisticated alternative to standard document cracking.6 This skill provides advanced document parsing, significantly improving the extraction of cross-page tables and rendering the structural output in Markdown format.6 While this represents a leap forward for PDFs and Office documents, its utility for natively structured code or markup files like YAML remains identical to plain text processing, as the underlying syntax is not algorithmically parsed into discrete objects.
Built-In Chunking Configuration and the Text Split Skill
Once document cracking extracts the text, the pipeline relies on the Text Split cognitive skill to divide the content into chunks suitable for embedding model context limits.7 This skill is inherently structural-agnostic for code; it operates purely on linguistic and character-based heuristics. The skill is configured globally within a skillset, though advanced architectures can utilize the Conditional skill to route different file types to differently configured Text Split skills.8
The parameters governing the Text Split skill dictate the fidelity of the resulting chunks:
textSplitMode: Determines the splitting methodology, offering either pages (fixed-size chunks) or sentences (splitting at language-dependent punctuation).7 For architecture files—which consist largely of code, brackets, and markup where standard sentence-ending punctuation is irregular—the pages mode is universally utilized.
maximumPageLength: Defines the strict upper bound of the chunk size. When the unit parameter is set to characters, this length is measured by string length, ranging from 300 to 50,000 characters, with a default of 5,000.7 More effectively, when the unit is set to azureOpenAITokens, the length is calculated using the specific tokenizer expected by the embedding model (e.g., cl100k_base for modern OpenAI models).7 A standard recommendation for dense vector embeddings is 512 tokens to maximize semantic density without diluting the attention mechanism of the embedding model.7
pageOverlapLength: Defines the overlap between consecutive chunks.7 Overlap is crucial because it acts as an adhesive, preserving transitional context that might otherwise be severed at a hard chunk boundary.7 This operates somewhat analogously to a sliding window, but it is applied sequentially during ingestion rather than as a continuous rolling evaluation at query time.
maximumPagesToTake: Limits the total chunks extracted from a single document.7 This parameter is highly useful for mitigating index bloat or controlling LLM processing costs when dealing with excessively verbose log files, though it is generally set to 0 (unlimited) for architecture files where total recall is required.7
defaultLanguageCode: Supports non-whitespace languages to avoid truncating words improperly, though architecture files predominantly rely on standard ASCII or UTF-8 spacing.7
While the Text Split skill provides granular control over token-bound constraints, its inability to recognize YAML hierarchies or JSON structures (unless specifically parsed via jsonArray modes 10) means that a chunk boundary will inevitably separate a parent YAML key from its nested properties if the file exceeds the token limit. In these instances, the default behavior of Azure AI Search devolves to arbitrary truncation, performing analogously to GitHub Copilot's generic fallback mechanics, slicing text strictly by length rather than preserving semantic integrity.
Integrated Vectorization Pipeline
The integrated vectorization pipeline in Azure AI Search represents a significant architectural shift, eliminating the need for external middleware, custom orchestration scripts, or manual database synchronization to handle data ingestion, chunking, and embedding generation. This end-to-end architecture continuously synchronizes a supported data source (such as Azure Blob Storage, Azure Data Lake Storage Gen2, or Microsoft OneLake) with a highly optimized vector index.11
Pipeline Architecture and Embedding Models
The pipeline is composed of three interconnected components: an indexer that retrieves and tracks raw data, a skillset that defines the transformation and enrichment operations, and the target search index that stores the schemas and vectors.11 When a document enters the pipeline, it is cracked, passed to the Text Split skill for chunking, and subsequently routed to an embedding skill.11
The AzureOpenAIEmbedding skill automatically generates vector arrays by transmitting the text chunks to designated embedding models hosted securely on Azure OpenAI.11 Vectorization is not an automatic byproduct of index creation; it requires explicit skillset configuration, where an embedding skill is mapped to the output of a chunking skill, and a vectorizer profile is bound to the target index fields.11
The available embedding models present distinct choices regarding dimensionality, pricing, and semantic quality 11:
Embedding Model
Output Dimensionality
Quality Profile
Relative Cost / Efficiency
text-embedding-ada-002
1536 dimensions
Legacy standard; strong general text comprehension.
Moderate cost; fixed dimension size limits index compression.
text-embedding-3-small
1536 dimensions (truncatable)
Superior multilingual and coding semantic retrieval vs ada-002.
Highly cost-effective; allows dimension truncation (e.g., to 512) for massive storage savings with minimal degradation.
text-embedding-3-large
3072 dimensions (truncatable)
Highest precision; captures deep semantic nuance in complex architecture documents.
Higher cost per token; yields the largest index footprint if not truncated.

Incremental Indexing Mechanics and Latency
Enterprise architecture repositories are highly dynamic, requiring search indexes to reflect commits and modifications rapidly. Azure AI Search handles this via incremental indexing.11
When utilizing the standard "pull" model, the indexer polls the data source for modifications using internal high-water marks or file system timestamps. If a single YAML file or Markdown document is modified, the indexer identifies the exact updated file, extracts the new payload, re-chunks the text, re-vectorizes the resulting chunks, and performs an atomic update on the search index.11 Crucially, only the modified document is processed; the remainder of the vector index remains untouched, preserving compute resources and OpenAI token quotas.11 Stale chunks belonging to the previous version of the file are overwritten or deleted depending on the document tracking configuration.
Latency in the pull model is fundamentally constrained by the indexer schedule. The minimum permissible execution interval for a scheduled indexer is five minutes.13 Therefore, the latency from a file modification to its availability in the index can span from a few seconds up to five minutes, plus the pipeline processing duration.
For scenarios demanding near real-time synchronization, Azure AI Search supports a "push" model. In this architecture, external compute layers—such as GitHub Actions or Azure Logic Apps—utilize the Search REST APIs to directly push updated document payloads and pre-computed vectors into the index immediately following a repository commit, completely bypassing the polling interval of the indexer.13 While this reduces latency to near-zero, it shifts the orchestration and retry logic burden entirely onto the client architecture.
Custom Skillset Extensibility for Non-Standard File Types
To achieve format-aware chunking that systematically outperforms generic sliding windows or arbitrary token limits, the Azure AI Search pipeline must be extended using Custom Web API skills. This extensibility allows the implementation of highly specialized parsing logic, such as a dedicated OpenAPI parser or an AST-based Tree-sitter mechanism, operating directly within the ingestion flow.15
Skillset Pipeline Architecture and Payload Structure
A Custom Web API skill is typically hosted as an externally accessible HTTP endpoint, most frequently an Azure Function.15 As the indexer processes documents, it sends an HTTP POST request to this custom endpoint. The request contains a JSON payload structured with a values array, where each item represents a document or a text node extracted by preceding skills.17
The custom Azure Function receives the raw text—for instance, a full OpenAPI YAML string. The function executes custom code to load the string into an OpenAPI parser, programmatically resolves internal and external $ref pointers, and splits the document logically by API endpoint definitions rather than blindly counting tokens. Once the processing is complete, the function constructs a JSON response that perfectly mirrors the incoming values array, containing the newly structured chunks appended with unique recordId identifiers and mapping the output to the target field definitions.17 The indexer receives this response and seamlessly injects the structured chunks back into the pipeline for subsequent vectorization.
Constraints, Limitations, and Performance Implications
Implementing custom skills introduces stringent engineering constraints that must be carefully managed to ensure pipeline stability:
Timeout Limits: Custom Web API skills operate under a default timeout of 30 seconds. This can be explicitly configured in the skillset definition up to an absolute maximum of 230 seconds.15 Processing deeply nested, 500-line OpenAPI YAML files with extensive external $ref resolutions across network boundaries must complete within this rigid window, or the indexer will throw a transient failure and drop the document enrichment.15
Cold Start Latency: Azure Functions hosted on standard consumption plans suffer from cold start latency. If an indexer runs on a sparse schedule and triggers the function after a period of dormancy, the initial HTTP request may experience multi-second delays, risking timeout.16 Deploying the function on Premium plans or dedicated Azure App Service plans mitigates this risk but substantially increases the baseline cost profile.
Payload Size Limits: The payloads transmitted to custom skills are constrained by standard HTTP and internal memory limits. Extremely large monolithic repositories or multi-megabyte log files cannot be sent in a single payload. They must either be pre-split using a built-in Text Split skill before being routed to the custom skill, or the function must be passed a URI reference to fetch the blob directly, bypassing the skillset payload restrictions.
Engineering and Maintenance Effort: Microsoft provides foundational examples of custom skills (e.g., the Power Skills repository) 18, but there is no out-of-the-box marketplace skill for OpenAPI, AsyncAPI, or Tree-sitter AST parsing.8 Developing these skills requires custom software engineering, robust error handling to prevent whole-pipeline failures due to malformed YAML files, and continuous maintenance of the underlying parsing libraries (e.g., swagger-parser, tree-sitter bindings).18
File-Type-Specific Analysis and Retrieval Comparison
The core objective of this assessment is to determine whether Azure AI Search provides meaningfully better chunking than GitHub Copilot's generic 60-line Jaccard sliding window fallback for specific architecture file types. The following section provides an exhaustive evaluation of default behaviors, potential customizations, and comparative retrieval superiority.
Summary Comparison Table
File Type
Default Azure AI Search Behavior
Optimal Custom Pipeline Architecture
Engineering Effort
Improvement vs. Copilot 60-Line Window
OpenAPI YAML
Plain text; arbitrary token splitting.
Custom Azure Function parsing OpenAPI DAG & resolving $ref.
High
Meaningfully better. Preserves endpoint schemas intact.
Markdown (MADR)
Native H1-H6 structural chunking (oneToMany).
Default configuration utilizing markdownParsingSubmode.
Low
Massively better. Preserves discrete ADR sections.
PlantUML (.puml)
Plain text; !include directives ignored.
Custom skill fetching includes & parsing diagram syntax.
Very High
Meaningfully better. Native indexer misses linked dependencies entirely.
AsyncAPI YAML
Plain text; arbitrary token splitting.
Custom Azure Function parsing event schemas and channels.
High
Meaningfully better. Prevents fragmentation of event definitions.
YAML Metadata
Plain text or json mode fallback.
Default text splitting (usually yields 1 chunk for small files).
Low
Equivalent. Small files do not trigger adverse fragmentation.
Source Code
Plain text; arbitrary token splitting.
Custom Azure Function wrapping a Tree-sitter AST parser.
Very High
Inferior by default. AST custom skill merely achieves parity with Copilot.
Config YAML
Plain text; arbitrary token splitting.
Default text splitting (usually yields 1 chunk for small files).
Low
Equivalent. Small files fit entirely in one context window.
Figma (JSON)
Native jsonArray structural chunking.
Configured documentRoot parsing to target design tokens.
Low
Better. JSON parsing flawlessly preserves discrete design objects.

4a. OpenAPI YAML Specifications
Default Behavior: Azure AI Search's document cracker does not possess inherent semantic awareness of YAML hierarchies. An OpenAPI file, even one exceeding 500 lines, is ingested and treated as a continuous plain text string.3 If this file is processed by the Text Split skill, a chunk boundary is highly likely to sever a deeply nested schema definition (e.g., within the components/schemas block) from its parent HTTP path, rendering both the path and the schema semantically orphaned in the vector space. Furthermore, $ref pointers are treated as literal strings; the system does not dynamically traverse, fetch, or inline external or internal references during indexing.
Best Achievable Behavior: Achieving structural coherence requires a custom Web API skill utilizing a parsing library (such as Swagger Parser).16 This custom Azure Function receives the raw YAML, dereferences all $ref pointers by traversing the document graph, and emits a structured JSON array where each element represents a fully contained endpoint definition (combining Path, Method, Parameters, and resolved Responses).
Engineering Effort: High. It requires deploying an Azure Function, managing parsing edge cases for invalid YAML, and ensuring that complex graph resolutions complete within the 230-second timeout limit.15 There is no existing Microsoft marketplace skill for OpenAPI parsing.
Comparison against Copilot: A 60-line sliding window frequently corrupts OpenAPI context. YAML relies heavily on vertical indentation and distant references; a 60-line window capturing an endpoint path will almost certainly fail to encompass the corresponding components/schemas reference located hundreds of lines below. While Azure AI Search's default behavior is equally poor, a custom skillset approach is meaningfully superior as it guarantees that the LLM receives complete, semantically intact API endpoints during retrieval, entirely eliminating reference fragmentation.
4b. Markdown (ADRs, Solution Designs)
Default Behavior: Azure AI Search excels at Markdown processing. By utilizing the markdownParsingSubmode parameter configured to oneToMany, the indexer automatically cracks the Markdown file based on header boundaries (H1 through H6) rather than arbitrary text length.5
Best Achievable Behavior: For a Markdown Architecture Decision Record (MADR) format file containing specific, structured sections (e.g., Status, Context, Decision Drivers, Considered Options, Decision Outcome), the default oneToMany parsing creates a distinct, highly coherent search document for each individual section.5 The resulting chunks include valuable structural metadata, such as header_level and ordinal_position, allowing downstream LLMs or Foundry IQ agents to understand exactly where the chunk originated within the document's logical hierarchy.5
Engineering Effort: Low. This is a native configuration parameter requiring no external compute or custom development.
Comparison against Copilot: Azure AI Search natively outperforms Copilot's generic windowing for Markdown. A 60-line window might arbitrarily straddle the end of the "Considered Options" section and the beginning of the "Decision Outcome" section, creating a confused, cross-contextual semantic vector. Azure AI Search's heading-aware chunking cleanly isolates the architectural reasoning into discrete, highly relevant vectors.
4c. PlantUML Diagrams (.puml)
Default Behavior: PlantUML files are treated strictly as plain text.3 Azure AI Search parses the raw text syntax but applies no visual, structural, or semantic analysis to the diagram graph. Critically, the blob indexer operates on single, isolated blobs. It does not possess a local file system context and therefore cannot natively follow or resolve !include directives pointing to companion files.3 The !include statement is indexed merely as an opaque text string, completely ignoring the dependent structural data.
Best Achievable Behavior: Achieving true diagram comprehension requires a complex custom skill that parses the .puml text, identifies !include directives, issues programmatic API calls to the storage account or Git repository to fetch the referenced text, and injects it into a unified syntax tree.16 The skill could further transform the PlantUML syntax into structured JSON defining actors, participants, and directional flow logic, which yields vastly superior semantic vectors than raw syntax.
Engineering Effort: Very High. Writing an Azure Function to recursively resolve includes across cloud storage boundaries is complex, highly error-prone, and susceptible to timeout failures if dependency graphs are deep.15
Comparison against Copilot: Copilot operates within a local IDE workspace where !include files are physically present on the local disk. While Copilot's 60-line text-window approach struggles to synthesize holistic diagram semantics, its ability to locally access referenced files gives it an environmental advantage. An Azure AI Search custom skill producing structured JSON would yield superior retrieval relevance, but the implementation overhead to replicate local file system resolution in a cloud indexer is severe.
4d. AsyncAPI Event Specifications
Default Behavior: The ingestion mechanics for AsyncAPI are identical to OpenAPI; the file is flattened into plain text.3 The Text Split skill will arbitrarily slice event definitions, payload schemas, and publish/subscribe channel descriptions based on token limits 7, destroying the relational context between a message schema and its transport channel.
Best Achievable Behavior: A custom Web API skill utilizing an AsyncAPI parsing library to resolve $ref pointers and chunk the file into discrete event definitions (pairing channels directly with their resolved payload schemas).
Engineering Effort: High, mirroring the exact architectural complexity and constraints of the OpenAPI custom skill.16
Comparison against Copilot: Custom format-aware chunking provides a massive advantage over Copilot's 60-line window. Event-driven architectures often decouple schemas from channel definitions. A sliding window will inevitably fragment deeply nested message schemas and sever them from their routing definitions, whereas a custom skillset ensures the LLM retrieves the complete event contract in a single chunk.
4e. YAML Metadata Files (Capabilities, Tickets, Domain Classifications)
Default Behavior: Small YAML metadata files (e.g., capability tags, domain classifications, or ticketing metadata generally under 150 lines) are cracked as plain text.3 Because the default maximumPageLength is 5,000 characters or 512 tokens 7, these small files comfortably fit within a single indexing chunk. The Text Split skill does not break them further, natively preserving their entire context.
Best Achievable Behavior: If the YAML files are converted to JSON prior to ingestion, the json parsing mode maps properties directly to Azure AI Search index fields, allowing for strict field-level filtering.10 Otherwise, retaining them as single plain text chunks is highly effective. The YAML key hierarchy does not influence boundaries, but because no boundaries are drawn within small files, the lack of awareness is irrelevant.
Engineering Effort: Low.
Comparison against Copilot: Azure AI Search and Copilot perform equivalently here. Small files do not exceed context boundaries, so neither system suffers from fragmentation penalties.
4f. Java / TypeScript / Python Source Code
Default Behavior: Azure AI Search treats programming source code as plain text. It natively lacks Abstract Syntax Tree (AST) parsing or function-level awareness.3 The Text Split skill divides the code based on arbitrary character or token counts. This means a chunk boundary might randomly divide a while loop, sever a method signature from its implementation logic, or separate a class declaration from its methods.7
Best Achievable Behavior: A custom skillset must be engineered using a containerized microservice or an advanced Azure Function that implements the Tree-sitter parsing library.16 This skill would receive the raw code, generate an AST, and emit discrete chunks strictly aligned with class, interface, and function boundaries, appending vital metadata (e.g., package names, import statements) to each chunk to preserve global context.
Engineering Effort: Very High. Hosting Tree-sitter binaries within Azure Functions or custom Web API containers requires significant development, dependency management, extensive testing against varied code styles, and continuous maintenance.16
Comparison against Copilot: GitHub Copilot's native integration of Tree-sitter AST parsing is vastly superior to Azure AI Search's default plain text chunking.1 Copilot natively understands code semantics, boundaries, and dependencies out-of-the-box. Replicating this behavior in Azure AI Search demands a massive engineering investment simply to achieve baseline parity. For pure source code retrieval, Copilot remains the superior architectural choice.
4g. Configuration YAML (Small Files)
Default Behavior: Configuration files under 100 lines easily bypass the threshold for token subdivision. The Text Split skill outputs a single chunk containing the entire configuration.7 The minimum chunk size is bounded theoretically only by the file length itself.
Best Achievable Behavior: The default behavior is optimal, ensuring the LLM sees the complete configuration state without fragmentation.
Engineering Effort: Low.
Comparison against Copilot: Equivalent. Both systems can process small configuration files within a single context window without data loss.
4h. Figma Wireframes
Default Behavior: Azure AI Search native indexers cannot authenticate to or connect directly with the Figma API URL to scrape dynamic graphical artboards. However, if Figma design tokens are exported as JSON files and committed to a Git repository, Azure AI Search leverages its highly effective jsonArray and jsonLines parsing modes.10
Best Achievable Behavior: Using the jsonArray parsing mode combined with the documentRoot parameter, Azure AI Search can dynamically target specific nested arrays within the Figma export.10 This chunks the file intelligently, creating one searchable vector document per design token object rather than creating a single monolithic, unsearchable JSON blob.
Furthermore, Foundry IQ agents can utilize Model Context Protocol (MCP) servers to query the live Figma platform directly via external APIs, bypassing the Azure AI Search indexer entirely and retrieving real-time data.23
Engineering Effort: Low for JSON indexing via native settings. Low to moderate for configuring an MCP server via Foundry IQ, assuming an existing Figma MCP server is utilized.
Comparison against Copilot: Azure AI Search's JSON parsing mode natively isolates design token objects flawlessly. A 60-line text window in Copilot might arbitrarily slice through a JSON object, corrupting the syntax and confusing the LLM. Azure AI Search handles structured JSON design tokens significantly better.
Retrieval Quality Comparison Points
The effectiveness of a chunking strategy is ultimately realized during the retrieval phase. Azure AI Search offers a sophisticated, server-side multi-stage retrieval architecture that contrasts sharply with localized, client-side mechanisms.
Retrieval Modes and Hybrid Search Mechanisms
Azure AI Search supports multiple retrieval modes: keyword search utilizing the industry-standard BM25 probabilistic algorithm, pure vector search utilizing Hierarchical Navigable Small World (HNSW) and exhaustive k-nearest neighbor (eKNN) algorithms, and hybrid search.24
The hybrid search implementation executes parallel L1 retrieval queries across both keyword inverted indexes and dense vector indexes. It merges the results mathematically using Reciprocal Rank Fusion (RRF), ensuring that documents ranking highly in both lexical and semantic spaces are promoted.24 This differs structurally from Copilot's hybrid approach, which often leans heavily on client-side context (open tabs, recently viewed files) combined with remote Jaccard sliding window metrics. Azure's server-side vector calculations span the entire enterprise repository simultaneously, unconstrained by the developer's immediate local workspace or IDE state.
Semantic Ranking (L2 Execution)
Azure AI Search implements an optional, highly advanced L2 execution step known as the Semantic Ranker. This system utilizes deep learning models adapted from Microsoft Bing to rescore the top 50 results retrieved by the L1 hybrid search.24 It evaluates the semantic relevance of the chunks against the specific cognitive intent of the user's query. For architecture files where exact technical terminology (captured by BM25) and conceptual similarity (captured by vectors) must be balanced, the Semantic Ranker demonstrates significant, measurable improvements in relevance over baseline vector retrieval.24
Latency Profiles and Direct File Access
Keyword Latency: Extremely low (single-digit milliseconds) due to optimized inverted index lookups.
Vector Latency: Low, relying on pre-computed HNSW graphs traversing memory-optimized nodes.
Hybrid Latency: Slightly elevated as it requires parallel processing across two distinct index structures and execution of the RRF merge algorithm.
Semantic Re-ranking: Adds measurable latency (up to a few seconds for large result sets) due to the real-time, compute-intensive inference required by the deep learning cross-encoder models.24
Retrieval can be securely scoped to specific directories, repositories, or user permissions through metadata filters and strict Role-Based Access Control (RBAC). Document-level permissions propagate from sources like Azure Data Lake or SharePoint natively, ensuring that highly sensitive architectural assets restricted to specific engineering teams are not exposed during vector search.25 While Azure AI Search is fundamentally a search retrieval engine rather than a file system, direct file access is possible by querying a document's specific ID or metadata path via the REST API to retrieve the exact, unmodified source text.11
Foundry IQ Layer and Agentic Retrieval
Foundry IQ introduces an advanced orchestration layer above the foundational Azure AI Search index, designed specifically to construct multi-source AI knowledge bases and manage complex, iterative retrieval pipelines automatically.27
Query Planning and Retrieval Instructions
Foundry IQ does not introduce new native chunking mechanics; it relies entirely on the ingestion pipeline and predefined skillsets of the underlying Azure AI Search resource.27 However, it drastically enhances retrieval intelligence through LLM-driven agentic query planning.26
A critical feature in Foundry IQ is the use of retrievalInstructions.25 This parameter is embedded within the knowledge base schema definition and serves as a system prompt to guide the LLM during the query planning phase. Rather than blindly executing a vector search, retrievalInstructions dictate how the query should be decomposed and explicitly constrain which knowledge sources should be included or excluded based on the query intent.25 This allows an enterprise architect to explicitly instruct the agent: "For queries regarding event routing, strictly query the AsyncAPI knowledge source; for code implementation details, query the Java codebase source." While these instructions guide source routing, they cannot alter the underlying chunking methodology of the files.
Reasoning Effort Levels
Foundry IQ allows configuration of the LLM's query-planning exertion via the retrievalReasoningEffort parameter, directly impacting retrieval quality for structured files by dictating the depth of the search 26:
Minimal: Bypasses LLM query planning entirely. It performs direct text and vector searches across up to 10 sources, returning raw passages. It minimizes latency and cost but relies entirely on the user's exact phrasing.26
Low (Default): Executes a single pass of LLM-based query planning. The LLM breaks the user query into component parts (up to three subqueries) and executes them across up to three sources, merging the results for answer synthesis. It operates within a 5,000-token budget.26
Medium: Deploys a sophisticated iterative search loop. It evaluates initial results using a high-precision semantic classifier (L3 classification). If the architectural context retrieved is deemed insufficient to answer the query accurately, it automatically reflects, revises the query plan, expands terminology, and executes a second retrieval pass across up to five sources and five subqueries, operating within a 10,000-token budget.26
GitHub Ingestion and MCP Exposure
Foundry IQ categorizes data sources as either indexed (stored persistently in Azure AI Search) or remote (queried dynamically on demand).27 Currently, native indexed sources focus heavily on Azure Blob Storage, OneLake, and SharePoint.27 Direct, native continuous indexing of GitHub repositories without a middle-tier synchronization pipeline (copying files to Blob Storage) is not an out-of-the-box indexed source feature.
However, Foundry IQ mitigates this through support for Model Context Protocol (MCP) servers as remote knowledge sources.33 An agent can be configured with a GitHub MCP endpoint, allowing it to dynamically execute specific tools (such as searching code, reading commits, or parsing issues) directly against the live GitHub repository.33 This dynamic approach ensures the agent accesses the most current file states, leveraging the MCP tool's specific semantic awareness without replicating the data into a static Azure vector index.
Cost Profile and Resource Modeling
Implementing integrated vectorization and custom skillsets within Azure AI Search incurs specific infrastructural and operational costs that must be factored into the architectural decision.
Required Pricing Tiers and Indexing Costs
While Azure AI Search offers a Free tier for initial experimentation, production deployments utilizing integrated vectorization, substantial vector storage, and adequate partition capacity strictly require the Standard 1 (S1) tier or higher.12 Older basic tiers or services provisioned prior to January 2019 lack the hardware architecture to support vector workloads.11
There is no per-document indexing cost levied directly by the Azure AI Search engine; users pay a flat rate for the allocated compute tier. For example, an S1 instance starts around $245–$269 per month depending on the specific Azure region and compute type.36 However, the act of vectorization incurs variable LLM token costs. Using the AzureOpenAIEmbedding skill requires API calls to models like text-embedding-ada-002 or text-embedding-3-small, which are billed by the token via the Azure OpenAI service.11
Query execution costs follow a similar paradigm: standard keyword, vector, and hybrid searches do not incur per-query charges from Azure AI Search itself, as they utilize the provisioned S1 compute.36 However, if Semantic Ranking is enabled or Foundry IQ Agentic Retrieval is utilized, additional costs apply. Agentic Retrieval query planning is billed via the LLM (e.g., GPT-4o input/output tokens), while the execution ranking includes a free allowance (first 50M tokens free per month) followed by a charge of $0.022 per 1M additional tokens.37
Custom Skillset Costs
Introducing custom skillsets (such as OpenAPI parsers or Tree-sitter AST containers) adds the execution cost of the external compute layer.8 If hosted on Azure Functions via a consumption plan, costs accumulate based on execution time and memory allocation, though Microsoft provides substantial monthly free grants. The primary cost, however, is the human capital and maintenance overhead required to develop, secure, monitor, and update these specialized parsing algorithms against evolving architecture specifications.19
Cost Model for 200 Architecture Files (Weekly Refresh)
For an enterprise repository containing approximately 200 architecture files (comprising OpenAPI specs, ADRs, PlantUML diagrams, and metadata) with a weekly automated refresh cycle, the resource model is highly predictable:
Resource Component
Estimated Metric
Estimated Monthly Cost
Notes
Azure AI Search (S1 Tier)
1 Unit (Replica/Partition)
~$250.00
Fixed base cost. 160 GB storage limit accommodates thousands of files easily.
Vectorization (OpenAI)
200 files * 2,000 tokens * 4 weeks
< $1.00
1.6M tokens/month. ada-002 and 3-small cost fractions of a cent per 1k tokens.
Agentic Retrieval / Semantic Ranker
Low Volume
$0.00
Falls well within the 50M token free allowance.
Custom Skills (Azure Functions)
800 executions / month
$0.00
Falls entirely within the 1 million execution free tier grant.

The predominant expense in this model is the static monthly allocation of the Azure AI Search compute tier. The execution costs for ingestion and vectorization are negligible at this scale. The hidden, unquantified cost remains the developmental investment required to build format-aware chunking custom skills for YAML and code files.
Strategic Conclusions
Azure AI Search and Foundry IQ present a highly customizable, centralized retrieval ecosystem that fundamentally contrasts with GitHub Copilot's local, workspace-oriented architecture.
For documentation formats like Markdown ADRs and small configuration files, Azure AI Search dramatically outperforms generic 60-line sliding windows due to its native structural cracking and header-aware subdivision. Furthermore, its ability to parse JSON design tokens directly into actionable fields provides a clear advantage for UI/UX architectural assets.
However, for highly structured engineering assets—specifically deeply nested OpenAPI/AsyncAPI YAML, PlantUML diagrams with distributed file dependencies, and programming source code—Azure AI Search’s default plain text chunking falls significantly short of the semantic coherence offered natively by Copilot's Tree-sitter integration and local workspace awareness.
To bridge this semantic gap, enterprise architecture teams must undertake moderate to high engineering efforts to develop custom Web API skillsets. Wrapping OpenAPI parsers and AST libraries within Azure Functions allows Azure AI Search to achieve pristine, semantically isolated chunking. When this rigorous custom chunking is coupled with Foundry IQ's agentic query planning, specific retrievalInstructions, and L3 iterative semantic ranking, a fully customized Azure AI Search pipeline offers an unparalleled, highly precise enterprise retrieval capability. This establishes a powerful, global knowledge base, albeit one that requires significant initial developmental investment compared to Copilot's out-of-the-box utility.
Works cited
Building a Knowledge Assistant over Code | Databricks Blog, accessed April 8, 2026, https://www.databricks.com/blog/building-knowledge-assistant-over-code
Stop Using AI Just for Code Completion — Here's a Workflow That Covers Your Entire SDLC, accessed April 8, 2026, https://dev.to/anderson_leite/stop-using-ai-just-for-code-completion-heres-a-workflow-that-covers-your-entire-sdlc-320b
Azure Blob Indexer - Azure AI Search | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/search-howto-indexing-azure-blob-storage#supported-document-formats
Document Extraction Cognitive Skill - Azure AI Search | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/cognitive-search-skill-document-extraction
Index Markdown blobs and files in Azure AI Search - Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/search-how-to-index-azure-blob-markdown
Azure Content Understanding Skill - Azure AI Search | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/cognitive-search-skill-content-understanding
Text Split Skill - Azure AI Search | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/cognitive-search-skill-textsplit
Skills Reference - Azure AI Search | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/cognitive-search-predefined-skills
Chunk large documents for RAG and vector search in Azure AI Search, accessed April 8, 2026, https://docs.azure.cn/en-us/search/vector-search-how-to-chunk-documents
Search Over JSON Blobs - Azure AI Search | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/search-howto-index-json-blobs
Integrated Vectorization Overview - Azure AI Search | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization
Set up integrated vectorization in Azure AI Search using REST - Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/search-how-to-integrated-vectorization
Push method for AI search index - Microsoft Community Hub, accessed April 8, 2026, https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/push-method-for-ai-search-index/4474330
Incrementally Indexing documents with AzureAI Search Integrated Vectorisation | by Ozgur Guler | Microsoft Azure | Medium, accessed April 8, 2026, https://medium.com/microsoftazure/incrementally-indexing-documents-with-azureai-search-integrated-vectorization-6f7150556f62
Custom Web API Skill in Skillsets - Azure AI Search - Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/cognitive-search-custom-skill-web-api
Custom Skill Interface - Azure AI Search - Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/cognitive-search-custom-skill-interface
How to populate Azure AI Search field with a custom skill? - Stack Overflow, accessed April 8, 2026, https://stackoverflow.com/questions/78328328/how-to-populate-azure-ai-search-field-with-a-custom-skill
Module 3: Introduction to Azure Functions and Custom Skills - GitHub, accessed April 8, 2026, https://github.com/Azure-Samples/azure-search-knowledge-mining/blob/master/workshops/Module%203.md
Introducing AI Prototyping Projects - Leading EDJE, accessed April 8, 2026, https://blog.leadingedje.com/post/aiprototyping/introducingaiprototyping.html
Search Index Overview - Azure AI Search | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/search-what-is-an-index
Scale and Manage Custom Skills - Azure AI Search | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/cognitive-search-custom-skill-scale
Agent Memory Indexer - Visual Studio Marketplace, accessed April 8, 2026, https://marketplace.visualstudio.com/items?itemName=Yensubldg.agent-memory-indexer
10 Microsoft MCP Servers to Accelerate Your Development Workflow, accessed April 8, 2026, https://developer.microsoft.com/blog/10-microsoft-mcp-servers-to-accelerate-your-development-workflow
Azure AI Search: Outperforming vector search with hybrid retrieval and reranking, accessed April 8, 2026, https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/azure-ai-search-outperforming-vector-search-with-hybrid-retrieval-and-reranking/3929167
What's New - Azure AI Search | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/whats-new
Set the Retrieval Reasoning Effort - Azure AI Search | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-set-retrieval-reasoning-effort
From Classic RAG to Agentic Retrieval: Inside Microsoft's Foundry IQ Architecture. - ITNEXT, accessed April 8, 2026, https://itnext.io/from-classic-rag-to-agentic-retrieval-inside-microsofts-foundry-iq-architecture-7338e1bd4eb4
Foundry IQ for Multi-Source AI Knowledge Bases - YouTube, accessed April 8, 2026, https://www.youtube.com/watch?v=bHL1jbWjJUc
Foundry IQ FAQ - Microsoft Foundry | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/foundry-iq-faq
What's New - Azure AI Search | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/whats-new#retrieval-instructions-preview
Create a Knowledge Base - Azure AI Search | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-create-knowledge-base
Foundry IQ: boost response relevance by 36% with agentic retrieval, accessed April 8, 2026, https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/foundry-iq-boost-response-relevance-by-36-with-agentic-retrieval/4470720
Foundry IQ for Multi-Source AI Knowledge Bases | by Mechanics Team - Medium, accessed April 8, 2026, https://officegarageitpro.medium.com/foundry-iq-for-multi-source-ai-knowledge-bases-d54bbff98505
punkpeye/awesome-mcp-servers: A collection of MCP servers. - GitHub, accessed April 8, 2026, https://github.com/punkpeye/awesome-mcp-servers
Vector Index Overview | Azure Docs, accessed April 8, 2026, https://docs.azure.cn/en-us/search/vector-store
Plan and manage costs of an Azure AI Search service, accessed April 8, 2026, https://docs.azure.cn/en-us/search/search-sku-manage-costs
Azure AI Search pricing, accessed April 8, 2026, https://azure.microsoft.com/en-us/pricing/details/search/
Azure OpenAI Service - Pricing, accessed April 8, 2026, https://azure.microsoft.com/en-us/pricing/details/azure-openai/
Azure AI Foundry vs Custom ML Pipelines for Enterprises, accessed April 8, 2026, https://www.imaginarycloud.com/blog/azure-ai-foundry-vs-custom-ml-pipelines
