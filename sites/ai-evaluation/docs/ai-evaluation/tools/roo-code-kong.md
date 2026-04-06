<!-- CONFLUENCE-PUBLISH -->

# Roo Code + Kong AI Gateway

> **You are reading:** Tool Profile | [Home](../../index.md)
>
> This is a detailed profile of one evaluated toolchain. See [Copilot vs Roo Code](../comparisons/copilot-vs-roocode.md) for the head-to-head comparison, or [Platform Options](../platform-options.md) for how this tool fits into composed options.

## Tool Profile

| | |
|---|---|
| **Type** | Open-source VS Code extension + API gateway |
| **IDE Integration** | VS Code (extension) |
| **Agent Mode** | Yes -- autonomous multi-step execution |
| **Pricing** | Pay-per-token via OpenRouter (no subscription) |
| **Model Used** | Claude Opus 4.6 (via OpenRouter) |
| **Workspace Indexing** | None built-in (requires external Qdrant + embedding provider) |
| **Vendor** | Roo Code (open source, MIT) + Kong Inc (gateway) |

---

## Architecture

The Roo Code + Kong stack is a three-layer architecture: VS Code extension (client) -> Kong AI Gateway (proxy) -> OpenRouter/AWS Bedrock (model provider). Each layer introduces complexity and potential failure points.

### No Built-In Workspace Indexing

Roo Code does not index the workspace. The settings UI displays a "Codebase Indexing" checkbox, but it is **greyed out by default** because it depends on external infrastructure that must be provisioned separately:

1. Choose and configure an **external embedding provider** (OpenAI, Google Gemini, or Ollama) — requires an API key and endpoint
2. Provision a **Qdrant vector database** (Docker container or Qdrant Cloud instance)
3. Maintain **real-time synchronization** between workspace files and the vector index

Until both the embedding provider and Qdrant are configured and reachable, the checkbox remains disabled. This is not a bug — it is a design constraint of the BYOI (Bring Your Own Infrastructure) model.

Without this infrastructure, the AI has no awareness of the workspace beyond what the user explicitly tells it to read. In practice, this means manually specifying files in the Roo Code window every time a task starts.

### Why Roo Code Indexing Is Not Equivalent to Copilot's Context Awareness

Even with Qdrant fully configured, Roo Code's workspace indexing is architecturally weaker than Copilot's server-side indexing in several critical ways:

| Aspect | GitHub Copilot | Roo Code + Qdrant |
|--------|----------------|--------------------|
| **Setup** | Zero — automatic on workspace open | Manual — provision Qdrant, configure embedding provider, maintain sync |
| **Index location** | GitHub servers (fully managed) | Local Docker or Qdrant Cloud (user maintains) |
| **Index trigger** | Automatic on workspace open and file changes | Manual configuration; sync must be maintained |
| **Retrieval trigger** | Proactive — Copilot injects relevant context before the model starts reasoning | Reactive — the LLM must issue an explicit `codebase_search` tool call |
| **Context curation** | Server-side — sends curated snippets, not full files | Raw search results returned to client, counted against token budget |
| **Cost of retrieval** | Free — tool calls (including search) are not billed | Billed — every search result adds tokens to the context window, increasing per-turn cost |
| **Failure mode** | Graceful — model has context even if it does not explicitly request it | Silent fabrication — if the model does not realize it needs context, it proceeds without it and hallucinates |

The critical gap is the **proactive vs. reactive** distinction. Copilot's server-side index automatically injects relevant workspace context into the model's prompt window before reasoning begins. The model does not need to know it is missing something — the infrastructure ensures it has what it needs.

Roo Code's indexing, even when fully operational, requires the LLM to **recognize its own knowledge deficit** and explicitly invoke a `codebase_search` tool call. If it does not realize it needs context, it proceeds without it — and fabricates. This is a fundamental architectural limitation: the model must be self-aware about what it does not know, which is precisely the scenario where LLMs perform worst.

Additionally, every search result returned by Qdrant is injected into the client-side context window and **billed at full token rates** on every subsequent turn. Copilot's server-side retrieval is free — it never enters the billing pipeline.

### Client-Side Context Accumulation

Roo Code maintains the entire conversational state client-side as a serialized JSON array. Every file read, every tool call, every AI response accumulates in memory and is retransmitted to the model on every turn. This creates exponential cost growth:

| Turn | Approximate Context | Approximate Cost |
|------|:---:|:---:|
| Turn 1 | ~5K tokens | ~$0.50 |
| Turn 10 | ~50K tokens | ~$5.00 |
| Turn 20 | ~120K tokens | ~$12.00 |
| Turn 40 | ~180K tokens | ~$20.00+ |

---

## Pricing

### OpenRouter (Pay-Per-Token)

| Parameter | Value |
|-----------|-------|
| Subscription fee | $0 |
| Billing model | Per input/output token |
| Claude Opus 4.6 rate | Variable (see OpenRouter pricing page) |
| Cost visibility | Full -- exact per-generation costs via API |
| Cost retrieval | `python3 portal/scripts/utilities/openrouter-cost.py` |

### Actual Cost Evidence (March 4, 2026)

| Time | Auto-Top-Up | Running Total |
|------|-------------|---------------|
| 10:11 AM | $25 | $25 |
| 10:27 AM | $25 | $50 |
| 10:32 AM | $25 | $75 |
| 10:37 AM | $25 | $100 |

Four $25 auto-top-up charges in a 26-minute window during the 5-scenario run. The total session consumed approximately **$100 in API credits**.

### Monthly Projection

| Workload | Monthly Cost |
|----------|-------------|
| 38 runs (with PROMOTE steps) | ~$507 |
| 50 runs | ~$667 |
| 100 runs | ~$1,334 |

There is no discount floor. Cost scales linearly with usage volume.

---

## Three Architectural Limitations

Deep research and production testing identified three cascading architectural failures in this stack. These are documented, reproducible, and unresolved.

### 1. Kong AI Gateway Translation Failures

Kong's `ai-proxy` Lua plugin translates between OpenAI and Anthropic API formats. The translation layer exhibits severe structural deficiencies:

| Failure | Impact |
|---------|--------|
| **Empty tool results** | Complex nested JSON tool calls decode to empty payloads in Lua |
| **Error obfuscation** | `context_length_exceeded` errors stripped; replaced with generic 500 |
| **Streaming fragility** | Content block deltas fracture at multibyte/JSON boundaries |
| **tool_choice mismatch** | String vs. nested dictionary schema incompatibility |

When Kong drops a tool call response, Roo Code receives an HTTP 200 with an empty body. The extension cannot distinguish between a model choosing silence and an upstream proxy dropping a malformed payload.

See [Kong AI Translation Failures](../research/kong-failures.md) for the full source code analysis.

### 2. Infinite Retry Loops

When Roo Code classifies a failure as transient (which it does for all Kong-obfuscated errors), it enters a `backoffAndAnnounce()` retry loop. Source code analysis reveals **no configured maximum retry limit** for "empty assistant response" failures when automatic approval is enabled.

Because the failure stems from a deterministic payload translation error at the Kong gateway (not a transient network timeout), the retry is mathematically guaranteed to fail again. Without a circuit breaker, Roo Code enters an infinite, uncapped retry loop -- consuming bandwidth, compute, and API credits indefinitely.

### 3. Context Condensing Race Condition

Roo Code implements "Intelligent Context Condensing" that triggers when token usage reaches a configurable threshold (default 80%). However, Kong's rate limiting uses asynchronous Redis synchronization. When the condensing request fires, the preceding large request may have just triggered a rate limit. Kong blocks the condensing request with HTTP 429.

**Result:** The application cannot proceed with normal tasks (at the 80% context limit) and cannot condense (blocked by the rate limiter). The session is paralyzed.

---

## Evaluation Results

### Quality Scores

Roo Code quality scoring is pending human evaluation using the same rubrics applied to Copilot. Both runs produced comparable file structures:

| Scenario | Files (Roo Code) | Files (Copilot) |
|----------|-----------------|----------------|
| SC-01: Ticket Triage | 8 | 8 |
| SC-02: Solution Design | 8 | 8 |
| SC-03: Investigation | 7 | 7 |
| SC-04: Architecture Update | 3 | 3 |
| SC-05: Publishing Prep | 10 | 11 |
| **Total** | **36-38** | **37** |

### Notable Differences from Copilot

| Aspect | Roo Code | Copilot |
|--------|----------|---------|
| SC-02 safety detection | Correctly flagged Pattern 1 default | Correctly flagged Pattern 1 default |
| SC-02 naming discrepancy | Flagged ActivityType mismatch | Did not flag |
| SC-03 root cause | Correct (boundary violation + PUT) | Correct (boundary violation + PUT) |
| SC-04 scope discipline | Added extra fields beyond approved design | Strictly limited to approved 2 fields |
| SC-05 source code analysis | Did not read CheckInController source | Identified 4 specific code gaps |

---

## Strengths

1. **Full cost transparency** -- exact per-request token counts and costs via OpenRouter API
2. **Model flexibility** -- can switch between any model on OpenRouter (Claude, GPT, Gemini, open-source)
3. **Open source** -- no vendor lock-in on the extension itself
4. **Custom instruction system** -- `.roo/rules/` enables fine-grained standards enforcement per mode
5. **MCP support** -- Model Context Protocol enables custom tool integration

---

## Limitations

1. **Cost** -- ~$100/run for architecture work ($507/month extrapolated) vs $0.48/run for Copilot
2. **No built-in workspace indexing** -- requires provisioning Qdrant + embedding provider + sync infrastructure
3. **Context accumulation** -- client-side state management causes quadratic cost growth per turn
4. **Gateway fragility** -- Kong AI translation layer drops tool calls, obfuscates errors, and truncates streams
5. **Infinite retry vulnerability** -- no circuit breaker on failed tool call responses
6. **Rate limiting race condition** -- asynchronous Redis sync blocks context condensing at critical moments
7. **No ecosystem integration** -- no PR review, no repository context, no GitHub integration
