# OpenSpec Evaluation: Should We Adopt It for Architecture Solution Design Workflow?

**Date**: 2026-03-17
**Status**: Draft
**Context**: Evaluate whether OpenSpec improves NovaTrek's AI-assisted architecture solution design workflow

---

## 1. Executive Summary

OpenSpec is a **spec-driven development workflow framework** for AI coding agents. It structures how developers and AI assistants plan, specify, and implement changes using organized artifacts (proposals, behavioral specs, design documents, task checklists) with a delta-based change tracking model.

NovaTrek already has a **purpose-built architecture solution design workflow** with a richer artifact structure (requirements, analysis, assumptions, capabilities, MADR decisions, guidance, per-service impacts, risks, user stories). The question is whether OpenSpec's workflow tooling — slash commands, schema-driven dependency graphs, delta spec merging, and multi-tool agent support — provides enough value to justify adopting it alongside or in place of the existing workflow.

**NOTE**: This evaluation is independent of NovaTrek's CALM (Architecture as Code) integration. CALM is a machine-readable architecture topology specification — a completely different category of tool. CALM handles system structure and governance; OpenSpec handles development workflow. They do not compete, and comparing them is a category error.

---

## 2. What OpenSpec Actually Is

### Core Concepts

| Concept | Description |
|---------|-------------|
| **Specs** | Behavioral contracts describing how the system works, organized by domain. Requirements use RFC 2119 keywords (SHALL/MUST/SHOULD/MAY) with Given/When/Then scenarios. Live in `openspec/specs/`. |
| **Changes** | Proposed modifications packaged as folders. Each change contains artifacts (proposal, design, tasks) and delta specs. Live in `openspec/changes/<name>/`. |
| **Delta Specs** | Describe what's changing (ADDED/MODIFIED/REMOVED requirements) relative to current specs. On archive, deltas merge into main specs. |
| **Artifacts** | Documents within a change: `proposal.md` (why + scope), `design.md` (how), `tasks.md` (implementation checklist), `specs/` (delta specs). |
| **Schemas** | YAML definitions of artifact types and their dependency graph. Customizable per project. |
| **Slash Commands** | AI agent workflow commands: `/opsx:propose`, `/opsx:apply`, `/opsx:archive`, etc. |

### How It Works

```
/opsx:propose "add-dark-mode"
    │
    ▼
openspec/changes/add-dark-mode/
├── proposal.md           # Why and what (intent, scope, approach)
├── specs/ui/spec.md      # Delta: ADDED/MODIFIED/REMOVED requirements
├── design.md             # How (technical approach, architecture decisions)
└── tasks.md              # Implementation checklist with checkboxes
    │
    ▼  (/opsx:apply — work through tasks)
    │
    ▼  (/opsx:archive — when done)
    │
openspec/specs/ui/spec.md  # Main spec now includes merged deltas
openspec/changes/archive/2026-03-17-add-dark-mode/  # Change preserved
```

### Key Properties

- **31.5k GitHub stars**, 50 contributors, MIT license, v1.2.0
- **Supports 20+ AI tools**: Claude Code, Cursor, Codex, GitHub Copilot, Windsurf, etc.
- **Custom schemas**: Define your own artifact types and dependency graphs
- **Brownfield-first**: Delta model designed for modifying existing systems, not just greenfield
- **No API keys, no MCP**: Pure file-based, convention-driven
- **By Fission AI** (startup) — not under a foundation governance model

---

## 3. Comparison: OpenSpec vs NovaTrek's Existing Solution Design Workflow

### 3.1 Artifact Mapping

| NovaTrek Current Artifact | Location | OpenSpec Equivalent | Assessment |
|--------------------------|----------|---------------------|------------|
| Ticket report | `1.requirements/` | `proposal.md` (Intent section) | OpenSpec lighter — merges requirements into proposal |
| Simple explanation | `2.analysis/` | `proposal.md` (Scope + Approach) | OpenSpec lighter — no separate analysis artifact |
| Assumptions | `3.solution/a.assumptions/` | Part of `proposal.md` or `design.md` | **Gap** — no dedicated assumptions artifact |
| Capabilities | `3.solution/c.capabilities/` | No equivalent | **Gap** — OpenSpec has no capability model |
| Decisions (MADR) | `3.solution/d.decisions/` | `design.md` (Architecture Decisions section) | **Gap** — OpenSpec's format is less rigorous than MADR |
| Guidance | `3.solution/g.guidance/` | `design.md` (Technical Approach) | Merged — not separated from decisions |
| Per-service impacts | `3.solution/i.impacts/` | No direct equivalent | **Gap** — no per-service impact assessment |
| Risks | `3.solution/r.risks/` | Part of `proposal.md` | **Gap** — no dedicated risk artifact |
| User stories | `3.solution/u.user.stories/` | `specs/` (Given/When/Then scenarios) | Different framing — behavioral specs vs. user stories |
| Master document | `NTK-XXXXX-solution-design.md` | `proposal.md` + cross-refs | OpenSpec lighter |
| Capability changelog | `capability-changelog.yaml` | `openspec/specs/` (delta merge) | Different mechanism entirely |

**Summary**: OpenSpec's default artifact model (proposal + specs + design + tasks) is a **simpler, flatter structure** designed for feature development. NovaTrek's solution design workflow is richer and purpose-built for architecture governance. OpenSpec's default schema lacks dedicated artifacts for assumptions, capabilities, impacts, risks, and MADR-format decisions.

### 3.2 Workflow Comparison

| Dimension | NovaTrek Current | OpenSpec |
|-----------|-----------------|----------|
| **Workflow enforcement** | Convention-based — documented in copilot-instructions.md, agent tries to follow | Schema-driven — dependency graph enforces artifact creation order |
| **AI agent guidance** | Long instruction document (~800 lines) AI reads and interprets | Slash commands + skill files AI tools natively understand |
| **Tool portability** | Copilot-specific (copilot-instructions.md) | 20+ tools supported natively |
| **Change tracking** | Capability changelog records what changed per solution | Delta specs (ADDED/MODIFIED/REMOVED) merge into behavioral source of truth |
| **Iteration model** | Linear: create artifacts in folder structure | Fluid: update any artifact anytime, no phase gates |
| **Artifact dependencies** | Implicit (documented conventions) | Explicit (YAML schema with `requires:` declarations) |
| **Archive/completion** | Solution folder stays in `architecture/solutions/` | Change moves to `archive/`, deltas merge into main specs |
| **Behavioral specs** | Requirements captured narratively from tickets | Formalized Given/When/Then scenarios with RFC 2119 keywords |
| **Review experience** | Reviewer reads full solution folder | Reviewer reads delta showing exactly what changed |

### 3.3 Where OpenSpec Is Stronger

1. **Workflow enforcement via schema**: OpenSpec's dependency graph (proposal -> specs -> design -> tasks) ensures artifacts are created in order. NovaTrek relies on AI reading instructions and hoping it follows the structure.

2. **AI agent portability**: OpenSpec works with 20+ tools natively. NovaTrek's workflow is encoded in Copilot-specific instructions. If we switch tools or add new ones, we must rewrite instructions.

3. **Delta-based change tracking**: OpenSpec's ADDED/MODIFIED/REMOVED model provides a clear behavioral diff. NovaTrek's capability changelog tracks capability changes but not behavioral contract evolution.

4. **Formalized behavioral specifications**: Given/When/Then scenarios with RFC 2119 keywords are testable and precise. NovaTrek captures requirements narratively.

5. **Fluid iteration**: OpenSpec explicitly supports updating artifacts mid-implementation without "going back." NovaTrek's workflow is implicitly linear.

### 3.4 Where NovaTrek's Existing Workflow Is Stronger

1. **Architecture-specific artifacts**: Dedicated assumptions, capabilities, impacts (per-service), risks, and guidance artifacts. OpenSpec lacks these.

2. **MADR decision rigor**: MADR format with required sections (Status, Date, Context, Decision Drivers, 2+ Options with pros/cons, Outcome, Consequences). OpenSpec's `design.md` has a simpler, less structured decisions section.

3. **Capability model integration**: NovaTrek's `capability-changelog.yaml` tracks L3 capability emergence per solution, feeding portal generators. OpenSpec has no capability concept.

4. **Per-service impact assessment**: NovaTrek creates separate impact files for each affected service, documenting API contract changes, data model modifications, and integration point changes. OpenSpec has no equivalent.

5. **Purpose-built for architecture**: The workflow was designed for architecture governance. OpenSpec was designed for feature development.

---

## 4. Can OpenSpec's Custom Schemas Bridge the Gap?

OpenSpec supports custom schemas that define artifact types and dependencies:

```yaml
# Hypothetical novatrek-architecture schema
name: novatrek-architecture
artifacts:
  - id: requirements
    generates: requirements.md
    requires: []
  - id: analysis
    generates: analysis.md
    requires: [requirements]
  - id: specs
    generates: specs/**/*.md
    requires: [requirements]
  - id: decisions
    generates: decisions.md
    requires: [specs]
  - id: impacts
    generates: impacts/**/*.md
    requires: [specs, decisions]
  - id: risks
    generates: risks.md
    requires: [specs]
  - id: tasks
    generates: tasks.md
    requires: [specs, decisions, impacts]
```

**Unknown**: Whether custom schemas can:
- Enforce specific formats within artifacts (e.g., MADR structure in decisions.md)
- Support template injection for artifact-specific conventions (e.g., ISO 25010 quality attributes in risks)
- Handle the capability changelog rollup pattern (metadata YAML update triggered by change completion)
- Accommodate per-service impact subdirectories with variable count

This is a **critical unknown** that deep research should resolve before committing to adoption.

---

## 5. Options Analysis

### Option A: Keep Existing Workflow (No OpenSpec)

Continue the current solution design workflow as-is.

**Advantages**:
- No new tooling to learn or maintain
- Workflow is purpose-built for architecture governance
- All required artifacts (impacts, capabilities, MADR decisions) are first-class
- No dependency on a startup's framework

**Disadvantages**:
- Workflow enforcement is convention-based, not tool-enforced
- AI agent guidance is Copilot-specific, not portable
- No formalized behavioral specification layer
- No delta-based change tracking for behavioral contracts

**Risk level**: LOW

### Option B: Adopt OpenSpec with Custom Architecture Schema

Adopt OpenSpec as the workflow engine, creating a custom schema that maps to NovaTrek's artifact structure. Use OpenSpec's slash commands, dependency graph, and delta model while preserving architecture-specific artifacts.

**Advantages**:
- Schema-enforced workflow ordering
- Multi-tool AI agent portability
- Delta spec model for behavioral change tracking
- Formalized Given/When/Then specifications
- Fluid iteration without phase gates

**Disadvantages**:
- Custom schema feasibility is unvalidated
- MADR format enforcement within OpenSpec artifacts is unclear
- Capability changelog integration requires custom work
- OpenSpec is from a startup — governance uncertain
- Additional npm dependency and learning curve
- Existing completed solutions would be in old format (inconsistency)

**Risk level**: MEDIUM

### Option C: Time-Boxed PoC

Run a single architecture scenario through both workflows (existing and OpenSpec) in parallel to collect evidence before deciding.

**Advantages**:
- Evidence-based decision instead of speculation
- Minimal commitment, fully reversible
- Tests the critical unknowns (custom schema feasibility, AI quality improvement, artifact coverage)
- Aligns with NovaTrek's PoC methodology

**Disadvantages**:
- Time investment for setup and dual execution
- PoC results from one scenario may not generalize

**Risk level**: LOW

---

## 6. Recommendation

**Recommendation: Option C (Time-Boxed PoC)**

### Rationale

1. **The critical unknowns are testable.** We don't know if custom schemas can accommodate architecture artifacts, if slash commands improve AI output quality, or if the delta model adds review value. A PoC answers all three.

2. **The existing workflow works.** It's not broken — it just lacks enforcement tooling and multi-tool portability. There's no urgency to replace it.

3. **OpenSpec's value proposition is narrow for architecture work.** The strongest value-adds (workflow enforcement, AI portability, delta specs) are real but modest. The gaps (no impacts, no capabilities, simpler decisions format) are significant for architecture governance.

4. **A PoC is reversible.** If OpenSpec doesn't improve the workflow, remove it and continue as-is.

### Decision Criteria (Post-PoC)

Adopt OpenSpec if ALL of the following are true:
- Custom schema successfully accommodates all NovaTrek artifact types
- AI agent output quality improves (fewer corrections, better artifact structure)
- Delta specs add clear review value beyond narrative analysis
- The overhead (npm dependency, learning curve, additional config) is justified

Stay with existing workflow if ANY of the following are true:
- Custom schema cannot accommodate impacts, capabilities, or MADR decisions
- AI agent quality improvement is marginal
- Delta specs duplicate information already in capability-changelog.yaml
- The two-system overhead creates confusion about where artifacts live

---

## 7. Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Custom schema can't accommodate architecture artifacts | Medium | High | Test in PoC; fall back to existing workflow |
| Fission AI abandons OpenSpec | Low | High | MIT license allows forking; evaluate governance trajectory |
| OpenSpec updates break custom schema | Medium | Medium | Pin version; test updates in CI |
| Team confusion about artifact locations | Medium | Medium | Clear documentation; single source-of-truth table |
| Behavioral specs drift from OpenAPI contracts | Medium | Medium | CI check comparing specs against OpenAPI |
| Maturity risk (v1.2.0, rapid iteration) | Medium | Medium | Pin version; evaluate stability before upgrading |

---

## 8. Key Unknowns for Deep Research

These questions cannot be answered from current research and are covered in [DEEP-RESEARCH-PROMPT-OPENSPEC-EVALUATION.md](DEEP-RESEARCH-PROMPT-OPENSPEC-EVALUATION.md):

1. **Custom schema limits**: Can OpenSpec schemas enforce artifact-internal formats (MADR), handle variable-count subdirectories (impacts), and trigger external rollups (capability changelog)?
2. **Enterprise adoption**: Who is actually using OpenSpec at scale? What is Comcast's specific use case?
3. **AI integration mechanics**: What exactly does OpenSpec generate for Copilot? Does it conflict with existing copilot-instructions.md?
4. **Governance trajectory**: Is Fission AI planning foundation membership?
5. **Architecture use cases**: Has anyone used OpenSpec for architecture governance, not just feature development?

---

## Appendix: Source Material

| Source | Access Date |
|--------|-------------|
| OpenSpec website (openspec.dev) | 2026-03-17 |
| OpenSpec GitHub (github.com/Fission-AI/OpenSpec) | 2026-03-17 |
| OpenSpec concepts docs (docs/concepts.md) | 2026-03-17 |
| OpenSpec OPSX workflow docs (docs/opsx.md) | 2026-03-17 |
| OpenSpec getting started (docs/getting-started.md) | 2026-03-17 |
| NovaTrek solution design workflow (copilot-instructions.md) | 2026-03-17 |
