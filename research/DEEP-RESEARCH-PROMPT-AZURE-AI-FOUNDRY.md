# Deep Research Prompt: Azure AI Foundry for Enterprise Architecture Practice

## Instructions for the Research Agent

You are conducting exhaustive technical research to inform a critical enterprise AI tooling decision. An Architecture Practice is evaluating whether to build a custom AI agent on **Azure AI Foundry** as an alternative to using **IDE-embedded AI agents** (GitHub Copilot, Roo Code) for solution architecture work.

The Architecture Practice has already completed a rigorous head-to-head comparison of two IDE-embedded tools:
- **GitHub Copilot Pro+** ($39/month per seat, 96.1% quality score, $0.48 per run)
- **Roo Code + OpenRouter** (~$507/month per seat, pay-per-token, fabrication issues noted)

Now the organization wants to evaluate a third option: **building a custom architecture agent on Azure AI Foundry** that would be accessible to all architects (and potentially non-architects) via a web UI or Microsoft Teams. The hypothesis is that a centralized custom agent could provide broader access to architecture knowledge across the organization.

This research must be **comprehensive, evidence-based, and cite authoritative sources**. The output will guide a Fortune 500 company's investment decision. Do not speculate — if you cannot find evidence for a claim, state that clearly. Provide citations with URLs for every factual claim.

**DATA ISOLATION REQUIREMENT**: This research is for a generic enterprise architecture practice. Do not reference any specific company, internal system, or proprietary information. All examples should use generic terms ("the enterprise", "the architecture practice") or the synthetic domain "NovaTrek Adventures" (a fictional outdoor adventure company).

---

## Background Context

### What the Architecture Practice Does

Solution architects perform these activities using AI-assisted tooling:

1. **Ticket triage** — Read JIRA tickets, classify by capability domain, assess architectural relevance
2. **Design pattern analysis** — Read source code (Java), identify anti-patterns, recommend improvements
3. **Production investigation** — Query Elasticsearch logs, trace error flows, produce investigation reports
4. **API contract management** — Read/update OpenAPI YAML specifications, ensure backward compatibility
5. **Solution design** — Produce full solution folders (15+ Markdown files per design) following MADR, C4, arc42 standards including PlantUML diagrams, impact assessments, user stories, and risk registers

### How IDE-Embedded Agents Work Today

The current tools (GitHub Copilot Agent Mode) operate **inside VS Code** with full access to the architect's local workspace:

- **35+ autonomous tool calls per session** — file reads, terminal commands, file edits, sub-agent invocations, search operations
- **Direct workspace access** — reads any file in the project, sees real-time git status, navigates full directory structure
- **Terminal execution** — runs Python scripts (mock JIRA, Elastic, GitLab clients), build tools, generators
- **File creation** — produces solution design artifacts directly in the workspace, ready for git commit
- **Standards compliance** — follows workspace-level instruction files (`.github/copilot-instructions.md`) containing architecture standards, naming conventions, and quality rules
- **Context window** — entire architecture workspace (OpenAPI specs, YAML metadata, decision records, source code) is accessible via file reads within the agent loop

A single architecture session typically involves:
- 1-4 user prompts
- 35-80 autonomous agent tool calls
- Reading 15-30 workspace files
- Creating 10-20 new files
- Running 5-10 terminal commands
- Producing standards-compliant output (MADR ADRs, C4 diagrams, arc42 documentation)

### What the Organization Envisions for Azure AI Foundry

The proposal is to build a **centralized architecture agent** that:
- Is accessible via web browser or Microsoft Teams (not limited to VS Code users)
- Has knowledge of the organization's architecture standards, patterns, and historical decisions
- Can answer questions about the architecture landscape
- Can generate documentation following corporate templates
- Is available to a broader audience than just architects with VS Code

### The Core Concern

The Architecture Practice is concerned that building a custom agent may be **reinventing the wheel** — creating at significant cost and engineering effort what commercial IDE tools already provide out of the box. This research must objectively assess whether that concern is valid.

---

## Research Questions — Organized by Priority

### PRIORITY 1: Azure AI Foundry Product Definition and Capabilities

#### Q1. What Is Azure AI Foundry as of Early 2026?

Azure AI product naming has changed multiple times (Azure ML Studio → Azure AI Studio → Azure AI Foundry). Research:

- What is the **current official name and product scope** as of March 2026?
- What is the **GA (General Availability) status**? Which features are GA vs Preview?
- What is the **product positioning** — is it a platform for building custom AI apps, a low-code agent builder, a model hosting service, or all of the above?
- How does it relate to **Azure OpenAI Service**? Are they separate products, or is Azure OpenAI now part of Foundry?
- How does it relate to **Copilot Studio**? Is Copilot Studio a subset of Foundry, a competitor, or a complementary product?

**Required sources**: Microsoft official documentation (learn.microsoft.com), Azure product announcements (azure.microsoft.com/blog), Microsoft Build/Ignite session recordings or summaries, and Gartner/Forrester analyst reports if available.

#### Q2. What Does "Building an Agent" on Azure AI Foundry Actually Entail?

When someone says "we'll use Azure AI Foundry to build our own agent," what does that concretely mean?

- **Development experience**: Is it primarily code-based (Python SDK, REST API), low-code (Prompt Flow visual designer), or no-code (drag-and-drop)?
- **Required skills**: What engineering skills are needed? Full-stack developers? ML engineers? Prompt engineers only?
- **Development timeline**: Based on published case studies, reference architectures, or community reports — how long does it take to build a production-ready enterprise agent?
- **Components to build**: Break down what "building an agent" involves:
  - Model selection and deployment
  - Knowledge base creation (document indexing, chunking strategy, embedding model)
  - Prompt engineering (system prompts, few-shot examples, guardrails)
  - Tool/function calling (if supported — connecting the agent to external systems)
  - User interface (web app, Teams integration, API endpoint)
  - Authentication and authorization
  - Monitoring and evaluation
  - Deployment and CI/CD

**Deliver**: A concrete breakdown of the engineering work required, with effort estimates where available. If Microsoft publishes reference architectures or "get started" guides, cite them and assess their realism.

#### Q3. Agent Autonomy and Tool Calling

This is critical for comparing against IDE-embedded agents. Research:

- Can Azure AI Foundry agents perform **multi-step autonomous workflows**? Specifically:
  - Can the agent call tools (functions) and use the results to decide its next action?
  - Can the agent chain 10-30+ tool calls in a single session without human intervention?
  - Can the agent execute code (e.g., Python) as part of its reasoning?
  - Can the agent access a file system (read/write files)?
  - Can the agent call external APIs (JIRA, GitLab, Elasticsearch) as tools?
- What is **Prompt Flow**? Is it the primary mechanism for multi-step orchestration? How does it compare to the autonomous agent loop in Copilot Agent Mode?
- Does Azure AI Foundry support the **ReAct pattern** (Reason → Act → Observe → Reason) natively, or only through custom code?
- What is the maximum practical chain length (number of sequential tool calls) before quality degrades or costs become prohibitive?
- Does Foundry support **sub-agent patterns** (spawning secondary agents for specialized tasks)?

**Comparison target**: GitHub Copilot Agent Mode routinely executes 35+ tool calls per session with file reads, terminal commands, file edits, and sub-agent invocations. Can a Foundry agent match this?

#### Q4. RAG (Retrieval-Augmented Generation) Architecture

Since the custom agent would need architecture knowledge, research:

- What is **Azure AI Search** (formerly Cognitive Search) and how does it power RAG in Foundry?
- **Indexing**: How are documents ingested? What file formats are supported (Markdown, YAML, JSON, PlantUML)?
- **Chunking**: What chunking strategies are available? Can custom chunking be defined for architecture-specific documents (e.g., preserving the integrity of YAML schemas or MADR ADRs)?
- **Embedding models**: Which embedding models are available? What are the trade-offs (cost, quality, dimension size)?
- **Index freshness**: How quickly do document changes propagate to the search index? Can indexing be triggered by git push (CI/CD pipeline)?
- **Retrieval quality**: What evidence exists on RAG retrieval accuracy? What are common failure modes (relevant document not retrieved, wrong chunk returned, context window overflow from too many retrieved chunks)?
- **Hybrid search**: Does Azure AI Search support keyword + semantic + vector search? How are results ranked?

**Critical comparison**: IDE agents read the exact current file content. RAG retrieves relevant chunks from a pre-built index. Research the quality gap between these approaches, especially for tasks that require:
- Reading complete YAML/JSON files (not excerpts)
- Cross-referencing information across multiple files
- Accessing the latest uncommitted changes

---

### PRIORITY 2: Cost Analysis

#### Q5. Azure AI Foundry Pricing Components

Provide exact, cited pricing for each component as of early 2026:

**Model Inference (Azure OpenAI Service)**:

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Source |
|-------|----------------------|------------------------|--------|
| GPT-4o | ? | ? | [cite] |
| GPT-4o-mini | ? | ? | [cite] |
| GPT-4 Turbo | ? | ? | [cite] |
| GPT-4.1 | ? | ? | [cite] |
| Claude 3.5 Sonnet (if available via Foundry) | ? | ? | [cite] |

**Azure AI Search**:

| Tier | Monthly Cost | Included Storage | Included Queries | Source |
|------|-------------|-----------------|-----------------|--------|
| Free | ? | ? | ? | [cite] |
| Basic | ? | ? | ? | [cite] |
| Standard S1 | ? | ? | ? | [cite] |
| Standard S2 | ? | ? | ? | [cite] |

**Azure Blob Storage** (for document source):

| Tier | Cost per GB/month | Source |
|------|------------------|--------|
| Hot | ? | [cite] |
| Cool | ? | [cite] |

**Compute (for agent hosting)**:

| Service | Configuration | Monthly Cost | Source |
|---------|--------------|-------------|--------|
| Azure App Service (B1) | ? | ? | [cite] |
| Azure Container Apps | ? | ? | [cite] |
| Azure Functions (consumption) | ? | ? | [cite] |

**Supporting services**: Key Vault, Monitor/Log Analytics, Entra ID, Virtual Network (if Private Endpoint required).

#### Q6. Total Cost of Ownership Model

Based on the pricing data from Q5, construct a TCO model for:

**Scenario**: 10 solution architects using the custom agent for architecture work equivalent to 38 runs/month (the same volume measured in Phase 1).

**Assumptions to state and calculate**:
- Each "run" equates to N tokens of input and M tokens of output (estimate based on architecture document sizes)
- The knowledge base contains approximately 500 architecture documents (OpenAPI specs, ADRs, solution designs, metadata YAML files)
- The index must refresh at least daily (or on every git push)
- The agent needs persistent hosting (always available during business hours)
- Engineering cost uses a blended rate of $150/hour (Fortune 500 enterprise rate)

**Deliver**: A 12-month TCO estimate with monthly breakdown, compared side-by-side with:
- Copilot Pro+: $39/seat/month × 10 seats = $390/month = $4,680/year
- Roo Code + OpenRouter: ~$507/seat/month × 10 seats = $5,070/month = ~$60,840/year

---

### PRIORITY 3: Enterprise Considerations

#### Q7. Security and Compliance

For a Fortune 500 enterprise evaluating Foundry:

- **Data residency**: Can all data (documents, embeddings, model inference) remain in a specific Azure region?
- **Network isolation**: Does Foundry support Private Endpoints and VNet integration? What components require network access?
- **RBAC**: What role-based access control is available? Can different users see different architectural domains?
- **Audit logging**: What actions are logged? Can you track who queried what and what answers were provided?
- **Content safety**: What content filtering is built in? Can it be customized for architecture-specific terminology (e.g., "injection" as a legitimate architectural pattern, not a security threat)?
- **SOC 2 / ISO 27001**: Is Azure AI Foundry covered by Microsoft's compliance certifications?
- **Data handling**: Are customer documents used for model training? What is the data retention policy?

#### Q8. Alternative Approaches Within the Microsoft Ecosystem

Before building a custom agent on Foundry, the enterprise should know what other Microsoft products might achieve the same goal with less effort:

- **Copilot Studio** (formerly Power Virtual Agents): Can it build a knowledge-base agent backed by architecture documents? What is the pricing? How does it compare to building on Foundry directly?
- **Microsoft 365 Copilot**: Can organizational architecture knowledge be surfaced through M365 Copilot via SharePoint-indexed documents? What are the limitations?
- **GitHub Copilot Extensions**: Can the Architecture Practice build a custom Copilot Extension that adds organizational knowledge to the IDE-embedded agent? Would this achieve "broader access" without a separate platform?
- **Azure AI Agents** (if this is a distinct product from Foundry): What is it and how does it compare?
- **Microsoft Copilot (Bing-based)**: Can enterprise search integration surface architecture knowledge?

For each alternative, provide: capabilities, pricing, effort to implement, and how it compares to building on Foundry.

#### Q9. Enterprise Case Studies and Lessons Learned

Research what enterprises have reported about building custom agents on Azure AI Foundry (or its predecessor Azure AI Studio):

- **Success stories**: What worked? What was the use case? What was the reported ROI?
- **Failure stories**: What did not work? Common pitfalls?
- **Cost surprises**: Did actual costs match estimates? Where did budgets overrun?
- **Timeline reality**: How long did it actually take vs estimates?
- **Adoption metrics**: Did users actually adopt the custom agent, or did they revert to other tools?

**Sources to check**: Microsoft customer stories (customers.microsoft.com), Gartner peer reviews, G2 reviews, conference presentations (Microsoft Build, Ignite), technical blog posts from consulting firms (Accenture, Deloitte, etc.), Stack Overflow / GitHub Discussions, Reddit (r/azure, r/MachineLearning).

---

### PRIORITY 4: Strategic and Comparative Analysis

#### Q10. The "Build vs Buy" Decision Framework

Research established frameworks for evaluating "build your own AI agent" vs "use commercial AI tools":

- What do industry analysts (Gartner, Forrester, IDC) recommend for enterprises deciding between custom AI applications and commercial AI assistants?
- Is there a published **maturity model** for enterprise AI adoption that distinguishes between "consume AI tools" and "build AI applications"?
- What is the **TCO multiplier** typically observed when enterprises build custom AI solutions vs using commercial SaaS? (e.g., "Custom solutions typically cost 3-10x more than equivalent SaaS tools over 3 years")
- Are there published **decision criteria** for when building custom is justified vs when it is not?

#### Q11. What Can a Custom Agent Do That IDE-Embedded Tools Cannot?

This is the most important strategic question. Research:

- **Broader audience access**: Can non-IDE users (project managers, business analysts, executives) meaningfully use an architecture knowledge agent? What use cases does this enable?
- **Cross-repo knowledge**: IDE agents see one workspace at a time. Can a centralized agent aggregate knowledge across multiple repositories and provide cross-cutting insights?
- **Organizational governance**: Can a centralized agent enforce architecture standards more consistently than distributed workspace-level instructions?
- **Historical trend analysis**: Can a centralized agent track architecture evolution over time (decision history, pattern adoption rates, technical debt trends)?
- **Integration with enterprise tools**: Can a Foundry agent be more deeply integrated with enterprise tools (JIRA, Confluence, ServiceNow) than an IDE extension?

For each claimed advantage, assess:
- Is this a genuine capability gap, or can IDE tools achieve the same thing with different approaches?
- How much additional value does this capability provide?
- Is the value sufficient to justify the cost difference?

#### Q12. Competitive Landscape: How Are Other Enterprises Solving This?

Beyond Microsoft's ecosystem, research:

- **Amazon Q Developer / Amazon Q Business**: How does Amazon's approach compare? Does it separate "developer AI" from "business AI"?
- **Google Vertex AI Agent Builder**: Google's equivalent — how does it compare in pricing, capabilities, and enterprise adoption?
- **Glean**: Enterprise AI search and knowledge management — is this a better fit for the "organizational knowledge" use case?
- **Atlassian Intelligence (Rovo)**: Since the architecture practice uses JIRA and Confluence, does Atlassian's AI already cover the "architecture knowledge" use case?
- **Custom GPTs (OpenAI)**: Could a Custom GPT with uploaded architecture documents achieve 80% of the goal at near-zero cost?

---

## Output Requirements

### 1. Structured Findings

For each research question (Q1-Q12), provide:
- **Finding**: The factual answer based on evidence
- **Sources**: Numbered citations with URLs
- **Confidence level**: HIGH (multiple authoritative sources agree), MEDIUM (limited sources or recent changes may not be reflected), LOW (primarily based on inference or single sources)
- **Relevance to the decision**: How this finding affects the build-vs-buy recommendation

### 2. Cost Model

Provide a complete, filled-in TCO model with:
- Itemized monthly costs for each Azure component
- 12-month projection for 10 architect seats
- Side-by-side comparison with Copilot Pro+ and Roo Code + OpenRouter
- Sensitivity analysis: what if usage is 2x higher? What if the engineering team costs more?

### 3. Capability Matrix

Complete this matrix with evidence-based assessments:

| Capability | Copilot Pro+ | Roo Code + OpenRouter | Azure AI Foundry Custom Agent |
|------------|-------------|----------------------|------------------------------|
| Local file read | YES | YES | ? |
| Terminal execution | YES | YES | ? |
| File creation/editing | YES | YES | ? |
| Multi-step autonomous execution (35+ tool calls) | YES | YES | ? |
| Standards compliance (MADR, C4, arc42) | YES (96.1%) | YES (with issues) | ? |
| Broad audience access (non-IDE users) | NO | NO | ? |
| Cross-repository knowledge | NO | NO | ? |
| Real-time workspace context | YES | YES | ? |
| Enterprise tool integration (JIRA, etc.) | Via mock scripts | Via mock scripts | ? |
| Monthly cost per seat | $39 | ~$507 | ? |
| Build effort | Zero | Near-zero | ? |
| Maintenance effort | Zero | Low | ? |

### 4. Recommendation Framework

Based on the evidence gathered, provide a framework — not a specific recommendation (since this research must remain unbiased) — that an enterprise can use to make the decision. Structure it as:

- **Decision criteria** (weighted, with rationale for weights)
- **Scoring methodology** (how to evaluate each option against each criterion)
- **Decision tree** (if X > Y, then recommend Z)
- **Red flags** (conditions under which each option should be immediately disqualified)

### 5. Source Quality Assessment

For each major source cited, assess:
- Is it from Microsoft (potentially biased toward Azure)?
- Is it from a competitor (potentially biased against Azure)?
- Is it from an independent analyst or practitioner?
- How recent is it? (Azure AI products change rapidly)
- Is it based on actual usage or marketing materials?

---

## Constraints and Guardrails

1. **No corporate data**: Do not reference any specific company name, internal system, or proprietary information. The enterprise is referred to only as "a Fortune 500 company" or "the organization."
2. **No fabricated costs**: Only use published Azure pricing. If pricing is not publicly available, state that clearly.
3. **No speculation presented as fact**: Clearly label inferences and estimates as such.
4. **Recency matters**: Azure AI products evolve rapidly. Flag any finding that may be outdated. Prefer sources from 2025-2026.
5. **Authoritative sources first**: Prioritize Microsoft Learn documentation, Azure pricing pages, Gartner/Forrester reports, peer-reviewed publications, and verified practitioner accounts over blog posts and marketing materials.
6. **Acknowledge limitations**: State what you could NOT determine and why.

---

## Why This Research Matters

The outcome of this research will directly influence whether a Fortune 500 company invests significant engineering resources in building a custom AI agent, or redirects those resources to leveraging existing commercial tools. The stakes include:

- **Budget**: The difference could be hundreds of thousands of dollars per year
- **Engineering capacity**: Building and maintaining a custom agent consumes engineering talent that could be applied elsewhere
- **Time to value**: IDE tools provide value today; a custom agent may take 3-6 months to build
- **Risk**: A failed custom agent project damages the credibility of the architecture practice's AI initiative

The research must be rigorous enough to withstand executive scrutiny and auditor review. Unsupported claims will undermine the analysis.
