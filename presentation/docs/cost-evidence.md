# Cost Evidence: Toolchain Comparison

## Same Model. Same Workspace. Same Scenarios. Materially Different Cost.

We ran the **exact same 5 architecture scenarios** against the **exact same workspace** using **two competing AI toolchains** — both backed by Claude Opus 4.6. The cost difference is not theoretical. It comes from actual billing data.

---

## The Head-to-Head Comparison

| | GitHub Copilot Pro+ | Roo Code + OpenRouter |
|---|:---:|:---:|
| **AI Model** | Claude Opus 4.6 | Claude Opus 4.6 |
| **Cost per run** | **$0.48** | ~$100 |
| **Monthly (38 runs)** | **$39** (fixed) | ~$507 (variable) |
| **Pricing model** | Fixed subscription | Pay-per-token |
| **Cost at 50 runs** | **$39** | ~$667 |
| **Cost at 100 runs** | **$39** | ~$1,334 |
| **Infrastructure** | None (SaaS) | Kong Gateway + vector DB |

The per-run cost difference is significant: $0.48 vs ~$100, using the same underlying AI model.

---

## Why the Difference Is So Large

### The Architectural Difference: RAG vs Long Context

**This is the biggest reason for the 208x cost difference.**

There are two fundamental approaches to giving an LLM access to a large knowledge base:

**RAG (Retrieval-Augmented Generation)** pre-indexes documents into a vector database. When a query arrives, it retrieves only the relevant snippets — the model sees a small, curated context window. Indexing cost is paid once and amortized across all future queries.

**Long Context** skips the index. With models that support very large context windows (100K–1M+ tokens), documents can be loaded directly into the prompt so the model's attention mechanism finds what it needs in a single pass. The model re-processes the same material from scratch each time. There is no amortization — you pay for everything, every turn.

GitHub Copilot and OpenRouter represent these two approaches directly:

| | GitHub Copilot | OpenRouter |
|---|:---:|:---:|
| **Architecture** | RAG — pre-indexes workspace (vector database + semantic retrieval) | Long Context — token-by-token, full re-transmission each turn |
| **Static Context Handling** | Indexed once, reused across all queries | Recalculated and billed on every request |
| **Cost Model** | Fixed subscription (amortizes indexing cost) | Pay-per-token (includes all recalculation) |
| **What You Pay For** | User query that searches the index | Every single token for every single request |

**Copilot's approach:**

GitHub maintains a vector database index of your entire workspace — your specs, source code, decision history, standards. When you ask a question, Copilot:
1. Searches the indexed content (semantic retrieval)
2. Pulls back only the most relevant snippets
3. Sends a small, curated context window to Claude Opus (typically under 5K tokens)
4. Charges you **once** for your user query

The indexing infrastructure cost is amortized across the entire user base through the $39/month subscription.

**OpenRouter's approach:**

Every time you run an architecture session, OpenRouter:
1. Re-calculates which context is relevant (no persistent index)
2. Sends **all relevant context** to Claude Opus on every turn
3. Bills you for **every token** in every direction
4. Charges you again for the full context on turn 2, turn 3, turn 4...

There's no amortization. No indexing. Each request starts from zero and includes all context recalculation costs.

---

### Three Structural Advantages of RAG — Three Copilot Wins

**Compute efficiency.** Long Context requires the model to re-process the same documents on every query turn. In a 20-turn architecture session at 150K tokens per turn, that is 3 million tokens billed for the same workspace context. RAG pays this cost once at indexing time. This single difference explains most of the session cost gap: $0.48 (Copilot) vs ~$100 (OpenRouter).

**No retrieval lottery.** The risk of Long Context is that even though everything is in the window, the model's attention can miss specific facts buried in a large context — particularly for questions that require comparing two documents or identifying gaps between them. Copilot's semantic retrieval is targeted: it pulls the specific specs and solution designs relevant to each query. In the head-to-head comparison, Copilot retrieved the approved solution design and applied only the specified changes; Roo Code's session did not have the right context and fabricated four OpenAPI fields that were not in the approved design.

**Scales to enterprise datasets.** A context window of 1 million tokens is roughly 700,000 words — impressive, but still a fraction of an enterprise knowledge base measured in terabytes. Copilot's indexed approach is the only architecture that scales to the full workspace as it grows. Roo Code's manual file selection approach requires the architect to anticipate which files the AI will need, every session.

---

### Why This Matters

In our 5-scenario POC, architects ran multi-turn sessions (4-20 turns per scenario). With OpenRouter's per-token approach:

- Turn 1: Full workspace context billed
- Turn 2: Full workspace context + accumulated conversation billed again
- Turn 3-20: Same context re-billed, growing context window, quadratic cost

With Copilot's indexed approach, that entire session is one or two queries against a pre-indexed database.

### The Billing Model: Intent-Based vs Token-Based

The architectural difference enables a different billing model:
| | Copilot | OpenRouter |
|---|:---:|:---:|
| **User types a prompt** | 1 premium request (fixed per query) | Tokens billed |
| **AI reads a file from the indexed workspace** | Included in query cost | Tokens billed |
| **AI running a terminal command** | Included in query cost | Tokens billed |
| **AI spawning a sub-agent** | Included in query cost | Tokens billed |
| **AI analyzing search results** | Included in query cost | Tokens billed |
| **Context re-transmission per turn** | Included (server-side semantic retrieval) | Tokens billed |

A typical 4-prompt architecture session on Copilot (4 queries to the indexed database):

> 4 prompts x 3 (Claude multiplier) x $0.04 = **$0.48**

The same session on OpenRouter recalculates context on every turn and bills every token. Context grows quadratically as the session progresses — a 4-turn session can easily generate 50K-100K tokens.

---

## Why Indexing Matters: The Context Cost Explosion

Without workspace indexing (OpenRouter's model), context costs explode as sessions get longer:

With indexed context (Copilot's model), semantic retrieval keeps context bounded regardless of session length:

| Turn | Context Size (OpenRouter) | Context Size (Copilot) |
|------|--------------------------|----------------------|
| Turn 1 | ~5K tokens | ~5K tokens |
| Turn 5 | ~50K tokens | ~5K tokens |
| Turn 10 | ~120K tokens | ~5K tokens |
| Turn 20 | ~180K tokens | ~5K tokens |

Copilot uses **server-side semantic retrieval** — it selects only the most relevant context for each turn, keeping context bounded at roughly 5K tokens regardless of session length.

OpenRouter re-transmits the **full conversation history** on every turn, meaning you pay for the same tokens over and over — and the cost per turn grows as the session gets longer.

!!! info "Measured Overhead"
    Our context window analysis found that Roo Code broadcasts **81 environment metadata blocks** consuming **1,885 lines** across a typical task — **16.3% of context** wasted on metadata the model doesn't need.

---

## Monthly Cost Projection

At the architecture practice's projected workload (38 runs/month — 26 base scenarios + 12 PROMOTE steps):

| Runs/Month | Copilot Pro+ | OpenRouter | Copilot Advantage |
|-----------|:---:|:---:|:---:|
| 10 | $39 | ~$133 | 3.4x |
| 20 | $39 | ~$267 | 6.8x |
| 38 | $39 | ~$507 | **13x** |
| 50 | $39 | ~$667 | **17x** |
| 100 | $39 | ~$1,334 | **34x** |

Copilot's cost line is **flat** regardless of volume. OpenRouter's grows linearly — and that's the optimistic case, ignoring the quadratic context re-transmission within each session.

---

## Budget Predictability

| Risk | Copilot | OpenRouter |
|------|---------|------------|
| Monthly budget | $39 (known, fixed) | Variable (depends on usage) |
| Runaway costs | Impossible | Possible (long sessions, complex scenarios) |
| Budget approval | Single line item | Requires usage monitoring and alerts |
| Cost per new architect | +$39/month | +$133-667/month (depends on workload) |
| Infrastructure costs | $0 | Kong Gateway + Qdrant + monitoring (unquantified) |

<div class="key-insight" markdown>
At projected usage volumes, the fixed-subscription model is consistently less expensive than per-token alternatives. The gap widens with usage, and does not account for infrastructure overhead (Kong Gateway, Qdrant, monitoring) required by the per-token stack.
</div>

<div class="cta-box" markdown>

### What did the AI actually produce?

[Output Analysis: What Was Produced in 5 Scenarios](quality-evidence.md)

</div>
