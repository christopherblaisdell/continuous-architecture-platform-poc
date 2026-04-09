<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2614462428/Platform+Landscape -->

# Platform Landscape

## Five Platforms, One Pattern

The AI coding platform market has converged on a common architecture: an IDE-integrated agent that reads workspace files, follows declarative rules, executes tools, and produces code and documentation. Five platforms dominate this space, all offering the capabilities described in [Build vs Leverage](build-vs-leverage.md). The question is not whether platforms can do this — they all can. The question is **which one best fits an enterprise architecture practice.**

This page compares the five platforms across dimensions that matter for this evaluation and concludes with the rationale for why GitHub Copilot is the strongest choice.

---

## Head-to-Head Comparison

### Pricing and Billing Model

| Platform | Individual Plan | Team/Enterprise Plan | Billing Model | Frontier Model Access |
|----------|----------------|---------------------|---------------|----------------------|
| **GitHub Copilot** | $39/mo (Pro+) | $19-39/user/mo (Business/Enterprise) | Fixed per-seat, intent-based (per user prompt, not per token) | Claude Opus 4.6 included at 3x multiplier; GPT-4o/4.1 unlimited (0x) |
| **Cursor** | $20/mo (Pro), $60/mo (Pro+) | $40/user/mo (Teams) | Usage-based with quotas; overages at API pricing | Claude, GPT, Gemini frontier models; Pro+ ($60) provides a $60 monthly credit pool for premium model usage |
| **Windsurf** (Cognition Inc.) | $20/mo (Pro), $200/mo (Max) | $40/user/mo (Teams) | Usage-based with daily/weekly refresh; overages at API pricing | OpenAI, Claude, Gemini; premium models consume quota faster |
| **Cline** | Free (open source) | N/A (self-managed) | Pay-per-token directly to model providers (OpenRouter, API keys) | Any model via API key; user pays full per-token cost |
| **Claude Code** | Part of Anthropic subscription | Via Anthropic API | Token-based billing through Anthropic | Claude models only; no multi-provider |

!!! note "Windsurf Corporate Status (Mid-2026)"
    Windsurf underwent a significant corporate transition in 2026. OpenAI's reported $3B acquisition bid collapsed. Google executed a $2.4B acqui-hire, licensing core technology and hiring Windsurf's CEO and top research scientists. Cognition Inc. (the company behind the Devin autonomous coding agent) subsequently acquired Windsurf's IDE, intellectual property, brand, and enterprise customer contracts. Windsurf is now operated by Cognition Inc. Pricing and feature set remain stable post-acquisition, but the long-term product roadmap is uncertain under new ownership.

**Key insight:** Copilot is the only platform where frontier model usage is absorbed into a fixed monthly price. Every other platform either charges per-token (making frontier models expensive) or uses quota systems where heavy architecture sessions burn through allowances quickly.

### Context Injection and Customization

| Capability | Copilot | Cursor | Windsurf | Cline | Claude Code |
|-----------|---------|--------|----------|-------|-------------|
| Always-on instructions | `copilot-instructions.md` | `.cursor/rules/*.md` (Always Apply) | `.windsurf/rules/*.md` (always_on) | `.clinerules/*.md` | `CLAUDE.md` |
| Scoped instructions | `.instructions.md` with `applyTo` globs | Rules with glob activation | Rules with glob triggers | Conditional rules (path globs) | Subdirectory `CLAUDE.md` |
| Skills / reusable workflows | `SKILL.md` with progressive disclosure | Skills (marketplace) | `.windsurf/skills/` with `SKILL.md` | N/A | Skills via `CLAUDE.md` |
| Custom agent modes | `.agent.md` with tool restrictions | N/A | Workflows (`.windsurf/workflows/`) | Custom modes in settings | Subagents (isolated contexts) |
| `AGENTS.md` support | Yes | Yes | Yes | Yes | N/A |
| MCP support | Native | Native | Native | Native | Native |
| Workspace indexing | Server-side, automatic, incremental | Server-side, automatic | Server-side (Fast Context) | Via API (no built-in) | Local, file reads |

!!! note "Claude Code Capabilities Update"
    Claude Code has expanded significantly beyond its initial terminal-only interface. As of mid-2026, Claude Code offers a dedicated VS Code extension, native support for Subagents (isolated execution contexts for parallel research tasks), and a Skills system (reusable workflows and knowledge stores invoked via `CLAUDE.md`). These capabilities bring Claude Code closer to parity with Copilot and Cursor on customization, though its ecosystem remains Anthropic-only.

**Key insight:** Copilot has the most sophisticated customization hierarchy — instructions, skills, agents, and hooks — all declarative, all version-controlled, all scoped to exactly the right context. Cursor and Windsurf are close behind. Cline uses a structured plan-and-act framework with policy-governed behavior — a different philosophy than Copilot's layered hierarchy but not lacking in capability. Claude Code now offers Skills and Subagents via its VS Code extension, bringing it closer to parity than its initial terminal-only release suggested.

### Enterprise Governance

| Capability | Copilot | Cursor | Windsurf | Cline | Claude Code |
|-----------|---------|--------|----------|-------|-------------|
| SOC 2 | Type II (via GitHub/Microsoft) | Type II | Not published | N/A (OSS) | Type II (Anthropic) |
| SSO (SAML/OIDC) | Yes (GitHub Enterprise Cloud) | Yes (Teams/Enterprise) | Enterprise only | N/A | Via Anthropic org |
| Data residency controls | Yes (GitHub Enterprise) | US-primary; no region selection | Not published | User controls (self-managed) | Anthropic policies |
| Audit trail | GitHub audit log integration | Enterprise: AI code tracking API | Enterprise only | Local logs only | Anthropic API logs |
| Privacy mode / zero retention | Enterprise: no code sent for training | Privacy Mode (enforced at team level) | Automated zero retention (Teams) | User controls API keys directly | Anthropic API terms |
| Admin controls | Organization policy management | Team admin dashboard, model blocklists | Admin dashboard, analytics | N/A | Organization settings |
| Role-based access control | GitHub org/team permissions | Teams/Enterprise | Enterprise only | N/A | Anthropic org roles |

**Key insight:** Copilot inherits GitHub's enterprise governance stack — the same SSO, audit logging, and policy management the organization already uses for source code. Cursor has strong enterprise features but requires a separate governance surface. Windsurf and Claude Code reserve enterprise features for custom contracts. Cline has no governance layer.

### Organizational Fit for This Practice

| Dimension | Copilot | Cursor | Windsurf | Cline | Claude Code |
|-----------|---------|--------|----------|-------|-------------|
| IDE | VS Code (native extension) | Cursor editor (VS Code fork) + JetBrains | Windsurf editor (Cognition Inc.; VS Code fork) + JetBrains | VS Code extension | VS Code extension + Terminal |
| Source control integration | Native GitHub integration (PRs, issues, code review) | Git support, no native GitHub integration | Git support, no native GitHub integration | Git support via terminal | Git support via terminal |
| Existing organizational investment | GitHub is already the source control platform | Separate product, separate vendor | Separate product, separate vendor | Free, but self-supported | Separate vendor |
| Procurement complexity | Add seats to existing GitHub contract | New vendor, new contract | New vendor, new contract | No procurement (OSS) | New vendor, new contract |
| Extension ecosystem | Full VS Code marketplace | VS Code marketplace (compatibility varies) | Windsurf marketplace | Full VS Code marketplace | N/A |
| Multi-IDE support | VS Code, JetBrains, Xcode, Neovim, Eclipse, Zed | Cursor editor, JetBrains | Windsurf editor, JetBrains | VS Code only | Terminal only |

**Key insight:** The organization already uses GitHub for source control. Copilot is the only platform that is a natural extension of the existing toolchain — same vendor, same contract, same governance surface, same SSO, same audit trail. Every other platform introduces a new vendor relationship, a new procurement process, and a new governance surface to manage.

---

## Why GitHub Copilot

The comparison above reveals that while all five platforms share the same core architecture (workspace-aware agent with declarative customization), they differ significantly on three dimensions that matter for enterprise adoption:

### 1. Cost Structure Favors Architecture Work

Architecture sessions are long, context-heavy, and model-intensive. A single solution design session may involve 10-20 file reads, 4-6 user prompts, and extensive reasoning across specs, ADRs, metadata, and source code. Per-token billing makes these sessions expensive. Copilot's intent-based billing (per user prompt, not per token) makes them cheap.

A 4-prompt architecture session on Claude Opus 4.6 costs **$0.48 on Copilot** versus **$5-15 on per-token platforms** depending on context size. Over 20 sessions per month, that is $9.60 vs $100-300 — and the Copilot cost is absorbed in the $39 flat fee.

See [Model Quality at Budget](model-quality-at-budget.md) for why this cost structure also determines which model tier each option actually uses.

### 2. Customization Maturity Matches the Use Case

The architecture practice has already built a sophisticated workspace-as-code configuration:

- 500+ line `copilot-instructions.md` defining the Solution Architect role, 19-service domain model, architectural standards, and safety constraints
- Scoped `.instructions.md` files for security context, OpenAPI design rules, and solution review checklists
- Mock tool scripts accessed via MCP for JIRA, Elastic, and GitLab simulation
- 4 completed solution designs demonstrating the workflow in production

This configuration relies on Copilot's instruction hierarchy (global → scoped → skills → agents). Migrating to another platform would require rewriting all customization files into that platform's format — a non-trivial effort with no quality improvement. The cross-platform `AGENTS.md` standard helps but does not cover Copilot's more advanced features like skills, hooks, and agent modes.

### 3. Zero Procurement Friction

Adding Copilot seats to an existing GitHub contract is an IT operations task, not a procurement project. Every other platform requires:

- New vendor evaluation and approval
- New contract negotiation
- New SSO integration
- New data governance assessment
- New audit trail integration

For a practice that wants to start delivering architecture value immediately, procurement friction is a hidden cost measured in months, not dollars.

---

## Competitive Risks and Honest Assessment

No evaluation is complete without acknowledging where alternatives have advantages:

| Risk | Assessment |
|------|-----------|
| **Cursor's agent quality** | Cursor invests heavily in custom models (Tab, agent-specific fine-tunes). If Cursor's agent produces meaningfully better architecture output, that could outweigh cost and governance advantages. This is testable. |
| **Windsurf's SWE-1.5 model (Cognition Inc.)** | Following Cognition Inc.'s acquisition of Windsurf, the proprietary SWE-1.5 agent model continues to be developed. If it excels at architecture work specifically, it deserves consideration — though the uncertain post-acquisition roadmap and potential Devin integration add strategic risk. |
| **Cline's full transparency** | Cline's open-source model gives complete visibility into agent behavior — every prompt, every decision, every token. For governance-sensitive environments, this transparency has real value. |
| **Claude Code's reasoning depth** | Claude Code running Claude Opus 4.6 natively may produce deeper reasoning than Copilot's integration. With its new VS Code extension, the workflow fit concern is largely resolved — the reasoning quality and native Subagent architecture are worth benchmarking. |
| **Platform lock-in** | Copilot's advanced customization features (skills, hooks, agent modes) are proprietary. The `AGENTS.md` standard and instruction file content are portable, but the activation mechanisms are not. |

These risks inform the [Evaluation Approach](../framework/evaluation-approach.md): test Option A (Copilot) and Option B (alternative platform) empirically before committing. If a competitor produces measurably better architecture output, the evidence will show it.

---

## Implications for DD-03 (AI Provider)

This landscape analysis provides the evidence base for DD-03 (AI Provider Selection). The formal decision will reference this comparison and apply the [Evaluation Methodology](../framework/evaluation-methodology.md) scoring to reach a defensible recommendation.

The five platforms map to the three evaluation options as follows:

| Evaluation Option | Platform(s) | Rationale |
|-------------------|------------|-----------|
| **Option A** | GitHub Copilot | Best cost structure, deepest customization, zero procurement friction, existing organizational fit |
| **Option B** | Roo Code + Kong (or Cursor/Windsurf as alternative) | Represents the "different platform + custom gateway" approach |
| **Option C** | Bespoke agent (Azure AI Foundry) | Custom-built, does not use any existing platform |

---

**See also:**

- [Build vs Leverage](build-vs-leverage.md) — Why all five platforms eliminate the need for custom RAG
- [Architecture Is Not Just Coding](architecture-not-just-coding.md) — Evidence that these platforms handle architecture work, not just code
- [Model Quality at Budget](model-quality-at-budget.md) — Why Copilot's fixed pricing delivers better model quality than per-token alternatives
- [Evaluation Approach](../framework/evaluation-approach.md) — How to test these claims empirically
- [Option D — Hybrid Architecture](option-d-hybrid-architecture.md) — How BYOK support enables a hybrid approach that combines Copilot's platform with a custom Foundry model
