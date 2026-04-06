<!-- CONFLUENCE-PUBLISH -->

# Run Analysis

## Cross-Platform Run Comparison Details

This page summarizes the detailed execution data from individual runs, providing the evidence base for the [Copilot vs Roo Code](copilot-vs-roocode.md) comparison.

---

## Run Inventory

| Run | Tool | Date | Scenarios | Files Created | Session Cost |
|-----|------|------|-----------|---------------|-------------|
| Copilot 001 | GitHub Copilot Pro+ | March 2026 | 5/5 | 37 | $0.48 |
| Copilot 002 | GitHub Copilot Pro+ | March 4, 2026 | 5/5 | 37 | $0.48 |
| Roo Code 001 | Roo Code + OpenRouter | March 3, 2026 | 5/5 | 37 | ~$75 |
| Roo Code 002 | Roo Code + OpenRouter | March 4, 2026 | 5/5 | 38 | ~$100 |

---

## Copilot Run 002 -- Detailed Metrics

### Execution Summary

| Metric | Value |
|--------|-------|
| Model | Claude Opus 4.6 (standard, 3x multiplier) |
| User prompts | 4 |
| Files created | 37 |
| Mock script executions | 5 |
| Workspace file reads | ~35 |
| Terminal commands | 8 |
| Scenarios completed | 5/5 |
| Issues/retries | 2 (GitLab mock args + cwd issue) |

### Billing

| Metric | Value |
|--------|-------|
| Premium requests consumed | 12 (4 prompts x 3x) |
| Notional cost | $0.48 |
| Day total (all projects) | 120 requests ($4.80) |
| Overage | $0 |

### Quality Scores (Run 001)

| Scenario | Score | Max | Notes |
|----------|-------|-----|-------|
| SC-01 | 23 | 25 | Correct classification, 4 user stories |
| SC-02 | 33 | 35 | 3 MADR ADRs, safety gap flagged |
| SC-03 | 30 | 30 | Perfect: boundary violation + PUT + 47ms race |
| SC-04 | 24 | 25 | Scope discipline: 2 fields only |
| SC-05 | 39 | 40 | 4 source code gaps identified |
| **Total** | **149** | **155** | **96.1%** |

---

## Roo Code Run 002 -- Detailed Metrics

### Execution Summary

| Metric | Value |
|--------|-------|
| Model | Claude Opus 4.6 (full) |
| Model turns | 65 |
| Files created/modified | 38 |
| Mock script executions | 4 |
| Total tool calls | 66 |
| Wall-clock time | ~31 minutes (10:05 AM - 10:36 AM EST) |
| Scenarios completed | 5/5 |
| Issues/retries | 1 (GitLab mock args) |

### Billing

| Metric | Value |
|--------|-------|
| Cost model | OpenRouter pay-per-token |
| Auto-top-ups | 4 x $25 (10:11 AM - 10:37 AM) |
| Session cost | ~$100 |
| Session cost indicator | $175.77 (includes post-run analysis) |

### Quality Scores

Pending human evaluation.

---

## Convergent Findings

Both platforms independently produced identical or near-identical findings in several scenarios, suggesting the results are grounded in workspace evidence rather than model-dependent reasoning:

### SC-03: Root Cause Convergence

Both platforms identified:

- **Root cause:** Architectural boundary violation -- `svc-scheduling-orchestrator` using PUT semantics to overwrite fields owned by other services
- **Evidence:** 4 ERROR log entries in Elasticsearch with identical trace IDs
- **Race condition:** 47ms concurrent modification window for guest G-4821
- **Proposed fixes:** PATCH semantics (ADR-010) and optimistic locking (ADR-011)

### SC-02: Safety Gap Convergence

Both platforms identified that the adventure classification engine defaults unknown categories to Pattern 1 (Basic) instead of Pattern 3 (Full Service), violating ADR-005's safety requirement.

### SC-05: Source Code Gap Divergence

Only Copilot identified 4 specific source code gaps by reading `CheckInController.java` and `GuestService.java`:

1. `Map<String,String>` stub in check-in controller
2. Email deduplication requirement in guest service
3. `guest_id` waiver lookup pattern
4. Missing `confirmation_code` in reservation response

Roo Code did not perform this source code analysis in its SC-05 execution.

---

## Cost per Output Unit

| Unit | Copilot ($0.48/run) | Roo Code (~$100/run) | Ratio |
|------|:---:|:---:|:---:|
| Per file | $0.013 | $2.70 | 208x |
| Per scenario | $0.10 | $20.00 | 200x |
| Per mock tool call | $0.10 | $25.00 | 250x |
| Per quality point | $0.26/month | TBD | TBD |

---

## Methodology Notes

### What These Costs Include

- **Copilot:** Only user prompts are billed. File reads, terminal commands, sub-agents, and context summarization are free.
- **OpenRouter:** Every token in both directions is billed. Context retransmission on each turn is the primary cost driver.

### What These Costs Exclude

- **Copilot:** The $39/month subscription base (covers ~125 runs at current multiplier)
- **OpenRouter:** Any non-run API usage (testing, debugging, experimentation)

### Data Sources

- Copilot billing: GitHub Billing dashboard, daily premium request totals
- OpenRouter billing: Auto-top-up transaction records, OpenRouter activity dashboard
- File counts: `ls` enumeration of run output directories
- Quality scores: Human architect evaluation using scenario rubrics
