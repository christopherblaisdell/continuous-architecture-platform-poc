#!/bin/bash
# ===========================================================================
# Generate All Portal Artifacts + Build MkDocs Site
# ===========================================================================
# Single entry point for the portal build pipeline.
# Architects edit YAML metadata + OpenAPI specs, then this script:
#   1. Generates Swagger UI pages from OpenAPI specs
#   2. Generates microservice deep-dive pages (MD + PUML + SVG)
#   3. Generates application pages (MD + PUML + SVG)
#   4. Generates AsyncAPI event pages
#   5. Generates standalone PlantUML diagrams
#   6. Builds MkDocs site
#   7. Copies non-markdown assets into site/ output
#
# Usage:
#   bash portal/scripts/generate-all.sh          # from repo root
#   bash scripts/generate-all.sh                 # from portal/
# ===========================================================================
set -euo pipefail

# Determine repo root (works whether called from repo root or portal/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORTAL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$PORTAL_DIR/.." && pwd)"

echo "============================================================"
echo "NovaTrek Portal — Full Build"
echo "============================================================"
echo "  Repo root: $REPO_ROOT"
echo "  Portal:    $PORTAL_DIR"
echo ""

# ------------------------------------------------------------------
# Step 1: Generate Swagger UI pages from OpenAPI specs
# ------------------------------------------------------------------
echo "[1/7] Generating Swagger UI pages..."
python3 "$SCRIPT_DIR/generate-swagger-pages.py"
echo ""

# ------------------------------------------------------------------
# Step 2: Generate microservice pages (MD + PUML + SVG)
# ------------------------------------------------------------------
echo "[2/7] Generating microservice pages..."
python3 "$SCRIPT_DIR/generate-microservice-pages.py"
echo ""

# ------------------------------------------------------------------
# Step 3: Generate application pages (MD + PUML + SVG)
# ------------------------------------------------------------------
echo "[3/7] Generating application pages..."
python3 "$SCRIPT_DIR/generate-application-pages.py"
echo ""

# ------------------------------------------------------------------
# Step 4: Generate wireframe pages from Excalidraw JSON
# ------------------------------------------------------------------
echo "[4/7] Generating wireframe pages..."
python3 "$SCRIPT_DIR/generate-wireframe-pages.py"
echo ""

# ------------------------------------------------------------------
# Step 5: Generate AsyncAPI event pages
# ------------------------------------------------------------------
echo "[5/10] Generating AsyncAPI event pages..."
python3 "$SCRIPT_DIR/generate-event-pages.py"
echo ""

# ------------------------------------------------------------------
# Step 6: Generate solution design pages
# ------------------------------------------------------------------
echo "[6/10] Generating solution design pages..."
python3 "$SCRIPT_DIR/generate-solution-pages.py"
echo ""

# ------------------------------------------------------------------
# Step 7: Generate business capability pages
# ------------------------------------------------------------------
echo "[7/10] Generating business capability pages..."
python3 "$SCRIPT_DIR/generate-capability-pages.py"
echo ""

# ------------------------------------------------------------------
# Step 8: Generate ticket pages
# ------------------------------------------------------------------
echo "[8/10] Generating ticket pages..."
python3 "$SCRIPT_DIR/generate-ticket-pages.py"
echo ""

# ------------------------------------------------------------------
# Step 9: Generate standalone PlantUML diagrams
# ------------------------------------------------------------------
echo "[9/10] Generating standalone PlantUML diagrams..."
bash "$SCRIPT_DIR/generate-svgs.sh"
echo ""

# ------------------------------------------------------------------
# Step 10: Build MkDocs site
# ------------------------------------------------------------------
echo "[10/10] Building MkDocs site..."
cd "$PORTAL_DIR"
python3 -m mkdocs build

# Copy non-markdown assets that MkDocs does not copy automatically
echo "  Copying assets into site/..."
cp -r docs/services/api site/services/ 2>/dev/null || true
cp -r "$REPO_ROOT/architecture/specs" site/ 2>/dev/null || true
cp -r docs/microservices/svg site/microservices/ 2>/dev/null || true
cp -r docs/applications/svg site/applications/ 2>/dev/null || true

# Copy wireframe assets (SVG + HTML) into matching site directories
for wf_dir in docs/applications/*/wireframes; do
  app_name="$(basename "$(dirname "$wf_dir")")"
  target="site/applications/$app_name/wireframes"
  mkdir -p "$target"
  cp -f "$wf_dir"/*.svg "$target/" 2>/dev/null || true
  cp -f "$wf_dir"/*.html "$target/" 2>/dev/null || true
done

cp -r docs/events-ui site/ 2>/dev/null || true
cp -r docs/diagrams/svg site/diagrams/ 2>/dev/null || mkdir -p site/diagrams && true
cp staticwebapp.config.json site/ 2>/dev/null || true

echo ""
echo "============================================================"
echo "Build complete!"
echo "  Site output: $PORTAL_DIR/site/"
echo "============================================================"
