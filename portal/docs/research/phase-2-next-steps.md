# Phase 2 Next Steps

| | |
|-----------|-------|
| **Author** | Christopher Blaisdell |
| **Date** | 2026-03-14 |
| **Status** | READY FOR DECISION |
| **Relates To** | ADR-001: AI Toolchain Selection (`decisions/ADR-001-ai-toolchain-selection.md`) |
| **Full Detail** | Full Next Steps Document (`research/PHASE-2-NEXT-STEPS.md`) |

---

## Where We Are

Phase 1 (AI Tool Cost Comparison) is complete.

| Finding | Evidence |
|---------|---------|
| GitHub Copilot (Claude Opus 4.6) scored 96.1% quality across all 5 scenarios | Phase 1 outputs |
| Roo Code + OpenRouter cost ~$100/run vs Copilot's ~$0.48/run | ADR-001 cost analysis |
| Copilot is ~208x cheaper per run and ~13x cheaper monthly | ADR-001 |
| Copilot has built-in workspace semantic search via `@workspace` | Deep Research: Copilot Billing |
| Kong AI Gateway cannot serve as a vector database | [Vector DB / RAG Feasibility Analysis](vector-db-rag-feasibility.md) |

**Phase 1 conclusion: GitHub Copilot Pro+ is the selected toolchain.**

---

## Decision Point

### Path A: Copilot-Only (No Build Required)

Copilot's `@workspace` already solves the workspace semantic search problem. For a single architect or small team all using Copilot, no additional infrastructure is needed.

**Next action:** Proceed to Phase 2 workflow tasks (AI instruction refinement, CI gates, solution design automation).

### Path B: MCP Vector Server + ChromaDB (3-6 Day Build)

If Roo Code remains in use or an on-premises, provider-agnostic semantic search layer is needed, build the MCP server. See [the implementation plan](vector-db-implementation-plan.md) for phases A through F.

**Next action:** Execute the implementation plan starting with Phase A (chunking pipeline).

---

## Chunking and Check-In: Clarification

> "If the chunking happens on a server, doesn't that mean that each architect must check in every single thing they want to chunk?"

No. The local file watcher (`watcher.py`) indexes files on every save — before any commit or check-in. Architects' working files are indexed in real time during editing.

CI-triggered indexing (on push to main) provides a shared team baseline but is supplementary, not the primary mechanism.

---

## Phase 2 Tasks (Independent of Vector DB Decision)

| Task | Priority |
|------|----------|
| AI instruction refinement (`.github/copilot-instructions.md`) | HIGH |
| Solution design automation (folder scaffolding script) | HIGH |
| CI validation gates (MADR format, OpenAPI spec, capability changelog) | HIGH |
| ADR promotion workflow (ticket-scoped → global `decisions/`) | MEDIUM |
| Capability rollup enforcement (required PR step) | MEDIUM |
| Continue.dev evaluation | LOW |

---

## Immediate Next Actions

1. **Decide Path A or Path B** — Is Roo Code still needed?
2. **Update ADR-001 status** from PROPOSED to ACCEPTED with Copilot as selected toolchain
3. **Begin Phase 2 tasks** listed above

---

## References

- Full Next Steps Document (`research/PHASE-2-NEXT-STEPS.md`)
- [Vector DB / RAG Feasibility Analysis](vector-db-rag-feasibility.md)
- [Workspace Vector DB Implementation Plan](vector-db-implementation-plan.md)
- ADR-001: AI Toolchain Selection (`decisions/ADR-001-ai-toolchain-selection.md`)
