# Azure AI Foundry: Third Platform Comparison Plan

## Extending the AI Toolchain Evaluation

| | |
|-----------|-------|
| **Project** | Continuous Architecture Platform POC |
| **Phase** | Phase 1 Extension — Third Platform Comparison |
| **Author** | Christopher Blaisdell |
| **Date** | 2026-03-16 |
| **Status** | DRAFT — Pending deep research results |
| **Objective** | Evaluate Azure AI Foundry as a third AI toolchain option alongside GitHub Copilot Pro+ and Roo Code + OpenRouter, with specific focus on the "build your own architecture agent" use case |

---

## 1 Background

### 1.1 Current State of the Comparison

Phase 1 evaluated two AI toolchains for architecture practice work:

| Platform | Cost Model | Monthly Cost | Per-Run Cost | Quality Score |
|----------|-----------|-------------|-------------|--------------|
| **GitHub Copilot Pro+** | Flat per-seat ($39/month) | $39 | $0.48 | 96.1% (149/155) |
| **Roo Code + OpenRouter** | Pay-per-token | ~$507 | ~$100 | TBD (fabrication issues noted) |

Both platforms embed AI assistance directly in the developer's IDE (VS Code). The architect interacts with the agent in their existing workflow — no separate application, no custom infrastructure.

### 1.2 Why a Third Option

The organization is evaluating **Azure AI Foundry** (formerly Azure AI Studio) as a platform to build a **custom architecture agent** — a centralized service that multiple architects (and potentially non-architects) could use to query architecture knowledge, generate documentation, and run architecture workflows.

This is a fundamentally different approach:
- Copilot and Roo Code are **IDE-embedded agents** that leverage the architect's local workspace context
- Azure AI Foundry would be a **centralized custom agent** built and maintained by the organization

This plan defines how we evaluate Azure AI Foundry against the two IDE-embedded options using the same evidence-based methodology from Phase 1.

### 1.3 The Core Concern

The proposal to "build our own agent" may be analogous to writing a custom database engine when mature commercial databases exist, or building a bespoke web framework when established frameworks solve the problem. This plan must objectively assess whether the custom-build path provides capabilities that the IDE-embedded tools cannot, or whether it duplicates functionality at higher cost and risk.

---

## 2 What Is Azure AI Foundry

### 2.1 Platform Overview (Pre-Research Understanding)

Azure AI Foundry is Microsoft's platform for building, evaluating, and deploying custom AI applications. Key components include:

| Component | Purpose |
|-----------|---------|
| **AI Foundry Portal** | Web-based UI for model selection, prompt engineering, evaluation |
| **Model Catalog** | Access to OpenAI, Meta, Mistral, Cohere, and other models |
| **Prompt Flow** | Visual orchestration of multi-step LLM workflows |
| **AI Search** | RAG-based retrieval over custom document indexes |
| **Evaluation** | Built-in evaluation and red-teaming for model outputs |
| **Deployment** | Managed endpoints for hosting custom AI applications |
| **Content Safety** | Built-in content filtering and responsible AI guardrails |

### 2.2 What the Organization Envisions

Based on initial conversations, the envisioned architecture agent would:

1. Be accessible to all architects via a web UI or Teams integration (not tied to VS Code)
2. Have knowledge of the organization's architecture standards, patterns, and decisions
3. Answer questions about the current architecture landscape
4. Generate documentation following corporate templates
5. Potentially perform ticket triage and impact analysis

### 2.3 What We Need to Validate Through Research

- Exact pricing model (consumption-based, reserved capacity, or hybrid)
- What "building an agent" actually entails (engineering effort, maintenance burden)
- Whether the custom agent can match the workspace-aware capabilities of IDE-embedded tools
- Whether Azure AI Foundry agents can execute multi-step autonomous workflows (tool calls, file operations, terminal commands) or are limited to chat/RAG patterns
- How the RAG approach compares to direct workspace context in terms of architecture output quality
- Total cost of ownership including infrastructure, engineering, and ongoing maintenance

---

## 3 Evaluation Framework

### 3.1 Comparison Dimensions

The evaluation must cover these dimensions to be directly comparable with the existing Phase 1 results:

| Dimension | What We Measure | Why It Matters |
|-----------|----------------|----------------|
| **Monthly cost per seat** | Total cost to provide AI-assisted architecture tooling to one architect | Direct budget impact; the primary decision driver (30% weight in ADR-001) |
| **Build cost** | One-time engineering effort to stand up the solution | IDE tools have near-zero build cost; custom agents do not |
| **Maintenance cost** | Ongoing engineering to operate, update, and improve | IDE tools are maintained by vendors; custom agents are maintained by the organization |
| **Architecture output quality** | Compliance with MADR, C4, arc42 standards | Architecture practice requires standards-compliant output (25% weight) |
| **Workspace awareness** | Ability to read, analyze, and reference local architecture artifacts | Architects work in file-based workspaces; the agent must navigate them |
| **Autonomy** | Ability to execute multi-step workflows without human intervention | Phase 1 scenarios require 35+ autonomous tool calls per session |
| **Accessibility** | Who can use it and from where | IDE tools require VS Code; web/Teams may reach more stakeholders |
| **Time to value** | How quickly can an architect start using it | IDE tools: install extension; custom agent: months of development |
| **Vendor lock-in** | Switching cost if the platform is abandoned | Affects long-term strategic flexibility |
| **Security and compliance** | Data residency, access control, audit logging | Fortune 500 requirements for PII handling and SOC 2 compliance |

### 3.2 Architecture Topology Comparison

The following diagrams illustrate where each agent lives and how architects interact with it.

#### Option A: GitHub Copilot Pro+ (Current Leader)

```
┌──────────────────────────────────────────────────────────────────┐
│  ARCHITECT'S WORKSTATION                                         │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  VS Code                                                 │    │
│  │                                                          │    │
│  │  ┌──────────────────┐    ┌───────────────────────────┐   │    │
│  │  │  Copilot Agent   │    │  Architecture Workspace   │   │    │
│  │  │  (built-in)      │◄──►│                           │   │    │
│  │  │                  │    │  ├── architecture/         │   │    │
│  │  │  - File reads    │    │  ├── decisions/            │   │    │
│  │  │  - Terminal cmds │    │  ├── specs/                │   │    │
│  │  │  - File edits    │    │  ├── portal/               │   │    │
│  │  │  - Sub-agents    │    │  └── scripts/              │   │    │
│  │  └────────┬─────────┘    └───────────────────────────┘   │    │
│  │           │                                               │    │
│  └───────────┼───────────────────────────────────────────────┘    │
│              │                                                    │
└──────────────┼────────────────────────────────────────────────────┘
               │ HTTPS (model inference only)
               ▼
      ┌─────────────────┐
      │  GitHub / Azure  │
      │  Model Hosting   │
      │  (Claude, GPT)   │
      └─────────────────┘

COST:  $39/month flat
BUILD: Zero (install extension)
MAINT: Zero (vendor-managed)
```

#### Option B: Roo Code + OpenRouter

```
┌──────────────────────────────────────────────────────────────────┐
│  ARCHITECT'S WORKSTATION                                         │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  VS Code                                                 │    │
│  │                                                          │    │
│  │  ┌──────────────────┐    ┌───────────────────────────┐   │    │
│  │  │  Roo Code Agent  │    │  Architecture Workspace   │   │    │
│  │  │  (extension)     │◄──►│                           │   │    │
│  │  │                  │    │  (same as Option A)        │   │    │
│  │  │  - File reads    │    │                           │   │    │
│  │  │  - Terminal cmds │    │                           │   │    │
│  │  │  - File edits    │    │                           │   │    │
│  │  └────────┬─────────┘    └───────────────────────────┘   │    │
│  │           │                                               │    │
│  └───────────┼───────────────────────────────────────────────┘    │
│              │                                                    │
└──────────────┼────────────────────────────────────────────────────┘
               │ HTTPS (pay-per-token)
               ▼
      ┌─────────────────┐
      │  OpenRouter      │
      │  (API Gateway)   │
      │  → Claude Opus   │
      └─────────────────┘

COST:  ~$507/month (usage-based)
BUILD: Low (install extension, configure API key)
MAINT: Low (API key management only)
```

#### Option C: Azure AI Foundry Custom Agent (Proposed)

```
┌──────────────────────────────────────────────────────────────────┐
│  ARCHITECT'S WORKSTATION                                         │
│                                                                  │
│  ┌────────────────────────────────────┐                          │
│  │  Browser / Teams / Custom App      │                          │
│  │  (thin client — no workspace       │                          │
│  │   access unless explicitly          │                          │
│  │   uploaded or indexed)              │                          │
│  └────────────┬───────────────────────┘                          │
│               │                                                   │
└───────────────┼───────────────────────────────────────────────────┘
                │ HTTPS
                ▼
┌──────────────────────────────────────────────────────────────────┐
│  AZURE CLOUD                                                      │
│                                                                    │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  Azure AI Foundry Project                                  │   │
│  │                                                            │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐   │   │
│  │  │  Custom Agent │  │  AI Search   │  │  Prompt Flow   │   │   │
│  │  │  (deployed    │  │  (RAG index  │  │  (orchestration │   │   │
│  │  │   endpoint)   │◄─┤   over arch  │  │   workflows)   │   │   │
│  │  │              │  │   documents) │  │                │   │   │
│  │  └──────┬───────┘  └──────────────┘  └────────────────┘   │   │
│  │         │                                                  │   │
│  │         │ Model inference                                  │   │
│  │         ▼                                                  │   │
│  │  ┌──────────────┐                                          │   │
│  │  │  Model        │                                          │   │
│  │  │  Deployment   │                                          │   │
│  │  │  (GPT-4o,     │                                          │   │
│  │  │   Claude, etc)│                                          │   │
│  │  └──────────────┘                                          │   │
│  │                                                            │   │
│  │  ┌──────────────────────────────────────────────────┐      │   │
│  │  │  Supporting Infrastructure                        │      │   │
│  │  │  ├── Azure OpenAI Service (model hosting)        │      │   │
│  │  │  ├── Azure AI Search (vector index)              │      │   │
│  │  │  ├── Azure Storage (document store)              │      │   │
│  │  │  ├── Azure App Service / Container Apps (UI)     │      │   │
│  │  │  ├── Azure Key Vault (secrets)                   │      │   │
│  │  │  ├── Azure Monitor (logging, cost tracking)      │      │   │
│  │  │  └── Azure Entra ID (authentication)             │      │   │
│  │  └──────────────────────────────────────────────────┘      │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

COST:  ??? (consumption + infrastructure + engineering)
BUILD: Significant (months of development)
MAINT: Ongoing (team required)
```

### 3.3 The Fundamental Architecture Difference

```
IDE-Embedded Agent (Copilot / Roo Code)           Custom Agent (AI Foundry)
═══════════════════════════════════════           ══════════════════════════

Context Source:                                   Context Source:
  LOCAL FILESYSTEM                                  RAG INDEX
  ├── Real-time workspace access                    ├── Pre-indexed document snapshots
  ├── Git status, diffs, branches                   ├── Periodic re-indexing required
  ├── Terminal command execution                    ├── No real-time file access
  ├── File creation and editing                     ├── No terminal access
  └── Full project structure awareness              └── Knowledge limited to index scope

Agent Capabilities:                               Agent Capabilities:
  ├── Read any file in workspace                    ├── Answer questions from index
  ├── Execute terminal commands                     ├── Generate text from templates
  ├── Create/edit files directly                    ├── Retrieve relevant documents
  ├── Run build tools and scripts                   ├── Summarize architecture content
  ├── Launch sub-agents for research                ├── (Custom tools if built)
  └── 35+ autonomous tool calls/session             └── Limited autonomous execution

Maintenance:                                      Maintenance:
  ├── Vendor handles updates                        ├── Organization handles updates
  ├── No infrastructure to manage                   ├── Index refresh pipeline
  └── Instructions via workspace files              ├── Model version management
                                                    ├── Prompt engineering iterations
                                                    ├── Infrastructure monitoring
                                                    └── Security patching
```

---

## 4 Cost Analysis Framework

### 4.1 Cost Components for Azure AI Foundry

Unlike IDE-embedded tools (which have simple per-seat pricing), a custom Azure AI Foundry agent involves multiple cost layers:

| Cost Layer | Components | Frequency |
|------------|-----------|-----------|
| **Model inference** | Azure OpenAI Service (per-token charges for GPT-4o, GPT-4, etc.) | Per query |
| **Search infrastructure** | Azure AI Search (index hosting, queries) | Monthly + per query |
| **Storage** | Azure Blob Storage for documents, embeddings | Monthly |
| **Compute** | App Service / Container Apps for agent UI/API | Monthly |
| **Networking** | VNet, Private Endpoints (if required by security) | Monthly |
| **Identity** | Azure Entra ID integration | Included (if existing tenant) |
| **Monitoring** | Azure Monitor, Log Analytics | Monthly |
| **Engineering — build** | Developer hours to design, build, test the agent | One-time |
| **Engineering — maintain** | Developer hours for updates, prompt tuning, index refresh, bug fixes | Monthly |
| **Engineering — content** | Architecture team time to prepare, clean, and curate content for the index | Ongoing |

### 4.2 Cost Estimation Methodology

To produce a fair comparison, we need to estimate TCO (Total Cost of Ownership) over 12 months for a team of N architects:

```
Copilot TCO    = N × $39 × 12
               = $468 × N per year

Roo Code TCO   = N × ~$507 × 12
               = ~$6,084 × N per year

Foundry TCO    = Build Cost + (Monthly Infra × 12) + (Monthly Engineering × 12) + (Per-Query × Queries × 12)
               = ??? (this is what the deep research must help us estimate)
```

### 4.3 Questions the Cost Analysis Must Answer

1. What is the Azure OpenAI Service pricing for GPT-4o (the most likely model choice) as of March 2026?
2. What is the Azure AI Search pricing for a typical architecture knowledge base (hundreds of documents, thousands of queries/month)?
3. What are typical Azure AI Foundry project costs reported by organizations that have deployed similar solutions?
4. What is the engineering effort (in person-months) to build a production-ready architecture agent?
5. What is the ongoing engineering effort to maintain the agent?
6. How does the per-query cost compare to Copilot's effective per-query cost ($0.48/run)?

### 4.4 Cost Comparison Template

Once research is complete, fill in this comparison matrix:

| Cost Component | Copilot Pro+ | Roo Code + OpenRouter | Azure AI Foundry |
|---------------|-------------|----------------------|-----------------|
| Monthly per-seat license | $39 | $0 | $0 |
| Monthly model inference (per seat) | $0 (included) | ~$507 | TBD |
| Monthly infrastructure | $0 | $0 | TBD |
| Monthly engineering/maintenance | $0 | $0 | TBD |
| Build cost (one-time, amortized monthly) | $0 | $0 | TBD |
| **Total monthly per seat** | **$39** | **~$507** | **TBD** |
| Annual cost (10 architects) | $4,680 | ~$60,840 | TBD |

---

## 5 Capability Gap Analysis

### 5.1 Phase 1 Scenario Requirements

The Phase 1 evaluation tested 5 scenarios that define the minimum capability bar:

| ID | Scenario | Key Capability Required |
|----|----------|------------------------|
| SC-01 | Ticket triage and classification | Read ticket data, classify against capability map, cross-reference existing work |
| SC-02 | Configuration-driven classification design | Read source code, analyze patterns, produce MADR ADR with options analysis |
| SC-03 | Production investigation | Query log data, read source code, trace data flows, produce investigation report |
| SC-04 | OpenAPI spec update | Read existing spec, identify gaps, produce updated YAML with backward compatibility |
| SC-05 | Complex cross-service solution design | Read multiple specs, produce full solution folder (15+ files), create PlantUML diagrams |

### 5.2 Capability Mapping

For each required capability, assess whether the platform can deliver it:

| Capability | Copilot Pro+ | Roo Code | Azure AI Foundry |
|------------|-------------|----------|-----------------|
| Read local files in real-time | YES | YES | NO — requires pre-indexing |
| Execute terminal commands | YES | YES | NO — unless custom tool built |
| Create/edit files directly | YES | YES | NO — output is chat/text only |
| Run mock tools (Python scripts) | YES | YES | NO — no local execution |
| Navigate git history | YES | YES | NO — unless indexed |
| Generate YAML/PUML artifacts | YES | YES | PARTIAL — generates text, cannot save to files |
| Multi-step autonomous execution | YES (35+ tool calls) | YES | PARTIAL — Prompt Flow supports chaining but at infrastructure level |
| Workspace-aware context | YES (full project) | YES (full project) | PARTIAL — limited to indexed content |
| Standards compliance (MADR, C4) | YES (via workspace instructions) | YES (via .roo rules) | REQUIRES — custom prompt engineering |
| Cross-reference OpenAPI specs | YES (reads files) | YES (reads files) | REQUIRES — specs indexed in AI Search |

### 5.3 The Workspace Gap

This is the critical architectural difference. IDE-embedded agents have **direct, real-time access** to the architect's workspace:

- They read the latest file content (not a stale index)
- They execute commands in the architect's terminal (mock tools, git, build scripts)
- They create and edit files directly in the workspace
- They see the full project structure and can navigate it autonomously

A custom Azure AI Foundry agent would need to either:

**(A) Replicate workspace access** — Build custom tools that connect the cloud agent to local file systems (complex, security concerns, latency)

**(B) Accept reduced capability** — Operate as a knowledge-base Q&A system without real-time workspace integration (simpler, but cannot perform SC-01 through SC-05 as tested)

**(C) Hybrid approach** — Use AI Foundry for broad organizational knowledge, but keep IDE-embedded tools for hands-on architecture work (adds cost, does not eliminate IDE tool need)

---

## 6 Risk Assessment

### 6.1 Risks of the Custom Agent Path

| Risk | Severity | Likelihood | Mitigation |
|------|----------|-----------|------------|
| **Reinventing the wheel** — Building capabilities that IDE tools already provide | HIGH | HIGH | This comparison plan; evidence-based evaluation before committing |
| **Perpetual beta** — Agent never reaches the quality of commercial tools | HIGH | MEDIUM | Define acceptance criteria before building; compare against Phase 1 quality scores |
| **Maintenance burden** — Organization must maintain what vendors maintain for free | MEDIUM | HIGH | Quantify ongoing FTE cost before committing |
| **Index staleness** — RAG index falls behind reality, producing outdated answers | MEDIUM | HIGH | Require automated re-indexing pipeline; measure freshness lag |
| **Scope creep** — "Architecture agent" becomes "everything agent" with unbounded requirements | HIGH | HIGH | Define clear capability boundaries before building |
| **Model version churn** — Azure OpenAI model versions deprecate, requiring prompt re-engineering | MEDIUM | MEDIUM | Budget for quarterly prompt/model update cycles |
| **Security surface** — Centralized agent with architecture knowledge becomes an attack target | HIGH | LOW | Defense-in-depth: Entra ID, Private Endpoints, content filtering |
| **Adoption failure** — Architects prefer IDE-embedded tools and do not use the custom agent | HIGH | MEDIUM | User research before building; measure adoption metrics post-launch |

### 6.2 Risks of NOT Building a Custom Agent

| Risk | Severity | Likelihood | Mitigation |
|------|----------|-----------|------------|
| **Limited audience** — IDE tools only reach VS Code users; non-architects cannot access architecture AI | MEDIUM | HIGH | Evaluate GitHub Copilot Extensions or Copilot for M365 as alternatives |
| **No organizational knowledge** — IDE tools have workspace context but not enterprise-wide architecture knowledge | MEDIUM | MEDIUM | Enhanced workspace instructions; curated architecture context in repos |
| **Vendor dependency** — Full reliance on GitHub/Microsoft for AI tooling | MEDIUM | LOW | Maintain ability to switch (Roo Code as fallback, OpenRouter for model flexibility) |

---

## 7 Evaluation Plan

### 7.1 Phase 1 Extension: Research and Analysis

| Step | Task | Method | Deliverable |
|------|------|--------|-------------|
| 7.1.1 | Deep research on Azure AI Foundry capabilities and pricing | AI deep research prompt | Research results document |
| 7.1.2 | Analyze Foundry agent architecture for architecture practice use case | Research synthesis | Architecture assessment |
| 7.1.3 | Estimate TCO for 12-month deployment with 10 architect seats | Cost modeling | Cost comparison matrix |
| 7.1.4 | Map Phase 1 scenarios to Foundry capabilities | Gap analysis | Capability mapping |
| 7.1.5 | Interview stakeholders on custom agent requirements | Conversations | Requirements document |
| 7.1.6 | Produce recommendation with evidence | ADR authoring | ADR addendum or update to ADR-001 |

### 7.2 Phase 1 Extension: Proof of Concept (If Warranted)

Only proceed to POC if the research phase indicates Foundry offers capabilities the IDE tools cannot match:

| Step | Task | Effort Estimate | Deliverable |
|------|------|----------------|-------------|
| 7.2.1 | Create Azure AI Foundry project with architecture document index | 2-3 days | Working AI Search index |
| 7.2.2 | Build minimal agent with architecture knowledge | 3-5 days | Deployable agent endpoint |
| 7.2.3 | Run Phase 1 scenarios SC-01 through SC-05 against Foundry agent | 1-2 days | Quality scores |
| 7.2.4 | Measure actual Azure costs for the test run | 1 day | Cost actuals |
| 7.2.5 | Compare results to Copilot and Roo Code scores | 1 day | Three-way comparison |

### 7.3 Decision Gate

After step 7.1.6, apply this decision tree:

```
Is there a capability that Azure AI Foundry provides
that IDE-embedded tools CANNOT provide?
  │
  ├── NO → Recommend against custom agent build
  │        (cost and complexity without unique value)
  │
  └── YES → Is that capability critical to the architecture practice?
             │
             ├── NO → Recommend against (nice-to-have does not justify TCO)
             │
             └── YES → Does the hybrid approach (Foundry + IDE tool) justify
                        the additional cost?
                        │
                        ├── NO → Recommend IDE tools only
                        │
                        └── YES → Proceed to Phase 1 Extension POC (7.2)
```

---

## 8 Presentation Integration

### 8.1 Updates to presentation.novatrek.cc

The presentation site currently compares two platforms. Adding the third requires:

| Page | Current Content | Proposed Update |
|------|----------------|-----------------|
| [cost-evidence.md](../presentation/docs/cost-evidence.md) | 2-column comparison (Copilot vs Roo Code) | 3-column comparison adding Foundry TCO |
| [solution.md](../presentation/docs/solution.md) | Solution pillars referencing IDE tools | Add "Why Not Build Your Own" section |
| [index.md](../presentation/docs/index.md) | Hero metrics for 2 platforms | Add third platform metric |
| NEW: foundry-analysis.md | — | Dedicated deep-dive page with architecture diagrams |

### 8.2 Updates to ADR-001

ADR-001 currently evaluates Option A (Roo Code) and Option B (Copilot). Add:

- **Option C: Azure AI Foundry Custom Agent** — with full pros/cons analysis
- Updated decision outcome table with three-way comparison
- Updated decision rationale explaining why Option C was or was not selected

---

## 9 Stakeholder Communication

### 9.1 Key Messages to Prepare

Depending on research findings, prepare messaging for one of these outcomes:

**If recommending AGAINST Foundry:**
- "We evaluated Azure AI Foundry as a platform for building a custom architecture agent. The IDE-embedded tools (GitHub Copilot) provide equivalent or superior capabilities at a fraction of the cost, without requiring custom infrastructure or ongoing engineering. Building a custom agent would replicate existing capabilities at [X]x the cost."

**If recommending FOR Foundry (as complement):**
- "Azure AI Foundry provides [specific capability] that IDE tools cannot match. We recommend a hybrid approach: IDE-embedded tools for hands-on architecture work, plus a lightweight Foundry agent for [specific use case]. The additional cost of $[X]/month is justified by [specific benefit]."

**If recommending further evaluation:**
- "The Azure AI Foundry option shows promise for [specific use case] but the cost and capability picture is not yet clear enough for a recommendation. We recommend a time-boxed POC of [X] days to gather concrete evidence."

### 9.2 What NOT to Communicate

Per the data isolation rules:

- Do NOT reference any real corporate system names, team names, or internal project identifiers
- Do NOT share any details about the organization's actual Azure subscription or infrastructure
- Do NOT name the Fortune 500 company — refer to it as "the organization" or "the enterprise"
- All examples use the NovaTrek Adventures synthetic domain exclusively
- All cost figures are based on published Azure pricing and the synthetic workload from Phase 1

---

## 10 Deliverables Checklist

| ID | Deliverable | Location | Status |
|----|------------|----------|--------|
| D1 | Deep research prompt for Azure AI Foundry | `research/DEEP-RESEARCH-PROMPT-AZURE-AI-FOUNDRY.md` | TODO |
| D2 | Deep research results (after executing D1) | `research/DEEP-RESEARCH-RESULTS-AZURE-AI-FOUNDRY.md` | BLOCKED on D1 |
| D3 | Cost comparison matrix (3-way) | Update in `phases/phase-1-ai-tool-cost-comparison/COST-MEASUREMENT-METHODOLOGY.md` | BLOCKED on D2 |
| D4 | ADR-001 addendum with Option C | Update in `decisions/ADR-001-ai-toolchain-selection.md` | BLOCKED on D2 |
| D5 | Presentation page with Foundry analysis | `presentation/docs/foundry-analysis.md` | BLOCKED on D2 |
| D6 | Updated cost-evidence page (3-column) | Update in `presentation/docs/cost-evidence.md` | BLOCKED on D2 |
| D7 | Stakeholder recommendation memo | TBD | BLOCKED on D2 |

---

## 11 Open Questions for Deep Research

These questions form the basis of the deep research prompt (D1):

1. **What exactly is Azure AI Foundry in March 2026?** Product naming has shifted (Azure AI Studio → Azure AI Foundry). What is the current product scope, GA status, and feature set?

2. **What does "building an agent" on Foundry actually entail?** Is it a low-code/no-code experience, or does it require significant software engineering? What skills are required?

3. **How does Foundry handle multi-step agent workflows?** Can it perform autonomous tool calls (file reads, API calls, code execution) like IDE-embedded agents, or is it primarily a chat/RAG system?

4. **What is the exact pricing model?** Consumption-based? Reserved capacity? Per-query? Per-token? What Azure services are required and what do they cost individually?

5. **What is the typical build time and engineering effort?** Case studies, reference architectures, or community reports on building enterprise knowledge agents on Foundry.

6. **How does RAG quality compare to direct file access?** Research on retrieval accuracy, index freshness, and answer quality in RAG-based architectures vs direct file reading.

7. **What are the limitations?** What can Foundry agents NOT do that IDE-embedded agents can? Where does the custom agent model break down?

8. **Are there alternative approaches within the Microsoft ecosystem?** Copilot Studio, Copilot for M365, Copilot Extensions — could these achieve the "accessible to everyone" goal without building a custom agent?

9. **What do enterprises that have built custom agents on Foundry report?** Success stories, failure stories, lessons learned, cost surprises.

10. **What is the security and compliance posture?** Data residency, RBAC, audit logging, SOC 2 alignment, content safety filtering.

---

## 12 Success Criteria

This plan is successful when:

- [ ] Deep research provides evidence-based answers to all 10 questions in Section 11
- [ ] A credible TCO estimate exists for a 12-month, 10-architect deployment
- [ ] The capability gap analysis is complete with concrete evidence (not speculation)
- [ ] ADR-001 is updated with a three-way comparison and clear recommendation
- [ ] The presentation site includes the third platform in its comparison
- [ ] Stakeholder messaging is prepared for the most likely outcome
- [ ] All analysis uses published pricing and the synthetic NovaTrek workload — zero corporate data exposure
