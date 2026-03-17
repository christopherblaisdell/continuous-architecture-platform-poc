---
agent: "agent"
description: "Multi-source deep research workflow for architecture investigations. Searches workspace evidence, synthesizes findings, and produces cited reports."
---

# Deep Research

Produce thorough, evidence-based research reports grounded in workspace data.

## When to Use

Invoke with `#deep-research` when:
- Investigating a ticket that requires understanding multiple services, specs, or logs
- Evaluating technology options or architectural trade-offs
- Performing due diligence on a proposed design change
- Any question requiring synthesis from multiple workspace sources

## Research Workflow

### Step 1: Define Research Questions

Break the topic into 3-5 specific sub-questions. Example:
- Topic: "Impact of adding real-time tracking to svc-check-in"
  - What does svc-check-in currently handle? (OpenAPI spec, source code)
  - What cross-service calls does svc-check-in make? (metadata/cross-service-calls.yaml)
  - Are there existing ADRs that constrain this design? (decisions/)
  - What capabilities are affected? (capability-changelog.yaml)
  - Are there error patterns in production logs? (mock Elastic)

### Step 2: Gather Evidence from Multiple Sources

Search these workspace sources systematically:

| Source | How to Search | What You Get |
|--------|--------------|--------------|
| OpenAPI specs | Read `architecture/specs/svc-*.yaml` | API contracts, schemas, endpoints |
| Source code | Read `source-code/svc-*/` | Implementation details, anti-patterns |
| Architecture metadata | Read `architecture/metadata/*.yaml` | Capabilities, cross-service calls, data stores |
| ADRs | Read `decisions/ADR-*.md` | Design constraints and rationale |
| Existing solutions | Read `architecture/solutions/_NTK-*/` | Prior art and precedent |
| JIRA tickets | `python3 scripts/mock-jira-client.py --ticket NTK-XXXXX` | Requirements and comments |
| Production logs | `python3 scripts/mock-elastic-searcher.py --service svc-name --level ERROR` | Error patterns |
| Merge requests | `python3 scripts/mock-gitlab-client.py --project svc-name --mrs` | Recent code changes |
| Capability changelog | Read `architecture/metadata/capability-changelog.yaml` | L3 capability history |

**Search order**: JIRA first (requirements) -> Elastic (production evidence) -> Specs and source code (current state) -> ADRs and solutions (constraints and prior art) -> GitLab (recent changes)

### Step 3: Cross-Reference and Verify

- Cross-reference findings across sources — does the source code match the OpenAPI spec?
- If only one source says something, flag it as unverified
- Note contradictions between sources (spec says X, code does Y)
- Check for stale data (spec version vs actual implementation)

### Step 4: Synthesize Report

Structure findings as:

```markdown
# [Topic]: Research Report
*Date: [YYYY-MM-DD] | Sources: [N files examined] | Confidence: [High/Medium/Low]*

## Summary
[3-5 sentences summarizing key findings]

## Findings

### 1. [First Theme]
[Evidence-backed findings with file path citations]
- Finding (Source: `architecture/specs/svc-check-in.yaml`, line 45)
- Finding (Source: `python3 scripts/mock-elastic-searcher.py --service svc-check-in --level ERROR`)

### 2. [Second Theme]
...

## Gaps and Unknowns
- [What could not be determined from available sources]
- [Assumptions made due to missing data]

## Recommendations
- [Actionable recommendation 1]
- [Actionable recommendation 2]
```

## Quality Rules

1. **Every claim needs a source.** Cite file paths and line numbers. No unsourced assertions.
2. **Run mock tools.** When the scenario requires data from JIRA, Elastic, or GitLab, run the mock scripts — do not guess what they would return.
3. **Acknowledge gaps.** If you could not find evidence for a sub-question, say so explicitly.
4. **No fabrication.** If data is not in the workspace, document it as an assumption — do not invent it.
5. **Separate fact from inference.** Label estimates, projections, and opinions clearly.
6. **Recency matters.** Note when source data may be stale (e.g., spec version does not match source code).
