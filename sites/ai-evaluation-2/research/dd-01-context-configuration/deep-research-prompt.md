# Deep Research Prompt: DD-01 Context and Configuration

## Objective

Investigate every factual claim about platform customization capabilities, context injection mechanisms, and the content taxonomy assessment on the DD-01 page. This decision page argues that native declarative configuration is sufficient — a skeptic will challenge whether the claimed capabilities actually exist and work as described.

---

## Claims to Investigate

### 1. Copilot Instruction Hierarchy

The page lists: "global instructions, scoped instructions, skills, agent modes, and MCP — all as workspace-committed files."

**Research questions:**
- Does GitHub Copilot support all five of these customization mechanisms? Cite official documentation for each:
  - `copilot-instructions.md` (global instructions)
  - `.instructions.md` with `applyTo` globs (scoped instructions)
  - `SKILL.md` (skills with progressive disclosure)
  - `.agent.md` (custom agent modes with tool restrictions)
  - MCP (Model Context Protocol) server integration
- Are there additional customization mechanisms not mentioned? (e.g., `AGENTS.md`, hooks, prompt files)
- Which of these are GA (generally available) vs preview/experimental?

### 2. "Zero engineering, zero infrastructure"

**Research questions:**
- Is "zero engineering" accurate for configuring Copilot with instruction files? Does writing 500+ lines of markdown configuration count as engineering effort?
- Distinguish between "engineering" (custom code development, infrastructure provisioning) and "configuration" (declarative file creation). Is this distinction standard in technology evaluations?
- Are there infrastructure requirements for Copilot's workspace indexing (e.g., GitHub Enterprise Cloud for server-side indexing)?

### 3. MCP Servers as Enterprise Tool Integration

The page claims enterprise tools (JIRA, Elastic, GitLab) are accessible via MCP servers.

**Research questions:**
- What is MCP (Model Context Protocol)? Who created it (Anthropic)? Cite the specification.
- Does Copilot natively support MCP? Since when? Cite the announcement or documentation.
- Are there production-grade MCP servers for JIRA, Elasticsearch, and GitLab available in the community, or would they need to be custom-built?
- Is the pilot's use of local Python scripts as mock MCP servers representative of how production MCP integration would work?

### 4. Content Taxonomy — "7 of 8 content categories are fully served by native capabilities"

**Research questions:**
- Verify each claimed "FULL" coverage category:
  - Architecture standards via instruction files — can instruction files effectively encode arc42, C4, MADR templates?
  - Domain model via workspace-indexed YAML — does workspace indexing handle YAML files effectively?
  - Prior solution designs via workspace-indexed markdown — is this retrieval reliable for large repositories?
  - Enterprise tools via MCP — see question 3 above
- Is the CMDB/cross-team data gap accurately characterized? Are there MCP servers or integrations that could close it?
- Is "Solvable — migrate to repo markdown, publish via CI" a fair characterization of the Confluence content gap? What are the limitations of this approach?

### 5. Roo Code / Cline Customization Capabilities

The page implies Option B (Roo Code) offers similar capabilities but with "different instruction format."

**Research questions:**
- What customization files does Roo Code / Cline support? (`.clinerules/*.md`, custom modes, etc.) Cite documentation.
- How do Roo Code's customization capabilities compare to Copilot's? Is "slight friction from different instruction format" accurate or does it understate the differences?
- Does Roo Code support MCP? Since when?

### 6. Option C — "Every domain change requires agent update, not just a file edit"

**Research questions:**
- Is this accurate for Azure AI Foundry agents? Can Azure AI Foundry agents be configured with file-based knowledge, or do they require code changes?
- Does Azure AI Foundry support prompt templates, knowledge bases, or grounding data that could be updated without engineering?
- Is this claim overstated to make Option C look worse?

---

## Expected Output Format

For each claim:
1. **Claim as stated** — exact quote from the page
2. **Verdict** — Confirmed / Partially Confirmed / Unconfirmed / Incorrect
3. **Evidence** — cited sources with URLs, dates accessed, and relevant excerpts
4. **Recommended correction** — if the claim needs updating, provide the corrected text
5. **Confidence level** — High / Medium / Low based on source quality

Include a summary table at the top with all claims and their verdicts.
