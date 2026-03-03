# Continuous Architecture Platform POC Roadmap

| | |
|-----------|-------|
| **Author** | Christopher Blaisdell |
| **Created** | 2026-03-01 |
| **Last Updated** | 2026-03-03 |
| **Status** | Active |

---

## Overview

This roadmap tracks the phased delivery of the Continuous Architecture Platform POC. Each phase builds on the previous one, but delivers standalone value. The roadmap is organized as a sequence of decisions, implementations, and validations that progressively transform the Architecture Practice from point-in-time documentation to a living, navigable architecture platform.

---

## Roadmap Timeline

```
Q1 2026                    Q2 2026                    Q3 2026
Mar         Apr         May         Jun         Jul         Aug
|-----------|-----------|-----------|-----------|-----------|
|== Phase 1 ==|                                             
|  AI Tool    |                                             
|  Comparison |                                             
    |== Phase 6 ==|                                         
    |  Docs        |                                        
    |  Publishing  |                                        
              |======= Phase 2 =======|                    
              |  AI-Integrated         |                    
              |  Workflow Design       |                    
                        |======= Phase 3 =======|         
                        |  DocFlow Pipeline       |         
                        |  Integration           |         
                                    |======= Phase 4 =======|
                                    |  Navigable Artifact    |
                                    |  Graph                 |
                                                |== Phase 5 ==|
                                                |  Continuous  |
                                                |  Improvement |
```

---

## Phase 1: AI Tool Cost Comparison

**Timeline:** March 2026
**Status:** Synthetic workspace complete, ready for execution
**Gate:** Decision document [ADR-001](../decisions/ADR-001-ai-toolchain-selection.md) approved

### Milestones

| ID | Milestone | Target Date | Status | Dependencies |
|----|-----------|-------------|--------|--------------|
| 1.1 | Synthetic workspace complete | 2026-03-01 | COMPLETE | None |
| 1.2 | Workspace transferred to evaluation environment | 2026-03-01 | COMPLETE | 1.1 |
| 1.3 | Roo Code + Kong AI scenario execution | 2026-03-07 | NOT STARTED | 1.2 |
| 1.4 | GitHub Copilot scenario execution | 2026-03-03 | COMPLETE | 1.2 |
| 1.5 | Cost-per-seat analysis complete | 2026-03-17 | NOT STARTED | 1.3, 1.4 |
| 1.6 | Quality and compliance comparison complete | 2026-03-19 | NOT STARTED | 1.3, 1.4 |
| 1.7 | ADR-001 AI Toolchain Selection decision recorded | 2026-03-21 | NOT STARTED | 1.5, 1.6 |
| 1.8 | Create initial service architecture pages from Phase 1 outputs | 2026-03-03 | COMPLETE | 1.4 |
| 1.9 | Create global decision log and promote Phase 1 ADRs (9 ADRs) | 2026-03-03 | COMPLETE | 1.4 |
| 1.10 | Closing-the-loop analysis documented | 2026-03-01 | COMPLETE | None |

### Deliverables

- Monthly cost-per-seat comparison table (Roo+Kong vs Copilot Business vs Copilot Enterprise)
- **Revised cost model including PROMOTE step** (38 runs/month baseline vs original 26)
- Quality score comparison across 5 architecture scenarios
- Standards compliance rate comparison
- [ADR-001: AI Toolchain Selection](../decisions/ADR-001-ai-toolchain-selection.md)
- [Closing the Loop: Continuous State Management](../CLOSING-THE-LOOP.md)
- [Initial service architecture pages](../services/README.md) (6 services touched by Phase 1)
- [Global ADR decision log](../decisions/README.md) with 9 promoted ADRs (ADR-003 through ADR-011)

### Exit Criteria

- [ ] All 5 scenario playbooks executed on both toolchains
- [ ] Token usage and cost data collected for all scenarios
- [ ] Quality scored by at least one architect
- [ ] Cost model revised to include PROMOTE step workload
- [ ] ADR-001 records the selected toolchain with rationale

---

## Phase 2: AI-Integrated Architecture Workflow

**Timeline:** April - May 2026
**Status:** Planned
**Gate:** Workflow definition reviewed by architecture practice

### Milestones

| ID | Milestone | Target Date | Status | Dependencies |
|----|-----------|-------------|--------|--------------|
| 2.1 | Current workflow documented (as-is) | TBD | NOT STARTED | Phase 1 complete |
| 2.2 | AI integration points identified per workflow step | TBD | NOT STARTED | 2.1 |
| 2.3 | Optimized AI instruction set authored | TBD | NOT STARTED | 2.2 |
| 2.4 | Pilot: 3 real tickets processed with new workflow | TBD | NOT STARTED | 2.3 |
| 2.5 | Quality measurement framework validated | TBD | NOT STARTED | 2.4 |
| 2.6 | Workflow definition finalized | TBD | NOT STARTED | 2.4, 2.5 |
| 2.7 | PROMOTE step defined in to-be workflow | TBD | NOT STARTED | 2.1 |
| 2.8 | SC-06 playbook: AI-assisted post-implementation promotion | TBD | NOT STARTED | 2.7 |
| 2.9 | PROMOTE step tested on Phase 1 scenario outputs | TBD | NOT STARTED | 2.8 |

### Deliverables

- As-is workflow documentation
- To-be workflow with AI integration points **including the PROMOTE step**
- Optimized AI instruction library for the selected toolchain
- Quality measurement framework
- Pilot results report
- **SC-06 playbook: Post-Implementation Promotion** (new scenario type)

### Exit Criteria

- [ ] End-to-end workflow defined (ticket intake **through promotion** — not just through publication)
- [ ] AI instructions produce consistently compliant outputs
- [ ] Quality metrics established with baseline measurements
- [ ] At least 3 real tickets processed successfully with new workflow
- [ ] PROMOTE step tested: corporate baselines updated, ADRs promoted, service pages refreshed

---

## Phase 3: DocFlow v5 Pipeline Integration

**Timeline:** May - June 2026
**Status:** Planned
**Gate:** Pipeline successfully publishes artifacts from CI/CD

### Milestones

| ID | Milestone | Target Date | Status | Dependencies |
|----|-----------|-------------|--------|--------------|
| 3.1 | Pipeline-mode publishing specification | TBD | NOT STARTED | Phase 2 complete |
| 3.2 | Validation gate rules defined | TBD | NOT STARTED | 2.3 |
| 3.3 | DocFlow headless mode implemented | TBD | NOT STARTED | 3.1 |
| 3.4 | Pre-publish validation integrated | TBD | NOT STARTED | 3.2, 3.3 |
| 3.5 | Artifact manifest specification | TBD | NOT STARTED | 3.1 |
| 3.6 | Incremental publishing implemented | TBD | NOT STARTED | 3.3, 3.5 |
| 3.7 | End-to-end pipeline demonstrated | TBD | NOT STARTED | 3.4, 3.6 |
| 3.8 | Staleness detection: flag services with stale baselines | TBD | NOT STARTED | 3.4 |
| 3.9 | Promotion-completeness check in deploy gates | TBD | NOT STARTED | 3.4, 2.7 |

### Deliverables

- DocFlow v5 pipeline-mode extensions
- CI/CD pipeline definition (publish on merge to main)
- Validation rule set (arc42 structure, C4 compliance, ADR completeness)
- Artifact manifest specification and generator
- Incremental publish capability
- **Staleness detection for corporate architecture baselines**
- **Promotion-completeness gate** (warn/block deploys without baseline updates)

### Exit Criteria

- [ ] Architecture artifacts publish automatically on merge
- [ ] Validation gates prevent non-compliant artifacts from publishing
- [ ] Cross-links resolve correctly in published output
- [ ] Only changed artifacts are re-published (incremental)
- [ ] Stale service baselines flagged automatically (>90 days without update)

---

## Phase 4: Navigable Architecture Artifact Graph

**Timeline:** June - July 2026
**Status:** Planned
**Gate:** Prototype demonstrates clickable component navigation

### Milestones

| ID | Milestone | Target Date | Status | Dependencies |
|----|-----------|-------------|--------|--------------|
| 4.1 | Publishing target evaluation (Confluence vs static site vs hybrid) | TBD | NOT STARTED | Phase 3 complete |
| 4.2 | ADR for publishing target selection | TBD | NOT STARTED | 4.1 |
| 4.3 | Artifact relationship model defined | TBD | NOT STARTED | 3.5 |
| 4.4 | Navigable prototype (10 interconnected artifacts) | TBD | NOT STARTED | 4.2, 4.3 |
| 4.5 | Clickable diagram components implemented | TBD | NOT STARTED | 4.4 |
| 4.6 | Search across artifact graph | TBD | NOT STARTED | 4.4 |
| 4.7 | Migration path from Confluence documented | TBD | NOT STARTED | 4.5, 4.6 |
| 4.8 | Bidirectional traceability: spec ↔ decision ↔ ticket | TBD | NOT STARTED | 4.3 |

### Deliverables

- Publishing target evaluation and ADR
- Artifact relationship model (component-to-spec, spec-to-decision, decision-to-diagram)
- Navigable prototype with clickable components
- Cross-artifact search capability
- Confluence migration path
- **Bidirectional traceability** from corporate artifacts back to the decisions/tickets that created them

### Exit Criteria

- [ ] Click on a component in a diagram, navigate to that component's architecture page
- [ ] Click on a component's page, navigate to related API specs, decisions, diagrams
- [ ] Search for a domain concept, find all related artifacts
- [ ] Migration path from Confluence is documented and feasible

---

## Phase 5: Continuous Improvement Loop

**Timeline:** July - August 2026
**Status:** Planned
**Gate:** Quality metrics trending upward over 3 architecture cycles

### Milestones

| ID | Milestone | Target Date | Status | Dependencies |
|----|-----------|-------------|--------|--------------|
| 5.1 | Quality metrics defined and instrumented | TBD | NOT STARTED | Phase 4 complete |
| 5.2 | AI instruction versioning process established | TBD | NOT STARTED | 2.6 |
| 5.3 | Template library with contribution workflow | TBD | NOT STARTED | 5.1 |
| 5.4 | Architecture health scorecard | TBD | NOT STARTED | 5.1, 5.3 |
| 5.5 | 3 architecture cycles measured and improved | TBD | NOT STARTED | 5.4 |
| 5.6 | Measure investigation time reduction vs. pre-promotion baseline | TBD | NOT STARTED | 5.1 |
| 5.7 | Track architecture freshness scores across all services | TBD | NOT STARTED | 5.4, 3.8 |

### Deliverables

- Quality metrics dashboard or report
- AI instruction versioning and refinement process
- Template library with architect contribution workflow
- Architecture health scorecard

### Exit Criteria

- [ ] Quality metrics tracked across at least 3 complete architecture cycles
- [ ] AI instructions refined based on measured quality gaps
- [ ] Template library populated with reusable patterns
- [ ] Demonstrable improvement trend in architecture quality metrics

---

## Phase 6: Documentation Publishing Platform

**Timeline:** March - April 2026 (parallel with Phase 1 completion)
**Status:** Planned
**Gate:** Architecture documentation live on Azure Static Web Apps
**Decision:** [ADR-002: Documentation Publishing Platform](../decisions/ADR-002-documentation-publishing-platform.md)

### Milestones

| ID | Milestone | Target Date | Status | Dependencies |
|----|-----------|-------------|--------|--------------|
| 6.1 | MkDocs Material local site rendering all workspace markdown | 2026-03-24 | NOT STARTED | None |
| 6.2 | Azure Static Web App provisioned | 2026-03-28 | NOT STARTED | None |
| 6.3 | GitHub Actions CI/CD pipeline deploying on push | 2026-03-31 | NOT STARTED | 6.1, 6.2 |
| 6.4 | Content enhancement (tags, search, attribution, PDF export) | 2026-04-07 | NOT STARTED | 6.3 |
| 6.5 | Workflow integration (PR validation, link checking, versioning) | 2026-04-14 | NOT STARTED | 6.4 |
| 6.6 | ADR-002 Documentation Publishing Platform decision recorded | 2026-03-21 | PROPOSED | None |

### Deliverables

- `mkdocs.yml` site configuration mapping repo structure to navigable documentation
- `.github/workflows/docs-deploy.yml` CI/CD pipeline
- Live documentation site on Azure Static Web Apps
- PlantUML and Mermaid diagram rendering inline
- Full-text search, tags, git attribution, PDF export
- [Detailed implementation plan](../phase-6-documentation-publishing/PUBLISHING-PLATFORM-PLAN.md)

### Exit Criteria

- [ ] All existing markdown renders correctly on the published site
- [ ] PlantUML and Mermaid diagrams render inline
- [ ] Push to main auto-deploys in under 5 minutes
- [ ] Full-text search works across all documents
- [ ] PR preview environments generate staging URLs
- [ ] Site scores >90 on Lighthouse performance

---

## Decisions Register

Formal architecture decisions are documented using the MADR (Markdown Any Decision Records) format and stored in the [decisions/](../decisions/) directory.

| ID | Decision | Phase | Status | Date |
|----|----------|-------|--------|------|
| ADR-001 | [AI Toolchain Selection](../decisions/ADR-001-ai-toolchain-selection.md) | Phase 1 | PROPOSED | 2026-03-01 |
| ADR-002 | [Documentation Publishing Platform](../decisions/ADR-002-documentation-publishing-platform.md) | Phase 6 | PROPOSED | 2026-03-21 |
| ADR-003 | Publishing Target Selection | Phase 4 | FUTURE | TBD |
| ADR-004 | Artifact Relationship Model | Phase 4 | FUTURE | TBD |

---

## Risk Register

| ID | Risk | Impact | Likelihood | Mitigation | Phase |
|----|------|--------|------------|------------|-------|
| R1 | Kong AI pricing changes during evaluation | Cost comparison becomes outdated | Medium | Document pricing snapshot date; re-validate before final recommendation | 1 |
| R2 | GitHub Copilot premium model limits too restrictive for architecture work | Cannot complete scenarios within included quota | Medium | Track overage costs separately; include in comparison | 1 |
| R3 | AI output quality insufficient for architecture standards | Architects reject AI-assisted workflow | Low | Quality measurement framework in Phase 2 catches this early | 2 |
| R4 | DocFlow pipeline mode requires significant refactoring | Phase 3 timeline extends | Medium | Evaluate scope during Phase 2; adjust timeline if needed | 3 |
| R5 | Confluence limitations cannot be overcome for artifact graph | Phase 4 must use alternative target | High | Phase 4 explicitly evaluates alternatives; this is not a surprise | 4 |
| R6 | Adoption resistance from architecture practice | Platform built but not used | Medium | Involve architects from Phase 2 onward; demonstrate value with real tickets | 2-5 |
