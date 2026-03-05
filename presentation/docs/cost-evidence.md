# Cost Evidence: The 208x Difference

## Same Model. Same Workspace. Same Scenarios. Radically Different Cost.

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

<div class="big-number">208x</div>

**cheaper per run** — $0.48 vs ~$100, using the same underlying AI model.

---

## Why the Difference Is So Large

### Copilot Bills Per User Prompt — Not Per Token

This was the key discovery from our deep research into GitHub's billing model:

| What gets billed | Copilot | OpenRouter |
|-----------------|---------|------------|
| User typing a prompt | 1 premium request (3x multiplier for Claude) | Tokens billed |
| AI reading a file | **Free** | Tokens billed |
| AI running a terminal command | **Free** | Tokens billed |
| AI spawning a sub-agent | **Free** | Tokens billed |
| AI analyzing search results | **Free** | Tokens billed |
| Context re-transmission per turn | **Free** (server-side) | Tokens billed |

A typical 4-prompt architecture session on Copilot:

> 4 prompts x 3 (Claude multiplier) x $0.04 = **$0.48**

The same session on OpenRouter bills for every token in every tool call, file read, terminal command, and context re-transmission — which compounds quadratically as the conversation gets longer.

---

## The Context Re-Transmission Tax

Per-token models have a hidden cost multiplier: **context re-transmission**.

Every time the AI takes a turn in a conversation, the entire conversation history must be re-sent to the model. As a session progresses:

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
**The cost advantage is not close.** At any realistic usage volume, Copilot Pro+ is between 3x and 34x cheaper than per-token alternatives — and that's before accounting for infrastructure overhead, monitoring, and the risk of runaway costs on complex sessions.
</div>

<div class="cta-box" markdown>

### But is the quality comparable?

[Quality Evidence: 96.1% on First Execution](quality-evidence.md)

</div>
