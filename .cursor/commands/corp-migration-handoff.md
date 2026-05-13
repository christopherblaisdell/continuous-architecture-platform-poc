---
name: /corp-migration-handoff
id: corp-migration-handoff
category: Workflow
description: 
---

# Greenfield/Brownfield Framework — Corporate Workspace Migration

You are being asked to migrate a set of files from a synthetic reference workspace
(NovaTrek Adventures) into this corporate workspace. All files exist in the NovaTrek
workspace at the paths listed below. Your job is to read each source file and create
it at the corresponding target path in this corporate workspace.

---

## What This Is

The greenfield/brownfield framework is a set of OpenSpec instruction files and prompts
that help AI reason correctly about whether architectural artifacts already exist
(brownfield) or are being created from scratch (greenfield). The synthetic NovaTrek
workspace was used to develop and validate this framework. Now it travels to this
corporate workspace, where the actual state of architecture artifacts needs to be
discovered and substituted for the synthetic assumptions.

This migration is **additive only**. It does not touch any existing OpenSpec
infrastructure in this workspace (skills, generator, instruction axes, prompts that
are already here). It only adds the 5 files listed below.

---

## Source Workspace

The NovaTrek synthetic workspace is at:

```
/Users/christopherblaisdell/Documents/continuous-architecture-platform-poc-2
```

If this path is not accessible from your current session, ask the user to confirm
the correct path before proceeding.

---

## Files to Copy

For each entry: read the source file at the NovaTrek path, then create it at the
target path in this corporate workspace. Do not modify file contents during the copy
unless a transformation is noted.

### File 1 — Greenfield vs Brownfield Instruction Axis

| | Path |
|-|------|
| Source | `{NOVATREK_ROOT}/.openspec/GREENFIELD-VS-BROWNFIELD.md` |
| Target | `.openspec/GREENFIELD-VS-BROWNFIELD.md` |
| Transformation | None — copy verbatim |

**Skip if already present.** Check whether `.openspec/GREENFIELD-VS-BROWNFIELD.md`
exists in this corporate workspace before creating it. If it exists, report its
presence and move to the next file.

---

### File 2 — All Concerns Stub (the main deliverable)

| | Path |
|-|------|
| Source | `{NOVATREK_ROOT}/.openspec/GREENFIELD-VS-BROWNFIELD-ALL-CONCERNS-CORP-STUB.md` |
| Target | `.openspec/GREENFIELD-VS-BROWNFIELD-ALL-CONCERNS.md` |
| Transformation | Rename on copy (the stub travels as the working document) |

**Note on existing file:** If `.openspec/GREENFIELD-VS-BROWNFIELD-ALL-CONCERNS.md`
already exists in this corporate workspace, do NOT overwrite it — report the conflict
and ask the user whether to proceed.

This file contains `PENDING DISCOVERY` markers throughout. After all 5 files are
in place, the user will run `.openspec/prompts/corp-discovery.prompt.md` to audit
the actual state of architecture artifacts, then rewrite the `PENDING DISCOVERY`
blocks in-place with real findings.

---

### File 3 — Migration Plan

| | Path |
|-|------|
| Source | `{NOVATREK_ROOT}/.openspec/CORP-MIGRATION-PLAN.md` |
| Target | `.openspec/CORP-MIGRATION-PLAN.md` |
| Transformation | None — copy verbatim |

---

### File 4 — Corporate Discovery Prompt

| | Path |
|-|------|
| Source | `{NOVATREK_ROOT}/.openspec/prompts/corp-discovery.prompt.md` |
| Target | `.openspec/prompts/corp-discovery.prompt.md` |
| Transformation | None — copy verbatim |

**Skip if already present.**

---

### File 5 — Deep Research Brownfield Adoption Prompt

| | Path |
|-|------|
| Source | `{NOVATREK_ROOT}/.openspec/prompts/deep-research-brownfield-adoption.prompt.md` |
| Target | `.openspec/prompts/deep-research-brownfield-adoption.prompt.md` |
| Transformation | None — copy verbatim |

**Skip if already present.**

---

## After Copying

Once all 5 files are in place, report a summary:

```
Files created:    [list]
Files skipped:    [list with reason]
Conflicts found:  [list with what was found]
```

Then tell the user:

> **Next step:** Open `.openspec/prompts/corp-discovery.prompt.md` and run it in
> this corporate workspace. That prompt will audit the actual state of architecture
> artifacts across 12 axes and produce `.openspec/CORP-DISCOVERY-FINDINGS.md`.
> After discovery is complete, rewrite the `PENDING DISCOVERY` blocks in
> `.openspec/GREENFIELD-VS-BROWNFIELD-ALL-CONCERNS.md` in-place based on the findings.

---

## What NOT to Copy

Do not copy any other `.openspec/` files from the NovaTrek workspace. All other
OpenSpec infrastructure (skills, generator, instruction axes, core prompts, security
review prompt, solution verification prompt, investigation prompt) is already present
in this corporate workspace and must not be overwritten.

Specifically, do NOT copy:
- `scripts/generate-tool-instructions.py` — already present
- `.openspec/MIGRATION-GUIDE.md` — already present
- `.openspec/prompts/bootstrap-instance.prompt.md` — already present
- `.openspec/prompts/security-review.prompt.md` — CUSTOMIZE file, NovaTrek-specific
- `.openspec/prompts/solution-verification.prompt.md` — CUSTOMIZE file, NovaTrek-specific
- `.openspec/prompts/investigation.prompt.md` — REPLACE file, NovaTrek-specific
- `.openspec/instructions/` — all instruction files, already present or NovaTrek-specific
- `.openspec/skills/` — all skill files, already present
- Any file in `architecture/`, `decisions/`, `config/`, `portal/` — all NovaTrek-specific
