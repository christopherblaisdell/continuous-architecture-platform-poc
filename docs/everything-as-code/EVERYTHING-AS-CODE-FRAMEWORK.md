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
| AI Instructions as Code | AIaC | Brand new (~2024-2026) — `copilot-instructions.md`, OpenSpec, `.clinerules` |
| Wireframes as Code | UIaC | Niche (Excalidraw JSON, Penpot, Mermaid) |
| Governance as Code | GaC | Emerging — change proposals, ADRs, capability changelogs |

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

Every EaC implementation can be mapped to a pillar. Below are the pillars relevant to a modern architecture practice (numbering matches the user's request, extended to cover everything in this workspace).

### Pillar 1 — Infrastructure as Code (IaC)

| | |
|---|---|
| **Purpose** | Provision and manage cloud and on-prem infrastructure declaratively |
| **Format** | HCL (Terraform), Bicep, ARM JSON, Pulumi (TS/Python/Go), CloudFormation YAML |
| **Source of truth** | `infra/` |
| **Generator** | `terraform apply`, `az deployment`, `pulumi up` |
| **Validator** | `terraform validate`, `tflint`, `checkov`, `tfsec`, `bicep build` |
| **AI fit** | Excellent — AI agents can read, modify, and propose changes against schemas |

### Pillar 2 — Pipeline as Code (PaC)

| | |
|---|---|
| **Purpose** | Define CI/CD pipelines declaratively |
| **Format** | GitHub Actions YAML, GitLab CI YAML, Tekton, Argo Workflows, Azure DevOps YAML |
| **Source of truth** | `.github/workflows/`, `.gitlab-ci.yml` |
| **Generator** | The CI platform |
| **Validator** | `actionlint`, `gitlab-ci-lint`, `yamllint` |
| **AI fit** | Excellent |

### Pillar 3 — Architecture as Code — Sequence Diagrams

| | |
|---|---|
| **Purpose** | Express runtime interaction flows declaratively |
| **Format** | PlantUML `.puml`, Mermaid `sequenceDiagram` |
| **Source of truth** | `portal/docs/microservices/puml/`, `architecture/diagrams/` |
| **Generator** | PlantUML jar, Kroki, Mermaid CLI → SVG |
| **Validator** | `plantuml -checkonly`, syntax linters |
| **AI fit** | Excellent — text-based, easy to diff, generated by `generate-microservice-pages.py` |

### Pillar 4 — Architecture as Code — C4 Component Diagrams

| | |
|---|---|
| **Purpose** | Express system structure at C4 levels (Context, Container, Component, Code) |
| **Format** | C4-PlantUML includes, Structurizr DSL, IcePanel YAML, Likec4 DSL |
| **Source of truth** | `architecture/diagrams/c4/` |
| **Generator** | PlantUML, Structurizr Lite, Likec4 |
| **Validator** | DSL parser, structure validator |
| **AI fit** | Excellent (textual DSL); poor when teams use Visio/Lucidchart |

### Pillar 5 — UI Wireframes as Code

| | |
|---|---|
| **Purpose** | Design and version UI screens declaratively |
| **Format** | Excalidraw `.excalidraw` JSON, Mermaid flowchart, Penpot, ASCII wireframes, JSX/HTML mockups |
| **Source of truth** | `architecture/wireframes/{app}/` |
| **Generator** | Excalidraw CLI → SVG (CI-driven) |
| **Validator** | JSON schema validation |
| **AI fit** | Good — JSON is parseable. Figma is **not** as-code (proprietary binary state) |

### Pillar 6 — Actors as Code

| | |
|---|---|
| **Purpose** | Catalog every human role, system, and external entity that interacts with the system |
| **Format** | YAML |
| **Source of truth** | `architecture/metadata/actors.yaml` |
| **Generator** | Portal page generator → `portal/docs/actors/` |
| **Validator** | JSON Schema for actors.yaml |
| **AI fit** | Excellent — used by AI to populate diagrams, ADRs, user stories |

### Pillar 7 — Applications as Code

| | |
|---|---|
| **Purpose** | Catalog every application, frontend, and consumer of the platform |
| **Format** | YAML |
| **Source of truth** | `architecture/metadata/applications.yaml` |
| **Generator** | Portal page generator → `portal/docs/applications/` |
| **Validator** | JSON Schema |
| **AI fit** | Excellent |

### Pillar 8 — Capabilities as Code

| | |
|---|---|
| **Purpose** | Express the L1/L2/L3 business capability map declaratively, link tickets and ADRs to capabilities |
| **Format** | YAML |
| **Source of truth** | `architecture/metadata/capabilities.yaml`, `architecture/metadata/capability-changelog.yaml` |
| **Generator** | `portal/scripts/generate-capability-pages.py` |
| **Validator** | JSON Schema, capability-changelog validator |
| **AI fit** | Excellent — capability changelog drives AI traceability across solutions |

### Pillar 9 — Everything Else Under `architecture/`

The user's pillar 9 is the catch-all: every file under `architecture/` must be as-code. Mapping the existing structure:

| Folder | Today | Status | Action |
|--------|-------|--------|--------|
| `architecture/specs/` | OpenAPI YAML | As code | Keep, add JSON Schema validation in CI |
| `architecture/events/` | AsyncAPI YAML | As code | Keep, add CI validation |
| `architecture/metadata/` | YAML files | As code | Add JSON Schema for each (capabilities, actors, applications, events, datastores, cross-service-calls, tickets, capability-changelog) |
| `architecture/wireframes/` | Excalidraw JSON | As code | Keep, ensure CI generation |
| `architecture/diagrams/` | PlantUML | As code | Keep, ensure all renders are CI-generated |
| `architecture/calm/` | CALM JSON | As code | Keep |
| `architecture/solutions/_NTK-*/` | Markdown solution designs | As code (Markdown) | Add structural schema for each subfolder |
| `architecture/reminders/` | Markdown | As code | Keep |

### Pillar 10 — Decisions as Code (ADRs)

| | |
|---|---|
| **Purpose** | Record architectural decisions in MADR format |
| **Format** | Markdown (MADR template) |
| **Source of truth** | `decisions/`, plus per-solution `3.solution/d.decisions/decisions.md` |
| **Generator** | Portal page generator |
| **Validator** | MADR section validator (custom script) |
| **AI fit** | Excellent — MADR has consistent sections AI can populate and parse |

### Pillar 11 — Tickets / Work Items as Code

| | |
|---|---|
| **Purpose** | Express work items, requirements, and traceability to capabilities and services as code |
| **Format** | YAML |
| **Source of truth** | `architecture/metadata/tickets.yaml` |
| **Generator** | `portal/scripts/generate-ticket-pages.py` |
| **AI fit** | Excellent — replaces opaque JIRA queries |

### Pillar 12 — Tests as Code (BDD Feature Files)

| | |
|---|---|
| **Purpose** | Express acceptance criteria as executable specifications |
| **Format** | Gherkin `.feature` files |
| **Source of truth** | `tests/` |
| **Generator** | Cucumber, Behave, SpecFlow |
| **AI fit** | Excellent — Gherkin is the natural-language-meets-structured format AI excels at |

### Pillar 13 — Policy / Governance as Code

| | |
|---|---|
| **Purpose** | Express organizational policies, security policies, and architectural constraints as enforceable rules |
| **Format** | OPA Rego, Conftest, Sentinel, ArchUnit |
| **Source of truth** | `policies/` (does not yet exist in this workspace) |
| **AI fit** | Excellent |

### Pillar 14 — AI Instructions as Code

| | |
|---|---|
| **Purpose** | Define AI agent behavior, personas, constraints, and skills declaratively, in a platform-agnostic way |
| **Format** | Markdown + YAML frontmatter; canonical source via OpenSpec; derived files per platform (`copilot-instructions.md`, `.clinerules`, `.cursor/rules/*.mdc`, `.windsurf/rules/`) |
| **Source of truth** | `sites/ai-evaluation-2/docs/open-spec/.ai-instructions/` (canonical hub) |
| **Generator** | Hub-and-spoke replication; OpenSpec governance |
| **Validator** | `scripts/validate-ai-instructions.sh` |
| **AI fit** | Mandatory — this is the AI's own behavioral contract |

See [AI-INSTRUCTIONS-AS-CODE.md](AI-INSTRUCTIONS-AS-CODE.md) for the deep dive.

### Pillar 15 — Documentation as Code (Docs as Code)

| | |
|---|---|
| **Purpose** | Author docs in plain text, build with a static site generator, deploy via CI |
| **Format** | Markdown + MkDocs Material |
| **Source of truth** | `portal/docs/` |
| **Generator** | `mkdocs build`, deployed to Azure Static Web Apps and Confluence (read-only mirror) |
| **AI fit** | Excellent |

## 5. Maturity Model — From Documents to AI-Native EaC

A practical maturity model for an architecture practice's EaC adoption:

| Level | Name | Description | Indicators |
|-------|------|-------------|------------|
| **0** | **Documents** | Word docs, slide decks, Visio, screenshots, wiki pages | No git history, no diffs, no AI accessibility |
| **1** | **Wikified** | Migrated to a wiki (Confluence, SharePoint) | Searchable, but not version-controlled or machine-parseable |
| **2** | **Docs as Code** | Markdown in git, rendered via static site | Reviewable diffs; partial AI accessibility |
| **3** | **Diagrams as Code** | Diagrams in PlantUML/Mermaid; wireframes in Excalidraw JSON | Visual artifacts now diffable |
| **4** | **Metadata as Code** | Capabilities, actors, applications, services in YAML with schemas | Structured data; AI can reason over it |
| **5** | **Generators in CI** | Portal pages, diagrams, and reports generated from YAML/specs by CI | Single source of truth enforced |
| **6** | **Governance as Code** | Change proposals (OpenSpec), ADRs, capability changelog enforced by CI | Every change reviewed and traceable |
| **7** | **AI Instructions as Code** | Hub-and-spoke AI instructions; platform-agnostic via OpenSpec | AI behavior itself is reviewable |
| **8** | **Policy as Code** | Architectural rules enforced by OPA, ArchUnit, custom linters in CI | Drift impossible without policy bypass |
| **9** | **AI-Native EaC** | Every artifact AI-readable; AI proposes changes via PR; generators are deterministic | Architecture practice operates at AI speed |

The synthetic exemplar workspace where this blueprint is being authored sits at approximately **Level 6**, with strong elements of Level 7 in flight — that score validates the model but is not a corporate fact. The actual maturity of any real practice MUST be re-assessed inside the corporate instance workspace using the assessment template.

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
| **Codify** | Author edits the declarative source file | VS Code, AI agent, OpenSpec proposal |
| **Validate** | Schema validation, lint, contract checks | JSON Schema, OPA, custom validators |
| **Generate** | Derived artifacts (HTML, SVG, code, docs) produced from source | MkDocs, PlantUML, codegen scripts |
| **Publish** | Generated outputs deployed to production targets | Azure Static Web Apps, Confluence mirror |

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
