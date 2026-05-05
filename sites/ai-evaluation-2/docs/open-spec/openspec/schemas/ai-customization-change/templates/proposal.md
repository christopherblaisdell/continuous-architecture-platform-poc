## Why

<!-- What rule, standard, or methodology is changing and why.
     What problem does this solve? Why now? -->

## What Changes

<!-- Describe the change to the AI customization rules.
     Be specific: which rule is being added, modified, or removed. -->

## Affected Canonical Files

<!-- List the .ai-customizations/ files that will be edited directly.
     These are the ONLY files that should be manually changed. -->

- [ ] `.ai-customizations/` <!-- path to canonical file -->

## Affected Derived Files

<!-- These files are updated automatically by scripts/sync-ai-customizations.sh.
     DO NOT edit them directly. List which ones will change as a result. -->

- `.clinerules` (always regenerated)
- `.github/copilot-instructions.md` (always regenerated)
<!-- Add .github/instructions/*.instructions.md if a paired methodology file changes -->

## Capabilities

### Modified Capabilities
- `ai-customization-governance`: updating AI customization rules

## Impact

<!-- How will this change affect AI behavior in Copilot and/or Roo?
     Any rules being overridden, any risk of conflicting instructions? -->

## Governance Reference

This change is governed by:
`openspec/specs/ai-customization-governance/spec.md`

Requirements satisfied:
- [ ] REQ-GOV-001: canonical files only — no direct edits to derived files
- [ ] REQ-GOV-002: change proposed via OpenSpec before any file is modified
- [ ] REQ-GOV-003: sync script will be called to update derived files atomically
- [ ] REQ-GOV-004: validate-ai-customizations.sh will be run before commit
