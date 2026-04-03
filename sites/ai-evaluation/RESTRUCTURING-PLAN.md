# AI Evaluation Site Restructuring Plan

**Date**: 2026-04-03
**Status**: Approved for Implementation
**Author**: Architecture Practice

---

## Problem Statement

The current AI evaluation site compares three toolchains (Copilot, Roo Code + Kong, Claude Code) as monolithic options. But stakeholders are conflating multiple independent architectural decisions into a single "which tool do we pick" question. Specifically:

1. **The MCP question is entangled with the toolchain question.** A camp wants Roo Code + Kong AI with custom-built MCP servers to inject enterprise context. The counter-argument is that this re-invents capabilities that native toolchains already provide. This needs to be decided independently — regardless of which toolchain wins, the practice needs a principled answer to "do we need custom MCP servers?"

2. **Billing model is conflated with toolchain.** Intent-based billing (Copilot) vs token-based billing (OpenRouter, Anthropic API) is not inherently tied to the tool — it is an economic architecture question.

3. **AI processing provider is conflated with delivery tool.** GitHub, Anthropic, Microsoft Azure AI Foundry, and Kong/OpenRouter are distinct provider options. The VS Code extension that presents the UX is a separate concern.

4. **Content injection location is unstated.** Whether enterprise context is injected on the developer workstation (local MCP, workspace files) or on a server (Azure MCP services, RAG pipeline) affects cost, security, and complexity — but is not discussed as its own decision.

---

## Solution: Decompose Into Four Decision Documents

Instead of one monolithic "pick a toolchain" comparison, decompose the evaluation into four independent decision documents. Each addresses a distinct architectural concern. The decisions then compose into side-by-side platform options that are scored.

### Decision Structure

```
Decision Documents (Why / What)
├── DD-01: Content Injection Strategy
│     Do we need custom MCP servers, or does native workspace + instructions suffice?
│
├── DD-02: Content Injection Location
│     Should context injection happen on the developer workstation or on a server?
│
├── DD-03: Billing Model Selection
│     Intent-based billing vs token-based billing — what economic model fits?
│
└── DD-04: AI Processing Provider
      Who do we buy AI processing from? GitHub, Anthropic, Microsoft, Kong/OpenRouter?
```

These four decisions map to existing Decision Points:
- DD-01 maps to DP-09 (Context Enrichment Strategy) + DP-19 (Hybrid MCP)
- DD-02 maps to DP-19 (MCP location) + DP-01 (Buy vs Build)
- DD-03 maps to DP-02 (Billing Model)
- DD-04 maps to DP-03 (Toolchain Selection) + DP-10 (Vendor Lock-In)

### How Decisions Compose Into Options

After the four decisions are analyzed independently, they compose into side-by-side platform options:

```
Platform Options (Composed from Decisions)
┌─────────────────────┬──────────────────┬──────────────────┬──────────────────┐
│                     │ Option A: Lean   │ Option B: Hybrid │ Option C: Full   │
├─────────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ DD-01 Content       │ Native workspace │ Native + targeted│ Custom MCP       │
│ Injection           │ + instructions   │ MCP servers      │ pipeline + RAG   │
├─────────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ DD-02 Location      │ Workstation only │ Workstation +    │ Server-hosted    │
│                     │                  │ selective server  │ AI orchestration │
├─────────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ DD-03 Billing       │ Intent-based     │ Intent-based +   │ Token-based      │
│                     │ (Copilot)        │ consumption       │ (pay-per-token)  │
├─────────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ DD-04 Provider      │ GitHub           │ GitHub + Azure   │ Azure Foundry or │
│                     │                  │                  │ Anthropic direct │
└─────────────────────┴──────────────────┴──────────────────┴──────────────────┘
```

---

## DD-01: Content Injection Strategy — Detailed Plan

### Objective

Produce a comprehensive decision document answering: **Does the architecture practice need custom MCP servers to inject enterprise context into AI workflows, or does native toolchain context management suffice?**

### Why This Matters

A camp of stakeholders advocates building custom MCP servers on Roo Code + Kong AI to inject proprietary enterprise context (Confluence knowledge bases, CMDB data, ServiceNow tickets, internal APIs). The counter-argument is that this re-invents capabilities native toolchains already provide — Copilot's workspace semantic indexing and instruction system achieve the same goal without custom infrastructure.

This decision must be made independently of toolchain selection. Regardless of which tool wins, the practice needs a principled framework for when custom content injection is justified vs when native capabilities are sufficient.

### Content Sections

1. **Problem Statement**: The gap between "what the AI knows" and "what the AI needs to know" for enterprise architecture work
2. **Content Injection Taxonomy**: Classification of all content types the AI consumes:
   - Architecture standards (arc42, C4, MADR) — static, evolves slowly
   - Domain model (services, APIs, data ownership) — semi-static
   - Ticket context (current work items) — dynamic
   - Production evidence (logs, metrics) — real-time
   - Enterprise knowledge (Confluence, CMDB, policies) — external, large corpus
   - Code and spec context (OpenAPI, source code) — workspace-local
3. **Options Analysis**:
   - **Option A: Native Only** — workspace files + instructions + built-in indexing
   - **Option B: Native + Targeted MCP** — native for workspace content, MCP for 2-3 specific external sources
   - **Option C: Full Custom MCP Pipeline** — MCP servers for all content injection, custom RAG for knowledge retrieval
4. **Evidence Assessment**: What content types are already well-served by native capabilities? Where are the gaps?
5. **"Reinventing the Wheel" Analysis**: Specific capabilities that custom MCP replicates vs genuinely new capabilities it would provide
6. **Cost-Benefit for Each Content Type**: Is the marginal value of custom injection worth the engineering cost?
7. **Decision Outcome**: Recommendation with justification
8. **Consequences**: Positive, negative, neutral

### Key Question to Answer

> For each content type the AI needs: is the gap caused by a toolchain limitation (justifying MCP) or by an investment gap (we have not written the instruction/metadata file yet)?

---

## DD-02: Content Injection Location — Detailed Plan

### Objective

Decide: **Should content injection happen on the developer's workstation (local) or on a server (remote)?**

### Why This Matters

This is an architectural question about where the "intelligence layer" lives. Local injection (workspace files, local MCP servers, IDE instructions) keeps everything on the developer machine — simple, fast, no infrastructure. Server-side injection (Azure MCP services, hosted RAG, centralized knowledge graph) enables shared enterprise context but adds infrastructure, latency, cost, and operational complexity.

### Content Sections

1. **Problem Statement**: Where should the enterprise context layer live?
2. **Workstation-Side Injection**: How it works today (workspace files, copilot-instructions.md, local MCP servers)
3. **Server-Side Injection**: How it would work (Azure AI Foundry, hosted MCP, vector stores, centralized RAG)
4. **Options Analysis**:
   - **Option A: Workstation Only** — all context is local. Single-player mode.
   - **Option B: Workstation + Server Hybrid** — local for workspace, server for enterprise-wide shared context
   - **Option C: Server-First** — server owns the context layer; workstation is thin client
5. **Evaluation Criteria**: Latency, security (where does enterprise data flow?), infrastructure cost, operational complexity, multi-team scalability, offline capability
6. **Security Implications**: Enterprise data on developer laptops vs centralized server with RBAC
7. **Decision Outcome**: Recommendation
8. **Consequences**

---

## DD-03: Billing Model Selection — Detailed Plan

### Objective

Decide: **Should the practice optimize for intent-based billing (flat per-action), token-based billing (metered), or subscription-with-ceiling?**

### Why This Matters

The 208x cost difference between Copilot ($0.48/run) and OpenRouter (~$100/run) is almost entirely attributable to billing architecture, not model quality. This decision has the single largest impact on monthly operating cost but is conflated with toolchain selection in the current analysis.

### Content Sections

1. **Problem Statement**: Billing model determines economics, usage behavior, and budget predictability
2. **Billing Model Taxonomy**:
   - **Intent-based**: Charges per user action (prompt). Platform absorbs autonomous work. Example: GitHub Copilot
   - **Token-based (pay-as-you-go)**: Charges per input/output token. Cost scales with context size and conversation length. Examples: OpenRouter, AWS Bedrock, Anthropic API
   - **Subscription with ceiling**: Flat monthly fee with usage cap. Example: Anthropic Max ($100-200/month)
   - **Infrastructure-amortized**: Build your own inference stack on Azure; pay compute costs. Example: Azure AI Foundry self-hosted
3. **Behavioral Economics**: How each model affects architect behavior — does cost anxiety suppress AI usage? Does "free autonomous work" encourage deeper investigations?
4. **Evidence from Phase 1**: Actual billing data supporting the 208x difference. Root cause: context accumulation under token billing vs server-side indexing under intent billing
5. **Sensitivity Analysis**: At what workload volume does each model become cheapest? Break-even analysis
6. **Risk Assessment**: Intent-based billing depends on GitHub not changing terms. Token-based is transparent but expensive today
7. **Decision Outcome**: Recommendation
8. **Consequences**

---

## DD-04: AI Processing Provider — Detailed Plan

### Objective

Decide: **Who should the practice buy AI processing from — and how does the provider choice affect cost, quality, governance, and portability?**

### Why This Matters

The "toolchain" question is really a provider question. The VS Code extension (Copilot, Roo Code, Claude Code) is the delivery vehicle, but the real decision is which company processes the architecture prompts and on what terms.

### Content Sections

1. **Problem Statement**: AI processing is a commodity; the differentiation is in pricing, integration, governance, and platform services
2. **Provider Landscape**:
   - **GitHub (Microsoft)**: Copilot Pro+ — intent-based billing, workspace indexing, GitHub integration, model marketplace
   - **Anthropic (direct)**: Claude Code / API — first-party model access, no translation layer, Max subscription option
   - **Kong / OpenRouter**: API gateway routing to multiple providers — full provider flexibility, token-based billing, enterprise gateway integration
   - **Microsoft Azure AI Foundry**: Self-hosted model inference — full control, Azure ecosystem integration, higher operational complexity
3. **Evaluation Dimensions**:
   - Model quality and availability
   - Pricing structure and predictability
   - Enterprise governance (SSO, audit, DLP)
   - Ecosystem integration (VS Code, GitHub, CI/CD)
   - Data residency and compliance
   - Platform longevity and vendor stability
   - Extensibility (MCP, tools, custom agents)
4. **Provider × Billing × Location Matrix**: How provider choice constrains billing model and injection location
5. **Decision Outcome**: Recommendation
6. **Consequences**

---

## Site Structure Changes

### New Pages

```
sites/ai-evaluation/docs/
├── decisions/                          (NEW directory)
│   ├── index.md                        (Decision framework overview)
│   ├── dd-01-content-injection.md      (Content injection strategy)
│   ├── dd-02-injection-location.md     (Workstation vs server)
│   ├── dd-03-billing-model.md          (Intent vs token billing)
│   └── dd-04-ai-provider.md            (GitHub vs Anthropic vs Azure vs Kong)
├── platform-options.md                 (NEW - composed side-by-side comparison)
└── ... (existing pages preserved)
```

### Navigation Update (mkdocs.yml)

```yaml
nav:
  - Home: index.md
  - Decisions:
    - Decision Framework: decisions/index.md
    - DD-01 Content Injection: decisions/dd-01-content-injection.md
    - DD-02 Injection Location: decisions/dd-02-injection-location.md
    - DD-03 Billing Model: decisions/dd-03-billing-model.md
    - DD-04 AI Provider: decisions/dd-04-ai-provider.md
  - Platform Options: platform-options.md
  - Evaluation Framework: evaluation-framework.md
  - Tools:
    - GitHub Copilot: tools/github-copilot.md
    - Roo Code + Kong AI: tools/roo-code-kong.md
    - Claude Code: tools/claude-code.md
  - Comparisons:
    - Copilot vs Roo Code: comparisons/copilot-vs-roocode.md
    - Run Analysis: comparisons/run-analysis.md
  - Research:
    - Copilot Billing Mechanics: research/copilot-billing.md
    - Kong AI Translation Failures: research/kong-failures.md
    - Context Management: research/context-management.md
  - Data Isolation: data-isolation.md
  - Decision Log: decision-log.md
```

### Index Page Update

Update the home page to reflect the new decomposed decision structure. The "Three Toolchains Compared" section becomes "Platform Decision Framework" pointing to the four decision documents and the composed platform options.

---

## Implementation Sequence

1. Create `decisions/` directory with all 5 files (index + 4 DDs)
2. Create `platform-options.md` (composed comparison)
3. Update `mkdocs.yml` navigation
4. Update `index.md` home page
5. Build, commit, push, publish

---

## What Does NOT Change

- Existing tool profiles (tools/) — preserved as reference material
- Existing comparisons (comparisons/) — preserved as Phase 1 evidence
- Existing research (research/) — preserved as supporting analysis
- Evaluation framework — preserved as methodology documentation
- Data isolation statement — preserved
- Decision log (ADR-001) — preserved but the four DDs supersede it as the decision structure
