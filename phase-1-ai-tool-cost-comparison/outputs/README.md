# Phase 1 Outputs

This directory contains the results of each AI tool execution run, organized by tool and run number.

## Directory Structure

```
outputs/
  copilot/
    001/                    # Run 001
      run-metadata.md       # Timing, cost, summary stats
      workspace-snapshot/   # Git diff of all workspace changes
      results.md            # Quality scoring and analysis
    002/                    # Run 002
      ...
  roo-code/
    001/
      ...
    002/
      ...
```

## Workflow

1. Reset the workspace to baseline before each run
2. Execute the AI tool (paste the execution prompt)
3. Run `../scripts/capture-run.sh <tool> [run-number]` to snapshot results
4. The script copies changed workspace files, generates a diff, and creates a run metadata template
5. Reset workspace again before the next run

## Run Numbering

Run numbers are zero-padded three-digit integers (001, 002, 003, ...). Each number represents one complete execution of all 5 scenarios. If you do not provide a run number, the capture script auto-increments from the last existing run.

## What Gets Captured

| Artifact | Description |
|----------|-------------|
| `run-metadata.md` | Wall-clock time, date, model, cost notes |
| `workspace-diff.patch` | Full `git diff` of workspace changes from baseline |
| `workspace-snapshot/` | Copy of all changed/created files (preserving folder structure) |
| `results.md` | Quality scoring per scenario (copied or created post-run) |
