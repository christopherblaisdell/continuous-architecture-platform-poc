<!-- CONFLUENCE-PUBLISH -->

# Practice Strategy — AI-Augmented Solution Architecture

## PSD-01: Adopting Agentic AI into the Solution Architecture Practice

**Status:** Proposed
**Date:** 2026-04-06

---

## Context and Problem Statement

The solution architecture practice is evaluating whether and how to adopt agentic AI as a core capability. This is not a toolchain selection decision — it is a practice transformation decision. The question is not "which AI tool?" but "how does our team work differently with AI, and what operating model supports that change?"

Toolchain selection (DD-01 through DD-04) determines the technology substrate. This practice strategy decision determines how architects interact with that substrate — the workflows, governance, quality gates, roles, and adoption path that make AI a productive member of the architecture practice rather than a novelty.

---

## Decision Scope

### What This Decision Covers (Layer 1 — Practice Strategy)

- How architects interact with AI agents (prompt patterns, session structure, review rituals)
- Where AI output enters the architecture governance process
- How we measure quality and maintain accountability for AI-generated artifacts
- Training and onboarding for the practice
- Incremental adoption path from pilot to team to organization
- Success metrics and feedback loops

### What This Decision Does NOT Cover (Layer 2 — Toolchain Decisions)

The following are addressed by the decomposed toolchain decisions and are inputs to this strategy, not outputs of it:

| Toolchain Decision | Question | Reference |
|-------------------|----------|-----------|
| [DD-01: Content Injection](decisions/dd-01-content-injection.md) | Custom MCP servers vs native context management | Layer 2 |
| [DD-02: Injection Location](decisions/dd-02-injection-location.md) | Workstation vs server-side context injection | Layer 2 |
| [DD-03: Billing Model](decisions/dd-03-billing-model.md) | Intent-based vs token-based billing | Layer 2 |
| [DD-04: AI Provider](decisions/dd-04-ai-provider.md) | GitHub, Anthropic, Azure AI Foundry, or Kong | Layer 2 |

---

## Two-Layer Decision Hierarchy

```
Layer 1: Practice Strategy (this document)
  "How does our architecture practice work with AI?"
  ├── Consumes Layer 2 toolchain decisions as inputs
  ├── Defines human-AI interaction patterns
  ├── Establishes governance and quality gates
  ├── Sets adoption roadmap (pilot → scale)
  └── Defines success metrics

Layer 2: Toolchain Decisions (DD-01 through DD-04)
  "What specific technology implements the operating model?"
  ├── DD-01: Content Injection Strategy
  ├── DD-02: Injection Location
  ├── DD-03: Billing Model
  └── DD-04: AI Provider
  Compose into: Option A (Lean) | Option B (Hybrid) | Option C (Full Build)
```

### Why Two Layers?

| Aspect | Layer 2 (Toolchain DDs) | Layer 1 (Practice Strategy) |
|--------|------------------------|---------------------------|
| Question | What do we buy or build? | How do we work? |
| Audience | Platform engineers, procurement | Practice leads, architects, leadership |
| Artifact | MADR ADRs per decision | Operating model document |
| Changes when | Vendor pricing shifts, new tools emerge | Team structure changes, new use cases surface |
| Reversibility | Swap tools in weeks | Methodology changes take months |
| Dependencies | Technology constraints | Organizational readiness, culture, skills |

---

## Proposed Operating Model

### Architect-Agent Interaction Pattern

The AI agent operates as a **junior architect with perfect recall but no judgment**. The human architect provides direction, evaluates output, and makes decisions. The agent executes research, drafting, and validation tasks autonomously.

| Phase | Human Architect | AI Agent |
|-------|----------------|----------|
| Intake | Reviews ticket, decides architectural relevance | Scaffolds workspace, gathers context from specs and logs |
| Research | Defines investigation scope, forms hypotheses | Searches specs, source code, logs, and prior solutions |
| Design | Evaluates options, selects approach, makes trade-offs | Drafts impact assessments, ADRs, user stories, diagrams |
| Review | Reviews all generated artifacts for accuracy and completeness | Validates cross-references, formatting, standards compliance |
| Publish | Approves final artifacts | Generates portal pages, updates metadata |

### Session Structure

A typical architecture session follows this pattern:

1. **Prompt** — The architect provides a ticket number or investigation question (1-4 prompts per session)
2. **Autonomous execution** — The agent reads specs, queries tools, drafts documents (50-200 tool calls, zero cost under intent-based billing)
3. **Review** — The architect reviews generated artifacts, provides corrections
4. **Iteration** — The agent incorporates feedback (1-2 additional prompts)
5. **Commit** — The agent commits, pushes, and regenerates portal pages

Average session duration: 15-45 minutes. Average cost: $0.48 (4 prompts on Claude Opus 4.6 via Copilot).

### Governance Model

| Gate | When | Who | What |
|------|------|-----|------|
| Architectural relevance | Ticket intake | Human architect | Decides if ticket warrants architecture work |
| Design review | After draft generation | Human architect | Reviews all ADRs, impacts, and diagrams for correctness |
| Standards compliance | Before publish | AI agent (automated) | Validates MADR format, C4 notation, cross-references |
| Peer review | Before merge (future) | Second architect | Reviews PR for architectural soundness |
| Quality audit | Monthly | Practice lead | Samples completed solutions for quality trends |

### Quality Accountability

AI-generated artifacts are **the architect's responsibility**. The agent is a tool, not a decision-maker. Specifically:

- The architect's name appears on all published architecture documents
- ADR decisions reflect the architect's judgment, not the agent's suggestion
- Factual claims must be verified against workspace evidence (specs, logs, source code)
- The agent must never fabricate data — assumptions are documented explicitly

---

## Adoption Roadmap

### Phase 1: Pilot (Current — 1 architect)

- Single architect using Copilot Pro+ for all 5 scenario types
- Workspace: NovaTrek Adventures (synthetic, zero corporate data)
- Goal: Validate quality, cost, and workflow feasibility
- Evidence: 149/155 quality score (96.1%), $0.48/run, 37 files per scenario

### Phase 2: Practice Adoption (Next — 3-5 architects)

- Extend to team of solution architects
- Real project workspace (with appropriate data isolation)
- Shared instruction files via Git (copilot-instructions.md, .instructions.md)
- Establish review rituals and quality baselines
- Goal: Validate team-scale adoption, identify instruction gaps

### Phase 3: Organization Scale (Future — 10+ architects)

- Standardized instruction library across architecture teams
- Shared MCP servers for enterprise data (if DD-01 selects Option B)
- Cross-team ADR index and capability sharing
- Governance dashboard and usage analytics
- Goal: Architecture practice operates with AI as standard capability

### Adoption Decision Gates

| Gate | Criteria | Go/No-Go |
|------|----------|----------|
| Phase 1 → 2 | Quality score >90%, cost <$2/run, no data leakage incidents | Go if all met |
| Phase 2 → 3 | Team adoption >80%, instruction reuse >50%, peer review pass rate >95% | Go if all met |

---

## Success Metrics

| Metric | Phase 1 Target | Measurement |
|--------|---------------|-------------|
| Architecture output quality | >90% (scoring rubric) | Architect-scored per scenario |
| Cost per architecture run | <$2.00 | Billing data |
| Time to first draft | <45 minutes | Session duration |
| Standards compliance rate | >95% | Automated validation |
| Manual corrections required | <10 per solution | Edit count after generation |
| Architect satisfaction | Qualitative | Post-session feedback |

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Over-reliance on AI output without review | Medium | High | Governance gates require human sign-off on all decisions |
| AI fabricates data (hallucination) | Medium | High | Instructions mandate evidence-based claims; audit samples monthly |
| Vendor lock-in to GitHub Copilot | Low | Medium | Instructions and workspace are portable; agent is replaceable |
| Cost escalation if billing model changes | Low | Medium | Monitor GitHub pricing; maintain Option B as fallback |
| Instruction drift across teams | Medium | Medium | Git-managed instructions with PR review process |

---

## Relationship to Toolchain Decisions

This practice strategy is designed to work with **any** of the three platform options from the Layer 2 evaluation:

| Platform Option | Practice Strategy Impact |
|----------------|------------------------|
| **Option A: Lean** (Copilot standalone) | Minimal infrastructure overhead; practice adoption is the primary change |
| **Option B: Hybrid** (Copilot + Azure MCP) | Adds enterprise data access; requires MCP server operational procedures |
| **Option C: Full Build** (Custom Azure platform) | Requires custom UX training; longer onboarding; higher operational burden |

The practice strategy recommends starting with Option A (proven, immediate) and evaluating the need for Option B based on Phase 2 findings. Option C is not recommended given the 2.78/5 weighted score and 6-18 month time-to-value.

---

## Related Documents

- [Decision Framework](decisions/decision-framework.md) — Layer 2 toolchain decision structure
- [Platform Options](platform-options.md) — Composed platform options from Layer 2
- [Evaluation Framework](evaluation-framework.md) — Phase 1 methodology and scoring
