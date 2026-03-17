# OpenSpec Evaluation: Why Native AI Tool Customization Wins

**Date**: 2026-03-17
**Status**: Decided — Do Not Adopt

---

## What Is OpenSpec?

OpenSpec is a **spec-driven development workflow framework** for AI coding agents (v1.2.0, Fission AI, 31.5k GitHub stars, MIT license). It structures how AI assistants plan and implement changes using folder-based artifacts (`proposal.md`, `specs/`, `design.md`, `tasks.md`), YAML dependency schemas, and slash commands (`/opsx:propose`, `/opsx:archive`). It supports 20+ AI tools natively.

The question: does OpenSpec provide enough value over native AI tool customization (`.instructions.md`, `copilot-instructions.md`, prompt templates) to justify adopting it?

**No.**

---

## What OpenSpec Offers

| OpenSpec Advantage | Why It Doesn't Matter |
|---|---|
| **Multi-tool portability** — works across 20+ AI tools (Claude Code, Cursor, Copilot, Windsurf, etc.) | If you're using one AI tool, this is worthless. You only need portability when you're actually switching tools — and that day may never come. |
| **Schema-enforced artifact ordering** — YAML dependency graph forces "proposal before design before tasks" | `.instructions.md` files achieve the same thing through convention, and AI compliance is high. Schema enforcement solves a problem that rarely manifests in practice. |
| **Slash commands** (`/opsx:propose`, `/opsx:archive`) — standardized workflow triggers | AI Agent Mode already handles multi-step workflows through instruction files. Slash commands are a convenience, not a capability gap. |

---

## What Native AI Tool Customization Gives You That OpenSpec Cannot

| Native Customization Advantage | Why It Matters |
|---|---|
| **Architecture-specific artifacts** — MADR decisions, per-service impact assessments, capability tracking, risk registers, assumption registers | OpenSpec's flat model (proposal/specs/design/tasks) has no concept of any of these. They are the core of architecture governance — not optional extras. |
| **Zero dependency** — no npm package, no startup risk, no framework to learn or maintain | OpenSpec is v1.2.0 from a startup (Fission AI) with no foundation governance (not FINOS, not Linux Foundation). GitHub stars reflect developer interest, not enterprise suitability. |
| **Full content control** — `.instructions.md` can enforce document structure (e.g., "MADR must have Status, Date, Context, Decision Drivers, 2+ Options, Outcome, Consequences") | OpenSpec schemas only validate that **files exist**, not **what is inside them**. You cannot enforce MADR structure, impact assessment completeness, or risk register format through OpenSpec schemas. |
| **Custom metadata workflows** — capability changelog rollups, portal generation triggers, ticket integration, CI governance rules | OpenSpec cannot trigger business logic on archive. It cannot update a capability changelog, regenerate portal pages, or integrate with ticket systems. These require custom tooling regardless. |

---

## The Core Problem

OpenSpec was designed for **feature development** — shipping code changes with AI assistance. Architecture governance is a fundamentally different activity that requires:

- Structured decision records with options analysis and trade-offs
- Per-service impact assessments across a microservice landscape
- Capability model tracking that feeds dashboards and portal generators
- Dedicated assumptions, risks, and guidance artifacts separated from design documents

OpenSpec merges all of these into its flat proposal/design model or omits them entirely. Adopting OpenSpec for architecture work means building custom tooling on top of it to fill the gaps — at which point the framework adds cost without proportional value.

---

## Decision

**Do not adopt OpenSpec.** Native AI tool customization (`.instructions.md`, `copilot-instructions.md`, prompt templates) is simpler, more powerful for architecture work, and free.

OpenSpec adds a layer of indirection that would be useful if you were switching AI tools frequently. If you are not, every feature OpenSpec provides is either unnecessary or already achievable through native customization — with the added benefit of full content control that OpenSpec's schema model cannot match.

### When to Revisit

- The team adopts a **second AI coding tool** and needs portable workflow instructions
- **Workflow enforcement becomes a real pain point** despite instruction file improvements
- OpenSpec achieves **foundation governance** and demonstrates enterprise architecture adoption
- OpenSpec adds **architecture-specific features** (MADR templates, impact tracking, metadata rollup hooks)

---

## Source Material

| Source | Access Date |
|--------|-------------|
| OpenSpec website (openspec.dev) | 2026-03-17 |
| OpenSpec GitHub (github.com/Fission-AI/OpenSpec) | 2026-03-17 |
| OpenSpec concepts docs (docs/concepts.md) | 2026-03-17 |
| OpenSpec OPSX workflow docs (docs/opsx.md) | 2026-03-17 |
| OpenSpec getting started (docs/getting-started.md) | 2026-03-17 |
