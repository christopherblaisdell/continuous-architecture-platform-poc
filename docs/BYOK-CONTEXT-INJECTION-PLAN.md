# Foundry Context Injection Plan — Making the NovaTrek Custom Model Knowledge-Aware

**Status:** Draft (Research Phase Complete)
**Date:** 2026-04-09
**Last Updated:** 2026-04-09
**Related:** [Option D — Hybrid Architecture](../sites/ai-evaluation-2/docs/evidence/option-d-hybrid-architecture.md), [Foundry IQ Comparison](../sites/ai-evaluation-2/docs/evidence/foundry-iq-comparison.md), [Context Injection Controls](../sites/ai-evaluation-2/docs/evidence/context-injection-controls.md), [BYOK POC Validation](../sites/ai-evaluation-2/docs/evidence/option-d-poc-validation.md)

---

## Problem Statement

The company is moving forward with a custom model in Azure AI Foundry. Under Option D (Hybrid), this model is consumed via Copilot's BYOK mechanism — but the model itself needs **domain-specific context** to produce architecture-grounded answers.

Currently the BYOK endpoint (`oai-novatrek-poc`) is a vanilla GPT-4o deployment. When selected in Copilot, it receives whatever context Copilot's orchestration layer sends (instruction files, workspace index results, conversation history) — but **on the Azure side, the model has no knowledge base, no vector index, no retrieval pipeline**. It cannot autonomously pull in architecture standards, cross-repo ADRs, or historical solution designs.

The goal: **build the server-side knowledge pipeline so the Foundry model delivers domain-specialized answers that justify the custom model investment over Copilot's built-in models.**

### The Architecture Challenge

Copilot sends standard OpenAI Chat Completions API requests to the BYOK endpoint:

```
Copilot (VS Code) → POST https://oai-novatrek-poc.openai.azure.com/openai/v1/chat/completions
                     { messages: [...], model: "gpt-4o" }
```

A vanilla Azure OpenAI deployment just runs the model against those messages. To inject knowledge, we need one of these architectures:

**~~Architecture A — Azure OpenAI "On Your Data"~~ ELIMINATED**
```
Copilot → Azure OpenAI + data_sources config → Azure AI Search index → RAG-augmented response
```
ELIMINATED: On Your Data is **deprecated and approaching retirement** (confirmed via deep research 2026-04-09). Microsoft has stopped onboarding new models. Once current model versions (GPT-4o, GPT-4.1) retire, all On Your Data API endpoints stop functioning. Additionally, function calling and `data_sources` are mutually exclusive — the model cannot use tools while grounding on data. **Do not build on this path.**

**Architecture B — Foundry Agent + Foundry IQ Knowledge Base**
```
Copilot → Translation proxy → Foundry Agent Service (Conversations API) → Agent calls knowledge_base_retrieve MCP tool → Foundry IQ agentic retrieval → Azure AI Search → Response
```
This is Microsoft's recommended path forward (replacing On Your Data). Foundry Agents use the Conversations API (not Chat Completions), so a translation layer is still needed for BYOK compatibility. However, the agentic retrieval pipeline is the most sophisticated option — it plans queries, decomposes complex questions into subqueries, runs parallel searches, applies semantic reranking, and returns citation-backed answers.

**Architecture C — Proxy with RAG Middleware**
```
Copilot → Azure Function / APIM proxy → Extract query → Search Azure AI Search → Prepend context to system message → Forward to Azure OpenAI → Response
```
This is the most flexible approach — the proxy can implement any retrieval strategy and the model receives contextually-enriched prompts via standard Chat Completions. No dependency on Foundry Agent Service (still preview). Uses Azure AI Search directly.

**Architecture D — MCP Bridge to Foundry IQ**
```
Copilot → BYOK model (receives Copilot context natively)
   +
Copilot → Local MCP server → HTTP call to Foundry IQ MCP endpoint → Agentic retrieval → Results injected as tool context
```
Foundry IQ knowledge bases expose a native MCP endpoint: `{search_endpoint}/knowledgebases/{kb_name}/mcp?api-version=2025-11-01-preview`. A local MCP server can call this endpoint and expose the `knowledge_base_retrieve` tool to Copilot. This keeps the BYOK endpoint simple (no proxy needed), retrieval happens client-side via MCP, and it leverages Foundry IQ's full agentic retrieval pipeline.

---

## Phase 1 Research Findings (Completed 2026-04-09)

### Block A: Foundry IQ — Key Findings

| Question | Finding |
|----------|---------|
| **Status** | **Public preview** (no SLA, not recommended for production). Last updated Feb 2026. |
| **GitHub repo indexing** | **NOT supported directly.** Supported knowledge sources: Azure Blob Storage, SharePoint (indexed or remote), OneLake, web (Bing), and existing search indexes. Content must be staged in Blob Storage or a search index first. |
| **Chunking for YAML/Java** | Foundry IQ uses Azure AI Search's integrated vectorization underneath. Supported blob formats include JSON, Markdown, XML, and plain text — YAML is not explicitly listed but would be indexed as plain text. Custom skillsets can pre-process before indexing. |
| **API surface** | REST API + Python SDK (`azure-ai-projects>=2.0.0`). The `KnowledgeBaseRetrievalClient` class provides `retrieve()`. MCP endpoint also available for agent integration. |
| **MCP endpoint** | Native MCP support: `{search_endpoint}/knowledgebases/{kb_name}/mcp?api-version=2025-11-01-preview`. Exposes `knowledge_base_retrieve` tool. Used by Foundry Agent Service but potentially callable from local MCP servers. |
| **Authentication** | DefaultAzureCredential, managed identities, RBAC. Search service needs system-assigned managed identity. User needs Azure AI User + Azure AI Project Manager roles. |
| **Supported LLMs** | GPT-4o, GPT-4o-mini, GPT-4.1, GPT-4.1-nano, GPT-4.1-mini, GPT-5, GPT-5-nano, GPT-5-mini (for query planning / answer synthesis) |
| **Retrieval reasoning effort** | Three levels: `minimal` (no LLM, cheapest), `low` (default, LLM query planning), `medium` (maximal LLM processing, most accurate) |
| **Cost** | Free tier available for Azure AI Search + free token allocation for agentic retrieval POC. Query planning LLM calls are billable at standard Azure OpenAI rates. |
| **Components** | Knowledge base → knowledge sources → agentic retrieval pipeline. All built on top of Azure AI Search. |
| **Relationship** | Part of a trio: **Foundry IQ** (enterprise data), **Fabric IQ** (analytics/Power BI), **Work IQ** (M365 collaboration). Each standalone but composable. |

### Block B: Azure OpenAI "On Your Data" — Key Findings

| Question | Finding |
|----------|---------|
| **Status** | **DEPRECATED AND APPROACHING RETIREMENT.** Microsoft stopped onboarding new models. |
| **Migration path** | Foundry Agent Service with Foundry IQ is the official replacement. |
| **Critical limitation** | Function calling and `data_sources` are **mutually exclusive** — the model cannot use tools while grounding on data. |
| **Supported file types** | .txt, .md, .html, .docx, .pptx, .pdf — NO .yaml, .java, .puml |
| **Architecture A verdict** | **ELIMINATED.** Building on a deprecated platform with known retirement timeline is not viable. |

### Block C: Azure AI Search Knowledge Sources — Key Findings

| Question | Finding |
|----------|---------|
| **GitHub connector** | **No built-in GitHub connector.** Must sync content to Blob Storage first (GitHub Actions, scripts, or manual). |
| **Supported knowledge source types** | `searchIndex` (wraps existing index), `azureBlob` (generates indexer pipeline), `indexedOneLake`, `indexedSharePoint`, `remoteSharePoint`, `webParameters` (Bing) |
| **Blob indexer file types** | CSV, EML, EPUB, GZ, HTML, JSON, KML, **Markdown**, Office formats, PDF, **plain text**, RTF, **XML**, ZIP |
| **YAML handling** | Not explicitly listed. Can be indexed as plain text (`.txt` parsing mode). Custom skillsets (Azure Functions) can pre-process YAML → Markdown or JSON before indexing. |
| **Markdown parsing** | Dedicated Markdown parsing mode available — heading-aware chunking. Ideal for ADRs and solution designs. |
| **Integrated vectorization** | Supported. Configurable chunk sizes: 256, 512, 1024 (default), 1536 tokens. |
| **Free tier** | 50MB storage, 3 indexes — sufficient for POC with selective content. |
| **Content pipeline** | GitHub repo → (sync script/GH Actions) → Azure Blob Storage → Azure AI Search blob indexer → search index → knowledge source → knowledge base |
| **Index refresh** | Built-in change detection via blob metadata timestamps. Supports scheduled or on-demand re-indexing. |

### Block D: Proxy/MCP Architecture — Key Findings

| Question | Finding |
|----------|---------|
| **MCP over HTTP** | Foundry IQ's MCP endpoint is HTTP-based. A local MCP server can act as a bridge: receive stdio MCP calls from Copilot → translate to HTTP calls to Foundry IQ's MCP endpoint → return results. |
| **Foundry Agent MCP integration** | Foundry Agent Service creates a `RemoteTool` connection to the knowledge base MCP endpoint using `ProjectManagedIdentity` auth. The agent then calls `knowledge_base_retrieve` natively. |
| **Per-request headers limitation** | Foundry Agent Service does NOT support per-request headers for MCP tools in preview. Headers set in agent definitions apply to all invocations. |
| **Chat Completions compatibility** | Foundry Agents use the Conversations API (`openai_client.conversations.create()` + `openai_client.responses.create()`), NOT Chat Completions. A translation layer is needed for BYOK. |
| **Azure Function cold start** | Consumption plan has cold starts (1-5s). Premium plan eliminates cold start. For BYOK proxy, latency matters — Premium or pre-warmed instances recommended. |

### Research Summary: Revised Architecture Recommendations

| Architecture | Viability | Recommended? | Key Advantage | Key Risk |
|-------------|-----------|-------------|---------------|----------|
| ~~A: On Your Data~~ | **DEAD** | NO | N/A — deprecated | Retirement timeline |
| B: Foundry Agent | Viable but complex | MAYBE (Phase 4) | Full agentic retrieval, Microsoft's strategic direction | Preview-only, needs translation layer, complex auth |
| C: RAG Proxy | **Viable** | YES (for POC) | Simplest server-side path, standard APIs, no preview dependencies | Custom code to maintain, no built-in citation support |
| D: MCP Bridge | **Viable** | YES (recommended) | No proxy needed, leverages Copilot's native MCP, can use Foundry IQ MCP endpoint | Client-side injection (depends on Copilot MCP behavior), Foundry IQ in preview |

**Recommended path: Architecture D (MCP Bridge) with Phase 4 upgrade to Architecture B (Foundry Agent) when it reaches GA.**

Architecture D is the lowest-friction option for POC: no proxy, no translation layer, uses Copilot's existing MCP infrastructure, and can optionally connect to Foundry IQ's MCP endpoint for agentic retrieval. Architecture C (RAG Proxy) is the fallback if MCP injection proves insufficient for the use case.

---

## Plan: Phased Implementation

### Phase 1: Deep Research (COMPLETE)

| Step | Action | Status | Key Finding |
|------|--------|--------|-------------|
| 1.1 | **Research Foundry IQ + GitHub repo indexing** | COMPLETE | Public preview, no direct GitHub indexing — must stage in Blob Storage. MCP endpoint available. Free tier for POC. |
| 1.2 | **Research Azure OpenAI "On Your Data" with BYOK** | COMPLETE | **DEPRECATED.** Approaching retirement. Architecture A eliminated. |
| 1.3 | **Research Azure AI Search GitHub connector** | COMPLETE | No built-in connector. Blob indexer supports Markdown, JSON, XML, plain text. Must sync repo content to Blob Storage. |
| 1.4 | **Research Foundry Agent as Chat Completions proxy** | COMPLETE | Uses Conversations API (not Chat Completions). Translation layer needed. Preview only. |
| 1.5 | **Evaluate architecture options (A-D)** | PENDING | Architecture A eliminated. Recommended: D (MCP Bridge) for POC, with C (RAG Proxy) as fallback. |

### Phase 2: Index Architecture Content in Azure AI Search

Regardless of which architecture is selected, the content needs to be indexed.

| Step | Action | Detail |
|------|--------|--------|
| 2.1 | **Provision Azure AI Search** | Deploy Basic tier ($73/mo) or Free tier (50MB, 3 indexes) for POC. Deploy via Bicep alongside existing `ai-poc.bicep` |
| 2.2 | **Sync GitHub repo content to indexable storage** | Options: (a) GitHub Actions pushes to Azure Blob Storage on commit, (b) Azure DevOps pipeline, (c) manual sync script. Content: OpenAPI specs, ADRs, metadata YAML, solution designs, Markdown docs |
| 2.3 | **Configure integrated vectorization** | Set up text splitting + embedding pipeline. Custom chunking profiles: heading-aware for Markdown, dereference-then-chunk for OpenAPI YAML, AST-aware for Java |
| 2.4 | **Build custom skillset for OpenAPI specs** | Azure AI Search custom skill (Azure Function) that runs `$ref` dereferencing before chunking — solves the dead-pointer problem |
| 2.5 | **Create search index schema** | Fields: `content`, `content_vector`, `source_file`, `file_type`, `service_name`, `domain`, `last_modified`. Filterable by service and domain for scoped retrieval |
| 2.6 | **Configure index refresh pipeline** | GitHub Actions workflow: on push to main → sync changed files → trigger re-indexing. Target: under 5 minutes from commit to searchable |
| 2.7 | **Validate index quality** | Run test queries against the index: "What is the check-in orchestration pattern?", "What does ADR-005 say about default fallback?", "What events does svc-check-in produce?" — verify relevant chunks are returned |

### Phase 3: Build the Context Injection Layer

Based on the architecture selected in Phase 1, build the middleware that connects the indexed content to the BYOK model.

#### ~~Architecture A (On Your Data)~~ — ELIMINATED

Azure OpenAI "On Your Data" is deprecated and approaching retirement. Do not build on this path. See Research Findings Block B above.

#### If Architecture C (Proxy with RAG Middleware):

| Step | Action | Detail |
|------|--------|--------|
| 3C.1 | **Deploy Azure Function as smart proxy** | Receives Chat Completions request, extracts the user's latest message, queries Azure AI Search, prepends top-K results to the system message, forwards enriched request to Azure OpenAI |
| 3C.2 | **Implement query extraction** | Parse the messages array to identify the user's intent; use the last user message + conversation summary for retrieval query |
| 3C.3 | **Implement context injection** | Prepend retrieved chunks as a `[ARCHITECTURE CONTEXT]` block in the system message. Include source file paths and relevance scores |
| 3C.4 | **Update BYOK baseUrl** | Point to the Azure Function URL |
| 3C.5 | **Implement context budget management** | Track token usage: system prompt + injected context + user messages must not exceed the model's context window. Truncate lowest-relevance chunks if needed |
| 3C.6 | **Add observability** | Log queries, retrieved chunks, and response quality metrics to Application Insights for monitoring and tuning |

#### If Architecture D (MCP Bridge to Foundry IQ) — RECOMMENDED:

| Step | Action | Detail |
|------|--------|--------|
| 3D.1 | **Build MCP server for Azure AI Search / Foundry IQ** | Python stdio MCP server that exposes tools: `search_architecture(query)`, `get_service_specs(svc_name)`, `search_adrs(query)`, `get_domain_context()`. Can call Azure AI Search directly OR the Foundry IQ MCP endpoint (`{search_endpoint}/knowledgebases/{kb_name}/mcp?api-version=2025-11-01-preview`) |
| 3D.2 | **Implement retrieval client** | Option 1: Use `azure-search-documents` Python SDK to query the search index directly. Option 2: Use HTTP calls to the Foundry IQ MCP endpoint to leverage agentic retrieval (query planning, decomposition, semantic reranking). Start with Option 1 (simpler), upgrade to Option 2 when Foundry IQ knowledge base is provisioned |
| 3D.3 | **Configure MCP server in VS Code** | Add to `.vscode/mcp.json` so it's available alongside the existing Vikunja MCP server. Authenticate via API key (local dev) or `DefaultAzureCredential` (production) |
| 3D.4 | **Respect MCP response limits** | Implement smart truncation: return summaries with file paths, not full documents. Include relevance scores and source citations. Paginate if result set is large |
| 3D.5 | **Test with BYOK model** | Verify that when using the NovaTrek BYOK model in Copilot Agent Mode, MCP tool results are injected into the context correctly. The BYOK model receives both Copilot's workspace context AND MCP retrieval results |
| 3D.6 | **Add Foundry IQ agentic retrieval** | Once Phase 2 index is working with direct search, create a Foundry IQ knowledge base and switch the MCP server to call the Foundry IQ MCP endpoint. This adds LLM-powered query planning and answer synthesis on top of the search index |

### Phase 4: Foundry Agent Service Integration (When GA)

If Foundry Agent Service reaches GA and the preview limitations (no per-request headers, no Chat Completions compatibility) are resolved, upgrade to the full Architecture B path.

| Step | Action | Detail |
|------|--------|--------|
| 4.1 | **Create Foundry project** | Deploy a Microsoft Foundry project with LLM deployment (GPT-4.1-mini recommended for cost-effective query planning) |
| 4.2 | **Create RemoteTool connection** | Connect the Foundry project to the Foundry IQ knowledge base MCP endpoint using `ProjectManagedIdentity` authentication |
| 4.3 | **Create Foundry Agent** | Deploy an agent with `MCPTool` pointing to the knowledge base. Set `allowed_tools = ["knowledge_base_retrieve"]`. Configure instructions optimized for architecture knowledge retrieval |
| 4.4 | **Evaluate Conversations API path** | Test if VS Code Copilot can interact with the Foundry Agent via the Conversations API, or if a Chat Completions translation proxy is still needed |
| 4.5 | **A/B test against MCP Bridge** | Compare Architecture D (MCP Bridge) vs Architecture B (Foundry Agent) on grounding accuracy, citation quality, and latency |
| 4.6 | **Cost analysis** | Track Foundry Agent compute costs (query planning LLM calls, agent hosting) vs the quality improvement over direct MCP Bridge |

### Phase 5: Fine-Tuning (Optional, High Investment)

Only if the model consistently misunderstands domain concepts despite having correct context.

| Step | Action | Detail |
|------|--------|--------|
| 5.1 | **Curate training dataset** | Extract Q&A pairs from existing solution designs, ADR reasoning chains, architecture reviews. Minimum 200 high-quality examples |
| 5.2 | **Format for Azure OpenAI fine-tuning** | JSONL format with system/user/assistant turns. Include instruction-following examples that demonstrate the NovaTrek architectural style |
| 5.3 | **Submit fine-tuning job** | Use Azure OpenAI fine-tuning API. Evaluate on a held-out test set of 50 architecture questions |
| 5.4 | **Deploy fine-tuned model** | Replace the base GPT-4o deployment. Same endpoint URL — zero BYOK config changes |
| 5.5 | **Regression testing** | Test fine-tuned model on general coding/architecture tasks to verify domain training didn't harm general capability |

---

## Deep Research Questions — ANSWERED (2026-04-09)

Research findings are compiled in the "Phase 1 Research Findings" section above. All 21 questions across 4 blocks have been investigated. Key answers summarized below.

### Block A: Foundry IQ — Answered

1. **Status**: Public preview. No SLA. Not recommended for production.
2. **GitHub indexing**: NOT supported directly. Must stage in Blob Storage or wrap an existing search index.
3. **Chunking**: Uses Azure AI Search integrated vectorization. YAML treated as plain text. Custom skillsets available for pre-processing.
4. **API surface**: REST + Python SDK (`azure-ai-projects>=2.0.0`). `KnowledgeBaseRetrievalClient.retrieve()`. MCP endpoint available.
5. **MCP authentication**: Foundry IQ MCP endpoint uses managed identities and RBAC. Local MCP servers would need `DefaultAzureCredential` or API key.
6. **Cost**: Free tier available. Query planning LLM calls billed at standard Azure OpenAI rates.

### Block B: Azure OpenAI "On Your Data" — Answered

1. **Proxy feasibility**: Moot — On Your Data is DEPRECATED.
2. **Response schema**: Moot.
3. **Latency**: Moot.
4. **Semantic ranking**: Moot.
5. **Deployment-level config**: Not possible — `data_sources` is per-request only. Additionally, function calling and data_sources are mutually exclusive.

### Block C: Azure AI Search — Answered

1. **GitHub connector**: No built-in connector. Must sync to Blob Storage.
2. **Vectorization cost**: Embedding generation uses Azure OpenAI embedding model — pay-per-token. Free tier allocations available.
3. **Custom skillsets**: Yes — Azure Functions can be used as custom skills for $ref dereferencing, YAML transformation, etc.
4. **Free tier**: 50MB, 3 indexes — sufficient for POC with selective high-value content.
5. **Refresh propagation**: Near real-time after indexer runs. Supports on-demand and scheduled indexing.

### Block D: Proxy Architecture — Answered

1. **Azure Function runtime**: Consumption plan has cold starts (1-5s). Premium plan or pre-warmed instances recommended for BYOK proxy.
2. **APIM alternative**: APIM could work for request transformation but would not have built-in RAG policy. Custom policy needed.
3. **Open-source proxy**: Multiple projects exist (`azure-search-openai-demo` is the reference architecture). No production-ready BYOK-specific proxy.
4. **Security**: Proxy adds a hop — API keys must be managed in Key Vault. Logging must mask sensitive content.
5. **Co-location**: Yes — deploy in same region (eastus2) for lowest latency.

---

## Architecture Decision Matrix (Updated Post-Research)

| Criteria | ~~A: On Your Data~~ | B: Foundry Agent | C: RAG Proxy | D: MCP Bridge |
|----------|---------------------|------------------|-------------|----------------|
| **Status** | **ELIMINATED** | Preview only | Production-ready | Production-ready (Search) + Preview (Foundry IQ) |
| Copilot BYOK compatible | N/A | Needs translation proxy | Needs proxy | Native (no proxy) |
| Infrastructure | N/A | Foundry project + Agent Service + AI Search | Azure Function + AI Search | Local MCP server + AI Search |
| Latency added | N/A | High (agent + search + LLM planning) | Medium (proxy + search) | Low (MCP is pre-fetched by Copilot) |
| Server-side retrieval | N/A | Yes — agent-managed with citations | Yes — injected in system prompt | No — client-side injection via MCP tools |
| Citation support | N/A | Built-in (Foundry Agent) | Custom implementation | Custom implementation |
| Complexity | N/A | High (auth, managed identity, translation layer) | Medium (Azure Function + search client) | **Low** (Python MCP server + search client) |
| Cost | N/A | AI Search + Foundry compute + agent hosting | AI Search + Function | **AI Search only** |
| Cross-repo support | N/A | Via knowledge base (multi-source) | Via index | Via index |
| Microsoft strategic alignment | Deprecated | **Highest** (official replacement for On Your Data) | Neutral (custom solution) | Good (uses AI Search + MCP standard) |
| Upgrade path | None | Already the target | Can migrate to B or D | Can add Foundry IQ agentic retrieval (step 3D.6) |

**RECOMMENDATION: Architecture D (MCP Bridge) for POC, with upgrade path to Architecture B (Foundry Agent) when GA.**

---

## Implementation Sequence

```
COMPLETE:   Phase 1 (1.1 - 1.4)     — Deep research (Architecture A eliminated, D recommended)
NEXT:       Phase 1.5               — Architecture selection decision (prompt-me)
Week 1:     Phase 2 (2.1 - 2.7)     — Index content in Azure AI Search
Week 2:     Phase 3D (3D.1 - 3D.6)  — Build MCP Bridge + optional Foundry IQ agentic retrieval
Week 2:     Validate                 — Test queries, measure grounding, tune
Week 3+:    Phase 4 (if Foundry GA)  — Foundry Agent Service integration
Later:      Phase 5 (if needed)      — Fine-tuning
```

---

## Cost Estimates

| Component | Monthly Cost | Notes |
|-----------|-------------|-------|
| Azure AI Search (Free tier) | $0 | 50MB, 3 indexes — sufficient for POC |
| Azure AI Search (Basic tier) | $73 | Production: 2GB, 15 indexes |
| Azure OpenAI GPT-4o | Pay-per-token | $0 idle; ~$0.005/1K input tokens, $0.015/1K output tokens |
| Azure Function (proxy) | ~$0 - $5 | Consumption plan: first 1M executions free |
| Foundry IQ (Phase 4) | Variable | Query planning LLM calls + compute |
| Fine-tuning (Phase 5) | $50-500 one-time | Training job + hosting fine-tuned model |

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Context hit rate | > 80% | % of queries where injected context is relevant to the question |
| Grounding accuracy | > 90% | % of model claims that match actual workspace content |
| Query latency | < 5s added | End-to-end time from prompt to first token |
| False retrieval rate | < 10% | % of queries where irrelevant content is injected |
| Cost per architecture query | < $0.05 | Azure consumption per query |

---

## Risks (Updated Post-Research)

| Risk | Impact | Mitigation |
|------|--------|-----------|
| ~~Copilot rejects proxy responses~~ | ~~Blocks Architecture A/C~~ | Architecture A eliminated. Architecture C tested separately from A. |
| Foundry IQ stays in preview, no GA timeline | Blocks Phase 4 upgrade | Architecture D (MCP Bridge) works with Azure AI Search directly — Foundry IQ is optional enhancement |
| Azure AI Search chunking is poor for YAML/PlantUML | Reduces retrieval quality | Custom skillset (Azure Function) for pre-processing. YAML → Markdown transformation. PlantUML → structured text extraction |
| MCP tool invocation is unreliable with BYOK model | Degrades Architecture D | Copilot should handle MCP tools regardless of model choice. If BYOK model doesn't trigger tools, fall back to Architecture C (proxy) |
| Blob Storage sync adds latency to content freshness | Stale search results | GitHub Actions workflow triggers on push to main — target < 5 minutes from commit to searchable |
| Free tier AI Search hits 50MB limit | Cannot index all content | Prioritize high-value content (specs, ADRs, metadata, solutions). Upgrade to Basic ($73/mo) if needed |
| Over-indexing noisy content | Floods context with irrelevant chunks | Scope index to high-value content: specs, ADRs, metadata YAML, solution designs |
| Fine-tuning degrades general capability | Model becomes domain-narrow | Maintain base model as fallback; A/B test before switching |

---

## Appendix: Current BYOK Configuration

```json
// .vscode/settings.json (gitignored — contains API key)
{
  "oaicopilot.models": [
    {
      "id": "gpt-4o",
      "owned_by": "azure-novatrek",
      "displayName": "NovaTrek GPT-4o (Azure BYOK)",
      "baseUrl": "https://oai-novatrek-poc.openai.azure.com/openai/v1",
      "context_length": 128000,
      "max_tokens": 4096,
      "temperature": 0,
      "headers": { "api-key": "***" }
    }
  ]
}
```

## Appendix: Existing Infrastructure

- **Azure OpenAI resource**: `oai-novatrek-poc` in `rg-novatrek-ai-poc` (eastus2)
- **Bicep templates**: `infra/ai-poc.bicep`, `infra/modules/azure-openai.bicep`
- **Deploy script**: `infra/deploy-ai-poc.sh`
- **Existing MCP server**: `scripts/mcp-vikunja-server.py` (6 tools, stdio transport, YAML file parsing)

## Appendix: Content to Index

| Content Type | Location | File Count | Priority | Notes |
|-------------|----------|-----------|----------|-------|
| OpenAPI specs | `architecture/specs/svc-*.yaml` | 19 | HIGH | Dereference `$ref` pointers before indexing |
| Architecture decisions | `decisions/ADR-*.md` | 14 | HIGH | Heading-aware chunking works well |
| Solution designs | `architecture/solutions/` | 4+ | HIGH | Full solution documents with sub-sections |
| Metadata YAML | `architecture/metadata/*.yaml` | 10 | HIGH | Capabilities, events, tickets, cross-service calls |
| AsyncAPI event specs | `architecture/events/*.yaml` | 6 | MEDIUM | Event schemas and channels |
| PlantUML diagrams | `architecture/diagrams/` | 50+ | MEDIUM | Need companion Markdown or structured extraction |
| Java source code | `source-code/` (if present) | Variable | MEDIUM | Tree-sitter-style chunking |
| Portal documentation | `portal/docs/` | 30+ | LOW | Generated content — index selectively |
| Evaluation documents | `sites/ai-evaluation-2/docs/` | 20+ | LOW | Meta-content about the evaluation itself |
