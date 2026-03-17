# Incorporating Everything Claude Code (ECC) into the NovaTrek Continuous Architecture Platform

**Date**: 2026-03-17
**Status**: Proposed
**Author**: Solution Architecture Team

---

## Executive Summary

This plan describes how to incorporate the [Everything Claude Code](https://github.com/affaan-m/everything-claude-code) (ECC) repository — a mature, community-driven AI agent harness performance system — into the NovaTrek Continuous Architecture Platform's GitHub Copilot AI workflow. ECC provides 108 skills, 25 specialized agents, 57 commands, automated hooks, MCP configurations, and language-specific rules that can significantly enhance the quality, consistency, and capability of AI-assisted architecture work.

The integration targets **GitHub Copilot Agent Mode** running in VS Code, adapting ECC's Claude Code-oriented patterns to the Copilot instruction and skill system (`.github/copilot-instructions.md`, `.instructions.md`, `.prompt.md` files).

---

## Table of Contents

1. [Current State Assessment](#1-current-state-assessment)
2. [ECC Asset Inventory — Relevant to NovaTrek](#2-ecc-asset-inventory--relevant-to-novatrek)
3. [Integration Strategy](#3-integration-strategy)
4. [Phase 1 — Foundation (Immediate)](#4-phase-1--foundation-immediate)
5. [Phase 2 — Architecture Skills (Short-Term)](#5-phase-2--architecture-skills-short-term)
6. [Phase 3 — Advanced Workflows (Medium-Term)](#6-phase-3--advanced-workflows-medium-term)
7. [Phase 4 — Continuous Learning (Longer-Term)](#7-phase-4--continuous-learning-longer-term)
8. [Skill Translation Guide — Claude Code to Copilot](#8-skill-translation-guide--claude-code-to-copilot)
9. [Demonstration Plan](#9-demonstration-plan)
10. [Risk Assessment](#10-risk-assessment)
11. [File Manifest — What Gets Created or Modified](#11-file-manifest--what-gets-created-or-modified)

---

## 1. Current State Assessment

### What We Have Today

| Asset | Location | Description |
|-------|----------|-------------|
| Copilot Instructions | `.github/copilot-instructions.md` | 700+ line comprehensive architecture instruction set for NovaTrek domain |
| Claude Skills (Jeffallan) | `claude-skills/skills/` | 66 skills from the Jeffallan claude-skills repository (language specialists, framework experts, architecture, security) |
| NovaTrek Domain Model | `architecture/metadata/` | YAML-based capabilities, tickets, services, events — the synthetic workspace |
| Solution Design Workflow | `architecture/solutions/` | Structured template for architecture solution design with prior-art discovery |
| Architecture Standards | `architecture-standards/` | MADR, C4, arc42, ISO 25010 templates |
| Mock Tools | `scripts/` | Local JIRA, Elastic, GitLab mock clients for realistic AI agent evaluation |

### What ECC Adds

| Capability | ECC Source | Gap It Fills |
|------------|-----------|--------------|
| Structured agent delegation | `agents/architect.md`, `agents/planner.md` | No formal agent routing in current Copilot setup |
| API design patterns | `skills/api-design/` | Current specs exist but no active design guidance for the AI |
| Security review workflow | `skills/security-review/`, `skills/security-scan/` | Security review is implicit in copilot-instructions but not structured |
| Deep research methodology | `skills/deep-research/` | We do deep research but without a codified methodology |
| TDD and verification loops | `skills/tdd-workflow/`, `skills/verification-loop/` | No test-driven workflow in current architecture process |
| Continuous learning | `skills/continuous-learning/`, `skills/continuous-learning-v2/` | Session insights are lost between conversations |
| Coding standards (Java) | `skills/java-coding-standards/`, `rules/java/` | We analyze Java source code but lack AI-enforced standards |
| Spring Boot patterns | `skills/springboot-patterns/`, `skills/springboot-security/` | NovaTrek services are Spring Boot; no Spring-specific AI guidance |
| Database migration patterns | `skills/database-migrations/` | Relevant to our database index change workflow |
| Docker patterns | `skills/docker-patterns/` | Relevant to our `docker-compose.yml` and local dev |
| MCP server patterns | `skills/mcp-server-patterns/` | Relevant to our mock tool architecture |
| Context management | `skills/strategic-compact/` | Long architecture sessions exhaust context windows |
| Research-first workflow | `skills/search-first/` | Aligns with our prior-art discovery requirement |

---

## 2. ECC Asset Inventory — Relevant to NovaTrek

### Tier 1 — Directly Applicable (Incorporate Now)

These skills map directly to activities our Solution Architect AI performs daily.

| ECC Asset | NovaTrek Use Case | Priority |
|-----------|------------------|----------|
| `skills/api-design/` | Designing and reviewing OpenAPI specs for 19 microservices | CRITICAL |
| `skills/deep-research/` | Multi-source investigation for architecture tickets | CRITICAL |
| `skills/search-first/` | Prior-art discovery before new solution designs | CRITICAL |
| `agents/architect.md` | System design delegation pattern | HIGH |
| `agents/planner.md` | Breaking down complex solution designs | HIGH |
| `skills/security-review/` | Security assessment for PII flows, auth, waivers | HIGH |
| `skills/java-coding-standards/` | Analyzing NovaTrek Java source code | HIGH |
| `skills/springboot-patterns/` | Spring Boot service analysis (17 of 19 services) | HIGH |
| `skills/database-migrations/` | Schema migration guidance for solution impacts | HIGH |
| `rules/common/security.md` | Security checklist for all reviews | HIGH |
| `contexts/research.md` | Research mode for investigation scenarios | HIGH |

### Tier 2 — Valuable Enhancements (Short-Term)

| ECC Asset | NovaTrek Use Case | Priority |
|-----------|------------------|----------|
| `skills/docker-patterns/` | Local development environment guidance | MEDIUM |
| `skills/postgres-patterns/` | Database design for NovaTrek data stores | MEDIUM |
| `skills/springboot-security/` | Security patterns for Spring Boot services | MEDIUM |
| `skills/jpa-patterns/` | JPA/Hibernate patterns for entity analysis | MEDIUM |
| `agents/security-reviewer.md` | Delegated security review agent | MEDIUM |
| `agents/database-reviewer.md` | Database design review delegation | MEDIUM |
| `skills/verification-loop/` | Pre-commit verification for solution designs | MEDIUM |
| `skills/continuous-learning/` | Auto-extract patterns from architecture sessions | MEDIUM |
| `skills/mcp-server-patterns/` | Improving mock tool architecture | MEDIUM |

### Tier 3 — Future Value (Medium-Term)

| ECC Asset | NovaTrek Use Case | Priority |
|-----------|------------------|----------|
| `skills/tdd-workflow/` | Test-driven approach to architecture validation | LOW |
| `skills/deployment-patterns/` | CI/CD patterns for portal deployment | LOW |
| `skills/enterprise-agent-ops/` | Long-lived agent session management | LOW |
| `skills/autonomous-loops/` | Autonomous architecture analysis workflows | LOW |
| `skills/agentic-engineering/` | Advanced AI agent workflow patterns | LOW |
| `skills/eval-harness/` | Evaluating AI output quality for architecture tasks | LOW |
| `skills/strategic-compact/` | Context management for long sessions | LOW |

---

## 3. Integration Strategy

### Approach: Adaptation, Not Direct Copy

ECC skills are designed for Claude Code's agent harness (subagent delegation, hooks, slash commands). GitHub Copilot uses a different mechanism:

| Claude Code Concept | Copilot Equivalent | Translation Method |
|--------------------|--------------------|--------------------|
| `CLAUDE.md` (project guidance) | `.github/copilot-instructions.md` | Already exists; augment with ECC patterns |
| `skills/X/SKILL.md` | `.instructions.md` files (folder-scoped) or Copilot custom skills | Create `.instructions.md` files with adapted content |
| `agents/X.md` (subagent delegation) | Copilot subagents (via `runSubagent`) | Reference agent patterns in instruction files |
| `rules/common/*.md` | `.github/copilot-instructions.md` sections | Merge relevant rules into existing instructions |
| `commands/X.md` (slash commands) | `.prompt.md` files (reusable prompts) | Create `.prompt.md` files for key workflows |
| `hooks/hooks.json` (triggers) | No direct equivalent | Document as manual workflow checkpoints |
| `contexts/X.md` (mode switching) | `.prompt.md` files for mode activation | Create mode-switching prompts |
| `mcp-configs/` | VS Code MCP configuration | Adapt relevant MCP configs |

### Key Principles

1. **Preserve NovaTrek domain specificity** — ECC's generic patterns are adapted to our adventure tourism microservices domain, not used as-is
2. **Augment, do not replace** — Our existing `copilot-instructions.md` is comprehensive and domain-specific; ECC adds workflow patterns and quality gates, not domain knowledge
3. **Gradual rollout** — Incorporate Tier 1 first, validate in real scenarios, then expand
4. **Source attribution** — All adapted content references the ECC origin for license compliance (MIT)

---

## 4. Phase 1 — Foundation (Immediate)

### 4.1 Create Architecture Skill Instructions

Create folder-scoped `.instructions.md` files that Copilot loads automatically when working in specific directories.

#### 4.1.1 Solution Design Instructions

**File**: `architecture/solutions/.instructions.md`

Adapts from: `agents/architect.md`, `agents/planner.md`, `skills/search-first/`

Content:
- Architecture review process (current state analysis, requirements gathering, design proposal, trade-off analysis)
- Prior-art discovery workflow (search-first pattern from ECC)
- MADR decision-making framework (already in copilot-instructions, reinforced here)
- Solution decomposition (from planner agent)

#### 4.1.2 API Spec Design Instructions

**File**: `architecture/specs/.instructions.md`

Adapts from: `skills/api-design/`

Content:
- REST API design patterns (resource naming, status codes, pagination, filtering)
- OpenAPI spec quality checklist (schema completeness, nullable annotations, enum validation)
- Backward compatibility rules for API changes
- Error response standardization

#### 4.1.3 Security Review Instructions

**File**: `architecture/.instructions.md`

Adapts from: `skills/security-review/`, `rules/common/security.md`

Content:
- OWASP Top 10 checklist adapted for NovaTrek services
- PII handling rules for guest profiles and waivers
- Authentication and authorization patterns (svc-guest-profiles as identity source)
- Input validation at service boundaries

### 4.2 Create Reusable Prompt Files

#### 4.2.1 Deep Research Prompt

**File**: `.github/prompts/deep-research.prompt.md`

Adapts from: `skills/deep-research/`

Content:
- Multi-source research methodology
- Source attribution requirements
- Evidence-based findings with workspace file references
- Synthesis and structured output format

#### 4.2.2 Architecture Review Prompt

**File**: `.github/prompts/architecture-review.prompt.md`

Adapts from: `agents/architect.md`, `skills/security-review/`

Content:
- Current state analysis checklist
- Trade-off documentation template
- ISO 25010 quality attribute assessment
- Anti-pattern detection (from copilot-instructions, enhanced with ECC patterns)

#### 4.2.3 Investigation Prompt

**File**: `.github/prompts/investigation.prompt.md`

Adapts from: `contexts/research.md`, `skills/search-first/`

Content:
- Research mode activation (understand before acting)
- Mock tool usage sequence (JIRA first, Elastic before GitLab)
- Evidence gathering and citation methodology
- Hypothesis formation and verification

### 4.3 Augment Copilot Instructions

Add an "AI Workflow Patterns" section to `.github/copilot-instructions.md` that incorporates:

- **Search-first principle** (from `skills/search-first/`): Always search for existing solutions before writing new code or creating new designs
- **Research mode** (from `contexts/research.md`): When investigating tickets, switch to exploration mode — read widely, form hypotheses, verify with evidence
- **Security-first** (from `rules/common/security.md`): Check for security implications in every solution design touching auth, PII, or cross-service data flows
- **Context management** (from `skills/strategic-compact/`): For long architecture sessions, compact context at logical breakpoints

---

## 5. Phase 2 — Architecture Skills (Short-Term)

### 5.1 Java and Spring Boot Analysis Skills

**File**: `source-code/.instructions.md`

Adapts from: `skills/java-coding-standards/`, `skills/springboot-patterns/`, `skills/jpa-patterns/`

Content:
- Java coding standards for NovaTrek source code analysis
- Spring Boot patterns (dependency injection, entity/repository, transactions)
- JPA/Hibernate anti-pattern detection (N+1 queries, entity replacement, missing `@Version`)
- Spring Security patterns for authentication and authorization

### 5.2 Database Design Skills

**File**: `architecture/metadata/.instructions.md`

Adapts from: `skills/postgres-patterns/`, `skills/database-migrations/`

Content:
- PostgreSQL schema design best practices
- Database migration strategy (no-downtime, rollback strategies)
- Index optimization patterns
- Data store documentation standards for NovaTrek services

### 5.3 Docker and Local Development

**File**: `docker-compose.yml` folder `.instructions.md`

Adapts from: `skills/docker-patterns/`

Content:
- Docker Compose patterns for multi-service orchestration
- Container security best practices
- Volume management for persistent data
- Network configuration for service isolation

### 5.4 Enhanced Security Review

**File**: `.github/prompts/security-review.prompt.md`

Adapts from: `skills/security-review/`, `skills/springboot-security/`

Content:
- Full OWASP Top 10 checklist
- Spring Boot-specific security patterns
- NovaTrek PII handling (guest profiles, waivers, payment data)
- Cross-service authentication patterns
- Severity rating methodology (Critical/High/Medium/Low)

---

## 6. Phase 3 — Advanced Workflows (Medium-Term)

### 6.1 Verification Loop for Solution Designs

Adapts from: `skills/verification-loop/`, `skills/springboot-verification/`

Create a verification prompt that runs a quality gate on solution designs before they are merged:

- All affected services identified with specific API/schema changes
- MADR ADRs created for cross-boundary decisions
- Impact assessments address WHAT changes (not HOW)
- User stories written from user perspective
- ISO 25010 quality attributes assessed
- Backward compatibility addressed
- Prior-art referenced

### 6.2 Continuous Learning Integration

Adapts from: `skills/continuous-learning/`, `skills/continuous-learning-v2/`

Implement pattern extraction from architecture sessions:

- After each solution design session, extract reusable patterns
- Store patterns in `architecture/reminders/` (existing location)
- Build instinct library: atomic observations that evolve into architectural heuristics
- Examples: "When svc-check-in is involved, always check Pattern 3 safety fallback" or "Cross-domain calls require event-driven integration"

### 6.3 Multi-Agent Workflow Patterns

Adapts from: `skills/autonomous-loops/`, `skills/enterprise-agent-ops/`

Document structured multi-agent workflows for complex scenarios:

- **Scenario 1 — Full Ticket Investigation**: Research agent explores ticket, Architect agent designs solution, Security reviewer agent validates
- **Scenario 2 — Impact Analysis**: One agent per affected service, results consolidated by architect agent
- **Scenario 3 — ADR Authoring**: Research agent gathers options, Architect agent evaluates trade-offs, Documentation agent formats MADR

### 6.4 Context Management Strategy

Adapts from: `skills/strategic-compact/`

Implement context checkpointing for long architecture sessions:

- Save progress to session memory at logical breakpoints
- Compact context when approaching limits
- Resume from checkpoints with full architectural context
- Use `architecture/reminders/` for persistent cross-session notes

---

## 7. Phase 4 — Continuous Learning (Longer-Term)

### 7.1 Architecture Instinct Library

Build a NovaTrek-specific instinct library based on ECC's continuous learning patterns:

| Instinct | Confidence | Source |
|----------|-----------|--------|
| "Unknown adventure categories default to Pattern 3" | HIGH | ADR-005 |
| "Cross-domain communication uses events, not REST" | HIGH | Bounded Context Rules |
| "svc-guest-profiles is the only identity source" | HIGH | Data Ownership |
| "PATCH semantics for schedule updates, not PUT" | HIGH | ADR-010 |
| "Always check capability-changelog.yaml before new solutions" | HIGH | Prior-art discovery |

### 7.2 Eval-Driven Architecture Quality

Adapts from: `skills/eval-harness/`

Create evaluation criteria for AI-generated architecture artifacts:

- **Solution Design Completeness**: Does it cover all required sections?
- **ADR Quality**: Are at least 2 genuine options considered? Are consequences documented?
- **Impact Assessment Accuracy**: Are affected services correctly identified? Are API changes specific?
- **Prior-Art Reference**: Is the capability changelog consulted? Are related solutions referenced?

### 7.3 Cost-Aware Model Routing for Architecture Tasks

Adapts from: `skills/cost-aware-llm-pipeline/`

Optimize model selection for different architecture tasks:

| Task | Recommended Model | Rationale |
|------|------------------|-----------|
| Ticket triage (simple) | GPT-4o (0x multiplier) | Low complexity, saves premium requests |
| Investigation and research | Claude Sonnet 4 (1x) | Good balance of depth and cost |
| Solution design | Claude Opus 4.6 (3x) | Complex reasoning, multi-service analysis |
| Documentation formatting | GPT-4o (0x) | Mechanical task, no deep reasoning needed |

---

## 8. Skill Translation Guide — Claude Code to Copilot

### How to Adapt an ECC Skill for Copilot

**Step 1**: Read the ECC `SKILL.md` file
- Extract the "When to Activate" triggers
- Extract the "Core Workflow" steps
- Extract the "Reference Guide" lookup table

**Step 2**: Determine the Copilot target format

| If the skill is... | Create... | Location |
|--------------------|-----------|----------|
| Folder-scoped (applies to a directory) | `.instructions.md` | In the relevant directory |
| A reusable workflow | `.prompt.md` | `.github/prompts/` |
| A global rule | Section in `copilot-instructions.md` | `.github/copilot-instructions.md` |

**Step 3**: Adapt the content
- Replace Claude Code-specific references (subagent delegation, hooks, slash commands)
- Add NovaTrek domain context (service names, data ownership, safety rules)
- Reference workspace files instead of generic examples
- Include file paths to relevant specs, metadata, and source code

**Step 4**: Test the skill
- Run a scenario that would trigger the skill
- Verify the AI follows the skill's workflow
- Check that domain-specific context is applied correctly

### Example Translation

**ECC Source** (`skills/api-design/SKILL.md`):
```markdown
## When to Activate
- Designing new API endpoints
- Reviewing existing API contracts
```

**Copilot Adaptation** (`architecture/specs/.instructions.md`):
```markdown
## When Working in This Directory
When creating or modifying OpenAPI specs in this directory:
1. Follow REST API design patterns (resource naming, status codes, pagination)
2. Validate schema completeness: all fields need types, descriptions, and nullable annotations
3. Check backward compatibility: new required fields break existing consumers
4. Cross-reference with data ownership boundaries in architecture/metadata/data-ownership.yaml
5. Verify enum values against NovaTrek domain values (adventure categories, check-in patterns)
```

---

## 9. Demonstration Plan

### Demo 1 — API Design Skill in Action

**Objective**: Show how the adapted API design skill improves OpenAPI spec quality.

**Setup**:
1. Create `architecture/specs/.instructions.md` with adapted API design patterns
2. Open an existing OpenAPI spec (e.g., `architecture/specs/svc-check-in.yaml`)

**Scenario**: Ask Copilot to "Add a new endpoint for group check-in to svc-check-in"

**Expected Behavior** (with ECC skill):
- Follows resource naming conventions (POST `/check-ins/group`)
- Includes proper status codes (201 Created, 400 Bad Request, 409 Conflict)
- Adds pagination for list endpoints
- Documents nullable fields
- Cross-references with `svc-guest-profiles` for identity resolution
- Applies Pattern 3 safety fallback rule

**Comparison** (without skill):
- May use inconsistent naming
- May omit error responses
- May not consider NovaTrek domain rules

### Demo 2 — Research-First Investigation

**Objective**: Show how the research-first workflow improves ticket investigation quality.

**Setup**:
1. Create `.github/prompts/investigation.prompt.md` with research mode
2. Use a ticket that requires cross-service investigation

**Scenario**: "Investigate NTK-10005 using the investigation workflow"

**Expected Behavior** (with ECC skill):
- Activates research mode (understand before acting)
- Runs JIRA mock tool first for ticket context
- Runs Elastic mock tool for production logs
- Runs GitLab mock tool for related MRs
- Forms hypothesis based on evidence
- Documents findings with specific file paths and line numbers
- Produces structured investigation report

### Demo 3 — Security Review Enhancement

**Objective**: Show how the security review skill catches issues in solution designs.

**Setup**:
1. Create `.github/prompts/security-review.prompt.md`
2. Use a solution design that involves PII or authentication

**Scenario**: "Run a security review on the NTK-10003 solution design"

**Expected Behavior** (with ECC skill):
- Applies OWASP Top 10 checklist
- Checks PII handling (guest profiles, waiver data)
- Validates authentication flow through svc-guest-profiles
- Identifies missing input validation at service boundaries
- Rates findings by severity
- Produces structured security report

### Demo 4 — Continuous Learning Capture

**Objective**: Show how architectural insights are captured and reused across sessions.

**Setup**:
1. Create a learning capture prompt
2. Complete a solution design session

**Scenario**: After completing a solution design, run "Capture architectural learnings from this session"

**Expected Behavior**:
- Extracts reusable patterns (e.g., "Group check-in requires orchestrator pattern")
- Stores in `architecture/reminders/` with timestamps
- On next session, loads relevant reminders as context
- Patterns evolve into architectural instincts over time

### Demo 5 — Before/After Comparison

**Objective**: Side-by-side comparison of AI output quality with and without ECC skills.

**Method**:
1. Run the same architecture task twice:
   - **Run A**: Default Copilot with existing `copilot-instructions.md` only
   - **Run B**: Copilot with ECC-adapted skills loaded
2. Compare output on these dimensions:

| Dimension | Measurement |
|-----------|------------|
| Completeness | Are all required sections present? |
| Domain accuracy | Does it respect NovaTrek data ownership, safety rules? |
| API quality | Do proposed API changes follow REST best practices? |
| Security coverage | Are security implications assessed? |
| Prior-art reference | Are existing solutions and ADRs consulted? |
| Actionability | Can the output be used as-is or needs significant rework? |

---

## 10. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Instruction overload — too many `.instructions.md` files confuse the AI | Medium | Medium | Start with Tier 1 only; validate before adding more |
| Context window exhaustion — long instructions consume tokens | Medium | High | Keep instructions concise; use `.prompt.md` for on-demand loading |
| Claude Code-specific patterns not translating to Copilot | Medium | Medium | Test each adaptation; document what works and what does not |
| ECC updates breaking adapted skills | Low | Low | Pin to current commit; update selectively |
| Skill conflicts with existing copilot-instructions | Low | Medium | Instructions augment, not override; test for contradictions |
| Over-engineering — adding skills that are never activated | Medium | Low | Track activation frequency; prune unused skills quarterly |

---

## 11. File Manifest — What Gets Created or Modified

### New Files to Create

| File | Source(s) | Phase |
|------|----------|-------|
| `architecture/solutions/.instructions.md` | `agents/architect.md`, `agents/planner.md`, `skills/search-first/` | 1 |
| `architecture/specs/.instructions.md` | `skills/api-design/` | 1 |
| `architecture/.instructions.md` | `skills/security-review/`, `rules/common/security.md` | 1 |
| `.github/prompts/deep-research.prompt.md` | `skills/deep-research/` | 1 |
| `.github/prompts/architecture-review.prompt.md` | `agents/architect.md`, `skills/security-review/` | 1 |
| `.github/prompts/investigation.prompt.md` | `contexts/research.md`, `skills/search-first/` | 1 |
| `.github/prompts/security-review.prompt.md` | `skills/security-review/`, `skills/springboot-security/` | 2 |
| `source-code/.instructions.md` | `skills/java-coding-standards/`, `skills/springboot-patterns/` | 2 |
| `.github/prompts/verification.prompt.md` | `skills/verification-loop/` | 3 |
| `.github/prompts/capture-learnings.prompt.md` | `skills/continuous-learning/` | 3 |

### Files to Modify

| File | Change | Phase |
|------|--------|-------|
| `.github/copilot-instructions.md` | Add "AI Workflow Patterns" section (search-first, research mode, security-first, context management) | 1 |
| `.gitignore` | Confirm `everything-claude-code/` is tracked or explicitly managed | 1 |

### Reference Files (Read-Only)

The `everything-claude-code/` directory remains as a read-only reference. Skills are adapted, not symlinked.

---

## Appendix A — ECC Skill Format Reference

### SKILL.md Structure (Claude Code)

```yaml
---
name: skill-name
description: When and why to use this skill
origin: ECC
---
```

```markdown
# Skill Name
## When to Activate
## Core Workflow
## Reference Guide
## Rules and Conventions
```

### Copilot .instructions.md Structure

```markdown
---
applyTo: "**/*.yaml"  # optional: restrict to file types
---

# Context for AI
## When Working in This Directory
## Quality Checklist
## Domain Rules
```

### Copilot .prompt.md Structure

```markdown
---
mode: "agent"
description: "Description shown in prompt picker"
---

# Workflow Name
## Steps
## Output Format
## Validation
```

---

## Appendix B — Full ECC Skills Catalog (108 Skills)

See the complete catalog in `everything-claude-code/README.md` or the detailed exploration notes. The skills are grouped into:

- **Architecture and Design** (11 skills) — api-design, backend-patterns, frontend-patterns, docker-patterns, android-clean-architecture, swiftui-patterns, kotlin-ktor-patterns, kotlin-exposed-patterns, kotlin-coroutines-flows, swift-actor-persistence, swift-concurrency-6-2
- **Security** (5 skills) — security-review, security-scan, django-security, laravel-security, springboot-security
- **Documentation and Research** (8 skills) — deep-research, article-writing, market-research, investor-materials, investor-outreach, documentation-lookup, regex-vs-llm-structured-text, iterative-retrieval
- **Testing and Quality** (16 skills) — tdd-workflow, springboot-tdd, e2e-testing, django-tdd, django-verification, laravel-verification, springboot-verification, cpp-testing, rust-testing, golang-testing, kotlin-testing, python-testing, verification-loop, eval-harness, test-coverage, quality-nonconformance
- **DevOps and Deployment** (4 skills) — deployment-patterns, database-migrations, bun-runtime, nextjs-turbopack
- **Code Quality and Patterns** (12 skills) — coding-standards, java-coding-standards, python-patterns, golang-patterns, rust-patterns, cpp-coding-standards, perl-patterns, laravel-patterns, django-patterns, springboot-patterns, plankton-code-quality, strategic-compact
- **AI/Agent Engineering** (12 skills) — agentic-engineering, autonomous-loops, continuous-agent-loop, continuous-learning, continuous-learning-v2, enterprise-agent-ops, skill-stocktake, team-builder, ralphinho-rfc-pipeline, nanoclaw-repl, agent-harness-construction, configure-ecc
- **Domain-Specific and Business** (13 skills) — Various industry verticals
- **Foundation Models and APIs** (4 skills) — foundation-models-on-device, claude-api, cost-aware-llm-pipeline, prompt-optimizer
- **Infrastructure and Search** (4 skills) — clickhouse-io, postgres-patterns, exa-search, search-first
- **Other** (19 skills) — Various specialized skills

---

## Appendix C — ECC Agents Catalog (25 Agents)

| Agent | Copilot Equivalent | Applicability |
|-------|--------------------:|---------------|
| architect | Copilot Agent Mode (default) | HIGH — already our primary use case |
| planner | Copilot Agent Mode with todo list | HIGH — maps to our solution design workflow |
| security-reviewer | `.prompt.md` security review | HIGH — important for NovaTrek safety domain |
| code-reviewer | Copilot code review feature | MEDIUM — useful for architecture code review |
| database-reviewer | `.prompt.md` database review | MEDIUM — relevant to data store analysis |
| java-reviewer | `.prompt.md` Java review | MEDIUM — relevant to source code analysis |
| doc-updater | Copilot Agent Mode | MEDIUM — documentation maintenance |
| build-error-resolver | N/A | LOW — we do not build NovaTrek services |
| tdd-guide | `.prompt.md` TDD workflow | LOW — architecture work, not implementation |
| Others | N/A | LOW — language/framework specific, not our focus |
