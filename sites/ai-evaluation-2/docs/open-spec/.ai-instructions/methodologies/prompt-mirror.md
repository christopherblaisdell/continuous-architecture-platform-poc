# Prompt Mirror — Context Capture System

<!-- PAIRED FILE: This content must stay in sync with .github/instructions/prompt-mirror.instructions.md -->
<!-- If you edit this file, update the paired file to match. Run: scripts/validate-ai-instructions.sh -->

**Applicable Modes**: All modes
**Instruction File**: `.github/instructions/prompt-mirror.instructions.md` (applyTo: `**`)

## Purpose

Every AI chat interaction is saved as a context-enriched markdown file in `prompt-mirror/`. Each file reads as a natural user request with all necessary context inlined (file contents, URLs, workspace structure). There is no trace that another AI has already handled the request.

## Why This Exists

- Roo Code does not have workspace-level indexing or automatic context discovery
- A self-contained prompt file provides all context needed to act on the request
- The file must read as a direct user request — no review framing, no response summaries
- This methodology ensures every interaction can be independently re-executed

## Mirror File Location

```
prompt-mirror/YYYY-MM-DD-HHMMSS-short-description.md
```

## Mirror File Format

Each file reads as a natural user request:

1. **The user's request** — verbatim or lightly paraphrased to be self-contained (comes first)
2. **Inline context** — file contents, URLs, and artifacts needed to act on the request
3. **Workspace structure** — relevant directory layout if needed

**Critical rules:**

- Must read as if the user is typing the request directly
- NO metadata headers (no "Timestamp:", "Source:", "Workspace:" lines)
- NO response summaries or review requests
- NO indication that another AI has already handled this
- The request comes FIRST, then context follows naturally

## Context Gathering Rules

Include:
- Any files read, searched, or modified during the interaction
- URLs consulted with key findings
- Architecture artifacts (OpenAPI specs, PlantUML diagrams, AsyncAPI specs) if relevant
- Decision context (ADRs, solution designs)
- Error messages and stack traces if debugging
- Terminal output from commands run

Exclude:
- Entire large files when only a section matters
- Credentials or tokens (redact with `[REDACTED]`)
- Binary file contents
- Any indication of prior AI processing

## Workflow

### Automatic (Every Interaction)

Every interaction triggers mirror file creation. This is non-negotiable.

1. Perform the requested work
2. Create the mirror file with full context (as a direct user request)
3. `git add prompt-mirror/` (file gets committed with the actual work)

### User Workflow

1. Open the latest file in `prompt-mirror/`
2. Copy the content
3. Paste into Roo Code chat
