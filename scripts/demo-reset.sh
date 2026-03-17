#!/bin/bash
# =============================================================================
# Demo Reset Script
# =============================================================================
# Resets the workspace to a clean state after running a demo.
#
# Usage:
#   Before demo: ./scripts/demo-reset.sh save     (saves current clean state)
#   After demo:  ./scripts/demo-reset.sh reset     (restores to saved state)
#   Check state: ./scripts/demo-reset.sh status    (shows what would be reset)
#
# The demo may create or modify files during live demonstration. This script
# uses git to restore the workspace to the exact state saved before the demo.
# =============================================================================

set -euo pipefail

DEMO_TAG="demo-checkpoint"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

usage() {
    echo "Usage: $0 {save|reset|status}"
    echo ""
    echo "  save    — Tag current commit as demo checkpoint (run BEFORE demo)"
    echo "  reset   — Hard reset to checkpoint and clean untracked files (run AFTER demo)"
    echo "  status  — Show changes since checkpoint (what would be reset)"
    exit 1
}

save_checkpoint() {
    # Verify clean working tree
    if [ -n "$(git status --porcelain)" ]; then
        echo "ERROR: Working tree is not clean. Commit or stash changes first."
        git status --short
        exit 1
    fi

    # Tag current commit
    git tag -f "$DEMO_TAG" HEAD
    echo "Checkpoint saved at $(git rev-parse --short HEAD)"
    echo "Branch: $(git branch --show-current)"
    echo ""
    echo "You can now run the demo. When done, run:"
    echo "  ./scripts/demo-reset.sh reset"
}

reset_to_checkpoint() {
    # Verify checkpoint exists
    if ! git rev-parse "$DEMO_TAG" >/dev/null 2>&1; then
        echo "ERROR: No demo checkpoint found. Run './scripts/demo-reset.sh save' first."
        exit 1
    fi

    local checkpoint_sha
    checkpoint_sha=$(git rev-parse --short "$DEMO_TAG")
    local current_sha
    current_sha=$(git rev-parse --short HEAD)

    echo "Resetting to checkpoint $checkpoint_sha (current: $current_sha)"
    echo ""

    # Show what will be discarded
    echo "Changes being discarded:"
    git diff --stat "$DEMO_TAG" HEAD 2>/dev/null || true
    echo ""
    echo "Untracked files being removed:"
    git clean -n -d 2>/dev/null || true
    echo ""

    # Reset
    git checkout "$(git branch --show-current)" 2>/dev/null
    git reset --hard "$DEMO_TAG"
    git clean -fd

    echo ""
    echo "Reset complete. Workspace is back to checkpoint $checkpoint_sha"
}

show_status() {
    if ! git rev-parse "$DEMO_TAG" >/dev/null 2>&1; then
        echo "No demo checkpoint saved."
        echo "Current state:"
        git status --short
        exit 0
    fi

    local checkpoint_sha
    checkpoint_sha=$(git rev-parse --short "$DEMO_TAG")
    echo "Demo checkpoint: $checkpoint_sha"
    echo ""
    echo "Changes since checkpoint:"
    git diff --stat "$DEMO_TAG" HEAD 2>/dev/null || true
    echo ""
    echo "Uncommitted changes:"
    git status --short
    echo ""
    echo "Untracked files:"
    git clean -n -d 2>/dev/null || true
}

case "${1:-}" in
    save)   save_checkpoint ;;
    reset)  reset_to_checkpoint ;;
    status) show_status ;;
    *)      usage ;;
esac
