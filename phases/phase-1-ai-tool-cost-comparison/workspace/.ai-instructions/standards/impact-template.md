# Impact Assessment Template

Use this template for documenting architectural impacts of a proposed change.
Copy into `i.impacts/impacts.md` and populate for each ticket.

---

```markdown
# [TICKET-ID] Impact Assessment

## Change Summary

_Brief description of the proposed change and its architectural scope._

## Affected Services

| Service | Impact Type | Severity |
|---------|------------|----------|
| | New / Modified / Deprecated | High / Medium / Low |

## API Impact

| Endpoint | Change | Breaking | Consumer Impact |
|----------|--------|----------|-----------------|
| | | Yes / No | |

## Data Flow Impact

_Describe how data flows are affected. Include before/after if applicable._

## Infrastructure Impact

_Describe any changes to deployment, scaling, or infrastructure configuration._

## Downstream Dependencies

_List services or teams affected by this change that need to be notified._

| Team / Service | Impact Description | Action Required |
|---------------|-------------------|-----------------|
| | | |

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| | | | |

## Rollback Strategy

_Describe how this change can be safely rolled back if issues arise._
```
