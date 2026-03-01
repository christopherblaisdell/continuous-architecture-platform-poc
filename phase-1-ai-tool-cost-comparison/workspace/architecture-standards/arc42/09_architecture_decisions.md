# 9. Architecture Decisions

> **Help**: Important, expensive, large scale, or risky architecture decisions including rationale. With "decisions" we mean selecting one alternative based on given criteria.
>
> Please use your judgment to decide whether an architectural decision should be documented here or whether it is better to document it in individual building blocks (Section 5). Avoid redundancy. Refer to Section 4 for the most general decisions that already have been captured there.
>
> **Motivation**: Stakeholders of your system should be able to comprehend and retrace your decisions. You should be able to explain the reasoning behind your decisions to your stakeholders at any time.
>
> **Form**: Various options:
> - Architecture Decision Records (ADRs) - **recommended format**
> - A decision log in tabular form
> - References to individual ADR documents (e.g., in a separate `/decisions/` folder)
>
> Keep the ADRs up to date, especially their status. A superseded or deprecated decision is valuable context for understanding the current architecture.

---

## Decision Log

| ID | Title | Status | Date | Decision |
|----|-------|--------|------|----------|
| ADR-001 | _\<Decision title\>_ | _\<Proposed/Accepted/Deprecated/Superseded\>_ | _\<YYYY-MM-DD\>_ | _\<Brief summary\>_ |
| ADR-002 | _\<Decision title\>_ | _\<Proposed/Accepted/Deprecated/Superseded\>_ | _\<YYYY-MM-DD\>_ | _\<Brief summary\>_ |
| ADR-003 | _\<Decision title\>_ | _\<Proposed/Accepted/Deprecated/Superseded\>_ | _\<YYYY-MM-DD\>_ | _\<Brief summary\>_ |

---

## ADR-001: _\<Decision Title\>_

### Status

_\<Proposed | Accepted | Deprecated | Superseded by ADR-XXX\>_

### Date

_\<YYYY-MM-DD\>_

### Context

> _\<Describe the issue motivating this decision. What is the problem, what forces are at play, and what are the constraints?\>_

### Decision

> _\<Describe the decision that was made. State the decision clearly and concisely.\>_

### Considered Alternatives

| Alternative | Pros | Cons |
|------------|------|------|
| _\<Option A (chosen)\>_ | _\<List advantages\>_ | _\<List disadvantages\>_ |
| _\<Option B\>_ | _\<List advantages\>_ | _\<List disadvantages\>_ |
| _\<Option C\>_ | _\<List advantages\>_ | _\<List disadvantages\>_ |

### Consequences

> _\<Describe the resulting context after applying the decision. What becomes easier or more difficult? What are the trade-offs?\>_

**Positive:**
- _\<Positive consequence 1\>_
- _\<Positive consequence 2\>_

**Negative:**
- _\<Negative consequence 1\>_
- _\<Negative consequence 2\>_

**Risks:**
- _\<Risk 1 and mitigation\>_

### Compliance

_\<How will adherence to this decision be verified? Automated checks, code review, architecture fitness functions?\>_

---

## ADR-002: _\<Decision Title\>_

### Status

_\<Proposed | Accepted | Deprecated | Superseded by ADR-XXX\>_

### Date

_\<YYYY-MM-DD\>_

### Context

> _\<Describe the issue motivating this decision.\>_

### Decision

> _\<Describe the decision that was made.\>_

### Considered Alternatives

| Alternative | Pros | Cons |
|------------|------|------|
| _\<Option A (chosen)\>_ | _\<List advantages\>_ | _\<List disadvantages\>_ |
| _\<Option B\>_ | _\<List advantages\>_ | _\<List disadvantages\>_ |

### Consequences

> _\<Describe the resulting context after applying the decision.\>_

**Positive:**
- _\<Positive consequence 1\>_

**Negative:**
- _\<Negative consequence 1\>_

---

## ADR Template (Copy for New Decisions)

```markdown
## ADR-XXX: <Decision Title>

### Status
<Proposed | Accepted | Deprecated | Superseded by ADR-XXX>

### Date
YYYY-MM-DD

### Context
<What is the issue that we're seeing that motivates this decision?>

### Decision
<What is the change that we're proposing and/or doing?>

### Considered Alternatives
| Alternative | Pros | Cons |
|------------|------|------|
| Option A (chosen) | ... | ... |
| Option B | ... | ... |

### Consequences
<What becomes easier or more difficult to do because of this change?>

**Positive:**
- ...

**Negative:**
- ...

### Compliance
<How will this decision be enforced or verified?>
```

---

> Based on the arc42 architecture template (https://arc42.org).  
> Created by Dr. Peter Hruschka and Dr. Gernot Starke.  
> Licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
