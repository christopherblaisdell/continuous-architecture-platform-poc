#!/bin/bash

# =============================================================================
# AI Instruction Validation Script
# =============================================================================
#
# Checks that AI instructions are in sync and properly
# configured. Run manually or via pre-commit hook.
#
# Usage:
#   scripts/validate-ai-instructions.sh
#
# Exit codes:
#   0 — all checks passed
#   1 — one or more checks failed
#
# =============================================================================

# =============================================================================
# DEFERRED — not yet activated in this workspace.
#
# This script was copied from cwb-roo-workspace-3 for reference.
# To activate it:
#   1. Verify all expected files exist at the paths checked below
#      (some paths reference files relative to repo root, not open-spec/)
#   2. Run the script from the workspace root: scripts/validate-ai-instructions.sh
#   3. Uncomment the block below and remove this notice
# =============================================================================
echo "[DEFERRED] validate-ai-instructions.sh has not been activated in this workspace yet."
echo "See the comment at the top of this file for activation steps."
exit 0

: <<'DEFERRED'

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
errors=0
warnings=0

# --- Helpers ------------------------------------------------------------------

pass() { echo "  [PASS] $1"; }
fail() { echo "  [FAIL] $1"; errors=$((errors + 1)); }
warn() { echo "  [WARN] $1"; warnings=$((warnings + 1)); }

# --- Check 1: Required files exist -------------------------------------------

echo ""
echo "=== File Existence Checks ==="
echo ""

required_files=(
    ".github/copilot-instructions.md"
    ".clinerules"
    ".ai-instructions/core-instructions.md"
    ".ai-instructions/modes.yaml"
    ".ai-instructions/setup-ai-tools.sh"
    ".github/instructions/prompt-me.instructions.md"
    ".ai-instructions/methodologies/guided-plan-execution.md"
    ".github/instructions/prompt-mirror.instructions.md"
    ".ai-instructions/methodologies/prompt-mirror.md"
    "prompt-mirror/README.md"
)

for f in "${required_files[@]}"; do
    if [ -f "$REPO_ROOT/$f" ]; then
        pass "$f exists"
    else
        fail "$f MISSING"
    fi
done

# --- Check 2: YAML frontmatter in .instructions.md files ---------------------

echo ""
echo "=== YAML Frontmatter Checks ==="
echo ""

for f in "$REPO_ROOT"/.github/instructions/*.instructions.md; do
    [ -e "$f" ] || continue
    filename=$(basename "$f")
    if head -1 "$f" | grep -q '^---$'; then
        if head -10 "$f" | grep -q 'applyTo:'; then
            pass "$filename has valid frontmatter with applyTo"
        else
            fail "$filename has frontmatter but missing applyTo"
        fi
    else
        fail "$filename missing YAML frontmatter (must start with ---)"
    fi
done

# --- Check 3: Paired file content sync ---------------------------------------

echo ""
echo "=== Paired File Sync Checks ==="
echo ""

# prompt-me.instructions.md <-> guided-plan-execution.md
# Strip YAML frontmatter and PAIRED FILE comments, then compare core content
primary_prompt="$REPO_ROOT/.github/instructions/prompt-me.instructions.md"
roo_prompt="$REPO_ROOT/.ai-instructions/methodologies/guided-plan-execution.md"

if [ -f "$primary_prompt" ] && [ -f "$roo_prompt" ]; then
    # Extract body content (skip frontmatter, multi-line HTML blocks, single-line comments, and mode-specific lines)
    # awk '/^<!-- ===/,/-->/' removes DERIVED FILE header blocks (<!-- === ... === -->)
    strip_html_blocks='BEGIN{skip=0} /^<!-- ===/{ skip=1 } skip && /-->$/{ skip=0; next } skip{ next } 1'
    primary_body=$(sed '1,/^---$/d' "$primary_prompt" | awk "$strip_html_blocks" | grep -v '^<!-- ' | grep -v '^$' | grep -v 'Applicable Modes' | sed 's/^[[:space:]]*//')
    roo_body=$(awk "$strip_html_blocks" "$roo_prompt" | grep -v '^<!-- ' | grep -v '^$' | grep -v 'Applicable Modes' | sed 's/^[[:space:]]*//')

    if [ "$primary_body" = "$roo_body" ]; then
        pass "prompt-me.instructions.md and guided-plan-execution.md are in sync"
    else
        fail "prompt-me.instructions.md and guided-plan-execution.md have DRIFTED"
        echo "       Run: diff <(sed '1,/^---$/d' .github/instructions/prompt-me.instructions.md) .ai-instructions/methodologies/guided-plan-execution.md"
    fi
else
    fail "Cannot compare paired files — one or both missing"
fi

# prompt-mirror.instructions.md <-> prompt-mirror.md
primary_mirror="$REPO_ROOT/.github/instructions/prompt-mirror.instructions.md"
roo_mirror="$REPO_ROOT/.ai-instructions/methodologies/prompt-mirror.md"

if [ -f "$primary_mirror" ] && [ -f "$roo_mirror" ]; then
    # Both files should contain the key PAIRED FILE comment
    if grep -q 'PAIRED FILE' "$primary_mirror" && grep -q 'PAIRED FILE' "$roo_mirror"; then
        pass "prompt-mirror.instructions.md and prompt-mirror.md both have PAIRED FILE markers"
    else
        fail "prompt-mirror paired files missing PAIRED FILE markers"
    fi
else
    fail "Cannot compare prompt-mirror paired files — one or both missing"
fi

# --- Check 4: Key rules present in both base instruction files ----------------

echo ""
echo "=== Key Rule Presence Checks ==="
echo ""

primary_base="$REPO_ROOT/.github/copilot-instructions.md"
roo_base="$REPO_ROOT/.clinerules"

key_phrases=(
    "NO EMOJIS"
    "NEVER use dollar values"
    "NEVER use sprint counts"
    "Security-first mindset"
    "hub-and-spoke"
    "conventional commit"
)

for phrase in "${key_phrases[@]}"; do
    in_primary=false
    in_roo=false

    if [ -f "$primary_base" ] && grep -qi "$phrase" "$primary_base"; then
        in_primary=true
    fi
    if [ -f "$roo_base" ] && grep -qi "$phrase" "$roo_base"; then
        in_roo=true
    fi

    if $in_primary && $in_roo; then
        pass "\"$phrase\" present in both base files"
    elif $in_primary && ! $in_roo; then
        fail "\"$phrase\" in copilot-instructions.md but MISSING from .clinerules"
    elif ! $in_primary && $in_roo; then
        fail "\"$phrase\" in .clinerules but MISSING from copilot-instructions.md"
    else
        fail "\"$phrase\" MISSING from both base files"
    fi
done

# --- Check 5A: Derived file headers -----------------------------------------

echo ""
echo "=== Derived File Header Checks ==="
echo ""

derived_files=(
    ".github/copilot-instructions.md"
    ".clinerules"
    ".github/instructions/prompt-me.instructions.md"
    ".github/instructions/prompt-mirror.instructions.md"
    ".github/instructions/plantuml-svg.instructions.md"
)

for f in "${derived_files[@]}"; do
    if grep -q "DERIVED FILE" "$REPO_ROOT/$f" 2>/dev/null; then
        pass "$f has DERIVED FILE header"
    else
        fail "$f is MISSING the DERIVED FILE header — was it edited directly?"
    fi
done

# --- Check 5: Symlink health -------------------------------------------------

echo ""
echo "=== Symlink Health Checks ==="
echo ""

roo_symlink="$HOME/.config/roo/ai-customizations"
if [ -L "$roo_symlink" ]; then
    if [ -e "$roo_symlink" ]; then
        pass "Roo ai-customizations symlink valid"
    else
        fail "Roo ai-customizations symlink BROKEN (target missing)"
    fi
else
    warn "Roo ai-customizations symlink not found (run setup-ai-tools.sh)"
fi

modes_symlink="$HOME/.config/roo/modes.yaml"
if [ -L "$modes_symlink" ]; then
    if [ -e "$modes_symlink" ]; then
        pass "Roo modes.yaml symlink valid"
    else
        fail "Roo modes.yaml symlink BROKEN (target missing)"
    fi
elif [ -f "$modes_symlink" ]; then
    warn "modes.yaml exists but is a regular file, not a symlink (re-run setup-ai-tools.sh)"
else
    warn "modes.yaml not found (run setup-ai-tools.sh)"
fi

vscode_prompts="$HOME/Library/Application Support/Code/User/prompts"
if [ -d "$vscode_prompts" ]; then
    linked=$(find "$vscode_prompts" -maxdepth 1 -type l 2>/dev/null | wc -l | tr -d ' ')
    if [ "$linked" -gt 0 ]; then
        pass "VS Code prompts: $linked symlinked file(s)"
    else
        warn "VS Code prompts directory exists but no symlinks found"
    fi
else
    warn "VS Code prompts directory not found (run setup-ai-tools.sh)"
fi

# --- Check 6: .roomodes staleness --------------------------------------------

echo ""
echo "=== .roomodes Check ==="
echo ""

roomodes="$REPO_ROOT/.roomodes"
if [ -f "$roomodes" ]; then
    if grep -q "cwb-corporate-airgapped" "$roomodes"; then
        warn ".roomodes references stale repo name 'cwb-corporate-airgapped' — consider updating"
    else
        pass ".roomodes does not reference stale repo names"
    fi
else
    pass "No .roomodes file (using global modes.yaml)"
fi

# --- Check 7: OpenSpec initialization ----------------------------------------

echo ""
echo "=== OpenSpec Checks ==="
echo ""

if [ -f "$REPO_ROOT/openspec/config.yaml" ]; then
    pass "openspec/config.yaml exists (OpenSpec initialized)"
else
    fail "openspec/config.yaml missing — run: openspec init"
fi

if [ -f "$REPO_ROOT/.github/prompts/opsx-propose.prompt.md" ]; then
    pass ".github/prompts/opsx-propose.prompt.md exists (Copilot slash commands installed)"
else
    fail ".github/prompts/opsx-propose.prompt.md missing — run: openspec init"
fi

if [ -f "$REPO_ROOT/openspec/specs/ai-instruction-governance/spec.md" ]; then
    pass "AI instruction governance spec exists"
else
    fail "openspec/specs/ai-instruction-governance/spec.md missing"
fi

# --- Summary ------------------------------------------------------------------

echo ""
echo "============================================"
echo "  Validation Summary"
echo "============================================"
echo ""
echo "  Errors:   $errors"
echo "  Warnings: $warnings"
echo ""

if [ "$errors" -gt 0 ]; then
    echo "  RESULT: FAILED — fix the errors above"
    exit 1
else
    if [ "$warnings" -gt 0 ]; then
        echo "  RESULT: PASSED with warnings"
    else
        echo "  RESULT: PASSED"
    fi
    exit 0
fi

DEFERRED
