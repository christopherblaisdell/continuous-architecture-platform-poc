# Strategic Realignment of Enterprise AI Architecture

**Date**: 2026-03-31
**Status**: Research Input
**Scope**: Enterprise Architecture Practice, AI Tooling, Governance, Integration

---

## Table of Contents

1. Executive Summaries
2. Individual Stakeholder Feedback Analysis
3. Integration of AI with CI and Documentation Pipelines
4. GitOps Governance for AI Customizations via Pull Requests
5. Balancing Mandatory Shared Context with Personal Workflow Customizations
6. Confluence Integration and Enterprise Knowledge Retrieval
7. Advanced Vectorization and Chunking of PlantUML Artifacts
8. Hybrid Architecture: GitHub Copilot + Azure AI Foundry via MCP
9. Two-Layer Decision Model
10. Conclusions
11. Decision Point Influence Assessment

---

## 1. Executive Summaries

### Micro Summary (One Paragraph)

The enterprise AI tooling strategy is not a forced choice between commercial IDE-native agents and custom backend orchestration. Model Context Protocol (MCP) enables a hybrid architecture where GitHub Copilot remains the local execution engine while Azure AI Foundry serves as a secure backend tool provider. Existing documentation-as-code pipelines already deliver deterministic linting, validation, and publishing, so AI should augment remediation rather than rebuild pipeline capabilities. Repository-managed instructions and skills provide governance through pull requests while preserving personal workflow customization. With direct Confluence retrieval and improved handling of PlantUML artifacts, the architecture practice can deliver contextual and autonomous assistance without sacrificing governance or undertaking heavy custom platform engineering.

### Meso Summary (One Page)

The historical framing of AI adoption as a binary decision (buy Copilot-like tooling versus build a custom Foundry app) is a false dichotomy. The practical architecture is hybrid: use the embedded execution strengths of Copilot in local workflows and expose governed enterprise capabilities from Azure through MCP servers.

The practice already has deterministic quality gates in documentation pipelines (lint, schema validation, artifact generation, publishing). AI should not replace deterministic checks. Instead, AI should detect and remediate failures by consuming pipeline logs and generating targeted fixes in pull requests.

Governance is strongest when instructions are managed in-repo. Custom instructions and skills evolve through pull request review, producing auditable history, peer validation, rollback safety, and alignment with normal software delivery controls.

A layered instruction strategy resolves enterprise compliance versus personal ergonomics:
- Enterprise mandatory controls at org/repo level
- Team/repo architecture standards in shared instructions
- Individual formatting and workflow preferences at user level

Confluence and related enterprise context should be retrieved live through authenticated MCP integration rather than solely through centralized static indexing. This improves freshness and security alignment because access follows user permissions.

For architecture-heavy practices, diagram handling is pivotal. Naive chunking often degrades PlantUML integrity; structural and agentic chunking strategies preserve semantic boundaries and reduce diagram hallucination risk.

Overall, the strongest strategy is to buy the execution client, build proprietary backend tools, and connect them through MCP.

The selection method should therefore also be split in two. Platform choice should be handled as a weighted option evaluation using factors similar to system quality attributes. The broader architecture-practice design should be handled separately as an operating-model decision map covering governance, trust, autonomy, knowledge curation, and integration patterns.

### Macro Summary (Three Page Equivalent)

#### 1) The Procurement Frame Is Outdated

The old question of "buy versus build" does not reflect current technical reality. Embedded assistants now support deep customization and MCP-based extension, while cloud platforms support enterprise integrations and governed data access. The resulting system is composable.

#### 2) Existing CI/CD and Docs Pipelines Are Strategic Assets

Documentation-as-code pipelines already provide deterministic governance:
- Markdown and YAML linting
- Link/reference integrity checks
- Diagram and content validation
- Automatic publish to documentation targets

AI should participate in this system by remediating failures, not by replacing deterministic controls.

#### 3) Instructions-as-Code Is the Governance Backbone

Managing AI behavior in repository files gives enterprises:
- Auditability of behavior changes
- Peer-reviewed policy evolution
- Fast rollback on problematic prompt/instruction changes
- Clear coupling between architecture standards and AI behavior

This model prevents prompt drift and aligns AI governance with existing GitOps operating models.

#### 4) Mandatory Standards and Personal Ergonomics Can Coexist

Layered instruction hierarchies allow non-negotiable enterprise controls while preserving developer-specific presentation and workflow preferences. The assistant synthesizes both without violating top-level constraints.

#### 5) Enterprise Knowledge Retrieval Must Be Live and Permission-Aware

MCP enables live retrieval from systems such as Confluence. This provides fresher context than static snapshots and preserves access boundaries through user credentials and enterprise identity controls.

#### 6) Diagram Intelligence Is a First-Class Requirement

Architecture practice depends on diagrams. Generic chunking can break PlantUML context. Structural parsing and agentic chunking approaches are required for reliable understanding and modification of diagram-as-code artifacts.

#### 7) The Optimal Pattern Is Hybrid

Use embedded tools for local autonomous execution (file edits, terminal runs, workspace context), and use Azure-hosted MCP services for enterprise-specific retrieval and governed tools. This minimizes custom UI/state-management engineering while maximizing enterprise integration value.

---

## 2. Individual Stakeholder Feedback Analysis

### Feedback 1: Existing MkDocs pipeline already lints, validates, publishes

Assessment: Correct and strategically important. Deterministic pipeline governance already exists; AI should focus on remediation and acceleration.

### Feedback 2: Shared solution + PR-driven skills/instructions evolution

Assessment: Correct. GitOps for AI customizations is a strong governance model and reduces need for a separate central AI admin application.

### Feedback 3: Mandatory shared customizations + personal workflow customizations

Assessment: Correct. Instruction hierarchy supports both compliance and productivity.

### Feedback 4: Copilot can retrieve Confluence context

Assessment: Correct direction. MCP-based retrieval narrows the historical local-context limitation.

### Feedback 5: Copilot vectorization can handle PlantUML better than many platforms

Assessment: Plausible and strategically relevant. Diagram handling is a key differentiator for architecture practices.

### Feedback 6: Evaluate non-mutual exclusivity and custom MCP service value

Assessment: Core strategic point. The best architecture is complementary: local execution engine plus custom cloud-hosted MCP capabilities.

---

## 3. Integration of AI with CI and Documentation Pipelines

### Practical Position

AI should not be the primary compliance gate. CI remains deterministic authority. AI becomes:
- Failure triage assistant
- Remediation generator
- Standards drift detector
- Artifact consistency maintainer

### Example Remediation Loop

1. Pipeline fails on link, lint, or diagram check
2. Agent reads logs and traces the exact source location
3. Agent proposes a focused fix in PR
4. CI re-runs and validates deterministically

---

## 4. GitOps Governance for AI Customizations via Pull Requests

### Guidance

Treat AI behavior as code:
- Shared instructions in repository
- Path-specific rules for focused contexts
- Reusable skills for multi-step workflows
- PR review for every behavior change

### Benefits

- Traceability of instruction changes
- Peer review of AI behavior changes
- Versioned rollback for regressions
- Alignment with existing architecture governance

---

## 5. Balancing Mandatory Shared Context with Personal Workflow Customizations

### Three-Tier Model

| Tier | Scope | Purpose |
|------|-------|---------|
| Enterprise | Organization policy | Non-negotiable security/compliance constraints |
| Repository | Project/practice standards | Architecture and workflow consistency |
| Personal | Individual profile | Output style and personal ergonomics |

### Design Principle

Higher tiers constrain lower tiers. Personal customization changes presentation and workflow style, not mandatory policy outcomes.

---

## 6. Confluence Integration and Enterprise Knowledge Retrieval

### Strategic Direction

Use authenticated MCP retrieval for live enterprise context. Preserve least-privilege by honoring user identity and source permissions.

### Value

- Current requirements and decision records are available in-session
- Reduced context switching for architects
- Improved mapping from business requirements to architecture artifacts

---

## 7. Advanced Vectorization and Chunking of PlantUML Artifacts

### Problem

Naive chunking splits diagram structure at arbitrary boundaries and corrupts semantic integrity.

### Recommended Approach

- Structural parsing where possible
- Semantic/agentic chunking for diagram sections
- Keep related diagram elements together in retrieval units
- Prefer retrieval strategies that preserve graph intent

### Expected Outcome

Better diagram reasoning fidelity and lower hallucination risk for architecture refactoring tasks.

---

## 8. Hybrid Architecture: GitHub Copilot + Azure AI Foundry via MCP

### Pattern

- Client: Local embedded assistant (Copilot in VS Code)
- Server: Azure AI Foundry-hosted MCP services for enterprise data/tools

### Why This Works

- Keeps strong local execution autonomy
- Avoids rebuilding IDE UX/state systems
- Enables secure enterprise integrations where needed
- Concentrates custom engineering on proprietary tool endpoints

### Typical Flow

1. Architect issues request locally
2. Local agent routes enterprise-specific tool call via MCP
3. Azure service executes governed backend logic
4. Result returns to local agent for synthesis and artifact updates

---

## 9. Two-Layer Decision Model

The architecture practice should use a two-layer decision structure rather than collapsing every question into a single list.

### Layer 1 - Platform Selection Scorecard

This layer answers: Which platform or platform combination should the practice adopt?

The method should be a weighted scorecard. Each option is scored against a fixed set of factors, and each factor carries a weight based on practice priorities.

Suggested factor types:

| Factor Category | Example Factors |
|----------------|-----------------|
| Cost | Seat cost, usage variability, overage risk |
| Quality | Architecture output quality, standards compliance, diagram handling |
| Workflow Fit | VS Code integration, GitHub/PR integration, CI/CD fit |
| Governance | Policy controls, auditability, instruction governance, permissions |
| Extensibility | MCP support, custom tools, enterprise integration capability |
| Portability | Vendor lock-in risk, portability of knowledge/configuration |
| Operations | Supportability, setup complexity, reliability, latency |

This is similar to system quality attribute trade-off analysis, but applied to AI platform options.

### Layer 2 - Operating Model Decision Map

This layer answers: Once a platform direction is selected, how should the practice actually operate it?

This includes questions such as:

- Buy vs build posture
- Billing model preference
- Single-tool vs multi-tool strategy
- Human review and trust model
- Standards enforcement model
- Knowledge curation model
- Ticketing and Confluence integration patterns
- Hybrid MCP architecture choices

These are not all platform-scoring criteria. Many are policy, governance, and operating-model questions that remain relevant after a platform is selected.

### Why The Layers Must Stay Separate

If everything is forced into one weighted scorecard, the practice will mix two different kinds of questions:

- Selection questions: Which option scores best against weighted criteria?
- Governance questions: How should the chosen option be used, constrained, and evolved?

Keeping them separate makes the decision process clearer:

1. Use Layer 1 to compare options objectively.
2. Use Layer 2 to define the rules of use and the long-term operating model.

### Practical Recommendation

Use the existing ADR-001 style criteria as the seed for Layer 1, but broaden them into a reusable platform scorecard. Keep the AI decision-point document as Layer 2 and explicitly treat it as the operating-model map, not the selection scorecard.

---

## 10. Conclusions

1. The enterprise should reject the false binary of buy versus build.
2. Deterministic CI/docs pipelines should remain source of truth for validation.
3. AI customizations should be governed via GitOps pull request workflows.
4. Layered instructions should enforce mandatory policy while preserving personal productivity.
5. Confluence and other enterprise context should be integrated through secure MCP retrieval.
6. Diagram-aware chunking strategy is required for architecture-grade PlantUML workflows.
7. A hybrid model (Copilot local + Azure MCP backend) is the strongest strategic architecture.
8. Platform selection should use a weighted scorecard, while operating-model design should remain a separate decision map.

---

## 11. Decision Point Influence Assessment

This research influences existing decision points as follows:

| Decision Point | Influence | Suggested Update |
|---------------|-----------|------------------|
| DP-01 Buy vs Build | Reinforces hybrid choice | No status change; strengthen rationale |
| DP-04 Single vs Multi-Tool | Clarifies complementarity (not mutually exclusive) | Keep partially decided, but add hybrid-specific direction |
| DP-05 Standards Enforcement | Confirms CI as deterministic gate + AI remediation role | Move from fully open toward layered model |
| DP-07 Knowledge Curation | Supports layered mandatory/shared/personal context model | Add explicit hierarchy strategy |
| DP-09 Context Enrichment | Reinforces live retrieval + indexing model | No status change; add Confluence/MCP nuance |
| DP-10 Vendor Lock-In vs Portability | Supports portable knowledge + vendor-specific execution | Move from open to partially decided |
| DP-14 Publishing Pipeline | Strongly reinforces current automated pipeline strategy | No status change |
| DP-16 Ticketing Integration | Supports MCP integration pattern already adopted | No status change |
| DP-18 Measuring Value | Adds need for remediation cycle metrics from CI failures | Expand measurement dimensions |
| New Decision Needed | Hybrid Copilot + Azure Foundry via MCP | Add new decision point |
