# OpenSpec Evaluation: Should We Adopt It for Architecture Solution Design Workflow?

**Date**: 2026-03-17
**Status**: Decided — Do Not Adopt
**Context**: Evaluate whether OpenSpec improves NovaTrek's AI-assisted architecture solution design workflow

---

## 1. Executive Summary

OpenSpec is a **spec-driven development workflow framework** for AI coding agents. It structures how developers and AI assistants plan, specify, and implement changes using organized artifacts (proposals, behavioral specs, design documents, task checklists) with a delta-based change tracking model.

NovaTrek already has a **purpose-built architecture solution design workflow** with a richer artifact structure (requirements, analysis, assumptions, capabilities, MADR decisions, guidance, per-service impacts, risks, user stories). The question is whether OpenSpec's workflow tooling — slash commands, schema-driven dependency graphs, delta spec merging, and multi-tool agent support — provides enough value to justify adopting it alongside or in place of the existing workflow.

**Decision**: Do not adopt. OpenSpec solves problems we don't have (multi-tool portability) and lacks the architecture-specific artifacts our governance workflow requires (MADR decisions, per-service impacts, capability model, dedicated risks and assumptions). The existing workflow is purpose-built and actively improving through native Copilot customization. See Section 6 for the full rationale.

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

## 5. Options Considered

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

Adopt OpenSpec as the workflow engine, creating a custom schema that maps to NovaTrek's artifact structure.

**Advantages**:
- Schema-enforced workflow ordering
- Multi-tool AI agent portability
- Delta spec model for behavioral change tracking
- Formalized Given/When/Then specifications

**Disadvantages**:
- Custom schema feasibility is unvalidated — no evidence it can enforce MADR format, handle variable-count impact subdirectories, or trigger capability changelog rollups
- OpenSpec is from a startup (Fission AI) with no foundation governance — sustainability uncertain
- Additional npm dependency and learning curve
- Existing completed solutions would be in old format (inconsistency)
- No enterprise adoption evidence for architecture governance use cases

**Risk level**: MEDIUM-HIGH

### Option C: Time-Boxed PoC

Run a single architecture scenario through both workflows in parallel.

**Advantages**:
- Evidence-based decision
- Minimal commitment, fully reversible

**Disadvantages**:
- Time investment for setup and dual execution on speculative tooling
- PoC results from one scenario may not generalize
- Diverts effort from higher-priority platform work

**Risk level**: LOW (but opportunity cost is real)

---

## 6. Decision: Do Not Adopt OpenSpec

**Decision: Option A — Keep existing workflow. Do not adopt OpenSpec.**

### Why Not OpenSpec

#### 1. OpenSpec solves a problem we don't have

OpenSpec's primary value is **multi-tool AI agent portability** (works with 20+ tools) and **workflow enforcement via schema**. NovaTrek currently uses a single AI tool (GitHub Copilot) with no plans to diversify. Multi-tool portability is a solution looking for a problem.

Workflow enforcement is a real gap, but we are actively addressing it through purpose-built mechanisms (`.instructions.md` files, prompt templates, copilot-instructions.md improvements) that are native to our toolchain and cost nothing to adopt.

#### 2. OpenSpec was designed for feature development, not architecture governance

OpenSpec's default artifact model (proposal + specs + design + tasks) is a flat, lightweight structure suited for shipping code changes. Architecture governance requires:

- **MADR-format decision records** with required sections (Status, Date, Context, Decision Drivers, 2+ Options with pros/cons, Outcome, Consequences) — OpenSpec's `design.md` has no equivalent rigor
- **Per-service impact assessments** documenting API contract changes, data model modifications, and integration point changes — OpenSpec has no concept of service-level impacts
- **Capability model tracking** recording L3 capability emergence per solution and feeding portal generators — OpenSpec has no capability model
- **Dedicated assumptions, risks, and guidance artifacts** — OpenSpec merges these into proposal/design documents without separation

These are not minor gaps. They are the core of what makes architecture governance different from feature development.

#### 3. Custom schema feasibility is unvalidated and likely insufficient

The theoretical custom schema (Section 4) could map artifact types, but critical questions remain unanswered:

- Can schemas enforce **content structure within artifacts** (e.g., MADR sections)? Likely not — schema validation appears to check file existence, not file content.
- Can schemas handle **variable-count subdirectories** (e.g., `impacts/impact.1/`, `impacts/impact.2/`)? Unknown.
- Can schemas **trigger metadata rollups** (e.g., updating `capability-changelog.yaml` on archive)? Almost certainly not — this is custom business logic, not file generation.

Building custom tooling to bridge these gaps would likely cost more than the value OpenSpec provides.

#### 4. Startup dependency risk with no governance safety net

OpenSpec is v1.2.0 from Fission AI, a startup. There is:

- No foundation governance (not FINOS, not Linux Foundation, not Apache)
- No public funding or sustainability information
- Rapid iteration with unclear breaking change policy
- No documented enterprise adoption for architecture use cases specifically

GitHub stars (31.5k) reflect developer interest, not enterprise suitability. The MIT license allows forking, but maintaining a fork of an abandoned framework is a cost, not a mitigation.

#### 5. Opportunity cost is real

Every hour spent evaluating, configuring, and integrating OpenSpec is an hour not spent on higher-value work: completing solution designs for pending NTK tickets, improving portal generators, building CI governance rules, or extending the capability model. The existing workflow is functional and actively improving. The ROI on OpenSpec investigation is speculative at best.

### What We Lose by Not Adopting

To be fair, we forgo:

| Capability | Impact of Not Having It |
|-----------|------------------------|
| Schema-enforced artifact ordering | LOW — `.instructions.md` and copilot-instructions.md provide adequate guidance; AI compliance is high |
| Multi-tool portability | NONE — we use one tool with no plans to change |
| Delta-based behavioral specs | LOW — capability changelog tracks architectural changes; behavioral contract evolution is tracked via OpenAPI spec versioning |
| Given/When/Then formalized specs | LOW — requirements from tickets are captured narratively; formalization adds precision but not enough to justify tooling overhead |
| Slash commands for AI workflow | LOW — Copilot Agent Mode handles multi-step workflows through instruction files effectively |

None of these losses represent a material risk to architecture quality or delivery velocity.

### When to Revisit

Revisit this decision if ANY of the following conditions change:

1. **We adopt a second AI coding tool** (e.g., Claude Code, Cursor) and need portable workflow instructions
2. **Workflow enforcement becomes a real pain point** — repeated failures where the AI agent produces architecturally incomplete solutions despite instruction file improvements
3. **OpenSpec achieves foundation governance** (joins FINOS, Linux Foundation, or equivalent) and demonstrates enterprise architecture adoption
4. **OpenSpec adds architecture-specific features** — capability models, MADR templates, per-service impact tracking, or metadata rollup hooks

Until then, invest in improving the existing workflow through native Copilot customization mechanisms.

---

## 7. Risk Assessment of This Decision

| Risk | Likelihood | Impact | Assessment |
|------|-----------|--------|-----------|
| OpenSpec becomes industry standard and we're behind | Low | Medium | MIT license means we can adopt later; architecture workflows are not easily commoditized |
| Existing workflow enforcement proves inadequate | Medium | Low | Addressable through `.instructions.md` improvements without external tooling |
| Competitor organizations gain AI workflow advantage via OpenSpec | Low | Low | OpenSpec's architecture governance gaps mean competitors face the same integration challenges |
| OpenSpec adds architecture features that would have been valuable | Low | Medium | Monitor releases; revisit criteria are explicitly defined above |

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
