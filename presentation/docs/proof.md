# The Proof

## A Live Architecture Portal — Built Entirely During This POC

The claims on the previous page are not theoretical. They were tested against 5 architecture scenarios using a synthetic workspace (NovaTrek Adventures), and the results are deployed as a live, browsable portal.

---

## The Portal

<div class="cta-box" markdown>

### [https://architecture.novatrek.cc](https://architecture.novatrek.cc)

Open in a new tab to explore alongside this presentation.

</div>

---

## What the AI + Automation Pipeline Produced

| Content Type | Count | Generated From |
|-------------|:-----:|----------------|
| Microservice deep-dive pages | 19 | OpenAPI specs + cross-service integration map |
| Endpoint sequence diagrams (SVG) | 139 | OpenAPI spec endpoints |
| C4 context diagrams (SVG) | 20 | Service dependency graph |
| Swagger UI pages (interactive) | 19 | OpenAPI specs (try-it-out capable) |
| Application integration diagrams (SVG) | 25 | App-to-service call flows |
| Markdown documentation pages | 57 | Architecture content + generated pages |
| **Total artifacts** | **301** | |

<div class="big-number">301</div>

**artifacts published automatically from a single `git push`.**

Total build time: under 30 seconds. Platform cost: $0/month (MkDocs open source + Azure Static Web Apps free tier).

---

## What to Look For in the Portal

### Clickable Architecture

Every C4 diagram arrow links to the **specific endpoint** on the target service's page — not just the service, but the exact operation. Click a relationship on any service page and it navigates to the relevant API endpoint documentation. This is what "navigable architecture" means, and it is generated automatically from the cross-service integration map.

### PCI Compliance Visualization

Payment data flows are highlighted in red across both enterprise-level and per-service C4 diagrams. This is not manually annotated — it is derived from the service metadata and rendered automatically.

### Zero Manual Authoring

Every page, every diagram, every Swagger UI was generated from OpenAPI specs and workspace metadata. No designer. No technical writer. No manual cross-linking.

---

## Live API Explorer

Three microservices are deployed to Azure Container Apps. Make live REST API calls directly from your browser:

<div class="cta-box" markdown>

### [Open API Explorer](api-demo.html){target="_blank"}

Live calls to svc-guest-profiles, svc-trip-catalog, and svc-trail-management.

</div>

NOTE: Container Apps scale to zero when idle. The first request after inactivity may take 10-15 seconds (cold start).

---

## Five Scenarios Tested

The AI assistant was given 5 representative architecture scenarios — the kinds of work architects do regularly:

| # | Scenario | Files Produced |
|:-:|----------|:-:|
| 1 | Triage and classify a new ticket | 4 |
| 2 | Design a solution for unregistered guest check-in | 11 |
| 3 | Investigate a production bug (schedule overwrite) | 8 |
| 4 | Assess impact of a new data field across services | 7 |
| 5 | Design a cross-service event-driven workflow | 9 |

Every scenario followed MADR, arc42, and C4 standards. The AI cited specific file paths, line numbers, and OpenAPI fields — not generic advice. See [Output Quality](quality-evidence.md) for the head-to-head comparison with the alternative toolchain.

---

## Summary of Claims vs Evidence

| Claim | How to Verify |
|-------|--------------|
| "Documentation is always current" | The portal content matches the specs in Git — because it is generated from them |
| "Diagrams are auto-generated" | 184 SVGs rendered from PlantUML, all generated from OpenAPI specs |
| "Cross-links are maintained" | Click any C4 arrow — it navigates to the correct endpoint |
| "Publishing is automated" | The entire portal deploys in under 30 seconds |
| "The AI follows standards" | Read any solution design — MADR headers, arc42 sections, C4 notation throughout |
| "Zero fabrication" | All API fields referenced in solution designs exist in the workspace OpenAPI specs |

<div class="cta-box" markdown>

### Ready for the ask?

[The Ask: One Test License](the-ask.md)

</div>
