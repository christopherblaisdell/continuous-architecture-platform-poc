# Deep Research Prompt: Everything as Code (EaC) — Maturity Models, Standards, and Industry Adoption

> **BLUEPRINT DOCUMENT.** This file is part of the portable EaC Blueprint and is exported to corporate Instance workspaces. It is target-agnostic — it contains no NovaTrek-specific content. An Instance team can re-run this prompt against a fresh deep-research session to get current industry data.

**Usage**: This is a deep research prompt suitable for an AI deep-research session (e.g., Claude/GPT/Gemini deep research mode). The expected output should be pasted into [Deep Research Response — EaC Maturity Model](DEEP-RESEARCH-PROMPT-EAC-MATURITY-MODEL-RESPONSE.md).

---

## Prompt

An enterprise software architecture practice is undertaking a transformation to make every architectural artifact — diagrams, capabilities, ADRs, wireframes, AI instructions, policies, runbooks — declarative, version-controlled, machine-readable, and human-readable. This is the philosophy commonly called **"Everything as Code" (EaC)**, a generalization of Infrastructure as Code, Diagrams as Code, Documentation as Code, Policy as Code, and adjacent disciplines.

Produce a comprehensive research document covering everything below. Include inline hyperlinks to authoritative primary sources for every factual claim — academic papers (DOI/arXiv), official documentation, vendor docs, conference talks, ThoughtWorks Technology Radar entries, IEEE / ISO / OASIS / W3C / IETF specifications and working drafts. The deliverable must be useful as the authoritative internal reference informing our adoption strategy.

### Section 1 — Terminology and Provenance

1. **Origin of "Everything as Code"**: Trace the term. Who first coined it? What conference talks, blog posts, or books popularized it? Provide direct links.
2. **Synonyms and adjacent terms**: Document every commonly-used synonym (Software-Defined X, Declarative-First, GitOps, Codification, Spec-Driven Development, Continuous Architecture, Architecture as Code) — with sources, dates of emergence, and the communities that use each term.
3. **Naming the transformation**: When an organization adopts EaC across its practice, what is that *transformation* called? Is there a recognized industry term, or is the field still naming it ad-hoc? Cite examples from large-enterprise transformations.
4. **Distinction vs. "DevOps"**: How does EaC relate to DevOps, GitOps, Platform Engineering, and Continuous Architecture as practices? Provide a clear conceptual map.

### Section 2 — The "X as Code" Family — Comprehensive Catalog

For each "X as Code" discipline below, provide: definition, year it emerged, dominant tools, official spec/standard if any, current adoption level (cite ThoughtWorks Radar where applicable), and authoritative reference links.

- Infrastructure as Code (IaC)
- Configuration as Code (CaC)
- Pipeline as Code (PaC)
- Documentation as Code (Docs as Code)
- Diagrams as Code (DaC)
- Policy as Code (PolaC)
- Architecture as Code (AaC)
- Security as Code (SecaC)
- Compliance as Code (CompaC)
- Tests as Code (TaC) — particularly BDD/Gherkin as specification
- Wireframes as Code / UI Design as Code
- Governance as Code (GaC)
- AI Instructions as Code (AIaC) — emerging in 2024-2026
- Runbooks as Code / Operations as Code
- Data Contracts as Code
- API as Code (OpenAPI, AsyncAPI, GraphQL SDL)
- Schema as Code (JSON Schema, Avro, Protobuf)
- Identity as Code

For each, also note: **what is the canonical declarative format**, **what generators consume it**, and **what validators exist**.

### Section 3 — Maturity Models for EaC Adoption

Find and document every published maturity model relevant to EaC adoption:

1. **DORA** State of DevOps maturity tiers (and how they relate to EaC) — link to current report
2. **CALMS** model (Culture, Automation, Lean, Measurement, Sharing) — origin and link
3. **OpenGitOps Principles maturity** (CNCF) — link
4. **CMMI for DevOps** if applicable
5. **ThoughtWorks Sensible Defaults** for IaC and DocsAsCode
6. **Architecture Maturity Models**: TOGAF ACMM, NASCIO Enterprise Architecture Maturity Model — and how they map to EaC adoption
7. **Any vendor or analyst maturity models** (Gartner, Forrester, IDC) covering "as code" adoption

Synthesize these into a **single recommended EaC maturity model with 0-9 levels** that an architecture practice can use to self-assess and roadmap its adoption.

### Section 4 — Architecture as Code (AaC) — Deep Dive

This is our most under-standardized pillar. Investigate:

1. **The AaC project** (DevOps-MBSE) — https://github.com/DevOps-MBSE/AaC — full evaluation: scope, adoption, status, who uses it
2. **Structurizr DSL** — https://structurizr.com/dsl — Simon Brown's C4 DSL, adoption, ecosystem
3. **Likec4** — https://likec4.dev/ — modern alternative, adoption
4. **IcePanel** — https://icepanel.io/ — collaborative C4 tool, what is its as-code story
5. **CALM (Common Architecture Language Model)** — FINOS / Bian — https://github.com/finos/architecture-as-code — full evaluation
6. **ArchiMate** — Open Group — does it have an as-code representation? What is the canonical text format?
7. **MBSE / SysML v2** — https://www.omg.org/spec/SysML/2.0/ — relevance to architecture as code
8. **Mermaid** for architecture diagrams — adoption and limitations
9. **Comparison table**: feature matrix across all of the above
10. **Recommendation**: For an enterprise adopting AaC today (mid-2026), what stack should they adopt for sequence diagrams, C4, and capability modeling?

### Section 5 — AI Instructions as Code (AIaC) — Deep Dive

Investigate the formalization of AI behavioral instruction governance:

1. **OpenSpec** — https://github.com/Fission-AI/OpenSpec — full evaluation
2. **AWS Kiro** — https://kiro.dev/ — Amazon's spec-driven IDE, evaluation
3. **GitHub Spec-Kit** — https://github.com/github/spec-kit — relevance to AIaC
4. **Anthropic Constitutional AI** — https://arxiv.org/abs/2212.08073 — relevance to declarative behavioral specs
5. **The Instruction Hierarchy** — https://arxiv.org/abs/2404.13208 — relevance to privilege tiers in instruction files
6. **MCP (Model Context Protocol)** — confirm it is Layer 3 (runtime integration), not Layer 1 (behavioral specification). Cite the spec.
7. **W3C AI Agent Protocol Community Group** — https://www.w3.org/community/agentprotocol/ — current deliverables
8. **OASIS / IEEE / ISO standards** addressing AI instruction schemas — every working draft, every NWIP
9. **Vendor instruction file formats** — comparative matrix: Copilot `.instructions.md`, Roo `.clinerules`, Cursor `.mdc`, Windsurf `.windsurfrules`, Continue.dev `config.yaml`, Aider `.aider.conf.yml` — link to official docs for each
10. **Hub-and-spoke architectures**: who else has published this pattern for AI instruction portability?

### Section 6 — Codification Patterns

Document the canonical patterns used across EaC implementations:

1. **The Codify-Validate-Generate (CVG) loop** — has anyone formally named or published this pattern? Cite if so.
2. **Single Source of Truth (SSoT) architecture** — origins, references
3. **Hub and Spoke** for canonical/derived files — references
4. **Drift detection** — how do mature EaC implementations detect drift between source and generated outputs
5. **Schema-first development** — JSON Schema, OpenAPI, AsyncAPI, Avro patterns
6. **Generator pipelines** — how mature implementations chain generators (e.g., OpenAPI → SDK → docs → diagrams)
7. **GitOps as the operational model** — Flux, Argo CD references; relevance to EaC beyond infrastructure

### Section 7 — Anti-Patterns and Failure Modes

Document the failure modes mature EaC adopters have published lessons-learned about:

1. **Schema drift** between code and YAML
2. **Generator divergence** when teams hand-edit generated outputs
3. **Bypass culture** when reviewers wave through non-compliant changes
4. **Tool lock-in** when a "canonical" format is actually proprietary
5. **Documentation drift** when docs-as-code falls out of sync with code
6. **Over-codification** — when forcing every artifact into code creates more friction than value
7. **AI hallucination amplification** when AI agents author against unvalidated schemas

For each anti-pattern, cite at least one published case study, blog post, or post-mortem.

### Section 8 — Standardization Status

Investigate the formal standardization status of EaC and each pillar:

1. Is there an ISO/IEC working group on EaC?
2. Is there an OpenChain or OpenSSF initiative on artifact codification?
3. Is there a CNCF subproject for EaC beyond GitOps?
4. Is there an IEEE working group?
5. What is the most likely path to a formal EaC standard?

### Section 9 — Vendor and Tool Landscape

Produce a comprehensive matrix of EaC tools by pillar — name, vendor, license, canonical format, adoption level, ThoughtWorks Radar status, official link.

### Section 10 — Adoption Case Studies

Identify and summarize 5+ public case studies of large enterprises that have adopted EaC (or specific pillars) at scale:

- Capital One (their published IaC and architecture-as-code work)
- Netflix (their internal platform)
- Spotify (Backstage and architecture catalogs)
- HashiCorp customer references
- ThoughtWorks client stories

For each: scope of EaC adoption, tools used, lessons learned, links to public talks or blogs.

### Section 11 — Recommendations for Adoption

Given everything above, produce concrete recommendations for an enterprise architecture practice in 2026:

1. **What pillars to adopt first** (priority order with rationale)
2. **What tools to standardize on** for each pillar
3. **What governance pattern to adopt** (OpenSpec or alternative) for AI instructions specifically
4. **What maturity level to target** by Q4 2026 vs Q4 2027
5. **What metrics to measure** EaC adoption progress
6. **What KPIs prove EaC is delivering value**

### Section 12 — Gap Analysis

End with a comprehensive table of remaining gaps in the EaC landscape:

| Gap | Current best mitigation | Standardization body most likely to close it | Estimated timeline |
|-----|------------------------|---------------------------------------------|--------------------|

---

## Deliverable Format

Single comprehensive document. Section headings as above. Inline hyperlinks (not footnotes). Every factual claim sourced. Comparison tables wherever possible. The deliverable should be 8000-15000 words and serve as our authoritative internal EaC reference.
