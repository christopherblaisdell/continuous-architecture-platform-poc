#!/usr/bin/env bash
# capture-run.sh — Snapshot workspace changes into the outputs directory after an AI tool run.
#
# Usage:
#   ./scripts/capture-run.sh <tool> [run-number]
#
# Arguments:
#   tool         "copilot" or "roo-code"
#   run-number   Optional 3-digit run number (e.g., 001). Auto-increments if omitted.
#
# Prerequisites:
#   - Run from the repository root (continuous-architecture-platform-poc/)
#   - Workspace changes are still present (do NOT reset before capturing)
#
# What it does:
#   1. Determines the next run number (or uses the one provided)
#   2. Creates the run directory under outputs/<tool>/<run-number>/
#   3. Generates a git diff patch of all workspace changes from baseline
#   4. Copies all changed/created workspace files into workspace-snapshot/
#   5. Creates a run-metadata.md template for the human to fill in
#   6. Copies the results file if it exists in the workspace

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
BASELINE_COMMIT="e83f83e"
WORKSPACE_REL="phase-1-ai-tool-cost-comparison/workspace"
OUTPUTS_DIR="$REPO_ROOT/phase-1-ai-tool-cost-comparison/outputs"

# --- Argument parsing ---

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <copilot|roo-code> [run-number]"
    echo ""
    echo "Examples:"
    echo "  $0 copilot           # Auto-assigns next run number"
    echo "  $0 roo-code 002      # Explicitly sets run 002"
    exit 1
fi

TOOL="$1"
if [[ "$TOOL" != "copilot" && "$TOOL" != "roo-code" ]]; then
    echo "ERROR: Tool must be 'copilot' or 'roo-code'. Got: $TOOL"
    exit 1
fi

TOOL_DIR="$OUTPUTS_DIR/$TOOL"

# --- Determine run number ---

if [[ $# -ge 2 ]]; then
    RUN_NUM="$2"
else
    # Auto-increment: find the highest existing run number and add 1
    LAST_RUN=$(find "$TOOL_DIR" -maxdepth 1 -type d -name '[0-9][0-9][0-9]' 2>/dev/null | sort | tail -1 | xargs basename 2>/dev/null || echo "000")
    if [[ "$LAST_RUN" == "000" ]] || [[ -z "$LAST_RUN" ]]; then
        RUN_NUM="001"
    else
        NEXT=$((10#$LAST_RUN + 1))
        RUN_NUM=$(printf "%03d" "$NEXT")
    fi
fi

RUN_DIR="$TOOL_DIR/$RUN_NUM"

if [[ -d "$RUN_DIR" ]]; then
    echo "WARNING: Run directory already exists: $RUN_DIR"
    echo "Contents will be overwritten."
    read -p "Continue? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
fi

echo "=== Capturing $TOOL run $RUN_NUM ==="
echo "  Run directory: $RUN_DIR"

mkdir -p "$RUN_DIR/workspace-snapshot"

# --- 1. Generate git diff patch ---

echo "  Generating workspace diff from baseline ($BASELINE_COMMIT)..."
cd "$REPO_ROOT"

git diff "$BASELINE_COMMIT" -- "$WORKSPACE_REL/" > "$RUN_DIR/workspace-diff.patch" 2>/dev/null || true

# Also capture newly added files (untracked)
git diff --cached "$BASELINE_COMMIT" -- "$WORKSPACE_REL/" >> "$RUN_DIR/workspace-diff.patch" 2>/dev/null || true

DIFF_LINES=$(wc -l < "$RUN_DIR/workspace-diff.patch" | tr -d ' ')
echo "  Diff: $DIFF_LINES lines"

# --- 2. Copy changed/created files into snapshot ---

echo "  Copying changed files to workspace-snapshot/..."

# Get list of changed files (tracked changes from baseline)
CHANGED_FILES=$(git diff --name-only "$BASELINE_COMMIT" -- "$WORKSPACE_REL/" 2>/dev/null || true)

# Get list of new files (added after baseline)
NEW_FILES=$(git diff --name-only --diff-filter=A "$BASELINE_COMMIT"..HEAD -- "$WORKSPACE_REL/" 2>/dev/null || true)

# Get untracked files in workspace
UNTRACKED_FILES=$(git ls-files --others --exclude-standard -- "$WORKSPACE_REL/" 2>/dev/null || true)

# Combine all file lists, deduplicate
ALL_FILES=$(echo -e "$CHANGED_FILES\n$NEW_FILES\n$UNTRACKED_FILES" | sort -u | grep -v '^$' || true)

FILE_COUNT=0
for FILE in $ALL_FILES; do
    if [[ -f "$REPO_ROOT/$FILE" ]]; then
        # Preserve directory structure under workspace-snapshot
        REL_PATH="${FILE#$WORKSPACE_REL/}"
        DEST_DIR="$RUN_DIR/workspace-snapshot/$(dirname "$REL_PATH")"
        mkdir -p "$DEST_DIR"
        cp "$REPO_ROOT/$FILE" "$DEST_DIR/"
        FILE_COUNT=$((FILE_COUNT + 1))
    fi
done

echo "  Copied $FILE_COUNT files"

# --- 3. Generate diff stats ---

STATS=$(git diff --stat "$BASELINE_COMMIT" -- "$WORKSPACE_REL/" 2>/dev/null | tail -1 || echo "no changes detected")

# --- 4. Create run-metadata.md ---

echo "  Creating run-metadata.md..."

TOOL_DISPLAY="GitHub Copilot"
if [[ "$TOOL" == "roo-code" ]]; then
    TOOL_DISPLAY="Roo Code + Kong AI"
fi

cat > "$RUN_DIR/run-metadata.md" << EOF
# Run $RUN_NUM Metadata — $TOOL_DISPLAY

| Field | Value |
|-------|-------|
| **Tool** | $TOOL_DISPLAY |
| **Run Number** | $RUN_NUM |
| **Date** | $(date '+%Y-%m-%d') |
| **Model** | _fill in_ |
| **Start Time** | _fill in (HH:MM)_ |
| **End Time** | _fill in (HH:MM)_ |
| **Wall Clock Duration** | _fill in (minutes)_ |
| **Scenarios Completed** | _fill in (X / 5)_ |

## Cost

| Metric | Value |
|--------|-------|
| **Subscription Cost** | _fill in_ |
| **Token Cost (if measurable)** | _fill in or N/A_ |
| **Total Run Cost** | _fill in_ |

## Diff Summary

\`\`\`
$STATS
\`\`\`

## Files Changed

$FILE_COUNT files captured in \`workspace-snapshot/\`.

## Notes

_Add any observations, issues, or corrections encountered during this run._

EOF

# --- 5. Copy results file if it exists ---

RESULTS_FILE=""
if [[ "$TOOL" == "copilot" ]]; then
    RESULTS_FILE="$REPO_ROOT/$WORKSPACE_REL/phase-1-copilot-results.md"
elif [[ "$TOOL" == "roo-code" ]]; then
    RESULTS_FILE="$REPO_ROOT/$WORKSPACE_REL/phase-1-roo-code-results.md"
fi

if [[ -n "$RESULTS_FILE" && -f "$RESULTS_FILE" ]]; then
    echo "  Copying results file..."
    cp "$RESULTS_FILE" "$RUN_DIR/results.md"
fi

# --- Done ---

echo ""
echo "=== Capture complete ==="
echo "  Run directory: $RUN_DIR"
echo "  Files captured: $FILE_COUNT"
echo "  Diff lines: $DIFF_LINES"
echo ""
echo "Next steps:"
echo "  1. Fill in run-metadata.md with timing and cost data"
echo "  2. Score each scenario and update results.md"
echo "  3. Reset workspace:  git checkout $BASELINE_COMMIT -- $WORKSPACE_REL/"
echo "  4. Run data isolation audit: ./scripts/audit-data-isolation.sh"
