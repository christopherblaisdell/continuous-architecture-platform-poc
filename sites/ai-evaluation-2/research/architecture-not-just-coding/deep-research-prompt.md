# Deep Research Prompt: Architecture Is Not Just Coding

## Objective

This page rebuts the skeptic's argument that AI coding assistants cannot do architecture work. It relies on (1) a task decomposition showing architecture is file-based, (2) a customization primitives comparison, (3) workspace evidence from the pilot, and (4) a mapping of bespoke components to native equivalents. Every claim and example must be verified.

---

## Claims to Investigate

### 1. Architecture Task Decomposition Table

**Research questions:**
- Is the claim that all architecture tasks reduce to "file-based work" (reads, creates, searches) defensible?
- Are there architecture tasks that genuinely require capabilities beyond file operations? (e.g., whiteboard collaboration, stakeholder interviews, consensus building, visual modeling)
- Should the page acknowledge the limitations — tasks that AI cannot assist with even using coding platforms?

### 2. "Customization primitives are content-agnostic — they inject ANY knowledge, not just coding patterns"

**Research questions:**
- Is "content-agnostic" an accurate description of instruction files? Are there documented examples of non-coding use cases in official platform documentation?
- Do platform vendors market their instruction/rules systems as general-purpose or coding-specific?
- Are there published case studies of architecture or documentation workflows using these platforms?

### 3. Cline Documentation Claim — "Cline's documentation uses `architecture.md` as an example rule file"

**Research questions:**
- Verify this specific claim. Does Cline's documentation at docs.cline.bot/customization/cline-rules use `architecture.md` as an example?
- If not, what examples do they use? Is the spirit of the claim (that Cline supports non-coding rules) still valid?

### 4. Windsurf Skills Claim — "Windsurf's Skills examples include `code-review/` bundles"

**Research questions:**
- Verify this specific claim. Does Windsurf documentation show `code-review/` as a Skills example?
- What Skills examples does Windsurf actually document?
- NOTE: Has this changed after the OpenAI acquisition of Windsurf?

### 5. Pilot Workspace Evidence Claims

**Research questions:**
- "500+ lines `copilot-instructions.md`" — verify the current line count of the file.
- "19-service microservice domain model" — verify the service count.
- "4 completed solution designs" — verify the count of solution directories.
- "19 microservice deep-dive pages with 139 PlantUML sequence diagrams" — verify these counts.
- "Capability changelog across multiple related tickets" — verify the changelog exists and spans multiple tickets.
- These are workspace-verifiable claims (not research claims), but accuracy matters for credibility.

### 6. Bespoke Component → Native Equivalent Mapping Table

**Research questions:**
- "Custom knowledge base → Workspace indexing of architecture/ directory" — is workspace indexing truly equivalent to a custom knowledge base? What are the limitations?
- Is semantic search over workspace files equivalent to vector-search over curated embeddings? What quality differences exist?
- "Custom prompt orchestration → copilot-instructions.md + scoped .instructions.md" — is instruction file injection equivalent to prompt orchestration frameworks like LangChain? What capabilities are lost?
- Is the claim "Building these as a bespoke agent would take weeks of engineering. Configuring them as instruction files takes hours" supportable? Are there estimates or case studies?

### 7. "The question is not 'can AI coding platforms do architecture work?'"

**Research questions:**
- Are there published evaluations, benchmarks, or case studies of AI coding platforms performing architecture work?
- Has anyone formally tested Copilot, Cursor, or Claude Code on architecture tasks (ADR writing, trade-off analysis, impact assessment)?
- Is the pilot itself the primary evidence, or is there external validation?

---

## Expected Output Format

For each claim:
1. **Claim as stated** — exact quote from the page
2. **Verdict** — Confirmed / Partially Confirmed / Unconfirmed / Incorrect
3. **Evidence** — cited sources with URLs, dates accessed, and relevant excerpts
4. **Recommended correction** — if the claim needs updating, provide the corrected text
5. **Confidence level** — High / Medium / Low based on source quality

Include a summary table at the top with all claims and their verdicts.
