# Phase 1: AI Tool Cost Comparison Plan

## Roo Code plus Kong AI vs GitHub Copilot for Architecture Practice

> This is **Phase 1** of the [Continuous Architecture Platform POC](README.md). It establishes the AI toolchain selection that will power all subsequent phases.

| | |
|-----------|-------|
| **Project** | Continuous Architecture Platform POC |
| **Phase** | Phase 1 - AI Tool Cost Comparison |
| **Author** | Christopher Blaisdell |
| **Date** | 2026-02-28 |
| **Status** | Synthetic workspace complete, ready for execution |
| **Objective** | Determine the monthly cost per architect seat for Roo Code + Kong AI vs GitHub Copilot by reproducing real architecture workflows with synthetic data on a separate computer (ZERO company data) |

---

## 1 Goal

Determine the **monthly cost per architect seat** for two AI-assisted architecture toolchains:

| Option A | Option B |
|----------|----------|
| **Roo Code** (VS Code extension) + **Kong AI** (API gateway to LLMs) | **GitHub Copilot** (Chat, Agent mode, Extensions) |

The key question: **What does it cost per month to give one solution architect AI-assisted tooling under each option?**

GitHub Copilot has a simple per-seat monthly price. Roo Code + Kong AI has a usage-based cost model (per-token LLM charges routed through Kong AI) that depends on actual usage volume. To compare them fairly, we need to measure what a typical architecture month looks like in terms of token consumption, then price that against both models.

The comparison must be performed on a **separate computer** using **entirely synthetic data** so that no the enterprise proprietary information leaves the corporate environment.

---

## 2 Approach Summary

**Phase 1 (This Computer)**: Use real corporate architecture data to create a synthetic dataset that is structurally representative but contains zero company data.

**Phase 2 (Separate Computer)**: Use the synthetic dataset on a clean machine to execute a representative month of architecture work against both toolchains, measuring token usage and quality to calculate monthly cost per seat.

---

## 3 Data Sanitization Principles

These rules apply to ALL synthetic data produced in Phase 1:

| Rule | Description |
|------|-------------|
| **No Real Service Names** | Replace all microservice names (ms-xxx, ms-yyy, etc.) with fictional equivalents |
| **No Real Endpoints** | Replace all API paths, URLs, hostnames with synthetic equivalents |
| **No Real Ticket IDs** | Replace all JIRA ticket IDs (UPT-XXXXXX) with fictional project keys |
| **No Real People** | Replace all team member names, email addresses, Slack handles |
| **No Real Business Logic** | Replace all domain-specific business rules with plausible fictional ones |
| **No Real Infrastructure** | Replace all GitLab URLs, Confluence page IDs, Elastic indices, Kong routes |
| **No Real Data** | Replace all guest data, reservation data, payment data, hotel data |
| **Structural Fidelity** | Preserve the structure, complexity, and relationships between artifacts |
| **Workflow Fidelity** | Preserve the steps, tool usage patterns, and decision-making process |

---

## 4 What Needs to Be Synthesized

The architecture workflow involves the following artifacts and activities. Each must be recreated in synthetic form.

### 4.1 Corporate Service Registry (Synthetic corporate-services Equivalent)

**Source on this machine**: `corporate-services/services/` (120+ OpenAPI/Swagger specs)

**Synthetic equivalent to produce**:
- 15-20 fictional microservice Swagger/OpenAPI YAML specs
- Each spec should be realistic in complexity (endpoints, schemas, error codes)
- Service names from a fictional domain (e.g., a fictional streaming platform, or a fictional logistics company)
- Cross-service references and shared models to preserve integration complexity

**Approach**: Select 15-20 representative real specs, study their structure and complexity, then write new specs in a completely different domain.

### 4.2 Corporate Architecture Diagrams (Synthetic Diagrams Equivalent)

**Source on this machine**: `corporate-services/diagrams/` (PlantUML component, sequence, system diagrams)

**Synthetic equivalent to produce**:
- 8-12 PlantUML component diagrams showing the synthetic microservice ecosystem
- Include standard diagram patterns: include files, macros, component groupings, Kafka topics
- Preserve the architectural style (box groupings, color coding, participant naming)

**Approach**: Study the diagram structure and style, create equivalent diagrams for the synthetic domain.

### 4.3 Ticket Workflow Artifacts

**Source on this machine**: `private-analysis/docs/work-items/tickets/` (9 ticket folders with full analysis)

**Synthetic equivalent to produce**:
- 3-5 synthetic ticket folders, each at different stages of completeness
- Each ticket folder following the standard structure:

```
_SYN-XXXXX-brief-title/
  SYN-XXXXX-solution-design.md
  1.requirements/
    SYN-XXXXX.ticket.report.md
  2.analysis/
    simple.explanation.md
  3.solution/
    a.assumptions/assumptions.md
    b.current.state/investigations.md
    c.decisions/decisions.md
    g.guidance/guidance.md
    i.impacts/
      impacts.md
      impact.1/impact.1.md
      impact.2/impact.2.md
    r.risks/risks.md
    u.user.stories/user-stories.md
```

**Ticket complexity tiers to cover**:

| Tier | Description | Example Synthetic Scenario |
|------|-------------|---------------------------|
| **Simple** | Single service modification, 1-2 endpoints | Add a new field to a GET response |
| **Medium** | 2-3 services impacted, API contract changes | New integration between two services requiring schema changes |
| **Complex** | 5+ services, new Kafka events, vendor integration | New capability requiring orchestration across multiple services and a third-party vendor |

**Synthesis Mapping: Real Tickets to Synthetic Equivalents**

Each synthetic ticket is structurally based on a real internal ticket. The domain, names, services, business rules, and all identifiable content are fully replaced, but the structural complexity, artifact count, comment thread depth, and iterative clarification patterns are preserved.

| Synthetic ID | Tier | Stage | Based On (Real) | What Is Preserved (Structure Only) |
|-------------|------|-------|-----------------|-----------------------------------|
| SYN-10001 | Simple | Complete | REDACTED-001 (single-field change) | Single-service field change, simple impact, 1 decision, minimal stakeholder discussion |
| SYN-10002 | Medium | Complete | **REDACTED-002 (classification with conditional logic)** | Classification table with conditional logic, 3 behavioral patterns, booking source overrides mapped to a synthetic domain equivalent, 18-comment stakeholder thread with iterative clarification, multiple PlantUML activity/sequence diagrams, v1.0 to v1.6 solution evolution |
| SYN-10003 | Complex | Complete | REDACTED-003 (unregistered guest check-in) | New end-to-end feature across 4+ services, orchestrator pattern with fallback, security review gate, UI wireframes, developer-verified current-state diagrams, 10+ PlantUML files, corporate Swagger MR |
| SYN-10004 | Medium | Investigation | REDACTED-004 (data overwrite bug) | Data ownership conflict investigation, field-level merge vs full-replacement analysis, race condition discovery, Elasticsearch validation queries, partial assumptions |
| SYN-10005 | Simple | Intake | REDACTED-005 (schema field addition) | Schema change request, just classified and workspace created, ticket report only |

### 4.4 Architecture Standards Framework (Public, Pre-existing)

**Instead of** sanitizing our internal standards, we will adopt an existing public architecture standards framework. This eliminates IP risk entirely and adds credibility (the AI tools must work with real, industry-recognized standards, not something we invented for the test).

**Primary framework: arc42** (https://arc42.org)

arc42 is an open-source, Creative Commons licensed architecture documentation template used industry-wide. It provides:

| arc42 Section | Maps to Internal Equivalent | Standards Complexity |
|--------------|----------------------|---------------------|
| 1. Introduction and Goals | Ticket requirements, quality goals | Stakeholder tables, quality scenarios |
| 2. Constraints | Business/technical constraints | Constraint classification |
| 3. Context and Scope | Current state discovery | System context diagrams, external interfaces |
| 4. Solution Strategy | Solution design overview | Top-level decomposition, tech decisions |
| 5. Building Block View | Component architecture | Hierarchical white-box/black-box decomposition |
| 6. Runtime View | Sequence diagrams, runtime scenarios | Important use cases, interaction patterns |
| 7. Deployment View | Infrastructure/deployment docs | Hardware, environments, topology mapping |
| 8. Crosscutting Concepts | Guidance documents | Domain models, patterns, implementation rules |
| 9. Architectural Decisions | Decision documents (ADRs) | Decision rationale, options analysis |
| 10. Quality Requirements | NFRs, quality attributes | Quality tree, quality scenarios |
| 11. Risks and Technical Debt | Risk documents | Known problems, risk assessment |
| 12. Glossary | Domain terminology | Ubiquitous language |

**Download format**: GitHub Markdown Multi-Page (with help text) from `arc42-template-EN-withhelp-gitHubMarkdownMP.zip`

**Supplementary frameworks to layer on top**:

| Framework | Source | What It Adds |
|-----------|--------|-------------|
| **MADR** (Markdown Any Decision Records) | https://adr.github.io/madr/ | Prescriptive ADR templates with options, pros/cons format |
| **C4 Model** diagramming standards | https://c4model.com/ | Strict rules for context, container, component, code diagrams |
| **ADR templates** (Joel Parker Henderson collection) | https://github.com/joelparkerhenderson/architecture-decision-record | 10+ ADR templates, examples, and governance rules |
| **arc42 Quality Model** | https://quality.arc42.org/ | Detailed quality properties/attributes (ISO 25010 aligned) |

**What to download and include in the synthetic workspace**:
1. arc42 template (GitHub Markdown MP with help) - 12 section files with detailed guidance
2. arc42 documentation site content (144 tips, 35 examples) - scraped or referenced
3. MADR template and examples from GitHub
4. ADR templates collection (Nygard, Tyree-Akerman, business case, Alexandrian)
5. C4 model diagramming rules and notation standards
6. arc42 Quality Model properties list

**Then create a `.ai-instructions/` directory that**:
- Tells the AI agent to follow arc42 structure for all documentation
- Specifies which ADR template to use for decisions
- Mandates C4 model compliance for all diagrams
- Defines the ticket-to-arc42 mapping (how a JIRA ticket becomes arc42 artifacts)
- Includes formatting rules, header conventions, and cross-referencing standards
- This instruction file IS synthetic but is small, contains no company data, and simply wires the public frameworks together

**Why this is better than sanitizing our standards**:
- ZERO risk of company data leakage (all public domain / Creative Commons)
- More rigorous test (real industry standards are more comprehensive than custom ones)
- More convincing comparison (stakeholders can verify the standards independently)
- Saves significant effort (no need to rewrite 40+ customization documents)

### 4.5 Source Code References (Synthetic Microservice Code)

**Source on this machine**: `source-code/microservices/` (10 reference microservices)

**Synthetic equivalent to produce**:
- 5-8 synthetic microservice skeletons (Java/Spring Boot or similar)
- Each with representative structure: controllers, services, repositories, DTOs, configs
- Enough code to simulate "read source code for investigation" workflow steps
- Not full implementations, just enough structure and placeholder logic

### 4.6 Tool Scripts (Synthetic Tooling)

**Source on this machine**: `private-analysis/scripts/` (JIRA client, GitLab client, Elastic searcher)

**Synthetic equivalent to produce**:
- Synthetic JIRA ticket extraction script (outputs synthetic ticket JSON)
- Synthetic merge request analysis script (outputs synthetic MR details)
- Synthetic Elastic query script (outputs synthetic log search results)
- These scripts should produce canned/mock outputs rather than calling real APIs

### 4.7 Workspace Configuration

**Source on this machine**: `.code-workspace`, `.vscode/`, `.github/copilot-instructions.md`

**Synthetic equivalent to produce**:
- A synthetic `.code-workspace` file with the correct multi-root structure
- Synthetic VS Code settings
- Synthetic Roo Code configuration (`.roo/` equivalent)
- Synthetic GitHub Copilot workspace instructions

---

## 5 Workflow Scenarios to Reproduce

These are the specific architecture tasks to execute on both toolchains for cost comparison. Each scenario should be documented as a "script" that can be followed identically on both tools.

### Scenario 1: New Ticket Intake and Classification

**Steps**:
1. Query synthetic JIRA for open tickets
2. Select a ticket and extract details
3. Classify the ticket (architecture-relevant vs code bug)
4. Create the ticket workspace folder structure
5. Generate the simple explanation document

**Measures**: Input tokens, output tokens, API calls, wall clock time, output quality

### Scenario 2: Current State Investigation

**Steps**:
1. Read the synthetic JIRA ticket report
2. Identify affected microservices from the ticket description
3. Analyze relevant Swagger/OpenAPI specs
4. Review relevant source code
5. Query synthetic Elastic logs for error patterns
6. Produce current state investigation documents

**Measures**: Input tokens, output tokens, API calls, wall clock time, output quality

### Scenario 3: Solution Design Creation

**Steps**:
1. Using the investigation from Scenario 2, create a solution design
2. Identify impacted components
3. Create impact documents for each component
4. Create PlantUML sequence diagrams (target state)
5. Create assumptions, decisions, and risks documents
6. Generate user stories with acceptance criteria

**Measures**: Input tokens, output tokens, API calls, wall clock time, output quality

### Scenario 4: Merge Request Review

**Steps**:
1. Analyze a synthetic merge request (Swagger spec changes, PlantUML changes)
2. Validate changes against the solution design
3. Produce a peer review document with findings

**Measures**: Input tokens, output tokens, API calls, wall clock time, output quality

### Scenario 5: Confluence Publishing Preparation

**Steps**:
1. Review all documents with `CONFLUENCE-PUBLISH` markers
2. Validate document formatting and structure against standards
3. Verify cross-references and links between documents
4. Produce a publishing readiness checklist

**Measures**: Input tokens, output tokens, API calls, wall clock time, output quality

### Monthly Volume Estimation

To convert scenario-level measurements into a monthly per-seat cost, we need to estimate how many of each scenario a single architect performs per month:

| Scenario | Estimated Frequency per Architect per Month | Rationale |
|----------|---------------------------------------------|----------|
| Ticket Intake | 8-12 tickets | Based on typical sprint cadence and ticket volume |
| Current State Investigation | 6-8 investigations | Not every ticket requires deep investigation |
| Solution Design Creation | 4-6 designs | Major deliverable, roughly weekly |
| Merge Request Review | 6-10 reviews | Peer reviews of Swagger/PlantUML MRs |
| Confluence Publishing | 4-6 publishing cycles | Aligned with solution design completion |

These frequencies will be validated during Phase 1 by examining actual ticket history patterns (using only counts and frequencies, not content).

---

## 6 Monthly Cost Per Seat Calculation

### Per-Scenario Metrics to Capture

| Metric | Description |
|--------|-------------|
| **Input Tokens** | Total tokens sent to the LLM per scenario execution |
| **Output Tokens** | Total tokens received from the LLM per scenario execution |
| **API Calls** | Number of distinct LLM API calls per scenario execution |
| **Wall Clock Time** | End-to-end architect time per scenario execution |
| **Quality Score** | Subjective 1-5 rating of output quality |
| **Standards Compliance** | Does the output follow the defined standards (pass/fail) |
| **Manual Corrections** | Number of manual edits needed after AI generation |

### Monthly Cost Formula

**Option A: Roo Code + Kong AI** (usage-based)

```
Monthly Cost Per Seat =
  (Total Monthly Input Tokens x Input Token Price)
  + (Total Monthly Output Tokens x Output Token Price)
  + Kong AI Gateway Monthly Fee (if any per-seat component)
  + Roo Code License (if any)
```

Where:
- Total Monthly Input Tokens = SUM(scenario input tokens x monthly frequency) across all scenarios
- Total Monthly Output Tokens = SUM(scenario output tokens x monthly frequency) across all scenarios
- Token prices come from AWS Bedrock pricing for the Claude model used via Kong AI

**Option B: GitHub Copilot** (seat-based)

```
Monthly Cost Per Seat =
  Copilot Business/Enterprise subscription per seat
  + Premium model request overage (if applicable)
```

GitHub Copilot Business is currently $19/seat/month. Copilot Enterprise is $39/seat/month. Premium requests for models like Claude Sonnet or GPT-4o may have usage limits with overage charges.

### Pricing Inputs to Research (Phase 2)

| Cost Component | Source | Notes |
|---------------|--------|-------|
| AWS Bedrock Claude input token price | AWS pricing page | Per 1K/1M tokens, varies by model |
| AWS Bedrock Claude output token price | AWS pricing page | Per 1K/1M tokens, varies by model |
| Kong AI gateway fee | Internal Kong AI team | May be flat rate or per-request |
| Roo Code license | Roo Code pricing page | Open source (free) vs Pro tier |
| GitHub Copilot Business seat price | GitHub pricing page | Currently $19/seat/month |
| GitHub Copilot Enterprise seat price | GitHub pricing page | Currently $39/seat/month |
| Copilot premium model overage | GitHub docs | Limits and overage rates for Claude/GPT-4o in Copilot |

### Comparison Output

The final deliverable will be a table like:

| | Roo Code + Kong AI | GitHub Copilot Business | GitHub Copilot Enterprise |
|---|---|---|---|
| Monthly input tokens per architect | X | (included in seat) | (included in seat) |
| Monthly output tokens per architect | Y | (included in seat) | (included in seat) |
| Token cost | $A | $0 (flat rate) | $0 (flat rate) |
| Gateway/platform cost | $B | $19/seat | $39/seat |
| Tool license cost | $C | (included) | (included) |
| **Total monthly per seat** | **$A+B+C** | **$19** | **$39** |
| Quality score (avg across scenarios) | Q1 | Q2 | Q2 |
| Standards compliance rate | S1% | S2% | S2% |

---

## 7 Execution Plan

### Phase 1: Synthetic Data Generation (This Computer)

| Step | Task | Estimated Effort | Dependencies |
|------|------|-----------------|--------------|
| 1.1 | Choose a fictional domain for the synthetic company | 1 hour | None |
| 1.2 | Create synthetic microservice Swagger specs (15-20) | 4-6 hours | Step 1.1 |
| 1.3 | Create synthetic PlantUML diagrams (8-12) | 3-4 hours | Step 1.2 |
| 1.4 | Create synthetic ticket folders with full artifacts (3-5) | 6-8 hours | Steps 1.2, 1.3 |
| 1.5 | Download and integrate public architecture standards (arc42, MADR, C4, ADR templates) | 2-3 hours | Step 1.1 |
| 1.6 | Create synthetic microservice code skeletons | 3-4 hours | Step 1.2 |
| 1.7 | Create synthetic tool scripts with mock outputs | 2-3 hours | Step 1.4 |
| 1.8 | Create synthetic workspace configuration | 1-2 hours | All above |
| 1.9 | Final sanitization audit: grep for ANY real company data | 2 hours | All above |
| 1.10 | Package synthetic workspace as a portable archive | 1 hour | Step 1.9 |

**Total Phase 1 estimate**: 24-34 hours

### Phase 2: Cost Comparison Execution (Separate Computer)

| Step | Task | Estimated Effort | Dependencies |
|------|------|-----------------|--------------|
| 2.1 | Set up separate computer with both toolchains | 2-4 hours | Phase 1 complete |
| 2.2 | Import synthetic workspace | 1 hour | Step 2.1 |
| 2.3 | Execute Scenario 1 on Roo Code + Kong AI | 1-2 hours | Step 2.2 |
| 2.4 | Execute Scenario 1 on GitHub Copilot | 1-2 hours | Step 2.2 |
| 2.5 | Execute Scenario 2 on both tools | 2-4 hours | Steps 2.3, 2.4 |
| 2.6 | Execute Scenario 3 on both tools | 3-5 hours | Step 2.5 |
| 2.7 | Execute Scenario 4 on both tools | 1-2 hours | Step 2.6 |
| 2.8 | Execute Scenario 5 on both tools | 1-2 hours | Step 2.7 |
| 2.9 | Compile metrics and produce comparison report | 3-4 hours | All above |

**Total Phase 2 estimate**: 14-24 hours

---

## 8 Sanitization Audit Checklist

Before transferring the synthetic workspace to the separate computer, run these checks:

```bash
# Search for any real microservice names
grep -ri "REAL-SVC-1\|REAL-SVC-2\|REAL-SVC-3" .  # Replace with actual internal service name patterns

# Search for any real ticket IDs
grep -ri "UPT-\|ARCH-\|UDX-" .

# Search for any real URLs
grep -ri "nbcu-ot\|atlassian\|gitlab\.use\|ucdp\.net\|kong\." .

# Search for any real people names (add known names)
grep -ri "blaisdell\|christopher\|specific-team-member-names" .

# Search for any real infrastructure references
grep -ri "bedrock\|elastic\|kibana\|confluence\|silverpop" .

# Search for "Universal" or company references
grep -ri "universal\|nbcuniversal\|comcast\|UPR\|UDX\|theme park\|resort" .
```

---

## 9 Deliverables

Everything below is what gets packaged and transferred to the other PC. The deliverable is a single portable directory that can be opened as a VS Code workspace immediately.

### 9.1 Portable Workspace Root Structure

```
ai-tool-cost-comparison-workspace/
  ai-tool-cost-comparison.code-workspace          # VS Code multi-root workspace file
  .github/
    copilot-instructions.md                        # GitHub Copilot workspace-level instructions
  .roo/                                            # Roo Code configuration equivalent
    rules/
  .vscode/
    settings.json                                  # VS Code workspace settings
  .ai-instructions/                                # AI agent instructions (wires public frameworks together)
    main-instructions.md                           # Primary AI agent instructions
    standards/                                     # Pointers and rules referencing arc42, C4, MADR
    templates/                                     # Solution design, impact, ADR templates
  architecture-standards/                          # PUBLIC FRAMEWORKS (downloaded, not synthesized)
    arc42/                                         # arc42 template (GitHub Markdown MP with help)
    adr-templates/                                 # ADR template collection (Nygard, Tyree-Akerman, etc.)
    madr/                                          # MADR template and examples
    c4-model/                                      # C4 model diagramming rules and notation
    quality-model/                                 # arc42 Quality Model properties
  corporate-services/                              # Synthetic service registry (equivalent of corporate-services)
    services/                                      # 15-20 synthetic OpenAPI/Swagger YAML specs
    diagrams/                                      # 8-12 synthetic PlantUML diagrams
      Components/
      Sequence/
      System/
      include.puml
      templates.puml
  source-code/                                     # Synthetic microservice code skeletons
    microservices/
      svc-one/                                     # 5-8 synthetic Java/Spring Boot skeletons
      svc-two/
      ...
  work-items/                                      # Synthetic ticket workspace (analysis docs)
    tickets/
      _SYN-10001-brief-title/                      # Simple tier ticket (complete)
      _SYN-10002-brief-title/                      # Medium tier ticket (complete)
      _SYN-10003-brief-title/                      # Complex tier ticket (complete)
      _SYN-10004-brief-title/                      # Ticket at investigation stage (partial)
      _SYN-10005-brief-title/                      # Ticket at intake stage (minimal)
  scripts/                                         # Synthetic tooling with mock outputs
    mock-jira-client.py
    mock-gitlab-client.py
    mock-elastic-searcher.py
    mock-data/                                     # Canned JSON responses for each script
  scenario-playbooks/                              # Step-by-step execution scripts
    scenario-1-ticket-intake.md
    scenario-2-current-state-investigation.md
    scenario-3-solution-design-creation.md
    scenario-4-merge-request-review.md
    scenario-5-publishing-preparation.md
    measurement-protocol.md                        # How to capture tokens, time, quality
  audit/                                           # Sanitization evidence
    sanitization-audit-log.md
    grep-results.txt
```

### 9.2 Deliverable Details

#### D1 Corporate Services (Synthetic)

| Item | Count | Format | Description |
|------|-------|--------|-------------|
| OpenAPI/Swagger specs | 15-20 | YAML | Realistic specs with endpoints, schemas, error codes, cross-service refs |
| PlantUML component diagrams | 4-6 | `.puml` + `.svg` | System-level and component-level diagrams |
| PlantUML sequence diagrams | 4-6 | `.puml` + `.svg` | Runtime interaction scenarios |
| PlantUML include/macro files | 2-3 | `.puml` | Shared styles, colors, participant definitions |

#### D2 Architecture Standards (Public Frameworks)

| Item | Source | License | Format |
|------|--------|---------|--------|
| arc42 template (12 sections with help) | github.com/arc42/arc42-template | Creative Commons | Markdown (multi-page) |
| arc42 Quality Model | quality.arc42.org | Creative Commons | Markdown |
| MADR template + examples | adr.github.io/madr | CC0/MIT | Markdown |
| ADR templates collection (6+ templates) | github.com/joelparkerhenderson/architecture-decision-record | CC | Markdown |
| C4 model notation rules | c4model.com | CC BY 4.0 | Markdown summary |

#### D3 Ticket Workflow Artifacts (Synthetic)

| Ticket | Tier | Stage | Based On | Artifacts Included |
|--------|------|-------|----------|---------------------|
| SYN-10001 | Simple | Complete | REDACTED-001 pattern | Solution design, ticket report, simple explanation, 1 impact, assumptions, 1 decision, user stories |
| SYN-10002 | Medium | Complete | **REDACTED-002 pattern** | Solution design (v1.6 equivalent), ticket report with 18-comment thread, simple explanation, 2 impacts with PlantUML activity/sequence diagrams, classification table with conditional patterns, assumptions, 2 decisions, guidance, user stories, risks |
| SYN-10003 | Complex | Complete | REDACTED-003 pattern | Solution design (v1.11 equivalent), ticket report, simple explanation, 4+ impacts with diagrams, assumptions, 3+ decisions, guidance, history, user stories, risks, functional requirements, security review request, UI wireframes |
| SYN-10004 | Medium | Investigation | REDACTED-004 pattern | Ticket report, simple explanation, current state investigations (2-3), data ownership analysis, race condition analysis, Elasticsearch validation queries, partial assumptions |
| SYN-10005 | Simple | Intake | REDACTED-005 pattern | Ticket report only (just classified, workspace created) |

Each complete ticket follows this structure:
```
_SYN-XXXXX-brief-title/
  SYN-XXXXX-solution-design.md
  1.requirements/
    SYN-XXXXX.ticket.report.md
  2.analysis/
    simple.explanation.md
  3.solution/
    a.assumptions/assumptions.md
    c.current.state/investigations.md
    d.decisions/decisions.md
    g.guidance/guidance.md
    i.impacts/
      impacts.md
      impact.1/impact.1.md    (+ .puml + .svg diagrams)
      impact.N/impact.N.md
    r.risks/risks.md
    u.user.stories/user-stories.md
```

#### D4 Source Code Skeletons (Synthetic)

| Item | Count | Language/Framework | Description |
|------|-------|--------------------|-------------|
| Microservice skeletons | 5-8 | Java / Spring Boot | Controllers, services, repositories, DTOs, configs |
| Lines of code per service | ~200-500 | Java | Enough structure for AI to investigate, not full implementations |
| Build files | 5-8 | Gradle or Maven | `build.gradle` or `pom.xml` per service |
| Application configs | 5-8 | YAML | `application.yml` with synthetic DB/queue/API references |

#### D5 Tool Scripts (Synthetic with Mock Data)

| Script | Equivalent Of | Output |
|--------|--------------|--------|
| `mock-jira-client.py` | `working_jira_client.py` | Returns synthetic ticket list and individual ticket details from `mock-data/` |
| `mock-gitlab-client.py` | `gitlab_api_client.py` | Returns synthetic MR details, diffs, and pipeline status from `mock-data/` |
| `mock-elastic-searcher.py` | `production_elastic_searcher.py` | Returns synthetic log search results from `mock-data/` |

Mock data files (JSON):
- `mock-data/jira-tickets.json` - 8-12 synthetic tickets at various statuses
- `mock-data/jira-ticket-SYN-10001.json` through `SYN-10005.json` - Individual ticket details
- `mock-data/gitlab-mr-101.json` through `mr-103.json` - 3 synthetic merge requests
- `mock-data/elastic-error-logs.json` - Synthetic error log search results
- `mock-data/elastic-api-traffic.json` - Synthetic API traffic patterns

#### D6 AI Agent Instructions (Synthetic, Minimal)

| File | Purpose |
|------|---------|
| `.ai-instructions/main-instructions.md` | Defines the architect role, workflow steps, tool usage, and maps tickets to arc42 artifacts |
| `.ai-instructions/standards/formatting-rules.md` | Header conventions, cross-referencing, markdown standards |
| `.ai-instructions/standards/diagram-standards.md` | C4 model compliance rules, PlantUML conventions |
| `.ai-instructions/standards/adr-standards.md` | Which ADR template to use, decision lifecycle rules |
| `.ai-instructions/templates/solution-design-template.md` | arc42-based solution design template |
| `.ai-instructions/templates/impact-template.md` | Component impact document template |
| `.ai-instructions/templates/ticket-report-template.md` | JIRA ticket extraction output format |
| `.github/copilot-instructions.md` | GitHub Copilot workspace instructions (references arc42 standards) |
| `.roo/rules/` | Roo Code mode-specific instruction files |

#### D7 Scenario Playbooks

| Playbook | Content |
|----------|---------|
| `scenario-1-ticket-intake.md` | Exact prompts, expected file operations, success criteria |
| `scenario-2-current-state-investigation.md` | Exact prompts, which specs/code to analyze, expected outputs |
| `scenario-3-solution-design-creation.md` | Exact prompts, expected arc42 artifacts, diagram requirements |
| `scenario-4-merge-request-review.md` | Exact prompts, which MR to review, expected review document |
| `scenario-5-publishing-preparation.md` | Exact prompts, validation checks, expected checklist output |
| `measurement-protocol.md` | How to capture input/output tokens, API call counts, wall clock time, and quality scoring rubric |

Each playbook includes:
- **Pre-conditions**: What must exist before starting
- **Exact prompts**: The literal text to send to each AI tool (identical wording for both)
- **Expected outputs**: What files/artifacts should be created
- **Measurement checkpoints**: When to record token counts and timing
- **Quality rubric**: How to score output on a 1-5 scale per criterion
- **Standards compliance checklist**: Specific arc42/C4/MADR rules to verify

#### D8 Sanitization Audit Log

| File | Content |
|------|---------|
| `audit/sanitization-audit-log.md` | Date, auditor, grep commands run, results, pass/fail per check |
| `audit/grep-results.txt` | Raw output of all sanitization grep commands (should all be empty) |

### 9.3 Transfer Method

The entire `ai-tool-cost-comparison-workspace/` directory will be:
1. Compressed into a single `.zip` or `.tar.gz` archive
2. Verified against the sanitization audit checklist one final time
3. Transferred to the separate computer via USB drive or secure file transfer
4. Extracted and opened as a VS Code workspace on the target machine

---

## 10 Fictional Domain Suggestions

The synthetic data needs a plausible domain that is complex enough to mimic theme park hospitality architecture. Suggestions:

| Domain | Rationale |
|--------|-----------|
| **GalaxyStream** - Fictional streaming platform | Content delivery, user profiles, subscriptions, recommendations, payments. Complex microservice ecosystem. |
| **NovaTrek Adventures** - Fictional outdoor recreation company | Reservations, gear inventory, trail management, weather integration, guide scheduling. Similar to hospitality. |
| **AquaVista Resorts** - Fictional resort chain (NOT theme parks) | Hotel stays, dining, activities, spa, loyalty program. Closest structural match but must avoid theme park overlap. |
| **MetroFleet Logistics** - Fictional delivery/logistics company | Route optimization, fleet management, warehouse operations, customer tracking, carrier integration. Different enough domain. |

**Recommendation**: **NovaTrek Adventures** or **MetroFleet Logistics** - different enough from the original domain to avoid any accidental overlap, but complex enough to exercise all the architecture patterns.

---

## 11 Next Steps

1. **Choose the fictional domain** for synthetic data
2. **Begin Phase 1 execution**, starting with Step 1.1
3. **Track progress** in this document by updating the execution plan table
4. **Review each synthetic artifact** against the sanitization checklist before moving on
