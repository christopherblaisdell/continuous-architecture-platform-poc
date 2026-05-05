#!/bin/bash

# =============================================================================
# AI Tools Global Setup Script
# =============================================================================
#
# This script configures Roo Code and VS Code to use
# the source-controlled AI instructions from this repository.
#
# What it does:
#   1. Roo Code:   Symlinks .ai-instructions/ → ~/.config/roo/ai-customizations
#                  Creates modes.yaml if missing
#   2. VS Code:    Symlinks user-prompts/*.prompt.md (and *.agent.md, *.instructions.md)
#                  → ~/Library/Application Support/Code/User/prompts/
#
# After running this script, all customizations are available from ANY
# VS Code workspace on this machine. Changes to the source files in this
# repo are immediately reflected everywhere — no drift, no duplication.
#
# Usage:
#   chmod +x .ai-instructions/setup-ai-tools.sh
#   ./.ai-instructions/setup-ai-tools.sh
#
# =============================================================================

set -euo pipefail

# --- Configuration -----------------------------------------------------------

# TODO: Update SOURCE_DIR to the absolute path of .ai-instructions/ in this workspace
# before running this script. Example:
#   SOURCE_DIR="/path/to/your-new-workspace/.ai-instructions"
SOURCE_DIR="/Users/christopherblaisdell/Documents/continuous-architecture-platform-poc-2/sites/ai-evaluation-2/docs/open-spec/.ai-instructions"
ROO_CONFIG_DIR="$HOME/.config/roo"
MODES_YAML="$ROO_CONFIG_DIR/modes.yaml"
VSCODE_PROMPTS_DIR="$HOME/Library/Application Support/Code/User/prompts"
USER_PROMPTS_DIR="$SOURCE_DIR/user-prompts"

# --- Helpers ------------------------------------------------------------------

create_symlink() {
    local target="$1"
    local link_path="$2"
    local label="$3"

    if [ -L "$link_path" ]; then
        local existing_target
        existing_target=$(readlink "$link_path")
        if [ "$existing_target" = "$target" ]; then
            echo "  [OK] $label already linked correctly"
            return
        fi
        echo "  Updating existing symlink for $label..."
        rm "$link_path"
    elif [ -e "$link_path" ]; then
        echo "  [WARN] $link_path exists and is not a symlink — skipping"
        echo "         Remove it manually and re-run this script"
        return
    fi

    ln -s "$target" "$link_path"
    echo "  [OK] $label linked"
}

# --- Preflight ----------------------------------------------------------------

echo ""
echo "============================================"
echo "  AI Tools Global Setup"
echo "============================================"
echo ""

if [ ! -d "$SOURCE_DIR" ]; then
    echo "[ERROR] Source directory not found: $SOURCE_DIR"
    exit 1
fi

# --- Part 1: Roo Code --------------------------------------------------------

echo "[1/2] Roo Code Configuration"
echo ""

mkdir -p "$ROO_CONFIG_DIR"

create_symlink "$SOURCE_DIR" "$ROO_CONFIG_DIR/ai-customizations" "ai-customizations -> Roo config"

# Symlink modes.yaml from source-controlled file
MODES_SOURCE="$SOURCE_DIR/modes.yaml"
if [ -f "$MODES_SOURCE" ]; then
    create_symlink "$MODES_SOURCE" "$MODES_YAML" "modes.yaml -> Roo config"
else
    echo "  [WARN] modes.yaml not found at $MODES_SOURCE"
    echo "         Create .ai-instructions/modes.yaml and re-run"
fi

# Verify setup
echo ""
echo "[2/2] VS Code User-Level Prompts"
echo ""

mkdir -p "$VSCODE_PROMPTS_DIR"

if [ -d "$USER_PROMPTS_DIR" ]; then
    file_count=0
    for file in "$USER_PROMPTS_DIR"/*.prompt.md "$USER_PROMPTS_DIR"/*.agent.md "$USER_PROMPTS_DIR"/*.instructions.md; do
        [ -e "$file" ] || continue
        filename=$(basename "$file")
        create_symlink "$file" "$VSCODE_PROMPTS_DIR/$filename" "$filename"
        file_count=$((file_count + 1))
    done

    if [ "$file_count" -eq 0 ]; then
        echo "  [INFO] No .prompt.md, .agent.md, or .instructions.md files found in user-prompts/"
    else
        echo "  Linked $file_count file(s) to VS Code user prompts"
    fi
else
    echo "  [WARN] user-prompts/ directory not found at $USER_PROMPTS_DIR"
    echo "         Create it and add .prompt.md files, then re-run"
fi

# --- Verification -------------------------------------------------------------

echo ""
echo "============================================"
echo "  Verification"
echo "============================================"
echo ""

errors=0

# Roo symlink
if [ -L "$ROO_CONFIG_DIR/ai-customizations" ] && [ -e "$ROO_CONFIG_DIR/ai-customizations" ]; then
    echo "  [OK] Roo: ai-customizations symlink valid"
else
    echo "  [FAIL] Roo: ai-customizations symlink broken or missing"
    errors=$((errors + 1))
fi

# Roo modes.yaml
if [ -f "$MODES_YAML" ]; then
    echo "  [OK] Roo: modes.yaml exists"
else
    echo "  [FAIL] Roo: modes.yaml not found"
    errors=$((errors + 1))
fi

# VS Code prompts
linked_prompts=$(find "$VSCODE_PROMPTS_DIR" -maxdepth 1 -type l 2>/dev/null | wc -l | tr -d ' ')
echo "  [OK] VS Code: $linked_prompts symlinked file(s) in user prompts dir"

echo ""
if [ "$errors" -eq 0 ]; then
    echo "  Setup complete — no errors"
else
    echo "  Setup completed with $errors error(s) — review above"
fi

echo ""
echo "  Summary:"
echo "    Roo config:     $ROO_CONFIG_DIR/ai-customizations -> $SOURCE_DIR"
echo "    Roo modes:      $MODES_YAML"
echo "    VS Code prompts: $VSCODE_PROMPTS_DIR/"
echo "    Source of truth: $SOURCE_DIR"
echo ""
echo "🚀 Next steps:"
echo "   1. Restart VS Code"
echo "   2. Open any project and use Roo"
echo "   3. The AI instructions will be automatically loaded"
echo ""
echo "💡 To update customizations:"
echo "   1. Edit files in: $SOURCE_DIR"
echo "   2. Commit changes to Git"
echo "   3. Changes apply immediately to all Roo instances"