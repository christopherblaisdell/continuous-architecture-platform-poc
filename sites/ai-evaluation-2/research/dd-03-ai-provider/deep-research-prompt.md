# Deep Research Prompt: DD-03 AI Provider

## Objective

Investigate every claim about provider capabilities, governance features, competitive positioning, and organizational fit on the DD-03 page. This page argues GitHub Copilot is the recommended AI provider — a skeptic will challenge whether the competitive comparison is fair and complete.

---

## Claims to Investigate

### 1. "Native integration — same vendor as the organization's source control platform"

**Research questions:**
- Does Copilot share SSO, audit trails, and policy management with GitHub Enterprise? Cite documentation on how Copilot inherits GitHub Enterprise governance.
- What specific governance features does Copilot Enterprise offer vs Copilot Business vs Copilot Pro+?
- Is the claim that Copilot governance is "already configured" accurate for an organization already using GitHub Enterprise Cloud?

### 2. Roo Code Governance — "no vendor governance" for the OSS component

**Research questions:**
- What is Roo Code's current project status? Is it actively maintained? Who maintains it? Cite the repository.
- Does "no vendor governance" accurately characterize an open-source tool? Or does OSS transparency provide a different form of governance?
- Does Kong provide enterprise governance (SOC 2, audit trails, access control)? Cite Kong's enterprise documentation.

### 3. Option C — "Azure governance for infrastructure; custom code = custom security surface"

**Research questions:**
- What compliance certifications does Azure AI Foundry carry? (SOC 2, ISO 27001, etc.) Cite Microsoft compliance documentation.
- Is "custom code = custom security surface" a fair characterization? When building on Azure, how much of the security surface is inherited vs custom?
- Are there Azure AI Foundry security best practices or reference architectures that mitigate the "custom security surface" concern?

### 4. "Zero procurement friction — adding Copilot seats to an existing GitHub contract is an IT operations task"

**Research questions:**
- Is adding Copilot seats to an existing GitHub Enterprise agreement truly friction-free? What approvals are typically required?
- Do enterprises typically need separate procurement for Copilot even with existing GitHub contracts? Cite any published enterprise adoption guides.
- Is "not a months-long vendor evaluation" accurate for most enterprises, or do AI tools face additional scrutiny (e.g., AI governance committees, data privacy reviews)?

### 5. "Single governance surface — every other option introduces a new governance boundary"

**Research questions:**
- Is "governance surface" a recognized concept in enterprise architecture? Cite sources (e.g., TOGAF, COBIT, enterprise architecture frameworks).
- How does Cursor handle enterprise governance? Cursor claims SOC 2 Type II and enterprise features — would adopting Cursor truly add a "new governance boundary" or could it integrate with existing SSO?
- Is the single-governance argument compelling enough to justify the provider recommendation, or is it secondary to output quality?

### 6. Competitive Risks — "Cursor's agent quality," "Windsurf's SWE-1.5 model"

**Research questions:**
- What is the current state of Cursor's agent capabilities? Has Cursor published benchmarks or case studies on agent-mode architecture work?
- What is Windsurf's SWE-1.5 model? Is it a real, published model or a proprietary internal model? Cite sources.
- Has Claude Code been benchmarked against Copilot for architecture-type tasks? Cite any comparative evaluations.
- Are there independent benchmarks comparing AI coding assistants on non-coding tasks (documentation, architecture analysis, decision records)?

### 7. Portability — "instruction content portable; activation format is proprietary"

**Research questions:**
- What exactly is portable vs proprietary in Copilot's customization system?
- Can `copilot-instructions.md` content be directly reused in Cursor rules, Windsurf rules, or CLAUDE.md?
- What is the AGENTS.md standard and how much does it cover? Does it make the portability concern negligible?
- What would the actual migration effort be to move from Copilot to Cursor or Windsurf? Has anyone documented such a migration?

---

## Expected Output Format

For each claim:
1. **Claim as stated** — exact quote from the page
2. **Verdict** — Confirmed / Partially Confirmed / Unconfirmed / Incorrect
3. **Evidence** — cited sources with URLs, dates accessed, and relevant excerpts
4. **Recommended correction** — if the claim needs updating, provide the corrected text
5. **Confidence level** — High / Medium / Low based on source quality

Include a summary table at the top with all claims and their verdicts.
