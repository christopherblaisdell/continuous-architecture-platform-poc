# Diagrams and Wireframes

This page covers how to create, edit, and publish all visual artifacts — C4 diagrams, sequence diagrams, and UI wireframes.

---

## C4 Model Diagrams

All architecture diagrams use the [C4 model](../standards/c4-model/index.md) notation with PlantUML. C4 provides four levels of abstraction:

| Level | Diagram Type | Shows | When to Use |
|-------|-------------|-------|-------------|
| L1 | System Context | Systems and external actors | Cross-system overviews |
| L2 | Container | Applications, data stores, services within a system | Service internals and deployment |
| L3 | Component | Internal components within a service | Within-service detail |
| L4 | Code | Class-level detail | Rarely used in architecture docs |

### Creating a Diagram

Diagrams are hand-authored in PlantUML and stored in `architecture/diagrams/`:

```
architecture/diagrams/
  System/          # L1 System Context diagrams
  Components/      # L3 Component diagrams per domain
  Sequence/        # Cross-service sequence diagrams
  Tickets/         # Ticket-specific diagrams
  endpoints/       # Per-endpoint overrides (replace generated versions)
  theme.puml       # Color theme (derived from domains.yaml)
  include.puml     # Shared macros and skinparams
  templates.puml   # Reusable diagram templates
```

### PlantUML Basics for C4

```plantuml
@startuml
!include <c4/C4_Container>
!include ../theme.puml

LAYOUT_TOP_DOWN()

title System Context - NovaTrek Check-in

Person(guest, "Guest", "Adventure participant")
System(checkin, "svc-check-in", "Manages day-of check-in")
System(profiles, "svc-guest-profiles", "Guest identity")

Rel(guest, checkin, "Checks in", "HTTPS/REST")
Rel(checkin, profiles, "Verifies identity", "HTTPS/REST")

@enduml
```

### Layout Rules

Follow these rules to keep diagrams readable:

1. **Always set `LAYOUT_TOP_DOWN()`** — vertical stacking is the default. Never rely on PlantUML's default left-to-right layout
2. **Group with `Boundary` or `Container_Boundary`** — cluster related components inside boundaries to constrain horizontal spread
3. **Target 1:1 to 2:1 height:width ratio** — diagrams should be roughly square to moderately tall, never wider than tall
4. **Use `Lay_D` / `Lay_R` for hints** — `Lay_D(a, b)` forces b below a; `Lay_R(a, b)` forces b right of a
5. **Wrap long labels with `\n`** — e.g., `"Adventure\nClassification\nEngine"`
6. **Split at 10+ elements** — decompose into separate diagrams per layer or subdomain
7. **Avoid `LAYOUT_LEFT_RIGHT()`** for Component diagrams — only acceptable for simple 3-4 element context diagrams

### Every Relationship Needs Labels

```plantuml
' Good - verb label + technology
Rel(checkin, profiles, "Verifies guest identity", "HTTPS/REST")

' Bad - no label
Rel(checkin, profiles, "")
```

### Rendering Diagrams to SVG

Hand-authored diagrams are rendered by CI using `portal/scripts/generate-svgs.sh`. To render locally:

```bash
bash portal/scripts/generate-svgs.sh
```

Output goes to `portal/docs/diagrams/svg/`.

### Endpoint Diagram Overrides

The microservice page generator auto-generates sequence diagrams for all 139 endpoints. To override a generated diagram with a hand-crafted version:

1. Create a `.puml` file in `architecture/diagrams/endpoints/` matching the generated filename
2. The generator checks this directory first and uses your override instead of auto-generating
3. Commit and push — CI uses the override

---

## Sequence Diagrams

Sequence diagrams show the runtime flow of a specific operation across services.

### Within Solution Designs

Solution design sequence diagrams live in the impact assessment folders:

```
3.solution/i.impacts/impact.1/
  sequence-diagram.puml        # Source PlantUML
  sequence-diagram.svg         # Rendered output
```

### Cross-Service Sequence Diagram Example

```plantuml
@startuml
!include ../../theme.puml

title Check-in with Waiver Verification

actor Guest
participant "svc-check-in" as checkin
participant "svc-guest-profiles" as profiles
participant "svc-reservations" as reservations
participant "svc-safety-compliance" as safety

Guest -> checkin: POST /check-ins
activate checkin

checkin -> profiles: GET /guests/{id}
activate profiles
profiles --> checkin: Guest profile
deactivate profiles

checkin -> reservations: GET /reservations/{id}
activate reservations
reservations --> checkin: Reservation details
deactivate reservations

checkin -> safety: GET /waivers?guest_id={id}
activate safety
safety --> checkin: Active waivers
deactivate safety

checkin --> Guest: 201 Check-in created
deactivate checkin

@enduml
```

### Highlighting Changes

Use light green groups to indicate modifications in before/after diagrams:

```plantuml
group #LightGreen New: RFID wristband assignment
  checkin -> gear: POST /wristbands/assign
  gear --> checkin: Wristband ID
end
```

---

## Event Flow Diagrams

Event flow diagrams are **always auto-generated** from `architecture/metadata/events.yaml`. Manual PUML files for event flows are not permitted.

### Decomposition Rules

Event flows are decomposed by domain:

| Diagram | Level | Contents |
|---------|-------|----------|
| Overview (`event-flow-overview`) | L1 | One box per domain with event counts, connected through Kafka |
| Per-domain (`event-flow-{domain}`) | L2 | Specific services and named events for one domain |

Never create a monolithic "all events" diagram.

---

## Wireframes (Excalidraw)

UI wireframes are maintained as Excalidraw JSON files.

### Source Location

```
architecture/wireframes/
  web-guest-portal/
    check-in-confirmation.excalidraw     # Guest check-in completion screen
  web-ops-dashboard/
    live-tracking.excalidraw             # Real-time adventure tracking map
  app-guest-mobile/
    adventure-selection.excalidraw       # Mobile adventure search and booking
```

### Editing Wireframes

**Option 1: VS Code (recommended)**

Install the Excalidraw extension:

1. Search "Excalidraw" in VS Code Extensions (or install `pomdtr.excalidraw-editor`)
2. Open any `.excalidraw` file — you get a live visual editor inside VS Code
3. Save and commit

**Option 2: excalidraw.com**

1. Open [excalidraw.com](https://excalidraw.com)
2. Upload the `.excalidraw` JSON file
3. Edit the design
4. Export as JSON and save back to `architecture/wireframes/{app}/`

### Naming Convention

- Kebab-case, descriptive: `check-in-confirmation.excalidraw`, `live-tracking.excalidraw`
- No version numbers in filenames — use git history for versioning

### Publishing

Commit only the `.excalidraw` source file. CI automatically generates:

- SVG previews for embedding in documentation
- Interactive HTML viewers for design collaboration
- Markdown wrapper pages

### When Wireframes Drive Architecture

Wireframe changes should precede API contract changes — design flows first, then define integration points. Wireframes inform:

- Which fields are displayed (drives API response schema)
- How data is paginated or filtered (drives query parameter design)
- User interaction patterns (drives event schema)

---

## SVG Embedding in Portal Pages

### Use `<object>` Tags, Not `<img>`

```html
<!-- Good - clickable links inside SVG work -->
<object data="../svg/filename.svg" type="image/svg+xml" style="width:100%"></object>

<!-- Bad - SVG rendered as flat image, links disabled -->
<img src="../svg/filename.svg" />
```

### Relative Path Rules

MkDocs builds each page into its own directory (e.g., `svc-check-in/index.html`), so SVG references from a page at `/microservices/svc-check-in/` must use `../svg/filename.svg` (not `svg/filename.svg`).

---

## Reference

- [C4 Model Standard](../standards/c4-model/index.md) — notation guide and checklist
- [C4-PlantUML Guide](../standards/c4-model/c4-plantuml-guide.md) — macros and syntax
- [Diagram Checklist](../standards/c4-model/c4-diagram-checklist.md) — review checklist for diagrams
