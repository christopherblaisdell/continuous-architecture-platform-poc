# Deep Research Prompt: Platform Landscape

## Objective

This is the most claim-dense page on the site. It contains 4 comparison tables (pricing, context injection, governance, organizational fit), a "Why GitHub Copilot" narrative section, and a competitive risks assessment. Every cell in every table and every assertion in the narrative must be verified against current (mid-2026) documentation.

---

## Claims to Investigate

### 1. Pricing Table — All Five Platforms

**Research questions:**
- **Copilot**: Is Pro+ still $39/mo? Is Business $19/user/mo and Enterprise $39/user/mo? Cite the pricing page.
- **Copilot**: Is the intent-based billing model (per user prompt, not per token) accurately described? Cite the billing documentation.
- **Copilot**: Is Claude Opus 4.6 available at a 3x multiplier? Are GPT-4o and GPT-4.1 truly 0x (unlimited, free)? Cite current multiplier documentation.
- **Cursor**: Is Pro $20/mo and Pro+ $60/mo? Is Teams $40/user/mo? What quota system do they use? Cite the pricing page.
- **Cursor**: Is "3x usage at Pro+" accurate? What does that mean exactly?
- **Windsurf**: Is Pro $20/mo and Max $200/mo? Is Teams $40/user/mo? What is the daily/weekly refresh model? Cite the pricing page. NOTE: Windsurf was acquired by OpenAI — has pricing changed?
- **Cline**: Is Cline still free and open source? What is its current project status? Cite the repository.
- **Claude Code**: Is it part of an Anthropic subscription? What are the actual pricing tiers? Cite the pricing page.

### 2. Context Injection Table

**Research questions:**
- **Copilot**: Is `copilot-instructions.md` the always-on instruction file? Is `.instructions.md` with `applyTo` globs the scoped mechanism? Is `SKILL.md` with progressive disclosure correct? Is `.agent.md` with tool restrictions correct? Cite documentation.
- **Cursor**: Does Cursor use `.cursor/rules/*.md` with "Always Apply"? Do they support Skills marketplace? Cite documentation.
- **Windsurf**: Does Windsurf use `.windsurf/rules/*.md` with "always_on"? Do they support `.windsurf/skills/` with `SKILL.md`? Do they support "Workflows"? Cite documentation.
- **Cline**: Does Cline use `.clinerules/*.md`? Does it support conditional rules with path globs? Cite documentation.
- **Claude Code**: Does Claude Code use `CLAUDE.md`? Does it support subdirectory `CLAUDE.md`? Is it accurate that Claude Code has no Skills or custom agent modes? Cite documentation.
- **AGENTS.md**: Which platforms support `AGENTS.md`? Is Claude Code really the only one that does NOT? Cite sources.
- **MCP**: Do all five platforms support MCP natively? Cite documentation for each.

### 3. Enterprise Governance Table

**Research questions:**
- **SOC 2**: Verify SOC 2 Type II status for Copilot, Cursor, and Anthropic. Is Windsurf's status truly "Not published"? Cite trust/security pages.
- **SSO**: Verify SSO support for each platform at stated tiers. Cite documentation.
- **Data residency**: Does Copilot offer data residency controls? Does Cursor really have "US-primary; no region selection"? Cite documentation.
- **Privacy mode**: Is Copilot's "no code sent for training" claim accurate under Enterprise? What about Business? What about Pro+? Cite terms of service or trust documentation.
- **Cursor Privacy Mode**: Is it "enforced at team level"? Cite documentation.
- **Windsurf zero retention**: Is "Automated zero retention (Teams)" accurate? Cite documentation.

### 4. Organizational Fit Table

**Research questions:**
- **Copilot Multi-IDE**: Does Copilot support VS Code, JetBrains, Xcode, Neovim, Eclipse, AND Zed? Cite current IDE support page.
- **Cursor**: Is Cursor still maintaining a VS Code fork? Do they support JetBrains? Cite documentation.
- **Windsurf**: Does Windsurf still maintain a VS Code fork? Or has OpenAI integrated it into something else? Cite current status.
- **Cline**: Is it truly VS Code only? Cite documentation.
- **Claude Code**: Is it truly terminal only? Or does it have VS Code integration? Cite documentation.

### 5. "A 4-prompt architecture session on Claude Opus 4.6 costs $0.48 on Copilot versus $5-15 on per-token platforms"

**Research questions:**
- Verify the $0.48 calculation: 4 prompts x 3x multiplier x $0.04 = $0.48. Is $0.04 the correct per-premium-request rate?
- What is the actual per-token cost of Claude Opus 4.6 via OpenRouter or direct API? For a typical architecture session (estimating ~100K input tokens, ~5K output tokens), what would the cost be?
- Is $5-15 a reasonable range for a 4-prompt architecture session on per-token billing? Show the calculation.

### 6. "Copilot has the most sophisticated customization hierarchy"

**Research questions:**
- Is this claim defensible? Does any other platform offer equivalent or superior customization?
- What specific features does Copilot have that others lack? What do others have that Copilot lacks?
- Is the claim "Cline is capable but lacks structured abstractions" fair? What abstractions does Cline offer?

### 7. Competitive Risks — Specific Claims

**Research questions:**
- **Cursor Tab and agent-specific fine-tunes**: What are Cursor's custom models? Are they publicly documented? What benchmarks exist?
- **Windsurf SWE-1.5**: Is this a real model? Is it publicly available? What benchmarks exist? What happened to it after the OpenAI acquisition?
- **Claude Code reasoning depth**: Are there benchmarks comparing Claude Code to Copilot on architecture-type tasks?
- **Platform lock-in**: Is AGENTS.md a real standard? Who maintains it? What does it cover? Cite the specification.
- **Agent Skills specification**: Is agentskills.io a real site? What is the Agent Skills specification? Who maintains it?

### 8. Cross-Platform Standard Convergence (AGENTS.md, Agent Skills)

**Research questions:**
- What is the current status of AGENTS.md as a cross-platform standard? Which platforms support it?
- What is the Agent Skills specification? Is it ratified or in draft?
- How much of Copilot's customization is portable via these standards vs proprietary?

---

## Expected Output Format

For each claim:
1. **Claim as stated** — exact quote from the page
2. **Verdict** — Confirmed / Partially Confirmed / Unconfirmed / Incorrect
3. **Evidence** — cited sources with URLs, dates accessed, and relevant excerpts
4. **Recommended correction** — if the claim needs updating, provide the corrected text
5. **Confidence level** — High / Medium / Low based on source quality

Include a summary table at the top with all claims and their verdicts.
