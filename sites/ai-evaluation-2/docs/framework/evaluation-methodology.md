<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2615967849/Evaluation+Methodology -->

# Evaluation Methodology

## Purpose

This document defines the systematic methodology for comparing, evaluating, and deciding between three AI platform options for the solution architecture practice:

- **Option A:** GitHub Copilot Pro+ (SaaS, lean)
- **Option B:** Roo Code + Kong AI Gateway (custom RAG, token-based)
- **Option C:** Bespoke Architecture Agent (Azure AI Foundry, custom build)

The methodology produces a defensible, weighted score that stakeholders can audit, challenge, and ultimately use to make an informed decision.

---

## Methodology Overview

### 1. Define Evaluation Factors

Twelve evaluation factors are organized into four categories aligned with ISO 25010 quality characteristics and enterprise decision-making concerns. Each factor has a clear definition, measurable indicators, and a scoring rubric.

### 2. Assign Weights

Each factor receives a percentage weight reflecting its importance to the architecture practice. Weights are assigned by the evaluation team before scoring begins — not adjusted after results are known. Total weights sum to 100%.

### 3. Score Each Option

Each option is scored 1-5 on every factor using the rubric definitions below. Scores are evidence-based: every score must cite a source (run data, vendor documentation, pricing page, POC result, or reasoned analysis with stated assumptions).

### 4. Calculate Weighted Scores

For each option: `Weighted Score = Sum of (Factor Score x Factor Weight)`. Maximum possible score is 5.00.

### 5. Sensitivity Analysis

Test whether the outcome changes if weights shift. If a 5-point weight change on any single factor flips the winner, the result is fragile and requires additional evidence gathering on that factor.

### 6. Recommendation

The highest weighted score wins, subject to:

- No factor scored 1 (critical failure) unless the evaluation team explicitly accepts the risk
- Sensitivity analysis confirms the result is robust
- Qualitative factors (team readiness, organizational appetite) are documented as context

---

## Evaluation Factors

### Category 1: Economics (Weight: 29%)

#### EF-01: Total Cost of Ownership (15%)

**Definition:** The fully loaded monthly cost per architect seat, including subscription fees, infrastructure, engineering investment (amortized over 24 months), and operational overhead.

| Score | Criteria |
|-------|----------|
| 5 | Less than $50/seat/month, no engineering investment |
| 4 | $50-100/seat/month, minimal engineering investment |
| 3 | $100-200/seat/month, moderate engineering investment (2-4 dev-months) |
| 2 | $200-400/seat/month, significant engineering investment (6-12 dev-months) |
| 1 | Over $400/seat/month or requires dedicated team to operate |

#### EF-02: Cost Predictability (8%)

**Definition:** How predictable and controllable the monthly cost is. Fixed costs score higher than variable costs. Token-based billing with no ceiling scores lowest.

| Score | Criteria |
|-------|----------|
| 5 | Fixed monthly cost regardless of usage |
| 4 | Fixed base with small, bounded variable component |
| 3 | Variable but predictable within a 30% range |
| 2 | Highly variable, dependent on usage patterns |
| 1 | Unbounded variable cost with no ceiling mechanism |

#### EF-03: Cost Scaling (6%)

**Definition:** How cost behaves as the team grows from 1 architect to 5 to 20. Linear per-seat scaling scores highest. Economies of scale (shared infrastructure amortized) improve the score.

| Score | Criteria |
|-------|----------|
| 5 | Strictly linear per-seat scaling, no shared infrastructure cost |
| 4 | Near-linear with small shared component that amortizes well |
| 3 | Sub-linear scaling — shared infrastructure reduces per-seat cost at scale |
| 2 | Requires step-function infrastructure investment at team thresholds |
| 1 | Cost grows super-linearly with team size |

---

### Category 2: Quality and Capability (Weight: 36%)

#### EF-04: Architecture Output Quality at Operating Budget (18%)

**Definition:** The quality of AI-generated architecture artifacts (solution designs, ADRs, impact assessments, diagrams) as measured by the scoring rubric applied to controlled scenarios — **using the model tier that each option will actually deploy at its operating budget, not the theoretical best model available.**

This factor explicitly accounts for budget-constrained model selection. An option that offers access to a frontier model but whose budget forces the use of a cheaper model is scored on the cheaper model's actual output quality. See [Model Quality at Budget](../evidence/model-quality-at-budget.md) for the detailed analysis.

| Score | Criteria |
|-------|----------|
| 5 | Frontier model included at operating budget; greater than 95% rubric score, minimal corrections |
| 4 | Strong model affordable at budget; 85-95% rubric score, minor corrections |
| 3 | Mid-tier model at budget; 70-85% rubric score, moderate corrections |
| 2 | Budget model forced by cost constraints; 50-70% rubric score, significant rework required |
| 1 | Cheapest model only affordable; below 50% or architecturally unsound output |

#### EF-05: Domain Context Awareness (8%)

**Definition:** The platform's ability to understand and apply domain-specific knowledge — service boundaries, data ownership rules, safety requirements, naming conventions, and architectural standards.

| Score | Criteria |
|-------|----------|
| 5 | Consistently applies domain rules without reminding; references prior decisions |
| 4 | Applies most domain rules; occasional gaps on edge cases |
| 3 | Needs explicit prompting for domain rules but follows them when reminded |
| 2 | Frequently ignores domain rules; produces generic output |
| 1 | No domain awareness; output is indistinguishable from generic AI |

#### EF-06: Tool Integration Breadth (3%)

**Definition:** The range of enterprise tools the platform can access — ticketing, logs, source control, specs, diagrams, documentation portals.

| Score | Criteria |
|-------|----------|
| 5 | Accesses all required enterprise tools natively or via standard protocols |
| 4 | Accesses most tools; 1-2 gaps fillable with minimal custom work |
| 3 | Accesses core tools; significant gaps require custom integration |
| 2 | Limited to workspace files; enterprise tool access requires extensive custom work |
| 1 | No tool integration beyond basic file read/write |

#### EF-07: Multi-Model Flexibility (3%)

**Definition:** The platform's ability to use different AI models for different tasks (e.g., faster/cheaper model for triage, stronger model for design) and to adopt new models as they become available.

| Score | Criteria |
|-------|----------|
| 5 | Full model selection per task; new models available within days of release |
| 4 | Multiple models available; some delay on new model adoption |
| 3 | 2-3 model options; new models take weeks to months |
| 2 | Single model or very limited selection |
| 1 | Locked to one model with no alternative |

#### EF-13: Architecture Content Retrieval Quality (5%)

**Definition:** How well the platform chunks, indexes, and retrieves the specific file types used in architecture work — OpenAPI/AsyncAPI YAML, PlantUML diagrams, Markdown ADRs, source code, YAML metadata, and Figma design tokens. This factor measures retrieval fidelity for architecture artifacts specifically, not general text search quality. Platforms with direct file access (bypassing chunking entirely) score higher because the architect's primary workflow reads whole files in context.

See [File-Type Handling: A vs C](../evidence/filetype-handling-a-vs-c.md) for the evidence base and [File-Type Chunking Strategy](filetype-chunking-strategy.md) for the per-file-type analysis.

| Score | Criteria |
|-------|----------|
| 5 | Structure-aware chunking for all architecture file types; direct file access; no workarounds needed |
| 4 | Structure-aware chunking for most file types (code, Markdown); low-effort workarounds for the rest; direct file access available |
| 3 | Structure-aware chunking for some file types; moderate-effort workarounds for others; retrieval-only (no direct file access) |
| 2 | Plain text chunking for most file types; custom engineering required for structure-aware retrieval; retrieval-only |
| 1 | No indexing capability; files must be manually copied into prompts |

---

### Category 3: Operational Fitness (Weight: 20%)

#### EF-08: Time to Value (8%)

**Definition:** How quickly the platform can be deployed and producing useful architecture output for the first architect.

| Score | Criteria |
|-------|----------|
| 5 | Same day — install extension, configure instructions, start working |
| 4 | 1-2 weeks — setup, configuration, and initial customization |
| 3 | 1-3 months — infrastructure provisioning, custom development, testing |
| 2 | 3-6 months — significant engineering, procurement, and integration work |
| 1 | 6+ months — major platform build before any architecture value |

#### EF-09: Operational Complexity (7%)

**Definition:** The ongoing operational burden — infrastructure to maintain, updates to apply, monitoring to watch, incidents to respond to.

| Score | Criteria |
|-------|----------|
| 5 | Zero infrastructure; vendor-managed SaaS; updates are automatic |
| 4 | Minimal infrastructure; occasional configuration updates |
| 3 | Moderate infrastructure; requires dedicated operational attention monthly |
| 2 | Significant infrastructure; requires weekly operational attention |
| 1 | Heavy infrastructure; requires dedicated operations staff |

#### EF-10: Workflow Integration (5%)

**Definition:** How naturally the platform fits into the architect's existing daily workflow — VS Code, git, PR review, documentation publishing.

| Score | Criteria |
|-------|----------|
| 5 | Native VS Code integration; no context switching; git-native |
| 4 | VS Code-based with minor workflow adaptations |
| 3 | Separate interface but integrates with git and existing toolchain |
| 2 | Requires significant workflow changes; parallel tool usage |
| 1 | Entirely separate workflow; copy-paste between systems |

---

### Category 4: Strategic and Risk (Weight: 15%)

#### EF-11: Vendor Lock-in Risk (8%)

**Definition:** The degree to which the platform creates dependency on a single vendor, and the cost/effort to switch if needed.

| Score | Criteria |
|-------|----------|
| 5 | Open standards throughout; all artifacts portable; switch in days |
| 4 | Mostly portable; instruction format is platform-specific but content transfers |
| 3 | Moderate lock-in; 1-2 months to migrate core workflows |
| 2 | Significant lock-in; custom integrations not portable; 3-6 month migration |
| 1 | Deep lock-in; proprietary formats; migration would be a rebuild |

#### EF-12: Governance and Compliance (6%)

**Definition:** The platform's ability to meet enterprise governance requirements — audit trails, data residency, access control, and compliance with corporate security policies.

| Score | Criteria |
|-------|----------|
| 5 | Enterprise-grade: SOC 2, data residency controls, full audit trail, SSO |
| 4 | Strong governance; minor gaps in audit trail or data residency options |
| 3 | Adequate governance; meets baseline requirements with some configuration |
| 2 | Limited governance; significant gaps in audit or compliance support |
| 1 | No governance capabilities; data handling is opaque |

---

## Weight Summary

| Category | Factor | Weight |
|----------|--------|--------|
| **Economics (29%)** | EF-01: Total Cost of Ownership | 15% |
| | EF-02: Cost Predictability | 8% |
| | EF-03: Cost Scaling | 6% |
| **Quality and Capability (37%)** | EF-04: Architecture Output Quality at Operating Budget | 18% |
| | EF-05: Domain Context Awareness | 8% |
| | EF-06: Tool Integration Breadth | 3% |
| | EF-07: Multi-Model Flexibility | 3% |
| | EF-13: Architecture Content Retrieval Quality | 5% |
| **Operational Fitness (20%)** | EF-08: Time to Value | 8% |
| | EF-09: Operational Complexity | 7% |
| | EF-10: Workflow Integration | 5% |
| **Strategic and Risk (14%)** | EF-11: Vendor Lock-in Risk | 8% |
| | EF-12: Governance and Compliance | 6% |
| | **Total** | **100%** |

---

## Scoring Process

### Step 1: Evidence Gathering

For each factor, collect evidence from:

- **Run data** — actual scenario execution results (quality scores, cost measurements)
- **Vendor documentation** — published pricing, architecture, compliance certifications
- **POC results** — hands-on testing where run data is not yet available
- **Reasoned analysis** — expert judgment with explicitly stated assumptions (marked as such)

### Step 2: Individual Scoring

Score each option 1-5 on each factor. Document the rationale and evidence source for every score in the scoring matrix.

### Step 3: Weighted Calculation

| Option | EF-01 (15%) | EF-02 (8%) | ... | EF-12 (7%) | **Weighted Total** |
|--------|-------------|------------|-----|------------|-------------------|
| A | score x 0.15 | score x 0.08 | ... | score x 0.07 | Sum |
| B | score x 0.15 | score x 0.08 | ... | score x 0.07 | Sum |
| C | score x 0.15 | score x 0.08 | ... | score x 0.07 | Sum |

### Step 4: Sensitivity Analysis

For each factor, test: "If this weight changed by +/- 5 percentage points (redistributed equally among other factors), would the winning option change?" Flag any factor where the answer is yes — these are **swing factors** requiring additional evidence.

### Step 5: Critical Failure Check

If any option scores 1 on any factor, document it as a **critical risk**. The evaluation team must explicitly accept the risk or disqualify the option.

---

## Scoring Matrix

### Option A: GitHub Copilot Pro+

| Factor | Score | Evidence | Source |
|--------|-------|----------|--------|
| EF-01: Total Cost of Ownership | | | |
| EF-02: Cost Predictability | | | |
| EF-03: Cost Scaling | | | |
| EF-04: Architecture Output Quality | | | |
| EF-05: Domain Context Awareness | | | |
| EF-06: Tool Integration Breadth | | | |
| EF-07: Multi-Model Flexibility | | | |
| EF-08: Time to Value | | | |
| EF-09: Operational Complexity | | | |
| EF-10: Workflow Integration | | | |
| EF-11: Vendor Lock-in Risk | | | |
| EF-12: Governance and Compliance | | | |

### Option B: Roo Code + Kong AI

| Factor | Score | Evidence | Source |
|--------|-------|----------|--------|
| EF-01: Total Cost of Ownership | | | |
| EF-02: Cost Predictability | | | |
| EF-03: Cost Scaling | | | |
| EF-04: Architecture Output Quality | | | |
| EF-05: Domain Context Awareness | | | |
| EF-06: Tool Integration Breadth | | | |
| EF-07: Multi-Model Flexibility | | | |
| EF-08: Time to Value | | | |
| EF-09: Operational Complexity | | | |
| EF-10: Workflow Integration | | | |
| EF-11: Vendor Lock-in Risk | | | |
| EF-12: Governance and Compliance | | | |

### Option C: Bespoke Architecture Agent

| Factor | Score | Evidence | Source |
|--------|-------|----------|--------|
| EF-01: Total Cost of Ownership | | | |
| EF-02: Cost Predictability | | | |
| EF-03: Cost Scaling | | | |
| EF-04: Architecture Output Quality | | | |
| EF-05: Domain Context Awareness | | | |
| EF-06: Tool Integration Breadth | | | |
| EF-07: Multi-Model Flexibility | | | |
| EF-08: Time to Value | | | |
| EF-09: Operational Complexity | | | |
| EF-10: Workflow Integration | | | |
| EF-11: Vendor Lock-in Risk | | | |
| EF-12: Governance and Compliance | | | |

---

## Results Summary

*To be completed after scoring.*

| Option | Weighted Score | Rank | Critical Failures |
|--------|---------------|------|-------------------|
| A: GitHub Copilot Pro+ | — | — | — |
| B: Roo Code + Kong AI | — | — | — |
| C: Bespoke Architecture Agent | — | — | — |

### Sensitivity Analysis Results

*To be completed after scoring.*

### Recommendation

*To be completed after scoring and sensitivity analysis.*
