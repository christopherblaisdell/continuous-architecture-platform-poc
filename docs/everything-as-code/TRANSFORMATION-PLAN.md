# Adoption Plan Template — Everything as Code (Blueprint)

> **BLUEPRINT — TEMPLATE.** This is a portable, target-agnostic adoption plan template. It is **not** a plan executed against this synthetic workspace. It is exported to a corporate **EaC Adoption Instance** workspace, where each section is tailored to the actual systems, services, and architecture practice in scope.
>
> The pillar structure, adoption steps, exit criteria, and CI patterns are the durable contributions of this template. Specific tool selections, file names, and folder layouts must be derived from the Instance assessment — not copied from any exemplar.

This template brings an architecture practice from a baseline state to **Level 9 — AI-Native EaC** by addressing each discipline ("pillar") in turn. Pillar adoption is independent — teams may adopt them in any order that fits their practice. The [Sequencing Guide](#sequencing-guide) at the end of this document suggests a dependency-aware order.

## Guiding Principles

1. **No artifact left behind** — every deliverable in the architecture practice has an as-code home
2. **Schema before automation** — every YAML gets a JSON Schema before generators consume it
3. **CI enforces the loop** — Codify → Validate → Generate → Publish runs on every PR
4. **Drift is a build failure** — generated artifacts that diverge from source fail CI
5. **AI is a first-class author** — every artifact must be readable and editable by an AI agent
6. **Open formats always** — canonical sources use open, text-based standards; derived formats are generated, never hand-edited
7. **Portability over convenience** — choose formats that survive tool changes; avoid vendor lock-in in canonical sources

---

## Bootstrap — Instance Charter

**Goal**: Make EaC an explicit organizational commitment before any pillar work begins.

### Tasks

- [ ] Import this blueprint into the corporate workspace as `docs/everything-as-code/`
- [ ] Conduct a real **current-state assessment** by tailoring the synthetic exemplar template (replace findings, keep structure)
- [ ] Review and ratify the framework with architecture practice stakeholders
- [ ] Author an **"Adopt Everything as Code"** ADR in the corporate decisions log
- [ ] Add an EaC compliance section to the corporate AI instruction hub
- [ ] Add an "Everything as Code Transformation" track to the corporate roadmap
- [ ] Identify a pilot pillar to demonstrate value within the first sprint

### Exit criteria

- Adoption ADR merged
- Real current-state assessment completed
- Roadmap reflects EaC as a top-level track
- Pilot pillar identified

---

## Pillar 1 — Infrastructure as Code (IaC)

**What it means**: Every cloud resource, network rule, and environment configuration is declared in text files that are version-controlled, reviewed via PR, and applied automatically.

### Artifact types

- Bicep / Terraform / Pulumi / CloudFormation modules
- Environment variable and secret references (never secret values)
- Resource group and subscription-level policies

### Adoption steps

- [ ] Inventory all infrastructure currently managed manually (console clicks, shell scripts, runbooks)
- [ ] Select an IaC tool appropriate to your cloud platform and team skill set; author the selection ADR
- [ ] Migrate existing manually-managed resources to declarative modules, starting with the highest-churn environment
- [ ] Establish a `infra/` folder (or equivalent) as the canonical location; document the convention in your AI instruction hub
- [ ] Wire CI to run plan/validate on every PR; require human approval before apply on production

### CI integration

- `terraform validate` / `bicep build` / `pulumi preview` on every PR
- Drift detection: scheduled run comparing declared state to actual cloud state
- Secret scanning: block any file containing plaintext credentials

### Exit criteria

- Zero infrastructure changes made outside of version-controlled IaC
- CI validates every proposed change before merge
- Drift check runs on a schedule and alerts on divergence

---

## Pillar 2 — Pipeline as Code (PaC)

**What it means**: Every build, test, release, and deployment workflow is declared in version-controlled YAML or DSL files, not configured through a GUI.

### Artifact types

- GitHub Actions workflows, GitLab CI pipelines, Jenkinsfiles, Tekton pipeline definitions
- Reusable composite actions or pipeline templates
- Environment promotion rules

### Adoption steps

- [ ] Audit existing pipelines; identify any defined only in a CI/CD GUI (not in source control)
- [ ] Migrate all GUI-only pipelines to YAML definitions committed alongside the code they build
- [ ] Create reusable pipeline templates for common patterns (build, test, deploy, scan)
- [ ] Enforce the convention: pipeline files live in `.github/workflows/`, `.gitlab-ci.yml`, or equivalent — never in external systems only

### CI integration

- `actionlint` (GitHub Actions) or equivalent linter on every PR touching pipeline files
- Dry-run or syntax validation before merge

### Exit criteria

- Zero active pipelines exist only in a CI/CD GUI
- Reusable templates documented and linked from the developer guide

---

## Pillar 3 — Actors as Code

**What it means**: Every human role, team, external system, and persona that interacts with your architecture is declared in a version-controlled YAML registry.

### Artifact types

- Actor registry YAML: each entry declares name, type (human / system / external), domain, and responsibilities
- JSON Schema validating the registry
- Generated portal pages or diagrams showing actor-to-service relationships

### Adoption steps

- [ ] Identify all actors in your architecture practice (teams, personas, external partners, automated systems)
- [ ] Create an `architecture/metadata/actors.yaml` (or equivalent) with one entry per actor
- [ ] Author a JSON Schema for the registry; add `$schema` header to the YAML
- [ ] Add CI validation so new actors without required fields fail the PR
- [ ] Wire a generator to produce actor context pages or C4 Person elements from this source

### CI integration

- JSON Schema validation on every PR touching the actors registry
- Drift detection: generated actor diagrams must match the registry

### Exit criteria

- All actors declared; schema-validated in CI
- At least one generated artifact (diagram or portal page) derives from the registry

---

## Pillar 4 — Applications as Code

**What it means**: Every application, service, and deployable unit in your portfolio is declared in a version-controlled registry that is the authoritative source for names, owners, repositories, and deployment targets.

### Artifact types

- Application / service registry YAML
- Domain grouping and ownership metadata
- JSON Schema validating the registry
- Generated service catalog pages

### Adoption steps

- [ ] Enumerate every deployable unit in your portfolio (microservices, batch jobs, scheduled functions, frontends)
- [ ] Create a service registry YAML with fields: name, domain, owner team, repository, deployment target, API spec path
- [ ] Author a JSON Schema; add `$schema` header
- [ ] Wire CI validation; wire a generator to produce the service catalog in your documentation portal
- [ ] Enforce: any new service added to a CI pipeline MUST have a corresponding registry entry (policy rule)

### CI integration

- JSON Schema validation on every PR touching the registry
- Policy check: services in pipeline definitions exist in the registry (OPA / Conftest)

### Exit criteria

- Every deployable unit in the portfolio has a registry entry
- Service catalog published and generated from the registry

---

## Pillar 5 — Architecture Artifacts as Code

**What it means**: Every architecture diagram — C4 context, container, component, sequence, event flow, deployment — is produced from a declarative source file, not drawn manually in a diagramming tool and exported as an image.

### Artifact types

- C4 model: Structurizr DSL, Likec4, or equivalent — describes system context, containers, and components
- Sequence diagrams: PlantUML or Mermaid, ideally generated from OpenAPI / AsyncAPI specs
- Event flow diagrams: generated from event registry YAML
- Deployment diagrams: generated from IaC or infrastructure metadata
- CALM (Cloud Architecture Language and Modeling) definitions for machine-readable architecture

### Adoption steps

- [ ] Audit existing diagrams; identify which are hand-drawn images with no declarative source
- [ ] Select a C4 DSL appropriate to your team; author the selection ADR
- [ ] Author C4 Level 1 (System Context) for your highest-visibility system first; commit the DSL source
- [ ] For each service with an OpenAPI spec, wire a sequence diagram generator that produces PUML from the spec
- [ ] Migrate hand-drawn diagrams to DSL sources; retire the image-only versions
- [ ] Wire CI to generate SVG outputs from all DSL sources and run a drift check

### CI integration

- `plantuml -checkonly` / `structurizr-cli validate` on every PR
- Drift check: generated SVGs must match DSL source on every PR
- Spec validator: OpenAPI / AsyncAPI pass schema validation before diagram generation runs

### Exit criteria

- Zero hand-drawn diagrams in the architecture practice without a corresponding DSL source
- All C4 levels 1-3 declared; diagrams generated and published to the documentation portal
- Sequence diagrams generated from API specs, not hand-maintained

---

## Pillar 6 — Capabilities as Code

**What it means**: The capability model of the architecture practice — the business capabilities the systems enable — is declared in a version-controlled YAML hierarchy with a JSON Schema, and a changelog records how capabilities evolve over time.

### Artifact types

- Capability hierarchy YAML (L1 / L2 / L3 capabilities)
- Capability changelog YAML: one entry per solution or change, recording which capabilities were affected and how
- JSON Schemas for both files
- Generated capability pages in the documentation portal

### Adoption steps

- [ ] Define your L1 and L2 capability taxonomy in a YAML file; keep it to ~30-50 entries to start
- [ ] Author a JSON Schema for the capability hierarchy; validate in CI
- [ ] Create a capability changelog YAML; establish the convention that every solution design records its capability impacts here
- [ ] Wire a generator to produce capability pages from the hierarchy and changelog
- [ ] Establish a policy: any solution design PR that does not update the capability changelog fails CI

### CI integration

- JSON Schema validation on both capability files on every PR
- Policy check: solution design folders MUST have a corresponding changelog entry

### Exit criteria

- Capability hierarchy declared; validated in CI
- Capability changelog in active use; every delivered solution has a recorded entry
- Generated capability pages published in the portal

---

## Pillar 7 — Decisions as Code (ADRs)

**What it means**: Every architecture decision — tool selection, pattern choice, data ownership boundary, API contract convention — is recorded in a version-controlled Markdown file using a standard template (MADR), reviewable via PR, and linked from the artifacts it governs.

### Artifact types

- Markdown Any Decision Record (MADR) files, one per decision
- ADR index page (generated)
- Links from capability pages, solution designs, and API specs back to governing ADRs

### Adoption steps

- [ ] Adopt MADR as the standard template (Status, Date, Context, Decision Drivers, Considered Options, Decision Outcome, Consequences)
- [ ] Establish a `decisions/` folder; number ADRs sequentially
- [ ] Back-fill the highest-impact existing decisions as ADRs (start with the 5 most consequential choices currently undocumented)
- [ ] Author a MADR validator script that asserts required sections exist; wire to CI
- [ ] Add a generator that produces `decisions/INDEX.md` from ADR frontmatter or headings
- [ ] Establish the convention: any PR that introduces a new cross-service boundary or changes data ownership MUST include an ADR

### CI integration

- MADR validator on every PR touching `decisions/` or solution-level decision files
- Generated index must not drift from the decisions on disk

### Exit criteria

- All significant active architectural constraints are recorded as ADRs
- MADR validator enforced in CI; missing required sections block merge
- ADR index page generated and published

---

## Pillar 8 — Tickets as Code

**What it means**: The work that shapes the architecture — feature tickets, architecture investigations, solution designs — is tracked in a version-controlled YAML registry linked to the capability model, so the connection between delivered work and architectural capability is machine-readable.

### Artifact types

- Ticket registry YAML: each entry declares ID, title, status, owning service(s), and planned or realized capability impacts
- JSON Schema validating the registry
- Generated ticket pages in the documentation portal

### Adoption steps

- [ ] Define the fields your ticket registry must carry (at minimum: ID, title, status, affected services, capability references)
- [ ] Author the registry YAML and JSON Schema; seed with current active work
- [ ] Establish a convention: new solution designs add a registry entry before work begins
- [ ] Wire a generator to produce ticket pages and cross-link them from capability and service pages
- [ ] Wire CI validation: capability IDs referenced in tickets must exist in the capability hierarchy

### CI integration

- JSON Schema validation on every PR touching the ticket registry
- Referential integrity check: capability IDs in tickets exist in capabilities YAML

### Exit criteria

- Active tickets registered; schema-validated in CI
- Generated ticket pages published and cross-linked from capability and service pages

---

## Pillar 9 — Tests as Code

**What it means**: Behavioral expectations for every service and capability are expressed in declarative specification files (Gherkin feature files, contract specs) that are executable in CI, not just documentation.

### Artifact types

- Gherkin `.feature` files organized by capability
- Consumer-Driven Contract (CDC) specs (Pact, Spring Cloud Contract)
- Test coverage report: capabilities with and without feature file coverage
- CI test runner configuration

### Adoption steps

- [ ] Audit existing test artifacts; classify each as "executable in CI" or "documentation only"
- [ ] Select a BDD runner appropriate to your tech stack (Cucumber, Behave, SpecFlow, pytest-bdd)
- [ ] Wire the runner in CI; ensure feature files produce machine-readable reports (JUnit XML or equivalent)
- [ ] Establish a convention: new capabilities require at least one `.feature` file before the capability is marked delivered
- [ ] Generate a capability-to-feature coverage report; publish in the portal
- [ ] For contract tests: identify producer-consumer pairs with the highest integration risk; introduce CDC specs there first

### CI integration

- BDD runner executes all `.feature` files on every PR
- Coverage report generated and published as a CI artifact
- Contract tests run on every PR touching an API spec or its consumer

### Exit criteria

- All `.feature` files execute in CI without manual setup
- Capability-to-feature coverage report published
- At least the highest-risk producer-consumer pairs have contract specs enforced in CI

---

## Pillar 10 — Policy as Code

**What it means**: Architectural governance rules — "every service must have an OpenAPI spec", "no cross-domain direct database access", "every ADR referenced in the changelog must exist" — are expressed as machine-readable policy files enforced automatically in CI, not enforced by reviewer vigilance alone.

### Artifact types

- OPA Rego rules (or Conftest policies) under `policies/`
- Policy catalog README: what each rule checks and why
- CI workflow running `conftest test` on every PR

### Adoption steps

- [ ] Identify the 5 governance rules most frequently violated or most costly when violated
- [ ] Create a `policies/` folder; author the first rule as a Rego file
- [ ] Wire `conftest test` to a CI workflow; confirm the first rule blocks a non-compliant PR
- [ ] Add rules incrementally — one per sprint — starting with referential integrity checks (IDs that reference other IDs must resolve)
- [ ] Document each rule: what it checks, what violation means, how to fix it
- [ ] Establish a governance ADR for adding or removing policy rules (changes to the rulebook require review)

### CI integration

- `conftest test` on every PR
- Policy violations block merge; findings include the rule name and remediation hint
- Policy catalog published in the documentation portal

### Exit criteria

- At least 5 policy rules active and enforced in CI
- Rule catalog documented and published
- Zero governance rules enforced only by reviewer comments

---

## Pillar 11 — AI Instructions as Code (AIaC)

**What it means**: The behavioral instructions that govern how AI agents operate in your development environment — what they know, how they respond, what they are forbidden from doing — are declared in version-controlled text files, reviewed via PR, and propagated to every supported AI tool from a single canonical hub.

### Artifact types

- Canonical hub file (e.g., `.github/copilot-instructions.md`) — the single source of truth
- Derived instruction files for each AI tool in use (Cursor, Windsurf, Roo Code, Continue.dev, etc.)
- OpenSpec governance spec: RFC 2119-language rules for the hub and derived files
- Validation script: verifies all required derived files exist and match expected structure
- Change archive: record of completed OpenSpec cycles

### Adoption steps

- [ ] Identify all AI tools in active use in your development environment
- [ ] Designate a canonical hub file; migrate all per-tool instruction content into it as the source of truth
- [ ] Author derived instruction files for each tool, each containing a `DERIVED FILE` header pointing to the hub
- [ ] Author an OpenSpec governance spec declaring the required hub sections, derived file names, and change workflow
- [ ] Implement a validation script that checks hub and derived file consistency; wire to CI
- [ ] Run the first change cycle: propose a new rule → apply to hub → propagate to derived files → archive the change
- [ ] Evaluate additional derived targets as new AI tools are adopted

### CI integration

- Validation script on every PR touching instruction files
- OpenSpec change archive updated as part of every instruction change PR

### Exit criteria

- All AI tools derive instructions from the canonical hub
- Validation script active in CI; hub-and-spoke architecture documented
- At least one complete change cycle archived

---

## Pillar 12 — Wireframes as Code (UIaC)

**What it means**: UI/UX wireframes and mockups are stored as structured JSON files (Excalidraw, Penpot, or equivalent) in version control, not as exported images in a design tool cloud. Changes are reviewable as diffs; images are generated by CI.

### Artifact types

- `.excalidraw` JSON files (or equivalent open-format design source)
- Generated SVG previews for embedding in documentation
- Generated interactive HTML viewers for design review
- Markdown portal pages linking wireframe to the corresponding architecture section

### Adoption steps

- [ ] Identify all active UI/UX wireframes; locate which exist only in a design tool cloud with no version-controlled source
- [ ] Select an open-format wireframing tool whose files are plain text (fully diffable JSON)
- [ ] Export all active wireframes to the open format; commit to `architecture/wireframes/{app}/`
- [ ] Wire a CI step to generate SVG and HTML from the source files and publish to the documentation portal
- [ ] Establish the naming convention: kebab-case, feature-descriptive names; no version numbers in filenames (git history provides that)
- [ ] Establish the workflow: wireframes precede API contract changes — design the flow first, then define integration points

### CI integration

- SVG / HTML generation runs on every PR touching wireframe source files
- Drift check: generated outputs must match source on PR

### Exit criteria

- Zero active wireframes exist only in a design tool cloud without a version-controlled source
- SVG previews generated and published in the documentation portal

---

## Pillar 13 — Documentation as Code (Docs as Code)

**What it means**: All architecture documentation — service pages, capability pages, decision records, solution designs, runbooks — is authored in Markdown (or equivalent plain text), version-controlled, reviewed via PR, and published by a CI/CD pipeline. No documentation lives only in a wiki or a PDF.

### Artifact types

- MkDocs / Docusaurus / Sphinx site source under `portal/docs/` (or equivalent)
- Automatically generated pages from YAML metadata (service pages, capability pages, ticket pages)
- Published static site deployed on every merge to main
- Drift check: generated pages cannot diverge from their source YAML

### Adoption steps

- [ ] Select a static site generator appropriate to your practice (MkDocs Material is recommended for architecture portals)
- [ ] Author a `portal/docs/` structure mirroring your architecture practice sections
- [ ] Identify which pages are currently hand-maintained but should be generated from YAML (service catalog, capability map, ADR index)
- [ ] Wire generators for each such page type; add drift checks to CI
- [ ] Wire CI to build and deploy the portal on every merge to main
- [ ] Add `mkdocs build --strict` (or equivalent) to PR CI to catch broken internal links before merge
- [ ] Add `markdownlint` to PR CI to enforce consistent Markdown style

### CI integration

- `mkdocs build --strict` on every PR
- `markdownlint` on every PR touching `.md` files
- Drift check: generated pages must match source YAML on every PR
- Portal deployed automatically on merge to main

### Exit criteria

- Zero documentation exists only in a wiki or PDF that is not mirrored or replaced in the portal
- All generated pages validated against their source in CI
- Portal deployed automatically on merge to main

---

## Pillar 14 — Governance as Code

**What it means**: The change governance workflow itself — how proposals are submitted, reviewed, approved, and archived — is declared in structured files and executed via tooling, not via informal Slack threads or undocumented review customs.

### Artifact types

- OpenSpec change specs: machine-readable change proposals with RFC 2119 language
- Change archive: completed proposals with approvals and outcomes recorded
- Governance ADR: the meta-decision declaring how governance rules are changed
- Policy rules enforcing that governed artifacts are only changed via the declared workflow

### Adoption steps

- [ ] Identify the highest-governance artifacts in your practice (API specs, AI instructions, architectural schemas, policy rules)
- [ ] Author a governance spec for at least one artifact type: what fields are required, who can approve changes, what the change workflow looks like
- [ ] Adopt OpenSpec (or an equivalent structured change proposal format) for governing changes to AI instruction files
- [ ] Archive the first completed change cycle as proof of the workflow
- [ ] Add a governance ADR: any change to a governance spec requires a PR reviewed by the architecture practice lead
- [ ] Wire a policy rule that validates governance metadata on every PR touching governed artifacts

### CI integration

- Governance spec validation on every PR touching governed artifacts
- Change archive completeness check: open proposals must not sit unresolved beyond a defined SLA

### Exit criteria

- At least one artifact class governed end-to-end with a declared, archived change workflow
- Governance ADR in the decisions log
- Policy rule enforcing governance in CI

---

## Pillar 15 — Operational Runbooks as Code

**What it means**: Every operational procedure — deployment steps, rollback procedures, on-call playbooks, incident response guides — is expressed as version-controlled Markdown with explicit commands and expected outputs, or as executable scripts/workflows. No procedures exist only in a wiki or in someone's head.

### Artifact types

- Markdown runbooks under `docs/operations/` with explicit command blocks and expected outputs
- Executable scripts or GitHub Actions / Tekton tasks for automation candidates
- On-call playbooks linked from monitoring alerts
- Runbook index page (generated)

### Adoption steps

- [ ] Inventory all operational procedures; classify each as "in version control" or "in a wiki or undocumented"
- [ ] For each procedure not in version control: author a Markdown runbook with explicit commands and expected outputs
- [ ] For high-frequency procedures (daily deployments, common rollbacks): convert to executable scripts or CI/CD workflow steps
- [ ] Link each runbook from the relevant service page in the documentation portal
- [ ] Add `markdownlint` and spell check to CI for the operations folder
- [ ] Establish a review cadence: runbooks are reviewed and updated at minimum on each major release

### CI integration

- `markdownlint` + spell check on every PR touching `docs/operations/`
- Broken link check: all linked scripts and workflows must exist

### Exit criteria

- Zero critical operational procedures exist only outside of version control
- All runbooks pass `markdownlint` in CI
- Runbook index generated and linked from the documentation portal

---

## Sequencing Guide

Pillar adoption is independent but not isolated — some pillars unlock others. The table below shows recommended sequencing for a practice starting from near zero.

| Wave | Pillars | Rationale |
|------|---------|-----------|
| **Wave 1 — Foundation** | Applications as Code (4), Architecture Artifacts as Code (5) | Establishes the registry of what exists and the canonical diagram sources. Everything else references these. |
| **Wave 2 — Governance** | Decisions as Code (7), Capabilities as Code (6), Actors as Code (3) | Governance and capability model unlock linkability in all later pillars. |
| **Wave 3 — Validation** | Policy as Code (10), Tests as Code (9), Pipeline as Code (2) | Validation pillars are most effective once there is a declared architecture to validate against. |
| **Wave 4 — AI + Docs** | AI Instructions as Code (11), Documentation as Code (13), Tickets as Code (8) | AI instructions require a stable architecture definition to reference. Docs as Code should consolidate outputs from all prior waves. |
| **Wave 5 — Automation** | Governance as Code (14), Wireframes as Code (12), Operational Runbooks as Code (15), Infrastructure as Code (1) | These pillars benefit from the CI patterns established in earlier waves and can proceed in parallel. |

**Critical-path minimum**: Pillars 4 (Applications) and 5 (Architecture Artifacts) are prerequisites for almost everything. Begin there.

**Quick wins** (≤1 day, no dependencies):

- [ ] Add `markdownlint` to PR CI
- [ ] Add `actionlint` (or pipeline linter) to PR CI
- [ ] Add `mkdocs build --strict` (or equivalent) to PR CI
- [ ] Add `# yaml-language-server: $schema=...` header to any YAML that already has a schema
- [ ] Back-fill the single most consequential undocumented decision as an ADR

> **Synthetic exemplar carry-over**: For workspace-specific deferred items that apply only to the synthetic NovaTrek exemplar workspace, see [SYNTHETIC-EXEMPLAR-BACKLOG.md](SYNTHETIC-EXEMPLAR-BACKLOG.md).
