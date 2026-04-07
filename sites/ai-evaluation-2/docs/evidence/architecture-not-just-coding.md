<!-- CONFLUENCE-PUBLISH -->
<!-- CONFLUENCE-URL: https://christopherblaisdell.atlassian.net/wiki/spaces/ARCH/pages/architecture-not-just-coding -->

# Architecture Is Not Just Coding — But the Tools Are the Same

## The Skeptic's Argument

> "AI coding assistants are designed for writing code. Architecture work is different — it requires reasoning about systems, trade-offs, standards, and organizational context. You need a bespoke solution, not a vibe coding tool."

This is a reasonable concern. It deserves a direct, evidence-based answer.

## What Architecture Work Actually Involves

When an architect works with AI assistance, the work breaks down into concrete tasks — all of which operate on workspace files:

| Architecture Task | Workspace Artifact | File Operations Required |
|-------------------|--------------------|-------------------------|
| Triage a ticket | Read ticket data, cross-reference OpenAPI specs | File reads, search, structured analysis |
| Analyze a service | Read source code, OpenAPI spec, metadata YAML | Multi-file reads, cross-referencing |
| Design a solution | Create solution folder, write ADR, impact assessments, user stories | File creation, template application |
| Review an API contract | Compare spec against source code, check backward compatibility | File reads, field-level comparison |
| Generate documentation | Read metadata YAML, produce Markdown pages with diagrams | File reads, file creation, command execution |
| Assess quality attributes | Evaluate against ISO 25010, cite evidence from specs and logs | File reads, structured reasoning |
| Produce a sequence diagram | Read OpenAPI spec, generate PlantUML, render SVG | File reads, file creation, terminal commands |

Every row in this table is file-based work. The architect reads files, reasons about their content, and produces new files. This is exactly what AI coding platforms are engineered to do.

## The Customization Primitives Are Domain-Agnostic

The objection assumes that "coding assistant" means the tool only understands code. In practice, the customization primitives offered by modern AI coding platforms are content-agnostic — they inject ANY knowledge, not just coding patterns:

| Customization Mechanism | Coding Example | Architecture Example |
|-------------------------|----------------|---------------------|
| Instruction files | "Use TypeScript, prefer composition over inheritance" | "Use MADR format for all decisions, default unknown categories to Pattern 3 (safety requirement)" |
| Scoped rules (glob-based) | "When editing `*.test.ts`, use describe/it blocks" | "When editing `architecture/specs/*.yaml`, verify all fields have types, descriptions, and nullable annotations" |
| Skills with supporting files | Deploy-to-staging skill with scripts and configs | Solution design skill with MADR template, impact assessment template, capability mapping checklist |
| Agent personas | Backend developer agent with database access | Solution Architect agent with read-only tool restrictions (no code execution, no deployment) |
| Workspace indexing | Index source code, package.json, tsconfig | Index OpenAPI specs, AsyncAPI events, metadata YAML, ADRs, prior solution designs |
| MCP integration | Connect to CI/CD pipelines, test results | Connect to ticket systems, production logs, service registries |

The platform vendors already recognize this. Cline's documentation uses `architecture.md` as an [example rule file](https://docs.cline.bot/customization/cline-rules) for "structural decisions." Windsurf's Skills examples include `code-review/` bundles with style guides and security checklists — not just code generation templates.

## Evidence from the Architecture Practice Pilot

The pilot itself is the strongest evidence. The `.github/copilot-instructions.md` file (500+ lines) defines:

- A **Solution Architect role** with explicit responsibilities and boundaries
- A **19-service microservice domain model** with bounded context rules and data ownership boundaries
- **Architecture standards** (MADR, C4 model, arc42, ISO 25010) loaded into every AI session
- **Safety constraints** ("unknown categories MUST default to Pattern 3") enforced through instruction files
- **Mock tool commands** for JIRA, Elastic, and GitLab — enabling the AI to investigate tickets using local scripts

The scoped `.instructions.md` files in `architecture/`, `architecture/specs/`, and `architecture/solutions/` inject additional context precisely when the architect is working in those directories — API design rules when editing specs, solution review checklists when designing solutions, security constraints when analyzing architecture.

The AI agent operating under these instructions has:

- Produced 4 complete solution designs with MADR ADRs, impact assessments, and user stories
- Generated 19 microservice deep-dive pages with 139 PlantUML sequence diagrams
- Maintained a capability changelog across multiple related tickets
- Conducted architectural investigations citing specific log entries, source code lines, and spec fields

None of this required building a bespoke agent. It required **configuring a general-purpose AI coding platform for architecture work** — using the same primitives that developers use to configure it for coding work.

## Why "Bespoke for Architecture" Is a Category Error

The argument for a bespoke architecture agent typically proposes building:

1. A custom knowledge base (vector DB + embedding pipeline) for architecture standards
2. Custom prompt orchestration to enforce MADR format, C4 notation, ISO 25010 analysis
3. A purpose-built agent with architecture-specific reasoning capabilities
4. Enterprise integrations for CMDB, ticket systems, and decision registries

Each of these maps directly to a native platform capability:

| Bespoke Component | Native Equivalent | Evidence |
|-------------------|-------------------|----------|
| Custom knowledge base | Workspace indexing of `architecture/` directory | 19 specs, 10 metadata YAML files, 11 ADRs — all indexed automatically |
| Custom prompt orchestration | `copilot-instructions.md` + scoped `.instructions.md` files | MADR format, C4 notation, ISO 25010 — all enforced via instruction files |
| Purpose-built architecture agent | Agent persona defined in instructions: "You operate as a Solution Architect" | Role boundaries, responsibilities, and constraints — all declarative |
| Enterprise integrations | MCP servers (Vikunja tickets, mock tools already implemented) | Working MCP connections to ticket systems, with extensibility for CMDB/ServiceNow |

Building these as a bespoke agent would take weeks of engineering. Configuring them as instruction files takes hours — and the result is version-controlled, shareable, and portable across platforms.

## The Real Question

The question is not "can AI coding platforms do architecture work?" — they demonstrably can, and the architecture practice pilot proves it daily.

The real question is "which AI coding platform does architecture work best?" — which is exactly what this evaluation answers. See the [Evaluation Methodology](../framework/evaluation-methodology.md) for the scoring framework that compares platform capabilities across 12 factors.

See also: [Build vs Leverage](build-vs-leverage.md) for the broader argument about when custom RAG pipelines are justified.
