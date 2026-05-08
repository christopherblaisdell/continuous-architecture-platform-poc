# Synthetic Exemplar Assessment — Everything as Code

> **BLUEPRINT — SYNTHETIC EXEMPLAR.** This document is **not** a corporate current-state assessment. It is a worked example demonstrating *how* the assessment template is applied, using the synthetic NovaTrek Adventures workspace as the subject. All scores, file counts, and gaps below describe the fictional workspace. When the blueprint is exported to a corporate **EaC Adoption Instance**, this document is replaced — pillar by pillar — with the real assessment of the actual practice. The structure, pillar list, scoring rubric, and gap-table format are the durable parts; the findings are not.

This document assesses where the synthetic exemplar workspace stands on the EaC maturity model, pillar by pillar. It is the worked example that informs [Transformation Plan](TRANSFORMATION-PLAN.md).

## Summary

| | |
|---|---|
| **Overall maturity level** | **Level 6 — Governance as Code** (with elements of Level 7 in flight) |
| **Strongest pillars** | Architecture metadata, OpenAPI specs, sequence diagrams, docs portal, ADRs |
| **Weakest pillars** | Policy as Code, AI Instructions as Code (governance still being activated), schema validation in CI |
| **Most impactful next step** | Activate JSON Schema validation for every YAML in `architecture/metadata/` |

## Pillar-by-Pillar Assessment

> This assessment uses the canonical 35-pillar numbering from [EVERYTHING-AS-CODE-FRAMEWORK.md](EVERYTHING-AS-CODE-FRAMEWORK.md). Pillars not represented in this synthetic exemplar workspace are marked NOT IN SCOPE — a full Instance assessment covers all 35 pillars.

### Pillar 1 — Infrastructure as Code

| | |
|---|---|
| **Status** | LIVE |
| **Files** | `infra/ai-poc.bicep`, `infra/bicepconfig.json` |
| **Generator** | `az deployment group create` / `azd up` |
| **Validator** | `bicep build` (manual; not yet in CI for every PR) |
| **Gap** | Add Bicep lint + `checkov` / `psrule` to CI on every PR touching `infra/` |
| **Maturity** | Level 5 (generators in CI partially) |

### Pillar 2 — Pipeline as Code

| | |
|---|---|
| **Status** | LIVE |
| **Files** | `.github/workflows/*.yml`; `architecture/metadata/pipeline-registry.yaml` (inventory, no schema) |
| **Generator** | GitHub Actions |
| **Validator** | None automated; relies on PR runs |
| **Gap** | Add `actionlint` to a PR-level workflow; add JSON Schema for `pipeline-registry.yaml` |
| **Maturity** | Level 5 |

### Pillar 3 — Actors as Code

| | |
|---|---|
| **Status** | LIVE |
| **File** | `architecture/metadata/actors.yaml` |
| **Generator** | Portal page generator |
| **Validator** | NONE — no JSON Schema |
| **Gap** | Author `architecture/schemas/actors.schema.json`; validate in CI |
| **Maturity** | Level 4 |

### Pillar 4 — Applications as Code

| | |
|---|---|
| **Status** | LIVE |
| **Files** | `architecture/metadata/applications.yaml`, `app-titles.yaml`, `consumers.yaml` |
| **Validator** | NONE |
| **Gap** | JSON Schema; consolidate `app-titles.yaml` into `applications.yaml` if titles are derivable |
| **Maturity** | Level 4 |

### Pillar 5 — Architecture Artifacts as Code

Covers C4 diagrams, sequence diagrams, OpenAPI specs, cross-service call maps, domain definitions, CALM topology, and solution design architecture artifacts.

| | |
|---|---|
| **Status** | PARTIAL — strong on sequence diagrams; weak on unified C4 model |
| **Files** | `portal/docs/microservices/puml/*.puml` (sequence), `architecture/diagrams/` (C4 PUML), `architecture/specs/*.yaml` (OpenAPI), `architecture/metadata/cross-service-calls.yaml`, `architecture/metadata/domains.yaml`, `architecture/metadata/label-to-svc.yaml`, `architecture/calm/*.json`, `architecture/solutions/_NTK-*/` (solution designs) |
| **Generator** | `portal/scripts/generate-microservice-pages.py` produces 139 sequence diagrams from OpenAPI specs |
| **Validator** | PlantUML `-checkonly` on demand; no OpenAPI lint in CI; no CALM validator in CI |
| **Gap (sequence)** | Add CI drift check: fail if generated PUML differs from committed PUML |
| **Gap (C4)** | No central C4 DSL — diagrams are per-service PUML, not a unified model; evaluate Structurizr DSL or Likec4 |
| **Gap (OpenAPI)** | `openapi-spec-validator` not in CI on every PR |
| **Gap (CALM)** | CALM validator not in CI |
| **Maturity** | Level 6 for sequence diagrams; Level 4 for C4; Level 4 for OpenAPI; Level 3 for CALM |

### Pillar 6 — Capabilities as Code

| | |
|---|---|
| **Status** | LIVE — strongest pillar |
| **Files** | `architecture/metadata/capabilities.yaml`, `capability-changelog.yaml` |
| **Generator** | `portal/scripts/generate-capability-pages.py` |
| **Validator** | Capability changelog validator (in `portal/scripts/utilities/`) |
| **Gap** | Formalize JSON Schema for both files; document the L1/L2/L3 model in this folder |
| **Maturity** | Level 6 |

### Pillar 7 — Decisions as Code (ADRs)

| | |
|---|---|
| **Status** | LIVE |
| **Files** | `decisions/ADR-001` through `ADR-014`; per-solution ADRs in `architecture/solutions/_NTK-*/3.solution/d.decisions/` |
| **Validator** | NONE — no MADR section validator |
| **Gap** | Custom validator asserting MADR sections (Status, Date, Context, Decision Drivers, Considered Options, Decision Outcome, Consequences) are present |
| **Maturity** | Level 4 |

### Pillar 9 — Tests as Code

| | |
|---|---|
| **Status** | PARTIAL |
| **Files** | `tests/`, plus `docs/BDD-AUTHORING-GUIDE.md` |
| **Validator** | Test runner of choice |
| **Gap** | Most "tests" today are documentation; BDD feature files need to be wired to executable runners for the synthetic NovaTrek services |
| **Maturity** | Level 3 |

### Pillar 10 — Policy as Code

| | |
|---|---|
| **Status** | NOT STARTED |
| **Gap** | No `policies/` folder; no OPA, no Conftest, no ArchUnit equivalents for architectural rules |
| **Recommendation** | Start with Conftest + Rego rules: "every service MUST have an OpenAPI spec", "every YAML in `architecture/metadata/` MUST validate against its schema" |
| **Maturity** | Level 0 |

### Pillar 11 — AI Instructions as Code (AIaC)

| | |
|---|---|
| **Status** | IN FLIGHT — hub-and-spoke active, OpenSpec governance phases 1–3 verified, Phase 5 (validation script) deferred |
| **Files** | `sites/ai-evaluation-2/docs/open-spec/.ai-instructions/` (canonical); 5 derived files (`.clinerules`, `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`) |
| **Validator** | `scripts/validate-ai-instructions.sh` (DEFERRED) |
| **Gap** | Activate validation script; complete OpenSpec Phase 10 (first real propose→apply→archive cycle); evaluate Cursor and Windsurf as additional derived targets |
| **Maturity** | Level 6; pushing toward Level 7 |

### Pillar 12 — Wireframes as Code (UIaC)

| | |
|---|---|
| **Status** | LIVE |
| **Files** | `architecture/wireframes/{web-guest-portal,web-ops-dashboard,app-guest-mobile}/*.excalidraw` |
| **Generator** | CI converts `.excalidraw` JSON → SVG + HTML + MD wrapper to `portal/docs/applications/{app}/wireframes/` |
| **Validator** | JSON parse only |
| **Gap** | No JSON Schema for Excalidraw files; CI generation not validated against a wireframe inventory |
| **Maturity** | Level 5 |

### Pillar 13 — Documentation as Code (Docs as Code)

| | |
|---|---|
| **Status** | LIVE — strong |
| **Files** | `portal/docs/`, `mkdocs.yml`, `sites/manifest.yaml` |
| **Generator** | MkDocs Material → Azure Static Web Apps + Confluence read-only mirror |
| **Validator** | `mkdocs build --strict`, link checker, Confluence drift check |
| **Maturity** | Level 7 |

### Pillar 14 — Governance as Code

| | |
|---|---|
| **Status** | LIVE |
| **Files** | `architecture/metadata/capability-changelog.yaml` (change record per solution); `architecture/solutions/_NTK-*/` (solution design as governed change artifact) |
| **Generator** | Capability page generator publishes change history; solution page generator publishes decisions |
| **Validator** | Capability changelog validator; solution folder structural convention |
| **Gap** | Formal OpenSpec change proposal workflow (propose→review→apply→archive) not yet enforced in CI; solution folder structure is conventional, not schema-validated |
| **Maturity** | Level 6 |

### Pillar 15 — Operational Runbooks as Code

| | |
|---|---|
| **Status** | NOT IN SCOPE |
| **Note** | NovaTrek Adventures is an architecture practice simulation, not a production operations environment. A real Instance assessment covers runbook as-code adoption. |

### Pillar 16 — Data Models as Code

| | |
|---|---|
| **Status** | PARTIAL |
| **Files** | `architecture/metadata/data-stores.yaml` (service-to-datastore registry) |
| **Gap** | `data-stores.yaml` catalogs data stores but declares no schemas, ER relationships, or field-level definitions; no DDL, Liquibase, dbt schema, or Avro/Protobuf files present |
| **Recommendation** | Add `architecture/metadata/schemas/{service}.schema.yaml` for entity type declarations per service; use as the seed for a real Instance's schema-as-code adoption |
| **Maturity** | Level 2 (catalog exists; no schema declarations) |

### Pillar 17 — Database Migrations as Code

| | |
|---|---|
| **Status** | NOT IN SCOPE |
| **Note** | Synthetic workspace has no live databases. A real Instance assessment covers Liquibase, Flyway, Atlas, or Alembic migration file adoption. |

### Pillar 18 — Data Contracts as Code

| | |
|---|---|
| **Status** | NOT IN SCOPE |
| **Note** | OpenAPI specs in `architecture/specs/` partially fulfill contract obligations between services, but no formal Data Contract Specification (Bitol/OpenDataMesh) files exist. A real Instance should formalize inter-service contracts here. |

### Pillar 19 — Event Schemas as Code

| | |
|---|---|
| **Status** | LIVE |
| **Files** | `architecture/events/*.yaml` (AsyncAPI specs per producer); `architecture/metadata/events.yaml` (event registry) |
| **Generator** | Event flow diagram generator |
| **Validator** | `asyncapi validate` — NOT yet in CI |
| **Gap** | Add `asyncapi validate` to CI on every PR touching `architecture/events/`; add JSON Schema for `events.yaml`; enforce that every event in the registry has a corresponding AsyncAPI spec |
| **Maturity** | Level 4 |

### Pillars 20–35

| Pillar | Status | Notes |
|--------|--------|-------|
| 20 — Security as Code | NOT IN SCOPE | No threat models, SAST configs, or IAM-as-code files in synthetic workspace |
| 21 — Compliance as Code | PARTIAL | `architecture/metadata/pci.yaml` catalogs PCI scope; no machine-verifiable compliance rules |
| 22 — Secrets Management as Code | NOT IN SCOPE | |
| 23 — SBOM as Code | NOT IN SCOPE | |
| 24 — Observability as Code | NOT IN SCOPE | |
| 25 — SLO / SLI as Code | NOT IN SCOPE | |
| 26 — Feature Flags as Code | NOT IN SCOPE | |
| 27 — Release Strategies as Code | NOT IN SCOPE | |
| 28 — Environment Definitions as Code | NOT IN SCOPE | |
| 29 — Service Mesh Configuration as Code | NOT IN SCOPE | |
| 30 — Team Topology as Code | NOT IN SCOPE | |
| 31 — Onboarding as Code | NOT IN SCOPE | |
| 32 — Developer Experience as Code | NOT IN SCOPE | |
| 33 — Architecture Principles as Code | NOT IN SCOPE | |
| 34 — Ubiquitous Language as Code | NOT IN SCOPE | |
| 35 — Coding Standards as Code | NOT IN SCOPE | |

> A real corporate Instance assessment fills in all 35 rows with actual status, files, gaps, and maturity scores. "NOT IN SCOPE" here means the synthetic NovaTrek workspace is an architecture practice simulation — it does not represent a full production delivery organization.

## Cross-Cutting Gaps

| Gap | Impact | Priority |
|-----|--------|----------|
| No JSON Schemas for `architecture/metadata/*.yaml` | AI cannot self-validate; PRs can introduce malformed data | HIGH |
| No drift check between source-of-truth YAML and generated portal pages | Generated pages can be hand-edited and diverge | HIGH |
| No central C4 DSL (Structurizr/Likec4) | C4 diagrams are scattered, not a unified model | MEDIUM |
| MADR validator not in CI | ADRs can be incomplete | MEDIUM |
| OpenAPI/AsyncAPI not validated in CI on every PR | Spec changes can break consumers | MEDIUM |
| AI instruction validation script deferred | Hub-and-spoke can drift silently | HIGH |
| Policy as Code absent | No machine-enforced architectural rules | LOW (start small) |
| BDD feature files not wired to runners | Tests are docs, not executable | LOW |

## Where We Are vs. The Maturity Model

```
Level 0 ─ Documents
Level 1 ─ Wikified
Level 2 ─ Docs as Code             ████████████████  COMPLETE
Level 3 ─ Diagrams as Code         ████████████████  COMPLETE
Level 4 ─ Metadata as Code         ████████████████  COMPLETE (no schemas)
Level 5 ─ Generators in CI         ██████████████░░  MOSTLY COMPLETE
Level 6 ─ Governance as Code       ███████████░░░░░  IN PROGRESS (OpenSpec)
Level 7 ─ AI Instructions as Code  ██████░░░░░░░░░░  IN FLIGHT
Level 8 ─ Policy as Code           ░░░░░░░░░░░░░░░░  NOT STARTED
Level 9 ─ AI-Native EaC            ░░░░░░░░░░░░░░░░  ASPIRATIONAL
```
