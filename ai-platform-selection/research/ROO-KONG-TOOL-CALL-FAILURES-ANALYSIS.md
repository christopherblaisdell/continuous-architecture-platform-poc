# Roo Code + Kong AI Gateway: Tool Call Failures and Context Window Breakdown

## Summary

When using Roo Code with Kong AI Gateway as a proxy to Anthropic's Claude API, architects experience constant tool call errors — messages stating that tool calls "cannot be handled." This document explains the root causes, attributes responsibility across the stack, analyzes context window management failures, and evaluates whether alternative VS Code plugins would resolve the issues.

---

## The Three Actors

| Component | Role | Responsibility |
|-----------|------|---------------|
| **Roo Code** | VS Code extension | Manages conversation state client-side, constructs tool call payloads, interprets API responses |
| **Kong AI Gateway** | API proxy (ai-proxy plugin) | Translates between OpenAI-format requests and Anthropic-format requests/responses |
| **Claude API (Anthropic)** | LLM backend | Processes requests, returns tool_use blocks, enforces context window limits |

---

## Root Cause: Who Is Responsible?

**All three share blame, but the primary fault is the Kong-Roo interface — neither component correctly handles the other's edge cases.**

### 1. Kong's ai-proxy Plugin: Error Schema Mismatch

Kong's `ai-proxy` Lua plugin translates between OpenAI and Anthropic API formats. It works for successful requests. But when Anthropic returns an error (especially `context_length_exceeded` or `overloaded_error`), Kong's translation fails:

- Anthropic returns: `{"error": {"type": "invalid_request_error", "message": "context_length_exceeded"}}`
- Kong's Lua code cannot cleanly map this into the OpenAI error schema Roo Code expects
- Kong returns either an HTTP 200 with an empty body or an HTTP 400 without the specific error strings Roo Code's parser needs
- **Result:** The descriptive error information is stripped during translation

This is **Kong's fault** — the ai-proxy plugin has incomplete error mapping for Anthropic's error taxonomy.

### 2. Roo Code: Brittle Response Parsing and Retry Logic

When Roo Code receives a response, it checks for specific content flags (`hasTextContent`, `hasToolUses`). When Kong returns an obfuscated error response with no content:

- Roo Code's parser finds no assistant content and no tool use blocks
- It falls through to a generic error handler: _"The language model did not provide any assistant messages"_
- The generic handler treats this as a **transient failure** and triggers `backoffAndAnnounce()` — which retries the exact same oversized payload
- This creates an **infinite retry loop** because the payload size never changes

This is **Roo Code's fault** — it should distinguish between "empty response" (transient) and "request rejected" (permanent), but its error classification is too coarse.

**Documented in Roo Code's own issue tracker:**

- Issue #7559: "Application becomes unusable when context window token limit is exceeded"
- Issue #9188: "[BUG] Roo Code is prone to HTTP 400 errors after multiple rounds of communication"

### 3. Claude API: No Fault (Behaves Correctly)

Anthropic's API behaves correctly — it returns a well-formed error with a clear `context_length_exceeded` type when the payload exceeds the model's limit. The problem is entirely in how Kong and Roo Code handle that response downstream.

---

## The Cascading Failure Sequence

```
Phase 1: Context accumulates across turns (Roo Code stores full history client-side)
    ↓
Phase 2: Payload exceeds Claude's 200K token context window
    ↓
Phase 3: Anthropic returns HTTP 400 with "context_length_exceeded"
    ↓
Phase 4: Kong's ai-proxy intercepts the error
         → Attempts Anthropic-to-OpenAI error format translation
         → Translation FAILS — returns HTTP 200 with empty body
           or HTTP 400 without recognizable error strings
    ↓
Phase 5: Roo Code receives obfuscated response
         → No hasTextContent, no hasToolUses
         → Throws: "Unexpected API Response: The language model
            did not provide any assistant messages"
    ↓
Phase 6: Roo Code's backoffAndAnnounce() retries same 200K payload
    ↓
Phase 7: INFINITE LOOP — rejected, obfuscated, misinterpreted, retried
```

### The Rate Limiting Trap

Kong's rate limiting compounds the problem. Kong calculates token costs **post-response** (asynchronously via Redis). When Roo Code's context condensing safety feature attempts to fire at 80% capacity:

1. The previous massive request already consumed the token quota
2. Kong blocks the condensing request with HTTP 429
3. The safety mechanism designed to prevent overflow is itself blocked
4. Context continues growing with no escape path

---

## How This Relates to Context Window Management

### Roo Code's Client-Side Architecture

Roo Code maintains the **entire conversation as a serialized JSON array on the client**. Every turn — user messages, assistant responses, tool calls, tool results, file contents — accumulates in memory and is retransmitted to the API on every subsequent turn.

| Turn | Approximate Payload | Cost at Claude Opus 4.6 Rates |
|------|:---:|:---:|
| Turn 1 | ~5K tokens | ~$0.50 |
| Turn 10 | ~50K tokens | ~$5.00 |
| Turn 20 | ~120K tokens | ~$12.00 |
| Turn 40 | ~180K tokens | ~$20.00+ |

Additionally, Roo Code injects an `<environment_details>` metadata block into every user message — containing workspace file listings, open tabs, terminal output, and session metadata. Empirical measurement showed **81 such blocks consuming 1,885 lines (16.3% of context)** in a typical architecture task.

### Context Condensing: The Failed Safety Net

Roo Code has a "context condensing" feature that should fire at ~80% of the context window. It sends a summarization request to the LLM, compressing earlier context into a shorter summary. In theory, this prevents overflow.

**In practice with Kong, it fails because:**

1. The condensing request itself requires LLM API access
2. Kong's token quota is already exhausted by the previous large request
3. Kong blocks the condensing request with HTTP 429
4. Context continues growing unbounded toward the hard limit
5. When it hits the limit, the infinite retry loop begins

### Contrast: GitHub Copilot's Server-Side Approach

GitHub Copilot manages context entirely on the server side:

| Aspect | Roo Code | Copilot |
|--------|----------|---------|
| **Context storage** | Client-side JSON array | Server-side managed |
| **History retransmission** | Full history every turn | Selective retrieval |
| **Overflow prevention** | Client-side condensing (often blocked by Kong) | Server-side sliding window + summarization |
| **Workspace awareness** | Manual file selection or Qdrant provisioning | Automatic server-side vector index |
| **Error handling** | Falls through to infinite retry | Server handles errors before client sees them |

Copilot's architecture makes context overflow **structurally impossible at the client layer** because the client never manages the full conversation history.

---

## Would a Different VS Code Plugin Fix This?

### The Short Answer

**Partially — a different plugin would fix Roo Code's parsing and retry bugs, but not Kong's error translation problem.**

### Analysis by Alternative

#### Option A: Continue (VS Code Extension)

Continue is an open-source alternative to Roo Code. It supports custom LLM providers including Kong-proxied endpoints.

- **Fixes:** Different response parsing logic — may handle empty responses more gracefully
- **Does NOT fix:** Kong's ai-proxy error translation. Continue would still receive obfuscated errors from Kong
- **Context management:** Similar client-side model — conversation history accumulates and is retransmitted
- **Verdict:** Marginal improvement. The Kong error mapping is the deeper problem

#### Option B: Cline (VS Code Extension)

Cline (formerly Claude Dev) is another agentic coding extension.

- **Fixes:** Cline has its own retry/error handling that may be more resilient
- **Does NOT fix:** Kong error obfuscation, context window re-transmission cost
- **Context management:** Client-side like Roo Code — same quadratic cost growth
- **Verdict:** May avoid the infinite loop but does not solve the economic or context management problems

#### Option C: Claude Code (Anthropic's Official Tool)

Claude Code is Anthropic's first-party CLI/VS Code integration.

- **Fixes:** Direct Anthropic API integration — no Kong proxy needed. Error responses are native format
- **Does NOT fix:** Requires Anthropic API key directly (bypasses Kong's cost controls and observability)
- **Context management:** On-demand file reading via tool calls. Compaction at configurable thresholds (recommended 50%). Subagent delegation for exploration
- **Verdict:** Eliminates the Kong translation problem entirely but removes enterprise gateway controls

#### Option D: GitHub Copilot

- **Fixes:** Everything — server-side context management, automatic workspace indexing, no proxy layer
- **Does NOT fix:** N/A for this failure class
- **Context management:** Fully server-managed. Context never approaches limits at the client
- **Verdict:** Eliminates all three failure modes (indexing, context overflow, error obfuscation)

### The Fundamental Problem

Any VS Code plugin that routes through Kong's ai-proxy will face the error translation problem. The fix must happen at one of these layers:

1. **Kong layer:** Write custom Lua scripts to properly map Anthropic error schemas (weeks of DevOps work)
2. **Plugin layer:** Choose a plugin that handles obfuscated errors gracefully and implements pre-request context size validation
3. **Architecture layer:** Remove the proxy entirely (use direct API access or a platform like Copilot that manages the backend)

---

## Recommended Mitigations

### If Staying on Roo Code + Kong

| Mitigation | Effort | Impact |
|------------|--------|--------|
| Custom Lua error mapping in Kong's ai-proxy | High (weeks) | Fixes infinite retry loop |
| Tune `sync_rate` in Kong rate limiting to near-minimum | Medium (days) | Reduces quota race condition |
| Implement "soft-cap" rate limit buffer for condensing requests | Medium (days) | Protects safety mechanism |
| Pre-request token counting in Roo Code (client-side) | High (requires Roo Code fork) | Prevents oversized payloads |
| Provision Qdrant + embeddings for workspace indexing | Medium (days) | Reduces context size via RAG |

### If Willing to Change Stack

| Option | Effort | Outcome |
|--------|--------|---------|
| Switch to Claude Code (bypass Kong) | Low (hours) | Eliminates proxy errors; loses gateway controls |
| Switch to GitHub Copilot Pro+ | Low (hours) | Eliminates all three failure classes; $39/month flat rate |
| Keep Kong but switch plugin to Continue/Cline | Medium (days) | May avoid infinite loop; does not fix root cause |

---

## Conclusion

The tool call errors are caused by an **incompatibility between Kong's ai-proxy error translation and Roo Code's response parsing** — neither product was designed to work with the other. Kong strips error semantics during Anthropic-to-OpenAI translation; Roo Code misinterprets the stripped response as a transient failure and retries infinitely.

This is compounded by Roo Code's client-side context management architecture, which allows payloads to grow unbounded until they exceed the model's context window — the very condition that triggers the Kong error translation failure.

No VS Code plugin change alone resolves the Kong error mapping. The options are: fix Kong's Lua scripts, bypass Kong entirely, or adopt a platform (Copilot) that manages the entire backend.

---

## References

| Source | Location |
|--------|----------|
| Kong failure cascade analysis | [DEEP-RESEARCH-2.md](DEEP-RESEARCH-2.md) |
| Context window utilization data | [CONTEXT-WINDOW-UTILIZATION-ANALYSIS.md](CONTEXT-WINDOW-UTILIZATION-ANALYSIS.md) |
| Copilot billing model analysis | [DEEP-RESEARCH-RESULTS-COPILOT-BILLING.md](DEEP-RESEARCH-RESULTS-COPILOT-BILLING.md) |
| Vector DB feasibility for Roo Code | [VECTOR-DB-RAG-FEASIBILITY-ANALYSIS.md](VECTOR-DB-RAG-FEASIBILITY-ANALYSIS.md) |
| Presentation-format failure summary | [roo-kong-failures.md](../../presentation/docs/roo-kong-failures.md) |
| ADR-001: Toolchain selection decision | [ADR-001](../../decisions/ADR-001-ai-toolchain-selection.md) |
| Roo Code Issue #7559 | https://github.com/RooCodeInc/Roo-Code/issues/7559 |
| Roo Code Issue #9188 | https://github.com/RooCodeInc/Roo-Code/issues/9188 |
