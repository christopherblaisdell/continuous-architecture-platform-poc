<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2606630902/Solution+Architecture+Practice+Comparative+Evaluation+of+Agentic+AI -->

# AI Toolchain Evaluation

## Purpose

The Solution Architecture practice is adopting AI-assisted workflows for architecture analysis, solution design, and documentation. This evaluation compares three platform options to determine which best supports architecture work — balancing output quality, cost, operational complexity, and strategic fit.

### Options Under Evaluation

- **Option A — GitHub Copilot**: SaaS platform with intent-based billing, native workspace indexing, and declarative customization via instruction files. Testable immediately with zero infrastructure.
- **Option B — Roo Code + Kong AI Gateway**: Open-source IDE extension with token-based billing through a self-managed API gateway. Testable with moderate setup, requires API key provisioning and gateway configuration.
- **Option C — Bespoke Architecture Agent**: Custom-built agent on Azure AI Foundry. Requires weeks of engineering investment before testing can begin.

### Evaluation Principles

This evaluation follows a phased approach: test reversible, low-cost options empirically before committing to irreversible, high-cost alternatives. Options A and B can be compared head-to-head using real architecture scenarios. Option C requires significant engineering investment before it can be tested — see [Evaluation Approach](framework/evaluation-approach.md) for why this shapes the evaluation sequence.

### The Architecture Practice Pilot

Rather than evaluating options theoretically, this evaluation is grounded in a working pilot. A solution architect configured GitHub Copilot (Option A) with declarative instruction files, scoped rules, and mock enterprise tool integrations — then executed real architecture scenarios against a synthetic 19-microservice domain. The pilot produced 4 complete solution designs, 14 architecture decision records, 139 generated sequence diagrams, and a live documentation portal. All configuration is version-controlled markdown — zero custom engineering, zero infrastructure. The pilot's outputs and configuration serve as the primary evidence base for this evaluation.

## Two-Layer Decision Hierarchy

The diagram below shows the evaluation structure. Layer 1 defines how the architecture practice works with AI. Layer 2 decomposes the toolchain selection into four independent decisions that compose into the three platform options.

![Two-Layer Decision Hierarchy](img/two-layer-hierarchy.svg)

## Page Index

| Page | Purpose | Key Question Answered |
|------|---------|----------------------|
| [Scoring Results](framework/scoring-results.md) | Weighted scoring matrix with sensitivity analysis | **Which option wins and by how much?** |
| [Evaluation Approach](framework/evaluation-approach.md) | Phased testing strategy and decision sequencing | Why test A and B before investing in C? |
| [Evaluation Methodology](framework/evaluation-methodology.md) | 12-factor weighted scoring framework | How do we score and compare the three options objectively? |
| [DD-01: Context and Configuration](decisions/dd-01-context-configuration.md) | How each option injects domain knowledge | Do we need custom RAG or does native configuration suffice? |
| [Platform Landscape](evidence/platform-landscape.md) | Five-platform head-to-head comparison | Why is GitHub Copilot the strongest choice among all AI coding platforms? |
| [Model Quality at Budget](evidence/model-quality-at-budget.md) | Model tier analysis by price point | What model quality does each option actually deliver at its operating cost? |
| [Build vs Leverage](evidence/build-vs-leverage.md) | Custom RAG vs native platform capabilities | When is building a custom pipeline justified vs leveraging what exists? |
| [Architecture Is Not Just Coding](evidence/architecture-not-just-coding.md) | Evidence that AI coding platforms handle architecture work | Can general-purpose AI coding platforms do architecture, or do we need something bespoke? |
