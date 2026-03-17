# Phase 1 Outputs

This directory contains the results of each AI tool execution run, organized by tool and run number.

## Key Principle: Every Run is Fresh

Each execution of an AI tool prompt produces a **completely new set of artifacts** in a **new numbered folder**. The AI never reuses output from a previous run — it always generates fresh content from scratch.

- The **workspace** (`../workspace/`) is **read-only input** — specs, source code, templates, mock scripts, and seed ticket reports
- All **generated output** goes into `outputs/<tool>/<RUN>/`
- No workspace reset is needed between runs

## Directory Structure

```
outputs/
  copilot/
    001/                    # Run 001
      work-items/tickets/   # All scenario output (ticket artifacts)
      corporate-services/   # Modified Swagger specs, diagrams (Scenario 4)
      run-summary.md        # AI-generated post-execution summary
      run-metadata.md       # Timing, cost, summary stats (human-filled)
      results.md            # Quality scoring and analysis (human-filled)
    002/                    # Run 002
      ...
  roo-code/
    001/
      ...
    002/
      ...
```

## Run Folder Contents

Each run folder mirrors the workspace structure for output artifacts:

| Path within run folder | Source |
|------------------------|--------|
| `work-items/tickets/_NTK-10005-.../` | Scenario 1 output |
| `work-items/tickets/_NTK-10002-.../` | Scenario 2 output |
| `work-items/tickets/_NTK-10004-.../` | Scenario 3 output |
| `work-items/tickets/_NTK-10001-.../` | Scenario 4 output |
| `corporate-services/services/svc-trail-management.yaml` | Scenario 4 modified spec |
| `corporate-services/diagrams/Components/...` | Scenario 4 and 5 diagrams |
| `run-summary.md` | AI-generated execution summary |
| `run-metadata.md` | Human: timing, cost data |
| `results.md` | Human: quality scores per scenario |

## Workflow

1. Open a new AI chat session (Copilot or Roo Code)
2. Paste the execution prompt — the AI auto-detects the next run number and creates the folder
3. AI reads from `workspace/` and writes all output to `outputs/<tool>/<RUN>/`
4. After completion, fill in `run-metadata.md` and `results.md`
5. Commit the run

## Run Numbering

Run numbers are zero-padded three-digit integers (001, 002, 003, ...). The AI auto-increments by listing existing folders and adding 1 to the highest number.
