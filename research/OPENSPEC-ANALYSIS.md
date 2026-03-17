# OpenSpec vs CALM: Comprehensive Analysis for NovaTrek Continuous Architecture Platform

**Date**: 2026-03-17
**Status**: Draft
**Context**: Evaluate OpenSpec as a complement or alternative to CALM within the NovaTrek Continuous Architecture Platform

---

## 1. Executive Summary

CALM (Common Architecture Language Model) and OpenSpec are **fundamentally different tools solving different problems in the software development lifecycle**. CALM is a machine-readable architecture specification format for system topology — nodes, relationships, interfaces, patterns, and governance controls. OpenSpec is a spec-driven development framework for AI coding agents that structures behavioral requirements, design decisions, and implementation workflows around change proposals.

The two frameworks operate at **different abstraction layers**: CALM operates at the **architecture governance layer** (structure, topology, validation rules), while OpenSpec operates at the **development workflow layer** (requirements, design, implementation tracking). They are complementary by nature, not competing. However, OpenSpec's artifact model overlaps partially with NovaTrek's existing solution design workflow, which means adoption requires careful integration to avoid creating duplicate structures.

---

## 2. Framework Comparison Matrix

| Dimension | CALM (FINOS) | OpenSpec (Fission AI) |
|-----------|-------------|----------------------|
| **Primary purpose** | Architecture-as-code: model, validate, govern system topology | Spec-driven development: structure AI-assisted coding workflows |
| **Core abstraction** | Nodes, relationships, interfaces, patterns | Specs, changes, artifacts, delta specs |
| **Format** | JSON (JSON Schema 2020-12 based) | Markdown (structured with conventions) |
| **Schema enforcement** | JSON Schema validation, pattern matching | Convention-based (ADDED/MODIFIED/REMOVED sections), YAML schema definitions |
| **What it models** | System topology: services, databases, actors, integrations, deployment | Behavioral contracts: what the system should do (requirements + scenarios) |
| **Governance** | CI-enforced architecture rules (patterns, controls, standards) | Convention-based verification (`/opsx:verify`) |
| **AI integration** | AI consumes CALM as context for topology-aware decisions | AI is the primary user — slash commands drive agent workflows |
| **Visualization** | Topology graphs, dependency matrices, domain maps | Change status dashboards, artifact dependency graphs |
| **Change tracking** | Timelines (moments with architectural snapshots) | Delta specs (ADDED/MODIFIED/REMOVED merge into source of truth) |
| **Tool ecosystem** | CALM CLI (`@finos/calm-cli`), custom generators | OpenSpec CLI, 20+ AI tool integrations (Claude Code, Copilot, Cursor, etc.) |
| **Governance body** | FINOS (Fintech Open Source Foundation) — Linux Foundation member | Fission AI (startup) |
| **License** | Apache 2.0 | MIT |
| **Community size** | 44 contributors, 287 stars, 94 forks | 50 contributors, 31.5k stars, 2.1k forks |
| **Maturity** | v1.2+ (stable, weekly CLI releases) | v1.2.0 (34 releases in ~7 months, rapid iteration) |
| **Installation** | npm (`@finos/calm-cli`) or custom scripts | npm (`@fission-ai/openspec`) |
| **Language** | 66% TypeScript, 22.8% Java | 98.7% TypeScript |
| **Primary users** | Architects, platform engineers | Developers, AI coding assistants |

---

## 3. Complementarity Analysis

### 3.1 Where They Are Orthogonal (No Overlap)

| CALM Capability | OpenSpec Equivalent | Verdict |
|----------------|--------------------|---------| 
| System topology modeling (nodes, relationships) | None | CALM only |
| Interface definition (host-port, path, URL, OAuth2) | None | CALM only |
| Architecture pattern enforcement (JSON Schema) | None | CALM only |
| Governance controls (data ownership, API-mediated access) | None | CALM only |
| Deployment decorators (Kubernetes, Helm) | None | CALM only |
| Standards composition (org-specific JSON Schema extensions) | None | CALM only |
| Timeline/moment tracking (architectural evolution snapshots) | None | CALM only |
| Behavioral requirements (SHALL/MUST/SHOULD with scenarios) | None | OpenSpec only |
| Delta spec model (ADDED/MODIFIED/REMOVED merge) | None | OpenSpec only |
| AI agent slash commands (`/opsx:propose`, `/opsx:apply`) | None | OpenSpec only |
| Task tracking with checkbox implementation flow | None | OpenSpec only |
| Change-scoped artifact packaging (proposal + design + tasks + specs) | None | OpenSpec only |

### 3.2 Where They Potentially Overlap

| Concern | CALM Approach | OpenSpec Approach | Overlap Degree |
|---------|-------------|-------------------|----------------|
| **API contract evolution** | Interface definitions in topology JSON; timeline moments capture state snapshots | Delta specs can describe API behavior changes (MODIFIED requirements) | Low — CALM models the structure, OpenSpec models the behavior |
| **Architecture decisions** | Not native; ADRs are separate artifacts | `design.md` captures technical approach and architecture decisions per change | Low — different scope (system-level vs. change-level) |
| **Change management** | Timelines track architectural state at significant moments | Changes track the full lifecycle of a proposed modification | Medium — both track evolution, but at different granularity |
| **Validation/CI** | JSON Schema validation of topology, pattern conformance | Convention-based verification of spec formatting, manual `/opsx:verify` | Low — different validation targets |

### 3.3 Where They Overlap with NovaTrek's Existing Workflow

This is the critical analysis — OpenSpec's artifact model overlaps significantly with our existing solution design workflow:

| NovaTrek Current Artifact | Location | OpenSpec Equivalent | Overlap Risk |
|--------------------------|----------|--------------------|-----------| 
| Ticket report | `1.requirements/` | `proposal.md` (Intent section) | HIGH |
| Simple explanation | `2.analysis/` | `proposal.md` (Scope + Approach sections) | HIGH |
| Assumptions | `3.solution/a.assumptions/` | Part of `proposal.md` or `design.md` | MEDIUM |
| Capabilities | `3.solution/c.capabilities/` | No equivalent — OpenSpec has no capability model | NONE |
| Decisions (MADR) | `3.solution/d.decisions/` | `design.md` (Architecture Decisions section) | HIGH |
| Guidance | `3.solution/g.guidance/` | `design.md` (Technical Approach section) | HIGH |
| Impacts | `3.solution/i.impacts/` | No direct equivalent | NONE |
| Risks | `3.solution/r.risks/` | Part of `proposal.md` | LOW |
| User stories | `3.solution/u.user.stories/` | `specs/` (scenarios in Given/When/Then) | MEDIUM |
| Solution master document | `NTK-XXXXX-solution-design.md` | `proposal.md` + cross-references | HIGH |
| Capability changelog | `architecture/metadata/capability-changelog.yaml` | `openspec/specs/` (delta merge on archive) | MEDIUM |

**Key Insight**: OpenSpec's change model (proposal + specs + design + tasks) is a **simpler, flatter version** of NovaTrek's solution design folder structure. NovaTrek's structure is richer (separate impacts, capabilities, assumptions, guidance) but more complex. The question is whether simplification would be a net benefit or would lose critical architecture governance artifacts.

---

## 4. Where OpenSpec Could Add Value

### 4.1 AI Agent Workflow Structuring

**Current gap**: NovaTrek's solution design workflow is documented in `copilot-instructions.md` as a long instruction set. The AI agent reads these instructions and tries to follow the folder structure, but there is no automated enforcement of the workflow sequence.

**OpenSpec value**: OpenSpec's slash commands (`/opsx:propose`, `/opsx:continue`, `/opsx:apply`, `/opsx:archive`) provide a structured, tool-aware workflow that AI agents natively understand. The schema-driven dependency graph (proposal -> specs -> design -> tasks) ensures artifacts are created in the right order.

### 4.2 Behavioral Specification as a Gap-Filler

**Current gap**: NovaTrek documents architecture (topology, API contracts, service interactions) but does not formally specify **behavioral requirements** with testable scenarios. Requirements come from JIRA tickets (mock) and are captured narratively.

**OpenSpec value**: OpenSpec's spec format (requirements with Given/When/Then scenarios) provides a structured way to capture behavioral contracts that are testable and version-controlled. The delta spec model makes it natural to track how behavior evolves over time.

### 4.3 Brownfield Change Management

**Current gap**: NovaTrek's capability changelog tracks what changed per solution, but does not capture a "before and after" behavioral diff.

**OpenSpec value**: Delta specs (ADDED/MODIFIED/REMOVED) provide a clear behavioral diff that reviewers can understand quickly. The archive process merges deltas into the main specs, building a cumulative behavioral specification over time.

### 4.4 Multi-Tool Agent Support

**Current gap**: NovaTrek's AI workflow is tightly bound to GitHub Copilot instructions. Phase 1 compares Copilot vs. Roo Code, but the instruction format differs between tools.

**OpenSpec value**: OpenSpec supports 20+ AI tools natively. If NovaTrek expands beyond Copilot/Roo Code, OpenSpec provides a universal workflow layer that works across all AI coding assistants.

---

## 5. Where OpenSpec Would NOT Add Value (or Would Conflict)

### 5.1 Architecture Topology and Governance

OpenSpec has **zero** capability for modeling system topology, service dependencies, database ownership, or infrastructure architecture. CALM is the only tool in this comparison that addresses these concerns. OpenSpec cannot replace CALM for:
- System topology visualization
- CI-enforced architecture rules
- Pattern-based governance
- Deployment architecture modeling
- Cross-service dependency analysis
- Blast radius assessment

### 5.2 Capability Model

NovaTrek's capability model (L1/L2 capabilities in `capabilities.yaml`, L3 emergence in `capability-changelog.yaml`) has no equivalent in OpenSpec. OpenSpec tracks behavioral specs, not business capabilities.

### 5.3 Impact Assessment

NovaTrek's per-service impact assessment artifacts have no OpenSpec equivalent. OpenSpec's `design.md` captures technical approach but not the structured "what changes for each affected service" analysis that the solution design workflow requires.

### 5.4 MADR Decision Records

NovaTrek uses MADR format with required sections (Status, Date, Context, Decision Drivers, Considered Options with pros/cons, Decision Outcome, Consequences). OpenSpec's `design.md` has an "Architecture Decisions" section but uses a simpler format without the rigor of MADR. Adopting OpenSpec's decision format would be a regression in decision quality.

### 5.5 Duplicate Source of Truth Risk

If OpenSpec specs (`openspec/specs/`) and CALM topology (`architecture/calm/`) both claim to be the source of truth for different aspects of the same services, drift is inevitable. Any integration must establish clear ownership boundaries.

---

## 6. Options Analysis

### Option A: CALM Only (Status Quo)

Continue the current CALM integration plan through phases 2-5 without adopting OpenSpec.

**Advantages**:
- No new tooling to learn, integrate, or maintain
- No risk of duplicate source-of-truth conflicts
- CALM roadmap (phases 2-5) already addresses topology governance, drift detection, blast radius
- FINOS governance provides long-term stability
- Existing solution design workflow is mature and purpose-built for architecture work

**Disadvantages**:
- No formalized behavioral specification layer — requirements remain narrative
- Solution design workflow depends on copilot-instructions.md conventions rather than tool-enforced structure
- No delta-based change tracking for behavioral contracts
- AI agent workflow is Copilot-specific, not portable

**Risk level**: LOW (known path, no new dependencies)

### Option B: CALM + OpenSpec (Complementary Adoption)

Adopt OpenSpec as a **development workflow layer** operating alongside CALM as the **architecture governance layer**. OpenSpec handles behavioral specs and AI agent workflow; CALM handles topology, validation, and governance.

**Integration model**:
```
                    Developer workflow (OpenSpec)
                    ┌─────────────────────────┐
                    │ /opsx:propose           │
                    │   proposal.md           │
                    │   specs/ (behavioral)   │
                    │   design.md             │
                    │   tasks.md              │
                    └────────────┬────────────┘
                                 │
                    Architecture governance (CALM)
                    ┌────────────▼────────────┐
                    │ Topology validation     │
                    │ Pattern enforcement     │
                    │ Control verification    │
                    │ Impact analysis         │
                    └─────────────────────────┘
```

**Advantages**:
- Adds behavioral specification layer that CALM lacks
- Improves AI agent workflow portability across 20+ tools
- Delta spec model provides structured change tracking
- Both tools are open source (MIT and Apache 2.0)
- Can be piloted on a single solution design before full adoption

**Disadvantages**:
- Two frameworks to maintain, update, and integrate
- Requires mapping between OpenSpec artifacts and NovaTrek's richer solution design structure
- Risk of artifact duplication (OpenSpec proposal.md vs. solution master document)
- OpenSpec is from a startup (Fission AI) — long-term governance uncertain
- Team must learn OpenSpec's workflow in addition to existing architecture practices
- Additional npm dependency in the workspace

**Risk level**: MEDIUM (integration complexity, governance uncertainty)

**Required adaptations**:
1. Custom OpenSpec schema mapping artifacts to NovaTrek's solution structure
2. Clear ownership boundary: OpenSpec owns behavioral specs, CALM owns topology
3. CI pipeline integration — OpenSpec verify + CALM validate in same workflow
4. Suppress or adapt overlapping artifacts (don't generate OpenSpec `design.md` if using MADR in `decisions/`)

### Option C: Replace Solution Design Workflow with OpenSpec (Partial Migration)

Replace the current `architecture/solutions/` folder structure with OpenSpec's change model. Keep CALM for topology governance.

**Advantages**:
- Simplifies the solution design workflow (fewer artifacts, flatter structure)
- OpenSpec's workflow is AI-native and tool-agnostic
- Archive model provides clean change history with behavioral delta merge
- Eliminates custom folder structure in favor of an open standard

**Disadvantages**:
- **Loses critical artifacts**: impacts, capabilities, assumptions, guidance are not part of the OpenSpec model
- MADR decision format would need to be shoe-horned into OpenSpec's design.md
- Capability changelog has no OpenSpec equivalent — would need custom schema
- All existing solution designs (already completed) would be in old format, creating inconsistency
- OpenSpec's schema customization is available but untested at architecture-governance scale
- The NovaTrek solution design workflow was purpose-built for architecture work; OpenSpec was designed for feature development

**Risk level**: HIGH (loss of architecture-specific artifacts, untested at this use case scale)

### Option D: Evaluate OpenSpec in a Time-Boxed PoC

Run a single architecture scenario (e.g., one NTK ticket) using OpenSpec alongside the existing workflow specifically to test:
1. Whether OpenSpec's slash commands improve AI agent guidance quality
2. Whether delta specs add value for tracking behavioral changes
3. Whether the two-framework overhead is manageable
4. Whether a custom OpenSpec schema can accommodate NovaTrek's artifact needs

**Advantages**:
- Minimal commitment — learn before deciding
- Reversible — remove OpenSpec if it doesn't add value
- Provides real evidence for the CALM+OpenSpec vs. CALM-only decision
- Aligns with NovaTrek's existing PoC methodology (Phase 1 AI tool comparison)

**Disadvantages**:
- Time investment for setup and evaluation
- PoC results may not generalize to full-scale adoption
- OpenSpec's workspace features (team collaboration) are still "coming soon"

**Risk level**: LOW (reversible, time-boxed)

---

## 7. Recommendation

**Recommendation: Option D (Time-Boxed PoC), with Option A as the fallback**

### Rationale

1. **CALM and OpenSpec solve different problems** — they are complementary, not competing. The question is not "which one?" but "does the second one add enough value to justify the overhead?"

2. **NovaTrek's existing solution design workflow already covers most of what OpenSpec offers** — the folder structure, artifact types, and AI instructions are purpose-built for architecture work. OpenSpec's simpler model is designed for feature development, not architecture governance.

3. **The areas where OpenSpec genuinely adds new value are narrow but potentially significant**:
   - Formalized behavioral specs with Given/When/Then scenarios
   - Delta-based change tracking with merge semantics
   - AI agent workflow portability across tools
   - Structured slash commands for workflow enforcement

4. **A PoC provides evidence without commitment** — run one architecture scenario through both workflows and compare the output quality, AI agent behavior, and developer experience.

5. **If the PoC shows insufficient value, no harm done** — the CALM integration plan continues on its current trajectory.

### Decision Criteria for PoC Evaluation

After the PoC, adopt OpenSpec (Option B) if ALL of the following are true:
- OpenSpec's slash commands measurably improve AI agent guidance quality (fewer corrections, better-structured output)
- Delta specs provide review-time value that narrative analysis does not
- The custom schema can accommodate NovaTrek-specific artifacts (impacts, capabilities, assumptions) without excessive ceremony
- OpenSpec's overhead (npm dependency, additional files, learning curve) is justified by the value delivered

If ANY of the following are true, stay with CALM only (Option A):
- The custom schema cannot accommodate NovaTrek's artifact needs without losing critical governance artifacts
- The two-framework overhead creates confusion about where artifacts live
- OpenSpec's delta specs duplicate information already captured in capability-changelog.yaml
- The AI agent workflow improvement is marginal (< significant qualitative improvement)

---

## 8. Key Unknowns Requiring Deep Research

The following questions cannot be answered from the current research and require deeper investigation. The companion deep research prompt covers these in detail:

1. **Enterprise evidence**: Who is actually using OpenSpec at scale? What does Comcast's adoption look like specifically?
2. **Custom schema limits**: Can OpenSpec's custom schema model accommodate architecture-specific artifacts (impact assessments, capability mapping, MADR decisions)?
3. **CALM interoperability**: Has anyone integrated CALM and OpenSpec? Are there known integration patterns?
4. **Governance trajectory**: Is Fission AI (OpenSpec's creator) planning to join a foundation (CNCF, FINOS, Linux Foundation)? What is the long-term governance plan?
5. **Workspace features**: OpenSpec's team collaboration features are "coming soon" — what's the timeline and scope?

---

## Appendix A: Glossary

| Term | Definition |
|------|-----------|
| CALM | Common Architecture Language Model — JSON-based architecture specification by FINOS |
| OpenSpec | Spec-driven development framework for AI coding agents by Fission AI |
| FINOS | Fintech Open Source Foundation — Linux Foundation member hosting CALM |
| Delta spec | OpenSpec's change format showing ADDED/MODIFIED/REMOVED behavioral requirements |
| Pattern (CALM) | JSON Schema-based blueprint defining required architecture structures |
| Control (CALM) | Governance requirement applied to architecture elements |
| Artifact (OpenSpec) | Document within a change: proposal, design, tasks, or delta specs |
| MADR | Markdown Any Decision Record — NovaTrek's architecture decision format |
| Topology | CALM's graph of nodes (services, databases, actors) and relationships (interactions, connections) |

## Appendix B: Source Material

| Source | URL | Access Date |
|--------|-----|-------------|
| OpenSpec website | openspec.dev | 2026-03-17 |
| OpenSpec GitHub | github.com/Fission-AI/OpenSpec | 2026-03-17 |
| OpenSpec concepts docs | github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md | 2026-03-17 |
| OpenSpec OPSX workflow docs | github.com/Fission-AI/OpenSpec/blob/main/docs/opsx.md | 2026-03-17 |
| OpenSpec getting started | github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md | 2026-03-17 |
| CALM specification | github.com/finos/architecture-as-code | 2026-03-10 |
| NovaTrek CALM integration plan | docs/CALM-INTEGRATION-PLAN.md | 2026-03-17 |
| NovaTrek CALM research summary | /memories/repo/calm-research-summary.md | 2026-03-17 |
