# Deep Research Results: Azure AI Search Chunking Mechanics (Fast Mode)

<!-- Paste fast mode deep research results below this line -->

Engineering Analysis of Azure AI Search Retrieval and Ingestion Architectures for Technical Documentation
The modernization of architectural documentation management requires a transition from passive storage to active, context-aware retrieval systems. As organizations move toward retrieval-augmented generation (RAG) and agentic workflows, the efficacy of information retrieval is fundamentally gated by the strategies employed during document cracking, chunking, and indexing. While many developers rely on the default behaviors of integrated development environments, such as GitHub Copilot’s 60-line sliding window fallback, enterprise-grade solutions like Azure AI Search offer a sophisticated, modular pipeline designed to handle the structural nuances of technical artifacts. This report examines the technical mechanisms of Azure AI Search across specific architectural file types, evaluates the engineering effort required for optimization, and benchmarks these outcomes against generic lexical retrieval methods.
Azure AI Search Document Cracking and Built-In Chunking
The ingestion lifecycle in Azure AI Search begins with document cracking, a multi-stage process where the search indexer extracts text, images, and metadata from binary data sources.1 This process transforms unstructured blobs or database rows into an internal representation known as an enrichment tree.1 The enrichment tree serves as a dynamic, in-memory structure that starts with the raw content at the root node, denoted as /document, and expands as subsequent cognitive skills add refined data nodes.2
Native File Format Support and Structural Recognition
Azure AI Search provides broad native support for various enterprise file formats, including PDF, Microsoft Office (Word, Excel, PowerPoint), HTML, XML, JSON, and plain text.4 For technical and architectural documentation, the service's behavior is specialized based on the detected MIME type and the configured parsing mode.
Markdown (.md): This is cracked with a specialized parser. Developers can choose between a one-to-one mode, which treats the entire file as a single document, or a one-to-many mode, which breaks the file into multiple search documents based on the Markdown header hierarchy.7
YAML, AsyncAPI, and Configuration Files: These are generally cracked as plain text unless they are processed as JSON-compatible or passed through a custom skillset.4 By default, the indexer extracts the entire file content into a flat string field.
PlantUML (.puml): This format is not natively recognized as a structured document. The indexer treats it as unknown text, extracting the raw string representation without understanding the relationships between participants, actors, or message flows.4
Available Chunking Strategies and the Text Split Skill
Once text is extracted, the Text Split cognitive skill is the primary mechanism for partitioning content into manageable chunks suitable for embedding models.10 This skill is critical for maintaining compliance with the input token limits of large language models, such as the 8,191-token limit for text-embedding-3-small.10
The Text Split skill operates in two distinct modes: pages and sentences.12 The pages mode is the most common for technical documentation, as it allows for fixed-length chunking with a configurable maximumPageLength.10 In the sentences mode, the skill terminates chunks at punctuation marks like periods or question marks.12 The boundaries are determined by a sophisticated algorithm that attempts to avoid breaking sentences mid-chunk, meaning the actual length of a chunk may be slightly less than the maximum specified.12

Parameter
Type
Default Value
Description and Range
textSplitMode
String
pages
Determines if text is split by page length or sentence boundaries. 12
maximumPageLength
Integer
5000
The max length of a chunk. Min: 300, Max: 50,000. 12
pageOverlapLength
Integer
0
The number of characters/tokens repeated from the previous chunk. 12
unit
String
characters
The measurement unit for length (characters or azureOpenAITokens). 12
defaultLanguageCode
String
en
Helps avoid word-splitting in non-whitespace languages. 12

The transition to token-based chunking in preview versions (2025-11-01-preview) allows developers to align chunking precisely with the cl100k_base tokenizer used by GPT-4 and newer models, preventing "overflow" issues where character-based limits might accidentally exceed the token budget of the embedding model.10
Semantic and Structure-Aware Chunking
Beyond simple text splitting, Azure AI Search supports "semantic chunking" through the Document Layout skill or the Azure Content Understanding skill.4 The Document Layout skill uses Azure Document Intelligence to identify headings, tables, and paragraphs, producing a Markdown-structured output that preserves the semantic relationship between elements.8 This approach is "structure-aware," as it ensures that related information (like a table spanning two pages) is treated as a single coherent unit rather than being arbitrarily severed by a line count or token limit.4
Integrated Vectorization Pipeline
The integrated vectorization pipeline represents a significant reduction in engineering overhead by managing the entire RAG lifecycle within the search service.15 This pipeline eliminates the need for external scripts to coordinate data ingestion, chunking, and embedding generation.
Pipeline Architecture and Workflow
The end-to-end flow is orchestrated by four primary components:
Data Source: Connects to supported repositories like Azure Blob Storage, ADLS Gen2, or Microsoft OneLake.6
Skillset: Defines the enrichment logic. A typical vectorization skillset includes a Text Split skill to create chunks and an Azure OpenAI Embedding skill to generate vectors for those chunks.3
Index: The physical storage where vectorized data resides. It includes a schema with vector fields and a "vectorizer" definition to handle query-time translation.11
Indexer: The execution engine that drives the data through the cracking and enrichment stages, ultimately populating the index.1
When an indexer is executed, it uses "index projections" to map one source document to many search documents in the index.8 This means a 50-page PDF becomes 50+ individual searchable chunks, each containing its own vector and a reference back to the parent file.8
Embedding Model Selection and Quality
Azure AI Search supports the latest generation of Azure OpenAI embedding models, which offer significant improvements in semantic density and pricing over legacy models.9

Model
Dimensions
Use Case
Pricing (per 1M tokens)
text-embedding-ada-002
1,536
Legacy applications, broad compatibility. 18
Standard tier rates
text-embedding-3-small
1,536 (variable)
High efficiency, low latency, standard RAG. 10
~$0.02
text-embedding-3-large
3,072 (variable)
High precision, complex technical semantics. 9
~$0.13

The quality difference between the "small" and "large" models is most evident in technical domains where subtle differences in architectural patterns require higher-dimensional representations to capture the specific intent of the designer.9
Incremental Indexing and Change Detection
Azure AI Search indexers utilize data change detection policies to optimize performance.15 If a single YAML file is updated in the source repository, the indexer identifies the change (via blob metadata or a high-water mark) and re-processes only that file.15 This incremental approach ensures that the entire index is not rebuilt for minor documentation updates, significantly reducing compute costs and processing time.20 The latency for an update to appear in the index is primarily a function of the indexer's schedule, which can be as frequent as every few minutes.15
Custom Skillsets for Non-Standard File Types
For architectural files with specialized syntax—such as OpenAPI, AsyncAPI, or PlantUML—the built-in chunking strategies may prove insufficient. In these scenarios, developers can implement Custom Web API skills to inject domain-specific parsing logic into the ingestion pipeline.17
Custom Logic and Interface Design
A custom skill is an HTTP endpoint, typically hosted as an Azure Function, that receives a JSON payload containing the document content and returns a set of "enriched" outputs.17 This allows for "logical chunking" rather than "token chunking." For instance, a custom skill can parse a 1,000-line OpenAPI spec and split it into discrete chunks based on each unique API endpoint definition, ensuring that every chunk contains the full context of a specific resource.17
The skillset pipeline can be chained so that a custom skill performs initial structure extraction or cleanup before passing the result to a built-in embedding skill.3 This "pipeline within a pipeline" architecture is powerful for complex technical data.1
Operational Constraints and Performance
Custom skills are subject to specific limits to maintain the stability of the indexing service:
Timeout: The maximum execution time for a custom skill is 230 seconds; the default is 30 seconds.23
Batch Size: The indexer can send multiple records in a single call (default is 1,000) to maximize throughput.23
Parallelism: Developers can configure the degreeOfParallelism (1 to 10) to control the number of simultaneous calls made to the custom API endpoint.23
The "cold start" latency of consumption-based Azure Functions can impact the start-up time of large indexing jobs, making Premium or Dedicated hosting plans preferable for high-volume or latency-sensitive documentation repositories.22
Cost of Custom Enrichment
The cost profile for custom skillsets involves both the execution cost of the Azure Function and the initial development effort.22 However, the development of a custom parser is often a one-time investment that significantly boosts the long-term utility of the search index by ensuring that retrieved chunks are logically complete and semantically accurate.25
File-Type-Specific Analysis
The efficacy of Azure AI Search depends on how it handles the structural nuances of specific architectural file types compared to generic lexical methods.
OpenAPI YAML Specs
Default Azure AI Search behavior treats OpenAPI YAML as plain text.4 A 500-line spec would likely be split by the Text Split skill based on token count, potentially severing the relationship between an endpoint path and its corresponding response schema or security parameters.
Customization allows for a custom skill to resolve $ref pointers—which are opaque to standard text splitters—and produce fully dereferenced endpoint chunks.24 This ensures that when an agent queries for "the response schema of the /orders endpoint," it retrieves the entire resolved definition, not just the top-level path declaration.
Engineering Effort: High. Requires writing a YAML-aware parser that understands OpenAPI specs and can follow internal/external references.
Improvement: Highly Meaningful. It transforms the search from a random line-based lookup into a resource-based retrieval that preserves API semantics.
Markdown (ADRs and Solution Designs)
Markdown is one of the few formats where Azure AI Search provides "out-of-the-box" structural intelligence.4 By configuring the parsingMode to markdown, the indexer automatically identifies headers (H1/H2/H3) and treats the content following them as discrete sections.7 For Architecture Decision Records (ADRs) following the MADR format, this ensures that sections like "Decision Outcome" or "Context" are indexed as separate, semantically relevant documents.7
Engineering Effort: Low. Primarily involves a configuration change in the indexer definition.
Improvement: Meaningful. It avoids the "mid-sentence" break common in 60-line sliding windows and keeps section-specific context together.
PlantUML Diagrams (.puml)
PlantUML files are not recognized as diagrams by Azure AI Search; they are treated as unknown text.4 Standard chunking might separate a participant declaration from the subsequent -> message flow, rendering the chunk meaningless to an LLM. Furthermore, !include directives are ignored, meaning the search engine cannot "see" the external components of the diagram.11
A custom skillset could parse the PlantUML syntax and "verbalize" the diagram into structured text (e.g., "Service A calls Service B with a POST request").25 This verbalized text would be much more effective for vector-based retrieval than the raw syntax.
Engineering Effort: High. Requires integrating a PlantUML-to-text conversion tool or a specialized LLM prompt for verbalization.
Improvement: Highly Meaningful. Raw indexing of PlantUML syntax is often low-quality; structural verbalization makes diagrams searchable.
AsyncAPI Event Specs
AsyncAPI faces the same challenges as OpenAPI. By default, it is flat text.4 Customization allows for "channel-aware" or "message-aware" chunking.24 This is particularly useful for large event-driven architectures where an event's schema might be defined at the end of a long file, far from the channel that uses it.
Engineering Effort: High.
Improvement: Meaningful. It ensures the event producer and its payload schema remain contextually linked in the index.
YAML Metadata and Configuration Files
For small metadata files (<150 lines), Azure AI Search typically produces a single chunk unless the token limit is exceeded.18 However, the YAML key hierarchy does not influence chunk boundaries by default.10 If a configuration file is 500 lines long, a standard split might cut through a nested object.
Engineering Effort: Low to Medium. For small files, the default is sufficient. For large files, a custom skill that respects nesting levels is required.
Improvement: Minimal for small files; meaningful for large, complex configurations.
Java, TypeScript, and Python Source Code
Unlike GitHub Copilot, which uses Tree-sitter for AST-aware chunking, Azure AI Search treats source code as plain text.26 Default chunking will split a function mid-way if it crosses the token limit.
To achieve Copilot-like performance, a custom skillset must implement AST-based chunking.26 This ensures that every chunk represents a complete function, class, or method, providing the LLM with a logical unit of code to reason over.
Engineering Effort: High. Requires implementing Tree-sitter or similar parsing logic in an Azure Function.
Improvement: Meaningful. It bridges the gap between "code-as-text" and "code-as-logic."
Figma Wireframes
Figma designs are typically hosted externally. While Foundry IQ can index external URLs via Bing, this is intended for public web data.28 For private architecture work, the standard pattern is to export Figma design tokens as JSON and commit them to git. Azure AI Search would then crack these JSON files.6 Without customization, JSON is cracked as a flat text blob or into specific fields.1
Engineering Effort: Medium. Requires a custom skill to parse the JSON hierarchy of design tokens.
Improvement: Meaningful. It prevents design tokens from being separated from their values or categories.
Retrieval Quality Comparison Points
The true power of Azure AI Search lies in its retrieval flexibility, which far exceeds the lexical-only Jaccard similarity fallback used by simpler tools.
Supported Retrieval Modes
Azure AI Search supports multiple retrieval strategies that can be combined for maximum accuracy:
Keyword (BM25): High-efficiency exact-match retrieval based on term frequency and document length.14
Vector Search: Semantic-match retrieval that finds conceptually similar content, even if the exact keywords differ.16
Hybrid Search: Simultaneously executes keyword and vector queries, merging the results using Reciprocal Rank Fusion (RRF).6
Semantic Ranking (L2): A secondary re-ranking stage that uses a sophisticated language model to re-evaluate the top 50 results based on deep semantic relevance.8
Latency and Scoping

Retrieval Mode
Latency Profile
Characteristics
Keyword Search
10-50ms
Fastest; best for exact IDs or names. 31
Vector Search
50-150ms
Semantic matching; handles synonyms. 32
Hybrid Search
100-250ms
Combines both; highly robust. 14
Semantic Ranker
200-500ms
Highest accuracy; re-ranks top 50 results. 30

Retrieval can be strictly scoped to specific directories or file types using OData filters on metadata fields like metadata_storage_path.21 Unlike direct file access, which is often a 1-to-1 reading operation, Azure AI Search is a "retrieval-first" system where documents are retrieved based on their relevance to a prompt.11
Foundry IQ Layer and Agentic Retrieval
Foundry IQ is a unified knowledge layer that sits on top of Azure AI Search, introducing "agentic retrieval" to handle complex, multi-part architectural questions.35
Reasoning Effort Levels
Foundry IQ offers three levels of retrieval reasoning that balance latency, cost, and completeness.28
Minimal: Direct keyword/vector search across sources. No LLM query planning. Lowest latency.36
Low: Uses an LLM to decompose a complex question into up to three sub-queries, which are executed in parallel.28
Medium: Adds a "reflective search" cycle. A semantic classifier (L3) evaluates initial results; if they are incomplete, it revisions the query plan and iterates once more to find missing details.38
Retrieval Instructions and Steering
Developers can provide "retrieval instructions" to the Foundry IQ knowledge base.28 For example, instructions can tell the engine to "prioritize ADRs over legacy technical debt wikis" or to "always provide code snippets when discussing architecture implementations".39 This steering ensures that the agent's behavior is aligned with the specific requirements of the architectural domain.
Foundry IQ can ingest data from Azure Blob Storage, SharePoint, and Microsoft OneLake.28 Currently, there is no direct-to-GitHub connector for Foundry IQ; content must be synchronized to a supported data source (like Blob Storage) before ingestion.28
Model Context Protocol (MCP) Integration
Foundry IQ knowledge bases are exposed as MCP endpoints.40 This allows agents to call the search index as a "tool," facilitating a secure and standardized way for LLMs to query the knowledge base.43 MCP allows for runtime overrides, where different users or contexts can target specific search indices dynamically.29
Cost Profile and Economic Model
The cost of an Azure AI Search solution is tiered based on storage and compute requirements.
Service Tiers and Infrastructure
For architectural documentation, the following tiers are most relevant:
Free: Suitable for POCs; limited to 3 indexes and 50MB of storage.46
Basic: The entry point for production, supporting up to 15 indexes and 15GB of storage.46
S1: The standard choice for medium enterprises, supporting up to 50 indexes and 160GB of storage.34

Tier
Monthly SU Cost (Approx)
Max Indexes
Storage
Basic
~$74.00
15
15 GB 47
Standard S1
~$245.00
50
160 GB 47

Operational Costs
Beyond the monthly search unit (SU) fee, integrated vectorization incurs costs from the Azure OpenAI service.47
Embeddings: Billed per 1,000 tokens (e.g., $0.0001 per 1k for text-embedding-3-small).49
Semantic Ranker: $1.00 per 1,000 requests after the first 1,000 free requests per month.47
Foundry IQ Agentic Retrieval: The first 50 million tokens per month are free, followed by $0.022 per 1 million additional tokens.47
Custom Skillsets: Azure Functions are billed based on execution duration and memory; for 200 documents, this is negligible (often within the free grant).22
Rough Monthly Cost Model (~200 Files, Weekly Refresh)
Item
Tier/Volume
Monthly Cost
Search Service
Basic Tier (1 SU)
~$74.00
Embeddings
~2M tokens (initial + 4 refreshes)
~$0.10
Semantic Ranker
~1,000 queries
$0.00 (Free Tier)
Foundry IQ
~2M retrieval tokens
$0.00 (Free Tier)
Custom Skills
Azure Functions (minimal)
< $1.00
Total


~$75.10

Conclusion and Strategic Comparison
The comparison between Azure AI Search and a generic 60-line sliding window reveals a fundamental trade-off between engineering effort and retrieval intelligence.
File Type
Default Azure AI Search Behavior
Improvement Over Copilot Fallback?
Engineering Effort Required
OpenAPI/AsyncAPI
Flat text, token split.
Minimal without customization.
High (Custom Skillset)
Markdown
Header-aware sections.
Meaningful.
Low (Config Only)
PlantUML
Raw syntax as text.
None without customization.
High (Custom Skillset)
Metadata YAML
Single chunk if small.
Minimal for small files.
Low
Source Code
Plain text, token split.
None (Copilot is better natively).
High (AST Skillset)
Figma (JSON)
Flat JSON extraction.
Meaningful with field mapping.
Medium

For organizations managing a small repository of simple text or Markdown files, the default behavior of Azure AI Search (Hybrid + Semantic Ranker) provides a meaningful improvement over Jaccard similarity with almost zero engineering effort. However, for specialized architectural file types like OpenAPI or PlantUML, Azure AI Search is a platform rather than a "box" solution; it requires the development of custom skillsets to achieve the structural understanding necessary for high-accuracy RAG. The primary value proposition of Azure AI Search is not its default chunking, but its modular enrichment pipeline and advanced re-ranking models, which allow architects to build a retrieval system that "understands" the logic of their design artifacts.
Works cited
Azure AI Search - Indexer Overview - Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/search-indexer-overview
Skillset Concepts - Azure AI Search | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/cognitive-search-working-with-skillsets
Create a Skillset - Azure AI Search | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/cognitive-search-defining-skillset
Azure Content Understanding Skill - Azure AI Search | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/cognitive-search-skill-content-understanding
I wanted to know list of files types supported by each model in Azure Open AI, accessed April 8, 2026, https://learn.microsoft.com/en-us/answers/questions/5533767/i-wanted-to-know-list-of-files-types-supported-by
Azure AI Search, accessed April 8, 2026, https://azure.microsoft.com/en-us/products/ai-services/ai-search
Index Markdown blobs and files in Azure AI Search - Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/search-how-to-index-azure-blob-markdown
Chunk and Vectorize by Document Layout - Azure AI Search | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/search-how-to-semantic-chunking
azure-docs-sdk-python/docs-ref-services/latest/ai-contentunderstanding-readme.md at main, accessed April 8, 2026, https://github.com/MicrosoftDocs/azure-docs-sdk-python/blob/main/docs-ref-services/latest/ai-contentunderstanding-readme.md
Chunk Documents - Azure AI Search | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents
Search Index Overview - Azure AI Search | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/search-what-is-an-index
Text Split Skill - Azure AI Search | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/cognitive-search-skill-textsplit
Document Layout Skill | Azure Docs, accessed April 8, 2026, https://docs.azure.cn/en-us/search/cognitive-search-skill-document-intelligence-layout
How To Prevent Context Loss In Azure AI Search RAG Pipelines - GoPenAI, accessed April 8, 2026, https://blog.gopenai.com/how-to-prevent-context-loss-in-azure-ai-search-rag-pipelines-497c346c7077
Integrated vector embedding in Azure AI Search - Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/vector-search-integrated-vectorization
Integrated Vectorization Using REST APIs - Azure AI Search ..., accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/search-how-to-integrated-vectorization
Invoking a custom Web API in Azure AI Search for enrichment - georgeollis.com, accessed April 8, 2026, https://www.georgeollis.com/invoking-a-custom-web-api-in-azure-ai-search-for-enrichment/
Regarding the automatic chunk splitting behavior in Azure AI Search without explicit configuration - Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/answers/questions/2238433/regarding-the-automatic-chunk-splitting-behavior-i
Building an Azure AI Search index with a custom skill - baeke.info, accessed April 8, 2026, https://baeke.info/2023/12/09/building-an-azure-ai-search-index-with-a-custom-skill/
Incrementally Indexing documents with AzureAI Search Integrated Vectorisation | by Ozgur Guler | Microsoft Azure | Medium, accessed April 8, 2026, https://medium.com/microsoftazure/incrementally-indexing-documents-with-azureai-search-integrated-vectorization-6f7150556f62
Create an index in Azure AI Search - Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/search-how-to-create-search-index
Custom Skill Example Using Bing Entity Search API - Azure AI Search | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/cognitive-search-create-custom-skill-example
Custom Web API Skill in Skillsets - Azure AI Search - Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/cognitive-search-custom-skill-web-api
How to best structure skillsets and indexing flow for chunking, embedding, and querying uploaded files via Azure AI Search and OpenAI? - Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/answers/questions/2337376/how-to-best-structure-skillsets-and-indexing-flow
Azure-Samples/ai-search-skills-in-a-box - GitHub, accessed April 8, 2026, https://github.com/Azure-Samples/ai-search-skills-in-a-box
Semantic Code Indexing with AST and Tree-sitter for AI Agents (Part — 1 of 3) - Medium, accessed April 8, 2026, https://medium.com/@email2dineshkuppan/semantic-code-indexing-with-ast-and-tree-sitter-for-ai-agents-part-1-of-3-eb5237ba687a
Building Real-Time Semantic Code Search With Tree-sitter and Vector Embeddings, accessed April 8, 2026, https://pub.towardsai.net/building-real-time-semantic-code-search-with-tree-sitter-and-vector-embeddings-b9b1fc0a94f3
Foundry IQ FAQ - Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/foundry-iq-faq
Agent tools overview for Foundry Agent Service - Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/tool-catalog
Improving Azure AI Search results with semantic search - DEV Community, accessed April 8, 2026, https://dev.to/willvelida/improving-azure-ai-search-results-with-semantic-search-1mpk
How to implement contains-like search logic and order results alphabetically in Azure Search - Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/answers/questions/5734733/how-to-implement-contains-like-search-logic-and-or
azure-ai-docs/articles/search/search-faq-frequently-asked-questions.yml at main - GitHub, accessed April 8, 2026, https://github.com/MicrosoftDocs/azure-ai-docs/blob/main/articles/search/search-faq-frequently-asked-questions.yml
Quickstart: Vector Search in the Azure portal - Azure AI Search, accessed April 8, 2026, https://docs.azure.cn/en-us/search/search-get-started-portal-import-vectors
[Azure AI Search] Index Management - Microsoft Q&A, accessed April 8, 2026, https://learn.microsoft.com/en-us/answers/questions/2154885/(azure-ai-search)-index-management
What is Foundry IQ? - Microsoft Foundry | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-foundry-iq
Foundry IQ: Agentic retrieval for more relevant AI responses - C# Corner, accessed April 8, 2026, https://www.c-sharpcorner.com/article/foundry-iq-agentic-retrieval-for-more-relevant-ai-responses/
Azure/Copilot-Studio-and-Azure - GitHub, accessed April 8, 2026, https://github.com/Azure/Copilot-Studio-and-Azure
Set the Retrieval Reasoning Effort - Azure AI Search | Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-set-retrieval-reasoning-effort
Foundry IQ: boost response relevance by 36% with agentic retrieval, accessed April 8, 2026, https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/foundry-iq-boost-response-relevance-by-36-with-agentic-retrieval/4470720
Connect Agents to Foundry IQ Knowledge Bases - Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/foundry-iq-connect
Azure OpenAI On Your Data (classic) - Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/foundry-classic/openai/concepts/use-your-data
Building Intelligent Agents with Microsoft Foundry IQ @ Microsoft AI Tour São Paulo (Feb 11) #322 - GitHub, accessed April 8, 2026, https://github.com/orgs/microsoft-foundry/discussions/322
Connect to MCP Server Endpoints for agents - Microsoft Foundry, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/model-context-protocol
Azure MCP Server - Microsoft Foundry Tools, accessed April 8, 2026, https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/tools/azure-foundry
Announcing Foundry MCP Server (preview) in the cloud, speeding up AI development with Microsoft Foundry - Microsoft Developer Blogs, accessed April 8, 2026, https://devblogs.microsoft.com/foundry/announcing-foundry-mcp-server-preview-speeding-up-ai-dev-with-microsoft-foundry/
Service Limits for Tiers and SKUs - Azure AI Search, accessed April 8, 2026, https://docs.azure.cn/en-us/search/search-limits-quotas-capacity
Azure AI Search pricing, accessed April 8, 2026, https://azure.microsoft.com/en-us/pricing/details/search/
Azure AI Search: Features, Best Practices, and Pricing Explained - ITMAGINATION, accessed April 8, 2026, https://www.itmagination.com/technologies/azure-ai-search
How do I see costs for Azure OpenAI? - Microsoft Learn, accessed April 8, 2026, https://learn.microsoft.com/en-my/answers/questions/5546755/how-do-i-see-costs-for-azure-openai
Azure OpenAI Service - Pricing, accessed April 8, 2026, https://azure.microsoft.com/en-us/pricing/details/azure-openai/
