# Transformation Plan — Everything as Code

This is a phased plan to bring this workspace from its current state (Level 6, with Level 7 in flight) to **Level 9 — AI-Native EaC**. Each phase has concrete tasks, exit criteria, and dependencies.

The plan is designed to be executed incrementally — each phase delivers value independently and does not require the next phase to begin.

## Guiding Principles

1. **No artifact left behind** — every deliverable in the architecture practice has an as-code home
2. **Schema before automation** — every YAML gets a JSON Schema before generators consume it
3. **CI enforces the loop** — Codify → Validate → Generate → Publish runs on every PR
4. **Drift is a build failure** — generated artifacts that diverge from source fail CI
5. **AI is a first-class author** — every artifact must be readable and editable by an AI agent
6. **Platform-agnostic** — derived artifacts can be regenerated for any target tool from canonical sources

---

## Phase 0 — Establish the EaC Charter (1 sprint)

**Goal**: Make EaC an explicit organizational commitment.

### Tasks

- [ ] Review and ratify [EVERYTHING-AS-CODE-FRAMEWORK.md](EVERYTHING-AS-CODE-FRAMEWORK.md) with stakeholders
- [ ] Author **ADR-015 — Adopt Everything as Code as the Architecture Practice Standard** in `decisions/`
- [ ] Add an EaC compliance section to `.github/copilot-instructions.md` referencing this folder
- [ ] Create a `policies/` folder placeholder with a README pointing to Pillar 13 plan
- [ ] Update `roadmap/ROADMAP.md` to add an "Everything as Code Transformation" track

### Exit criteria

- ADR-015 merged
- Roadmap reflects EaC as a top-level track

---

## Phase 1 — Schema-ify All Architecture Metadata (1-2 sprints)

**Goal**: Every YAML under `architecture/metadata/` validates against a JSON Schema in CI.

### Tasks

- [ ] Create `architecture/schemas/` folder
- [ ] Author JSON Schema for each file:
  - [ ] `actors.schema.json`
  - [ ] `applications.schema.json`
  - [ ] `app-titles.schema.json`
  - [ ] `capabilities.schema.json`
  - [ ] `capability-changelog.schema.json`
  - [ ] `consumers.schema.json`
  - [ ] `cross-service-calls.schema.json`
  - [ ] `data-stores.schema.json`
  - [ ] `delivery-status.schema.json`
  - [ ] `domains.schema.json`
  - [ ] `events.schema.json`
  - [ ] `label-to-svc.schema.json`
  - [ ] `pci.schema.json`
  - [ ] `pipeline-registry.schema.json`
  - [ ] `tickets.schema.json`
- [ ] Add `# yaml-language-server: $schema=...` headers to each YAML for VS Code intellisense
- [ ] Add a CI workflow `validate-architecture-metadata.yml` that runs `ajv-cli` (or `python jsonschema`) against every YAML
- [ ] Write a contributor guide: `architecture/schemas/README.md`

### Exit criteria

- Every metadata YAML has a schema and passes validation in CI
- VS Code surfaces autocomplete and validation errors as you type

### Why this is highest priority

JSON Schemas turn YAML into a typed contract. AI agents stop hallucinating fields, generators stop crashing on bad input, PRs catch errors before merge. Every other phase becomes easier once schemas exist.

---

## Phase 2 — Validate Specs and Diagrams in CI (1 sprint)

**Goal**: OpenAPI, AsyncAPI, PlantUML, CALM all validate on every PR.

### Tasks

- [ ] Add `openapi-spec-validator` (or Spectral) to a CI workflow validating all `architecture/specs/*.yaml`
- [ ] Add AsyncAPI validator to a CI workflow validating `architecture/events/*.yaml`
- [ ] Add `plantuml -checkonly` to a CI workflow validating all `*.puml` files
- [ ] Add CALM validator (if available) to validate `architecture/calm/*.json`
- [ ] Configure Spectral rulesets to enforce internal naming conventions (kebab-case paths, schema descriptions required, etc.)

### Exit criteria

- Every spec/diagram type validates on every PR
- Spectral ruleset documented in `architecture/specs/.spectral.yaml`

---

## Phase 3 — Drift Detection (1 sprint)

**Goal**: Generated artifacts cannot silently diverge from their source.

### Tasks

- [ ] Add a CI step that runs `bash portal/scripts/generate-all.sh` then runs `git diff --exit-code` against the working tree
- [ ] Add the same pattern for the wireframe SVG generator
- [ ] Add the same pattern for the Confluence staging directory (`portal/scripts/confluence-prepare.py` then `git diff --exit-code portal/confluence/`)
- [ ] Document the drift-check pattern in a new `docs/everything-as-code/DRIFT-DETECTION.md`

### Exit criteria

- A PR that hand-edits a generated portal page fails CI
- A PR that changes source YAML without regenerating fails CI

---

## Phase 4 — Unified C4 Model (2 sprints)

**Goal**: A single declarative model defines every container and component, replacing scattered PUML.

### Tasks

- [ ] Spike: evaluate Structurizr DSL vs Likec4 vs IcePanel-as-code for the unified model
- [ ] Author ADR-016 selecting the DSL
- [ ] Migrate existing C4-style diagrams under `architecture/diagrams/` to the chosen DSL
- [ ] Wire CI to generate diagram SVGs from the DSL on every change
- [ ] Keep service-internal sequence diagrams as PUML (still generated from OpenAPI specs)
- [ ] Update generator to deep-link from C4 component diagrams to per-service pages

### Exit criteria

- A single source-of-truth file (or directory) describes the entire NovaTrek system at C4 levels 1-3
- All C4 diagrams in the portal are generated from this source

---

## Phase 5 — Activate AI Instructions Governance (1 sprint)

**Goal**: Complete OpenSpec governance loop; AI instructions are fully as-code with active validation.

### Tasks (resumes from prior session work)

- [ ] Fix two issues in `scripts/validate-ai-instructions.sh`:
  - Remove `prompt-mirror/README.md` from required files list
  - Update or remove the global symlink check (`~/.config/roo/ai-customizations`)
- [ ] Remove the DEFERRED block from the script
- [ ] Run script; fix any remaining failures
- [ ] Add the script to a `validate-ai-instructions.yml` GitHub Actions workflow
- [ ] Run the first real OpenSpec change cycle (`/opsx:propose → /opsx:apply → /opsx:archive`) with a test rule
- [ ] Document the workflow in [AI-INSTRUCTIONS-AS-CODE.md](AI-INSTRUCTIONS-AS-CODE.md)
- [ ] Evaluate adding Cursor `.mdc` and Windsurf `.windsurfrules` as derived targets

### Exit criteria

- Validation script active and CI-enforced
- At least one OpenSpec change cycle completed end-to-end
- Hub-and-spoke architecture documented

---

## Phase 6 — MADR Validator and ADR Linkability (1 sprint)

**Goal**: ADRs cannot merge if they are missing required sections; ADRs are linked into capability/solution context automatically.

### Tasks

- [ ] Author `scripts/validate-madr.py` that asserts required MADR sections exist (Status, Date, Context, Decision Drivers, Considered Options, Decision Outcome, Consequences with positive/negative/neutral)
- [ ] Add to CI on changes to `decisions/**` and `**/d.decisions/**`
- [ ] Add a generator that produces `decisions/INDEX.md` from frontmatter (or first headings) of each ADR
- [ ] Link ADRs from capability pages and solution master documents automatically via the changelog

### Exit criteria

- ADRs missing sections fail CI
- ADR index page generated and linked

---

## Phase 7 — Solution Design Folder Schema (1 sprint)

**Goal**: Every `architecture/solutions/_NTK-*/` folder structure is enforced by a schema.

### Tasks

- [ ] Define the canonical solution folder layout in YAML or as a simple JSON Schema for required paths/files
- [ ] Author `scripts/validate-solution-folders.py`
- [ ] Add to CI on changes to `architecture/solutions/**`
- [ ] Generate a "Solution Design Quickstart" template generator: `scripts/scaffold-solution.sh NTK-XXXXX-slug`

### Exit criteria

- A new solution folder must include all required subdirectories or fails CI
- Scaffolding script in place

---

## Phase 8 — Tests as Code Maturity (2 sprints)

**Goal**: BDD feature files are executable, not just documentation.

### Tasks

- [ ] Audit `tests/` for existing `.feature` files
- [ ] Wire a runner (Behave for Python, or pytest-bdd) for the synthetic NovaTrek workspace
- [ ] Generate a coverage report: which capabilities have BDD coverage vs not
- [ ] Add CI step that runs feature files (where executable) and emits the coverage report

### Exit criteria

- BDD feature files run in CI
- Capability-to-feature coverage report published in the portal

---

## Phase 9 — Policy as Code (2 sprints)

**Goal**: Architectural rules enforced by machine, not by reviewer vigilance.

### Tasks

- [ ] Create `policies/` folder with a `README.md` and `.rego` files
- [ ] Author rules using OPA/Conftest:
  - Every entry in `services/` MUST have a matching entry in `architecture/specs/`
  - Every capability referenced in `tickets.yaml` MUST exist in `capabilities.yaml`
  - Every service in `cross-service-calls.yaml` MUST exist in the OpenAPI specs catalog
  - Every solution folder MUST link to at least one capability via the changelog
  - Every ADR referenced in `capability-changelog.yaml` MUST exist
- [ ] Add `conftest test` to a CI workflow
- [ ] Document the rule catalog and how to add new rules

### Exit criteria

- At least 5 policy rules enforced in CI
- Rule catalog published in the portal

---

## Phase 10 — Operational Runbooks as Code (1 sprint)

**Goal**: Operational procedures are executable scripts or declarative workflows, not wiki pages.

### Tasks

- [ ] Audit existing operational documentation (deployment guides, troubleshooting steps)
- [ ] Convert each into either a script under `scripts/` or a Markdown runbook with explicit commands and expected outputs
- [ ] Link runbooks from the portal under `portal/docs/operations/`
- [ ] For automation candidates, convert to GitHub Actions or Tekton tasks

### Exit criteria

- No operational procedure exists only in a wiki or PDF
- All runbooks pass a markdownlint + spell check in CI

---

## Phase 11 — Vendor-Agnostic Layer (2 sprints)

**Goal**: Reduce coupling to specific vendor formats; make every artifact portable.

### Tasks

- [ ] Document tool-specific dependencies for each pillar in [EVERYTHING-AS-CODE-FRAMEWORK.md](EVERYTHING-AS-CODE-FRAMEWORK.md)
- [ ] For AI instructions: complete OpenSpec hub-and-spoke for all 5 supported tools (Copilot, Roo, Cursor, Windsurf, Continue.dev)
- [ ] For diagrams: ensure every diagram source is in an open DSL (PlantUML, Mermaid, Structurizr DSL) — no proprietary formats
- [ ] For wireframes: confirm Excalidraw remains the standard (open JSON spec, fully diffable)
- [ ] For metadata: confirm YAML + JSON Schema (open standards) — never tool-specific imports
- [ ] Author a "Portability Manifest" listing the canonical format and acceptable derived formats per pillar

### Exit criteria

- Portability Manifest published
- Every derived format generated from canonical via CI

---

## Phase 12 — AI-Native PR Workflow (3 sprints)

**Goal**: AI agents propose changes via PR using the OpenSpec workflow, with full validation gates.

### Tasks

- [ ] Configure Copilot Coding Agent (or equivalent) to operate from `.github/copilot-instructions.md`
- [ ] Configure GitHub Issues to seed AI proposals via the `/opsx:propose` command
- [ ] Wire CI to run all schema validators, drift checks, and policy rules on AI-authored PRs
- [ ] Establish a human review gate for any change touching `decisions/`, `architecture/schemas/`, or `policies/`
- [ ] Pilot with one capability area (e.g., `svc-check-in` enhancements)
- [ ] Capture lessons learned and refine

### Exit criteria

- At least 5 AI-authored PRs merged through the full validated workflow
- Lessons-learned document published

---

## Phase 13 — Maturity Audit and Continuous Improvement (recurring)

**Goal**: Re-assess EaC maturity quarterly.

### Tasks

- [ ] Author `scripts/eac-maturity-audit.py` that scores each pillar against the criteria
- [ ] Run quarterly; publish results in `docs/everything-as-code/audits/YYYY-QQ.md`
- [ ] Use audit gaps to seed the next quarter's roadmap

### Exit criteria

- First audit published
- Audit cadence in the team calendar

---

## Critical Path Summary

```
Phase 0 (Charter) ──► Phase 1 (Schemas) ──► Phase 2 (Validate Specs) ──► Phase 3 (Drift)
                                                                            │
                  ┌─────────────────────────────────────────────────────────┘
                  │
                  ▼
              Phase 5 (AI Instructions Governance) ──► Phase 12 (AI-Native PRs)
                  │
                  ├─► Phase 4 (Unified C4)
                  ├─► Phase 6 (MADR Validator)
                  ├─► Phase 7 (Solution Schema)
                  ├─► Phase 8 (Tests as Code)
                  └─► Phase 9 (Policy as Code)
                                  │
                                  ▼
                              Phase 11 (Vendor-Agnostic)
                                  │
                                  ▼
                              Phase 13 (Maturity Audit)
```

Phases 1, 2, 3, and 5 are the **critical path** — every other phase is enabled by them.

## Quick-Win Backlog (≤1 day each)

These items can be done immediately without waiting for any phase:

- [ ] Add `# yaml-language-server: $schema=...` headers to YAML files (once schemas exist)
- [ ] Add `actionlint` to PR CI
- [ ] Add `markdownlint` to PR CI
- [ ] Add `mkdocs build --strict` to PR CI (catches broken internal links)
- [ ] Author the missing JSON Schema for `capability-changelog.yaml` (highest leverage, single file)
- [ ] Move the AI instructions validation script issues into specific GitHub issues for Phase 5
