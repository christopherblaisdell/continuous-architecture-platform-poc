<!-- CONFLUENCE-PUBLISH -->

# DD-03: AI Provider

| | |
|-----------|-------|
| **Status** | Under Evaluation |
| **Date** | 2026-04-07 |
| **Scope** | Which vendor and platform delivers AI-assisted architecture capabilities? |
| **Feeds into** | DD-04 (Model Routing), EF-04 (Output Quality), EF-10 (Workflow Integration) |

---

## Problem Statement

The architecture practice needs an AI platform that integrates into the architect's daily workflow — VS Code, git, pull requests, documentation publishing — and delivers frontier-model reasoning on complex, multi-service analysis. The provider decision determines not just which AI the practice uses, but how it fits into the existing toolchain, how it is governed, and how it scales.

The question is: **which provider best combines output quality, workflow integration, governance, and organizational fit for an enterprise architecture practice?**

---

## Options

### Option A: GitHub Copilot (SaaS Platform)

A first-party GitHub product embedded in VS Code with intent-based billing, native workspace indexing, and declarative customization via instruction files.

- **Native integration** — same vendor as the organization's source control platform; SSO, audit trails, and policy management are already configured
- **Declarative customization** — instruction files, skills, agent modes, and MCP servers — all version-controlled in the repository
- **Fixed-price frontier model** — Claude Opus 4.6 included at $39/month per seat (see [DD-02](dd-02-billing-model.md))
- **Proven in practice** — the architecture practice pilot has produced 4 solution designs, 14 ADRs, and 139 generated diagrams using this platform
- **Limitation:** Copilot's advanced customization features (skills, hooks, agent modes) are proprietary — the format is not portable, though the content is

### Option B: Roo Code + Kong AI Gateway (Open-Source + Custom Gateway)

An open-source VS Code extension paired with a self-managed API gateway for model routing, cost tracking, and policy enforcement.

- **Full model control** — any model from any provider, routed through Kong with per-request cost visibility
- **Open-source transparency** — Roo Code's agent behavior is fully inspectable; no black-box decisions
- **Gateway overhead** — Kong requires provisioning, configuration, API key management, and operational monitoring
- **Separate governance surface** — security, audit, and access control are managed outside GitHub, adding administrative complexity
- **Rule migration required** — existing Copilot instruction files would need conversion to Roo Code's format

### Option C: Bespoke Agent (Azure AI Foundry)

A custom-built agent with embedded domain knowledge, deployed on Azure AI Foundry infrastructure.

- **Maximum customization** — agent behavior is purpose-built for architecture work
- **Azure governance** — inherits Azure's compliance certifications, data residency controls, and identity management
- **Heaviest engineering investment** — custom agent framework, knowledge embedding pipeline, ongoing maintenance
- **Budget-constrained model tier** — per-token pricing at scale forces cheaper models (see [Model Quality at Budget](../evidence/model-quality-at-budget.md))
- **Longest time to value** — weeks to months of engineering before the first architecture scenario can be tested

---

## Assessment

The [Platform Landscape](../evidence/platform-landscape.md) page provides a detailed head-to-head comparison across five AI coding platforms (Copilot, Cursor, Windsurf, Cline, Claude Code) on pricing, context injection, enterprise governance, and organizational fit. The key findings relevant to DD-03:

| Dimension | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| Workflow integration | Native VS Code + GitHub; zero context switching | VS Code extension + separate gateway dashboard | Separate agent interface; parallel management surfaces |
| Governance | Inherits existing GitHub Enterprise governance — SSO, audit, policies | Separate governance for Roo Code (OSS, no vendor governance) + Kong (enterprise tier available) | Azure governance for infrastructure; custom code = custom security surface |
| Organizational fit | Adds seats to existing GitHub contract | New vendor relationship, new procurement process | Engineering project with ongoing staffing requirements |
| Customization maturity | Most sophisticated hierarchy — instructions, skills, agents, hooks | Capable but different format; .clinerules-style rules | Everything is custom — maximum flexibility, maximum maintenance burden |
| Portability | Instruction content portable; activation format is proprietary | Open-source; fully portable | Deep lock-in — migration means rebuilding |

---

## Recommendation

**GitHub Copilot (Option A)** is the recommended provider for DD-03. The decision rests on three structural advantages that alternatives cannot replicate without significant investment:

1. **Zero procurement friction** — adding Copilot seats to an existing GitHub contract is an IT operations task, not a months-long vendor evaluation
2. **Single governance surface** — every other option introduces a new governance boundary to manage alongside GitHub
3. **Proven architecture output** — the architecture practice pilot demonstrates that Copilot, configured with declarative instruction files, produces architecture-quality output today — not after weeks of engineering

The competitive risks (Cursor's agent quality, Windsurf's SWE-1.5 model, Cline's transparency) are real but testable — the [Evaluation Approach](../framework/evaluation-approach.md) sequences empirical testing before commitment.

---

**See also:**

- [Platform Landscape](../evidence/platform-landscape.md) — Five-platform head-to-head comparison across pricing, customization, governance, and organizational fit
- [DD-01: Context and Configuration](dd-01-context-configuration.md) — How each option injects domain knowledge
- [DD-02: Billing Model](dd-02-billing-model.md) — Why per-seat fixed billing favors architecture work
- [Architecture Is Not Just Coding](../evidence/architecture-not-just-coding.md) — Evidence that general-purpose AI coding platforms handle architecture work
