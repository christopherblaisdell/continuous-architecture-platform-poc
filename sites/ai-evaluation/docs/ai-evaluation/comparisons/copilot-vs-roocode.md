<!-- CONFLUENCE-PUBLISH -->

# Copilot vs Roo Code

## Head-to-Head Comparison

Both toolchains used the same AI model (Claude Opus 4.6), the same synthetic workspace (NovaTrek Adventures), and the same 5 architecture scenarios. The differences in cost and reliability come down to **architecture** -- how each platform handles billing, context, and API translation.

---

## Cost Comparison

| | GitHub Copilot Pro+ | Roo Code + OpenRouter |
|---|:---:|:---:|
| **AI Model** | Claude Opus 4.6 | Claude Opus 4.6 |
| **Cost per run** | **$0.48** | ~$100 |
| **Monthly (38 runs)** | **$39** (fixed) | ~$507 (variable) |
| **Pricing model** | Fixed subscription | Pay-per-token |
| **Cost at 50 runs** | **$39** | ~$667 |
| **Cost at 100 runs** | **$39** | ~$1,334 |
| **Infrastructure** | None (SaaS) | Kong Gateway + vector DB |
| **Per-run cost ratio** | **1x** | ~208x |

### Why the 208x Difference

The cost difference is not a pricing promotion or temporary discount. It is a fundamental architectural divergence:

**Copilot indexes once, retrieves on demand.** GitHub maintains a vector database index of the entire workspace. When the AI needs context, it performs semantic retrieval and sends a small, curated context window to the model. The indexing cost is amortized across the user base through the $39/month subscription.

**OpenRouter recalculates from scratch every turn.** Each turn requires retransmitting the full conversational history. By turn 40, the model receives ~180K tokens of accumulated context just to remember what it did in turns 1-39. Every token is billed.

Additionally, Copilot bills per user prompt (4 prompts = $0.48), while OpenRouter bills per token (hundreds of thousands of tokens per session = ~$100).

### Billing Evidence (March 4, 2026)

**OpenRouter:** 4 auto-top-up charges of $25 each between 10:11 AM and 10:37 AM = $100 consumed in 26 minutes.

**Copilot:** 120 premium requests at $0.04 each = $4.80 notional for the entire day across all projects. The architecture session consumed 12 of those requests ($0.48). $0 overage charged.

---

## Quality Comparison

### Copilot Quality Scores (Run 001)

| Scenario | Score | Max | Percentage |
|----------|-------|-----|-----------|
| SC-01: Ticket Triage | 23 | 25 | 92% |
| SC-02: Solution Design | 33 | 35 | 94% |
| SC-03: Investigation | 30 | 30 | 100% |
| SC-04: Architecture Update | 24 | 25 | 96% |
| SC-05: Publishing Prep | 39 | 40 | 98% |
| **Total** | **149** | **155** | **96.1%** |

### Roo Code Quality Scores

Pending human evaluation using the same rubrics.

---

## Execution Metrics (Run 002)

| Metric | Copilot | Roo Code |
|--------|:---:|:---:|
| Scenarios completed | 5/5 | 5/5 |
| Files created | 37 | 37 |
| Mock script executions | 5 | 4 |
| Workspace file reads | ~35 | 22 |
| Terminal commands | 8 | 5 |
| Issues or retries | 2 | 1 |

Both platforms completed all scenarios and produced comparable file structures. The differences are in approach, not completion.

---

## Per-Scenario Comparison

### SC-01: Ticket Triage (NTK-10005)

| Aspect | Copilot | Roo Code |
|--------|---------|---------|
| Files created | 8 | 8 |
| User stories | 4 | 5 |
| RFID format discrepancy flagged | Not reported | Yes |

### SC-02: Solution Design (NTK-10002)

| Aspect | Copilot | Roo Code |
|--------|---------|---------|
| Files created | 8 | 8 |
| ADRs created | 3 (MADR format) | 3 (MADR format) |
| Safety gap (Pattern 1 default) | Correctly flagged | Correctly flagged |
| ActivityType naming discrepancy | Not flagged | Flagged |
| Assumptions documented | 8 | 8 |
| Risks documented | 5 | 5 |

Both platforms correctly identified the critical safety issue: unknown adventure categories defaulting to Pattern 1 (Basic) instead of Pattern 3 (Full Service). This is a safety requirement documented in ADR-005.

### SC-03: Investigation (NTK-10004)

| Aspect | Copilot | Roo Code |
|--------|---------|---------|
| Files created | 7 | 7 |
| Root cause | Correct (boundary violation + PUT semantics) | Correct (boundary violation + PUT semantics) |
| ADRs created | 2 (PATCH semantics, optimistic locking) | 2 (PATCH semantics, optimistic locking) |
| Elastic log evidence | 4 ERROR entries with trace IDs | 4 ERROR entries with trace IDs |
| Concurrent race window | 47ms for G-4821 | 47ms for G-4821 |

Both platforms independently identified the same root cause, the same evidence, and the same race window. This convergence suggests the findings are grounded in workspace evidence rather than model-dependent reasoning.

### SC-04: Architecture Update (NTK-10001)

| Aspect | Copilot | Roo Code |
|--------|---------|---------|
| Files created | 3 | 3 |
| Version bump | 1.1.0 -> 1.2.0 | 1.1.0 -> 1.2.0 |
| Fields added | 2 (per solution design) | 5 (per prompt instructions) |
| Scope discipline | Strict -- rejected 3 extra fields as scope creep | Loose -- added all fields from prompt |

**Key difference:** Copilot limited elevation field changes to the 2 fields specified in the approved solution design, explicitly rejecting the 5 fields suggested in the execution prompt as scope creep. Roo Code added all fields from the prompt instructions regardless of the solution design scope.

### SC-05: Publishing Preparation

| Aspect | Copilot | Roo Code |
|--------|---------|---------|
| Files created | 11 | 10 |
| Component diagram | Yes (C4 PlantUML) | Yes (C4 PlantUML) |
| Sequence diagram | Yes (PlantUML) | Yes (PlantUML) |
| ADRs | 4 | 4 |
| Impact assessments | 4 | 4 |
| Source code gap analysis | **Yes** (4 specific gaps identified) | Not performed |

Copilot performed deeper source code analysis in SC-05, reading `CheckInController.java` and `GuestService.java` to identify 4 specific implementation gaps (Map<String,String> stub, email dedup requirement, guest_id waiver lookup, missing confirmation_code).

---

## Architecture Reliability

### Copilot

- Server-side workspace indexing -- no manual file selection
- Context summarization handled server-side
- No gateway translation layer -- direct model access via GitHub infrastructure
- No infinite retry vulnerability

### Roo Code + Kong

- No built-in workspace indexing -- requires Qdrant + embedding provider
- Client-side context accumulation causes exponential cost growth
- Kong AI gateway drops tool calls, obfuscates errors, truncates streams
- Infinite retry loop vulnerability with no circuit breaker
- Context condensing blocked by rate limiting race condition

See [Kong AI Translation Failures](../research/kong-failures.md) for the full technical analysis.

---

## Cost Efficiency

| Metric | Copilot | Roo Code |
|--------|:---:|:---:|
| Cost per file created | ~$0.013 | ~$2.70 |
| Cost per scenario | ~$0.10 | ~$20.00 |
| Cost per quality point | $0.26 (at $39/month) | TBD |

---

## Summary

GitHub Copilot is the clear winner on cost (208x cheaper per run) and demonstrated 96.1% quality in the evaluation. Roo Code provides better cost transparency and model flexibility, but the Kong AI gateway introduces three cascading architectural failures that undermine reliability in agentic workflows with complex tool calls.

The cost gap is architectural and will persist regardless of pricing changes: intent-based billing with server-side indexing (Copilot) is fundamentally cheaper for agentic workflows than token-based billing with client-side context accumulation (OpenRouter).
