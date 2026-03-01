# ADR-0000: Use Markdown Any Decision Records

## Status

Accepted

## Date

2026-02-28

## Context and Problem Statement

The architecture team needs a consistent way to document significant decisions made during the design and evolution of our systems. Without a standard format, decision rationale is lost in Slack threads, meeting notes, and tribal knowledge. New team members struggle to understand why past decisions were made.

We need to choose a format and process for recording architecture decisions that is lightweight, version-controllable, and easy to adopt.

## Decision Drivers

- Records must be stored alongside code in version control
- Format must be easy to read and write without specialized tools
- Template should be structured enough to ensure completeness but not so rigid that it discourages use
- Must support decision lifecycle (proposed, accepted, deprecated, superseded)
- Should be a recognized industry standard with community support

## Considered Options

1. MADR (Markdown Any Decision Records) v3.0.0
2. Michael Nygard's original ADR format
3. Confluence pages with a custom template
4. Informal decision logs in a shared document

## Decision Outcome

**Chosen Option**: "MADR v3.0.0", because it provides a well-structured template that balances completeness with simplicity. It is Markdown-based (version-controllable), has active community support, and includes sections for decision drivers, options analysis, and consequences that our governance process requires.

### Confirmation

Adoption will be confirmed when the first three genuine ADRs are written using the MADR template and reviewed through the architecture review process. The team will reassess the format after 10 ADRs have been created.

## Consequences

### Positive

- Consistent structure across all decision records
- Easy to review in pull requests alongside code changes
- Searchable history of architectural decisions
- Supports onboarding by providing context for past decisions

### Negative

- Requires discipline to create ADRs for every significant decision
- Some team members may need time to adopt the habit

### Neutral

- ADRs are stored in the repository under `docs/decisions/`
- Numbering convention uses four-digit sequential IDs (0000, 0001, ...)

## More Information

- MADR GitHub repository: [https://github.com/adr/madr](https://github.com/adr/madr)
- ADR organization: [https://adr.github.io](https://adr.github.io)
- Nygard's original blog post: [https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
