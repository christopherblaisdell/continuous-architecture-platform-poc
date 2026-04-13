# Confluence Page Hierarchy Reference

This file documents how pages are organized in the Confluence space (UPA) under the parent page
"Solution Architecture Practice — Comparative Evaluation of Agentic AI".

This layout is mirrored in the homepage Page Index (docs/index.md) as separate tables per section.

## Hierarchy

```
Solution Architecture Practice — Comparative Evaluation of Agentic AI  (index.md)
├── Evaluation Methodology  (framework/evaluation-methodology.md)
│   ├── Scoring Results  (framework/scoring-results.md)
│   └── Evaluation Approach  (framework/evaluation-approach.md)
├── Toolchain Decisions
│   ├── DD-01: Context and Configuration  (decisions/dd-01-context-configuration.md)
│   ├── DD-02: Billing Model  (decisions/dd-02-billing-model.md)
│   ├── DD-03: AI Provider  (decisions/dd-03-ai-provider.md)
│   ├── DD-04: Model Routing  (decisions/dd-04-model-routing.md)
│   └── DD-05: Architect Model Selection Autonomy  (decisions/dd-05-model-selection-autonomy.md)
├── Comparative Analysis (A, B, C)
│   ├── File-Type Handling: Option A vs Option C  (evidence/filetype-handling-a-vs-c.md)
│   ├── Build vs Leverage: Custom RAG in Context  (evidence/build-vs-leverage.md)
│   ├── Model Quality at Budget  (evidence/model-quality-at-budget.md)
│   └── Platform Landscape  (evidence/platform-landscape.md)
├── Option A (GitHub Copilot)
│   ├── File-Type Chunking Strategy for GitHub Copilot  (framework/filetype-chunking-strategy.md)
│   ├── GitHub Copilot Rollout Roadmap  (framework/copilot-rollout-roadmap.md)
│   ├── Architecture Is Not Just Coding — But the Tools Are the Same  (evidence/architecture-not-just-coding.md)
│   └── Controlling What Copilot Sees: The Context Injection Pipeline  (evidence/context-injection-controls.md)
│   └── AI Customization as a Living Practice: Extensibility, Governance, and Ownership  (evidence/customization-extensibility-governance.md)
├── Option C (Foundry IQ Integration)
│   └── What Does Foundry IQ Actually Require?  (evidence/foundry-iq-comparison.md)
└── Appendix
    ├── Deep Research Reports  (research/index.md)
    └── AI Glossary  (reference/glossary.md)
```

## Notes

- "Toolchain Decisions", "Comparative Analysis (A, B, C)", "Option A (GitHub Copilot)",
  "Option C (Foundry IQ Integration)", and "Appendix" are **folder pages** in Confluence
  (containers only, no corresponding source file).
- The homepage Page Index (docs/index.md) mirrors this hierarchy using separate H3 tables
  per section rather than a single flat table.
- Page order within each section matches the Confluence sidebar order.
- When adding new pages, update both this file and the Page Index tables in docs/index.md.
