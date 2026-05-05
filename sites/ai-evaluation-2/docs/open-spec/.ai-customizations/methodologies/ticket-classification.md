# Ticket Classification Framework

**Applicable Modes**: Solution Architect, Orchestrator

## Overview

The Ticket Classification Framework provides a systematic approach to categorizing work requests based on complexity, impact, and effort. This ensures appropriate resource allocation and sets realistic expectations.

## Classification Levels

### Level 1: Simple Request
**Characteristics**:
- Single component or service
- Well-defined requirements
- Minimal dependencies
- Standard patterns apply
- Low risk

**Typical Effort**: 1-3 days
**Complexity**: Low
**Example**: Add a new field to an existing API endpoint

### Level 2: Moderate Enhancement
**Characteristics**:
- Multiple components affected
- Some integration required
- Moderate dependencies
- May need minor design decisions
- Medium risk

**Typical Effort**: 3-10 days (0.5-1 sprint)
**Complexity**: Medium
**Example**: Implement a new authentication method for existing service

### Level 3: Complex Feature
**Characteristics**:
- Cross-system impact
- Significant integration work
- Multiple dependencies
- Requires architecture decisions
- Higher risk

**Typical Effort**: 2-4 sprints
**Complexity**: High
**Example**: Add real-time synchronization between multiple services

### Level 4: Major Initiative
**Characteristics**:
- Enterprise-wide impact
- New architectural patterns
- Extensive dependencies
- Strategic decision required
- Very high risk

**Typical Effort**: 2-6 months
**Complexity**: Very High
**Example**: Migrate from monolith to microservices architecture

### Level 5: Transformation Program
**Characteristics**:
- Business transformation
- Multiple major initiatives
- Organizational change required
- Long-term strategic impact
- Extreme complexity and risk

**Typical Effort**: 6+ months
**Complexity**: Extreme
**Example**: Complete digital transformation of legacy systems

## Classification Process

### Step 1: Initial Assessment
Evaluate the request against these criteria:

1. **Scope Analysis**
   - Number of systems affected
   - Number of teams involved
   - Geographic distribution
   - User base impact

2. **Technical Complexity**
   - New vs. existing patterns
   - Integration requirements
   - Performance requirements
   - Security implications

3. **Business Impact**
   - Revenue impact
   - Customer experience impact
   - Regulatory compliance
   - Strategic alignment

### Step 2: Dependency Mapping
Identify and categorize dependencies:

- **Technical Dependencies**
  - Systems and services
  - Libraries and frameworks
  - Infrastructure components
  - External APIs

- **Organizational Dependencies**
  - Team availability
  - Skill requirements
  - Approval processes
  - Change windows

### Step 3: Risk Assessment
Evaluate risks across dimensions:

| Risk Category | Level 1 | Level 2 | Level 3 | Level 4 | Level 5 |
|--------------|---------|---------|---------|---------|---------|
| Technical | Low | Low-Med | Medium | High | Very High |
| Schedule | Minimal | Low | Medium | High | Very High |
| Resource | Minimal | Low | Medium | High | Extreme |
| Business | Minimal | Low | Medium | High | Extreme |

### Step 4: Final Classification
Based on the assessment, assign the appropriate level and document:
- Classification level (1-5)
- Primary complexity drivers
- Key risks identified
- Recommended approach

## Two-Tier Impact Organization

### Tier 1: Simple Impact (Levels 1-2)
**Approach**: Direct implementation
- Minimal design documentation
- Standard patterns and practices
- Quick iteration cycles
- Lightweight approval process

**Documentation Required**:
- Brief technical specification
- Test cases
- Basic deployment guide

### Tier 2: Complex Impact (Levels 3-5)
**Approach**: Phased implementation with governance
- Comprehensive design documentation
- Architecture review required
- Formal project planning
- Structured approval gates

**Documentation Required**:
- Detailed architecture design
- Risk mitigation plan
- Phased implementation roadmap
- Comprehensive test strategy
- Operational runbook

## Classification Quick Reference

### Questions for Rapid Classification

1. **How many systems are affected?**
   - 1 system → Consider Level 1-2
   - 2-3 systems → Consider Level 2-3
   - 4+ systems → Consider Level 3-5

2. **What's the implementation timeframe?**
   - < 1 week → Level 1-2
   - 1-4 weeks → Level 2-3
   - 1-3 months → Level 3-4
   - 3+ months → Level 4-5

3. **What's the business impact?**
   - Minimal → Level 1-2
   - Departmental → Level 2-3
   - Business unit → Level 3-4
   - Enterprise → Level 4-5

4. **Are new patterns/technologies required?**
   - No → Level 1-2
   - Minor → Level 2-3
   - Significant → Level 3-4
   - Fundamental → Level 4-5

## Escalation Triggers

Automatically escalate classification if:
- Security vulnerabilities discovered → +1 level
- Regulatory compliance required → +1 level
- Customer data involved → +1 level
- Revenue impact > $100k → +1 level
- Downtime required → +1 level

## De-escalation Opportunities

Consider reducing classification if:
- Existing patterns can be reused
- Proven solutions available
- Limited to single team
- Low user impact
- Flexible timeline

## Documentation Templates by Level

### Level 1 Documentation
```markdown
# Quick Change Request

## Summary
[Brief description]

## Technical Approach
[2-3 sentences]

## Testing
[Basic test scenarios]

## Deployment
[Simple steps]
```

### Level 3+ Documentation
```markdown
# Architecture Design Document

## Executive Summary
## Current State Analysis
## Proposed Architecture
## Security Considerations
## Risk Assessment
## Implementation Roadmap
## Success Criteria
```

## Integration with Other Frameworks

### With 4-Phase Investigation
- Level 1-2: Compressed investigation (1-2 days)
- Level 3: Standard investigation (1 week)
- Level 4-5: Comprehensive investigation (2-4 weeks)

### With Architecture Backlog
- Level 1-2: Tactical backlog items
- Level 3: Feature backlog items
- Level 4-5: Strategic initiatives

## Common Misclassifications

### Under-classification Signs
- Continuous scope creep
- Unexpected dependencies
- Timeline overruns
- Quality issues

### Over-classification Signs
- Excessive documentation
- Analysis paralysis
- Unnecessary approvals
- Resource waste

## Best Practices

1. **Classify Early** - Within first day of request
2. **Document Rationale** - Explain classification decision
3. **Review Regularly** - Adjust as understanding improves
4. **Communicate Clearly** - Ensure stakeholder alignment
5. **Learn from History** - Track actual vs. estimated

---

The Ticket Classification Framework ensures appropriate effort and attention is applied to each request, preventing both under-engineering simple solutions and over-engineering complex ones.