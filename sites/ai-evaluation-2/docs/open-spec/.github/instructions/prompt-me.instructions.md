---
applyTo: "**"
---

<!-- ============================================================
     DERIVED FILE — DO NOT EDIT DIRECTLY
     Canonical source: .ai-customizations/methodologies/guided-plan-execution.md
     To make changes: /opsx:propose "description of change"
     Then run: scripts/sync-ai-customizations.sh
     Validation: scripts/validate-ai-customizations.sh
     Governance: openspec/specs/ai-customization-governance/spec.md
     ============================================================ -->

# Guided Plan Execution — Interactive Decision Loop

<!-- PAIRED FILE: This content must stay in sync with .ai-customizations/methodologies/guided-plan-execution.md -->
<!-- If you edit this file, update the paired file to match. Run: scripts/validate-ai-customizations.sh -->

**Triggers**: User says "prompt me", "execute this plan", or "let's work through this step by step"

## Activation

- If a plan or task list is already in progress, step through it one item at a time using the workflow below.
- If the user says "prompt me" with additional context (e.g., "prompt me on the review findings"), use that to identify which plan or list to step through.
- If no plan is in progress, ask: **"What plan or list should I step through with you?"** and provide lettered options (A, B, C, etc.) for any likely candidates based on context.

## Workflow — For Each Item

### Step 1 — Investigate

Before presenting anything, thoroughly research the item using the **authoritative architecture artifacts**. Do not make assumptions — go read the actual files.

**Primary sources of truth** (check these first):

- **OpenAPI specs** (`external-repos/architecture/udx-architecture-artifacts/services/`) — the official API contracts for every service. Field names, types, required/optional, enum values, and endpoint definitions live here. If a claim contradicts the spec, the spec wins.
- **PlantUML sequence diagrams** (`external-repos/architecture/udx-architecture-artifacts/diagrams/`) — the official cross-service interaction flows. These show who calls whom, in what order, with what data.
- **PlantUML component diagrams** (`external-repos/architecture/udx-architecture-artifacts/diagrams/Components/`) — the official internal structure of each service and domain.

**Supporting sources** (check when relevant):

- **AsyncAPI event specs** (`external-repos/architecture/udx-architecture-artifacts/events/`) — event schemas and channel definitions
- **Architecture decisions** (`decisions/ADR-*.md`) — settled design constraints that must not be contradicted
- **Existing solution designs** (`architecture/solutions/`) — prior art that may overlap or constrain

**Investigation rules:**

- Read the actual file content — do not rely on memory or assumptions about what a spec contains
- Cross-reference claims against the OpenAPI spec before presenting options
- If something looks wrong or inconsistent between artifacts, flag it explicitly
- Be skeptical — question whether the "obvious" answer actually matches the evidence
- Do not overreach — only present findings supported by artifact evidence

### Step 2 — Present

State the item clearly, then provide:

- **Context**: What the issue is, with relevant quotes or file references
- **Why**: Explain why the change is needed (cite the source: meeting decision, feedback, requirement, plan item)
- **Files**: Identify the specific file(s) that need to be changed
- **Lettered options** (A, B, C, etc.): Each option gets:
  - A short label (e.g., "Accept as-is", "Add validation", "Redesign")
  - A plain-language explanation of what it means and what happens if chosen
  - Any trade-offs or consequences
- Always include at minimum:
  - **(A)** Implement as described (recommended default)
  - **(B)** Skip for now (defer to later)
  - **(C)** Modify the approach (discuss alternatives)
- **Recommendation**: State which option you recommend and a one-sentence rationale

### Step 3 — Wait

**STOP and wait** for the user to respond with a letter. Do NOT proceed, skip ahead, or batch multiple items.

### Step 4 — Apply

Implement the user's chosen option (edit files, update docs, run commands, etc.).

**Post-change obligations (before user review):**
- If any `.puml` files were changed: regenerate SVGs using the pinned PlantUML version — generate IN the corporate repo folder (`diagrams/Service/` or `diagrams/Components/`), copy the outputs to the ticket workspace, then delete the generated SVGs from the corporate repo. See `.github/instructions/plantuml-svg.instructions.md` for the full workflow.
- Ensure all downstream artifacts (SVGs, PR branches) have pending changes ready
- Stage but do NOT commit — the user reviews pending changes first

### Step 5 — Wait Again

After applying the change, **STOP and wait** for the user to confirm before moving on.
- The user reviews all pending changes in their VS Code source control panel
- Do NOT commit or push until the user confirms (e.g., says "ok", "good", "commit", etc.)
- If the user requests modifications, make them and wait for review again

### Step 6 — Commit and Push

Only after the user confirms:
- Stage the changed files (including regenerated SVGs)
- Commit with a descriptive conventional commit message
- Push to the current branch
- If changes affect `udx-architecture-artifacts`, also commit and push to the PR branch

### Step 7 — Next

Present the next item using the same format.

## Session State

- Track which plan items are completed, skipped, or pending
- If a session is interrupted, be able to resume from where it left off
- Use todo list tracking to maintain visibility

## Rules

- **One item at a time** — never present multiple items in a single message
- **Always use lettered options** — every question or choice presented to the user must have lettered options (A, B, C, etc.), even when asking which plan to step through
- **Always investigate before presenting** — no shallow or speculative options
- **Be skeptical** — question assumptions, flag risks, surface non-obvious concerns
- **Keep explanations simple and direct** — no jargon walls
- **Spec wins** — if a claim contradicts an OpenAPI spec or sequence diagram, the artifact is authoritative

## When NOT to Use

- User wants all changes made at once without review
- The "plan" is a single item that can be done immediately
- User explicitly opts out of step-by-step review
