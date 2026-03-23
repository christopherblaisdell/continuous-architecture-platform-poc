# Claude Code

## Tool Profile

| | |
|---|---|
| **Type** | CLI-based coding agent |
| **IDE Integration** | Terminal-native; VS Code integration via extension |
| **Agent Mode** | Yes -- autonomous multi-step execution |
| **Pricing** | Pay-per-token via Anthropic API (direct) |
| **Model Used** | Claude Opus 4.6 (native Anthropic API) |
| **Workspace Indexing** | Built-in project context and CLAUDE.md |
| **Vendor** | Anthropic |

!!! warning "Spike Pending"
    Claude Code has not yet been tested against the NovaTrek evaluation scenarios. The information below is based on public documentation and the Everything Claude Code (ECC) community harness analysis. A limited 1-2 scenario spike is planned to gather real cost and quality data.

---

## Architecture

Claude Code is Anthropic's official coding agent, designed as a terminal-native tool that operates directly against the Anthropic API without intermediate gateways or translation layers.

### Key Architectural Characteristics

| Characteristic | Detail |
|---------------|--------|
| API access | Direct Anthropic API (no proxy, no translation layer) |
| Context management | Built-in truncation and compaction tuned to Claude model token bounds |
| Tool call format | Native `tool_use` -- no OpenAI translation required |
| Error handling | Designed around Anthropic's error taxonomy; `context_length_exceeded` handled natively |
| Project context | `CLAUDE.md` file (analogous to Copilot's `copilot-instructions.md`) |

### Why Claude Code Bypasses Kong Failures

The three architectural limitations identified in the [Roo Code + Kong](roo-code-kong.md) stack do not apply to Claude Code:

1. **No translation layer:** Claude Code speaks native Anthropic API. No Lua-based JSON transformation means no empty tool results, no error obfuscation, no streaming fragility.
2. **Native error handling:** `context_length_exceeded` is received in its original format. The agent can respond appropriately (compress, truncate, or alert).
3. **Direct API billing:** No gateway rate limiting race conditions. Cost is transparent and immediate.

---

## Pricing

Claude Code uses Anthropic's direct API pricing. As of March 2026:

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| Claude Opus 4.6 | Variable | Variable |
| Claude Sonnet 4 | Variable | Variable |

**Cost characteristics:**

- Pay-per-token with no subscription floor
- Context accumulation costs apply (similar to OpenRouter)
- No intent-based billing subsidy (unlike Copilot)
- Prompt caching may reduce repeated context costs

**Projected cost per architecture run:** Unknown -- pending spike execution. Expected to be higher than Copilot ($0.48) due to per-token billing, but potentially lower than OpenRouter (~$100) due to direct API access without gateway overhead.

---

## Everything Claude Code (ECC) Integration

The [Everything Claude Code](https://github.com/affaan-m/everything-claude-code) repository is a mature community-driven harness providing 108 skills, 25 specialized agents, 57 commands, and automated hooks for Claude Code.

### Relevance to NovaTrek

The ECC harness was analyzed for incorporation into the NovaTrek Copilot workflow. Skills were classified into three tiers:

### Tier 1 -- Directly Applicable (13 skills)

| ECC Skill | NovaTrek Use Case | Priority |
|-----------|------------------|----------|
| `skills/api-design/` | OpenAPI spec design and review for 19 microservices | CRITICAL |
| `skills/deep-research/` | Multi-source investigation for architecture tickets | CRITICAL |
| `skills/search-first/` | Prior-art discovery before new solution designs | CRITICAL |
| `agents/architect.md` | System design delegation pattern | HIGH |
| `agents/planner.md` | Breaking down complex solution designs | HIGH |
| `skills/security-review/` | Security assessment for PII flows, auth, waivers | HIGH |
| `skills/java-coding-standards/` | Analyzing NovaTrek Java source code | HIGH |
| `skills/springboot-patterns/` | Spring Boot service analysis (17 of 19 services) | HIGH |
| `skills/database-migrations/` | Schema migration guidance for solution impacts | HIGH |
| `rules/common/security.md` | Security checklist for all reviews | HIGH |
| `contexts/research.md` | Research mode for investigation scenarios | HIGH |

### Tier 2 -- Valuable Enhancements (9 skills)

Docker patterns, PostgreSQL patterns, Spring Boot security, JPA patterns, security reviewer agent, database reviewer agent, verification loop, continuous learning, MCP server patterns.

### Tier 3 -- Future Value (7 skills)

TDD workflow, deployment patterns, enterprise agent ops, autonomous loops, agentic engineering, eval harness, strategic compact.

### Adaptation Strategy

ECC skills are designed for Claude Code's agent harness. For Copilot integration, they are **adapted, not directly copied**:

| Claude Code Concept | Copilot Equivalent |
|--------------------|-------------------|
| `CLAUDE.md` | `.github/copilot-instructions.md` |
| `skills/X/SKILL.md` | `.instructions.md` (folder-scoped) |
| `agents/X.md` | Copilot subagents via `runSubagent` |
| `rules/common/*.md` | Sections in `copilot-instructions.md` |
| `commands/X.md` | `.prompt.md` files |
| `hooks/hooks.json` | No direct equivalent (manual checkpoints) |

---

## Planned Spike

A limited 1-2 scenario spike will execute SC-02 (Solution Design) and SC-03 (Investigation) using Claude Code against the NovaTrek workspace. This will produce:

- Actual per-run cost data (comparable to Copilot's $0.48 and OpenRouter's ~$100)
- Quality scores using the same rubrics
- Assessment of terminal-native workflow fit for architecture tasks
- Comparison of Claude Code's native context management vs. Copilot's server-side indexing

The spike results will be published to this site when available.

---

## Strengths (Expected)

1. **No translation layer** -- direct Anthropic API eliminates the Kong failure modes
2. **Native error handling** -- context window management designed for Claude models
3. **ECC community harness** -- 108 skills provide structured workflows for architecture tasks
4. **Terminal-native** -- lightweight, no heavy IDE dependency
5. **Model alignment** -- built by the same company that builds the model

---

## Limitations (Expected)

1. **Pay-per-token** -- no intent-based billing subsidy; context accumulation costs apply
2. **Terminal workflow** -- less visual than VS Code-integrated tools for architecture diagrams and documentation
3. **No GitHub ecosystem** -- no PR review, no repository context indexing (comparable to Roo Code gap)
4. **Single vendor** -- locked to Anthropic models only
5. **ECC maturity** -- community harness, not an enterprise-supported product
