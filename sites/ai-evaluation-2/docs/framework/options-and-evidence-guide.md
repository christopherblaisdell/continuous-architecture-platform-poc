<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: -->

# Options and Evidence Guide

This page provides detailed descriptions of each option evaluated and a complete index of all evidence pages organized by topic.

## Options Under Evaluation

- **Option A — GitHub Copilot**: SaaS platform with intent-based billing, native workspace indexing, and declarative customization via instruction files. Testable immediately with zero infrastructure. Customizations are portable Markdown; file naming conventions are platform-specific but converging on open standards.
- **Option B — Roo Code + Kong AI Gateway**: Open-source IDE extension with token-based billing through a self-managed API gateway. Testable with moderate setup, requires API key provisioning and gateway configuration. Fully open-source; all configuration is portable.
- **Option C — Bespoke Architecture Agent**: Custom-built agent on Azure AI Foundry. Requires weeks of engineering investment before testing can begin. Deep platform lock-in — customizations, knowledge pipelines, and integrations are Azure-specific; migration would mean rebuilding.
- **Option D — Hybrid (A absorbs C)**: Deploy Copilot (Option A) as the platform, then integrate Option C's custom Foundry model as a BYOK endpoint within it. Architects get built-in models for routine work, frontier models for complex design, and the domain-specialized model for enterprise analysis — all in the same model picker, with no custom IDE infrastructure. Inherits Option A's customization portability; accepts infrastructure lock-in only where Foundry adds unique value.

## Two-Layer Decision Hierarchy

The diagram below shows the evaluation structure. Layer 1 defines how the architecture practice works with AI. Layer 2 decomposes the toolchain selection into six independent decisions that compose into three discrete platform options — plus Option D, which is a hybrid composition of Options A and C.

![Two-Layer Decision Hierarchy](../img/two-layer-hierarchy.svg)

## Evidence Guide

### Evaluation Methodology

| Page | Purpose | Key Question Answered |
|------|---------|----------------------|
| [Scoring Results](scoring-results.md) | Weighted scoring matrix with sensitivity analysis | **Which option wins and by how much?** |
| [Evaluation Approach](evaluation-approach.md) | Phased testing strategy and decision sequencing | Why test A and B before investing in C? |
| [Evaluation Methodology](evaluation-methodology.md) | 13-factor weighted scoring framework | How do we score and compare the options objectively? |

### Toolchain Decisions

| Page | Purpose | Key Question Answered |
|------|---------|----------------------|
| [DD-01: Context and Configuration](../decisions/dd-01-context-configuration.md) | How each option injects domain knowledge | Do we need custom RAG or does native configuration suffice? |
| [DD-02: Billing Model](../decisions/dd-02-billing-model.md) | Per-seat vs per-token vs hybrid billing | Which billing model supports sustained architecture work without perverse incentives? |
| [DD-03: AI Provider](../decisions/dd-03-ai-provider.md) | Provider selection across all options | Which vendor best combines output quality, workflow integration, and governance? |
| [DD-04: Model Routing](../decisions/dd-04-model-routing.md) | Model selection and routing strategy | Does model routing require custom infrastructure or is it built into the platform? |
| [DD-05: Model Selection Autonomy](../decisions/dd-05-model-selection-autonomy.md) | Architect control over model choice | Should architects choose their model, or should it be locked down by a central team? |
| [DD-06: IDE Client Selection](../decisions/dd-06-ide-client-selection.md) | Which IDE client consumes the custom Foundry model | If we build a custom model, which IDE client should consume it — and does that client preserve architect autonomy? |

### Comparative Analysis (A, B, C)

| Page | Purpose | Key Question Answered |
|------|---------|----------------------|
| [File-Type Handling: A vs C](../evidence/filetype-handling-a-vs-c.md) | Side-by-side comparison of how Options A and C handle each architecture file type | Does Azure AI Search chunk architecture files better than Copilot? |
| [Build vs Leverage](../evidence/build-vs-leverage.md) | Custom RAG vs native platform capabilities | When is building a custom pipeline justified vs leveraging what exists? |
| [Model Quality at Budget](../evidence/model-quality-at-budget.md) | Model tier analysis by price point | What model quality does each option actually deliver at its operating cost? |
| [Platform Landscape](../evidence/platform-landscape.md) | Five-platform head-to-head comparison | Why is GitHub Copilot the strongest choice among all AI coding platforms? |

### Option A (GitHub Copilot)

| Page | Purpose | Key Question Answered |
|------|---------|----------------------|
| [File-Type Chunking Strategy](filetype-chunking-strategy.md) | Per-file-type optimization plan for Copilot context delivery | How do we ensure each architecture artifact type is chunked and retrieved correctly? |
| [Copilot Rollout Roadmap](copilot-rollout-roadmap.md) | Practical deployment plan for the architecture team | How do we actually roll out Copilot and get architecture content into AI? |
| [Architecture Is Not Just Coding](../evidence/architecture-not-just-coding.md) | Evidence that AI coding platforms handle architecture work | Can general-purpose AI coding platforms do architecture, or do we need something bespoke? |
| [Controlling What Copilot Sees](../evidence/context-injection-controls.md) | Context injection pipeline — what controls exist and how to optimize | How does Copilot decide what enters the LLM's context window, and what can we control? |

### Option D (Hybrid Architecture)

| Page | Purpose | Key Question Answered |
|------|---------|----------------------|
| [Option D — Hybrid Architecture](../evidence/option-d-hybrid-architecture.md) | BYOK integration analysis with feature compatibility and risk assessment | Can the Foundry model run inside Copilot via BYOK, and what are the limitations? |
| [Option D POC: BYOK Endpoint Validation](../evidence/option-d-poc-validation.md) | Live proof that Azure OpenAI deploys in minutes via Bicep IaC, scales to zero, and matches BYOK API format | Does the Azure-side infrastructure actually work, and how hard is it to set up? |
| [Cost Offset Analysis](../evidence/cost-offset-hybrid-subsidy.md) | Financial case for 0x models subsidizing the Foundry investment | How much does Copilot's free model tier reduce the net cost of maintaining a custom model? |
| [DD-06: IDE Client Selection](../decisions/dd-06-ide-client-selection.md) | IDE client comparison for consuming a custom Foundry model | Which IDE client should consume the custom model — and what are the frozen customization risks? |
| [Customization Extensibility and Governance](../evidence/customization-extensibility-governance.md) | Inner source governance model for AI customization ownership and evolution | Who owns AI customizations, how do they evolve, and what happens if architects cannot control them? |
| [Customization Portability: Option D + OpenSpec](../evidence/customization-lock-in-foundry-vs-portable.md) | How Option D, living practice customization, and OpenSpec neutralize Foundry lock-in across four layers | What happens to Foundry customizations if you switch platforms — and how does Option D make the risk acceptable? |

### Option C (Foundry IQ Integration)

| Page | Purpose | Key Question Answered |
|------|---------|----------------------|
| [What Does Foundry IQ Actually Require?](../evidence/foundry-iq-comparison.md) | Operational requirements for a Foundry IQ-based agent | Is Foundry IQ a turnkey product or a build-it-yourself platform? |
