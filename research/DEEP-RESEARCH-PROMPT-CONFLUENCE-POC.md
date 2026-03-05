# Deep Research Prompt: Cheapest Way to POC Publishing to Confluence

## Research Objective

I need to find the cheapest (ideally free) way to set up a proof-of-concept that publishes architecture documentation pages to Atlassian Confluence from an automated CI pipeline. This is for a demo/evaluation — not production use. I need concrete, current (2025-2026) answers with exact pricing, API details, and pipeline integration steps.

## Context

We have an architecture documentation portal built with MkDocs Material, deployed to Azure Static Web Apps. The portal generates Markdown pages for 19 microservices, an event catalog, architecture decision records (ADRs), and service catalog pages — all from Python scripts that read OpenAPI/AsyncAPI YAML specs and produce Markdown + PlantUML SVG diagrams.

We want to demonstrate that the same generated content can be **published to Confluence** as part of a CI/CD pipeline, proving that architecture documentation can flow into an enterprise wiki automatically. This is a proof-of-concept only — we need the cheapest possible path to a working demo.

## Specific Questions to Answer

### 1. Confluence Cloud Free Tier

- Does Atlassian Confluence Cloud still offer a **free tier** in 2025-2026? What are its exact limits (users, spaces, storage, API rate limits)?
- Can a single developer sign up for a free Confluence Cloud instance for evaluation/POC purposes without a credit card?
- What is the exact URL to sign up? What is the onboarding process?
- Are there any **time-limited free trials** of Confluence Cloud Standard or Premium that would give more API access? How long do they last?
- Is there a **developer/partner program** that gives free or discounted Confluence Cloud access for building integrations?

### 2. Confluence Cloud API for Publishing

- What is the current Confluence Cloud REST API for creating and updating pages? (v1 vs v2 — which should we use?)
- What authentication method is required? (API token, OAuth 2.0, PAT?) What are the exact steps to generate credentials?
- Can the API accept **Atlassian Document Format (ADF)** or just **Confluence Storage Format (XHTML-like)**? Which is easier for converting from Markdown?
- What are the API rate limits on the free tier? Are they sufficient for publishing ~30 pages in a single pipeline run?
- Can we embed **SVG images** (PlantUML sequence diagrams, C4 diagrams) in Confluence pages via the API? Do we need to upload them as attachments first and then reference them, or can we inline SVG?

### 3. Markdown to Confluence Conversion

- What are the best open-source tools for converting Markdown to Confluence storage format? Evaluate:
  - **md2cf** (Python) — https://github.com/iamjackg/md2cf
  - **mark** (Go) — https://github.com/kovetskiy/mark
  - **confluence-publisher** (Java/Maven)
  - **pandoc** with Confluence output format
  - Any other actively maintained tools (2024-2025 commits)
- Which tool handles these features best:
  - Markdown tables
  - Fenced code blocks with language syntax highlighting
  - Embedded images (SVG files referenced in Markdown)
  - MkDocs Material admonitions/callouts (translating to Confluence info/warning/note macros)
  - Frontmatter metadata (tags, title overrides)
  - Idempotent updates (update existing page rather than creating duplicates)
- Can any of these tools be run headlessly in a CI pipeline (GitHub Actions, Azure Pipelines)?

### 4. Pipeline Integration

- What does a minimal **GitHub Actions workflow** look like that:
  1. Checks out the repo
  2. Generates Markdown pages (runs our Python scripts)
  3. Converts Markdown to Confluence format
  4. Publishes pages to a Confluence Cloud space via API
  5. Handles page hierarchy (parent/child pages mirroring our nav structure)
- How do we store Confluence credentials securely in GitHub Actions? (secrets, environment variables)
- Can we do a **dry-run mode** that shows what would be published without actually pushing?
- How do we handle **page versioning** — does the API auto-version, or do we need to manage version numbers?

### 5. Confluence Data Center / Server (Self-Hosted Alternative)

- Is there a way to run **Confluence Data Center** locally (Docker) for free as a trial/evaluation?
- Does Atlassian provide a Docker image or Helm chart for Confluence evaluation?
- What are the system requirements (RAM, CPU) for running a local Confluence instance?
- How long does the evaluation license last? Can it be renewed?
- Would a local Docker instance be simpler for a demo than using Confluence Cloud?

### 6. Alternative Wiki Platforms (If Confluence Is Too Expensive/Complex)

- If Confluence free tier is too limited, are there alternative enterprise wiki platforms that:
  - Have a REST API for publishing pages
  - Accept Markdown or have good Markdown conversion
  - Offer a free tier or are open-source
  - Are commonly used in enterprises (so the demo is still relevant)
  - Examples to evaluate: **Notion API**, **GitBook**, **Bookstack**, **Wiki.js**, **XWiki**
- How do these compare to Confluence for enterprise adoption credibility?

### 7. Cost Summary

Provide a comparison table:

| Option | Setup Cost | Monthly Cost | API Access | Effort to Integrate | Enterprise Credibility |
|--------|-----------|-------------|------------|--------------------|-----------------------|
| Confluence Cloud Free | ? | ? | ? | ? | High |
| Confluence Cloud Trial | ? | ? | ? | ? | High |
| Confluence Data Center Docker | ? | ? | ? | ? | High |
| Notion API | ? | ? | ? | ? | Medium |
| Wiki.js (self-hosted) | ? | ? | ? | ? | Low-Medium |
| BookStack (self-hosted) | ? | ? | ? | ? | Low |

### 8. Recommended Approach

Based on all findings, recommend the single cheapest path to a working demo that:
- Costs $0 or as close to $0 as possible
- Can be set up in under 2 hours
- Publishes at least 5-10 generated architecture pages
- Handles images (SVG diagrams)
- Can be automated in a CI pipeline
- Has high enterprise credibility (i.e., "yes, this would work in a real enterprise Confluence instance")

## Output Format

Structure the response with clear sections matching the questions above. Include:
- Exact URLs for signup/download
- Exact CLI commands for tool installation
- Exact API curl examples for page creation
- Exact GitHub Actions YAML snippets
- Current pricing (as of 2025-2026)
- Any gotchas, limitations, or known issues discovered
