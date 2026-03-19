# Missing Links Analysis — NovaTrek Architecture Portal

| | |
|-----------|-------|
| **Author** | Christopher Blaisdell |
| **Date** | 2026-03-19 |
| **Scope** | All hand-authored pages in `portal/docs/` |
| **Purpose** | Identify every instance where a meaningful link is missing — file paths, service names, ADR references, ticket references, capability references, config files, scripts, and cross-page references that could link to GitHub source or portal pages |

---

## Executive Summary

A comprehensive audit of the NovaTrek Architecture Portal identified **~120 missing link opportunities** across 15 hand-authored files. The most impactful categories are:

| Category | Count | Link Target |
|----------|-------|-------------|
| Service names (unlinked `svc-*`) | ~50 | Portal microservice pages (`/microservices/svc-xxx/`) |
| ADR references (unlinked `ADR-NNN`) | 6 | Portal decision pages (`/decisions/ADR-xxx/`) |
| Config file paths (backtick, unlinked) | 9 | GitHub source (blob/main) |
| Metadata YAML paths (backtick, unlinked) | 18 | GitHub source (blob/main) |
| Generator scripts (backtick, unlinked) | 14 | GitHub source (blob/main) |
| Spec file paths (backtick, unlinked) | 6 | GitHub source (tree/main) |
| Architecture directory paths (backtick, unlinked) | 8 | GitHub source (tree/main) |
| Generated output paths (backtick, unlinked) | 8 | Portal pages or GitHub |
| Solutions index (unlinked CAP/NTK in tables) | 14 | Portal capability/ticket pages |

NOTE: Generated files (solutions pages, microservice pages, capability pages, ticket pages) are excluded from this audit since they are produced by scripts and should be fixed at the generator level.

---

## Category 1: Unlinked Service Names

Service names like `svc-check-in` appear as plain text or in backticks throughout the architect guide but do not link to their portal microservice pages.

**Link target pattern**: `/microservices/{svc-name}/` (portal page)

### domain-model.md (~30 instances)

| Line | Text | Context |
|------|------|---------|
| 19 | `svc-check-in, svc-scheduling-orchestrator` | Service Domains table |
| 20 | `svc-guest-profiles` | Service Domains table |
| 21 | `svc-reservations` | Service Domains table |
| 22 | `svc-trip-catalog, svc-trail-management` | Service Domains table |
| 23 | `svc-safety-compliance` | Service Domains table |
| 24 | `svc-transport-logistics, svc-gear-inventory` | Service Domains table |
| 25 | `svc-guide-management` | Service Domains table |
| 26 | `svc-partner-integrations` | Service Domains table |
| 27 | `svc-notifications, svc-payments, ...` (8 services) | Service Domains table |
| 39 | `svc-check-in` | Bounded Context Rules |
| 40 | `svc-scheduling-orchestrator` | Bounded Context Rules |
| 41 | `svc-guest-profiles` | Bounded Context Rules |
| 51-58 | All service names in Data Ownership table (16 cells) | Owning Service and Read Access columns |

### anti-patterns.md (~5 instances)

| Line | Text | Context |
|------|------|---------|
| 17 | `` `svc-analytics` ``, `` `svc-check-in` `` | Shared Database example |
| 55 | `` `svc-guest-profiles` `` | Shadow Guest Records |
| 59 | `` `svc-guest-profiles` `` | Shadow Guest Records alternative |

### quick-reference.md (~2 instances)

| Line | Text | Context |
|------|------|---------|
| 234 | `svc-guest-profiles` | Safety Rules |

### Recommendation

Link service names to their portal microservice page: `[svc-check-in](../microservices/svc-check-in/)`. In tables with many service names, this is high value because readers can click through to see the service's full API, data stores, and integration patterns.

**Exclusion**: Service names inside code blocks (bash commands, PlantUML examples, commit messages) should NOT be linked — they are code, not references.

---

## Category 2: Unlinked ADR References

ADR identifiers appear as parenthetical notes (e.g., "(ADR-005)") or inline text but are not linked to the corresponding decision page.

**Link target pattern**: `../decisions/ADR-NNN-slug.md` (portal decision page)

| File | Line | Text | Target |
|------|------|------|--------|
| `architect-guide/index.md` | 69 | `(ADR-005)` | `../decisions/ADR-005-pattern3-default-fallback.md` |
| `architect-guide/domain-model.md` | 77 | `(ADR-004)` | `../decisions/ADR-004-configuration-driven-classification.md` |
| `architect-guide/domain-model.md` | 103 | `(ADR-006)` | N/A (ADR-006 exists as `ADR-006-orchestrator-pattern-checkin.md` but may not be in portal nav) |
| `index.md` | 130 | `(ADR-005)` | `decisions/ADR-005-pattern3-default-fallback.md` |
| `artifact-registry.md` | ~95 | `(ADR-012)` | `decisions/ADR-012-test-methodology-tdd-bdd-hybrid.md` |
| `artifact-registry.md` | ~338, ~397 | `(ADR-013)` (2 instances) | `decisions/ADR-013-spring-cloud-contract-testing.md` |

NOTE: Some ADR references in `anti-patterns.md` and `testing-guide.md` are already properly linked (e.g., ADR-010, ADR-011, ADR-003, ADR-012, ADR-013 at page bottom). This category covers only the UNLINKED instances.

---

## Category 3: Unlinked Config File Paths

Config file paths appear in backticks but are not linked to GitHub source.

**Link target pattern**: `https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/config/{filename}`

| File | Line | Path | Context |
|------|------|------|---------|
| `architect-guide/anti-patterns.md` | 83 | `` `config/adventure-classification.yaml` `` | Hardcoded Classification alternative |
| `architect-guide/domain-model.md` | 75 | `` `config/adventure-classification.yaml` `` | Safety rule warning |
| `architect-guide/domain-model.md` | 77 | `` `config/adventure-classification.yaml` `` | Configuration-driven paragraph |
| `architect-guide/testing-guide.md` | 23 | `` `config/test-standards.yaml` `` | What the Architect Influences |
| `architect-guide/testing-guide.md` | 123 | `` `config/test-standards.yaml` `` | Test Standards Configuration section |
| `architect-guide/testing-guide.md` | 176 | `` `config/test-standards.yaml` `` | Reference section |
| `architect-guide/your-role.md` | 97 | `` `config/test-standards.yaml` `` | Shared Ownership table |
| `architect-guide/quick-reference.md` | 21-22 | `` `config/adventure-classification.yaml` `` and `` `config/test-standards.yaml` `` | Architecture Sources table |
| `standards/solution-design/solution-design-template.md` | 164 | `` `config/test-standards.yaml` `` | Inline |

---

## Category 4: Unlinked Metadata YAML File Paths

Metadata YAML file names or paths appear in backticks without links to GitHub source.

**Link target pattern**: `https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/{filename}`

### metadata-and-artifacts.md (~12 instances)

All 15 metadata files are listed in tables with backtick names but no links:

| Line | Path |
|------|------|
| 29 | `` `domains.yaml` `` |
| 30 | `` `cross-service-calls.yaml` `` |
| 31 | `` `data-stores.yaml` `` |
| 32 | `` `label-to-svc.yaml` `` |
| 33 | `` `delivery-status.yaml` `` |
| 37 | `` `actors.yaml` `` |
| 38 | `` `applications.yaml` `` |
| 39 | `` `consumers.yaml` `` |
| 40 | `` `app-titles.yaml` `` |
| 43 | `` `events.yaml` `` |
| 47 | `` `capabilities.yaml` `` |
| 48 | `` `capability-changelog.yaml` `` |
| 49 | `` `tickets.yaml` `` |
| 53 | `` `pci.yaml` `` |
| 54 | `` `pipeline-registry.yaml` `` |

### quick-reference.md (~6 instances)

| Line | Path | Context |
|------|------|---------|
| 11 | `` `architecture/metadata/` `` | Architecture Sources table |
| 12 | `` `architecture/specs/` `` | Architecture Sources table |
| 13 | `` `architecture/events/` `` | Architecture Sources table |
| 14 | `` `architecture/solutions/_NTK-XXXXX-slug/` `` | Architecture Sources table |
| 15 | `` `decisions/` `` | Architecture Sources table |
| 16-20 | Various directory paths | Architecture Sources table |

### Other files

| File | Text | Context |
|------|------|---------|
| `testing-guide.md` | `` `data-stores.yaml` `` | What the Architect Influences |
| `your-role.md` | `` `data-stores.yaml` `` | Shared Ownership table |
| `your-role.md` | `` `tickets.yaml` `` | Core Responsibilities table |
| `solution-design-workflow.md` | `` `architecture/metadata/capability-changelog.yaml` `` | Step 7 |

---

## Category 5: Unlinked Generator Script References

Script names appear in backticks in tables without GitHub source links.

**Link target pattern**: `https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/{filename}`

### quick-reference.md (11 instances)

All entries in the "Generator Scripts" table:

| Script |
|--------|
| `` `portal/scripts/generate-all.sh` `` |
| `` `portal/scripts/generate-microservice-pages.py` `` |
| `` `portal/scripts/generate-application-pages.py` `` |
| `` `portal/scripts/generate-swagger-pages.py` `` |
| `` `portal/scripts/generate-event-pages.py` `` |
| `` `portal/scripts/generate-solution-pages.py` `` |
| `` `portal/scripts/generate-capability-pages.py` `` |
| `` `portal/scripts/generate-ticket-pages.py` `` |
| `` `portal/scripts/generate-topology-pages.py` `` |
| `` `portal/scripts/generate-svgs.sh` `` |
| `` `portal/scripts/load_metadata.py` `` |

### portal-publishing.md (11 instances)

Generator names in the Build Pipeline table (stage 1-10):

| Script |
|--------|
| `` `generate-swagger-pages.py` `` |
| `` `generate-microservice-pages.py` `` |
| `` `generate-application-pages.py` `` |
| `` `generate-wireframe-pages.py` `` |
| `` `generate-event-pages.py` `` |
| `` `generate-solution-pages.py` `` |
| `` `generate-capability-pages.py` `` |
| `` `generate-ticket-pages.py` `` |
| `` `generate-topology-pages.py` `` |
| `` `generate-svgs.sh` `` |
| `` `portal/scripts/confluence-prepare.py` `` |

### metadata-and-artifacts.md (11 instances)

"Scripts Generate (Do Not Edit)" table:

| Script |
|--------|
| `` `generate-microservice-pages.py` `` |
| `` `generate-application-pages.py` `` |
| `` `generate-swagger-pages.py` `` |
| `` `generate-event-pages.py` `` |
| `` `generate-solution-pages.py` `` |
| `` `generate-capability-pages.py` `` |
| `` `generate-ticket-pages.py` `` |
| `` `generate-topology-pages.py` `` |
| `` `generate-calm.py` `` |
| `` `generate-microservice-pages.py` `` (actor catalog) |
| `` `portal/scripts/load_metadata.py` `` |

---

## Category 6: Unlinked OpenAPI/AsyncAPI Spec Paths

Spec file paths and directories appear in backticks or code blocks without links.

**Link targets**: GitHub tree/blob or portal Swagger UI pages

| File | Text | Better Link Target |
|------|------|--------------------|
| `api-contracts.md` | `` `architecture/specs/` `` | GitHub tree |
| `api-contracts.md` | `` `architecture/events/` `` | GitHub tree |
| `api-contracts.md` | `` `architecture/metadata/events.yaml` `` | GitHub blob |
| `api-contracts.md` | `` `portal/scripts/generate-swagger-pages.py` `` | GitHub blob |
| `diagrams-and-wireframes.md` | `` `architecture/diagrams/` `` and subdirectories | GitHub tree |
| `solution-design-workflow.md` | `` `architecture/specs/` `` | GitHub tree |

---

## Category 7: Unlinked Portal Cross-References

References to other portal pages or sections appear as plain text and could be hyperlinked.

| File | Line | Text | Target |
|------|------|------|--------|
| `architect-guide/domain-model.md` | 117 | `` `architecture/wireframes/` `` | `diagrams-and-wireframes.md` or GitHub tree |
| `architect-guide/api-contracts.md` | 77 | `` `/services/api/{svc-name}.html` `` | Could be a live example link to one service |
| `architect-guide/api-contracts.md` | 146 | `` `/microservices/{svc-name}/` `` | Could be a live example link |
| `architect-guide/api-contracts.md` | 155 | `` `/api-explorer.html` `` | Could link to actual API Explorer page |
| `testing-guide.md` | 176 | `` `config/test-standards.yaml` `` | GitHub blob (listed above) |

---

## Category 8: Generated Solutions Index (Portal Generator Fix)

The solutions index (`portal/docs/solutions/index.md`) is auto-generated and contains unlinked identifiers in the Capability Coverage table. These should be fixed at the generator level.

| Text | Target |
|------|--------|
| `CAP-1.2`, `CAP-1.7`, `CAP-2.1`, `CAP-2.2`, `CAP-2.4`, `CAP-5.4`, `CAP-5.5` | `/capabilities/index.md#cap-XX-slug` |
| `NTK-10001` through `NTK-10009` in Capability Coverage table | `/tickets/NTK-XXXXX/` or solution detail pages |

These should be linked in `portal/scripts/generate-solution-pages.py`.

---

## Category 9: Homepage Unlinked ADR Reference

| File | Line | Text | Target |
|------|------|------|--------|
| `index.md` | 130 | `(ADR-005)` | `decisions/ADR-005-pattern3-default-fallback.md` |

---

## Files Already Well-Linked (No Action Needed)

These files are already well-cross-linked and require no changes:

- `platform-operations.md` — all workflows, scripts, and GitHub paths are linked
- `artifact-registry.md` — all file paths now linked to GitHub (completed 2026-03-19)
- `index.md` — Service Domains table has all service names linked to microservice pages
- `anti-patterns.md` — ADR-010, ADR-011, ADR-005, ADR-004, ADR-003 references are linked (only `svc-*` names and `config/` path missing)

---

## Priority Ranking

| Priority | Category | Impact | Effort |
|----------|----------|--------|--------|
| **P1** | Service names in domain-model.md tables | Very High — these are the primary orientation page; readers should click through to service details | Medium |
| **P2** | ADR references (6 unlinked) | High — readers need to understand WHY decisions were made | Low |
| **P3** | Metadata YAML paths in metadata-and-artifacts.md | High — YAML files are the core editing artifacts; readers should see them on GitHub | Medium |
| **P4** | Config file paths (9 instances) | Medium — useful for quick access to the actual config | Low |
| **P5** | Generator scripts in quick-reference.md | Medium — useful for power users | Medium |
| **P6** | Generator scripts in portal-publishing.md | Medium — same as P5 | Medium |
| **P7** | Generator scripts in metadata-and-artifacts.md | Medium — same as P5 | Medium |
| **P8** | Service names in anti-patterns.md | Low — fewer instances, context is illustrative | Low |
| **P9** | Solutions index generator fix (CAP/NTK links) | Medium — requires generator code change | Medium |
| **P10** | Remaining file paths and cross-references | Low | Low |
