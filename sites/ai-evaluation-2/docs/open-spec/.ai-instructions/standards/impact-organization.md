# Impact Organization Standards

**Applicable Modes**: Solution Architect, Orchestrator

## Overview

The Two-Tier Impact Organization framework provides a structured approach to categorizing and managing changes based on their complexity and scope. This ensures appropriate levels of design, review, and governance are applied to each initiative.

## Two-Tier Classification

### Tier 1: Simple Impact
**Definition**: Localized changes with minimal cross-system impact
**Characteristics**:
- Single system or component
- Well-understood patterns
- Limited dependencies
- Low risk profile
- Standard implementation approach

**Examples**:
- Adding a new field to an API
- Updating validation rules
- Minor UI enhancements
- Configuration changes
- Bug fixes

### Tier 2: Complex Impact
**Definition**: Multi-system changes requiring coordination and design
**Characteristics**:
- Multiple systems affected
- New patterns or technologies
- Significant dependencies
- Higher risk profile
- Requires architectural review

**Examples**:
- New microservice introduction
- Cross-system integration
- Data model restructuring
- Security framework changes
- Performance optimization initiatives

## Component Resource Hierarchy

### Core Principle: One Impact Per Resource

Each resource (component, service, system) should have a single, well-defined impact in any given change. This ensures:
- Clear ownership and accountability
- Predictable change scope
- Manageable testing requirements
- Reduced risk of cascading failures

### Resource Impact Mapping

```yaml
Change Request: Add Real-time Notifications
Resources and Impacts:
  NotificationService:
    Impact: Primary - New service creation
    Responsibility: Handle notification logic
    
  UserService:
    Impact: Secondary - Add notification preferences
    Responsibility: Store user settings
    
  APIGateway:
    Impact: Tertiary - Route notification endpoints
    Responsibility: Handle new routes
    
  Database:
    Impact: Secondary - New notification tables
    Responsibility: Store notification data
```

## Impact Assessment Process

### Step 1: Initial Classification
```markdown
## Impact Assessment Checklist

### System Scope
- [ ] Single system only → Tier 1
- [ ] 2-3 systems → Consider complexity
- [ ] 4+ systems → Tier 2

### Technical Complexity
- [ ] Using existing patterns → Tier 1
- [ ] Minor pattern variations → Consider scope
- [ ] New patterns required → Tier 2

### Risk Assessment
- [ ] Low risk, well-understood → Tier 1
- [ ] Medium risk, some unknowns → Consider scope
- [ ] High risk, many unknowns → Tier 2

### Complexity Footprint
- [ ] 1-2 changes, all LOW → Likely Tier 1
- [ ] 3-5 changes, mixed LOW/MEDIUM → Consider scope
- [ ] 5+ changes or any HIGH → Tier 2
```", "oldString": "### Timeline Impact\n- [ ] < 1 sprint → Likely Tier 1\n- [ ] 1-2 sprints → Consider complexity\n- [ ] > 2 sprints → Tier 2\n```

### Step 2: Resource Impact Analysis

For each affected resource, document:

1. **Impact Type**
   - Primary: Core changes required
   - Secondary: Supporting changes needed
   - Tertiary: Minor adjustments only

2. **Change Scope**
   - Code changes required
   - Configuration updates
   - Schema modifications
   - API contract changes

3. **Dependencies**
   - Upstream dependencies
   - Downstream impacts
   - Parallel work required

### Step 3: Tier Assignment

Based on the analysis, assign the appropriate tier:

```markdown
## Tier Assignment Matrix

| Criteria | Tier 1 | Tier 2 |
|----------|--------|--------|
| Systems Affected | 1-2 | 3+ |
| New Patterns | No | Yes |
| Architecture Review | Optional | Required |
| Risk Level | Low | Medium-High |
| Documentation | Light | Comprehensive |
| Governance | Standard | Enhanced |
```

## Documentation Requirements by Tier

### Tier 1 Documentation
```markdown
# Quick Impact Assessment

## Change Summary
[Brief description - 2-3 sentences]

## Affected Components
- Component A: [specific change]
- Component B: [specific change]

## Implementation Approach
[Brief technical approach]

## Testing Requirements
- Unit tests for modified code
- Integration tests for touchpoints
- Regression tests for affected flows

## Rollback Plan
[Simple rollback steps]
```

### Tier 2 Documentation
```markdown
# Comprehensive Impact Assessment

## Executive Summary
[Detailed overview of the change and its business value]

## Current State Analysis
### System Architecture
[Current system diagram and description]

### Identified Gaps
[What's missing or needs improvement]

## Proposed Changes
### Architecture Design
[New architecture diagram with changes highlighted]

### Component Impact Analysis
For each component:
- Current responsibility
- Required changes
- New responsibility
- Integration modifications

## Risk Assessment
### Technical Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | Medium | High | [Mitigation steps] |

### Business Risks
[Business continuity, user impact, revenue impact]

## Implementation Plan
### Phase 1: Foundation
- Tasks and timeline
- Resource requirements
- Success criteria

### Phase 2: Integration
- Tasks and timeline
- Resource requirements
- Success criteria

## Governance Requirements
- Architecture review board approval
- Security review
- Performance benchmarks
- Stakeholder sign-offs
```

## Governance by Tier

### Tier 1 Governance
- **Approval**: Team lead or senior developer
- **Review**: Standard code review process
- **Documentation**: Update relevant wikis
- **Communication**: Team notification

### Tier 2 Governance
- **Approval**: Architecture review board
- **Review**: Formal design review
- **Documentation**: Complete design documents
- **Communication**: Stakeholder briefings

## Impact Organization Patterns

### Pattern 1: Isolated Impact
```
Service A → Service A'
         ↓
    Database A → Database A'
```
**Characteristics**: Changes contained within service boundary
**Tier**: Usually Tier 1

### Pattern 2: Cascading Impact
```
Service A → Service A'
    ↓           ↓
Service B → Service B'
    ↓           ↓
Service C → Service C'
```
**Characteristics**: Changes flow through multiple services
**Tier**: Usually Tier 2

### Pattern 3: Hub Impact
```
        Service B
            ↓
Service A → Hub → Service A'
            ↓
        Service C
```
**Characteristics**: Central component affects multiple services
**Tier**: Always Tier 2

### Pattern 4: Mesh Impact
```
Service A ↔ Service B
    ↓   ×   ↓
Service C ↔ Service D
```
**Characteristics**: Multiple interconnected changes
**Tier**: Always Tier 2

## Best Practices

### Do's ✅
1. **Assess Early**: Determine tier during planning
2. **Document Impacts**: Clear documentation for each affected resource
3. **Limit Scope**: One primary impact per resource
4. **Plan Phases**: Break Tier 2 into manageable phases
5. **Communicate**: Keep stakeholders informed based on tier

### Don'ts ❌
1. **Underestimate**: Don't force Tier 2 work into Tier 1
2. **Over-engineer**: Don't apply Tier 2 process to simple changes
3. **Skip Assessment**: Always document impact analysis
4. **Ignore Dependencies**: Consider all downstream effects
5. **Rush Classification**: Take time to properly assess

## Metrics and Monitoring

### Tier Distribution Targets
```yaml
Healthy Portfolio:
  Tier 1: 70-80%  # Most work should be simple
  Tier 2: 20-30%  # Strategic initiatives
  
Warning Signs:
  Tier 1 < 60%    # Too much complexity
  Tier 2 > 40%    # Possible over-engineering
```

### Impact Realization Tracking
```markdown
## Post-Implementation Review

### Predicted vs Actual
- Predicted Tier: [1 or 2]
- Actual Complexity: [Simple/Complex]
- Predicted Timeline: [X sprints]
- Actual Timeline: [Y sprints]

### Lessons Learned
- What went well
- What was underestimated
- Improvement recommendations
```

## Examples

### Example 1: API Field Addition (Tier 1)
```yaml
Change: Add "preferred_language" field to user profile
Impact:
  UserService:
    - Add field to data model
    - Update validation logic
  UserAPI:
    - Add field to response DTOs
    - Update OpenAPI spec
  Database:
    - Add column with default value
    
Classification: Tier 1
Rationale: Simple, well-understood change pattern
```

### Example 2: Authentication System Upgrade (Tier 2)
```yaml
Change: Migrate from session-based to JWT authentication
Impact:
  AuthService:
    - Complete authentication logic rewrite
    - New token generation/validation
  All Services:
    - Update authentication middleware
    - Modify authorization checks
  API Gateway:
    - New routing rules
    - Token validation layer
  Database:
    - Remove session tables
    - Add token blacklist
    
Classification: Tier 2
Rationale: Fundamental pattern change affecting all services
```

## Integration with Other Frameworks

### With Ticket Classification
- Level 1-2 tickets → Usually Tier 1
- Level 3-5 tickets → Usually Tier 2

### With Architecture Backlog
- Tier 1 items → Tactical backlog
- Tier 2 items → Strategic initiatives

### With 4-Phase Investigation
- Tier 1 → Compressed investigation
- Tier 2 → Full 4-phase process

---

The Two-Tier Impact Organization ensures that we apply the right level of rigor to each change, avoiding both under-engineering critical changes and over-engineering simple ones.