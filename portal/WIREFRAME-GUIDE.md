# Wireframe Management Guide

Quick reference for creating and managing wireframes in the Mango Sand portal.

## Editing Wireframes

### Option 1: VS Code (Recommended)
1. Open any `.excalidraw` file in VS Code
2. VS Code will show a preview pane (Excalidraw Editor extension)
3. Edit directly with live preview
4. Save (Ctrl+S / Cmd+S)
5. Run regeneration (see below)

### Option 2: Web Editor (excalidraw.com)
1. Navigate to [excalidraw.com](https://excalidraw.com)
2. Open → paste contents of `.excalidraw` JSON file OR upload the file
3. Design your screen
4. Export as JSON
5. Save JSON back to the `.excalidraw` file in the repo
6. Run regeneration

## Regenerating Wireframe Pages

After editing `.excalidraw` files, regenerate the pages:

```bash
# Full regeneration (all generators + MkDocs build)
bash portal/scripts/generate-all.sh

# Just wireframes (faster)
python3 portal/scripts/generate-wireframe-pages.py
```

This creates:
- `.svg` — static preview image
- `.html` — interactive Excalidraw viewer (with zoom/pan)
- `.md` — MkDocs wrapper page with info + embeds

## Current Wireframes

### Web Guest Portal
- **Location**: `portal/docs/applications/web-guest-portal/wireframes/`
- **check-in-confirmation.excalidraw** — Guest check-in completion flow with guest info, safety checklist, wristband ID

**See on site**: [Check-in Confirmation](https://mango-sand-083b8ce0f.4.azurestaticapps.net/applications/web-guest-portal/wireframes/check-in-confirmation/)

### Web Operations Dashboard
- **Location**: `portal/docs/applications/web-ops-dashboard/wireframes/`
- **live-tracking.excalidraw** — Real-time adventure map with guest positions, alerts, and stats

**See on site**: [Live Tracking](https://mango-sand-083b8ce0f.4.azurestaticapps.net/applications/web-ops-dashboard/wireframes/live-tracking/)

### Mobile Guest App
- **Location**: `portal/docs/applications/app-guest-mobile/wireframes/`
- **adventure-selection.excalidraw** — Adventure listings with filters, availability, and booking

**See on site**: [Adventure Selection](https://mango-sand-083b8ce0f.4.azurestaticapps.net/applications/app-guest-mobile/wireframes/adventure-selection/)

## Adding New Wireframes

1. Create new `.excalidraw` file:
   ```bash
   # Name it kebab-case, descriptive
   touch portal/docs/applications/{app}/wireframes/feature-screen-name.excalidraw
   ```

2. Design in VS Code or excalidraw.com

3. If using web editor, export JSON and save to the file above

4. Regenerate:
   ```bash
   python3 portal/scripts/generate-wireframe-pages.py
   ```

5. Update MkDocs nav if needed (usually automatic for existing apps)

6. Commit all files:
   ```bash
   git add portal/docs/applications/*/wireframes/
   git commit -m "Add wireframe: feature-screen-name"
   ```

## File Structure

```
portal/docs/applications/
├── web-guest-portal/
│   ├── index.md
│   └── wireframes/
│       ├── check-in-confirmation.excalidraw  ← Source (edit this)
│       ├── check-in-confirmation.md          ← Generated wrapper
│       ├── check-in-confirmation.svg         ← Generated preview
│       └── check-in-confirmation.html        ← Generated viewer
├── web-ops-dashboard/
│   ├── index.md
│   └── wireframes/
│       ├── live-tracking.excalidraw
│       ├── live-tracking.md
│       ├── live-tracking.svg
│       └── live-tracking.html
└── app-guest-mobile/
    ├── index.md
    └── wireframes/
        ├── adventure-selection.excalidraw
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

When proposing UI/UX changes in solution designs, reference wireframes like:

```markdown
### User Interface

See wireframe: [Check-in Confirmation Screen](../../applications/web-guest-portal/wireframes/check-in-confirmation.md)

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
