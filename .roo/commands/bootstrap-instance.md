# Bootstrap Instance

Bootstrap the OpenSpec AI customization system in this workspace from the migration blueprint

Bootstrap the OpenSpec AI customization system in this workspace by following the migration guide from the source workspace.

**Input**: Provide the path to the source workspace (the NovaTrek blueprint workspace). Example: `/bootstrap-instance source=/path/to/continuous-architecture-platform-poc-2`

**What you are about to do**

You are setting up the hub-and-spoke AI instruction architecture in THIS workspace:
- `.openspec/` will become the single source of truth for all AI tool instructions
- `scripts/generate-tool-instructions.py` will distribute `.openspec/` to all AI tool-native formats
- Generated outputs will be written to `.github/`, `.cursor/`, `.roo/`, `.windsurfrules`, `CLAUDE.md`, `GEMINI.md`, `.foundry/`

---

**Steps**

## Step 1: Read the migration guide

Read the full migration guide from the source workspace:

```
{source_workspace}/.openspec/MIGRATION-GUIDE.md
```

Confirm you have read all 9 steps and all 4 appendices before proceeding.

---

## Step 2: Identify the target workspace

The target workspace is the current workspace (the one the user has open in VS Code). Confirm the workspace root path.

Ask the user: "Is this workspace at `{current_workspace_path}`? Confirm before I copy any files."

Wait for confirmation.

---

## Step 3: Execute the migration steps

Work through each step in the migration guide in order. For each step:

1. State which step you are executing (e.g., "Executing Step 2: Copy Source Files")
2. Run the commands or create the files
3. Confirm the step is complete before moving to the next

**Step 2 (Copy Source Files):** Copy `.openspec/`, `scripts/generate-tool-instructions.py`, and `.github/workflows/validate-instructions.yml` from the source workspace to this workspace. Use exact paths from the migration guide.

**Step 3 (Install openspec CLI):** Run `openspec --version`. If the CLI is not installed or is the wrong version, run `npm install -g openspec@1.3.1` and verify.

**Step 4 (Configure openspec CLI):** Run the three `openspec config set` commands. Verify with `openspec config list`.

**Step 5 (Initialize workspace):** Run `openspec init` or create `openspec/changes/archive/` and `openspec/specs/` manually. Verify both directories exist.

**Step 6 (Customize for your domain):** Pause here. Present the user with the classification table from the migration guide (REPLACE / CUSTOMIZE / KEEP for all 21 `.openspec/` files). Ask:

> "Before I run the generator, do you want to customize the domain-specific files now (Step 6), or run the generator first with NovaTrek placeholder content and customize afterward?"

Wait for the user's answer before proceeding to Step 7.

**Step 7 (Run the generator):** Run `python3 scripts/generate-tool-instructions.py`. If errors occur, diagnose and fix before continuing.

**Step 8 (Wire up CI):** Confirm `.github/workflows/validate-instructions.yml` was copied in Step 2. Review the `paths:` trigger list with the user and update it if their workspace uses different directories.

**Step 9 (Verify):** Work through all 6 verification gates in order. Report pass/fail for each gate. Do not mark the bootstrap complete until all 6 gates pass.

---

## Step 4: Commit

Once all 6 verification gates pass:

```bash
git add -A
git commit -m "chore: bootstrap OpenSpec AI customization system"
```

Ask the user if they want to push.

---

## Completion

Report which files were created or modified, confirm the `.openspec/` directory is now the source of truth in this workspace, and remind the user that the next action is Step 6 (domain customization) if they deferred it.
