# [Solution Name] v1.0

| | |
|-----------|-------|
| **Solution Architect** | [Architect Name] |
| **Solution Name** | [Descriptive Solution Name] |
| **Ticket** | [TICKET-ID] |
| **Capabilities** | CAP-X.Y (extends), CAP-X.Y (modifies) |
| **Status** | DRAFT / IN REVIEW / APPROVED / IMPLEMENTED / SUPERSEDED |
| **Impacted Services** | [svc-xxx, svc-yyy] |
| **Related ADRs** | ADR-NNN, ADR-NNN |
| **Supersedes** | [TICKET-ID] (if this replaces a prior solution) |

## Overview

[1-2 paragraph executive summary of the solution]

**Problem Statement**: [Clear description of the business problem being solved]

**Solution Overview**: [High-level description of the proposed solution approach]

## Component Architecture

**Component Diagram**:

![Component Architecture](3.solution/00.component.diagram.svg)

**Figure 1**: [Brief description of the component diagram - what it shows and key integration points]. *Source: `architecture/solutions/_TICKET-ID-slug/3.solution/00.component.diagram.puml`*

**Affected Components Table**:

| Component | Change Type | Change Area | Endpoint | Description |
|-----------|-------------|-------------|----------|-------------|
| **[component-1]** | Modify | [Area being modified] | `[endpoint-path]` | [Description of changes] |
| **[component-2]** | Modify | [Area being modified] | `[endpoint-path]` | [Description of changes] |
| **[component-3]** | Existing | N/A | `[endpoint-path]` | [Why no changes needed] |

---

### [Component-1 Name] Modifications

**Component**: [component-1]  
**Change Type**: Modify  
**Priority**: [CRITICAL | HIGH | MEDIUM | LOW]  
**Endpoints Modified**: [list endpoints]  
**Status**: [Defined | In Progress | Implemented | Validated]

#### Current State

[Brief description of current behavior without detailed steps]

**Problem**: [Clear problem statement]

#### Modifications Required

The endpoint logic adds [brief description of what's being added/modified]:

1. **[Change Category 1]**: [High-level description]
2. **[Change Category 2]**: [High-level description]
3. **[Change Category 3]**: [High-level description]

#### Sequence Diagrams

**[Workflow Name]**:

![Workflow Diagram](3.solution/01b.[component].[workflow].sequence.diagram.target.svg)

**Figure 1**: [Caption describing workflow]. Light green groups indicate changes. *Source: `architecture/solutions/_TICKET-ID-slug/3.solution/i.impacts/impact.N/[sequence].puml`*

**Sequence Diagram Summary**:

[Brief paragraph explaining what the sequence diagram shows - describe the workflow from user perspective, not implementation steps]

---

### [Component-2 Name] Modifications

**Component**: [component-2]  
**Change Type**: Modify  
**Priority**: [CRITICAL | HIGH | MEDIUM | LOW]  
**Endpoints Modified**: [list endpoints]  
**Status**: [Defined | In Progress | Implemented | Validated]

#### Current State

[Brief description of current behavior]

**Problem**: [Clear problem statement]

#### Modifications Required

1. **[Change Category 1]**: [High-level description]
2. **[Change Category 2]**: [High-level description]
3. **[Change Category 3]**: [High-level description]

**Configuration**: [Any configuration requirements]

**Implementation Guidance**: See [Guidance N - Topic](3.solution/g.guidance/guidance.N/guidance.N.md) *(if applicable)*

#### Sequence Diagrams

**[Workflow Name]**:

![Workflow Diagram](3.solution/02b.[component].[workflow].sequence.diagram.target.svg)

**Figure 2**: [Caption describing workflow]. Light green groups indicate changes.

**Sequence Diagram Summary**:

[Brief paragraph explaining what the sequence diagram shows]

---

### [Component-3 Name] (Existing - No Changes)

**Component**: [component-3]  
**Change Type**: Existing  
**Role**: [How this component is used in the solution without modification]

---

## Assumptions

Assumptions capture conditions that are accepted as true for the solution design to proceed but require validation. Each assumption states WHAT is being assumed (the premise) and WHY the assumption is reasonable (the rationale), without prescribing HOW to implement. Assumptions marked PROPOSED require stakeholder confirmation or technical validation before implementation begins.

| Assumption # | Assumption Name | Description | Status | Priority |
|--------------|----------------|-------------|--------|----------|
| Assumption 1 | [Short descriptive name] | [Brief 1-2 sentence explanation] | [VALIDATED\|PROPOSED] | [CRITICAL\|HIGH\|MEDIUM\|LOW] |
| Assumption 2 | [Short descriptive name] | [Brief explanation] | [Status with checkmark] | [Priority] |
| Assumption N | [Short descriptive name] | [Brief explanation] | [Status with checkmark] | [Priority] |

## Architecture Decisions

Architecture decisions document key decision points where multiple options were considered. Each decision captures the question being decided, the options evaluated, the recommended or approved option, and the rationale (WHY) behind the selection -- including business justification, architectural fit, and tradeoffs considered. Decisions describe WHAT was decided, not HOW to implement it.

| Decision # | Decision Name | Description | Status | Recommended Option |
|------------|---------------|-------------|--------|-------------------|
| Decision 1 | [Short descriptive name] | [Brief 1-2 sentence explanation of decision question] | [APPROVED\|RECOMMENDATION MADE\|UNDER ANALYSIS] | [Option name] |
| Decision 2 | [Short descriptive name] | [Brief explanation] | [Status with checkmark] | [Option name] |
| Decision N | [Short descriptive name] | [Brief explanation] | [Status with checkmark] | [Option name] |

## Risks

Risks identify what could go wrong with the solution and how each risk is addressed. Each risk states WHAT the concern is (the risk statement) and WHY it is mitigated or accepted (the rationale), along with any residual risk that remains. Risks do not include implementation-level mitigation details -- those belong in guidance documents.

| Risk # | Risk Name | Description | Risk Level | Status |
|--------|-----------|-------------|------------|--------|
| Risk 1 | [Short descriptive name] | [Brief 1-2 sentence explanation] | [VERY LOW\|LOW\|MEDIUM\|HIGH\|CRITICAL] | [FULLY MITIGATED\|ACCEPTED\|MONITORING] |
| Risk 2 | [Short descriptive name] | [Brief explanation] | [Risk level] | [Status with checkmark] |
| Risk N | [Short descriptive name] | [Brief explanation] | [Risk level] | [Status with checkmark] |

## Functional and Non-Functional Requirements *(Optional - only if requirements exist)*
Requirements capture explicit functional behaviors and non-functional quality attributes that the solution must satisfy beyond what is documented in JIRA tickets. Functional requirements define WHAT the system must do (e.g., enforce a validation rule, return specific error codes), while non-functional requirements define quality constraints such as performance, scalability, or compliance. Only include this section when requirements have been formally identified and documented.
| Requirement ID | Type | Requirement Name | Description | Priority | Status |
|----------------|------|------------------|-------------|----------|--------|
| NFR-1 | Non-Functional | [Short descriptive name] | [Brief 1-2 sentence explanation] | [CRITICAL\|HIGH\|MEDIUM\|LOW] | [Defined\|In Progress\|Implemented\|Validated] |
| FR-1 | Functional | [Short descriptive name] | [Brief explanation] | [Priority] | [Status with checkmark] |
| FR-N | Functional | [Short descriptive name] | [Brief explanation] | [Priority] | [Status with checkmark] |

**NOTE**: Only include this section if requirements documents exist. See [Optional Sections Standard](/.ai-instructions/customizations/solution-design-optional-sections-standard.md).

## Implementation Guidance *(Optional - only if guidance exists)*

Guidance provides optional, advisory-only HOW recommendations prepared by the solution architect to help development teams with implementation. This is the one section that intentionally crosses the WHAT/WHY boundary into implementation detail -- including code examples, configuration patterns, testing approaches, and data structure specifications. Guidance is supplementary and does not constrain development teams; they may adopt, adapt, or disregard these recommendations.

For solutions that touch service logic, include a test plan at `3.solution/g.guidance/test-plan.md` covering:

- Which test layers are affected (unit, integration, contract, acceptance)
- New test scenarios required (unit and integration)
- BDD scenarios derived from user story acceptance criteria (Gherkin format, where applicable)
- Contract test additions for any new cross-service integrations documented in `cross-service-calls.yaml`
- Existing tests that need updating due to changed behavior

Coverage thresholds and tooling are defined in `config/test-standards.yaml` (ADR-012).

**NOTE**: Only include this section if guidance documents exist. See [Optional Sections Standard](/.ai-instructions/customizations/solution-design-optional-sections-standard.md).

## Security Considerations *(Optional - only if security concerns exist)*

Security considerations address solution-specific concerns around authentication, authorization, data protection, PCI compliance, secrets management, or other security controls. Only include this section when the solution explicitly introduces or modifies security-relevant behavior -- such as new authentication mechanisms, payment processing, credential handling, or changes to data access patterns. Do not include as boilerplate for solutions with no security implications.

[Security analysis specific to this solution]

**NOTE**: Only include this section if solution has specific security concerns. See [Optional Sections Standard](/.ai-instructions/customizations/solution-design-optional-sections-standard.md).

---
