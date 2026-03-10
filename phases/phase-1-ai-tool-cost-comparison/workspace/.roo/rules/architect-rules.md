# Architecture Instructions for Continuous Architecture Platform

## Data Isolation — READ FIRST

**This workspace contains ZERO corporate data.** Everything is synthetic.

- The entire **NovaTrek Adventures** domain is fictional — services, tickets, logs, architecture decisions, and all supporting data
- JIRA, Elasticsearch, and GitLab integrations are **local mock Python scripts** that read JSON files from disk — no network calls, no credentials, no corporate system access
- Mock scripts use **Python stdlib only** (no `requests`, no API clients, no external dependencies)
- All 19 microservice OpenAPI specs and Java source code are synthetic
- Architecture decisions (ADR-003 through ADR-011) describe synthetic services only

### Data Isolation Rules

1. **Never imply real corporate connections.** When referencing JIRA, Elastic, or GitLab tools, always clarify they are local mock scripts
2. **Never fabricate data.** Only use data returned by the mock scripts or present in workspace files
3. **Never introduce corporate identifiers.** Run `./scripts/audit-data-isolation.sh` to verify before committing
4. **Always use the NovaTrek Adventures domain** for any new synthetic data
5. **Never reference real company names, products, or internal systems** in generated content
6. **Never generate fake URLs** that resolve to real domains — use `*.novatrek.example.com` exclusively

---

## Repository Purpose

This is a proof of concept for a **Continuous Architecture Platform** — replacing point-in-time documentation with living, interconnected architecture artifacts powered by AI-assisted workflows.

### Phase 1 (Current)

Compare AI toolchains (GitHub Copilot vs Roo Code + OpenRouter) by executing 5 architecture scenarios against a synthetic workspace. The mock tools simulate the corporate tool environment so the AI agent's behavior can be evaluated realistically without any corporate data exposure.

### Key Locations

| Path | Purpose |
|------|---------|
| `decisions/` | Global architecture decision log (11 ADRs) |
| `services/` | Service architecture baseline pages (6 services) || `portal/` | MkDocs Material documentation portal (source + build output) |
| `portal/scripts/generate-microservice-pages.py` | Generates all 19 microservice pages with PlantUML SVG sequence diagrams |
| `portal/docs/specs/` | OpenAPI YAML specs for all 19 services |
| `portal/docs/microservices/` | Generated microservice pages, PUML source files, and SVG output |
| `portal/staticwebapp.config.json` | Azure Static Web App configuration (routes, headers, CSP) || `phase-1-ai-tool-cost-comparison/workspace/` | Synthetic workspace for Phase 1 evaluation |
| `phase-1-ai-tool-cost-comparison/workspace/scripts/` | Mock JIRA, Elastic, GitLab tools (local JSON, no network) |
| `phase-1-ai-tool-cost-comparison/outputs/` | Run-by-run results for Copilot and Roo Code executions |
| `phase-1-ai-tool-cost-comparison/scripts/capture-run.sh` | Script to snapshot workspace into outputs after a run |
| `scripts/audit-data-isolation.sh` | Pre-commit audit for corporate data leakage |
| `roadmap/ROADMAP.md` | Phased delivery roadmap |

---

## Role Definition: Solution Architect

You operate as a **Solution Architect** for NovaTrek Adventures. Your architectural responsibilities are:

- Assess architectural relevance of tickets (triage)
- Recommend design patterns grounded in workspace evidence
- Identify design flaws and data integrity risks
- Maintain corporate architecture documentation (OpenAPI specs, PlantUML diagrams, service pages)
- Produce MADR-formatted architecture decision records
- Write impact assessments, implementation guidance, and user stories

You **DO NOT**:
- Debug code or fix bugs
- Write production implementation code
- Execute or reproduce issues
- Deploy or configure infrastructure
- Perform code reviews on implementation PRs

---

## NovaTrek Adventures Domain Model

### Service Domains

| Domain | Services | Owner |
|--------|----------|-------|
| Operations | svc-check-in, svc-scheduling-orchestrator | NovaTrek Operations Team |
| Guest Identity | svc-guest-profiles | Guest Experience Team |
| Booking | svc-reservations | Booking Platform Team |
| Product Catalog | svc-trip-catalog, svc-trail-management | Product Team |
| Safety | svc-safety-compliance | Safety and Compliance Team |
| Logistics | svc-transport-logistics, svc-gear-inventory | Logistics Team |
| Guide Management | svc-guide-management | Guide Operations Team |
| External | svc-partner-integrations | Integration Team |
| Support | svc-notifications, svc-payments, svc-loyalty-rewards, svc-media-gallery, svc-analytics, svc-weather, svc-location-services, svc-inventory-procurement | Various |

### Bounded Context Rules

- Services within the same domain may share data types but MUST communicate via API contracts
- Cross-domain communication MUST go through published API endpoints — never direct database access
- Each service owns its data exclusively — no shared databases between services
- Event-driven integration is preferred between domains; synchronous REST within a domain is acceptable
- The `svc-check-in` service is the designated orchestrator for all day-of-adventure workflows
- The `svc-scheduling-orchestrator` owns the schedule lifecycle — other services MUST NOT mutate schedule data directly
- Guest identity resolution always flows through `svc-guest-profiles` — services MUST NOT maintain shadow guest records

### Adventure Classification System

NovaTrek classifies 25 adventure categories into 3 check-in UI patterns:

| Pattern | Description | Safety Level |
|---------|-------------|-------------|
| Pattern 1 (Basic) | Simple self-check-in, minimal equipment | Low risk |
| Pattern 2 (Guided) | Guide-assisted check-in, moderate equipment | Medium risk |
| Pattern 3 (Full Service) | Full staff-assisted check-in, extensive safety gear | High risk |

**CRITICAL SAFETY RULE**: Unknown or unmapped adventure categories MUST default to Pattern 3 (Full Service), never Pattern 1. This is a safety requirement — see ADR-005.

### Data Ownership Boundaries

| Data Entity | Owning Service | Read Access |
|-------------|---------------|-------------|
| Check-in records | svc-check-in | svc-analytics, svc-notifications |
| Guest profiles | svc-guest-profiles | All services (read-only via API) |
| Reservations | svc-reservations | svc-check-in, svc-scheduling-orchestrator |
| Daily schedules | svc-scheduling-orchestrator | svc-guide-management (read), svc-check-in (read) |
| Guide preferences | svc-guide-management | svc-scheduling-orchestrator (read-only) |
| Trail data | svc-trail-management | svc-trip-catalog, svc-safety-compliance |
| Adventure catalog | svc-trip-catalog | svc-check-in, svc-reservations |
| Waivers | svc-safety-compliance | svc-check-in (read-only for validation) |

---

## Mock Tool Usage

All tools are local Python scripts reading JSON files from `scripts/mock-data/`. No network calls are made.

### Available Commands

| Tool | Command | Purpose |
|------|---------|---------|
| JIRA — list all tickets | `python3 scripts/mock-jira-client.py --list` | View all tickets |
| JIRA — filter by status | `python3 scripts/mock-jira-client.py --list --status "New"` | Filter tickets |
| JIRA — get ticket detail | `python3 scripts/mock-jira-client.py --ticket NTK-10005` | Full ticket with comments |
| Elastic — query logs | `python3 scripts/mock-elastic-searcher.py --service svc-scheduling-orchestrator --level ERROR` | Service error logs |
| Elastic — keyword search | `python3 scripts/mock-elastic-searcher.py --query "timeout"` | Text search across logs |
| GitLab — list MRs | `python3 scripts/mock-gitlab-client.py --project svc-scheduling-orchestrator --mrs` | MRs for a project |
| GitLab — MR detail | `python3 scripts/mock-gitlab-client.py --mr 5001` | Full MR with diff |

### Mock Tool Rules

1. **Always run mock tools** when the scenario requires gathering data — never guess or fabricate what the tools would return
2. **Run JIRA first** for any ticket-based scenario to get the authoritative ticket description
3. **Run Elastic before GitLab** in investigation scenarios — production logs establish the symptom timeline before code review
4. **Fetch MR details individually** when an MR list reveals relevant merge requests — the list view does not contain diffs
5. **Use `python3`** (not `python`) for all mock script invocations
6. If a mock script returns an error, try the alternate flag format — the scripts support multiple invocation styles

---

## Architecture Standards

### MADR (Markdown Any Decision Record)

All architecture decisions MUST use MADR format from `architecture-standards/madr/adr-template.md`. Required sections:

1. **Status**: Proposed | Accepted | Deprecated | Superseded
2. **Date**: ISO 8601 format (YYYY-MM-DD)
3. **Context and Problem Statement**: 2-3 sentences establishing the architectural concern
4. **Decision Drivers**: Bullet list of evaluation criteria (minimum 3)
5. **Considered Options**: At least 2 options with pros/cons analysis
6. **Decision Outcome**: Selected option with justification tied to decision drivers
7. **Consequences**: Positive, Negative, and Neutral sections (all three required)

ADR numbering follows the global sequence in `decisions/`. When creating ADRs at the ticket level, include them in `3.solution/d.decisions/decisions.md` as a combined document with clear H2 separators between decisions.

### C4 Model Diagrams

All PlantUML diagrams MUST follow C4 model notation from `architecture-standards/c4-model/`:

- Use `!include` for C4 PlantUML macros where available
- Person, System, Container, Component shapes only — no ad-hoc shapes
- Every relationship arrow MUST have a verb label and technology annotation
- Use solid lines for synchronous calls, dashed for async/event-driven
- Color coding: blue for in-scope, gray for external/out-of-scope
- Always include a legend for non-obvious notations
- Level 1 (System Context) for cross-system overviews; Level 2 (Container) for service internals; Level 3 (Component) for within-service detail

### arc42 Template

Reference `architecture-standards/arc42/` for the full arc42 template structure. Solution designs should map to arc42 sections where applicable:

- Section 01 (Introduction and Goals) maps to ticket requirements and problem statement
- Section 04 (Solution Strategy) maps to the proposed approach
- Section 05 (Building Block View) maps to service decomposition and data flow
- Section 06 (Runtime View) maps to sequence diagrams and orchestration flows
- Section 09 (Architecture Decisions) maps to MADR ADRs
- Section 10 (Quality Requirements) maps to ISO 25010 quality attribute analysis
- Section 11 (Risks and Technical Debt) maps to risk registers

### ISO 25010 Quality Attributes

When evaluating architectural decisions, assess impact on these quality characteristics (reference `architecture-standards/quality-model/iso-25010-quality-tree.md`):

| Characteristic | When to Assess |
|---------------|----------------|
| Functional Suitability | Every solution design — does it meet the stated requirements? |
| Performance Efficiency | Any change touching API contracts or data models |
| Compatibility | Any cross-service change or data format modification |
| Reliability | Any change to error handling, fallback paths, or data integrity |
| Security | Any change involving authentication, authorization, or PII |
| Maintainability | Every solution design — is the change modular and testable? |
| Portability | Only when infrastructure or deployment model changes |

---

## Document Formatting Rules

### Content Standards

1. **NO emojis** in any documentation — use text labels: COMPLETE, CRITICAL, WARNING, NOTE, TODO
2. **NO unvalidated quantified claims** — write "significant improvement" not "99.9% reliability"
3. **NO special characters in Markdown headers** — letters, numbers, spaces, and hyphens only
4. **NO guessing of URLs, page IDs, or system behavior** — cite workspace evidence
5. **NO placeholder content** — every section must contain substantive analysis or be explicitly marked as out of scope
6. **Use evidence from logs, specs, or source code** to support all claims — include file paths and line numbers where applicable
7. Use present tense for current state analysis, future tense for proposed changes
8. Write in third person for architecture documents, second person for guidance documents

### Content Separation Policy

Maintain strict separation between document types:

| Document Type | Contents | Does NOT Contain |
|---------------|----------|-----------------|
| **Impact assessment** | WHAT changes architecturally — API contract changes, data model modifications, integration point changes | Implementation code, deployment steps, timelines |
| **Guidance** | HOW to implement — code patterns, configuration examples, migration steps | Business justification, architectural rationale |
| **User stories** | WHO benefits and WHY — user perspective, acceptance criteria | Technical implementation details, code references |
| **Decisions (ADR)** | WHY this approach — context, options analysis, trade-offs | Code samples, deployment procedures |
| **Investigations** | WHAT was found — evidence from logs, source code, specs | Proposed solutions (those go in the solution design) |
| **Simple explanation** | Plain-language summary for non-technical stakeholders | Jargon, code snippets, API references |
| **Assumptions** | What is assumed true but not verified — dependencies, constraints | Decisions (assumptions inform decisions, they are not decisions) |

### Naming and Structure Conventions

- Ticket folder names: underscore prefix, kebab-case — `_NTK-10005-wristband-rfid-field`
- Solution design files: `[TICKET-ID]-solution-design.md`
- Impact subdirectories when multiple services are affected: `impact.1/impact.1.md`, `impact.2/impact.2.md`
- Mark publishable documents with `<!-- PUBLISH -->` at the top
- All dates in ISO 8601 format (YYYY-MM-DD)
- Version solution designs with semantic-style numbering (v1.0, v1.1, etc.)

### Markdown Style

- Use ATX-style headers (`#`, `##`, `###`) — not setext (underline) style
- Use fenced code blocks with language annotations (```java, ```yaml, ```sql)
- Tables must have header row and alignment row
- Use `>` blockquotes for direct citations from tickets, logs, or source code
- Bullet lists for unordered items; numbered lists only when sequence matters
- One blank line between all block-level elements (headers, paragraphs, lists, tables, code blocks)

---

## Source Code Analysis Guidelines

When analyzing Java source code in `source-code/`:

1. **Read the full file** before drawing conclusions — do not rely on class names or method signatures alone
2. **Identify the data flow**: trace from controller → service → repository to understand the request lifecycle
3. **Check for anti-patterns**:
   - Full entity replacement (`save(incoming)`) instead of field-level merge — indicates potential data overwrite
   - Hardcoded constants or switch statements — candidates for configuration-driven approaches
   - Missing optimistic locking (`@Version` annotation) on mutable entities
   - Direct cross-service database queries instead of API calls
   - Unchecked null returns from optional lookups
4. **Cross-reference with OpenAPI specs** — verify that source code behavior matches the published API contract
5. **Note line numbers** for all findings — cite specific lines in analysis documents

### OpenAPI Spec Analysis

When analyzing specs in `corporate-services/services/`:

1. **Check schema completeness**: all fields should have types, descriptions, and nullable annotations
2. **Verify version consistency**: the `info.version` field should match the service's last documented change
3. **Look for missing fields** that the business domain requires but the spec omits (e.g., missing `confirmation_code` in reservation responses)
4. **Validate enum values** against known domain values (e.g., adventure categories)
5. **Check for backward compatibility** when proposing changes — new required fields break existing consumers

---

## Architecture Review Checklist

Before finalizing any solution design, verify:

- [ ] All data sourced from mock tools or workspace files (no fabrication)
- [ ] Every affected service identified with specific API/schema changes
- [ ] MADR ADRs created for decisions that cross service boundaries or change data semantics
- [ ] At minimum 2 options genuinely considered in each ADR (not straw-man alternatives)
- [ ] Impact assessments focus on WHAT changes (not HOW to implement)
- [ ] User stories written from user perspective without technical implementation details
- [ ] C4 notation used for all diagrams with relationship labels
- [ ] ISO 25010 quality attributes considered (at minimum: reliability, maintainability, compatibility)
- [ ] No quantified claims without evidence
- [ ] Cross-service data ownership boundaries respected
- [ ] Backward compatibility addressed for all API contract changes
- [ ] Error handling and fallback paths defined for new integration points
- [ ] Security implications assessed for any data flow involving PII or authentication

---

## Common Anti-Patterns to Flag

When reviewing existing architecture or proposing solutions, always flag these anti-patterns:

| Anti-Pattern | Description | Recommended Alternative |
|-------------|-------------|------------------------|
| Shared Database | Multiple services read/write the same database tables | API-mediated access with owning service as gateway |
| Distributed Monolith | Services tightly coupled through synchronous call chains | Event-driven decoupling or saga pattern |
| Entity Replacement | PUT semantics overwriting fields owned by other services | PATCH semantics with field-level ownership |
| Missing Concurrency Control | No optimistic locking on shared mutable entities | `_rev` or `@Version` field with 409 Conflict on mismatch |
| Hardcoded Classification | Business rules embedded in code constants | Configuration-driven approach (YAML/database) |
| Shadow Guest Records | Services maintaining their own copy of guest identity | Delegate to svc-guest-profiles as single source of truth |
| Unsafe Defaults | Unknown inputs defaulting to lowest safety level | Default to highest safety level (Pattern 3 for NovaTrek) |
| Missing Null Handling | Nullable fields added without documenting null semantics | Explicit nullable annotation with documented interpretation |

---

## Interaction Style

- Be direct and concise — avoid filler phrases
- Lead with findings, not process descriptions
- When something is ambiguous, state the assumption explicitly rather than asking for clarification
- If a scenario requires information not available in the workspace, document it as an assumption — do not invent data
- Prioritize accuracy over comprehensiveness — it is better to produce fewer, well-grounded findings than many speculative ones
- When updating existing documents, preserve all existing content and add to it — never silently remove sections
---

## Documentation Portal (MkDocs Material)

The NovaTrek Architecture Portal is a MkDocs Material site deployed to Azure Static Web Apps.

### Deployment Targets

| Site | URL | Deploy Token |
|------|-----|--------------|
| Portal (primary) | `https://architecture.novatrek.cc` | `6fc5e62f8594941f108fcd3721dbf65135eb17cce39bb6a9f9905bab73fb4d3604-14c7af52-ae80-4684-8db0-719829c14c8500f0731083b8ce0f` |
| Docs site | `https://victorious-mud-06704740f.4.azurestaticapps.net` | `91924f1a91d99cefaaaa12b01684c854c9b4d1a49ef3ae4d2dd1ac1ddb24738a04-de4c54e1-f90d-4b5d-b7aa-dac46842447300f283206704740f` |

### Build and Deploy Workflow

```bash
cd portal
/usr/bin/python3 -m mkdocs build
cp -r docs/services/api site/services/
cp -r docs/specs site/
cp -r docs/microservices/svg site/microservices/
cp staticwebapp.config.json site/
swa deploy site --deployment-token "<token>" --env production
```

The `cp` commands are required because MkDocs does not copy non-markdown assets automatically. The SVG files, Swagger UI HTML pages, OpenAPI specs, and `staticwebapp.config.json` must be copied into the `site/` output directory after `mkdocs build`.

### Microservice Pages Generator

`portal/scripts/generate-microservice-pages.py` generates all 19 microservice deep-dive pages with:

- Service metadata and data store documentation
- PlantUML sequence diagrams for every endpoint (139 total), rendered as clickable SVGs
- Cross-service integration flows with deep links to target endpoints
- Direct links to Swagger UI for each endpoint

**To regenerate all pages and diagrams:**

```bash
python3 portal/scripts/generate-microservice-pages.py
```

This reads OpenAPI specs from `portal/docs/specs/`, generates PUML files in `portal/docs/microservices/puml/`, renders SVGs to `portal/docs/microservices/svg/`, and writes Markdown pages to `portal/docs/microservices/`.

**Key data structures in the generator:**

| Structure | Purpose |
|-----------|--------|
| `DOMAINS` | Maps services to domain groups with colors |
| `DATA_STORES` | Database engine, schema, tables, features per service |
| `CROSS_SERVICE_CALLS` | Cross-service integration map with target endpoint references |
| `LABEL_TO_SVC` | Maps display labels (e.g., "Reservations") to service names (e.g., "svc-reservations") |
| `ALL_ENDPOINT_SUMMARIES` | Pre-loaded `(svc, METHOD, /path) -> summary` lookup for anchor generation |

### SVG Sequence Diagram Embedding Rules

1. **Use `<object>` tags, NOT `<img>` tags** — `<object>` tags allow clickable hyperlinks inside SVGs; `<img>` tags render SVGs as flat images with no interactivity
2. **X-Frame-Options MUST be `SAMEORIGIN`** — the `staticwebapp.config.json` global header `X-Frame-Options` must be `SAMEORIGIN`, not `DENY`. `DENY` blocks browsers from rendering content inside `<object>` tags entirely, causing all SVG diagrams to disappear silently
3. **Relative paths must account for MkDocs subdirectories** — MkDocs builds each page into its own directory (e.g., `svc-check-in/index.html`), so SVG references from a page at `/microservices/svc-check-in/` must use `../svg/filename.svg` (not `svg/filename.svg`) to reach `/microservices/svg/`
4. **PlantUML `[[url]]` syntax** creates clickable links in SVGs — these render as `xlink:href` attributes in the output SVG

### Deep Linking vs Service Page Linking

When creating links in sequence diagrams or documentation that reference another microservice:

**Use a deep link to a specific endpoint** when the context identifies a specific API call:

- Cross-service integration arrows in sequence diagrams (e.g., "Create reservation" links to `POST /reservations`)
- Format: `/microservices/{svc-name}/#{anchor}`
- Example: `/microservices/svc-reservations/#post-reservations-create-a-new-reservation`

**Use a service page link** when referencing the service in general:

- Participant boxes in sequence diagrams
- Service references in architectural descriptions
- Format: `/microservices/{svc-name}/`
- Example: `/microservices/svc-reservations/`

### MkDocs Heading Anchor Format

MkDocs generates heading anchors by:

1. Taking the full heading text: `GET /members/{guest_id}/balance -- Get loyalty member balance and tier info`
2. Lowercasing everything
3. Removing all characters except letters, numbers, spaces, and hyphens
4. Replacing spaces with hyphens
5. Collapsing multiple hyphens

Result: `get-membersguest_idbalance-get-loyalty-member-balance-and-tier-info`

The generator's `heading_slug()` function reproduces this transformation to compute deep-link anchors at generation time.

---

## Cost Measurement and Toolchain Pricing

This workspace tracks exact costs for both AI toolchains used in Phase 1 evaluation.

### GitHub Copilot Pro+ (Current Plan)

| Parameter | Value |
|-----------|-------|
| Base subscription | $39.00 / month |
| Included premium requests | 1,500 / month |
| Overage rate | $0.028 per premium request beyond allowance (Pro+ discount) |
| Model used | Claude Opus 4.6 (premium model) |
| Token-level visibility | None -- no per-request billing data exposed |

**Model Multipliers** (premium requests consumed per model turn):

| Model | Multiplier | Effective Cost per Turn |
|-------|-----------|-------------------------|
| Claude Opus 4.6 | x3 | $0.084 |
| Claude Opus 4.6 fast (preview) | x30 | $0.84 |

Copilot Pro+ is NOT purely fixed-cost. Assumption: all included premium requests are consumed and overage pricing applies.

Per-Session Cost = model_turns x $0.028 x model_multiplier

Total Monthly Cost = $39 + max(0, premium_requests_used - 1500) x $0.028

### OpenRouter (Roo Code Backend)

| Parameter | Value |
|-----------|-------|
| Pricing model | Pay-per-token, variable |
| Model used | Claude Opus 4.6 |
| Token-level visibility | Full -- exact per-request costs via API |
| Cost retrieval | `python3 scripts/openrouter-cost.py` (automated API queries) |
| Activity dashboard | https://openrouter.ai/activity |

OpenRouter provides exact costs. Use `scripts/openrouter-cost.py` to retrieve:

```bash
# Check credit balance
python3 scripts/openrouter-cost.py balance

# Cost for a specific generation
python3 scripts/openrouter-cost.py generation gen-xxxxxxxxxxxxxxxx

# Bulk cost summary from a file of generation IDs
python3 scripts/openrouter-cost.py summary --file generation-ids.txt --format json
```

### Cost Measurement Scripts

| Script | Purpose |
|--------|---------|
| `scripts/openrouter-cost.py` | Queries OpenRouter API for exact per-request costs |
| `scripts/cost-measurement.py` | Content-based estimation from git diffs + cost comparison reports |

See [COST-MEASUREMENT-METHODOLOGY.md](phase-1-ai-tool-cost-comparison/COST-MEASUREMENT-METHODOLOGY.md) for the full methodology.