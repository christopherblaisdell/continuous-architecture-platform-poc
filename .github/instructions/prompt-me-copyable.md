# Prompt Me — Copyable Instruction for Other AI Instances

Copy everything below the line and paste it into your AI chat window to set up the "prompt me" behavior.

---

## Instruction: "Prompt Me" Interactive Decision Loop

When I say **"prompt me"**, it means a plan or task list is already in progress. I want you to step through it interactively, one item at a time, with full control over each decision.

### For each item, follow this workflow:

**Step 1 — Investigate**

Before presenting anything, thoroughly research the item using the **authoritative architecture artifacts**. Do not make assumptions — go read the actual files.

Primary sources of truth (check these first):

- **OpenAPI specs** (`architecture/specs/svc-*.yaml`) — the official API contracts for every service. Field names, types, required/optional, enum values, and endpoint definitions live here. If a claim contradicts the spec, the spec wins.
- **PlantUML sequence diagrams** (`architecture/diagrams/Sequence/` and `architecture/diagrams/endpoints/`) — the official cross-service interaction flows. These show who calls whom, in what order, with what data.
- **PlantUML component diagrams** (`architecture/diagrams/Components/`) — the official internal structure of each service and domain.

Supporting sources (check when relevant):

- **AsyncAPI event specs** (`architecture/events/svc-*.events.yaml`) — event schemas and channel definitions
- **Metadata YAML files** (`architecture/metadata/`) — domain classifications, cross-service calls, capabilities, data stores, events catalog
- **Architecture decisions** (`decisions/ADR-*.md`) — settled design constraints that must not be contradicted
- **Existing solution designs** (`architecture/solutions/`) — prior art that may overlap or constrain

Investigation rules:

- Read the actual file content — do not rely on memory or assumptions about what a spec contains
- Cross-reference claims against the OpenAPI spec before presenting options
- If something looks wrong or inconsistent between artifacts, flag it explicitly
- Be skeptical — question whether the "obvious" answer actually matches the evidence
- Do not overreach — only present findings supported by artifact evidence

**Step 2 — Present**

State the item clearly, then provide:

- **Context**: What the issue is, with relevant quotes or file references
- **Lettered options** (A, B, C, etc.): Each option gets:
  - A short label (e.g., "Accept as-is", "Add validation", "Redesign")
  - A plain-language explanation of what it means and what happens if chosen
  - Any trade-offs or consequences
- **Recommendation**: State which option you recommend and a one-sentence rationale

**Step 3 — Wait**

Stop and wait for me to respond with a letter. Do NOT proceed, skip ahead, or batch multiple items.

**Step 4 — Apply**

Implement my chosen option (edit files, update docs, run commands, etc.).

**Step 5 — Wait Again**

After applying the change, stop and wait for me to confirm before moving on.

**Step 6 — Next**

Only after I confirm, present the next item using the same format.

### Rules

- One item at a time — never present multiple items in a single message
- Always investigate before presenting — no shallow or speculative options
- Be skeptical — question assumptions, flag risks, surface non-obvious concerns
- Keep explanations simple and direct — no jargon walls
- If I say "prompt me" with additional context (e.g., "prompt me on the review findings"), use that to identify which plan or list to step through
- If no plan is in progress, ask: "What plan or list should I step through with you?"
