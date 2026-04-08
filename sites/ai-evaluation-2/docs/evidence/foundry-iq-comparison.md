<!-- CONFLUENCE-PUBLISH -->

# What Does Foundry IQ Actually Require?

## Context

A stakeholder proposed that the evaluation's "build vs leverage" framing mischaracterizes the alternative. The argument: Foundry IQ is a managed service, not a self-managed pipeline, so the real comparison is "buy Foundry IQ vs buy Copilot" — two managed offerings with different levels of control.

This is a fair reframe that deserves a substantive response. Rather than dismissing it, this page inventories what standing up Foundry IQ actually requires — based on Microsoft's own documentation — so the comparison is grounded in evidence rather than labels.

## What Is Foundry IQ?

Foundry IQ is a managed knowledge layer built on Azure AI Search's agentic retrieval engine. It lets agents access enterprise content through knowledge bases that orchestrate chunking, vectorization, retrieval, and permission enforcement.

Key capabilities (from [Microsoft's documentation](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-foundry-iq)):

- Connect one knowledge base to multiple agents
- Automate document chunking, vector embedding generation, and metadata extraction
- Issue keyword, vector, or hybrid queries across indexed and remote knowledge sources
- Use agentic retrieval with an LLM for query planning and parallel search
- Synchronize access control lists (ACLs) and enforce permissions at query time
- Expose knowledge bases via MCP endpoints for agent integration

## Production Readiness

!!! warning "Public Preview — No SLA"
    As of April 2026, Foundry IQ is in **public preview** — and to his credit, Troy was upfront about this, noting the preview status when describing SharePoint access control synchronization.

    Microsoft's documentation states: *"This preview is provided without a service-level agreement, and we don't recommend it for production workloads. Certain features might not be supported or might have constrained capabilities."*

    The underlying Azure AI Search service is GA, and individual features like skillsets and scoring profiles are GA. But the Foundry IQ orchestration layer — the knowledge base abstraction, agentic retrieval engine, and MCP endpoint exposure that make it a coherent "managed" product — is in preview.

    This distinction matters: the "buy vs buy" reframe depends on Foundry IQ being a stable, production-ready product you can adopt with confidence. A preview service with no SLA is closer to "bet on" than "buy."

## What "Buying" Foundry IQ Actually Requires

The table below compares the operational requirements of both approaches, using GitHub Copilot's workspace indexing as the baseline and Foundry IQ as the proposed alternative.

| Activity | GitHub Copilot (Platform-Native) | Foundry IQ (Managed RAG) |
|----------|----------------------------------|--------------------------|
| **Provision infrastructure** | Install VS Code extension | Provision Azure AI Search service (select tier: $73–$1,962/mo), create Microsoft Foundry project, deploy LLM for query planning (gpt-4o/gpt-4.1/gpt-5) |
| **Design knowledge architecture** | Nothing — workspace is the knowledge base | Design knowledge bases, select knowledge sources, write retrieval instructions, choose reasoning effort levels (minimal/low/medium) |
| **Write integration code** | Nothing | Python SDK or REST API calls to create project connections, MCP tool bindings, agent definitions ([see code samples](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/foundry-iq-connect)) |
| **Configure chunking** | Automatic | Custom skillsets for non-standard formats (PlantUML, structured markdown) |
| **Configure relevance tuning** | Automatic | Scoring profiles with freshness functions, boost rules, field weighting |
| **Set up access control** | GitHub repository permissions | Azure RBAC (Azure AI User, Azure AI Project Manager, Search Index Data Reader roles), ACL synchronization per knowledge source, Entra identity configuration |
| **Set up data refresh** | Incremental workspace indexing (automatic) | Configure indexer schedules per knowledge source for incremental refresh |
| **Manage costs** | $39/seat/month (all-inclusive) | Azure AI Search tier + Azure OpenAI tokens for query planning + Foundry Agent Service + overage tokens for agentic retrieval |
| **Debug failures** | VS Code error messages | Troubleshoot auth failures (401/403), MCP endpoint errors (400/404), empty result sets, permission mismatches across services ([troubleshooting guide](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/foundry-iq-connect#troubleshooting)) |
| **Production SLA** | GA with SLA | Public preview — no SLA |

## The "Build on Managed Primitives" Spectrum

The stakeholder's point is valid in one sense: Foundry IQ is less building than a fully self-managed pipeline (no Qdrant to operate, no custom embedding models to train, no vector database capacity planning). It moves the effort up the stack from infrastructure to configuration.

But "managed" does not mean "turnkey." The table above shows that Foundry IQ requires:

- **Infrastructure design decisions** — which Azure AI Search tier, which LLM for query planning, how many knowledge sources
- **Knowledge architecture** — how to organize knowledge bases, what retrieval instructions to write, what reasoning effort level to use
- **Integration development** — Python SDK code to create project connections and bind MCP tools to agents
- **Multi-service debugging** — auth failures span Azure AI Search, Foundry, and Azure OpenAI; each has its own RBAC model
- **Ongoing cost management** — multiple Azure meters instead of one fixed subscription

This is a real reduction in complexity compared to building from scratch. But it is not comparable to "install an extension and start working."

## Interoperability Gap

A critical finding from [Microsoft's FAQ](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/foundry-iq-faq):

> "You can't use Foundry IQ knowledge sources in Copilot, and you can't use Copilot knowledge sources in Foundry IQ."

This means Foundry IQ does not replace Copilot's workspace indexing — it runs alongside it. For IDE-based architecture work, architects would still use Copilot's native indexing (which works today, in GA, with zero configuration). Foundry IQ would serve a separate use case: cross-repository, cross-format knowledge retrieval from outside the IDE.

This raises the question: is the team asking for **a replacement** for Copilot's indexing, or **an addition** to it? If it's an addition, both the cost and complexity are additive — the $39/seat for Copilot plus the Azure AI Search infrastructure for Foundry IQ.

## Where Foundry IQ Has Genuine Advantages

This analysis should not be read as a dismissal. Foundry IQ offers real capabilities that platform-native indexing does not:

| Capability | Why It Matters |
|------------|---------------|
| **Cross-repository knowledge** | Queries across content from multiple Azure, SharePoint, and OneLake sources — not limited to one workspace |
| **Custom chunking per format** | Skillsets can preserve semantic coherence for formats like PlantUML that generic chunking breaks |
| **Scoring profiles with freshness** | Recency-weighted search prevents outdated solutions from ranking equally with current ones |
| **Document-level access control** | Entra identity enforcement means architects only see content they're authorized to access |
| **MCP endpoint exposure** | Any MCP-compatible client can query the knowledge base — not locked to one IDE |
| **Agentic retrieval** | LLM-assisted query planning with 36% higher response quality than single-shot RAG ([Microsoft benchmark](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/foundry-iq-boost-response-relevance-by-36-with-agentic-retrieval/4470720)) |

These capabilities become valuable when the architecture practice's needs outgrow what a single workspace can provide — when retrieval across thousands of documents in multiple formats and repositories is a daily requirement, not a speculative one.

## Recommendation

The evaluation's position is not "Foundry IQ is bad." It is:

1. **For IDE-based architecture generation** (the pilot's primary use case today) — platform-native indexing works, is GA, costs $39/month, and requires zero infrastructure. Foundry IQ does not replace this capability and is not interoperable with it.

2. **For cross-repository knowledge retrieval** (a future need that may emerge) — Foundry IQ is a credible option worth evaluating when that need is concrete and when the service exits preview. Investing in preview infrastructure to solve a problem that hasn't been demonstrated yet compounds two risks.

3. **The framing matters** — calling Foundry IQ "buy" rather than "build" sets expectations that it is turnkey. The evidence shows it requires meaningful design, development, and operational investment. A more accurate framing: "build on managed primitives" — which is genuinely less effort than building from scratch, but not comparable to the zero-config platform-native alternative.

## Sources

- [What is Foundry IQ?](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-foundry-iq) — Microsoft Learn, updated Feb 2026
- [Foundry IQ FAQ](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/foundry-iq-faq) — Microsoft Learn
- [Connect a Foundry IQ Knowledge Base to Foundry Agent Service](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/foundry-iq-connect) — Microsoft Learn, updated Apr 2026
- [What is Azure AI Search?](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search) — Microsoft Learn
- [Foundry IQ: Boost Response Relevance by 36% with Agentic Retrieval](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/foundry-iq-boost-response-relevance-by-36-with-agentic-retrieval/4470720) — Microsoft Tech Community
