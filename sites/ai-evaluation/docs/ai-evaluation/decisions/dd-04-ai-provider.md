<!-- CONFLUENCE-PUBLISH -->

# DD-04: AI Processing Provider

## Who Do We Buy AI From?

| | |
|-----------|-------|
| **Status** | Under Evaluation |
| **Date** | 2026-04-03 |
| **Category** | Strategy |
| **Maps to** | DP-03 (Toolchain Selection), DP-10 (Vendor Lock-In) |
| **Constrains** | DD-03 (Billing Model) — provider determines available billing models |

---

## Context and Problem Statement

The "which AI tool should we use?" question is actually a provider question in disguise. The VS Code extension (Copilot, Roo Code, Claude Code) is the **delivery vehicle**, but the real decision is: **which company processes our architecture prompts, on what terms, and with what platform services?**

Four providers occupy distinct positions in the enterprise AI market:

1. **GitHub (Microsoft)** — Platform-first: bundles model access with IDE integration, workspace indexing, and intent-based billing
2. **Anthropic** — Model-first: offers the best reasoning model (Claude) with direct API access or subscription ceiling
3. **Kong / OpenRouter** — Gateway-first: routes to any model provider, full flexibility, token-based billing
4. **Microsoft Azure AI Foundry** — Infrastructure-first: self-hosted model inference with full organizational control

Each provider makes different trade-offs between cost, quality, control, and operational complexity.

---

## Provider Profiles

### Provider 1: GitHub (Microsoft)

**Delivery vehicle:** GitHub Copilot Pro+ (VS Code extension with agent mode)

**What you are buying:** A platform, not just a model. GitHub bundles model access (Claude, GPT, Gemini) with:

- Server-side workspace semantic indexing (included, no additional infrastructure)
- Intent-based billing ($0.04 per prompt x model multiplier)
- Deep GitHub ecosystem integration (PRs, code suggestions, repository context)
- Agent mode with autonomous multi-step execution
- Custom instruction system (`copilot-instructions.md`, `.instructions.md`, SKILL.md)
- MCP client integration for external tool servers
- Enterprise org-wide policy controls

**Pricing:**

| Component | Cost |
|-----------|------|
| Pro+ subscription | $39/month |
| Included premium requests | 1,500/month |
| Overage | $0.04 x model multiplier per request |
| Infrastructure | $0 (SaaS) |

**Model availability (March 2026):**

| Model | Multiplier | Cost per Prompt |
|-------|-----------|-----------------|
| GPT-4.1, GPT-4o | 0x | $0 (unlimited) |
| Claude Sonnet 4, o4-mini, Gemini 2.5 Pro | 1x | $0.04 |
| Claude Opus 4.6 | 3x | $0.12 |
| Claude Opus 4.6 fast | 30x | $1.20 |

**Strategic position:**

- GitHub controls the most popular developer platform (100M+ developers)
- Microsoft's AI investment ($10B+ in OpenAI) ensures long-term commitment
- GitHub is integrating AI into every developer workflow (PR review, code search, Copilot Workspace)
- The platform approach creates strong lock-in but also strong network effects

**Evaluation:**

| Factor | Score | Evidence |
|--------|-------|---------|
| Model quality | 4/5 | Access to Claude Opus 4.6 (same model as direct Anthropic) |
| Pricing predictability | 5/5 | $39/month flat, 1,500 requests included |
| Cost per run | 5/5 | $0.48/run — 208x cheaper than token-based |
| Enterprise governance | 4/5 | Org policies, audit log, SSO — missing centralized usage dashboard |
| Ecosystem integration | 5/5 | Native VS Code, GitHub PRs, code suggestions, agent mode |
| Data residency | 3/5 | Data processed in GitHub's cloud — limited regional control |
| Platform longevity | 5/5 | Microsoft/GitHub backing — near-zero platform risk |
| Extensibility | 4/5 | MCP support, custom instructions, extensions marketplace |
| Model flexibility | 3/5 | Limited to GitHub's offered models — cannot bring your own |
| Transparency | 2/5 | No per-request token data — aggregate premium request count only |

---

### Provider 2: Anthropic (Direct)

**Delivery vehicle:** Claude Code (CLI + VS Code extension) or Anthropic API

**What you are buying:** Direct access to the model vendor's best product. No translation layer, no intermediary — prompts go straight to Anthropic's infrastructure.

**Pricing options:**

| Option | Cost | Model |
|--------|------|-------|
| Anthropic API (pay-per-token) | Variable — ~$15/M input, ~$75/M output for Opus | Token-based |
| Anthropic Max Professional | $100/month | Subscription with ceiling |
| Anthropic Max Team | $200/month | Subscription with ceiling + admin features |

**Delivery capabilities:**

- Claude Code: CLI-first agent with autonomous execution, CLAUDE.md project context
- Extended thinking mode: transparent reasoning chains
- Native tool calling: no translation layer artifacts
- Sub-agent spawning for parallel research
- MCP support (client-side)

**Strategic position:**

- Anthropic built the leading reasoning model (Claude Opus)
- Smaller company than Microsoft — enterprise support and compliance commitments less established
- Model quality leadership may not be permanent — OpenAI, Google, and others are closing the gap
- Direct relationship with model vendor — no intermediary translation failures

**Evaluation:**

| Factor | Score | Evidence |
|--------|-------|---------|
| Model quality | 5/5 | First-party access to Claude Opus — no translation layer |
| Pricing predictability | 3/5 | API is variable; Max subscription is predictable but capped |
| Cost per run | 2/5 | API: ~$50-100/run (context accumulation); Max: included until cap |
| Enterprise governance | 2/5 | Limited — no org-wide policies, basic SSO on Team tier |
| Ecosystem integration | 2/5 | No GitHub integration, no PR review, CLI-first |
| Data residency | 3/5 | Anthropic's cloud — limited regional control |
| Platform longevity | 3/5 | Well-funded but smaller company — higher platform risk than Microsoft |
| Extensibility | 4/5 | MCP support, CLAUDE.md instructions, tool calling |
| Model flexibility | 1/5 | Claude models only — single vendor |
| Transparency | 5/5 | Full per-request token data, cost visibility |

---

### Provider 3: Kong / OpenRouter (Gateway)

**Delivery vehicle:** Roo Code (VS Code extension) routing through Kong AI Gateway or OpenRouter

**What you are buying:** Flexibility and transparency. Kong/OpenRouter routes prompts to any model provider (Anthropic, OpenAI, Google, Mistral) through a single API gateway with full token-level cost visibility.

**Pricing:**

| Component | Cost |
|-----------|------|
| Roo Code license | $0 (open source) |
| Kong AI Gateway | $0-500/month (depends on deployment) |
| Model tokens (via OpenRouter) | Variable — per-token per-provider |
| Infrastructure (Qdrant, if custom indexing) | $75-250/month |

**Delivery capabilities:**

- Roo Code: VS Code extension with custom modes, `.roo/rules/` instruction system
- Kong AI Gateway: enterprise API gateway with rate limiting, auth, logging
- OpenRouter: model marketplace with 50+ model options
- Full cost transparency per request
- Custom instruction modes (orchestrator, code, architect, etc.)

**Strategic position:**

- Kong is an established enterprise API gateway vendor
- OpenRouter is a model aggregator — not a model vendor
- This approach maximizes flexibility but adds a translation layer between the IDE and the model
- Enterprise gateway patterns are familiar to infrastructure teams

**Evaluation:**

| Factor | Score | Evidence |
|--------|-------|---------|
| Model quality | 4/5 | Access to any model — but through translation layer (Kong drops tool calls) |
| Pricing predictability | 1/5 | Fully variable — $100/run observed; unpredictable monthly spend |
| Cost per run | 1/5 | ~$100/run — 208x more expensive than intent-based |
| Enterprise governance | 3/5 | Kong provides API-level governance; no AI-specific policies |
| Ecosystem integration | 2/5 | No GitHub integration; separate from PR workflow |
| Data residency | 4/5 | Can route through enterprise-controlled infrastructure |
| Platform longevity | 3/5 | Kong is stable; OpenRouter is a startup; Roo Code is open source |
| Extensibility | 5/5 | Any model, any provider, full MCP support, custom modes |
| Model flexibility | 5/5 | Maximum — route to any provider through the gateway |
| Transparency | 5/5 | Exact per-request costs via OpenRouter API |

**Critical failures documented:**

- Kong AI gateway drops tool calls (transforms incompatible with Claude's tool calling schema)
- Error response obfuscation: Kong strips `context_length_exceeded` error details
- No circuit breaker: context-length errors can trigger infinite retry loops
- See [Kong AI Translation Failures](../research/kong-failures.md) for detailed failure analysis

---

### Provider 4: Microsoft Azure AI Foundry (Self-Hosted)

**Delivery vehicle:** Custom web application, API endpoints, or MCP servers hosted on Azure

**What you are buying:** Full organizational control. Host your own AI inference, RAG pipeline, and agent orchestration on Azure infrastructure. Choose any model available through Azure AI Foundry's model catalog.

**Pricing:**

| Component | Cost |
|-----------|------|
| Azure AI Foundry compute | $200-500/month per team (GPU instances) |
| Azure AI Search (vector index) | $75-250/month |
| Azure App Service (custom web app) | $50-150/month |
| Azure Cosmos DB (state management) | $25-100/month |
| Infrastructure overhead | $50-100/month |
| Engineering: build + operate | 6-12 dev-months initial, 1-2 FTE ongoing |

**Delivery capabilities:**

- Custom agent with architecture-specific system prompt
- Custom RAG pipeline (Azure AI Search + embeddings)
- Full tool calling with enterprise backend integration
- Custom UX (web app) or MCP server interface
- Model selection from Azure catalog (Claude via Bedrock, GPT via Azure OpenAI, open-source models)

**Strategic position:**

- Azure is the enterprise cloud leader for Microsoft-centric organizations
- Azure AI Foundry is Microsoft's play to capture custom AI workloads
- Maximum control comes with maximum operational burden
- Makes sense at organizational scale (50+ users) where infrastructure costs amortize

**Evaluation:**

| Factor | Score | Evidence |
|--------|-------|---------|
| Model quality | 4/5 | Access to multiple models — but adds inference infrastructure complexity |
| Pricing predictability | 3/5 | Infrastructure cost is predictable; token-based per-model still applies |
| Cost per run | 2/5 | ~$5-15/run estimated (lower than OpenRouter, higher than Copilot) |
| Enterprise governance | 5/5 | Full RBAC, audit logging, DLP, data residency control |
| Ecosystem integration | 2/5 | Custom build — limited VS Code integration unless MCP servers are built |
| Data residency | 5/5 | Full control — data stays in organization's Azure tenant |
| Platform longevity | 5/5 | Azure is not going anywhere — Microsoft's strategic cloud platform |
| Extensibility | 5/5 | Full control — build any capability |
| Model flexibility | 4/5 | Azure model catalog + bring-your-own; slightly less than OpenRouter's breadth |
| Transparency | 4/5 | Azure Cost Management provides detailed breakdowns |

---

## Provider Comparison Matrix

| Factor | Weight | GitHub | Anthropic | Kong/OpenRouter | Azure Foundry |
|--------|--------|:---:|:---:|:---:|:---:|
| Model quality | 15% | 4 | 5 | 4 | 4 |
| Pricing predictability | 15% | 5 | 3 | 1 | 3 |
| Cost per run | 20% | 5 | 2 | 1 | 2 |
| Enterprise governance | 10% | 4 | 2 | 3 | 5 |
| Ecosystem integration | 10% | 5 | 2 | 2 | 2 |
| Data residency | 5% | 3 | 3 | 4 | 5 |
| Platform longevity | 5% | 5 | 3 | 3 | 5 |
| Extensibility | 5% | 4 | 4 | 5 | 5 |
| Model flexibility | 10% | 3 | 1 | 5 | 4 |
| Transparency | 5% | 2 | 5 | 5 | 4 |
| **Weighted Score** | **100%** | **4.15** | **2.75** | **2.60** | **3.30** |

!!! note "Scores Are Preliminary"
    These scores reflect the architect's initial assessment based on Phase 1 evidence. They have NOT been reviewed or ratified by stakeholders. The weight distribution (cost and pricing at 35% combined) reflects an architecture practice where budget predictability is a hard requirement.

---

## Provider x Billing Model Matrix

Not every provider offers every billing model. This matrix shows availability:

| Provider | Intent-Based | Token-Based | Subscription Ceiling | Infrastructure |
|----------|:---:|:---:|:---:|:---:|
| GitHub | YES ($0.04 x multiplier) | No | No | No |
| Anthropic | No | YES (API) | YES (Max $100-200) | No |
| Kong/OpenRouter | No | YES (per-token) | No | No |
| Azure AI Foundry | No | YES (per-token) | No | YES (compute) |

**Key insight:** Intent-based billing is **only available from GitHub**. Choosing any other provider forces token-based or subscription-ceiling billing. This is the strongest lock-in factor — the billing architecture is provider-exclusive.

---

## Provider x Content Injection Matrix

How provider choice constrains content injection options:

| Provider | Native Workspace Indexing | Local MCP | Remote MCP | Custom RAG |
|----------|:---:|:---:|:---:|:---:|
| GitHub Copilot | YES (built-in) | YES | YES | No (not needed) |
| Anthropic Claude Code | No (explicit file reads) | YES | YES | Custom build |
| Roo Code (Kong/OpenRouter) | No (requires Qdrant) | YES | YES | Custom build |
| Azure AI Foundry | No (custom build) | N/A (server-side) | N/A | YES (native) |

**Key insight:** Only GitHub provides native workspace indexing at zero cost. All other providers require custom infrastructure for equivalent capability, which compounds onto the token-based billing cost.

---

## Decision Drivers

1. **Cost dominance**: GitHub is 208x cheaper per run and 13x cheaper monthly. This is not marginal — it is decisive for a cost-conscious practice.
2. **Billing model exclusivity**: Intent-based billing is only available from GitHub. This is the primary cost advantage and it is unique to this provider.
3. **Ecosystem fit**: The practice already uses VS Code, GitHub, and the Copilot instruction system. Switching providers means rebuilding the instruction layer.
4. **Governance requirements**: If regulatory compliance requires data residency or centralized audit beyond GitHub's capabilities, Azure AI Foundry becomes necessary.
5. **Model quality preservation**: All providers can access Claude Opus 4.6 — model quality is not a differentiator (except for Kong's translation layer failures).
6. **Vendor concentration risk**: GitHub + Azure = Microsoft dependency for both IDE and AI processing. Some organizations prefer provider diversification.

---

## Preliminary Recommendation

!!! tip "Working Recommendation: GitHub as Primary, with Anthropic as Evaluated Complement"
    Adopt GitHub (Copilot Pro+) as the primary AI processing provider. The combination of intent-based billing, native workspace indexing, and deep GitHub ecosystem integration creates a 208x cost advantage that no other provider can match. Evaluate Anthropic (Claude Code) as a potential complement for deep research tasks where its strengths (extended thinking, native tool calling, no translation layer) may add value. Do not adopt Kong/OpenRouter or Azure AI Foundry as the primary provider for architecture work.

### Why Not Kong/OpenRouter?

- 208x more expensive per run using the same model
- Kong AI Gateway introduces translation failures that degrade tool calling
- Custom infrastructure (Qdrant, embedding pipeline) is needed to replicate Copilot's free workspace indexing
- The "flexibility" advantage (any model, any provider) is theoretical — the practice uses Claude Opus 4.6 regardless

### Why Not Azure AI Foundry (as primary)?

- 6-12 month build time before first value — the practice is already delivering value today
- Custom agent execution engine must be built from scratch — this is the hardest unsolved problem in AI tooling
- $150-350/month per seat vs $39/month — 4-9x more expensive
- The primary advantages (data residency, centralized governance) are not yet requirements for this practice

### Why Anthropic as Complement?

- Claude Code offers native Anthropic API access without translation layer
- Extended thinking mode provides reasoning transparency not available in Copilot
- Terminal-native workflow may complement VS Code for specific tasks (deep research, complex analysis)
- The planned spike (SC-02 + SC-03) will provide cost and quality data to validate

---

## Consequences

### If GitHub is selected as primary provider

**Positive:**

- 208x per-run cost advantage locked in
- Zero infrastructure beyond existing VS Code + GitHub
- Proven 96.1% quality score
- Deep ecosystem integration (PRs, code, agent mode)
- Native workspace indexing eliminates need for custom RAG

**Negative:**

- Locked to GitHub's model roster and pricing decisions
- No per-request token visibility
- Microsoft vendor concentration (IDE + AI + cloud)
- If GitHub changes intent-based pricing, the cost advantage evaporates

**Neutral:**

- Anthropic complement is an option, not a commitment — the spike will inform
- Azure AI Foundry remains available for future enterprise data requirements (DD-02, Option B MCP servers)

---

## Links

- [GitHub Copilot Profile](../tools/github-copilot.md) — Detailed capabilities and pricing
- [Roo Code + Kong Profile](../tools/roo-code-kong.md) — Capabilities and documented failures
- [Claude Code Profile](../tools/claude-code.md) — Capabilities and spike plan
- [DD-03: Billing Model](dd-03-billing-model.md) — Provider choice constrains billing options
- [Platform Options](../platform-options.md) — How provider maps to platform options
