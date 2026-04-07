<!-- CONFLUENCE-PUBLISH -->

# DD-01: Context and Configuration

| | |
|-----------|-------|
| **Status** | Under Evaluation |
| **Date** | 2026-04-07 |
| **Scope** | How does the AI platform acquire and apply enterprise domain knowledge? |
| **Feeds into** | DD-03 (AI Provider), EF-05 (Domain Context Awareness) |

---

## Problem Statement

The architecture practice requires AI to reason about a complex enterprise domain: 19 microservices, cross-service data ownership rules, safety constraints, MADR/C4/arc42 standards, and solution design workflows. The AI must apply this knowledge consistently — not just when prompted, but as always-on context that shapes every response.

The question is not whether to inject domain knowledge — all three options require it. The question is **how**: through declarative configuration files in the repository, through programmatic RAG pipelines, or through a custom-built agent with embedded knowledge.

---

## What the Pilot Already Demonstrates

The architecture practice pilot is a working demonstration. The practice has already built a comprehensive context injection system using native platform capabilities:

| Content Layer | Mechanism | Size | Evidence |
|---------------|-----------|------|----------|
| Role definition and domain model | `copilot-instructions.md` | 500+ lines | Solution Architect persona, 19-service domain, bounded context rules, data ownership |
| Security context | `architecture/.instructions.md` | Scoped | Data ownership boundaries, identity resolution, safety defaults, API contract security |
| OpenAPI design rules | `architecture/specs/.instructions.md` | Scoped | Resource naming, HTTP methods, schema completeness checklist, backward compatibility |
| Solution review checklist | `architecture/solutions/.instructions.md` | Scoped | Prior-art discovery, architecture review criteria, anti-pattern detection |
| Interactive workflows | `.github/instructions/prompt-me.instructions.md` | On-demand | Decision-loop workflow with lettered options and recommendations |
| Mock enterprise tools | MCP servers (local Python scripts) | 3 tools | JIRA, Elastic, GitLab simulation via JSON fixtures |

**Total investment: zero engineering, zero infrastructure.** All configuration is declarative markdown committed to the repository. The AI reads it, follows it, and produces architecture-quality output — as demonstrated by 4 completed solution designs, 14 ADRs, 139 generated sequence diagrams, and a live architecture portal.

---

## Options

### Option A: Native Declarative Configuration (Copilot)

Use the platform's built-in instruction hierarchy — global instructions, scoped instructions, skills, agent modes, and MCP — all as workspace-committed files. No custom infrastructure.

- **Already proven** with 96%+ quality scores on architecture scenarios
- **Zero engineering cost** — configuration is markdown, maintained by architects
- **Portable content** — instruction file content (not format) transfers to any platform
- **Gap:** Enterprise data sources outside the repository (CMDB, ServiceNow) require manual lookup or future MCP server development

### Option B: Custom RAG Pipeline (Roo Code + Kong)

Build a retrieval-augmented generation pipeline — vector database, embedding pipeline, prompt orchestration — to inject workspace and enterprise content into AI context.

- **Reconstructs native capabilities** — see [Build vs Leverage](../evidence/build-vs-leverage.md) for the 8-component comparison
- **Engineering investment** — months of development before productive use
- **Ongoing operational burden** — embedding jobs, vector DB maintenance, prompt engineering
- **Advantage:** Full control over retrieval quality and content ranking

### Option C: Embedded Knowledge Agent (Azure AI Foundry)

Build a custom agent with domain knowledge embedded in the system prompt, fine-tuned model, or retrieval backend. The agent "knows" the architecture domain by construction.

- **Budget-constrained model selection** — see [Model Quality at Budget](../evidence/model-quality-at-budget.md) for why this degrades output
- **Heaviest engineering investment** — custom agent framework, embedded knowledge maintenance
- **Knowledge maintenance burden** — every domain change requires agent update, not just a file edit
- **Advantage:** Maximum customization, purpose-built for exact workflow

---

## Assessment

The content taxonomy from the pilot tells the story:

| Content Type | Native Coverage | Custom Pipeline Needed? |
|-------------|----------------|------------------------|
| Architecture standards (arc42, C4, MADR) | FULL — `copilot-instructions.md` | No |
| Domain model (services, APIs, data ownership) | FULL — workspace-indexed YAML and specs | No |
| Solution templates and conventions | FULL — scoped `.instructions.md` | No |
| Prior solution designs | FULL — workspace-indexed markdown | No |
| Source code and OpenAPI specs | FULL — workspace-indexed | No |
| Enterprise tools (tickets, logs, code review) | FULL — MCP servers | No |
| Enterprise knowledge base (Confluence) | Solvable — migrate to repo markdown, publish via CI | No |
| CMDB / cross-team data | GAP — requires integration | Possibly, regardless of platform |

**7 of 8 content categories are fully served by native capabilities.** The remaining gap (enterprise data sources outside the repository) exists for all three options — it is a content availability problem, not a platform capability problem.

---

## Recommendation

**Option A (Native Declarative Configuration)** is the clear winner for DD-01. The evidence is not theoretical — it is running in production in the architecture practice pilot. Building a custom RAG pipeline or embedded agent to inject domain knowledge solves a problem that is already solved.

The decision to invest in custom infrastructure should be driven by a **demonstrated gap that native capabilities cannot fill**, not by an assumption that custom is better. No such gap has been identified.

---

**See also:**

- [Build vs Leverage](../evidence/build-vs-leverage.md) — Why custom RAG reconstructs native platform capabilities
- [Platform Landscape](../evidence/platform-landscape.md) — How all five major platforms handle context injection
- [Architecture Is Not Just Coding](../evidence/architecture-not-just-coding.md) — Evidence that declarative configuration works for architecture, not just coding
