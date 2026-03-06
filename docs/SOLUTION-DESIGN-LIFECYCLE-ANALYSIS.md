# NovaTrek Adventures — Solution Design Lifecycle Analysis and Integration Plan

| | |
|-----------|-------|
| **Author** | Christopher Blaisdell |
| **Date** | 2026-03-06 |
| **Status** | Proposed |
| **Purpose** | Define how solution designs are created, source-controlled, published, and rolled up to business capabilities so that architectural knowledge accumulates over time instead of being lost when tickets close |
| **Companion Documents** | [CAPABILITY-MAP-ANALYSIS.md](CAPABILITY-MAP-ANALYSIS.md), [TICKETING-INTEGRATION-ANALYSIS.md](TICKETING-INTEGRATION-ANALYSIS.md) |

---

## 1. The Problem: Solution Designs Have No Home After Tickets Close

The NovaTrek architecture practice produces valuable solution design artifacts for every ticket. A single ticket like NTK-10003 generates:

- A master solution design document (`NTK-10003-solution-design.md`)
- A ticket requirements report (`1.requirements/NTK-10003.ticket.report.md`)
- A plain-language explanation (`2.analysis/simple.explanation.md`)
- Per-service impact assessments (`3.solution/i.impacts/impact.1/impact.1.md` through `impact.4/`)
- Architecture decisions in MADR format (`3.solution/d.decisions/decisions.md`)
- User stories with acceptance criteria (`3.solution/u.user.stories/user-stories.md`)
- Assumptions (`3.solution/a.assumptions/assumptions.md`)
- Risks (`3.solution/r.risks/risks.md`)
- Implementation guidance (`3.solution/g.guidance/guidance.md`)
- PlantUML diagrams and rendered SVGs (`3.solution/i.impacts/impact.1/*.puml`, `*.svg`)

This is a rich, well-structured body of architectural knowledge. But today it has three fatal problems:

1. **It is invisible.** Solution designs live in deep ticket folder paths (`phases/phase-1-ai-tool-cost-comparison/workspace/work-items/tickets/_NTK-10003-unregistered-guest-self-checkin/`) that no one navigates to after the ticket closes. They are not published to the portal, not indexed, not searchable.

2. **It is disconnected.** The solution design for NTK-10003 describes changes to svc-check-in, svc-guest-profiles, svc-reservations, and svc-safety-compliance — but the microservice pages in the portal have no knowledge of these solutions. The ADRs created inside the ticket folder exist separately from the global ADR log in `decisions/`. The capability map has no record of what NTK-10003 contributed.

3. **It does not accumulate.** When the next architect picks up a check-in ticket, they start from the OpenAPI spec and microservice page. They have no way to discover that NTK-10003 already solved a similar problem, created ADR-006 through ADR-008, and established patterns for temporary guest profiles. The architecture resets instead of growing.

The result is **architecture amnesia** — valuable design decisions, impact analyses, and architectural patterns are produced, reviewed, approved, and then functionally forgotten.

---

## 2. What We Have Today

### 2.1 Solution Design Templates

The practice has two solution design templates, serving different purposes:

**Template A — Phase 1 Workspace Template** (`phases/.../workspace/.ai-instructions/standards/solution-design-template.md`):
A lightweight template optimized for AI agent execution. Flat structure with sections for problem statement, current state, API/data/service changes, sequence diagrams, risks, acceptance criteria, and NFRs. Designed for the AI to fill in during Phase 1 scenario evaluation.

**Template B — NovaTrek Solution Design Template** (`portal/docs/standards/solution-design/solution-design-template.md`):
A comprehensive, production-grade template with component architecture diagrams, per-component modification sections with sequence diagrams, structured assumptions/decisions/risks tables with status tracking, optional sections for requirements, guidance, and security. Designed for manual or AI-assisted architect use in a real practice.

Both templates produce Markdown files. Both expect PlantUML diagrams. Neither template currently includes capability mapping or rollup metadata.

### 2.2 Solution Design Folder Structure

The Phase 1 workspace uses a structured folder convention per ticket:

```
work-items/tickets/_NTK-XXXXX-slug/
├── NTK-XXXXX-solution-design.md          # Master document
├── 1.requirements/
│   └── NTK-XXXXX.ticket.report.md        # Ticket description + acceptance criteria
├── 2.analysis/
│   └── simple.explanation.md             # Plain-language summary
└── 3.solution/
    ├── a.assumptions/
    │   └── assumptions.md                # Assumptions register
    ├── d.decisions/
    │   └── decisions.md                  # ADRs (MADR format)
    ├── g.guidance/
    │   └── guidance.md                   # Implementation guidance (HOW)
    ├── i.impacts/
    │   ├── impact.1/
    │   │   ├── impact.1.md               # Service impact assessment
    │   │   ├── *.puml                    # Sequence diagram source
    │   │   └── *.svg                     # Rendered diagram
    │   ├── impact.2/
    │   ├── impact.3/
    │   └── impact.4/
    ├── r.risks/
    │   └── risks.md                      # Risk register
    └── u.user.stories/
        └── user-stories.md               # User stories + acceptance criteria
```

This is a well-thought-out decomposition that enforces the content separation policy: impacts describe WHAT changes, guidance describes HOW to implement, decisions describe WHY, user stories describe WHO benefits. The structure scales from simple tickets (1 impact file) to complex cross-service changes (4+ impact files).

### 2.3 What the Portal Publishes Today

The NovaTrek Architecture Portal currently publishes:

| Section | Content | Generated From |
|---------|---------|---------------|
| Design Standards | arc42, C4, MADR, ADR templates, ISO 25010 quality tree | Static Markdown in `portal/docs/standards/` |
| Service Catalog | Summary table of all 21 services | `architecture/metadata/microservices.yaml` |
| Applications | 3 app pages + wireframes | `architecture/metadata/applications.yaml` |
| Microservice Pages | 21 deep-dive pages with sequence diagrams | OpenAPI specs + `generate-microservice-pages.py` |
| Event Catalog | Domain event schemas | `architecture/events/` |
| Actor Catalog | System actors | `architecture/metadata/actors.yaml` |
| Global Decisions | 11 ADRs (ADR-001 through ADR-011) | Static Markdown in `decisions/` |

**Not published:**
- Solution designs (zero visibility)
- Ticket-scoped ADRs (buried inside ticket folders)
- Impact assessments (buried inside ticket folders)
- User stories (buried inside ticket folders)
- Capability map (planned, not yet built — see CAPABILITY-MAP-ANALYSIS.md)
- Ticket index (planned, not yet built — see TICKETING-INTEGRATION-ANALYSIS.md)

---

## 3. Vision: Solution Designs as First-Class Architecture Artifacts

The goal is a system where:

1. **Every solution design is published** to the portal with its own page, cross-linked to the services it impacts, the capabilities it touches, and the decisions it produced
2. **Solution designs are source-controlled** in a canonical location within the architecture repository — not buried inside phase-specific workspace paths
3. **Architects can create solution designs manually or with AI assistance**, using the same template and folder structure regardless of authoring method
4. **Completed solutions roll up to capabilities** so that the capability map grows richer with every ticket, and future architects can see the full history of how a capability evolved
5. **ADRs created inside tickets are promoted** to the global decision log, maintaining traceability back to the originating ticket and solution design
6. **The AI agent is aware of all prior solutions** and can reference them when working on new tickets, detecting patterns, conflicts, and opportunities to reuse existing designs

This is what makes architecture **continuous** — knowledge produced during solutioning feeds back into the platform, making every subsequent design richer and more informed than the last.

---

## 4. Source Control Strategy: Where Solution Designs Live

### 4.1 The Problem with the Current Location

Solution designs currently live at:

```
phases/phase-1-ai-tool-cost-comparison/workspace/work-items/tickets/_NTK-XXXXX-slug/
```

This path is phase-specific and deeply nested. It made sense for Phase 1 evaluation but is not a sustainable home for architecture artifacts. When Phase 2 begins, where do new solutions go? Into a `phase-2/` folder? The path structure implies transience — these are work products of a specific evaluation phase, not permanent architecture records.

### 4.2 Proposed Location: `architecture/solutions/`

Move solution designs into the architecture source directory, alongside the other architect-maintained source artifacts:

```
architecture/
├── diagrams/              # PlantUML diagrams (existing)
├── events/                # AsyncAPI event specs (existing)
├── metadata/              # YAML metadata files (existing)
├── specs/                 # OpenAPI specs (existing)
├── wireframes/            # Excalidraw wireframes (existing)
└── solutions/             # NEW: Solution designs
    ├── _NTK-10001-add-elevation-to-trail-response/
    │   ├── NTK-10001-solution-design.md
    │   ├── 1.requirements/
    │   ├── 2.analysis/
    │   └── 3.solution/
    ├── _NTK-10002-adventure-category-classification/
    ├── _NTK-10003-unregistered-guest-self-checkin/
    ├── _NTK-10004-guide-schedule-overwrite-bug/
    └── _NTK-10005-wristband-rfid-field/
```

**Why `architecture/solutions/`:**

- Follows the established convention of `architecture/` as the source directory for all architect-maintained artifacts
- Solution designs are architecture artifacts — same as specs, events, and wireframes
- Survives across phases — no phase-specific path contamination
- Natural discovery — `ls architecture/solutions/` shows all solutions at a glance
- Git history tracks the full lifecycle of every solution design

**Naming convention:** `_TICKET-ID-kebab-case-slug/` — the underscore prefix groups solution folders visually and matches the existing Phase 1 convention.

### 4.3 Branching Strategy: One Branch per Solution Design

Every solution design MUST be developed on a dedicated Git branch and delivered through a pull request. This is not optional process overhead — it is the mechanism that makes architecture review, portal integrity, and concurrent work possible.

#### Why Branch per Solution

| Concern | How Branching Addresses It |
|---------|---------------------------|
| **Review gate** | The PR IS the architecture review. The reviewer applies the checklist (Section 8.3) directly on the PR. No separate review meeting or email approval needed unless the team chooses to add one. |
| **Portal integrity** | Only `main` is published. Draft solutions on branches are invisible to the portal. Stakeholders never see half-finished designs. |
| **Concurrent architects** | Multiple architects (human or AI) can work on separate solutions simultaneously without stepping on each other. Two architects modifying `capabilities.yaml` in the same sprint will see the conflict at merge time, not at commit time. |
| **Atomic delivery** | The solution folder, metadata updates (capabilities.yaml, capability-changelog.yaml, cross-service-calls.yaml), and promoted ADRs are all in one PR. They are reviewed together and merged together. No orphaned metadata. |
| **CI validation** | The branch CI runs generators, validates YAML syntax, builds the portal preview, and catches broken cross-links BEFORE merge. A broken diagram or malformed capability ID never reaches main. |
| **Auditability** | Git log on `main` shows clean, approved merges. The PR conversation captures review comments, requested changes, and approval rationale. This is the architecture governance audit trail. |
| **AI workflow alignment** | An AI agent can produce a complete solution on a branch. The human architect reviews the AI's output in the PR diff, adjusts what is needed, and approves — the same workflow as reviewing a human architect's work. |
| **Rollback safety** | If a merged solution turns out to be wrong, reverting the merge commit cleanly removes the solution, its metadata, and its portal pages. No manual cleanup across scattered files. |

#### Why NOT Alternative Approaches

| Alternative | Why It Fails |
|-------------|--------------|
| **Working directly on main** | No review gate. Draft content published immediately. Multiple architects overwriting each other's changes. Capability metadata updated without review. |
| **Long-lived feature branches** | Over-engineering. Solution designs are focused, bounded work — they should merge within days, not weeks. Long-lived branches diverge from main and create painful merge conflicts. |
| **Branch per artifact** (one PR for impacts, another for decisions, another for metadata) | Breaks the review context. The reviewer needs to see the complete solution — impacts, decisions, capability mapping, and metadata updates — as a coherent whole. Splitting across PRs makes review fragmented and error-prone. |
| **No branches, use a "review" status field** | Status fields in documents are not enforceable. Nothing prevents someone from deploying a DRAFT solution to the portal. Git branch protections are enforceable. |

#### Branch Naming Convention

```
solution/NTK-XXXXX-kebab-slug
```

Examples:
- `solution/NTK-10003-unregistered-guest-self-checkin`
- `solution/NTK-10005-wristband-rfid-field`
- `solution/NTK-10008-group-booking-capacity`

The `solution/` prefix groups solution branches visually in `git branch --list 'solution/*'` and distinguishes them from other branch types (e.g., `feature/`, `fix/`, `infra/`).

#### Branch Protection Rules

Configure branch protection on `main` to enforce the review gate:

| Rule | Setting | Rationale |
|------|---------|-----------|
| Require pull request before merge | Yes | No direct pushes to main for `architecture/solutions/` or `architecture/metadata/` paths |
| Required reviewers | 1 (minimum) | At least one architect reviews every solution |
| Require status checks | Yes — YAML validation, portal build | CI catches broken metadata and diagrams before merge |
| Require conversation resolution | Yes | All review comments must be resolved |
| Require linear history | Recommended (squash merge) | Each solution is a single commit on main — clean history, easy revert |

#### The Full Branch Lifecycle

```
1. Ticket assigned to architect
   │
2. Architect creates branch:
   │  git checkout -b solution/NTK-XXXXX-slug
   │
3. Architect creates solution folder on the branch:
   │  architecture/solutions/_NTK-XXXXX-slug/
   │  ├── NTK-XXXXX-solution-design.md
   │  ├── 1.requirements/
   │  ├── 2.analysis/
   │  └── 3.solution/ (impacts, decisions, capabilities, etc.)
   │
4. Architect updates architecture metadata on the same branch:
   │  ├── architecture/metadata/capabilities.yaml (new L3 entries)
   │  ├── architecture/metadata/capability-changelog.yaml (new entry)
   │  ├── architecture/metadata/cross-service-calls.yaml (if new integrations)
   │  └── decisions/ADR-NNN-*.md (promoted ADRs)
   │
5. Architect pushes branch, opens pull request:
   │  PR title: "NTK-XXXXX: [Solution Name]"
   │  PR description: Links to ticket, lists capabilities touched,
   │                  lists services impacted
   │
6. CI runs on the PR:
   │  ├── Validate YAML syntax (capabilities.yaml, changelog, etc.)
   │  ├── Run portal generators (solution pages, capability pages)
   │  ├── Build MkDocs portal
   │  └── Report: "Portal builds successfully with this solution"
   │
7. Reviewer applies architecture review checklist (Section 8.3):
   │  ├── Completeness — all required artifacts present?
   │  ├── Capability rollup — capabilities declared and changelog drafted?
   │  ├── Content separation — impacts describe WHAT, decisions describe WHY?
   │  ├── Metadata consistency — YAML changes match the solution?
   │  └── Backward compatibility — API changes non-breaking?
   │
8. PR approved → squash merge to main
   │
9. Main CI triggers:
   │  ├── Run all generators
   │  ├── Build portal
   │  └── Deploy to Azure Static Web Apps
   │
10. Solution is published, indexed, cross-linked, and rolled up to capabilities
    └── The architecture is now richer than before this ticket
```

#### Solution Design Status Mapping

The solution design `Status` field in the master document header maps directly to the branch/PR state:

| Status | Git State | Portal Visibility |
|--------|-----------|-------------------|
| DRAFT | Branch exists, no PR yet | Not published |
| IN REVIEW | PR open, reviewers assigned | Not published (preview available via CI) |
| CHANGES REQUESTED | PR has requested changes | Not published |
| APPROVED | PR approved, ready to merge | Not published (until merged) |
| IMPLEMENTED | PR merged to main | Published on portal |
| SUPERSEDED | A later solution replaces this one | Published with superseded banner |

The status field is updated as the last step before each state transition — but the **enforceable** gate is the PR state, not the status field. A solution cannot reach the portal without passing through PR review and merge, regardless of what its status field says.

#### Handling Concurrent Solutions That Touch the Same Metadata

When two architects are working on solutions that both modify `capabilities.yaml` or `capability-changelog.yaml`:

1. **Git handles it naturally.** If the changes are to different lines (different capabilities), Git merges automatically.
2. **If there is a true conflict** (both solutions add the same L3 capability, or both modify the same changelog entry), Git reports a merge conflict on the second PR.
3. **The second architect resolves the conflict** by rebasing their branch on the updated main, reviewing the first solution's changes, and adjusting their metadata to be additive rather than overwriting.
4. **This is a feature, not a bug.** The merge conflict forces the second architect to be aware of the first solution's changes. This is exactly the "conflict detection" that prevents architecture drift.

#### When to Skip Branching

Branching is required for solution designs and their metadata. It is NOT required for:

- Typo fixes in portal content
- Minor YAML corrections (e.g., fixing a malformed field)
- Template updates (standards are infrastructure, not deliverables)
- Generator script changes (code, not architecture artifacts)

These can go directly to main via a lightweight commit, unless branch protection rules require PRs for all changes.

---

## 5. The Enhanced Solution Design Template

The existing NovaTrek solution design template (Section 2.1, Template B) is a strong foundation. It needs three additions to support the continuous architecture lifecycle:

### 5.1 Capability Mapping Section

Add after the Component Architecture section:

```markdown
## Capability Mapping

This section declares which business capabilities (from `architecture/metadata/capabilities.yaml`) 
this solution touches and how. These declarations drive the capability rollup — connecting this 
ticket's work to the long-term architecture evolution.

### Capabilities Modified

| Capability ID | Capability Name | Impact Type | Description |
|--------------|----------------|-------------|-------------|
| CAP-X.Y | [Name] | EXTENDS | [What new behavior is added] |
| CAP-X.Y | [Name] | MODIFIES | [What existing behavior changes] |

### Capabilities Depended Upon (Read-Only)

| Capability ID | Capability Name | Usage |
|--------------|----------------|-------|
| CAP-X.Y | [Name] | [How this capability is consumed] |

### New L3 Capabilities Introduced

| Parent | L3 ID | L3 Name | Description |
|--------|-------|---------|-------------|
| CAP-X.Y | CAP-X.Y.Z | [Name] | [What this new capability does] |

**Impact Types:**
- **EXTENDS** — Adds new behavior to an existing capability (new flow, new endpoint)
- **MODIFIES** — Changes existing behavior (schema change, logic change)
- **CREATES** — Introduces a new L2 or L3 capability
- **DEPENDS** — Uses the capability read-only (no changes)
- **DEPRECATES** — Phases out a capability or sub-capability
```

### 5.2 Solution Metadata Header Extension

Extend the master document header table to include capability and lifecycle metadata:

```markdown
| | |
|-----------|-------|
| **Solution Architect** | [Architect Name] |
| **Solution Name** | [Descriptive Solution Name] |
| **Ticket** | [TICKET-ID] |
| **Capabilities** | CAP-X.Y (extends), CAP-X.Y (modifies) |
| **Status** | DRAFT / IN REVIEW / APPROVED / IMPLEMENTED / SUPERSEDED |
| **Impacted Services** | [svc-xxx, svc-yyy] |
| **Related ADRs** | ADR-NNN, ADR-NNN |
| **Supersedes** | [TICKET-ID] (if this replaces a prior solution) |
```

### 5.3 Capability Changelog Entry

Add as the final section, to be completed when the solution is approved:

```markdown
## Capability Changelog Entry

Copy this YAML block into `architecture/metadata/capability-changelog.yaml` when this 
solution is approved:

```yaml
- ticket: [TICKET-ID]
  date: YYYY-MM-DD
  status: APPROVED
  capabilities:
    - id: CAP-X.Y
      impact: extends
      summary: "[One-line description of what changed]"
      l3_added:
        - id: CAP-X.Y.Z
          name: "[L3 capability name]"
  services_impacted:
    - svc-xxx
    - svc-yyy
  decisions:
    - ADR-NNN-short-title
```
```

These three additions transform the solution design from a point-in-time document into a **traceable architecture artifact** that feeds back into the platform.

---

## 6. The Solution Design Artifact Model

A solution design is not a single file — it is a **composed document** assembled from a structured set of artifacts. Each artifact type has a specific purpose, audience, and content boundary.

### 6.1 Artifact Catalog

This table defines every artifact type that can appear in a solution design, its role, and its content boundary:

| Artifact | Location | Audience | Describes | Does NOT Describe |
|----------|----------|----------|-----------|-------------------|
| **Master Document** | `NTK-XXXXX-solution-design.md` | All stakeholders | End-to-end solution overview with component architecture | Implementation code, deployment steps |
| **Ticket Report** | `1.requirements/NTK-XXXXX.ticket.report.md` | Architects, PMs | Original requirements, acceptance criteria, business context | Solutions, architecture decisions |
| **Simple Explanation** | `2.analysis/simple.explanation.md` | Non-technical stakeholders | What the problem is and what changes, in plain language | Technical details, code references |
| **Assumptions** | `3.solution/a.assumptions/assumptions.md` | Architects, reviewers | What is assumed true but not verified — WHAT and WHY | Decisions (assumptions inform decisions) |
| **Decisions** | `3.solution/d.decisions/decisions.md` | Architecture governance | WHY this approach — MADR format with options analysis | Implementation code, deployment steps |
| **Guidance** | `3.solution/g.guidance/guidance.md` | Development teams | HOW to implement — code patterns, config, test examples | Business justification, architecture rationale |
| **Impact Assessments** | `3.solution/i.impacts/impact.N/impact.N.md` | Service owners, architects | WHAT changes per service — API, schema, integration changes | Why the change was chosen (that is in decisions) |
| **Risks** | `3.solution/r.risks/risks.md` | Architecture governance | What could go wrong and how risks are mitigated | Implementation-level mitigation (that is in guidance) |
| **User Stories** | `3.solution/u.user.stories/user-stories.md` | PMs, business analysts | WHO benefits and WHY — user perspective | Technical implementation details |
| **Capability Mapping** | `3.solution/c.capabilities/capabilities.md` | Architecture practice | Which capabilities this solution touches and how | Implementation details |
| **Sequence Diagrams** | `3.solution/i.impacts/impact.N/*.puml` | Architects, developers | Runtime flow for new/modified interactions | Static structure (that is in component diagrams) |
| **Component Diagrams** | `3.solution/00.component.diagram.puml` | All stakeholders | System-level view of affected components | Runtime sequences (that is in sequence diagrams) |

### 6.2 Required vs. Optional Artifacts

Not every ticket needs every artifact. The practice distinguishes between mandatory and optional artifacts:

| Artifact | When Required |
|----------|--------------|
| Master Document | Always |
| Ticket Report | Always |
| Simple Explanation | Always (even for simple changes — it is 1-2 paragraphs) |
| Capability Mapping | Always (even if only `DEPENDS` references — forces the architect to think about capability impact) |
| Impact Assessments | When any service API, schema, or integration changes |
| Decisions | When multiple approaches were considered (minimum 2 options) |
| Assumptions | When the solution depends on conditions not yet verified |
| Risks | When there is non-trivial risk of failure, data loss, or backward incompatibility |
| User Stories | When the change is user-facing or affects a user workflow |
| Guidance | Optional — only when the architect wants to provide implementation advice |
| Sequence Diagrams | When the solution involves multi-service orchestration or complex flows |
| Component Diagrams | When 3+ services are impacted or a new service is introduced |

### 6.3 Content Separation Enforcement

The content separation policy is the most important quality standard for solution designs. It prevents the common failure mode where everything is jammed into one long document with blurred boundaries.

**The rule:** Each artifact answers exactly ONE question. If you find yourself explaining WHY in an impact file, move that content to a decision. If you find yourself writing code in a decision, move it to guidance. If you find HOW leaks into a risk, move it to guidance.

| Question | Answer Lives In |
|----------|----------------|
| What does the ticket ask for? | Ticket Report |
| What does this mean in simple terms? | Simple Explanation |
| What is assumed to be true? | Assumptions |
| What changes per service? | Impact Assessments |
| Why was this approach chosen? | Decisions |
| How should it be implemented? | Guidance |
| What could go wrong? | Risks |
| Who benefits and why? | User Stories |
| Which capabilities are affected? | Capability Mapping |

---

## 7. Publishing Solution Designs to the Portal

### 7.1 Portal Section: Solution Designs

Add a new top-level navigation section to the NovaTrek Architecture Portal:

```yaml
nav:
  - Home: index.md
  - Design Standards:
    - standards/index.md
    - Solution Design Template: standards/solution-design/solution-design-template.md
    # ... existing arc42, C4, MADR, etc.
  - Service Catalog: services/index.md
  - Solution Designs:                              # NEW
    - solutions/index.md
    # Per-solution pages generated by the generator
  - Business Capabilities: capabilities/index.md   # From CAPABILITY-MAP-ANALYSIS.md
  - User Stories: tickets/index.md                 # From TICKETING-INTEGRATION-ANALYSIS.md
  - Applications: ...
  - Microservice Pages: ...
  - Event Catalog: events/index.md
  - Actor Catalog: actors/index.md
```

### 7.2 Solution Design Index Page

The generator produces `portal/docs/solutions/index.md` containing:

**Summary Dashboard:**

| Metric | Value |
|--------|-------|
| Total Solutions | 5 |
| APPROVED | 3 |
| IN REVIEW | 1 |
| DRAFT | 1 |
| Services Impacted | 8 (of 21) |
| Capabilities Touched | 6 (of 34) |

**Solution Table (sortable, filterable):**

| Ticket | Solution Name | Status | Services | Capabilities | Architect | Date |
|--------|--------------|--------|----------|-------------|-----------|------|
| NTK-10001 | Add Elevation Data to Trail Response | APPROVED | svc-trail-management | CAP-4.2 | Morgan Rivera | 2026-01-10 |
| NTK-10002 | Adventure Category Classification | APPROVED | svc-check-in, svc-trip-catalog | CAP-2.1, CAP-1.2 | Alex Chen | 2026-01-20 |
| NTK-10003 | Unregistered Guest Self-Check-In | APPROVED | svc-check-in, svc-guest-profiles, svc-reservations, svc-safety-compliance | CAP-2.1, CAP-1.1, CAP-1.3, CAP-3.1 | Alex Chen | 2026-02-20 |

**Filter Views:**
- By service: "Show all solutions affecting svc-check-in"
- By capability: "Show all solutions touching CAP-2.1 (Check-In)"
- By status: "Show all APPROVED solutions"
- By architect: "Show all solutions by Alex Chen"

### 7.3 Per-Solution Pages

Each solution gets a dedicated portal page at `portal/docs/solutions/NTK-XXXXX.md`. The generator composes this page by reading the solution folder structure and assembling the content:

```markdown
# NTK-10003 — Unregistered Guest Self-Service Check-In

## Solution Overview
[Content from the master document's Overview section]

## Component Architecture
[Component diagram embedded as SVG/object tag]
[Affected components table from master document]

## Capability Mapping
[Content from 3.solution/c.capabilities/capabilities.md]
[Deep links to capability pages in the portal]

## Service Impacts
### svc-check-in
[Content from 3.solution/i.impacts/impact.1/impact.1.md]
[Sequence diagram embedded from impact.1/*.svg]
[Deep link to svc-check-in microservice page]

### svc-guest-profiles
[Content from 3.solution/i.impacts/impact.2/impact.2.md]
[Deep link to svc-guest-profiles microservice page]

## Architecture Decisions
[Content from 3.solution/d.decisions/decisions.md]
[Links to promoted ADRs in the global decision log]

## User Stories
[Content from 3.solution/u.user.stories/user-stories.md]

## Assumptions
[Content from 3.solution/a.assumptions/assumptions.md]

## Risks
[Content from 3.solution/r.risks/risks.md]

## Plain-Language Summary
[Content from 2.analysis/simple.explanation.md]
```

The generator does not modify the source files — it reads them and composes a single publishable page. This means the architect maintains the decomposed artifacts, and the portal presents a unified view.

### 7.4 Generator Script: `portal/scripts/generate-solution-pages.py`

A new generator script that follows the patterns established by `generate-microservice-pages.py`:

```python
"""
Generate solution design pages for the NovaTrek Architecture Portal.

Reads: architecture/solutions/_NTK-XXXXX-*/
Writes: portal/docs/solutions/index.md
        portal/docs/solutions/NTK-XXXXX.md (per solution)
Copies: SVG diagrams to portal/docs/solutions/svg/

The script:
1. Scans architecture/solutions/ for solution folders
2. Parses the master document header table for metadata
3. Reads each sub-artifact (impacts, decisions, user stories, etc.)
4. Composes a unified portal page per solution
5. Generates an index page with summary dashboard and filterable table
6. Copies SVG diagrams for embedding
"""
```

**Key design decisions for the generator:**

| Decision | Rationale |
|----------|-----------|
| Read Markdown, write Markdown | Consistent with all other generators in the portal |
| Parse header table for metadata | The master document's metadata table is the single source of truth for ticket ID, status, capabilities, services |
| Compose rather than concatenate | Sub-artifacts may need reformatting for the portal context (e.g., adjusting heading levels, resolving relative paths) |
| Copy SVGs into `portal/docs/solutions/svg/` | Same pattern as microservice pages — SVGs live alongside generated Markdown |
| Generate cross-links | Link to microservice pages, capability pages, ADR pages, and ticket pages |

### 7.5 Cross-Linking from Existing Pages

When solution pages are published, they create bidirectional links across the portal:

**From Microservice Pages:**
```markdown
## Solution Designs Affecting This Service

| Ticket | Solution Name | Change Type | Status |
|--------|--------------|-------------|--------|
| [NTK-10003](../solutions/NTK-10003/) | Unregistered Guest Self-Check-In | New endpoint | APPROVED |
| [NTK-10005](../solutions/NTK-10005/) | Wristband RFID Field | Schema change | DRAFT |
```

**From Capability Pages:**
```markdown
## Solutions That Shaped This Capability

| Date | Ticket | Impact | L3 Capabilities Added |
|------|--------|--------|----------------------|
| 2026-02-20 | [NTK-10003](../solutions/NTK-10003/) | EXTENDS | CAP-2.1.4 Reservation-Based Guest Lookup |
| 2026-03-03 | [NTK-10005](../solutions/NTK-10005/) | MODIFIES | — |
```

**From Global Decision Pages:**
```markdown
## Origin
This decision was created as part of [NTK-10003 — Unregistered Guest Self-Check-In](../solutions/NTK-10003/).
```

This cross-linking web is what makes the portal a **knowledge graph** rather than a collection of static pages.

---

## 8. Capability Rollup: Making Solutions Accumulate

This section synthesizes the rollup model from `CAPABILITY-MAP-ANALYSIS.md` (Section 7) with the solution design lifecycle defined above.

### 8.1 The Rollup Chain

```
Solution Design (ticket-scoped)
  └── Capability Mapping (which L1/L2 capabilities are touched)
       └── L3 Capabilities (emergent features introduced by the solution)
            └── Capability Changelog (append-only history per capability)
                 └── Capability Page in Portal (auto-generated timeline + metrics)
```

Every solution design that gets APPROVED contributes to this chain. Over time, the capability pages become the richest part of the portal because they accumulate the design rationale, impact history, and emerging L3 capabilities from all solutions.

### 8.2 The Rollup Workflow

```
Step 1: Architect creates branch and begins solutioning
  │  git checkout -b solution/NTK-XXXXX-slug
  │  ├── AI agent reads architecture/metadata/capabilities.yaml
  │  ├── AI agent reads architecture/metadata/capability-changelog.yaml
  │  └── AI agent reads architecture/solutions/ for prior art
  │
Step 2: Architect creates capability mapping (on the branch)
  │  └── 3.solution/c.capabilities/capabilities.md
  │       ├── Declares EXTENDS/MODIFIES/CREATES/DEPENDS
  │       ├── Identifies new L3 capabilities
  │       └── Documents read-only dependencies
  │
Step 3: Architect updates architecture metadata (on the same branch)
  │  ├── capabilities.yaml — adds new L3 entries (if any)
  │  ├── capability-changelog.yaml — appends this solution's entry
  │  ├── cross-service-calls.yaml — if new integrations
  │  ├── microservices.yaml — if new endpoints or schema changes
  │  └── events.yaml — if new domain events
  │
Step 4: Architect opens PR for architecture review
  │  ├── PR contains the complete solution + all metadata updates
  │  ├── Branch CI validates YAML, runs generators, builds portal preview
  │  └── Reviewer applies architecture review checklist (Section 8.3)
  │
Step 5: PR approved and merged to main
  │  └── Squash merge creates a single audit-trail commit
  │
Step 6: Main CI pipeline runs generators
  │  ├── generate-solution-pages.py → portal/docs/solutions/
  │  ├── generate-capability-pages.py → portal/docs/capabilities/
  │  ├── generate-microservice-pages.py → portal/docs/microservices/
  │  └── generate-ticket-pages.py → portal/docs/tickets/
  │
Step 7: Portal publishes with all cross-links
  │  └── The architecture is now richer than before this ticket
```

**Steps 3 and 4 are the critical steps.** Step 3 is where the solution design feeds back into the architecture metadata that powers the portal — and because metadata updates are on the same branch as the solution, they are reviewed together in the PR (Step 4). This eliminates the "skipped metadata update" failure mode: you cannot merge a solution without a reviewer seeing whether you updated (or deliberately chose not to update) the metadata files. Without this, the solution is published but isolated. With it, the solution becomes part of the living architecture.

### 8.3 Preventing the "Skipped Metadata Update" Problem

The CAPABILITY-MAP-ANALYSIS.md identified that metadata updates get skipped because they are optional and disconnected from the ticket workflow. The branching strategy (Section 4.3) is the primary enforcement mechanism, supplemented by three additional safeguards:

**Mechanism 1: Branch-enforced co-location**

Because metadata updates live on the same branch as the solution design, the PR diff shows both the solution AND the metadata changes (or the conspicuous absence of metadata changes). A reviewer can immediately see: "This architect added a new endpoint to svc-check-in but did not update cross-service-calls.yaml — why?" The branch model makes omissions visible by default.

**Mechanism 2: Capability changelog entry embedded in the solution**

The enhanced template (Section 5.3) includes a pre-formatted YAML block that the architect fills in as part of the solution. This makes the changelog entry a natural byproduct of solutioning rather than a separate task.

**Mechanism 2: AI agent automation**

When the AI agent produces a solution design, it can automatically:
- Read `capabilities.yaml` and suggest capability mappings
- Generate the `c.capabilities/capabilities.md` file
- Draft the `capability-changelog.yaml` entry
- Identify which metadata files need updating and produce diffs

This reduces the Step 4 burden from "remember to update 5 YAML files" to "review and merge the AI's suggested metadata updates."

**Mechanism 3: Architecture review checklist**

Add to the solution review process:

```markdown
## Solution Design Review Checklist

### Completeness
- [ ] Master document has Overview and Component Architecture
- [ ] All impacted services have impact assessment files
- [ ] At least 2 options considered in each decision (MADR format)

### Capability Rollup (must complete before APPROVED)
- [ ] Capability IDs declared in master document header
- [ ] 3.solution/c.capabilities/capabilities.md exists with impact types
- [ ] New L3 capabilities identified and named (if applicable)
- [ ] capability-changelog.yaml entry drafted in the Capability Changelog Entry section
- [ ] All affected metadata YAML files identified for update

### Content Separation
- [ ] Impact files describe WHAT, not WHY or HOW
- [ ] Decision files describe WHY, not HOW
- [ ] Guidance files describe HOW (if present)
- [ ] User stories describe WHO benefits, not technical details
```

---

## 9. ADR Promotion: Ticket Decisions to Global Log

### 9.1 The Problem

ADRs created inside ticket solutions (`3.solution/d.decisions/decisions.md`) are invisible to the global decision log (`decisions/ADR-001-....md` through `decisions/ADR-011-....md`). An architect looking at the global log would never know that ADR-006 through ADR-008 exist in NTK-10003's solution folder.

### 9.2 The Promotion Model

When a solution is APPROVED, any ADRs within it that cross service boundaries or establish reusable patterns should be **promoted** to the global decision log:

1. The decision gets a global ADR number (next in sequence after ADR-011)
2. A copy is placed in `decisions/ADR-NNN-short-title.md`
3. The copy includes a provenance header linking back to the originating solution:

```markdown
# ADR-012: Orchestrator Pattern for Check-In Workflows

## Status
Accepted

## Date
2026-02-20

## Provenance
- **Originating Ticket**: NTK-10003
- **Solution Design**: [NTK-10003 — Unregistered Guest Self-Check-In](../architecture/solutions/_NTK-10003-unregistered-guest-self-checkin/NTK-10003-solution-design.md)
```

4. The original decision in the solution folder is updated with a note: "Promoted to global ADR-012"

### 9.3 Which Decisions Get Promoted

Not every ticket-level decision needs global promotion. Promote when:

| Criterion | Example |
|-----------|---------|
| Decision crosses service boundaries | "svc-check-in will orchestrate the multi-service check-in flow" |
| Decision establishes a reusable pattern | "Use four-field identity verification for all guest lookups" |
| Decision changes a data ownership boundary | "Temporary guest profiles are owned by svc-guest-profiles, not svc-check-in" |
| Decision has safety or security implications | "Unknown adventure categories must default to Pattern 3" |

Do not promote decisions that are purely internal to one service with no cross-cutting implications (e.g., "use a HashMap instead of TreeMap for lookup cache").

---

## 10. AI-Assisted Solution Design Workflow

### 10.1 How the AI Agent Creates Solution Designs Today

In Phase 1, the AI agent (Copilot or Roo Code) executes solution design scenarios by:

1. Reading the ticket via `mock-jira-client.py`
2. Querying production logs via `mock-elastic-searcher.py`
3. Reviewing merge requests via `mock-gitlab-client.py`
4. Reading OpenAPI specs, source code, and architecture metadata
5. Producing the solution folder structure with all artifacts

The agent follows the template in `.ai-instructions/standards/solution-design-template.md` and the instructions in `copilot-instructions.md`.

### 10.2 What Changes for the Continuous Architecture Practice

With the enhanced template, `architecture/solutions/` as the canonical location, and the branch-per-solution workflow, the AI agent workflow becomes:

```
1. Agent reads ticket requirements
   │
2. Agent reads prior solutions from architecture/solutions/
   │  └── Finds related solutions by service or capability overlap
   │     (e.g., "NTK-10003 also modified svc-check-in")
   │
3. Agent reads architecture/metadata/capabilities.yaml
   │  └── Identifies which L1/L2 capabilities this ticket maps to
   │
4. Agent reads architecture/metadata/capability-changelog.yaml
   │  └── Sees history of changes to relevant capabilities
   │
5. Agent creates solution branch: solution/NTK-XXXXX-slug
   │  └── If the agent has terminal access, it runs:
   │      git checkout -b solution/NTK-XXXXX-slug
   │
6. Agent creates solution folder: architecture/solutions/_NTK-XXXXX-slug/
   │  ├── Fills in master document with capability metadata header
   │  ├── Creates all required sub-artifacts
   │  ├── Generates 3.solution/c.capabilities/capabilities.md
   │  └── Drafts capability-changelog.yaml entry
   │
7. Agent identifies metadata updates needed
   │  └── Proposes changes to capabilities.yaml, cross-service-calls.yaml, etc.
   │      These changes are committed to the same branch as the solution.
   │
8. Agent commits and pushes the branch
   │  └── Human architect opens PR (or agent opens PR if tooling supports it)
   │
9. Human architect reviews the PR diff:
   │  ├── Solution design artifacts
   │  ├── Metadata updates
   │  ├── CI validation results (YAML syntax, portal build)
   │  └── Applies architecture review checklist
   │
10. PR approved → merge to main → CI deploys → architecture grows
```

The branching model makes AI-produced solutions reviewable in exactly the same way as human-produced solutions. The PR diff is the review surface. The CI pipeline is the quality gate. The approval is the governance checkpoint. Whether the author is a human or an AI agent is irrelevant to the review process.

### 10.3 AI Instructions Update

The `copilot-instructions.md` file needs these additions:

**New Section: Solution Design Lifecycle**

```markdown
### Solution Design Location

All solution designs MUST be created in `architecture/solutions/_TICKET-ID-kebab-case-slug/`.
Do NOT create solutions in the Phase 1 workspace or any phase-specific path.

### Branching Requirement

Every solution design MUST be developed on a dedicated branch named 
`solution/TICKET-ID-kebab-case-slug`. Create the branch before beginning work.
All solution artifacts AND metadata updates go on the same branch.
Do NOT commit solution designs directly to main.

### Capability Mapping Requirement

Every solution design MUST include `3.solution/c.capabilities/capabilities.md` declaring
which capabilities are touched. Read `architecture/metadata/capabilities.yaml` to find
the correct capability IDs.

### Prior Art Discovery

Before beginning a new solution, read `architecture/solutions/` to discover existing
solutions that affect the same services or capabilities. Reference relevant prior
solutions in the master document.

### Metadata Update Preparation

After completing the solution, identify all metadata YAML files that need updating
and draft the changes ON THE SAME BRANCH. Include the capability-changelog.yaml entry 
in the master document's Capability Changelog Entry section. Commit metadata updates
alongside the solution so they are reviewed together in the PR.
```

### 10.4 Manual Architect Workflow

For architects working without AI assistance, the workflow is the same but without automated prior-art discovery:

1. Create branch: `git checkout -b solution/NTK-XXXXX-slug`
2. Copy the solution design template from the portal (Design Standards > Solution Design Template)
3. Create the folder structure in `architecture/solutions/_NTK-XXXXX-slug/`
4. Fill in artifacts, starting with the master document and working through impacts, decisions, etc.
5. Open `capabilities.yaml` and identify which capabilities are affected
6. Create `c.capabilities/capabilities.md` with the mapping
7. Draft the capability-changelog.yaml entry
8. Update metadata YAML files on the same branch
9. Push branch, open PR, request architecture review
10. Address review feedback, get approval, merge

The key difference: AI can automate steps 5-8 and create the branch programmatically. A manual architect does them explicitly. Both paths produce the same output, both use the same branch-and-PR workflow, and both go through the same review gate.

---

## 11. The Full Integration Picture

This diagram shows how solution designs connect to every other component of the continuous architecture platform:

```
                         ┌─────────────────────────┐
                         │      TICKET SYSTEM       │
                         │  (Vikunja or tickets.yaml)│
                         └────────────┬──────────────┘
                                      │ ticket assigned
                                      ▼
                         ┌─────────────────────────┐
                         │   GIT BRANCH             │
                         │   solution/NTK-XXXXX-slug│
                         └────────────┬──────────────┘
                                      │ architect creates
                                      ▼
                         ┌─────────────────────────┐
                         │   SOLUTION DESIGN        │
                         │  architecture/solutions/  │
                         │  _NTK-XXXXX-slug/        │
                         │                          │
                         │  ├── master document     │
                         │  ├── impacts (per svc)   │
                         │  ├── decisions (MADR)    │
                         │  ├── user stories        │
                         │  ├── capabilities map    │
                         │  ├── diagrams (PUML)     │
                         │  └── risks/assumptions   │
                         └──┬───────┬───────┬───────┘
                            │       │       │
              ┌─────────────┘       │       └─────────────┐
              ▼                     ▼                     ▼
   ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
   │ METADATA UPDATE   │  │ ADR PROMOTION    │  │ CAPABILITY ROLLUP│
   │ (same branch)     │  │ (same branch)    │  │ (same branch)    │
   │                   │  │                  │  │                  │
   │ microservices.yaml│  │ decisions/       │  │ capabilities.yaml│
   │ cross-svc-calls   │  │ ADR-NNN-*.md     │  │ capability-      │
   │ data-stores.yaml  │  │                  │  │ changelog.yaml   │
   │ events.yaml       │  │                  │  │                  │
   └────────┬──────────┘  └────────┬─────────┘  └────────┬─────────┘
            │                      │                     │
            └──────────┬───────────┴─────────────────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │   PULL REQUEST       │
            │                      │
            │ ├── Architecture     │
            │ │   review checklist │
            │ ├── CI validation    │
            │ │   (YAML, portal)   │
            │ └── Reviewer approval│
            └──────────┬───────────┘
                       │ merge to main
                       ▼
            ┌──────────────────────┐
            │   PORTAL GENERATORS   │
            │                      │
            │ generate-solution-   │
            │   pages.py           │
            │ generate-capability- │
            │   pages.py           │
            │ generate-microservice│
            │   -pages.py          │
            │ generate-ticket-     │
            │   pages.py           │
            └──────────┬───────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │   NOVATREK PORTAL    │
            │                      │
            │ ├── Solution Designs │◄── "NTK-10003 changed svc-check-in"
            │ ├── Capabilities     │◄── "CAP-2.1 was extended by NTK-10003"
            │ ├── Microservices    │◄── "svc-check-in affected by 3 solutions"
            │ ├── Decisions        │◄── "ADR-006 originated from NTK-10003"
            │ ├── User Stories     │◄── "NTK-10003 maps to CAP-2.1"
            │ └── Event Catalog    │
            └──────────────────────┘
```

Every arrow is a data flow that can be traced. Every component feeds into the portal. The branching model ensures that nothing reaches the portal without passing through review. The portal presents a unified view of the architecture that grows with every merged solution.

---

## 12. Implementation Plan

### Phase 1: Foundation (Immediate)

| Step | Task | Depends On | Effort |
|------|------|-----------|--------|
| 1.1 | Create `architecture/solutions/` directory | — | Small |
| 1.2 | Migrate 5 existing solutions from Phase 1 workspace to `architecture/solutions/` | 1.1 | Small |
| 1.3 | Add `c.capabilities/` folder to the solution folder template | 1.1 | Small |
| 1.4 | Enhance the NovaTrek solution design template with capability mapping, metadata header, and changelog sections (Section 5) | 1.3 | Small |
| 1.5 | Publish enhanced template to portal at `standards/solution-design/` | 1.4 | Small |
| 1.6 | Create `architecture/metadata/capabilities.yaml` with 34 L2 capabilities (from CAPABILITY-MAP-ANALYSIS.md) | — | Small |
| 1.7 | Create `architecture/metadata/capability-changelog.yaml` with retrospective entries for NTK-10001 through NTK-10005 | 1.6 | Medium |
| 1.8 | Configure branch protection rules on `main` for `architecture/solutions/` and `architecture/metadata/` paths | — | Small |
| 1.9 | Document branch naming convention (`solution/NTK-XXXXX-slug`) in CONTRIBUTING.md or copilot-instructions.md | — | Small |
| 1.10 | Add PR template (`.github/pull_request_template.md`) with architecture review checklist from Section 8.3 | — | Small |

**Outcome:** Solution designs have a canonical home, the template supports capability rollup, the metadata backbone exists, and the branch-based review workflow is enforced.

### Phase 2: Portal Publishing (Short Term)

| Step | Task | Depends On | Effort |
|------|------|-----------|--------|
| 2.1 | Write `portal/scripts/generate-solution-pages.py` — index page + per-solution pages | 1.2 | Medium |
| 2.2 | Write `portal/scripts/generate-capability-pages.py` — capability map with timeline | 1.6, 1.7 | Medium |
| 2.3 | Update `generate-microservice-pages.py` to include "Solutions Affecting This Service" section | 2.1 | Small |
| 2.4 | Add Solution Designs and Business Capabilities nav sections to `portal/mkdocs.yml` | 2.1, 2.2 | Small |
| 2.5 | Wire all generators into `portal/scripts/generate-all.sh` | 2.1, 2.2 | Small |
| 2.6 | Promote ADR-006 through ADR-008 from NTK-10003 to global `decisions/` | — | Small |
| 2.7 | Create CI workflow (`.github/workflows/validate-solution.yml`) that runs YAML validation and portal build on PRs touching `architecture/` | 1.8 | Medium |
| 2.8 | Test full pipeline: branch → solution → PR → CI validates → merge → deploy | 2.5, 2.7 | Small |

**Outcome:** Solution designs and capability pages are live on the portal with cross-links. Branch CI validates solutions before merge.

### Phase 3: AI Integration (Short Term)

| Step | Task | Depends On | Effort |
|------|------|-----------|--------|
| 3.1 | Update `copilot-instructions.md` with solution design lifecycle instructions including branching requirement (Section 10.3) | 1.4, 1.9 | Small |
| 3.2 | Update Roo Code instructions equivalently | 3.1 | Small |
| 3.3 | Add capability rollup checklist to AI instructions | 1.6 | Small |
| 3.4 | Add prior-art discovery workflow to AI instructions | 1.2 | Small |
| 3.5 | Test AI agent — create a new solution for NTK-10006 on a dedicated branch using the enhanced workflow, validate PR diff is reviewable | 3.1, 3.3, 3.4 | Medium |

**Outcome:** AI agent automatically produces capability-mapped solutions on dedicated branches. PR review workflow is the same for AI and human authors.

### Phase 4: Advanced Features (Medium Term)

| Step | Task | Depends On | Effort |
|------|------|-----------|--------|
| 4.1 | Add capability health dashboard to capability pages (churn, staleness) | 2.2 | Medium |
| 4.2 | Implement solution search — full-text search across all solution designs | 2.1 | Medium |
| 4.3 | Add "Related Solutions" auto-detection (same service or capability overlap) | 2.1, 2.2 | Medium |
| 4.4 | Implement solution versioning — track when a solution is superseded by a later ticket | 2.1 | Small |
| 4.5 | Add solution design status badges to the ticket pages | 2.1 | Small |

**Outcome:** The portal becomes an intelligent architecture knowledge base with rich navigation and discovery.

---

## 13. How This Connects to the Companion Documents

This analysis builds on and connects to two companion documents:

### CAPABILITY-MAP-ANALYSIS.md

- **Section 2 (Business Capability Map)** defines the 34 L2 capabilities that solution designs map to
- **Section 4 (Portal Integration)** defined `capabilities.yaml` and the capability page generator — this document adds the solution design feed into those pages
- **Section 7 (Capability Rollup)** established the three-layer traceability chain — this document operationalizes it through the enhanced solution design template and generator

### TICKETING-INTEGRATION-ANALYSIS.md

- **Section 6 (Ticket Structure)** defined the user story template with capability tags — this document adds the structured folder and artifact model that sits *between* the ticket and the capability rollup
- **Section 7 (Portal Integration)** defined ticket pages with cross-links to capability and service pages — this document adds solution design pages as the missing middle layer
- **Section 8 (AI Awareness)** defined how the AI reads tickets — this document extends that to reading prior solutions and producing capability-mapped output

**The three documents together form a complete continuous architecture system:**

```
TICKETING-INTEGRATION-ANALYSIS.md     This document                  CAPABILITY-MAP-ANALYSIS.md
  (tickets come in)              →    (solutions are designed)    →   (capabilities accumulate)
  
  Ticket → Use Cases                  Solution Design                 L3 Capability → L2 → L1
  Capability tags on tickets          Branch per solution             Capability changelog
  AI reads tickets                    PR review = arch review         AI suggests rollup
  Ticket pages in portal              Merge to main = publish         Capability pages in portal
  Ticket status ← PR status           Solution pages in portal        Capability timeline grows
```

Each document covers one stage of the lifecycle. Together, they ensure that work flows from ticket to solution to capability without losing information at any stage.

---

## 14. What Success Looks Like

Six months from now, an architect picking up a new check-in ticket should be able to:

1. Open the **capability page for CAP-2.1 (Day-of-Adventure Check-In)** in the portal
2. See a **timeline of every solution** that has touched this capability — NTK-10001 through NTK-10005 and beyond
3. Read the **L3 capabilities** that emerged: reservation-based lookup, RFID wristband assignment, group check-in, etc.
4. Click through to any prior **solution design** to understand what was decided and why
5. See which **ADRs** shaped the check-in domain (ADR-005, ADR-006, ADR-007, ADR-008)
6. Understand the **current state of the service** through the microservice page, which references all impacting solutions
7. Start their new solution with **full context** — not from a blank page, but from the accumulated knowledge of every prior check-in decision

That is continuous architecture. Not documentation that decays, but knowledge that compounds.
