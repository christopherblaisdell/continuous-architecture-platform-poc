# NovaTrek Adventures — Continuous Architecture Platform Roadmap

| | |
|-----------|-------|
| **Author** | Christopher Blaisdell |
| **Date** | 2026-03-06 |
| **Status** | Approved |
| **Purpose** | Consolidated roadmap and implementation plan for the Continuous Architecture Platform — combining capability mapping, ticketing integration, solution design lifecycle, and portal publishing into a phased delivery plan |

---

## 1. Vision

The Continuous Architecture Platform replaces point-in-time architecture documentation with a **living, interconnected architecture knowledge base** that grows with every ticket. The platform ensures that:

- Every solution design is published, indexed, and cross-linked
- Business capabilities accumulate intelligence from every ticket
- Architecture decisions maintain full traceability from ticket to capability
- AI agents can discover prior art, detect conflicts, and suggest capability mappings
- The portal is the single source of truth for NovaTrek Adventures architecture

**The core insight:** Architecture amnesia — where valuable solution designs are produced, reviewed, approved, and then forgotten — is eliminated by making capability rollup a natural byproduct of the solution design workflow, enforced by branch protection and PR review.

---

## 2. Current State

### What Exists

| Component | Status | Location |
|-----------|--------|----------|
| NovaTrek Architecture Portal | Deployed | Azure Static Web Apps (primary portal) |
| Docs Site | Deployed | Azure Static Web Apps (project documentation) |
| OpenAPI Specs | 19 service specs | `architecture/specs/` |
| Microservice Pages | 19 generated pages with sequence diagrams | `portal/docs/microservices/` |
| Architecture Decisions | 11 ADRs (ADR-001 through ADR-011) | `decisions/` |
| Event Catalog | 6 producers, 7 events | `architecture/events/` |
| Actor Catalog | System actors | `architecture/metadata/actors.yaml` |
| Applications | 3 app pages with wireframes | `portal/docs/applications/` |
| Service Catalog | 21 services | `portal/docs/services/` |
| Phase 1 Evaluation | 5 scenarios compared (Copilot vs Roo Code) | `phases/phase-1-ai-tool-cost-comparison/` |
| Mock Tools | JIRA, Elastic, GitLab (local Python scripts, no network) | `phases/.../workspace/scripts/` |
| Solution Design Template | Copied and published | `portal/docs/standards/solution-design/` |

### What Is Missing

| Gap | Impact | Addressed In |
|-----|--------|-------------|
| No capability map | Cannot trace business needs to services | Phase 1 |
| No solution design publishing | Designs invisible after tickets close | Phase 2 |
| No ticketing integration | No structured user stories, no capability tagging | Phase 3 |
| No capability rollup | Architecture resets instead of growing | Phase 2 |
| No branch-per-solution workflow | No review gate, no CI validation | Phase 1 |
| No ADR promotion | Ticket-scoped decisions invisible globally | Phase 2 |
| Corporate data in template | Solution design template has corporate URLs | Phase 0 |
| No Confluence mirror | Enterprise stakeholders cannot consume architecture docs in their standard wiki | Phase 6 |

---

## 3. Business Capability Map

NovaTrek Adventures has 7 Level 1 capability domains encompassing 34 Level 2 capabilities.

### Coverage Summary

| Status | Count | Percentage |
|--------|-------|-----------|
| Implemented | 24 | 70.6% |
| Partial | 4 | 11.8% |
| Not Implemented | 6 | 17.6% |

### Level 1 Domains

| Domain | L2 Capabilities | Implemented | Partial | Gaps |
|--------|----------------|-------------|---------|------|
| Guest Experience | 8 | 6 | 0 | 2 (Reviews, Recommendations) |
| Adventure Operations | 5 | 5 | 0 | 0 |
| Safety and Risk | 5 | 5 | 0 | 0 |
| Resource Management | 5 | 4 | 0 | 1 (Facility Management) |
| Revenue and Finance | 5 | 2 | 3 | 0 |
| Partner Ecosystem | 3 | 1 | 1 | 1 (Channel Rate Parity) |
| Platform Services | 3 | 2 | 0 | 1 (Search Engine) |

### Priority Gaps

| Capability | Priority | Rationale |
|-----------|----------|-----------|
| 1.7 Reviews and Feedback | HIGH | Guest trip reviews drive bookings; no social proof mechanism |
| 5.5 Refund and Dispute Management | HIGH | Basic refund endpoint exists but no dispute workflows |
| 1.8 Personalized Recommendations | MEDIUM | Increases average booking value; currently flat catalog |
| 6.3 Channel Rate Parity | MEDIUM | Partners may undercut direct pricing |
| 7.3 Search and Discovery Engine | MEDIUM | No cross-entity search or relevance ranking |
| 4.5 Facility and Venue Management | LOW | Currently handled informally through svc-location-services |

---

## 4. Architecture Practice Model

### Solution Design Lifecycle

```
Ticket Assigned
  |
  v
Create Branch: solution/NTK-XXXXX-slug
  |
  v
Create Solution in: architecture/solutions/_NTK-XXXXX-slug/
  |-- Master document (overview, component architecture)
  |-- 1.requirements/ (ticket report)
  |-- 2.analysis/ (simple explanation)
  |-- 3.solution/
  |   |-- a.assumptions/
  |   |-- c.capabilities/ (capability mapping -- REQUIRED)
  |   |-- d.decisions/ (MADR format)
  |   |-- g.guidance/ (implementation advice -- optional)
  |   |-- i.impacts/ (per-service impact assessments)
  |   |-- r.risks/
  |   |-- u.user.stories/
  |   |-- 00.component.diagram.puml
  |   |-- *.puml, *.svg (sequence diagrams)
  |
  v
Update Metadata (same branch):
  |-- architecture/metadata/capabilities.yaml (new L3 entries)
  |-- architecture/metadata/capability-changelog.yaml (append entry)
  |-- architecture/metadata/cross-service-calls.yaml (if new integrations)
  |-- decisions/ADR-NNN-*.md (promoted ADRs)
  |
  v
Open Pull Request
  |-- CI validates YAML, builds portal preview
  |-- Reviewer applies architecture checklist
  |
  v
Merge to Main --> Portal Publishes --> Architecture Grows
```

### Branching Strategy

Every solution design is developed on a dedicated branch (`solution/NTK-XXXXX-slug`) and delivered through a pull request. This enforces:

- **Review gate** — PR is the architecture review
- **Portal integrity** — only `main` is published; drafts are invisible
- **Concurrent work** — multiple architects work without conflicts
- **Atomic delivery** — solution + metadata + ADRs reviewed and merged together
- **CI validation** — YAML syntax, portal build, cross-link validation before merge
- **Rollback safety** — revert merge commit cleanly removes everything

### Content Separation Rules

| Artifact | Answers | Does NOT Answer |
|----------|---------|----------------|
| Ticket Report | What does the ticket ask for? | Solutions |
| Simple Explanation | What does this mean simply? | Technical details |
| Impact Assessments | What changes per service? | Why or how |
| Decisions (MADR) | Why this approach? | How to implement |
| Guidance | How to implement? | Why it was chosen |
| User Stories | Who benefits and why? | Technical details |
| Capability Mapping | Which capabilities affected? | Implementation details |

### Capability Rollup Model

```
Solution Design (ticket-scoped)
  --> Capability Mapping (which L1/L2 capabilities touched)
    --> L3 Capabilities (emergent features from the solution)
      --> Capability Changelog (append-only history)
        --> Capability Page in Portal (auto-generated timeline)
```

L1 and L2 capabilities are top-down and stable. L3 capabilities emerge bottom-up from ticket work. The changelog bridges bottom-up work into top-down visibility.

---

## 5. Ticketing Strategy

### Recommended Tool: Vikunja

| Parameter | Value |
|-----------|-------|
| Tool | Vikunja (Go binary, AGPL-3.0) |
| Database | SQLite (upgrade path to PostgreSQL) |
| Hosting | Azure Container Apps (consumption plan) |
| Cost | $0-5/month (scale to zero) |
| API | REST, well-documented |
| Custom fields | Label-based capability tagging |

### Starting Approach: YAML-First

Before deploying Vikunja, start with `architecture/metadata/tickets.yaml` as the source of truth. This validates the information architecture without infrastructure cost. Vikunja becomes the UI layer when broader team adoption requires it.

### Ticket Structure

Every ticket uses structured user story format with:

- User story (As a / I want / So that)
- Use cases with preconditions, main flow, postconditions
- Acceptance criteria
- Capability mapping (CAP-X.Y with impact type)
- Affected services table

### AI Access to Tickets

| Pattern | Description | When |
|---------|-------------|------|
| File-based | AI reads `tickets.yaml` from workspace | Phase 1 (now) |
| CLI script | `ticket-client.py` with capability/service filtering | Phase 1 (now) |
| MCP server | Real-time Vikunja API access | Phase 3 (later) |

---

## 6. Portal Publishing Architecture

### Portal Sections (Target State)

| Section | Generator | Source |
|---------|-----------|--------|
| Design Standards | Static Markdown | `portal/docs/standards/` |
| Service Catalog | Static + metadata | `architecture/metadata/microservices.yaml` |
| **Solution Designs** | `generate-solution-pages.py` | `architecture/solutions/` |
| **Business Capabilities** | `generate-capability-pages.py` | `architecture/metadata/capabilities.yaml` |
| **User Stories** | `generate-ticket-pages.py` | `architecture/metadata/tickets.yaml` |
| Applications | Static + wireframes | `architecture/metadata/applications.yaml` |
| Microservice Pages | `generate-microservice-pages.py` | `architecture/specs/` |
| Event Catalog | Static | `architecture/events/` |
| Actor Catalog | Static | `architecture/metadata/actors.yaml` |
| Decisions | Static | `decisions/` |

### Confluence Mirror (Read-Only)

Every page published to Azure SWA is simultaneously published to Confluence Cloud as a **read-only mirror**. Git remains the single source of truth. The `mark` CLI tool (Go binary) converts portal Markdown to Confluence Storage Format and publishes via the Confluence REST API. A pre-processing script (`confluence-prepare.py`) injects `mark` metadata headers, rewrites internal links to Confluence page titles, converts MkDocs Material syntax (admonitions, content tabs, `<object>` SVGs) to Confluence-compatible equivalents, and adds a "do-not-edit" banner. Pages are locked after publish so only the CI service account can modify them. See [CONFLUENCE-PUBLISHING-PLAN.md](../research/CONFLUENCE-PUBLISHING-PLAN.md) for the complete design.

### Cross-Linking Web

When fully implemented, every artifact connects:

- Solution pages link to impacted services, capabilities, and decisions
- Capability pages show timeline of all solutions that shaped them
- Microservice pages list all solutions affecting them
- Decision pages trace back to originating solution
- Ticket pages link to solution, capabilities, and services

---

## 7. Phased Implementation Plan

### Phase 0: Data Isolation Cleanup (Immediate)

Scrub corporate identifiers from all published content.

| Step | Task | Effort |
|------|------|--------|
| 0.1 | COMPLETE — Replaced corporate URLs in solution design template with NovaTrek equivalents | Small |
| 0.2 | COMPLETE — Replaced auto-generated Azure SWA name references with "NovaTrek Architecture Portal" throughout docs | Small |
| 0.3 | COMPLETE — Replaced corporate org references with "NovaTrek" in analysis documents | Small |
| 0.4 | COMPLETE — Ran audit script, all violations resolved | Small |
| 0.5 | COMPLETE — Added Azure SWA auto-name pattern to audit script | Small |

### Phase 1: Foundation (Immediate)

Build the metadata backbone and establish the solution design workflow.

| Step | Task | Depends On | Effort |
|------|------|-----------|--------|
| 1.1 | COMPLETE -- Created `architecture/solutions/` directory | -- | Small |
| 1.2 | COMPLETE -- Migrated 5 existing solutions from Phase 1 workspace to `architecture/solutions/` | 1.1 | Small |
| 1.3 | COMPLETE -- Added `c.capabilities/` folder to the solution folder template | 1.1 | Small |
| 1.4 | COMPLETE -- Enhanced solution design template with capability mapping, metadata header, changelog sections | 1.3 | Small |
| 1.5 | COMPLETE -- Published enhanced template to portal at `standards/solution-design/` | 1.4 | Small |
| 1.6 | COMPLETE -- Created `architecture/metadata/capabilities.yaml` with 34 L2 capabilities | -- | Small |
| 1.7 | COMPLETE -- Created `architecture/metadata/capability-changelog.yaml` with retrospective entries for NTK-10001 through NTK-10005 | 1.6 | Medium |
| 1.8 | COMPLETE -- Created `architecture/metadata/tickets.yaml` -- migrated 7 tickets from mock JSON with capability mappings | 1.6 | Small |
| 1.9 | COMPLETE -- Wrote `scripts/ticket-client.py` -- YAML-reading CLI with capability/service filtering | 1.8 | Small |
| 1.10 | COMPLETE -- Created branch ruleset (ID 13600522) on `main` requiring PRs and `validate-solution` status check, with admin bypass. Repo made public to enable rulesets on free plan | -- | Small |
| 1.11 | COMPLETE -- Documented branch naming convention (`solution/NTK-XXXXX-slug`) in copilot-instructions.md | -- | Small |
| 1.12 | COMPLETE -- Added PR template (`.github/pull_request_template.md`) with architecture review checklist | -- | Small |

**Outcome:** Solution designs have a canonical home, the template supports capability rollup, the metadata backbone exists, and the branch-based review workflow is documented.

### Phase 2: Portal Publishing (Short Term)

Build generators and publish solution designs, capabilities, and tickets to the portal.

| Step | Task | Depends On | Effort |
|------|------|-----------|--------|
| 2.1 | COMPLETE -- Wrote `portal/scripts/generate-solution-pages.py` -- index + per-solution pages | 1.2 | Medium |
| 2.2 | COMPLETE -- Wrote `portal/scripts/generate-capability-pages.py` -- capability map with timeline | 1.6, 1.7 | Medium |
| 2.3 | COMPLETE -- Wrote `portal/scripts/generate-ticket-pages.py` -- index + per-ticket pages | 1.8 | Medium |
| 2.4 | COMPLETE -- Updated `generate-microservice-pages.py` to include "Solutions Affecting This Service" section with cross-links to solution pages, capability IDs, and dates | 2.1 | Small |
| 2.5 | COMPLETE -- Added Solution Designs, Business Capabilities, Tickets, and nav sections to `portal/mkdocs.yml` | 2.1-2.3 | Small |
| 2.6 | COMPLETE -- Wired all generators into `portal/scripts/generate-all.sh` | 2.1-2.3 | Small |
| 2.7 | COMPLETE -- Promoted ADR-006 through ADR-008 from NTK-10003 to global `decisions/` | -- | Small |
| 2.8 | COMPLETE -- Created CI workflow (`.github/workflows/validate-solution.yml`) for PR validation | 1.10 | Medium |
| 2.9 | COMPLETE -- Tested full pipeline: branch, solution, PR, CI, merge, deploy | 2.6, 2.8 | Small |

**Outcome:** Solution designs, capability pages, and ticket pages are live on the portal with cross-links. Branch CI validates solutions before merge.

### Phase 3: AI Integration (Short Term)

Make the AI agent fully aware of the continuous architecture workflow.

| Step | Task | Depends On | Effort |
|------|------|-----------|--------|
| 3.1 | COMPLETE -- Updated `copilot-instructions.md` with solution design lifecycle and branching requirement | 1.4, 1.11 | Small |
| 3.2 | COMPLETE -- Added capability rollup checklist to AI instructions | 1.6 | Small |
| 3.3 | COMPLETE -- Added prior-art discovery workflow to AI instructions | 1.2 | Small |
| 3.4 | COMPLETE -- Added ticket commands (`ticket-client.py`) to AI instructions | 1.9 | Small |
| 3.5 | COMPLETE -- Tested AI agent -- created NTK-10008 and NTK-10009 solutions on dedicated branches using the enhanced workflow | 3.1-3.4 | Medium |

**Outcome:** AI agent automatically produces capability-mapped solutions on dedicated branches with the same review workflow as human architects.

### Phase 4: Ticketing Infrastructure (Medium Term)

Deploy Vikunja as the ticketing UI.

| Step | Task | Depends On | Effort |
|------|------|-----------|--------|
| 4.1 | COMPLETE -- Created `infra/modules/container-apps-env.bicep` (Log Analytics + managed environment) and `infra/modules/vikunja.bicep` (Container App with Azure Files persistent storage, init container for permissions) | -- | Medium |
| 4.2 | COMPLETE -- Added Vikunja parameters to `infra/parameters/prod.bicepparam` and wired modules into `main.bicep` with `deployVikunja` flag, Azure Storage Account and File Share for SQLite persistence | 4.1 | Small |
| 4.3 | COMPLETE -- Deployed Vikunja v2.1.0 to Azure Container Apps (`ca-vikunja-prod`) with Azure Files persistent storage, registered admin user, seeded 38 labels + 7 tickets | 4.1, 4.2 | Medium |
| 4.4 | COMPLETE -- `scripts/vikunja-seed.py` creates NovaTrek project and seeds 34 capability labels + 4 status labels | 4.3 | Small |
| 4.5 | COMPLETE -- `scripts/vikunja-seed.py` imports all 7 tickets with descriptions, priorities, and label associations | 4.3 | Small |
| 4.6 | COMPLETE -- `portal/scripts/sync-tickets.py` bidirectional sync (push new YAML tickets, pull status/priority changes from Vikunja) | 4.3 | Medium |
| 4.7 | COMPLETE -- Configured Vikunja webhook for task events + GitHub Actions `sync-vikunja.yml` workflow (cron every 30 min + manual dispatch + repository_dispatch) to pull Vikunja changes into tickets.yaml and auto-commit | 4.6 | Medium |

**Outcome:** Vikunja provides a UI for ticket management. `sync-tickets.py` keeps `tickets.yaml` in sync. Portal pages generated from YAML as before.

### Phase 5: Advanced Features (Medium Term)

| Step | Task | Depends On | Effort |
|------|------|-----------|--------|
| 5.1 | COMPLETE -- Added Capability Health Dashboard to `generate-capability-pages.py` with staleness detection (active/aging/stale/untouched), churn analysis, L3 emergence counts, and per-capability health table | 2.2 | Medium |
| 5.2 | COMPLETE -- MkDocs Material built-in search covers full-text search across all portal content including solution designs | 2.1 | Medium |
| 5.3 | COMPLETE -- Added Related Solutions auto-detection to `generate-solution-pages.py` by service and capability overlap, renders cross-link table on each solution page | 2.1, 2.2 | Medium |
| 5.4 | COMPLETE -- `scripts/mcp-vikunja-server.py` MCP server with 6 tools (list_tickets, get_ticket, search_tickets, get_capability_tickets, list_capabilities, get_capability) over stdio, Vikunja + YAML dual-source, configured in `.vscode/mcp.json` | 4.3 | Medium |
| 5.5 | COMPLETE -- `scripts/sync-branch-status.py` detects solution branches and updates ticket status (New -> In Progress -> Ready for Dev), integrated into `validate-solution.yml` workflow | 4.7 | Medium |
| 5.6 | COMPLETE -- Bicep infrastructure already supports custom domains (`customDomain` parameter in main.bicep, conditional resource). Prod parameter file has placeholder ready to uncomment. Remaining work is manual: register domain, configure DNS, uncomment parameter | -- | Small |
| 5.7 | COMPLETE -- Created full solution designs for two priority gap capabilities: NTK-10008 (Guest Reviews and Ratings, CAP-1.7 NEW) with svc-reviews OpenAPI spec, 3 ADRs, 5 user stories, 5 risks, and NTK-10009 (Refund Dispute Management, CAP-5.5 enhanced) with svc-payments v1.1.0 dispute endpoints, 3 ADRs, 5 user stories, 5 risks. Updated capability-changelog.yaml with 11 L3 capabilities | 2.2 | Large |

**Outcome:** The portal becomes an intelligent architecture knowledge base with rich navigation, discovery, and real-time AI integration.

### Phase 6: Confluence Publishing (Short Term)

Publish the NovaTrek Architecture Portal as a read-only mirror in Confluence Cloud. The same `git push` that deploys to Azure SWA also publishes to Confluence — one pipeline, two outputs, zero manual steps. See [CONFLUENCE-PUBLISHING-PLAN.md](../research/CONFLUENCE-PUBLISHING-PLAN.md) for the full design, tool evaluation, and transformation pipeline.

**Tool:** `mark` by Kovetskiy (Go binary, MIT license) — purpose-built for Git Markdown to Confluence publishing.

**Architecture:**

```
Git Push to main
      │
      ▼
  GitHub Actions
      │
  ┌───┴───┐
  │       │
  ▼       ▼
Azure   mark
 SWA    publish
  │       │
  ▼       ▼
Portal  Confluence
(primary) (mirror)
```

| Step | Task | Depends On | Effort |
|------|------|-----------|--------|
| 6.1 | COMPLETE -- Confluence Cloud free-tier instance created (`christopherblaisdell.atlassian.net`), API access verified | -- | Small |
| 6.2 | COMPLETE -- ARCH space created (homepage ID 1310899), parent pages auto-created by mark during publish | 6.1 | Small |
| 6.3 | COMPLETE -- API token generated, GitHub secrets stored (`CONFLUENCE_API_TOKEN`, `CONFLUENCE_USERNAME`, `CONFLUENCE_BASE_URL`, `CONFLUENCE_SPACE`) | 6.1 | Small |
| 6.4 | COMPLETE -- `mark` v15.3.0 installed via Homebrew, single page test publish validated | 6.1 | Small |
| 6.5 | COMPLETE -- `portal/scripts/confluence-prepare.py` with header injection, link rewriting, admonition conversion, SVG handling, banner insertion | 2.6 | Medium |
| 6.6 | COMPLETE -- `<object>` to `![](img)` conversion for SVG diagrams | 6.5 | Small |
| 6.7 | COMPLETE -- MkDocs admonition to Confluence macro conversion (`!!! note` to `{note}`) | 6.5 | Small |
| 6.8 | COMPLETE -- Internal link rewriting (relative MD paths to Confluence page titles) | 6.5 | Small |
| 6.9 | COMPLETE -- Content tab fallback (tabs to H3 sections) and MkDocs syntax stripping (attribute lists, Material emoji, HTML comments) | 6.5 | Small |
| 6.10 | COMPLETE -- Full publish of 84 pages to Confluence ARCH space via `mark` CLI, 0 errors. Fixed parent/title collision for nested index pages (grandparent resolution). Fixed internal link rewriting to use `ac:` prefix for mark inter-page links (including angle-bracket syntax for space-containing titles). Fixed portal fallback URLs with `/../` path segments. Page locking requires Confluence Standard plan (free-tier limitation); 3 other drift prevention layers active. | 6.5-6.9 | Medium |
| 6.11 | COMPLETE -- Added `publish-confluence` job to `docs-deploy.yml` (prepare, mark publish, lock pages) | 6.10 | Small |
| 6.12 | COMPLETE -- Added `validate-confluence` dry-run job to `docs-deploy.yml` for PR validation | 6.11 | Small |
| 6.13 | COMPLETE -- `portal/scripts/confluence-lock-pages.py` sets edit restrictions on auto-generated pages (requires Standard plan) | 6.11 | Small |
| 6.14 | COMPLETE -- `portal/scripts/confluence-drift-check.py` detects unauthorized edits via editor and content hash checks | 6.13 | Small |
| 6.15 | COMPLETE -- `.github/workflows/confluence-drift-check.yml` scheduled weekdays 6 AM UTC | 6.14 | Small |
| 6.16 | COMPLETE -- Added Confluence Publishing section to `copilot-instructions.md` with commands, CI/CD, secrets | 6.11 | Small |

**Drift Prevention (4 layers):**

1. **Page restrictions** — only CI service account can edit
2. **`do-not-edit` label** — visual signal on every page
3. **Banner warning** — every page starts with "auto-generated from Git" notice
4. **Overwrite on deploy** — `mark` replaces full page body on every pipeline run

**What will look different in Confluence:**

| Feature | Azure SWA (Material) | Confluence |
|---------|---------------------|------------|
| SVG interactivity | Clickable links in diagrams | Static images (banner links to portal) |
| Content tabs | Tabbed sections | Sequential H3 sections |
| Dark mode | Toggle switch | Not available |
| Admonitions | Material-styled callouts | Confluence Info/Warning/Note macros |
| Swagger UI | Interactive API explorer | Link to Azure SWA |

**Cost:** $0/month (Confluence Cloud free tier, 10 users, 2 GB storage)

**Outcome:** Enterprise stakeholders consume architecture documentation in their standard wiki. Content is always identical to the portal. Zero manual synchronization.

### Future Initiatives Summary

All Phases 0-6 are COMPLETE. The following initiatives represent the next wave of work, consolidated from plan documents, reminders, and proposed enhancements across the repository. Each initiative has a detailed companion document linked below.

#### CALM — Automated Architecture Governance

**Status:** Phases 0-2 Complete, Phases 3-5 Planned | **Companion:** [docs/CALM-INTEGRATION-PLAN.md](../docs/CALM-INTEGRATION-PLAN.md) | **Portal:** [CALM Topology Layer](calm.md)

CALM (Common Architecture Language Model) is the next major evolution of the platform. It adds a formal, machine-validatable topology layer on top of the existing architecture practice.

**Architects do not write CALM.** CALM documents are **automatically generated** from the artifacts architects already maintain — OpenAPI specs, AsyncAPI specs, and metadata YAML files (`domains.yaml`, `cross-service-calls.yaml`, `data-stores.yaml`, `events.yaml`, `actors.yaml`). Bridge scripts transform these into the CALM format, and `calm validate` runs in CI to enforce architecture rules automatically.

**Why auto-generate instead of hand-author?**

1. **No new format to learn** — architects stay in YAML and OpenAPI specs, which are already the source of truth
2. **Validation is the value, not authoring** — CALM patterns and controls catch violations (shared databases, missing team ownership, undeclared cross-service calls) regardless of whether CALM was hand-written or generated
3. **No drift by construction** — a single source of truth (specs + metadata YAML) feeds both the portal generators and the CALM topology; two representations cannot diverge
4. **Incremental adoption** — existing workflows are unchanged; CALM is a CI-layer addition, not a workflow replacement

**What CALM delivers:**

| Capability | Today (Manual) | With CALM (Automated) |
|-----------|---------------|----------------------|
| No shared databases | PR reviewer reads YAML | CI rejects PRs that connect a database to multiple services |
| API-only cross-service access | Rule text in copilot-instructions.md | CI validates no JDBC relationships exist between services |
| PCI scope tracking | Manual list in `pci.yaml` | CALM decorator flags PCI-scoped nodes and relationships |
| Impact analysis | Architect reads cross-service-calls.yaml | Graph traversal shows all upstream/downstream dependencies |
| Architecture drift | Undetected | CALM topology compared against running system metadata |
| Topology visualization | Static PlantUML diagrams | Interactive system map generated from CALM graph |

**5-phase rollout:** Pilot (1 domain) -> Full topology (all 22 services) -> Generator integration (portal consumes CALM) -> Governance automation (6+ CI-enforced rules) -> Advanced capabilities (blast radius, drift detection, timeline visualization)

See [CALM Integration Plan](../docs/CALM-INTEGRATION-PLAN.md) for the full phased implementation with JSON examples, CI integration, and migration strategy.

---

#### Priority: HIGH

| Initiative | Status | Companion Document | Summary |
|-----------|--------|-------------------|---------|
| Test Methodology and Practice | In Progress | [TEST-METHODOLOGY-ROADMAP.md](TEST-METHODOLOGY-ROADMAP.md) | Comprehensive TDD/BDD practice, coverage standards (80% line, 70% branch, 60% mutation), contract testing for cross-service boundaries, automated regression gates in CI |
| Fix Deploy Failures | Backlog | [architecture/reminders/FIX-DEPLOY-FAILURES.md](../architecture/reminders/FIX-DEPLOY-FAILURES.md) | Audit and fix recurring CI/CD pipeline failures — flaky tests, misconfigured secrets, Bicep errors, SWA deploy issues, PlantUML timeouts. Prerequisite for reliable incremental delivery |
| Azure Microservices Implementation | Draft | [docs/AZURE-IMPLEMENTATION-PLAN.md](../docs/AZURE-IMPLEMENTATION-PLAN.md) | Build out the full NovaTrek microservices platform in Azure — cheapest possible, IaC with Bicep, ephemeral environments, deep linking from architecture artifacts to live implementations |

#### Priority: MEDIUM

| Initiative | Status | Companion Document | Summary |
|-----------|--------|-------------------|---------|
| Separation of Concerns | Proposed | [portal/SEPARATION-OF-CONCERNS-PLAN.md](../portal/SEPARATION-OF-CONCERNS-PLAN.md) | Extract metadata from Python generators into YAML files; stop committing generated artifacts; CI handles all generation; architects edit YAML only |
| Figma Wireframes | Proposed | [portal/FIGMA-WIREFRAMES-PLAN.md](../portal/FIGMA-WIREFRAMES-PLAN.md) | Embed Figma wireframes directly into portal application pages — connect architecture artifacts to visual design layer |
| Event Catalog Expansion | Proposed | [portal/EVENT-CATALOG-PLAN.md](../portal/EVENT-CATALOG-PLAN.md) | Formalize domain events with AsyncAPI specs — producers, consumers, schemas, portal pages with the same rigor as REST API documentation |
| Presentation Site | Draft | [portal/PRESENTATION-SITE-PLAN.md](../portal/PRESENTATION-SITE-PLAN.md) | Executive pitch deck as a third MkDocs Material site — live demo selling Continuous Architecture Platform adoption to leadership and budget holders |

#### Priority: LOW

| Initiative | Status | Companion Document | Summary |
|-----------|--------|-------------------|---------|
| Root Folder Reorganization | Proposed | [portal/ROOT-FOLDER-REORGANIZATION-PLAN.md](../portal/ROOT-FOLDER-REORGANIZATION-PLAN.md) | Reduce 20+ root-level items to intuitive subfolder hierarchy |
| Frontend Applications | Draft | [portal/drafts/PLAN-frontend-applications.md](../portal/drafts/PLAN-frontend-applications.md) | Add 3 frontend application pages (web-guest-portal, web-ops-dashboard, app-guest-mobile) to portal |

#### Completed Initiatives (Reference)

| Initiative | Completed | Companion Document |
|-----------|-----------|-------------------|
| Confluence Publishing | Phase 6 | [research/CONFLUENCE-PUBLISHING-PLAN.md](../research/CONFLUENCE-PUBLISHING-PLAN.md) |
| Documentation Publishing Platform | Phase 6 | [phases/phase-6-documentation-publishing/PUBLISHING-PLATFORM-PLAN.md](../phases/phase-6-documentation-publishing/PUBLISHING-PLATFORM-PLAN.md) |
| AI Tool Cost Comparison | Phase 1 | [phases/phase-1-ai-tool-cost-comparison/AI-TOOL-COST-COMPARISON-PLAN.md](../phases/phase-1-ai-tool-cost-comparison/AI-TOOL-COST-COMPARISON-PLAN.md) |

#### Reminders (Architecture Parking Lot)

These are deferred evaluations and operational items tracked in `architecture/reminders/`:

| Reminder | Date | Status | File |
|----------|------|--------|------|
| CALM Evaluation | 2026-03-06 | Complete — Phases 0-2 delivered | [architecture/reminders/CALM-EVALUATION.md](../architecture/reminders/CALM-EVALUATION.md) |
| Fix Deploy Failures | 2026-03-10 | Backlog (HIGH) | [architecture/reminders/FIX-DEPLOY-FAILURES.md](../architecture/reminders/FIX-DEPLOY-FAILURES.md) |
| Test Methodology | 2026-03-11 | Backlog (HIGH) | [architecture/reminders/TEST-METHODOLOGY.md](../architecture/reminders/TEST-METHODOLOGY.md) |

---

## 8. Architecture Review Checklist

This checklist is applied during PR review of every solution design:

### Completeness

- [ ] Master document has Overview and Component Architecture
- [ ] All impacted services have impact assessment files
- [ ] At least 2 options considered in each decision (MADR format)

### Capability Rollup

- [ ] Capability IDs declared in master document header
- [ ] `3.solution/c.capabilities/capabilities.md` exists with impact types
- [ ] New L3 capabilities identified and named (if applicable)
- [ ] `capability-changelog.yaml` entry drafted
- [ ] All affected metadata YAML files identified for update

### Content Separation

- [ ] Impact files describe WHAT, not WHY or HOW
- [ ] Decision files describe WHY, not HOW
- [ ] Guidance files describe HOW (if present)
- [ ] User stories describe WHO benefits, not technical details

### Metadata Consistency

- [ ] YAML changes match the solution content
- [ ] Cross-service calls updated if new integrations added
- [ ] Backward compatibility addressed for all API changes

### Test Coverage (ADR-012)

- [ ] Test plan included in `3.solution/g.guidance/test-plan.md` (required for solutions touching service logic)
- [ ] Coverage thresholds met for affected services (see `config/test-standards.yaml`)
- [ ] Contract tests added for any new cross-service integrations
- [ ] BDD scenarios correspond to acceptance criteria in user stories (where applicable)

---

## 9. Success Criteria

Six months from now, an architect picking up a new check-in ticket should be able to:

1. Open the **capability page for CAP-2.1** in the portal
2. See a **timeline of every solution** that has touched this capability
3. Read the **L3 capabilities** that emerged from prior work
4. Click through to any prior **solution design** to understand what was decided and why
5. See which **ADRs** shaped the check-in domain
6. Understand the **current service state** through microservice pages referencing all impacting solutions
7. Start their new solution with **full context** -- not from a blank page, but from accumulated knowledge
8. Find the **same content in Confluence** if that is their preferred consumption surface — always in sync, never diverged

That is continuous architecture. Not documentation that decays, but knowledge that compounds.

---

## 10. Companion Analysis Documents

This roadmap synthesizes three detailed analysis documents:

| Document | Focus | Key Contribution |
|----------|-------|-------------------|
| [CAPABILITY-MAP-ANALYSIS.md](../CAPABILITY-MAP-ANALYSIS.md) | Business capability identification and gap analysis | 34 L2 capabilities, coverage assessment, rollup model |
| [TICKETING-INTEGRATION-ANALYSIS.md](../TICKETING-INTEGRATION-ANALYSIS.md) | Ticketing tool evaluation and integration plan | Vikunja recommendation, ticket structure, AI access patterns |
| [SOLUTION-DESIGN-LIFECYCLE-ANALYSIS.md](../SOLUTION-DESIGN-LIFECYCLE-ANALYSIS.md) | Solution design creation, source control, and publishing | Branching strategy, folder structure, portal generators, ADR promotion |
| [CONFLUENCE-PUBLISHING-PLAN.md](../research/CONFLUENCE-PUBLISHING-PLAN.md) | Confluence Cloud mirror — tool selection, transformation pipeline, CI/CD, drift prevention | `mark` tool selection, `confluence-prepare.py` design, 4-layer drift prevention, page hierarchy mapping |
