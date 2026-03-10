# NovaTrek Adventures — Business Capability Map Analysis and Integration Plan

| | |
|-----------|-------|
| **Author** | Christopher Blaisdell |
| **Date** | 2026-03-06 |
| **Status** | Proposed |
| **Purpose** | Identify all business capabilities, assess implementation coverage, and plan integration into the NovaTrek Architecture Portal |

---

## 1. What NovaTrek Adventures Does

NovaTrek Adventures is an outdoor adventure experience company that connects guests with guided trips — hiking, kayaking, rock climbing, mountain biking, and 20+ other adventure categories. The company manages the full lifecycle from trip discovery and booking through day-of-adventure operations, safety compliance, and post-trip engagement.

The platform is a microservice architecture comprising **21 services** across **9 business domains**, **3 frontend applications** (guest web portal, operations dashboard, mobile companion app), and **9 domain events** flowing through Apache Kafka. The system supports approximately 5,000 check-ins/day, 2,000 reservations/day, and 10,000 catalog reads/day during peak season.

---

## 2. Business Capability Map

A business capability map describes WHAT an organization does, independent of HOW it does it. Capabilities are stable over time — even as technology changes, the business still needs to "manage reservations" or "process payments." Mapping capabilities to services reveals coverage gaps, redundancies, and alignment between business needs and technical architecture.

### Level 1 Capabilities (7 domains)

| # | Level 1 Capability | Description |
|---|-------------------|-------------|
| 1 | **Guest Experience** | Everything the guest interacts with: identity, discovery, booking, loyalty, communications, memories |
| 2 | **Adventure Operations** | Day-of execution: check-in, scheduling, guide management, trail operations, transport |
| 3 | **Safety and Risk** | Regulatory compliance, incident response, emergency coordination, environmental monitoring |
| 4 | **Resource Management** | Physical assets: gear, vehicles, locations, procurement, capacity |
| 5 | **Revenue and Finance** | Payment processing, pricing, analytics, financial reporting |
| 6 | **Partner Ecosystem** | Third-party booking channels, affiliates, external integrations |
| 7 | **Platform Services** | Cross-cutting technical capabilities: notifications, location, weather, search |

### Level 2 Capabilities (34 total)

#### 1. Guest Experience (8 capabilities)

| # | Capability | Implementing Service | Status |
|---|-----------|---------------------|--------|
| 1.1 | Guest Identity and Profile Management | svc-guest-profiles | IMPLEMENTED |
| 1.2 | Adventure Discovery and Browsing | svc-trip-catalog + web-guest-portal | IMPLEMENTED |
| 1.3 | Reservation Management | svc-reservations | IMPLEMENTED |
| 1.4 | Loyalty and Rewards | svc-loyalty-rewards | IMPLEMENTED |
| 1.5 | Guest Communications | svc-notifications | IMPLEMENTED |
| 1.6 | Trip Media and Memories | svc-media-gallery | IMPLEMENTED |
| 1.7 | Reviews and Feedback | — | NOT IMPLEMENTED |
| 1.8 | Personalized Recommendations | — | NOT IMPLEMENTED |

#### 2. Adventure Operations (5 capabilities)

| # | Capability | Implementing Service | Status |
|---|-----------|---------------------|--------|
| 2.1 | Day-of-Adventure Check-In | svc-check-in | IMPLEMENTED |
| 2.2 | Schedule Planning and Optimization | svc-scheduling-orchestrator | IMPLEMENTED |
| 2.3 | Guide Assignment and Management | svc-guide-management | IMPLEMENTED |
| 2.4 | Trail Operations | svc-trail-management | IMPLEMENTED |
| 2.5 | Transport Coordination | svc-transport-logistics | IMPLEMENTED |

#### 3. Safety and Risk (5 capabilities)

| # | Capability | Implementing Service | Status |
|---|-----------|---------------------|--------|
| 3.1 | Waiver and Compliance Management | svc-safety-compliance | IMPLEMENTED |
| 3.2 | Incident Reporting and Response | svc-safety-compliance | IMPLEMENTED |
| 3.3 | Emergency Response Coordination | svc-emergency-response | IMPLEMENTED |
| 3.4 | Wildlife and Environmental Monitoring | svc-wildlife-tracking | IMPLEMENTED |
| 3.5 | Weather Monitoring and Alerting | svc-weather | IMPLEMENTED |

#### 4. Resource Management (5 capabilities)

| # | Capability | Implementing Service | Status |
|---|-----------|---------------------|--------|
| 4.1 | Gear Inventory and Tracking | svc-gear-inventory | IMPLEMENTED |
| 4.2 | Procurement and Vendor Management | svc-inventory-procurement | IMPLEMENTED |
| 4.3 | Location and Capacity Management | svc-location-services | IMPLEMENTED |
| 4.4 | Vehicle Fleet Management | svc-transport-logistics | IMPLEMENTED |
| 4.5 | Facility and Venue Management | — | NOT IMPLEMENTED |

#### 5. Revenue and Finance (5 capabilities)

| # | Capability | Implementing Service | Status |
|---|-----------|---------------------|--------|
| 5.1 | Payment Processing | svc-payments | IMPLEMENTED |
| 5.2 | Trip Pricing and Yield Management | svc-trip-catalog (partial) | PARTIAL |
| 5.3 | Analytics and Business Intelligence | svc-analytics | IMPLEMENTED |
| 5.4 | Financial Reporting and Reconciliation | svc-payments (partial) | PARTIAL |
| 5.5 | Refund and Dispute Management | svc-payments (partial) | PARTIAL |

#### 6. Partner Ecosystem (3 capabilities)

| # | Capability | Implementing Service | Status |
|---|-----------|---------------------|--------|
| 6.1 | Third-Party Booking Channels | svc-partner-integrations | IMPLEMENTED |
| 6.2 | Affiliate and Commission Management | svc-partner-integrations (partial) | PARTIAL |
| 6.3 | Channel Rate Parity Management | — | NOT IMPLEMENTED |

#### 7. Platform Services (3 capabilities)

| # | Capability | Implementing Service | Status |
|---|-----------|---------------------|--------|
| 7.1 | Notification Delivery (Multi-Channel) | svc-notifications | IMPLEMENTED |
| 7.2 | Geospatial and Location Services | svc-location-services | IMPLEMENTED |
| 7.3 | Search and Discovery Engine | — | NOT IMPLEMENTED |

---

## 3. Coverage Summary

| Status | Count | Percentage |
|--------|-------|-----------|
| IMPLEMENTED | 24 | 70.6% |
| PARTIAL | 4 | 11.8% |
| NOT IMPLEMENTED | 6 | 17.6% |
| **Total** | **34** | **100%** |

### Unimplemented Capabilities (6)

| # | Capability | Business Justification | Recommended Priority |
|---|-----------|----------------------|---------------------|
| 1.7 | **Reviews and Feedback** | Guest trip reviews drive future bookings. Guide ratings exist in svc-guide-management but guest-facing trip reviews do not. Without this, the guest portal has no social proof mechanism. | HIGH |
| 1.8 | **Personalized Recommendations** | "Guests who enjoyed kayaking also booked..." increases average booking value. Currently guests browse a flat catalog with no personalization. | MEDIUM |
| 4.5 | **Facility and Venue Management** | Base camps, equipment stations, parking areas, and trailhead facilities need capacity tracking and maintenance scheduling. Currently handled informally through svc-location-services. | LOW |
| 5.5 | **Refund and Dispute Management** | svc-payments has a basic refund endpoint but lacks dispute workflows, chargeback handling, and refund policy enforcement. This is a significant operational gap. | HIGH |
| 6.3 | **Channel Rate Parity** | Ensuring consistent pricing across direct bookings and partner channels. Without this, partners may undercut direct pricing. | MEDIUM |
| 7.3 | **Search and Discovery Engine** | Dedicated full-text and faceted search across trips, trails, guides, and locations. Currently svc-trip-catalog has basic search but no cross-entity search or relevance ranking. | MEDIUM |

### Partial Capabilities (4)

| # | Capability | Gap Description |
|---|-----------|----------------|
| 5.2 | **Trip Pricing and Yield Management** | svc-trip-catalog has static pricing tiers but no dynamic yield management (demand-based pricing, seasonal adjustments, early-bird discounts) |
| 5.4 | **Financial Reporting and Reconciliation** | svc-payments provides daily summaries but lacks end-of-month reconciliation, revenue recognition, and partner settlement reports |
| 5.5 | **Refund and Dispute Management** | Basic refund endpoint exists but no dispute tracking, chargeback workflow, or policy enforcement |
| 6.2 | **Affiliate and Commission Management** | svc-partner-integrations tracks bookings but commission calculation and payout workflows are not defined |

---

## 4. How to Incorporate Capabilities into the NovaTrek Architecture Portal

The NovaTrek Architecture Portal (Azure Static Web Apps) currently organizes architecture artifacts by **technical structure** — services, events, actors, applications. Adding a **business capability view** creates a top-down navigation layer that connects business language to technical implementation.

### 4.1 New Portal Section: Business Capabilities

**Navigation placement:** Top-level nav item, positioned after "Service Catalog" and before "Applications."

```
nav:
  - Home: index.md
  - Service Catalog: services/index.md
  - Business Capabilities: capabilities/index.md    # NEW
  - Applications: applications/...
  - Microservices: microservices/...
  - ...
```

**Index page (`capabilities/index.md`)** would contain:

1. **Interactive Capability Map** — A visual grid or treemap showing all 7 Level 1 domains, expandable to 34 Level 2 capabilities
2. **Coverage Heatmap** — Color-coded status: green (implemented), amber (partial), red (not implemented)
3. **Service Mapping Table** — Which services realize each capability, with deep links to microservice pages
4. **Gap Analysis Summary** — The 6 unimplemented and 4 partial capabilities with business justification

### 4.2 Architecture Metadata Extension

Add a new metadata file: `architecture/metadata/capabilities.yaml`

```yaml
capabilities:
  - id: CAP-1
    name: Guest Experience
    level: 1
    children:
      - id: CAP-1.1
        name: Guest Identity and Profile Management
        level: 2
        status: implemented
        services:
          - svc-guest-profiles
        description: >
          Single source of truth for guest identity including profiles,
          certifications, medical info, and emergency contacts.
      - id: CAP-1.7
        name: Reviews and Feedback
        level: 2
        status: not-implemented
        services: []
        description: >
          Guest trip reviews and ratings that drive future bookings.
          Guide ratings exist but guest-facing trip reviews do not.
        gap_notes: >
          Would require a new svc-reviews service or extension to
          svc-media-gallery with review content types.
```

### 4.3 Generator Script

Create `portal/scripts/generate-capability-pages.py` that:

1. Reads `architecture/metadata/capabilities.yaml`
2. Cross-references with `architecture/metadata/microservices.yaml` (service domains)
3. Generates `portal/docs/capabilities/index.md` with:
   - Visual capability map (PlantUML or HTML/CSS grid)
   - Coverage statistics
   - Deep links to implementing service pages
4. Optionally generates per-capability detail pages for Level 2 capabilities

### 4.4 PlantUML Capability Map Diagram

Generate a C4-style capability map diagram showing:

- Level 1 domains as large containers
- Level 2 capabilities as components within containers
- Color-coded by implementation status
- Clickable links to service pages

### 4.5 Integration with Existing Pages

- **Service pages** (`portal/docs/microservices/svc-*.md`) — Add a "Capabilities Realized" section showing which business capabilities each service supports
- **Applications pages** (`portal/docs/applications/*.md`) — Add capability coverage matrix showing which capabilities each application exposes to users
- **Event catalog** (`portal/docs/events/index.md`) — Map events to capability workflows

### 4.6 Implementation Steps

| Step | Task | Effort |
|------|------|--------|
| 1 | Create `architecture/metadata/capabilities.yaml` with all 34 capabilities | Small |
| 2 | Write `portal/scripts/generate-capability-pages.py` generator | Medium |
| 3 | Add PlantUML capability map diagram generation | Medium |
| 4 | Wire into `portal/scripts/generate-all.sh` pipeline | Small |
| 5 | Add nav entry to `portal/mkdocs.yml` | Small |
| 6 | Cross-link from service and application pages | Medium |
| 7 | Test full pipeline and publish | Small |

---

## 5. Friendly URL Options

The current portal URL is:

```
https://architecture.novatrek.cc
```

This is the auto-generated Azure Static Web Apps hostname, which is not memorable or professional. Here are the options for adding a friendlier URL:

### Option A: Custom Domain on Azure Static Web Apps (Recommended)

Azure Static Web Apps supports custom domains with free managed TLS certificates. The infrastructure is already prepared:

- `infra/main.bicep` has a `customDomain` parameter and conditional resource block (lines 48, 88-91)
- `infra/parameters/prod.bicepparam` has `docs.novatrek.example.com` commented out (line 22)

**Steps to enable:**

1. **Register a domain** — Purchase a domain through any registrar. Suggested names:
   - `novatrek.dev` — clean, developer-friendly TLD (~$12/year on Google Domains / Cloudflare)
   - `novatrek-arch.dev` — explicitly architecture-focused
   - `novatrek.io` — common for tech platforms
   - `novatrek.pages.dev` — free via Cloudflare Pages (alternative hosting)

2. **Configure DNS** — Add a CNAME record pointing to the Azure SWA default hostname:
   ```
   docs.novatrek.dev  CNAME  mango-sand-083b8ce0f.4.azurestaticapps.net
   ```

3. **Validate domain ownership** — Azure requires a TXT record for validation:
   ```
   asuid.docs.novatrek.dev  TXT  <validation-token-from-azure>
   ```

4. **Uncomment the parameter** and redeploy infrastructure:
   ```bicep
   param customDomain = 'docs.novatrek.dev'
   ```

5. **Deploy** — Run:
   ```bash
   az deployment group create \
     --resource-group <rg-name> \
     --template-file infra/main.bicep \
     --parameters infra/parameters/prod.bicepparam
   ```

Azure automatically provisions and manages a free TLS certificate. No additional configuration needed.

### Option B: GitHub Pages Custom Domain (Alternative)

If migrating from Azure SWA to GitHub Pages:

- GitHub Pages supports custom domains with free TLS
- Configure via repository Settings > Pages
- Simpler setup but loses Azure SWA features (routing rules, headers configuration, auth)

### Option C: Cloudflare Proxy (Keep Azure SWA + Add Vanity URL)

Use Cloudflare as a DNS proxy in front of Azure SWA:

- Register domain with Cloudflare or transfer nameservers
- Set up CNAME proxied through Cloudflare
- Benefits: CDN caching, analytics, DDoS protection, page rules
- Free tier sufficient for documentation sites

### Recommendation

**Option A** is the simplest path since the infrastructure is already coded. The only action needed is:

1. Register a domain
2. Configure two DNS records (CNAME + TXT)
3. Uncomment one line in `prod.bicepparam`
4. Redeploy the Bicep template

The Standard SKU ($9/month) is required for custom domains on Azure SWA if the Free tier does not support it in your region. Check current Azure pricing.

---

## 6. Capability Map — Visual Reference

```
+------------------------------------------------------------------------+
|                     NOVATREK ADVENTURES                                 |
|                   Business Capability Map                               |
+------------------------------------------------------------------------+

+--------------------------+  +--------------------------+
| 1. GUEST EXPERIENCE      |  | 2. ADVENTURE OPERATIONS  |
|--------------------------|  |--------------------------|
| 1.1 Guest Identity   [G] |  | 2.1 Day-of Check-In  [G] |
| 1.2 Discovery         [G] |  | 2.2 Scheduling       [G] |
| 1.3 Reservations      [G] |  | 2.3 Guide Mgmt       [G] |
| 1.4 Loyalty           [G] |  | 2.4 Trail Ops        [G] |
| 1.5 Communications    [G] |  | 2.5 Transport        [G] |
| 1.6 Media/Memories    [G] |  +--------------------------+
| 1.7 Reviews           [R] |
| 1.8 Recommendations   [R] |
+--------------------------+

+--------------------------+  +--------------------------+
| 3. SAFETY AND RISK       |  | 4. RESOURCE MANAGEMENT   |
|--------------------------|  |--------------------------|
| 3.1 Waivers/Compliance[G]|  | 4.1 Gear Inventory   [G] |
| 3.2 Incident Response [G] |  | 4.2 Procurement      [G] |
| 3.3 Emergency Coord   [G] |  | 4.3 Location/Capacity[G] |
| 3.4 Wildlife Monitor  [G] |  | 4.4 Vehicle Fleet    [G] |
| 3.5 Weather Alerts    [G] |  | 4.5 Facility Mgmt    [R] |
+--------------------------+  +--------------------------+

+--------------------------+  +--------------------------+
| 5. REVENUE AND FINANCE   |  | 6. PARTNER ECOSYSTEM     |
|--------------------------|  |--------------------------|
| 5.1 Payments          [G] |  | 6.1 3P Bookings      [G] |
| 5.2 Pricing/Yield     [A] |  | 6.2 Affiliate Mgmt   [A] |
| 5.3 Analytics/BI      [G] |  | 6.3 Channel Parity   [R] |
| 5.4 Financial Reports [A] |  +--------------------------+
| 5.5 Refunds/Disputes  [A] |
+--------------------------+

+--------------------------+
| 7. PLATFORM SERVICES     |
|--------------------------|
| 7.1 Notifications     [G] |
| 7.2 Geospatial/Loc    [G] |
| 7.3 Search Engine     [R] |
+--------------------------+

Legend: [G] = Implemented   [A] = Partial   [R] = Not Implemented
```

---

## 7. Capability Rollup — Making Ticket Solutions Grow the Architecture

### 7.1 The Problem: Architecture Amnesia

Today, when an architect solutions a ticket (e.g., NTK-10003 "Unregistered Guest Self-Check-In"), the work produces valuable artifacts:

- Impact assessments per service (`i.impacts/impact.1/impact.1.md` for svc-check-in, etc.)
- Architecture decisions in MADR format (`d.decisions/decisions.md`)
- User stories with acceptance criteria
- PlantUML sequence diagrams showing new flows

But these artifacts are **orphaned once the ticket closes**. They live in a ticket folder, disconnected from the capability map, the service pages, and the architecture metadata. The next architect who picks up a related ticket starts from scratch — reading old specs, re-discovering service boundaries, re-learning the same integration patterns. The architecture does not accumulate intelligence. It resets.

The current flow is:

```
Ticket → Solution Design → Impact Files → (manual) → Update metadata YAML → (manual) → Rebuild portal
                                         ↑
                                    This step gets skipped
```

The metadata YAML files (`cross-service-calls.yaml`, `data-stores.yaml`, `microservices.yaml`) are the source of truth for the portal, but nothing in the ticket workflow forces or even reminds the architect to update them. Impact files describe service changes in rich detail, but that detail evaporates when the ticket closes.

**What is missing**: A declared, traceable link from ticket → capability, and a workflow that makes capability rollup a natural byproduct of solutioning — not an afterthought.

### 7.2 The Rollup Model

The goal is a **three-layer traceability chain**:

```
L1 Capability
  └── L2 Capability
        └── L3 Capability (ticket-scoped feature / user story)
              └── Service Impact (API changes, schema changes, new events)
```

Today, ticket solutions produce the bottom layer (service impacts) and sometimes the third layer (user stories). But there is no declared link upward to L2 and L1 capabilities. Adding that link requires two things:

1. **A capability reference in every ticket solution** (the upward link)
2. **A capability changelog that accumulates over time** (the memory)

### 7.3 Ticket-to-Capability Declaration

Add a new metadata section to every solution design master document. This declares which capabilities the ticket touches and how:

**In the solution design header table:**

```markdown
| Field | Value |
|-------|-------|
| Version | 1.0 |
| Status | DRAFT |
| Ticket | NTK-10003 |
| Capabilities | CAP-1.1 (extends), CAP-2.1 (extends), CAP-1.3 (depends) |
```

**And a new file in the solution folder: `3.solution/c.capabilities/capabilities.md`:**

```markdown
# Capability Impact

## Capabilities Modified

| Capability ID | Capability Name | Impact Type | Description |
|--------------|----------------|-------------|-------------|
| CAP-2.1 | Day-of-Adventure Check-In | EXTENDS | Adds reservation-based lookup flow for unregistered guests — new orchestration path in check-in lifecycle |
| CAP-1.1 | Guest Identity and Profile Management | EXTENDS | Introduces temporary guest profile creation with 90-day TTL and merge-on-return semantics |

## Capabilities Depended Upon (Read-Only)

| Capability ID | Capability Name | Usage |
|--------------|----------------|-------|
| CAP-1.3 | Reservation Management | Reads reservation data to verify guest identity during kiosk check-in |
| CAP-3.1 | Waiver and Compliance Management | Reads waiver status to determine safety compliance before check-in completion |

## Proposed New L3 Capabilities

| Parent | L3 ID | L3 Name | Description |
|--------|-------|---------|-------------|
| CAP-2.1 | CAP-2.1.4 | Reservation-Based Guest Lookup | Kiosk lookup flow using confirmation code, last name, adventure date, and party size |
| CAP-1.1 | CAP-1.1.3 | Temporary Guest Profile Lifecycle | Create, merge, and expire temporary profiles for walk-in or unregistered guests |
```

**Impact types:**
- `EXTENDS` — Adds new behavior to an existing capability (new endpoint, new flow, new data)
- `MODIFIES` — Changes existing behavior of a capability (schema change, logic change)
- `CREATES` — Introduces a brand new L2 or L3 capability
- `DEPENDS` — Uses the capability read-only (no changes, but documents the dependency)
- `DEPRECATES` — Marks a capability or sub-capability as being phased out

### 7.4 Capability Changelog (Architecture Memory)

Create `architecture/metadata/capability-changelog.yaml` — an append-only log that accumulates every capability-touching change:

```yaml
changelog:
  - ticket: NTK-10003
    date: 2026-02-20
    status: APPROVED
    capabilities:
      - id: CAP-2.1
        impact: extends
        summary: "Reservation-based kiosk lookup for unregistered guests"
        l3_added:
          - id: CAP-2.1.4
            name: "Reservation-Based Guest Lookup"
      - id: CAP-1.1
        impact: extends
        summary: "Temporary guest profile with 90-day TTL"
        l3_added:
          - id: CAP-1.1.3
            name: "Temporary Guest Profile Lifecycle"
    services_impacted:
      - svc-check-in
      - svc-guest-profiles
      - svc-safety-compliance
      - svc-reservations
    decisions:
      - ADR-006-orchestrator-pattern-checkin
      - ADR-007-four-field-identity-verification
      - ADR-008-temporary-guest-profile

  - ticket: NTK-10005
    date: 2026-03-03
    status: DRAFT
    capabilities:
      - id: CAP-2.1
        impact: modifies
        summary: "RFID wristband tag field added to check-in schema"
    services_impacted:
      - svc-check-in
    decisions: []
```

This file is the **architecture memory**. It answers questions that are currently unanswerable:

- "What has changed about our check-in capability in the last 6 months?" — Filter by `CAP-2.1`
- "Which tickets drove changes to svc-guest-profiles?" — Filter by `services_impacted`
- "How has our Guest Experience domain evolved?" — Filter by `CAP-1.*`
- "Which capabilities have the most churn?" — Count entries per capability ID
- "What L3 capabilities have emerged from ticket work?" — Aggregate `l3_added` entries

### 7.5 Capability Evolution in the Portal

The capability page generator (Section 4.3) should consume the changelog to produce:

1. **Capability Timeline** — Per-capability page showing when changes occurred, which tickets drove them, and what L3 capabilities emerged:

   ```
   ## CAP-2.1: Day-of-Adventure Check-In

   ### Evolution Timeline

   | Date | Ticket | Change | L3 Added |
   |------|--------|--------|----------|
   | 2026-02-20 | NTK-10003 | Reservation-based kiosk lookup | CAP-2.1.4 |
   | 2026-03-03 | NTK-10005 | RFID wristband tag field | — |
   ```

2. **Service-to-Capability Matrix** — Auto-generated from the changelog, showing which services realize which capabilities and how they evolved over time

3. **Capability Health Indicators** — Capabilities with high churn might indicate poor initial design. Capabilities with zero tickets might be stale or over-engineered.

4. **Decision Traceability** — Each capability page links to all ADRs that shaped it, and each ADR links back to the capabilities it affected

### 7.6 The Rollup Workflow

Here is how the rollup works in practice during ticket solutioning:

```
1. Architect picks up ticket
   │
2. Reads ticket requirements (1.requirements/)
   │
3. Opens capabilities.yaml — finds relevant L1/L2 capabilities
   │
4. Creates 3.solution/c.capabilities/capabilities.md
   │  ├── Declares which capabilities are EXTENDED/MODIFIED/CREATED
   │  ├── Identifies L3 capabilities being added
   │  └── Documents capability dependencies (read-only usage)
   │
5. Writes impact files per service (3.solution/i.impacts/)
   │  └── Each impact references the capability it serves
   │
6. Solution is approved
   │
7. Architect updates architecture metadata:
   │  ├── capabilities.yaml — adds new L3 entries if any
   │  ├── capability-changelog.yaml — appends ticket entry
   │  ├── cross-service-calls.yaml — if new integrations
   │  ├── microservices.yaml — if new endpoints
   │  └── events.yaml — if new domain events
   │
8. Portal generator runs (CI or manual)
   │  ├── Capability pages regenerated with timeline
   │  ├── Service pages show capability associations
   │  └── Capability map heatmap reflects current state
   │
9. Architecture is now richer than before the ticket
```

**Step 7 is the critical difference.** Today it is optional and often skipped. In this model, capability rollup is an explicit deliverable of every solution design — the architect cannot mark a solution as APPROVED without the capability declaration and changelog entry.

### 7.7 AI-Assisted Rollup (Platform Automation)

The AI agent (Copilot or Roo Code) can automate parts of this rollup during solutioning:

1. **Auto-suggest capabilities**: When the agent reads a ticket, it can match keywords and affected services against `capabilities.yaml` to pre-populate `c.capabilities/capabilities.md`

2. **Changelog generation**: After the solution is approved, the agent can auto-generate the `capability-changelog.yaml` entry from the capabilities declaration and impact files

3. **Metadata diff**: The agent can compare the solution's impact files against the current metadata YAML files and generate a "metadata update PR" showing exactly what changed:
   - New endpoint in `cross-service-calls.yaml`
   - New table in `data-stores.yaml`
   - New L3 capability in `capabilities.yaml`

4. **Staleness detection**: The agent can flag capabilities that have not been touched by any ticket in a configurable period, suggesting they may need review or retirement

5. **Conflict detection**: If two in-flight tickets both declare `MODIFIES CAP-2.1`, the agent can surface the potential conflict before either solution is approved

### 7.8 L3 Capabilities — The Emergent Layer

L1 and L2 capabilities are defined top-down in the capability map (Section 2). They are stable and business-aligned. **L3 capabilities emerge bottom-up from ticket work.** They are the specific features and flows that realize the higher-level capabilities.

Over time, the L3 layer becomes the most valuable part of the capability map because it captures the **actual architecture** — not what was planned, but what was built:

```
CAP-2.1 Day-of-Adventure Check-In (L2 — planned)
  ├── CAP-2.1.1 Standard Guest Check-In (L3 — baseline)
  ├── CAP-2.1.2 Group Check-In (L3 — NTK-10001)
  ├── CAP-2.1.3 Guide-Assisted Check-In (L3 — NTK-10002)
  ├── CAP-2.1.4 Reservation-Based Guest Lookup (L3 — NTK-10003)
  └── CAP-2.1.5 RFID Wristband Assignment (L3 — NTK-10005)
```

Each L3 links to:
- The ticket that created it
- The services that implement it
- The ADRs that shaped its design
- The user stories that define its acceptance criteria

This is how architecture becomes a **living, growing record** instead of a point-in-time snapshot that immediately starts decaying.

### 7.9 Preventing Architecture Amnesia — Checklist

Add this to the architecture review checklist (copilot-instructions.md and solution design templates):

- [ ] Capability IDs declared in solution design header (`Capabilities` field)
- [ ] `3.solution/c.capabilities/capabilities.md` created with impact types
- [ ] New L3 capabilities identified and named
- [ ] `capability-changelog.yaml` entry drafted
- [ ] Existing metadata YAML files updated to reflect new endpoints, schemas, or integrations
- [ ] Portal regenerated to verify capability pages reflect the changes

### 7.10 Rollup Summary

| Layer | Source | Updated By | Frequency |
|-------|--------|-----------|-----------|
| L1 Capability | `capabilities.yaml` | Business/architecture leadership | Rarely (annual strategy) |
| L2 Capability | `capabilities.yaml` | Solution architects | Occasionally (new domain area) |
| L3 Capability | `capabilities.yaml` + `capability-changelog.yaml` | Ticket solutioning | Every ticket |
| Service Impact | `cross-service-calls.yaml`, `data-stores.yaml`, etc. | Ticket solutioning | Every ticket |
| Portal View | Generated from all of the above | CI pipeline | Every push |

The key insight: **L1 and L2 are top-down and stable. L3 is bottom-up and emergent. The changelog is the bridge that makes bottom-up work accumulate into top-down visibility.**

---

## 8. Next Steps

1. **Immediate**: Create `architecture/metadata/capabilities.yaml` with the 34 L2 capabilities defined in Section 2
2. **Immediate**: Create `architecture/metadata/capability-changelog.yaml` with retrospective entries for existing tickets (NTK-10001 through NTK-10005)
3. **Short term**: Add `3.solution/c.capabilities/` to the solution design folder template so every future ticket includes capability declarations
4. **Short term**: Write the capability page generator (`portal/scripts/generate-capability-pages.py`) consuming both `capabilities.yaml` and `capability-changelog.yaml`, and wire it into `generate-all.sh`
5. **Short term**: Register a custom domain and enable the Bicep custom domain parameter
6. **Medium term**: Update `copilot-instructions.md` and Roo Code instructions with the capability rollup checklist (Section 7.9) so the AI agent auto-suggests capability mappings during solutioning
7. **Medium term**: Implement the 6 missing capabilities as new services or extensions to existing services (requires new OpenAPI specs, metadata entries, and ADRs for each)
8. **Ongoing**: Every ticket solution must produce a capability declaration and changelog entry — this is what makes the architecture grow instead of reset
