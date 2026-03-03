# Deep Research Prompt: Context Window Management in AI Coding Agents

## Instructions for the Research Agent

You are conducting exhaustive technical research to inform a critical enterprise tooling decision. The Architecture Practice at a Fortune 500 company needs to select between two AI coding toolchains: **Roo Code + Kong AI Gateway** (open-source, usage-based pricing) and **GitHub Copilot** (proprietary, flat-rate pricing). A key differentiator we have identified — but not yet fully quantified — is how each tool manages the LLM context window.

This research will feed directly into an Architecture Decision Record (ADR) that leadership will use to make a procurement decision affecting multiple architect seats. The research must be comprehensive, evidence-based, and cite specific sources. Do not speculate — if you cannot find evidence for a claim, state that clearly.

---

## Background Context You Need to Know

### What We Have Already Discovered

Through source code analysis of Roo Code (open-source, GitHub: RooCodeInc/Roo-Code) and empirical measurement of exported task logs, we found:

1. **Roo Code injects an `<environment_details>` XML block into every user-role message** sent to the LLM. This block is constructed by the function `getEnvironmentDetails()` in `src/core/environment/getEnvironmentDetails.ts`. It contains: all visible VS Code file paths, all open tab paths (up to 20), all active and inactive terminal output, recently modified files, the current ISO timestamp, current session cost, current mode metadata (slug, name, model, role definition, custom instructions), browser session status, and a recursive workspace directory listing of up to 200 files.

2. **In a real task session from our enterprise workspace, we measured 81 environment_details injections consuming 1,885 lines (16.3% of the entire 11,573-line task log).** The largest blocks were 226 lines each (when they included the full workspace file listing). Compact blocks (without file listing) were 21 lines each.

3. **Roo Code's CHANGELOG documents a chronic pattern of context window overflow bugs** (PRs #9442, #8821, issues #1173, and multiple unlabeled fixes for "sliding window overflow," "context window truncation math," "context window size calculation," etc.), suggesting this is an ongoing architectural challenge, not a solved problem.

4. **Roo Code attempted mitigation** with a deduplication filter (tested in `task-tool-history.spec.ts`: "should filter out existing environment_details blocks before adding new ones"), but the recurring bugs suggest the mitigation is incomplete.

5. **GitHub Copilot appears to use selective, server-managed context inclusion** — no equivalent of environment_details is injected into messages, workspace awareness comes from server-side indexing, and conversation history is compressed/summarized rather than sent in full.

### What We Do NOT Yet Know (And Need You to Research)

The gaps in our knowledge are extensive. This is what we need you to fill.

---

## Research Questions — Organized by Priority

### PRIORITY 1: Roo Code Context Window Mechanics (Deep Technical)

1. **Exact token measurement of environment_details blocks.** Using typical tokenizer estimates (cl100k_base for OpenAI-compatible, Claude tokenizer for Anthropic):
   - What is the token count of a compact environment_details block (21 lines: tabs, time, mode)?
   - What is the token count of a full environment_details block (226 lines: includes workspace file listing for a workspace with ~200 files)?
   - What is the token count of Roo Code's default system prompt (the full prompt including tool definitions, persona, and mode instructions)?

2. **Sliding window behavior.** When Roo Code's conversation history exceeds the model's context window:
   - How does Roo Code's sliding window implementation work? What code path handles truncation?
   - Does it truncate from the beginning of the conversation? From the middle? Does it use summarization?
   - Are environment_details blocks preserved, discarded, or compressed during truncation?
   - What is the "keepMessageCount" or equivalent parameter? Is it configurable?
   - What happens to tool call results and tool use blocks during truncation?

3. **Cumulative token waste calculation.** For an N-turn conversation:
   - Confirm or refute our triangular accumulation hypothesis: that total input tokens billed across all API calls for environment metadata follows approximately $\sum_{i=1}^{n} i \times s$ where $s$ is average block token size
   - If the sliding window discards old blocks at some point, what is the actual accumulation curve?
   - What percentage of total billed input tokens in a typical 40-turn and 80-turn task are attributable to environment_details?

4. **Configuration levers.** What settings in Roo Code can reduce context waste?
   - `maxWorkspaceFiles` — what is the minimum? Can it be set to 0? What breaks if it is?
   - `maxOpenTabsContext` — same questions
   - `includeCurrentTime`, `includeCurrentCost` — can these be disabled?
   - Is there any setting to disable environment_details injection entirely?
   - What is the effect of `.rooignore` on context size?
   - Are there any community forks or patches that address context bloat specifically?

5. **The "Power Steering" experiment.** The source code shows that when the `POWER_STEERING` experiment is enabled, the role definition and custom instructions are also injected into the environment_details block. Research:
   - What is Power Steering and what does it add to each environment block?
   - How much additional token overhead does it create?
   - Is it enabled by default?
   - How does this interact with `.roo/rules/` custom instruction files?

### PRIORITY 2: GitHub Copilot Context Management (Deep Technical)

6. **How does GitHub Copilot manage conversation context?** Specifically:
   - Does Copilot send full conversation history to the LLM, or does it summarize/compress prior turns?
   - Is there a known conversation summarization mechanism? At what point does it trigger?
   - How does Copilot handle workspace awareness — does it use RAG, server-side indexing, or some other mechanism?
   - Does Copilot inject any ambient/environmental metadata into messages? If so, what and how much?

7. **Copilot's context window efficiency.** Research:
   - What is Copilot's effective context utilization ratio (tokens available for task work vs total tokens consumed)?
   - How does Copilot handle long multi-step tasks (20+ turns)? Does quality degrade?
   - Does Copilot have an equivalent to Roo Code's sliding window? How does it handle context overflow?
   - What is Copilot's system prompt size? (from any available research, leaked prompts, or documentation)

8. **Copilot Agent mode specifically.** Since our use case is architecture work (not simple code completion):
   - How does Copilot Agent mode manage context differently from Copilot Chat?
   - Does Agent mode use tool calls? If so, how does it manage tool definition overhead in the context?
   - What is the maximum effective conversation length in Agent mode before quality degrades?
   - Does Agent mode have conversation summarization that Chat mode does not?

### PRIORITY 3: Competitive Landscape (Context Management Across Tools)

9. **How do other AI coding agents handle this problem?** Research context management in:
   - **Cursor** (cursor.com) — How does Cursor manage context? Does it inject environment metadata? What is its approach to long conversations?
   - **Windsurf / Codeium** — Same questions
   - **Aider** (aider.chat) — Aider is open-source and well-documented; how does it manage context? Does it have a repo map? How does the repo map compare to Roo Code's file listing approach?
   - **Continue** (continue.dev) — Open-source; how does it handle context?
   - **Claude Code** (Anthropic's CLI agent) — How does Claude Code manage context? Does it inject workspace metadata?
   - **Amazon Q Developer** — As a corporate alternative, how does it manage context?

10. **Best practices and research.** Are there academic papers, technical blog posts, or established patterns for:
    - Optimal context window management in agentic AI systems?
    - The cost of ambient context injection vs on-demand retrieval?
    - Conversation summarization techniques for coding agent conversations?
    - "Context pollution" or "context dilution" — the phenomenon where irrelevant context degrades output quality?

### PRIORITY 4: Cost Impact Quantification

11. **Token pricing analysis.** Calculate the actual dollar cost of context waste for our scenario:
    - **AWS Bedrock pricing** for Claude Sonnet 4 and Claude Opus 4 (our Kong AI backend): input token price, output token price
    - **Anthropic direct API pricing** for the same models (for comparison)
    - Using the cumulative waste formula from question 3, what is the dollar cost of environment_details waste per task for a 40-turn task? An 80-turn task?
    - At 5 architects executing 5-10 tasks per week, what is the monthly dollar waste attributable to environment metadata?

12. **Break-even analysis.** At what usage level does Roo Code's wasted-token overhead make it more expensive than Copilot's flat-rate pricing?
    - GitHub Copilot Business: $39/seat/month
    - GitHub Copilot Enterprise: $39/seat/month (was $39, verify current pricing)
    - At what number of monthly tasks does the context waste cost alone exceed the Copilot flat rate?

13. **Hidden costs beyond tokens.** Research and quantify:
    - Architect time wasted re-explaining context after truncation events
    - Quality degradation cost (rework due to inconsistent AI output after context loss)
    - Configuration and tuning overhead (time spent optimizing `maxWorkspaceFiles`, `.rooignore`, etc.)
    - Are there any studies or anecdotal reports on productivity loss from context window limitations in AI coding tools?

### PRIORITY 5: Mitigation and Solutions

14. **Can Roo Code's context waste be eliminated or significantly reduced?** Research:
    - Is there an open issue or RFC in the Roo Code repository proposing to make environment_details optional?
    - Are there community forks that have addressed this?
    - Could a custom Roo Code mode be configured to minimize environment injection?
    - What would a "minimal environment" configuration look like (all optional components disabled)?
    - If we reduce `maxWorkspaceFiles` to 0, `maxOpenTabsContext` to 0, and disable time/cost/git, what is the irreducible minimum environment_details block?

15. **Alternative architectures for context management.** What approaches could be used instead of broadcast-everything?
    - On-demand retrieval (like Copilot): workspace index + semantic search, only include what's needed
    - Hierarchical summarization: compress old context, preserve recent context
    - External memory / RAG: store conversation history externally, retrieve relevant portions
    - Context caching (Anthropic's prompt caching): does this mitigate the cost of repeated environment blocks?
    - MCP (Model Context Protocol): could MCP servers provide environment state on-demand instead of broadcast?

16. **Anthropic prompt caching specifically.** This is critical for the Roo Code + Bedrock path:
    - Does AWS Bedrock support Anthropic's prompt caching feature?
    - If so, does it cache the repeated portions of environment_details blocks?
    - What is the cache hit rate for environment_details content that is identical across turns?
    - What is the cost difference between cached and uncached input tokens on Bedrock?
    - Could prompt caching effectively neutralize the cost overhead of environment_details?

---

## Output Format Requirements

Structure your response as follows:

### 1. Executive Summary (1 page)
A concise summary of findings with the top 3-5 actionable insights for our toolchain decision.

### 2. Detailed Findings (organized by Priority sections above)
For each research question:
- **Finding**: What you discovered
- **Evidence**: Specific sources (URLs, commit hashes, documentation sections, paper citations)
- **Confidence level**: HIGH (verified from primary sources), MEDIUM (inferred from multiple signals), LOW (limited evidence, stated for completeness)
- **Implications for our decision**: How this affects the Roo Code vs Copilot choice

### 3. Quantitative Analysis
- Token waste calculations with worked examples
- Cost projections for our team size (5 architects)
- Break-even analysis table
- Sensitivity analysis (what if our assumptions about turns-per-task or tokens-per-block are off by 50%?)

### 4. Competitive Matrix
A comparison table of at least 6 AI coding agents across these dimensions:
- Context injection approach (broadcast vs selective vs hybrid)
- Workspace awareness mechanism (file listing vs index vs RAG)
- Conversation history management (full vs sliding window vs summarization)
- Maximum effective conversation length
- Configuration options for context management
- Pricing model impact

### 5. Recommendations
Based on the evidence:
- For the toolchain selection decision specifically
- For mitigating context waste if Roo Code is selected
- For monitoring and measuring context efficiency in production
- For future re-evaluation criteria (when should we revisit this decision?)

### 6. Source Bibliography
Complete list of all sources cited, organized by type (source code, documentation, academic papers, blog posts, community discussions).

---

## Constraints

- **Do not guess.** If you cannot find evidence for a claim, say "insufficient evidence found" and explain what you looked for.
- **Cite everything.** Every factual claim must have a source. Preference for primary sources (source code, official documentation) over secondary (blog posts, forum discussions).
- **Be precise about dates.** AI tooling changes rapidly. Note the date of every source and flag any information that may be outdated (older than 6 months from March 2026).
- **Account for prompt caching.** This is a potential game-changer for the cost analysis. If prompt caching neutralizes the cost of repeated environment_details blocks, that materially changes the recommendation.
- **Consider our specific use case.** We are solution architects, not software developers. Our tasks are longer, more document-heavy, and more multi-step than typical coding tasks. Context window efficiency matters more for us than for someone doing quick code completions.
