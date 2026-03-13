# Continuous Architecture Platform POC

> Proof of concept for a continuous architecture platform that replaces point-in-time documentation with living, interconnected architecture artifacts that improve over time — powered by AI-assisted workflows, automated publishing pipelines, and navigable artifact graphs.

| | |
|-----------|-------|
| **Author** | Christopher Blaisdell |
| **Created** | 2026-02-28 |
| **Status** | Active |
| **Organization** | Architecture Practice |

> **DATA ISOLATION NOTICE:** This repository contains **zero corporate data**. All services, tickets, logs, and tools use the **NovaTrek Adventures** synthetic domain. JIRA, Elasticsearch, and GitLab integrations are **local mock scripts** that read from JSON files on disk — no network calls, no credentials, no corporate system access. See [Data Isolation](#data-isolation) below.

---

## The Problem

Architecture documentation today is written once and immediately begins to decay. Solution designs capture a moment in time, get published to Confluence, and are never updated as the system evolves. Within months, the documented architecture no longer reflects reality. Teams make decisions based on stale diagrams. New architects onboard against outdated artifacts. There is no reliable way to navigate from one artifact to a related artifact — if you are looking at a component diagram and want to see the API contract for that component, you search Confluence manually and hope you find the right page.

Additionally, the current publishing workflow depends entirely on Confluence, which imposes a flat page hierarchy and does not natively support rich cross-linking between architecture artifacts. Clicking on a component in a diagram should take you to that component's architecture page, but Confluence makes this difficult to achieve and impossible to maintain at scale.

---

## The Vision

A **continuous architecture platform** where:

1. **Architecture is living, not point-in-time.** Artifacts are continuously updated as systems evolve. Every solution design, component diagram, API contract, and decision record stays current because the workflow makes updates the path of least resistance.

2. **Artifacts are interconnected and navigable.** You can click on a component in an architecture diagram and navigate directly to that component's API specification, decision records, quality attributes, and deployment view. The artifact graph is maintained automatically, not manually.

3. **AI accelerates every workflow step.** From ticket triage to solution design to publishing, AI-assisted tooling reduces the time and effort per artifact while increasing quality and standards compliance.

4. **Publishing pipelines automate delivery.** Architecture artifacts flow through automated pipelines — from local workspace to published platform — with validation gates, cross-link resolution, and format conversion handled automatically.

5. **The platform improves itself over time.** Each architecture cycle feeds back into the platform: better templates, better AI instructions, better cross-references, better standards compliance. The cost of maintaining architecture decreases as the corpus grows.

---

## Project Phases

### Phase 1: AI Tool Cost Comparison

**Status:** Synthetic workspace complete, ready for execution

**Objective:** Determine the monthly cost per architect seat for Roo Code + Kong AI versus GitHub Copilot by executing representative architecture workflows against both toolchains using synthetic data.

**Why this is first:** Before investing in platform capabilities, we need to select the AI toolchain that will power the workflow. This phase produces a defensible cost-per-seat comparison with quality metrics, giving leadership the data to make a tooling decision.

**Deliverables:**
- Synthetic workspace (NovaTrek Adventures domain) with 19 microservices, 5 tickets, architecture standards
- 5 scenario playbooks for controlled comparison
- Monthly cost-per-seat calculation for each option
- Quality and standards compliance comparison

**Details:** See [phases/phase-1-ai-tool-cost-comparison/AI-TOOL-COST-COMPARISON-PLAN.md](phases/phase-1-ai-tool-cost-comparison/AI-TOOL-COST-COMPARISON-PLAN.md)

---

### Phase 2: AI-Integrated Architecture Workflow

**Status:** Planned

**Objective:** Redesign the end-to-end architecture workflow to incorporate AI at every step, using the toolchain selected in Phase 1. Define the optimal human-AI collaboration pattern for each workflow stage.

**Key questions to answer:**
- What is the ideal prompt strategy for each workflow step (ticket triage, investigation, solution design, review, publishing)?
- How should AI instructions be structured to enforce architecture standards automatically?
- What is the right balance between AI generation and human review at each stage?
- How do we measure and continuously improve AI output quality?

**Deliverables:**
- Optimized AI instruction set for the selected toolchain
- Workflow definition covering ticket-to-publication lifecycle
- Quality measurement framework for AI-assisted architecture outputs
- Feedback loop design for continuous improvement of AI instructions

---

### Phase 3: DocFlow v5 Pipeline Integration

**Status:** Planned

**Objective:** Extend DocFlow v5 to support automated publishing pipelines that validate, cross-link, and deliver architecture artifacts without manual intervention.

**Current DocFlow v5 capabilities (foundation to build on):**
- Markdown-to-Confluence publishing with recursive child page support
- Two-pass cross-link resolution (file references become Confluence page links)
- Anchor-based in-page navigation (headings become linkable anchors)
- PlantUML-to-SVG generation with automatic image upload
- Overwrite protection with diff reports (F5001/F5002)
- Confluence hierarchy preservation on extraction
- JIRA ticket extraction and workspace scaffolding

**New capabilities to add:**
- **Pipeline mode**: Headless publishing triggered by CI/CD (no VS Code UI required)
- **Validation gates**: Pre-publish checks for standards compliance (arc42 structure, C4 diagram rules, ADR completeness)
- **Artifact manifest**: Machine-readable index of all published artifacts with metadata and relationships
- **Incremental publishing**: Detect and publish only changed artifacts, preserving stable cross-links
- **Bidirectional sync**: Detect external Confluence edits and merge them back to the source-of-truth workspace

**Deliverables:**
- DocFlow v5 extensions for pipeline-mode publishing
- CI/CD pipeline definitions (GitHub Actions or equivalent)
- Validation rule set aligned with architecture standards
- Artifact manifest specification

---

### Phase 4: Navigable Architecture Artifact Graph

**Status:** Planned

**Objective:** Create a publishing target that supports rich, navigable cross-linking between architecture artifacts — overcoming the limitations of Confluence's flat page hierarchy.

**The Confluence limitation:** Confluence organizes content as a tree of pages. Cross-linking between pages requires manual URL insertion, and there is no native concept of "this component in Diagram A links to Page B's Component section." When artifacts are reorganized or renamed, links break silently. Building a navigable artifact graph on Confluence requires constant manual maintenance that does not scale.

**Approaches to evaluate:**
- **Enhanced Confluence publishing**: Push the limits of Confluence macros, page properties, and anchor links to create richer navigation within the existing platform
- **Static site generator**: Publish architecture artifacts as a navigable static site (e.g., using MkDocs, Docusaurus, or a custom generator) with automatic cross-linking, search, and diagram interaction
- **Hybrid approach**: Continue publishing to Confluence for discoverability while maintaining a parallel navigable site for deep navigation
- **Custom artifact browser**: A purpose-built web application that renders the artifact graph with clickable diagram components, breadcrumb navigation, and semantic search

**Target experience:**
- View a system context diagram; click on any component to navigate to its architecture page
- View a component's architecture page; see links to all related API specs, decision records, sequence diagrams, and quality attributes
- Search for "reservation" and see all artifacts across all architecture views that reference the reservation domain
- View an API specification and click through to the component that owns it, the decisions that shaped it, and the sequence diagrams that exercise it

**Deliverables:**
- Evaluation of publishing targets (Confluence enhanced vs. static site vs. hybrid vs. custom)
- Selected approach with architectural decision record
- Navigable artifact prototype with cross-linked components
- Migration path from current Confluence-only publishing

---

### Phase 5: Continuous Improvement Loop

**Status:** Planned

**Objective:** Close the loop so that each architecture cycle makes the platform better — better AI instructions, better templates, better artifact relationships, better publishing quality.

**Key mechanisms:**
- **Architecture quality metrics**: Track standards compliance, artifact freshness, cross-link completeness, and navigation coverage over time
- **AI instruction refinement**: Use quality metrics and architect feedback to iteratively improve AI prompts, instructions, and standards enforcement
- **Template evolution**: As patterns emerge from completed designs, extract them into reusable templates
- **Artifact relationship enrichment**: As the corpus grows, discover and codify relationships between artifacts that were not explicitly linked

**Deliverables:**
- Quality metrics dashboard (or reporting mechanism)
- AI instruction versioning and improvement process
- Template library with contribution workflow
- Architecture health scorecard

---

## Guiding Principles

| Principle | Description |
|-----------|-------------|
| **Source of truth in code** | Architecture artifacts live in version-controlled workspaces, not in Confluence. Confluence is a publishing target, not the authoring environment. |
| **Standards as guardrails, not gatekeeping** | Public frameworks (arc42, C4, MADR) provide structure. AI enforces compliance automatically. Architects focus on decisions, not formatting. |
| **Incremental value** | Each phase delivers standalone value. Phase 1 produces a cost comparison even if later phases are never executed. |
| **Zero proprietary data in POC** | All proof-of-concept work uses synthetic data (NovaTrek Adventures domain). No corporate data exists in this repository. See [Data Isolation](#data-isolation). |
| **Measure everything** | Every phase defines measurable outcomes. Progress is tracked with data, not opinions. |

---

## Key Documents

| Document | Purpose |
|----------|---------|
| [Roadmap](docs/roadmap/ROADMAP.md) | Phased timeline with milestones, deliverables, exit criteria, and risk register |
| [Closing the Loop](docs/CLOSING-THE-LOOP.md) | Analysis of the gap between point-in-time architecture and continuous state management, with a plan to fix it |
| [ADR-001: AI Toolchain Selection](decisions/ADR-001-ai-toolchain-selection.md) | Formal decision record for Kong AI vs GitHub Copilot |
| [ADR-002: Documentation Publishing Platform](decisions/ADR-002-documentation-publishing-platform.md) | Decision record for Material for MkDocs on Azure Static Web Apps |
| [Context Window Utilization Analysis](research/CONTEXT-WINDOW-UTILIZATION-ANALYSIS.md) | Empirical analysis of Roo Code vs Copilot context window efficiency |
| [Phase 1 Plan](phases/phase-1-ai-tool-cost-comparison/AI-TOOL-COST-COMPARISON-PLAN.md) | Detailed plan for AI cost comparison with synthetic workspace |
| [Phase 1 Outputs](phases/phase-1-ai-tool-cost-comparison/outputs/README.md) | Run-by-run results for Copilot and Roo Code executions |
| [Publishing Platform Plan](phases/phase-6-documentation-publishing/PUBLISHING-PLATFORM-PLAN.md) | Material for MkDocs → Azure Static Web Apps implementation plan |
| [Architecture Decision Log](decisions/README.md) | Global index of all 11 architecture decisions with service and status views |
| [Cost Measurement Methodology](phases/phase-1-ai-tool-cost-comparison/COST-MEASUREMENT-METHODOLOGY.md) | Autonomous cost measurement approach, tool, and Copilot execution analysis |

---

## Data Isolation

This repository is designed to contain **absolutely no corporate data**. Every artifact is synthetic.

| Component | What It Looks Like | What It Actually Is |
|-----------|-------------------|--------------------|
| JIRA tickets | `python scripts/mock-jira-client.py --ticket NTK-10005` | Local Python script reading `mock-data/tickets.json` — no network, no credentials |
| Elasticsearch logs | `python scripts/mock-elastic-searcher.py --service svc-scheduling-orchestrator` | Local Python script reading `mock-data/elastic-logs.json` — no network, no credentials |
| GitLab merge requests | `python scripts/mock-gitlab-client.py --mr 5001` | Local Python script reading `mock-data/merge-requests.json` — no network, no credentials |
| Microservices (19) | OpenAPI specs + Java source code | 100% synthetic NovaTrek Adventures domain |
| Architecture decisions | ADR-003 through ADR-011 | Decisions about synthetic services, not real systems |
| Service pages | `services/svc-check-in.md` etc. | Architecture baselines for synthetic services |

**All three mock tools:**
- Use **Python stdlib only** (no `requests`, no API clients)
- Read from **local JSON files** in `scripts/mock-data/`
- Require **no credentials, tokens, or network access**
- Are designed so the AI under test cannot distinguish them from real CLI tools

**Pre-commit audit:** Run `./portal/scripts/utilities/audit-data-isolation.sh` to verify no corporate data has leaked in. This script checks all tracked files against a pattern list of known corporate identifiers.

---

## Repository Structure

```
continuous-architecture-platform-poc/
  README.md                                         # This document (project vision)
  docs/
    roadmap/
      ROADMAP.md                                      # Phased roadmap with milestones and timeline
    CLOSING-THE-LOOP.md                               # Analysis of point-in-time vs continuous architecture
    decisions/                                        # Symlink to decisions/ for MkDocs
    research/                                         # Symlink to research/ for MkDocs
  decisions/
    README.md                                       # Global decision log (index of all ADRs)
    ADR-001-ai-toolchain-selection.md               # Kong AI vs GitHub Copilot decision
    ADR-002-documentation-publishing-platform.md    # Material for MkDocs selection
    ADR-003 through ADR-011                         # 9 promoted Phase 1 service decisions
  research/
    CONTEXT-WINDOW-UTILIZATION-ANALYSIS.md           # Roo Code vs Copilot context window efficiency
  architecture/
    scripts/
      ticket-client.py                              # CLI for querying architecture metadata
      mcp-vikunja-server.py                         # MCP server for AI tool integration
      sync-branch-status.py                         # Sync ticket status from branches
      generate-calm.py                              # Auto-generate CALM topology from metadata
      validate-calm.py                              # Validate CALM topology in CI
      vikunja-seed.py                               # Seed Vikunja with tickets and labels
      init-schemas.sql                              # Database schema initialization
  portal/
    scripts/
      utilities/
        cost-measurement.py                         # Autonomous cost measurement tool (stdlib only)
        audit-data-isolation.sh                     # Pre-commit data isolation audit
  phases/
    phase-1-ai-tool-cost-comparison/                # AI tool cost comparison (synthetic workspace + plan)
      AI-TOOL-COST-COMPARISON-PLAN.md               # Detailed Phase 1 plan
      COST-MEASUREMENT-METHODOLOGY.md               # Cost measurement approach, analysis, and results
      workspace/                                    # Portable synthetic workspace for Phase 1 execution
        novatrek-workspace.code-workspace
        architecture-standards/
        corporate-services/
        source-code/
        work-items/
        scripts/
        playbooks/
        scenario-playbooks/
        ...
    phase-2-ai-workflow/                            # (future) AI-integrated workflow design
    phase-3-ci-pipelines/                           # (future) CI/CD pipeline extensions
    phase-4-artifact-graph/                         # (future) Navigable architecture artifact graph
    phase-5-continuous-improvement/                 # (future) Quality metrics and feedback loops
    phase-6-documentation-publishing/               # Documentation publishing platform
```
