<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: -->

# AI Customization as a Living Practice: Extensibility, Governance, and Ownership

!!! note "Context for This Analysis"
    This page presents observations and analysis from the architecture practice pilot. The pilot team ran real architecture scenarios against a synthetic workspace, maintaining AI customizations throughout the evaluation. The findings below reflect what that experience revealed about customization extensibility and governance. The team presenting this evaluation does not own the toolchain decision — this analysis is offered as input for the decision-makers to weigh alongside other factors they may consider.

## The Core Premise: AI Customizations Are Never "Done"

AI customizations — instruction files, custom agent definitions, skills, scoped rules — are not a deliverable with a completion date. They are **living artifacts** that grow and evolve continuously with the practice they serve. Every architecture decision record, every new service boundary, every revised data ownership rule, every new workflow convention creates a potential gap between what the AI knows and what the practice needs.

This is not a defect. It is the nature of domain knowledge itself. Architecture practices are not static — they evolve through daily work, through solution designs, through lessons learned in production. If the AI customization layer does not evolve at the same pace, it risks becoming a liability rather than an asset.

The NovaTrek pilot provides direct evidence:

| Metric | Value | Implication |
|--------|-------|-------------|
| `copilot-instructions.md` starting size | ~200 lines | Initial domain model and basic conventions |
| `copilot-instructions.md` ending size | 1,172 lines | Continuous growth as the practice discovered gaps |
| Number of instruction file updates | Dozens during evaluation | Every update was a response to a real gap — not speculative |
| Elapsed time per update | Minutes | Architect fixed the gap in the same session it was discovered |
| Additional scoped instruction files created | 5+ | New patterns emerged that required file-type-specific rules |
| Custom agent definitions added | 1 | Specialized persona for architecture work |

Every one of those updates represents a moment where the AI's behavior diverged from the practice's needs — and was corrected immediately by the practicing architect. In a system where that correction requires a retraining cycle, a ticket to another team, or a multi-week pipeline, those corrections either do not happen or happen too late to matter.

## Extensibility Considerations

For AI customizations to function as living practice artifacts, the pilot experience suggests the customization system benefits from four properties:

### 1. Practitioners Can Modify Customizations Directly

The people who use the AI daily are the people who discover its gaps. If they cannot modify the customization layer themselves — if they must request changes through a separate team, submit tickets, wait for retraining cycles — then the feedback loop that keeps customizations current is broken.

This concern is supported by McKinsey's research on developer productivity with generative AI: "While off-the-shelf generative AI-based tools know a lot about coding, they won't know the specific needs of a given project and organization. Such knowledge is vital... it will be up to software developers to provide these tools with the context." The same principle applies to architecture practices: domain context must flow from practitioners to the AI system without organizational barriers.

### 2. Changes Are Reviewable and Auditable

Extensibility without governance creates risk. When any practitioner can modify the AI's behavior, the practice benefits from mechanisms that ensure quality, consistency, and accountability. Effective governance mechanisms would:

- Make every change visible to the team (transparency)
- Allow team members to review and challenge changes (peer review)
- Record what changed, when, and why (auditability)
- Enable rollback if a change degrades behavior (reversibility)

### 3. New Practitioners Inherit the Full Customization Layer

When a new architect joins the practice, ideally they would receive the entire accumulated customization — every convention, every workflow rule, every domain boundary — without configuration effort. A customization system that is distributable by default avoids the problem of manually reconstructing configuration per person.

### 4. Customizations Compose Without Conflict

As the practice scales, multiple architects will likely contribute customizations across different domains. A system that supports composition — global rules plus domain-specific overrides plus file-type-specific rules — avoids the need for a central coordinator to resolve conflicts manually.

## The Non-Extensible Counterfactual: What Happens When Architects Cannot Control Their Own Customizations

This section examines the concrete consequences of deploying AI customizations through a system that the architecture practice cannot directly modify — for example, a custom fine-tuned model managed by a separate ML engineering team, or a bespoke agent platform maintained by a different organizational unit.

### Consequence 1: The Knowledge Gap Bottleneck

When customizations are controlled by a team that does not practice architecture, every domain knowledge update must cross an organizational boundary:

```
Architect discovers gap → writes ticket describing gap → ML team interprets ticket
→ ML team curates training data → ML team retrains model → ML team validates
→ ML team deploys → Architect tests → (gap may not be fully fixed → repeat)
```

Each step in this chain introduces latency and information loss. The architect who discovered the gap understands it precisely — they can describe the exact scenario, the exact wrong output, and the exact correct behavior. By the time this understanding passes through a ticket, is interpreted by someone who does not practice architecture, is translated into training data, and is embedded in model weights, precision is lost.

This is likely not a process efficiency problem that better ticketing can solve. It appears to be a **structural problem** — the knowledge holders (architects) are separated from the customization mechanism (model weights or platform configuration) by an organizational boundary that cannot be eliminated without collapsing the two teams into one.

### Consequence 2: The Decay Curve Accelerates

DD-06 documents the predictable decay curve of a custom fine-tuned model without sustainable ownership:

| Period | State | Symptom |
|--------|-------|---------|
| Months 1-3 | Current | Output quality is high, architect trust is strong |
| Months 4-6 | Drifting | New services, updated contracts, revised ownership rules not reflected — architects notice increasing inaccuracies |
| Months 7-12 | Stale | Retraining happens if budgeted, but training data curation is slow, ML team is context-switching. Retrained model fixes some gaps, introduces others |
| Month 12+ | Abandoned | Architects no longer trust the custom model's domain knowledge. They either abandon it or add manual corrections that negate the productivity benefit |

When the architecture practice has no direct control over the customization layer, this decay curve is the default trajectory. The only force that can counteract decay is continuous maintenance — and continuous maintenance requires that the maintainers understand the domain. An ML team that is organizationally separate from the architecture practice may struggle to sustain the domain understanding required to keep customizations current.

### Consequence 3: Innovation Is Centrally Bottlenecked

In a non-extensible system, every customization innovation — a new agent persona, a new workflow pattern, a new set of scoped rules for a specific file type — must flow through the team that controls the platform. This creates two problems:

1. **The controlling team becomes a bottleneck for innovation.** They have finite capacity, and every architecture customization request competes with their other priorities (infrastructure maintenance, security patches, feature work for other consumers).

2. **The practicing architects lose the ability to experiment.** The most valuable customizations are discovered through daily work — an architect tries a new prompt pattern, discovers it produces better output, and encodes it as a reusable instruction. In a non-extensible system, this discovery-to-encoding loop is either impossible or requires a multi-week process through the controlling team.

### Consequence 4: The Practice Cannot Build Institutional Knowledge

Architecture practices accumulate institutional knowledge: naming conventions, data ownership rules, safety requirements, solution design workflows, quality standards. In a well-functioning AI-assisted practice, this institutional knowledge is codified in the customization layer — instruction files are documentation that also configures AI behavior.

When the customization layer is controlled by a separate team, institutional knowledge accumulation is blocked. The architecture practice's conventions exist only in the heads of practicing architects or in documents that the AI system never reads. The customization layer becomes a frozen snapshot of whatever the ML team encoded at training time — a point-in-time artifact in a domain that changes continuously.

## Analysis: The Organizational Design Problem

The four consequences above flow from a single root cause: **organizational separation between the domain experts and the customization mechanism**.

This is a well-understood anti-pattern in software engineering. Conway's Law states that organizations design systems that mirror their communication structures. When the architecture practice and the customization team are separate organizational units — with separate priorities, separate backlogs, separate managers, separate incentive structures — the customization system will reflect that separation. It will be optimized for the customization team's workflow (batch retraining cycles, formal validation gates, staged deployments), not the architecture practice's workflow (continuous small updates, rapid experimentation, immediate feedback).

The InnerSource Commons documents this pattern through the Trusted Committer model: when cross-team contributions are required, projects must establish explicit mechanisms for recognizing contributors, formalizing their access, and maintaining the relationship between maintainers and contributors. Without these mechanisms, the organizational boundary becomes a wall that blocks the feedback loop required for living artifacts.

The question is likely not whether customizations should be governed — but rather **where the governance boundary sits**: between the organization and the customization system (so practitioners govern directly via standard engineering workflows) or between the practitioners and a controlling team (so practitioners govern indirectly through tickets and requests).

## Options Assessment

### Option E: Dedicated AI Customization Team (Separate from Architecture Practice)

A specialized team (e.g., an ML engineering group, an AI platform team, or a center of excellence) owns all AI customization artifacts. Architects submit requirements; the customization team implements them.

**How it works:**

- Customization team maintains the fine-tuned model, the agent platform, or whatever system delivers customized AI behavior
- Architects submit tickets describing gaps, new conventions, or workflow changes
- Customization team interprets requirements, implements changes, validates, and deploys
- Architects receive the updated system after the change cycle completes

**Strengths:**

- Clear ownership and accountability for the customization system
- Customization team develops deep expertise in the customization mechanism (fine-tuning, embedding pipelines, model evaluation)
- Centralized quality gate ensures consistency across the organization

**Weaknesses:**

- **Knowledge gap is structural and persistent.** The customization team does not practice architecture. They cannot judge whether output quality meets architectural standards, whether a domain rule is correctly encoded, or whether a new convention should override an existing one. They depend on architects to specify requirements — and requirement specification is itself a lossy process.
- **Change velocity is measured in weeks, not minutes.** A retraining cycle for a fine-tuned model involves data curation, training, validation, and deployment. Even in a well-run MLOps pipeline, this takes days to weeks. For a platform configuration change, the cycle may be shorter but still involves cross-team coordination, prioritization, and scheduling.
- **Innovation is bottlenecked.** Every customization idea — no matter how small — requires a ticket, a handoff, and a wait. The friction suppresses experimentation.
- **The customization team becomes a single point of failure.** If they are understaffed, reprioritized, or reorganized, the architecture practice's AI effectiveness degrades with no recourse.
- **Institutional knowledge is fragmented.** The architecture practice's conventions exist in one place (architects' heads, practice documents); the AI's customizations exist in another place (model weights, platform config). No single artifact captures both — and they inevitably drift apart.

**Industry precedent:** This model is analogous to the "shared services" or "center of excellence" pattern that has been widely studied in enterprise IT. Research from Gartner, Forrester, and McKinsey consistently finds that centralized shared services teams struggle to maintain domain relevance when they are organizationally separated from the business units they serve. The same structural problem applies to AI customization.

### Option F: Architecture Practice Owns All Customizations (No Specialized Team)

The architecture practice directly maintains all AI customization artifacts. No separate team is involved.

**How it works:**

- Architects use declarative customization mechanisms (instruction files, custom agents, skills, scoped rules) that are checked into the architecture repository
- Changes follow standard Git workflows: branch, edit, PR, review, merge
- Every architect can read, modify, and propose changes to the customization layer
- Governance is enforced through code review — the same process used for ADRs, OpenAPI specs, and solution designs

**Strengths:**

- **Zero organizational boundary between domain experts and customization mechanism.** The people who know the domain are the people who write the customization. No knowledge translation required.
- **Change velocity matches practice velocity.** An architect discovers a gap, opens the instruction file, corrects it, and the next prompt uses the corrected context. Same session. No waiting.
- **Innovation is distributed.** Any architect can experiment with new agent personas, workflow patterns, or scoped rules. Successful experiments are submitted as PRs for the team to review and adopt.
- **Institutional knowledge accumulates organically.** Instruction files are documentation that also configures AI behavior. As the practice grows, the customization layer captures increasing depth of domain knowledge in a format that is both human-readable and machine-usable.
- **Onboarding is automatic.** A new architect clones the repository and inherits the full customization layer — every convention, every workflow rule, every domain boundary. No configuration required.

**Weaknesses:**

- **Expertise gap for non-declarative customizations.** If the practice needs fine-tuned models, embedding pipelines, or custom RAG infrastructure, architects lack the ML engineering skills to build and maintain these systems.
- **No specialized support for platform-level concerns.** Model evaluation, cost optimization, usage analytics, and enterprise integration (SSO, audit logging, compliance) are not architecture competencies.
- **Risk of inconsistency at scale.** Without a dedicated governance process, multiple architects contributing customizations could produce conflicting rules. (Mitigated by PR review, but requires discipline.)

**Industry precedent:** This model is analogous to the InnerSource Trusted Committer pattern, where project maintainers empower contributors to make changes directly, with formal review mechanisms to maintain quality. It is also consistent with the DevOps principle of "you build it, you run it" — the people who create value are the people who maintain it.

### Option G: Hybrid Inner Source Model (Option D Extended with Practice-Led Customization Governance)

The architecture practice owns the declarative customization layer directly. A specialized team (if one exists) owns only the infrastructure-level concerns. Architects prototype, test, and submit customizations through a structured inner source workflow with peer review.

**How it works:**

- **Layer 1 — Declarative customizations (owned by architecture practice):** Instruction files, custom agents, skills, scoped rules, `AGENTS.md`, prompt workflows. These are Markdown files in the architecture repository, governed by PR review. Any architect can propose changes. Senior architects serve as Trusted Committers with merge authority.
- **Layer 2 — Model infrastructure (owned by platform/ML team, if applicable):** BYOK endpoint registration, model deployment, API key management, enterprise admin configuration. The platform team provides the model as a service; the architecture practice provides the domain knowledge that shapes its behavior via Layer 1.
- **Layer 3 — Cross-cutting governance (shared):** Cost monitoring, usage analytics, compliance controls, model evaluation. Shared responsibility with clear RACI.

**The prototyping workflow:**

1. **Architect discovers a gap** — the AI does not know a convention, misapplies a rule, or lacks context about a new service
2. **Architect prototypes a fix** — edits an instruction file, creates a new scoped rule, or defines a new agent persona. Tests the fix locally with their preferred model (built-in Claude Opus, GPT-4.1, or the custom BYOK model)
3. **Architect opens a PR** — submits the customization change for peer review. The PR includes "before and after" evidence: the prompt that produced incorrect output, and the same prompt producing correct output with the updated customization
4. **Practice reviews** — other architects review the customization change using the same criteria they apply to ADRs: Is the rule accurate? Is it scoped correctly? Does it conflict with existing customizations? Is it documented clearly?
5. **Merge and distribute** — after approval, the change is merged to main. Every architect who pulls the repository inherits the improved customization immediately
6. **Institutional knowledge grows** — the Git commit history captures what changed, when, why, and who approved it. The customization layer is a living changelog of the practice's evolving conventions

**How this relates to Option D (Hybrid Architecture):**

Option D defines the deployment topology: Copilot as the platform, BYOK for the custom Foundry model. Option G defines the **governance topology**: who maintains what, how changes flow, and how the practice scales its AI effectiveness over time.

| Concern | Option D Addresses | Option G Addresses |
|---------|-------------------|-------------------|
| Which platform? | Copilot (with BYOK for custom model) | N/A — uses whatever Option D provides |
| Which models? | Built-in (Claude Opus, GPT-4.1) + custom Foundry model | N/A — architects select per task |
| Who customizes AI behavior? | Not specified | Architecture practice (Layer 1), platform team (Layer 2) |
| How do customizations evolve? | Not specified | Inner source workflow with PR review and Trusted Committers |
| How is quality maintained? | Not specified | Peer review, "before/after" evidence, governance roadmap |
| How do new architects onboard? | Not specified | Clone repo, inherit full customization layer |

**Strengths:**

- **Combines the best of Options E and F.** Architects own behavioral customizations (where domain expertise matters most); the platform team owns infrastructure (where ML/DevOps expertise matters most). Neither team is asked to do work outside their competency.
- **The prototyping-to-production workflow eliminates the ticket bottleneck.** Architects do not request customizations — they build them, test them with different models (enabled by Option D's multi-model picker), and submit them for peer review. The customization team is not in the critical path for behavioral changes.
- **Multi-model prototyping validates customization quality.** Because Option D provides access to multiple models (built-in + custom), architects can test whether a customization works across models. A rule that produces correct output on Claude Opus but not on the custom Foundry model reveals a model gap; a rule that works on both confirms robustness.
- **Governance scales with the practice.** The same PR review process that works for 2 architects works for 20. As the practice grows, Trusted Committers emerge naturally — the architects who contribute the most customizations and demonstrate the deepest understanding of the customization layer.
- **Customizations and models reinforce each other.** When the custom Foundry model is retrained (a Layer 2 activity), the retraining can incorporate the declarative customizations as training signal — the instruction files document exactly what the practice expects. This creates a positive feedback loop: instruction files improve model behavior immediately via context injection; model retraining incorporates instruction file patterns for deeper behavioral alignment.

**Weaknesses:**

- **Requires initial investment in governance structure.** Defining the Trusted Committer model, establishing PR review conventions for instruction files, and documenting the contribution workflow require effort upfront.
- **Assumes a declarative customization platform exists.** This model depends on GitHub Copilot's instruction file architecture (or an equivalent system). If the selected platform does not support composable declarative customization, Option G cannot function.
- **Does not eliminate the need for ML expertise.** Model retraining, fine-tuning, and evaluation still require specialized skills. Option G does not solve this — it delegates it to the appropriate team (Layer 2) while ensuring the architecture practice controls the behavioral layer (Layer 1).

**Industry precedent:**

This model draws from three established practices:

1. **InnerSource Trusted Committer pattern** (InnerSource Commons): Practitioners who demonstrate consistent contribution quality are granted merge authority, formalizing their role in community governance. Applied to AI customization, this means senior architects who contribute the most effective instruction files become the reviewers and approvers for the customization layer.

2. **Infrastructure as Code (IaC) governance** (DevOps): Infrastructure teams provide the platform; application teams define their infrastructure declaratively in version-controlled files (Terraform, Bicep, CloudFormation). Applied to AI customization, the platform team provides the AI platform; the architecture practice defines its behavioral customization declaratively in version-controlled instruction files.

3. **Community of Practice model** (Wenger, 1998): Knowledge management through a community of practitioners who share a domain, a practice, and a set of shared resources. AI customization files become the shared resource that the community maintains together.

## Suggested Direction: Option G (Hybrid Inner Source Model)

Based on the pilot experience and industry patterns reviewed, **the analysis points toward Option G** as the approach most likely to address the organizational design problem that Options E and F each leave partially unresolved. The team presenting this evaluation recognizes that decision-makers may weigh additional factors — organizational constraints, existing team structures, strategic priorities — that this analysis does not fully account for.

### Considerations Against Option E (Dedicated Customization Team)

Option E creates an organizational boundary between domain experts and the customization mechanism. This boundary is the root cause of:

- Knowledge decay (the team that maintains customizations does not practice the domain)
- Change velocity mismatch (retraining cycles vs. daily practice evolution)
- Innovation bottleneck (every customization idea requires a ticket)
- Institutional knowledge fragmentation (practice conventions and AI behavior are maintained separately)

These appear to be structural properties of the organizational design rather than risks that can be mitigated through process improvement alone.

The strongest version of this argument comes from the pilot evidence itself: the NovaTrek `copilot-instructions.md` was updated dozens of times during the evaluation. If each update had required a ticket to a separate team, the pilot would have produced significantly fewer than 4 solution designs, 14 ADRs, and 139 diagrams — because the architect would have been blocked waiting for customization updates instead of producing architectural output.

### Considerations Against Option F (Practice Owns Everything)

Option F correctly places behavioral customization in the hands of domain experts but ignores the reality that some AI capabilities require specialized skills the architecture practice does not have:

- Fine-tuning a model requires ML engineering expertise
- Managing BYOK endpoint registration requires enterprise admin access
- Cost optimization across models requires usage analytics infrastructure
- Compliance and audit controls require enterprise security integration

Option F works well for the declarative customization layer. However, it may not scale to the full AI stack without specialized support.

### Why the Analysis Points Toward Option G

Option G attempts to resolve the tension by establishing a clear separation of concerns:

| Layer | Owner | Artifacts | Governance |
|-------|-------|-----------|------------|
| **Behavioral customization** | Architecture practice | Instruction files, custom agents, skills, scoped rules | PR review by architect Trusted Committers |
| **Model infrastructure** | Platform/ML team | Foundry deployment, BYOK registration, API keys | Standard enterprise change management |
| **Cross-cutting** | Shared | Cost monitoring, compliance, usage analytics | Joint review cadence |

The behavioral customization layer — where domain knowledge matters most and where change velocity matters most — is fully controlled by the architecture practice. The infrastructure layer — where ML and platform engineering expertise matters most — is controlled by the team with those skills. Neither team blocks the other.

### Supporting Evidence

This suggested direction is supported by three lines of evidence:

**1. Empirical evidence from the pilot.** The NovaTrek pilot demonstrates that architect-maintained declarative customizations produce high-quality output. 4 solution designs, 14 ADRs, 139 diagrams, and a live documentation portal were produced under a customization layer that the practicing architect maintained directly. No separate customization team was involved. The customization layer grew organically from ~200 lines to 1,172 lines, with every addition responding to a real gap discovered in daily work.

**2. Alignment with industry-validated patterns.** Option G draws from InnerSource (Trusted Committer model for distributed contribution governance), Infrastructure as Code (declarative configuration with version control), and Community of Practice (knowledge management through practitioner community). Each of these patterns has been validated at enterprise scale across hundreds of organizations documented by the InnerSource Commons, the DevOps Research and Assessment (DORA) program, and Wenger's community of practice research.

**3. Structural analysis of the organizational design problem.** Conway's Law suggests that placing behavioral customization ownership with the architecture practice would align the customization system with the practice's communication structure and workflow cadence. Other ownership models risk creating an organizational boundary that could degrade change velocity, fragment institutional knowledge, and bottleneck innovation.

### Implementation Prerequisites

Option G would require that the selected AI platform support composable declarative customization. For reference, here is how GitHub Copilot (Option D) maps to these requirements:

| Requirement | GitHub Copilot (Option D) |
|-------------|--------------------------|
| Repository-wide instruction files | Supported (`copilot-instructions.md`) |
| Path-scoped instruction files | Supported (`.instructions.md` with `applyTo` globs) |
| Custom agent definitions | Supported (`.github/agents/*.md`, `AGENTS.md`) |
| Skills | Supported (`SKILL.md`) |
| Version control | Git-native — all configuration is Markdown in the repository |
| PR review workflow | Standard GitHub PR review — diffs, comments, approvals |
| Composability | Global + scoped + agent-specific instructions compose automatically |
| Automatic distribution | Clone the repository = inherit all customizations |

Option D (Copilot + BYOK) satisfies every prerequisite. Option G is designed to operate on top of Option D as the governance and ownership model for the customization layer.

## Suggested Governance Roadmap

Building on the governance roadmap established in DD-05, the following phases illustrate how Option G could be deployed incrementally:

| Phase | Milestone | Activities | Success Criteria |
|-------|-----------|------------|-----------------|
| **Phase 0 (Current)** | Pilot validated | Single architect manages full customization layer. Instruction files, custom agent, and scoped rules are in production use. | COMPLETE — demonstrated in evaluation |
| **Phase 1** | Team onboarding | Additional architects clone the repository and inherit customizations. First external PRs to instruction files submitted and reviewed. | At least 2 architects contributing customization changes via PR |
| **Phase 2** | Trusted Committers established | Architects who demonstrate consistent contribution quality are granted merge authority for customization files. Contribution guide documented. | At least 1 Trusted Committer beyond the original pilot architect |
| **Phase 3** | Domain decomposition | Global instructions decomposed into domain-scoped files. Teams develop domain-specific agents and skills. Composition model tested at scale. | Instruction file total size distributed across 10+ scoped files |
| **Phase 4** | Cross-model validation | Customizations tested across built-in models and custom BYOK model. Model-specific instruction files created where behavioral differences require it. | Output quality parity for common tasks across at least 2 models |
| **Phase 5** | Enterprise governance | Cost monitoring, usage analytics, compliance controls integrated. Customization quality metrics established. | Quarterly governance review cadence in place |

## Relationship to Other Decision Pages

| Decision Page | Relationship |
|---------------|-------------|
| [DD-05: Model Selection Autonomy](../decisions/dd-05-model-selection-autonomy.md) | DD-05 establishes guided freedom for model selection and introduces the declarative customization taxonomy. This page extends DD-05's governance roadmap with the inner source ownership model. |
| [DD-06: IDE Client Selection](../decisions/dd-06-ide-client-selection.md) | DD-06 identifies the Frozen Customization Problem and the customization ownership question. This page explores a potential answer: the hybrid inner source model (Option G) that would keep behavioral customization in practitioner hands. |
| [Option D — Hybrid Architecture](option-d-hybrid-architecture.md) | Option D defines the deployment topology (Copilot + BYOK). This page explores a complementary governance topology (inner source + Trusted Committers). Together, they would describe the complete model: what platform, what models, who customizes, and how changes flow. |
| [Copilot Rollout Roadmap](../framework/copilot-rollout-roadmap.md) | The rollout roadmap defines Phase 3 (customization setup) and Phase 4 (scaling). This page suggests a governance framework for how customizations could be managed at each phase. |
| [Build vs Leverage](build-vs-leverage.md) | Build vs Leverage argues against building custom infrastructure when native capabilities exist. This page extends the argument: even the governance model could leverage existing engineering workflows (Git, PRs, code review) rather than building bespoke customization management processes. |
