<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: https://christopherblaisdell.atlassian.net/wiki/spaces/ARCH/pages/build-vs-leverage -->

# Build vs Leverage: Custom RAG in Context

## When Custom RAG Is the Right Answer

Building a custom Retrieval-Augmented Generation (RAG) pipeline is a well-established pattern when **AI is the product**. Organizations whose core business is delivering AI-powered experiences — search engines, recommendation systems, domain-specific copilots sold to customers — rightfully invest in:

- **Vector databases** (Pinecone, Weaviate, Qdrant) for embedding storage and similarity search
- **Chunking and embedding pipelines** to ingest proprietary corpora
- **Prompt orchestration frameworks** (LangChain, LlamaIndex) to compose retrieval with generation
- **Fine-tuned or distilled models** optimized for their specific domain
- **Evaluation harnesses** (RAGAS, custom benchmarks) to measure retrieval precision and answer quality

This investment is justified because the RAG pipeline *is* the product. The engineering team owns every layer, tunes every parameter, and differentiates on retrieval quality.

## When Custom RAG Reinvents the Wheel

The calculus changes entirely when **AI is a tool** — when the goal is to augment developers and architects working inside an IDE, not to ship an AI product to customers.

For IDE-integrated architecture and coding workflows, the custom RAG approach reconstructs capabilities that already exist natively in modern AI coding platforms:

| RAG Pipeline Component | What You Build | Copilot Native Equivalent |
|------------------------|----------------|---------------------------|
| Document ingestion | Chunking scripts, embedding jobs, scheduled re-indexing | Workspace indexing — automatic, incremental, zero-config |
| Vector store | Pinecone/Weaviate cluster, schema design, capacity planning | Built-in semantic search index (local + cloud) |
| Retrieval | Similarity search queries, re-ranking, context window assembly | `@workspace` — single command retrieves relevant files, symbols, and definitions |
| Context injection | Custom prompt templates stitching retrieved chunks into system prompts | `.github/copilot-instructions.md`, `.instructions.md`, `SKILL.md` — declarative files, no code |
| Behavior configuration | Prompt engineering, agent routing logic, mode switching | `.agent.md` files, custom agent modes, tool restrictions — all workspace-as-code |
| Tool integration | MCP server development, function-calling schemas, tool dispatch | Native MCP support, built-in tools (terminal, file ops, search), extensible via MCP |
| Multi-agent orchestration | Agent framework (CrewAI, AutoGen), coordination logic, state management | Native sub-agents, `Explore` agent, automatic tool delegation |
| Evaluation | Custom benchmarks, A/B testing infrastructure | Direct observation — same IDE, same workflow, immediate feedback |

### The Infrastructure Tax

Every component in the left column requires:

- **Development effort** to build and integrate
- **Operational overhead** to monitor, scale, and maintain
- **Ongoing cost** for compute, storage, and API calls
- **Expertise** in ML infrastructure that may not exist on the architecture team

Option A (GitHub Copilot) delivers all of these capabilities as platform features included in the subscription. No infrastructure to provision, no pipelines to maintain, no embedding jobs to schedule.

## The Core Argument

Custom RAG is the right choice when your organization's competitive advantage depends on retrieval quality and you need full control over every layer of the AI pipeline.

It is the wrong choice when:

1. **The AI platform already indexes your workspace** — Copilot's workspace indexing performs the same function as a RAG retrieval pipeline, automatically and incrementally
2. **Context injection is solved by convention** — instruction files (`.instructions.md`, `copilot-instructions.md`) inject domain knowledge without writing code
3. **The team's expertise is architecture, not ML infrastructure** — time spent maintaining embedding pipelines is time not spent on architecture work
4. **The cost model penalizes complexity** — every additional component (vector DB, embedding service, orchestration layer) adds to TCO with no proportional quality gain over native capabilities

## Implications for This Evaluation

This analysis directly informs two evaluation factors:

- **EF-08 Time to Value**: Option A delivers context-aware AI assistance from day one with declarative configuration. Option B requires building and validating the RAG pipeline before productive use begins.
- **EF-09 Operational Complexity**: Option A adds zero infrastructure. Option B adds vector storage, embedding pipelines, and prompt orchestration as ongoing operational responsibilities.

The dedicated decision page [DD-01 Context and Configuration](dd-01-context-configuration.md) evaluates how each option handles knowledge injection and behavior customization.
