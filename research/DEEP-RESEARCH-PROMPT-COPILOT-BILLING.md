# Deep Research Prompt: GitHub Copilot Premium Request Billing Mechanics

## Research Objective

I need a comprehensive, technically precise understanding of how GitHub Copilot bills premium requests in Agent Mode, specifically for cost measurement in an AI toolchain comparison study. I am comparing GitHub Copilot (Pro+ subscription, $39/month) against Roo Code with OpenRouter (pay-per-token) by running identical architecture scenarios and measuring cost, quality, and effort.

OpenRouter provides exact per-request token counts and costs via API. GitHub Copilot does not. This asymmetry is the core problem I need to solve.

---

## My Exact Setup

- **Subscription**: GitHub Copilot Pro+ ($39/month, 1,500 included premium requests/month)
- **IDE**: VS Code (multiple instances open simultaneously on different projects)
- **Mode**: Agent Mode (the AI autonomously calls tools — file reads, terminal commands, file edits, searches, sub-agents — in a loop until done)
- **Model**: The model selector shows "Claude Opus 4.6" but the system prompt identifies the model as "Claude Opus 4.6 fast (preview)"
- **Date**: March 2026

### Observed Billing Data

On one specific day (March 4, 2026), I used Copilot extensively across multiple projects and VS Code instances. My GitHub billing dashboard for that day showed:

```
Copilot Premium Request
78 requests
$0.04
$3.12
$0
```

Interpretation: 78 premium requests at $0.04 each = $3.12 total, $0 overage (within the 1,500/month included allowance).

### The Specific Agent Mode Session

One of those sessions was a single-prompt Agent Mode interaction where:
- I pasted a long execution prompt (approximately 400 lines of instructions)
- The agent autonomously executed 5 complex architecture scenarios
- The agent made approximately 35+ workspace file reads, 37 file creates, 8 terminal commands, 6 sub-agent invocations, and multiple search operations
- The session involved at least one context summarization (the context window filled up and was compressed mid-session)
- The session lasted several hours wall-clock time
- I typed exactly 1 user prompt to start, then 3 short follow-up prompts after the main work completed

---

## Specific Questions to Research

### 1. What Exactly Counts as a "Premium Request" in Agent Mode?

When Copilot Agent Mode is running autonomously (the user typed one prompt, and the agent is iterating through tool calls), what constitutes a single "premium request"?

Possible interpretations:
- **(A) Each model invocation**: Every time the LLM generates output (whether that output is visible text, a tool call, or an internal decision), that is 1 premium request. A single user prompt could trigger 50+ premium requests as the agent loops through read → decide → act → read → decide → act.
- **(B) Each user-visible response**: Only responses that produce user-visible output count. Tool calls that happen "behind the scenes" might be bundled.
- **(C) Each user turn**: The entire agent execution from one user prompt to the next user prompt counts as 1 premium request (unlikely given multipliers, but need to rule out).
- **(D) Token-bucket based**: Premium requests are consumed based on token volume rather than invocation count — e.g., every N tokens of input+output consumes 1 premium request.

Which interpretation matches GitHub's actual billing implementation as of early 2026?

### 2. How Do Model Multipliers Actually Work?

GitHub's documentation lists model multipliers. For the models relevant to my setup:

| Model | Listed Multiplier |
|-------|------------------|
| Claude Opus 4.6 | x3 |
| Claude Opus 4.6 fast (preview) | x30 |

**Critical question**: If the x30 multiplier were applied per model invocation (interpretation A above), then my agent session alone would have consumed 50+ invocations x 30 = 1,500+ premium requests. But the entire day only showed 78 requests. This is a 20x discrepancy.

Possible explanations:
- **(A)** The multiplier is NOT applied per-invocation in Agent Mode — it applies to the overall session or turn differently
- **(B)** The model is actually Claude Opus 4.6 (x3), not "fast (preview)" (x30), despite what the system prompt says
- **(C)** The 78 "requests" shown in billing already have the multiplier baked in (i.e., the actual model invocation count is 78/30 = ~2.6, which would mean billing counts are post-multiplier)
- **(D)** Agent Mode tool calls (file reads, terminal commands, etc.) do NOT consume premium requests — only the "thinking" invocations do
- **(E)** The multiplier system changed between when the documentation was written and March 2026
- **(F)** There is a billing cap, batch bucketing, or rounding behavior not documented

Which explanation is correct? Provide evidence from GitHub documentation, changelogs, blog posts, or community reports.

### 3. How Does Context Summarization Affect Billing?

During long Agent Mode sessions, VS Code may compress/summarize the conversation context when it exceeds the model's context window. In my session, this happened at least once (evidenced by a "conversation summary" appearing in the context).

- Does the summarization step itself consume a premium request?
- After summarization, does the agent continue consuming requests at the same rate, or does the compressed context reduce per-invocation cost?
- Is summarization performed by the same model (and therefore subject to the same multiplier)?

### 4. How Do Sub-Agents Affect Billing?

Copilot Agent Mode can launch sub-agents (e.g., `search_subagent`, `runSubagent`) that perform autonomous multi-step work. In my session, I observed 6 sub-agent invocations. Each sub-agent may itself make multiple model invocations internally.

- Does each sub-agent invocation count as 1 premium request, or does each internal model call within the sub-agent count separately?
- Are sub-agents billed at the same model multiplier as the parent agent?
- Is there any documentation on how sub-agent billing works?

### 5. What is the Actual Per-Premium-Request Price?

My billing dashboard showed $0.04 per premium request. Various documentation sources cite different rates:

| Source | Rate |
|--------|------|
| My billing dashboard (March 2026) | $0.04 per premium request |
| GitHub docs (Pro+ overage) | $0.04 per premium request |
| My project's execution prompt (written earlier) | $0.028 per premium request (claimed "Pro+ discount") |
| GitHub Copilot pricing page | varies by source |

**Questions**:
- Is $0.04 the current (March 2026) rate for Pro+ overage?
- Was $0.028 ever the rate, or was that always incorrect?
- Does the $0.04 rate apply both to included requests and overage, or is the $0.04 only a display convention for the included allowance (i.e., $39/month / 975 effective requests = $0.04)?
- Has the pricing changed between when Pro+ launched and March 2026?

### 6. Per-Session Cost Isolation

GitHub's billing dashboard shows daily aggregate usage, not per-session or per-project breakdowns.

- Is there ANY way to isolate the premium request count for a single Agent Mode session? (API, audit log, VS Code extension log, telemetry export, etc.)
- Does the GitHub REST API (`/user/copilot/usage` or `/orgs/{org}/copilot/usage`) provide per-session granularity?
- Are there VS Code extension logs (e.g., in the Copilot output channel) that record each premium request or model invocation?
- Is there a way to query usage by time window narrower than daily?

### 7. How Does the 1,500 Included Request Allowance Work?

- Do included requests reset on a calendar month boundary or billing cycle anniversary?
- When the dashboard shows "$0" in the overage column, does that mean all 78 requests came from the included 1,500?
- If I am mid-month and have consumed, say, 400 of 1,500 included requests, is there any dashboard or API that shows the remaining balance?
- Is the $0.04 shown next to each request the "notional" value (what it would cost if it were overage), even when it comes from the included allowance?

### 8. Billing for Parallel Tool Calls

In Agent Mode, the agent can execute multiple tool calls in parallel (e.g., reading 3 files simultaneously). 

- Does a batch of parallel tool calls count as 1 model invocation (1 premium request x multiplier), or does each parallel branch count separately?
- When the agent calls `read_file` on 3 files in one response, is that 1 premium request or 3?

---

## What I Need From This Research

1. **Definitive answers** to questions 1-8 above, with citations to GitHub documentation, blog posts, changelog entries, or community reports (Stack Overflow, GitHub Discussions, etc.)
2. **A billing model** that reconciles my observed data (78 requests for a full day of heavy Agent Mode usage including a session with 50+ agent iterations) with the documented multiplier system
3. **A practical methodology** for measuring per-session Copilot costs that I can use in my comparison study, given the limitations identified
4. **Any changes to the billing model** between the launch of Copilot Pro+ and March 2026 — if the multiplier system or pricing changed, I need to know when and how
5. **Comparison to OpenRouter billing** — OpenRouter provides exact per-request costs via API with generation IDs. How does Copilot's billing granularity compare, and what is the best approximation method when exact per-session data is unavailable?

---

## Context: Why This Matters

This research directly feeds into a cost comparison methodology document. The current methodology assumed:
```
Copilot session cost = model_turns x $0.028 x model_multiplier
```

This formula produced a $46.20 estimate for a single session. The actual billing data for the entire day was $3.12. The methodology is wrong by at least an order of magnitude, and I need to understand why before I can produce a valid cost comparison between Copilot and OpenRouter/Roo Code.

The stakes: this comparison will influence a corporate decision about which AI toolchain to adopt for architecture work. Inaccurate cost data could lead to the wrong platform choice.
