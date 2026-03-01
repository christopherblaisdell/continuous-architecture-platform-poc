# ADR Templates Collection

## Overview

An Architecture Decision Record (ADR) is a document that captures an important architectural decision made along with its context and consequences. ADRs are a lightweight way to create and maintain a decision log for a project.

## Origin

The concept of ADRs was introduced by Michael Nygard in his November 2011 blog post, **"Documenting Architecture Decisions"**. Since then, several template variations have emerged to suit different organizational needs.

Reference: [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)

## When to Create an ADR

Create an ADR when you make a decision that:

- Affects the structure of the system (components, modules, layers)
- Selects a technology, framework, library, or tool
- Establishes a pattern, convention, or standard
- Involves a significant trade-off between competing concerns
- Will be difficult or expensive to reverse later
- Needs to be communicated to current and future team members

## Templates in This Collection

| Template | Style | Best For |
|----------|-------|----------|
| `nygard-template.md` | Original/Minimal | Quick decisions, small teams |
| `alexandrian-template.md` | Pattern-oriented | Decisions with complex forces/trade-offs |
| `tyree-akerman-template.md` | Business-oriented | Enterprise environments with compliance needs |

## Conventions

- Number ADRs sequentially: `0001-short-title.md`
- Use lowercase with hyphens in filenames
- ADRs are **immutable** once accepted -- create a new ADR to supersede
- Store ADRs in a `docs/decisions/` directory within the repository

## Additional Resources

- Joel Parker Henderson's ADR collection: [https://github.com/joelparkerhenderson/architecture-decision-record](https://github.com/joelparkerhenderson/architecture-decision-record) (CC0 License)
- ADR Tools: [https://github.com/npryce/adr-tools](https://github.com/npryce/adr-tools)
- ADR organization: [https://adr.github.io](https://adr.github.io)

## License

This templates collection references formats from the community. The original Nygard template and Henderson's collection are available under **CC0 (public domain)**. See individual sources for specific license terms.
