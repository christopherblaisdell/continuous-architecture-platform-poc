# OpenSpec: Greenfield vs Brownfield — Corporate Workspace Migration Plan

**Date:** 2026-05-13
**Source workspace (synthetic):** `/Users/christopherblaisdell/Documents/continuous-architecture-platform-poc-2`
**Target:** Your actual corporate workspace

---

## Why This Migration Is Needed

The `GREENFIELD-VS-BROWNFIELD-ALL-CONCERNS.md` document was written while looking only at this synthetic NovaTrek workspace. It makes assumptions that may not match your corporate reality:

| Assumption in Current Document | What It Might Actually Be |
|-------------------------------|--------------------------|
| "No formal ADR registry exists" | You may have ADRs in Confluence, a wiki, or a docs folder |
| "No formal capability taxonomy" | You may have a service catalog, an EA model, or team-defined domains |
| "Existing diagrams in non-PlantUML format" | You may use Structurizr, draw.io, Miro, Lucidchart, Visio, or none at all |
| "Swagger specs must be imported" | Your specs may already be in a dedicated repo, may not exist at all, or may be auto-generated and never manually maintained |
| "Confluence contains solution designs" | Your solution history may be in Notion, Confluence, a wiki, a SharePoint, or engineering blogs |
| "Event schemas live in code" | You may have a schema registry (Confluent, AWS Glue), AsyncAPI files, or no formal schema tracking |
| Mock JIRA, Elastic, GitLab tools | Your actual tools may be Jira Cloud, Datadog, GitHub, Azure DevOps, ServiceNow, or something else entirely |
| "CI/CD pipeline exists" | You may use GitHub Actions, Azure DevOps, Jenkins, GitLab CI, or a combination |
| "BDD/Gherkin infrastructure does not exist" | You may have a mature test pyramid or none of it |

The goal of this migration is to replace every one of these assumptions with evidence from your actual corporate workspace, and then rewrite the greenfield/brownfield analysis document to reflect reality.

---

## What This Migration Accomplishes

> NOTE: The target corporate workspace already has OpenSpec fully in place. This migration is ADDITIVE — it does not re-bootstrap OpenSpec. It migrates only the greenfield/brownfield framework files and the discovery tooling.

1. Adds the greenfield/brownfield framework documents to the corporate workspace
2. Runs a structured discovery in the corporate workspace to audit the actual state of each artifact axis
3. Rewrites `GREENFIELD-VS-BROWNFIELD-ALL-CONCERNS.md` based on real findings — no more synthetic assumptions
4. Establishes the customization backlog for any domain-specific instruction files that need updating

---

## File Inventory: What Goes, What Stays

### Files That Travel Verbatim (KEEP — no NovaTrek content)

> NOTE: Since OpenSpec is already in place in the corporate workspace, most of these files are already present there. They are listed here for completeness and for comparison — if the synthetic workspace version contains improvements or corrections, review and selectively update the corporate copy.

| File | Source Path | Action |
|------|-------------|--------|
| MIGRATION-GUIDE.md | `.openspec/MIGRATION-GUIDE.md` | Compare, update if improved |
| GREENFIELD-VS-BROWNFIELD.md | `.openspec/GREENFIELD-VS-BROWNFIELD.md` | Copy if not present in corp |
| github-urls.instructions.md | `.openspec/instructions/github-urls.instructions.md` | Already present — no action |
| prompt-me.instructions.md | `.openspec/instructions/prompt-me.instructions.md` | Already present — no action |
| prompt-me-copyable.md | `.openspec/instructions/prompt-me-copyable.md` | Already present — no action |
| deep-research.prompt.md | `.openspec/prompts/deep-research.prompt.md` | Already present — no action |
| deep-research-brownfield-adoption.prompt.md | `.openspec/prompts/deep-research-brownfield-adoption.prompt.md` | Copy if not present in corp |
| bootstrap-instance.prompt.md | `.openspec/prompts/bootstrap-instance.prompt.md` | Already present — no action |
| opsx-propose.prompt.md | `.openspec/prompts/opsx-propose.prompt.md` | Already present — no action |
| opsx-apply.prompt.md | `.openspec/prompts/opsx-apply.prompt.md` | Already present — no action |
| opsx-explore.prompt.md | `.openspec/prompts/opsx-explore.prompt.md` | Already present — no action |
| opsx-archive.prompt.md | `.openspec/prompts/opsx-archive.prompt.md` | Already present — no action |
| openspec-propose SKILL.md | `.openspec/skills/openspec-propose/SKILL.md` | Already present — no action |
| openspec-apply-change SKILL.md | `.openspec/skills/openspec-apply-change/SKILL.md` | Already present — no action |
| openspec-archive-change SKILL.md | `.openspec/skills/openspec-archive-change/SKILL.md` | Already present — no action |
| openspec-explore SKILL.md | `.openspec/skills/openspec-explore/SKILL.md` | Already present — no action |
| Generator script | `scripts/generate-tool-instructions.py` | Already present — no action |
| CI validation workflow | `.github/workflows/validate-instructions.yml` | Already present — no action |

### Files That Travel as Stubs (REPLACE — domain-specific, must be rewritten for corp)

These files contain NovaTrek-specific content. They travel as empty stubs with section headings. The corporate workspace AI fills them in after running the discovery prompt.

| File | Why It Needs Replacement |
|------|-------------------------|
| `core-instructions.md` | Contains the NovaTrek Adventures domain model, service names, mock tool commands, and NovaTrek-specific safety rules |
| `architecture.instructions.md` | Contains NovaTrek security context, data ownership rules for specific NovaTrek services |
| `architecture-solutions.instructions.md` | Contains NovaTrek solution workflow, folder structure referencing NovaTrek naming conventions |
| `architecture-specs.instructions.md` | Contains NovaTrek-specific API design rules and backward compatibility guidance |
| `investigation.prompt.md` | Hard-coded NovaTrek mock tool commands (python3 scripts/mock-jira-client.py, etc.) |
| `architecture-review.prompt.md` | References NovaTrek service names |
| `security-review.prompt.md` | References NovaTrek data ownership policies |
| `solution-verification.prompt.md` | References NovaTrek folder paths |

Stub templates for each of these are available in `MIGRATION-GUIDE.md` Step 6.2.

### Files That Travel as Draft / Discovery-Pending

| File | Status in Corp Workspace |
|------|------------------------|
| `GREENFIELD-VS-BROWNFIELD-ALL-CONCERNS.md` | Travel as a draft with "PENDING DISCOVERY" markers. Run the corp discovery prompt, then rewrite each section in place. |
| `CORP-MIGRATION-PLAN.md` (this file) | Travel to corp workspace for reference. Update with real workspace path when known. |
| `corp-discovery.prompt.md` | Travel as the executable starting prompt. Run it first in the corporate workspace. |

### Files That Stay (NovaTrek Only — Do Not Copy)

| File | Why |
|------|-----|
| `agents/novatrek-solution-architect.agent.md` | NovaTrek-specific agent persona — replace with your role |
| `.github/copilot-instructions.md` | Generated from NovaTrek content — regenerate from scratch in corp workspace |
| `CLAUDE.md`, `GEMINI.md`, `.windsurfrules` | Generated outputs — regenerate in corp workspace |
| `.cursor/`, `.roo/`, `.foundry/` | Generated outputs — regenerate in corp workspace |
| Everything in `architecture/`, `phases/`, `services/` | NovaTrek-specific artifacts — no corporate value |

---

## Migration Phases

### Phase 1: Prepare for Migration (this workspace)

All migration artifacts have been created in the NovaTrek workspace. No script or export directory is needed. The handoff is driven by a prompt.

**Files produced in this workspace (narrow scope — additive only):**
- `.openspec/GREENFIELD-VS-BROWNFIELD.md` — generic axis guide, clean, travels verbatim
- `.openspec/GREENFIELD-VS-BROWNFIELD-ALL-CONCERNS-CORP-STUB.md` — stub with PENDING DISCOVERY markers; travels as `GREENFIELD-VS-BROWNFIELD-ALL-CONCERNS.md` in the corp workspace
- `.openspec/CORP-MIGRATION-PLAN.md` — this file
- `.openspec/prompts/corp-discovery.prompt.md` — AI audit prompt for the corporate workspace
- `.openspec/prompts/deep-research-brownfield-adoption.prompt.md` — supplementary research prompt
- `.openspec/prompts/corp-migration-handoff.prompt.md` — the handoff prompt that drives Phase 2

**Verify before handing off:**
- [ ] `corp-discovery.prompt.md` is complete and self-contained (no NovaTrek references)
- [ ] `GREENFIELD-VS-BROWNFIELD-ALL-CONCERNS-CORP-STUB.md` contains zero synthetic assumptions (all replaced with PENDING DISCOVERY markers)
- [ ] `corp-migration-handoff.prompt.md` references the correct source paths

---

### Phase 2: Copy Files to the Corporate Workspace

Open the corporate workspace in your AI tool. Give it the contents of `.openspec/prompts/corp-migration-handoff.prompt.md` as a new conversation.

That prompt tells the AI:
- Which 5 files to read from the NovaTrek workspace (source paths provided)
- Where to create each file in the corporate workspace (target paths provided)
- Which files to skip if already present
- Which files to stop on if a conflict is detected
- What to do after all files are in place

The AI will report which files were created, which were skipped, and whether any conflicts were found.

**Deliverables from Phase 2:**
- Up to 5 new files present in the corporate `.openspec/` directory
- Existing instruction files, prompts, skills, and generator untouched

---

### Phase 3: Run the Corporate Discovery Prompt

Open the corporate workspace in your AI tool. Run the contents of `.openspec/prompts/corp-discovery.prompt.md` as a new conversation.

The discovery prompt instructs the AI to:
1. Audit the actual state of the corporate workspace across all 10 axes from the Starting Position table
2. Examine existing files, directories, and configurations — not assume
3. Return structured findings in a format that maps directly to `GREENFIELD-VS-BROWNFIELD-ALL-CONCERNS.md`
4. Flag gaps, uncertainties, and anything it cannot determine from the workspace alone

**Do not skip this phase.** Without it, you are substituting one set of synthetic assumptions for another.

**Deliverables from Phase 3:**
- AI returns a structured discovery report for each axis
- You review the report for accuracy — add what the AI could not find (things that exist only in people's heads)
- Discovery report saved as `.openspec/CORP-DISCOVERY-FINDINGS.md` in the corporate workspace

---

### Phase 4: Rewrite the ALL-CONCERNS Document

Using the real findings from Phase 3, rewrite `.openspec/GREENFIELD-VS-BROWNFIELD-ALL-CONCERNS.md` in the corporate workspace.

For each axis in the Starting Position table, update:
- The State column (Greenfield / Brownfield / Institutional knowledge / etc.)
- The Notes column with real, accurate observations
- The corresponding section body with real guidance specific to your environment

Remove all synthetic assumptions. Where you are genuinely uncertain, mark the entry "Unknown — verify with team" rather than guessing.

**Deliverables from Phase 4:**
- Updated `GREENFIELD-VS-BROWNFIELD-ALL-CONCERNS.md` with zero NovaTrek assumptions
- Starting Position table reflects the actual state of the corporate architecture practice

---

### Phase 5: Customize the Instruction Files

For each REPLACE file, use `MIGRATION-GUIDE.md` Step 6.2 template stubs as scaffolding. Fill in:
- Your organization's domain model
- Your actual services, teams, and boundaries
- Your actual tool commands (not mock Python scripts)
- Your actual data ownership rules
- Your actual safety-critical defaults

Order of priority for customization (do these first):
1. `core-instructions.md` — the AI knows nothing useful until this exists
2. `investigation.prompt.md` — replace mock tool commands with real tool CLI commands or API queries
3. `architecture-specs.instructions.md` — needed before the first API contract proposal
4. `architecture-solutions.instructions.md` — needed before the first solution design

**Deliverables from Phase 5:**
- At minimum, `core-instructions.md` and `investigation.prompt.md` are populated with real content
- AI can now run a proposal without hallucinating domain details

---

### Phase 6: Run the Generator

```bash
cd /path/to/corporate-workspace
python3 scripts/generate-tool-instructions.py
```

Verify that the tool-native output files were created correctly for each AI tool you use.

```bash
python3 scripts/generate-tool-instructions.py --check  # CI gate — exits 1 if outputs are stale
```

**Deliverables from Phase 6:**
- `.github/copilot-instructions.md` populated with real domain content
- `CLAUDE.md`, `GEMINI.md`, `.windsurfrules` generated (if those tools are used)
- Generator runs clean with no errors

---

## Inaccurate Assumptions to Replace

This is the authoritative list of things in `GREENFIELD-VS-BROWNFIELD-ALL-CONCERNS.md` that are based on synthetic assumptions and must be verified and replaced in the corporate version.

### In "Our Starting Position" Table

| Row | Assumption to Verify |
|-----|---------------------|
| AI instruction infrastructure | Assumed greenfield — verify no `copilot-instructions.md`, `.cursorrules`, or other instruction files exist |
| OpenAPI / Swagger specs | Assumed brownfield (specs exist) — verify location, format, count, and whether they are current vs stale |
| Component diagrams | Assumed brownfield in non-PlantUML format — verify tool (Miro/Lucidchart/Structurizr/draw.io/Visio/none) |
| Sequence diagrams | Same as component diagrams |
| ADRs | Assumed "institutional knowledge only" — verify whether any ADR-like docs exist in Confluence, wiki, or docs folders |
| Capability model | Assumed none — verify whether any service catalog, EA model, or domain taxonomy exists |
| Solution designs | Assumed in Confluence — verify the actual location and whether Confluence is the right answer |
| Test standards | Assumed informal conventions — verify actual test infrastructure (frameworks, BDD, contract testing, etc.) |
| AsyncAPI / event specs | Assumed "live in code" — verify whether a schema registry, AsyncAPI files, or event catalog exists |
| CI/CD pipeline | Assumed exists — identify the actual CI tool and pipeline structure |

### In the "OpenAPI / Swagger Specifications" Section

- The "auto-generated specs" warning references springdoc / Django REST Framework — these are synthetic. Identify your actual code-gen toolchain.
- "Import all existing Swagger files into `architecture/specs/`" — the target path is assumed. Verify the correct target directory for your corporate workspace.

### In the "Institutional Knowledge" Sections

- "Start at ADR-001" — if your corp workspace already has ADRs in any form, the numbering must follow whatever already exists.
- "Populate `architecture/metadata/capabilities.yaml`" — the path is NovaTrek-specific. Identify the correct metadata location for your corporate workspace.
- "Reference Confluence URLs in the requirements section" — Confluence is assumed. Identify the actual prior-art location.

### In the "Workflow Adjustments" Section

- Both adjustments are likely correct in principle but the specific folder paths and file names need to be updated to match the corporate workspace structure.

---

## The Discovery Prompt

The self-contained discovery prompt lives at:

```
.openspec/prompts/corp-discovery.prompt.md
```

This is the file to open in the corporate workspace AI tool and run as a fresh conversation. It produces the structured findings needed for Phase 3 and 4 above.
