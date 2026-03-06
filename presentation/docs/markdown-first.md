# Markdown-First: Extending What Teams Already Do

## Many Teams Already Author in Text Formats — Extending the Pattern

Many architecture practices already author OpenAPI specs in YAML and diagrams in PlantUML or Mermaid — text formats checked into version control. The platform extends this practice to **solution designs, ADRs, and impact assessments** in Markdown, completing the set of version-controlled architecture artifacts.

---

## Extending Version-Controlled Artifacts

| Artifact | Current State (Industry Pattern) | With the Platform |
|----------|:---:|:---:|
| **OpenAPI specs** | Version-controlled (gated) | Version-controlled (same) + AI-assisted updates |
| **Diagram source** (PlantUML, Mermaid) | Version-controlled | Version-controlled (same) + auto-rendered to portal |
| **Solution designs** | Manual wiki or ticket attachments | Markdown in version control + auto-published |
| **Architecture Decision Records** | In ticket branches (not discoverable) | Markdown in version control + global searchable log |
| **Impact assessments** | Wiki or email | Markdown in version control |
| **Service documentation** | Manual wiki updates (often skipped) | Auto-generated from specs |
| **Cross-service links** | Manually maintained in wiki | Auto-generated from dependency graph |

---

## Current Industry Pattern

```
1. Architect updates OpenAPI specs and diagram source files in version control
2. Changes are checked in (governance gate — this typically works well)
3. Architect is supposed to update wiki service pages manually
4. Sometimes this happens, often it doesn't
5. Solution design lives in a ticket branch or wiki — not discoverable later
6. ADRs stay in ticket context, never promoted to a global log
7. After deployment, nobody reconciles design intent vs actual implementation
```

## Enhanced Workflow

```
1. AI agent reads the version-controlled repository (specs, diagrams, previous designs)
2. AI scaffolds solution design from template in VS Code
3. Architect reviews and refines (with AI assistance)
4. Specs, diagrams, and solution design committed together
5. Pull request for architecture review with line-by-line diffs
6. Merge to main triggers automated publishing to browsable portal
7. Optionally synced to wiki via API (no manual step)
8. AI reads the design in future sessions (full context)
9. PROMOTE step reconciles design intent with actual implementation
```

---

## Every Design Artifact in This POC is Markdown

The proof of concept produced 39 files across 5 scenarios — all in Markdown, all version-controlled alongside the specs and diagrams already in Git:

- **Solution designs** — arc42-structured Markdown with embedded PlantUML
- **Architecture Decision Records** — MADR format (Markdown Any Decision Record)
- **Impact assessments** — service-level analysis in Markdown tables
- **User stories** — acceptance criteria in Markdown lists
- **Investigation reports** — evidence-grounded analysis with code block citations
- **Implementation guidance** — code patterns in fenced code blocks
- **Simple explanations** — non-technical summaries for stakeholders

None of these required Word. None required Confluence. All are version-controlled, AI-readable, and auto-publishable.

---

## Confluence Compatibility

!!! info "This replaces the manual Confluence step — not Confluence itself"
    The platform can publish to **both** MkDocs and Confluence from the same source. The difference: updates happen automatically on `git push` instead of relying on a voluntary manual step.

``` mermaid
flowchart LR
    A[Markdown in Git\nsingle source of truth] --> B[MkDocs Build]
    A --> C[Confluence API Sync]
    B --> D[Architecture Portal\nalways current]
    C --> E[Confluence Pages\nalways current]

    style A fill:#00897b,color:#fff
    style D fill:#ff8f00,color:#fff
    style E fill:#1565c0,color:#fff
```

The key difference: **publishing is automated**, not voluntary. Git remains the source of truth (as it already is for specs), and Confluence becomes a read-only mirror. This means:

- Architecture changes go through pull request review (extending what we already do for specs)
- The AI reads the Git version (always available, always current)
- Confluence stays up to date automatically (no manual step to skip)
- Browsable documentation always reflects the latest checked-in artifacts

---

## Migration Path

This builds on what architects already do — **no disruption required**:

| Phase | Action | Disruption |
|-------|--------|:---:|
| **Already done** | Specs and diagrams are in Git | None — this is the existing process |
| **Start** | New solution designs and ADRs authored in Markdown in the same repo | None — same content, text format |
| **Automatic** | Browsable portal generated from Git on every push | None — replaces a manual step that was often skipped |
| **Optional** | Confluence sync from the same Markdown source | None — additive, not replacement |
| **Never required** | Converting all historical Confluence content | Not needed — only active designs matter |

<div class="key-insight" markdown>
**The migration cost is near zero.** Architects already author in text formats (YAML specs, PlantUML). Markdown is the same skill. And the AI handles formatting automatically.
</div>

<div class="cta-box" markdown>

### How does publishing work?

[Automated Publishing: Replace the Manual Confluence Step](publishing-pipeline.md)

</div>
