# Plan: Option C File-Type Decision Matrix and A-vs-C Comparison

## Purpose

The existing [File-Type Chunking Strategy](../docs/framework/filetype-chunking-strategy.md) thoroughly documents how GitHub Copilot (Option A) handles each architecture file type — native chunking quality, workarounds, and implementation sequencing. But this analysis is one-sided: it tells us where Option A struggles without establishing whether Option C (Azure AI Foundry / Foundry IQ) would do any better.

A stakeholder could reasonably ask: "You say PlantUML chunks poorly in Copilot — but would a custom Foundry IQ pipeline actually chunk it better?" Without a comparable analysis for Option C, the evaluation cannot answer that question with evidence.

### Deliverables

1. **Option C File-Type Decision Matrix** — Same structure as the existing Copilot matrix, but for a Foundry IQ-backed bespoke agent. For each file type: native indexing quality in Azure AI Search, available chunking customizations, integration effort, and target state.

2. **A-vs-C Comparison Matrix** — Side-by-side table for each file type showing: which option handles it better, what each requires, and the net advantage (if any) of building custom infrastructure.

3. **Both deliverables published as a single new page** on the evaluation site and Confluence.

---

## Phase 1: Deep Research (Prerequisites)

Before writing anything, we need evidence-grounded answers to specific questions about Azure AI Search and Foundry IQ's chunking behavior. The existing evaluation site has general Foundry IQ analysis but no file-type-level chunking data.

### Research Round 1: Azure AI Search Chunking Mechanics

**Goal:** Establish the baseline — how does Azure AI Search actually chunk each file type?

Questions to answer via deep research:

1. **What chunking strategies does Azure AI Search support?** Document-level, fixed-size, semantic, custom skillsets. What are the defaults? What's configurable?
2. **How does it handle YAML files?** Does it treat YAML as plain text? Can custom skillsets parse YAML structure? Does it resolve `$ref` pointers?
3. **How does it handle Markdown files?** Is there heading-aware chunking? Does it understand MADR structure?
4. **How does it handle PlantUML (.puml) files?** Is there any parser, or is it plain-text windowed chunking? Can a custom skillset parse PlantUML syntax?
5. **What is the chunk size configuration?** Default token window, overlap, configurable ranges?
6. **What embedding models are available?** Azure OpenAI embeddings, custom models, dimensionality options?
7. **What is the `text-split` cognitive skill?** How does it compare to Copilot's Tree-sitter + Jaccard approach?
8. **Can custom skillsets call external services?** (e.g., a PlantUML parser, an OpenAPI resolver) — and what does that cost?
9. **How does integrated vectorization work?** Is it automatic or does it require explicit configuration per data source?
10. **What file formats does the built-in document cracking support?** PDF, Office, HTML — but what about YAML, PUML, AsyncAPI?

**Source:** Microsoft Learn documentation for Azure AI Search, Foundry IQ, and Azure AI Document Intelligence.

### Research Round 2: Foundry IQ Knowledge Base Configuration

**Goal:** Understand what Foundry IQ adds on top of Azure AI Search — specifically for architecture artifact types.

Questions to answer:

1. **What knowledge source types does Foundry IQ support?** Azure Blob, SharePoint, OneLake, Azure AI Search index — can it ingest git repositories directly?
2. **How are retrieval instructions configured?** Can they be file-type-specific? Can they match the scoped `.instructions.md` granularity?
3. **What reasoning effort levels exist?** Minimal, low, medium — how do these affect retrieval quality for structured files?
4. **Does Foundry IQ add any chunking intelligence beyond Azure AI Search?** Or is it purely an orchestration layer over the same index?
5. **Can MCP endpoints expose file-type-specific queries?** (e.g., "get endpoint definition from OpenAPI spec" vs generic document search)
6. **What is the latency profile?** Azure AI Search query → LLM query planning → result assembly — how does this compare to Copilot's sub-second workspace search?
7. **How does access control interact with git-based content?** If specs are in GitHub, does Foundry IQ require them to be copied to Azure Blob or SharePoint?

### Research Execution

- **Method:** Deep Research prompts (same methodology as the 5 existing chunking research rounds)
- **Estimated output:** 2 research reports, ~50-70 sources each
- **Time:** 1-2 deep research sessions

---

## Phase 2: Option C File-Type Decision Matrix

Using research findings, construct a matrix with identical structure to the existing Copilot matrix.

### Matrix Structure

| File Type | Azure AI Search Chunking Quality | Available Customizations | Integration Effort | Custom Skillset Required? | Target State |
|-----------|----------------------------------|--------------------------|-------------------|--------------------------|-------------|

### File Types to Cover (same 10 as existing matrix)

1. Java / TypeScript / Python source code
2. Markdown ADRs and solution designs
3. OpenAPI YAML specs (small, <150 lines)
4. OpenAPI YAML specs (large, >150 lines)
5. AsyncAPI event specs
6. YAML metadata files (capabilities, tickets, domains)
7. PlantUML diagrams (.puml)
8. Figma wireframes
9. Configuration YAML
10. Confluence-migrated Markdown

### Key Questions per File Type

For each file type, the matrix must answer:

- Does Azure AI Search's document cracking recognize this format?
- What chunking granularity is achievable (document-level, section-level, element-level)?
- Is a custom skillset required, and if so, how complex?
- Does the custom skillset improve chunking enough to justify the engineering cost?
- What is the ongoing maintenance burden?

### Writing Standards

- Every claim must cite a Microsoft Learn doc or deep research finding
- No speculative claims — if Azure AI Search's behavior for a file type is undocumented, state "undocumented; requires empirical testing"
- Compare against the same "native chunking quality" scale used in the Copilot matrix (HIGH / MEDIUM / LOW / VERY LOW / NONE)

---

## Phase 3: A-vs-C Comparison Matrix

The culminating artifact. For each file type, put Options A and C side by side.

### Matrix Structure

| File Type | Option A (Copilot) | Option A Workaround | Option C (Foundry IQ) | Option C Workaround | Net Advantage | Verdict |
|-----------|--------------------|--------------------|-----------------------|--------------------|--------------|---------| 

### Columns Explained

- **Option A (Copilot):** Native chunking quality (from existing matrix)
- **Option A Workaround:** Primary mitigation strategy (from existing matrix)
- **Option C (Foundry IQ):** Azure AI Search chunking quality (from Phase 2 matrix)
- **Option C Workaround:** Custom skillset or configuration required to improve chunking
- **Net Advantage:** Which option handles this file type better after workarounds are applied on both sides
- **Verdict:** One of:
  - **A wins** — Copilot handles it better or equally, with less effort
  - **C wins** — Foundry IQ handles it better, and the engineering effort is justified
  - **Draw** — Both require similar workarounds with similar outcomes
  - **Neither** — Both handle it poorly; the file type needs restructuring regardless of platform

### Analysis Requirements

For each file type, the comparison must address:

1. **Baseline chunking quality** — Are both platforms equally bad at YAML? Or does Azure AI Search's custom skillset pipeline give it an edge?
2. **Workaround effort** — Copilot workarounds are scoped instruction files and companion Markdown (hours). Foundry IQ workarounds are custom skillsets and Azure Functions (days-weeks). Is the quality difference worth the effort difference?
3. **Maintenance burden** — Copilot workarounds are Markdown files in git. Foundry IQ workarounds are Azure services that need monitoring, scaling, and cost management.
4. **The "direct file access" factor** — Copilot reads files directly from the workspace. Foundry IQ retrieves chunks from an index. For file types where direct access works (the agent reads the whole file), retrieval quality is irrelevant.

### Key Hypothesis to Test

The existing evaluation argues that Copilot's direct file access bypasses chunking for most use cases. The comparison matrix should explicitly test this hypothesis for each file type:

- **File types where direct access works:** The agent reads the whole file. Chunking quality is irrelevant. Advantage: A (zero infrastructure).
- **File types where retrieval matters:** The agent cannot read every relevant file (too many, too large, or spread across repos). Chunking quality affects retrieval quality. Advantage: potentially C, if custom skillsets meaningfully improve it.
- **File types where neither helps:** The format is inherently opaque to LLMs (binary, visual). Both platforms need the same kind of bridge (MCP, export pipeline).

---

## Phase 4: Page Construction and Publishing

### Page Title

**"File-Type Handling: Option A vs Option C"** (or similar — should be distinct from the existing strategy page)

### Page Structure

1. TL;DR admonition — one-sentence verdict
2. Why this comparison matters — addresses the "maybe Option C is better at chunking" argument
3. Option C File-Type Decision Matrix (full)
4. A-vs-C Comparison Matrix (full)
5. Analysis: Where does custom infrastructure actually help?
6. Analysis: The direct-access factor
7. Conclusion: Does Option C's chunking advantage (if any) justify its engineering cost?
8. See also links

### Publishing

- Add `<!-- CONFLUENCE-PUBLISH -->` header
- Add to mkdocs.yml nav under Evidence section
- Add to homepage Page Index table
- Cross-reference from existing File-Type Chunking Strategy page
- Cross-reference from Build vs Leverage page
- Cross-reference from Foundry IQ comparison page

---

## Phase 5: Cross-References and Site Integration

After publishing, update existing pages:

1. **File-Type Chunking Strategy** — Add "See also" link to the new comparison page. Add a note in the introduction acknowledging the matrix is Option A-specific and pointing to the comparison.
2. **Build vs Leverage** — Reference the comparison matrix in the "PlantUML Chunking Argument" section as evidence.
3. **What Does Foundry IQ Actually Require** — Add a row or section on file-type chunking customization effort.
4. **Homepage index.md** — Add the new page to the Page Index table.
5. **Confluence URL registry** — Add the new page after publishing.

---

## Implementation Sequence Summary

| Step | What | Effort | Dependency |
|------|------|--------|------------|
| 1 | Deep Research Round 1: Azure AI Search chunking mechanics | 1 session | None |
| 2 | Deep Research Round 2: Foundry IQ knowledge base configuration | 1 session | None (can run in parallel with Step 1) |
| 3 | Incorporate research findings into evidence notes | 1-2 hours | Steps 1-2 |
| 4 | Write Option C File-Type Decision Matrix | 2-3 hours | Step 3 |
| 5 | Write A-vs-C Comparison Matrix | 2-3 hours | Step 4 |
| 6 | Write analysis sections and page framing | 1-2 hours | Step 5 |
| 7 | Add to site nav, homepage, cross-references | 30 min | Step 6 |
| 8 | Publish to Confluence | 15 min | Step 7 |

**Total estimated effort:** 2 deep research sessions + 1 day of writing and integration.

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Azure AI Search documentation lacks file-type-specific chunking details | Matrix has "undocumented" entries that weaken the comparison | State gaps explicitly; frame as "burden of proof is on Option C to demonstrate improvement" |
| Foundry IQ is in preview; behavior may change | Matrix may become stale | Date-stamp all findings; note preview status prominently |
| Custom skillset capabilities are overstated in documentation | Comparison may credit Option C with capabilities it cannot deliver in practice | Distinguish between "documented capability" and "empirically verified" in every cell |
| Research confirms Option C chunks files identically to Option A | The new page adds minimal analytical value | This is itself a finding — "Option C does not improve chunking quality" is a valuable conclusion that strengthens the existing recommendation |
