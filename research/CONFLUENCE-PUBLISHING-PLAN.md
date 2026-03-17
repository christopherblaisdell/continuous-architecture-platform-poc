# Confluence Publishing Plan — Read-Only Mirror of NovaTrek Architecture Portal

## Executive Summary

This plan defines how to publish the NovaTrek Architecture Portal (currently deployed to Azure Static Web Apps at `mango-sand-083b8ce0f.4.azurestaticapps.net`) as a **read-only mirror** in Confluence Cloud, ensuring both targets always show identical content and never diverge. Git remains the single source of truth. Confluence is a consumption surface only — no editing on the Confluence side.

**Core principle:** The same `git push` that deploys to Azure SWA also publishes to Confluence. One pipeline, two outputs, zero manual steps.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Tool Selection: `mark` by Kovetskiy](#tool-selection-mark-by-kovetskiy)
3. [Why `mark` Over Alternatives](#why-mark-over-alternatives)
4. [Confluence Cloud Setup](#confluence-cloud-setup)
5. [Content Strategy: What Gets Published](#content-strategy-what-gets-published)
6. [Markdown Preparation: Confluence Headers](#markdown-preparation-confluence-headers)
7. [SVG and Image Handling](#svg-and-image-handling)
8. [MkDocs Material Feature Mapping](#mkdocs-material-feature-mapping)
9. [Page Hierarchy and Space Structure](#page-hierarchy-and-space-structure)
10. [CI/CD Pipeline Design](#cicd-pipeline-design)
11. [Page Locking and Drift Prevention](#page-locking-and-drift-prevention)
12. [Divergence Detection](#divergence-detection)
13. [Rollback and Recovery](#rollback-and-recovery)
14. [Content Transformation Pipeline](#content-transformation-pipeline)
15. [Limitations and Trade-offs](#limitations-and-trade-offs)
16. [Implementation Phases](#implementation-phases)
17. [Cost Analysis](#cost-analysis)
18. [Security Considerations](#security-considerations)
19. [Monitoring and Observability](#monitoring-and-observability)
20. [Decision Record](#decision-record)

---

## Architecture Overview

```
                          Git Push to main
                               │
                               ▼
                    ┌─────────────────────┐
                    │   GitHub Actions     │
                    │   docs-deploy.yml    │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
     ┌────────────────┐ ┌───────────┐ ┌──────────────────┐
     │ generate-all.sh│ │ mark      │ │ Transform        │
     │ + mkdocs build │ │ preprocess│ │ MD → Confluence  │
     └───────┬────────┘ └─────┬─────┘ └────────┬─────────┘
             │                │                 │
             ▼                │                 ▼
     ┌────────────────┐       │        ┌──────────────────┐
     │  Azure SWA     │       │        │ mark publish     │
     │  Deploy        │       │        │ → Confluence API │
     └────────────────┘       │        └──────────────────┘
             │                │                 │
             ▼                │                 ▼
     ┌────────────────┐       │        ┌──────────────────┐
     │  Portal Live   │       │        │  Confluence      │
     │  (mango-sand)  │◄──────┘        │  Space (mirror)  │
     │  PRIMARY       │  same content  │  READ-ONLY       │
     └────────────────┘                └──────────────────┘
```

**Key design decisions:**

1. **Git is the single source of truth** — all content originates from Markdown files in the repository
2. **Pipeline publishes to both targets atomically** — a single CI run deploys to Azure SWA AND Confluence
3. **Confluence pages are locked after publish** — prevents manual edits that would cause divergence
4. **Idempotent updates** — `mark` updates existing pages by title match, never creates duplicates
5. **Pre-built HTML/SVG assets** are uploaded as Confluence attachments and referenced in pages

---

## Tool Selection: `mark` by Kovetskiy

**Selected tool:** [`mark`](https://github.com/kovetskiy/mark) (Go binary, MIT license)

`mark` is a CLI tool purpose-built for publishing Markdown files to Confluence Cloud or Data Center. It reads Markdown files with Confluence metadata headers, converts them to Confluence Storage Format (XHTML), and publishes via the Confluence REST API.

### How `mark` Works

1. Each Markdown file gets a metadata header block:

   ```markdown
   <!-- Space: ARCH -->
   <!-- Parent: NovaTrek Architecture Portal -->
   <!-- Title: svc-check-in — Microservice Deep Dive -->
   <!-- Label: microservice, svc-check-in, auto-generated -->

   # svc-check-in — Microservice Deep Dive
   ...
   ```

2. `mark` reads these headers, converts the Markdown body to Confluence Storage Format, and calls the Confluence REST API to create or update the page
3. Images referenced in Markdown are uploaded as page attachments automatically
4. Page hierarchy is derived from `Parent` headers — nested pages map to Confluence parent/child relationships
5. Updates are idempotent — `mark` matches by Space + Title and updates in place

### Installation

```bash
# macOS
brew install mark

# Linux (GitHub Actions)
curl -sL https://github.com/kovetskiy/mark/releases/latest/download/mark_linux_amd64 -o /usr/local/bin/mark
chmod +x /usr/local/bin/mark

# Or via Go
go install github.com/kovetskiy/mark@latest
```

### Key `mark` Features

| Feature | Description |
|---------|-------------|
| **Idempotent publish** | Creates page on first run, updates on subsequent runs — no duplicates |
| **Parent page support** | `<!-- Parent: ... -->` header creates Confluence page hierarchy |
| **Label support** | `<!-- Label: tag1, tag2 -->` applies Confluence labels |
| **Attachment upload** | Local images referenced in Markdown are uploaded as attachments |
| **Dry-run mode** | `--dry-run` shows what would be published without making API calls |
| **Batch publish** | Accepts glob patterns to publish many files at once |
| **Code block mapping** | Fenced code blocks convert to Confluence code macros with language |
| **Table support** | Markdown tables convert to Confluence table markup |
| **Macro insertion** | `<!-- Macro: ... -->` syntax for inline Confluence macros |

---

## Why `mark` Over Alternatives

| Tool | Language | Idempotent | Hierarchy | Images | Macros | CI-Ready | Active (2025) | Verdict |
|------|----------|-----------|-----------|--------|--------|----------|---------------|---------|
| **`mark`** | Go | Yes | Yes (`Parent` header) | Yes (auto-upload) | Yes | Yes (single binary) | Yes | **SELECTED** |
| `md2cf` | Python | Yes | Partial (flat) | Manual upload | No | Yes | Sporadic | Weak hierarchy support |
| `confluence-publisher` | Java/Maven | Yes | Yes (YAML config) | Yes | Yes | Heavy (JVM) | Yes | JVM dependency in CI is wasteful |
| `pandoc` + custom writer | Haskell | No (manual API) | No | Manual | No | Complex | Yes | Too much glue code required |
| Confluence REST API direct | Any | Manual | Manual | Manual | Manual | Manual | N/A | Maximum effort, no abstractions |

**Why `mark` wins:**

1. **Single static binary** — no runtime dependencies, downloads in 2 seconds in CI
2. **Purpose-built** for exactly this workflow (Git Markdown → Confluence)
3. **Metadata-in-file** pattern — each Markdown file declares its own Confluence location, making the mapping self-documenting
4. **Actively maintained** — regular releases, responsive to issues, 1.5K+ GitHub stars
5. **Dry-run mode** — critical for PR validation without touching Confluence
6. **Handles images natively** — SVG/PNG files referenced in Markdown are uploaded as Confluence attachments automatically

---

## Confluence Cloud Setup

### Account and Space Provisioning

1. **Create Confluence Cloud instance** (free tier supports up to 10 users):
   - Navigate to: `https://www.atlassian.com/software/confluence/free`
   - Sign up with a business email
   - Instance URL will be: `https://novatrek.atlassian.net`

2. **Create a Space** for the architecture portal:
   - Space key: `ARCH`
   - Space name: `NovaTrek Architecture Portal`
   - Space type: Knowledge Base (better for documentation-style content)

3. **Create API token** for CI/CD:
   - Navigate to: `https://id.atlassian.com/manage-profile/security/api-tokens`
   - Create token with description: `GitHub Actions — Portal Confluence Sync`
   - Store as GitHub secret: `CONFLUENCE_API_TOKEN`

4. **Create root parent pages** (manual, one-time setup):

   ```
   NovaTrek Architecture Portal (space home)
   ├── Design Standards
   ├── Service Catalog
   ├── Solutions
   ├── Business Capabilities
   ├── Tickets
   ├── Applications
   ├── Microservice Pages
   ├── Event Catalog
   └── Actor Catalog
   ```

### Free Tier Limits (2025-2026)

| Resource | Free Tier Limit | Our Usage | Status |
|----------|----------------|-----------|--------|
| Users | 10 | 1 (service account) + architects | OK |
| Storage | 2 GB | ~50 MB (text + SVGs) | OK |
| Pages | Unlimited | ~80 pages | OK |
| API rate limit | 100 requests/minute | ~80 pages per deploy | OK (under limit) |
| Spaces | Unlimited | 1 | OK |
| Attachments | 250 MB per file | SVGs are < 200 KB each | OK |

---

## Content Strategy: What Gets Published

### Published Content (Confluence mirror)

| Content Type | Source | Confluence Parent | Page Count |
|-------------|--------|-------------------|------------|
| Home / Index | `portal/docs/index.md` | Space home | 1 |
| Design Standards | `portal/docs/standards/**/*.md` | Design Standards | ~20 |
| Service Catalog | `portal/docs/services/index.md` | Service Catalog | 1 |
| Solutions | `portal/docs/solutions/*.md` | Solutions | 5+ |
| Business Capabilities | `portal/docs/capabilities/*.md` | Business Capabilities | 2+ |
| Tickets | `portal/docs/tickets/*.md` | Tickets | 7+ |
| Applications | `portal/docs/applications/*.md` | Applications | 3+ |
| Wireframes | `portal/docs/applications/*/wireframes/*.md` | (child of parent app) | 3+ |
| Microservice Pages | `portal/docs/microservices/svc-*.md` | Microservice Pages | 19 |
| Event Catalog | `portal/docs/events/*.md` | Event Catalog | 6+ |
| Actor Catalog | `portal/docs/actors/*.md` | Actor Catalog | ~5 |

**Total estimated pages: ~75-85**

### Excluded Content (Azure SWA only)

| Content | Reason for Exclusion |
|---------|---------------------|
| Swagger UI HTML pages (`services/api/`) | Interactive HTML apps; Confluence cannot host these — link to Azure SWA instead |
| Raw OpenAPI YAML specs (`specs/`) | Machine-readable files; not documentation — link to Azure SWA |
| Search index (`search/`) | MkDocs-specific JavaScript search — Confluence has its own search |
| SVG source files (standalone) | Embedded as images on pages, not published as separate pages |
| PlantUML `.puml` source | Intermediate build artifact; SVG output is what matters |
| `events-ui/` HTML | Interactive AsyncAPI viewer — link to Azure SWA instead |
| `staticwebapp.config.json` | Azure-specific infrastructure config |
| Tags index | MkDocs-specific feature — Confluence has Labels |

### Linking Strategy for Excluded Content

For content that lives on Azure SWA only (Swagger UI, interactive viewers), Confluence pages include a callout box:

```markdown
> **Interactive Version Available**
> This page has an interactive version with live API exploration at:
> [View on NovaTrek Architecture Portal](https://architecture.novatrek.cc/microservices/svc-check-in/)
```

Implemented as a Confluence Info macro:

```html
<ac:structured-macro ac:name="info">
  <ac:rich-text-body>
    <p><strong>Interactive Version Available</strong><br/>
    This page has an interactive version with live API exploration at:
    <a href="https://architecture.novatrek.cc/microservices/svc-check-in/">View on NovaTrek Architecture Portal</a></p>
  </ac:rich-text-body>
</ac:structured-macro>
```

---

## Markdown Preparation: Confluence Headers

### Header Injection Script

A Python script (`portal/scripts/confluence-prepare.py`) runs as a pre-publish step. It reads each generated Markdown file and prepends `mark`-compatible metadata headers based on the file's position in the nav structure.

**How it works:**

1. Parse `portal/mkdocs.yml` `nav:` structure to build a mapping of file path → (title, parent page)
2. For each Markdown file in `portal/docs/`, generate a corresponding file in a staging directory (`portal/confluence/`) with the `mark` header prepended
3. Rewrite internal links to point to Confluence page titles instead of relative file paths
4. Rewrite image paths to use relative references (for `mark` auto-upload)

**Example transformation:**

**Input** (`portal/docs/microservices/svc-check-in.md`):

```markdown
# svc-check-in — Operations Check-In Service

## Overview
The Check-In service handles day-of-adventure guest registration...

![Check-In Flow](svg/svc-check-in-post-checkins.svg)

See also: [svc-guest-profiles](svc-guest-profiles.md)
```

**Output** (`portal/confluence/microservices/svc-check-in.md`):

```markdown
<!-- Space: ARCH -->
<!-- Parent: Microservice Pages -->
<!-- Title: svc-check-in — Operations Check-In Service -->
<!-- Label: microservice, svc-check-in, auto-generated, do-not-edit -->

# svc-check-in — Operations Check-In Service

> **Interactive Version Available**
> View the full interactive version with clickable SVG diagrams and Swagger UI at:
> [NovaTrek Architecture Portal](https://architecture.novatrek.cc/microservices/svc-check-in/)

## Overview
The Check-In service handles day-of-adventure guest registration...

![Check-In Flow](svg/svc-check-in-post-checkins.svg)

See also: [svc-guest-profiles — Guest Identity Service](svc-guest-profiles — Guest Identity Service)
```

**Key transformations:**

| Transformation | Before | After |
|---------------|--------|-------|
| Add `mark` headers | (none) | `<!-- Space/Parent/Title/Label -->` |
| Internal links | `[text](svc-guest-profiles.md)` | `[text](Title of target page)` — `mark` resolves Confluence page titles |
| Image references | `![alt](svg/file.svg)` | `![alt](svg/file.svg)` — `mark` auto-uploads as attachment |
| `<object>` SVG tags | `<object data="../svg/file.svg">` | `![alt](../svg/file.svg)` — convert to standard image refs |
| MkDocs admonitions | `!!! note "Title"` | Confluence macros (see Feature Mapping) |
| Add portal link banner | (none) | Info callout linking to Azure SWA |
| `do-not-edit` label | (none) | Applied to every page to signal read-only |

### Nav-to-Parent Mapping Logic

The script reads `portal/mkdocs.yml` and builds the parent mapping:

```python
NAV_PARENT_MAP = {
    "standards/": "Design Standards",
    "services/": "Service Catalog",
    "solutions/": "Solutions",
    "capabilities/": "Business Capabilities",
    "tickets/": "Tickets",
    "applications/": "Applications",
    "microservices/": "Microservice Pages",
    "events/": "Event Catalog",
    "actors/": "Actor Catalog",
}
```

For nested content (e.g., wireframes under applications), the script uses the nav hierarchy to determine transitive parents:

```
applications/web-guest-portal/wireframes/check-in-confirmation.md
  → Parent: "web-guest-portal" (which itself has Parent: "Applications")
```

---

## SVG and Image Handling

### The SVG Challenge

The portal uses `<object>` tags for SVG embedding (required for clickable hyperlinks in PlantUML diagrams). Confluence does not support `<object>` tags. Strategy:

| Portal (Azure SWA) | Confluence | Rationale |
|--------------------|-----------|-----------|
| `<object data="svg/file.svg">` | `<ac:image><ri:attachment ri:filename="file.svg"/></ac:image>` | Confluence renders SVGs as static images via attachment macro |
| Clickable links inside SVG | Not supported | Link to Azure SWA for interactive version |
| Relative `../svg/` paths | Attachment references | `mark` uploads files as page attachments |

### Image Pipeline

1. **During `generate-all.sh`**: PlantUML renders `.puml` → `.svg` files into `portal/docs/microservices/svg/`, `portal/docs/applications/svg/`, etc.
2. **During `confluence-prepare.py`**: 
   - Copy SVG files to the confluence staging directory alongside their referencing Markdown files
   - Convert `<object data="...">` tags to `![alt](path)` image references
   - `mark` automatically uploads referenced images as Confluence page attachments on publish
3. **Result**: SVGs display inline on Confluence pages as static images

### Image Sizing

Add Confluence image sizing via `mark`'s macro syntax where needed:

```markdown
<!-- Macro: ac:image
     ri:filename: svc-check-in-post-checkins.svg
     ac:width: 800 -->
```

Or use standard Markdown with `mark`'s width attribute support:

```markdown
![Check-In Flow|width=800](svg/svc-check-in-post-checkins.svg)
```

---

## MkDocs Material Feature Mapping

### Feature-by-Feature Confluence Equivalents

| MkDocs Material Feature | Confluence Equivalent | Transformation |
|------------------------|----------------------|----------------|
| `!!! note "Title"` (admonition) | `{note:title=Title}content{note}` | Regex replacement in pre-processor |
| `!!! warning "Title"` | `{warning:title=Title}content{warning}` | Regex replacement |
| `!!! tip "Title"` | `{tip:title=Title}content{tip}` | Regex replacement |
| `!!! danger "Title"` | `{warning:title=Title}content{warning}` | Map to warning (Confluence has no "danger") |
| `!!! info "Title"` | `{info:title=Title}content{info}` | Regex replacement |
| `!!! example "Title"` | `{panel:title=Title}content{panel}` | Map to panel |
| `??? note "Title"` (collapsible) | `{expand:title=Title}content{expand}` | Map to expand macro |
| Content tabs (`=== "Tab 1"`) | Separate H3 sections | Confluence tabs require paid plugin; fall back to sections |
| Mermaid diagrams | Pre-rendered PNG/SVG | Render in CI, upload as attachment |
| Code blocks with annotations | Code macro + footnotes | Annotations become numbered notes below code block |
| Task lists `- [x]` | Confluence task list macro | `mark` handles natively |
| Tables | Confluence tables | `mark` handles natively |
| Footnotes | Footnote text inline | Expand footnotes inline (Confluence has no footnote macro) |
| Tags/labels | Confluence labels | Via `<!-- Label: ... -->` header |
| `<object>` SVG embeds | `<ac:image>` attachment | Pre-processor converts |
| Internal `[link](file.md)` | `[link](Page Title)` | Pre-processor rewrites to Confluence page title links |
| `#anchor` links | Confluence heading anchors | Rewrite to `#Title-text` format |

### Admonition Conversion Detail

`mark` supports Confluence macros natively via a template syntax. The pre-processor converts MkDocs admonitions:

**Input (MkDocs):**
```markdown
!!! warning "Safety Critical"
    Unknown adventure categories MUST default to Pattern 3 (Full Service).
    This is a safety requirement per ADR-005.
```

**Output (mark-compatible):**
```markdown
<!-- Macro: warning
     Title: Safety Critical -->
Unknown adventure categories MUST default to Pattern 3 (Full Service).
This is a safety requirement per ADR-005.
<!-- /Macro -->
```

### What Will Look Different

Some visual differences between Azure SWA and Confluence are unavoidable:

| Aspect | Azure SWA (Material) | Confluence | Impact |
|--------|---------------------|-----------|--------|
| Theme/colors | Custom NovaTrek navy/copper theme | Confluence default or space theme | Visual only — content identical |
| Navigation | Left sidebar + top tabs | Confluence page tree | Navigation model differs |
| Search | MkDocs lunr.js search | Confluence built-in search | Both work; different UX |
| SVG interactivity | Clickable links in diagrams | Static image display | Info banner links to portal for interactive version |
| Content tabs | Tabbed sections | Sequential H3 sections | Slightly more scrolling on Confluence |
| Code highlighting | Pygments with Material theme | Confluence code macro | Both highlight; different styles |
| Dark mode | Toggle switch | Not available (unless Confluence theme supports) | Azure SWA advantage |
| Social cards | Auto-generated OG meta tags | Not applicable | N/A |

---

## Page Hierarchy and Space Structure

### Confluence Space Layout

```
ARCH Space
│
├── NovaTrek Architecture Portal (Home)
│
├── Design Standards
│   ├── arc42 Template
│   │   ├── Master Document
│   │   ├── 01 Introduction and Goals
│   │   ├── 02 Architecture Constraints
│   │   └── ... (12 sub-pages)
│   ├── C4 Model
│   │   ├── Notation Guide
│   │   ├── C4-PlantUML Guide
│   │   └── Diagram Checklist
│   ├── MADR
│   │   ├── Full Template
│   │   ├── Short Template
│   │   └── Examples
│   ├── ADR Templates
│   │   └── (3 template pages)
│   └── Quality Model
│       └── ISO 25010 Quality Tree
│
├── Service Catalog
│
├── Solutions
│   ├── Solutions Index
│   ├── NTK-10001 — Add Elevation to Trail Response
│   ├── NTK-10002 — Adventure Category Classification
│   ├── NTK-10004 — Guide Schedule Overwrite Bug
│   └── NTK-10005 — Wristband RFID Field
│
├── Business Capabilities
│   └── Business Capabilities Index
│
├── Tickets
│   ├── Tickets Index
│   ├── NTK-10001
│   ├── NTK-10002
│   └── ... (7 tickets)
│
├── Applications
│   ├── Applications Index
│   ├── web-guest-portal
│   │   └── Wireframes
│   │       └── Check-in Confirmation
│   ├── web-ops-dashboard
│   │   └── Wireframes
│   │       └── Live Tracking
│   └── app-guest-mobile
│       └── Wireframes
│           └── Adventure Selection
│
├── Microservice Pages
│   ├── Microservice Pages Index
│   ├── svc-analytics
│   ├── svc-check-in
│   └── ... (19 services)
│
├── Event Catalog
│   ├── Event Catalog Index
│   └── ... (event pages)
│
└── Actor Catalog
    └── ... (actor pages)
```

### Parent Page Resolution

The `confluence-prepare.py` script resolves parent pages using this precedence:

1. **Explicit mapping** from MkDocs `nav:` structure (highest priority)
2. **Directory convention**: `portal/docs/{section}/` → parent page named after section
3. **Nested directories**: each level becomes a parent in Confluence hierarchy
4. **Index pages**: `index.md` files become the parent page itself (not a child)

---

## CI/CD Pipeline Design

### Updated GitHub Actions Workflow

The existing `docs-deploy.yml` workflow gains a new job: `publish-confluence`.

```yaml
# New job in .github/workflows/docs-deploy.yml

  # -------------------------------------------------------------------------
  # Publish to Confluence (read-only mirror)
  # -------------------------------------------------------------------------
  publish-confluence:
    runs-on: ubuntu-latest
    name: Publish to Confluence
    needs: build
    if: github.event_name == 'push'  # Only publish on merge to main
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Download build artifact
        uses: actions/download-artifact@v4
        with:
          name: docs-site
          path: site/

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: pip

      - name: Install mark
        run: |
          curl -sL https://github.com/kovetskiy/mark/releases/latest/download/mark_linux_amd64 \
            -o /usr/local/bin/mark
          chmod +x /usr/local/bin/mark

      - name: Prepare Confluence pages
        run: python3 portal/scripts/confluence-prepare.py
        env:
          PORTAL_BASE_URL: https://architecture.novatrek.cc

      - name: Publish to Confluence (dry-run on PR)
        run: |
          mark \
            --base-url "https://${{ vars.CONFLUENCE_DOMAIN }}.atlassian.net/wiki" \
            --username "${{ secrets.CONFLUENCE_USERNAME }}" \
            --password "${{ secrets.CONFLUENCE_API_TOKEN }}" \
            --files "portal/confluence/**/*.md" \
            --color \
            --ci
        env:
          CONFLUENCE_DOMAIN: ${{ vars.CONFLUENCE_DOMAIN }}

      - name: Lock published pages
        run: |
          python3 portal/scripts/confluence-lock-pages.py \
            --base-url "https://${{ vars.CONFLUENCE_DOMAIN }}.atlassian.net/wiki" \
            --username "${{ secrets.CONFLUENCE_USERNAME }}" \
            --api-token "${{ secrets.CONFLUENCE_API_TOKEN }}" \
            --space "ARCH" \
            --label "auto-generated"
```

### Required GitHub Secrets and Variables

| Name | Type | Value | Purpose |
|------|------|-------|---------|
| `CONFLUENCE_API_TOKEN` | Secret | Atlassian API token | Authentication for REST API |
| `CONFLUENCE_USERNAME` | Secret | Atlassian account email | Authentication identity |
| `CONFLUENCE_DOMAIN` | Variable | `novatrek` | Atlassian instance subdomain |

### Pipeline Flow

```
                    Push to main
                        │
              ┌─────────┴──────────┐
              │                    │
              ▼                    ▼
         Build Job            (waits)
              │                    │
              ▼                    │
     generate-all.sh               │
     mkdocs build                  │
              │                    │
              ▼                    │
     Upload artifact ──────────────┤
              │                    │
       ┌──────┴──────┐            │
       │             │            │
       ▼             ▼            │
   Deploy to     Publish to       │
   Azure SWA     Confluence       │
       │             │            │
       │        ┌────┘            │
       │        │                 │
       │        ▼                 │
       │   confluence-prepare.py  │
       │   (inject headers,       │
       │    rewrite links,        │
       │    convert admonitions)  │
       │        │                 │
       │        ▼                 │
       │   mark publish           │
       │   (create/update pages,  │
       │    upload SVG attachments)│
       │        │                 │
       │        ▼                 │
       │   confluence-lock-pages  │
       │   (restrict editing)     │
       │                          │
       ▼                          ▼
    Portal Live             Confluence Live
    (primary)               (read-only mirror)
```

### PR Validation (Dry Run)

For pull requests, add dry-run validation to catch Confluence formatting issues early:

```yaml
  validate-confluence:
    runs-on: ubuntu-latest
    name: Validate Confluence Output
    needs: build
    if: github.event_name == 'pull_request'
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Download build artifact
        uses: actions/download-artifact@v4
        with:
          name: docs-site
          path: site/

      - name: Prepare Confluence pages
        run: python3 portal/scripts/confluence-prepare.py

      - name: Install mark
        run: |
          curl -sL https://github.com/kovetskiy/mark/releases/latest/download/mark_linux_amd64 \
            -o /usr/local/bin/mark
          chmod +x /usr/local/bin/mark

      - name: Dry-run Confluence publish
        run: |
          mark \
            --base-url "https://${{ vars.CONFLUENCE_DOMAIN }}.atlassian.net/wiki" \
            --username "${{ secrets.CONFLUENCE_USERNAME }}" \
            --password "${{ secrets.CONFLUENCE_API_TOKEN }}" \
            --files "portal/confluence/**/*.md" \
            --dry-run \
            --color
```

---

## Page Locking and Drift Prevention

### Strategy: Multi-Layer Protection

Since Confluence is a consumption-only mirror, we need to prevent anyone from editing pages there. Four layers of protection:

### Layer 1: Page Restrictions via API

After every publish, `confluence-lock-pages.py` sets page restrictions so only the service account can edit:

```python
"""
confluence-lock-pages.py
Sets edit restrictions on all auto-generated pages so only the
CI service account can modify them.
"""

# For each page with label "auto-generated":
# PUT /wiki/rest/api/content/{id}/restriction
# {
#   "results": [{
#     "operation": "update",
#     "restrictions": {
#       "user": {
#         "results": [{"accountId": "<service-account-id>"}]
#       }
#     }
#   }]
# }
```

### Layer 2: `do-not-edit` Label

Every published page gets the Confluence labels `auto-generated` and `do-not-edit`. This is a visual signal to users:

```markdown
<!-- Label: auto-generated, do-not-edit, novatrek-portal -->
```

### Layer 3: Banner Warning

Every Confluence page starts with an Info macro warning:

```markdown
> **This page is auto-generated from Git. Do not edit here.**
> Source: [NovaTrek Architecture Portal](https://architecture.novatrek.cc)
> Any changes made on this Confluence page will be overwritten on the next deploy.
```

### Layer 4: Overwrite on Deploy

Even if someone bypasses restrictions and edits a page, the next pipeline run overwrites it with the authoritative Git content. `mark` always replaces the full page body — manual edits are not preserved.

---

## Divergence Detection

### Automated Drift Check

An optional scheduled workflow runs daily to verify no drift:

```yaml
# .github/workflows/confluence-drift-check.yml
name: Confluence Drift Check

on:
  schedule:
    - cron: '0 6 * * 1-5'  # 6 AM UTC weekdays
  workflow_dispatch: {}

jobs:
  check-drift:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: pip install requests pyyaml

      - name: Check for drift
        run: python3 portal/scripts/confluence-drift-check.py
        env:
          CONFLUENCE_BASE_URL: https://${{ vars.CONFLUENCE_DOMAIN }}.atlassian.net/wiki
          CONFLUENCE_USERNAME: ${{ secrets.CONFLUENCE_USERNAME }}
          CONFLUENCE_API_TOKEN: ${{ secrets.CONFLUENCE_API_TOKEN }}
          CONFLUENCE_SPACE: ARCH
```

**`confluence-drift-check.py` logic:**

1. For each page with label `auto-generated` in the ARCH space:
   - Fetch page content via Confluence REST API
   - Fetch the corresponding Markdown source from Git
   - Compare a normalized text hash (strip whitespace, Confluence formatting)
   - If hashes differ AND last editor is NOT the service account → **drift detected**
2. Report drift findings:
   - Log which pages drifted, who edited them, when
   - Optionally open a GitHub Issue or send a Slack notification
3. **Auto-remediation option**: Re-publish drifted pages from Git to restore authoritative state

---

## Rollback and Recovery

### Scenario: Bad Publish

If a pipeline run publishes broken content to Confluence:

1. **Confluence page history**: Every `mark` update creates a new version. Confluence retains all versions. Manual rollback via Confluence UI: Page → `...` → Page History → Restore Previous Version
2. **Git-based rollback**: Revert the commit in Git, push, pipeline re-publishes correct content
3. **Selective re-publish**: Run `mark` locally against specific files:

   ```bash
   mark \
     --base-url "https://novatrek.atlassian.net/wiki" \
     --username "$CONFLUENCE_USERNAME" \
     --password "$CONFLUENCE_API_TOKEN" \
     --files "portal/confluence/microservices/svc-check-in.md"
   ```

### Scenario: Confluence Space Corruption

If the Confluence space is damaged or accidentally deleted:

1. Re-create the ARCH space and root parent pages (manual, ~10 minutes)
2. Run the full publish pipeline — `mark` creates all pages from scratch
3. Run `confluence-lock-pages.py` to re-apply edit restrictions

Total recovery time: one pipeline run (~5 minutes).

---

## Content Transformation Pipeline

### `confluence-prepare.py` — Detailed Design

This is the most critical new script. It transforms portal Markdown into Confluence-ready Markdown.

```
portal/docs/**/*.md  ──→  confluence-prepare.py  ──→  portal/confluence/**/*.md
                                    │
                    Reads: portal/mkdocs.yml (nav structure)
                    Reads: portal/docs/**/*.svg (images to stage)
                    Writes: portal/confluence/**/*.md (with mark headers)
                    Copies: SVG/PNG files alongside their Markdown
```

### Transformation Steps (in order)

| Step | Input Pattern | Output | Purpose |
|------|--------------|--------|---------|
| 1. Parse nav | `portal/mkdocs.yml` | Parent-page mapping dict | Determine Confluence hierarchy |
| 2. Prepend headers | (computed) | `<!-- Space/Parent/Title/Label -->` | `mark` metadata |
| 3. Add banner | (template) | Info macro at top of body | Warn readers this is auto-generated |
| 4. Convert admonitions | `!!! type "title"` blocks | `mark` macro syntax | MkDocs → Confluence macros |
| 5. Convert collapsible | `??? type "title"` blocks | `{expand}` macro | Collapsible sections |
| 6. Convert content tabs | `=== "Tab Name"` | H3 sections with dividers | No free Confluence tab plugin |
| 7. Rewrite `<object>` tags | `<object data="...svg">` | `![alt](path.svg)` | SVG as standard images |
| 8. Rewrite internal links | `[text](relative/path.md)` | `[text](Confluence Page Title)` | `mark` resolves page titles |
| 9. Rewrite anchor links | `[text](page.md#anchor)` | `[text](Page Title#anchor)` | Confluence heading anchors |
| 10. Strip MkDocs-only syntax | `{: .class }`, attr_list | Remove | Not supported in Confluence |
| 11. Copy referenced images | SVG/PNG files | Staged alongside Markdown | `mark` auto-uploads |
| 12. Strip HTML comments | `<!-- CONFLUENCE-PUBLISH -->` etc. | Remove | Clean output |
| 13. Fix emoji shortcodes | `:material-xxx:` | Unicode or remove | MkDocs-specific emoji |
| 14. Add portal link | (computed per page) | Absolute URL to Azure SWA page | Direct link to interactive version |

### Script Skeleton

```python
#!/usr/bin/env python3
"""
confluence-prepare.py
Transforms portal Markdown files into mark-compatible Confluence Markdown.
Reads MkDocs nav structure to determine page hierarchy.
Stages transformed files in portal/confluence/ for mark to publish.
"""

import os
import re
import shutil
import yaml
from pathlib import Path

PORTAL_DIR = Path(__file__).parent.parent
DOCS_DIR = PORTAL_DIR / "docs"
CONFLUENCE_DIR = PORTAL_DIR / "confluence"
MKDOCS_YML = PORTAL_DIR / "mkdocs.yml"
SPACE_KEY = "ARCH"
PORTAL_BASE_URL = os.environ.get(
    "PORTAL_BASE_URL",
    "https://architecture.novatrek.cc"
)

DO_NOT_EDIT_BANNER = """
> **This page is auto-generated from Git. Do not edit here.**
> Source: [{portal_url}]({portal_url})
> Any changes made on this Confluence page will be overwritten on the next deploy.

"""

def load_nav_structure():
    """Parse mkdocs.yml nav to build file → (title, parent) mapping."""
    ...

def convert_admonitions(content: str) -> str:
    """Convert MkDocs admonitions to mark macro syntax."""
    ...

def convert_object_tags(content: str) -> str:
    """Convert <object data='...svg'> to ![alt](path.svg)."""
    ...

def rewrite_internal_links(content: str, nav_map: dict) -> str:
    """Rewrite [text](file.md) to [text](Confluence Page Title)."""
    ...

def inject_headers(content: str, space: str, parent: str,
                   title: str, labels: list) -> str:
    """Prepend mark metadata headers."""
    ...

def prepare_file(src: Path, dst: Path, nav_map: dict):
    """Full transformation pipeline for a single file."""
    ...

def main():
    nav_map = load_nav_structure()
    if CONFLUENCE_DIR.exists():
        shutil.rmtree(CONFLUENCE_DIR)
    CONFLUENCE_DIR.mkdir(parents=True)

    for md_file in DOCS_DIR.rglob("*.md"):
        rel = md_file.relative_to(DOCS_DIR)
        dst = CONFLUENCE_DIR / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        prepare_file(md_file, dst, nav_map)

    # Copy images alongside their referencing markdown
    for img in DOCS_DIR.rglob("*.svg"):
        dst = CONFLUENCE_DIR / img.relative_to(DOCS_DIR)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(img, dst)

    print(f"Prepared {sum(1 for _ in CONFLUENCE_DIR.rglob('*.md'))} "
          f"Confluence pages in {CONFLUENCE_DIR}")

if __name__ == "__main__":
    main()
```

---

## Limitations and Trade-offs

### Accepted Limitations

| Limitation | Impact | Mitigation |
|-----------|--------|-----------|
| No clickable SVG links in Confluence | Users cannot click through sequence diagram participants | Banner links to interactive portal version |
| No dark mode in Confluence | Confluence uses its own theme | Content is identical; visual presentation differs |
| No tabbed content | Content tabs become sequential sections | Slightly more scrolling; content unchanged |
| Confluence free tier: 10 users | Limited viewer seats | Sufficient for architecture team; upgrade to Standard ($5.75/user/mo) if needed |
| API rate limit: 100 req/min | Large publishes may need throttling | ~80 pages fits in one batch; add back-off if count grows |
| Admonition styling differs | Confluence macros look different from Material admonitions | Content and semantic meaning preserved |
| No code annotations | MkDocs code annotations have no Confluence equivalent | Convert to numbered footnotes below code block |
| Search experience differs | MkDocs lunr.js vs Confluence search | Both functional; different UX |

### Hard Boundaries (Will Not Attempt)

| Feature | Reason |
|---------|--------|
| Confluence → Git sync | Bi-directional sync creates merge conflicts, complexity, and governance problems. Git is authoritative. |
| Custom Confluence theme matching Material | Theme customization requires Confluence admin + custom CSS injection. Not worth the maintenance. |
| Embedding Swagger UI in Confluence | Confluence cannot host interactive HTML apps. Link to Azure SWA instead. |
| Real-time sync (webhook on every commit) | Overkill for architecture docs that change at PR merge cadence. Pipeline-based is sufficient. |

---

## Implementation Phases

### Phase A: Foundation (estimated effort: 4-6 hours)

| # | Task | Output |
|---|------|--------|
| 1 | Create Confluence Cloud free-tier instance | `novatrek.atlassian.net` live |
| 2 | Create ARCH space with root parent pages | Space structure ready |
| 3 | Generate API token, add as GitHub secret | `CONFLUENCE_API_TOKEN`, `CONFLUENCE_USERNAME` |
| 4 | Install `mark` locally, test manual publish of 1 page | Validation that `mark` → Confluence works |
| 5 | Create `portal/scripts/confluence-prepare.py` (basic version) | Header injection + image staging |
| 6 | Manual publish of 5 pages via `mark` CLI | Proof of concept validated |

### Phase B: Transformation Pipeline (estimated effort: 6-8 hours)

| # | Task | Output |
|---|------|--------|
| 1 | Implement admonition → macro conversion | `!!! note` → `{note}` |
| 2 | Implement `<object>` → `<img>` conversion | SVGs render as static images |
| 3 | Implement internal link rewriting (MD → page titles) | Cross-references work in Confluence |
| 4 | Implement MkDocs syntax stripping (attr_list, emoji) | Clean Confluence output |
| 5 | Implement collapsible section conversion | `??? ` → `{expand}` |
| 6 | Implement content tab fallback (tabs → H3 sections) | Tabbed content accessible |
| 7 | Add `do-not-edit` banner to all pages | Users warned against editing |
| 8 | Test full publish of all ~80 pages | Complete mirror verified |

### Phase C: CI/CD Integration (estimated effort: 3-4 hours)

| # | Task | Output |
|---|------|--------|
| 1 | Add `publish-confluence` job to `docs-deploy.yml` | Automated publish on push to main |
| 2 | Add `validate-confluence` dry-run for PRs | PR validation without touching Confluence |
| 3 | Create `confluence-lock-pages.py` | Edit restrictions applied after publish |
| 4 | Test full pipeline: push → Azure SWA + Confluence | End-to-end validation |
| 5 | Add Confluence deployment to GitHub environment | Deployment tracking in GitHub UI |

### Phase D: Governance and Monitoring (estimated effort: 2-3 hours)

| # | Task | Output |
|---|------|--------|
| 1 | Create `confluence-drift-check.py` | Drift detection script |
| 2 | Create scheduled drift-check workflow | Daily automated verification |
| 3 | Document the Confluence publishing workflow in portal | Self-documenting system |
| 4 | Add `confluence` label to `copilot-instructions.md` | AI agent awareness |

### Total Estimated Effort: 15-21 hours

---

## Cost Analysis

### Confluence Cloud

| Tier | Monthly Cost | Users | Features |
|------|-------------|-------|----------|
| **Free** | $0 | Up to 10 | 2 GB storage, basic permissions, API access |
| Standard | $5.75/user/mo | 11+ | 250 GB, advanced permissions, audit logs |
| Premium | $11/user/mo | Any | Unlimited storage, analytics, team calendars |

**Recommendation:** Start with Free tier. 10 users is sufficient for an architecture team. Upgrade to Standard only if more viewers are needed.

### CI/CD Compute

| Resource | Cost | Notes |
|----------|------|-------|
| GitHub Actions minutes | Free (2,000 min/mo on free plan) | Confluence job adds ~2-3 minutes per run |
| `mark` binary download | Free | Cached via GitHub Actions cache |
| Azure SWA deployment | Free | Already running |

### Total Additional Cost: $0/month

(Assuming Confluence Cloud free tier and existing GitHub Actions minutes)

---

## Security Considerations

### Credential Management

| Credential | Storage | Rotation |
|-----------|---------|----------|
| Confluence API token | GitHub Secret (`CONFLUENCE_API_TOKEN`) | Rotate every 90 days |
| Confluence username | GitHub Secret (`CONFLUENCE_USERNAME`) | Tied to service account |
| Azure SWA token | GitHub Secret (existing) | No change |

### Access Control

| Actor | Confluence Permissions | Purpose |
|-------|----------------------|---------|
| CI service account | Space Admin (ARCH space only) | Create/update/restrict pages |
| Architects | View only | Read documentation |
| All org users | View only (if space is public) | Consume architecture docs |

### Data Isolation

- All published content originates from the NovaTrek Adventures synthetic domain
- No corporate data passes through the Confluence API
- The `audit-data-isolation.sh` script runs BEFORE the Confluence publish step
- Confluence space uses `*.novatrek.example.com` URLs exclusively

---

## Monitoring and Observability

### Pipeline Monitoring

| Metric | Source | Alert Threshold |
|--------|--------|----------------|
| Confluence publish duration | GitHub Actions job duration | > 10 minutes |
| Pages published count | `mark` output (parsed) | Differs from expected count |
| Publish failures | GitHub Actions job status | Any failure |
| API rate limit hits | `mark` error output | Any 429 response |

### Drift Monitoring

| Metric | Source | Alert Threshold |
|--------|--------|----------------|
| Pages edited outside CI | `confluence-drift-check.py` | Any page modified by non-service account |
| Pages missing labels | Confluence API query | Any auto-generated page without `do-not-edit` label |
| Page count mismatch | Compare Git file count vs Confluence page count | Any difference |

---

## Decision Record

### ADR: Confluence Publishing Strategy

**Status:** Proposed

**Context:** The NovaTrek Architecture Portal is deployed to Azure Static Web Apps. Enterprise stakeholders consume architecture documentation via Confluence. Publishing to both targets from a single Git source ensures consistency and eliminates manual synchronization.

**Decision Drivers:**
- Single source of truth (Git) — content must never be authored in Confluence
- Zero-drift guarantee — both targets must always show identical content
- Minimal operational overhead — publishing must be fully automated
- Enterprise adoption — Confluence is the standard enterprise wiki

**Decision:** Use `mark` (Go CLI tool) to publish Markdown to Confluence as a CI/CD pipeline step, running in parallel with the Azure SWA deploy. A pre-processing script (`confluence-prepare.py`) transforms MkDocs Material syntax to Confluence-compatible Markdown with `mark` metadata headers.

**Consequences:**
- Positive: Single pipeline produces both outputs atomically
- Positive: `mark` handles idempotent updates, image uploads, and page hierarchy
- Positive: Dry-run mode enables PR validation without touching Confluence
- Negative: Some MkDocs Material features (tabs, interactive SVGs, dark mode) degrade gracefully in Confluence
- Negative: Adds ~2-3 minutes to CI pipeline duration
- Neutral: Confluence becomes a read-only consumption surface, which aligns with the "Git as source of truth" principle

---

## Appendix A: Alternative Approaches Considered

### Approach 1: Publish MkDocs HTML to Confluence via iframe

Embed the Azure SWA portal inside a Confluence page using an iframe macro.

**Rejected because:**
- Confluence Cloud blocks iframes from external domains by default
- Requires Confluence admin to whitelist the Azure SWA domain
- Creates a dependency on Azure SWA uptime for Confluence users
- Search, navigation, and accessibility are broken inside iframes
- Not a true mirror — it is a window into the other site

### Approach 2: Confluence REST API direct (no tool)

Write a custom Python script that calls the Confluence REST API directly.

**Rejected because:**
- Rebuilds what `mark` already provides (page creation, hierarchy, attachments, idempotency)
- More code to maintain, more edge cases to handle
- No dry-run mode without building it ourselves
- `mark` is battle-tested by thousands of users; a custom script is not

### Approach 3: `md2cf` (Python)

Use the `md2cf` Python tool to publish Markdown to Confluence.

**Rejected because:**
- Weak hierarchy support — does not natively support parent page specification via file headers
- Image handling requires manual attachment upload
- Less active maintenance than `mark`
- No macro conversion support

### Approach 4: Confluence Publisher Maven Plugin

Use the Java-based `confluence-publisher` tool.

**Rejected because:**
- Requires JVM in CI — adds ~1 minute to install Java
- Configuration is YAML-based (separate from the Markdown files), creating a second source of truth for page mapping
- Heavier dependency for a pipeline that is otherwise Python + Go

### Approach 5: `pandoc` with Confluence writer

Convert Markdown → Confluence Storage Format using pandoc.

**Rejected because:**
- Pandoc converts format but does not publish — still need API glue code
- No page hierarchy, no attachment handling, no idempotency
- Would need to pair with a custom publish script (see Approach 2)

---

## Appendix B: `mark` Command Reference

```bash
# Publish all files matching glob
mark --files "portal/confluence/**/*.md" \
     --base-url "https://novatrek.atlassian.net/wiki" \
     --username "user@example.com" \
     --password "ATATT3xxxxxxxxxxx"

# Dry-run (validate without publishing)
mark --files "portal/confluence/**/*.md" \
     --base-url "https://novatrek.atlassian.net/wiki" \
     --username "user@example.com" \
     --password "ATATT3xxxxxxxxxxx" \
     --dry-run

# Publish single file
mark --files "portal/confluence/microservices/svc-check-in.md" \
     --base-url "https://novatrek.atlassian.net/wiki" \
     --username "user@example.com" \
     --password "ATATT3xxxxxxxxxxx"

# With color output and CI mode (non-interactive)
mark --files "portal/confluence/**/*.md" \
     --base-url "https://novatrek.atlassian.net/wiki" \
     --username "user@example.com" \
     --password "ATATT3xxxxxxxxxxx" \
     --color --ci

# Trace mode for debugging
mark --files "portal/confluence/solutions/*.md" \
     --base-url "https://novatrek.atlassian.net/wiki" \
     --username "user@example.com" \
     --password "ATATT3xxxxxxxxxxx" \
     --trace
```

---

## Appendix C: Confluence Page Header Template

Every published page starts with this header block (injected by `confluence-prepare.py`):

```markdown
<!-- Space: ARCH -->
<!-- Parent: {parent_page_title} -->
<!-- Title: {page_title} -->
<!-- Label: auto-generated, do-not-edit, novatrek-portal, {content-type-label} -->

> **This page is auto-generated from the NovaTrek Architecture Portal.**
> **Source of truth:** [View on Architecture Portal]({portal_url}/{page_path})
> **Do not edit this page.** Changes will be overwritten on the next deploy.

```

Content-type labels used:

| Label | Applied To |
|-------|-----------|
| `microservice` | Microservice deep-dive pages |
| `solution-design` | Solution design pages |
| `capability` | Business capability pages |
| `ticket` | Ticket pages |
| `event-catalog` | Event catalog pages |
| `design-standard` | arc42, C4, MADR, quality model pages |
| `application` | Application and wireframe pages |
| `actor` | Actor catalog pages |

---

## Appendix D: File Inventory — New and Modified Files

### New Files

| File | Purpose |
|------|---------|
| `portal/scripts/confluence-prepare.py` | Transform portal Markdown → `mark`-compatible Confluence Markdown |
| `portal/scripts/confluence-lock-pages.py` | Apply edit restrictions to published pages via Confluence API |
| `portal/scripts/confluence-drift-check.py` | Detect unauthorized edits to auto-generated pages |
| `.github/workflows/confluence-drift-check.yml` | Scheduled workflow for daily drift detection |

### Modified Files

| File | Change |
|------|--------|
| `.github/workflows/docs-deploy.yml` | Add `publish-confluence` job (parallel with Azure SWA deploy) |
| `.github/copilot-instructions.md` | Document Confluence publishing workflow for AI agent awareness |

### Generated (Not Committed)

| Directory | Purpose |
|-----------|---------|
| `portal/confluence/` | Staging directory for `mark`-ready Markdown files (gitignored) |
