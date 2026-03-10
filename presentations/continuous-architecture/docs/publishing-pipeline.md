# Automated Publishing: Replace the Manual Wiki Step

## Version Control Push. Documentation Updates Automatically.

Today, updating wiki pages after checking specs into version control is a voluntary manual step — and it gets skipped. The platform replaces that step with an automated pipeline: a version control push triggers a build that publishes the entire architecture portal. No manual copy-paste. No "I'll update the wiki later."

---

## The Pipeline

``` mermaid
flowchart LR
    A[Version control push] --> B[CI/CD Pipeline]
    B --> C[Python generators\nrun against specs]
    C --> D[MkDocs build]
    D --> E[Deploy to Azure\nStatic Web Apps]
    E --> F[Live architecture\nportal updated]

    style A fill:#37474f,color:#fff
    style C fill:#00897b,color:#fff
    style F fill:#ff8f00,color:#fff
```

**Build steps:**

1. Python generators read OpenAPI specs and produce Markdown pages + PlantUML diagrams
2. PlantUML renders sequence diagrams and C4 context diagrams to SVG
3. MkDocs Material builds the site with search, navigation, and responsive layout
4. Non-Markdown assets (SVGs, Swagger UI HTML, OpenAPI YAML downloads) are copied to the output
5. Azure Static Web Apps CLI deploys to a global CDN with SSL

**Total build time:** Under 30 seconds.

---

## What Gets Published

The architecture portal that exists today — built entirely during this proof of concept:

| Content Type | Count | Generated From |
|-------------|:-----:|----------------|
| Microservice deep-dive pages | 19 | OpenAPI specs + cross-service integration map |
| Application consumer pages | 3 | Application-to-service dependency map |
| Endpoint sequence diagrams (SVG) | 139 | OpenAPI spec endpoints |
| C4 context diagrams (SVG) | 20 | Service dependency graph (19 per-service + 1 enterprise) |
| Application integration diagrams (SVG) | 25 | App-to-service call flows |
| Swagger UI pages | 19 | OpenAPI specs (interactive, inline) |
| Downloadable OpenAPI YAML specs | 19 | Source specs copied to portal |
| Markdown documentation pages | 57 | Architecture content + generated pages |
| **Total artifacts** | **301** | |

<div class="big-number">301</div>

**artifacts published automatically from a single version control push.**

---

## What the Generators Produce

### Microservice Pages

For each of the 19 microservices, the generator creates a deep-dive page with:

- Service metadata (domain, owner, version, data store)
- **Every endpoint** documented with a clickable SVG sequence diagram showing the request/response flow
- **Cross-service integrations** with deep links to the target service's specific endpoint
- **C4 context diagram** showing all services that call this service and all services it depends on
- **PCI DSS compliance indicators** — payment data flows highlighted with red lines
- Links to the Swagger UI page and downloadable OpenAPI spec

### Swagger UI Pages

Interactive API documentation for each service — try-it-out capable, with the full OpenAPI spec embedded inline. No external Swagger hosting required.

### Enterprise C4 Diagram

A system-level view of all 19 microservices grouped by domain, with:

- Clickable service boxes that navigate to the deep-dive page
- PCI DSS compliance zone with red data flow lines
- External system integrations (Payment Gateway, Stripe API, mapping providers, etc.)
- Cross-domain relationship arrows with technology annotations

---

## Platform Cost

| Component | Monthly Cost |
|-----------|:---:|
| MkDocs Material (open source) | $0 |
| Azure Static Web Apps (free tier) | $0 |
| PlantUML (open source) | $0 |
| GitHub Actions (included with repo) | $0 |
| **Total** | **$0** |

!!! info "Optional: Material for MkDocs Insiders"
    The Insiders sponsorship ($15/month) unlocks premium features like social cards, blog support, and advanced search. Not required for the base platform.

---

## Wiki Sync (Optional)

For organizations that require wiki integration as the canonical documentation platform:

``` mermaid
flowchart TD
    A[Markdown in Version Control] --> B[MkDocs Build]
    A --> C[Wiki API Sync]
    B --> D[Architecture Portal]
    C --> E[Wiki Platform]

    D -.-> F[Architects browse\nportal for navigation]
    E -.-> G[Stakeholders browse\nwiki for familiarity]

    style A fill:#00897b,color:#fff
    style D fill:#ff8f00,color:#fff
    style E fill:#1565c0,color:#fff
```

The wiki sync publishes the same Markdown content as wiki pages via REST API. Key principles:

- **Version control remains the source of truth** — edits happen in Markdown, not in the wiki
- **Wiki pages are read-only mirrors** — a banner indicates the source is in version control
- **Same content, two renderers** — MkDocs for architects (rich navigation, diagrams), wiki for stakeholders (familiar interface)
- **No dual maintenance** — one version control push updates both

---

## Before and After

| Aspect | Before (Manual Wiki Step) | After (Automated Pipeline) |
|--------|:---:|:---:|
| Publish a design update | Voluntary wiki update (often skipped) | Version control push (automatic, never skipped) |
| Update a diagram | Diagram source in version control, then manually re-render for wiki | Edit diagram source, push (auto-renders to portal) |
| Cross-service links | Manually maintained in wiki (break constantly) | Auto-generated from dependency graph |
| Search across all designs | Wiki search (often miss results) | MkDocs search (full-text, instant) |
| Verify spec matches rendered docs | Manual comparison | Same spec file generates the portal page |
| Add a new service | Check spec in + create wiki pages manually | Add spec to repository, push (portal page auto-generated) |

<div class="cta-box" markdown>

### The innovation that makes this continuous

[Closing the Loop: The PROMOTE Step](closing-the-loop.md)

</div>
