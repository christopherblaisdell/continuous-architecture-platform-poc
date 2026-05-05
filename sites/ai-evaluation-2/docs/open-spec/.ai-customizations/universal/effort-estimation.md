# Effort Estimation Standards - Universal Application

All modes MUST follow these effort estimation standards. Dollar-based estimates are STRICTLY PROHIBITED across Universal Destinations and Experiences.

## Core Principle: Components and Endpoints, Not Dollars or Sprints

### Why Component-Level Complexity
- Grounds estimates in concrete, verifiable scope (which endpoints change?)
- Avoids false precision of sprint counts that change during planning
- Lets reviewers assess complexity per-item rather than trusting a rolled-up number
- Avoids financial commitments AI cannot validate

### Prohibited Estimation Methods
❌ **NEVER USE**:
- Dollar amounts ("$50,000", "$1M budget")
- Hourly costs ("$150/hour", "500 hours at $X")
- FTE calculations with rates
- Budget ranges in currency
- Cost-benefit in monetary terms
- Sprint counts as top-level sizing ("3-5 sprints")
- T-shirt sizes as top-level sizing ("Medium")
- Story points as top-level sizing

✅ **ALWAYS USE**:
- A table of affected components and endpoints with per-item complexity (LOW, MEDIUM, HIGH)
- A summary line: total components, total changes, breakdown by complexity level
- Confidence level (Low, Medium, High) with rationale
- Assumptions that affect the estimate

## Complexity Table Format

Every solution design MUST include a complexity estimate as a table:

```markdown
## Complexity Estimate

| Component | Change | Complexity |
|-----------|--------|------------|
| `ms-example` `get_items` | Add pagination support | LOW |
| `ms-example` `create_item` | Add cross-service validation call | MEDIUM |
| `ms-example` `batch_import` | New endpoint with retry logic and dead-letter handling | HIGH |

**Total**: 1 component, 3 changes (1 HIGH, 1 MEDIUM, 1 LOW)

**Confidence**: Medium — [rationale for confidence level]
```

### Complexity Levels

| Level | Criteria |
|-------|----------|
| **LOW** | Standard patterns, single-service, no new dependencies, well-defined scope |
| **MEDIUM** | Cross-service calls, moderate integration, some custom logic, known patterns applied in new context |
| **HIGH** | Novel logic, multi-service coordination, production data analysis required, edge-case-heavy, new infrastructure |

### What Counts as a Change

Each row in the complexity table should represent one discrete unit of work:
- A new or modified endpoint (use `operationId` where available)
- A schema change (new field, type change)
- A new infrastructure component (queue, cache, scheduled job)
- A one-time operational task (data migration, cleanup script)

Do NOT combine multiple endpoints into one row. Do NOT split a single endpoint change across multiple rows.

## Confidence Levels

| Level | Meaning |
|-------|---------|
| **High** | Scope is well-understood, patterns are established, no significant unknowns |
| **Medium** | Some unknowns exist (production data volume, edge cases, external dependencies) but approach is sound |
| **Low** | Significant unknowns — may need spike or analysis phase before committing to approach |

## Special Considerations

### Fixed-Price Requests
When stakeholders request dollar estimates:
1. Redirect to component-level complexity discussion
2. Provide the complexity table
3. Defer monetary calculations to finance

Example response:
```
"I can provide a breakdown of affected components and endpoints with
complexity ratings. The financial translation would need to come from
your finance team based on resource costs and allocation."
```

### Comparison Requests
When asked to compare options by cost:
- Compare by effort (sprints)
- Compare by complexity
- Compare by risk profile
- Compare by time-to-value

### Long-Term Planning
For multi-quarter initiatives:
- Break into phases
- Estimate each phase separately
- Identify decision points
- Allow for re-estimation

## Audit Requirements

### Documentation
Every estimate must include:
- Assumptions made
- Scope included/excluded  
- Risks identified
- Complexity factors
- Comparison methodology

### Defensibility
Estimates must be:
- Based on decomposition
- Supported by complexity analysis
- Comparable to similar efforts
- Adjustable with new information

## Quick Reference

### Estimation Checklist
- [ ] No dollar amounts used
- [ ] Sprint-based sizing provided
- [ ] Complexity factors documented
- [ ] Risks identified and buffered
- [ ] Assumptions clearly stated
- [ ] Ranges provided, not points
- [ ] Defensible methodology used

### Red Flags to Avoid
- "This will cost $X"
- "Budget of $Y required"
- "ROI of Z%"
- "Hourly rate calculations"
- "FTE cost analysis"

---

**Remember**: We estimate EFFORT, not COST. Financial calculations are the domain of finance professionals with access to rate cards, resource costs, and budget allocations.