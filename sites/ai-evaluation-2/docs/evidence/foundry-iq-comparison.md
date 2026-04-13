<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2619932980/What+Does+Foundry+IQ+Actually+Require -->

# What Does Foundry IQ Actually Require?

## Context

A stakeholder proposed that the evaluation's "build vs leverage" framing mischaracterizes the alternative. The argument: Foundry IQ is a managed service, not a self-managed pipeline, so the real comparison is "buy Foundry IQ vs buy Copilot" — two managed offerings with different levels of control.

This is a fair reframe that deserves a substantive response. Rather than dismissing it, this page inventories what standing up Foundry IQ actually requires — based on Microsoft's own documentation — so the comparison is grounded in evidence rather than labels.

## What Is Foundry IQ?

Foundry IQ is what Microsoft calls a "managed knowledge layer" — their term for managed retrieval and indexing infrastructure — built on Azure AI Search's agentic retrieval engine. It lets agents access enterprise content through knowledge bases that orchestrate chunking, vectorization, retrieval, and permission enforcement.

Key capabilities (from [Microsoft's documentation](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-foundry-iq)):

- Connect one knowledge base to multiple agents
- Automate document chunking, vector embedding generation, and metadata extraction
- Issue keyword, vector, or hybrid queries across indexed and remote knowledge sources
- Use agentic retrieval with an LLM for query planning and parallel search
- Synchronize access control lists (ACLs) and enforce permissions at query time
- Expose knowledge bases via MCP endpoints for agent integration

## Production Readiness

!!! warning "Public Preview — No SLA"
    As of April 2026, Foundry IQ is in **public preview** — and to their credit, the Foundry team was upfront about this, noting the preview status when describing SharePoint access control synchronization.

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

## What Are We Actually Comparing?

The conversation around Foundry IQ vs Copilot has conflated three separate things. Getting precise about what each platform provides — and what investment is at risk — requires separating them. (See the [Glossary](../reference/glossary.md) for full definitions of each term.)

### Three Layers, Three Portability Questions

| Layer | What it is | Copilot | Foundry IQ | Portable? |
|-------|-----------|---------|------------|-----------|
| **Content** | The architecture artifacts themselves (ADRs, specs, diagrams, YAML) | Files in git repositories | Files in SharePoint, Azure Blob, OneLake, or git | Always portable — these are just files |
| **Customizations** | Behavioral configuration that shapes how the AI agent works (instructions, skills, agent definitions) | Markdown files checked into the repo (`.instructions.md`, `SKILL.md`, `.agent.md`) | Not applicable — Foundry IQ does not provide agent customization | Content is portable (plain Markdown); format is converging on open standards ([SKILL.md](https://agentskills.io), AGENTS.md, MCP) |
| **Retrieval** | The search infrastructure that finds relevant content and feeds it to the LLM | Automatic workspace indexing (zero config, per-workspace, per-client) | Knowledge bases with custom chunking, scoring profiles, agentic retrieval, MCP endpoint | Not portable between platforms — but indexes are derived from content, so switching means rebuilding the index, not losing data |

### What Would Be Lost in a Platform Switch?

A natural question for any AI toolchain investment: if the team commits to one platform's customization model and later needs to switch, what is lost? For Copilot, the answer is:

| Investment | Dead-end risk | Why |
|------------|--------------|-----|
| **Architecture content** (ADRs, specs, designs) | None | Files in git. Any platform can read them. |
| **Instruction files** (`.instructions.md`, `copilot-instructions.md`) | Low and shrinking | The *content* is plain Markdown — transferable to any platform. The *file naming convention* varies by platform, but Roo Code, Cursor, and Claude Code already read Copilot's format. The AGENTS.md / SKILL.md standards are converging across vendors. |
| **Skills** (`SKILL.md`) | Low | Follows an emerging open standard from agentskills.io. Multiple clients already support it. Even if the format diverges, the procedural knowledge inside (templates, checklists, workflow steps) is plain text. |
| **Agent definitions** (`.agent.md`) | Moderate | Currently Copilot-specific format. But the *content* (behavioral rules, tool restrictions) can be expressed in any agent framework. Migration would require reformatting, not rewriting. |
| **MCP server configurations** | None | MCP is an open standard (Anthropic). MCP servers work with Copilot, Cursor, Windsurf, Claude Desktop, and Foundry IQ. |
| **Workspace index** | None — there is no investment | Workspace indexing is automatic and zero-config. There is nothing to lose because there is nothing to build. Each platform rebuilds its own index from the source files. |

The total dead-end risk is a **reformatting cost** — not a data loss or rebuild. The architecture content, the procedural knowledge inside skills, and the behavioral rules in agent definitions all survive a platform switch. What changes is the file naming and activation syntax, which is converging toward open standards.

### Foundry IQ Is Additive, Not a Replacement

[Microsoft's FAQ](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/foundry-iq-faq) confirms that Foundry IQ and Copilot serve different layers:

> "The supported data sources differ by platform and aren't interoperable. In other words, you can't use Foundry IQ knowledge sources in Copilot, and you can't use Copilot knowledge sources in Foundry IQ."

This is not a trivial limitation. It means:

- **Architects would have a split workflow.** Copilot handles workspace-scoped generation (writing ADRs, analyzing specs, producing diagrams). Foundry IQ handles cross-repository retrieval ("which solutions touch step-up auth and PCI?"). These are separate systems with separate query experiences.
- **The "invest in knowledge once" promise has a gap.** Content indexed in Foundry IQ does not enhance Copilot's workspace context. Content indexed by Copilot is not searchable by Foundry IQ. Each system maintains its own retrieval layer over the same content.

### Can MCP Bridge the Gap?

The Foundry team's proposal emphasizes that Foundry IQ exposes an MCP endpoint — and since Copilot consumes MCP servers, this should bridge the interoperability gap. The research shows this is partially true:

**What works:**

- Foundry IQ exposes each knowledge base at `{endpoint}/knowledgebases/{kb}/mcp?api-version=2025-11-01-preview`
- VS Code Copilot supports HTTP MCP servers via `.vscode/mcp.json` with `"type": "http"`
- The [Foundry IQ FAQ confirms](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/foundry-iq-faq) that knowledge bases can be called from *"any application that supports the knowledge base APIs from Azure AI Search"*

**What doesn't bridge today:**

- The MCP connection uses `ProjectManagedIdentity` authentication — a Foundry-specific auth type. [Microsoft's docs note](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/foundry-iq-connect): *"The RemoteTool category and ProjectManagedIdentity authentication type are specific to Microsoft Foundry project connections."*
- VS Code's MCP server configuration does not natively support Foundry's managed identity auth flow
- Microsoft explicitly states the two systems are "not interoperable"

**What could work with additional development:**

- A thin MCP wrapper server that authenticates to the Foundry IQ knowledge base API using Azure credentials and re-exposes the results as a standard MCP tool for VS Code
- This is viable but is custom integration development — exactly the kind of "build" work the evaluation is assessing

**Bottom line:** The MCP bridge is architecturally sound but not turnkey. Making Foundry IQ knowledge available inside Copilot's chat would require writing and maintaining a custom MCP server adapter. This is a solvable problem, but it is engineering work — not configuration.

NOTE: This auth gap is not Copilot-specific. The `ProjectManagedIdentity` credential type is a Foundry-internal authentication mechanism — no IDE-based agent (Copilot, Cursor, Roo Code, Windsurf, Claude Code) natively supports it. The only turnkey client for Foundry IQ is Microsoft's own Foundry Agent Service, which runs in the cloud, not in an IDE. Any IDE client would require the same custom MCP adapter to bridge the auth gap.

## The Undefined Workload Problem

The distinction between generation and retrieval workloads is valid — but it surfaces a more fundamental gap: **the team has not defined what retrieval workload it actually needs.**

The number "4,100+ docs" appears in the conversation as the scale of the cross-repository retrieval problem. But before investing in infrastructure to search 4,100 documents, three questions need answers:

### 1. What content actually requires cross-repository retrieval?

Not all 4,100 documents are equally relevant to architecture work. A content audit would likely reveal that the daily retrieval need is concentrated in a much smaller set: active ADRs, recent solution designs, current OpenAPI specs, and a handful of reference standards. If 80% of the value comes from 500 documents, the infrastructure requirements change dramatically.

### 2. Can the relevant content be rationalized into the workspace?

Content that lives in SharePoint, Confluence, or vendor portals today may be there for historical reasons — not because those are the right locations. A git-based workflow where architecture content is consolidated into repositories has a compounding advantage: every tool (Copilot, Cursor, Roo Code, Claude Code) can index it automatically, with zero infrastructure. Migrating content to git is a one-time effort that pays off across every future tool.

This is not an argument to move everything to git — vendor docs and regulatory materials have legitimate reasons to stay where they are. But architecture-owned content (ADRs, specs, solution designs, capability maps) can and should live where the tools natively ingest it.

### 3. Is the retrieval problem daily or occasional?

If "which solutions touch step-up auth?" is asked weekly, that is a search problem worth solving with infrastructure. If it is asked during quarterly architecture reviews, a manual search or a curated index may be sufficient. The frequency determines whether the infrastructure investment is justified.

Until these questions are answered, the debate between Copilot and Foundry IQ for retrieval is premature. The evaluation recommends **defining the retrieval workload concretely** before selecting a tool to serve it.

## Where Foundry IQ Has Genuine Advantages

This analysis should not be read as a dismissal. Foundry IQ offers real capabilities that platform-native indexing does not:

| Capability | Why It Matters |
|------------|---------------|
| **Cross-repository knowledge** | Queries across content from multiple Azure, SharePoint, and OneLake sources — not limited to one workspace |
| **Custom chunking per format** | Skillsets can preserve semantic coherence for formats like PlantUML that generic chunking breaks |
| **Scoring profiles with freshness** | Recency-weighted search prevents outdated solutions from ranking equally with current ones |
| **Document-level access control** | Entra identity enforcement means architects only see content they're authorized to access |
| **MCP endpoint exposure** | Knowledge bases are exposed as MCP endpoints — any MCP-compatible client can query them, though bridging to Copilot requires a custom adapter (see [Can MCP Bridge the Gap?](#can-mcp-bridge-the-gap) above) |
| **Agentic retrieval** | LLM-assisted query planning with 36% higher response quality than single-shot RAG ([Microsoft benchmark](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/foundry-iq-boost-response-relevance-by-36-with-agentic-retrieval/4470720)) |

These capabilities become valuable when the architecture practice's needs outgrow what a single workspace can provide — when retrieval across thousands of documents in multiple formats and repositories is a daily requirement, not a speculative one.

## Recommendation

The evaluation's position is not "Foundry IQ is bad." It is:

1. **For IDE-based architecture generation** (the pilot's primary use case today) — platform-native indexing works, is GA, costs $39/month, and requires zero infrastructure. Foundry IQ does not natively enhance Copilot's workspace context. Bridging them via MCP is architecturally possible but requires custom development.

2. **For cross-repository knowledge retrieval** (a future need that may emerge) — Foundry IQ is a credible option worth evaluating when that need is concrete and when the service exits preview. Investing in preview infrastructure to solve a problem that hasn't been demonstrated yet compounds two risks.

3. **The framing matters** — calling Foundry IQ "buy" rather than "build" sets expectations that it is turnkey. The evidence shows it requires meaningful design, development, and operational investment. A more accurate framing: "build on managed primitives" — which is genuinely less effort than building from scratch, but not comparable to the zero-config platform-native alternative.

## Sources

- [What is Foundry IQ?](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-foundry-iq) — Microsoft Learn, updated Feb 2026
- [Foundry IQ FAQ](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/foundry-iq-faq) — Microsoft Learn
- [Connect a Foundry IQ Knowledge Base to Foundry Agent Service](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/foundry-iq-connect) — Microsoft Learn, updated Apr 2026
- [Add and manage MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/chat/mcp-servers) — VS Code Docs, updated Apr 2026
- [What is Azure AI Search?](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search) — Microsoft Learn
- [Foundry IQ: Boost Response Relevance by 36% with Agentic Retrieval](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/foundry-iq-boost-response-relevance-by-36-with-agentic-retrieval/4470720) — Microsoft Tech Community

For a file-type-by-file-type comparison of how Azure AI Search's chunking stacks up against Copilot's, see [File-Type Handling: A vs C](filetype-handling-a-vs-c.md).

For how the Foundry model can be consumed inside Copilot via BYOK — making Foundry IQ simpler to deploy as a retrieval complement rather than a standalone platform — see [Option D — Hybrid Architecture](option-d-hybrid-architecture.md).

For the inverse lock-in question — what happens to Foundry customizations if the team later needs to switch platforms, and how Option D + OpenSpec makes that risk acceptable — see [Customization Portability: Option D + OpenSpec](customization-lock-in-foundry-vs-portable.md).
