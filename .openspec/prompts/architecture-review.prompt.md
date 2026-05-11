---
agent: "agent"
description: "Run a structured architecture review of a NovaTrek service, solution design, or proposed change. Analyzes current state, evaluates trade-offs against ISO 25010 quality attributes, and detects anti-patterns."
---

# Architecture Review

Perform a structured architecture review following the process below.

## Scope

Determine what is being reviewed:
- **Service review**: Analyze a single service's API contracts, data model, and integration points
- **Solution review**: Evaluate a proposed solution design for completeness and soundness
- **Change review**: Assess a proposed API or schema change for compatibility and impact

## Phase 1: Current State Analysis

Gather evidence before forming opinions.

### For Service Reviews
1. Read the OpenAPI spec: `architecture/specs/svc-{name}.yaml`
2. Read the source code: `source-code/svc-{name}/`
3. Check cross-service calls: `architecture/metadata/cross-service-calls.yaml`
4. Check data store ownership: `architecture/metadata/data-stores.yaml`
5. Check production errors: `python3 scripts/mock-elastic-searcher.py --service svc-{name} --level ERROR`
6. Check recent MRs: `python3 scripts/mock-gitlab-client.py --project svc-{name} --mrs`

### For Solution Reviews
1. Read the full solution design: `architecture/solutions/_NTK-XXXXX-*/`
2. Verify all affected services are identified
3. Check prior art: `python3 scripts/ticket-client.py --list --capability CAP-X.Y`
4. Cross-reference with capability changelog: `architecture/metadata/capability-changelog.yaml`
5. Review related ADRs: `decisions/`

### For Change Reviews
1. Read the current spec for the affected service
2. Identify all consumers of the changed endpoint or schema
3. Assess backward compatibility
4. Check for data ownership violations

## Phase 2: Anti-Pattern Detection

Scan for these architectural anti-patterns:

| Anti-Pattern | What to Look For | Severity |
|-------------|-----------------|----------|
| Shared Database | Multiple services querying same tables | CRITICAL |
| Entity Replacement | PUT semantics overwriting fields from other services | HIGH |
| Missing Concurrency Control | No `@Version` or `_rev` on mutable entities | HIGH |
| Shadow Guest Records | Services maintaining local guest identity copies | HIGH |
| Unsafe Defaults | Unknown inputs defaulting to lowest safety level | CRITICAL |
| Hardcoded Classification | Business rules embedded in switch/case or constants | MEDIUM |
| Distributed Monolith | Tight synchronous call chains across domains | MEDIUM |
| Missing Null Handling | Nullable fields without documented null semantics | MEDIUM |

## Phase 3: Quality Attribute Assessment

Evaluate against ISO 25010 quality characteristics:

| Characteristic | Key Questions |
|---------------|--------------|
| Functional Suitability | Does the design meet the stated requirements? Are there gaps? |
| Performance Efficiency | Will the change introduce latency? Are there N+1 query risks? |
| Compatibility | Are API changes backward-compatible? Do consumers need updates? |
| Reliability | Are error handling and fallback paths defined? Is there retry/timeout logic? |
| Security | Does it touch PII, auth, or cross-service data flows? Is input validated? |
| Maintainability | Is the change modular and testable? Does it follow existing patterns? |

## Phase 4: Trade-Off Documentation

For each significant finding, document:

1. **Finding**: What was observed — cite file paths and line numbers
2. **Risk**: What could go wrong if this is not addressed
3. **Options**: At least 2 genuine alternatives (not straw-man)
4. **Recommendation**: Which option is preferred and why
5. **Quality Impact**: Which ISO 25010 characteristics are affected

## Output Format

```markdown
# Architecture Review: [Subject]
*Date: [YYYY-MM-DD] | Reviewer: AI-Assisted | Scope: [Service/Solution/Change]*

## Summary
[2-3 sentences: overall assessment and key concerns]

## Findings

### [SEVERITY] Finding 1: [Title]
**Location**: [file path, line numbers]
**Description**: [What was found]
**Risk**: [What could go wrong]
**Recommendation**: [Proposed action]

### [SEVERITY] Finding 2: [Title]
...

## Quality Assessment
| Characteristic | Rating | Notes |
|---------------|--------|-------|
| Functional Suitability | [Pass/Concern/Fail] | [Brief note] |
| Compatibility | [Pass/Concern/Fail] | [Brief note] |
| Reliability | [Pass/Concern/Fail] | [Brief note] |
| Security | [Pass/Concern/Fail] | [Brief note] |
| Maintainability | [Pass/Concern/Fail] | [Brief note] |

## Recommendations
1. [Actionable recommendation with priority]
2. [Actionable recommendation with priority]
```

## Rules

- **Evidence over opinion.** Every finding must cite a file path or tool output.
- **Run the tools.** Use mock JIRA, Elastic, and GitLab when the review requires production data.
- **Respect data ownership.** Reference `architecture/metadata/data-stores.yaml` for who owns what.
- **Check the safety rule.** Unknown adventure categories MUST default to Pattern 3 (ADR-005).
- **No quantified claims without evidence.** Write "significant improvement" not "99.9% reliability".
