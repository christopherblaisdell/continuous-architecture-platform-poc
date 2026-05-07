# Follow-Up Research Prompt: AI Instruction Taxonomy — Correcting Categorical Errors and Filling Critical Gaps

**Usage**: Paste this as a follow-up message in the same AI session that produced `AI-INSTRUCTION-TAXONOMY.md`. The session has full context of that document.

---

## Prompt

The research document you produced is a strong foundation, but it contains several categorical errors and critical gaps that undermine its central thesis and its usefulness as a framework for achieving real AI instruction portability. Before I can use this as a reference, I need you to produce a revised and extended version that corrects these issues. Please write a comprehensive research document that addresses every point below.

---

### Issue 1 — MCP is categorized in the wrong layer

The document places MCP alongside Cursor `.mdc` files, GitHub Copilot `.instructions.md`, and Roo Code `.clinerules` as if they are answers to the same question. They are not.

MCP is a **runtime integration protocol** — an RPC transport for connecting a model to external systems at inference time. It answers: *"What can the AI access and invoke right now?"*

Behavioral instruction files answer: *"How does this AI reason, what constraints govern its behavior, what persona does it adopt, what standards must it follow?"*

These are fundamentally different layers. Please:

1. Explicitly define and name the three distinct layers that this taxonomy is actually spanning:
   - **Layer 1 — Behavioral Specification**: The authored instructions that define AI reasoning, constraints, personas, and standards (the actual subject of this taxonomy)
   - **Layer 2 — Change Governance**: The process by which Layer 1 artifacts are proposed, reviewed, versioned, and archived
   - **Layer 3 — Runtime Integration**: The transport mechanisms that deliver context and capability to the model at inference time (where MCP belongs)

2. Clarify definitively: MCP belongs in Layer 3. It is not a behavioral instruction system. The document's recommendation that MCP be extended with an "Instruction Content block" conflates the transport layer with the specification layer — this is architecturally unsound. Explain why, and propose what the correct layer for that extension would be.

3. Research and document what Layer 3 actually contains in depth — not just MCP, but the full ecosystem of runtime context delivery mechanisms: RAG pipelines, vector stores, tool registries, agent memory architectures, and how these interact with Layer 1 instructions. Provide authoritative sources and links.

---

### Issue 2 — OpenSpec is not characterized accurately

The document does not cover OpenSpec. It must be covered as a primary subject, positioned correctly as a **Layer 2 (Change Governance)** system, not a portability abstraction layer.

Please research and document:

1. **What OpenSpec actually does**: Spec-Driven Development for AI instruction files. The `/opsx:propose → /opsx:apply → /opsx:archive` workflow. Delta Specs. The artifact structure: `proposal.md`, `spec.md`, `design.md`, `tasks.md`. The phase-gated execution model. The canonical hub + derived files pattern (one source of truth, platform-specific derived files). RFC 2119 language enforcement.

2. **What OpenSpec does NOT do**: It does not abstract away platform-specific instruction formats. The downstream files are still platform-specific (`.clinerules` for Roo Code, `copilot-instructions.md` for GitHub Copilot, `.mdc` for Cursor). OpenSpec governs the *process* of changing these files — it does not unify their *schemas*.

3. **Why this distinction matters for portability**: True AI instruction portability requires a solution at Layer 1 (a portable behavioral specification schema), not just at Layer 2 (governance). OpenSpec enables platform-agnostic *governance* of platform-*specific* instructions. That is valuable, but it is not the same as portability. Document this gap explicitly and explain what would need to exist at Layer 1 to close it.

4. **How OpenSpec and a future Layer 1 standard interact**: If a formal behavioral specification schema were standardized (see Issue 3 below), OpenSpec's governance workflow could operate on that schema instead of on platform-specific files, achieving true end-to-end portability. Describe this architecture.

---

### Issue 3 — The portability gap is identified but not researched

The document correctly identifies in its final section that no formal typed schema exists for Layer 1 behavioral specifications, and that this is the central standardization gap. But it does not research what already exists toward filling that gap. Please produce a thorough investigation of:

1. **Existing schema proposals and working drafts**: Are there any formal proposals (IETF drafts, W3C notes, OASIS working documents, ISO/IEC NWIPs) for a typed behavioral instruction schema? Search specifically for:
   - W3C AI Agent Protocol Community Group deliverables and meeting notes (link to actual CG page and any published outputs)
   - OASIS committees covering agentic AI behavior standards
   - IEEE P3394, P3395, or related AI agent standards in progress
   - ISO/IEC JTC 1/SC 42 work items beyond 42001 that address agentic behavior
   - IETF working groups covering agent-to-agent communication and behavioral contracts

2. **Academic proposals for instruction schemas**: Beyond PROMPTPRISM and the Instruction Hierarchy (which the document covers), what formal schema proposals have emerged from NeurIPS, ICLR, ACL, or AAAI specifically for structured behavioral instruction representation? Find and link to specific papers.

3. **Industry schema proposals**: Have any vendors (Anthropic, OpenAI, Google DeepMind, Microsoft, Hugging Face) published formal schema specifications — not just file format conventions — for behavioral AI instructions? Review model cards, system card formats, and any structured instruction schema proposals.

4. **The Constitutional AI angle**: Anthropic's Constitutional AI defines behavioral constraints as explicit principles. Has Anthropic or the research community proposed a machine-readable schema for constitutional principles that could serve as a portable behavioral specification format? Link to relevant papers and any open-source implementations.

---

### Issue 4 — Portability strategy is missing

Given our goal of achieving AI instruction portability across GitHub Copilot, Roo Code, Cursor, Windsurf, and other tools — the document does not provide a concrete, actionable portability strategy. Please produce:

1. **A layered portability framework** with three tiers:
   - **Semantic portability**: Writing instructions in platform-agnostic language (RFC 2119 MUST/SHOULD/MAY, structured sections, no tool-specific syntax) so they can be copied to any platform with minimal adaptation
   - **Structural portability**: Using a hub-and-spoke architecture where a canonical source file drives platform-specific derived files (this is what OpenSpec's governance enables today)
   - **Schema portability**: A hypothetical future where instructions conform to a formal typed schema that any compliant AI tool can natively parse and apply (the gap that currently exists)

2. **Current state of each tier**: Which tier is achievable today? What tools or frameworks support it? What are the blockers?

3. **Migration path**: If someone is today using GitHub Copilot `.instructions.md` files and wants to switch to Roo Code or Cursor — what does that migration look like? What does OpenSpec make easier? What remains manual?

4. **The OpenSpec + formal schema future state**: Describe the target architecture in which a developer writes a single behavioral specification in a standard schema, and OpenSpec's governance workflow automatically produces compliant derived files for every target AI tool.

---

### Issue 5 — Cross-platform instruction routing is underspecified

The document covers routing mechanisms per-platform (Cursor's YAML frontmatter, Copilot's `applyTo` glob, Roo Code's mode system) but does not analyze the routing semantics comparatively. Please:

1. **Produce a formal comparison of routing models** across Cursor, Copilot, Roo Code, Windsurf, and Continue.dev:
   - What triggers instruction loading? (always-on, glob match, semantic match, explicit invocation, mode activation)
   - What is the conflict resolution model when multiple instructions apply? (priority order, last-writer-wins, explicit precedence)
   - What is the scope model? (global, repo, directory, file, session)
   - Link to official documentation for each routing model

2. **Identify the routing primitives that are common** across platforms — the intersection set that a portable routing specification could target

3. **Identify what cannot be ported** — routing features that are platform-specific with no cross-platform equivalent

---

### Issue 6 — Security model of behavioral instructions is absent

The Instruction Hierarchy (system > user > tool > resource privilege tiers) is mentioned but the security implications are not researched. Given that AI instructions in enterprise settings define safety boundaries, access controls, and prohibited actions, please research:

1. **Prompt injection via instruction files**: Can a malicious instruction in a `.clinerules` file or `.mdc` rule override safety constraints? What mitigations exist? Link to CVEs or security research.

2. **Privilege escalation via MCP tools**: If an MCP tool delivers a Prompt that contradicts a behavioral instruction at Layer 1, how do current AI tools resolve this? Is there an established security model?

3. **Instruction integrity**: What mechanisms exist (or should exist) for verifying that instruction files have not been tampered with? How does OpenSpec's immutable archive contribute to this? What gaps remain?

4. **OWASP AI Security Top 10 relevance**: Map the relevant OWASP AI Security Top 10 risks to the instruction taxonomy layers and identify where current tooling has no mitigation.

---

### Deliverable Requirements

Please produce a single, comprehensive research document that:

1. **Opens with a corrected three-layer framework** — clearly distinguishing behavioral specification (Layer 1), change governance (Layer 2), and runtime integration (Layer 3) — before discussing any specific tools or protocols

2. **Covers every section requested above** with depth appropriate to a technical architecture decision record

3. **Includes links to authoritative sources** for every factual claim — academic papers (with DOI or arXiv link), official documentation, specification drafts, W3C/OASIS/IETF pages, vendor documentation. Every claim that can be linked to a primary source must be.

4. **Covers OpenSpec as a first-class subject** in Layer 2, with its workflow, its strengths, its limitations relative to full portability, and how it fits into a future-state portability architecture

5. **Provides a concrete portability strategy** that is actionable today, including what can be done now with OpenSpec + hub-and-spoke + RFC 2119 language, and what requires a future Layer 1 standard to complete

6. **Ends with a gap analysis table**: For each gap in the current landscape (no formal Layer 1 schema, no cross-platform routing standard, no instruction integrity mechanism, etc.), list the gap, the current best mitigation, and the standardization body or initiative most likely to close it

7. **Formats all source citations as inline hyperlinks** — not footnotes, not a bibliography at the end — so the document is useful as a live reference

The goal of this document is to serve as the authoritative internal reference for our AI instruction governance strategy, informing decisions about which Layer 1 specification approach to adopt, how to implement OpenSpec as our Layer 2 governance framework, and how to design our hub-and-spoke instruction architecture for maximum future compatibility with emerging standards.
