<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2606630902/Solution+Architecture+Practice+Comparative+Evaluation+of+Agentic+AI -->

# AI Toolchain Evaluation

## Purpose

The Solution Architecture practice is adopting AI-assisted workflows for architecture analysis, solution design, and documentation. This evaluation compares three platform options to determine which best supports architecture work — balancing output quality, cost, operational complexity, and strategic fit.

### Options Under Evaluation

- **Option A — GitHub Copilot**: SaaS platform with intent-based billing, native workspace indexing, and declarative customization via instruction files. Testable immediately with zero infrastructure.
- **Option B — Roo Code + Kong AI Gateway**: Open-source IDE extension with token-based billing through a self-managed API gateway. Testable with moderate setup, requires API key provisioning and gateway configuration.
- **Option C — Bespoke Architecture Agent**: Custom-built agent on Azure AI Foundry with a purpose-built VS Code extension. Requires weeks of engineering investment before testing can begin.

### Evaluation Principles

This evaluation follows a phased approach: test reversible, low-cost options empirically before committing to irreversible, high-cost alternatives. Options A and B can be compared head-to-head using real architecture scenarios. Option C requires significant engineering investment before it can be tested — see [Evaluation Approach](evaluation-approach.md) for why this shapes the evaluation sequence.

## Two-Layer Decision Hierarchy

The diagram below shows the evaluation structure. Layer 1 defines how the architecture practice works with AI. Layer 2 decomposes the toolchain selection into four independent decisions that compose into the three platform options.

![Two-Layer Decision Hierarchy](img/two-layer-hierarchy.svg)

## Page Index

| Page | Purpose | Key Question Answered |
|------|---------|----------------------|
| [Evaluation Approach](evaluation-approach.md) | Phased testing strategy and decision sequencing | Why test A and B before investing in C? |
| [Evaluation Methodology](evaluation-methodology.md) | 12-factor weighted scoring framework | How do we score and compare the three options objectively? |
| [Build vs Leverage](build-vs-leverage.md) | Custom RAG vs native platform capabilities | When is building a custom pipeline justified vs leveraging what exists? |
| [Architecture Is Not Just Coding](architecture-not-just-coding.md) | Evidence that AI coding platforms handle architecture work | Can general-purpose AI coding platforms do architecture, or do we need something bespoke? |
