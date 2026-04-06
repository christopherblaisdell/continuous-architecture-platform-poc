<!-- CONFLUENCE-PUBLISH -->

# Platform Options

> **You are reading:** Layer 2 — Platform Options | [Decision Framework](decisions/decision-framework.md) | [Home](../index.md)
>
> These options compose Layer 2 toolchain decisions into coherent packages. For the practice-level operating model, see [Practice Strategy](practice-strategy.md) (Layer 1).

## Composed Side-by-Side Comparison

This page presents three platform options composed from the four independent decision documents. Each option represents a coherent combination of choices across content injection strategy, injection location, billing model, and AI processing provider.

---

## How Options Were Composed

Each platform option is a specific combination of DD-01 through DD-04 choices:

| Decision | Option A: Lean | Option B: Hybrid | Option C: Full Build |
|----------|---|---|---|
| [DD-01: Content Injection](decisions/dd-01-content-injection.md) | Native workspace + instructions | Native + targeted MCP for external data | Full custom MCP pipeline + RAG |
| [DD-02: Injection Location](decisions/dd-02-injection-location.md) | Workstation only | Workstation + selective server | Server-hosted AI orchestration |
| [DD-03: Billing Model](decisions/dd-03-billing-model.md) | Intent-based (fixed $39/mo) | Intent-based + consumption (MCP infra) | Token-based (variable) |
| [DD-04: AI Provider](decisions/dd-04-ai-provider.md) | GitHub (Copilot Pro+) | GitHub + Azure AI Foundry (MCP) | Azure AI Foundry or Anthropic direct |

---

## Option A: Copilot Pro+ Standalone (Lean)

### Description

GitHub Copilot Pro+ is the sole AI platform. All architectural work happens inside VS Code Agent Mode. Enterprise context is provided through the existing workspace (specs, metadata, instructions) and local MCP servers (ticketing, mock tools). No custom AI backend infrastructure is built.

### Architecture

```
┌──────────────────────────────────────────────────┐
│  Architect's VS Code                             │
│  ┌────────────────────────────────────────────┐  │
│  │  GitHub Copilot Pro+ (Agent Mode)          │  │
│  │  - Claude Opus 4.6 via GitHub              │  │
│  │  - copilot-instructions.md (700+ lines)    │  │
│  │  - .instructions.md, SKILL.md files        │  │
│  │  - Native workspace semantic indexing      │  │
│  └──────────┬─────────────────────────────────┘  │
│             │                                    │
│  ┌──────────▼──────────┐                         │
│  │  Local MCP Servers  │                         │
│  │  - Vikunja tickets  │                         │
│  │  - Mock tools       │                         │
│  └─────────────────────┘                         │
└──────────────────────────────────────────────────┘
```

### Cost Model

| Component | Monthly Cost per Seat |
|-----------|---------------------|
| Copilot Pro+ subscription | $39.00 |
| Overage (if >1,500 req) | $0.04 x multiplier per request |
| Azure Static Web Apps (portal) | ~$10 (shared) |
| Infrastructure engineering | $0 |
| **Total per seat** | **~$39-50** |

### What You Get

- 96.1% quality score (proven — 149/155 across 5 scenarios)
- Intent-based billing: autonomous agent work is free ($0.48/run)
- Deep VS Code + GitHub integration (PRs, code suggestions, agent mode)
- Native workspace semantic indexing — no custom RAG needed
- Custom instructions, skills, and agent files for domain knowledge
- MCP integration for local tool servers
- GitOps governance: instruction changes go through PR review

### What You Do NOT Get

- No access to enterprise databases beyond workspace + local MCP
- No centralized AI governance dashboard
- No custom model fine-tuning
- Dependent on GitHub's model availability and pricing
- No shared enterprise context layer across teams

### Decision Justification

| Decision | Choice | Rationale |
|----------|--------|-----------|
| DD-01 | Native only | 7/10 content types already covered; no custom MCP reinvention |
| DD-02 | Workstation only | Zero infrastructure; proven 96.1% quality |
| DD-03 | Intent-based | 208x cheaper per run; $39/month predictable |
| DD-04 | GitHub | Best weighted score (4.15/5); strongest ecosystem fit |

---

## Option B: Copilot + Azure MCP Services (Hybrid)

### Description

GitHub Copilot Pro+ remains the local execution engine and primary UX. Azure AI Foundry hosts targeted MCP servers that expose 1-2 enterprise-specific tools — CMDB lookup and cross-team ADR index. Confluence content is migrated to repository markdown and published via CI, eliminating the need for a Confluence MCP server. The local agent calls Azure services on demand via MCP.

### Architecture

```
┌──────────────────────────────────────────────────┐
│  Architect's VS Code                             │
│  ┌────────────────────────────────────────────┐  │
│  │  GitHub Copilot Pro+ (Agent Mode)          │  │
│  │  - Native workspace indexing + MCP client  │  │
│  └──────────┬──────────────────┬──────────────┘  │
│             │                  │                  │
│  ┌──────────▼──────────┐      │                  │
│  │  Local MCP Servers  │      │                  │
│  │  - Vikunja tickets  │      │                  │
│  └─────────────────────┘      │                  │
└───────────────────────────────┼──────────────────┘
                                │ MCP (HTTPS)
                                │ Auth: Entra ID
┌───────────────────────────────▼──────────────────┐
│  Azure (Targeted MCP Services)                   │
│  ┌────────────────────────────────────────────┐  │
│  │  CMDB / ServiceNow Lookup MCP              │  │
│  │  Cross-Team ADR Index MCP                  │  │
│  └────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────┐  │
│  │  Entra ID + Key Vault + Azure Monitor      │  │
│  └────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
```

### Cost Model

| Component | Monthly Cost per Seat |
|-----------|---------------------|
| Copilot Pro+ subscription | $39.00 |
| Azure MCP compute (shared) | ~$10-30 |
| Azure infrastructure (shared) | ~$5-15 |
| Engineering (amortized 2-4 months) | Significant one-time |
| **Total per seat (5-person team)** | **~$70-130** |

### What You Get

- Everything in Option A, plus:
- Confluence content accessible natively via migrated markdown in the repository
- CMDB/ServiceNow service metadata at AI query time
- Cross-team architecture decisions accessible without manual lookup
- Enterprise identity (Entra ID) for access control on all backend tools
- Shared context layer usable by multiple architects
- MCP is an open standard — backend services work with any MCP client

### What You Do NOT Get

- No custom chat UX — still VS Code Copilot
- No custom model hosting — still GitHub's model routing
- MCP remote servers (HTTPS/SSE) are still maturing — protocol risk
- Engineering investment required before value is delivered

### Decision Justification

| Decision | Choice | Rationale |
|----------|--------|-----------|
| DD-01 | Native + targeted MCP | Native for workspace (C1-C7); Confluence migrated to repo markdown (C8); targeted MCP for enterprise gaps (C9-C10) |
| DD-02 | Workstation + selective server | Local for workspace context; server for enterprise data only |
| DD-03 | Intent-based + consumption | Copilot billing unchanged; Azure infrastructure is incremental |
| DD-04 | GitHub + Azure | Copilot remains primary; Azure provides enterprise backend |

---

## Option C: Custom AI Platform (Full Build)

### Description

Azure AI Foundry is the primary AI platform. A custom web application or comprehensive MCP server farm handles all context injection, agent orchestration, and enterprise knowledge retrieval. Copilot may remain for basic coding assistance but is not the architecture workflow tool.

### Architecture

```
┌──────────────────────────────────────────────────┐
│  Custom Architecture AI Portal or MCP Farm       │
│  ┌────────────────────────────────────────────┐  │
│  │  AI Orchestrator (Azure AI Foundry)        │  │
│  │  - Custom system prompt                    │  │
│  │  - RAG pipeline (Azure AI Search)          │  │
│  │  - Full tool calling: CMDB, Confluence,    │  │
│  │    JIRA, GitLab, workspace files           │  │
│  │  - Model selection per task type           │  │
│  └──────────┬─────────────────────────────────┘  │
│             │                                    │
│  ┌──────────▼──────────────────────────────────┐ │
│  │  Context Layer                              │ │
│  │  - Qdrant / Azure AI Search (vector DB)     │ │
│  │  - Workspace sync (git clone)               │ │
│  │  - Confluence indexer (embeddings)           │ │
│  │  - CMDB integration                         │ │
│  │  - Production log aggregator                │ │
│  └─────────────────────────────────────────────┘ │
│                                                  │
│  ┌─────────────────────────────────────────────┐ │
│  │  Infrastructure                             │ │
│  │  - Azure Cosmos DB (state)                  │ │
│  │  - Azure App Service                        │ │
│  │  - Azure Key Vault + Monitor                │ │
│  │  - Entra ID + custom RBAC                   │ │
│  └─────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

### Cost Model

| Component | Monthly Cost per Seat |
|-----------|---------------------|
| Copilot Pro+ (optional, basic coding) | $39.00 |
| Azure AI Foundry (model inference) | ~$40-100 |
| Azure AI Search (vector store) | ~$15-50 |
| Azure App Service | ~$10-30 |
| Azure Cosmos DB | ~$5-20 |
| Azure infrastructure | ~$10-20 |
| Engineering (6-12 dev-months + 1-2 FTE) | Major ongoing |
| **Total per seat (5-person team)** | **~$150-350** |

### What You Get

- Full control over AI model selection and orchestration
- Comprehensive enterprise data access (all sources indexed)
- Custom UX designed for architecture workflows
- Centralized governance with full audit logging
- Custom fine-tuning capability (future)
- Serves non-VS-Code users (browser-based)

### What You Do NOT Get

- No deep VS Code integration (unless rebuilt)
- No intent-based billing — token-based pricing applies
- Agent execution engine must be built from scratch (hardest problem)
- 6-18 months to first production value
- 1-2 FTE ongoing operational commitment
- Competes with GitHub's product engineering team on UX and agent quality

### Decision Justification

| Decision | Choice | Rationale |
|----------|--------|-----------|
| DD-01 | Full custom MCP pipeline + RAG | All context types managed by custom infrastructure |
| DD-02 | Server-hosted | Centralized context layer; workstation is thin client |
| DD-03 | Token-based | No intent-based option available outside GitHub |
| DD-04 | Azure AI Foundry | Maximum control; enterprise governance |

### The Reinvention Cost

Per DD-01 analysis, Option C reinvents 6 of 10 capabilities that native toolchains already provide:

| Reinvented Capability | Native Solution | Custom Build Cost |
|-----------------------|-----------------|-------------------|
| Workspace file search | Copilot semantic search (free) | 2 months + Qdrant ($75-250/mo) |
| Architecture standards injection | `copilot-instructions.md` | 1 month |
| OpenAPI spec retrieval | Workspace files (indexed) | 2 months + embedding pipeline |
| Ticket access | Vikunja MCP (already built) | 1 month |
| Source code analysis | Native file reads | 1 month |
| Solution design templates | `.instructions.md` + SKILL.md | 0.5 months |
| **Subtotal: reinvention** | **$0** | **~7.5 months + $75-250/mo** |

---

## Comparative Scorecard

### Evaluation Criteria

| # | Factor | Weight | Option A | Option B | Option C |
|---|--------|--------|:---:|:---:|:---:|
| 1 | Total cost of ownership (3-year) | 15% | 5 | 4 | 2 |
| 2 | Time to first production value | 10% | 5 | 3 | 1 |
| 3 | Architecture output quality | 20% | 5 | 5 | 3 |
| 4 | Enterprise data access breadth | 8% | 2 | 4 | 5 |
| 5 | Workflow integration depth | 12% | 5 | 5 | 2 |
| 6 | Agent execution autonomy | 10% | 5 | 5 | 2 |
| 7 | Governance and auditability | 8% | 3 | 4 | 5 |
| 8 | Instruction management model | 5% | 4 | 4 | 3 |
| 9 | Extensibility and custom tooling | 5% | 3 | 4 | 5 |
| 10 | Portability and exit cost | 3% | 4 | 4 | 3 |
| 11 | Operational burden | 2% | 5 | 3 | 1 |
| 12 | Scalability across teams | 2% | 2 | 4 | 5 |
| | **Weighted Score** | **100%** | **4.39** | **4.34** | **2.78** |

!!! warning "Scores Are Preliminary"
    These scores are the architect's initial assessment. They have NOT been ratified by stakeholders. The weight distribution reflects the current practice's priorities (quality, cost, workflow integration). Different stakeholders may assign different weights.

### Score Justification Notes

| Factor | Option A | Option B | Option C |
|--------|---------|---------|---------|
| F-01 Cost | $39/mo/seat, proven | $70-130/mo, estimated | $150-350/mo, estimated |
| F-02 Time | Already in production | 3-6 months to first MCP | 6-18 months minimum |
| F-03 Quality | 96.1% demonstrated | Same (same agent engine) | Unproven — custom agent is a risk |
| F-04 Enterprise data | Local workspace only | Targeted enterprise access | Comprehensive access |
| F-05 Workflow | Native VS Code integration | Same (Copilot unchanged) | Custom UX — separate tool |
| F-06 Autonomy | GitHub-managed (proven) | Same | Custom-built (unproven) |
| F-07 Governance | Repo-based (GitOps) | Repo + Azure RBAC | Full centralized governance |
| F-08 Instructions | GitOps native | Same | Custom admin (must be built) |
| F-09 Extensibility | MCP client + instructions | MCP + Azure services | Full custom (any capability) |
| F-10 Portability | Knowledge in Markdown/YAML | Same | Some lock-in to custom platform |
| F-11 Operations | Zero infrastructure | 2-3 servers to monitor | Full-stack application |
| F-12 Scalability | Add Copilot seats | Add seats + shared MCP | Add infrastructure + training |

---

## Staged Recommendation

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Today ─────── 3-6 months ─────── 12+ months               │
│                                                             │
│  Option A         Option B             Option B+            │
│  (Lean)          (Hybrid)            (Expanded)             │
│                                                             │
│  Copilot Pro+   + First MCP server  + Additional MCP       │
│  Workstation    + Server hosting      servers as validated  │
│  Native context + Enterprise data                          │
│  $39/seat       + $70-130/seat                             │
│                                                             │
│  ─ ─ ─ ─ Option C not recommended ─ ─ ─ ─ ─ ─ ─ ─ ─ ─    │
│  Full build eliminated unless 20+ architect seats needed    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Start with Option A** (proven, zero infrastructure, 96.1% quality). **Evolve to Option B** when specific enterprise data needs are validated (DD-01 criteria). **Eliminate Option C** unless the organization grows to 20+ architect seats with deep enterprise integration requirements.

---

## Validation POC Plan

Before committing beyond Option A, a 4-6 week validation POC is recommended:

| Week | Activity |
|------|----------|
| 1-2 | Instrument current workflow to measure enterprise data access frequency (how often do architects need CMDB / cross-team ADR data during AI sessions?) |
| 3-4 | Build one targeted MCP server (CMDB lookup) as a prototype; measure latency, reliability, and value-add |
| 5-6 | Score 3 architecture sessions with vs without the MCP server; compare quality scores |
| Final | Decision: proceed to Option B or remain at Option A based on measured impact |

---

## Links

- [Decision Framework](decisions/decision-framework.md) — How these options were composed from four independent decisions
- [DD-01: Content Injection](decisions/dd-01-content-injection.md)
- [DD-02: Injection Location](decisions/dd-02-injection-location.md)
- [DD-03: Billing Model](decisions/dd-03-billing-model.md)
- [DD-04: AI Provider](decisions/dd-04-ai-provider.md)
- [Evaluation Framework](evaluation-framework.md) — Phase 1 methodology
