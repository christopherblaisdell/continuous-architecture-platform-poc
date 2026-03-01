# arc42 Architecture Documentation Template

## About arc42

**arc42** is a template for architecture communication and documentation, developed by Dr. Peter Hruschka and Dr. Gernot Starke. It provides a proven, practical, and pragmatic structure for documenting and communicating software and system architectures.

arc42 is based on practical experience of many systems in various domains, from information and web development to real-time and embedded systems.

## Template Structure

This template is organized into 12 sections:

| Section | File | Purpose |
|---------|------|---------|
| Master Document | [00_arc42-template.md](00_arc42-template.md) | Table of contents and overview |
| 1. Introduction and Goals | [01_introduction_and_goals.md](01_introduction_and_goals.md) | Requirements, quality goals, stakeholders |
| 2. Architecture Constraints | [02_architecture_constraints.md](02_architecture_constraints.md) | Technical, organizational, convention constraints |
| 3. Context and Scope | [03_context_and_scope.md](03_context_and_scope.md) | Business and technical context |
| 4. Solution Strategy | [04_solution_strategy.md](04_solution_strategy.md) | Fundamental decisions and solution approaches |
| 5. Building Block View | [05_building_block_view.md](05_building_block_view.md) | Static decomposition of the system |
| 6. Runtime View | [06_runtime_view.md](06_runtime_view.md) | Behavior and interactions at runtime |
| 7. Deployment View | [07_deployment_view.md](07_deployment_view.md) | Technical infrastructure and deployment |
| 8. Cross-cutting Concepts | [08_concepts.md](08_concepts.md) | Overarching patterns and structures |
| 9. Architecture Decisions | [09_architecture_decisions.md](09_architecture_decisions.md) | Important architectural decisions (ADRs) |
| 10. Quality Requirements | [10_quality_requirements.md](10_quality_requirements.md) | Quality tree and scenarios |
| 11. Risks and Technical Debt | [11_risks_and_technical_debt.md](11_risks_and_technical_debt.md) | Known risks and technical debt |
| 12. Glossary | [12_glossary.md](12_glossary.md) | Domain and technical terms |

## How to Use This Template

1. **Start with Section 1** - Define your goals, requirements, and stakeholders
2. **Work through Sections 2-4** - Establish constraints, context, and strategy
3. **Detail Sections 5-7** - Document building blocks, runtime, and deployment
4. **Capture cross-cutting concerns** in Section 8
5. **Record decisions** in Section 9 using ADR format
6. **Define quality** in Section 10 with measurable scenarios
7. **Track risks** in Section 11 throughout the project lifecycle
8. **Maintain the glossary** in Section 12 as a living document

### Tips

- Not every section needs to be filled out for every project
- Start with the sections most relevant to your stakeholders
- Keep the documentation close to the code (documentation-as-code)
- Update continuously rather than in big batches
- Use diagrams where they add clarity (PlantUML, Mermaid, C4, etc.)

## License

This template is based on the arc42 architecture template, licensed under the **Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)**.

- **Authors**: Dr. Peter Hruschka and Dr. Gernot Starke
- **Website**: [https://arc42.org](https://arc42.org)
- **License**: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

You are free to:
- **Share** - copy and redistribute the material in any medium or format
- **Adapt** - remix, transform, and build upon the material for any purpose

Under the following terms:
- **Attribution** - You must give appropriate credit to arc42
- **ShareAlike** - If you remix or transform, you must distribute under the same license
