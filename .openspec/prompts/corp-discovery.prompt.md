---
description: "Corporate workspace discovery — audit the actual state of architecture practice to replace synthetic assumptions in the OpenSpec greenfield/brownfield analysis"
---

# Corporate Architecture Practice — Discovery Audit

You are running a structured discovery of this corporate workspace. The goal is to audit the actual state of architecture artifacts and tooling so that a context-specific greenfield vs brownfield analysis can be written based on evidence rather than assumptions.

Do NOT assume anything. For every axis below, examine what actually exists in this workspace before answering. Read files, list directories, check configurations. If something cannot be determined from the workspace alone, say so explicitly — do not guess.

When the audit is complete, return a structured findings report in the exact format described at the end of this prompt.

---

## What to Audit

Work through each axis below. For each one, examine the workspace using file system tools and return what you actually find.

---

### Axis 1: AI Instruction Files

Search for existing AI tool instruction files. These might be located at:

- `.github/copilot-instructions.md`
- `.cursorrules`
- `.cursor/rules/` (directory)
- `.windsurfrules`
- `CLAUDE.md`
- `GEMINI.md`
- `.roo/rules/` or `.roo/rules-architect/`
- `.foundry/`
- Any file named `*.instructions.md` anywhere in the workspace
- Root-level `AGENTS.md`

For each file found:
- Note the full path
- Read the first 20 lines to understand what it contains
- Identify whether it was manually written or looks like a generated file

Report: How many instruction files exist? Are they coordinated or independently maintained? Is there a pattern suggesting a generator system is already in place?

---

### Axis 2: OpenAPI / Swagger Specifications

Search for existing API contract files. These might be located at:

- Any `*.yaml`, `*.yml`, `*.json` file with OpenAPI/Swagger content
- Directories named `specs/`, `api/`, `openapi/`, `swagger/`, `contracts/`
- Files named `openapi.yaml`, `swagger.yaml`, `api-spec.yaml`, or similar
- Auto-generated paths like `src/main/resources/`, `build/`, `target/`

For each spec found:
- Note the full path
- Check `openapi:` or `swagger:` version field
- Check `info.version` to estimate how recently it was updated
- Note whether it looks manually maintained or auto-generated (check for annotation-based generation comments)

Report: How many specs exist? Where are they? Are they current or stale? Manually maintained or auto-generated?

---

### Axis 3: Architecture Diagrams

Search for existing architecture diagrams:

- `.puml`, `.plantuml` files
- `.drawio`, `.xml` files (draw.io format)
- `.excalidraw` files
- `.mermaid`, `.md` files with embedded Mermaid blocks
- Directories named `diagrams/`, `architecture/diagrams/`, `docs/diagrams/`
- Image files (`*.png`, `*.svg`) in architecture or docs directories that may be diagram exports
- Any `structurizr.dsl` file
- Links in README files pointing to Lucidchart, Miro, Mural, Visio

For each format found:
- Note the tool and format
- Count approximate number of diagrams
- Note whether they appear to be current (recently modified) or stale

Report: What diagramming tools are in use? Are diagrams in the repo or externally hosted? What format?

---

### Axis 4: Architecture Decision Records (ADRs)

Search for decision records:

- Directories named `decisions/`, `adr/`, `architecture/decisions/`, `docs/decisions/`
- Files named `ADR-*.md`, `adr-*.md`, `*.adr.md`
- Files with "decision record" or "architectural decision" in their content
- `DECISIONS.md` or `ARCHITECTURE.md` at the root
- Any README that mentions ADRs

If ADR files exist:
- Count them
- Read 2-3 to understand the format used (MADR, Y-Statements, custom, etc.)
- Note the highest ADR number to understand sequence

If no formal ADRs exist, check Confluence references or links in any docs that point to decision documentation.

Report: Do formal ADRs exist in the repo? What format? How many? What numbering convention?

---

### Axis 5: Capability Model or Service Catalog

Search for any capability taxonomy, service catalog, or domain model:

- Files named `capabilities.yaml`, `service-catalog.yaml`, `domain-model.yaml`, `services.yaml`
- Directories named `architecture/metadata/`
- Any markdown or YAML files that list services/capabilities/domains
- `mkdocs.yml`, `docs/` structure that reveals how services are organized
- README files that describe the system's service decomposition

Report: Is there a formal capability model or service catalog? If not, is there any informal documentation of what services/domains exist?

---

### Axis 6: Solution Designs

Search for solution design artifacts:

- Directories named `solutions/`, `architecture/solutions/`, `design/`, `rfcs/`, `proposals/`
- Files named `*-solution-design.md`, `RFC-*.md`, `DESIGN-*.md`
- Any markdown files with headings like "Decision Drivers", "Considered Options", "Design"
- README files or wikis that describe past design decisions

Report: Are solution designs tracked in this repo? What format? If not in the repo, is there evidence of where they live (links, references)?

---

### Axis 7: Test Standards

Search for documented test standards:

- Files named `test-standards.yaml`, `testing.md`, `TEST-STANDARDS.md`
- `sonar-project.properties` or `.sonarqube/` directory
- Test directories: `tests/`, `test/`, `spec/`, `__tests__/`
- Configuration files: `jest.config.*`, `pytest.ini`, `build.gradle` with test config, `pom.xml` with test plugins
- BDD: `features/`, `*.feature` files
- Contract testing: `contracts/`, Pact files (`*.json` in pact directories)

For any test infrastructure found:
- Identify the frameworks in use
- Note whether BDD/Gherkin is in place
- Note whether contract testing is in place

Report: What test frameworks are in use? Is there a documented test standard? What levels of testing exist (unit, integration, contract, E2E)?

---

### Axis 8: AsyncAPI / Event Schemas

Search for event-driven architecture documentation:

- Files named `*.events.yaml`, `asyncapi.yaml`, `events.yaml`
- Directories named `events/`, `schemas/`, `messages/`
- References to schema registry (Confluent, AWS Glue, Apicurio) in configuration files
- Kafka configuration: `kafka*.yaml`, `kafka*.properties`
- Event constants in source code that suggest an event catalog

Report: Are event schemas formally documented? Where? Is there a schema registry? Are AsyncAPI files present?

---

### Axis 9: CI/CD Pipeline

Search for CI/CD pipeline configuration:

- `.github/workflows/` directory and its `.yml` files
- `.gitlab-ci.yml`
- `Jenkinsfile`
- `azure-pipelines.yml`
- `bitbucket-pipelines.yml`
- `.circleci/config.yml`
- `Makefile` with deploy/build targets

For each pipeline found:
- Identify the CI tool
- Note what stages exist (lint, test, build, deploy, security scan)
- Check whether any AI instruction validation step exists (look for `generate-tool-instructions.py`, `openspec`, or similar)

Report: What CI tool is used? What pipeline stages exist? Is there capacity to add an OpenSpec generator check gate?

---

### Axis 10: Documentation Portal

Search for documentation infrastructure:

- `mkdocs.yml` — MkDocs
- `docusaurus.config.*` — Docusaurus
- `_config.yml` + `docs/` — Jekyll / GitHub Pages
- `vitepress.config.*` — VitePress
- `antora-playbook.yml` — Antora
- Confluence space links in README files
- Azure Static Web Apps, GitHub Pages, or Netlify deploy configuration

Report: Is there a docs portal? What technology? Is it deployed? Where does architecture documentation currently live (repo, Confluence, wiki, or not formally maintained)?

---

### Axis 11: Corporate Tool Identification

This is critical for writing accurate instruction files. Identify the actual tools in use:

**Issue / Project Tracking:**
- Check README for Jira, Linear, Shortcut, GitHub Issues, Azure DevOps mentions
- Look for ticket ID patterns in commit messages (`git log --oneline -50`)
- Look for `.jira/`, `.linear/`, or issue tracker configuration files

**Log Aggregation / Observability:**
- Check infrastructure files for Datadog, Splunk, Grafana, CloudWatch, Elastic/Kibana mentions
- Look for observability SDK imports in package.json, pom.xml, requirements.txt, or build.gradle

**Source Control / Code Review:**
- Determine: GitHub, GitLab, Bitbucket, Azure DevOps, or self-hosted
- Check remote URL: `git remote -v`

**Communication / Documentation:**
- Look for Confluence space URLs in any README or docs file
- Look for Notion links, SharePoint references, or internal wiki URLs

Report: For each tool category, what specific tool is in use?

---

### Axis 12: Service / System Inventory

List the actual services or systems that exist in this workspace:

- Top-level directories in the repository
- Services defined in `docker-compose.yml`, `docker-compose.*.yml`
- Services in Kubernetes manifests (`k8s/`, `kubernetes/`, `helm/`)
- Microservice directories in a monorepo (look for multiple `package.json`, `pom.xml`, or `build.gradle` files)
- Infrastructure components in Terraform or Bicep files

Report: What are the top-level systems/services? How many? Are they a monorepo, polyrepo, or mixed?

---

## Findings Report Format

Return your findings in this exact structure. Use "NOT FOUND" if something does not exist. Use "UNCERTAIN — [reason]" if you cannot determine the answer from the workspace alone.

```markdown
## Corporate Architecture Practice — Discovery Findings

**Date:** [today's date]
**Workspace:** [workspace root path]
**Audited by:** [AI tool name]

---

### Axis 1: AI Instruction Files
- Files found: [list with paths]
- Coordinated or independent: [answer]
- Generator system in place: [Yes / No / Uncertain]
- Action needed: [Greenfield / Brownfield / Uncertain]

### Axis 2: OpenAPI / Swagger Specifications
- Files found: [count and paths]
- Format: [Swagger 2.0 / OpenAPI 3.x / mixed]
- Maintenance: [manually maintained / auto-generated / unknown]
- Currency: [appears current / appears stale / mixed]
- Action needed: [Import verbatim / Already in place / Not present — start greenfield]

### Axis 3: Architecture Diagrams
- Format in use: [PlantUML / draw.io / Miro / Lucidchart / Mermaid / none found]
- Location: [in-repo / externally hosted / mixed]
- Count (approximate): [number]
- Currency: [appears current / appears stale / unknown]
- Action needed: [Convert / Generate from spec / No action needed / Start greenfield]

### Axis 4: Architecture Decision Records
- Format: [MADR / Y-Statements / Custom / None found]
- Location: [path if found]
- Count: [number or "none"]
- Highest number: [ADR-XXX or "n/a"]
- Action needed: [Continue sequence / Start at ADR-001 / Retroactive triage needed]

### Axis 5: Capability Model / Service Catalog
- Formal taxonomy: [Yes — path / No]
- Informal service list: [Yes — where / No]
- Action needed: [Import existing / Derive from service inventory]

### Axis 6: Solution Designs
- In-repo format: [Yes — path / No]
- External location: [Confluence / Notion / Wiki / Unknown]
- External URL pattern: [example URL or "not found"]
- Action needed: [Start fresh in repo / Import existing / Migrate from external]

### Axis 7: Test Standards
- Documented standard: [Yes — path / No]
- Test frameworks in use: [list]
- BDD / Gherkin in place: [Yes / No / Partial]
- Contract testing in place: [Yes / No]
- Action needed: [Write config/test-standards.yaml — document what exists]

### Axis 8: AsyncAPI / Event Schemas
- Formal schema docs: [Yes — format and path / No]
- Schema registry: [Confluent / AWS Glue / Apicurio / None]
- Action needed: [Import / Start greenfield / Out of scope]

### Axis 9: CI/CD Pipeline
- CI tool: [GitHub Actions / Azure DevOps / GitLab CI / Jenkins / CircleCI / Other]
- Pipeline file(s): [path(s)]
- Stages: [list]
- AI instruction gate possible: [Yes / Needs investigation]

### Axis 10: Documentation Portal
- Portal technology: [MkDocs / Docusaurus / Jekyll / Antora / None]
- Deployed at: [URL or "not deployed"]
- Architecture docs location: [in portal / Confluence / wiki / not maintained]

### Axis 11: Corporate Tools
- Issue tracking: [tool name + evidence]
- Observability / logs: [tool name + evidence]
- Source control: [tool + remote URL]
- Documentation: [Confluence / Notion / SharePoint / wiki + URL pattern]

### Axis 12: Service / System Inventory
- Repo type: [monorepo / polyrepo / mixed]
- Services/systems found: [list — top 10-15 if many]
- Total count: [number]

---

### Corrections to the Synthetic Assumptions

Based on the above findings, list which assumptions from `.openspec/GREENFIELD-VS-BROWNFIELD-ALL-CONCERNS.md` need to be updated, and what the correct answer is for each:

| Synthetic Assumption | Actual State |
|---------------------|-------------|
| [assumption from the document] | [what you found] |
```

When the findings report is complete, save it as `.openspec/CORP-DISCOVERY-FINDINGS.md` in this workspace.

Then, using the findings, rewrite `.openspec/GREENFIELD-VS-BROWNFIELD-ALL-CONCERNS.md` to replace every synthetic assumption with the real answer. Where the answer is still unknown after discovery, mark it "PENDING — [what you need to verify with the team]" rather than guessing.
