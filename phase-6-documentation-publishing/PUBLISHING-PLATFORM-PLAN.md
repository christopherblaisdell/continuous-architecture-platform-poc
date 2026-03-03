# Phase 6: Architecture Documentation Publishing Platform

## Platform Recommendation: Material for MkDocs

### Why Material for MkDocs

**Material for MkDocs** is the most respected and widely adopted open-source framework for publishing markdown documentation as rich, searchable, professional websites. It is purpose-built for exactly this use case: markdown files in git → comprehensive online documentation.

### Adoption Evidence

| Metric | Material for MkDocs |
|--------|-------------------|
| **GitHub Stars** | 21,000+ |
| **PyPI Downloads** | 2M+ per month |
| **Used By** | Google Cloud, Microsoft, AWS CDK, FastAPI, Pydantic, Kubernetes, Netflix, Stripe, Cloudflare, HashiCorp, Mozilla, CNCF projects |
| **License** | MIT (core) |
| **Maintainer** | Martin Donath (squidfunk) — full-time dedicated maintainer |
| **First Release** | 2016 |
| **Plugin Ecosystem** | 150+ community plugins |

### Why Not the Alternatives

| Framework | Stars | Why Not |
|-----------|-------|---------|
| **Docusaurus** (Meta) | 57K | General-purpose (docs + blog + landing page). React dependency. Overkill for pure documentation. Better for product marketing sites. |
| **Hugo** | 77K | General static site generator, not documentation-specific. Requires theme hunting + configuration. Documentation themes lack the polish of Material. |
| **VitePress** (Vue) | 13K | Smaller ecosystem. Vue dependency. Less mature for large documentation sites. |
| **Starlight** (Astro) | 5K | Too young. Limited plugin ecosystem. Unproven at enterprise scale. |
| **GitBook** | N/A | Commercial, not fully open source. Vendor lock-in. |
| **Docsify** | 27K | No static build — requires JavaScript runtime. SEO limitations. |

### Architecture Documentation Fit

Material for MkDocs is specifically exceptional for architecture documentation:

| Feature | Architecture Use Case |
|---------|----------------------|
| **Admonitions** | ADR status badges, warning callouts, notes on decisions |
| **Content Tabs** | Compare service impacts side-by-side, show before/after |
| **Mermaid Diagrams** | Render C4, sequence, and component diagrams inline from markdown |
| **PlantUML Plugin** | Render existing `.puml` files directly in documentation pages |
| **Code Annotations** | Annotate Java/YAML code samples with inline explanations |
| **Navigation Tabs** | Map directly to arc42 sections (Introduction, Constraints, Context, etc.) |
| **Built-in Search** | Full-text search across all ADRs, solution designs, and investigations |
| **Tags** | Categorize documents by service, ticket, complexity, status |
| **Git Integration** | Last-updated dates from git history, contributors, revision links |
| **Social Cards** | Auto-generated link preview cards for sharing docs in Teams/Slack |
| **Versioning** | `mike` plugin provides version-selector dropdown for documentation releases |
| **Offline Support** | Download as PDF or offline HTML bundle |

---

## Deployment Target: Azure Static Web Apps

### Why Azure Static Web Apps

| Feature | Value |
|---------|-------|
| **Cost** | Free tier available (sufficient for architecture practice docs) |
| **CI/CD** | Built-in GitHub Actions integration — deploy on push to main |
| **Custom Domain** | Supported with free SSL/TLS certificates |
| **Authentication** | Azure AD integration for private documentation (if needed) |
| **Global CDN** | Automatic global distribution for fast load times |
| **Staging Environments** | Preview PRs with ephemeral staging URLs |
| **Zero Infrastructure** | No VMs, containers, or web servers to manage |

### Architecture

```
┌──────────────┐     ┌──────────────────┐     ┌───────────────────────┐
│  Git Push    │────>│  GitHub Actions   │────>│  Azure Static Web     │
│  (main)      │     │  - mkdocs build   │     │  Apps                 │
│              │     │  - deploy         │     │  - Global CDN         │
└──────────────┘     └──────────────────┘     │  - Custom Domain      │
                                               │  - Azure AD Auth      │
┌──────────────┐     ┌──────────────────┐     │  - Free SSL           │
│  Git Push    │────>│  GitHub Actions   │     └───────────────────────┘
│  (PR branch) │     │  - mkdocs build   │────>  Staging Preview URL
└──────────────┘     └──────────────────┘
```

---

## Implementation Plan

### Phase 6A: Foundation (Week 1)

**Goal**: Working local MkDocs site rendering the existing workspace markdown.

| # | Task | Effort | Output |
|---|------|--------|--------|
| 1 | Install MkDocs + Material theme (`pip install mkdocs-material`) | 15 min | Working local toolchain |
| 2 | Create `mkdocs.yml` configuration at repo root | 1 hour | Site configuration with navigation, theme, and plugins |
| 3 | Structure `nav:` to map repo folders to documentation hierarchy | 2 hours | Logical navigation reflecting arc42 structure |
| 4 | Configure PlantUML plugin for `.puml` rendering | 30 min | Diagrams render inline in docs |
| 5 | Configure Mermaid for inline diagram support | 15 min | Mermaid fenced code blocks render as diagrams |
| 6 | Add admonition styling for ADR status badges | 30 min | `!!! accepted`, `!!! proposed`, `!!! deprecated` callouts |
| 7 | `mkdocs serve` — verify all pages render correctly | 1 hour | Local preview at http://localhost:8000 |
| 8 | Fix any markdown rendering issues (link paths, image refs) | 2 hours | All cross-references resolve correctly |

**Deliverable**: `mkdocs serve` produces a fully navigable local site.

### Phase 6B: Azure Deployment (Week 2)

**Goal**: Automated CI/CD pipeline publishing docs to Azure on every push.

| # | Task | Effort | Output |
|---|------|--------|--------|
| 1 | Create Azure Static Web App resource (Azure Portal or `az cli`) | 30 min | Azure resource provisioned |
| 2 | Create `.github/workflows/docs-deploy.yml` GitHub Actions workflow | 1 hour | CI/CD pipeline definition |
| 3 | Configure deployment token as GitHub secret | 15 min | `AZURE_STATIC_WEB_APPS_API_TOKEN` |
| 4 | Test push-to-main deployment | 30 min | Live site accessible at Azure URL |
| 5 | Configure custom domain (optional: `docs.{domain}`) | 30 min | Custom domain with SSL |
| 6 | Configure Azure AD authentication (if private docs) | 1 hour | Only authenticated users can access |
| 7 | Test PR preview environment | 30 min | PR creates ephemeral staging site |

**Deliverable**: Push to `main` automatically publishes updated docs to `https://{app-name}.azurestaticapps.net`.

### Phase 6C: Content Enhancement (Week 3)

**Goal**: Optimize the documentation site for architecture practice consumption.

| # | Task | Effort | Output |
|---|------|--------|--------|
| 1 | Create landing page (`docs/index.md`) with project overview | 1 hour | Professional home page |
| 2 | Add tags to all documents (service, ticket, status) | 2 hours | Filterable tag-based navigation |
| 3 | Create architecture decision log page (auto-generated ADR index) | 1 hour | Sortable ADR list |
| 4 | Add `git-revision-date-localized` plugin for auto "last updated" dates | 30 min | Every page shows last modified date |
| 5 | Add `git-committers` plugin for author attribution | 30 min | Contributor avatars on each page |
| 6 | Configure social cards for link previews in Teams/Slack | 30 min | Rich link previews when sharing |
| 7 | Add PDF export capability via `mkdocs-with-pdf` plugin | 1 hour | Download entire site as PDF |
| 8 | Create `.pages` files for custom folder ordering | 1 hour | Logical page ordering |

**Deliverable**: Polished, professional documentation site with full-text search, tags, attribution, and PDF export.

### Phase 6D: Integration with Architecture Workflow (Week 4)

**Goal**: Integrate documentation publishing into the continuous architecture workflow.

| # | Task | Effort | Output |
|---|------|--------|--------|
| 1 | Add MkDocs build validation to PR checks | 1 hour | PRs that break docs cannot merge |
| 2 | Add link-check plugin to CI | 30 min | Broken cross-references caught automatically |
| 3 | Create doc templates for new tickets/ADRs with front matter | 1 hour | Consistent metadata for tags + search |
| 4 | Add `CONFLUENCE-PUBLISH` marker handling (existing comments in solution designs) | 2 hours | Automated Confluence sync if needed |
| 5 | Document the publishing workflow in the playbooks | 1 hour | Team knows how to publish |
| 6 | Add versioning with `mike` for documentation releases | 2 hours | Version selector (e.g., v1.0, v2.0, latest) |

**Deliverable**: Documentation publishing is a seamless part of the architecture workflow — commit markdown, push, site updates automatically.

---

## Configuration Skeleton

### `mkdocs.yml`

```yaml
site_name: Continuous Architecture Platform
site_url: https://{app-name}.azurestaticapps.net
site_description: Architecture Practice — Solution Designs, ADRs, and Architecture Documentation
repo_url: https://github.com/christopherblaisdell/continuous-architecture-platform-poc
repo_name: continuous-architecture-platform-poc
edit_uri: edit/main/

theme:
  name: material
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.tabs
    - navigation.tabs.sticky
    - navigation.sections
    - navigation.expand
    - navigation.path
    - navigation.indexes
    - navigation.top
    - search.suggest
    - search.highlight
    - search.share
    - content.code.copy
    - content.code.annotate
    - content.tabs.link
    - toc.follow
  icon:
    repo: fontawesome/brands/github

plugins:
  - search
  - tags
  - git-revision-date-localized:
      enable_creation_date: true
  - git-committers:
      repository: christopherblaisdell/continuous-architecture-platform-poc
      branch: main
  - plantuml:
      puml_url: https://www.plantuml.com/plantuml/
  - minify:
      minify_html: true

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.critic
  - pymdownx.caret
  - pymdownx.keys
  - pymdownx.mark
  - pymdownx.tilde
  - attr_list
  - md_in_html
  - tables
  - toc:
      permalink: true

nav:
  - Home: index.md
  - Project:
    - README.md
    - Roadmap: roadmap/ROADMAP.md
    - Decisions:
      - ADR-001 AI Toolchain Selection: decisions/ADR-001-ai-toolchain-selection.md
  - Phase 1 - AI Tool Comparison:
    - Overview: phase-1-ai-tool-cost-comparison/AI-TOOL-COST-COMPARISON-PLAN.md
    - Results: phase-1-ai-tool-cost-comparison/workspace/phase-1-copilot-results.md
    - Playbooks:
      - SC-01 Ticket Triage: phase-1-ai-tool-cost-comparison/workspace/playbooks/scenario-01-new-ticket-triage.md
      - SC-02 Solution Design: phase-1-ai-tool-cost-comparison/workspace/playbooks/scenario-02-solution-design.md
      - SC-03 Investigation: phase-1-ai-tool-cost-comparison/workspace/playbooks/scenario-03-investigation-analysis.md
      - SC-04 Architecture Update: phase-1-ai-tool-cost-comparison/workspace/playbooks/scenario-04-architecture-update.md
      - SC-05 Cross-Service: phase-1-ai-tool-cost-comparison/workspace/playbooks/scenario-05-complex-cross-service.md
      - Measurement Protocol: phase-1-ai-tool-cost-comparison/workspace/playbooks/measurement-protocol.md
  - Architecture Standards:
    - arc42: phase-1-ai-tool-cost-comparison/workspace/architecture-standards/arc42/README.md
    - C4 Model: phase-1-ai-tool-cost-comparison/workspace/architecture-standards/c4-model/README.md
    - MADR: phase-1-ai-tool-cost-comparison/workspace/architecture-standards/madr/README.md
    - Quality Model: phase-1-ai-tool-cost-comparison/workspace/architecture-standards/quality-model/README.md
  - NovaTrek Workspace:
    - Tickets:
      - NTK-10001 Elevation Data: phase-1-ai-tool-cost-comparison/workspace/work-items/tickets/_NTK-10001-add-elevation-to-trail-response/NTK-10001-solution-design.md
      - NTK-10002 Category Classification: phase-1-ai-tool-cost-comparison/workspace/work-items/tickets/_NTK-10002-adventure-category-classification/NTK-10002-solution-design.md
      - NTK-10003 Unregistered Check-in: phase-1-ai-tool-cost-comparison/workspace/work-items/tickets/_NTK-10003-unregistered-guest-self-checkin/NTK-10003-solution-design.md
      - NTK-10004 Schedule Overwrite Bug: phase-1-ai-tool-cost-comparison/workspace/work-items/tickets/_NTK-10004-guide-schedule-overwrite-bug/NTK-10004-solution-design.md
      - NTK-10005 Wristband RFID: phase-1-ai-tool-cost-comparison/workspace/work-items/tickets/_NTK-10005-wristband-rfid-field/NTK-10005-solution-design.md
  - Research:
    - Context Window Analysis: research/CONTEXT-WINDOW-UTILIZATION-ANALYSIS.md
```

### `.github/workflows/docs-deploy.yml`

```yaml
name: Deploy Documentation

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    name: Build and Deploy Docs
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Required for git-revision-date-localized plugin

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install mkdocs-material \
                      mkdocs-git-revision-date-localized-plugin \
                      mkdocs-git-committers-plugin-2 \
                      mkdocs-minify-plugin \
                      mkdocs-plantuml-plugin \
                      mkdocs-material[imaging]

      - name: Build MkDocs site
        run: mkdocs build --strict

      - name: Deploy to Azure Static Web Apps
        if: github.event_name == 'push'
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: upload
          app_location: site
          skip_app_build: true
```

---

## Cost Estimate

| Component | Monthly Cost |
|-----------|-------------|
| Azure Static Web Apps (Free tier) | $0 |
| Custom Domain SSL | $0 (included) |
| GitHub Actions CI/CD | $0 (included in GitHub plan) |
| Material for MkDocs (MIT core) | $0 |
| Material for MkDocs Insiders (optional sponsor) | $15/month |
| **Total** | **$0 - $15/month** |

The Insiders sponsorship ($15/month) unlocks premium features like social cards, privacy plugin, optimized search, and blog support. Not required but recommended for a professional practice site.

---

## Success Criteria

| Criterion | Target |
|-----------|--------|
| All existing markdown renders correctly | 100% of pages |
| Diagrams (PlantUML/Mermaid) render inline | All diagrams visible |
| Full-text search works across all documents | < 200ms search response |
| Push-to-main deploys in under 5 minutes | < 5 min CI/CD pipeline |
| PR preview environments work | Ephemeral staging URLs generated |
| Mobile-responsive design | Readable on phone/tablet |
| Lighthouse performance score | > 90 |

---

## Timeline

| Week | Phase | Milestone |
|------|-------|-----------|
| Week 1 | 6A: Foundation | Local MkDocs site rendering all markdown |
| Week 2 | 6B: Azure Deployment | Live site auto-deploying on push |
| Week 3 | 6C: Content Enhancement | Tags, search, PDF export, attribution |
| Week 4 | 6D: Workflow Integration | CI validation, versioning, team onboarding |

**Total effort**: ~25-30 hours across 4 weeks (parallelizable with other phases).
