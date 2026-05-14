# Presentations as Code — Capability Definition

> **BLUEPRINT — NOT AN INSTANCE.** This document is part of the EaC blueprint — a portable
> pattern designed for export to a real corporate workspace (the Instance). All NovaTrek
> Adventures content (services, tickets, ADRs, architecture decisions) is **fully synthetic
> exemplar data** created solely to validate the pattern. No corporate data, real systems,
> or organisation-specific tool choices are represented here. Organisation-specific current-
> state context belongs in the Instance, not in this blueprint.

> **Status:** Draft — v1.0 — 2026-05-14
>
> **Scope:** This document defines what the Presentations as Code capability is, who it serves,
> what it must do, and how we will know it works. It is the authoritative requirements and
> vision reference for all implementation work. The corresponding implementation plan is in
> [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md).

---

## 1. Capability Statement

**Presentations as Code (PrC)** is the practice of authoring, versioning, rendering, and
governing architecture presentations as plain-text, machine-readable source files committed to the
same version-controlled repository that holds the architecture artifacts they describe. It is
Pillar N of the Everything as Code (EaC) framework.

The core premise: a High-Level Design deck presented to an Architecture Review Board is as
architecturally significant as the ADR that documents the outcome of that review. It warrants the
same treatment — version control, PR review, CI validation, traceability to other artifacts, and
a permanent archive record.

The capability has three concrete deliverables in this workspace:

1. **A governed presentation pipeline** — the tooling, schema, scripts, workflows, and portal
   integration that make any architecture presentation a first-class managed artifact.

2. **A corporate identity theme library** — the Marp CSS theme files that apply organisational
   identity (colour palette, typography, logo placement) to every rendered presentation. Themes
   are versioned artifacts governed by the same PR workflow as slide source. They are the bridge
   between plain Markdown source and professional, on-brand output that can be delivered directly
   to an Architecture Review Board or engineering leadership without post-processing in an external slide authoring tool.

   Note on tooling: these are **Marp CSS themes**, not MkDocs themes. Marp is the rendering engine
   that converts Markdown slide source to HTML and PDF. MkDocs governs only the portal index page
   that lists presentations — it does not render slides. A theme file is a plain CSS file stored
   in `presentations/themes/` and referenced by name in each slide deck's front matter.

3. **A living presentation library** — the actual presentations (slide sources, rendered HTML,
   PDFs, manifests) produced by the architecture practice, hosted as a searchable, linked library
   on the architecture portal.

---

## 2. The Problem This Solves

### 2.1 The Binary Slide File Problem

Architecture presentations are commonly authored in graphical WYSIWYG slide authoring tools. These
tools produce binary or proprietary-format files with no meaningful diff, no AI readability, and
no linkage to the architecture artifacts they describe.

When ADR-006 (Orchestrator Pattern for Check-in) was decided, a presentation likely walked the
Architecture Review Board through the options analysis. That presentation — the artefact that
actually influenced the decision-makers — lives on someone's desktop or in a shared drive. It
is not in source control. It has no reference to ADR-006. It cannot be found by searching the
architecture portal. An AI agent reading the workspace cannot discover it.

This workspace already has 11 ADRs, 34 capabilities, 19 service OpenAPI specs, and 139 documented
API endpoints. It has zero governed architecture presentations.

> **Instance onboarding note:** When adopting this pillar, the first step is to document which
> graphical slide authoring tool(s) your practice currently uses — that is the instance-level
> baseline for Pillar N. This blueprint describes the problem class that motivates the pillar,
> independent of which specific tool any adopting organisation happens to use.

### 2.2 The Silent Drift Problem

A presentation that accurately described the Check-in Service in February 2026 is factually
wrong by May 2026 if ADR-010 (PATCH semantics) was accepted in March. The presentation has not
been updated. There is no mechanism to detect the drift. A new team member shown the February
deck receives incorrect information with no indication that it is stale.

Documentation as Code (Pillar M) addresses drift in reference documentation through continuous
CI validation. Presentations require a different approach: rather than expecting presentations to
stay current indefinitely, they are archived as permanent records on delivery and superseded by
new presentations when the architecture changes.

### 2.3 The AI Blindspot Problem

An AI agent operating in this workspace can read every OpenAPI spec, every ADR, every capability
definition, and every solution design. It cannot meaningfully process a binary slide file. The binary
format is opaque to the model — it cannot summarise the deck, check its accuracy against current
specs, or propose updates.

When an AI is asked to generate a High-Level Design presentation for a new solution, it currently
has no examples to learn from, no templates to follow, and no prior art to reference. Each
presentation starts from scratch.

Presentations as Code closes the AI blindspot: every slide deck becomes readable, summarisable,
and improvable by the same models that maintain the rest of the architecture.

### 2.4 The Record Gap Problem

The architecture practice does not currently have a canonical record of what was presented to
whom, when, and what was decided. Architecture Review Board submissions are not tracked. Onboarding
briefings are not versioned. There is no way to answer: "What was the design we proposed for the
Scheduling Orchestrator in Q1, before we changed direction?"

The presentation manifest and archive system creates that record.

---

## 3. Vision

The architecture practice produces presentation-format artifacts as naturally as it produces ADRs
and solution designs. Every Architecture Review Board submission, every High-Level Design walkthrough,
and every strategy briefing is:

- Authored in Markdown alongside the solution design it supports
- Versioned in the same repository as the architecture it describes
- Rendered to presentation-quality HTML and PDF by CI
- Published to the architecture portal as a searchable, linked artifact
- Permanently archived as a record of what was communicated, to whom, and when
- Readable, summarisable, and improvable by AI
- Linked bidirectionally to the ADRs, capabilities, and tickets it references

The end state: asking "What did we present to the Architecture Review Board about the Check-in
Service in February?" is answered by a portal search, not a desktop hunt.

---

## 4. Personas and Use Cases

### 4.1 Personas

| Persona | Role | Relationship to Presentations as Code |
|---------|------|----------------------------------------|
| Solution Architect | Authors presentation source; reviews AI-generated drafts; delivers presentations to stakeholders | Primary author; primary consumer of authoring workflow |
| Architecture Practice Lead | Governs the presentation library; approves theme changes; owns archive policy | Governance owner |
| Decision-Making Audience | Engineering leadership, product leadership, board or steering committee members who receive presentations | End consumers of rendered output; never touch source |
| New Team Member | Onboarded using architecture briefings; reads archived presentations to understand historical decisions | Passive consumer; benefits from the archive |
| AI Agent | Reads slide source to check accuracy against current specs; generates first-draft slide decks from solution designs; flags stale references | Automated participant |

### 4.2 Use Cases

**UC-01: Author a High-Level Design deck**

The Solution Architect is completing a solution design for NTK-10005. The solution design includes
impact assessments, ADR decisions, and capability changes. The architect generates (or manually
authors) a HLD slide deck in Markdown, registers it with a manifest, opens a PR, and CI renders
it to HTML for stakeholder review before the Architecture Review Board session.

**UC-02: Deliver and archive a presentation**

After the Architecture Review Board session approves the HLD, the architect updates the manifest
`status` from `review` to `delivered`. CI detects the transition, renders the final version, and
archives it in `presentations/archive/HLD-001/v1.2.0/`. The portal presentations index lists it
as a delivered artifact with a permanent link to the archived HTML.

**UC-03: Discover prior presentations**

A new architect asks: "What design was presented for the Scheduling Orchestrator before
ADR-010?" The portal's presentations section is searchable. The query returns the HLD deck from
Q4 2025, which references `svc-scheduling-orchestrator` and cites ADR-006, ADR-007. The architect
reads the slide source directly in VS Code or views the rendered HTML via the portal link.

**UC-04: AI-assisted first draft**

The architect opens GitHub Copilot in Agent Mode and says: "Generate a first-draft HLD presentation
for NTK-XXXXX using the solution design artifacts." The AI reads the solution design master
document, impact assessments, and ADR decisions in `architecture/solutions/_NTK-XXXXX/`, and
produces a Markdown slide deck with the structure, cross-references, and assertions pre-populated.
The architect refines the narrative before opening a PR.

**UC-05: Staleness detection**

A scheduled CI job reads every delivered presentation manifest. For each one, it checks whether
any referenced ADR has been superseded, whether any referenced capability has changed, and whether
any referenced service endpoint has been modified. It opens a GitHub Issue listing the stale
presentations and the specific references that have drifted. The architect decides to archive the
stale deck or create an updated version.

**UC-06: Onboarding briefing delivery**

The architecture practice maintains a versioned onboarding briefing (`ONBOARDING-001`). When a
new architect joins, the practice lead points them to the portal presentation link. The briefing
is always at the current version because it is updated via PR workflow like any other source file.

---

## 5. Functional Requirements

### 5.1 Presentation Authoring

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | Slide source files are plain Markdown (`slides.md`) authored in VS Code without requiring a separate tool | Must have |
| FR-02 | Slides are separated by `---` on a standalone line; speaker notes are appended after a `^--` separator | Must have |
| FR-03 | Diagrams inside slides are authored as fenced PlantUML or Mermaid code blocks; no screenshot images are permitted | Must have |
| FR-04 | The first slide must declare front matter: `title`, `author`, `date`, `theme` | Must have |
| FR-05 | Slide source files reference architecture artifacts using their canonical IDs (ADR-NNN, CAP-X.Y, NTK-XXXXX) | Must have |
| FR-06 | Authors can create a new presentation by creating `presentations/{id}/` with `manifest.yaml` and `slides.md` | Must have |
| FR-07 | An AI agent can generate a first-draft `slides.md` from a solution design folder given a prompt | Should have |

### 5.2 Presentation Manifest

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-08 | Every governed presentation has a `manifest.yaml` that declares: `presentation_id`, `title`, `version`, `status`, `type`, `audience`, `authors`, `delivery`, `source`, `references`, `metadata` | Must have |
| FR-09 | `status` follows the lifecycle: `draft` → `review` → `delivered` → `archived` | Must have |
| FR-10 | `type` is one of: `hld`, `adr-walkthrough`, `onboarding`, `strategy`, `review-board` | Must have |
| FR-11 | Manifests validate against a published JSON Schema (`schemas/presentation-manifest.schema.json`) | Must have |
| FR-12 | The manifest version (`semver`) increments on every substantive content change | Should have |
| FR-13 | CI fails if a manifest is missing a required field or contains an invalid `status` or `type` value | Must have |

### 5.3 Rendering Pipeline

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-14 | CI renders every changed presentation on every PR that touches a file in `presentations/` | Must have |
| FR-15 | HTML output is produced for all presentation types; PDF output is produced for `hld`, `adr-walkthrough`, `strategy`, and `review-board` types | Must have |
| FR-16 | PlantUML and Mermaid code blocks are pre-rendered to SVG before the slide renderer runs | Must have |
| FR-17 | Rendered HTML is self-contained and navigable without a local server | Must have |
| FR-18 | Speaker notes are excluded from the audience-facing HTML output; they are preserved in a separate notes view or PDF | Should have |
| FR-19 | Rendering supports at least five themes (see Theme System requirements below) | Must have |
| FR-20 | Rendering is incremental in CI — only presentations with changed source files are re-rendered (not all presentations on every run) | Should have |

### 5.4 Cross-Reference Validation

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-21 | CI validates that every ADR ID in `manifest.yaml references.adrs` resolves to a file in `decisions/` | Must have |
| FR-22 | CI validates that every capability ID in `references.capabilities` resolves to a capability entry in `architecture/metadata/capabilities.yaml` | Must have |
| FR-23 | CI validates that every ticket ID in `references.tickets` resolves to a ticket entry in `architecture/metadata/tickets.yaml` | Must have |
| FR-24 | CI fails the validation step (not just warns) if any reference is unresolvable | Must have |
| FR-25 | Validation produces a structured report listing every broken reference with the file and field where it was found | Should have |

### 5.5 Archive and Lifecycle

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-26 | When a presentation transitions to `status: delivered` on the default branch, CI copies the rendered output to `presentations/archive/{id}/v{version}/` | Must have |
| FR-27 | Archived presentations are immutable — CI fails if a delivered/archived presentation's rendered content is overwritten rather than versioned | Must have |
| FR-28 | The archive is browsable via the portal presentations index | Must have |
| FR-29 | A delivered presentation can be superseded by creating a new version (incrementing `version` in `manifest.yaml`) | Must have |
| FR-30 | Presentations in `status: draft` are not published to the portal presentations index | Should have |

### 5.6 Portal Integration

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-31 | The architecture portal includes a `Presentations` section listing all governed presentations that are `status: review`, `delivered`, or `archived` | Must have |
| FR-32 | Each portal presentation entry shows: title, type, version, status, delivery date (if applicable), audience, and cross-referenced ADRs | Must have |
| FR-33 | Portal entries link to the rendered HTML for the current version and to the archive for previous versions | Must have |
| FR-34 | The portal presentations section is searchable and filterable by `type`, `status`, and referenced ADR or capability | Should have |
| FR-35 | The capability changelog entry for a solution links to the corresponding presentation if one exists | Should have |

### 5.7 Theme System

Themes are Marp CSS files. Marp is the rendering engine; it reads a CSS file named by the
`theme` key in each slide deck's front matter and applies it during HTML and PDF generation.
MkDocs is not involved in slide rendering — it only builds the portal index page. A theme
change requires a PR; the rendered output is deterministic, so a CI diff will show the visual
impact of any theme modification before it is merged.

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-36 | Themes are defined as CSS files versioned in `presentations/themes/` | Must have |
| FR-37 | At minimum five themes are defined: `architecture-hld`, `architecture-adr`, `architecture-onboarding`, `architecture-strategy`, `architecture-review-board` | Must have |
| FR-38 | A theme change that alters the visual appearance of all presentations requires a PR with at least one reviewer | Should have |
| FR-39 | Each theme applies organisational identity (colour palette, typography, logo) consistently across all presentations using that theme | Must have |
| FR-40 | Each theme CSS file defines organisational identity values as CSS custom properties (design tokens) at the `:root` level — colour palette, font family, and font size scale are expressed as variables so that a brand update requires editing one block, not scattered individual rules | Must have |
| FR-41 | Logo assets used in theme CSS are bundled as inline SVG data URIs within the CSS file — no external URL references are permitted, consistent with NFR-13 (no network calls at render time) | Must have |

---

## 6. Non-Functional Requirements

### 6.1 Performance

| ID | Requirement |
|----|-------------|
| NFR-01 | Rendering a single presentation (diagram pre-render + slide render + portal update) completes in under 3 minutes in CI |
| NFR-02 | The portal presentations index page renders in under 2 seconds in a standard browser |
| NFR-03 | PDF output for a 20-slide deck is produced in under 60 seconds |

### 6.2 Reliability

| ID | Requirement |
|----|-------------|
| NFR-04 | CI rendering is deterministic — the same source input always produces identical HTML output |
| NFR-05 | A rendering failure for one presentation does not block CI for unrelated presentations or for the main portal build |
| NFR-06 | Archive writes are atomic — a partial write (e.g., CI runner killed mid-copy) does not corrupt the archive directory |

### 6.3 Maintainability

| ID | Requirement |
|----|-------------|
| NFR-07 | The rendering pipeline is implemented as Python scripts using stdlib and well-supported packages (no bespoke rendering engines) |
| NFR-08 | Each script has a clear single responsibility (validate, render, archive, generate index) |
| NFR-09 | Adding a new presentation type requires only: adding an entry to the theme configuration YAML and creating a CSS file — no code change in the rendering scripts |
| NFR-10 | The JSON Schema for manifest validation is the canonical definition of all required fields — it is not duplicated in script validation logic |

### 6.4 Security

| ID | Requirement |
|----|-------------|
| NFR-11 | No presentation source file embeds external URLs, credentials, or corporate identifiers (enforced by CI lint step) |
| NFR-12 | Rendered HTML output uses a Content Security Policy that disables inline scripts (enforced in `staticwebapp.config.json`) |
| NFR-13 | PDF generation does not make network calls at render time — all resources (fonts, images, theme CSS) are bundled locally |
| NFR-14 | CI rendering runs in a sandboxed GitHub Actions runner with no access to production secrets |

### 6.5 Portability

| ID | Requirement |
|----|-------------|
| NFR-15 | Presentation source files are pure Markdown with no tool-specific extensions — they are readable without the rendering pipeline |
| NFR-16 | The rendering pipeline runs on any POSIX system with Python 3.12+, Node.js 20+, and the Java runtime (for PlantUML) — same prerequisites as the existing portal build |
| NFR-17 | Rendered HTML files are self-contained (no external CDN dependencies) so they can be emailed, shared as files, or hosted on any static server |

---

## 7. Relationship to Other Pillars

| Pillar | Relationship |
|--------|--------------|
| Pillar E — Architecture Artifacts as Code | Presentations re-use the PlantUML and Mermaid rendering infrastructure from Pillar E. The same diagram pre-render step that produces SVGs for the microservice portal pages also produces SVGs for slide diagrams. |
| Pillar L — Wireframes as Code | Excalidraw wireframes (Pillar L) may be referenced in presentations but are not embedded as code blocks — they are referenced as static SVG exports. PrC governs slide decks; Pillar L governs UI design artifacts. |
| Pillar M — Documentation as Code | Presentations and documentation share the MkDocs Material infrastructure but serve distinct purposes. Documentation is persistent reference material; presentations are point-in-time communication artifacts. The portal hosts both but under separate navigation sections. |
| Pillar O — Governance as Code | The change proposal workflow (Pillar O) applies when a delivered presentation is superseded or a theme change affects all presentations. PrC is a governed pillar — it does not create its own governance mechanism but uses the one Pillar O defines. |
| Pillar G — Decisions as Code | ADRs (Pillar G) are the primary cross-referenced artifact type in presentation manifests. A HLD presentation typically cites 3-6 ADRs. The bidirectional link (ADR → presentation, presentation → ADR) is enforced by CI validation. |
| Pillar C — Capabilities as Code | The capability changelog (Pillar C) references the presentation ID for the solution that introduced a capability change. This creates the chain: ticket → solution design → HLD presentation → capability change record. |

---

## 8. What This Capability Is NOT

It is important to state explicitly what Presentations as Code does not govern, because the
boundary is frequently misunderstood:

| Not in scope | Why |
|-------------|-----|
| Informal working-session slide decks | No permanent architectural significance; governance overhead exceeds value |
| Vendor demo presentations and external decks | Not authored by the architecture practice; cannot be made version-controlled |
| The `presentations/continuous-architecture/` MkDocs site | This is a narrative web presentation (Pillar M territory); it uses MkDocs pages, not slide format. It predates PrC and is a separate, compatible artifact. See Section 10 for the boundary. |
| Excalidraw wireframes (`architecture/wireframes/`) | These are Pillar L (Wireframes as Code). They are design artifacts, not communication decks. |
| Binary slide files attached to tickets | Binary files are explicitly out of scope. If a ticket attachment is architecturally significant, it should be re-authored as a PrC slide deck. |
| Meeting agendas formatted as slides | Presentations as Code governs architecturally significant communication, not operational meeting materials. |

---

## 9. The Existing presentations/ Directory

This workspace already has a `presentations/continuous-architecture/` directory containing a
MkDocs Material site. This site has its own `mkdocs.yml`, `docs/`, and `site/` structure and
produces a standalone web presentation about the Continuous Architecture Platform.

That artifact is **not** a Presentations as Code artifact in the Pillar N sense. It:

- Uses MkDocs pages (not slide format with `---` separators)
- Has no manifest that registers it in the governed presentation library
- Is not rendered by the Marp-based rendering pipeline
- Has no cross-reference validation against ADRs or capabilities

It is a valuable artifact and should be preserved. The implementation plan (Section 2 of the
plan document) explicitly handles how it coexists with Pillar N without conflict. The two
structures are complementary, not redundant.

---

## 10. Success Criteria

The capability is considered successfully implemented when all of the following are true:

### Wave 1 (L1 Maturity) — Complete

- [ ] At least one governed presentation exists with a valid `manifest.yaml`
- [ ] The manifest validates against the published JSON Schema in CI
- [ ] The presentation source file is committed to `presentations/` in the repository
- [ ] CI runs on every PR that touches `presentations/`

### Wave 2 (L2 Maturity) — Core Pipeline

- [ ] CI renders every changed presentation to HTML
- [ ] Rendered HTML is published to the architecture portal under `Presentations`
- [ ] The portal presentations index lists all `review`, `delivered`, and `archived` presentations
- [ ] PDF output is generated for `hld`, `strategy`, and `review-board` type presentations
- [ ] At least three governed presentations exist covering different `type` values

### Wave 3 (L3 Maturity) — Notation Compliance and Theme Library

- [ ] All diagrams in governed presentations are PlantUML or Mermaid code blocks (zero screenshot images)
- [ ] The CI diagram pre-render step runs before the slide renderer on every PR
- [ ] A CI check rejects any `<img>` reference to a local `.png` or `.jpg` inside a slide source file
- [ ] The five required Marp CSS themes are defined in `presentations/themes/` and applied correctly to their respective `type` values
- [ ] Each theme CSS file uses CSS custom properties (`:root` design tokens) for colour palette, font family, and font size scale
- [ ] Logo assets are bundled as inline SVG data URIs in each theme CSS — no external URL references exist in any theme file
- [ ] A rendered HTML output from each theme is visually reviewed and confirmed on-brand before the theme is merged to `main`

### Wave 4 (L4 Maturity) — Governance and Archive

- [ ] CI validates all ADR, capability, and ticket cross-references in every manifest
- [ ] Presentations with `status: delivered` are automatically archived by CI on merge to `main`
- [ ] The archive directory structure is correct and browsable via the portal
- [ ] A staleness detection job runs on a schedule and opens Issues for presentations with stale references
- [ ] The bidirectional capability changelog → presentation link is established for all post-Wave 4 solutions

### AI-Readiness (L5 Maturity)

- [ ] A GitHub Copilot Agent Mode prompt reliably generates a syntactically correct first-draft `slides.md` from a solution design folder
- [ ] An AI agent can answer questions about presentation content from the Markdown source (e.g., "What did HLD-001 say about the data model?")
- [ ] The staleness detection job is AI-augmented (uses an LLM to interpret whether a reference change is substantively breaking or cosmetic)

---

## 11. Data Model

### Presentation Lifecycle States

```
draft ──────────────────────────────────── abandoned (no manifest)
  │
  ▼
review ──────────────────────────────────── withdrawn
  │
  ▼
delivered ──────────────────────────────── (archived by CI automatically)
  │
  ▼
archived (permanent record — immutable rendered output in presentations/archive/)
```

State transitions:
- `draft` → `review`: Author manually sets status; triggers CI render for stakeholder review
- `review` → `delivered`: Author sets status after delivery event; CI triggers archive step
- `delivered` → `archived`: Automatic — CI sets this after archiving; the presentation is now a permanent record
- Any state → `archived` (manual): Governance lead can archive a draft that was never delivered

### Presentation Identifier Convention

Identifiers follow a type-prefix convention:

| Type | Prefix | Example |
|------|--------|---------|
| High-Level Design | `HLD-` | `HLD-001`, `HLD-002` |
| ADR Walkthrough | `ADR-WALK-` | `ADR-WALK-001` |
| Onboarding briefing | `OB-` | `OB-001` |
| Strategy/Roadmap | `STR-` | `STR-001` |
| Architecture Review Board | `ARB-` | `ARB-001` |

---

## 12. Quality Attributes (ISO 25010)

| Characteristic | Assessment |
|---------------|------------|
| Functional Suitability | The capability addresses all five use cases defined in Section 4.2. The rendering pipeline produces HTML and PDF suitable for direct stakeholder delivery. |
| Performance Efficiency | Incremental rendering (only changed presentations re-rendered) keeps CI latency within the 3-minute threshold (NFR-01). |
| Compatibility | Slide source format (Markdown + `---` separators) is compatible with multiple renderers (Marp, Slidev, Pandoc). No proprietary extensions are required. |
| Reliability | Deterministic rendering (NFR-04) and atomic archive writes (NFR-06) prevent silent corruption. |
| Security | CSP enforcement on rendered HTML (NFR-12) and sandboxed CI rendering (NFR-14) address presentation content security. |
| Maintainability | Single-responsibility scripts (NFR-08) and schema-driven validation (NFR-10) minimize coupling. Adding a new presentation type requires zero code changes (NFR-09). |
| Portability | Self-contained rendered HTML (NFR-17) allows offline sharing. Standard tool prerequisites (NFR-16) enable the pipeline on any CI environment. |

---

## 13. Constraints

| Constraint | Source | Impact |
|-----------|--------|--------|
| Azure Static Web Apps Free tier | Existing infrastructure | Maximum 100 GB bandwidth/month; no custom authentication on routes — presentation preview links are publicly accessible |
| GitHub Actions free tier | CI/CD platform | 2,000 minutes/month on free plan; rendering must be incremental to stay within quota |
| PlantUML requires Java runtime | Diagram pre-render step | All CI runners must have JRE installed; same constraint as the existing portal build |
| MkDocs Material is the portal framework | Existing technology choice | Portal presentation index page is generated by a Python script that integrates with the MkDocs navigation — not a standalone site per presentation |
| No separate Azure SWA per presentation | Cost and operational complexity | Presentations are hosted as subdirectories under the main portal SWA, not as individual SWA resources |

---

## 14. Assumptions

| ID | Assumption | Consequence if Wrong |
|----|-----------|----------------------|
| A-01 | The Marp CLI (`@marp-team/marp-cli`) produces self-contained HTML that does not require external CDN dependencies when `--allow-local-files` is used | If wrong, rendered HTML requires a CDN at render time; workaround is `--html` flag with inline assets |
| A-02 | PlantUML diagram pre-rendering using the existing `generate-svgs.sh` script is reusable for presentations with minimal modification | If wrong, a separate diagram pre-render script is needed for presentations |
| A-03 | GitHub Actions can install Marp CLI via `npm install -g @marp-team/marp-cli` without requiring a separate Docker container | If wrong, add a Docker-based rendering step |
| A-04 | The existing `presentations/continuous-architecture/` site is not migrated to Pillar N Marp format — it remains as a standalone MkDocs site | If wrong (user wants it migrated), the migration adds Wave 2 effort but does not block the core pipeline |
| A-05 | Presentation PDF output is generated by Marp's built-in Chromium headless renderer (via `--pdf`) — no separate Puppeteer or wkhtmltopdf installation is required | If wrong, add a `puppeteer` dependency or use a GitHub Action with a pre-installed Chromium |

---

## 15. Open Questions

| ID | Question | Owner | Target Resolution |
|----|---------|-------|-------------------|
| OQ-01 | Should `status: draft` presentations be visible in the portal (with a draft watermark), or hidden entirely until `review`? | Architecture Practice Lead | Before Wave 2 implementation |
| OQ-02 | Is the speaker notes view required as a separate HTML page, or is inclusion in the PDF sufficient? | Solution Architect | Before Wave 2 implementation |
| OQ-03 | Should the staleness detection job file a PR (automated update) or a GitHub Issue (human decision)? | Practice Lead | Before Wave 4 implementation |
| OQ-04 | What is the retention policy for archive entries? Are old versions of archived presentations ever deleted? | Practice Lead | Before Wave 4 implementation |
| OQ-05 | Does the `presentations/continuous-architecture/` site need to appear in the portal presentations index, or is it always accessed via its direct URL? | Architect | Before Wave 1 implementation |

---
