# MADR - Markdown Any Decision Records

## Overview

MADR (Markdown Any Decision Records) is a lean template for recording architectural decisions in a structured, consistent format using Markdown. It captures the context, decision drivers, considered options, and outcomes of significant architectural choices.

## What is MADR?

MADR provides a standardized way to document **any decision** -- not just architectural ones. Each decision record captures:

- **Why** a decision was needed (context and problem statement)
- **What** options were considered
- **Which** option was chosen and why
- **What** consequences follow from the decision

## When to Use MADR

Create a new ADR when:

- Selecting a technology, framework, or library
- Choosing between architectural patterns or approaches
- Making a significant design trade-off
- Establishing a standard or convention for the team
- Deciding NOT to do something (these are equally important to record)

## How MADR Fits Into Architecture Governance

1. **Traceability** -- Every significant decision has a documented rationale
2. **Onboarding** -- New team members can understand why decisions were made
3. **Review** -- Decisions can be revisited when context changes
4. **Accountability** -- Clear ownership and status tracking

## Templates

| Template | Use Case |
|----------|----------|
| `adr-template.md` | Full MADR v3.0.0 template with all sections |
| `adr-template-short.md` | Quick/minor decisions with minimal sections |

## Examples

| File | Description |
|------|-------------|
| `0000-use-madr.md` | Example: choosing MADR as the ADR format |
| `0001-example-technology-selection.md` | Example: REST framework comparison |

## References

- **MADR GitHub**: [https://github.com/adr/madr](https://github.com/adr/madr)
- **ADR Organization**: [https://adr.github.io](https://adr.github.io)
- **MADR Version**: 3.0.0

## License

MADR is licensed under the **MIT License**. See the [MADR repository](https://github.com/adr/madr) for full license text.
