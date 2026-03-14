# Phase 2 Next Steps: AI Workflow Enhancement

| | |
|-----------|-------|
| **Author** | Christopher Blaisdell |
| **Date** | 2026-03-14 |
| **Status** | READY FOR DECISION |
| **Relates To** | [ADR-001: AI Toolchain Selection](../decisions/ADR-001-ai-toolchain-selection.md) |
| **Preceding** | [Vector DB / RAG Feasibility Analysis](VECTOR-DB-RAG-FEASIBILITY-ANALYSIS.md) |
| **Implementation Detail** | [Workspace Vector DB Implementation Plan](WORKSPACE-VECTOR-DB-KONG-AI-IMPLEMENTATION-PLAN.md) |

---

## Where We Are

Phase 1 (AI Tool Cost Comparison) is complete. The key findings:

| Finding | Evidence |
|---------|---------|
| GitHub Copilot (Claude Opus 4.6) scored 96.1% quality across all 5 scenarios | `phases/phase-1-ai-tool-cost-comparison/outputs/copilot/` |
| Roo Code + OpenRouter cost ~$100/run vs Copilot's ~$0.48/run | ADR-001, OpenRouter billing receipts |
| Copilot is ~208x cheaper per run and ~13x cheaper monthly | ADR-001 cost analysis |
| Copilot has built-in workspace semantic search via `@workspace` | Deep Research: Copilot Billing |
| Roo Code lacks native workspace indexing — relies on file reads that fill the context window | Context Window Utilization Analysis |
| Kong AI Gateway cannot serve as a vector database or retrieval engine | Vector DB / RAG Feasibility Analysis |

**Phase 1 conclusion: GitHub Copilot Pro+ is the primary AI assistant for the architecture practice.**

---

## The Open Question

During Phase 1, the following question was raised and investigated:

> "Is it possible to create a vector database out of EVERYTHING in the VS Code solution and give Roo Code access to query it automatically?"

This led to a full feasibility analysis and implementation plan. The answer is: **yes, it is technically feasible**, and a complete plan exists. But before building it, the practice must decide whether it needs it.

---

## Decision Point: Build the MCP Vector Server?

Two paths forward exist.

### Path A: Copilot-Only (No Build Required)

**Rationale:** Copilot's `@workspace` semantic indexing already solves the problem. It indexes the entire repository server-side, supports semantic queries, manages context budgets automatically, and costs nothing beyond the subscription.

**When this is the right choice:**

- The practice is a single architect or a small team all using Copilot
- There is no requirement to use Roo Code for any scenario
- The practice can accept GitHub's proprietary indexing (no on-premises requirement)
- Quality bar is met: 96.1% quality was demonstrated with zero additional retrieval infrastructure

**Next action:** No new infrastructure. Proceed to Phase 2 workflow enhancement (improving AI instructions, adding CI gates, solution design automation).

### Path B: MCP Vector Server + ChromaDB (3-6 Day Build)

**Rationale:** If Roo Code is still needed (e.g., for cost scenarios, model flexibility, or specific use cases), or if the practice wants an on-premises, provider-agnostic semantic search layer, build the MCP server described in the implementation plan.

**When this is the right choice:**

- Roo Code is still used for specific tasks alongside Copilot
- The practice wants a retrieval layer that works with any AI assistant, not just Copilot
- A local, auditable index is required for compliance or air-gapped environments
- The team wants to demonstrate the MCP + RAG pattern as a reference architecture

**Next action:** Execute the [implementation plan](WORKSPACE-VECTOR-DB-KONG-AI-IMPLEMENTATION-PLAN.md) phases A through E (and optionally F for the VS Code extension wrapper).

### Addressing the "Server Chunking" Concern

During the Phase 1 conversation, this concern was raised:

> "If the chunking happens on a server, doesn't that mean that each architect must check in every single thing they want to chunk?"

This is a valid practical concern. The implementation plan addresses it in two ways:

**Option 1 (Local watcher — recommended):** The chunking pipeline runs locally on each architect's machine via `scripts/vector-db/watcher.py`. It watches the filesystem for changes and re-indexes on every file save — **no check-in required**. Any file the architect is editing is indexed in real time, regardless of whether it has been committed.

**Option 2 (CI-triggered indexing):** A GitHub Actions workflow triggers re-indexing on push to main. This does require a check-in, but it provides a shared team index that all architects benefit from. Suitable as a supplement to local indexing, not a replacement.

**Recommended approach:** Local watcher for day-to-day work (indexes immediately on save), CI indexing for publishing the shared team baseline.

### VS Code Plugin: Should It Be Built?

The feasibility analysis and implementation plan both address this. The short answer:

| Scenario | Recommendation | Reason |
|----------|---------------|--------|
| Solo architect wanting RAG now | Python scripts from the plan | Working in days, not weeks |
| Solo architect who wants polish | Install Continue.dev | Zero development, built-in `@codebase` |
| Team of 3-5 architects | Python scripts + thin extension wrapper | Auto-start eliminates "forgot to run the watcher" failure mode |
| Product for broad distribution | Full VS Code extension | Only if packaging for users who cannot run Python |

Building a full VS Code extension from scratch is NOT recommended because Continue.dev already IS this extension — open source, local-first, with built-in codebase indexing. Building a custom extension duplicates their work.

If a lightweight VS Code integration is wanted, the plan proposes a **thin wrapper extension** (~200 lines TypeScript) that calls the existing Python scripts — auto-starting the watcher on workspace open, showing chunk count in the status bar, and adding a command palette entry for full re-index.

---

## Phase 2 Scope (Regardless of Path)

The following Phase 2 tasks proceed independently of the vector DB decision:

| Task | Description | Priority |
|------|-------------|----------|
| AI instruction refinement | Improve `.github/copilot-instructions.md` based on Phase 1 quality observations | HIGH |
| Solution design automation | Scaffold solution folder structure via script or Copilot agent | HIGH |
| CI validation gates | Validate MADR format, OpenAPI spec changes, and capability changelog on PR | HIGH |
| ADR promotion workflow | Automate promotion of ticket-scoped ADRs to `decisions/` on merge | MEDIUM |
| Capability rollup enforcement | Make `capability-changelog.yaml` update a required PR step | MEDIUM |
| Continue.dev evaluation | Install and evaluate Continue.dev `@codebase` as a Copilot complement | LOW |

---

## Immediate Next Actions

1. **Decide on Path A or Path B** — Answer: does the practice need Roo Code + MCP vector server, or is Copilot sufficient?
2. **If Path A:** Close the vector DB investigation and proceed to Phase 2 task list above
3. **If Path B:** Assign 3-6 days to execute [the implementation plan](WORKSPACE-VECTOR-DB-KONG-AI-IMPLEMENTATION-PLAN.md) starting with Phase A (chunking pipeline) and Phase B (ChromaDB setup)
4. **Regardless of path:** Update ADR-001 status from PROPOSED to ACCEPTED, with Copilot as the selected toolchain

---

## References

- [Vector DB / RAG Feasibility Analysis](VECTOR-DB-RAG-FEASIBILITY-ANALYSIS.md)
- [Workspace Vector DB Implementation Plan](WORKSPACE-VECTOR-DB-KONG-AI-IMPLEMENTATION-PLAN.md)
- [ADR-001: AI Toolchain Selection](../decisions/ADR-001-ai-toolchain-selection.md)
- [Context Window Utilization Analysis](CONTEXT-WINDOW-UTILIZATION-ANALYSIS.md)
- [Deep Research: Copilot vs Kong+Roo Economics](DEEP-RESEARCH-1.md)
- [Deep Research: Copilot Billing](DEEP-RESEARCH-RESULTS-COPILOT-BILLING.md)
