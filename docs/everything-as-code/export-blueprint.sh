#!/usr/bin/env bash
# export-blueprint.sh
#
# Copies the EaC Adoption Blueprint to a target corporate workspace.
# Run this from inside the synthetic exemplar workspace to seed a new Instance.
#
# Usage:
#   ./export-blueprint.sh --target /path/to/corporate/workspace
#   ./export-blueprint.sh --target /path/to/corporate/workspace --dry-run
#
# What the script does:
#   - Copies all portable blueprint documents to <target>/docs/everything-as-code/
#   - Copies CURRENT-STATE-ASSESSMENT.md as an exemplar template (replace with a real assessment)
#   - Skips SYNTHETIC-EXEMPLAR-BACKLOG.md and blank placeholder files (NovaTrek-specific only)
#
# After running, complete the steps printed by this script in the target workspace.

set -euo pipefail

TARGET=""
DRY_RUN=false
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  echo "Usage: $0 --target /path/to/corporate/workspace [--dry-run]" >&2
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) TARGET="$2"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    *) usage ;;
  esac
done

[[ -z "$TARGET" ]] && usage
[[ ! -d "$TARGET" ]] && { echo "Error: target directory does not exist: $TARGET" >&2; exit 1; }

DEST="$TARGET/docs/everything-as-code"

echo "EaC Blueprint Export"
echo "  Source : $SCRIPT_DIR"
echo "  Target : $DEST"
echo "  Mode   : $( $DRY_RUN && echo "dry-run (no files written)" || echo "live" )"
echo ""

copy_file() {
  local src="$1" dest_path="$2"
  local label
  label="$(basename "$src")"
  if $DRY_RUN; then
    echo "  [dry-run] would copy: $label"
  else
    mkdir -p "$(dirname "$dest_path")"
    cp "$src" "$dest_path"
    echo "  copied : $label"
  fi
}

warn_missing() {
  echo "  WARNING: blueprint file not found, skipping: $1" >&2
}

# ---------------------------------------------------------------------------
# Category 1 — Pure blueprint documents (target-agnostic, copy as-is)
# ---------------------------------------------------------------------------
BLUEPRINT_FILES=(
  "README.md"
  "EVERYTHING-AS-CODE-FRAMEWORK.md"
  "TRANSFORMATION-PLAN.md"
  "AI-INSTRUCTIONS-AS-CODE.md"
  "DEEP-RESEARCH-PROMPT-EAC-MATURITY-MODEL.md"
  "DEEP-RESEARCH-PROMPT-AI-NATIVE-ARCHITECTURE.md"
  "standardized.taxonomy.of.ai.instructions.etc.deep.research.response.md"
)

echo "Blueprint documents:"
for f in "${BLUEPRINT_FILES[@]}"; do
  src="$SCRIPT_DIR/$f"
  if [[ -f "$src" ]]; then
    copy_file "$src" "$DEST/$f"
  else
    warn_missing "$f"
  fi
done

echo ""

# ---------------------------------------------------------------------------
# Category 2 — Synthetic exemplar template (copy; Instance team replaces content)
# ---------------------------------------------------------------------------
echo "Exemplar templates (replace content with real assessments):"
EXEMPLAR_TEMPLATES=(
  "CURRENT-STATE-ASSESSMENT.md"
)
for f in "${EXEMPLAR_TEMPLATES[@]}"; do
  src="$SCRIPT_DIR/$f"
  if [[ -f "$src" ]]; then
    copy_file "$src" "$DEST/$f"
  else
    warn_missing "$f"
  fi
done

echo ""

# ---------------------------------------------------------------------------
# Category 3 — Excluded (NovaTrek-specific; not exported to Instance)
# ---------------------------------------------------------------------------
echo "Excluded (NovaTrek-specific — not exported):"
EXCLUDED=(
  "SYNTHETIC-EXEMPLAR-BACKLOG.md"
  "DEEP-RESEARCH-PROMPT-EAC-MATURITY-MODEL-RESPONSE.md"
  "DEEP-RESEARCH-PROMPT-AI-NATIVE-ARCHITECTURE-RESPONSE.md"
)
for f in "${EXCLUDED[@]}"; do
  echo "  skipped: $f"
done

echo ""
echo "Export $( $DRY_RUN && echo "simulation" || echo "complete" )."
echo ""
echo "Next steps in the corporate workspace ($TARGET):"
echo ""
echo "  1. cd $DEST"
echo "  2. Open TRANSFORMATION-PLAN.md — complete the Bootstrap section:"
echo "        a. Run the pillar selection exercise (mark each of the 35 pillars In Scope / Out of Scope / Future)"
echo "        b. Identify the pilot pillar"
echo "  3. Replace CURRENT-STATE-ASSESSMENT.md with a real assessment of your workspace"
echo "     (keep the structure; replace all NovaTrek findings with your actual findings)"
echo "  4. Author the adoption ADR in your decisions/ folder"
echo "     (use the MADR template; declare which pillars are in scope for Wave 1)"
echo "  5. Commit docs/everything-as-code/ to version control"
echo "  6. Add the EaC track to your roadmap"
echo ""
