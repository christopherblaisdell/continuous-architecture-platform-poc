# Deep Research Prompt: BYOK Hybrid Architecture Validation

Use this prompt with GitHub Copilot Deep Research or equivalent tool.

---

## Prompt

Research the following questions about GitHub Copilot's "Bring Your Own Key" (BYOK) / custom model support feature, which allows enterprise administrators to register their own LLM provider API keys so that organization members can use custom models through GitHub Copilot Chat and CLI.

For every claim, provide authoritative links (GitHub Docs, GitHub Blog, GitHub Changelog, Microsoft Learn, or official release notes). Flag any claims that cannot be verified with primary sources.

### Feature Status and Timeline

1. What is the current status of BYOK in GitHub Copilot? (Public preview? GA? Date launched?)
2. Which GitHub Copilot plans support BYOK? (Enterprise Cloud only? Business? Pro+?)
3. What is the historical trajectory — when was it announced, when did it enter preview, and what's the expected GA timeline?
4. Has GitHub published a roadmap or blog post about BYOK going GA?

### Supported Providers and Models

5. Exactly which LLM providers are supported as of April 2026? List each one.
6. Can fine-tuned models deployed on Azure AI Foundry be used via BYOK? What are the documented limitations?
7. Can models from the Azure AI Foundry Model Catalog (not custom-deployed, but catalog models like Llama, Mistral, Phi) be used via BYOK?
8. What model capabilities can be declared in the enterprise admin? (tool calling, vision, thinking/reasoning)

### Feature Compatibility

9. Does a BYOK model work in Copilot Agent Mode (VS Code)? Specifically: tool calling, file reads, terminal commands, multi-step autonomous loops?
10. Does a BYOK model work with MCP (Model Context Protocol) servers?
11. Does a BYOK model receive instruction files (copilot-instructions.md, .instructions.md, AGENTS.md)?
12. Does a BYOK model receive workspace context from Copilot's indexing pipeline (Tree-sitter AST chunks, heading-aware Markdown)?
13. Does a BYOK model work for inline code completions, or only for Chat/CLI?
14. Does a BYOK model work with the Copilot coding agent (cloud-based, works from GitHub issues)?
15. Does a BYOK model work with Copilot code review (pull request review)?
16. Can the BYOK model coexist with built-in models? (i.e., can an architect switch between Claude Opus and the custom model in the same session?)

### Enterprise Administration

17. How does an enterprise admin register a Foundry deployment? (deployment URL, API key, model ID)
18. Can access be scoped to specific organizations within the enterprise?
19. Can token limits (max input/output) be configured per model?
20. What audit logging exists for BYOK model usage?
21. What happens to data in transit — does prompt content flow through GitHub's servers to the Foundry endpoint, or is there a direct connection?

### Cost and Billing

22. When using a BYOK model, what does the user pay? (Copilot subscription + per-token via their own API key?)
23. Do BYOK model requests consume premium requests from the Copilot subscription, or are they billed separately?
24. Is the $39/seat subscription still required, or can BYOK be used with cheaper plans?

### Limitations and Risks

25. What are the documented limitations of BYOK? (GitHub's own warnings, known issues, preview caveats)
26. Are there any models that explicitly DO NOT work with BYOK?
27. What happens if the BYOK feature is deprecated or changed during preview — what's the fallback?
28. Are there documented quality or performance issues with fine-tuned models in BYOK compared to built-in models?

### Competitor Comparison

29. Can Cursor, Windsurf, Cline, or Claude Code consume a custom Foundry model? How?
30. How does each competitor's client-side orchestration (tool calling, workspace indexing, instruction files, agent loops) compare to Copilot's when using a custom model?
31. Does any competitor offer BYOK with better feature compatibility than Copilot?

### Enterprise Readiness

32. What compliance certifications does BYOK inherit from GitHub Enterprise Cloud?
33. Does BYOK work with GitHub Enterprise Managed Users (EMU)?
34. Is there any documentation about BYOK in GovCloud or FedRAMP environments?

### Output Format

For each answer:
- Cite the specific URL
- Quote the relevant text where possible
- Flag unanswered questions as "NOT VERIFIED — requires manual confirmation" and explain why
- At the end, provide a summary scorecard: how many verified, partially verified, and not verified
