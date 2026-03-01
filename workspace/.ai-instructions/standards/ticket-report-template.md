# Ticket Report Template

Use this template when generating ticket reports from JIRA data.
Copy into `[TICKET-ID].ticket.report.md` and populate from JIRA query results.

---

```markdown
# [TICKET-ID] Ticket Report

## Ticket Summary

| Field | Value |
|-------|-------|
| Ticket ID | [TICKET-ID] |
| Title | |
| Status | |
| Priority | |
| Assignee | |
| Reporter | |
| Created | |
| Updated | |
| Sprint | |
| Epic | |

## Description

_Paste or summarize the full ticket description from JIRA._

## Architecture Relevance Classification

| Criteria | Assessment |
|----------|------------|
| Design flaw | Yes / No |
| API contract change | Yes / No |
| Service interaction change | Yes / No |
| Data model change | Yes / No |
| Infrastructure impact | Yes / No |
| **Architecture Relevant** | **Yes / No** |

## Rationale

_Explain why this ticket is or is not architecturally relevant._

## Related Tickets

_List any linked or related tickets._

## Evidence Gathered

_List sources consulted: JIRA, GitLab MRs, production logs, API specs._

| Source | Reference | Key Finding |
|--------|-----------|-------------|
| | | |

## Next Steps

_Outline recommended next steps based on classification._
```
