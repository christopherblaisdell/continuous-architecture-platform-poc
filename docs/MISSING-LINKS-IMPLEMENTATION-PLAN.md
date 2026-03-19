# Portal Cross-Linking Implementation Plan

| | |
|-----------|-------|
| **Author** | Christopher Blaisdell |
| **Date** | 2026-03-19 |
| **Status** | Proposed |
| **Depends On** | [Missing Links Analysis](MISSING-LINKS-ANALYSIS.md) |
| **Purpose** | Step-by-step plan to add all missing links identified in the analysis |

---

## Scope

Implement all missing hyperlinks across the NovaTrek Architecture Portal hand-authored pages. Links target either:

- **Portal pages** — microservice pages (`/microservices/svc-xxx/`), decision pages, capability pages
- **GitHub source** — YAML metadata files, config files, script files, spec directories

---

## Link Pattern Reference

| Target Type | Link Pattern |
|-------------|-------------|
| Microservice portal page | `[svc-check-in](../microservices/svc-check-in/)` |
| ADR decision page | `[ADR-005](../decisions/ADR-005-pattern3-default-fallback.md)` |
| Capability page anchor | `[CAP-2.1](../capabilities/index.md#cap-21-day-of-adventure-check-in)` |
| GitHub file (blob) | `[`filename`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/path/filename)` |
| GitHub directory (tree) | `[`dirname/`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/path/dirname)` |

---

## Implementation Steps

### Step 1: Domain Model Service Names (P1 -- High Impact)

**File**: `portal/docs/architect-guide/domain-model.md`
**What**: Link all ~30 service names in the Service Domains table, Bounded Context Rules, and Data Ownership table to their portal microservice pages.
**Estimated instances**: ~30

**Rules**:
- Service names in table cells: wrap each as `[svc-check-in](../microservices/svc-check-in/)`
- Service names in prose (bold or backtick): wrap as link
- Service names inside code blocks or PlantUML: leave unlinked (they are code)
- Comma-separated service lists in cells: link each individually

**Example before**:
```
| **Operations** | svc-check-in, svc-scheduling-orchestrator | NovaTrek Operations | ... |
```

**Example after**:
```
| **Operations** | [svc-check-in](../microservices/svc-check-in/), [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator/) | NovaTrek Operations | ... |
```

---

### Step 2: Unlinked ADR References (P2 -- Low Effort, High Value)

**Files**: Multiple (6 instances)
**What**: Convert parenthetical ADR references to links.

| File | Text | Replacement |
|------|------|-------------|
| `architect-guide/index.md` | `(ADR-005)` | `([ADR-005](../decisions/ADR-005-pattern3-default-fallback.md))` |
| `architect-guide/domain-model.md` | `(ADR-004)` | `([ADR-004](../decisions/ADR-004-configuration-driven-classification.md))` |
| `architect-guide/domain-model.md` | `(ADR-006)` | `([ADR-006](../decisions/ADR-006-orchestrator-pattern-checkin.md))` |
| `index.md` (homepage) | `(ADR-005)` | `([ADR-005](decisions/ADR-005-pattern3-default-fallback.md))` |
| `artifact-registry.md` | `(ADR-012)` | `([ADR-012](decisions/ADR-012-test-methodology-tdd-bdd-hybrid.md))` |
| `artifact-registry.md` | `(ADR-013)` x2 | `([ADR-013](decisions/ADR-013-spring-cloud-contract-testing.md))` |

---

### Step 3: Metadata YAML Paths in metadata-and-artifacts.md (P3)

**File**: `portal/docs/architect-guide/metadata-and-artifacts.md`
**What**: Link all 15 metadata YAML file names in the reference tables to GitHub source.

**Example before**:
```
| `domains.yaml` | 9 service domain groupings... |
```

**Example after**:
```
| [`domains.yaml`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/domains.yaml) | 9 service domain groupings... |
```

Also link directory paths and source categories in the "You Edit" table:
- `` `architecture/metadata/` `` -> GitHub tree link
- `` `architecture/specs/` `` -> GitHub tree link
- `` `architecture/events/` `` -> GitHub tree link
- `` `architecture/solutions/` `` -> GitHub tree link
- `` `architecture/diagrams/` `` -> GitHub tree link
- `` `architecture/wireframes/` `` -> GitHub tree link
- `` `config/` `` -> GitHub tree link
- `` `decisions/` `` -> GitHub tree link

---

### Step 4: Config File Paths (P4 -- Low Effort)

**Files**: Multiple (9 instances)
**What**: Link config file paths to GitHub source.

| File | Path | GitHub URL |
|------|------|-----------|
| `anti-patterns.md` | `` `config/adventure-classification.yaml` `` | blob/main/config/adventure-classification.yaml |
| `domain-model.md` | `` `config/adventure-classification.yaml` `` x2 | same |
| `testing-guide.md` | `` `config/test-standards.yaml` `` x3 | blob/main/config/test-standards.yaml |
| `your-role.md` | `` `config/test-standards.yaml` `` | same |
| `quick-reference.md` | both config files | same |
| `solution-design-template.md` | `` `config/test-standards.yaml` `` | same |

---

### Step 5: Generator Scripts in quick-reference.md (P5)

**File**: `portal/docs/architect-guide/quick-reference.md`
**What**: Link all 11 script names in the Generator Scripts table to GitHub source.

**Example before**:
```
| `portal/scripts/generate-all.sh` | Run all generators + build |
```

**Example after**:
```
| [`portal/scripts/generate-all.sh`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/portal/scripts/generate-all.sh) | Run all generators + build |
```

---

### Step 6: Generator Scripts in portal-publishing.md (P6)

**File**: `portal/docs/architect-guide/portal-publishing.md`
**What**: Link generator names in the Build Pipeline table (11 instances).

---

### Step 7: Generator Scripts in metadata-and-artifacts.md (P7)

**File**: `portal/docs/architect-guide/metadata-and-artifacts.md`
**What**: Link generator names in the "Scripts Generate" table (11 instances).

---

### Step 8: Service Names in anti-patterns.md (P8)

**File**: `portal/docs/architect-guide/anti-patterns.md`
**What**: Link 5 backtick-wrapped service names to portal pages.

**Example before**:
```
If `svc-analytics` needs check-in data, it calls `svc-check-in`'s API
```

**Example after**:
```
If [`svc-analytics`](../microservices/svc-analytics/) needs check-in data, it calls [`svc-check-in`](../microservices/svc-check-in/)'s API
```

---

### Step 9: Solutions Index Generator Fix (P9 -- Code Change)

**File**: `portal/scripts/generate-solution-pages.py`
**What**: Modify the generator to produce linked CAP-X.Y and NTK-XXXXX references in the Capability Coverage table.

**Current output**:
```
| CAP-1.2 | NTK-10002, NTK-10008 |
```

**Desired output**:
```
| [CAP-1.2](../capabilities/index.md#cap-12-adventure-discovery-and-browsing) | [NTK-10002](_NTK-10002-adventure-category-classification.md), [NTK-10008](_NTK-10008-guest-reviews-and-ratings.md) |
```

This requires modifying the generator code to:
1. Look up CAP-X.Y descriptions from capabilities.yaml for anchor slugs
2. Look up NTK-XXXXX solution file names from the solution index

---

### Step 10: Remaining File Paths and Cross-References (P10)

**Files**: Various
**What**: Link remaining backtick-wrapped paths:

| File | Path | Target |
|------|------|--------|
| `quick-reference.md` | `` `architecture/metadata/` `` | GitHub tree |
| `quick-reference.md` | `` `architecture/specs/` `` | GitHub tree |
| `quick-reference.md` | `` `architecture/events/` `` | GitHub tree |
| `quick-reference.md` | `` `decisions/` `` | GitHub tree |
| `quick-reference.md` | `` `architecture/diagrams/{...}/` `` | GitHub tree |
| `quick-reference.md` | `` `architecture/wireframes/{app}/` `` | GitHub tree |
| `quick-reference.md` | `` `mkdocs.yml` `` | GitHub blob |
| `api-contracts.md` | `` `architecture/specs/` `` | GitHub tree |
| `api-contracts.md` | `` `architecture/events/` `` | GitHub tree |
| `api-contracts.md` | `` `architecture/metadata/events.yaml` `` | GitHub blob |
| `diagrams-and-wireframes.md` | `` `architecture/diagrams/` `` subdirs | GitHub tree |
| `diagrams-and-wireframes.md` | `` `architecture/wireframes/` `` subdirs | GitHub tree |
| `solution-design-workflow.md` | `` `architecture/specs/` `` | GitHub tree |
| `solution-design-workflow.md` | `` `architecture/metadata/capability-changelog.yaml` `` | GitHub blob |

---

## Execution Order Summary

| Step | Files Modified | Instances | Effort |
|------|---------------|-----------|--------|
| 1 | domain-model.md | ~30 | Medium |
| 2 | index.md, domain-model.md, artifact-registry.md, index.md (homepage) | 6 | Low |
| 3 | metadata-and-artifacts.md | ~23 | Medium |
| 4 | anti-patterns.md, domain-model.md, testing-guide.md, your-role.md, quick-reference.md, solution-design-template.md | 9 | Low |
| 5 | quick-reference.md | 11 | Low |
| 6 | portal-publishing.md | 11 | Low |
| 7 | metadata-and-artifacts.md | 11 | Low |
| 8 | anti-patterns.md | 5 | Low |
| 9 | generate-solution-pages.py | 1 (code) | Medium |
| 10 | quick-reference.md, api-contracts.md, diagrams-and-wireframes.md, solution-design-workflow.md | ~14 | Low |
| **Total** | **~15 files** | **~120** | |

---

## Validation

After each step:

1. Run `cd portal && python3 -m mkdocs build --strict` to catch broken links
2. Preview locally: `cd portal && python3 -m mkdocs serve`
3. Verify links render correctly and targets resolve
4. Commit and push

After all steps:

1. Run `bash portal/scripts/generate-all.sh` to regenerate all pages
2. Deploy: `npx swa deploy site --deployment-token "<token>" --env production`
3. Spot-check 5-10 links on the live site

---

## Out of Scope

- **Generated pages** (microservice pages, solution detail pages, capability pages, ticket pages) — these are produced by scripts; any linking improvements go into generator code (only Step 9 touches a generator)
- **Code blocks** — service names and file paths inside fenced code blocks, bash commands, and PlantUML snippets are NOT linked (they are code examples, not references)
- **Security documentation** (`portal/docs/security/`) — these pages are research documents with few cross-references to architecture artifacts
- **Standards documentation** (`portal/docs/standards/`) — these are reference material with minimal cross-referencing needs
