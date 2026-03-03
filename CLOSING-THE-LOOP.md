# Closing the Loop: From Point-in-Time Architecture to Continuous State Management

> **The core problem**: Our architecture practice documents the *next effort* in rich detail — current state, target state, decisions, impacts, risks — then abandons that knowledge the moment the project ships. The target state we just built becomes the new current state, but nobody records it. The next architect starts from zero, rediscovering what we already knew.

| | |
|-----------|-------|
| **Author** | Christopher Blaisdell |
| **Created** | 2026-03-01 |
| **Status** | Active |
| **Organization** | Architecture Practice |
| **Related** | [ADR-001: AI Toolchain Selection](decisions/ADR-001-ai-toolchain-selection.md) • [Roadmap](roadmap/ROADMAP.md) • [Phase 1 Outputs](phase-1-ai-tool-cost-comparison/outputs/README.md) |

---

## 1. The Problem in Full

### 1.1 What We Do Today

The Architecture Practice runs a well-structured workflow for each architectural effort:

1. **Ticket intake** → classify complexity, scaffold a workspace
2. **Investigation** → analyze current state (logs, source code, APIs, dependencies)
3. **Solution design** → document current state → target state transformation with ADRs, impacts, risks, user stories, guidance
4. **Architecture update** → modify corporate artifacts (Swagger specs, PlantUML diagrams) to reflect the target state
5. **Publish** → push solution design to Confluence

This workflow produces high-quality artifacts. Our Phase 1 AI-assisted execution scored **149/155 (96.1%)** across 5 representative scenarios. The *format* of what we produce is excellent.

### 1.2 What We Don't Do

**We never close the loop.**

After a project ships, the solution design sits in Confluence as a historical snapshot. The target state it described is now reality — the Swagger specs were updated, the code was deployed, the database was migrated. But:

- The **solution design still describes a current→target transformation** that is no longer meaningful. It's a diff that's already been applied.
- The **corporate architecture artifacts** (Swagger specs, component diagrams) are updated *during* the project but their relationship to the design that drove the change is severed.
- The **investigation artifacts** captured a current state that no longer exists. Nobody goes back to record what the current state actually became.
- The **next architect** who picks up a ticket touching the same service has to **re-investigate the current state from scratch** — reading source code, running queries, tracing API contracts — because there is no authoritative "this is what the system looks like *now*."

### 1.3 The Concrete Cost

Consider what actually happened in our Phase 1 scenarios:

| Scenario | What Was Captured | What Was Lost |
|----------|-------------------|---------------|
| **NTK-10004** (Schedule Overwrite Bug) | Detailed investigation: 4 ERROR logs, 2 WARN logs, source code analysis of `SchedulingService.java`, root cause identification (PUT vs PATCH + no @Version), 3-phase remediation plan, 2 ADRs | After the fix ships: nobody records that the scheduling service now uses PATCH semantics with optimistic locking. The next architect investigating a scheduling issue starts from scratch. |
| **NTK-10003** (Unregistered Guest Check-In) | Comprehensive design: orchestrator pattern, 4-field verification, temporary profiles, 30-min sessions, 6 service impacts, 5 risks, 4 ADRs, sequence diagram, C4 component diagram | After deployment: the `POST /check-ins/lookup-reservation` endpoint exists but is documented only in the solution design. The corporate Swagger spec was not updated. No component diagram shows the new orchestration flow as the *current* state. |
| **NTK-10002** (Category Classification) | Config-driven classification with 25→3 mapping, Pattern 3 fallback, 2 ADRs | After deployment: the classification logic exists in code but the architectural decisions that shaped it live only in a ticket workspace folder. No living record that svc-check-in now owns category classification via a configuration-driven approach. |
| **NTK-10001** (Elevation Data) | Swagger spec updated, component diagram annotated | This was the *only* scenario that partially closed the loop — because the scenario was specifically "update corporate artifacts." But even here, the solution design that drove the change is not linked back to the spec. |

**The pattern**: We invest 20-100 minutes per effort to document current→target state in detail, then we throw away the result by never promoting the target state to become the new baseline.

### 1.4 The Compounding Effect

This isn't just inefficiency — it's **compounding knowledge destruction**:

```
Project 1:  Current State A → Target State B   (documented, designed, shipped)
                                                 Target State B is never recorded as the new current state
Project 2:  ??? → Target State C                 (architect must rediscover "A as modified by B"
                                                   from source code, logs, and tribal knowledge)
                                                 Target State C is never recorded as the new current state
Project 3:  ??? → Target State D                 (architect must rediscover "A as modified by B
                                                   as modified by C" — compounding uncertainty)
```

By Project 5, no one knows the current state of the system with confidence. The corporate Swagger specs may or may not reflect reality. The component diagrams may or may not include the last 3 changes. Architects work from a blend of stale documentation, source code reading, tribal knowledge, and guesswork.

**This is the architecture practice equivalent of never committing to version control** — like developing software where you write code, deploy it, then delete the source and start over next sprint.

---

## 2. What "Closing the Loop" Means

### 2.1 The Missing Step

Every architecture effort today has these steps:

```
INTAKE → INVESTIGATE → DESIGN → BUILD → DEPLOY → ✅ Done
```

What's missing is:

```
INTAKE → INVESTIGATE → DESIGN → BUILD → DEPLOY → PROMOTE → ✅ Done
```

**PROMOTE** means: after the effort ships, update the authoritative architecture baseline to reflect the new reality. Specifically:

| Artifact | Current Practice | Closed-Loop Practice |
|----------|-----------------|---------------------|
| **Corporate Swagger specs** | Sometimes updated during the project (SC-04 pattern) | Always updated. Post-deployment verification confirms spec matches deployed reality. |
| **Component diagrams** | Sometimes annotated during the project | Always updated. Target-state diagram from the solution design *replaces* the current diagram, not annotates it. |
| **Service architecture pages** | Don't exist as a living document | Each service has a living architecture page that aggregates: current API contract, current data model, active ADRs, integration points, quality attributes. Updated after every effort that touches the service. |
| **Decision records (ADRs)** | Created during the project, filed in the ticket workspace folder | Promoted to a service-level or system-level decision log. Status updated (PROPOSED → ACCEPTED → SUPERSEDED) as the system evolves. |
| **Investigation artifacts** | Describe the pre-project current state | Post-project: the "current state" section is updated to reflect the *post-project* reality. The investigation becomes a historical record of what changed and why. |
| **Solution design** | Snapshot of current→target transformation | Post-project: status updated to IMPLEMENTED. A "Post-Implementation Notes" section added documenting deviations, lessons learned, and actual vs. planned outcomes. |

### 2.2 The State Machine

Architecture artifacts should follow a lifecycle, not be one-shot documents:

```
┌───────────┐     ┌───────────┐     ┌───────────┐     ┌───────────┐
│  DRAFTED  │────>│ APPROVED  │────>│IMPLEMENTING│───>│IMPLEMENTED│
└───────────┘     └───────────┘     └───────────┘     └─────┬─────┘
                                                            │
                                                            v
                                                    ┌───────────────┐
                                                    │   PROMOTED    │
                                                    │ (baseline     │
                                                    │  updated)     │
                                                    └───────┬───────┘
                                                            │
                                                            v
                                                    ┌───────────────┐
                                                    │   ARCHIVED    │
                                                    │ (historical   │
                                                    │  record)      │
                                                    └───────────────┘
```

**PROMOTED** is the key state that doesn't exist today. It means:
- Corporate artifacts have been updated to reflect the new reality
- ADRs have been moved to the appropriate decision log
- Service architecture pages reflect the post-project state
- The solution design has been annotated with implementation notes
- The next architect can start from *here* instead of reconstructing from source code

### 2.3 What Gets Promoted Where

```
Solution Design Artifacts          Corporate Architecture Baseline
────────────────────────           ──────────────────────────────
                                   
ticket-workspace/                  corporate-services/
├── NTK-XXXXX-solution-design.md     ├── services/
│   (current→target)                 │   └── svc-xxx.yaml        ← Swagger spec updated
├── 3.solution/                      ├── diagrams/
│   ├── d.decisions/                 │   └── Components/*.puml   ← Diagrams updated
│   │   └── decisions.md  ─────────>│
│   │       (ADRs)                   ├── decision-log/            ← ADRs promoted here
│   ├── i.impacts/                   │   └── svc-xxx-decisions.md
│   │   └── impacts.md              │
│   ├── c.current.state/            ├── service-pages/            ← Living service docs
│   │   └── investigations.md ─────>│   └── svc-xxx.md            (current state lives here)
│   └── ...                         │
│                                    └── architecture-log/        ← Historical record
└── (status: PROMOTED)                  └── 2026-Q1/NTK-XXXXX.md  (what changed, when, why)
```

---

## 3. Audit: What Works and What Doesn't

### 3.1 What Our Current Practice Gets Right

| Practice Element | Strength | Evidence |
|-----------------|----------|---------|
| **Structured workspace scaffolding** | Consistent folder structure (`1.requirements/`, `2.analysis/`, `3.solution/`) ensures every effort captures the same categories of information | All 5 NTK tickets use the same structure |
| **MADR decision records** | Decisions are captured with context, options analysis, and consequences — not just "we decided X" | 9 ADRs across 5 scenarios, all with proper pros/cons analysis |
| **Investigation methodology** | Current state investigations are thorough — log analysis, source code reading, API contract review | NTK-10004 investigation traced 4 ERROR logs through causal chain to root cause |
| **Corporate artifact management** | Swagger specs and PlantUML diagrams exist as a corporate baseline | 19 service specs, component/system/sequence diagrams |
| **AI-assisted quality** | AI tooling produces standards-compliant artifacts at 96.1% quality | Phase 1 results across all complexity levels |
| **arc42 structure** | Architecture documentation follows a recognized framework with 12 sections covering all views | Templates and standards in `architecture-standards/` |

### 3.2 What Our Current Practice Gets Wrong

| Gap | Description | Impact | Severity |
|-----|-------------|--------|----------|
| **No promotion step** | After deployment, no workflow step requires updating the corporate baseline to reflect the new reality | Next architect must rediscover current state from scratch | **CRITICAL** |
| **ADRs siloed in ticket folders** | Decision records live in `_NTK-XXXXX/3.solution/d.decisions/` — once the ticket is closed, they're buried in a project folder | Decisions are effectively lost. No one browses closed ticket folders looking for past ADRs. | **HIGH** |
| **No living service architecture pages** | There is no single document per service that says "here is what this service looks like *right now*" | Architects read Swagger specs (schema only) and source code (implementation only) but have no architectural context — no "why it was built this way" or "what patterns it uses" | **HIGH** |
| **Solution designs are write-once** | Designs go from DRAFTED → APPROVED → IMPLEMENTED but never to PROMOTED or ARCHIVED with post-implementation notes | We capture what we *planned* but never what we *actually built*. Planned vs. actual divergence is invisible. | **HIGH** |
| **Investigation artifacts expire immediately** | The "current state" captured in an investigation is the *pre-project* state. After the project ships, this document describes a state that no longer exists. | A future architect reading this investigation gets *wrong* information about the current state. Stale current-state docs are worse than no docs. | **MEDIUM** |
| **Diagrams are annotated, not updated** | SC-04 added a `note` to the component diagram rather than updating the diagram structure. This is the norm — diagrams get annotations, not structural updates. | Over time, diagrams become layered with notes pointing to changes but the base diagram drifts from reality. | **MEDIUM** |
| **No backlinking from corporate artifacts to decisions** | The Swagger spec for svc-trail-management was updated with `elevation_loss_m` but there's no trace in the spec that points to NTK-10001 or ADR that justified the change. | You can see *what* changed in the spec, but not *why*. Git blame helps but is fragile and doesn't surface architectural rationale. | **MEDIUM** |
| **Confluence as a graveyard** | Solution designs are published to Confluence and never touched again. Confluence accumulates stale pages with no mechanism to mark them superseded or refresh them. | Confluence becomes a museum of past decisions rather than a living architecture reference. New team members can't distinguish current from historical. | **HIGH** |

### 3.3 The Gap Quantified

For the 5 scenarios executed in Phase 1:

| Metric | Produced | Promoted to Baseline | Gap |
|--------|----------|---------------------|-----|
| ADRs created | 9 | 0 | 9 ADRs exist only in ticket folders — none are in a global decision log |
| Service impacts documented | 12 | 1 (partial) | Only NTK-10001's Swagger update was applied; NTK-10003's 6 service impacts exist only in the solution design |
| Diagrams created | 2 new + 1 updated | 1 (annotated, not restructured) | NTK-10003's C4 component diagram is a project artifact, not a corporate diagram |
| Investigation current states | 3 | 0 | All 3 investigations describe pre-project state that will become stale on deployment |
| Solution design statuses | 5 (all APPROVED or equivalent) | 0 updated to IMPLEMENTED/PROMOTED | All 5 solution designs will sit in ticket folders with no lifecycle progression |

**Gap rate: 95%+ of architecture knowledge produced during a project is abandoned in ticket folders after deployment.**

---

## 4. The Plan: Closing the Loop

### 4.1 Immediate Actions (Can Begin Now)

These require no new tooling — they are process changes that fit within our existing workspace structure.

#### 4.1.1 Create Living Service Architecture Pages

**What**: For each of the 19 services in `corporate-services/services/`, create a companion markdown file: `corporate-services/service-pages/svc-xxx-architecture.md`

**Content**:
```markdown
# svc-scheduling-orchestrator — Architecture Overview

## Current State (as of 2026-03-01)

### Purpose
Orchestrates daily adventure scheduling by coordinating guide assignments,
trail availability, and equipment allocation.

### API Contract Summary
- PUT /guides/{guideId}/schedule — Full guide schedule replacement [SEE ADR-NTK10004-001: MIGRATING TO PATCH]
- POST /schedules/daily-assignments — Generate daily assignments
- GET /schedules/{date} — Retrieve daily schedule

### Active Architecture Decisions
| ADR | Decision | Status | Ticket |
|-----|----------|--------|--------|
| ADR-NTK10004-001 | Use PATCH semantics for partial schedule updates | ACCEPTED | NTK-10004 |
| ADR-NTK10004-002 | JPA @Version for optimistic locking on DailySchedule | ACCEPTED | NTK-10004 |

### Integration Points
- svc-guide-management (reads guide certifications, specializations, languages)
- svc-trail-management (reads trail availability)
- svc-gear-inventory (reads equipment allocation)

### Patterns & Constraints
- Data ownership: schedule data owned by orchestrator; guide profile data owned by guide-management
- Concurrency: Optimistic locking via @Version (post NTK-10004)
- API style: PATCH with field-level merge semantics (post NTK-10004)

### Change History
| Date | Ticket | Change |
|------|--------|--------|
| 2026-Q1 | NTK-10004 | Migrated PUT→PATCH, added @Version optimistic locking, added concurrent update monitoring |
```

**Effort**: ~30 min per service initial creation; ~10 min per update after each project
**Immediate value**: Next architect has a starting point instead of source code

#### 4.1.2 Create a Global ADR Decision Log

**What**: Create `corporate-services/decision-log/README.md` that indexes all active ADRs across all services. After each project, promote ticket-level ADRs to this log.

**Structure**:
```markdown
# Architecture Decision Log

| ID | Service(s) | Decision | Status | Date | Source Ticket |
|----|-----------|----------|--------|------|--------------|
| ADR-NTK10004-001 | svc-scheduling-orchestrator | PATCH semantics for schedule updates | ACCEPTED | 2026-03 | NTK-10004 |
| ADR-NTK10004-002 | svc-scheduling-orchestrator | JPA @Version optimistic locking | ACCEPTED | 2026-03 | NTK-10004 |
| ADR-NTK10003-001 | svc-check-in | Orchestrator pattern for unregistered check-in | ACCEPTED | 2026-03 | NTK-10003 |
| ADR-NTK10003-002 | svc-check-in, svc-reservations | 4-field reservation verification | ACCEPTED | 2026-03 | NTK-10003 |
| ADR-NTK10003-003 | svc-guest-profiles | Temporary guest profiles with merge-on-register | ACCEPTED | 2026-03 | NTK-10003 |
| ADR-NTK10003-004 | svc-check-in | 30-minute session expiry for kiosk tokens | ACCEPTED | 2026-03 | NTK-10003 |
| ADR-NTK10002-001 | svc-check-in | Config-driven classification with Pattern 3 fallback | ACCEPTED | 2026-03 | NTK-10002 |
| ADR-NTK10002-002 | svc-check-in | Configuration-based classification over code-based | ACCEPTED | 2026-03 | NTK-10002 |
```

**Effort**: 15 min initial setup; 5 min per project to promote ADRs
**Immediate value**: Architects can see all active decisions in one place, filterable by service

#### 4.1.3 Add PROMOTE Checklist to Solution Design Template

**What**: Add a "Post-Implementation Promotion" section to every solution design template:

```markdown
## Post-Implementation Promotion Checklist

- [ ] Corporate Swagger specs updated to reflect implemented state
- [ ] Component diagrams updated (structure, not just annotations)
- [ ] ADRs promoted to global decision log
- [ ] Service architecture page(s) updated with new patterns, endpoints, constraints
- [ ] Investigation "current state" updated to reflect post-implementation reality
- [ ] Solution design status updated to IMPLEMENTED → PROMOTED
- [ ] Post-implementation notes added (planned vs. actual deviations)
```

**Effort**: Template change (5 min); discipline enforcement (ongoing)
**Immediate value**: The promotion step becomes visible and checkable

### 4.2 Short-Term Improvements (Phase 2 Integration)

These enhancements integrate closing-the-loop into the AI-assisted workflow.

#### 4.2.1 AI-Assisted Promotion

When the AI toolchain is used for the PROMOTE step:

1. **Read the solution design** (current→target transformation)
2. **Read the current corporate artifacts** (Swagger specs, diagrams, service pages)
3. **Generate the updates** to promote the target state to the new baseline
4. **Update the decision log** with new ADRs
5. **Update the service architecture page** with post-project changes
6. **Mark the solution design** as PROMOTED with implementation notes

This is essentially Scenario 04 (Architecture Update) extended to include all promotion activities, not just the Swagger spec update.

**Key insight from Phase 1**: SC-04 already demonstrated that AI can update corporate artifacts from a solution design (quality score: 24/25). The PROMOTE step is a natural extension of what we already proved works.

#### 4.2.2 Stale Detection

Automate detection of drift between solution designs and corporate artifacts:

- After N days post-deployment, check if corporate artifacts were updated
- Flag services where the Swagger spec was modified but the service architecture page was not
- Detect ADRs in ticket folders that were never promoted to the global log
- Surface solution designs stuck in APPROVED status for more than one sprint

#### 4.2.3 Architecture Freshness Score

Add to each service architecture page:

```markdown
### Architecture Freshness
| Metric | Value |
|--------|-------|
| Last architecture update | 2026-03-15 (NTK-10004) |
| Active ADRs | 2 |
| Swagger spec last modified | 2026-03-15 |
| Days since last update | 14 |
| Freshness status | 🟢 CURRENT (< 90 days) |
```

Services with no update in >90 days get flagged for review. This creates a *pull* mechanism — visibility into staleness motivates architects to update.

### 4.3 Medium-Term Improvements (Phase 3-4 Integration)

#### 4.3.1 Pipeline-Enforced Promotion Gates

In Phase 3 (Pipeline Integration), add a promotion validation step:

```yaml
# CI/CD pipeline step
- name: Validate Architecture Promotion
  steps:
    - check: solution-design-status != APPROVED for > 30 days
    - check: all ADRs from ticket promoted to decision-log
    - check: all impacted service-pages updated
    - check: swagger-spec last-modified > solution-design approval-date
    - check: component-diagrams structurally updated (not just annotated)
```

Deployments where the architecture baseline wasn't updated generate warnings (initially) or blocks (eventually).

#### 4.3.2 Artifact Graph with Traceability

In Phase 4 (Artifact Graph), every corporate artifact links back to the decision/project that created or modified it:

```yaml
# In svc-trail-management.yaml metadata
x-architecture:
  elevation_loss_m:
    introduced_by: NTK-10001
    adr: ADR-NTK10001-001
    date: 2026-03-15
```

This provides **bidirectional traceability**: from the spec you can find the decision; from the decision you can find all affected specs.

### 4.4 Long-Term Vision (Phase 5 Integration)

#### 4.4.1 Continuous State Is the Default

In the mature state, "current state" is never something an architect has to investigate from scratch:

```
Today:
  Architect picks up ticket → INVESTIGATE current state (1-2 hours) → Design

Future:
  Architect picks up ticket → READ service architecture page (5 minutes) → Design
                                    ↑ Always current because promotion is mandatory
```

#### 4.4.2 Architecture Archaeology Is Eliminated

Every design question has a traceable answer:

- "Why does svc-scheduling-orchestrator use PATCH?" → ADR-NTK10004-001 (linked from service page)
- "When was the unregistered check-in flow added?" → NTK-10003, 2026-Q1 (in change history)
- "What pattern does svc-check-in use for verification?" → Orchestrator with 4-field verification (in service page patterns section)
- "Who made this decision and what alternatives were rejected?" → Full MADR record in global decision log

#### 4.4.3 The Flywheel Effect

As the corpus of living architecture documentation grows with each promoted effort:

1. **Investigations get faster** — the current state is already documented
2. **Designs get better** — past decisions are visible and inform new ones
3. **Reviews get more precise** — reviewers can point to existing ADRs and patterns
4. **AI assistance gets more effective** — the AI has authoritative current state to work from, not stale docs
5. **Onboarding accelerates** — new architects read service pages, not source code

---

## 5. Revised Outcomes for the Cost Comparison

Phase 1's AI Tool Cost Comparison evaluated toolchains based on quality, cost, and standards compliance. The discovery that our practice fails to close the loop between architecture efforts changes how we should evaluate these outcomes.

### 5.1 Original Evaluation Focus

The original Phase 1 evaluation focused on:
- Cost per seat (fixed vs. usage-based)
- Quality score per scenario (rubric-based)
- Standards compliance (arc42, C4, MADR format adherence)
- Workflow integration friction

### 5.2 Revised Evaluation Focus

The evaluation must now also account for:

| New Criterion | Why It Matters | Impact on Tool Selection |
|---------------|---------------|-------------------------|
| **Promotion capability** | Can the tool execute the PROMOTE step — updating corporate artifacts, promoting ADRs, refreshing service pages — from a completed solution design? | Both tools can do this (SC-04 proved it). But the tool that does it *better* (fewer corrections, more complete coverage) reduces the cost of closing the loop. |
| **Baseline awareness** | Can the tool use living service architecture pages as context when investigating current state? | The tool with better context window utilization (more files read, deeper cross-reference) will benefit more from maintained baselines. |
| **Drift detection** | Can the tool identify when corporate artifacts are stale relative to deployed reality? | Usage-based (Kong AI) tooling may be cheaper for periodic "staleness scans" that don't require full design work. |
| **End-to-end workflow cost** | What is the total cost to go from ticket intake through promotion (not just through design)? | Adding the PROMOTE step increases the per-project token usage by ~30-50% but prevents ~2 hours of re-investigation on the next project. |

### 5.3 Updated Cost Model

The original cost model assumed 26 runs/month across 5 scenario types. With the PROMOTE step added:

| Scenario | Monthly Freq | Original | + Promote Step | New Total |
|----------|-------------|----------|---------------|-----------|
| SC-01: Ticket Triage | 10 | 10 runs | +0 (triage doesn't need promotion) | 10 |
| SC-02: Solution Design | 6 | 6 runs | +6 promote runs | 12 |
| SC-03: Investigation | 4 | 4 runs | +4 promote runs | 8 |
| SC-04: Architecture Update | 4 | 4 runs | +0 (this IS the promotion step) | 4 |
| SC-05: Cross-Service | 2 | 2 runs | +2 promote runs | 4 |
| **Total** | | **26** | **+12** | **38** |

This is significant: the promote step adds ~12 runs/month, pushing the workload to 38 runs/month. At this level:

| Tool | Monthly Cost (38 runs) | Notes |
|------|----------------------|-------|
| **Copilot Business** | $19.00 | Fixed — unaffected by volume increase |
| **Copilot Enterprise** | $39.00 | Fixed — unaffected by volume increase |
| **Kong AI** | **~$67.46** | 38 runs × ~$1.78/run — **3.5× Copilot Business** |

The actual per-run variable cost of ~$1.78 accounts for the agentic re-transmission tax: Roo Code's client-side architecture re-transmits the entire conversation history at every turn of the agentic loop. With an average of 17 tool calls per scenario and cumulative context growth from ~10K to ~60-120K tokens per turn, the process cost far exceeds the content cost. See [COST-MEASUREMENT-METHODOLOGY.md](phase-1-ai-tool-cost-comparison/COST-MEASUREMENT-METHODOLOGY.md) for the full analysis.

**Key finding**: **Copilot Business is 3.5× cheaper** than Kong AI at the realistic 38 runs/month workload ($19 vs $67). This advantage grows with volume — the PROMOTE step amplifies Copilot's cost advantage.

### 5.4 Updated Breakeven Analysis

```
Breakeven (Copilot Business vs Kong AI):   ~11 runs/month
Revised workload with PROMOTE step:        ~38 runs/month   (3.5× past breakeven)
```

At an average variable cost of ~$1.78/run, Kong AI exceeds Copilot Business ($19/month) at just ~11 runs/month. Our realistic workload of 38 runs/month is **3.5× past the breakeven point**. This is not a close call — Copilot's flat-rate model dominates for any architecture practice doing more than minimal work.

### 5.5 Updated Recommendation Factors

| Factor | Kong AI + Roo Code | Copilot Business | Impact of PROMOTE |
|--------|-------------------|-----------------|-------------------|
| Cost at 26 runs/mo | ~$58.10 | $19.00 ✅ | Copilot **3× cheaper** even without promotion |
| Cost at 38 runs/mo | **~$67.46** | **$19.00** ✅ | Copilot **3.5× cheaper** at realistic workload |
| Cost at 50 runs/mo (growth) | ~$89.00 | $19.00 ✅ | Copilot **4.7× cheaper** — gap widens with volume |
| Promotion quality | TBD | 24/25 (SC-04) ✅ | Both tools can promote; Copilot proven |
| Baseline context utilization | TBD | Strong (40 files read across scenarios) | Both benefit from maintained baselines |
| Budget predictability | Variable ❌ | Fixed ✅ | PROMOTE adds volume uncertainty — fixed rate is safer |
| Infrastructure risk | Kong Gateway + Qdrant + API keys ❌ | GitHub-managed ✅ | Custom stack adds 15-20% annual drift tax |
| Failure mode risk | Infinite retry loop (documented) ❌ | Server-side compaction ✅ | Roo+Kong error obfuscation creates runaway cost risk |

### 5.6 Net Impact on ADR-001

The PROMOTE workflow addition should be reflected in ADR-001 as:

1. **The per-project workload increases ~46%** (from 26 to 38 runs) — this was hidden cost that exists regardless of which tool we select
2. **The increase favors flat-rate pricing** (Copilot) over usage-based pricing (Kong AI) at realistic volumes
3. **Both tools must be evaluated on promotion quality**, not just design quality — SC-04 is the proxy scenario for this
4. **The "cost per quality point" metric should be recalculated** at the revised 38 runs/month workload

---

## 6. Integration with the Overall Plan

### 6.1 Phase Mapping

The closing-the-loop improvements map directly to existing roadmap phases:

| Improvement | Phase | Integration Point |
|-------------|-------|-------------------|
| Living service architecture pages | **Phase 1** (can start now) | Create initial pages based on Phase 1 scenario artifacts |
| Global ADR decision log | **Phase 1** (can start now) | Promote the 9 ADRs from Phase 1 scenarios as the first entries |
| PROMOTE checklist in templates | **Phase 2** (workflow design) | Bake promotion into the AI-assisted workflow definition |
| AI-assisted PROMOTE step | **Phase 2** (workflow design) | Define as a new scenario type (SC-06: Post-Implementation Promotion) |
| Staleness detection | **Phase 3** (pipeline integration) | Add freshness checks to the CI/CD validation pipeline |
| Architecture freshness score | **Phase 3** (pipeline integration) | Publish freshness metrics alongside documentation |
| Bidirectional traceability | **Phase 4** (artifact graph) | Artifact graph links decisions to specs to diagrams |
| Pipeline-enforced promotion gates | **Phase 3** (pipeline integration) | Block or warn on deploys without architecture promotion |
| Flywheel metrics | **Phase 5** (continuous improvement) | Measure investigation time reduction as baselines improve |

### 6.2 Recommended Roadmap Additions

The following milestones should be added to the existing phases:

**Phase 1 (immediate)**:
- 1.8: Create initial service architecture pages from Phase 1 scenario outputs
- 1.9: Create global decision log and promote Phase 1 ADRs

**Phase 2 (workflow design)**:
- 2.7: Define PROMOTE step in the to-be workflow
- 2.8: Create SC-06 playbook for AI-assisted post-implementation promotion
- 2.9: Test PROMOTE step on Phase 1 scenario outputs

**Phase 3 (pipeline integration)**:
- 3.8: Implement staleness detection in validation pipeline
- 3.9: Add promotion-completeness check to deploy gates

**Phase 4 (artifact graph)**:
- 4.8: Implement bidirectional traceability (spec ↔ decision ↔ ticket)

**Phase 5 (continuous improvement)**:
- 5.6: Measure investigation time reduction vs. pre-promotion baseline
- 5.7: Track architecture freshness scores across all services

---

## 7. Definition of Done

We will know we have solved this problem when:

1. **No architect ever starts an investigation by reading source code as the primary source of truth.** Service architecture pages are the starting point.
2. **Every active ADR is findable in the global decision log** — not buried in a closed ticket folder.
3. **Corporate diagrams reflect the actual deployed architecture** — not a base diagram plus notes.
4. **Solution designs have a terminal state** (PROMOTED or ARCHIVED) — none are stuck in APPROVED forever.
5. **The time from "architect picks up ticket" to "current state understood" drops by >60%** — because the current state is already documented.
6. **Architecture freshness scores are green (< 90 days) for >80% of services** — the baseline is actively maintained.

---

## 8. Starting Now

We don't need to wait for Phase 2 or Phase 3 to begin closing the loop. The first three actions can happen immediately:

1. **Create `corporate-services/service-pages/`** with an initial architecture page for each of the services touched by Phase 1 scenarios (svc-scheduling-orchestrator, svc-check-in, svc-trail-management, svc-guest-profiles, svc-reservations, svc-trip-catalog)
2. **Create `corporate-services/decision-log/`** with the 9 ADRs from Phase 1 promoted to a global index
3. **Add the PROMOTE checklist** to the solution design template

These three actions take ~4 hours and immediately demonstrate the value of closing the loop — providing a tangible starting point that every subsequent phase builds upon.

**The alternative is what we've always done: produce excellent architecture documentation, then abandon it the moment the project ships, forcing the next architect to start from scratch. We know how that ends.**
