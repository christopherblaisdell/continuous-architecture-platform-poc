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

### Stakeholder Score Review (REQUIRED)

NOTE: These scores are the **architect's preliminary estimates only**. Every score must be defensible to stakeholders who may challenge it. Before the scorecard is finalized:

1. Circulate the scored scorecard (below) to all stakeholders
2. Each score includes a written justification — stakeholders should challenge any justification they find insufficient
3. Stakeholders may propose alternative scores with their own justifications
4. Disputed scores are resolved through discussion, not averaging — the goal is consensus on the evidence, not compromise on numbers
5. Lock scores only after all stakeholders have had the opportunity to review and challenge
6. Document dissenting views — if a stakeholder disagrees with a final score, record their position and reasoning

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

### Score Justification Details

Every score must be defensible. This section provides the detailed justification for each preliminary score.

#### F-01: Total Cost of Ownership (15%)

| Option | Score | Justification |
|--------|-------|---------------|
| 1: Copilot Standalone | **5** | **Measured.** $39/seat/month. 3-year TCO per seat: ~$1,400. No infrastructure cost. No engineering build cost. Billing data from ADR-001: $0.48/run actual (verified March 4, 2026). Zero overage within 1,500 included requests |
| 2: Copilot + Azure MCP | **3** | **Projected.** $39/seat + Azure compute (~$50-150/month shared) + Azure AI Search (~$75-250/month shared) + 2-4 dev-months build + 0.5 FTE ongoing. 3-year TCO per seat (5-person team): ~$20K-40K. Moderate cost increase for enterprise capability gain |
| 3: Custom Platform | **1** | **Projected.** $39/seat (optional Copilot) + Azure AI Foundry (~$200-500/month) + App Service + Cosmos DB + AI Search + 6-12 dev-months + 1-2 FTE ongoing. 3-year TCO per seat: ~$80K-150K. Order-of-magnitude more expensive than Option 1 |

#### F-02: Time to First Production Value (10%)

| Option | Score | Justification |
|--------|-------|---------------|
| 1: Copilot Standalone | **5** | **Measured.** Already in production. Delivering 96.1% quality across 5 architecture scenarios since March 2026. Zero additional ramp-up |
| 2: Copilot + Azure MCP | **3** | **Projected.** Existing Copilot workflow continues immediately. First Azure MCP service estimated 3-6 months (Azure provisioning + MCP server development + security review + testing). Incremental — each subsequent MCP service adds value faster |
| 3: Custom Platform | **1** | **Projected.** 6-12 months to MVP (web app + agent + RAG pipeline + auth). 12-18 months for feature parity with current Copilot workflow. No architecture value delivered during build phase. Significant opportunity cost |

#### F-03: Architecture Output Quality (20%)

| Option | Score | Justification |
|--------|-------|---------------|
| 1: Copilot Standalone | **4** | **Measured.** 96.1% quality (149/155) across 5 scenarios in Phase 1. Not 5 because quality is bounded by local workspace context — the AI cannot access enterprise data it has never seen. Proven, not projected |
| 2: Copilot + Azure MCP | **4** | **Projected.** Same Copilot quality engine + enterprise context via MCP should maintain or improve quality. Score not higher than Option 1 because: (a) Azure MCP services are unbuilt and unproven, (b) quality improvement from enterprise data access is hypothetical, (c) uncertainty penalized per scoring rules |
| 3: Custom Platform | **3** | **Projected.** Custom agent quality depends entirely on engineering execution. No benchmark data. Custom RAG could theoretically outperform Copilot's built-in indexing for enterprise data, but agent execution quality (multi-step reasoning, file editing, tool use) is extremely hard to replicate. Scored adequate — could be higher or lower depending on build quality |

#### F-04: Enterprise Data Access Breadth (8%)

| Option | Score | Justification |
|--------|-------|---------------|
| 1: Copilot Standalone | **2** | **Measured.** Access limited to local workspace files + local MCP servers (Vikunja, mock tools). Cannot reach enterprise CMDB, ServiceNow, Confluence at scale, or internal APIs beyond what's checked into the repo. Scored 2 (not 1) because local MCP integration exists and works |
| 2: Copilot + Azure MCP | **4** | **Projected.** Azure-hosted MCP services can reach any enterprise data source with proper auth (Entra ID). Scored 4 (not 5) because: services are unbuilt, latency over HTTPS/SSE is unknown, and MCP remote transport is still maturing |
| 3: Custom Platform | **5** | **Projected.** Full custom RAG pipeline with Azure AI Search can index enterprise-wide data. Custom tool integrations can reach any API. Maximum possible data access breadth. Scored 5 despite being unbuilt because the architectural ceiling is highest here |

#### F-05: Workflow Integration Depth (12%)

| Option | Score | Justification |
|--------|-------|---------------|
| 1: Copilot Standalone | **5** | **Measured.** Native VS Code integration: inline suggestions, agent mode, PR review, terminal access, file editing. Zero context switching. GitHub ecosystem (PRs, Actions, branches) fully integrated. CI/CD pipeline integration proven |
| 2: Copilot + Azure MCP | **5** | **Projected.** Same VS Code integration. Azure MCP services are called transparently by the Copilot agent — the architect never leaves VS Code. MCP calls are invisible to the user experience. Same score as Option 1 because the UX is identical |
| 3: Custom Platform | **2** | **Projected.** Custom web app runs in a browser, separate from VS Code. Architect must switch between IDE (for code) and browser (for AI). No inline code suggestions. No PR review integration unless rebuilt. Fundamental workflow disruption |

#### F-06: Agent Execution Autonomy (10%)

| Option | Score | Justification |
|--------|-------|---------------|
| 1: Copilot Standalone | **5** | **Measured.** GitHub-managed autonomous execution: file reading/writing, terminal commands, sub-agent spawning, MCP tool calls — all in a single agent loop. Autonomous work is free (intent-based billing). Proven across 5 scenarios with multi-step solution designs |
| 2: Copilot + Azure MCP | **5** | **Projected.** Same Copilot execution engine. Azure MCP services add tools to the agent's toolkit without changing the execution model. Each Azure tool call is just another tool in the autonomous loop |
| 3: Custom Platform | **2** | **Projected.** Autonomous multi-step execution with file editing and terminal access must be built from scratch. This is the hardest engineering challenge in custom AI agent development. State management across long agent sessions is a known unsolved problem. Azure AI Foundry Agents provide some primitives but not VS Code-level file system and terminal access. Scored 2 (not 1) because basic tool calling is available in Foundry |

#### F-07: Governance and Auditability (8%)

| Option | Score | Justification |
|--------|-------|---------------|
| 1: Copilot Standalone | **3** | **Measured.** Governance is repository-based: instruction changes go through PR review, git history provides version control, CI/CD validates outputs. No centralized audit dashboard. No usage analytics beyond GitHub's built-in metrics. Adequate for current scale but may not satisfy enterprise audit requirements |
| 2: Copilot + Azure MCP | **4** | **Projected.** Same repo-based governance for instructions + Azure RBAC for backend tool access + Azure Monitor for audit logging + Key Vault for secrets. Dual-layer governance model provides both developer-facing and enterprise-facing controls |
| 3: Custom Platform | **5** | **Projected.** Fully centralized governance: custom RBAC, audit logging, usage dashboards, model governance, access controls. Maximum control. Every interaction logged and auditable. Highest governance ceiling — but must be built entirely |

#### F-08: Instruction Management Model (5%)

| Option | Score | Justification |
|--------|-------|---------------|
| 1: Copilot Standalone | **4** | **Measured.** GitOps model: instructions in repo, changes via PR, version-controlled, peer-reviewed. 700+ line copilot-instructions.md + modular .instructions.md + SKILL.md files. Proven effective. Scored 4 (not 5) because the monolith/modular balance is not yet formalized (DP-07) |
| 2: Copilot + Azure MCP | **4** | **Projected.** Same GitOps model for Copilot instructions. Azure-hosted tools governed separately via Azure policies. No conflict between the two governance models |
| 3: Custom Platform | **3** | **Projected.** Custom admin UI must be built for prompt management. Version control and peer review of prompts is possible but not automatic — must be designed into the platform. Risk of prompt drift if governance is an afterthought |

#### F-09: Extensibility and Custom Tooling (5%)

| Option | Score | Justification |
|--------|-------|---------------|
| 1: Copilot Standalone | **3** | **Measured.** Extensible via local MCP servers only. Each new tool requires a local Python/Node script. Cannot integrate with enterprise backends that require server-side auth or network access. Adequate for current needs but limited ceiling |
| 2: Copilot + Azure MCP | **5** | **Projected.** Azure MCP servers can integrate with any enterprise backend. MCP is an open standard — services are reusable with any MCP client. Each new capability is a new MCP server deployment, not a platform rebuild |
| 3: Custom Platform | **5** | **Projected.** Full custom integration capability. Can build any tool, any integration, any workflow. Same ceiling as Option 2 for enterprise integrations, plus custom UX integrations that MCP cannot provide |

#### F-10: Portability and Exit Cost (3%)

| Option | Score | Justification |
|--------|-------|---------------|
| 1: Copilot Standalone | **4** | **Measured.** Knowledge layer is entirely Markdown/YAML — portable to any AI tool. OpenAPI specs, MADR ADRs, YAML metadata are standard formats. Only the execution configuration (copilot-instructions.md, hooks) is Copilot-specific. Scored 4 (not 5) because switching execution tools requires instruction translation |
| 2: Copilot + Azure MCP | **4** | **Projected.** Same knowledge portability. MCP backend services are protocol-standard — reusable with any MCP-compatible client (Claude Code, Roo Code, etc.). Azure infrastructure is relocatable. Same exit cost as Option 1 |
| 3: Custom Platform | **2** | **Projected.** Custom web UX, RAG pipeline, agent logic, and state management are proprietary to the build. Knowledge in the vector store may be portable, but the orchestration layer is not. Highest switching cost — exit means abandoning the custom build |

#### F-11: Operational Burden (2%)

| Option | Score | Justification |
|--------|-------|---------------|
| 1: Copilot Standalone | **5** | **Measured.** GitHub manages the platform: model hosting, indexing, billing, uptime. Architect's operational burden is zero beyond VS Code extension updates. Portal hosting (Azure Static Web Apps) is the only infrastructure |
| 2: Copilot + Azure MCP | **3** | **Projected.** Azure infrastructure needs provisioning (IaC), monitoring (Azure Monitor), cost management, security patching, and incident response. Each MCP server is a deployed service. Moderate ops overhead — manageable with IaC but not zero |
| 3: Custom Platform | **1** | **Projected.** Full-stack application: web frontend, API backend, database, vector store, search service, agent orchestrator, model endpoint, networking, monitoring, security. Each component needs provisioning, patching, scaling, and incident response. Significant DevOps investment |

#### F-12: Scalability Across Teams (2%)

| Option | Score | Justification |
|--------|-------|---------------|
| 1: Copilot Standalone | **4** | **Measured.** Add a Copilot seat, share the repo. Instructions propagate automatically. Training is the main bottleneck — new architects need to learn the instruction model and workflow. Scored 4 (not 5) because no formal onboarding process exists yet |
| 2: Copilot + Azure MCP | **4** | **Projected.** Same seat-based scaling. Azure services handle additional load. Per-user cost increase is modest (Copilot seat only — Azure services are shared). Same training bottleneck as Option 1 |
| 3: Custom Platform | **3** | **Projected.** Custom app must be load-tested, scaled, and supported. Training is more extensive — users must learn a new UX in addition to architecture workflows. But the web-based UX is accessible to non-VS-Code users, which is a scaling advantage for non-developer stakeholders |

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
