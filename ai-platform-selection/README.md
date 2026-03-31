# AI Platform Selection — Complete Package

**Date**: 2026-03-31
**Status**: In Progress — Stakeholder Review Required
**Owner**: Architecture Practice

---

## Purpose

This package contains the complete body of work supporting the AI platform selection decision for the enterprise architecture practice. It includes the formal weighted scorecard, supporting research, tool evaluations, cost methodology, and customization guides.

The recommendation is a **staged approach**: start with GitHub Copilot Pro+ standalone (Option 1), evolve to Copilot + Azure MCP services (Option 2) when enterprise data needs are triggered, and eliminate the custom platform option (Option 3).

**This recommendation is unratified.** All weights and scores require stakeholder review. A validation POC phase (4-6 weeks) is required before the final decision.

---

## Document Map

### Strategic Documents (Start Here)

| Document | Description |
|----------|-------------|
| [AI Platform Selection Plan](strategic/AI-PLATFORM-SELECTION-PLAN.md) | **PRIMARY DOCUMENT** — Weighted scorecard with 3 options, 12 factors, preliminary scores, sensitivity analysis, staged recommendation, and POC validation plan |
| [AI Architecture Practice Decision Points](strategic/AI-ARCHITECTURE-PRACTICE-DECISION-POINTS.md) | Layer 2 operating model — 19 decision points spanning strategy, tooling, governance, knowledge, security, and workflow |
| [Strategic Realignment Research](strategic/STRATEGIC-REALIGNMENT-ENTERPRISE-AI-ARCHITECTURE-RESEARCH.md) | Deep technical analysis advocating the hybrid architecture (Copilot + Azure MCP). Foundation for the three solution options |

### Architecture Decision Records

| Document | Description |
|----------|-------------|
| [ADR-001: AI Toolchain Selection](decisions/ADR-001-ai-toolchain-selection.md) | ACCEPTED — Original decision to adopt GitHub Copilot Pro+. Will be amended or superseded by the platform selection outcome |

### Tool Evaluations and Comparisons

| Document | Description |
|----------|-------------|
| [Copilot vs OpenSpec Comparison](comparisons/COPILOT-VS-OPENSPEC-COMPARISON.md) | Feature-by-feature comparison of Copilot native customization vs OpenSpec framework |
| [Copilot vs Roo Code Comparison](comparisons/copilot-vs-roocode.md) | Run-by-run Phase 1 comparison across 5 architecture scenarios |
| [Evaluation Framework](comparisons/evaluation-framework.md) | Controlled evaluation methodology — same model, same workspace, same scenarios, single evaluator |
| [Run Analysis](comparisons/run-analysis.md) | Detailed per-run metrics, cost breakdowns, and quality assessments |
| [Decision Log](comparisons/decision-log.md) | Chronological decisions made during the Phase 1 evaluation |

### Customization Guides

| Document | Description |
|----------|-------------|
| [GitHub Copilot Customization Guide](guides/GITHUB-COPILOT-CUSTOMIZATION-GUIDE.md) | Comprehensive reference for all 6 Copilot customization primitives with real workspace examples |
| [OpenSpec Customization Guide](guides/OPENSPEC-CUSTOMIZATION-GUIDE.md) | Technical documentation of the OpenSpec v1.2.0 framework by Fission AI |

### Research

| Document | Description |
|----------|-------------|
| [Copilot Billing Analysis](research/DEEP-RESEARCH-RESULTS-COPILOT-BILLING.md) | Definitive analysis: Copilot bills per user prompt intention, not per model invocation. 39 cited sources |
| [Kong Tool Call Failures](research/DEEP-RESEARCH-RESULTS-KONG-TOOL-CALL-FAILURES.md) | Root cause analysis of systematic tool call failures in Roo Code + Kong AI Gateway |
| [Roo/Kong Failures Analysis](research/ROO-KONG-TOOL-CALL-FAILURES-ANALYSIS.md) | Supplementary failure pattern documentation from Phase 1 runs |
| [Context Window Utilization](research/CONTEXT-WINDOW-UTILIZATION-ANALYSIS.md) | How context windows are managed: Copilot (server-side RAG) vs OpenRouter (client-side re-submission) |
| [OpenSpec Analysis](research/OPENSPEC-ANALYSIS.md) | Technical capabilities and limitations of OpenSpec v1.2.0 |
| [Vector DB RAG Feasibility](research/VECTOR-DB-RAG-FEASIBILITY-ANALYSIS.md) | Feasibility of vector database + RAG for enterprise knowledge retrieval (relevant to Option 3) |
| [Comprehensive Comparison](research/DEEP-RESEARCH-RESULTS-COMPREHENSIVE-COMPARISON.md) | Cross-toolchain comparison covering all evaluated platforms |
| [Deep Research 1 — Token Economics](research/DEEP-RESEARCH-1.md) | Foundational: token economics, ReAct re-transmission tax, agentic patterns |
| [Deep Research 2 — Model Comparisons](research/DEEP-RESEARCH-2.md) | Foundational: comprehensive model comparisons informing Phase 1 cost methodology |

### Cost Methodology

| Document | Description |
|----------|-------------|
| [Cost Measurement Methodology](cost/COST-MEASUREMENT-METHODOLOGY.md) | How costs are measured: OpenRouter provides exact token data; Copilot provides none (intent-based billing) |
| [AI Tool Cost Comparison Plan](cost/AI-TOOL-COST-COMPARISON-PLAN.md) | Phase 1 project plan: 5 synthetic scenarios, cost per architect seat |
| [sensitivity-analysis.py](cost/sensitivity-analysis.py) | Python script computing weighted score sensitivity across 5 scenarios |

### Tool Profiles

| Document | Description |
|----------|-------------|
| [GitHub Copilot](tool-profiles/github-copilot.md) | Capabilities, pricing, and feature profile |
| [Roo Code + Kong AI](tool-profiles/roo-code-kong.md) | Architecture, capabilities, and evaluation findings |
| [Claude Code](tool-profiles/claude-code.md) | Anthropic's CLI assistant — capabilities and comparison reference |

### Data Isolation

| Document | Description |
|----------|-------------|
| [Data Isolation Statement](data-isolation/data-isolation.md) | Confirms all evaluation data is synthetic (NovaTrek Adventures). Zero corporate data exposure |

---

## Reading Order

For stakeholders reviewing this package, the recommended reading order is:

1. **AI Platform Selection Plan** (strategic/) — the primary decision document
2. **ADR-001** (decisions/) — the existing accepted decision this work extends
3. **Strategic Realignment Research** (strategic/) — the analysis that motivated the three options
4. **Copilot vs Roo Code Comparison** (comparisons/) — Phase 1 empirical results
5. **Copilot Billing Analysis** (research/) — critical cost model finding
6. Everything else as reference material

---

## Confluence Publishing Notes

This package is designed for import into a Confluence space. Suggested page hierarchy:

```
AI Platform Selection (parent page — use this README)
├── Strategic Documents
│   ├── AI Platform Selection Plan
│   ├── AI Architecture Practice Decision Points
│   └── Strategic Realignment Research
├── Architecture Decisions
│   └── ADR-001 AI Toolchain Selection
├── Tool Evaluations
│   ├── Copilot vs OpenSpec Comparison
│   ├── Copilot vs Roo Code Comparison
│   ├── Evaluation Framework
│   ├── Run Analysis
│   └── Decision Log
├── Customization Guides
│   ├── GitHub Copilot Customization Guide
│   └── OpenSpec Customization Guide
├── Research
│   ├── Copilot Billing Analysis
│   ├── Kong Tool Call Failures
│   ├── Context Window Utilization
│   ├── OpenSpec Analysis
│   ├── Vector DB RAG Feasibility
│   ├── Comprehensive Comparison
│   └── Foundational Research (Deep Research 1 & 2)
├── Cost Methodology
│   ├── Cost Measurement Methodology
│   └── AI Tool Cost Comparison Plan
├── Tool Profiles
│   ├── GitHub Copilot
│   ├── Roo Code + Kong AI
│   └── Claude Code
└── Data Isolation Statement
```

---

## File Inventory

**28 documents** across 8 categories:

| Category | Count |
|----------|-------|
| Strategic Documents | 3 |
| Architecture Decisions | 1 |
| Comparisons | 5 |
| Customization Guides | 2 |
| Research | 9 |
| Cost Methodology | 3 (2 docs + 1 script) |
| Tool Profiles | 3 |
| Data Isolation | 1 |
| **Total** | **28** |
