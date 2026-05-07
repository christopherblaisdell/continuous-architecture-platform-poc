# Synthetic Exemplar Backlog

> **SYNTHETIC WORKSPACE ONLY — NOT BLUEPRINT CONTENT.**
>
> This file tracks carry-over tasks and deferred work specific to the **NovaTrek Adventures synthetic exemplar workspace**. These items are not part of the portable EaC Blueprint. They are the housekeeping work needed to keep this synthetic workspace valid as a proof-of-concept for the blueprint it validates.
>
> Corporate **EaC Adoption Instance** workspaces do NOT inherit this file. They inherit only the clean blueprint documents: [EVERYTHING-AS-CODE-FRAMEWORK.md](EVERYTHING-AS-CODE-FRAMEWORK.md), [TRANSFORMATION-PLAN.md](TRANSFORMATION-PLAN.md), [AI-INSTRUCTIONS-AS-CODE.md](AI-INSTRUCTIONS-AS-CODE.md), and the assessment template in [CURRENT-STATE-ASSESSMENT.md](CURRENT-STATE-ASSESSMENT.md).

---

## Phase 5 Carry-Over — AI Instructions Governance

These tasks complete the Pillar 14 work deferred in a prior session against this synthetic workspace.

- [ ] Fix `scripts/validate-ai-instructions.sh`:
  - [ ] Remove `prompt-mirror/README.md` from the required files list
  - [ ] Update or remove the global symlink check (`~/.config/roo/ai-customizations`)
  - [ ] Remove the DEFERRED block from the script
- [ ] Run the fixed script against this exemplar workspace; resolve any remaining failures
- [ ] Add the script to a `validate-ai-instructions.yml` GitHub Actions workflow in this repo
- [ ] Run the first real OpenSpec change cycle in this exemplar (`/opsx:propose → /opsx:apply → /opsx:archive`) with a test rule
- [ ] Evaluate adding Cursor `.mdc` and Windsurf `.windsurfrules` as additional derived targets in the hub-and-spoke

---

## General Exemplar Maintenance

- [ ] Keep `docs/everything-as-code/` export-clean — no synthetic NovaTrek service names, ticket IDs, or workspace-specific file paths should appear in the blueprint documents; only in this backlog and in the explicitly-labeled exemplar assessment
- [ ] Verify the CURRENT-STATE-ASSESSMENT exemplar scores stay in sync with actual workspace state after each blueprint revision
- [ ] When any phase of the blueprint is refined, run through the corresponding exemplar pillar to confirm the synthetic workspace still validates the updated pattern
