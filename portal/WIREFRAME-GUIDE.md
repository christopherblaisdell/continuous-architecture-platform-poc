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

- **Source**: `architecture/wireframes/web-guest-portal/reservation-lookup.excalidraw`
- Landing screen where guests enter a booking reference or email address to look up their reservation before beginning the check-in process.
- **See on site**: [Reservation Lookup](https://architecture.novatrek.cc/applications/web-guest-portal/wireframes/reservation-lookup/)

- **Source**: `architecture/wireframes/web-guest-portal/check-in-confirmation.excalidraw`
- Full check-in confirmation screen (step 4 of 4) with adventure details, guest information, safety and compliance status, wristband assignment, loyalty points earned, and action buttons.
- **See on site**: [Check-in Confirmation](https://architecture.novatrek.cc/applications/web-guest-portal/wireframes/check-in-confirmation/)

- **Source**: `architecture/wireframes/web-guest-portal/safety-waiver.excalidraw`
- Digital liability waiver and safety acknowledgment screen (step 3 of 4). Includes scrollable waiver text, risk acknowledgment checkboxes, emergency contact confirmation, and digital signature capture.
- **See on site**: [Safety Waiver](https://architecture.novatrek.cc/applications/web-guest-portal/wireframes/safety-waiver/)

### Web Operations Dashboard

- **Source**: `architecture/wireframes/web-ops-dashboard/live-tracking.excalidraw`
- Real-time GPS tracking of all active adventure groups. Shows map with group markers, alert banner for incidents, per-group status panel, and key operational metrics (guests on trail, active alerts, response time).
- **See on site**: [Live Tracking](https://architecture.novatrek.cc/applications/web-ops-dashboard/wireframes/live-tracking/)

- **Source**: `architecture/wireframes/web-ops-dashboard/todays-schedule.excalidraw`
- Full daily adventure schedule table organized by time period (Morning, Afternoon, Evening). Displays departure time, adventure name, guide assignment, guest count, check-in pattern, status, and gate for each departure slot.
- **See on site**: [Today's Schedule](https://architecture.novatrek.cc/applications/web-ops-dashboard/wireframes/todays-schedule/)

- **Source**: `architecture/wireframes/web-ops-dashboard/check-in-management.excalidraw`
- Staff-facing check-in queue management. Left panel shows the guest queue with status badges (Ready, Waiver Pending, Gear, etc.). Right panel shows the selected guest's full safety checklist, wristband assignment, and action controls.
- **See on site**: [Check-In Management](https://architecture.novatrek.cc/applications/web-ops-dashboard/wireframes/check-in-management/)

### Mobile Guest App

- **Source**: `architecture/wireframes/app-guest-mobile/adventure-selection.excalidraw`
- Adventure discovery screen with category filter chips (All, Hiking, Kayaking, Climbing, Wildlife, Cycling), detailed adventure cards (rating, difficulty, duration, price, slot availability), and booking CTAs.
- **See on site**: [Adventure Selection](https://architecture.novatrek.cc/applications/app-guest-mobile/wireframes/adventure-selection/)

- **Source**: `architecture/wireframes/app-guest-mobile/booking-detail.excalidraw`
- Booking detail screen with large QR code for day-of check-in, adventure details (guide, meeting point, duration), cancellation option, and loyalty points earned.
- **See on site**: [Booking Detail](https://architecture.novatrek.cc/applications/app-guest-mobile/wireframes/booking-detail/)

- **Source**: `architecture/wireframes/app-guest-mobile/guest-profile.excalidraw`
- Guest profile screen with loyalty tier card (points balance and progress to next tier), upcoming adventures, adventure history stats, and account settings links.
- **See on site**: [Guest Profile](https://architecture.novatrek.cc/applications/app-guest-mobile/wireframes/guest-profile/)

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
│   ├── reservation-lookup.excalidraw
│   ├── check-in-confirmation.excalidraw
│   └── safety-waiver.excalidraw
├── web-ops-dashboard/
│   ├── live-tracking.excalidraw
│   ├── todays-schedule.excalidraw
│   └── check-in-management.excalidraw
└── app-guest-mobile/
    ├── adventure-selection.excalidraw
    ├── booking-detail.excalidraw
    └── guest-profile.excalidraw

portal/docs/applications/             ← GENERATED (by CI)
├── web-guest-portal/
│   └── wireframes/
│       ├── reservation-lookup.md        ← Generated wrapper
│       ├── reservation-lookup.svg       ← Generated preview
│       ├── reservation-lookup.html      ← Generated viewer
│       ├── check-in-confirmation.md
│       ├── check-in-confirmation.svg
│       ├── check-in-confirmation.html
│       ├── safety-waiver.md
│       ├── safety-waiver.svg
│       └── safety-waiver.html
├── web-ops-dashboard/
│   └── wireframes/
│       ├── live-tracking.md
│       ├── live-tracking.svg
│       ├── live-tracking.html
│       ├── todays-schedule.md
│       ├── todays-schedule.svg
│       ├── todays-schedule.html
│       ├── check-in-management.md
│       ├── check-in-management.svg
│       └── check-in-management.html
└── app-guest-mobile/
    └── wireframes/
        ├── adventure-selection.md
        ├── adventure-selection.svg
        ├── adventure-selection.html
        ├── booking-detail.md
        ├── booking-detail.svg
        ├── booking-detail.html
        ├── guest-profile.md
        ├── guest-profile.svg
        └── guest-profile.html
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

The guest check-in flow spans four screens:
1. Reservation lookup (`reservation-lookup.excalidraw`)
2. Identity verification (no dedicated wireframe — handled inline)
3. Safety waiver signing (`safety-waiver.excalidraw`)
4. Confirmation (`check-in-confirmation.excalidraw`)
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
