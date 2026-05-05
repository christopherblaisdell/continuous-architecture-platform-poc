## 1. Edit Canonical Files

<!-- Edit only files in .ai-instructions/ — never derived files directly -->

- [ ] 1.1 Edit `.ai-instructions/` <!-- canonical file path --> as specified in `design.md`
<!-- Add additional canonical file edits here if needed -->

## 2. Sync Derived Files

- [ ] 2.1 Run `scripts/sync-ai-instructions.sh` to propagate changes to all derived files
- [ ] 2.2 Confirm the script exits 0 (it runs validate-ai-instructions.sh internally)

## 3. Verify

- [ ] 3.1 Run `scripts/validate-ai-instructions.sh` — confirm Errors: 0, Warnings: 0
- [ ] 3.2 Spot-check at least one derived file to confirm the change is reflected

## 4. Commit

- [ ] 4.1 Stage all changed files: canonical source(s) and all regenerated derived files
- [ ] 4.2 Commit with message: `feat(ai-customizations): <!-- change description -->`
