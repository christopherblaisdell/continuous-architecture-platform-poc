<!-- CONFLUENCE-PUBLISH -->

# Kong AI Translation Failures

> **You are reading:** Research — Deep Dive | [Home](../../index.md)
>
> This deep research supports [DD-04: AI Provider](../decisions/dd-04-ai-provider.md) (Layer 2) by documenting structural deficiencies in the Kong/OpenRouter gateway approach.

## Deep Research Results: Kong ai-proxy Tool Call Translation

This page summarizes the findings of a deep research analysis conducted on March 17, 2026, investigating the structural deficiencies in Kong AI Gateway's translation layer when proxying Anthropic Claude API requests through an OpenAI-compatible interface.

---

## The Problem

Kong's `ai-proxy` Lua plugin translates between OpenAI and Anthropic API formats. This translation layer exhibits severe structural deficiencies that cause three cascading failures in agentic VS Code extension workflows.

---

## Failure 1: Empty Tool Results

When Claude returns a complex tool call response, Kong must decode the Anthropic `tool_use` content block, transform it into the OpenAI `tool_calls` format, and re-encode it. The Lua parser frequently fails on:

- Multiple sequential `tool_use` blocks
- Deeply nested JSON arguments
- Exceptionally large string values

**Result:** Kong outputs an HTTP 200 OK with an empty body or strips the tool calls entirely. The downstream client (Roo Code) receives a "successful" response containing no actionable data.

Kong maintainers have acknowledged these bugs, noting that "tools (function) calls to Anthropic would return empty results" in versions prior to 3.8.0. Core contributors stated a "massive revamp to tool_use mappings" would be required.

### tool_choice Schema Mismatch

A specific failure point: OpenAI permits `tool_choice` as a flat string (`{"tool_choice": "auto"}`), while Anthropic requires a nested dictionary (`{"tool_choice": {"type": "auto"}}`). The Kong driver performed naive direct assignment, causing Anthropic to reject payloads with `invalid_request_error`.

---

## Failure 2: Error Obfuscation

Kong aggressively strips Anthropic's granular error semantics, replacing specific error types with generic HTTP 500 responses.

| Anthropic Error | Kong Translation | Impact |
|----------------|-----------------|--------|
| `context_length_exceeded` | Generic 400/500 | Client safety mechanisms for context compaction fail to trigger |
| `overloaded_error` | Generic 502/503 | Clients retry aggressively, worsening the load |
| `rate_limit_error` | Kong's own 429 | Obfuscates whether Anthropic or Kong triggered the limit |
| `authentication_error` | Standard 401 | Detailed JSON body explaining the key failure is lost |
| `invalid_request_error` | Generic 500 | Client assumes transient proxy failure, not deterministic defect |

### Critical Impact: context_length_exceeded

Anthropic uses this specific error code to signal when the context window exceeds the model's maximum (e.g., 200K tokens for Claude Sonnet). Kong lacks a dedicated parsing routine for this sub-error, so it falls through to the generic handler.

Downstream applications that search for `"context_length_exceeded"` in API responses are blinded to the context boundary. This is the root cause of Roo Code's infinite retry loops -- the extension cannot detect that it has hit the token ceiling.

---

## Failure 3: Streaming Fragility

Anthropic's streaming API emits granular events (`content_block_start`, `content_block_delta`, `content_block_stop`). When an assistant invokes a tool, the JSON arguments arrive as fragmented substrings across multiple `content_block_delta` events.

Kong translates incrementally rather than buffering the entire response, which reduces latency but exponentially increases parsing fragility. When a tool call argument spans multibyte characters or complex JSON boundaries, the incremental translation logic fractures the payload.

Official Kong changelogs document: "Anthropic provider failed to stream function call responses" and "Anthropic provider could truncate tokens in streaming responses."

---

## Downstream Impact: Roo Code Infinite Retry

When Kong drops a tool call response, Roo Code's parser evaluates:

```
hasTextContent = assistantMessage.length > 0
hasToolUses = this.assistantMessageContent.some(...)
```

If both evaluate to `false`, Roo Code throws: *"The language model did not provide any assistant messages."*

With `autoApprovalEnabled = true`, this triggers `backoffAndAnnounce()` -- an exponential backoff retry with **no configured maximum retry limit**. Because the failure is a deterministic translation error (not transient), every retry fails identically. The result is an infinite, uncapped retry loop consuming bandwidth, compute, and API credits.

---

## Alternative Gateway Comparison

| Gateway | Tool Call Fidelity | Error Preservation | Streaming | Rate Limiting |
|---------|:---:|:---:|:---:|:---:|
| **Kong ai-proxy** | Poor | Poor | Unstable | Async (race conditions) |
| **LiteLLM** | Moderate | Good | Highly stable | Sync (no race conditions) |
| **OpenRouter** | Excellent | Excellent | Highly stable | Sync (immediate) |
| **Portkey** | High | Excellent | Stable | Sync (edge-deployed) |

OpenRouter resolves the infinite loop vulnerability natively by transforming `context_length_exceeded` into a successful completion flagged with `finish_reason: length`. This tells Roo Code the response was legitimately truncated, not arbitrarily failed.

---

## Alternative Extension Comparison

| Capability | Roo Code | Cline | Continue | Claude Code |
|-----------|:---:|:---:|:---:|:---:|
| **Proxy support** | Dependent on fidelity | Specialized toggles | Excellent routing | Demands native Anthropic |
| **Tool call format** | Rigid OpenAI adapter | Native tool bypass toggle | Multi-provider parsing | Native `tool_use` |
| **Error recovery** | Infinite retry loops | Similar (being patched) | Graceful user alerts | Native error taxonomy |
| **Context management** | 80% threshold condensing | Similar condensing | LRU eviction | Built-in compaction |

Cline partially mitigates the fragility by exposing a "Enable Native Tool Calling" toggle that bypasses the gateway translation layer. Claude Code sidesteps the issue entirely by refusing to integrate with OpenAI-standardized translation proxies.

---

## Recommended Fix Paths

### 1. Native Format Passthrough (Lowest Effort)

Configure Kong's `ai-proxy` with `config.llm_format = "anthropic"` (Kong v3.10+) to bypass the Lua translation driver entirely. Configure VS Code extensions to use native Anthropic formatting.

**Resolves:** All three failures (empty tool results, error obfuscation, streaming fragility).

### 2. Migrate to Dedicated AI Gateway (Moderate Effort)

Replace Kong's `ai-proxy` endpoint with OpenRouter or Portkey. These platforms execute complex adapter patterns required for Anthropic's stateful `tool_use` alternation rules without dropping tokens.

**Resolves:** All three failures plus the rate limiting race condition.

### 3. Custom Lua Error Mapping (High Effort)

Deploy custom Lua `pre-function`/`post-function` plugins to intercept and repair the specific error obfuscation. Tune the `ai-rate-limiting-advanced` sync interval to near-zero.

**Resolves:** Error obfuscation only. Does not fix tool call truncation during streaming.

---

## Source

Full analysis with source code traces, GitHub issue references, and Kong changelog citations: `docs/research/DEEP-RESEARCH-RESULTS-KONG-TOOL-CALL-FAILURES.md`.
