# AI Toolchain Research

| | |
|-----------|-------|
| **Phase** | Phase 1 — AI Tool Cost Comparison |
| **Status** | COMPLETE |
| **Decision** | ADR-001: AI Toolchain Selection (`decisions/ADR-001-ai-toolchain-selection.md`) |

---

## Overview

Phase 1 of the Continuous Architecture Platform evaluated two AI toolchains for architecture practice workflows:

- **GitHub Copilot** (Pro+, Claude Opus 4.6, Agent Mode)
- **Roo Code + OpenRouter** (Claude Opus 4.6 via OpenRouter API)

Five representative architecture scenarios were executed on each toolchain. Results were scored on quality, standards compliance, and cost.

**Phase 1 conclusion: GitHub Copilot Pro+ is the selected toolchain.**

---

## Research Documents

### Phase 1 Evaluation

| Document | Description |
|----------|-------------|
| Phase 1 Evaluation Plan (`phases/phase-1-ai-tool-cost-comparison/AI-TOOL-COST-COMPARISON-PLAN.md`) | Scenario playbook, scoring rubric, and evaluation methodology |
| Cost Measurement Methodology (`phases/phase-1-ai-tool-cost-comparison/COST-MEASUREMENT-METHODOLOGY.md`) | How costs were measured for both toolchains |

### Workspace Semantic Search (Vector DB / RAG)

During Phase 1, the practice investigated whether a vector database could be built over the entire workspace to give Roo Code semantic search capability. The research also evaluated Kong AI Gateway's role in this architecture.

| Document | Description |
|----------|-------------|
| [Vector DB / RAG Feasibility Analysis](vector-db-rag-feasibility.md) | Feasibility, tool comparison, and recommendation for solution architecture practice |
| [Workspace Vector DB Implementation Plan](vector-db-implementation-plan.md) | Detailed implementation plan: chunking pipeline, ChromaDB, MCP server, Kong AI Gateway, VS Code extension option |
| [Phase 2 Next Steps](phase-2-next-steps.md) | Decision point and action items following Phase 1 completion |

### Deep Research

| Document | Description |
|----------|-------------|
| Copilot vs Kong+Roo Economics (`research/DEEP-RESEARCH-1.md`) | Token economics, semantic indexing architecture, and cost modeling |
| Context Window Utilization Analysis (`research/CONTEXT-WINDOW-UTILIZATION-ANALYSIS.md`) | Empirical comparison of context management between Roo Code and Copilot |
| Copilot Billing Deep Research (`research/DEEP-RESEARCH-RESULTS-COPILOT-BILLING.md`) | Intent-based billing model, model multipliers, and overage calculation |

---

## Key Findings Summary

### Cost Comparison (Actual Billing Data, 2026-03-04)

| Metric | Roo Code + OpenRouter | GitHub Copilot Pro+ |
|--------|----------------------|---------------------|
| Actual per-run cost | ~$100 | ~$0.48 |
| Monthly cost (38 runs) | ~$507 | $39 (flat, all within allowance) |
| Cost per run ratio | ~208x more expensive | 1x (baseline) |

### Quality Comparison (Copilot, 5 Scenarios)

| Scenario | Score | Max | Pct |
|----------|-------|-----|-----|
| SC-01 Ticket intake and classification | 23 | 25 | 92% |
| SC-02 Current state investigation | 33 | 35 | 94% |
| SC-03 Solution design creation | 30 | 30 | 100% |
| SC-04 Merge request review | 24 | 25 | 96% |
| SC-05 Publishing preparation | 39 | 40 | 98% |
| **Total** | **149** | **155** | **96.1%** |

### Vector DB / RAG Key Findings

| Question | Answer |
|----------|--------|
| Can a vector DB be built over the entire workspace? | Yes — technically feasible, 3-6 day build |
| Can Roo Code query it automatically? | Yes — via MCP server protocol |
| Can Kong AI Gateway serve as the vector DB? | No — Kong is an API gateway, not a retrieval engine |
| Does Copilot already do this? | Yes — `@workspace` semantic indexing is built in |
| Should a custom VS Code extension be built? | Not recommended — Continue.dev already provides this; thin wrapper is the pragmatic option |
| Does server-side chunking require check-in of every file? | No — local file watcher indexes on save, before any commit |

---

## Decision

See ADR-001: AI Toolchain Selection (`decisions/ADR-001-ai-toolchain-selection.md`) for the full decision record.

**Selected: GitHub Copilot Pro+** — 208x cheaper per run, 96.1% quality, built-in workspace semantic indexing via `@workspace`, zero retrieval infrastructure required.
