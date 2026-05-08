# Everything as Code (EaC) — Adoption Blueprint

> **BLUEPRINT — NOT AN INSTANCE.** This folder contains a portable, target-agnostic **EaC Adoption Blueprint**. It is authored and refined inside this synthetic workspace (NovaTrek Adventures), where every artifact is fictional. The blueprint is not executed here. It is exported to a separate corporate **EaC Adoption Instance** workspace where it is instantiated against real infrastructure, real tickets, real source code, and the real architecture practice.
>
> **Two artifacts, two roles:**
>
> | Artifact | Lives in | Purpose |
> |----------|----------|---------|
> | **Blueprint** (this folder) | Synthetic workspace | Pattern definition, refined safely against fictional data |
> | **Instance** (future) | Corporate workspace | The blueprint applied to actual systems |
>
> All references to specific paths, services, file counts, or maturity scores in this folder describe the **synthetic exemplar** used to validate the blueprint — they are illustrative, not corporate facts.

This folder contains the framework, the synthetic exemplar that validates it, the adoption plan template, and the supporting research for adopting an **Everything as Code** (EaC) practice.

## What is "Everything as Code"?

**Everything as Code (EaC)** is the architectural philosophy that *every artifact required to design, build, operate, govern, and evolve a software system* is expressed as a **declarative, version-controlled, machine-readable, human-readable text file** stored in source control alongside application code.

It is the generalization of:

- **Infrastructure as Code (IaC)** — Terraform, Bicep, Pulumi
- **Pipeline as Code** — GitHub Actions YAML, GitLab CI YAML, Tekton
- **Configuration as Code** — Helm, Kustomize, App Configuration files
- **Documentation as Code (Docs as Code)** — Markdown + static site generators
- **Diagrams as Code** — PlantUML, Mermaid, Structurizr DSL
- **Policy as Code** — OPA/Rego, Sentinel, Conftest
- **Architecture as Code (AaC)** — system structure and runtime flows expressed as diagrams and specs (e.g., C4-PlantUML, Structurizr DSL, OpenAPI, AsyncAPI)
- **Actors as Code** — every human role, external system, and persona declared in a version-controlled registry (e.g., YAML actor catalog with JSON Schema)
- **Capabilities as Code** — L1/L2/L3 business capability hierarchy in YAML with a changelog that links every solution and change to the capabilities it affects
- **Tests as Code** — BDD feature files, contract tests
- **AI Instructions as Code** — platform-specific instruction files (e.g., `copilot-instructions.md` for GitHub Copilot, `.clinerules` for Roo Code), governed via a structured change workflow (e.g., OpenSpec)
- **UI Wireframes as Code** — Excalidraw JSON, Mermaid diagrams
- **Governance as Code** — change proposals, ADRs, capability changelogs
- **Patterns and Anti-patterns as Code** — a version-controlled YAML catalog of approved architectural patterns and identified anti-patterns, linked to the decisions and services where they apply (e.g., Saga, CQRS, Strangler Fig; anti-patterns like Shared Database, Distributed Monolith)

## Why now?

AI agents reason over **structured, declarative artifacts** — not screenshots, slide decks, or wiki pages locked behind WYSIWYG editors. As AI takes a larger role in software architecture work, every artifact that is not "as code" becomes:

1. **Invisible to AI** — agents cannot read or reason over it
2. **Untestable** — there is no diff, no validation, no review gate
3. **Untraceable** — no git history, no blame, no audit trail
4. **Non-portable** — locked to a vendor's tool format
5. **Drift-prone** — diverges silently from the system it describes

EaC is the prerequisite for **AI-assisted continuous architecture** — the practice this workspace exists to prove.

## Documents

| Document | Purpose |
|----------|---------|
| [EVERYTHING-AS-CODE-FRAMEWORK.md](EVERYTHING-AS-CODE-FRAMEWORK.md) | The full framework — definitions, pillars, naming, industry terms, maturity model |
| [CURRENT-STATE-ASSESSMENT.md](CURRENT-STATE-ASSESSMENT.md) | **Synthetic exemplar assessment** — demonstrates the assessment template applied to the fictional NovaTrek workspace; serves as the worked example to copy when assessing a real corporate workspace |
| [TRANSFORMATION-PLAN.md](TRANSFORMATION-PLAN.md) | **Adoption plan template** — phased blueprint to be tailored and instantiated in the corporate workspace |
| [AI-INSTRUCTIONS-AS-CODE.md](AI-INSTRUCTIONS-AS-CODE.md) | Treating AI instructions as a first-class EaC pillar — platform-agnostic via OpenSpec |
| [AI-INSTRUCTION-GOVERNANCE.md](AI-INSTRUCTION-GOVERNANCE.md) | Pillar 11 governance annex — single source of truth, conflict detection, baseline access; extends AI-INSTRUCTIONS-AS-CODE.md |
| [DEEP-RESEARCH-PROMPT-EAC-MATURITY-MODEL.md](DEEP-RESEARCH-PROMPT-EAC-MATURITY-MODEL.md) | Deep research prompt — formal naming, frameworks, maturity models, industry adoption |
| [DEEP-RESEARCH-PROMPT-EAC-MATURITY-MODEL-RESPONSE.md](DEEP-RESEARCH-PROMPT-EAC-MATURITY-MODEL-RESPONSE.md) | Response placeholder — paste deep research results here; not exported to Instance workspaces |
| [DEEP-RESEARCH-PROMPT-AI-NATIVE-ARCHITECTURE.md](DEEP-RESEARCH-PROMPT-AI-NATIVE-ARCHITECTURE.md) | Deep research prompt — what does an AI-native architecture practice look like |
| [DEEP-RESEARCH-PROMPT-AI-NATIVE-ARCHITECTURE-RESPONSE.md](DEEP-RESEARCH-PROMPT-AI-NATIVE-ARCHITECTURE-RESPONSE.md) | Response placeholder — paste deep research results here; not exported to Instance workspaces |
| [standardized.taxonomy.of.ai.instructions.etc.deep.research.response.md](standardized.taxonomy.of.ai.instructions.etc.deep.research.response.md) | Deep research response — standardized taxonomy of AI instructions formats and OpenSpec governance model; supports Pillar 11 (AI Instructions as Code) |
| [SYNTHETIC-EXEMPLAR-BACKLOG.md](SYNTHETIC-EXEMPLAR-BACKLOG.md) | **NovaTrek carry-over only** — deferred tasks specific to this synthetic workspace; not exported to Instance workspaces |
| [export-blueprint.sh](export-blueprint.sh) | Shell script to copy the blueprint to a corporate Instance workspace; not exported (it runs from this workspace) |

## Exporting to a Corporate Instance

The blueprint in this folder is designed to travel. Once it has been validated and refined against the synthetic NovaTrek exemplar, it is exported to a real corporate workspace (the **Instance**) where it is instantiated against actual systems.

### What the export produces

| Category | Files | What to do in the Instance |
|----------|-------|---------------------------|
| **Pure blueprint** | README.md, EVERYTHING-AS-CODE-FRAMEWORK.md, TRANSFORMATION-PLAN.md, AI-INSTRUCTIONS-AS-CODE.md, AI-INSTRUCTION-GOVERNANCE.md, DEEP-RESEARCH-PROMPT-EAC-MATURITY-MODEL.md, DEEP-RESEARCH-PROMPT-AI-NATIVE-ARCHITECTURE.md, standardized.taxonomy.of.ai.instructions.etc.deep.research.response.md | Use as-is. No Instance-specific edits needed. |
| **Exemplar template** | CURRENT-STATE-ASSESSMENT.md | Keep the structure; replace all NovaTrek findings with real workspace findings. |
| **Excluded** | SYNTHETIC-EXEMPLAR-BACKLOG.md, DEEP-RESEARCH-PROMPT-EAC-MATURITY-MODEL-RESPONSE.md, DEEP-RESEARCH-PROMPT-AI-NATIVE-ARCHITECTURE-RESPONSE.md | Not exported. NovaTrek carry-over and response placeholder files only. |

### How to export

A shell script automates the copy. Run it from this synthetic workspace, pointing at the root of the corporate workspace:

```bash
# Dry run — verify what will be copied without writing anything
./docs/everything-as-code/export-blueprint.sh \
  --target /path/to/corporate/workspace \
  --dry-run

# Live export
./docs/everything-as-code/export-blueprint.sh \
  --target /path/to/corporate/workspace
```

The script copies all blueprint files to `<target>/docs/everything-as-code/` and prints a numbered next-steps checklist.

### Manual export (alternative)

If the corporate workspace cannot be reached from the same machine, copy these files manually:

```
docs/everything-as-code/README.md
docs/everything-as-code/EVERYTHING-AS-CODE-FRAMEWORK.md
docs/everything-as-code/TRANSFORMATION-PLAN.md
docs/everything-as-code/AI-INSTRUCTIONS-AS-CODE.md
docs/everything-as-code/CURRENT-STATE-ASSESSMENT.md          ← replace content; keep structure
docs/everything-as-code/DEEP-RESEARCH-PROMPT-EAC-MATURITY-MODEL.md
docs/everything-as-code/DEEP-RESEARCH-PROMPT-AI-NATIVE-ARCHITECTURE.md
docs/everything-as-code/standardized.taxonomy.of.ai.instructions.etc.deep.research.response.md
```

Do **not** copy `SYNTHETIC-EXEMPLAR-BACKLOG.md` — it contains NovaTrek-specific deferred items that have no meaning in any other workspace.

### Post-export checklist

After placing the files in the corporate workspace:

- [ ] Record the imported blueprint version in the Instance README (see the Blueprint Version table at the bottom of this file — copy and update it, replacing `Blueprint` with `Instance imported` and noting the date)
- [ ] Complete the Bootstrap pillar selection exercise in TRANSFORMATION-PLAN.md (mark each of the 35 pillars In Scope / Out of Scope / Future)
- [ ] Replace CURRENT-STATE-ASSESSMENT.md with a real assessment of the corporate workspace
- [ ] Author the adoption ADR in the corporate `decisions/` folder; declare which pillars are in Wave 1 scope
- [ ] Commit `docs/everything-as-code/` to version control in the corporate workspace
- [ ] Add the EaC transformation track to the corporate roadmap

---

## Quick Answer to "What is this called?"

The umbrella term is **Everything as Code** (EaC). The transformation toward it has several emerging names:

| Term | Used by |
|------|---------|
| **Everything as Code (EaC) transformation** | Most common umbrella term |
| **Codification** | Generic term for converting any artifact to code |
| **Declarative transformation** | Used in the cloud-native / GitOps community |
| **GitOps for Architecture** | When the workflow uses git as the single source of truth |
| **Continuous Architecture** | The practice; EaC is the enabling technique |
| **AI-native architecture practice** | Emerging term — architecture practice designed for AI co-authorship |
| **Spec-Driven Development** | Adjacent term (OpenSpec, AWS Kiro) for AI-assisted authoring of specs as code |

There is no single ISO/IEEE-blessed term yet. See the deep research prompt for an investigation into formal standardization status.

---

## Blueprint Version

| Field | Value |
|-------|-------|
| **Blueprint version** | 2026.05 |
| **Pillar count** | 35 |
| **Maturity model levels** | 0–9 |
| **Last updated** | 2026-05-07 |

When you export this blueprint to a corporate Instance workspace, record the version you exported in the Instance's `docs/everything-as-code/README.md`. This allows the Instance team to track when the pattern was imported and whether a newer version of the blueprint is available.

A version bump is warranted when:
- The pillar count changes
- The maturity model levels change
- The export script categories change (files added to or removed from the blueprint)
- The canonical pillar names or numbers change
