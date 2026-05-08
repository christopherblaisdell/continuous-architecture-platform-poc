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
- [ ] Complete a **pillar selection exercise**: review all 35 pillars in this document; mark each as **In Scope**, **Out of Scope**, or **Future**; record the decision in the adoption ADR

### Exit criteria

- Adoption ADR merged, including a pillar selection record (in scope / out of scope / future for all 35 pillars)
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

> **See also**: [AI-INSTRUCTIONS-AS-CODE.md](AI-INSTRUCTIONS-AS-CODE.md) — full deep dive on the three-layer model, hub-and-spoke architecture, and OpenSpec governance pattern.

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

<!-- THEME: Data Layer — Pillars 16–19 -->

## Pillar 16 — Data Models as Code

**What it means**: Entity schemas, data dictionaries, and entity-relationship definitions are declared in version-controlled text files. The database schema is derived from the declaration — never the other way around.

### Artifact types

- Database schema definition files (SQL DDL, YAML entity specs, dbt models, Avro/Protobuf schemas for shared structures)
- Entity-relationship diagrams generated from schema declarations
- Data dictionary YAML: human-readable descriptions of every table, column, and constraint
- JSON Schema or Avro/Protobuf schemas for data structures shared across services

### Adoption steps

- [ ] Inventory all databases and data stores; identify which have no version-controlled schema declaration
- [ ] Select a schema declaration format appropriate to the data platform (SQL DDL, Liquibase changelogs, dbt sources, YAML entity specs)
- [ ] Declare the current schema for the highest-churn data store first; commit to version control
- [ ] Add a data dictionary YAML with descriptions for every table and column; wire a generator to produce documentation from it
- [ ] Wire CI to validate schema declarations are syntactically correct and match a known format
- [ ] Establish the convention: any PR that changes a data store must update the schema declaration; no undeclared schema changes

### CI integration

- Schema syntax validation on every PR touching schema files
- `schemadiff` or equivalent to detect undeclared divergence between the declared schema and applied migrations
- Data dictionary completeness check: every column must have a description

### Exit criteria

- Every data store has a version-controlled schema declaration
- Data dictionary published and generated from schema files
- CI blocks PRs that introduce undeclared schema changes

---

## Pillar 17 — Database Migrations as Code

**What it means**: Every schema change — adding a column, dropping a table, adding an index, changing a data type — is expressed as a numbered, version-controlled migration file applied in a deterministic sequence. No undeclared schema change ever reaches a database.

### Artifact types

- Migration files: numbered, timestamped SQL or DSL migration scripts (one per change)
- Rollback scripts: corresponding undo operations where applicable
- Migration state table: applied migration log maintained by the migration tool
- CI workflow: migrations validated and applied against an ephemeral test database on every PR

### Adoption steps

- [ ] Select a migration tool appropriate to the data platform (Liquibase, Flyway, Alembic, golang-migrate, Atlas)
- [ ] Initialize the migration tool against the current schema; generate a baseline migration capturing current state
- [ ] Establish the convention: any database change requires a new migration file in the same PR as the application code change
- [ ] Wire CI to run migrations against an ephemeral test database on every PR; confirm the schema matches expectations after migration
- [ ] Document the rollback process; mark migrations that cannot be safely rolled back with an explicit comment
- [ ] Wire a drift check: the migration tool's applied state must match the declared migrations on every build

### CI integration

- Migration tool validates all migration files for syntax on every PR
- Test database provisioned, migrations applied, schema validated, database torn down — on every PR touching migration files
- Drift check: migration tool state must match declared migrations

### Exit criteria

- Zero schema changes applied without a corresponding migration file in version control
- CI applies migrations to a test database on every PR
- Rollback procedure documented for all migration files

---

## Pillar 18 — Data Contracts as Code

**What it means**: Producers of data (event publishers, API providers, data pipeline outputs) explicitly declare their guarantees to consumers in a machine-readable, version-controlled contract. Consumers validate against the contract in CI. Breaking changes require a contract version bump and consumer notification.

### Artifact types

- Data contract YAML files (one per producer–consumer pair or per published dataset): schema, SLA, ownership, version, and changelog
- Consumer registration: which teams consume which contract and at which version
- Breaking change policy: declared in the contract or in a governing ADR
- CI validation: consumer tests run against the contract schema on every PR

### Adoption steps

- [ ] Identify the highest-risk producer-consumer data flows (those where a past breaking change caused an incident)
- [ ] Select a data contract format (Data Contract Specification — Bitol, OpenDataMesh, or custom YAML with JSON Schema)
- [ ] Author the first data contract for the highest-risk flow: declare producer, schema, SLA, version, and consumer list
- [ ] Wire a CI check: consumer integration tests run against the declared contract schema on every PR
- [ ] Establish a breaking change policy ADR: what constitutes a breaking change, how consumers are notified, how versions are bumped
- [ ] Expand to all high-risk flows incrementally; low-risk flows follow as capacity allows

### CI integration

- Contract schema validation on every PR touching contract files
- Consumer integration tests run against the contract on every PR
- Breaking change detector: flag additions/removals of required fields, type changes, and enum changes

### Exit criteria

- All high-risk producer-consumer flows have a declared, version-controlled data contract
- CI runs consumer tests against the contract on every PR
- Breaking change policy documented in an ADR

---

## Pillar 19 — Event Schemas as Code

**What it means**: Every event published to an event bus or message broker — its structure, semantics, producer, and registered consumers — is declared in a version-controlled AsyncAPI spec or schema registry definition. No event topic exists without a machine-readable declaration.

### Artifact types

- AsyncAPI spec YAML files: one per event domain or per producer service
- Schema registry definitions (Avro, Protobuf, JSON Schema) for event payloads
- Event catalog: generated registry of all events, their producers, consumers, and versions
- Consumer registration: which services subscribe to which events

### Adoption steps

- [ ] Inventory all events currently published across all event buses and message brokers
- [ ] Select a schema format for event payloads (Avro for Kafka, JSON Schema for simpler brokers, Protobuf for cross-language high-performance needs)
- [ ] Author AsyncAPI specs for the highest-volume or highest-risk event streams first
- [ ] Wire AsyncAPI validator to CI; wire a schema registry sync step if a registry is in use
- [ ] Generate an event catalog page for the documentation portal from the AsyncAPI specs
- [ ] Establish the convention: no new event topic created without a corresponding AsyncAPI spec in the same PR

### CI integration

- `asyncapi validate` on every PR touching AsyncAPI specs
- Schema registry diff: proposed payload schema changes flagged as breaking or non-breaking
- Drift check: generated event catalog must match AsyncAPI sources

### Exit criteria

- Every event stream has a version-controlled AsyncAPI spec
- Schema validation enforced in CI on every PR
- Event catalog published and generated from specs

---

<!-- THEME: Security and Compliance — Pillars 20–23 -->

## Pillar 20 — Security as Code

**What it means**: Threat models, security scan configurations, RBAC/IAM policies, network security rules, and security testing rule sets are all declared in version-controlled files — reviewed, tested, and enforced automatically. Security is embedded in the development workflow, not bolted on at release.

### Artifact types

- Threat model files (OWASP Threat Dragon JSON, YAML-based STRIDE models)
- Static analysis configs (Semgrep rulesets, SonarQube config, CodeQL query sets)
- SAST/DAST pipeline steps declared in pipeline YAML
- IAM / RBAC policy files (AWS IAM JSON, Azure RBAC Bicep, Kubernetes RBAC YAML)
- Network security group and firewall rules declared in IaC

### Adoption steps

- [ ] Author a threat model for the highest-risk service or data flow; commit as a structured file
- [ ] Select a SAST tool appropriate to the language stack; commit the ruleset configuration to version control
- [ ] Wire SAST scanning to CI as a required check on every PR; configure fail thresholds
- [ ] Declare all IAM / RBAC policies in IaC (not in cloud consoles); review all policy changes via PR
- [ ] Add a dependency vulnerability scan (Dependabot, Snyk, OWASP Dependency-Check) to CI; configure fail thresholds
- [ ] Establish a security ADR for every significant access control decision

### CI integration

- SAST scan on every PR (Semgrep / CodeQL / SonarQube)
- Dependency vulnerability scan on every PR
- IaC security scan (Checkov, Trivy, TFSec) on every PR touching infrastructure files
- Threat model lint: basic structural validation of threat model files

### Exit criteria

- Threat model exists for every high-risk service
- SAST and dependency scanning enforced in CI with defined fail thresholds
- All IAM/RBAC policies declared in version-controlled IaC

---

## Pillar 21 — Compliance as Code

**What it means**: Regulatory and internal compliance requirements (GDPR, SOC2, HIPAA, PCI-DSS, ISO 27001, internal security baselines) are expressed as machine-verifiable rules. Audit evidence is generated automatically from CI/CD results, not assembled manually ahead of an audit.

### Artifact types

- Compliance control YAML: mapping of regulatory controls to declared technical controls
- OPA / Conftest rules implementing compliance checks as code
- Audit evidence manifests: CI-generated records of which controls passed on which commit
- Compliance posture report: generated summary of pass/fail per control framework

### Adoption steps

- [ ] Identify the compliance framework(s) most relevant to the Instance (SOC2, GDPR, PCI, ISO 27001, internal)
- [ ] Map the highest-priority controls to verifiable technical assertions (e.g., "all data at rest encrypted" → check IaC encryption flags)
- [ ] Implement the first 5 controls as OPA / Conftest rules; wire to CI
- [ ] Wire CI to generate an audit evidence manifest on every merge to main: commit hash, timestamp, passing controls, failing controls
- [ ] Store evidence manifests in a durable, immutable location (S3 versioned bucket, Azure Blob immutable tier)
- [ ] Expand controls incrementally; target 80% coverage of the highest-priority framework before expanding to a second

### CI integration

- `conftest test` with compliance ruleset on every PR
- Audit evidence manifest generated and stored on every merge to main
- Compliance posture report published in the documentation portal on a schedule

### Exit criteria

- At least one compliance framework partially covered by machine-verifiable rules
- Audit evidence generated automatically from CI; not assembled manually
- Compliance posture report published and kept current

---

## Pillar 22 — Secrets Management as Code

**What it means**: Every secret, certificate, and API key used by the system is registered, rotated, and access-controlled via a secrets manager whose configuration is itself version-controlled. No secret ever appears in source code, environment variable files, or CI/CD configuration in plaintext.

### Artifact types

- Vault policy files / Key Vault access policy Bicep / AWS Secrets Manager policy JSON
- Secret rotation schedule declarations
- Certificate management configuration (cert-manager manifests, Azure Key Vault certificate policies)
- Secret reference declarations: code references secret names, never secret values

### Adoption steps

- [ ] Inventory all secrets currently in use; identify any hardcoded in source or CI/CD config
- [ ] Select a secrets manager appropriate to the platform (HashiCorp Vault, Azure Key Vault, AWS Secrets Manager, GCP Secret Manager)
- [ ] Migrate all secrets to the secrets manager; remove all plaintext values from every repository
- [ ] Declare access policies (who and what can read which secret) in version-controlled IaC
- [ ] Wire a secret scanning step to CI (truffleHog, git-secrets, GitHub secret scanning) that fails on any committed secret value
- [ ] Declare rotation schedules for all secrets; wire automated rotation where the platform supports it

### CI integration

- Secret scanning on every PR (fails on any plaintext credential or key)
- IaC policy check: no secret values in Terraform/Bicep variable files
- Certificate expiry check: scheduled CI alerts N days before expiry

### Exit criteria

- Zero plaintext secrets in source code, CI config, or container images
- All access policies declared in version-controlled IaC
- Secret scanning enforced in CI on every PR

---

## Pillar 23 — SBOM as Code

**What it means**: A Software Bill of Materials — the complete inventory of every third-party library, framework, and transitive dependency in every deployable artifact — is generated automatically as part of every build, stored in a standard format, and version-controlled alongside the release artifact.

### Artifact types

- CycloneDX or SPDX SBOM documents (one per deployable artifact, per release)
- Dependency lock files committed to version control (`package-lock.json`, `poetry.lock`, `go.sum`, `pom.xml` with locked versions)
- Vulnerability report: known CVEs in current dependencies, generated from the SBOM
- License inventory: third-party licenses declared and reviewed for policy compliance

### Adoption steps

- [ ] Commit all dependency lock files to version control across all services (no floating versions in production artifacts)
- [ ] Select an SBOM generation tool (Syft, cdxgen, `cyclonedx-npm`, `jake`)
- [ ] Wire SBOM generation to the CI build step; store the SBOM alongside the release artifact
- [ ] Wire a vulnerability scan against the SBOM on every build (Grype, Trivy, OSV-Scanner); configure fail thresholds by severity
- [ ] Wire a license compliance check: flag any dependency whose license is not on the approved list
- [ ] Publish a current SBOM for every deployed service in the documentation portal

### CI integration

- SBOM generated on every build
- Vulnerability scan against SBOM on every build; fails on CVEs above the defined severity threshold
- License compliance check on every PR that modifies dependency files

### Exit criteria

- SBOM generated for every deployable artifact on every build
- Vulnerability scanning automated in CI with defined fail thresholds
- All dependency lock files committed to version control

---

<!-- THEME: Observability and Reliability — Pillars 24–26 -->

## Pillar 24 — Observability as Code

**What it means**: Dashboards, alert rules, log queries, tracing configurations, and synthetic monitors are all declared in version-controlled files — reviewed, tested, and deployed via CI/CD, not configured interactively in an observability tool's GUI.

### Artifact types

- Dashboard definitions (Grafana dashboard JSON/YAML, Datadog dashboard Terraform, Azure Workbooks JSON)
- Alert rule declarations (Prometheus alerting rules YAML, Azure Monitor alert Bicep, Datadog Terraform)
- Log query files (KQL, PromQL, LogQL saved as named queries in version control)
- Synthetic monitor definitions (Playwright-based uptime checks, Datadog Synthetics Terraform)
- SLO tracking dashboards linked to Pillar 25 SLO declarations

### Adoption steps

- [ ] Inventory all active dashboards and alerts; identify which exist only in a tool GUI
- [ ] Select an observability-as-code tool appropriate to the stack (Grafana Grizzly, Terraform providers for Datadog/New Relic, Azure Monitor Bicep)
- [ ] Export the three most critical dashboards to their version-controlled format; commit and wire to CI deployment
- [ ] Declare all production alert rules in version-controlled format; retire GUI-only alerts
- [ ] Wire CI to validate alert rule syntax and deploy dashboard/alert changes on merge to main
- [ ] Link dashboards to the services they monitor in the service registry (Pillar 4)

### CI integration

- Alert rule syntax validation on every PR
- Dashboard schema validation on every PR
- Drift check: deployed dashboards must match declared source on a schedule

### Exit criteria

- All production dashboards and alert rules declared in version control
- CI deploys observability configuration changes on merge to main
- Zero active alerts exist only in a GUI with no corresponding version-controlled declaration

---

## Pillar 25 — SLO / SLI as Code

**What it means**: Service Level Objectives and the Service Level Indicators they measure are declared in a standard, machine-readable format per service — linked to the service registry, tracked automatically, and reported without manual data assembly.

### Artifact types

- SLO definition files (OpenSLO YAML, Sloth YAML, or custom YAML with JSON Schema)
- SLI calculation rules: how each indicator is computed from raw metrics
- Error budget tracking declarations: automated error budget burn rate rules
- SLO compliance report: generated per service, per period

### Adoption steps

- [ ] Identify the three most critical services; define one SLO per service (availability or latency to start)
- [ ] Select an SLO declaration format (OpenSLO is the open standard; Sloth generates Prometheus recording rules from it)
- [ ] Declare each SLO as a YAML file linked to the service in the service registry
- [ ] Wire SLI calculation to the metrics stack (Prometheus recording rules, Azure Monitor KQL, Datadog SLO API)
- [ ] Wire error budget tracking to the observability dashboards from Pillar 24
- [ ] Expand SLO coverage incrementally; every service in the registry should have at least one SLO

### CI integration

- OpenSLO / Sloth schema validation on every PR touching SLO files
- SLI calculation rule dry-run on every PR
- Drift check: SLOs declared in files must match SLOs registered in the observability platform

### Exit criteria

- Every service in the service registry has at least one declared SLO
- Error budget tracking automated; no manual data assembly required for SLO reports
- SLO compliance report published on a defined cadence

---

## Pillar 26 — Feature Flags as Code

**What it means**: Feature toggle definitions, targeting rules, and rollout percentages are declared in version-controlled configuration files — not set interactively in a feature flag platform's GUI. Changes to flag behavior flow through PR review, with the same change governance as any other code change.

### Artifact types

- Feature flag definition files (YAML or JSON declaring flag name, type, default, variants, and targeting rules)
- Targeting rule declarations: which user segment or environment sees which variant
- Flag lifecycle policy: when flags are created, when they must be cleaned up (stale flag = tech debt)
- OpenFeature provider config if using the OpenFeature standard

### Adoption steps

- [ ] Select a feature flag platform with a config-as-code mode (LaunchDarkly config export, Unleash YAML, OpenFeature + Flagd, or a custom YAML-backed solution)
- [ ] Declare all currently active flags in version-controlled YAML; wire sync to the flag platform
- [ ] Establish a flag lifecycle policy: maximum flag age, cleanup PR requirement before closing a feature
- [ ] Wire CI to validate flag definition syntax on every PR
- [ ] Link flags to the capabilities they gate (reference Pillar 6); a flag without a capability reference is incomplete
- [ ] Wire a stale flag linter: flags older than the lifecycle policy's maximum age fail CI until cleaned up or explicitly renewed

### CI integration

- Flag definition syntax validation on every PR
- Stale flag check: flags beyond lifecycle age trigger a CI warning or failure
- Platform sync: flag definitions pushed to the feature flag platform on merge to main

### Exit criteria

- All active feature flags declared in version control
- Flag lifecycle policy documented and enforced in CI
- Stale flag linter active

---

<!-- THEME: Deployment and Release — Pillars 27–29 -->

## Pillar 27 — Release Strategies as Code

**What it means**: How a new version of a service is released to production — canary percentages, blue/green cutover rules, A/B test split weights, rollback triggers, and traffic shifting schedules — is declared in version-controlled deployment configuration, not configured interactively in a deployment tool.

### Artifact types

- Progressive delivery configuration (Argo Rollouts Rollout YAML, Flagger Canary YAML)
- Traffic routing rules (Istio VirtualService, Nginx Ingress config, AWS ALB listener rules)
- Rollback trigger thresholds (error rate, latency percentile, custom metric)
- Release strategy ADR: why a given strategy was chosen for a given service class

### Adoption steps

- [ ] Classify services by release risk: high-traffic/safety-critical, standard production, or internal tooling — each class warrants a different default strategy
- [ ] Select a progressive delivery tool appropriate to the deployment platform (Argo Rollouts for Kubernetes, deployment slots for PaaS, CodeDeploy for VM-based services)
- [ ] Declare the release strategy for the highest-risk service first; commit as a versioned deployment config
- [ ] Define rollback triggers: metric thresholds that automatically pause or roll back a canary
- [ ] Author a release strategy ADR for each service class; link from the service registry entry
- [ ] Expand to all production services; lowest-risk internal services may use a simple rolling update declaration

### CI integration

- Release strategy config schema validation on every PR
- Rollback threshold smoke test: validate that referenced metrics exist in the observability stack

### Exit criteria

- Every production service has a declared release strategy in version control
- Rollback triggers declared and linked to observable metrics
- Release strategy ADRs in the decisions log for all service classes

---

## Pillar 28 — Environment Definitions as Code

**What it means**: The full catalog of environments — development, staging, production, feature branches, performance test — including what is deployed in each, which version, and the promotion path between them, is declared in version-controlled manifests.

### Artifact types

- Environment catalog YAML: one entry per environment declaring name, tier, purpose, and services deployed
- Promotion path declaration: from dev to staging to production, with gate criteria
- GitOps application declarations (Argo CD Application / ApplicationSet YAML, Flux HelmRelease)
- Environment-specific configuration overlays (Kustomize overlays, Helm values files per environment)

### Adoption steps

- [ ] List all environments currently in use; identify any that exist only in a deployment tool GUI without a version-controlled declaration
- [ ] Commit an environment catalog YAML; declare each environment's purpose and promotion criteria
- [ ] Adopt a GitOps tool (Argo CD, Flux) or equivalent; declare what runs in each environment as YAML committed to version control
- [ ] Use Kustomize / Helm values overlays for environment-specific configuration; never modify shared base configs per environment manually
- [ ] Declare promotion gates: which checks must pass before a release advances from one environment to the next
- [ ] Wire CI to validate environment declarations and overlay syntax on every PR

### CI integration

- Kustomize / Helm values validation on every PR
- GitOps app declaration schema validation on every PR
- Environment drift check: what is declared must match what is deployed (reconciled by the GitOps tool)

### Exit criteria

- Every environment catalogued in version-controlled declarations
- Promotion path and gates declared; no implicit "just push to prod" paths
- GitOps reconciliation active; deployment drift is detected and alerts

---

## Pillar 29 — Service Mesh Configuration as Code

**What it means**: Traffic management policies, retry budgets, circuit breaker thresholds, mutual TLS settings, and observability sidecar configurations for the service mesh are all declared in version-controlled manifest files — reviewed and deployed via CI/CD, not configured interactively in a mesh control plane.

### Artifact types

- Virtual service and destination rule declarations (Istio, Linkerd ServiceProfiles, AWS App Mesh)
- mTLS policy declarations
- Retry and circuit breaker configuration files
- Traffic routing rules (weighted routing for canary, header-based routing for A/B tests)

### Adoption steps

- [ ] Identify the service mesh in use (Istio, Linkerd, Consul Connect, AWS App Mesh, Dapr)
- [ ] Export current mesh configuration to version-controlled YAML; commit as the starting baseline
- [ ] Establish the convention: all mesh configuration changes flow through PR review — no direct `kubectl apply` or control plane GUI changes
- [ ] Author a mesh configuration ADR covering the chosen policies for retries, timeouts, and circuit breakers per service class
- [ ] Wire CI to validate mesh config YAML syntax and run a dry-apply before merge

### CI integration

- Mesh config schema validation on every PR
- Dry-apply / diff against current cluster state on every PR
- Drift check: deployed mesh config must match declared source

### Exit criteria

- All mesh configuration committed to version control
- No mesh configuration changes applied outside of PR-reviewed version-controlled declarations
- Mesh configuration ADR in the decisions log

---

<!-- THEME: People and Organization — Pillars 30–32 -->

## Pillar 30 — Team Topology as Code

**What it means**: The organizational structure of teams, their interaction modes (collaboration, X-as-a-service, facilitating), their service ownership, and their platform or enabling capabilities are declared in a version-controlled YAML registry — making the organizational architecture as legible and evolvable as the technical architecture.

### Artifact types

- Team registry YAML: name, type (stream-aligned, platform, enabling, complicated-subsystem), members, services owned, communication channels
- Interaction mode declarations: which teams interact with which other teams, in which mode
- Generated organizational topology diagram
- Service ownership index: derived from the team registry — for any service, which team owns it

### Adoption steps

- [ ] Enumerate all teams in the engineering organization; classify each by Team Topologies type
- [ ] Create a team registry YAML with entries for each team; include service ownership references to the service registry (Pillar 4)
- [ ] Declare interaction modes between teams; note where modes are aspirational vs current
- [ ] Wire a generator to produce an organizational topology diagram and a service ownership index
- [ ] Add CI validation: every service in the service registry must have an owning team in the team registry
- [ ] Review the topology quarterly; update the registry as teams change; track topology evolution in git history

### CI integration

- Team registry JSON Schema validation on every PR
- Referential integrity: every service registry entry must reference a valid team ID
- Generated topology diagram drift check

### Exit criteria

- All teams declared; every service has a declared owning team
- Organizational topology diagram generated and published in the portal
- Service ownership index generated and cross-linked from service pages

---

## Pillar 31 — Onboarding as Code

**What it means**: The process of bringing a new developer onto the team — from first repository access to shipping a first PR — is documented as executable, version-controlled steps, not as tribal knowledge passed person-to-person or as a wiki page that drifts from reality.

### Artifact types

- Onboarding checklist Markdown with explicit, testable steps and expected outputs
- Dev container definition (`devcontainer.json`) or environment setup script that runs without manual intervention
- New-joiner first-PR template: a scripted first contribution that exercises the full development workflow
- Onboarding smoke test script: runs on a clean environment to verify the guide is not broken

### Adoption steps

- [ ] Interview three recent new joiners; document every step they had to take that was not in any guide
- [ ] Author the onboarding guide as Markdown with explicit commands and expected outputs; commit to `docs/onboarding/`
- [ ] Author or adopt a dev container definition that provisions the full local development environment automatically
- [ ] Wire a new-joiner smoke test script: run it on a fresh machine; if it fails, the onboarding guide is broken — fix both
- [ ] Review and update the onboarding guide on every major platform or toolchain change

### CI integration

- `markdownlint` on onboarding documentation
- Dev container build validation: `devcontainer build` runs in CI to confirm the image still builds
- Onboarding smoke test runs on a schedule against a clean environment

### Exit criteria

- A new developer can provision their local environment by running a single command
- Onboarding guide reviewed and validated within the last 60 days
- Dev container definition passes CI build on every PR

---

## Pillar 32 — Developer Experience as Code

**What it means**: The local development toolchain — IDE settings, recommended extensions, code formatter configs, linter configs, pre-commit hooks, and local service runner scripts — is declared in version-controlled files shared across the team, so every developer works with a consistent, reproducible environment.

### Artifact types

- `.editorconfig` — universal IDE whitespace and encoding settings
- `.devcontainer/devcontainer.json` — full local dev environment as a container definition
- Formatter configs (`.prettierrc`, `pyproject.toml [tool.ruff]`, `google-java-format` settings)
- Pre-commit hook config (`.pre-commit-config.yaml`) — runs linters and formatters before every commit
- VS Code workspace settings and recommended extensions (`.vscode/settings.json`, `.vscode/extensions.json`)
- Local runner scripts (Docker Compose, Tilt, Skaffold) for spinning up all service dependencies locally

### Adoption steps

- [ ] Commit `.editorconfig` establishing universal whitespace and encoding rules
- [ ] Commit formatter configs for all languages in the codebase; wire to pre-commit hooks
- [ ] Commit `.vscode/extensions.json` with the extensions every developer should have; add `.vscode/settings.json` for shared IDE settings
- [ ] Commit a `.pre-commit-config.yaml` with at minimum: format check, lint, secret scan, trailing whitespace check
- [ ] Wire CI to run the same checks as pre-commit hooks — "works on my machine" cannot reach CI
- [ ] Document in the onboarding guide (Pillar 31): the pre-commit hooks are not optional; a PR that bypasses them will fail CI

### CI integration

- Same linters and formatters that run in pre-commit hooks also run in CI; no divergence permitted
- Dev container build validation (see Pillar 31)
- Extension recommendation drift check: `.vscode/extensions.json` kept in sync with any tool added to the workflow

### Exit criteria

- `.editorconfig`, formatter configs, and pre-commit hooks committed and documented
- CI runs the same checks as local pre-commit hooks
- Every developer uses the declared dev container or has an equivalent locally verified setup

---

<!-- THEME: Knowledge and Language — Pillars 33–35 -->

## Pillar 33 — Architecture Principles as Code

**What it means**: The standing architectural principles of the practice — the heuristics and constraints that inform every design decision below the level of a specific ADR — are declared in a version-controlled list with rationale, enforcement status, and links to the ADRs and policy rules that give them teeth.

### Artifact types

- Principles YAML: each entry declares name, statement, rationale, enforcement status (aspirational / policy-enforced / ADR-mandated), and links to governing ADRs and policy rules
- Generated principles page in the documentation portal
- Policy rules implementing machine-verifiable principles (reference Pillar 10)

### Adoption steps

- [ ] Facilitate a principles workshop: gather the 10–15 principles that the architecture practice's senior practitioners apply most often
- [ ] Declare each principle in a YAML file with: statement, rationale, and enforcement status
- [ ] For each principle with enforcement status "policy-enforced": verify a corresponding policy rule exists (or create one); link the rule from the principle entry
- [ ] For each principle with enforcement status "ADR-mandated": verify a corresponding ADR exists; link it from the principle entry
- [ ] Wire a generator to produce a principles page in the documentation portal
- [ ] Review the principles annually; add, retire, or promote principles through a PR review process

### CI integration

- Principles YAML schema validation on every PR
- Referential integrity: ADR references in principles must resolve to existing ADR files
- Policy rule references must resolve to existing rule files

### Exit criteria

- All standing architectural principles declared in version control with rationale
- Machine-enforceable principles linked to active policy rules
- Principles page generated and published in the portal

---

## Pillar 34 — Ubiquitous Language as Code

**What it means**: The domain vocabulary of the organization — bounded context terms, entity names, event names, capability names, and their precise definitions — is declared in a version-controlled glossary. Every code artifact, spec, and document uses terms from this glossary. The glossary is the single source of truth for naming.

### Artifact types

- Domain glossary YAML: each entry declares term, bounded context, definition, synonyms (for search), deprecated aliases, and links to the artifacts that use the term
- Generated searchable glossary page in the documentation portal
- Optional naming linter: checks that new code artifacts (table names, event names, API paths) use only glossary-registered terms

### Adoption steps

- [ ] Start with the 30–50 most-used domain terms; avoid attempting to define all terms at once
- [ ] For each term: declare its definition in plain language, the bounded context it belongs to, and at least one artifact that uses it
- [ ] Wire a generator to produce a searchable glossary page in the documentation portal
- [ ] Establish the convention: new API field names, event names, and table names that introduce a new domain term require a glossary PR in the same batch
- [ ] Optionally wire a naming linter: new entity or event names not found in the glossary trigger a CI warning
- [ ] Review the glossary on each significant domain expansion; terms that fall out of use are deprecated, not deleted (history matters)

### CI integration

- Glossary YAML schema validation on every PR
- Optional naming linter: new symbols in API specs and event schemas cross-checked against glossary
- Drift check: generated glossary page must match source YAML

### Exit criteria

- The top 50 domain terms declared with definitions and bounded context assignments
- Generated glossary page published and searchable in the portal
- Convention established: new domain terms added to the glossary alongside the code that introduces them

---

## Pillar 35 — Coding Standards as Code

**What it means**: The formatting, style, and quality rules that govern all source code in the practice are declared in version-controlled configuration files — not enforced inconsistently by individual reviewer preference. Linters run automatically in CI; violations block merge.

### Artifact types

- Language-specific linter configuration files (`.eslintrc`, `pyproject.toml [tool.ruff]`, `checkstyle.xml`, `golangci-lint.yaml`, `.rubocop.yml`)
- Formatter configuration files (`.prettierrc`, `google-java-format` settings, `black` config)
- `.editorconfig` (shared with Pillar 32; referenced here for completeness)
- Coding standards ADR: rationale for non-default rule choices
- Linter suppression policy: when and how `# noqa` / `@SuppressWarnings` / `// eslint-disable` are permitted

### Adoption steps

- [ ] Inventory all language stacks in the codebase; select a linter and formatter for each
- [ ] Commit the linter configuration files; wire to CI as required checks on every PR
- [ ] Commit the formatter configuration; wire a formatting check to CI (format check only — not auto-fix; auto-fix belongs in pre-commit hooks)
- [ ] Author a coding standards ADR documenting the non-default rule choices and their rationale
- [ ] Document the suppression policy: suppression annotations must include a reason comment and a tracking reference
- [ ] Enforce the suppression policy in CI (e.g., a lint rule that requires a comment on every suppression)

### CI integration

- Linter runs on every PR; failures block merge
- Formatter check (not auto-fix) runs on every PR
- Suppression annotation audit: suppression without a reason comment fails CI

### Exit criteria

- Linter and formatter configured, committed, and enforced in CI for all language stacks
- Coding standards ADR in the decisions log
- Suppression policy documented and enforced

---

## Sequencing Guide

Pillar adoption is independent but not isolated — some pillars unlock others. The table below shows recommended sequencing for a practice adopting all 35 pillars from near zero. **Teams should select only the pillars marked In Scope during the Bootstrap pillar selection exercise and sequence those pillars, not all 35.**

| Wave | Pillars | Rationale |
|------|---------|-----------|
| **Wave 1 — Foundation** | Infrastructure as Code (1), Applications as Code (4), Architecture Artifacts as Code (5), Data Models as Code (16) | Establishes the registry of what exists, canonical diagram sources, IaC baseline, and the entity schema layer. Everything else references these. |
| **Wave 2 — Governance + Language** | Decisions as Code (7), Capabilities as Code (6), Actors as Code (3), Architecture Principles as Code (33), Ubiquitous Language as Code (34) | Governance, capability model, and shared vocabulary unlock linkability and consistency in all later pillars. |
| **Wave 3 — Data** | Database Migrations as Code (17), Event Schemas as Code (19), Coding Standards as Code (35) | Schema evolution and event contracts build on the data model foundation. Coding standards establish baseline quality before validation pillars apply them. |
| **Wave 4 — Security + Compliance** | Security as Code (20), Compliance as Code (21), Secrets Management as Code (22), SBOM as Code (23) | Security and compliance pillars depend on having declared services (Wave 1) and governance (Wave 2) before they can define what to protect and what to audit. |
| **Wave 5 — Validation** | Policy as Code (10), Tests as Code (9), Pipeline as Code (2), Data Contracts as Code (18) | Validation pillars are most effective once there is a declared architecture, data model, and security baseline to validate against. |
| **Wave 6 — Reliability** | Observability as Code (24), SLO / SLI as Code (25), Feature Flags as Code (26) | Observability requires deployed services. SLOs require observability. Feature flags require a service registry to link to. |
| **Wave 7 — Delivery** | Release Strategies as Code (27), Environment Definitions as Code (28), Service Mesh Configuration as Code (29) | Progressive delivery and environment governance build on the CI/CD pipeline established in Wave 5. |
| **Wave 8 — AI + Docs + Tickets** | AI Instructions as Code (11), Documentation as Code (13), Tickets as Code (8) | AI instructions require a stable architecture definition. Docs as Code consolidates outputs from all prior waves. Ticket linkage closes the traceability loop. |
| **Wave 9 — Organization + DX** | Team Topology as Code (30), Onboarding as Code (31), Developer Experience as Code (32) | Organizational and developer experience pillars are most valuable once the technical pillars have stabilized — the toolchain they document is no longer changing rapidly. |
| **Wave 10 — Capstone** | Governance as Code (14), Wireframes as Code (12), Operational Runbooks as Code (15) | These pillars benefit from the full CI pattern library established in earlier waves and can proceed in parallel once a team has capacity. |

**Critical-path minimum**: Pillars 4 (Applications) and 5 (Architecture Artifacts) are prerequisites for almost everything. Begin there.

**Quick wins** (≤1 day, no dependencies):

- [ ] Add `markdownlint` to PR CI
- [ ] Add `actionlint` (or pipeline linter) to PR CI
- [ ] Add `mkdocs build --strict` (or equivalent) to PR CI
- [ ] Add `# yaml-language-server: $schema=...` header to any YAML that already has a schema
- [ ] Commit `.editorconfig` to every repository
- [ ] Add secret scanning to CI (truffleHog, GitHub secret scanning)
- [ ] Back-fill the single most consequential undocumented decision as an ADR

> **Synthetic exemplar carry-over**: For workspace-specific deferred items that apply only to the synthetic NovaTrek exemplar workspace, see [SYNTHETIC-EXEMPLAR-BACKLOG.md](SYNTHETIC-EXEMPLAR-BACKLOG.md).
