# Wireframe Management Guide

Quick reference for creating and managing wireframes in the NovaTrek Architecture Portal.

## Source Location

Wireframe source files live under `architecture/wireframes/{app}/` — the same root as all other architect-edited artifacts (specs, metadata, events). CI generates SVG, HTML, and Markdown pages into `portal/docs/applications/{app}/wireframes/`.

## Editing Wireframes

### Option 1: VS Code (Recommended)
1. Open any `.excalidraw` file from `architecture/wireframes/{app}/` in VS Code
2. VS Code will show a preview pane (Excalidraw Editor extension)
3. Edit directly with live preview
4. Save (Cmd+S)

### Option 2: Web Editor (excalidraw.com)
1. Navigate to [excalidraw.com](https://excalidraw.com)
2. Open → paste contents of `.excalidraw` JSON file OR upload the file
3. Design your screen
4. Export as JSON
5. Save JSON back to the `.excalidraw` file in the repo

## Publishing

Commit only the `.excalidraw` source file and push to `main`. CI automatically:

1. Runs `generate-wireframe-pages.py` (reads from `architecture/wireframes/`)
2. Generates SVG + HTML + MD into `portal/docs/applications/{app}/wireframes/`
3. Builds MkDocs site and deploys to NovaTrek Architecture Portal

No manual regeneration or committing of generated files required.

## Current Wireframes

### Web Guest Portal
- **Source**: `architecture/wireframes/web-guest-portal/check-in-confirmation.excalidraw`
- Guest check-in completion flow with guest info, safety checklist, wristband ID

**See on site**: [Check-in Confirmation](https://architecture.novatrek.cc/applications/web-guest-portal/wireframes/check-in-confirmation/)

### Web Operations Dashboard
- **Source**: `architecture/wireframes/web-ops-dashboard/live-tracking.excalidraw`
- Real-time adventure map with guest positions, alerts, and stats

**See on site**: [Live Tracking](https://architecture.novatrek.cc/applications/web-ops-dashboard/wireframes/live-tracking/)

### Mobile Guest App
- **Source**: `architecture/wireframes/app-guest-mobile/adventure-selection.excalidraw`
- Adventure listings with filters, availability, and booking

**See on site**: [Adventure Selection](https://architecture.novatrek.cc/applications/app-guest-mobile/wireframes/adventure-selection/)

## Adding New Wireframes

1. Create new `.excalidraw` file:
   ```bash
   # Name it kebab-case, descriptive
   touch architecture/wireframes/{app}/feature-screen-name.excalidraw
   ```

2. Design in VS Code or excalidraw.com

3. If using web editor, export JSON and save to the file above

4. Add nav entry to `portal/mkdocs.yml` under the app's Wireframes section

5. Commit and push:
   ```bash
   git add architecture/wireframes/{app}/feature-screen-name.excalidraw portal/mkdocs.yml
   git commit -m "Add wireframe: feature-screen-name"
   git push
   ```

CI handles all generation and deployment.

## File Structure

```
architecture/wireframes/              ← SOURCE (architect-edited)
├── web-guest-portal/
│   └── check-in-confirmation.excalidraw
├── web-ops-dashboard/
│   └── live-tracking.excalidraw
└── app-guest-mobile/
    └── adventure-selection.excalidraw

portal/docs/applications/             ← GENERATED (by CI)
├── web-guest-portal/
│   └── wireframes/
│       ├── check-in-confirmation.md     ← Generated wrapper
│       ├── check-in-confirmation.svg    ← Generated preview
│       └── check-in-confirmation.html   ← Generated viewer
├── web-ops-dashboard/
│   └── wireframes/
│       ├── live-tracking.md
│       ├── live-tracking.svg
│       └── live-tracking.html
└── app-guest-mobile/
    └── wireframes/
        ├── adventure-selection.md
        ├── adventure-selection.svg
        └── adventure-selection.html
```

## Excalidraw Quick Tips

- **Shapes**: Rectangles, circles, lines, arrows, text labels
- **Grouping**: Select multiple elements → Group (Ctrl+G / Cmd+G)
- **Fonts**: Change font size in top toolbar
- **Colors**: Click shape → fill/stroke color picker
- **Export**: File → Export to export as SVG, PNG, or copy as JSON
- **Keyboard shortcuts**: `?` to see all shortcuts

## Linking in Architecture Documents

When proposing UI/UX changes in solution designs, reference wireframes by source path:

```markdown
### User Interface

See wireframe source: `architecture/wireframes/web-guest-portal/check-in-confirmation.excalidraw`

The user flow is:
1. Guest scans wristband (captured in `#wristbandRfid`)
...
```

## Troubleshooting

**Wireframe doesn't render on the site:**
- Ensure filename is kebab-case: `my-screen-name.excalidraw`
- Run `python3 portal/scripts/generate-wireframe-pages.py` again
- Check MkDocs nav includes the `.md` file under the correct app section

**Interactive HTML viewer doesn't load:**
- Excalidraw CDN might be blocked — check browser console for CORS errors
- Ensure `staticwebapp.config.json` allows external scripts

**JSON export from excalidraw.com doesn't work:**
- Excalidraw JSON is located under `elements` and `appState` keys
- Just copy the full JSON and paste into the `.excalidraw` file

---

*Last updated: 2026-03-06*
