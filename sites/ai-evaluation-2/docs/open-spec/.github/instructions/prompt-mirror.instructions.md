---
applyTo: "**"
---

<!-- ============================================================
     DERIVED FILE — DO NOT EDIT DIRECTLY
     Canonical source: .ai-instructions/methodologies/prompt-mirror.md
     To make changes: /opsx:propose "description of change"
     Then run: scripts/sync-ai-instructions.sh
     Validation: scripts/validate-ai-instructions.sh
     Governance: openspec/specs/ai-instruction-governance/spec.md
     ============================================================ -->

# Prompt Mirror — Context Capture System

<!-- PAIRED FILE: This content must stay in sync with .ai-instructions/methodologies/prompt-mirror.md -->
<!-- If you edit this file, update the paired file to match. Run: scripts/validate-ai-instructions.sh -->

**MANDATORY**: This instruction applies to EVERY interaction in this chat window. There are NO exceptions.

## What This Does

Every time the user types anything in this chat window, you MUST save a context-enriched prompt file to `prompt-mirror/`. The file must read as if the user is sending the request directly — with all necessary context and file contents inlined. There must be NO trace that another AI has already handled the request.

## Workflow — Every Single Interaction

### Step 1 — Perform the requested work normally

Respond to the user's request as you normally would. Complete the task, answer the question, etc.

### Step 2 — Create the mirror file

After completing your response, create a markdown file in `prompt-mirror/` with this naming convention:

```
prompt-mirror/YYYY-MM-DD-HHMMSS-short-description.md
```

Use the current timestamp and a 2-4 word kebab-cased description of the request.

### Step 3 — Mirror file contents

The file must read as a natural user request with inline context. Use this structure:

```markdown
[The user's request — verbatim or lightly paraphrased to be self-contained.
If the original request references prior conversation context, incorporate that
context so the request stands alone.]

Here is the relevant context for this task:

### [relative/path/to/file.ext]

\`\`\`[language]
[Include the relevant content from the file — not the entire file unless small,
but enough to act on the request without workspace indexing.
For large files, include the specific sections that matter.]
\`\`\`

### [Another file or resource if needed]

[Continue with additional context as needed.]

### Workspace Structure

\`\`\`
[Include relevant directory tree if the request involves file creation,
navigation, or understanding project layout]
\`\`\`
```

**Critical rules for the mirror file:**

- It must read as if the user is typing the request directly
- NO headers like "AI Response Summary", "Review Request", or "Original Request"
- NO metadata headers (no "Timestamp:", "Source:", "Workspace:" lines)
- NO request for review or assessment — it is a direct task request
- NO indication that another AI has already handled this
- The user's request comes FIRST, then supporting context follows naturally
- Context sections use `###` headers with file paths or descriptive labels

### Step 4 — Git add the mirror file

Run `git add prompt-mirror/` after creating the file. Do NOT commit — the mirror file gets committed alongside the actual work when you commit and push.

## Context Gathering Rules

When building the mirror file, you MUST include:

1. **Referenced files**: Any file you read, searched, or modified during the interaction — include the relevant portions
2. **URLs consulted**: Any web pages fetched — include key findings
3. **Architecture artifacts**: If OpenAPI specs, PlantUML diagrams, or AsyncAPI specs were relevant — include the relevant portions
4. **Decision context**: If ADRs or solution designs informed your response — reference them
5. **Error context**: If debugging, include the error messages and stack traces
6. **Terminal output**: If commands were run, include relevant output

## What NOT to Include

- Entire large files when only a section matters — excerpt the relevant parts
- Sensitive credentials or tokens (redact with `[REDACTED]`)
- Binary file contents
- Any indication that another AI has already processed this request
- Response summaries, review requests, or assessment prompts

## File Size Guidelines

- Target: 100-500 lines for typical interactions
- Maximum: 1000 lines — if more context is needed, split into referenced files
- Minimum: 30 lines — even simple questions need enough context to be actionable
