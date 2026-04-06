
# Decision Log

## ADR-001: AI Toolchain Selection for Architecture Workflows

| | |
|-----------|-------|
| **Status** | ACCEPTED |
| **Date** | 2026-03-01 |
| **Last Updated** | 2026-03-22 |
| **Phase** | Phase 1 -- AI Tool Cost Comparison |

---

## Context and Problem Statement

Architecture teams evaluating AI-assisted tooling for solution architecture workflows -- from ticket triage and investigation through solution design, review, and publishing -- face a choice among several viable options. The selection must balance cost, quality, standards compliance, and operational fit.

**Which AI toolchain best supports AI-assisted solution architecture work?**

---

## Decision Drivers

- **Monthly cost per architect seat**: Per-seat cost must be justifiable for a multi-architect team
- **Architecture output quality**: AI-generated artifacts must meet arc42, C4, and MADR standards without excessive manual correction
- **Standards compliance**: The toolchain must be configurable to enforce architecture standards automatically
- **Workflow integration**: The toolchain must integrate with a VS Code-based architecture workflow
- **Extensibility**: The toolchain must support future pipeline integration (Phase 3) and custom tooling
- **Model flexibility**: The ability to select and switch between LLM models as pricing and capabilities evolve
- **Corporate governance**: The toolchain must operate within typical enterprise security, procurement, and data handling policies
- **Architecture reliability**: The toolchain must handle complex tool calls, error responses, and long sessions without cascading failures

---

## Considered Options

### Option A: Roo Code + Kong AI Gateway

**Description:** Roo Code is a free, open-source VS Code extension that provides AI-assisted coding and architecture support. Kong AI Gateway routes LLM API requests through an enterprise API gateway to backend model providers (OpenRouter with Claude models).

**Pricing model:** Usage-based. Cost determined by actual token consumption. No per-seat software license fee.

**Cost formula:** `Monthly Cost = (Input Tokens x Rate) + (Output Tokens x Rate)`

**Strengths:**

- Cost scales with actual usage -- light months cost less
- Full model flexibility -- can switch between Claude Sonnet, Haiku, Opus, or other providers
- Custom instruction system (`.roo/rules/`) enables fine-grained standards enforcement per mode
- Open source -- no vendor lock-in on the extension
- Full cost transparency -- exact per-request costs via OpenRouter API
- Supports MCP (Model Context Protocol) for custom tool integration

**Weaknesses:**

- Actual cost is ~$100/run (~$507/month at 38 runs) -- dramatically higher than expected
- Client-side context accumulation causes quadratic cost growth per turn
- Kong AI gateway drops tool calls, obfuscates errors, truncates streams
- Infinite retry vulnerability with no circuit breaker
- No built-in workspace indexing -- requires external Qdrant + embedding provider
- No GitHub ecosystem integration
- Three cascading architectural failures documented (see [Kong Failures](research/kong-failures.md))

### Option B: GitHub Copilot Pro+

**Description:** GitHub Copilot is a commercial AI assistant integrated into VS Code with chat, inline suggestions, agent mode, and workspace indexing. Pro+ plan at $39/seat/month with 1,500 included premium requests.

**Pricing model:** Flat per-seat monthly subscription with intent-based billing (per user prompt, not per token).

**Cost formula:** `Session Cost = User Prompts x Model Multiplier x $0.04`

**Strengths:**

- Predictable monthly cost -- $39/month regardless of usage volume
- Intent-based billing -- autonomous tool calls are free, only user prompts are billed
- Server-side workspace indexing -- automatic, no infrastructure to maintain
- Deep GitHub integration (PR reviews, code suggestions, repository context)
- Agent mode handles 50+ autonomous tool calls per session reliably
- Enterprise tier includes organization-wide policy controls
- 96.1% quality score demonstrated across 5 architecture scenarios

**Weaknesses:**

- Per-seat cost applies regardless of usage volume -- light users pay the same
- No per-request token visibility -- cost estimates are approximations
- Model selection limited to what GitHub offers
- Context summarization during long sessions may cause quality drift
- Fixed cost floor of $39/month even for zero usage

### Option C: Claude Code (Anthropic CLI)

**Description:** Claude Code is Anthropic's official CLI-based coding agent. Terminal-native with direct Anthropic API access, project context via `CLAUDE.md`, and native tool call handling without translation layers.

**Pricing model:** Usage-based. Pay-per-token via direct Anthropic API.

**Cost formula:** `Monthly Cost = (Input Tokens x Rate) + (Output Tokens x Rate)`

**Strengths:**

- Direct Anthropic API -- no translation layer, no gateway failures
- Native error handling -- `context_length_exceeded` handled natively
- Everything Claude Code (ECC) community harness provides 108 reusable skills
- Terminal-native -- lightweight, fast startup
- Built by the model vendor -- optimal integration with Claude reasoning

**Weaknesses:**

- Pay-per-token -- context accumulation costs apply (similar to OpenRouter, likely lower due to direct API)
- No workspace indexing -- relies on `CLAUDE.md` project context and explicit file reads
- Terminal-first -- less visual than VS Code for architecture diagrams and documentation
- Single vendor lock-in to Anthropic models
- No GitHub ecosystem integration
- Cost and quality data pending (limited spike not yet executed)

---

## Evaluation Results

### Cost Comparison

| Metric | Option A (Roo Code) | Option B (Copilot) | Option C (Claude Code) |
|--------|:---:|:---:|:---:|
| Actual per-run cost | ~$100 | **$0.48** | TBD |
| Monthly (38 runs) | ~$507 | **$39** | TBD |
| Per-run cost ratio | ~208x | **1x** | TBD |
| Infrastructure | Kong + Qdrant | None | None |

### Quality Comparison

| Scenario | Option A | Option B | Option C |
|----------|:---:|:---:|:---:|
| SC-01: Ticket Triage (/25) | TBD | 23 (92%) | TBD |
| SC-02: Solution Design (/35) | TBD | 33 (94%) | TBD |
| SC-03: Investigation (/30) | TBD | 30 (100%) | TBD |
| SC-04: Architecture Update (/25) | TBD | 24 (96%) | TBD |
| SC-05: Publishing Prep (/40) | TBD | 39 (98%) | TBD |
| **Total (/155)** | **TBD** | **149 (96.1%)** | **TBD** |

### Reliability Comparison

| Factor | Option A | Option B | Option C |
|--------|---------|---------|---------|
| Workspace indexing | Manual (Qdrant) | Automatic (server-side) | Manual (CLAUDE.md) |
| Tool call fidelity | Poor (Kong drops calls) | High (native) | High (native Anthropic) |
| Error handling | Obfuscated by Kong | Standard | Native Anthropic |
| Context management | Client-side (costly) | Server-side (free) | Client-side (direct API) |
| Retry safety | No circuit breaker | Built-in | Built-in |

---

## Decision Outcome

**Selected option: Option B -- GitHub Copilot Pro+**

GitHub Copilot is recommended as the primary AI toolchain for architecture workflows based on:

1. **Cost:** 208x cheaper per run than Roo Code + OpenRouter ($0.48 vs ~$100), using the same underlying model
2. **Quality:** 96.1% quality score across all 5 evaluation scenarios (149/155)
3. **Reliability:** No gateway translation failures, no infinite retry loops, no context condensing race conditions
4. **Infrastructure:** Zero additional infrastructure required (no Kong gateway, no Qdrant database, no embedding provider)
5. **Predictability:** Fixed $39/month regardless of usage volume, covering ~125 architecture runs within the included allowance

The cost gap is architectural and persistent: intent-based billing with server-side indexing (Copilot) is fundamentally cheaper for agentic architecture workflows than token-based billing with client-side context accumulation (OpenRouter/direct API).

### Claude Code Disposition

Claude Code remains under evaluation as a potential **complement** for specific use cases where its strengths (native Anthropic API, ECC skill harness, terminal-native workflow) may add value. The ECC skill patterns are being adapted for Copilot integration regardless of Claude Code's standalone adoption. A limited spike (1-2 scenarios) will provide cost and quality data to inform whether Claude Code warrants a secondary role.

---

## Consequences

### Positive

- 96.1% quality across all scenarios with minimal manual correction
- $39/month predictable budget per seat
- Zero infrastructure maintenance (no gateway, no vector database)
- Autonomous multi-step execution reduces architect time per scenario
- Deep GitHub ecosystem integration for PR reviews and repository context

### Negative

- No per-request token visibility limits cost optimization opportunities
- Fixed $39/month cost regardless of actual usage volume
- Model selection limited to GitHub's offered models
- Context summarization during very long sessions may degrade quality
- Vendor lock-in to the GitHub/Microsoft ecosystem

### Neutral

- ECC skill patterns are transferable to Copilot's instruction system regardless of this decision
- Roo Code remains viable for organizations with different workload patterns (many short queries vs. few long sessions)
- Claude Code spike results may inform future toolchain evolution

---

## Links

- [Evaluation Framework](evaluation-framework.md)
- [Copilot vs Roo Code Comparison](comparisons/copilot-vs-roocode.md)
- [Copilot Billing Mechanics](research/copilot-billing.md)
- [Kong AI Translation Failures](research/kong-failures.md)
- [Context Management Analysis](research/context-management.md)
