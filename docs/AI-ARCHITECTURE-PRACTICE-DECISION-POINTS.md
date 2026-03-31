# AI in Architecture Practice — Decision Points

**Date**: 2026-03-31
**Status**: Living Document
**Author**: Solution Architecture Team

---

## Purpose

This document catalogs every significant decision point an architecture practice faces when incorporating AI into its workflows. Each decision is classified by status (recommendation draft, under evaluation, or open) and cross-referenced to the evidence or ADR that informed it.

This is not an ADR — it is a **decision map** that shows the full landscape of choices, which ones currently have recommendation drafts, which are under evaluation, and which remain open.

This document is the **operating-model layer** of the overall AI decision structure. It is not the weighted platform-selection scorecard. Platform comparison should be performed separately using weighted factors such as cost, quality, workflow fit, governance, extensibility, portability, and operational complexity.

---

## Decision Point Index

| # | Decision Point | Category | Status |
|---|---------------|----------|--------|
| DP-01 | [Buy vs Build](#dp-01-buy-vs-build) | Strategy | Recommendation Draft (Hybrid) |
| DP-02 | [Billing Model: Intent-Based vs Raw Token](#dp-02-billing-model-intent-based-vs-raw-token) | Cost | Recommendation Draft |
| DP-03 | [AI Toolchain Selection](#dp-03-ai-toolchain-selection) | Tooling | Recommendation Draft |
| DP-04 | [Single Tool vs Multi-Tool Strategy](#dp-04-single-tool-vs-multi-tool-strategy) | Tooling | Under Evaluation |
| DP-05 | [Standards Enforcement: Advisory vs Deterministic](#dp-05-standards-enforcement-advisory-vs-deterministic) | Governance | Under Evaluation |
| DP-06 | [AI Autonomy Level: Human-in-the-Loop vs Autonomous](#dp-06-ai-autonomy-level-human-in-the-loop-vs-autonomous) | Governance | Open |
| DP-07 | [Knowledge Curation: Monolith vs Modular Instructions](#dp-07-knowledge-curation-monolith-vs-modular-instructions) | Knowledge | Under Evaluation |
| DP-08 | [AI Skill Library: Build vs Adapt Community](#dp-08-ai-skill-library-build-vs-adapt-community) | Knowledge | Under Evaluation |
| DP-09 | [Context Enrichment Strategy](#dp-09-context-enrichment-strategy) | Architecture | Recommendation Draft |
| DP-10 | [Vendor Lock-In vs Portability](#dp-10-vendor-lock-in-vs-portability) | Strategy | Under Evaluation |
| DP-11 | [Organizational Adoption Model](#dp-11-organizational-adoption-model) | Organizational | Open |
| DP-12 | [AI Output Review and Trust Model](#dp-12-ai-output-review-and-trust-model) | Governance | Under Evaluation |
| DP-13 | [Data Isolation and Security Posture](#dp-13-data-isolation-and-security-posture) | Security | Recommendation Draft |
| DP-14 | [Publishing Pipeline: Manual vs Automated](#dp-14-publishing-pipeline-manual-vs-automated) | Workflow | Recommendation Draft |
| DP-15 | [Multi-Model Strategy: Single vs Best-of-Breed](#dp-15-multi-model-strategy-single-vs-best-of-breed) | Tooling | Open |
| DP-16 | [Ticketing Integration Pattern](#dp-16-ticketing-integration-pattern) | Integration | Recommendation Draft |
| DP-17 | [Architecture-as-Code Framework](#dp-17-architecture-as-code-framework) | Standards | Under Evaluation |
| DP-18 | [Measuring AI Value: Cost vs Quality vs Speed](#dp-18-measuring-ai-value-cost-vs-quality-vs-speed) | Measurement | Under Evaluation |
| DP-19 | [Hybrid Copilot + Azure AI Foundry via MCP](#dp-19-hybrid-copilot--azure-ai-foundry-via-mcp) | Integration | Open |

---

## DP-01: Buy vs Build

**Category**: Strategy
**Status**: Recommendation Draft (Hybrid, Unratified)

### The Question

Should the architecture practice buy a commercial AI platform purpose-built for architecture work, build a custom AI toolchain from scratch, or assemble a hybrid from commercial and open-source components?

### Options

| Option | Description | Trade-off |
|--------|-------------|-----------|
| **A. Pure Buy** | Purchase an enterprise AI architecture platform (e.g., Ardoq AI, LeanIX AI, Bizzdesign) | Fast to deploy; expensive; opinionated workflows; limited customization; vendor controls the roadmap |
| **B. Pure Build** | Build a custom AI agent from scratch using raw LLM APIs, custom RAG, bespoke UX | Maximum flexibility; high build cost; ongoing maintenance burden; slow to first value |
| **C. Hybrid — Commercial AI + Custom Instructions** | Use a commercial AI coding assistant (Copilot, Claude Code) and customize it with domain-specific instructions, skills, and metadata | Fast to first value; low cost; high customization; dependent on vendor for base capabilities |

### Working Recommendation

**Option C — Hybrid.** The practice uses GitHub Copilot Pro+ as the commercial foundation and layers domain-specific customization on top: `copilot-instructions.md` (700+ lines of domain knowledge), custom skills, solution design templates, and metadata YAML files that the AI reads at runtime. No custom LLM infrastructure was built.

### Evidence

- ADR-001 selected Copilot Pro+ at $39/seat vs building a custom RAG pipeline
- Vector DB feasibility analysis concluded Copilot's built-in semantic indexing eliminates the need for custom retrieval infrastructure
- The 700+ line `copilot-instructions.md` file demonstrates that deep customization is achievable without building a platform

### What This Means

The practice does not own the AI model, the embedding infrastructure, or the chat UX. It owns **the knowledge layer** — the instructions, the metadata, the specs, and the solution templates that make the AI behave like a senior architect. This is a deliberate trade-off: low infrastructure cost in exchange for dependency on GitHub's platform trajectory.

---

## DP-02: Billing Model — Intent-Based vs Raw Token

**Category**: Cost
**Status**: Recommendation Draft (Unratified)

### The Question

How should the practice pay for AI usage — per token consumed (metered), or per user action (intent-based)?

### Options

| Option | Description | Trade-off |
|--------|-------------|-----------|
| **A. Raw Token Billing** | Pay per input/output token. Cost scales linearly with context size and conversation length. Providers: OpenRouter, AWS Bedrock direct, Anthropic API | Full cost visibility; unpredictable monthly spend; penalizes large context windows; cost anxiety discourages exploration |
| **B. Intent-Based Billing** | Pay per user prompt (intent). Autonomous agent work — tool calls, file reads, sub-agents, context management — is absorbed by the platform. Provider: GitHub Copilot | Predictable cost; encourages AI use; no visibility into token consumption; vendor subsidizes heavy usage today but may change terms |
| **C. Subscription with Ceiling** | Flat monthly fee with a usage cap. Provider: Anthropic Max ($100-200/month) | Budget predictable; cap may throttle heavy days; per-seat cost higher than intent-based |

### Working Recommendation

**Option B — Intent-Based Billing** via GitHub Copilot Pro+.

### Evidence

- Deep research confirmed Copilot bills per user prompt, not per model invocation. A 4-prompt session on Claude Opus 4.6 costs $0.48 regardless of how many autonomous tool calls execute
- Actual billing data: Copilot Pro+ cost $0.48/run vs ~$100/run on OpenRouter for the same model and workspace — a 208x difference
- The 208x gap is structural: intent-based billing amortizes workspace indexing across the user base; token billing charges for re-indexing on every conversation turn

### What This Means

Intent-based billing fundamentally changes AI usage behavior. Architects do not hesitate to ask follow-up questions, run exploratory analyses, or let the agent investigate deeply — because the marginal cost of autonomous agent work is zero. Under raw token billing, every additional context file and every follow-up question has a visible cost, which creates friction that reduces AI adoption.

### Risk

GitHub controls the pricing model. The current 3x multiplier for Claude Opus 4.6 and the "autonomous work is free" model may change. The practice should monitor GitHub's billing announcements and maintain awareness of raw token costs as a fallback benchmark.

---

## DP-03: AI Toolchain Selection

**Category**: Tooling
**Status**: Recommendation Draft (Unratified)

### The Question

Which AI coding assistant should the architecture practice standardize on?

### Options

| Option | Monthly Cost | Billing | Quality |
|--------|------------|---------|---------|
| A. Roo Code + OpenRouter | ~$507 (variable) | Per-token | TBD |
| B. GitHub Copilot Business | $19 (flat) | Per-seat | Not tested |
| C. GitHub Copilot Pro+ | $39 (flat) | Intent-based | 96.1% (149/155) |
| D. Claude Code (API) | $100-200 or variable | Per-token or subscription | Spike planned |

### Working Recommendation

**Option C — GitHub Copilot Pro+.** See ADR-001 for full analysis.

### Evidence

- 5 evaluation scenarios, 155-point quality rubric, actual billing data from both toolchains
- 96.1% quality score at $0.48/run
- Deep GitHub/VS Code integration supports existing workflow

---

## DP-04: Single Tool vs Multi-Tool Strategy

**Category**: Tooling
**Status**: Under Evaluation

### The Question

Should the practice standardize on one AI tool for all work, or use different tools for different types of tasks?

### Options

| Option | Description | Trade-off |
|--------|-------------|-----------|
| **A. Single Tool** | One AI assistant for all architecture work | Simpler governance; single set of instructions; may not be best-in-class for every task type |
| **B. Complementary Tools** | Primary tool for daily work + specialized tool for specific tasks (e.g., deep research, complex reasoning) | Best-of-breed per task; duplicate instruction maintenance; context does not transfer between tools |
| **C. Full Multi-Tool** | Architects choose whichever tool fits the moment | Maximum flexibility; governance nightmare; inconsistent outputs; no shared instruction investment |

### Current Position

**Leaning toward Option B.** Copilot Pro+ is the primary tool. Claude Code is recognized as a potential complement for deep research and complex multi-step reasoning (ADR-001 notes a planned spike). No formal decision yet on whether to formally adopt a second tool.

### Open Questions

- Does the Claude Code spike confirm complementary value?
- Can instructions be shared across tools (Copilot `instructions.md` vs Claude `CLAUDE.md`)?
- Is the operational overhead of maintaining two instruction sets justified?

---

## DP-05: Standards Enforcement — Advisory vs Deterministic

**Category**: Governance
**Status**: Under Evaluation

### The Question

How should the practice enforce architecture standards in AI-generated outputs — through advisory instructions (the AI is told what to do) or deterministic hooks (automated checks that block non-compliant outputs)?

### Options

| Option | Description | Trade-off |
|--------|-------------|-----------|
| **A. Advisory Only** | Standards encoded in `copilot-instructions.md` as prose. AI follows them most of the time. Non-compliance caught in human review | Low maintenance; works today; AI compliance is probabilistic (~96%); drift accumulates |
| **B. Deterministic Hooks** | Copilot hooks (`PreToolUse`/`PostToolUse`) run shell scripts that validate output before the AI commits. Non-compliant writes are blocked | Guaranteed compliance; requires scripting and maintenance; brittle if standards evolve; hooks are Copilot-specific |
| **C. CI/CD Validation** | Standards enforced in the PR pipeline (linting, schema validation, custom checks). AI outputs are validated at merge time, not creation time | Tool-agnostic; later feedback loop; non-compliance discovered after the work is done; aligns with existing PR workflow |
| **D. Layered** | Advisory instructions for guidance + hooks for critical rules + CI for comprehensive validation | Best coverage; highest maintenance; most complex; each layer catches what the others miss |

### Current Position

Current evidence supports **Option D (Layered)** as the target model, with **Option A + C already in place**. Standards are encoded in `copilot-instructions.md` prose, and deterministic CI/docs pipeline validation already gates merges. The missing piece is selective local/runtime enforcement (hooks or equivalent) for high-risk rules.

### Decision Drivers

- What is the cost of a standards violation that slips through? (Low for documentation, high for safety rules like Pattern 3 defaults)
- How often do standards change? (Frequently changing standards make hooks expensive to maintain)
- Does the practice have engineering capacity to build and maintain hooks?

---

## DP-06: AI Autonomy Level — Human-in-the-Loop vs Autonomous

**Category**: Governance
**Status**: Open

### The Question

How much latitude should the AI agent have to create, modify, and publish architecture artifacts without human review?

### Options

| Option | Description | Trade-off |
|--------|-------------|-----------|
| **A. Full Human-in-the-Loop** | AI drafts everything; architect reviews and approves every artifact before it is committed or published | Maximum quality control; slowest throughput; architect becomes a reviewer rather than a producer |
| **B. Trust but Verify** | AI commits to a branch and creates a PR. Architect reviews the PR before merge. Publishing is automated on merge | Good quality gate; aligns with existing Git workflow; overhead per solution design; PR review is the control point |
| **C. Autonomous with Guardrails** | AI commits directly to main (admin bypass) with automated validation. Human reviews periodically or on flagged items | Fastest throughput; relies on automated validation; risks accumulating drift if reviews are skipped |
| **D. Tiered Autonomy** | Different autonomy levels for different artifact types: autonomous for low-risk (portal regeneration, formatting), human review for high-risk (ADRs, API contract changes, safety decisions) | Matches risk to review effort; requires clear artifact classification; most nuanced to implement |

### Current Position

Currently operating between **Option B and C** depending on the task. Solution designs go through branch + PR review. Portal regeneration and metadata updates are committed directly to main with admin bypass.

### Open Questions

- Should ADRs require explicit human approval before the AI creates them?
- Is the current admin bypass (AI pushes to main) sustainable as the practice scales?
- What artifacts are "low risk" enough for autonomous publishing?

---

## DP-07: Knowledge Curation — Monolith vs Modular Instructions

**Category**: Knowledge
**Status**: Under Evaluation

### The Question

How should the practice organize the domain knowledge that informs the AI agent — as a single comprehensive instruction file, or as modular topic-specific files?

### Options

| Option | Description | Trade-off |
|--------|-------------|-----------|
| **A. Monolith** | One large `copilot-instructions.md` with everything | Always loaded; AI has full context every session; file grows unwieldy; changes risk regressions; context window pressure |
| **B. Modular** | Base instructions + topic-specific `.instructions.md` files activated by `applyTo` glob or `description` match | Focused context per task; smaller base file; risk of missing context if the wrong module loads; more files to maintain |
| **C. Skills-Based** | Core standards in base instructions + deep knowledge packaged as skills (`SKILL.md`) invoked on demand | On-demand loading reduces context waste; skills are self-contained; requires clear naming for discoverability |
| **D. Layered Hybrid** | Monolith base (always-on essentials) + modular instructions (auto-loaded by context) + skills (on-demand deep dives) | Best of all approaches; most complex file structure; requires clear documentation of what goes where |

### Current Position

Currently using **Option A** trending toward **Option D**. The `copilot-instructions.md` is 700+ lines and growing. The ECC incorporation plan adds `.instructions.md` and `.prompt.md` files for specific skills. No formal strategy for what belongs in the monolith vs modules.

### Decision Drivers

- Context window limits: how large can the monolith grow before it degrades AI performance?
- Discoverability: can the AI reliably find and load the right modular instruction?
- Maintenance: who curates the instructions, and how are conflicts between modules detected?

---

## DP-08: AI Skill Library — Build vs Adapt Community

**Category**: Knowledge
**Status**: Under Evaluation

### The Question

Should the practice build its AI skill library from scratch (based on its own experience) or adapt existing community skill libraries?

### Options

| Option | Description | Trade-off |
|--------|-------------|-----------|
| **A. Build from Scratch** | Write all skills based on the practice's own workflows and standards | Perfectly tailored; slow to build; limited by internal experience; no community feedback loop |
| **B. Adapt Community Libraries** | Take open-source skill collections (ECC, Jeffallan, etc.) and translate them to the practice's format and standards | Faster coverage; external expertise; adaptation effort; may import patterns that don't fit |
| **C. Curated Hybrid** | Build practice-specific skills for core workflows; adapt community skills for generic capabilities (security review, coding standards, etc.) | Best coverage-to-effort ratio; requires clear criteria for what to build vs adapt |

### Current Position

**Option C in progress.** The ECC Incorporation Plan selects 13 Tier 1 skills from Everything Claude Code for adaptation. The Jeffallan claude-skills collection (66 skills) is already available. Practice-specific skills (solution design lifecycle, capability rollup) are custom-built.

### Evidence

- ECC Incorporation Plan defines Tier 1 scope and translation methodology
- 66 Jeffallan skills available in `claude-skills/skills/`
- Custom skills built for NovaTrek domain workflows

---

## DP-09: Context Enrichment Strategy

**Category**: Architecture
**Status**: Recommendation Draft (Unratified)

### The Question

How should the practice provide the AI with the architectural context it needs — passive (AI reads files on demand), active (context pushed into every session), or indexed (semantic retrieval from a knowledge base)?

### Options

| Option | Description | Trade-off |
|--------|-------------|-----------|
| **A. Passive (File-Based)** | AI reads specs, source code, and metadata files when it needs them. No pre-processing | Simple; no infrastructure; AI must know what to look for; slow for large workspaces |
| **B. Active (Broadcast)** | Full workspace context injected into every conversation turn | AI always has full context; enormous token cost; 16.3% of Roo Code task logs were repetitive metadata broadcast |
| **C. Indexed (Semantic Retrieval)** | Workspace pre-indexed in a vector database. AI queries the index for relevant context per question | Fast retrieval; relevant context only; requires indexing infrastructure; may miss context not in the index |
| **D. Hybrid (Instructions + Indexing)** | Always-on instructions provide core knowledge + semantic indexing provides on-demand file retrieval | Best of active and indexed; Copilot implements this natively |

### Working Recommendation

**Option D — Hybrid** via GitHub Copilot's native architecture. Copilot always loads `copilot-instructions.md` (active core knowledge) and uses workspace semantic indexing for on-demand retrieval (indexed). No custom infrastructure required.

### Evidence

- Context Window Utilization Analysis showed Roo Code's broadcast approach wasted 16.3% of token budget on repetitive environment details
- Vector DB feasibility analysis confirmed Copilot already implements semantic retrieval natively
- The 208x cost difference is partially attributable to this architectural choice

---

## DP-10: Vendor Lock-In vs Portability

**Category**: Strategy
**Status**: Under Evaluation

### The Question

How much should the practice invest in tool-specific customization (deep Copilot integration) vs portable formats that work across AI tools?

### Options

| Option | Description | Trade-off |
|--------|-------------|-----------|
| **A. Deep Lock-In** | Maximize Copilot-specific features: hooks, agent tool restrictions, GitHub integration, MCP servers | Best capabilities today; highest switching cost; full governance features; tied to GitHub's roadmap |
| **B. Portable First** | Use tool-agnostic formats (OpenSpec, generic Markdown instructions, standard MCP). Accept reduced capabilities for portability | Lower switching cost; less capable AI interaction; misses Copilot-specific enforcement features |
| **C. Portable Core + Vendor Extensions** | Keep the knowledge layer portable (Markdown specs, YAML metadata, standard MCP) and use vendor-specific features only for enforcement (hooks, agent restrictions) | Knowledge survives tool migration; enforcement layer must be rebuilt; the most portable layer (knowledge) is also the most valuable |

### Current Position

Now explicitly operating at **Option C**. The knowledge assets (OpenAPI specs, YAML metadata, solution designs, ADRs) are tool-agnostic Markdown/YAML, while execution/enforcement features remain tool-specific. The strategic realignment research reinforces this split as the practical balance between portability and capability.

### Decision Drivers

- How likely is a tool migration in the next 2 years?
- How much of the investment is in portable knowledge vs Copilot-specific configuration?
- Does OpenSpec provide enough value to justify maintaining a parallel configuration format?

---

## DP-11: Organizational Adoption Model

**Category**: Organizational
**Status**: Open

### The Question

How should AI-assisted architecture be rolled out across the organization — centralized in a center of excellence, distributed to all architects, or piloted in a single team?

### Options

| Option | Description | Trade-off |
|--------|-------------|-----------|
| **A. Center of Excellence** | A dedicated team builds and maintains the AI workspace; other architects consume the outputs | High quality; bottleneck risk; other architects do not learn the AI workflow |
| **B. Distributed Adoption** | All architects get Copilot seats and the shared workspace. Each works in the AI workflow independently | Scales naturally; inconsistent quality; instruction drift across teams; requires training |
| **C. Champion Model** | One AI champion per team seeds adoption, curates team-specific instructions, and coaches peers | Balanced scaling; champions need dedicated time; quality depends on champion skill |
| **D. Phased Rollout** | Start with one team (pilot), refine the workflow, then expand team by team with documentation and training | Low risk; slow; pilot team carries extra load; learnings are captured before scaling |

### Current Position

Currently at **pre-decision** — the POC demonstrates feasibility with a single practitioner. Organizational rollout strategy has not been formally addressed.

### Decision Drivers

- How many architects will use AI-assisted workflows?
- What is the training investment per architect?
- Who maintains the shared instruction corpus as the practice scales?
- How are conflicting architectural preferences resolved when multiple architects contribute to instructions?

---

## DP-12: AI Output Review and Trust Model

**Category**: Governance
**Status**: Under Evaluation

### The Question

How should the practice validate AI-generated architecture artifacts — and how does trust evolve over time?

### Options

| Option | Description | Trade-off |
|--------|-------------|-----------|
| **A. Full Review** | Every AI output is reviewed line-by-line by a human architect before acceptance | Highest quality; slowest; does not scale; negates throughput benefits of AI |
| **B. Scored Trust** | AI outputs are scored on a rubric. As scores consistently exceed a threshold, review depth decreases for that artifact type | Progressive trust building; requires scoring infrastructure; transparent quality evolution |
| **C. Spot Check** | A random sample of AI outputs is reviewed in depth. Systemic issues trigger full review periods | Efficient; risks missing one-off errors; statistical confidence depends on sample size |
| **D. Exception-Based** | AI outputs are accepted by default. Automated checks flag anomalies (e.g., missing sections, unknown service references). Only flagged items are reviewed | Fastest throughput; requires good anomaly detection; silent failures in unflagged artifacts |

### Current Position

Currently using **Option B implicitly** — the Phase 1 evaluation scored outputs on a 155-point rubric (96.1% result). The practice is between "full review" (solution designs are PR-reviewed) and "scored trust" (the rubric data exists but is not formalized into a progressive trust framework).

### Open Questions

- What score threshold triggers reduced review? (95%? 98%?)
- Should different artifact types have different trust levels? (ADRs may need more scrutiny than portal page regeneration)
- How is regression detected if review depth decreases?

---

## DP-13: Data Isolation and Security Posture

**Category**: Security
**Status**: Recommendation Draft (Unratified)

### The Question

How should the practice ensure AI tools do not ingest, leak, or hallucinate real corporate data?

### Working Recommendation

**Synthetic workspace with strict isolation rules.** The entire NovaTrek Adventures domain is fictional. All mock tools are local Python scripts reading JSON files — no network calls, no credentials, no corporate system access. An audit script (`audit-data-isolation.sh`) validates data isolation before every commit.

### Evidence

- `copilot-instructions.md` includes explicit "Data Isolation — READ FIRST" section
- All 19 microservice specs and Java source code are synthetic
- Mock tools use Python stdlib only — no `requests`, no API clients

### Open Questions for Scaling

- When the practice moves from synthetic to real corporate data, what guardrails are needed?
- Does AI-generated content need to be reviewed for inadvertent data leakage?
- How should PII in real tickets be handled when the AI processes them?

---

## DP-14: Publishing Pipeline — Manual vs Automated

**Category**: Workflow
**Status**: Recommendation Draft (Unratified)

### The Question

How should architecture documentation get from the architect's workspace to a browsable, shareable portal?

### Working Recommendation

**Automated on `git push`.** MkDocs Material builds the portal. GitHub Actions deploys to Azure Static Web Apps. Confluence receives an automated read-only mirror. No manual wiki editing step exists.

### Evidence

- Portal deployed at `architecture.novatrek.cc`
- Confluence drift detection runs daily to prevent manual edits from diverging from source
- 19 microservice deep-dive pages auto-generated with PlantUML sequence diagrams

---

## DP-15: Multi-Model Strategy — Single vs Best-of-Breed

**Category**: Tooling
**Status**: Open

### The Question

Should the practice use one LLM for all tasks, or select different models for different types of work?

### Options

| Option | Description | Trade-off |
|--------|-------------|-----------|
| **A. Single Model** | Use Claude Opus 4.6 for everything | Consistent behavior; single set of instructions; may overpay for simple tasks; may underperform on specialized tasks |
| **B. Tiered by Complexity** | Opus for complex reasoning (solution design, investigation); Sonnet for routine work (portal generation, formatting); Haiku for classification | Cost-optimized; requires task classification; different models may interpret instructions differently |
| **C. Best-of-Breed by Domain** | Different providers for different domains: Anthropic for architecture reasoning, OpenAI for code generation, Google for search/retrieval | Theoretical quality gains; massive operational complexity; no shared context; impractical for most teams |

### Current Position

Currently using **Option A** — Claude Opus 4.6 for all work via Copilot Pro+. The Copilot platform offers model selection (GPT-4.1 at 0x multiplier, Sonnet at lower multiplier) but the practice has not evaluated whether simpler models suffice for routine tasks.

### Decision Drivers

- Is the cost difference between Opus and Sonnet material given intent-based billing? (0x for GPT-4.1 vs 3x for Opus)
- Does quality degrade noticeably on simpler models for architecture work?
- Is the complexity of model-switching per task justified by the savings?

---

## DP-16: Ticketing Integration Pattern

**Category**: Integration
**Status**: Recommendation Draft (Unratified)

### The Question

How should AI access architecture tickets — via file, CLI, or live integration?

### Working Recommendation

**Progressive: YAML to CLI to MCP.** Started with `tickets.yaml` (Phase 1), added `ticket-client.py` CLI (Phase 3), then built a Vikunja MCP server for real-time access (Phase 5). The MCP server exposes 6 tools over stdio.

### Evidence

- Ticketing Integration Analysis evaluated 7 tools; Vikunja selected (4.15/5.0)
- MCP server deployed and integrated with Copilot Agent Mode
- YAML file retained as portable fallback

---

## DP-17: Architecture-as-Code Framework

**Category**: Standards
**Status**: Under Evaluation

### The Question

Should the practice adopt a formal architecture-as-code specification (e.g., CALM) to machine-validate architectural models?

### Options

| Option | Description | Trade-off |
|--------|-------------|-----------|
| **A. Informal (Current)** | YAML metadata files + OpenAPI specs + manual conventions | Flexible; no formal validation; conventions enforced by AI instructions only |
| **B. CALM (Common Architecture Language Model)** | Formal JSON Schema-based architecture specification with CI-enforced validation | Machine-readable topology; auto-generated visualizations; adoption learning curve; schema rigidity |
| **C. C4-as-Code (Structurizr DSL)** | Architecture models in Structurizr DSL; rendered to C4 diagrams | Good visualization; limited to C4 views; does not cover data flows or governance rules |

### Current Position

**Option B in progress.** CALM Phase 0 (JSON Schema authoring) and Phase 1 (CI validation) are complete per the roadmap. The practice is evaluating how CALM integrates with the existing YAML metadata and AI workflow.

### Evidence

- `architecture/calm/` directory exists with CALM artifacts
- CALM integration plan documented in `docs/CALM-INTEGRATION-PLAN.md`

---

## DP-18: Measuring AI Value — Cost vs Quality vs Speed

**Category**: Measurement
**Status**: Under Evaluation

### The Question

How should the practice measure whether AI adoption is delivering value — and what metrics matter most?

### Options

| Option | Description | Trade-off |
|--------|-------------|-----------|
| **A. Cost-Centric** | Measure reduction in tooling spend and time-to-document | Easy to measure; misses quality improvements; may optimize for cheapness over correctness |
| **B. Quality-Centric** | Measure standards compliance rate, defect density in AI outputs, rework rate | Directly measures what matters; harder to quantify; rubric development required |
| **C. Speed-Centric** | Measure time from ticket to published solution design | Easy to measure; speed without quality is dangerous; may incentivize corner-cutting |
| **D. Balanced Scorecard** | Track cost per solution, quality score, time to first draft, standards compliance rate, and architect satisfaction | Comprehensive; measurement overhead; requires baseline data from pre-AI workflow |

### Current Position

Phase 1 measured **cost and quality** (155-point rubric, actual billing data). Speed has not been formally measured. No pre-AI baseline exists for comparison. The practice has cost evidence and quality evidence but not a balanced measurement framework.

### Open Questions

- What was the time-to-solution before AI? (No baseline captured)
- Is architect satisfaction being tracked?
- How frequently should quality scoring be repeated as the AI instructions evolve?

### Added Metric Candidate from New Research

- CI remediation efficiency: mean time from failed validation to AI-proposed fix and successful pipeline pass

---

## DP-19: Hybrid Copilot + Azure AI Foundry via MCP

**Category**: Integration
**Status**: Open

### The Question

Should the practice formally adopt a hybrid architecture where GitHub Copilot remains the local execution engine and Azure AI Foundry hosts enterprise MCP services for proprietary tools and governed data access?

### Options

| Option | Description | Trade-off |
|--------|-------------|-----------|
| **A. Copilot-Only** | Keep all AI operations in Copilot with existing integrations | Lowest complexity; limited access to bespoke enterprise backends |
| **B. Foundry-Centric Custom App** | Build custom centralized AI app on Azure for end-to-end workflow | High control; highest engineering cost; duplicates local execution capabilities |
| **C. Hybrid MCP Pattern** | Keep Copilot as client; add Azure-hosted MCP services for enterprise-specific tools/data | Best capability mix; moderate complexity; requires MCP service engineering and security controls |

### Current Position

The practice has adopted MCP patterns for ticketing and local mock tools. The remaining decision is whether to extend this pattern with Azure AI Foundry-hosted MCP servers for enterprise data sources and specialized governance tools.

### Decision Drivers

- Enterprise data access requirements beyond current local workspace scope
- Security and identity controls for governed backend tool execution
- Engineering capacity to build and operate MCP services in Azure
- Latency and reliability requirements for local agent workflows

---

---

## Decision Dependency Map

Some decisions constrain or inform others. This map shows the key dependencies:

```
DP-01 (Buy vs Build)
  └─> DP-03 (Toolchain Selection)
        ├─> DP-02 (Billing Model)
        ├─> DP-04 (Single vs Multi-Tool)
        │     └─> DP-15 (Multi-Model Strategy)
        ├─> DP-09 (Context Enrichment)
  ├─> DP-10 (Vendor Lock-In vs Portability)
  └─> DP-19 (Hybrid Copilot + Azure Foundry via MCP)

DP-06 (AI Autonomy Level)
  ├─> DP-05 (Standards Enforcement)
  ├─> DP-12 (Trust Model)
  └─> DP-14 (Publishing Pipeline)

DP-07 (Knowledge Curation)
  └─> DP-08 (Skill Library Strategy)

DP-11 (Org Adoption Model)
  ├─> DP-07 (Knowledge Curation)
  └─> DP-18 (Measuring AI Value)

DP-13 (Data Isolation)
  └─> Precondition for all other decisions

DP-16 (Ticketing Integration Pattern)
  └─> DP-19 (Hybrid Copilot + Azure Foundry via MCP)
```

---

## Summary: Recommendation and Evaluation State

### Recommendation Drafts (7)

| # | Decision | Outcome |
|---|----------|---------|
| DP-01 | Buy vs Build | Hybrid — commercial AI + custom instructions |
| DP-02 | Billing Model | Intent-based (Copilot Pro+) |
| DP-03 | Toolchain | GitHub Copilot Pro+ (Claude Opus 4.6) |
| DP-09 | Context Enrichment | Hybrid — always-on instructions + semantic indexing |
| DP-13 | Data Isolation | Synthetic workspace, audit script, no network calls |
| DP-14 | Publishing | Automated on git push (MkDocs + Azure + Confluence mirror) |
| DP-16 | Ticketing Integration | Progressive: YAML to CLI to MCP |

### Under Evaluation - Active Work (2)

| # | Decision | Current State |
|---|----------|---------------|
| DP-08 | Skill Library | ECC Tier 1 adaptation underway |
| DP-17 | Architecture-as-Code | CALM Phase 0+1 complete |

### Under Evaluation - Recommendation Exists (6)

| # | Decision | What Remains |
|---|----------|-------------|
| DP-04 | Single vs Multi-Tool | Claude Code spike not yet executed |
| DP-05 | Standards Enforcement | Layered model selected in principle; high-risk runtime checks not implemented |
| DP-07 | Knowledge Curation | No formal strategy for monolith vs modular split |
| DP-10 | Vendor Lock-In | Portable-core strategy chosen; no ADR yet for long-term portability policy |
| DP-12 | Trust Model | Rubric exists but progressive trust framework not formalized |
| DP-18 | Measuring AI Value | Cost and quality measured; speed and satisfaction not baselined |

### Open (4)

| # | Decision | Why It Matters |
|---|----------|---------------|
| DP-06 | AI Autonomy Level | Current approach is ad-hoc, not policy |
| DP-11 | Org Adoption Model | Scaling beyond one practitioner is unplanned |
| DP-15 | Multi-Model Strategy | Potential cost savings from model tiering unexplored |
| DP-19 | Hybrid Copilot + Azure Foundry via MCP | Determines whether enterprise-grade backend intelligence is added without rebuilding local execution |
