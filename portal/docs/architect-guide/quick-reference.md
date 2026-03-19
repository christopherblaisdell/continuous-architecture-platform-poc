# Quick Reference

Commands, file locations, naming conventions, and common operations — all in one place.

---

## File Locations

### Architecture Sources (You Edit These)

| What | Where |
|------|-------|
| Metadata YAML (15 files) | [`architecture/metadata/`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/architecture/metadata) |
| OpenAPI specs (23 services) | [`architecture/specs/`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/architecture/specs) |
| AsyncAPI event specs (8 services) | [`architecture/events/`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/architecture/events) |
| Solution designs | [`architecture/solutions/_NTK-XXXXX-slug/`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/architecture/solutions) |
| Global ADRs | [`decisions/`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/decisions) |
| Hand-authored diagrams | [`architecture/diagrams/{System,Components,Sequence,Tickets}/`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/architecture/diagrams) |
| Endpoint diagram overrides | [`architecture/diagrams/endpoints/`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/architecture/diagrams/endpoints) |
| Wireframes | [`architecture/wireframes/{app}/`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/architecture/wireframes) |
| Adventure classification config | [`config/adventure-classification.yaml`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/config/adventure-classification.yaml) |
| Test standards config | [`config/test-standards.yaml`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/config/test-standards.yaml) |
| Portal hand-authored pages | `portal/docs/` (selected files) |
| MkDocs configuration | [`mkdocs.yml`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/mkdocs.yml) |

### Generated Output (Do Not Edit)

| What | Where |
|------|-------|
| Microservice pages | `portal/docs/microservices/` |
| Application pages | `portal/docs/applications/` |
| Swagger UI pages | `portal/docs/services/api/` |
| Sequence diagram SVGs | `portal/docs/microservices/svg/` |
| Event catalog pages | `portal/docs/events/` |
| Solution portal pages | `portal/docs/solutions/` |
| Capability pages | `portal/docs/capabilities/` |
| Ticket pages | `portal/docs/tickets/` |
| Topology pages | `portal/docs/topology/` |
| CALM JSON | `architecture/calm/` |
| Built site | `portal/site/` |

### Generator Scripts

| Script | Purpose |
|--------|---------|
| [`portal/scripts/generate-all.sh`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/generate-all.sh) | Run all generators + build |
| [`portal/scripts/generate-microservice-pages.py`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/generate-microservice-pages.py) | Service pages + diagrams |
| [`portal/scripts/generate-application-pages.py`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/generate-application-pages.py) | App pages + wireframes |
| [`portal/scripts/generate-swagger-pages.py`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/generate-swagger-pages.py) | Swagger UI HTML |
| [`portal/scripts/generate-event-pages.py`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/generate-event-pages.py) | Event catalog |
| [`portal/scripts/generate-solution-pages.py`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/generate-solution-pages.py) | Solution pages |
| [`portal/scripts/generate-capability-pages.py`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/generate-capability-pages.py) | Capability hierarchy |
| [`portal/scripts/generate-ticket-pages.py`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/generate-ticket-pages.py) | Ticket registry |
| [`portal/scripts/generate-topology-pages.py`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/generate-topology-pages.py) | CALM topology views |
| [`portal/scripts/generate-svgs.sh`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/generate-svgs.sh) | PlantUML -> SVG |
| [`portal/scripts/load_metadata.py`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/load_metadata.py) | Central metadata loader |

---

## Common Commands

### Ticket Research

```bash
# List all tickets
python3 scripts/ticket-client.py --list

# Filter by status
python3 scripts/ticket-client.py --list --status "New"

# Filter by capability
python3 scripts/ticket-client.py --list --capability CAP-2.1

# Filter by service
python3 scripts/ticket-client.py --list --service svc-check-in
```

### Mock Tools (Phase 1 Environment)

```bash
# JIRA — get ticket detail
python3 scripts/mock-jira-client.py --ticket NTK-10005

# JIRA — list all tickets
python3 scripts/mock-jira-client.py --list

# Elastic — service error logs
python3 scripts/mock-elastic-searcher.py --service svc-check-in --level ERROR

# Elastic — keyword search
python3 scripts/mock-elastic-searcher.py --query "timeout"

# GitLab — list MRs for a project
python3 scripts/mock-gitlab-client.py --project svc-check-in --mrs

# GitLab — MR detail with diff
python3 scripts/mock-gitlab-client.py --mr 5001
```

### Portal

```bash
# Regenerate everything
bash portal/scripts/generate-all.sh

# Local preview
cd portal && python3 -m mkdocs serve

# Strict build (catch errors)
cd portal && python3 -m mkdocs build --strict

# Manual deploy
cd portal
python3 -m mkdocs build
cp -r docs/services/api site/services/
cp -r docs/specs site/
cp -r docs/microservices/svg site/microservices/
cp staticwebapp.config.json site/
npx swa deploy site --deployment-token "<token>" --env production
```

### CALM Topology

```bash
# Generate CALM JSON
python3 scripts/generate-calm.py

# Validate topology
python3 scripts/validate-calm.py
```

### Data Isolation Audit

```bash
./portal/scripts/utilities/audit-data-isolation.sh
```

---

## Naming Conventions

### Branch Names

```
solution/NTK-XXXXX-kebab-case-slug
```

Examples: `solution/NTK-10005-wristband-rfid-field`, `solution/NTK-10008-guest-reviews`

### Solution Folders

```
architecture/solutions/_NTK-XXXXX-kebab-case-slug/
```

Underscore prefix, kebab-case. Example: `_NTK-10005-wristband-rfid-field`

### Solution Design Files

```
NTK-XXXXX-solution-design.md
```

### ADR Files

```
decisions/ADR-{NNN}-{kebab-case-slug}.md
```

Sequential numbering. Check the highest existing number and increment.

### Commit Messages

Use conventional commits:

```
feat(solution): NTK-XXXXX short description
fix(spec): correct nullable annotation in svc-check-in
docs(portal): add wireframe for check-in confirmation screen
chore(metadata): update cross-service-calls for new integration
```

### Dates

ISO 8601 everywhere: `YYYY-MM-DD` (e.g., `2026-03-19`)

### Versions

Solution designs use semantic-style numbering: `v1.0`, `v1.1`, `v2.0`

---

## Solution Design Folder Structure

```
architecture/solutions/_NTK-XXXXX-slug/
  NTK-XXXXX-solution-design.md           # Master document
  1.requirements/                         # Ticket requirements report
  2.analysis/                             # Plain-language explanation
  3.solution/
    a.assumptions/                        # Assumptions (VALIDATED / PROPOSED)
    c.capabilities/capabilities.md        # Capability mappings -> changelog
    d.decisions/decisions.md              # MADR-formatted decisions
    g.guidance/                           # Implementation advice (optional)
      guidance.1/guidance.1.md
    i.impacts/                            # Per-service impact assessments
      impact.1/impact.1.md
      impact.2/impact.2.md
    r.risks/                              # Risk register
    u.user.stories/                       # User stories + acceptance criteria
```

---

## Document Formatting Rules

| Rule | Example |
|------|---------|
| No emojis | Use `CRITICAL`, `WARNING`, `NOTE`, not icons |
| No unvalidated claims | "Significant improvement" not "99.9% reliability" |
| No special chars in headers | Letters, numbers, spaces, hyphens only |
| Evidence-based claims | Cite file paths and line numbers |
| ISO 8601 dates | `2026-03-19` |
| Present tense for current state | "The service validates..." |
| Future tense for proposals | "The endpoint will accept..." |
| Third person for arch docs | "The architect evaluates..." |
| Second person for guides | "You create the folder structure..." |

---

## Safety Rules (Non-Negotiable)

1. Unknown adventure categories default to **Pattern 3** (Full Service) — [ADR-005](../decisions/ADR-005-pattern3-default-fallback.md)
2. Guest identity resolution goes through **svc-guest-profiles** only — no shadow records
3. Each service owns its data exclusively — **no shared databases**
4. PII fields require access control and security assessment
5. Input validation at service boundaries — never trust upstream callers

---

## Quality Attributes (ISO 25010)

Assess every solution design against these:

| Attribute | Always Assess? | When Specifically |
|-----------|---------------|-------------------|
| Functional Suitability | Yes | Every design |
| Performance Efficiency | | API or data model changes |
| Compatibility | | Cross-service or format changes |
| Reliability | | Error handling, fallback paths |
| Security | | Auth, PII, data flows |
| Maintainability | Yes | Every design |
| Portability | | Infrastructure changes only |
