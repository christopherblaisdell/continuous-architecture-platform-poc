# AI Platform Selection Plan — Weighted Scorecard (Layer 1)

**Date**: 2026-03-31
**Status**: Draft — Ready for Review
**Author**: Solution Architecture Team
**Related**: [AI Decision Points (Layer 2)](AI-ARCHITECTURE-PRACTICE-DECISION-POINTS.md) | [Strategic Realignment Research](STRATEGIC-REALIGNMENT-ENTERPRISE-AI-ARCHITECTURE-RESEARCH.md) | [ADR-001](../decisions/ADR-001-ai-toolchain-selection.md)

---

## Purpose

This document is the **execution plan** for making the AI platform selection decision using a formal weighted scorecard. It defines:

0. Three solution options — detailed enough to score against evaluation factors
1. Evaluation factors — what the company needs to consider
2. Factor weights — how important each factor is to the company
3. Scoring method — how each option is rated on each factor
4. Final computation — how to arrive at a ranked recommendation

This is the **Layer 1 (Platform Selection Scorecard)** artifact described in the two-layer decision model. It replaces the informal ADR-001 evaluation criteria (which were scoped to IDE tool comparison only) with a comprehensive platform-level assessment that covers architecture, cost, governance, extensibility, and operational concerns.

---

## Methodology: Parallel Build (Option C)

This plan uses the **Parallel Build** methodology:

1. Draft solution options and evaluation factors simultaneously
2. Cross-check: every factor must discriminate between at least two options; every option must differ meaningfully on the factors
3. Lock factors and weights
4. Score each option on each factor
5. Compute weighted scores and rank

---

## Part 0: Solution Options

Three options represent genuinely different investment levels and capability profiles. Each is described in enough detail to score.

### Option 1: Copilot Pro+ Standalone (Lean)

**Summary**: GitHub Copilot Pro+ is the sole AI platform. All architectural work happens inside VS Code Agent Mode. Enterprise context is provided through the existing workspace (specs, metadata, instructions) and local MCP servers (ticketing, mock tools). No custom AI backend infrastructure is built.

**Architecture**:

```
┌────────────────────────────────────────────────────────────┐
│  Architect's VS Code                                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  GitHub Copilot Pro+ (Agent Mode)                    │  │
│  │  - Claude Opus 4.6 via GitHub                        │  │
│  │  - copilot-instructions.md (700+ lines)              │  │
│  │  - .instructions.md, SKILL.md files                  │  │
│  │  - Workspace semantic indexing (built-in)             │  │
│  └──────────┬───────────────────────────────┬───────────┘  │
│             │                               │              │
│  ┌──────────▼──────────┐  ┌─────────────────▼───────────┐  │
│  │  Local MCP Servers  │  │  CI/CD Pipeline             │  │
│  │  - Vikunja tickets  │  │  - MkDocs build + publish   │  │
│  │  - Mock tools       │  │  - Schema validation        │  │
│  │  - Confluence (MCP) │  │  - Confluence mirror        │  │
│  └─────────────────────┘  └─────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

**Cost model**:

| Component | Monthly Cost per Seat |
|-----------|---------------------|
| Copilot Pro+ subscription | $39.00 |
| Overage (if >1,500 premium requests) | $0.04 x model multiplier per request |
| Azure Static Web Apps (portal) | ~$10 (shared) |
| Infrastructure engineering | $0 (no custom backend) |
| **Total per seat** | **~$39-50** |

**What you get**:
- 96.1% quality score (proven in Phase 1, 149/155)
- Intent-based billing: autonomous agent work is free; only user prompts cost
- Deep VS Code + GitHub integration (PRs, code suggestions, agent mode)
- Custom instructions, skills, and agent files for domain knowledge
- Native workspace semantic indexing — no custom RAG needed
- MCP integration for local tool servers (ticketing, mock tools, Confluence)
- GitOps governance: instruction changes go through PR review
- Existing CI/CD pipeline for deterministic validation and publishing

**What you do NOT get**:
- No access to proprietary enterprise databases beyond what MCP servers expose locally
- No centralized AI governance dashboard — governance is repo-based only
- No custom model fine-tuning or specialization
- No enterprise-wide AI usage analytics beyond GitHub's built-in reporting
- Dependent on GitHub's model availability, pricing, and feature roadmap
- No offline or air-gapped operation

**Governance model**: Repository-based. `copilot-instructions.md` + `.instructions.md` files in the repo. Changes reviewed via PR. CI/CD pipeline is the deterministic compliance gate. No centralized admin UI.

**Operational complexity**: Minimal. One VS Code extension + local MCP servers. No infrastructure to provision, monitor, or maintain beyond the existing portal hosting.

**Timeline to production value**: Already in production. No additional ramp-up needed.

---

### Option 2: Copilot + Azure MCP Services (Hybrid)

**Summary**: GitHub Copilot Pro+ remains the local execution engine and primary UX. Azure AI Foundry hosts custom MCP servers that expose enterprise-specific tools — proprietary databases, governed APIs, specialized compliance checks, and enterprise-wide knowledge retrieval. The local agent calls Azure services on demand via MCP.

**Architecture**:

```
┌────────────────────────────────────────────────────────────┐
│  Architect's VS Code                                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  GitHub Copilot Pro+ (Agent Mode)                    │  │
│  │  - Claude Opus 4.6 via GitHub                        │  │
│  │  - Full local execution autonomy                     │  │
│  │  - MCP client connecting to local + remote servers   │  │
│  └──────────┬───────────────────┬───────────────────────┘  │
│             │                   │                          │
│  ┌──────────▼──────────┐       │                          │
│  │  Local MCP Servers  │       │                          │
│  │  - Vikunja tickets  │       │                          │
│  │  - Mock tools       │       │                          │
│  └─────────────────────┘       │                          │
└────────────────────────────────┼──────────────────────────┘
                                 │  MCP (HTTPS/SSE)
                                 │
┌────────────────────────────────▼──────────────────────────┐
│  Azure AI Foundry (Enterprise Backend)                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Custom MCP Servers                                  │  │
│  │  - Enterprise Confluence indexer (vector store)       │  │
│  │  - Architecture standards validator                  │  │
│  │  - Enterprise CMDB/ServiceNow integration            │  │
│  │  - Compliance checker (security, data classification)│  │
│  │  - Cross-team architecture knowledge graph           │  │
│  └──────────┬───────────────────────────────────────────┘  │
│             │                                              │
│  ┌──────────▼──────────────────────────────────────────┐   │
│  │  Azure Infrastructure                               │   │
│  │  - Entra ID (auth + RBAC)                           │   │
│  │  - Azure AI Search (vector index)                   │   │
│  │  - Azure Key Vault (secrets)                        │   │
│  │  - Azure Monitor (usage analytics)                  │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────┘
```

**Cost model**:

| Component | Monthly Cost per Seat |
|-----------|---------------------|
| Copilot Pro+ subscription | $39.00 |
| Azure AI Foundry (compute for MCP servers) | ~$50-150 (shared across team) |
| Azure AI Search (vector index) | ~$75-250 (shared, depends on data volume) |
| Azure infrastructure (Key Vault, Monitor, networking) | ~$20-50 (shared) |
| Engineering effort to build + maintain MCP servers | Significant — estimated 2-4 developer-months initial, 0.5-1 FTE ongoing |
| **Total per seat (5-person team)** | **~$70-130** (infrastructure amortized) |

**What you get**:
- Everything in Option 1, plus:
- Secure, governed access to enterprise data sources (CMDB, Confluence at scale, ServiceNow, internal APIs)
- Centralized vector store for enterprise-wide architecture knowledge retrieval
- Custom compliance and validation tools callable from the local agent
- Enterprise identity (Entra ID) for access control on all backend tools
- Usage analytics and audit logging via Azure Monitor
- Ability to build specialized tools for any enterprise backend
- MCP is an open standard — backend services are not locked to Copilot

**What you do NOT get**:
- No custom chat UX — still using VS Code Copilot as the interface
- No custom model hosting — still using GitHub's model routing
- No custom model fine-tuning
- Adds operational complexity: Azure infrastructure needs provisioning, monitoring, cost management
- MCP remote servers (HTTPS/SSE) are still maturing — protocol stability risk
- Engineering investment required before value is delivered

**Governance model**: Dual-layer. Repository-based governance (same as Option 1) for instruction management. Azure-based governance for backend tool access (Entra ID RBAC, API auditing, Key Vault for secrets). Centralized usage analytics via Azure Monitor.

**Operational complexity**: Moderate. Existing Copilot workflow is unchanged. New Azure infrastructure must be provisioned, MCP servers developed, and backend services monitored. Requires DevOps/cloud engineering capacity.

**Timeline to production value**: 3-6 months for first MCP services. Incremental — each new MCP server adds a capability without disrupting the existing workflow.

---

### Option 3: Custom AI Platform on Azure (Full Build)

**Summary**: Azure AI Foundry is the primary AI platform. A custom web application provides the architecture assistant UX — a purpose-built chat interface with embedded architecture tooling, enterprise knowledge retrieval, and centralized governance. Copilot may remain available for basic coding assistance but is not the architecture workflow tool.

**Architecture**:

```
┌────────────────────────────────────────────────────────────┐
│  Custom Architecture AI Portal (Web Application)           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Custom Chat UX                                      │  │
│  │  - Architecture-specific interface                   │  │
│  │  - Embedded diagram viewer and editor                │  │
│  │  - Ticket triage dashboard                           │  │
│  │  - Solution design wizard                            │  │
│  └──────────┬───────────────────────────────────────────┘  │
│             │                                              │
│  ┌──────────▼──────────────────────────────────────────┐   │
│  │  Azure AI Foundry — Agent Orchestrator              │   │
│  │  - Custom agent with architecture system prompt      │   │
│  │  - RAG pipeline (Azure AI Search + embeddings)       │   │
│  │  - Tool calling: CMDB, Confluence, JIRA, GitLab     │   │
│  │  - Model selection: Claude/GPT per task type         │   │
│  │  - Custom fine-tuned model (optional, Phase 2)       │   │
│  └──────────┬───────────────────────────────────────────┘   │
│             │                                              │
│  ┌──────────▼──────────────────────────────────────────┐   │
│  │  Azure Infrastructure                               │   │
│  │  - Entra ID + custom RBAC                           │   │
│  │  - Azure AI Search (enterprise vector store)        │   │
│  │  - Azure Cosmos DB (conversation state, audit log)  │   │
│  │  - Azure App Service (web app hosting)              │   │
│  │  - Azure Key Vault, Monitor, Front Door             │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  Architect's VS Code (secondary)                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  GitHub Copilot (basic coding assistance)            │  │
│  │  - Code suggestions and inline chat                  │  │
│  │  - NOT the primary architecture workflow tool        │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

**Cost model**:

| Component | Monthly Cost per Seat |
|-----------|---------------------|
| Copilot Pro+ (optional, basic coding only) | $39.00 |
| Azure AI Foundry (model inference) | ~$200-500 (token-based, per-seat share) |
| Azure AI Search (enterprise vector store) | ~$75-250 (shared) |
| Azure App Service (web app) | ~$50-150 (shared) |
| Azure Cosmos DB (state management) | ~$25-100 (shared) |
| Azure infrastructure (networking, monitoring, security) | ~$50-100 (shared) |
| Engineering effort: web app + agent + RAG pipeline | Major — estimated 6-12 developer-months initial, 1-2 FTE ongoing |
| **Total per seat (5-person team)** | **~$150-350** (infrastructure amortized) |

**What you get**:
- Purpose-built UX designed specifically for architecture workflows
- Full control over the AI model: choose, switch, fine-tune, or host your own
- Enterprise-wide knowledge retrieval with custom RAG pipeline
- Centralized governance dashboard with audit logging, usage analytics, and access controls
- Custom agent orchestration with architecture-specific tools
- Full autonomy from GitHub's platform direction — no dependency on Copilot's feature roadmap
- Ability to serve non-VS-Code users (browser-based, accessible to stakeholders)
- Custom fine-tuning on the practice's own architecture corpus (future)

**What you do NOT get**:
- No deep VS Code integration — the custom web app is a separate window/tab
- No inline code suggestions or PR review assistance (unless rebuilt)
- No intent-based billing — model inference is token-based (pay per token)
- Massive engineering investment before first useful output
- Operational burden: web app, agent, RAG pipeline, vector store, database, networking all need monitoring
- Custom UX must be built, tested, and maintained — competes with GitHub's product engineering team
- Agent execution engine (autonomous multi-step tool calling, file editing, terminal access) must be built from scratch — this is the hardest part
- State management for long-running agent sessions is a known hard problem in custom builds
- No community ecosystem of skills, extensions, or integrations

**Governance model**: Fully centralized. Custom RBAC, audit logging, usage dashboards, model governance — all controlled by the architecture practice. Maximum control, maximum maintenance.

**Operational complexity**: High. Full-stack application to build, deploy, and operate. Requires dedicated DevOps, frontend, backend, and AI engineering capacity. Ongoing model cost management, infrastructure monitoring, and security patching.

**Timeline to production value**: 6-12 months minimum for MVP. 12-18 months for feature parity with the current Copilot workflow. Ongoing development indefinitely.

---

## Option Cross-Reference Summary

| Dimension | Option 1: Copilot Standalone | Option 2: Copilot + Azure MCP | Option 3: Custom Platform |
|-----------|------------------------------|-------------------------------|---------------------------|
| Monthly cost per seat | ~$39-50 | ~$70-130 | ~$150-350 |
| Engineering investment | None (already running) | 2-4 dev-months + 0.5 FTE ongoing | 6-12 dev-months + 1-2 FTE ongoing |
| Time to production value | Now (already live) | 3-6 months | 6-18 months |
| Enterprise data access | Local workspace + local MCP | Local + Azure-hosted MCP services | Full custom RAG + tool integration |
| UX | VS Code (Copilot Agent Mode) | VS Code (same) | Custom web app |
| Agent execution | GitHub-managed (free autonomous work) | GitHub-managed (same) | Custom-built (hard, expensive) |
| Model control | GitHub's model roster | GitHub's roster + Azure models for backend | Full control |
| Governance | Repository-based (GitOps) | Repository + Azure RBAC/audit | Fully centralized (custom) |
| Vendor dependency | High (GitHub) | Medium (GitHub + Azure) | Low (Azure, but self-maintained) |
| Billing model | Intent-based ($0.48/run) | Intent-based + Azure consumption | Token-based (~$5-15/run estimated) |
| Portability of knowledge | High (Markdown/YAML) | High (same + MCP is open standard) | Medium (locked in custom app) |
| Operational complexity | Minimal | Moderate | High |

---

## Part 1: Evaluation Factors

These factors are designed to discriminate between the three options. Each factor was cross-checked: does it differ meaningfully across at least two options?

### Factor Definitions

| # | Factor | Category | What It Measures | Why It Matters |
|---|--------|----------|-----------------|----------------|
| F-01 | Total cost of ownership (3-year) | Cost | All-in cost: subscriptions, infrastructure, engineering labor, ongoing maintenance | Budget directly affects feasibility and ROI timeline |
| F-02 | Time to first production value | Cost | Calendar time from decision to first useful architectural output | Late delivery means negative ROI in Year 1 |
| F-03 | Architecture output quality | Quality | Standards compliance, accuracy, completeness of AI-generated artifacts | The reason the practice is adopting AI — quality must not regress |
| F-04 | Enterprise data access breadth | Quality | Range of enterprise data sources the AI can query at runtime | Determines whether the AI can work beyond the local workspace |
| F-05 | Workflow integration depth | Workflow | Seamlessness with VS Code, GitHub PRs, CI/CD, existing DocFlow pipeline | Friction kills adoption; context switching reduces productivity |
| F-06 | Agent execution autonomy | Workflow | Ability to perform multi-step tasks (file edit, terminal, tool calls) without human intervention per step | Autonomous execution is what makes AI a force multiplier vs a chatbot |
| F-07 | Governance and auditability | Governance | Policy enforcement, change tracking, access control, usage monitoring | Enterprise mandate — non-negotiable for regulated environments |
| F-08 | Instruction management model | Governance | How AI behavior standards are defined, reviewed, versioned, and deployed | Determines whether the AI stays aligned with evolving architecture standards |
| F-09 | Extensibility and custom tooling | Extensibility | Ability to add new capabilities (tools, data sources, validation checks) over time | The platform must grow with the practice's needs |
| F-10 | Portability and exit cost | Portability | Cost and effort to migrate to a different platform if the current one fails or becomes unsuitable | De-risks the decision — reduces consequences of being wrong |
| F-11 | Operational burden | Operations | Infrastructure provisioning, monitoring, incident response, patching, scaling | Engineering effort diverted from architecture work to platform maintenance |
| F-12 | Scalability across teams | Operations | Effort to onboard additional architects or teams onto the platform | A platform that only works for one person has limited organizational value |

### Cross-Check: Factor Discrimination

Every factor discriminates between at least two options — confirmed:

| Factor | Options that differ most |
|--------|------------------------|
| F-01 Total cost | All three (1 order of magnitude range) |
| F-02 Time to value | Option 1 (now) vs Option 3 (6-18 months) |
| F-03 Quality | Needs scoring — Option 1 has evidence; Options 2-3 are projections |
| F-04 Enterprise data | Option 1 (local only) vs Options 2+3 (enterprise-wide) |
| F-05 Workflow integration | Options 1+2 (VS Code native) vs Option 3 (separate web app) |
| F-06 Agent execution | Options 1+2 (GitHub-managed, free) vs Option 3 (custom-built) |
| F-07 Governance | Option 1 (repo-only) vs Option 3 (fully centralized) |
| F-08 Instruction management | Options 1+2 (GitOps) vs Option 3 (custom admin) |
| F-09 Extensibility | Option 1 (limited to MCP) vs Options 2+3 (custom services) |
| F-10 Portability | Options 1+2 (knowledge in Markdown/YAML) vs Option 3 (locked in custom app) |
| F-11 Operational burden | Option 1 (near-zero) vs Option 3 (full-stack app) |
| F-12 Scalability | Option 1 (add seats) vs Option 3 (add infrastructure + training) |

---

## Part 2: Factor Weights

Weights reflect **what matters most to this architecture practice**, not what differentiates the options. They should be assigned before scoring to prevent bias.

### Proposed Weight Categories

Weights are distributed across 100 points. The allocation below is the **starting proposal** — it should be reviewed and adjusted by the decision-making stakeholders before scoring begins.

| # | Factor | Proposed Weight | Rationale |
|---|--------|----------------|-----------|
| F-01 | Total cost of ownership | **15%** | Important but not dominant — the practice must justify spend, but cheapest is not necessarily best |
| F-02 | Time to first production value | **10%** | High weight for a practice that is already delivering value — delay has real opportunity cost |
| F-03 | Architecture output quality | **20%** | The primary reason for adopting AI. Quality regression is unacceptable |
| F-04 | Enterprise data access breadth | **8%** | Strategically valuable but not immediately blocking — current local workspace approach works |
| F-05 | Workflow integration depth | **12%** | High because friction directly reduces adoption and productivity |
| F-06 | Agent execution autonomy | **10%** | The difference between a chatbot and a force multiplier |
| F-07 | Governance and auditability | **8%** | Mandatory for enterprise adoption, but the current repo-based approach may suffice initially |
| F-08 | Instruction management model | **5%** | Important for long-term maintenance, but the differences are manageable |
| F-09 | Extensibility and custom tooling | **5%** | Future-proofing — matters more as the practice matures |
| F-10 | Portability and exit cost | **3%** | Risk mitigation — matters if vendor relationship deteriorates |
| F-11 | Operational burden | **2%** | Running infrastructure diverts engineering effort from architecture work |
| F-12 | Scalability across teams | **2%** | Matters when the practice grows beyond the current team |
| | **TOTAL** | **100%** | |

### Stakeholder Weight Review (REQUIRED)

NOTE: These weights are the **architect's starting proposal only**. They have NOT been reviewed or ratified by the broader decision-making stakeholders. Before final scoring, all stakeholders who will be affected by this decision must have the opportunity to adjust the weight allocation. Different roles may have materially different priorities (e.g., engineering leadership may weight cost and operational burden higher; security may weight governance higher; individual architects may weight workflow integration higher).

**Process for stakeholder input:**

1. Circulate this factor/weight table to all stakeholders
2. Each stakeholder independently distributes 100 points across the 12 factors
3. Average the distributions (or discuss divergences to reach consensus)
4. Lock the consensus weights before any scoring begins
5. Document who participated and the final agreed weights

### Weight Adjustment Process

Before scoring, the decision-making stakeholders should:

1. Review the 12 factors — add, remove, or combine as needed
2. Distribute 100 points across the final factor set
3. Validate: does the weight distribution reflect actual priorities? Would you trade a high score on a low-weight factor for a lower score on a high-weight factor?
4. Lock weights before any scoring begins

---

## Part 3: Scoring Method

### Scale

Each option is scored on each factor using a **1-5 scale**:

| Score | Meaning | Guidance |
|-------|---------|----------|
| 1 | Poor | Does not meet the need; significant risk or gap |
| 2 | Below Average | Partially meets the need; notable limitations |
| 3 | Adequate | Meets the basic need; acceptable but not differentiated |
| 4 | Good | Meets the need well; minor limitations only |
| 5 | Excellent | Fully meets or exceeds the need; clear strength |

### Scoring Rules

1. **Evidence-based scoring**: each score must cite evidence (measured data, documented capability, or reasoned projection). No scores without justification
2. **Comparative, not absolute**: a score of 3 means "adequate for this practice's needs" — not "average in the market"
3. **Score the option as designed above**: do not score aspirational futures. Score what each option delivers at the stated investment level
4. **Uncertainty is penalized**: if a capability is projected but unproven, it scores lower than a proven capability of equal potential
5. **Each factor scored independently**: do not let a high score on one factor inflate scores on others

### Preliminary Score Estimates

These are **draft estimates** based on available evidence. They should be validated and adjusted during the formal scoring session.

| # | Factor (Weight) | Option 1: Copilot Standalone | Option 2: Copilot + Azure MCP | Option 3: Custom Platform |
|---|----------------|------------------------------|-------------------------------|--------------------------|
| F-01 | Total cost (15%) | **5** — $39/seat, no infrastructure; 3-year TCO ~$1,400/seat | **3** — ~$100/seat + Azure + engineering; 3-year TCO ~$20K-40K/seat | **1** — ~$250/seat + major engineering; 3-year TCO ~$80K-150K/seat |
| F-02 | Time to value (10%) | **5** — Already in production, delivering 96.1% quality | **3** — 3-6 months to first Azure MCP service | **1** — 6-18 months to MVP |
| F-03 | Quality (20%) | **4** — 96.1% proven (149/155); limited by local workspace context | **4** — Same Copilot quality + enterprise context should improve it | **3** — Unproven; custom agent quality depends entirely on engineering |
| F-04 | Enterprise data (8%) | **2** — Local workspace + local MCP only; no direct enterprise DB access | **4** — Azure MCP services can reach enterprise data sources | **5** — Full custom RAG + enterprise integration |
| F-05 | Workflow integration (12%) | **5** — Native VS Code + GitHub + CI/CD; zero context switching | **5** — Same VS Code integration (Azure services are transparent) | **2** — Separate web app; context switching between VS Code and browser |
| F-06 | Agent execution (10%) | **5** — GitHub-managed autonomous execution; free multi-step agent work | **5** — Same GitHub execution + backend tools via MCP | **2** — Must build from scratch; state management is hard; latency |
| F-07 | Governance (8%) | **3** — Repo-based only; no centralized audit or usage analytics | **4** — Repo-based + Azure RBAC + Monitor for audit trail | **5** — Fully centralized dashboard; maximum control |
| F-08 | Instruction mgmt (5%) | **4** — GitOps model works well; PR-reviewed; version-controlled | **4** — Same GitOps model (enterprise tools governed separately) | **3** — Custom admin UI must be built; governance of prompts is harder |
| F-09 | Extensibility (5%) | **3** — Limited to what MCP servers can do locally | **5** — Azure MCP servers can integrate anything; MCP is open standard | **5** — Full custom integration capability |
| F-10 | Portability (3%) | **4** — Knowledge layer is Markdown/YAML; execution depends on Copilot | **4** — Same portability; MCP backend services are reusable with any client | **2** — Custom UX, RAG pipeline, agent logic locked in Azure app |
| F-11 | Operational burden (2%) | **5** — Near-zero ops; GitHub manages the platform | **3** — Azure infrastructure needs provisioning + monitoring | **1** — Full-stack app: web, database, search, agent, monitoring |
| F-12 | Scalability (2%) | **4** — Add a seat + share the repo; instructions propagate automatically | **4** — Same + Azure services scale; cost increases per-user are modest | **3** — Custom app must be scaled, tested under load, and supported |

### Preliminary Weighted Scores

| Factor | Weight | Opt 1 Raw | Opt 1 Weighted | Opt 2 Raw | Opt 2 Weighted | Opt 3 Raw | Opt 3 Weighted |
|--------|--------|-----------|----------------|-----------|----------------|-----------|----------------|
| F-01 Total cost | 15% | 5 | 0.75 | 3 | 0.45 | 1 | 0.15 |
| F-02 Time to value | 10% | 5 | 0.50 | 3 | 0.30 | 1 | 0.10 |
| F-03 Quality | 20% | 4 | 0.80 | 4 | 0.80 | 3 | 0.60 |
| F-04 Enterprise data | 8% | 2 | 0.16 | 4 | 0.32 | 5 | 0.40 |
| F-05 Workflow integration | 12% | 5 | 0.60 | 5 | 0.60 | 2 | 0.24 |
| F-06 Agent execution | 10% | 5 | 0.50 | 5 | 0.50 | 2 | 0.20 |
| F-07 Governance | 8% | 3 | 0.24 | 4 | 0.32 | 5 | 0.40 |
| F-08 Instruction mgmt | 5% | 4 | 0.20 | 4 | 0.20 | 3 | 0.15 |
| F-09 Extensibility | 5% | 3 | 0.15 | 5 | 0.25 | 5 | 0.25 |
| F-10 Portability | 3% | 4 | 0.12 | 4 | 0.12 | 2 | 0.06 |
| F-11 Operational burden | 2% | 5 | 0.10 | 3 | 0.06 | 1 | 0.02 |
| F-12 Scalability | 2% | 4 | 0.08 | 4 | 0.08 | 3 | 0.06 |
| **TOTAL** | **100%** | | **4.20** | | **4.00** | | **2.63** |

### Preliminary Ranking

| Rank | Option | Weighted Score | Profile |
|------|--------|---------------|---------|
| 1 | Option 1: Copilot Standalone | **4.20 / 5.00** | Highest in cost, speed, workflow, execution. Weakest in enterprise data access |
| 2 | Option 2: Copilot + Azure MCP | **4.00 / 5.00** | Close second. Gains enterprise data and governance at moderate cost. Same workflow quality |
| 3 | Option 3: Custom Platform | **2.63 / 5.00** | Strongest in enterprise data and governance. Weakest in cost, speed, workflow, execution |

---

## Part 4: Execution Plan

### Step-by-Step Process

| Step | Activity | Owner | Output | Duration |
|------|----------|-------|--------|----------|
| **Step 0** | Review the three solution options in this document. Are they the right options? Should any be added, removed, or modified? | Decision stakeholders | Finalized option set | 1 session |
| **Step 1** | Review the 12 evaluation factors. Add, remove, or combine factors as needed. Confirm that every factor discriminates between options | Decision stakeholders | Finalized factor list | Same session |
| **Step 2** | Assign weights. Distribute 100 points across the finalized factors. Validate with trade-off test: would you trade a high score on a low-weight factor for a lower score on a high-weight factor? | Decision stakeholders | Locked weight allocation | Same session |
| **Step 3** | Score each option on each factor. Use 1-5 scale. Every score must have a written justification citing evidence or reasoned projection. Use the preliminary scores as a starting point | Decision stakeholders + architect | Completed scorecard with justifications | 1-2 sessions |
| **Step 4** | Compute weighted scores. Identify the winning option. Perform sensitivity analysis: do the rankings change if the top 2-3 weight allocations shift by +/-5%? | Architect | Final ranking + sensitivity analysis | 1 session |
| **Step 5** | Document the decision as a formal ADR (amend ADR-001 or create ADR-015). Reference this scorecard as evidence | Architect | Published ADR | After decision |
| **Step 6** | Translate the platform decision into Layer 2 operating model decisions. Update the AI Decision Points document to reflect any operating-model choices that are now constrained by the platform selection | Architect | Updated decision-point document | After ADR |

### Sensitivity Analysis Guidance

After scoring, test the following scenarios to verify the result is robust:

1. **"What if enterprise data access matters more?"** — Move F-04 weight from 8% to 18% (take 10% from F-01 and F-02). Does Option 2 overtake Option 1?
2. **"What if cost matters less?"** — Move F-01 weight from 15% to 5% (redistribute to F-07 and F-09). Does Option 3 become competitive?
3. **"What if quality evidence changes?"** — If Option 3 quality score improves to 4 (parity with Option 1), does the ranking change?
4. **"What if GitHub changes pricing?"** — If Copilot moves to token-based billing (F-01 score drops to 3), does the ranking change?

### Decision Threshold

The winning option should score at least **0.5 points higher** than the second-place option to justify a clear recommendation. If the gap is smaller, the decision is close enough to warrant deeper investigation of the differentiating factors or a hybrid approach (e.g., start with Option 1, plan migration path to Option 2).

---

## Relationship to Existing Artifacts

| Artifact | Relationship |
|----------|-------------|
| [ADR-001](../decisions/ADR-001-ai-toolchain-selection.md) | ADR-001 evaluated IDE tools only (5 factors). This scorecard evaluates full solution architectures (12 factors). The final decision should amend or supersede ADR-001 |
| [AI Decision Points (Layer 2)](AI-ARCHITECTURE-PRACTICE-DECISION-POINTS.md) | This scorecard is Layer 1 (platform selection). The decision-point document is Layer 2 (operating model). The selected platform constrains which Layer 2 decisions are relevant |
| [Strategic Realignment Research](STRATEGIC-REALIGNMENT-ENTERPRISE-AI-ARCHITECTURE-RESEARCH.md) | The research advocated the hybrid model (Option 2). This scorecard tests that advocacy against formal criteria |

---

## Open Questions

1. **Are three options sufficient, or should a fourth be added?** (e.g., Claude Code standalone, or a multi-vendor option)
2. **Should the Claude Code spike (planned in ADR-001) be completed before scoring?** The spike could inform the Single vs Multi-Tool decision (DP-04) and may affect quality scores
3. **Who are the decision-making stakeholders?** This plan assumes the architecture practice lead + engineering leadership. If other stakeholders are involved, their priorities may shift the weight allocation
4. **Should this scoring be done in a single workshop or across multiple sessions?** A single workshop maintains momentum; multiple sessions allow for research between steps
