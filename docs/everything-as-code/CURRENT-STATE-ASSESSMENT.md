# Synthetic Exemplar Assessment — Everything as Code

> **BLUEPRINT — SYNTHETIC EXEMPLAR.** This document is **not** a corporate current-state assessment. It is a worked example demonstrating *how* the assessment template is applied, using the synthetic NovaTrek Adventures workspace as the subject. All scores, file counts, and gaps below describe the fictional workspace. When the blueprint is exported to a corporate **EaC Adoption Instance**, this document is replaced — pillar by pillar — with the real assessment of the actual practice. The structure, pillar list, scoring rubric, and gap-table format are the durable parts; the findings are not.

This document assesses where the synthetic exemplar workspace stands on the EaC maturity model, pillar by pillar. It is the worked example that informs [TRANSFORMATION-PLAN.md](TRANSFORMATION-PLAN.md).

## Summary

| | |
|---|---|
| **Overall maturity level** | **Level 6 — Governance as Code** (with elements of Level 7 in flight) |
| **Strongest pillars** | Architecture metadata, OpenAPI specs, sequence diagrams, docs portal, ADRs |
| **Weakest pillars** | Policy as Code, AI Instructions as Code (governance still being activated), schema validation in CI |
| **Most impactful next step** | Activate JSON Schema validation for every YAML in `architecture/metadata/` |

## Pillar-by-Pillar Assessment

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
| **Files** | `.github/workflows/*.yml`, `.gitlab-ci.yml` (if present) |
| **Generator** | GitHub Actions |
| **Validator** | None automated; relies on PR runs |
| **Gap** | Add `actionlint` to a PR-level workflow |
| **Maturity** | Level 5 |

### Pillar 3 — Architecture as Code (Sequence Diagrams)

| | |
|---|---|
| **Status** | LIVE — generated |
| **Files** | `portal/docs/microservices/puml/*.puml` |
| **Generator** | `portal/scripts/generate-microservice-pages.py` produces 139 diagrams from OpenAPI specs |
| **Validator** | PlantUML `-checkonly` on demand |
| **Gap** | Add a CI step that fails if generated PUML differs from committed PUML (drift check) |
| **Maturity** | Level 6 |

### Pillar 4 — Architecture as Code (C4 Component Diagrams)

| | |
|---|---|
| **Status** | PARTIAL |
| **Files** | `architecture/diagrams/` (PlantUML); some inlined in solution designs |
| **Generator** | PlantUML CLI |
| **Validator** | None |
| **Gap** | No central C4 DSL (Structurizr, Likec4) — diagrams are per-service PUML, not a unified model |
| **Recommendation** | Evaluate Structurizr DSL or Likec4 for the unified C4 model; keep PUML for service-internal diagrams |
| **Maturity** | Level 4 |

### Pillar 5 — UI Wireframes as Code

| | |
|---|---|
| **Status** | LIVE |
| **Files** | `architecture/wireframes/{web-guest-portal,web-ops-dashboard,app-guest-mobile}/*.excalidraw` |
| **Generator** | CI converts `.excalidraw` JSON → SVG + HTML + MD wrapper to `portal/docs/applications/{app}/wireframes/` |
| **Validator** | JSON parse only |
| **Gap** | No JSON Schema for Excalidraw files; CI generation works but is not validated against a wireframe inventory |
| **Maturity** | Level 5 |

### Pillar 6 — Actors as Code

| | |
|---|---|
| **Status** | LIVE |
| **File** | `architecture/metadata/actors.yaml` |
| **Generator** | Portal page generator (if applicable) |
| **Validator** | NONE — no JSON Schema |
| **Gap** | Author `architecture/schemas/actors.schema.json`; validate in CI |
| **Maturity** | Level 4 |

### Pillar 7 — Applications as Code

| | |
|---|---|
| **Status** | LIVE |
| **Files** | `architecture/metadata/applications.yaml`, `app-titles.yaml`, `consumers.yaml` |
| **Validator** | NONE |
| **Gap** | JSON Schema; consolidate `app-titles.yaml` into `applications.yaml` if titles are derivable |
| **Maturity** | Level 4 |

### Pillar 8 — Capabilities as Code

| | |
|---|---|
| **Status** | LIVE — strongest pillar |
| **Files** | `architecture/metadata/capabilities.yaml`, `capability-changelog.yaml` |
| **Generator** | `portal/scripts/generate-capability-pages.py` |
| **Validator** | Capability changelog validator (in `portal/scripts/utilities/`?) |
| **Gap** | Formalize JSON Schema for both files; document the L1/L2/L3 model in this folder |
| **Maturity** | Level 6 |

### Pillar 9 — Everything Under `architecture/`

Inventory of `architecture/metadata/`:

| File | As-code? | Schema? | Used by |
|------|----------|---------|---------|
| `actors.yaml` | YES | NO | (manual reference) |
| `app-titles.yaml` | YES | NO | Portal generators |
| `applications.yaml` | YES | NO | Portal generators |
| `capabilities.yaml` | YES | NO | Capability page generator |
| `capability-changelog.yaml` | YES | Custom | Capability page generator, solution rollup |
| `consumers.yaml` | YES | NO | Portal generators |
| `cross-service-calls.yaml` | YES | NO | Microservice page generator |
| `data-stores.yaml` | YES | NO | Microservice page generator |
| `delivery-status.yaml` | YES | NO | (manual reference) |
| `domains.yaml` | YES | NO | Microservice page generator (DOMAINS dict mirrors this) |
| `events.yaml` | YES | NO | Event flow diagram generator |
| `label-to-svc.yaml` | YES | NO | Anchor / link generator |
| `pci.yaml` | YES | NO | Compliance reporting |
| `pipeline-registry.yaml` | YES | NO | (TBD) |
| `tickets.yaml` | YES | NO | Ticket page generator, ticket-client.py |

Other `architecture/` subfolders:

| Folder | As-code? | Notes |
|--------|----------|-------|
| `architecture/specs/` | YES | OpenAPI YAML — needs `openapi-spec-validator` in CI |
| `architecture/events/` | YES | AsyncAPI YAML — needs validation in CI |
| `architecture/wireframes/` | YES | Excalidraw JSON — CI generates SVG |
| `architecture/diagrams/` | YES | PlantUML |
| `architecture/calm/` | YES | CALM JSON — needs CALM validator in CI |
| `architecture/solutions/_NTK-*/` | YES (Markdown) | Folder structure is conventional, not enforced |
| `architecture/reminders/` | YES | Markdown |

### Pillar 10 — Decisions as Code (ADRs)

| | |
|---|---|
| **Status** | LIVE |
| **Files** | `decisions/ADR-001` through `ADR-014`; per-solution ADRs in `3.solution/d.decisions/` |
| **Validator** | NONE — no MADR section validator |
| **Gap** | Custom validator that asserts MADR sections (Status, Date, Context, Decision Drivers, Considered Options, Decision Outcome, Consequences) are present |
| **Maturity** | Level 4 |

### Pillar 11 — Tickets as Code

| | |
|---|---|
| **Status** | LIVE |
| **File** | `architecture/metadata/tickets.yaml` |
| **Generator** | `portal/scripts/generate-ticket-pages.py` |
| **Validator** | NONE |
| **Gap** | JSON Schema; ensure capability mappings derive from changelog (not duplicated) |
| **Maturity** | Level 5 |

### Pillar 12 — Tests as Code

| | |
|---|---|
| **Status** | PARTIAL |
| **Files** | `tests/`, plus `BDD-AUTHORING-GUIDE.md` in `docs/` |
| **Validator** | Test runner of choice |
| **Gap** | Most "tests" today are documentation; need to wire BDD feature files to executable runners for the synthetic NovaTrek services |
| **Maturity** | Level 3 |

### Pillar 13 — Policy / Governance as Code

| | |
|---|---|
| **Status** | NOT STARTED |
| **Gap** | No `policies/` folder; no OPA, no Conftest, no ArchUnit equivalents for architectural rules |
| **Recommendation** | Start with Conftest + Rego rules to enforce things like "every service MUST have an OpenAPI spec" or "every YAML in metadata MUST validate against its schema" |
| **Maturity** | Level 0 for this pillar |

### Pillar 14 — AI Instructions as Code

| | |
|---|---|
| **Status** | IN FLIGHT — hub-and-spoke active, OpenSpec governance phases 1-3 verified, Phase 5 (validation script) deferred |
| **Files** | `sites/ai-evaluation-2/docs/open-spec/.ai-instructions/` (canonical); 5 derived files (`.clinerules`, `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`) |
| **Validator** | `scripts/validate-ai-instructions.sh` (DEFERRED) |
| **Gap** | Activate validation script; complete OpenSpec Phase 10 (first real propose→apply→archive cycle); evaluate Cursor and Windsurf as additional derived targets |
| **Maturity** | Level 6 for this pillar; pushing toward Level 7 |

### Pillar 15 — Documentation as Code

| | |
|---|---|
| **Status** | LIVE — strong |
| **Files** | `portal/docs/`, `mkdocs.yml`, `sites/manifest.yaml` |
| **Generator** | MkDocs Material → Azure Static Web Apps + Confluence read-only mirror |
| **Validator** | `mkdocs build --strict`, link checker, Confluence drift check |
| **Maturity** | Level 7 |

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
