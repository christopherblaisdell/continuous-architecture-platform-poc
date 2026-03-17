---
agent: "agent"
description: "Run a structured investigation of a NovaTrek architecture ticket using mock tools in the correct sequence: JIRA first, then Elastic logs, then GitLab MRs. Produces an evidence-based investigation report."
---

# Investigation Workflow — NovaTrek Architecture

You are performing a structured investigation of a NovaTrek Adventures architecture ticket. This workflow ensures evidence is gathered systematically from all available sources before forming conclusions.

## Investigation Target

Identify the ticket to investigate. If not specified, ask for the ticket ID (e.g., NTK-10003).

## Phase 1: Ticket Context (JIRA First)

Always start with the ticket to understand the stated problem.

```bash
python3 scripts/ticket-client.py --ticket NTK-XXXXX
```

Also retrieve the mock JIRA ticket for additional context (comments, priority, assignee):

```bash
python3 phases/phase-1-ai-tool-cost-comparison/workspace/scripts/mock-jira-client.py --ticket NTK-XXXXX
```

Record:
- What is the stated problem or request?
- Which services are mentioned?
- What is the priority and status?
- Are there comments with additional context?

## Phase 2: Production Evidence (Elastic Logs)

Before looking at code changes, establish the production symptom timeline.

```bash
# Search for errors in the primary service
python3 phases/phase-1-ai-tool-cost-comparison/workspace/scripts/mock-elastic-searcher.py --service [primary-service] --level ERROR

# Search for related keyword patterns
python3 phases/phase-1-ai-tool-cost-comparison/workspace/scripts/mock-elastic-searcher.py --query "[relevant keyword]"
```

Record:
- What errors are occurring in production?
- When did the errors start?
- What is the frequency and pattern?
- Are multiple services affected?

## Phase 3: Code Changes (GitLab MRs)

Now examine recent code changes that may be related.

```bash
# List MRs for the affected service
python3 phases/phase-1-ai-tool-cost-comparison/workspace/scripts/mock-gitlab-client.py --project [service-name] --mrs

# Get details for relevant MRs
python3 phases/phase-1-ai-tool-cost-comparison/workspace/scripts/mock-gitlab-client.py --mr [MR-ID]
```

Record:
- What recent changes were made to the affected service?
- Do any MR diffs correlate with the production symptoms?
- Are there MR comments indicating known risks?

## Phase 4: Architecture Context

Read the relevant architecture artifacts:

1. **OpenAPI spec**: `architecture/specs/[service-name].yaml`
2. **Cross-service calls**: `architecture/metadata/cross-service-calls.yaml`
3. **Data stores**: `architecture/metadata/data-stores.yaml`
4. **Existing solutions**: Check if prior solutions touch the same services
   ```bash
   python3 scripts/ticket-client.py --list --service [service-name]
   ```
5. **Source code** (if available): `source-code/[service-name]/`

## Phase 5: Synthesis

Combine evidence from all four phases to form a coherent analysis.

## Output Format

```markdown
# Investigation Report: NTK-XXXXX — [Ticket Title]

**Date**: [today]
**Investigator**: AI Investigation Workflow (ECC-adapted)
**Ticket**: NTK-XXXXX
**Services Affected**: [list]

## 1. Problem Statement

[2-3 sentences from ticket context]

## 2. Evidence Timeline

### JIRA Context
- Priority: [X]
- Status: [X]
- Key details: [from ticket and comments]

### Production Logs (Elastic)
| Timestamp | Service | Level | Message |
|-----------|---------|-------|---------|
| ... | ... | ... | ... |

**Pattern**: [describe the error pattern]

### Code Changes (GitLab)
| MR | Service | Title | Date | Relevance |
|----|---------|-------|------|-----------|
| ... | ... | ... | ... | ... |

## 3. Architecture Context

- **Affected services**: [list with roles]
- **Cross-service dependencies**: [from metadata]
- **Data ownership**: [which service owns what]
- **Existing ADRs**: [relevant decisions]
- **Prior solutions**: [related work]

## 4. Analysis

[Evidence-based analysis connecting logs, code changes, and architecture context]

### Root Cause Hypothesis
[Hypothesis grounded in evidence, not speculation]

### Contributing Factors
- [Factor 1 with evidence citation]
- [Factor 2 with evidence citation]

## 5. Architectural Relevance

| Criterion | Assessment |
|-----------|-----------|
| Crosses service boundaries? | Yes/No |
| Changes data ownership? | Yes/No |
| Requires new API contracts? | Yes/No |
| Affects safety/compliance? | Yes/No |
| Needs ADR? | Yes/No |

## 6. Recommended Next Steps

1. [Action with rationale]
2. [Action with rationale]
3. [Action with rationale]
```

## Rules

- ALWAYS run JIRA before Elastic, and Elastic before GitLab — this sequence builds understanding from problem statement to symptoms to code
- NEVER skip a phase — if a tool returns no results, document that as a finding ("No errors found in svc-X logs")
- ALWAYS cite specific log entries, MR IDs, and file paths as evidence
- NEVER fabricate log data, MR details, or source code findings — only report what the mock tools return
- If evidence is contradictory, document both sides and flag the contradiction
- Use `python3` (not `python`) for all mock script invocations
