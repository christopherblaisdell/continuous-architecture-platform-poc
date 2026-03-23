# Evaluation Framework

## Methodology for AI Toolchain Comparison

This evaluation compares AI toolchains for enterprise solution architecture workflows. The framework is designed to produce defensible, evidence-based recommendations by controlling for model, workspace, and scenario variables.

---

## Controlled Variables

| Variable | Value | Rationale |
|----------|-------|-----------|
| AI Model | Claude Opus 4.6 | Same model eliminates reasoning quality as a variable |
| Workspace | NovaTrek Adventures (synthetic) | 19 microservices, OpenAPI specs, Java source, mock tools |
| Scenarios | 5 identical architecture tasks | Same inputs produce comparable outputs |
| Evaluator | Single human architect | Consistent scoring across all runs |

---

## Evaluation Criteria

| Criterion | Weight | Measurement Method |
|-----------|--------|--------------------|
| Monthly cost per seat | 30% | Actual billing data extrapolated to monthly volume |
| Architecture output quality | 25% | Architect-scored rubric (1-5) per scenario |
| Standards compliance rate | 20% | Pass/fail checklist against arc42, C4, MADR rules |
| Manual corrections required | 15% | Count of edits needed after AI generation |
| Workflow integration friction | 10% | Qualitative assessment of setup, configuration, and daily use |

---

## Scenario Definitions

### SC-01: Ticket Intake and Classification

**What it tests:** AI's ability to parse a JIRA ticket, classify architectural relevance, and scaffold the solution workspace.

**Inputs:** JIRA ticket NTK-10005 (wristband RFID field addition)

**Expected outputs:**

- Ticket report with architectural classification
- Simple explanation for non-technical stakeholders
- Initial folder structure following solution design conventions
- User stories from the user perspective

**Scoring (25 points max):**

- Correct classification of architectural relevance (5)
- Complete ticket report with all fields (5)
- Plain-language explanation without jargon (5)
- User stories written from user perspective (5)
- Folder structure following naming conventions (5)

### SC-02: Solution Design Creation

**What it tests:** AI's ability to produce arc42-compliant solution designs with impact assessments, architecture decisions, and C4 diagrams.

**Inputs:** JIRA ticket NTK-10002 (adventure classification engine)

**Expected outputs:**

- MADR-formatted ADRs with at least 2 genuine options each
- Impact assessments per affected service
- C4 PlantUML diagrams
- Risk register
- Assumptions documentation

**Scoring (35 points max):**

- MADR format compliance (5)
- At least 2 genuine options per ADR (5)
- Impact assessments address WHAT, not HOW (5)
- C4 notation with relationship labels (5)
- Risk identification with mitigations (5)
- Safety fallback correctly identified (Pattern 3 default) (5)
- Prior-art referenced where applicable (5)

### SC-03: Current State Investigation

**What it tests:** AI's ability to analyze Swagger specs, source code, and production logs to identify root causes.

**Inputs:** JIRA ticket NTK-10004 (scheduling orchestrator data overwrite)

**Expected outputs:**

- Investigation report with evidence citations
- Root cause analysis with log evidence
- ADRs for proposed fixes
- Timeline reconstruction from Elastic logs

**Scoring (30 points max):**

- Root cause correctly identified (architectural boundary violation + PUT semantics) (10)
- Elastic log evidence cited with trace IDs (5)
- Concurrent race window identified (5)
- ADRs with genuine options (5)
- Source code analysis with line numbers (5)

### SC-04: Architecture Update (Spec/Diagram Modification)

**What it tests:** AI's ability to modify OpenAPI specs and PlantUML diagrams per an approved solution design.

**Inputs:** JIRA ticket NTK-10001 (elevation fields addition to trail management spec)

**Expected outputs:**

- Updated OpenAPI YAML with new fields
- Version bump following semver
- PlantUML diagram updates if applicable

**Scoring (25 points max):**

- Correct fields added per solution design (10)
- Scope discipline -- only approved changes, no extras (5)
- Proper version bump (5)
- Schema completeness (types, descriptions, nullable) (5)

### SC-05: Publishing Preparation

**What it tests:** AI's ability to validate cross-references, formatting standards compliance, and produce publication-ready documentation.

**Inputs:** Existing solution design artifacts from prior scenarios

**Expected outputs:**

- Validation report identifying issues
- Source code gap analysis
- Component and sequence diagrams
- Formatted ADRs ready for publication

**Scoring (40 points max):**

- Cross-reference validation (5)
- Source code gap identification (5)
- C4 component diagram with proper notation (5)
- Sequence diagram with interaction labels (5)
- ADR formatting compliance (5)
- Impact assessment separation (WHAT vs HOW) (5)
- User story quality (user perspective, acceptance criteria) (5)
- Standards compliance (arc42, C4, MADR) (5)

---

## Cost Measurement Methodology

### The Fundamental Asymmetry

The two primary toolchains use fundamentally different billing architectures, creating an inherent measurement challenge:

| | GitHub Copilot | OpenRouter (Roo Code) |
|---|---|---|
| **Billing unit** | Premium request (per user prompt) | Token (per input/output token) |
| **Visibility** | Daily aggregate only | Exact per-request costs |
| **Session isolation** | Manual differential polling | Generation ID lookup |
| **Cost formula** | `User Prompts x Model Multiplier x $0.04` | `(Input Tokens x Rate) + (Output Tokens x Rate)` |

### Copilot Cost Calculation

GitHub Copilot bills per **user prompt**, not per model invocation. In Agent Mode, the autonomous loop (tool calls, file reads, terminal commands, sub-agents, context summarization) is absorbed by GitHub's infrastructure at no additional charge.

**Formula:** `Session Cost = User Prompts x Model Multiplier x $0.04`

**Model multipliers (March 2026):**

| Model | Multiplier | Cost per User Prompt |
|-------|-----------|----------------------|
| GPT-4.1, GPT-4o | 0x | $0 (included, unlimited) |
| Claude Opus 4.6 | 3x | $0.12 |
| Claude Opus 4.6 fast (preview) | 30x | $1.20 |

**Example:** A 4-prompt Agent Mode session on Claude Opus 4.6 (3x) = 4 x 3 x $0.04 = **$0.48**, regardless of how many autonomous tool calls the agent executes.

See [Copilot Billing Mechanics](research/copilot-billing.md) for the full deep research analysis with 39 cited sources.

### OpenRouter Cost Calculation

OpenRouter provides exact per-generation costs via API. Every token transmitted to and generated by the model incurs a micro-charge.

**Retrieval:** `python3 portal/scripts/utilities/openrouter-cost.py generation <gen-id>`

**Key characteristic:** In agentic workflows, context accumulates with each turn. By turn 40, the model receives the full history of 39 prior turns, making later turns exponentially more expensive than earlier ones.

See [Context Management](research/context-management.md) for analysis of this accumulation pattern.

---

## Data Sources

All evaluation data comes from actual tool executions, not projections:

| Data Point | Source |
|-----------|--------|
| Copilot billing | GitHub Billing dashboard (120 premium requests, March 4, 2026) |
| OpenRouter billing | Auto-top-up transaction records (4 x $25, March 4, 2026) |
| Quality scores | Human architect scoring using rubrics above |
| File counts | `ls` enumeration of run output directories |
| Mock tool usage | Terminal history from each run |
| Copilot billing model | Deep research with 39 cited sources |
| Kong failure modes | Deep research with source code analysis |
