---
description: "Use when the user says 'prompt me' — activates an interactive decision-loop workflow where the agent presents each step or issue with lettered options, a recommendation, and waits for the user to choose before proceeding."
---

# Prompt Me — Interactive Decision Loop

When the user says **"prompt me"**, a plan or task list is already in progress. The user wants to step through it interactively, one item at a time, with full control over each decision.

## Workflow

For each item in the plan (issue, step, finding, change, etc.):

### 1. Investigate

Before presenting anything, thoroughly research the item:

- Read the relevant files, specs, logs, or metadata
- Understand the current state and what changing it would involve
- Identify risks, trade-offs, and alternatives
- Be skeptical — do not assume the obvious answer is correct

### 2. Present

State the item clearly, then provide:

- **Context**: What the issue is, with relevant quotes or file references
- **Lettered options** (A, B, C, etc.): Each option gets:
  - A short label (e.g., "Accept as-is", "Add validation", "Redesign")
  - A plain-language explanation of what it means and what happens if chosen
  - Any trade-offs or consequences
- **Recommendation**: State which option is recommended and a one-sentence rationale

### 3. Wait

Stop and wait for the user to respond with a letter. Do NOT proceed, skip ahead, or batch multiple items.

### 4. Apply

Implement the user's chosen option (edit files, update docs, run commands, etc.).

### 5. Wait Again

After applying the change, stop and wait for the user to confirm (they may check the result and push before continuing).

### 6. Next

Only after confirmation, present the next item using the same format.

## Rules

- One item at a time — never present multiple items in a single message
- Always investigate before presenting — no shallow or speculative options
- Be skeptical — question assumptions, flag risks, surface non-obvious concerns
- Keep explanations simple and direct — no jargon walls
- If the user says "prompt me" with additional context (e.g., "prompt me on the review findings"), use that to identify which plan or list to step through
- If no plan is in progress, ask: "What plan or list should I step through with you?"
