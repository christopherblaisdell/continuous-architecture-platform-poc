# OpenSpec Evaluation Plan for NovaTrek Continuous Architecture Platform

**Date**: 2026-03-17
**Status**: Proposed
**Prerequisites**: Review of [OPENSPEC-CALM-ANALYSIS.md](OPENSPEC-CALM-ANALYSIS.md) and approval of Option D (Time-Boxed PoC)
**Estimated effort**: 1 development session (single architecture scenario)

---

## 1. Objective

Run a controlled evaluation of OpenSpec alongside the existing CALM-based architecture workflow to determine whether OpenSpec adds measurable value for:
- AI agent workflow guidance
- Behavioral specification capture
- Change tracking and delta management
- Multi-tool portability

---

## 2. Pre-Conditions

Before starting the PoC:

- [ ] Read deep research results (after running the deep research prompt from [DEEP-RESEARCH-PROMPT-OPENSPEC-CALM-COMPARISON.md](DEEP-RESEARCH-PROMPT-OPENSPEC-CALM-COMPARISON.md))
- [ ] Review analysis and confirm Option D is still the right approach
- [ ] Identify a suitable NTK ticket for the evaluation (ideally a new ticket that would normally go through the solution design workflow)

---

## 3. Phase 1: Installation and Setup

### 3.1 Install OpenSpec

```bash
npm install -g @fission-ai/openspec@latest
```

### 3.2 Initialize in Workspace

```bash
cd /Users/christopherblaisdell/Documents/continuous-architecture-platform-poc-2
openspec init
```

### 3.3 Create Custom Schema

Create a custom schema that maps to NovaTrek's architecture workflow. This is the critical integration point.

```bash
openspec schema init novatrek-architecture
```

Proposed schema mapping:

```yaml
# openspec/schemas/novatrek-architecture/schema.yaml
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

### 3.4 Create Project Configuration

```yaml
# openspec/config.yaml
schema: novatrek-architecture

context: |
  NovaTrek Adventures is a fictional adventure tourism platform with 19
  microservices across 9 bounded domains. Architecture decisions follow
  MADR format. API contracts are defined in OpenAPI YAML specs under
  architecture/specs/. System topology is modeled in CALM JSON under
  architecture/calm/. All architecture work is ticket-driven (NTK-XXXXX).

rules:
  requirements:
    - Source requirements from JIRA ticket (mock tool) first
    - Include ticket ID (NTK-XXXXX) in the document title
    - Cross-reference with capability model in architecture/metadata/capabilities.yaml
  specs:
    - Use Given/When/Then format for all scenarios
    - Use RFC 2119 keywords (SHALL, MUST, SHOULD, MAY)
    - Organize by affected service domain
    - Reference OpenAPI spec paths where applicable
  decisions:
    - Use MADR format (Status, Date, Context, Decision Drivers, Options, Outcome, Consequences)
    - Require at minimum 2 genuinely considered options
    - Tie decision outcome to decision drivers
    - Include Positive, Negative, and Neutral consequences
  impacts:
    - Create one impact file per affected service
    - Focus on WHAT changes (API contracts, data models, integration points)
    - Do NOT include implementation code or deployment steps
  risks:
    - Assess ISO 25010 quality attributes (reliability, maintainability, compatibility at minimum)
    - Include mitigation strategies for each risk
```

### 3.5 Configure OpenSpec for Copilot

Verify that `openspec init` generated compatible skill/instruction files for GitHub Copilot. Check:

```bash
ls -la .github/copilot/skills/openspec-*/ 2>/dev/null || echo "Check OpenSpec docs for Copilot integration path"
```

---

## 4. Phase 2: Parallel Execution

### 4.1 Select Test Ticket

Choose an NTK ticket that:
- Touches at least 2 services (cross-domain preferred)
- Requires API contract changes
- Has clear behavioral requirements
- Has not been started yet

Candidates (check tickets.yaml for current status):
- Any "New" status ticket that involves cross-service changes

### 4.2 Execute Solution Design — Traditional Workflow

Run the ticket through the existing solution design workflow as documented in copilot-instructions.md:

1. Create branch `solution/NTK-XXXXX-slug`
2. Create folder structure under `architecture/solutions/_NTK-XXXXX-slug/`
3. Execute mock tools (JIRA, Elastic, GitLab)
4. Create requirements, analysis, decisions, impacts, risks, user stories
5. Update capability-changelog.yaml
6. Run portal generators

Record:
- Number of AI prompts required
- Quality of AI output (did the agent follow the workflow correctly?)
- Time from start to complete solution design
- Artifact completeness (did all required sections get populated?)

### 4.3 Execute Solution Design — OpenSpec Workflow

On a separate branch, run the SAME ticket through the OpenSpec workflow:

1. Create branch `solution/NTK-XXXXX-slug-openspec`
2. Run `/opsx:propose NTK-XXXXX-description`
3. Let OpenSpec create artifacts according to the custom schema
4. Use `/opsx:continue` or `/opsx:ff` to build out all artifacts
5. Compare the generated artifacts against the traditional workflow output

Record:
- Number of AI prompts required
- Quality of AI output (did the agent produce architecture-quality artifacts?)
- Time from start to complete solution design
- Artifact completeness (did the custom schema capture all necessary information?)
- Delta spec quality (was the behavioral diff clear and useful?)

---

## 5. Phase 3: Evaluation

### 5.1 Comparison Criteria

| Criterion | Traditional Workflow | OpenSpec Workflow | Winner |
|-----------|---------------------|-------------------|--------|
| **AI guidance quality** | Did the agent follow instructions correctly? | Did the slash commands produce better-structured output? | |
| **Artifact completeness** | Were all required artifacts populated? | Did the custom schema capture all architecture needs? | |
| **Behavioral spec quality** | How well were requirements captured? | Did Given/When/Then scenarios improve clarity? | |
| **Change reviewability** | How easy is the solution to review? | Do delta specs improve review experience? | |
| **Workflow portability** | Copilot-specific instructions | Would this work with other AI tools? | |
| **CALM integration** | Direct — CALM is already integrated | Did OpenSpec conflict with or complement CALM? | |
| **Overhead** | Familiar workflow, no additional tooling | Was the OpenSpec overhead justified? | |
| **Missing artifacts** | N/A (purpose-built for architecture) | What was lost vs. gained? | |

### 5.2 Decision Gate

Based on the evaluation, decide:

- **Adopt (Option B)**: OpenSpec adds measurable value across 4+ criteria AND the custom schema accommodates all NovaTrek artifact needs -> proceed to integration plan
- **Defer**: OpenSpec shows promise but custom schema needs work or team workspace features are needed -> revisit when OpenSpec releases workspace features
- **Reject (Option A)**: OpenSpec does not add sufficient value over the existing workflow, or creates source-of-truth conflicts with CALM -> continue CALM-only path

---

## 6. Phase 4: Integration (Conditional — only if PoC passes decision gate)

### 6.1 Workflow Integration

If adopted, OpenSpec would slot into the existing workflow as follows:

```
Ticket received (NTK-XXXXX)
    │
    ▼
/opsx:propose (creates change with NovaTrek schema)
    │
    ├── requirements.md ──── Sources from mock JIRA
    ├── specs/ ──────────── Behavioral contracts (Given/When/Then)
    ├── decisions.md ────── MADR format (from custom template)
    ├── impacts/ ────────── Per-service impact assessments
    ├── risks.md ────────── ISO 25010 quality analysis
    └── tasks.md ────────── Implementation checklist
    │
    ▼
CALM validation (CI)
    │
    ├── Topology validation (generate-calm.py + validate-calm.py)
    ├── OpenSpec verification (/opsx:verify or openspec validate)
    └── Portal generation (generate-all.sh)
    │
    ▼
/opsx:archive (merge behavioral deltas into main specs)
    │
    ▼
Update capability-changelog.yaml
Run portal generators
```

### 6.2 File System Layout

```
openspec/
├── specs/                           # Behavioral source of truth
│   ├── operations/spec.md           # svc-check-in, svc-scheduling-orchestrator
│   ├── guest-identity/spec.md       # svc-guest-profiles
│   ├── booking/spec.md              # svc-reservations
│   ├── product-catalog/spec.md      # svc-trip-catalog, svc-trail-management
│   ├── safety/spec.md               # svc-safety-compliance
│   ├── logistics/spec.md            # svc-transport-logistics, svc-gear-inventory
│   ├── guide-management/spec.md     # svc-guide-management
│   ├── external/spec.md             # svc-partner-integrations
│   └── support/spec.md              # 8 support services
├── changes/                         # Active work
│   └── NTK-XXXXX-slug/
│       ├── requirements.md
│       ├── analysis.md
│       ├── decisions.md
│       ├── impacts/
│       ├── risks.md
│       ├── tasks.md
│       └── specs/                   # Delta specs
└── config.yaml

architecture/
├── calm/                            # Structural source of truth (unchanged)
│   ├── novatrek-topology.json
│   ├── domains/
│   ├── patterns/
│   └── controls/
├── metadata/                        # Metadata YAML (unchanged)
├── specs/                           # OpenAPI specs (unchanged)
├── events/                          # AsyncAPI specs (unchanged)
└── solutions/                       # Legacy solutions (preserved, read-only)
```

### 6.3 Source-of-Truth Boundaries

| Concern | Source of Truth | Location |
|---------|---------------|----------|
| System topology | CALM | `architecture/calm/` |
| API contracts | OpenAPI specs | `architecture/specs/` |
| Event schemas | AsyncAPI specs | `architecture/events/` |
| Behavioral requirements | OpenSpec specs | `openspec/specs/` |
| Architecture decisions | MADR ADRs | `decisions/` (global) |
| Capability model | Capability YAML | `architecture/metadata/capabilities.yaml` |
| Capability changes | Capability changelog | `architecture/metadata/capability-changelog.yaml` |
| Service metadata | Metadata YAML | `architecture/metadata/` |
| Active solution work | OpenSpec changes | `openspec/changes/` |

### 6.4 CI Pipeline Updates

Add to `.github/workflows/validate-solution.yml`:

```yaml
- name: Validate OpenSpec specs
  run: |
    npx openspec validate || true  # Non-blocking during pilot
```

---

## 7. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Custom schema cannot accommodate all NovaTrek artifacts | Medium | High | Test in PoC before committing; fall back to Option A |
| OpenSpec updates break custom schema | Medium | Medium | Pin OpenSpec version; test updates in CI |
| Fission AI abandons OpenSpec | Low | High | MIT license; fork-able; evaluate governance trajectory in deep research |
| Behavioral specs drift from OpenAPI contracts | Medium | Medium | Add CI check comparing OpenSpec specs against OpenAPI endpoints |
| Team confusion about artifact locations | Medium | Medium | Clear source-of-truth table; documentation in copilot-instructions.md |
| Additional npm dependency in architecture workspace | Low | Low | Isolate to dev dependency; not required for production services |

---

## 8. Success Criteria

The PoC is successful if:

1. The custom OpenSpec schema produces all artifacts the traditional workflow produces, with equivalent or better quality
2. AI agent guidance quality improves measurably (fewer corrections, better artifact structure)
3. Delta specs provide review-time value that narrative analysis does not
4. The CALM + OpenSpec integration does not create source-of-truth conflicts
5. The overhead (learning curve, additional files, npm dependency) is justified by the workflow improvement

---

## 9. Timeline

| Step | Action | Dependency |
|------|--------|-----------|
| 1 | Run deep research prompt | None |
| 2 | Review deep research results | Step 1 |
| 3 | Confirm Option D (PoC) | Step 2 |
| 4 | Install OpenSpec and create custom schema | Step 3 |
| 5 | Select test ticket | Step 3 |
| 6 | Execute parallel workflows | Steps 4, 5 |
| 7 | Evaluate results against criteria | Step 6 |
| 8 | Decision gate: Adopt / Defer / Reject | Step 7 |
| 9 | (Conditional) Integration implementation | Step 8 = Adopt |
