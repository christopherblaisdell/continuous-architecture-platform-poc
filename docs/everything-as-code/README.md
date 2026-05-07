# Everything as Code (EaC)

This folder contains the framework, transformation plan, and supporting research for adopting an **Everything as Code** (EaC) practice for the Continuous Architecture Platform.

## What is "Everything as Code"?

**Everything as Code (EaC)** is the architectural philosophy that *every artifact required to design, build, operate, govern, and evolve a software system* is expressed as a **declarative, version-controlled, machine-readable, human-readable text file** stored in source control alongside application code.

It is the generalization of:

- **Infrastructure as Code (IaC)** — Terraform, Bicep, Pulumi
- **Pipeline as Code** — GitHub Actions YAML, GitLab CI YAML, Tekton
- **Configuration as Code** — Helm, Kustomize, App Configuration files
- **Documentation as Code (Docs as Code)** — Markdown + static site generators
- **Diagrams as Code** — PlantUML, Mermaid, Structurizr DSL
- **Policy as Code** — OPA/Rego, Sentinel, Conftest
- **Architecture as Code (AaC)** — C4 DSL, ADRs, capability YAML, actor YAML
- **Tests as Code** — BDD feature files, contract tests
- **AI Instructions as Code** — `copilot-instructions.md`, `.clinerules`, OpenSpec specs
- **UI Wireframes as Code** — Excalidraw JSON, Mermaid diagrams
- **Governance as Code** — change proposals, ADRs, capability changelogs

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
| [CURRENT-STATE-ASSESSMENT.md](CURRENT-STATE-ASSESSMENT.md) | What is already as-code in this workspace; what is not |
| [TRANSFORMATION-PLAN.md](TRANSFORMATION-PLAN.md) | Phased plan to bring everything to EaC, with concrete tasks |
| [AI-INSTRUCTIONS-AS-CODE.md](AI-INSTRUCTIONS-AS-CODE.md) | Treating AI instructions as a first-class EaC pillar — platform-agnostic via OpenSpec |
| [DEEP-RESEARCH-PROMPT-EAC-MATURITY-MODEL.md](DEEP-RESEARCH-PROMPT-EAC-MATURITY-MODEL.md) | Deep research prompt — formal naming, frameworks, maturity models, industry adoption |
| [DEEP-RESEARCH-PROMPT-EAC-MATURITY-MODEL-RESPONSE.md](DEEP-RESEARCH-PROMPT-EAC-MATURITY-MODEL-RESPONSE.md) | Blank file to paste the deep research response into |
| [DEEP-RESEARCH-PROMPT-AI-NATIVE-ARCHITECTURE.md](DEEP-RESEARCH-PROMPT-AI-NATIVE-ARCHITECTURE.md) | Deep research prompt — what does an AI-native architecture practice look like |
| [DEEP-RESEARCH-PROMPT-AI-NATIVE-ARCHITECTURE-RESPONSE.md](DEEP-RESEARCH-PROMPT-AI-NATIVE-ARCHITECTURE-RESPONSE.md) | Blank file for that response |

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
