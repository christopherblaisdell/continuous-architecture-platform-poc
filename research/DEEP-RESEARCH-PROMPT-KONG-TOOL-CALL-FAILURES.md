# Deep Research Prompt: Kong AI Gateway Tool Call Translation Failures with LLM-Powered VS Code Extensions

## Instructions for the Research Agent

You are conducting exhaustive technical research into a **specific, documented production failure**: when VS Code extensions (Roo Code, Continue, Cline, or any OpenAI-compatible client) route requests through Kong AI Gateway's `ai-proxy` plugin to Anthropic's Claude API, tool call responses are frequently corrupted, error responses are obfuscated, and the client enters infinite retry loops.

This research will inform an enterprise architecture decision about whether to invest in fixing the Kong proxy layer, bypass it entirely, or adopt a fully managed platform. The research must be technical, evidence-based, and cite specific sources (GitHub issues, Kong plugin source code, Anthropic API documentation, Roo Code source code). Do not speculate — if evidence is unavailable, state that clearly.

---

## Background Context You Need to Know

### What We Have Already Observed

Through empirical testing of the Roo Code + Kong AI Gateway + Claude Opus 4.6 stack, we documented the following failures:

1. **Kong's `ai-proxy` plugin fails to translate Anthropic error responses into OpenAI format.** When Anthropic returns `{"error": {"type": "invalid_request_error", "message": "context_length_exceeded"}}`, Kong's Lua translation code produces either an HTTP 200 with an empty body or an HTTP 400 without the specific error strings the client expects. The descriptive error semantics are stripped during translation.

2. **Roo Code misinterprets obfuscated error responses as transient failures.** When it receives an empty response (no `hasTextContent`, no `hasToolUses`), it triggers `backoffAndAnnounce()` and retries the identical oversized payload — creating an infinite loop.

3. **Kong's rate limiting creates a race condition with context condensing.** Kong calculates token costs post-response (asynchronously via Redis). When Roo Code's context condensing safety feature fires at 80% capacity, Kong blocks it with HTTP 429 because the previous request already exhausted the quota. The safety mechanism fails silently.

4. **Tool call format translation is lossy.** Beyond error responses, we observe tool_use blocks from Claude being malformed or dropped during Kong's Anthropic-to-OpenAI translation, particularly when responses contain multiple sequential tool calls or deeply nested JSON arguments.

### What We Do NOT Yet Know

The gaps below are what we need research to fill.

---

## Research Questions — Organized by Priority

### PRIORITY 1: Kong ai-proxy Tool Call Translation (Deep Technical)

1. **Exact translation logic for Anthropic tool_use blocks.**
   - Where in Kong's `ai-proxy` Lua code does the Anthropic-to-OpenAI tool call translation happen?
   - Source repository: https://github.com/Kong/kong — locate the `ai-proxy` plugin handler code
   - What is the mapping from Anthropic's `content[].type: "tool_use"` blocks to OpenAI's `tool_calls[]` format?
   - Is the `tool_use_id` preserved? The `name`? The `input` JSON object?
   - What happens when a response contains multiple tool_use blocks in sequence?
   - What happens when tool_use arguments contain nested JSON, arrays, or large string values?

2. **Error response translation completeness.**
   - Does Kong's ai-proxy handle ALL Anthropic error types? Cross-reference against Anthropic's documented error taxonomy: https://docs.anthropic.com/en/api/errors
   - Specifically test these error types:
     - `invalid_request_error` (including `context_length_exceeded`)
     - `overloaded_error`
     - `rate_limit_error`
     - `api_error`
     - `authentication_error`
   - For each: what does Kong's ai-proxy output versus what the raw Anthropic response contains?
   - Is there a known bug or open issue in Kong's repository for this?

3. **Streaming vs non-streaming behavior.**
   - Does the tool call translation behave differently for streamed (`stream: true`) versus non-streamed responses?
   - How does Kong handle `content_block_start`, `content_block_delta`, and `content_block_stop` SSE events for tool_use blocks?
   - Does Kong buffer the entire streamed response before translating, or translate incrementally?
   - Are there known issues with streaming tool call translation in Kong's issue tracker?

4. **Kong ai-proxy plugin version history.**
   - When was Anthropic provider support added to Kong's ai-proxy plugin?
   - What version of Kong Gateway introduced Anthropic tool call (function calling) translation?
   - Are there known regressions or fixes related to Anthropic tool call handling?
   - What is the current status of the Anthropic provider in Kong's `ai-proxy`? (GA, beta, experimental?)

**Key sources to search:**
- Kong Gateway GitHub: https://github.com/Kong/kong
- Kong ai-proxy plugin docs: https://docs.konghq.com/hub/kong-inc/ai-proxy/
- Kong AI Gateway docs: https://docs.konghq.com/gateway/latest/ai-gateway/
- Kong community forum: https://discuss.konghq.com/
- Kong GitHub issues labeled `ai-proxy` or `anthropic`

### PRIORITY 2: Roo Code's Tool Call Handling and Error Recovery

5. **Roo Code's response parsing for tool calls.**
   - Source repository: https://github.com/RooCodeInc/Roo-Code
   - How does Roo Code parse tool call responses? Does it expect OpenAI format (`tool_calls[]`) or Anthropic format (`content[].type: "tool_use"`)?
   - What adapter layer, if any, translates between formats?
   - How does Roo Code handle partial tool call responses (e.g., truncated JSON in arguments)?

6. **Error classification in Roo Code.**
   - What specific error strings does Roo Code regex-match to classify errors as "context window exceeded" versus "transient failure"?
   - Source file: search for `backoffAndAnnounce`, `hasTextContent`, `hasToolUses` in the Roo Code repo
   - Is there a configurable retry limit, or does it retry indefinitely?
   - Has this been fixed in any recent version? Check CHANGELOG.md and recent PRs

7. **Context condensing trigger conditions.**
   - What exact conditions trigger Roo Code's context condensing?
   - Is the 80% threshold configurable?
   - What happens when condensing fails (HTTP 429 from upstream)?
   - Does Roo Code have a fallback when condensing is blocked?

**Key sources to search:**
- Roo Code GitHub: https://github.com/RooCodeInc/Roo-Code
- Issues: https://github.com/RooCodeInc/Roo-Code/issues/7559
- Issues: https://github.com/RooCodeInc/Roo-Code/issues/9188
- Roo Code CHANGELOG: https://github.com/RooCodeInc/Roo-Code/blob/main/CHANGELOG.md

### PRIORITY 3: Anthropic API Tool Use Contract

8. **Anthropic's official tool use specification.**
   - Tool use documentation: https://docs.anthropic.com/en/docs/build-with-claude/tool-use
   - What is the exact JSON schema for tool_use content blocks in responses?
   - What is the maximum number of tool_use blocks per response?
   - What happens when a tool call's arguments exceed a certain size?
   - How does Anthropic signal tool call errors versus content generation errors?

9. **Anthropic's error response format for tool-related failures.**
   - What error does Anthropic return when a tool call is malformed in the request?
   - What error does Anthropic return when tool results exceed the context window?
   - Is there a difference between "request too large" and "context_length_exceeded" when tool definitions inflate the system prompt?

10. **Anthropic API compatibility guarantees.**
    - Does Anthropic publish a compatibility matrix for third-party proxies?
    - Are there known issues with proxied/translated API access to Claude?
    - Does Anthropic's API explicitly support OpenAI-format requests, or is translation always third-party?

**Key sources:**
- Anthropic API reference: https://docs.anthropic.com/en/api/messages
- Anthropic tool use guide: https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- Anthropic errors reference: https://docs.anthropic.com/en/api/errors
- Anthropic changelog: https://docs.anthropic.com/en/docs/about-claude/changelog

### PRIORITY 4: Alternative VS Code Extensions and Their Proxy Compatibility

11. **Continue (VS Code extension) — proxy compatibility.**
    - Source: https://github.com/continuedev/continue
    - Does Continue support custom API base URLs (proxied endpoints)?
    - How does Continue parse tool call responses? Does it use OpenAI format or support multiple formats?
    - Does Continue have explicit Kong/proxy compatibility documentation?
    - How does Continue handle error responses from proxied endpoints?

12. **Cline (VS Code extension) — proxy compatibility.**
    - Source: https://github.com/cline/cline (formerly Claude Dev)
    - Same questions as above for Continue
    - Does Cline connect directly to Anthropic API (native format) or through OpenAI-compatible endpoints?
    - How does Cline's error recovery differ from Roo Code's?

13. **Claude Code (Anthropic's official) — architecture.**
    - Does Claude Code use the Anthropic API directly (no translation layer)?
    - Can Claude Code be configured to route through a proxy/gateway?
    - How does Claude Code handle context window limits internally?
    - What is Claude Code's compaction strategy versus Roo Code's condensing?

**Key sources:**
- Continue docs: https://docs.continue.dev/
- Continue GitHub: https://github.com/continuedev/continue
- Cline GitHub: https://github.com/cline/cline
- Claude Code docs: https://docs.anthropic.com/en/docs/claude-code

### PRIORITY 5: Kong ai-proxy Alternatives and Fixes

14. **Custom Lua scripting in Kong for error mapping.**
    - Can Kong's `post_function` or `response-transformer` plugins be used to fix error schema translation?
    - What would a custom Lua script look like to properly map Anthropic errors to OpenAI format?
    - Is there precedent in the Kong community for custom error mapping?

15. **Alternative AI gateways with Anthropic support.**
    - How do these alternatives handle Anthropic-to-OpenAI tool call translation?
      - LiteLLM (https://github.com/BerriAI/litellm) — Python proxy, widely used
      - Portkey (https://portkey.ai/) — AI gateway with multi-provider support
      - Helicone (https://helicone.ai/) — observability-focused proxy
    - Do any of these have documented, tested support for Anthropic tool call translation?
    - What is LiteLLM's track record with tool call format translation? (Check GitHub issues)

16. **OpenRouter as an alternative to Kong.**
    - OpenRouter: https://openrouter.ai/
    - OpenRouter already handles Anthropic-to-OpenAI translation server-side
    - Does OpenRouter correctly translate tool_use blocks?
    - Does OpenRouter correctly translate error responses?
    - What is OpenRouter's track record with tool call fidelity? (Check community reports)
    - Could Roo Code route through OpenRouter instead of Kong to eliminate the translation problem?

**Key sources:**
- LiteLLM GitHub: https://github.com/BerriAI/litellm
- LiteLLM docs: https://docs.litellm.ai/
- OpenRouter docs: https://openrouter.ai/docs
- Portkey docs: https://docs.portkey.ai/
- Kong plugin development: https://docs.konghq.com/gateway/latest/plugin-development/

---

## Deliverable Format

Structure your research report as follows:

### Section 1: Kong ai-proxy Tool Call Translation — Technical Analysis
- Exact code paths for Anthropic tool_use to OpenAI tool_calls translation
- Known bugs, open issues, and version history
- Error translation completeness matrix (all Anthropic error types)

### Section 2: Roo Code Response Handling — Source Code Analysis
- Response parsing logic with file/function citations
- Error classification decision tree
- Retry behavior and failure modes
- Context condensing trigger/failure paths

### Section 3: Incompatibility Analysis — Where the Stack Breaks
- Specific format mismatches between Kong output and Roo Code expectations
- Race conditions in rate limiting + context condensing
- Streaming vs non-streaming differences

### Section 4: Alternative Extension Compatibility Matrix
- Table comparing Continue, Cline, Claude Code, and Copilot against:
  - Proxy support (Kong, LiteLLM, OpenRouter)
  - Tool call format expectations
  - Error recovery resilience
  - Context window management approach

### Section 5: Alternative Gateway Compatibility Matrix
- Table comparing Kong ai-proxy, LiteLLM, OpenRouter, and Portkey against:
  - Anthropic tool call translation fidelity
  - Error response preservation
  - Rate limiting behavior
  - Streaming support

### Section 6: Recommended Fix Paths
- Ranked by effort and impact
- Include "do nothing" cost projection
- Reference specific GitHub issues, PRs, or documentation for each recommendation

---

## Research Quality Standards

- Cite specific GitHub issue numbers, PR numbers, or commit hashes where possible
- Include direct quotes from documentation or source code
- Distinguish between verified facts (from source code or docs) and inferences
- If a question cannot be answered from available sources, state "NOT FOUND" and explain what was searched
- Provide URLs for all cited sources
- Do not fabricate version numbers, feature claims, or compatibility statements
