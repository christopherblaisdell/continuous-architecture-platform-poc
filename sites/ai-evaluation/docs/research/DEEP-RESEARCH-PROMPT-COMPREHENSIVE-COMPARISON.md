# Deep Research Prompt: Comprehensive AI Toolchain Comparison for Enterprise Architecture

> Paste this entire document into AI deep research (e.g., ChatGPT Deep Research, Perplexity, Gemini Deep Research). The prompt is structured to produce a single comprehensive report covering all open questions in our AI toolchain evaluation.

---

## PROMPT START

I am evaluating three AI coding assistant toolchains for enterprise solution architecture work. I need a comprehensive, heavily sourced research report covering every topic listed below. For each topic, cite specific sources (official documentation, GitHub issues, blog posts, pricing pages, changelogs, community discussions). Do not guess — if current data is unavailable, state that explicitly.

### Context

We are a solution architecture team evaluating AI toolchains for daily architecture work: solution design, ticket triage, OpenAPI spec maintenance, investigation of production issues, architecture decision records (ADRs), and PlantUML diagram generation. Our workloads involve long multi-step agentic sessions (40-60 tool calls per session) against a large workspace (19 microservices, 700+ lines of workspace instructions).

We have completed a controlled evaluation using the same AI model (Claude Opus 4.6) across two toolchains: GitHub Copilot Pro+ and Roo Code + OpenRouter (via Kong AI Gateway). A third toolchain (Claude Code by Anthropic) is under consideration. All three produce comparable architecture output quality — the differences are in cost, reliability, context management, and ecosystem integration.

### What We Know (Verified)

- **GitHub Copilot Pro+ costs $0.48 per architecture run** (4 user prompts × 3x Claude Opus 4.6 multiplier × $0.04/request). Intent-based billing charges per user prompt only; autonomous tool calls are free.
- **Roo Code + OpenRouter costs ~$100 per equivalent run** due to per-token billing with client-side context accumulation (quadratic cost growth per turn).
- **Copilot has server-side workspace indexing** — automatic vector database on GitHub servers, transparent to the user, retrieval is free and proactive.
- **Roo Code has no built-in workspace indexing** — requires external Qdrant + embedding provider. The "Codebase Indexing" checkbox in Roo Code settings is greyed out until external infrastructure is configured. Even when enabled, retrieval is reactive (LLM must explicitly request it) and billed at token rates.
- **Kong AI Gateway has three documented failure modes**: (1) empty tool results from Lua translation bugs, (2) error obfuscation stripping `context_length_exceeded`, (3) streaming fragility truncating tool call arguments.
- **Roo Code has an infinite retry vulnerability** when Kong drops tool calls — no circuit breaker, no maximum retry limit.
- **Both tools scored comparably on quality** — Copilot scored 149/155 (96.1%) across 5 architecture scenarios; Roo Code produced 37 comparable files but scoring is pending.

---

## Research Questions

### SECTION 1: Workspace Indexing and Context Awareness (Comprehensive)

1. **How exactly does GitHub Copilot's workspace indexing work?** Describe the full pipeline: when is the index built, where is it stored, what embedding model is used, how is retrieval triggered, how are results injected into the prompt, and what is the token budget for retrieved context? Cite GitHub's official documentation, VS Code extension source code references, and any engineering blog posts.

2. **How does Copilot's `@workspace` and automatic context injection differ?** In agent mode, does Copilot inject workspace context automatically (proactively) into every prompt, or only when the agent explicitly requests it via a tool call? Is there a difference between chat mode `@workspace` queries and agent mode context injection?

3. **How does Roo Code's codebase indexing work when fully configured?** What embedding providers are supported (OpenAI, Google, Ollama — which models specifically)? What vector database backends are supported beyond Qdrant? What is the indexing latency for a 19-service workspace? How does the `codebase_search` tool call work — what parameters does it accept, how many results does it return, and how are results ranked?

4. **What is the architectural difference between proactive and reactive context injection?** Copilot reportedly injects relevant context before the model begins reasoning. Roo Code requires the model to issue an explicit `codebase_search` call. Research whether this proactive/reactive distinction is accurate, and what evidence exists about its impact on output quality and hallucination rates.

5. **How does Claude Code handle workspace context?** Claude Code uses `CLAUDE.md` files and has built-in project context. Does it index the full workspace like Copilot? How does it decide what context to include? Does it use vector search, grep, or some other mechanism? How does its context awareness compare to Copilot's server-side indexing?

6. **How does Cursor's workspace indexing compare?** Cursor is another AI coding tool with workspace indexing. Include it in the comparison — how does its indexing architecture compare to Copilot's and Roo Code's? Is it proactive or reactive? What is the cost model?

7. **How does Augment Code's workspace indexing compare?** Augment Code advertises deep codebase understanding. How does its indexing work? How does it compare architecturally to Copilot and Roo Code?

8. **What is the current state of Cline's workspace indexing?** Cline is a competitor to Roo Code. Does it have built-in workspace indexing? If so, how does it compare?

### SECTION 2: GitHub Copilot Billing — Current State (March 2026)

9. **What are the current Copilot Pro+ model multipliers?** List ALL models available in Copilot Pro+ with their exact multipliers as of March 2026. Specifically confirm: Is Claude Opus 4.6 still 3x? Is GPT-4.1 still 0x? What about Claude Sonnet 4, Gemini models, o3, o4-mini? Has the 30x Claude Opus 4.6 fast preview changed?

10. **Has intent-based billing changed?** Confirm that Copilot still bills per user prompt only and that autonomous tool calls remain free. Has GitHub announced any changes to this model? Are there any signals that tool calls may become billable in the future?

11. **What is the current state of Copilot's quota system?** Confirm 1,500 premium requests/month for Pro+. Has this changed? What happens when the quota is exhausted — does it fall back to 0x models or stop entirely?

12. **Are sub-agent invocations still free?** We documented a telemetry bug where `runSubagent` erroneously triggered premium request deductions. Has this been fixed? Are sub-agents confirmed free?

13. **What is Copilot Enterprise vs Pro+ pricing?** For a team of 5-10 architects, what is the per-seat cost difference between Pro+, Business, and Enterprise? Do Enterprise features (knowledge bases, fine-tuning) justify the price difference for architecture work?

### SECTION 3: Roo Code Current State and Roadmap

14. **What is Roo Code's current version and recent changelog?** What major features or fixes have been released since March 2026? Has workspace indexing been improved? Has the infinite retry vulnerability been fixed?

15. **Has Roo Code added built-in workspace indexing?** Is external Qdrant still required, or has Roo Code added a built-in indexing solution? If still external, has the configuration been simplified?

16. **Has Roo Code fixed the infinite retry loop?** Is there now a maximum retry limit for empty assistant responses? Has a circuit breaker been implemented?

17. **What is Roo Code's context condensing state?** Has the context condensing mechanism been improved to handle rate limiting failures? Is there a fallback when condensing is blocked?

18. **How does Roo Code compare to Cline at this point?** Roo Code forked from Cline. What are the current meaningful differences between the two? Has one pulled ahead on reliability, features, or community support?

### SECTION 4: Kong AI Gateway vs Alternatives

19. **Has Kong fixed the ai-proxy tool call translation bugs?** Specifically: empty tool results for complex nested JSON, `tool_choice` schema mismatch (string vs dictionary), error obfuscation stripping `context_length_exceeded`, streaming truncation of tool call arguments. Check Kong changelogs for versions 3.8+, 3.9+, and 3.10+.

20. **Has Kong added native Anthropic format passthrough?** We documented that `config.llm_format = "anthropic"` in Kong v3.10+ should bypass the Lua translation. Has this been released and confirmed working?

21. **How do LiteLLM, Portkey, and OpenRouter compare as AI gateways?** For each: tool call fidelity, error preservation, streaming stability, rate limiting behavior, and pricing. Which is the most reliable for Anthropic Claude in agentic VS Code extension workflows?

22. **Is there a "best practice" gateway architecture for AI coding assistants in 2026?** What do enterprise teams actually deploy? Direct API, thin proxy (LiteLLM), managed gateway (Kong/Portkey), or managed service (OpenRouter)?

### SECTION 5: Claude Code Deep Dive

23. **What is Claude Code's current pricing model?** Provide exact per-token rates for Claude Opus 4.6, Claude Sonnet 4, and any other models. Is there a subscription option? What would a typical 40-60 turn architecture session cost?

24. **How does Claude Code's context management work?** Describe the internal truncation, compaction, and summarization mechanisms. How does it compare to Copilot's server-side summarization and Roo Code's client-side condensing?

25. **Does Claude Code have workspace indexing?** How does it discover and read files? Does it use `CLAUDE.md` only, or does it also build a semantic index of the workspace? How does it compare to Copilot's automatic indexing?

26. **How does Claude Code handle tool calls?** Since it uses native Anthropic API, are the Kong translation failures irrelevant? What is the tool call reliability compared to Copilot's tool infrastructure?

27. **What is the Everything Claude Code (ECC) community harness?** Current status, adoption, quality of skills/agents, and maintenance state. Is it production-ready for enterprise architecture workflows?

28. **How does Claude Code integrate with VS Code?** Is there a VS Code extension, or is it terminal-only? What is the workflow experience like compared to Copilot's native VS Code integration?

29. **What is Claude Code's MCP (Model Context Protocol) implementation?** How does it compare to Copilot's MCP support and Roo Code's MCP support? Which is more mature?

### SECTION 6: Emerging Competitors and Market Landscape

30. **What AI coding assistants should we be tracking in 2026?** Beyond Copilot, Roo Code, Claude Code, Cursor, and Augment — what other tools are relevant for enterprise architecture work? Consider: Amazon Q Developer, JetBrains AI, Tabnine, Sourcegraph Cody, Windsurf, Devin, etc.

31. **Which tools have agent mode (autonomous multi-step execution)?** For each tool in the landscape, does it support agentic workflows comparable to Copilot's Agent Mode?

32. **Which tools have workspace indexing?** For each tool, what level of workspace awareness does it provide — none, reactive (on-demand search), or proactive (automatic context injection)?

33. **What is the pricing landscape for AI coding assistants as of March 2026?** Create a comprehensive comparison table: subscription cost, per-token cost (if applicable), included quotas, model availability, and effective cost for a "typical architecture session" (analogous to our 4-prompt, 50-turn workload).

### SECTION 7: Context Window and Cost Economics

34. **How do different context management strategies affect cost?** Compare: (a) server-side indexing with retrieval (Copilot), (b) client-side full history retransmission (Roo Code/OpenRouter), (c) native truncation and compaction (Claude Code), (d) prompt caching (Anthropic's prompt caching feature). What is the theoretical cost per turn for each strategy on a 180K-token context window?

35. **What is Anthropic's prompt caching, and does it help?** Can Roo Code or Claude Code leverage Anthropic's prompt caching to reduce retransmission costs? How much would it save? What are the requirements for cache hits?

36. **What is Google's context caching, and how does it compare?** For Gemini models, Google offers context caching. How does this compare to Anthropic's approach? Is this relevant for any of the toolchains we're evaluating?

37. **How do extended context windows (1M+ tokens) change the economics?** If models support 1M+ token context windows, does client-side retransmission become more viable? Or does it just increase cost faster?

### SECTION 8: Enterprise Considerations

38. **Data residency and privacy**: For each toolchain (Copilot, Roo Code + OpenRouter, Claude Code), where does code go? Is it retained for training? What are the data privacy guarantees? What enterprise certifications (SOC 2, ISO 27001, GDPR) does each tool hold?

39. **SSO and team management**: Which tools support enterprise SSO, team seat management, usage dashboards, and audit logging?

40. **Customization depth**: Compare the customization systems — Copilot's `copilot-instructions.md` + `.instructions.md` + `.prompt.md`, Roo Code's `.roo/rules/`, Claude Code's `CLAUDE.md` + ECC harness. Which offers the deepest architecture-specific customization?

41. **MCP (Model Context Protocol) ecosystem**: What is the current state of MCP support across all tools? Which has the most mature MCP integration? What MCP servers are available for architecture workflows (JIRA, Confluence, GitLab, Elasticsearch)?

### SECTION 9: Specific Technical Questions

42. **Can Roo Code use OpenRouter directly without Kong?** If we eliminate the Kong gateway entirely and point Roo Code directly at OpenRouter's API endpoint, do the three gateway failure modes disappear? What is the setup?

43. **What are the known issues with Roo Code + OpenRouter (no Kong)?** Without the Kong translation layer, does Roo Code + OpenRouter work reliably for agentic workflows? Are there any documented issues?

44. **Can Copilot's automatic workspace indexing be configured or tuned?** Can you exclude files, set index refresh intervals, or see what is indexed? Or is it fully opaque?

45. **How does Copilot handle very large workspaces (1000+ files)?** Does indexing performance degrade? Are there known limits?

---

## Output Format Requirements

Structure your response as a single document with the following format:

1. **Executive Summary** (1 page) — Key findings, updated recommendations, and any changes to the current evaluation's conclusions
2. **Sections 1-9** — Each section as an H2 header with numbered answers matching the questions above
3. **Updated Comparison Table** — A comprehensive comparison matrix of all tools evaluated, covering: cost, workspace indexing, context management, reliability, ecosystem integration, enterprise features, and customization
4. **Open Questions** — Any questions you could not fully answer with available sources, with suggestions for how to resolve them
5. **Sources** — Full bibliography with URLs and access dates

Prioritize accuracy over breadth. State explicitly when information is unavailable, outdated, or uncertain. Cite official documentation over blog posts, and blog posts over community speculation.

## PROMPT END
