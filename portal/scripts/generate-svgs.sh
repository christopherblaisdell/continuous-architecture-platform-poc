#!/bin/bash
# Generate SVGs from all PlantUML diagrams
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SRC="$ROOT/phases/phase-1-ai-tool-cost-comparison/workspace/corporate-services/diagrams"
WI="$ROOT/phases/phase-1-ai-tool-cost-comparison/workspace/work-items/tickets"
OUT="$ROOT/portal/docs/diagrams/svg"

mkdir -p "$OUT"

FILES=(
  "$SRC/Sequence/check-in-process-flow.puml"
  "$SRC/Sequence/partner-booking-flow.puml"
  "$SRC/Sequence/reservation-booking-flow.puml"
  "$SRC/Sequence/scheduling-orchestration-flow.puml"
  "$SRC/Components/booking-domain-components.puml"
  "$SRC/Components/guest-domain-components.puml"
  "$SRC/Components/novatrek-component-overview.puml"
  "$SRC/Components/ntk10003-unregistered-checkin-components.puml"
  "$SRC/System/novatrek-system-context.puml"
  "$WI/_NTK-10002-adventure-category-classification/3.solution/i.impacts/impact.1/classification-flow.puml"
  "$WI/_NTK-10003-unregistered-guest-self-checkin/3.solution/i.impacts/impact.1/lookup-orchestration.puml"
)

for f in "${FILES[@]}"; do
  name=$(basename "$f" .puml)
  echo "Generating: $name"
  plantuml -tsvg -o "$OUT" "$f"
  echo "  -> OK"
done

echo ""
echo "Generated $(ls "$OUT"/*.svg | wc -l) SVG files:"
ls -la "$OUT"/*.svg
