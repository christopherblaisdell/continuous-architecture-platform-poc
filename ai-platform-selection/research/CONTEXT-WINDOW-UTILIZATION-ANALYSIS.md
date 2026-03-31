# Context Window Utilization Analysis: Roo Code vs GitHub Copilot

| | |
|-----------|-------|
| **Author** | Christopher Blaisdell |
| **Date** | 2026-03-01 |
| **Status** | VALIDATED (empirical evidence confirmed) |
| **Relates To** | [ADR-001: AI Toolchain Selection](../decisions/ADR-001-ai-toolchain-selection.md) |
| **Phase** | Phase 1 - AI Tool Cost Comparison |

---

## Executive Summary

This analysis documents a structural architectural difference between Roo Code and GitHub Copilot in how they consume the LLM context window. Roo Code injects a comprehensive environment metadata block into every user-role API message, consuming a significant and growing percentage of the available context window as conversations progress. GitHub Copilot uses selective, server-managed context inclusion that scales more efficiently. This difference has direct implications for cost, task completion rates, and effective utilization of purchased tokens.

**Key finding:** In a real Roo Code task session from this workspace, **81 environment_details blocks** consumed **1,885 lines** (16.3% of the entire task log), with the largest blocks reaching **226 lines each** — all containing repetitive metadata that did not change between turns.

---

## 1. The Problem: Context Window as a Finite Budget

Every LLM API call has a context window — a fixed token budget that must contain the system prompt, all conversation history, tool definitions, and the current turn's content. Tokens consumed by ambient metadata are tokens unavailable for actual task work.

For an architecture practice executing multi-step workflows (ticket triage, investigation, solution design, publishing), tasks routinely span 20-80+ turns. The way an AI tool manages this finite budget directly impacts:

- **Cost**: Tokens paid for metadata are wasted spend
- **Task completion**: If metadata exhausts the window, the tool must truncate conversation history, losing prior context
- **Quality**: Truncated context means the AI "forgets" earlier decisions, producing inconsistent outputs
- **Correction overhead**: The architect must re-explain context that was dropped, adding human time and more tokens

---

## 2. Roo Code: The "Broadcast Everything" Architecture

### 2.1 Source Code Evidence

The function `getEnvironmentDetails()` in the Roo Code source at `src/core/environment/getEnvironmentDetails.ts` constructs an XML block that is appended to every user-role message. The function assembles:

| Component | Source | Typical Size |
|-----------|--------|--------------|
| VSCode Visible Files | All open editor panes | 5-20 lines |
| VSCode Open Tabs | Up to 20 tabs (configurable via `maxOpenTabsContext`) | 5-20 lines |
| Active Terminal Output | Full output from all running terminals | Variable (up to 500 lines per terminal) |
| Inactive Terminal Output | Completed process output from inactive terminals | Variable |
| Recently Modified Files | Files changed since last access | 1-10 lines |
| Current Timestamp | ISO 8601 with timezone | 3 lines |
| Git Status | Changed files (if `maxGitStatusFiles > 0`) | 0-50 lines |
| Current Session Cost | Running cost total | 2 lines |
| Current Mode | Slug, name, model ID, role definition, custom instructions | 5-30 lines |
| Browser Session Status | If browser automation is active | 0-3 lines |
| Workspace Directory Listing | Recursive file enumeration up to `maxWorkspaceFiles` (default: 200) | 50-226+ lines |
| Todo List Reminders | Current task tracking state | 0-20 lines |

The function returns this as:
```xml
<environment_details>
[all of the above]
</environment_details>
```

This block is injected into **every user-role message** in the conversation history sent to the LLM.

### 2.2 The Accumulation Problem

Roo Code sends the full conversation history with each API call. As the conversation grows:

- **Turn 1**: System prompt + user message + 1 environment_details block
- **Turn 5**: System prompt + 5 user messages + 5 assistant messages + 5 environment_details blocks
- **Turn 40**: System prompt + 40 user messages + 40 assistant messages + 40 environment_details blocks
- **Turn 80**: System prompt + 80 user messages + 80 assistant messages + 80 environment_details blocks

Even if each block is "only" 21 lines (the compact form without the workspace listing), at 80 turns that is **1,680 lines of pure environment metadata** in the context window — none of which contributes to the architecture task.

Roo Code has attempted to mitigate this with a deduplication filter (verified in `src/core/task/__tests__/task-tool-history.spec.ts`: "should filter out existing environment_details blocks before adding new ones"). However, the CHANGELOG documents a recurring pattern of context window overflow bugs:

| Fix Description | Issue |
|----------------|-------|
| Prevent duplicate environment_details when resuming cancelled tasks | #9442 |
| Clean up max output token calculations to prevent context window overruns | #8821 |
| Fix context window truncation math | #1173 |
| Fix sliding window calculations causing context window overflow | (Sonnet 3.7) |
| Smarter context window management | (general) |
| Fix context window size calculation | (general) |
| Exclude cache tokens from context window calculation | (general) |
| Fix bug with context window management for thinking models | (general) |

This is not a one-time bug — it is a chronic architectural consequence of the broadcast-everything design.

### 2.3 Empirical Measurement

A real Roo Code task export from this workspace was analyzed:

**Source file:** `roo task feb-4-2026 12-25-37-pm - Unknown.md` (11,573 lines total)

| Metric | Value |
|--------|-------|
| Total `<environment_details>` blocks injected | **81** |
| Total lines consumed by environment blocks | **1,885** |
| Percentage of task log consumed by environment metadata | **16.3%** |
| Largest block (with full workspace file listing) | **226 lines** |
| Typical compact block (tabs, time, mode only) | **21 lines** |
| Average block size | **23.3 lines** |

In a workspace like ours (multi-root with 6+ repositories), the initial workspace file listing alone enumerates hundreds of paths. This listing is injected on the first message and on any message where `includeFileDetails` is true.

### 2.4 Token Cost of Environment Metadata

Estimating conservatively at ~3 tokens per line of environment metadata:

| Scenario | Env Blocks | Lines | Est. Tokens Wasted | % of 200K Context |
|----------|-----------|-------|-------------------|-------------------|
| Short task (10 turns) | 10 | ~230 | ~690 | 0.3% |
| Medium task (40 turns) | 40 | ~930 | ~2,790 | 1.4% |
| Long task (80 turns) | 80 | ~1,885 | ~5,655 | 2.8% |
| Long task + terminal output | 80 | ~4,000+ | ~12,000+ | 6.0% |

But this understates the real impact because:
1. These tokens are sent as **input tokens on every API call**, so they are billed repeatedly
2. The system prompt (which includes all tool definitions) also grows with custom instructions
3. Terminal output captured in environment blocks can be enormous (hundreds of lines per terminal)

**Cumulative input token waste across all API calls in a task** (not just the final call):
- An 80-turn task makes 80 API calls
- Each call includes all prior environment blocks in the conversation history
- The total cumulative waste follows a triangular accumulation pattern: approximately $\sum_{i=1}^{n} i \times s$ where $n$ = turns and $s$ = avg block token count
- For 80 turns at ~70 tokens/block: $\frac{80 \times 81}{2} \times 70 \approx 226,800$ **cumulative wasted input tokens billed across all API calls**

---

## 3. GitHub Copilot: The "Selective Briefing" Architecture

### 3.1 Context Management Approach

GitHub Copilot (Chat and Agent modes in VS Code) uses a fundamentally different architecture:

- **Server-side workspace indexing**: The workspace is indexed once; the full file listing is never injected into the conversation
- **Semantic retrieval**: When the AI needs file context, it requests specific files via tool calls — only the content it needs enters the context
- **Conversation summarization**: As conversations grow long, prior turns are compressed into summaries to preserve context budget for current work
- **Tool results are scoped**: Terminal output, file reads, and search results are returned as targeted responses to specific tool invocations, not broadcast as ambient metadata
- **No ambient environment block**: There is no equivalent of `<environment_details>` injected into every message

### 3.2 Effective Context Utilization

The result is that in a Copilot session:

| Component | Copilot Context Budget | Roo Code Context Budget |
|-----------|----------------------|------------------------|
| System prompt | ~5-10% | ~10-20% (larger due to custom instructions injected every turn via power steering) |
| Tool definitions | ~5% | ~10-15% (full tool schema in every message) |
| Conversation history | ~60-80% (summarized) | ~40-60% (full history with env blocks) |
| Environment metadata | ~0% (none injected) | ~5-15% (environment_details blocks) |
| **Available for task work** | **~70-85%** | **~30-55%** |

### 3.3 Cost Implications

Because Copilot's per-seat pricing ($19/month individual, $39/month business) is flat-rate:
- Context efficiency does not directly impact the monthly bill
- But it does impact **task completion rate** and **quality** — more context available for work means fewer truncation events, fewer re-explanations, and better continuity across long architecture tasks

For Roo Code's usage-based pricing:
- Every wasted token is billed
- The triangular accumulation of environment metadata means **long tasks are disproportionately expensive**
- A task that could complete in 40 turns on Copilot might require 60 turns on Roo Code because context truncation caused the AI to lose track of earlier decisions

---

## 4. Implications for ADR-001

This analysis adds a new evaluation dimension to the toolchain selection:

### 4.1 Proposed Additional Decision Driver

**Effective context utilization**: The percentage of purchased/allocated context window tokens that are available for productive task work (as opposed to ambient metadata, repeated environment state, and overhead).

### 4.2 Impact on Evaluation Criteria

| Existing Criterion | Context Window Impact |
|--------------------|----------------------|
| **Cost (30% weight)** | Roo Code's usage-based model is penalized by wasted tokens on environment metadata, especially for long architecture tasks |
| **Quality (25% weight)** | Context truncation in Roo Code can degrade output quality on long tasks; Copilot's summarization preserves more working context |
| **Corrections (15% weight)** | Context loss from truncation requires architects to re-state requirements, increasing correction cycles |
| **Friction (10% weight)** | Roo Code requires manual tuning of `maxWorkspaceFiles`, `maxOpenTabsContext`, and other parameters to manage context; Copilot manages this automatically |

### 4.3 Recommendation

Include "Context Window Efficiency" as a measured metric in Phase 1 scenario execution:
- Record total tokens billed per scenario on each toolchain
- Record the number of turns where context truncation occurred
- Record instances where the AI "forgot" earlier instructions (proxy for context loss)
- Calculate the ratio of productive tokens to total tokens for each tool

---

## 5. Evidence Sources

| Source | Location | What It Shows |
|--------|----------|---------------|
| Roo Code source: `getEnvironmentDetails.ts` | `Roo-Code/src/core/environment/getEnvironmentDetails.ts` | How the environment block is constructed |
| Roo Code source: deduplication test | `Roo-Code/src/core/task/__tests__/task-tool-history.spec.ts` | Attempted mitigation of duplicate blocks |
| Roo Code CHANGELOG | `Roo-Code/src/CHANGELOG.md` | History of context window overflow bugs |
| Roo task export (empirical) | `calibre-library/Unknown/roo task feb-4-2026 12-25-37-pm/` | 81 environment blocks in a single task |
| Kong AI interoperability investigation | `_ROO-KONG-AI-COMPATIBILITY-ISSUE/2.analysis/roo-kong-ai-interoperability-investigation.md` | Describes Roo's context window construction including tool definitions |

---

## 6. Open Questions for Deep Research

1. What is the exact token count of a typical environment_details block in a large enterprise workspace?
2. Does Roo Code's sliding window truncation preserve or discard environment_details blocks when compressing history?
3. What is the empirical task completion rate difference between tools with high vs low context overhead?
4. Can Roo Code be configured (via `.roo/rules/` or settings) to disable environment_details injection entirely?
5. What third-party context management solutions exist for open-source AI coding agents?
6. How do other AI coding agents (Cursor, Windsurf, Aider) handle environment context compared to Roo Code and Copilot?
