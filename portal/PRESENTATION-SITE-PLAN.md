# Presentation Site Plan — Continuous Architecture Platform Pitch Deck

> **Purpose:** Build a third MkDocs Material site as an executive presentation selling the Continuous Architecture Platform for organizational adoption.
>
> **Date:** 2026-03-05
>
> **Status:** DRAFT

---

## 1. Objective

Create a standalone MkDocs Material presentation site that makes the case for adopting the Continuous Architecture Platform. The audience is engineering leadership, enterprise architecture leadership, and budget holders. The site itself serves as a live demo of the platform's publishing capability.

The presentation argues for four interconnected decisions:

1. **Adopt an all-you-can-eat AI platform (GitHub Copilot Pro+)** instead of per-token models like Roo Code + OpenRouter
2. **Keep everything in a shared architecture workspace** so the AI model sees full context — specs, decisions, diagrams, service pages — in VS Code
3. **Move solution designs to Markdown** (replacing Word/Confluence-first authoring) so they are version-controlled, diffable, and AI-readable
4. **Publish via CI/CD pipeline to MkDocs** (with optional Confluence sync) so architecture documentation is living and always current

---

## 2. Site Technology

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Framework | MkDocs Material | Same stack as the architecture portal — dogfooding |
| Theme features | Navigation tabs, content tabs, admonitions, data tables | Presentation-grade formatting without PowerPoint |
| Presentation plugin | None — use MkDocs pages as "slides" with dense content per page | Avoids reveal.js complexity; pages are self-contained and linkable |
| Deployment | Azure Static Web Apps (same infra as portal) | Free tier, instant deploy, shareable URL |
| Source location | `presentation/` directory in this repo | Alongside `portal/` and `docs/` |

---

## 3. Site Structure — Slide-by-Slide Outline

### 3.1 Landing Page — The Pitch in 60 Seconds

**File:** `docs/index.md`

- One-sentence thesis: "We can give every architect an AI assistant that produces 96% standards-compliant work for $39/month — and we've already proven it."
- Three proof points as hero cards:
  - 208x cheaper per run vs per-token models
  - 96.1% quality score across 5 real-world scenarios
  - 184 SVG diagrams auto-generated from a single workspace
- Call to action: "See the evidence" navigation

### 3.2 The Problem — Why Architecture Documentation Decays

**File:** `docs/problem.md`

Content:
- Architecture designs document a moment in time, get published to Confluence, then decay
- Teams rediscover system architecture from source code instead of updated docs
- No reliable navigation between related artifacts (spec to diagram to ADR to service page)
- The "last mile" gap: projects produce architecture artifacts but never promote them to the corporate baseline
- Evidence: from CLOSING-THE-LOOP.md — 9 ADRs created across 5 scenarios, 0 promoted to global decision log (95%+ gap rate)

### 3.3 The Solution — Continuous Architecture Platform

**File:** `docs/solution.md`

Content:
- Replace point-in-time documentation with living, interconnected architecture artifacts
- Four pillars:
  1. AI-assisted architecture workflows in VS Code
  2. Shared workspace with full context (specs, decisions, diagrams, source code)
  3. Markdown-first authoring (version-controlled, diffable, AI-readable)
  4. Automated publishing via CI/CD (MkDocs + optional Confluence sync)
- Diagram: high-level flow from ticket to published architecture page
- Reference the 6-phase roadmap

### 3.4 Cost Evidence — The 208x Difference

**File:** `docs/cost-evidence.md`

Content (all from actual billing data):
- Head-to-head comparison table: Copilot Pro+ vs Roo Code + OpenRouter
  - Same model (Claude Opus 4.6), same workspace, same 5 scenarios
  - Copilot: $0.48/run, $39/month fixed | OpenRouter: ~$100/run, ~$507/month variable
  - 208x cheaper per run, 13x cheaper monthly
- Billing model discovery: Copilot bills per user prompt, not per model turn
  - Tool calls, file reads, terminal commands, sub-agents = FREE (absorbed by GitHub)
  - 4-prompt session = 4 x 3 multiplier x $0.04 = $0.48
- Context window efficiency: Roo Code wastes 16.3% of context on metadata overhead per turn
- Budget predictability: fixed $39/month vs variable costs that scale with usage
- Chart: cost projection at 10, 20, 38, 50 runs/month showing Copilot flat line vs OpenRouter linear growth

### 3.5 Quality Evidence — 96.1% on First Execution

**File:** `docs/quality-evidence.md`

Content (all from Phase 1 execution results):
- Scorecard across 5 scenarios:
  - SC-01 Ticket Triage: 23/25 (92%)
  - SC-02 Classification Design: 33/35 (94%)
  - SC-03 Investigation: 30/30 (100%)
  - SC-04 Architecture Update: 24/25 (96%)
  - SC-05 Complex Cross-Service: 39/40 (98%)
  - **Total: 149/155 (96.1%)**
- What was produced: 39 files, 9 MADR ADRs, PlantUML diagrams, Swagger spec updates
- Copilot vs Roo Code quality comparison:
  - Copilot: zero fabrication, 39 files, all standards-compliant
  - Roo Code: fabricated 4 OpenAPI schema elements in Scenario 4, missed 2 required files
- Standards enforced automatically: arc42, MADR, C4 Model, ISO 25010

### 3.6 The Shared Workspace — AI Sees What the Architect Sees

**File:** `docs/shared-workspace.md`

Content:
- Workspace-as-context: the AI model in VS Code reads the same specs, ADRs, service pages, and diagrams the architect uses
- copilot-instructions.md: 500+ lines of domain knowledge, bounded context rules, data ownership, mock tool commands — loaded automatically into every AI session
- Evidence from POC:
  - 19 OpenAPI specs analyzed and cross-referenced by AI during scenario execution
  - Source code anti-patterns identified with specific line numbers
  - Cross-service data flow traced through API contracts
- The flywheel: as the workspace grows with more artifacts, every AI session gets richer context at zero additional cost (Copilot's fixed pricing)
- Comparison with Confluence-first: AI cannot read Confluence pages during architecture work; workspace-first means full context is always available

### 3.7 Markdown-First Architecture — Why It Matters

**File:** `docs/markdown-first.md`

Content:
- Markdown is version-controlled (git diff shows exactly what changed in a design)
- Markdown is AI-readable (the model can analyze, update, and cross-reference designs)
- Markdown is publishable (MkDocs, Confluence API, PDF export — write once, publish anywhere)
- Markdown is reviewable (pull request reviews on architecture changes, not comment threads on Confluence)
- Evidence: every artifact in this POC is Markdown — ADRs, solution designs, impact assessments, user stories, service pages
- Migration path: existing Confluence content can be exported to Markdown; new work starts in Markdown immediately
- Template standards preserved: arc42 sections, MADR format, C4 diagram notation — all work natively in Markdown

### 3.8 CI/CD Publishing — Living Documentation

**File:** `docs/publishing-pipeline.md`

Content:
- The pipeline: `git push` to main triggers MkDocs build and deploys to Azure Static Web Apps
- What gets published automatically:
  - 19 microservice deep-dive pages with 139 endpoint sequence diagrams
  - 3 application consumer pages with 25 integration diagrams
  - Enterprise C4 system context diagram with PCI DSS compliance zone
  - Per-service C4 context diagrams with clickable drill-down links
  - 19 Swagger UI pages with inline OpenAPI specs
  - Global ADR decision log (11 decisions)
  - Service architecture baselines
- Portal artifact inventory (built by AI from this workspace):
  - 57 Markdown pages
  - 184 PlantUML source files rendered to SVG
  - 19 Swagger UI HTML pages
  - 19 downloadable OpenAPI YAML specs
- Confluence sync option: publish the same Markdown to Confluence via API (for organizations that require it) — single source of truth in git, rendered copies in both MkDocs and Confluence
- Zero manual publishing: no copy-paste, no screenshot updates, no broken cross-links

### 3.9 Live Demo — The Architecture Portal

**File:** `docs/live-demo.md`

Content:
- Link to the live portal: `https://mango-sand-083b8ce0f.4.azurestaticapps.net`
- Guided tour of key pages:
  - Enterprise C4 diagram with clickable services and PCI compliance zone
  - Microservice deep-dive page (e.g., svc-check-in) with endpoint sequence diagrams
  - Swagger UI page with interactive API documentation
  - Cross-service navigation: click a relationship arrow in a C4 diagram to jump to the target service's endpoint
  - Fullscreen diagram view with breadcrumb navigation back
- Everything on this portal was generated by AI from OpenAPI specs + workspace context
- Screenshot/annotated walkthrough for offline viewing

### 3.10 Closing the Loop — The PROMOTE Step

**File:** `docs/closing-the-loop.md`

Content:
- The gap: architecture designs describe a target state, but after deployment, corporate baselines are never updated
- Evidence: 9 ADRs created in Phase 1, 0 promoted to global decision log
- The PROMOTE workflow:
  1. After deployment, AI updates OpenAPI specs to match implemented changes
  2. ADRs from ticket-level decisions are promoted to global decision log
  3. Service architecture pages are refreshed with new integration points
  4. Solution design is marked PROMOTED with date and version
- Cost impact: adds 12 runs/month (26 to 38); Copilot still $39/month, OpenRouter adds ~$13/month
- This is the innovation that transforms architecture from point-in-time to continuous

### 3.11 Roadmap — What Comes Next

**File:** `docs/roadmap.md`

Content:
- 6-phase delivery timeline:
  - Phase 1: AI toolchain comparison — COMPLETE
  - Phase 6: Documentation publishing platform — COMPLETE (the portal is live)
  - Phase 2: AI-integrated workflow design (April-May 2026)
  - Phase 3: Pipeline integration with validation gates (May-June 2026)
  - Phase 4: Navigable artifact graph (June-July 2026)
  - Phase 5: Continuous improvement loop with quality metrics (July-August 2026)
- Each phase delivers standalone value
- Full vision by August 2026

### 3.12 The Ask — What We Need to Move Forward

**File:** `docs/the-ask.md`

Content:
- Approval for GitHub Copilot Pro+ licenses for the architecture practice ($39/seat/month)
- Agreement to adopt Markdown-first authoring for new solution designs (no workflow disruption — same content, different format)
- CI/CD pipeline access for automated MkDocs publishing (Azure Static Web Apps free tier)
- Optional: Confluence API access for dual-publish capability
- Pilot scope: start with one team/domain, measure quality and adoption, then expand
- Risk profile: low cost ($39/month), reversible (Markdown is portable), proven (96.1% quality demonstrated)

---

## 4. Visual Design and Theme

| Element | Specification |
|---------|---------------|
| Color palette | Professional blue/teal primary, high-contrast data tables |
| Custom CSS | Larger headings, card-style callouts for key metrics, full-width tables |
| Admonitions | `success` for proven outcomes, `info` for evidence citations, `warning` for gaps/risks |
| Data visualization | Embedded comparison tables with color-coded cells (green = advantage) |
| Screenshots | Annotated portal screenshots for live demo section |
| Diagrams | Mermaid flowcharts for pipeline and workflow visualizations |

### MkDocs Configuration

```yaml
theme:
  name: material
  palette:
    primary: teal
    accent: amber
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.top
    - content.tabs.link

plugins:
  - search

markdown_extensions:
  - admonitions
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_mermaid
  - pymdownx.tabbed:
      alternate_style: true
  - tables
  - attr_list
  - md_in_html

extra_css:
  - stylesheets/presentation.css
```

---

## 5. Build and Deploy

### Directory Structure

```
presentation/
  mkdocs.yml
  docs/
    index.md
    problem.md
    solution.md
    cost-evidence.md
    quality-evidence.md
    shared-workspace.md
    markdown-first.md
    publishing-pipeline.md
    live-demo.md
    closing-the-loop.md
    roadmap.md
    the-ask.md
    stylesheets/
      presentation.css
    img/
      (annotated screenshots)
```

### Build Commands

```bash
cd presentation
pip install mkdocs-material
mkdocs build
```

### Deployment

Deploy to the secondary Azure Static Web App (docs site):

```bash
swa deploy site \
  --deployment-token "91924f1a91d99cefaaaa12b01684c854c9b4d1a49ef3ae4d2dd1ac1ddb24738a04-de4c54e1-f90d-4b5d-b7aa-dac46842447300f283206704740f" \
  --env production
```

Live URL: `https://victorious-mud-06704740f.4.azurestaticapps.net`

---

## 6. Content Source Mapping

Every claim in the presentation must cite workspace evidence. No fabricated numbers.

| Slide | Source File(s) |
|-------|---------------|
| Cost evidence | `phase-1-ai-tool-cost-comparison/COST-MEASUREMENT-METHODOLOGY.md`, `research/DEEP-RESEARCH-RESULTS-COPILOT-BILLING.md` |
| Quality scores | `phase-1-ai-tool-cost-comparison/outputs/copilot-vs-roocode-001-comparison.md` |
| Closing the loop | `CLOSING-THE-LOOP.md` |
| Toolchain decision | `decisions/ADR-001-ai-toolchain-selection.md` |
| Publishing platform | `decisions/ADR-002-documentation-publishing-platform.md`, `phase-6-documentation-publishing/PUBLISHING-PLATFORM-PLAN.md` |
| Roadmap | `roadmap/ROADMAP.md` |
| Context window analysis | `research/CONTEXT-WINDOW-UTILIZATION-ANALYSIS.md` |
| Portal artifact counts | Generated by `portal/scripts/generate-microservice-pages.py` and `generate-swagger-pages.py` |

---

## 7. Key Messages to Emphasize

1. **"208x cheaper per run — same model, same quality"** — The cost difference is not a projection. It is actual billing data from two runs against the same workspace using the same Claude Opus 4.6 model.

2. **"96.1% standards compliance on first execution"** — The AI produces arc42-compliant solution designs, MADR-formatted ADRs, and C4-notation diagrams automatically. 149 out of 155 quality checks passed.

3. **"The AI sees everything the architect sees"** — By keeping specs, decisions, diagrams, and service pages in a shared workspace, the AI model has full context. This is impossible with Confluence-first authoring.

4. **"Write once, publish everywhere"** — Markdown in git is the single source of truth. CI/CD publishes to MkDocs automatically. Confluence sync is optional. No manual copy-paste.

5. **"Closing the loop is the innovation"** — Every architecture practice fails to update baselines post-deployment. The PROMOTE step fixes this. Living documentation replaces decaying snapshots.

6. **"184 diagrams generated from specs"** — The architecture portal was generated entirely by AI from OpenAPI specs and workspace context. 19 microservice pages, 139 endpoint sequence diagrams, enterprise C4 with PCI compliance zone, interactive Swagger UI — all automated.

7. **"$39/month, fixed, predictable"** — No runaway costs. No token metering. No infrastructure to manage. Budget is locked regardless of usage volume.

---

## 8. Implementation Steps

| Step | Action | Dependency |
|------|--------|------------|
| 1 | Create `presentation/` directory structure | None |
| 2 | Write `mkdocs.yml` with navigation and theme config | None |
| 3 | Write `presentation.css` for presentation-grade styling | None |
| 4 | Write landing page (`index.md`) with hero metrics | None |
| 5 | Write problem statement page | None |
| 6 | Write solution overview page with architecture diagram | None |
| 7 | Write cost evidence page with comparison tables and charts | Source: cost methodology + billing research |
| 8 | Write quality evidence page with scorecard | Source: comparison output |
| 9 | Write shared workspace page | Source: copilot-instructions.md |
| 10 | Write markdown-first page | Source: workspace artifacts |
| 11 | Write publishing pipeline page with artifact inventory | Source: portal generators |
| 12 | Capture and annotate portal screenshots for live demo page | Requires portal deployed |
| 13 | Write closing-the-loop page | Source: CLOSING-THE-LOOP.md |
| 14 | Write roadmap page | Source: ROADMAP.md |
| 15 | Write the-ask page | All previous pages |
| 16 | Build and test locally (`mkdocs serve`) | Steps 1-15 |
| 17 | Deploy to Azure Static Web Apps | Step 16 |
| 18 | Share URL with stakeholders | Step 17 |
