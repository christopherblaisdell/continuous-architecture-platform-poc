# Figma Wireframes Integration Plan

| Field | Value |
|-------|-------|
| **Author** | NovaTrek Architecture Team |
| **Created** | 2026-03-05 |
| **Status** | Proposed |
| **Related** | [EVENT-CATALOG-PLAN.md](EVENT-CATALOG-PLAN.md), [generate-application-pages.py](scripts/generate-application-pages.py), [generate-microservice-pages.py](scripts/generate-microservice-pages.py) |

---

## 1. Problem Statement

The NovaTrek Architecture Portal documents microservices, events, actors, and applications, but lacks visual representation of **what users actually see**. Application pages describe screens with sequence diagrams and service dependencies, but there is no way to understand the user experience without switching to an external Figma workspace.

Embedding Figma wireframes directly into the portal closes this gap by connecting architecture artifacts to the visual design layer. Architects, developers, and product owners can see the screen alongside its service dependencies, data flows, and API contracts — all in one place.

---

## 2. Figma Embedding Options

### Option A: Figma Embed (iframe via `<iframe>`)

Figma natively supports oEmbed and iframe embedding. Any frame, page, or component in a Figma file can be embedded with a URL of the form:

```
https://www.figma.com/embed?embed_host=share&url=<figma-file-url>
```

**Pros:**

- Always up-to-date — renders live from Figma
- Interactive — viewers can zoom, pan, inspect (if permissions allow)
- No build step, no image export, no stale assets
- Figma provides view-only embed links that require no authentication for public/org-shared files

**Cons:**

- Requires network access to Figma at render time — no offline support
- `X-Frame-Options` / CSP headers must allow `figma.com` as a frame source
- Figma embed links can break if the file is moved, renamed, or access revoked
- Loading latency on first render (Figma renderer initializes in the iframe)

### Option B: Exported Image Assets (PNG/SVG) Committed to Repo

Export frames from Figma as PNG or SVG images, commit them to the repo under `portal/docs/wireframes/`, and embed them as `<img>` tags.

**Pros:**

- Works offline — no external dependencies
- Fast rendering — static image, no JavaScript
- Full control over versioning via git history
- No CSP/iframe configuration needed

**Cons:**

- Images go stale the moment the Figma file changes — manual re-export required
- No interactivity — cannot zoom into details or inspect components
- Adds binary assets to the repo (PNG) or verbose SVG markup
- Requires a manual workflow or CI script to keep images in sync

### Option C: Hybrid — Live Embed with Static Fallback

Use live Figma `<iframe>` embeds as the primary display, with a static PNG fallback image shown if the iframe fails to load (e.g., offline or Figma unavailable).

**Pros:**

- Best of both worlds — live when online, static when offline
- Graceful degradation without broken UI
- Static fallback provides a snapshot for documentation review

**Cons:**

- Requires maintaining both the embed URL and the fallback image
- More complex rendering logic
- Fallback images still go stale

### Recommendation

**Option A (Figma Embed via iframe)** for the initial implementation. The portal is already deployed as a web application (Azure Static Web Apps) and is always accessed online. The live embed keeps wireframes permanently in sync with the design source without any export workflow.

If offline access becomes a requirement, upgrade to Option C (Hybrid) later.

---

## 3. Figma and GitHub Source Control

### How Figma Relates to Git

Figma files are cloud-native SaaS artifacts — there is no local editable file format to commit. The design source of truth **always lives on figma.com**. GitHub and Figma coexist with distinct ownership:

| System | Owns | Version Control |
|--------|------|----------------|
| **Figma** | Visual design files (frames, components, prototypes) | Figma's built-in version history, named versions, and branching (Org/Enterprise plans) |
| **GitHub** | Architecture artifacts, generator scripts, wireframe metadata, embed URLs | Git commits |

Design files never enter the git repo. GitHub stores **derived artifacts and metadata** that reference Figma:

| What GitHub Stores | What It References |
|-------------------|-------------------|
| `WIREFRAMES` dict (embed URLs, structured metadata) | Figma frame URLs |
| CSP configuration allowing `figma.com` iframes | Figma embed renderer |
| Generated Markdown with `<iframe>` tags | Live Figma content |

### Figma-GitHub Integration Points

| Integration | What It Does | Design Files Stay on figma.com? |
|-------------|-------------|----------------------------------|
| **Figma Embed (iframe)** | Renders live Figma frames inside the portal | Yes — iframe reads from figma.com |
| **Figma for VS Code** extension | Browse and inspect designs inside VS Code | Yes — reads from figma.com |
| **Tokens Studio** plugin | Syncs design tokens (colors, spacing, typography) to GitHub as JSON | Yes — tokens are an export, source stays in Figma |
| **Figma REST API** | Export frames as PNG/SVG, read component metadata, automate asset pipelines | Yes — API reads from figma.com |
| **GitHub PR links** | Paste Figma URLs in PRs/issues — GitHub renders preview cards | Yes — just a URL reference |
| **Figma Dev Mode** | Generates code snippets, links designs to code in connected repos | Yes — Figma stays the source |

### Figma Branching and Versioning (Native)

Figma provides its own version control features that handle the design lifecycle without Git:

| Feature | Plan Required | Use Case |
|---------|--------------|----------|
| Automatic version history (every save) | All plans | Full change history |
| Named versions (milestone snapshots) | All plans | "v2.0 — Booking Flow Redesign" |
| Branching (parallel design work, merge back) | Organization / Enterprise | Feature branches for design exploration |
| Publishing components to team library | Professional+ | Shared design system |

### Key Principle

The `WIREFRAMES` dict in the generator script is a **metadata index**, not a source-of-truth copy. It stores URLs, descriptions, and structured metadata that point to — and describe — the live Figma designs. If a Figma file is moved or restructured, only the URL in the dict needs updating.

---

## 4. Figma URL Structure and Data Model

### Figma URL Anatomy

Figma provides several URL patterns:

| URL Pattern | Use Case |
|-------------|----------|
| `https://www.figma.com/design/<file_key>/<file_name>` | Full file (landing page) |
| `https://www.figma.com/design/<file_key>/<file_name>?node-id=<node_id>` | Specific frame/page |
| `https://www.figma.com/proto/<file_key>/<file_name>?node-id=<node_id>` | Prototype (interactive flow) |

The embed URL wraps any of these:

```
https://www.figma.com/embed?embed_host=share&url=<encoded_figma_url>
```

### Wireframe Data Structure in the Generator

Add a new `WIREFRAMES` dict to `generate-application-pages.py` mapping each application screen to its Figma frame. Each entry carries **two layers of information**:

1. **Figma embed metadata** — URL, status, last sync date (used to render the human-visible iframe)
2. **Structured screen metadata** — components, data fields, user actions, API calls (used for AI-assisted architectural reasoning)

```python
WIREFRAMES = {
    # app_key -> { screen_name -> { figma metadata + structured screen metadata } }
    "web-guest-portal": {
        "Booking Flow": {
            # -- Figma embed metadata --
            "figma_url": "https://www.figma.com/design/XXXXXXXXXX/NovaTrek-Guest-Portal?node-id=100-200",
            "proto_url": "https://www.figma.com/proto/XXXXXXXXXX/NovaTrek-Guest-Portal?node-id=100-200",  # optional interactive prototype
            "status": "final",       # draft | review | final
            "last_synced": "2026-03-05",
            # -- Structured screen metadata (AI-readable) --
            "description": "Multi-step booking wizard with trip selection, date picker, participant entry, and payment",
            "components": [
                "Trip search bar with date range picker",
                "Trip card grid (photo, title, price, difficulty badge, availability count)",
                "Participant form (name, DOB, email per participant)",
                "Waiver checkbox with link to PDF",
                "Payment form (card number, expiry, CVV — Stripe Elements iframe)",
                "Confirmation screen (confirmation code, QR code, calendar add link)",
            ],
            "data_displayed": ["trip_name", "base_price", "available_spots", "difficulty_level", "duration_hours", "confirmation_code"],
            "data_collected": ["guest_name", "date_of_birth", "email", "party_size", "waiver_signed", "payment_token"],
            "user_actions": ["search trips", "select date", "add participant", "sign waiver", "submit payment"],
            "api_calls": ["GET /trips", "GET /trips/{id}/availability", "POST /reservations", "POST /payments"],
        },
        "Guest Profile": {
            "figma_url": "https://www.figma.com/design/XXXXXXXXXX/NovaTrek-Guest-Portal?node-id=100-300",
            "status": "review",
            "last_synced": "2026-03-05",
            "description": "Guest profile dashboard showing upcoming trips, adventure history, and certifications",
            "components": [
                "Profile header (name, photo, loyalty tier badge)",
                "Upcoming trips list (date, trip name, status badge)",
                "Adventure history timeline (completed trips with ratings)",
                "Certifications card list (cert type, issuer, expiry indicator)",
                "Emergency contacts section (name, phone, relationship)",
            ],
            "data_displayed": ["first_name", "last_name", "email", "loyalty_tier", "trip_name", "trip_date", "cert_type", "expiry_date", "rating"],
            "data_collected": ["first_name", "last_name", "phone", "email", "emergency_contact_name", "emergency_contact_phone"],
            "user_actions": ["edit profile", "upload photo", "view trip details", "add emergency contact"],
            "api_calls": ["GET /guests/{id}", "PATCH /guests/{id}", "GET /guests/{id}/certifications", "GET /reservations?guest_id={id}"],
        },
        "Reservation Management": {
            "figma_url": "https://www.figma.com/design/XXXXXXXXXX/NovaTrek-Guest-Portal?node-id=100-400",
            "status": "draft",
            "last_synced": "2026-03-05",
            "description": "Reservation list and detail view with modification and cancellation options",
            "components": [
                "Reservation list with status filters (upcoming, past, cancelled)",
                "Reservation detail card (confirmation code, trip name, date, participants)",
                "Participant list with waiver status indicators",
                "Modify reservation modal (date change, party size)",
                "Cancel reservation confirmation dialog with refund estimate",
            ],
            "data_displayed": ["confirmation_code", "trip_name", "trip_date", "party_size", "status", "total_amount", "participant_names", "waiver_signed"],
            "data_collected": ["new_trip_date", "new_party_size", "cancellation_reason"],
            "user_actions": ["filter reservations", "view details", "modify reservation", "cancel reservation"],
            "api_calls": ["GET /reservations?guest_id={id}", "GET /reservations/{id}", "PATCH /reservations/{id}", "POST /reservations/{id}/cancel"],
        },
        # ... additional screens
    },
    "web-ops-dashboard": {
        "Check-In Station": {
            "figma_url": "https://www.figma.com/design/XXXXXXXXXX/NovaTrek-Ops-Dashboard?node-id=200-100",
            "status": "final",
            "last_synced": "2026-03-05",
            "description": "Staff-facing check-in station with guest lookup, gear verification, and wristband assignment",
            "components": [
                "Guest lookup bar (search by confirmation code, name, or QR scan)",
                "Reservation detail panel (guest name, trip, participants, waiver status)",
                "Gear verification checklist (item, size, condition, RFID tag)",
                "Wristband assignment panel (NFC ID, activation toggle)",
                "Check-in completion confirmation with print receipt option",
            ],
            "data_displayed": ["confirmation_code", "guest_name", "adventure_category", "check_in_pattern", "gear_items", "waiver_status", "wristband_nfc_id"],
            "data_collected": ["gear_verification_status", "wristband_nfc_id", "staff_id", "check_in_notes"],
            "user_actions": ["search guest", "scan QR code", "verify gear", "assign wristband", "complete check-in"],
            "api_calls": ["GET /check-ins/lookup?confirmation_code={code}", "POST /check-ins", "POST /check-ins/{id}/gear-verification", "POST /check-ins/{id}/wristband"],
        },
        # ... additional screens
    },
    "app-guest-mobile": {
        "Self Check-In": {
            "figma_url": "https://www.figma.com/design/XXXXXXXXXX/NovaTrek-Mobile-App?node-id=300-100",
            "status": "draft",
            "last_synced": "2026-03-05",
            "description": "Mobile self-check-in flow with QR code scan, waiver confirmation, and digital wristband",
            "components": [
                "Reservation QR code scanner (camera viewfinder with overlay)",
                "Reservation confirmation card (trip name, date, participants)",
                "Waiver acceptance toggle with expandable legal text",
                "Digital wristband display (NFC activation instructions, QR fallback)",
                "Check-in success screen with adventure countdown timer",
            ],
            "data_displayed": ["confirmation_code", "trip_name", "trip_date", "adventure_category", "wristband_nfc_id"],
            "data_collected": ["qr_scan_result", "waiver_accepted"],
            "user_actions": ["scan QR code", "accept waiver", "activate wristband", "view check-in confirmation"],
            "api_calls": ["GET /reservations/{id}", "POST /check-ins", "GET /check-ins/{id}/wristband"],
        },
        # ... additional screens
    },
}
```

### Screen Name Alignment

Screen names in `WIREFRAMES` MUST match the screen names already used in the application page generator's `SCREENS` dict and in the `APP_CONSUMERS` dict in the microservice page generator. This ensures wireframes link correctly to existing screen sequence diagrams and service dependency tables.

---

## 5. Portal Publishing Plan

### 4.1 Where Wireframes Appear

Wireframes integrate into **four** existing page types plus one new page:

| Page Type | What Shows | Link Direction |
|-----------|-----------|----------------|
| **Application pages** (per-app) | Wireframe embed per screen, inline with the existing screen section | Existing page, wireframe added within each screen block |
| **Microservice pages** (per-service) | Wireframe thumbnails in the "Consuming Applications" section | Microservice -> Application screen wireframe |
| **Wireframe Gallery** (new page) | Browsable gallery of all wireframes across all apps, filterable by app and status | Central index -> individual app screen sections |
| **Home page** | New card in the portal grid linking to the Wireframe Gallery | Home -> Gallery |
| **Actor Catalog** | Link from human actors (Guest, Operations Staff) to relevant wireframes | Actor -> Application screen wireframe |

### 4.2 Application Page Integration (Primary)

Each application page already has screen sections with sequence diagrams. Add the wireframe embed **above** the sequence diagram for each screen:

```markdown
### Booking Flow

**Status:** :material-check-circle:{ .status--final } Final

> Multi-step booking wizard with trip selection, date picker, participant entry, and payment

#### Wireframe

<div class="wireframe-wrap">
  <a href="https://www.figma.com/design/XXXXXXXXXX/NovaTrek-Guest-Portal?node-id=100-200"
     target="_blank" class="wireframe-figma-link" title="Open in Figma">
    <svg>...</svg>  <!-- Figma logo icon -->
  </a>
  <iframe
    src="https://www.figma.com/embed?embed_host=share&url=https%3A%2F%2Fwww.figma.com%2Fdesign%2FXXXXXXXXXX%2FNovaTrek-Guest-Portal%3Fnode-id%3D100-200"
    style="border: 1px solid rgba(0, 0, 0, 0.1); border-radius: 8px;"
    width="100%" height="500" allowfullscreen>
  </iframe>
</div>

#### Sequence Diagram
... (existing diagram)

#### Service Dependencies
... (existing table)
```

The wireframe appears first because it answers "what does the user see?" before "how does it work?"

### 4.3 Microservice Page Cross-Links

The existing "Consuming Applications" section table gains a wireframe icon column:

```markdown
## :material-cellphone-link: Consuming Applications

| Application | Screens | Wireframes |
|-------------|---------|------------|
| [Guest Portal](../../applications/web-guest-portal/) | Booking Flow, Guest Profile | [:material-pencil-ruler: View](../../applications/web-guest-portal/#booking-flow-wireframe) |
```

The "View" link deep-links to the wireframe heading anchor on the application page.

### 4.4 Wireframe Gallery (New Page)

A new top-level page at `portal/docs/wireframes/index.md` provides a browsable overview:

```markdown
# Wireframe Gallery

> All NovaTrek screen designs — linked to their architecture documentation

## Guest Portal (web-guest-portal)

| Screen | Status | Wireframe | Architecture |
|--------|--------|-----------|--------------|
| Booking Flow | :material-check-circle:{ .status--final } Final | [View Wireframe](#booking-flow) | [Sequence Diagram](../applications/web-guest-portal/#booking-flow) |
| Guest Profile | :material-progress-check:{ .status--review } Review | [View Wireframe](#guest-profile) | [Sequence Diagram](../applications/web-guest-portal/#guest-profile) |

### Booking Flow { #booking-flow }

<iframe src="..." width="100%" height="600" allowfullscreen></iframe>

... (repeat for each screen)
```

### 4.5 Home Page Card

Add a seventh card to the home page grid:

```markdown
<a class="portal-card" href="wireframes/">
  <div class="card-icon">:material-pencil-ruler:</div>
  <strong>Wireframes</strong>
  <span>{n} Screens across {m} Applications</span>
</a>
```

### 4.6 Actor Catalog Links

In the Actor Catalog, human actors (Guest, Operations Staff, Guide) gain a "Screens" column or subsection linking to the application screens (and their wireframes) where that actor interacts with the system.

### 4.7 Navigation Structure

```yaml
nav:
  - Home: index.md
  - Service Catalog: services/index.md
  - Design Standards: ...
  - Applications:
    - applications/index.md
    - web-guest-portal: applications/web-guest-portal.md
    - web-ops-dashboard: applications/web-ops-dashboard.md
    - app-guest-mobile: applications/app-guest-mobile.md
  - Wireframes: wireframes/index.md          # NEW
  - Microservice Pages:
    - microservices/index.md
    - ...
  - Event Catalog: events/index.md
  - Actor Catalog: actors/index.md
  - Tags: tags.md
```

---

## 6. AI Readability Strategy

GitHub Copilot and other AI tools **cannot see inside a Figma iframe** — it is just a URL string to them. The `WIREFRAMES` dict solves this with a dual-layer approach: the iframe serves **human eyes**, the structured metadata serves **AI reasoning**.

### The Problem

| What AI Sees | What AI Needs |
|-------------|---------------|
| `"figma_url": "https://www.figma.com/design/..."` | What components are on this screen? |
| An opaque URL string | What data does this screen display and collect? |
| Nothing about the visual layout | What API calls does this screen trigger? |

### The Solution: Structured Screen Metadata

Each entry in the `WIREFRAMES` dict carries five metadata fields that fully describe the screen in text form:

| Field | Purpose | AI Use Case |
|-------|---------|-------------|
| `description` | One-line summary of the screen | Contextual understanding, search results |
| `components` | List of UI components visible on screen | Trace component -> data field -> API -> service -> database column |
| `data_displayed` | Field names shown to the user (read path) | Cross-reference against OpenAPI response schemas and DATA_STORES columns |
| `data_collected` | Field names entered by the user (write path) | Cross-reference against OpenAPI request body schemas |
| `user_actions` | What the user can do on this screen | Map actions to API calls and event triggers |
| `api_calls` | API endpoints invoked by this screen | Cross-reference against OpenAPI specs and CROSS_SERVICE_CALLS |

### What This Enables for AI Agents

**Traceability queries the AI can now answer:**

- "Which screens display the `confirmation_code` field?" — search `data_displayed` across all wireframes
- "If we add a new field to `GET /reservations/{id}`, which wireframes need updating?" — match `api_calls` to find affected screens
- "What PII does the Guest Profile screen collect?" — inspect `data_collected` and cross-reference with DATA_STORES encrypted columns
- "Which screens are still in draft?" — filter by `status`
- "What user actions trigger the `reservation.cancelled` event?" — trace from `user_actions` -> `api_calls` -> EVENT_CATALOG producers

**Impact analysis:**

When a microservice API changes (e.g., adding a required field to `POST /check-ins`), the AI can automatically identify:

1. Which wireframes call that endpoint (via `api_calls`)
2. Whether the screen already collects the new field (via `data_collected`)
3. Which UI components need modification (via `components`)
4. Which application and screen owner to notify

### Optional Enhancement: Figma REST API Export

For even richer AI understanding, a script can call the Figma REST API to export the frame's component tree as JSON:

```bash
python3 scripts/figma-export.py --file-key XXXXXXXXXX --node-id 100-200 --output wireframe-metadata/
```

This produces a machine-readable node tree:

```json
{
  "frame": "Booking Flow",
  "children": [
    {"type": "FRAME", "name": "Step 1 - Search", "children": [
      {"type": "TEXT", "characters": "Find your next adventure"},
      {"type": "INSTANCE", "component": "DateRangePicker"},
      {"type": "INSTANCE", "component": "TripCard", "count": 6}
    ]},
    {"type": "FRAME", "name": "Step 2 - Participants", "children": ["..."]}
  ]
}
```

This is a supplementary enrichment — the structured text metadata in the `WIREFRAMES` dict is the primary AI-readable layer and does not require a Figma API token.

### Rendering Metadata on Portal Pages

The structured metadata is also valuable for human readers. The generator can render it below the wireframe embed:

```markdown
#### Wireframe Details

**Components:**

- Trip search bar with date range picker
- Trip card grid (photo, title, price, difficulty badge, availability count)
- ...

**Data Displayed:** `trip_name`, `base_price`, `available_spots`, `difficulty_level`, `confirmation_code`

**Data Collected:** `guest_name`, `date_of_birth`, `email`, `party_size`, `waiver_signed`, `payment_token`

**API Calls:** `GET /trips` | `GET /trips/{id}/availability` | `POST /reservations` | `POST /payments`
```

This serves as human-readable documentation that also keeps the metadata visible for review.

---

## 7. Linking Strategy — Forward and Back

Every wireframe must be reachable from every related artifact, and every wireframe must link back to its architecture context.

### 5.1 Complete Link Map

```
Home Page
  └─> Wireframe Gallery card

Wireframe Gallery
  ├─> Each wireframe embed (inline on page)
  ├─> Link to Application page screen section (architecture context)
  └─> Link back to Home

Application Page (per screen)
  ├─> Wireframe embed (inline above sequence diagram)
  ├─> "Open in Figma" link (external, opens Figma)
  ├─> Sequence diagram (existing)
  ├─> Service dependency table (existing)
  └─> Link from screen heading back to Wireframe Gallery

Microservice Page ("Consuming Applications" section)
  └─> Wireframe deep-link per screen (-> Application page #screen-wireframe)

Actor Catalog (human actors)
  └─> Links to screens relevant to that actor (-> Application page #screen)

C4 Context Diagrams (per-service, enterprise)
  └─> Application containers already link to /applications/{app}/
       (wireframes are inline on those pages — no additional links needed)

Sequence Diagrams (per-screen in application pages)
  └─> Already link to /microservices/{svc}/#{endpoint}
       (bidirectional — no changes needed)
```

### 5.2 Anchor Convention

Wireframe sections use the anchor format `{screen-slug}-wireframe`:

- `#booking-flow-wireframe`
- `#check-in-station-wireframe`
- `#self-check-in-wireframe`

This avoids collision with the existing screen heading anchors (which are just `#booking-flow`, etc.) and gives a predictable deep-link target from microservice pages and the gallery.

---

## 8. CSP and Security Configuration

### 6.1 staticwebapp.config.json Changes

The portal's Content Security Policy must be updated to allow Figma iframes:

```json
{
  "globalHeaders": {
    "Content-Security-Policy": "... frame-src 'self' https://www.figma.com; ...",
    "X-Frame-Options": "SAMEORIGIN"
  }
}
```

Key additions:

| Directive | Value | Reason |
|-----------|-------|--------|
| `frame-src` | `https://www.figma.com` | Allow Figma embed iframes |
| `connect-src` | `https://www.figma.com` | Allow Figma renderer WebSocket/API calls |

`X-Frame-Options` stays `SAMEORIGIN` (already set for PlantUML SVG `<object>` tags).

### 6.2 Figma Access Permissions

Figma embed links must be set to one of:

| Access Level | Audience | How to Set |
|-------------|----------|------------|
| **Anyone with the link** | Public portal | Figma Share > "Anyone with the link" > "can view" |
| **Organization** | Internal portal | Figma Share > Organization-level access |

NOTE: Figma embeds for files with restricted access show a "Request Access" screen inside the iframe. Ensure all embedded files have at minimum view-only link sharing enabled.

---

## 9. CSS Styling

### 7.1 New CSS Classes

Add to `portal/docs/stylesheets/custom.css`:

```css
/* Wireframe embed container */
.wireframe-wrap {
  position: relative;
  margin: 1rem 0;
  border: 1px solid var(--md-default-fg-color--lighter);
  border-radius: 8px;
  overflow: hidden;
  background: #fafafa;
}

.wireframe-wrap iframe {
  display: block;
  width: 100%;
  min-height: 500px;
  border: none;
}

/* Figma link button (floats top-right like diagram-expand) */
.wireframe-figma-link {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  z-index: 10;
  background: rgba(0, 0, 0, 0.5);
  color: #fff;
  border-radius: 6px;
  padding: 0.3rem 0.6rem;
  font-size: 0.75rem;
  text-decoration: none;
  opacity: 0.5;
  transition: opacity 0.2s;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}
.wireframe-figma-link:hover {
  opacity: 1;
  color: #fff;
}

/* Status indicators for wireframe status */
.wireframe-status {
  display: inline-block;
  padding: 0.1rem 0.5rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 600;
}
.wireframe-status--draft {
  background: #fff3cd;
  color: #856404;
}
.wireframe-status--review {
  background: #cce5ff;
  color: #004085;
}
.wireframe-status--final {
  background: #d4edda;
  color: #155724;
}
```

The `.wireframe-figma-link` mirrors the existing `.diagram-expand` pattern used for PlantUML SVG fullscreen buttons — consistent UX across diagram types.

---

## 10. Generator Integration

### 8.1 Changes to `generate-application-pages.py`

| Change | Details |
|--------|---------|
| **New dict** | Add `WIREFRAMES` dict (see Section 3) |
| **Screen rendering** | Before each screen's sequence diagram, emit the wireframe `<iframe>` embed if a wireframe exists for that screen |
| **Wireframe heading** | Add `#### Wireframe { #<screen-slug>-wireframe }` subheading with explicit anchor |
| **Status badge** | Render the wireframe status as a colored badge |
| **Figma link** | Add floating "Open in Figma" link in `.wireframe-wrap` container |

### 8.2 Changes to `generate-microservice-pages.py`

| Change | Details |
|--------|---------|
| **Import WIREFRAMES** | Import or duplicate the `WIREFRAMES` dict |
| **Consuming Applications table** | Add a "Wireframes" column with deep-links to `../../applications/{app_key}/#{screen_slug}-wireframe` for screens that have wireframes |

### 8.3 New Generator Function

Add `generate_wireframe_gallery()` to `generate-application-pages.py` (or a new `generate-wireframe-pages.py`):

| Input | Output |
|-------|--------|
| `WIREFRAMES` dict + `APP_TITLES` | `portal/docs/wireframes/index.md` |

The gallery page groups wireframes by application, shows status badges, and embeds each wireframe with links back to the architecture page.

### 8.4 Home Page Update

In `portal/docs/index.md`, add the Wireframes card to the portal grid:

```html
<a class="portal-card" href="wireframes/">
  <div class="card-icon">:material-pencil-ruler:</div>
  <strong>Wireframes</strong>
  <span>Screen designs across all applications</span>
</a>
```

### 8.5 Actor Catalog Update

In `generate-microservice-pages.py`'s `generate_actors_page()`, add a "Screens" subsection to human actors (Guest, Operations Staff, Guide) showing which application screens they interact with, linking to the wireframe:

```markdown
#### Screens

| Application | Screen | Wireframe |
|-------------|--------|-----------|
| [Guest Portal](/applications/web-guest-portal/) | Booking Flow | [View](/applications/web-guest-portal/#booking-flow-wireframe) |
```

### 8.6 Build Pipeline

No new build tools needed. The `<iframe>` embeds are pure HTML rendered inline by MkDocs. No PlantUML rendering, no image export.

Build steps remain:

```bash
python3 portal/scripts/generate-application-pages.py   # now also generates wireframe gallery
python3 portal/scripts/generate-microservice-pages.py   # updated consuming apps section
cd portal && /usr/bin/python3 -m mkdocs build
# existing cp commands for assets
cp staticwebapp.config.json site/
swa deploy site --deployment-token "..." --env production
```

---

## 11. Implementation Phases

### Phase 1: Foundation

- [ ] Update `staticwebapp.config.json` CSP to allow `frame-src https://www.figma.com`
- [ ] Add wireframe CSS classes to `custom.css`
- [ ] Add `WIREFRAMES` dict to `generate-application-pages.py` (initially empty or with placeholder URLs)
- [ ] Add Wireframes nav entry to `mkdocs.yml`
- [ ] Deploy and verify iframe renders correctly with a test Figma embed

### Phase 2: Application Page Integration

- [ ] Update application page generator to render wireframe embeds per screen
- [ ] Add wireframe heading with explicit anchor per screen
- [ ] Add "Open in Figma" floating link
- [ ] Add status badges (draft/review/final)
- [ ] Regenerate application pages and verify

### Phase 3: Cross-Linking

- [ ] Update microservice page generator's "Consuming Applications" section with wireframe column
- [ ] Generate wireframe gallery page (`wireframes/index.md`)
- [ ] Add Wireframes card to home page
- [ ] Update actor catalog with screen links for human actors
- [ ] Verify all forward and back links work

### Phase 4: Content Population

- [ ] Create Figma file(s) for NovaTrek applications with frame-per-screen structure
- [ ] Set sharing to "Anyone with the link can view"
- [ ] Populate `WIREFRAMES` dict with real Figma URLs and node IDs
- [ ] Full regenerate, build, deploy, and link audit

---

## 12. Copilot Instructions Updates

Add to `.github/copilot-instructions.md`:

### Wireframes Section

```markdown
### Wireframe Integration

The portal embeds Figma wireframes as live iframes on application pages and in the wireframe gallery.
Figma files live on figma.com (cloud-native SaaS) — they are never committed to git.
The `WIREFRAMES` dict stores metadata that references the live Figma designs.

| Structure | Location |
|-----------|----------|
| `WIREFRAMES` dict | `portal/scripts/generate-application-pages.py` |
| Wireframe Gallery | `portal/docs/wireframes/index.md` (generated) |
| CSS | `portal/docs/stylesheets/custom.css` (.wireframe-wrap, .wireframe-figma-link) |

**Rules:**
1. Screen names in `WIREFRAMES` MUST match screen names in `SCREENS` and `APP_CONSUMERS`
2. Figma URLs MUST use the `https://www.figma.com/design/` format with `node-id` parameter
3. Embed URLs are constructed as `https://www.figma.com/embed?embed_host=share&url=<encoded>`
4. Every wireframe MUST have bidirectional links: app page <-> gallery, microservice -> wireframe
5. Use `{ #screen-slug-wireframe }` explicit anchors to avoid collision with screen headings
6. The `WIREFRAMES` dict carries structured metadata (components, data_displayed, data_collected, user_actions, api_calls) — this is the AI-readable layer
7. The iframe embed is for human viewers — the structured metadata is for AI reasoning and impact analysis
8. When adding wireframes for a new screen, always populate ALL metadata fields — the AI relies on them for traceability
```

---

## 13. Open Questions

| # | Question | Options | Recommendation |
|---|----------|---------|----------------|
| 1 | Should wireframes be in the same Figma file (one per app) or one master file? | A) One file per app B) One master file with pages per app | **A** — matches the app-centric page structure and simplifies per-team access control |
| 2 | Should we embed full pages or individual frames? | A) Full Figma page B) Individual frame per screen | **B** — individual frames give focused context per screen section |
| 3 | How to handle screens with no wireframe yet? | A) Hide the wireframe section B) Show placeholder with "Design in progress" | **B** — makes gaps visible and encourages completion |
| 4 | Should the gallery show live embeds or thumbnail images? | A) Live embeds (iframes) B) Static thumbnails linking to app page | **B** for the gallery (faster page load), **A** on app pages (full detail) |
| 5 | Prototype links (interactive flows) vs static wireframes? | A) Static frames only B) Both static and prototype links | **B** — show static wireframe inline, add "View Prototype" link for interactive flows when available |
| 6 | Should wireframes be tagged in MkDocs? | A) Yes, with `wireframe` tag B) No | **A** — enables tag-based discovery alongside microservices and events |
| 7 | Should the Figma REST API export script be built in Phase 1 or deferred? | A) Phase 1 B) Deferred to Phase 4+ | **B** — structured text metadata in the dict is sufficient for AI reasoning; API export is a nice-to-have enrichment |
| 8 | Should wireframe metadata be rendered on portal pages or kept only in the generator? | A) Render as "Wireframe Details" section B) Keep in generator only | **A** — visible metadata helps human reviewers and keeps AI-readable data auditable |
