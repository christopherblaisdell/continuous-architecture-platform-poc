# OpenSpec: Greenfield vs Brownfield Adoption

This guide explains how OpenSpec adoption differs depending on whether you are starting in a **greenfield** workspace (new, no prior AI instructions or architecture artifacts) or a **brownfield** workspace (existing codebase with established conventions, toolchains, and possibly scattered AI instruction files).

Both paths use the same MIGRATION-GUIDE.md steps (1–9), but the work inside those steps is fundamentally different.

---

## The Core Distinction

| Dimension | Greenfield | Brownfield |
|-----------|-----------|------------|
| Starting state | Empty workspace, new domain | Existing repo, existing processes |
| REPLACE files | Written from first principles | Capture existing conventions FIRST |
| CUSTOMIZE files | Define intended toolchain | Map corporate tools that already exist |
| Prior-art discovery | Nothing to find | Non-trivial archaeology required |
| Migration risk | Low | High — existing conventions must be respected |
| First step | Write domain model | Audit existing instructions and artifacts |
| Generator risk | None — no existing files to overwrite | Must reconcile with existing tool-native files |

---

## Greenfield OpenSpec

### What Greenfield Means

A greenfield workspace is one where:

- No architecture artifacts exist yet (no specs, no ADRs, no solution designs)
- No AI instruction files exist (no `copilot-instructions.md`, no `.cursorrules`, no `.windsurfrules`)
- No team conventions have been established in documentation
- You are free to choose and define all standards from the start

### Step-by-Step Greenfield Path

**Before Step 6 (Customize)**

Copy `.openspec/` from the blueprint workspace as-is. Because there is no existing domain to audit, you move directly to writing your domain model.

**Step 6 — REPLACE files: Write from first principles**

This is the highest-value work in a greenfield. You are defining what the AI knows about your domain. Cover:

- Domain model: what systems/services exist, what they own, how they communicate
- Data ownership boundaries: which system owns which data, who may read it
- Safety-critical defaults: what must never fail silently
- Role definition: what the agent does and explicitly does not do
- Architecture standards: naming conventions, decision record format, diagram notation, quality model
- Toolchain order: which tools to run first, which data they return

Because nothing exists yet, you have full freedom. Use the template stubs in `MIGRATION-GUIDE.md` Step 6.2 directly.

**Step 6 — CUSTOMIZE files: Design for intended toolchain**

If you know your corporate toolchain (e.g., Jira + Splunk + GitHub), write the CUSTOMIZE prompts for it now. If you do not yet know, use placeholders and revisit after the first few real changes.

**After Bootstrap**

First changes through `openspec propose` are typically foundational:

- Defining the base data model or API contracts
- Establishing the first ADRs
- Creating the solution folder structure

Because there is no prior art, the `proposal.md` for early changes is unconstrained. The explore workflow (`/opsx-explore`) is useful for thinking through domain model choices before locking them in a proposal.

**Risk Profile**

| Risk | Mitigation |
|------|-----------|
| Instructions too abstract (no real domain yet to ground them) | Work through 2-3 real proposals before finalizing `core-instructions.md` — revise as the domain becomes concrete |
| Over-engineering standards before the domain is understood | Defer MADR/C4/ISO 25010 detail until you have a real architecture decision to make |
| Instructions go stale as the domain grows | Schedule a quarterly review of `core-instructions.md` against what the team has actually built |

---

## Brownfield OpenSpec

### What Brownfield Means

A brownfield workspace is one where:

- Architecture artifacts exist: specs, ADRs, solution designs, capability registries, wiki pages
- Team conventions are established but may be undocumented or only in people's heads
- AI instruction files may already exist — scattered, inconsistent, possibly conflicting
- A toolchain is in use: specific JIRA projects, Splunk dashboards, GitLab groups, internal CLIs
- Existing folder structures and naming conventions must be preserved

### The Discovery Phase (Before Step 6)

In brownfield, Step 6 cannot start until you have completed a discovery phase. Do not write REPLACE files until you have read what already exists.

**What to audit:**

1. Existing AI instruction files in the repo:
   - `.github/copilot-instructions.md`
   - `.cursor/rules/*.mdc` or `.cursorrules`
   - `.windsurfrules`
   - `CLAUDE.md`, `GEMINI.md`
   - Any ad-hoc prompt files, slash commands, or workflow definitions

2. Architecture and process documentation:
   - README files at the repo root and in key subdirectories
   - Onboarding guides, wiki pages, Confluence spaces
   - Existing ADRs or decision log
   - Architecture diagrams and how they are maintained

3. Established conventions:
   - Naming conventions (service names, file names, branch names)
   - Folder structure for solution designs, specs, or documentation
   - PR/MR review checklists
   - Any explicit team agreements about how AI tools should behave

4. Toolchain inventory:
   - Ticketing system (Jira, ADO, Linear) and project keys
   - Log platform (Splunk, Elastic, Datadog) and how it is queried
   - Source control tooling (GitLab, GitHub) and merge request conventions
   - Any internal CLIs or data access scripts

**Output of discovery:** A list of all conventions, constraints, and tool commands that must be encoded into the REPLACE files.

### Step 6 — REPLACE files: Encode existing conventions

The critical difference from greenfield: you are **capturing** what exists, not inventing what should exist. Failure to capture an existing convention means the AI will contradict it.

**`core-instructions.md`**

Write this by consolidating all existing scattered instruction files. For each existing instruction source:

1. Read it
2. Extract the rule or convention
3. Place it in the appropriate section of `core-instructions.md`
4. After generator runs, delete the old file (it is now superseded)

Common consolidation targets:

| Old location | Goes into |
|-------------|----------|
| `.github/copilot-instructions.md` | `core-instructions.md` (domain model, role definition, workflow rules) |
| `.cursorrules` | `core-instructions.md` (same) |
| Ad-hoc prompt files | Appropriate KEEP or CUSTOMIZE prompts |
| Onboarding wiki sections | `core-instructions.md` (tool usage, conventions) |

**Do not discard content.** If existing instruction files contain something you are unsure belongs in the new system, capture it in `core-instructions.md` with a comment. You can tighten it later.

**Path-scoped instructions (architecture, solutions, specs)**

In brownfield, these files must reflect your existing folder structure. If your specs live in `services/openapi/` rather than `architecture/specs/`, the path scope must match your actual structure.

**Agent persona**

The agent name and description must match how the team refers to this role. If the team says "platform engineer" and your agent says "solution architect", the persona feels wrong and the team stops trusting it.

### Step 6 — CUSTOMIZE files: Map existing toolchain

The four CUSTOMIZE prompts (`investigation`, `architecture-review`, `security-review`, `solution-verification`) contain NovaTrek-specific tool commands. Replace every tool command with your actual corporate equivalents:

| NovaTrek example | What to replace it with |
|-----------------|------------------------|
| `python3 scripts/mock-jira-client.py --ticket NTK-XXXXX` | Your Jira REST call, ADO query, or Linear API command |
| `python3 scripts/mock-elastic-searcher.py --service X --level ERROR` | Your Splunk search, CloudWatch Logs Insights query, or Datadog log search |
| `python3 scripts/mock-gitlab-client.py --mr 5001` | Your `gh pr view`, `glab mr view`, or internal CLI |
| NovaTrek service names (svc-check-in, etc.) | Your system or service names |
| NTK-XXXXX ticket format | Your ticket ID format |

If your team uses a search-first principle (check a capability registry or ADR log before proposing), encode that in `architecture-review.prompt.md`.

### Generator Reconciliation (After Step 7)

When you run the generator in a brownfield workspace, it will write to files that already exist. Before committing, compare the generator output against the originals:

```bash
python3 scripts/generate-tool-instructions.py --dry-run
```

For each generated file, check: is there content in the old file that is NOT in the new generator output? If yes, it means something from the discovery phase was missed in the REPLACE files. Go back and add it to the appropriate `.openspec/` source file, then re-run.

Only delete old instruction files AFTER verifying that all their content is captured in the generator output.

### After Bootstrap: The First Brownfield Changes

In brownfield, the first few changes through `openspec propose` should be **documentation changes**, not feature changes. The goal is to bring existing undocumented architecture into the artifact system:

1. Create an ADR for a significant existing decision that was never documented
2. Formalize an existing implicit convention as a written standard
3. Create a solution design for a recently-delivered feature (retroactively)

This serves two purposes: it tests that the workflow works end-to-end, and it starts building the prior-art registry that future proposals will depend on.

**Prior-art discovery in brownfield is non-trivial.** When a developer says "we already decided this", that decision may be in a Confluence page, a Slack thread, an old PR description, or someone's head. The `openspec explore` workflow is valuable here — use it to surface what exists before every new proposal.

**Risk Profile**

| Risk | Mitigation |
|------|-----------|
| Discovery incomplete — AI contradicts established conventions | Spend at least one full session on Step 6 discovery before touching REPLACE files |
| Generator overwrites existing tool-native files with content that doesn't capture everything | Always run `--dry-run` first; reconcile before committing |
| Team doesn't recognize the agent persona | Match agent name and description to actual role language |
| New OpenSpec conventions conflict with old ad-hoc prompts | Delete old tool-native files only after generator output is verified complete |
| Prior art not discoverable by AI | Retroactively create solution designs for key existing decisions as first changes |

---

## Workflow Differences: Propose / Explore / Apply / Archive

### Explore

| Greenfield | Brownfield |
|-----------|------------|
| Envisioning: "What should this system look like?" | Archaeology: "What does this system actually look like?" |
| Freedom to design ideal architecture | Must surface what is real vs documented |
| Explores problem space, options, and trade-offs | Explores gaps between documented and actual behavior |
| Useful before foundational proposals | Useful before every new proposal |

In brownfield, always enter explore mode before a new proposal to answer: "Has this been decided before? Where is the prior art? What are the existing constraints?"

### Propose

| Artifact | Greenfield | Brownfield |
|----------|-----------|------------|
| `proposal.md` | Describes new capability being built | Must also state current state and why the change is needed |
| `design.md` | Designs from scratch | Must address: what breaks, what is the migration path, backward compat |
| `tasks.md` | Pure creation tasks | Includes investigation, migration, deprecation, and validation tasks |

In brownfield, `design.md` must contain a migration strategy section. Changes that alter existing contracts, schemas, or behaviors require explicit backward compatibility analysis.

### Apply

Both greenfield and brownfield use the same apply workflow. The difference is in task complexity:

- Greenfield tasks: create the file, define the schema, write the spec
- Brownfield tasks: update the file (with backward compat), deprecate the old field, notify consumers, validate against existing behavior

### Archive

Identical in both cases. In brownfield, the archive is especially valuable — it becomes the canonical record of why things changed, complementing the existing ADR history.

---

## The Hub-and-Spoke Model in Each Context

The OpenSpec hub-and-spoke model (`.openspec/` as single source of truth, tool-native directories as generated outputs) has different starting conditions:

```
GREENFIELD                        BROWNFIELD

.openspec/                        Existing:
  (written fresh)                   .github/copilot-instructions.md
       │                             .cursorrules
       ▼                             CLAUDE.md
generator                            various prompt files
       │                                    │
       ▼                          Discovery │
.github/   .cursor/   .roo/        phase   │
CLAUDE.md  .windsurfrules          REPLACE files encode ──▶ .openspec/
GEMINI.md                          existing content              │
                                                                 ▼
                                                           generator
                                                                 │
                                                                 ▼
                                                    .github/  .cursor/  .roo/
                                                    CLAUDE.md .windsurfrules
                                                    (old files replaced)
```

---

## Decision Matrix: Which Path Are You On?

Answer these questions to determine your path:

| Question | Yes → | No → |
|---------|-------|------|
| Does `.github/copilot-instructions.md` exist with content? | Brownfield | Possible greenfield |
| Do ADRs or architecture decision records exist? | Brownfield | Possible greenfield |
| Has the team been using AI coding tools with any configured instructions? | Brownfield | Possible greenfield |
| Does the repo have an established folder structure for architecture work? | Brownfield | Possible greenfield |
| Are there existing API specs, solution designs, or capability registries? | Brownfield | Likely greenfield |

If any answer is "Yes", treat the workspace as brownfield and do the discovery phase before Step 6.

---

## Summary Table

| Step | Greenfield | Brownfield |
|------|-----------|------------|
| Pre-Step 6 | None required | Discovery phase: audit all existing instructions, conventions, toolchain |
| Step 6 REPLACE | Write from first principles using template stubs | Consolidate from existing files; encode all discovered conventions |
| Step 6 CUSTOMIZE | Design for intended toolchain | Map to existing corporate tools; match existing tool command patterns |
| Step 6 KEEP | Copy verbatim | Copy verbatim |
| Step 7 Generator | Run and commit | Run `--dry-run` first; reconcile; then run and commit; delete old files |
| First changes | Foundational: domain model, base specs, first ADRs | Documentation: retroactively formalize existing decisions |
| Explore mode | Envision and design | Archaeology and gap analysis |
| Proposal artifacts | Unconstrained; pure creation | Include current state, migration path, backward compat |
| Prior-art discovery | Minimal (nothing exists) | Critical; must be done before every proposal |
| CI setup | From day one | Integrate with existing pipelines; do not replace working CI |
