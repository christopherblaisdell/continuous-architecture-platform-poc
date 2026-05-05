---
applyTo: "**/*.puml,**/*.svg,**/generate-review-svgs.py"
---

<!-- ============================================================
     DERIVED FILE — DO NOT EDIT DIRECTLY
     Canonical source: .ai-instructions/methodologies/plantuml-svg-workflow.md
     To make changes: /opsx:propose "description of change"
     Then run: scripts/sync-ai-instructions.sh
     Validation: scripts/validate-ai-instructions.sh
     Governance: openspec/specs/ai-instruction-governance/spec.md
     ============================================================ -->

# PlantUML SVG Generation Rules

## CRITICAL: PlantUML Version Compatibility

**PlantUML 1.2026.2+ generates SVGs that do not render correctly in Confluence.** The SVGs look fine locally but break when published.

### Rules

1. **Never call `/opt/homebrew/bin/plantuml` directly** — it uses the latest Homebrew version which is incompatible with Confluence.

2. **For UPT-193355 review SVGs**, always use the generation script:
   ```
   python3 scripts/generate-review-svgs.py
   ```
   This script uses the pinned PlantUML 1.2025.4 JAR, handles color variable fixes, and extracts/renames all diagrams correctly.

3. **For corporate architecture artifacts** — generate SVGs in-situ in the corporate repo folder, then copy to the ticket workspace. Never generate from a renamed or copied PUML outside the corporate repo:
   ```bash
   # Step 1: Generate in the PUML's own folder (so include.puml footer uses the correct filename)
   cd external-repos/architecture/udx-architecture-artifacts/diagrams/Service/
   java -jar /opt/homebrew/Cellar/plantuml/plantuml-1.2025.4.jar -tsvg ms-<service>.puml

   # Step 2: Copy resulting SVGs to the ticket workspace
   cp "<SVG Title>.svg" /path/to/ticket/3.solution/<NNx-description.svg>

   # Step 3: Delete all generated SVGs from the corporate repo
   rm -f *.svg
   git clean -fd .
   ```
   The `include.puml` file in `udx-architecture-artifacts` generates a diagram footer that uses the source PUML filename. If SVGs are generated outside the corporate repo folder (or from renamed/copied files), the footer is incorrect. The corporate repo must contain only official architecture artifacts — no generated SVGs.

4. **For any other SVG generation**, use the pinned JAR directly:
   ```
   java -jar /opt/homebrew/Cellar/plantuml/plantuml-1.2025.4.jar -tsvg <file.puml>
   ```
   Must run from the PUML file's parent directory so `!include ../include.puml` resolves.

5. **Never regenerate individual SVGs by hand** when a generation script exists — always use the script. It handles edge cases (color variable substitution, directory context, diagram extraction by title) that manual commands miss.

### Pinned Version

| Version | Status | Notes |
|---------|--------|-------|
| 1.2025.4 | **Use this** | Confluence-compatible SVGs |
| 1.2026.2+ | **Do not use** | SVGs break in Confluence |

### JAR Location

```
/opt/homebrew/Cellar/plantuml/plantuml-1.2025.4.jar
```

## Current-State vs Target-State Diagram Changes

When modifying an existing sequence diagram (e.g., replacing a data source), the target-state diagram must be a **near-copy** of the current-state with only the changed lines modified. Do not rewrite from scratch, abbreviate, or use `ref` blocks for unchanged sections. The line count difference should be minimal (< 10%).

Use green-tinted notes (`#DAF7A6`) to annotate changes in the target-state diagram.

## Side-by-Side Embedding in Solution Designs

Embed current and target state diagrams in a **markdown comparison table**:

```markdown
| Current State — [Label] | Target State — [Label] |
|---|---|
| ![Current State](path/to/current.svg) | ![Target State](path/to/target.svg) |
| `operationId: current_op` | `operationId: target_op` |
| Source: [file.puml (L###)](path) | Source: [file.puml (L###)](path) |
```
