# Context Management

## How Context Handling Drives the 208x Cost Difference

The single largest factor in the cost difference between GitHub Copilot and Roo Code + OpenRouter is **how each platform handles context** -- the accumulated conversational state that the AI model needs to understand what it has already done and what it should do next.

---

## Two Architectural Approaches

### Copilot: Index Once, Retrieve On Demand

GitHub Copilot pre-indexes the entire workspace into a server-side vector database. When the AI needs context:

1. Searches the indexed content (semantic retrieval)
2. Pulls back only the most relevant snippets
3. Sends a small, curated context window to the model (typically under 5K tokens)
4. Charges the user once for the prompt

The indexing infrastructure cost is amortized across the entire user base through the $39/month subscription. The key insight: **static workspace context (specs, source code, ADRs) is indexed once and reused across all queries**, not retransmitted on every turn.

### OpenRouter: Retransmit Everything, Every Turn

When Roo Code operates an agentic loop through OpenRouter, it maintains the entire conversational state client-side. Every turn requires retransmitting the full history:

1. Turn 1: Send the initial prompt (~5K tokens)
2. Turn 2: Resend Turn 1 + Turn 1 response + new prompt (~15K tokens)
3. Turn 10: Resend all 9 prior turns + all responses (~50K tokens)
4. Turn 40: Resend all 39 prior turns + all responses (~180K tokens)

Each token is billed. There is no caching, no indexing, no amortization. The cost per turn grows quadratically with session length.

---

## Cost Accumulation Profile

| Turn | Copilot Cost (Cumulative) | OpenRouter Cost (Cumulative) |
|------|:---:|:---:|
| Turn 1 | $0.12 (1 prompt x 3x x $0.04) | ~$0.50 |
| Turn 10 | $0.12 (no additional prompts) | ~$5.00 |
| Turn 20 | $0.12 | ~$17.00 |
| Turn 30 | $0.12 | ~$40.00 |
| Turn 40 | $0.12 | ~$70.00 |
| Turn 50 | $0.12 | ~$100.00+ |

For Copilot, turns 2-50 are autonomous tool calls that cost nothing. For OpenRouter, each turn retransmits the full context history at per-token rates.

A typical architecture session involves 4 human prompts across 50 agent turns:

- **Copilot:** 4 x $0.12 = **$0.48**
- **OpenRouter:** ~**$100** (accumulated across 50+ turns)

---

## Context Summarization

### Copilot: Server-Side Compression

When the context window approaches the model's maximum, VS Code's Copilot extension triggers a context summarization protocol:

- Pauses to compress conversation history
- Substitutes verbatim logs with dense summaries
- Uses efficient routing models (zero-multiplier GPT-5 mini) for compression
- Summarization itself does not consume premium requests

**Trade-off:** Lossy compression may occasionally cause context drift or hallucination loops if critical nuances are lost during summarization.

### Roo Code: Client-Side Condensing

Roo Code implements "Intelligent Context Condensing" that monitors token consumption against a configurable threshold (default 80%):

- When `contextPercent >= effectiveThreshold`, the extension halts
- Dispatches a secondary prompt instructing the LLM to summarize the conversation
- Replaces the full history with the condensed version

**Vulnerability:** The condensing request itself may fail:

1. If it receives HTTP 429 (rate limit) from Kong, the session is paralyzed -- too bloated to continue, blocked from condensing
2. The condensing prompt itself consumes tokens, adding cost
3. If condensing fails silently, the next request hits the hard context ceiling, triggering `context_length_exceeded` -- which Kong then strips (see [Kong Failures](kong-failures.md))

---

## The Re-Transmission Tax

In pay-per-token models, every piece of static context (workspace instructions, file contents, prior decisions) is re-billed on every turn. For the NovaTrek workspace:

| Context Element | Size | Re-transmitted per Turn |
|----------------|------|------------------------|
| Copilot instructions | ~10K tokens | Yes (OpenRouter) / No (Copilot indexes) |
| OpenAPI spec content | ~5-20K tokens per file | Yes / No |
| Source code reads | ~2-10K tokens per file | Yes / No |
| Prior conversation | Grows per turn | Yes / No |
| Tool call results | ~1-5K tokens each | Yes / No |

In a 50-turn session, the copilot-instructions.md file alone is retransmitted ~50 times by OpenRouter -- billed at full rate each time. Copilot indexes it once and retrieves relevant snippets as needed.

---

## Implications for Tool Selection

### For Architecture Work (Long Sessions, Deep Context)

Architecture tasks typically involve:

- Reading multiple OpenAPI specs (19 services)
- Analyzing Java source code files
- Running mock tools and processing responses
- Creating multi-file solution designs
- Maintaining awareness of ADRs, capability maps, and domain rules

These sessions generate 40-60 agent turns with a large, growing context window. **Copilot's model is 100-200x cheaper** for this workload pattern.

### For Quick Queries (Short Sessions, Minimal Context)

Simple code generation tasks with 1-3 turns and minimal context history would cost fractions of a penny on OpenRouter. Copilot's per-prompt multiplier model may consume premium requests faster for high-volume, low-complexity queries.

### For Cost Transparency

OpenRouter provides exact per-generation costs. Copilot provides only daily aggregate premium request counts. If precise per-session cost tracking is a requirement, OpenRouter's transparency is unmatched -- but the cost of that transparency is 208x higher per session.

---

## Related Research

- [Copilot Billing Mechanics](copilot-billing.md) -- How intent-based billing works, model multipliers, quota mechanics
- [Kong AI Translation Failures](kong-failures.md) -- How the gateway compounds context problems by blocking error-driven context condensing
