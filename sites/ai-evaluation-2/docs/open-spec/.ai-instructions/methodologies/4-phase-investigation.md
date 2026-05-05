# 4-Phase Investigation Process

**Applicable Modes**: Solution Architect, Orchestrator, Ask

## Overview

The 4-Phase Investigation Process is a systematic approach to understanding complex problems, systems, or requirements. This methodology ensures thorough analysis and defensible recommendations.

## The Four Phases

### Phase 1: Discovery and Context Gathering
**Objective**: Understand the current state and establish context

#### Activities
1. **Identify Stakeholders**
   - Primary users/consumers
   - Technical teams
   - Business owners
   - External dependencies

2. **Document Current State**
   - Existing systems and components
   - Current workflows and processes
   - Known pain points
   - Technical debt inventory

3. **Gather Requirements**
   - Functional requirements
   - Non-functional requirements (NFRs)
   - Constraints and limitations
   - Success criteria

4. **Define Scope**
   - In-scope elements
   - Out-of-scope elements
   - Assumptions
   - Dependencies

#### Deliverables
- Stakeholder map
- Current state documentation
- Requirements matrix
- Scope definition document

### Phase 2: Analysis and Assessment
**Objective**: Analyze findings and identify gaps, risks, and opportunities

#### Activities
1. **Gap Analysis**
   - Current vs. desired state
   - Missing capabilities
   - Technical gaps
   - Process gaps

2. **Risk Assessment**
   - Technical risks
   - Business risks
   - Security risks
   - Operational risks

3. **Dependency Mapping**
   - System dependencies
   - Data dependencies
   - Team dependencies
   - External dependencies

4. **Constraint Analysis**
   - Technical constraints
   - Resource constraints
   - Time constraints
   - Regulatory constraints

#### Deliverables
- Gap analysis report
- Risk register with mitigation strategies
- Dependency diagram
- Constraints documentation

### Phase 3: Solution Design
**Objective**: Design solutions that address identified needs while managing constraints

#### Activities
1. **Alternative Analysis**
   - Identify multiple solution approaches
   - Evaluate pros and cons
   - Consider build vs. buy vs. hybrid
   - Assess feasibility

2. **Architecture Design**
   - High-level architecture
   - Component design
   - Integration patterns
   - Data flow design

3. **Security Design**
   - Security controls
   - Authentication/authorization approach
   - Data protection measures
   - Compliance requirements

4. **Operational Design**
   - Deployment approach
   - Monitoring strategy
   - Support model
   - Disaster recovery

#### Deliverables
- Solution alternatives matrix
- Architecture diagrams (PlantUML)
- Security design document
- Operational runbook outline

### Phase 4: Recommendation and Roadmap
**Objective**: Provide clear recommendations with implementation roadmap

#### Activities
1. **Solution Recommendation**
   - Recommended approach with rationale
   - Trade-off analysis
   - Risk mitigation plan
   - Success metrics

2. **Implementation Roadmap**
   - Phased approach
   - Timeline with milestones
   - Resource requirements
   - Dependencies and prerequisites

3. **Effort Estimation**
   - Component/endpoint complexity table
   - Per-item complexity assessment (LOW/MEDIUM/HIGH)
   - Team composition needs
   - Parallel work streams

4. **Success Planning**
   - Definition of done
   - Acceptance criteria
   - Validation approach
   - Transition planning

#### Deliverables
- Executive recommendation summary
- Detailed implementation roadmap
- Effort estimation breakdown
- Success criteria documentation

## Phase Execution Guidelines

### Time Allocation (Typical)
- Phase 1: 30% of total investigation time
- Phase 2: 25% of total investigation time
- Phase 3: 30% of total investigation time
- Phase 4: 15% of total investigation time

### Key Principles
1. **No Skipping Phases** - Each phase builds on the previous
2. **Document Everything** - Maintain audit trail
3. **Validate Assumptions** - Test and confirm
4. **Iterate When Needed** - Phases can inform earlier phases
5. **Stakeholder Checkpoints** - Validate findings at each phase

## Application by Mode

### Solution Architect Mode
- Full application of all 4 phases
- Emphasis on technical depth
- Detailed architecture artifacts
- Comprehensive documentation

### Orchestrator Mode
- Uses 4-phase for complex multi-mode tasks
- May delegate phase activities to other modes
- Focuses on coordination and integration
- Ensures phase transitions

### Ask Mode
- Applies framework for complex explanations
- May compress phases for simpler queries
- Uses phase structure to organize responses
- Ensures comprehensive coverage

## Common Pitfalls to Avoid

1. **Rushing Discovery** - Incomplete understanding leads to poor solutions
2. **Analysis Paralysis** - Balance thoroughness with progress
3. **Single Solution Fixation** - Always consider alternatives
4. **Ignoring Constraints** - Constraints shape viable solutions
5. **Weak Recommendations** - Be specific and actionable

## Templates and Tools

### Phase 1 Checklist
- [ ] Stakeholders identified and documented
- [ ] Current state fully mapped
- [ ] Requirements gathered and validated
- [ ] Scope clearly defined with boundaries

### Phase 2 Checklist
- [ ] All gaps identified and categorized
- [ ] Risks assessed with mitigation strategies
- [ ] Dependencies mapped and validated
- [ ] Constraints documented and confirmed

### Phase 3 Checklist
- [ ] Multiple alternatives evaluated
- [ ] Architecture designed and documented
- [ ] Security controls defined
- [ ] Operational aspects planned

### Phase 4 Checklist
- [ ] Clear recommendation with rationale
- [ ] Realistic roadmap created
- [ ] Effort estimated in sprints
- [ ] Success criteria defined

## Integration with Other Methodologies

### With BDD/TDD (When applicable)
- Phase 1: Gather scenarios for BDD
- Phase 2: Identify test requirements
- Phase 3: Design testable components
- Phase 4: Include testing in roadmap

### With Ticket Classification
- Phase 1: Classify initial request
- Phase 2: Refine classification based on findings
- Phase 3: Design per classification level
- Phase 4: Adjust roadmap for classification

## Reporting Format

### Executive Summary Structure
1. **Situation** - Brief context
2. **Findings** - Key discoveries
3. **Recommendation** - Clear direction
4. **Next Steps** - Immediate actions

### Detailed Report Structure
1. **Executive Summary**
2. **Phase 1 Findings**
3. **Phase 2 Analysis**
4. **Phase 3 Design Options**
5. **Phase 4 Recommendations**
6. **Appendices**

---

The 4-Phase Investigation Process ensures systematic, thorough analysis leading to defensible recommendations. Apply this methodology whenever facing complex problems or designing significant solutions.