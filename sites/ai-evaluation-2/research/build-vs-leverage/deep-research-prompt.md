# Deep Research Prompt: Build vs Leverage

## Objective

This page argues that custom RAG pipelines reinvent capabilities already native to AI coding platforms. The central 8-row comparison table mapping RAG components to native equivalents is the core artifact to verify. A skeptic familiar with RAG architecture will challenge whether native platform capabilities truly match purpose-built pipelines.

---

## Claims to Investigate

### 1. The 8-Row RAG Comparison Table

For each row, verify whether the "Native Platform Equivalent" accurately describes what the platforms offer:

**Row 1 — Document Ingestion → Workspace Indexing**
- Do Copilot, Cursor, and Windsurf perform automatic, incremental workspace indexing? How does each platform's indexing work? Cite documentation.
- Does Claude Code perform workspace indexing? The table says it does — is this accurate?
- Is "zero-config" a fair characterization? Are there configuration options or limitations?

**Row 2 — Vector Store → Built-in Semantic Search**
- Do Copilot, Cursor, and Windsurf maintain a built-in semantic search index? Is it local, cloud-based, or hybrid?
- What is the quality of native semantic search vs a purpose-built vector DB (Pinecone, Weaviate)?
- Are there context window limitations that make native search inferior for large codebases?

**Row 3 — Retrieval → @workspace / @codebase**
- Does Copilot use `@workspace`? Does Cursor use `@codebase`? Does Windsurf have an equivalent? Does Cline? Cite current documentation.
- How does native retrieval quality compare to custom RAG retrieval with re-ranking?

**Row 4 — Context Injection → Declarative Instruction Files**
- Is "no code required" accurate for context injection? Are there limitations?
- Do all five platforms support declarative instruction files? (The table says yes for all.) Cite documentation for each.

**Row 5 — Behavior Configuration → Rules, Custom Agents**
- Do Copilot, Cursor, Windsurf, and Cline all support workspace-as-code behavior configuration? Cite documentation.
- What specific mechanisms does each offer? (Rules, agents, modes, etc.)

**Row 6 — Tool Integration → Native MCP Support**
- Do all five platforms support MCP natively? Cite documentation for each.
- Is MCP support at the same maturity level across all platforms?

**Row 7 — Multi-Agent Orchestration → Native Sub-Agents**
- The table claims Copilot, Windsurf, and Cline support native sub-agents. Is this accurate? Cite documentation.
- Does Cursor support sub-agents or multi-agent orchestration? The table omits Cursor — is this correct?
- Does Claude Code support sub-agents? The table omits Claude Code — is this correct?

**Row 8 — Evaluation → Direct Observation**
- Is "direct observation" a fair equivalent to custom A/B testing infrastructure? This seems like a weak equivalence — investigate whether platforms offer any evaluation tooling.

### 2. "The Infrastructure Tax"

**Research questions:**
- The page claims every RAG component requires development, operations, ongoing cost, and ML expertise. Is this a fair characterization?
- Are there managed RAG services (e.g., Amazon Bedrock Knowledge Bases, Azure AI Search + OpenAI) that significantly reduce the infrastructure tax?
- Should the page acknowledge managed RAG-as-a-service offerings as a middle ground between full custom and native platform capabilities?

### 3. Cross-Platform Standard Claims

**Research questions:**
- Is `AGENTS.md` supported by Cursor, Windsurf, and Cline? Cite sources.
- Is [agentskills.io](https://agentskills.io) a real website with a real specification? What does it define?
- What is the current state of cross-platform customization standards?
- Is the claim that instruction content is portable across platforms accurate? What is and isn't portable?

### 4. "Custom RAG Is the Right Answer When AI Is the Product... Wrong Choice When AI Is a Tool"

**Research questions:**
- Is this distinction recognized in industry literature? Cite sources on "AI as product vs AI as tool."
- Are there counterexamples where organizations successfully use custom RAG for internal developer tools?
- Is there a middle ground the page should acknowledge?

### 5. Footnote Claims

**Research questions:**
- Footnote (1): "a cross-platform standard is emerging via `AGENTS.md`" — verify this claim with current status.
- Does the page accurately describe the file conventions for each platform? (.instructions.md for Copilot, .cursor/rules/*.md for Cursor, etc.)

---

## Expected Output Format

For each claim:
1. **Claim as stated** — exact quote from the page
2. **Verdict** — Confirmed / Partially Confirmed / Unconfirmed / Incorrect
3. **Evidence** — cited sources with URLs, dates accessed, and relevant excerpts
4. **Recommended correction** — if the claim needs updating, provide the corrected text
5. **Confidence level** — High / Medium / Low based on source quality

Include a summary table at the top with all claims and their verdicts.
