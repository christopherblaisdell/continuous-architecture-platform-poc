# Everything as Code — Framework (Blueprint)

> **BLUEPRINT DOCUMENT.** This is the portable framework definition. It is target-agnostic and intended for export to a corporate **EaC Adoption Instance** workspace. All examples in this document use the synthetic NovaTrek Adventures workspace as the exemplar. See the [README](README.md) for the Blueprint vs Instance distinction.

## 1. Definition

**Everything as Code (EaC)** is the practice of expressing every artifact required to design, build, run, govern, and evolve a software system as a **declarative, version-controlled, machine-readable, human-readable text file** living in source control alongside the application.

The defining properties of an EaC artifact:

| Property | Meaning |
|----------|---------|
| **Declarative** | Describes desired state, not procedural steps |
| **Text-based** | Stored as plain text (YAML, JSON, Markdown, DSL) — never binary, never WYSIWYG |
| **Version-controlled** | Lives in git with full history, blame, branch, diff, merge, review |
| **Machine-readable** | Parseable by tools, validators, generators, AI agents |
| **Human-readable** | A human can open the file in a text editor and understand it |
| **Testable** | Can be linted, validated against a schema, dry-run, and verified in CI |
| **Reviewable** | Changes flow through pull requests with diffs |
| **Reproducible** | The artifact + a generator deterministically produces the runtime/visual output |

If an artifact lacks any of these, it is **not** "as code" — it is a document, a screenshot, or a database record.

## 2. The Industry Name

The umbrella term is **Everything as Code (EaC)**. It generalizes a family of related "X as Code" disciplines:

| Discipline | Acronym | Established |
|------------|---------|-------------|
| Infrastructure as Code | IaC | Mainstream since ~2014 (Terraform, CloudFormation) |
| Configuration as Code | CaC | Mainstream since ~2010 (Puppet, Chef, Ansible) |
| Pipeline as Code | PaC | Mainstream since ~2017 (Jenkinsfile, GitHub Actions, GitLab CI) |
| Documentation as Code | Docs as Code | Mainstream since ~2015 (Write the Docs movement, MkDocs, Sphinx) |
| Diagrams as Code | DaC | Mainstream since ~2018 (PlantUML, Mermaid, Structurizr) |
| Policy as Code | PolaC | Mainstream since ~2019 (Open Policy Agent, Sentinel) |
| Architecture as Code | AaC | Emerging since ~2020 (Structurizr DSL, AaC project, ADRs) |
| Security as Code | SecaC | Emerging (TFSec, Checkov, Snyk IaC) |
| Compliance as Code | CompaC | Emerging (Conftest, Open Compliance) |
| Tests as Code | TaC | Always — but feature files (Gherkin) push this to specification level |
| AI Instructions as Code | AIaC | Brand new (~2024-2026) — platform-specific instruction files (e.g., `copilot-instructions.md`, `.clinerules`, Azure AI Foundry agent instructions), governed via a structured change workflow (e.g., OpenSpec) |
| Wireframes as Code | UIaC | Niche (Excalidraw JSON, Penpot, Mermaid) |
| Governance as Code | GaC | Emerging — change proposals, ADRs, capability changelogs |
| Patterns and Anti-patterns as Code | PaAC | Emerging — version-controlled YAML catalogs linking named patterns and anti-patterns to the decisions and services where they apply |

Adjacent and synonymous terms used in industry:

- **Software Defined Everything (SDE / SDx)** — used in networking and infrastructure circles to mean the same thing as EaC
- **Declarative-first** — used in Kubernetes / cloud-native communities
- **GitOps** — when git is the single source of truth and reconciliation is automated (Flux, Argo CD)
- **Spec-Driven Development (SDD)** — emphasizing that specifications precede implementation (AWS Kiro, OpenSpec, Spec-Kit)
- **Single Source of Truth (SSoT) architecture** — the goal that EaC enables

## 3. The Transformation Has a Name Too

Adopting EaC across an organization or practice is referred to as:

| Name | Origin / Usage |
|------|---------------|
| **Codification** | The most common generic verb — "we are codifying our architecture" |
| **EaC transformation** | Generic umbrella term |
| **Declarative transformation** | Cloud-native / Kubernetes community |
| **GitOps adoption** | When git becomes the operational source of truth |
| **AI-native transformation** | When the driver is enabling AI agents |
| **Continuous Architecture adoption** | When the practice frames it (Erder, Pureur, Woods) |
| **Codify-Validate-Generate (CVG) loop** | The operational pattern at the core of EaC |

The transformation this blueprint describes is best named:

> **AI-Native Continuous Architecture via Everything as Code**

…which reads as: a **continuous architecture practice** (the "what"), enabled by **everything as code** (the "how"), targeted at **AI-native** workflows (the "why"). This blueprint is the pattern; the corporate instance is the realization.

## 4. The Pillars

Every EaC implementation is organized around pillars — one per discipline. The full adoption guide for each pillar (artifact types, adoption steps, CI integration, exit criteria) lives in [TRANSFORMATION-PLAN.md](TRANSFORMATION-PLAN.md). This section is the reference catalog: purpose, format, and AI fit for all 35 pillars.

### Pillar 1 — Infrastructure as Code (IaC)

| | |
|---|---|
| **Purpose** | Provision and manage cloud and on-prem infrastructure declaratively |
| **Format** | HCL (Terraform), Bicep, ARM JSON, Pulumi (TS/Python/Go), CloudFormation YAML |
| **Validator** | `terraform validate`, `tflint`, `checkov`, `tfsec`, `bicep build` |
| **AI fit** | Excellent — AI agents can read, modify, and propose changes against schemas |

### Pillar 2 — Pipeline as Code (PaC)

| | |
|---|---|
| **Purpose** | Define CI/CD pipelines declaratively |
| **Format** | GitHub Actions YAML, GitLab CI YAML, Tekton, Argo Workflows, Azure DevOps YAML |
| **Validator** | `actionlint`, `gitlab-ci-lint`, `yamllint` |
| **AI fit** | Excellent |

### Pillar 3 — Actors as Code

| | |
|---|---|
| **Purpose** | Catalog every human role, system, and external entity that interacts with the system |
| **Format** | YAML with JSON Schema |
| **Generator** | Portal page generator |
| **AI fit** | Excellent — used by AI to populate diagrams, ADRs, and user stories |

### Pillar 4 — Applications as Code

| | |
|---|---|
| **Purpose** | Catalog every application, frontend, and service; the registry layer for the entire system |
| **Format** | YAML with JSON Schema |
| **Generator** | Portal page generator |
| **AI fit** | Excellent — service registry is the anchor for all other pillars |

### Pillar 5 — Architecture Artifacts as Code

| | |
|---|---|
| **Purpose** | Express system structure and runtime flows declaratively — C4 diagrams, sequence diagrams, context maps |
| **Format** | C4-PlantUML, Structurizr DSL, Mermaid, AsyncAPI, OpenAPI YAML |
| **Generator** | PlantUML, Structurizr Lite, Kroki, Mermaid CLI → SVG |
| **Validator** | DSL syntax validators; `asyncapi validate`; OpenAPI linters |
| **AI fit** | Excellent — text-based DSLs diff cleanly; AI can propose and update diagrams |

### Pillar 6 — Capabilities as Code

| | |
|---|---|
| **Purpose** | Declare the L1/L2/L3 business capability map; link tickets and ADRs to capabilities |
| **Format** | YAML with JSON Schema |
| **Generator** | Capability page generator, capability changelog generator |
| **AI fit** | Excellent — capability changelog drives AI traceability across solutions |

### Pillar 7 — Decisions as Code (ADRs)

| | |
|---|---|
| **Purpose** | Record architectural decisions in a standard, reviewable format |
| **Format** | Markdown (MADR template) |
| **Generator** | Portal page generator |
| **Validator** | MADR section validator |
| **AI fit** | Excellent — MADR has consistent sections AI can populate and parse |

### Pillar 8 — Tickets as Code

| | |
|---|---|
| **Purpose** | Express work items and requirements in version-controlled YAML; link to capabilities and services |
| **Format** | YAML with JSON Schema |
| **Generator** | Ticket page generator |
| **AI fit** | Excellent — replaces opaque ticket tracker queries; enables AI traceability |

### Pillar 9 — Tests as Code

| | |
|---|---|
| **Purpose** | Express acceptance criteria as executable specifications (BDD) and contract tests |
| **Format** | Gherkin `.feature` files (BDD), PACT / Spring Cloud Contract files |
| **Generator** | Cucumber, Behave, SpecFlow, Pact Broker |
| **AI fit** | Excellent — Gherkin is the natural-language-meets-structured format AI excels at |

### Pillar 10 — Policy as Code

| | |
|---|---|
| **Purpose** | Enforce architectural constraints, security rules, and governance policies as machine-verifiable rules |
| **Format** | OPA Rego, Conftest, Sentinel, ArchUnit |
| **Validator** | `conftest test`, `opa eval`, ArchUnit test suite |
| **AI fit** | Excellent — policy rules are themselves declarative text |

### Pillar 11 — AI Instructions as Code (AIaC)

| | |
|---|---|
| **Purpose** | Define AI agent behavior, personas, constraints, and skills declaratively, platform-agnostically |
| **Format** | Markdown + YAML frontmatter; canonical hub replicated to per-platform derived files |
| **Generator** | Hub-and-spoke replication; OpenSpec governance |
| **Validator** | Instruction file linter, hub-spoke drift check |
| **AI fit** | Mandatory — this is the AI's own behavioral contract |

See [AI-INSTRUCTIONS-AS-CODE.md](AI-INSTRUCTIONS-AS-CODE.md) for the deep dive.

### Pillar 12 — Wireframes as Code (UIaC)

| | |
|---|---|
| **Purpose** | Design and version UI screens declaratively |
| **Format** | Excalidraw `.excalidraw` JSON, Penpot, ASCII wireframes, JSX mockups |
| **Generator** | Excalidraw CLI → SVG (CI-driven) |
| **Validator** | JSON schema validation |
| **AI fit** | Good — JSON is parseable; Figma is not as-code (proprietary binary state) |

### Pillar 13 — Documentation as Code (Docs as Code)

| | |
|---|---|
| **Purpose** | Author docs in plain text, build with a static site generator, deploy via CI |
| **Format** | Markdown + MkDocs Material, Docusaurus, Sphinx |
| **Generator** | `mkdocs build`, deployed via CI to static hosting |
| **AI fit** | Excellent |

### Pillar 14 — Governance as Code

| | |
|---|---|
| **Purpose** | Declare change governance rules — capability changelogs, change proposal workflows, review gates |
| **Format** | YAML (changelogs), Markdown (change proposals), OPA/Conftest (gate rules) |
| **Generator** | Capability changelog generator, change proposal portal pages |
| **AI fit** | Excellent — AI can author and review change proposals against declared governance rules |

### Pillar 15 — Operational Runbooks as Code

| | |
|---|---|
| **Purpose** | Capture operational procedures and incident response steps as version-controlled Markdown |
| **Format** | Markdown; executable steps link to automation scripts |
| **Generator** | Runbook index generator for the documentation portal |
| **AI fit** | Good — Markdown runbooks are readable; fully executable runbooks (Ansible, Runbooks.io) are excellent |

### Pillar 16 — Data Models as Code

| | |
|---|---|
| **Purpose** | Declare entity schemas, data dictionaries, and ER relationships as version-controlled text |
| **Format** | SQL DDL, Liquibase YAML changelogs, dbt `schema.yml`, Avro/Protobuf, DBML |
| **Generator** | DbDocs, SchemaSpy, ER diagram generators |
| **Validator** | Schema lint, schemadiff |
| **AI fit** | Excellent — structured schema formats are AI-readable and diffable |

### Pillar 17 — Database Migrations as Code

| | |
|---|---|
| **Purpose** | Express every schema change as a numbered, version-controlled migration file applied deterministically |
| **Format** | Liquibase changesets, Flyway SQL, Alembic Python, golang-migrate SQL, Atlas HCL |
| **Generator** | Migration tool applies files in sequence to target database |
| **Validator** | Migration tool dry-run against a test database |
| **AI fit** | Excellent — migration files are short, structured, and diffs are precise |

### Pillar 18 — Data Contracts as Code

| | |
|---|---|
| **Purpose** | Declare producer guarantees to consumers in machine-readable contracts; enforce in CI |
| **Format** | Data Contract Specification (Bitol) YAML, OpenDataMesh, custom JSON Schema |
| **Validator** | Contract schema validator, consumer integration tests |
| **AI fit** | Excellent — structured YAML contracts are AI-parseable; AI can detect breaking changes |

### Pillar 19 — Event Schemas as Code

| | |
|---|---|
| **Purpose** | Declare every event's structure, producer, consumers, and version in a machine-readable spec |
| **Format** | AsyncAPI YAML, Avro, Protobuf, JSON Schema |
| **Generator** | Event catalog page generator |
| **Validator** | `asyncapi validate`, schema registry diff |
| **AI fit** | Excellent |

### Pillar 20 — Security as Code

| | |
|---|---|
| **Purpose** | Declare threat models, SAST configs, IAM policies, and security scan rules as version-controlled files |
| **Format** | OWASP Threat Dragon JSON, Semgrep YAML rules, Checkov/TFSec policies, IAM JSON/Bicep |
| **Validator** | SAST scan, IaC security scan (Checkov, Trivy, TFSec), dependency scan |
| **AI fit** | Excellent — policy rules and threat models are structured and diffable |

### Pillar 21 — Compliance as Code

| | |
|---|---|
| **Purpose** | Express regulatory controls as machine-verifiable rules; generate audit evidence automatically from CI |
| **Format** | OPA Rego / Conftest rules mapped to control frameworks; control mapping YAML |
| **Generator** | Audit evidence manifest generator, compliance posture report |
| **Validator** | `conftest test` with compliance ruleset |
| **AI fit** | Excellent — control mappings and evidence manifests are structured YAML |

### Pillar 22 — Secrets Management as Code

| | |
|---|---|
| **Purpose** | Declare secret access policies and rotation schedules in version-controlled IaC; enforce no plaintext secrets |
| **Format** | HashiCorp Vault policy HCL, Azure Key Vault Bicep, AWS Secrets Manager Terraform |
| **Validator** | Secret scanning (truffleHog, git-secrets), IaC policy check |
| **AI fit** | Good — policy declarations are readable; secret values must never appear in files |

### Pillar 23 — SBOM as Code

| | |
|---|---|
| **Purpose** | Generate and version a Software Bill of Materials for every deployable artifact on every build |
| **Format** | CycloneDX JSON/XML, SPDX YAML; dependency lock files committed to version control |
| **Generator** | Syft, cdxgen, `cyclonedx-npm` |
| **Validator** | Grype, Trivy, OSV-Scanner (vulnerability scan against SBOM); license compliance check |
| **AI fit** | Good — SBOM documents are structured; AI can reason over dependency trees |

### Pillar 24 — Observability as Code

| | |
|---|---|
| **Purpose** | Declare dashboards, alert rules, log queries, and synthetic monitors as version-controlled files |
| **Format** | Grafana dashboard JSON/YAML, Prometheus alerting rules YAML, Azure Monitor Bicep, Datadog Terraform |
| **Generator** | Terraform / Bicep apply; Grafana Grizzly |
| **Validator** | Alert rule syntax validation, dashboard schema validation |
| **AI fit** | Excellent — alert rules and dashboard JSON are AI-readable and generatable |

### Pillar 25 — SLO / SLI as Code

| | |
|---|---|
| **Purpose** | Declare Service Level Objectives per service; automate error budget tracking |
| **Format** | OpenSLO YAML, Sloth YAML |
| **Generator** | Sloth generates Prometheus recording rules; SLO compliance reports |
| **Validator** | OpenSLO schema validation, SLI calculation dry-run |
| **AI fit** | Excellent — OpenSLO is a structured, machine-readable standard |

### Pillar 26 — Feature Flags as Code

| | |
|---|---|
| **Purpose** | Declare feature toggle definitions, targeting rules, and rollout percentages in version-controlled YAML |
| **Format** | LaunchDarkly config YAML, Unleash YAML, OpenFeature Flagd YAML, custom YAML |
| **Validator** | Flag definition syntax validation, stale flag linter |
| **AI fit** | Excellent — flag definitions are concise structured YAML |

### Pillar 27 — Release Strategies as Code

| | |
|---|---|
| **Purpose** | Declare canary weights, blue/green rules, rollback triggers, and traffic shifting schedules |
| **Format** | Argo Rollouts YAML, Flagger Canary YAML, Istio VirtualService YAML |
| **Validator** | Config schema validation, rollback trigger metric resolution check |
| **AI fit** | Excellent — deployment strategy YAML is structured and diffable |

### Pillar 28 — Environment Definitions as Code

| | |
|---|---|
| **Purpose** | Catalog environments and declare what runs in each; define promotion paths with gate criteria |
| **Format** | Argo CD Application YAML, Flux HelmRelease YAML, Kustomize overlays, Helm values files |
| **Validator** | Kustomize / Helm values validation, GitOps app declaration schema check |
| **AI fit** | Excellent |

### Pillar 29 — Service Mesh Configuration as Code

| | |
|---|---|
| **Purpose** | Declare traffic policies, retry budgets, circuit breakers, and mTLS settings for the service mesh |
| **Format** | Istio VirtualService / DestinationRule YAML, Linkerd ServiceProfile YAML, Consul Connect HCL |
| **Validator** | Mesh config schema validation, dry-apply diff |
| **AI fit** | Excellent — mesh config YAML is structured and the impact of changes is analysable |

### Pillar 30 — Team Topology as Code

| | |
|---|---|
| **Purpose** | Declare team definitions, types, interaction modes, and service ownership in a version-controlled registry |
| **Format** | YAML (Backstage `catalog-info.yaml` compatible) |
| **Generator** | Organizational topology diagram generator, service ownership index |
| **Validator** | Referential integrity: every service must have an owning team |
| **AI fit** | Excellent — team registries are structured YAML; AI can reason over ownership and interaction patterns |

### Pillar 31 — Onboarding as Code

| | |
|---|---|
| **Purpose** | Document the new-developer onboarding process as executable, version-controlled steps |
| **Format** | Markdown with explicit commands; `devcontainer.json` for environment automation |
| **Validator** | Dev container build validation; onboarding smoke test on a schedule |
| **AI fit** | Good — Markdown onboarding guides are AI-readable; AI can assist in executing steps |

### Pillar 32 — Developer Experience as Code

| | |
|---|---|
| **Purpose** | Declare the shared local development toolchain — IDE settings, formatters, linters, pre-commit hooks |
| **Format** | `.editorconfig`, `.devcontainer/devcontainer.json`, `.pre-commit-config.yaml`, `.vscode/settings.json` |
| **Validator** | Pre-commit hooks, CI linter parity check |
| **AI fit** | Excellent — config files are structured and AI can suggest improvements |

### Pillar 33 — Architecture Principles as Code

| | |
|---|---|
| **Purpose** | Declare standing architectural principles with rationale and enforcement status |
| **Format** | YAML (principle name, statement, rationale, enforcement status, ADR links) |
| **Generator** | Principles page in the documentation portal |
| **Validator** | Principles YAML schema; referential integrity to ADR and policy files |
| **AI fit** | Excellent — principles are structured facts AI can check decisions against |

### Pillar 34 — Ubiquitous Language as Code

| | |
|---|---|
| **Purpose** | Declare domain vocabulary — terms, definitions, bounded contexts — as a version-controlled glossary |
| **Format** | YAML glossary (term, bounded context, definition, synonyms, deprecated aliases) |
| **Generator** | Searchable glossary page in the documentation portal |
| **Validator** | YAML schema; optional naming linter for API/event/entity names |
| **AI fit** | Excellent — AI can use the glossary to enforce naming consistency and generate correctly-named artifacts |

### Pillar 35 — Coding Standards as Code

| | |
|---|---|
| **Purpose** | Declare formatting, style, and quality rules for all source code as version-controlled config files |
| **Format** | `.eslintrc`, `pyproject.toml [tool.ruff]`, `checkstyle.xml`, `.rubocop.yml`, `.editorconfig` |
| **Validator** | Linter runs in CI; formatter check in CI; suppression annotation audit |
| **AI fit** | Excellent — linter configs are structured; AI can propose rule changes and auto-fix violations |

### Pillar 36 — Patterns and Anti-patterns as Code

| | |
|---|---|
| **Purpose** | Catalog approved architectural patterns and identified anti-patterns in a version-controlled, linkable registry; give AI agents and human reviewers a shared vocabulary of approved solutions and known pitfalls |
| **Format** | YAML catalog (per entry: name, type, category, problem statement, solution or remediation, consequences, ADR references, service/system links, status); optional Markdown narrative per pattern |
| **Generator** | Patterns catalog page in the documentation portal |
| **Validator** | JSON Schema; referential integrity checks to ADR files and the application/service registry |
| **AI fit** | Excellent — AI can match patterns to proposed designs, flag anti-patterns during PR review, and suggest approved alternatives |

## 5. Maturity Model — From Documents to AI-Native EaC

A practical maturity model for an architecture practice's EaC adoption:

| Level | Name | Description | Indicators |
|-------|------|-------------|------------|
| **0** | **Documents** | Word docs, slide decks, Visio, screenshots, wiki pages | No git history, no diffs, no AI accessibility |
| **1** | **Wikified** | Migrated to a wiki (Confluence, SharePoint) | Searchable, but not version-controlled or machine-parseable |
| **2** | **Docs as Code** | Markdown in git, rendered via static site | Reviewable diffs; partial AI accessibility |
| **3** | **Diagrams as Code** | Diagrams in PlantUML/Mermaid; wireframes in Excalidraw JSON; sequence diagrams CI-generated | Visual artifacts diffable; architecture diagrams version-controlled |
| **4** | **Metadata as Code** | Capabilities, actors, applications, services, data models, event schemas, and tickets in YAML with schemas | Structured data; AI can reason over it; schemas enforce shape |
| **5** | **Generators in CI** | Portal pages, diagrams, reports, and derived artifacts generated from YAML/specs by CI | Single source of truth enforced; manual edits to generated files fail CI |
| **6** | **Governance as Code** | ADRs, capability changelog, and change proposals enforced by CI | Every architectural change is reviewed and traceable |
| **7** | **AI Instructions as Code** | Hub-and-spoke AI instructions; platform-agnostic via canonical source | AI behavior itself is reviewable, diffable, and governed |
| **8** | **Policy as Code** | Architectural rules, security policies, and compliance controls enforced by OPA, ArchUnit, or custom linters in CI | Drift impossible without explicit policy bypass |
| **9** | **AI-Native EaC** | Every artifact AI-readable; AI proposes changes via PR; generators are deterministic and AI-invoking | Architecture practice operates at AI speed |

The maturity levels describe organizational milestones, not per-pillar completion gates. An organization reaches Level N when the majority of relevant pillars in that level's category are producing validated, CI-enforced artifacts. Individual pillars can sit at different levels; the overall practice maturity is the mode or median across the active pillars.

**Pillar groups by maturity level:**

| Level | Pillar groups typically active |
|-------|-------------------------------|
| 2–3 | Pillars 5 (Architecture Artifacts), 12 (Wireframes), 13 (Documentation) |
| 4 | Pillars 3, 4, 6, 8 (core metadata — actors, apps, capabilities, tickets); Pillars 16, 19 (data models, event schemas) |
| 5 | Pillars 1, 2, 7 (IaC, Pipeline, Decisions) reaching generator-in-CI state; Pillars 24, 25 (Observability, SLOs) |
| 6 | Pillars 7, 14, 36 (Decisions, Governance, Patterns and Anti-patterns) with CI-enforced change records |
| 7 | Pillar 11 (AI Instructions as Code) with hub-and-spoke governance active |
| 8 | Pillars 10, 20, 21, 22 (Policy, Security, Compliance, Secrets Management) |
| 9 | All 35 pillars active; AI-driven proposal cycle closes the CVG loop autonomously |

To assess where a real practice sits today, use the assessment template in [CURRENT-STATE-ASSESSMENT.md](CURRENT-STATE-ASSESSMENT.md).

## 6. The Codify-Validate-Generate (CVG) Loop

Every EaC pillar implements the same operational loop:

```
┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐
│  CODIFY    │ ──► │  VALIDATE  │ ──► │  GENERATE  │ ──► │  PUBLISH   │
│ (author)   │     │   (CI)     │     │   (CI)     │     │ (deploy)   │
└────────────┘     └────────────┘     └────────────┘     └────────────┘
      ▲                                                          │
      └──────────────── feedback / refinement ──────────────────┘
```

| Stage | What happens | Tool |
|-------|--------------|------|
| **Codify** | Author edits the declarative source file | any text editor or AI-assisted authoring tool (e.g., VS Code, AI agents, a structured change proposal) |
| **Validate** | Schema validation, lint, contract checks | JSON Schema, OPA, custom validators |
| **Generate** | Derived artifacts (HTML, SVG, code, docs) produced from source | static site generators, diagram renderers, and codegen scripts (e.g., MkDocs, PlantUML) |
| **Publish** | Generated outputs deployed to production targets | static hosting, documentation portals, or wiki mirrors (e.g., GitHub Pages, Azure Static Web Apps, Confluence) |

The CVG loop is the operational core of EaC. Every pillar must implement it end-to-end before that pillar can be considered "as code."

## 7. Anti-Patterns That Prevent True EaC

| Anti-pattern | Why it breaks EaC |
|--------------|-------------------|
| Diagrams in Visio / Lucidchart / Draw.io binary format | Not diffable; AI cannot read |
| Architecture in slide decks | Untestable, unversioned |
| Capabilities in a Confluence table | No schema; cannot drive generators |
| Manual portal page edits | Diverges from source of truth |
| Wiki-driven runbooks | Not testable; drift from automation |
| Figma as design source of truth | Proprietary binary state; export-only-pipeline at best |
| ADRs that exist only in pull-request descriptions | Not searchable, not linked, not surfaced |
| Tickets in JIRA without YAML mirror | AI cannot reason without API access; opaque to git |
| AI instructions edited per tool, no canonical source | Drift across Copilot, Roo, Cursor; impossible to govern |

> The table above catalogs EaC adoption anti-patterns — the organizational and tooling failures that prevent true "as code" status. For a version-controlled catalog of domain-level architectural patterns and anti-patterns in your system design (Saga, CQRS, Shared Database, Distributed Monolith, etc.), see **Pillar 36 — Patterns and Anti-patterns as Code**.

## 8. Key References

This section will be populated by the deep research response. See [DEEP-RESEARCH-PROMPT-EAC-MATURITY-MODEL.md](DEEP-RESEARCH-PROMPT-EAC-MATURITY-MODEL.md).

Initial seed references:

- ThoughtWorks Technology Radar — multiple "X as Code" entries
- HashiCorp's "Infrastructure as Code" methodology
- The Open Group ArchiMate specification
- Architecture as Code (AaC) project — https://github.com/DevOps-MBSE/AaC
- Structurizr DSL — https://structurizr.com/dsl
- Likec4 — https://likec4.dev/
- IcePanel — https://icepanel.io/
- Diátaxis documentation framework — https://diataxis.fr/
- MADR ADR template — https://adr.github.io/madr/
- OpenSpec — https://github.com/Fission-AI/OpenSpec
- AWS Kiro (spec-driven development) — https://kiro.dev/
- The arc42 template — https://arc42.org/
- C4 Model — https://c4model.com/
- Continuous Architecture in Practice (Erder, Pureur, Woods) — Addison-Wesley, 2021
- Standardized taxonomy of AI instructions and OpenSpec governance model (workspace deep research) — [standardized.taxonomy.of.ai.instructions.etc.deep.research.response.md](standardized.taxonomy.of.ai.instructions.etc.deep.research.response.md)
