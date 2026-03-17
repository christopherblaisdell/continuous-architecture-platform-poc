# Deep Research Prompt: OpenSpec vs CALM — Complementary or Competing Frameworks for Continuous Architecture

## Research Objective

I need a comprehensive, technically precise analysis of OpenSpec (by Fission AI) and how it compares to, complements, or conflicts with CALM (Common Architecture Language Model, by FINOS/Architecture as Code). I am building a **Continuous Architecture Platform** for a microservices-based system (19 services, 9 domains) and currently use CALM as an auto-generated governance and topology layer. A peer organization (Comcast) has begun adopting OpenSpec with some teams, and I need to understand whether OpenSpec adds value to my existing CALM stack, could replace aspects of it, or is solving an entirely different problem.

---

## My Exact Setup

### Current Architecture Platform (NovaTrek Adventures — Synthetic POC)

- **19 microservices** across 9 bounded domains with OpenAPI specs, AsyncAPI event specs, and YAML metadata
- **CALM integration** (Phase 0-1 active): auto-generated CALM topology JSON from metadata YAML, CI-enforced architecture rules (no shared databases, API-mediated access), portal visualization
- **Solution design workflow**: ticket-driven architecture work with structured folder layout (requirements, analysis, solution with assumptions/capabilities/decisions/guidance/impacts/risks/user stories)
- **AI-assisted architecture**: GitHub Copilot Agent Mode operating as Solution Architect role with mock JIRA/Elastic/GitLab tools
- **Documentation portal**: MkDocs Material site with auto-generated microservice pages, topology pages, capability pages, solution pages
- **Architecture standards**: MADR for decisions, C4 model for diagrams, arc42 template structure, ISO 25010 quality attributes
- **CI/CD**: GitHub Actions validating CALM topology, solution folder structure, YAML schema, and portal generation

### CALM Specifics

- **Generator**: `scripts/generate-calm.py` reads metadata YAML and OpenAPI specs, produces domain-specific JSON + full system topology
- **Validator**: `scripts/validate-calm.py` enforces 5 architecture rules (no shared databases, API-mediated access, service metadata required, relationship integrity, no orphan services)
- **Patterns**: `architecture/calm/patterns/novatrek-microservice.json` — reusable architecture rules
- **Controls**: `architecture/calm/controls/data-ownership.json`, `api-mediated-access.json`
- **Topology**: 74 nodes, 146 relationships across 9 domain files + 1 system-level file
- **Portal integration**: `portal/scripts/generate-topology-pages.py` produces Mermaid system maps, dependency matrices, domain statistics
- **Planned (Phase 2-5)**: portal generators consuming CALM directly, 6+ CI governance rules, solution design topology diffs, drift detection, blast radius analysis, timeline visualization

### OpenSpec Basics (From My Initial Research)

- **Framework**: Lightweight, spec-driven framework for AI coding agents and CLIs
- **Core concept**: Specs (system behavior contracts) + Changes (proposed modifications as delta specs)
- **Artifacts per change**: proposal.md, design.md, tasks.md, delta specs
- **Workflow**: `/opsx:propose` -> `/opsx:apply` -> `/opsx:archive`
- **Archive**: Delta specs merge into main specs, change folder preserved in archive
- **31.5k GitHub stars**, 50 contributors, MIT license, npm package
- **Supports**: Claude Code, Cursor, Codex, GitHub Copilot, and 16+ more tools
- **Key differentiator**: Brownfield-first (delta specs), fluid iteration (not phase-locked), tool-agnostic

---

## Specific Questions to Research

### 1. Are CALM and OpenSpec Solving the Same Problem?

CALM is a **machine-readable architecture specification** format (JSON Schema-based) for defining system topology — nodes, relationships, interfaces, patterns, controls, timelines, decorators. It enables automated validation, visualization, and governance of architecture.

OpenSpec is a **spec-driven development framework** for AI coding agents that uses structured Markdown to capture behavioral requirements, design decisions, and implementation tasks.

- Are these genuinely complementary layers (architecture topology vs. behavioral contracts)?
- Does OpenSpec have any architecture modeling capabilities that overlap with CALM's node/relationship/interface model?
- Is OpenSpec's "spec" concept more analogous to CALM's "pattern" concept, or to something CALM doesn't cover at all?

### 2. How Does OpenSpec Handle Architecture-Level Concerns?

- Can OpenSpec specs describe cross-service interactions, data ownership rules, or API contracts?
- Does OpenSpec have any concept of system topology, service dependencies, or deployment architecture?
- How does OpenSpec handle non-functional requirements (performance, reliability, security) compared to CALM's controls and standards?
- Does OpenSpec support schema validation or CI enforcement of architecture rules?

### 3. What Does OpenSpec's Adoption Look Like at Enterprise Scale?

- What is Comcast's specific use case for OpenSpec? How are they using it with their engineering teams?
- Are there other large enterprises using OpenSpec? What scale (number of services, team size)?
- Is OpenSpec being used for architecture governance, or purely for feature development workflow?
- What is the maturity level — is it production-ready for enterprise architecture platforms?
- How does OpenSpec's governance model compare to CALM's (FINOS foundation vs. Fission AI startup)?

### 4. Where Could OpenSpec Add Value to a CALM-Based Platform?

Given that CALM handles topology, validation, and governance, could OpenSpec add value in:

- **Solution design workflow**: Could OpenSpec's change/artifact/delta model improve or replace my current `architecture/solutions/` folder structure?
- **Requirements capture**: Could OpenSpec specs replace or supplement the ticket-based requirements gathering in my solution design workflow?
- **AI agent guidance**: Could OpenSpec's slash commands and skill files improve how AI agents interact with my architecture workspace?
- **Implementation tracking**: Could OpenSpec's task tracking and delta spec model improve how I track the implementation of architecture decisions?
- **Spec evolution**: Could OpenSpec's archive model (delta merge into source of truth) improve how I manage API contract evolution?

### 5. What Are the Integration Points Between CALM and OpenSpec?

- Could OpenSpec change proposals trigger CALM topology updates?
- Could CALM topology data be surfaced as context in OpenSpec specs?
- Is there a natural mapping between OpenSpec artifacts and CALM concepts (e.g., OpenSpec design.md -> CALM pattern, OpenSpec spec.md -> CALM interface)?
- Could the two tools share a CI/CD pipeline (e.g., OpenSpec validates behavioral specs, CALM validates structural topology)?

### 6. What Are the Risks of Adopting OpenSpec?

- **Overlap risk**: Would OpenSpec create a second source of truth that conflicts with CALM?
- **Tooling lock-in**: OpenSpec is MIT license but by a startup (Fission AI) — what is the bus factor?
- **Context window impact**: Does OpenSpec's spec-in-repo model add meaningful context weight for AI agents? Is that a benefit or a cost?
- **Team adoption**: Is OpenSpec designed for individual developers or teams? What's the team collaboration model?
- **Maturity risk**: OpenSpec is at v1.2.0 with 34 releases in ~7 months — is the API stable enough for enterprise commitment?

### 7. How Does OpenSpec Compare to Our Existing Solution Design Workflow?

My current workflow already has structured artifacts:

| My Current Workflow | OpenSpec Equivalent |
|--------|---------|
| `architecture/solutions/_NTK-XXXXX-slug/` | `openspec/changes/<name>/` |
| `1.requirements/` | Part of `proposal.md` |
| `2.analysis/` | `proposal.md` + `/opsx:explore` |
| `3.solution/d.decisions/decisions.md` | `design.md` |
| `3.solution/i.impacts/` | No direct equivalent? |
| `3.solution/u.user.stories/` | Part of `specs/` scenarios? |
| `architecture/metadata/capability-changelog.yaml` | `openspec/specs/` (delta merge on archive) |

Is OpenSpec's artifact model richer, simpler, or just different from my existing solution design workflow?

---

## What I Need from This Research

1. **Category clarity**: Is OpenSpec in the same category as CALM, or a different category entirely? What Venn diagram best describes their overlap/complementarity?
2. **Enterprise evidence**: Real-world adoption data — who is using OpenSpec at scale, for what use cases, and what outcomes they report
3. **Integration feasibility**: Concrete assessment of whether the two frameworks can coexist in a single CI/CD pipeline without creating source-of-truth conflicts
4. **Recommendation framework**: A decision matrix for choosing between "CALM only", "CALM + OpenSpec", and "CALM replaced by OpenSpec" based on platform maturity, team size, and use case
5. **Migration path**: If OpenSpec is valuable, what does a phased adoption look like alongside existing CALM infrastructure?
6. **Risk register**: What could go wrong with each adoption option, and what mitigations exist?

---

## Research Constraints

- I am NOT looking for a "gut feel" recommendation — I need evidence-based analysis with source citations
- I need to understand the **current state** of both projects as of March 2026, not historical or aspirational
- I care about **architecture governance and platform engineering** use cases specifically, not generic developer productivity
- I need to understand whether OpenSpec's "spec-driven development" paradigm conflicts with or enhances my "continuous architecture" paradigm
- I am evaluating this for a **proof of concept** — I need to know the minimum viable experiment to test the hypothesis before committing

---

## Output Format

Please structure your response as:

1. **Executive Summary** (3-5 sentences)
2. **Framework Comparison Matrix** (side-by-side feature table)
3. **Complementarity Analysis** (where they overlap, where they're orthogonal)
4. **Enterprise Adoption Evidence** (real-world cases with citations)
5. **Integration Architecture** (how they could coexist technically)
6. **Risk Assessment** (per-option risk register)
7. **Recommendation** (with decision criteria and confidence level)
8. **Minimum Viable Experiment** (concrete next steps to validate the recommendation)
