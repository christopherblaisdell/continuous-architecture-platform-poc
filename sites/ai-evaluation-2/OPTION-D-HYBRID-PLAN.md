# Option D (Hybrid) — Site Update Plan

## Desired Outcome

Reframe the evaluation from "Option A wins, Option C loses" to **"Option D (Hybrid) is the recommended path"** — Copilot is the client, Troy's Foundry model is a model choice inside it. No conflict, everyone wins.

### Option D Definition

> **Option D — Hybrid (Copilot + Custom Foundry Model)**: GitHub Copilot provides the development environment, orchestration, and built-in frontier models. Troy's team fine-tunes a domain-specialized model in Azure AI Foundry. Architects access both via the same model picker — built-in models for everyday tasks, the custom model when domain specialization adds value. BYOK (Bring Your Own Key) bridges the two.

### Stakeholder Framing

| Framing | How Troy hears it | How Matt hears it |
|---------|-------------------|-------------------|
| "A absorbs C" | "My work was unnecessary" | "There's a winner and a loser on my team" |
| **"Option D — Hybrid"** | **"My Foundry model is a key component of the recommended approach"** | **"The team collaborated and found the best of both worlds"** |

### Cost Offset Argument

The objection "you're double-paying for Copilot AND the custom model" is actually backwards. Without Copilot:
- Every query hits the custom Foundry model at per-token cost — even routine tasks like formatting tables, generating boilerplate, or simple Q&A
- Architecture teams typically spend 80%+ of their AI interactions on routine tasks that don't require domain-specialized context

With Copilot:
- GPT-4o and GPT-4.1 are available at the 0x multiplier (unlimited, $0 incremental cost) for all routine tasks
- The custom Foundry model is only invoked when the architect explicitly selects it for tasks requiring domain specialization
- Net effect: $39/mo buys unlimited routine task capacity, reducing custom model token consumption by 80%+
- At scale, this saves more than the subscription cost

---

## Phase 0: Validate (Research Before Building)

### 0.1 Deep Research: BYOK Validation

- [ ] **Status:** Not started
- **Purpose:** Validate every claim before publishing. We need to be bulletproof.
- **Method:** Run comprehensive deep research prompt (see Appendix A below)
- **Gate:** If deep research reveals showstoppers, revise the plan before building

---

## Phase 1: New Content

### 1.1 Create Evidence Page: "Option D — Hybrid Architecture (BYOK)"

- [ ] **Status:** Not started
- **Purpose:** Cornerstone document defining Option D for stakeholders
- **Location:** `sites/ai-evaluation-2/docs/evidence/option-d-hybrid-architecture.md`
- **Content:**
  - What BYOK is and how it works (enterprise admin registers Foundry endpoint + API key)
  - Feature compatibility matrix (what works: chat, agent mode, tool calling, instruction files, MCP, workspace indexing; what doesn't: inline completions)
  - The hybrid model picker UX (built-in models + custom model in same dropdown)
  - Integration path and timeline (Troy builds model -> admin registers -> architects use)
  - Cost offset analysis summary (links to 1.3)
  - Limitations and risks (preview status, Enterprise Cloud requirement, data transit)
  - Authoritative sources (GitHub Docs, changelog entries, video reference)
- **Confluence:** Needs CONFLUENCE-PUBLISH header and unique H1

### 1.2 Create Decision Page: "DD-06 — IDE Client Selection for Custom Models"

- [ ] **Status:** Not started
- **Purpose:** Compare clients for consuming a custom Foundry model — proves Copilot is the best client, which is WHY Option D exists
- **Location:** `sites/ai-evaluation-2/docs/decisions/dd-06-ide-client-selection.md`
- **Content:**
  - Problem statement: "Given that the team is building a custom model in Foundry, which IDE client should consume it?"
  - Comparison matrix across 6 clients:
    - GitHub Copilot (BYOK)
    - Cursor
    - Windsurf
    - Cline (open source)
    - Claude Code
    - Custom VS Code Extension (Option C's current approach)
  - Evaluation dimensions:
    - BYOK / custom model support mechanism
    - Agent mode / tool calling capability
    - Workspace indexing and context injection
    - Instruction file support (declarative customization)
    - Client-side thinking / reasoning display
    - MCP support
    - Enterprise governance (SSO, audit, compliance)
    - Cost model when using custom model
  - Verdict: Copilot is the strongest client for consuming a Foundry model
- **Confluence:** Needs CONFLUENCE-PUBLISH header and unique H1

### 1.3 Create Evidence Page: "Cost Offset — Free Tier Models as Hybrid Subsidy"

- [ ] **Status:** Not started
- **Purpose:** Dedicated analysis proving $39/mo subscription saves more than it costs
- **Location:** `sites/ai-evaluation-2/docs/evidence/cost-offset-free-tier-subsidy.md`
- **Content:**
  - Task distribution analysis: what % of architecture tasks need domain context vs. routine AI assistance
  - Per-token cost of routing ALL tasks through custom Foundry model
  - Per-token cost of routing only domain-specialized tasks through custom model (80% reduction)
  - Break-even analysis: at what usage level does the $39 Copilot subscription pay for itself?
  - Comparison table: Option C alone vs Option D (hybrid) monthly cost at various usage levels
  - The "208x cheaper" argument for GPT-4o (0x) vs custom model per-token pricing
- **Confluence:** Needs CONFLUENCE-PUBLISH header and unique H1

---

## Phase 2: Score Updates

### 2.1 Update EF-07 (Multi-Model Flexibility): A from 4 to 5

- [ ] **Status:** Not started
- **Purpose:** BYOK closes the model flexibility gap between A and B
- **Files:** `sites/ai-evaluation-2/docs/framework/scoring-results.md`
- **Changes:**
  - EF-07 Option A score: 4 -> 5
  - EF-07 evidence column: add BYOK reference
  - Recalculate Category 2 subtotal
  - Recalculate weighted total for A (should go from 4.81 to 4.84)
  - Update Summary table at top

### 2.2 Update Evaluation Methodology (EF-07 Rubric)

- [ ] **Status:** Not started
- **Purpose:** Ensure the score-5 rubric criteria clearly covers BYOK/custom model support
- **Files:** `sites/ai-evaluation-2/docs/framework/evaluation-methodology.md`
- **Changes:**
  - Adjust EF-07 definition to mention BYOK/custom model integration
  - Score 5 criteria: confirm it covers "custom/fine-tuned models via BYOK" alongside built-in models

### 2.3 Regenerate All Scoring Graphics (SVG + PNG)

- [ ] **Status:** Not started
- **Purpose:** Heatmap, radar, bar chart, stacked bars must reflect A's EF-07 = 5
- **Files:** `sites/ai-evaluation-2/docs/img/generate-scoring-graphics.py` + all 8 output files
- **Changes:**
  - Update `scores_a` array: index 6 (EF-07) from 4 to 5
  - Recalculate `weighted_a` in script
  - Run script to regenerate all SVG + PNG
  - Verify embedded images in scoring-results.md and index.md render correctly

---

## Phase 3: Existing Page Updates

### 3.1 Update DD-05 (Model Selection Autonomy)

- [ ] **Status:** Not started
- **Purpose:** Custom Foundry models join the "guided freedom" model picker
- **Files:** `sites/ai-evaluation-2/docs/decisions/dd-05-model-selection-autonomy.md`
- **Changes:**
  - Add row to the task/model recommendation table:
    - Task Type: "Domain-specialized analysis (company-specific context)"
    - Recommended Model: "Custom Foundry Model (BYOK)"
    - Multiplier: "Per-token (via Foundry API)"
    - Cost Per Prompt: "Variable (per-token)"
  - Add paragraph explaining that BYOK extends guided freedom to include enterprise-specific models
  - Reference DD-06 for the client selection rationale

### 3.2 Update DD-04 (Model Routing)

- [ ] **Status:** Not started
- **Purpose:** BYOK is a new routing option under Option A
- **Files:** `sites/ai-evaluation-2/docs/decisions/dd-04-model-routing.md`
- **Changes:**
  - Update the Option A row in the routing comparison table to mention BYOK
  - Add a section explaining how BYOK routing works (architect selects from picker, request routes to Foundry endpoint via GitHub)
  - Note that this gives Option A the routing flexibility previously only available in Option B

### 3.3 Update Copilot Rollout Roadmap

- [ ] **Status:** Not started
- **Purpose:** Add BYOK integration as a future phase
- **Files:** `sites/ai-evaluation-2/docs/framework/copilot-rollout-roadmap.md`
- **Changes:**
  - Add new phase (Phase 3 or 4): "Integrate Custom Foundry Model via BYOK"
  - Phase deliverables:
    - Troy's team deploys fine-tuned model to Foundry
    - Enterprise admin registers Foundry endpoint + API key in GitHub Enterprise Cloud
    - Test model in Copilot agent mode with architecture workspace
    - Compare output quality: built-in Claude Opus vs custom model
    - Establish guidance: when to use custom model vs built-in
  - Phase prerequisites: BYOK reaches GA (or organization accepts preview risk), Troy's model is production-ready
  - Note existing Tier 4 / Foundry IQ section already exists — cross-reference it

### 3.4 Update Scoring Results Conclusion

- [ ] **Status:** Not started
- **Purpose:** Reframe conclusion from "A wins" to "D (Hybrid) is the recommended path"
- **Files:** `sites/ai-evaluation-2/docs/framework/scoring-results.md`
- **Changes:**
  - Keep all existing evidence and analysis — it demonstrates why Copilot is the right client
  - Rewrite Conclusion section to recommend Option D
  - Key message: "Start with Copilot today (Option A's immediate value). Integrate Troy's Foundry model when ready (Option C's investment has a clear integration path via BYOK). Option D combines the strengths of both without the weaknesses of either."
  - Add "Option D — Hybrid" explanation section before or after the existing conclusion
  - Reference the new evidence and decision pages

### 3.5 Update Index Page (Homepage)

- [ ] **Status:** Not started
- **Purpose:** Add Option D to the site, update navigation, reframe narrative
- **Files:** `sites/ai-evaluation-2/docs/index.md`
- **Changes:**
  - Add Option D to "Options Under Evaluation" list
  - Add new pages to Page Index (option-d-hybrid, DD-06, cost-offset)
  - Adjust "At a Glance" caption to mention Option D recommendation
  - Reframe evaluation narrative in Purpose section to conclude with D

---

## Phase 4: NovaTrek POC Extension

### 4.1 Plan the Option D POC

- [ ] **Status:** Not started
- **Purpose:** Define what "proving Option D works" means
- **Location:** New document or section in the NovaTrek workspace
- **Content:**
  - Test plan:
    1. Deploy a model to Azure AI Foundry (can use a base model for POC — fine-tuning not required to prove the BYOK integration)
    2. Register the model via BYOK in GitHub Enterprise Cloud (or simulate if we don't have Enterprise Cloud)
    3. Use the BYOK model in Copilot agent mode for architecture work
    4. Compare output quality: built-in Claude Opus vs BYOK model on same architecture tasks
    5. Demonstrate the model-switching workflow (architect toggles between models per task)
    6. Document results with screenshots and output comparison
  - Success criteria: Copilot agent mode functions fully with the BYOK model (tool calling, file access, instruction files work)
  - Failure criteria: Agent mode features degrade or don't work with BYOK model

### 4.2 Build Representative Sample of Option C Use Cases

- [ ] **Status:** Not started
- **Purpose:** Prove that Option D handles what Troy wants to do with Option C
- **Content:**
  - Interview Troy/Gabriel to identify top 3-5 use cases for the custom agent
  - Reproduce each use case in NovaTrek domain
  - Demonstrate Option D handling each use case via Copilot + BYOK model
  - Document comparison: Option C approach vs Option D approach for each use case
  - Deliverable: side-by-side evidence that Option D matches or exceeds Option C capability

---

## Appendix A: Deep Research Prompt

### Deep Research: Validate BYOK Hybrid Architecture for GitHub Copilot

Research the following questions about GitHub Copilot's "Bring Your Own Key" (BYOK) / custom model support. For every claim, provide authoritative links (GitHub Docs, GitHub Blog, GitHub Changelog, Microsoft Learn, or official release notes). Flag any claims that cannot be verified with primary sources.

**Feature Status and Timeline:**

1. What is the current status of BYOK in GitHub Copilot? (Public preview? GA? Date launched?)
2. Which GitHub Copilot plans support BYOK? (Enterprise Cloud only? Business? Pro+?)
3. What is the historical trajectory — when was it announced, when did it enter preview, and what's the expected GA timeline?
4. Has GitHub published a roadmap or blog post about BYOK going GA?

**Supported Providers and Models:**

5. Exactly which LLM providers are supported as of April 2026? List each one.
6. Can fine-tuned models deployed on Azure AI Foundry be used via BYOK? What are the documented limitations?
7. Can models from the Azure AI Foundry Model Catalog (not custom-deployed, but catalog models like Llama, Mistral, Phi) be used via BYOK?
8. What model capabilities can be declared in the enterprise admin? (tool calling, vision, thinking/reasoning)

**Feature Compatibility:**

9. Does a BYOK model work in Copilot Agent Mode (VS Code)? Specifically: tool calling, file reads, terminal commands, multi-step autonomous loops?
10. Does a BYOK model work with MCP (Model Context Protocol) servers?
11. Does a BYOK model receive instruction files (copilot-instructions.md, .instructions.md, AGENTS.md)?
12. Does a BYOK model receive workspace context from Copilot's indexing pipeline (Tree-sitter AST chunks, heading-aware Markdown)?
13. Does a BYOK model work for inline code completions, or only for Chat/CLI?
14. Does a BYOK model work with the Copilot coding agent (cloud-based, works from GitHub issues)?
15. Does a BYOK model work with Copilot code review (pull request review)?
16. Can the BYOK model coexist with built-in models? (i.e., can an architect switch between Claude Opus and the custom model in the same session?)

**Enterprise Administration:**

17. How does an enterprise admin register a Foundry deployment? (deployment URL, API key, model ID)
18. Can access be scoped to specific organizations within the enterprise?
19. Can token limits (max input/output) be configured per model?
20. What audit logging exists for BYOK model usage?
21. What happens to data in transit — does prompt content flow through GitHub's servers to the Foundry endpoint, or is there a direct connection?

**Cost and Billing:**

22. When using a BYOK model, what does the user pay? (Copilot subscription + per-token via their own API key?)
23. Do BYOK model requests consume premium requests from the Copilot subscription, or are they billed separately?
24. Is the $39/seat subscription still required, or can BYOK be used with cheaper plans?

**Limitations and Risks:**

25. What are the documented limitations of BYOK? (GitHub's own warnings, known issues, preview caveats)
26. Are there any models that explicitly DO NOT work with BYOK?
27. What happens if the BYOK feature is deprecated or changed during preview — what's the fallback?
28. Are there documented quality or performance issues with fine-tuned models in BYOK compared to built-in models?

**Competitor Comparison:**

29. Can Cursor, Windsurf, Cline, or Claude Code consume a custom Foundry model? How?
30. How does each competitor's client-side orchestration (tool calling, workspace indexing, instruction files, agent loops) compare to Copilot's when using a custom model?
31. Does any competitor offer BYOK with better feature compatibility than Copilot?

**Enterprise Readiness:**

32. What compliance certifications does BYOK inherit from GitHub Enterprise Cloud?
33. Does BYOK work with GitHub Enterprise Managed Users (EMU)?
34. Is there any documentation about BYOK in GovCloud or FedRAMP environments?

For each answer, cite the specific URL. Flag unanswered questions as "NOT VERIFIED — requires manual confirmation" and explain why.
