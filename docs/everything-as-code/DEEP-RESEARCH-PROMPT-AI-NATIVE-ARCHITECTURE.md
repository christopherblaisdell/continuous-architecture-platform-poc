# Deep Research Prompt: AI-Native Architecture Practice

**Usage**: This is a deep research prompt suitable for an AI deep-research session. The expected output should be pasted into [DEEP-RESEARCH-PROMPT-AI-NATIVE-ARCHITECTURE-RESPONSE.md](DEEP-RESEARCH-PROMPT-AI-NATIVE-ARCHITECTURE-RESPONSE.md).

---

## Prompt

I am leading the modernization of an enterprise software architecture practice. We have committed to **Everything as Code** as our foundation. The next question is: when AI agents are co-authors of every artifact, what does the architecture practice look like? Produce a comprehensive research document on **AI-Native Architecture Practice** — what it is, who is defining it, what tools instantiate it, and what an enterprise should do today (mid-2026) to adopt it.

Include inline hyperlinks to authoritative primary sources for every factual claim — academic papers (DOI/arXiv), official documentation, vendor announcements, conference talks. Rich linking is mandatory.

### Section 1 — Defining "AI-Native"

1. **What does "AI-native" mean** when applied to a software architecture practice? Cite definitions from vendors (AWS, GitHub, Anthropic, Google, Microsoft) and analysts (Gartner, Forrester, ThoughtWorks).
2. **Distinguish AI-augmented vs AI-native**: When is a practice AI-augmented (AI is a tool used by humans) vs AI-native (AI is a primary author/operator)? Cite published frameworks.
3. **Industry terminology**: Spec-driven development, intent-driven engineering, AI-native SDLC, agentic engineering — provide a glossary with sources.
4. **The role of architecture specifically**: What changes in the architect's role when AI is a co-author? Cite published thinking from leading architects (Simon Brown, Gregor Hohpe, Martin Fowler, Sam Newman, Mark Richards, Eduardo da Silva).

### Section 2 — The Spec-Driven Development Movement

Investigate the spec-driven development paradigm comprehensively:

1. **AWS Kiro** — https://kiro.dev/ — full evaluation: positioning, target users, spec format, IDE integration, current adoption, pricing, enterprise readiness, comparison to competing approaches
2. **GitHub Spec-Kit** — https://github.com/github/spec-kit — full evaluation: design, supported workflows, integration with GitHub Copilot, current state
3. **OpenSpec** — https://github.com/Fission-AI/OpenSpec — full evaluation: maturity, adoption, ecosystem, governance model
4. **Anthropic's published guidance** on spec-driven approaches — link every relevant blog post, paper, prompt engineering guide
5. **Google Gemini Code Assist** spec-driven features — current state
6. **Cursor / Windsurf** spec workflows — current state
7. **Comparison matrix** of all of the above
8. **The "what if all coding became spec-writing?" thesis**: who is articulating this most credibly? Cite.

### Section 3 — Agentic Architecture Tools

Investigate tools that specifically position themselves as AI-native architecture aids:

1. **IcePanel AI features** — https://icepanel.io/
2. **Structurizr AI integrations**
3. **Backstage AI plugins** — https://backstage.io/
4. **Multiplayer.app** — and similar AI architecture diagram tools
5. **GitDiagram** — https://gitdiagram.com/
6. **Cursor / Windsurf / Cline / Roo Code** — comparing their architecture awareness features
7. **Claude Projects / ChatGPT Projects** for architecture work — actual capabilities and limits
8. **Agentic coding agents** (OpenAI Codex agent, GitHub Copilot Coding Agent, Claude Code, Devin, Gemini Code Assist agent) — how each handles architecture-level reasoning vs implementation

### Section 4 — Layered Behavior Governance Model

Investigate the formal layering of AI behavior governance, particularly:

1. **Layer 1 — Behavioral Specification**: instruction file formats, evaluations of each (Copilot, Cursor, Roo, Windsurf, Continue, Aider)
2. **Layer 2 — Change Governance**: OpenSpec and any alternatives — how is the *process of changing* AI behavior itself governed?
3. **Layer 3 — Runtime Integration**: MCP, RAG, vector stores, tool registries — how is context delivered at inference time
4. **Constitutional AI** — Anthropic's published method (https://arxiv.org/abs/2212.08073) and its relevance to enterprise behavioral specification
5. **Instruction Hierarchy** — OpenAI's published method (https://arxiv.org/abs/2404.13208) and its enterprise implications
6. **Privilege tiers**: how should an enterprise architecture practice formally distinguish corporate-mandatory rules vs project rules vs session rules vs user-overridable preferences? Cite published thinking.

### Section 5 — The AI-Native SDLC

Map the AI-native software development lifecycle:

1. **Discovery and ideation**: How AI agents participate in capability discovery, business analysis, requirements
2. **Architecture and design**: How AI agents author specs, ADRs, diagrams
3. **Implementation**: Agentic coding loops, autonomous PRs
4. **Validation**: AI-authored tests, generated coverage reports, AI-driven code review
5. **Operations**: AI-authored runbooks, autonomous incident response
6. **Continuous learning**: How AI feedback closes the loop into the next iteration

For each, cite vendor patterns, published case studies, and emerging best practices.

### Section 6 — Workflows That Change

What concrete architecture workflows change in an AI-native practice? For each, describe the before, the after, and the enabling tools:

1. ADR authoring
2. C4 diagram creation
3. Capability map maintenance
4. Solution design
5. API contract design
6. Code review (architectural review specifically)
7. Cross-team architectural communication
8. Onboarding new architects
9. Architecture documentation maintenance
10. Architectural debt detection

### Section 7 — Required Skills and Roles

What new skills do architects need? What old skills become less critical? What new roles emerge?

1. **Spec authoring / prompt engineering for architects**
2. **Validator authoring** — writing JSON Schemas, OPA policies, lint rules
3. **Generator authoring** — writing code that produces docs/diagrams from canonical sources
4. **AI behavioral governance** — managing OpenSpec or equivalent
5. **Eval authoring** — measuring AI agent quality on architectural tasks
6. **AI auditing** — verifying AI-authored architectural artifacts before merge
7. **New role: AI Architecture Officer / Agentic SRE** — does this role exist in published org charts? Cite.

### Section 8 — Quality, Safety, and Audit

Address the quality and safety questions:

1. **How do you certify** that an AI-authored ADR is sound?
2. **How do you detect** AI hallucination in architectural artifacts?
3. **How do you audit** the chain of custody from human intent → AI agent → committed artifact?
4. **How do you handle compliance** (SOC 2, ISO 27001) when AI agents author production-affecting changes?
5. **What evals** measure AI quality on architectural tasks specifically?
6. **What human-in-the-loop gates** are non-negotiable?

Cite published practices, frameworks, and case studies.

### Section 9 — Open Questions and Research Frontiers

What questions are still open in this space? Where is the active research frontier? Cite recent papers (2024-2026) on:

1. Multi-agent architecture authoring
2. Agent specialization for architecture vs implementation
3. Long-horizon agentic planning for architecture
4. Self-improving architecture practices
5. Verifiable AI-authored architecture

### Section 10 — Vendor Visions

Summarize what each major vendor publicly says is their vision for AI-native architecture practice:

- Microsoft / GitHub
- Anthropic
- OpenAI
- Google
- AWS (Kiro and beyond)
- Atlassian (Rovo)
- Cursor
- Codeium / Windsurf
- ThoughtWorks
- Capgemini / Accenture / Deloitte (consultancies)

For each, what tools, frameworks, and methodologies are they pushing? Cite.

### Section 11 — Maturity Model for AI-Native Architecture Practice

Synthesize a 0-9 maturity model specifically for AI-native architecture practice (distinct from generic EaC maturity):

| Level | Description | Indicators | Vendor parallel (if any) |
|-------|-------------|------------|--------------------------|

### Section 12 — Recommendations for Adoption Today

For a mid-sized enterprise architecture practice in mid-2026, give a concrete adoption roadmap:

1. **First 90 days**: foundational adoption
2. **First year**: core practice transformation
3. **18-24 months**: AI-native operating model
4. **Beyond**: continuous improvement
5. **Anti-patterns to avoid**: explicit list with citations

### Section 13 — Gap Analysis

| Gap | Current best mitigation | Watch for resolution from | Estimated timeline |
|-----|------------------------|---------------------------|--------------------|

---

## Deliverable Format

Single comprehensive document. Section headings as above. Inline hyperlinks. Every factual claim sourced. The deliverable should be 8000-15000 words and serve as our authoritative internal reference for AI-native architecture practice adoption.
