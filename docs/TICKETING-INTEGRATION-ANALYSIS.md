# NovaTrek Adventures — Ticketing Integration Analysis and Plan

| | |
|-----------|-------|
| **Author** | Christopher Blaisdell |
| **Date** | 2026-03-06 |
| **Status** | Proposed |
| **Purpose** | Evaluate open-source ticketing solutions, plan integration with the NovaTrek Architecture Portal, define ticket-to-capability rollup structure, and ensure AI awareness of all tickets |

---

## 1. Problem Statement

The continuous architecture platform needs a real ticketing system to replace the mock JIRA scripts. Currently, tickets live as JSON records in `phases/phase-1-ai-tool-cost-comparison/workspace/scripts/mock-data/tickets.json` and are read by `mock-jira-client.py` — a pure Python script with no network calls.

This served Phase 1 evaluation well, but the platform vision demands:

1. **Navigable tickets in the portal** — Architects and stakeholders should browse user stories directly from the NovaTrek Architecture Portal, with deep links from capability pages to the tickets that shaped them
2. **Capability rollup** — Every user story defines use cases that map to L1/L2/L3 capabilities (per Section 7 of `CAPABILITY-MAP-ANALYSIS.md`). The ticketing system must support structured capability tagging
3. **AI awareness** — The AI agent (Copilot or Roo Code) MUST be able to read all tickets, their full descriptions, comments, and linked capabilities without manual copy-pasting
4. **Self-hosted on Azure** — The solution must run on Azure infrastructure within the existing resource group, using free or open-source software
5. **User stories as first-class artifacts** — Tickets should follow a structured template: user story format, acceptance criteria, capability references, and use case descriptions

---

## 2. Current State: Mock JIRA Infrastructure

### 2.1 What Exists Today

| Component | Location | Purpose |
|-----------|----------|---------|
| Mock JIRA CLI | `phases/.../scripts/mock-jira-client.py` | Python stdlib script reading JSON |
| Ticket data | `phases/.../scripts/mock-data/tickets.json` | 7 tickets (NTK-10001 through NTK-10007) |
| Solution folders | `phases/.../workspace/work-items/tickets/_NTK-XXXXX-*/` | Architect workspace per ticket |
| Mock Elastic | `phases/.../scripts/mock-elastic-searcher.py` | Synthetic production logs |
| Mock GitLab | `phases/.../scripts/mock-gitlab-client.py` | Synthetic merge request data |

### 2.2 Ticket Data Model (Current)

```json
{
  "key": "NTK-10003",
  "summary": "Support Unregistered Guest Self-Service Check-In",
  "description": "Multi-line description with acceptance criteria",
  "status": "In Progress",
  "priority": "Critical",
  "assignee": "alex.chen",
  "reporter": "sarah.martinez",
  "labels": ["architecture", "guest-experience"],
  "created": "2026-01-15T09:00:00Z",
  "updated": "2026-02-20T14:30:00Z",
  "sprint": "Sprint 26-3",
  "components": ["svc-check-in", "svc-guest-identity", "svc-scheduling-orchestrator"],
  "comments_count": 4
}
```

### 2.3 What Is Missing

| Gap | Impact |
|-----|--------|
| No capability references | Cannot trace tickets to L1/L2/L3 capabilities |
| No use case structure | Acceptance criteria are free-text, not structured use cases |
| No portal integration | Tickets are invisible from the architecture portal |
| No real workflow | Status transitions are manual JSON edits |
| No AI-native access | AI agent must run a mock script and parse formatted output |
| Not scalable | Flat JSON file works for 7 tickets, not for 70 or 700 |

---

## 3. Requirements for a Ticketing Solution

### 3.1 Hard Requirements

| # | Requirement | Rationale |
|---|-------------|-----------|
| R1 | Free or open-source with permissive license | POC budget constraint |
| R2 | Self-hostable on Azure | Data isolation — no SaaS dependency |
| R3 | REST API for CRUD operations | AI agent integration via HTTP calls |
| R4 | Custom fields support | Capability IDs, use case references, impact types |
| R5 | Markdown support in descriptions | Architecture documentation lives in Markdown |
| R6 | Can run as a container (Docker) | Azure deployment via Container Apps or App Service |
| R7 | Lightweight — runs on small infrastructure | POC does not justify a $200/month VM |

### 3.2 Desired Features

| # | Feature | Rationale |
|---|---------|-----------|
| D1 | Board/Kanban view | Visual workflow management |
| D2 | Labels/tags | Capability tagging (CAP-1.1, CAP-2.1, etc.) |
| D3 | File attachments | Attach solution designs, diagrams |
| D4 | Webhooks or event hooks | Trigger portal regeneration on ticket updates |
| D5 | Import/export (JSON/CSV) | Migrate from current mock data seamlessly |
| D6 | User/role management | Differentiate architects, stakeholders, developers |
| D7 | Search and filter API | AI queries like "all tickets touching CAP-2.1" |
| D8 | Lightweight database | SQLite or PostgreSQL, not Oracle |

---

## 4. Ticketing Solution Evaluation

### 4.1 Candidates

| Tool | License | Language | Database | Docker | API | Custom Fields |
|------|---------|----------|----------|--------|-----|---------------|
| **Plane** | AGPL-3.0 | Python/TypeScript | PostgreSQL | Yes | REST + GraphQL | Yes (via properties) |
| **Leantime** | AGPL-3.0 | PHP | MySQL/MariaDB | Yes | REST | Yes |
| **Taiga** | MPL-2.0 | Python (Django) | PostgreSQL | Yes | REST | Yes (custom attributes) |
| **OpenProject** | GPL-3.0 | Ruby on Rails | PostgreSQL | Yes | REST (HAL+JSON) | Yes (custom fields) |
| **Vikunja** | AGPL-3.0 | Go | SQLite/PostgreSQL/MySQL | Yes | REST | Yes (via attributes) |
| **Focalboard** | Apache-2.0+ | Go/TypeScript | SQLite/PostgreSQL/MySQL | Yes | REST | Yes (property-based) |
| **WeKan** | MIT | JavaScript (Meteor) | MongoDB | Yes | REST | Yes (custom fields) |

### 4.2 Evaluation Matrix

| Criterion | Weight | Plane | Taiga | Vikunja | Focalboard | OpenProject |
|-----------|--------|-------|-------|---------|------------|-------------|
| **API completeness** | 25% | 5 | 4 | 4 | 3 | 5 |
| **Resource footprint** | 20% | 2 | 3 | 5 | 5 | 2 |
| **Custom field flexibility** | 20% | 5 | 4 | 3 | 4 | 5 |
| **Docker simplicity** | 15% | 3 | 3 | 5 | 5 | 3 |
| **Community and maturity** | 10% | 4 | 4 | 3 | 3 | 5 |
| **AI integration ease** | 10% | 4 | 4 | 4 | 3 | 4 |
| **Weighted Score** | | **3.85** | **3.60** | **4.15** | **3.95** | **3.65** |

Scale: 1 (poor) — 5 (excellent)

### 4.3 Top 3 Recommendations

#### Option A: Vikunja (Recommended)

**Why Vikunja fits the NovaTrek platform:**

- **Single Go binary** — Minimal resource footprint. Runs on Azure Container Apps with 0.25 vCPU / 0.5 GB RAM
- **SQLite support** — No external database required for a POC. Upgrade path to PostgreSQL if needed
- **Clean REST API** — Full CRUD on tasks, labels, projects, and attributes. Well-documented OpenAPI spec
- **Docker image under 50MB** — Fast cold starts on Container Apps
- **Labels support** — Perfect for capability tagging (create labels like `CAP-1.1`, `CAP-2.1`, etc.)
- **Markdown descriptions** — Native Markdown rendering in task descriptions
- **Webhooks** — Can trigger portal regeneration on task state changes
- **CalDAV support** — Optionally sync with calendar tools for schedule-aware tickets
- **AGPL-3.0** — Free for self-hosted use

**Estimated Azure cost:** $5-10/month on Container Apps consumption plan (scale to zero when idle)

**Trade-offs:**
- Less feature-rich than Plane or OpenProject for enterprise PM workflows
- No built-in Gantt charts (not needed for architecture ticketing)
- Custom fields are label-based rather than typed properties

#### Option B: Focalboard

**Why Focalboard fits:**

- **Single Go binary** — Same lightweight profile as Vikunja
- **Property-based custom fields** — Define typed properties (text, number, select, multi-select, date) per board. Ideal for capability IDs as a multi-select property
- **Board/list/calendar views** — Visual ticket management out of the box
- **SQLite default** — Zero external dependencies
- **Apache-2.0 license** — Most permissive option
- **Originally Mattermost project** — Well-engineered, though community maintenance varies since Mattermost pivoted

**Trade-offs:**
- API is functional but less documented than Vikunja or Plane
- Smaller active community since Mattermost discontinuation
- No built-in webhooks (would need polling or database triggers)

#### Option C: Plane

**Why Plane fits:**

- **Most JIRA-like experience** — Familiar UI for teams coming from JIRA
- **Cycles, modules, views** — Rich project management features
- **REST + GraphQL API** — Comprehensive programmatic access
- **Issue properties** — Typed custom fields (text, number, select, multi-select, date, relation)
- **Webhooks** — Event-driven integration
- **Active development** — Rapid release cycle, growing community

**Trade-offs:**
- **Heavy footprint** — Requires PostgreSQL, Redis, and multiple services (API, worker, web, proxy). Minimum 1 GB RAM, typically 2-4 GB
- **Complex Docker Compose** — 5+ containers vs. Vikunja's 1
- **Azure cost** — $30-50/month on Container Apps or App Service due to multiple containers
- **AGPL-3.0** — Requires source disclosure if modified and distributed

---

## 5. Recommended Architecture: Vikunja on Azure

### 5.1 Deployment Topology

```
Azure Resource Group: rg-continuous-architecture
├── Static Web App: NovaTrek Architecture Portal
│   └── https://mango-sand-083b8ce0f.4.azurestaticapps.net
│
├── Container App: Vikunja Ticketing
│   ├── Image: vikunja/vikunja:latest
│   ├── Port: 3456
│   ├── Storage: Azure File Share (SQLite persistence)
│   ├── Scale: 0-1 replicas (consumption plan)
│   └── URL: https://tickets.mango-sand-083b8ce0f.4.azurecontainerapps.io
│
├── Container Apps Environment: cae-continuous-architecture
│   └── Log Analytics Workspace
│
└── Storage Account: Vikunja SQLite database file
    └── File Share: vikunja-data/vikunja.db
```

### 5.2 Infrastructure as Code

New Bicep module: `infra/modules/vikunja.bicep`

```bicep
// Vikunja ticketing on Azure Container Apps
param location string
param containerAppsEnvironmentId string
param storageAccountName string
param tags object = {}

resource vikunja 'Microsoft.App/containerApps@2024-03-01' = {
  name: 'vikunja-ticketing'
  location: location
  tags: tags
  properties: {
    environmentId: containerAppsEnvironmentId
    configuration: {
      ingress: {
        external: true
        targetPort: 3456
        transport: 'http'
      }
    }
    template: {
      containers: [
        {
          name: 'vikunja'
          image: 'vikunja/vikunja:latest'
          resources: {
            cpu: json('0.25')
            memory: '0.5Gi'
          }
          env: [
            { name: 'VIKUNJA_DATABASE_TYPE', value: 'sqlite' }
            { name: 'VIKUNJA_DATABASE_PATH', value: '/data/vikunja.db' }
            { name: 'VIKUNJA_SERVICE_FRONTENDURL', value: 'https://tickets.example.com' }
          ]
          volumeMounts: [
            { volumeName: 'vikunja-data', mountPath: '/data' }
          ]
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 1
      }
      volumes: [
        {
          name: 'vikunja-data'
          storageName: 'vikunja-storage'
          storageType: 'AzureFile'
        }
      ]
    }
  }
}
```

### 5.3 Cost Estimate

| Resource | SKU | Monthly Cost |
|----------|-----|-------------|
| Container Apps (consumption) | 0.25 vCPU, 0.5 GB | $0-5 (scale to zero) |
| Storage Account (File Share) | LRS, 1 GB | $0.06 |
| Container Apps Environment | Consumption | $0 (shared with other apps) |
| **Total** | | **$0.06-5.06/month** |

---

## 6. Ticket Structure: User Stories with Capability Rollup

### 6.1 Ticket Template (User Story Format)

Every ticket in Vikunja will follow this structured template:

```markdown
## User Story

**As a** [actor from actors.yaml],
**I want to** [action],
**So that** [business value].

## Use Cases

### UC-1: [Use Case Name]

**Preconditions:** [State before the use case begins]

**Main Flow:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Postconditions:** [State after the use case completes]

**Alternative Flows:**
- [2a] If [condition], then [alternative step]

### UC-2: [Use Case Name]
...

## Acceptance Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Capability Mapping

| Capability ID | Capability Name | Impact Type |
|--------------|----------------|-------------|
| CAP-X.Y | [Name] | EXTENDS / MODIFIES / CREATES / DEPENDS |

## Affected Services

| Service | Change Type |
|---------|------------|
| svc-xxx | API change / Schema change / New endpoint / Configuration |
```

### 6.2 Capability Tagging via Vikunja Labels

Create Vikunja labels matching the capability hierarchy:

**L1 Labels (color-coded by domain):**

| Label | Color | Hex |
|-------|-------|-----|
| `L1:Guest-Experience` | Blue | `#4A90D9` |
| `L1:Adventure-Operations` | Green | `#2E7D32` |
| `L1:Safety-Risk` | Red | `#C62828` |
| `L1:Resource-Management` | Orange | `#EF6C00` |
| `L1:Revenue-Finance` | Purple | `#6A1B9A` |
| `L1:Partner-Ecosystem` | Teal | `#00796B` |
| `L1:Platform-Services` | Gray | `#546E7A` |

**L2 Labels (subset examples):**

| Label | Parent |
|-------|--------|
| `CAP-1.1:Guest-Identity` | L1:Guest-Experience |
| `CAP-1.3:Reservations` | L1:Guest-Experience |
| `CAP-2.1:Check-In` | L1:Adventure-Operations |
| `CAP-2.2:Scheduling` | L1:Adventure-Operations |
| `CAP-3.1:Waivers-Compliance` | L1:Safety-Risk |

**Impact Type Labels:**

| Label | Meaning |
|-------|---------|
| `impact:extends` | Adds new behavior to existing capability |
| `impact:modifies` | Changes existing behavior |
| `impact:creates` | New L2 or L3 capability |
| `impact:depends` | Read-only dependency |

### 6.3 Example: NTK-10003 as a Vikunja Ticket

**Title:** Support Unregistered Guest Self-Service Check-In

**Labels:** `CAP-2.1:Check-In`, `CAP-1.1:Guest-Identity`, `L1:Adventure-Operations`, `L1:Guest-Experience`, `impact:extends`

**Description:**

```markdown
## User Story

**As a** Guest arriving for an adventure without prior registration,
**I want to** check in at a self-service kiosk using my reservation details,
**So that** I can begin my adventure without waiting for staff assistance.

## Use Cases

### UC-1: Reservation-Based Kiosk Lookup

**Preconditions:** Guest has a valid reservation but no guest profile in svc-guest-profiles.

**Main Flow:**
1. Guest approaches self-service kiosk
2. Guest enters confirmation code, last name, adventure date, and party size
3. System calls svc-reservations to validate the four-field combination
4. System creates a temporary guest profile in svc-guest-profiles (90-day TTL)
5. System checks waiver status via svc-safety-compliance
6. System completes check-in and issues wristband

**Postconditions:** Guest has an active check-in record and a temporary profile.

**Alternative Flows:**
- [3a] If reservation not found, display error and suggest front desk assistance
- [5a] If waiver not signed, redirect to digital waiver signing flow

### UC-2: Walk-In Guest Registration

**Preconditions:** Guest has no reservation and no profile.

**Main Flow:**
1. Guest selects "I don't have a reservation" at kiosk
2. System displays available adventures for today
3. Guest selects adventure and enters personal details
4. System creates reservation in svc-reservations
5. System creates temporary guest profile
6. System completes check-in

**Postconditions:** Guest has reservation, profile, and active check-in.

## Acceptance Criteria

- [ ] Kiosk lookup succeeds with valid confirmation code + last name + date + party size
- [ ] Temporary guest profile created with 90-day TTL
- [ ] Profile merges automatically if guest creates a full account within TTL
- [ ] Waiver validation enforced before check-in completion
- [ ] Unknown adventure categories default to Pattern 3 (Full Service)

## Capability Mapping

| Capability ID | Capability Name | Impact Type |
|--------------|----------------|-------------|
| CAP-2.1 | Day-of-Adventure Check-In | EXTENDS |
| CAP-1.1 | Guest Identity and Profile Management | EXTENDS |
| CAP-1.3 | Reservation Management | DEPENDS |
| CAP-3.1 | Waiver and Compliance Management | DEPENDS |

## Affected Services

| Service | Change Type |
|---------|------------|
| svc-check-in | New endpoint: POST /check-ins/lookup-reservation |
| svc-guest-profiles | New endpoint: POST /guests/temporary |
| svc-reservations | New query: GET /reservations/lookup (four-field) |
| svc-safety-compliance | No changes (read-only consumer) |
```

---

## 7. Portal Integration: Seeing Tickets from the NovaTrek Architecture Portal

### 7.1 Integration Architecture

The portal needs to display ticket data without requiring Vikunja to be online at build time. This is achieved through a **sync-and-generate** pattern:

```
Vikunja API (runtime)             Architecture Repo (build time)
┌──────────────┐                  ┌─────────────────────────────┐
│  REST API    │─── sync ────────>│ architecture/metadata/      │
│  /api/v1/    │    script        │   tickets.yaml              │
│              │                  │                             │
│  Tasks       │                  │ portal/scripts/             │
│  Labels      │                  │   generate-ticket-pages.py  │
│  Projects    │                  │                             │
└──────────────┘                  │ portal/docs/tickets/        │
                                  │   index.md                  │
                                  │   NTK-10003.md              │
                                  │   NTK-10005.md              │
                                  │   ...                       │
                                  └─────────────────────────────┘
```

### 7.2 Sync Script: `portal/scripts/sync-tickets.py`

A Python script that calls the Vikunja REST API and writes `architecture/metadata/tickets.yaml`:

```python
"""
Sync tickets from Vikunja API to architecture/metadata/tickets.yaml.

Usage:
  python3 portal/scripts/sync-tickets.py --url https://vikunja.example.com --token <api-token>

The script:
  1. Fetches all tasks from the NovaTrek project
  2. Fetches all labels (capability tags)
  3. Maps labels to capability IDs
  4. Writes structured YAML to architecture/metadata/tickets.yaml
"""
```

Output format:

```yaml
tickets:
  - key: NTK-10003
    summary: "Support Unregistered Guest Self-Service Check-In"
    status: "In Progress"
    priority: "Critical"
    assignee: "alex.chen"
    capabilities:
      - id: CAP-2.1
        impact: extends
      - id: CAP-1.1
        impact: extends
      - id: CAP-1.3
        impact: depends
      - id: CAP-3.1
        impact: depends
    services:
      - svc-check-in
      - svc-guest-profiles
      - svc-reservations
    use_cases:
      - UC-1: "Reservation-Based Kiosk Lookup"
      - UC-2: "Walk-In Guest Registration"
    solution_folder: "work-items/tickets/_NTK-10003-unregistered-guest-self-checkin/"
    created: "2026-01-15"
    updated: "2026-02-20"

  - key: NTK-10005
    summary: "Add Wristband RFID Field to Check-In Record"
    status: "New"
    priority: "Medium"
    assignee: null
    capabilities:
      - id: CAP-2.1
        impact: modifies
    services:
      - svc-check-in
    use_cases:
      - UC-1: "RFID Wristband Assignment During Check-In"
    solution_folder: "work-items/tickets/_NTK-10005-wristband-rfid-field/"
    created: "2026-03-01"
    updated: "2026-03-03"
```

### 7.3 Ticket Page Generator: `portal/scripts/generate-ticket-pages.py`

Generates MkDocs pages from `tickets.yaml`:

**Index page (`portal/docs/tickets/index.md`):**

- Summary table of all tickets with status, priority, capability tags, and assigned architect
- Filter controls (by capability, by service, by status)
- Cross-reference counts: "12 tickets touching Guest Experience, 8 touching Adventure Operations"
- Link to Vikunja instance for full ticket management

**Per-ticket pages (`portal/docs/tickets/NTK-10003.md`):**

- Full user story with use cases
- Capability mapping table with deep links to capability pages
- Affected services with deep links to microservice pages
- Solution design link (to the ticket folder in the workspace)
- Timeline: created, updated, status transitions
- Related ADRs (from capability-changelog.yaml)

### 7.4 Portal Navigation Update

```yaml
# portal/mkdocs.yml additions
nav:
  - Home: index.md
  - Service Catalog: services/index.md
  - Business Capabilities: capabilities/index.md
  - User Stories: tickets/index.md           # NEW
  - Applications: applications/...
  - Microservices: microservices/...
  - Event Catalog: events/index.md
  - Actor Catalog: actors/index.md
```

### 7.5 Cross-Linking Strategy

The ticket pages create a web of cross-references across the portal:

```
Capability Page (CAP-2.1: Check-In)
  └── "Tickets that shaped this capability"
       ├── NTK-10002: Adventure Category Classification
       ├── NTK-10003: Unregistered Guest Self-Check-In
       └── NTK-10005: Wristband RFID Field

Microservice Page (svc-check-in)
  └── "Tickets affecting this service"
       ├── NTK-10002 (new classification endpoint)
       ├── NTK-10003 (new lookup-reservation endpoint)
       └── NTK-10005 (schema change: rfid_tag field)

Ticket Page (NTK-10003)
  ├── "Capabilities" → CAP-2.1, CAP-1.1
  ├── "Services" → svc-check-in, svc-guest-profiles
  ├── "Decisions" → ADR-006, ADR-007, ADR-008
  └── "Solution" → work-items/tickets/_NTK-10003-*/
```

---

## 8. AI Awareness: Making Tickets Visible to the Agent

### 8.1 The AI Visibility Problem

The AI agent (Copilot or Roo Code) needs to know about ALL tickets to:

1. **Auto-suggest capability mappings** when solutioning a new ticket
2. **Detect conflicts** between in-flight tickets modifying the same capability
3. **Reference prior art** — "NTK-10003 already solved a similar problem for svc-check-in"
4. **Maintain architectural consistency** — Ensure new solutions do not contradict existing decisions

Currently, the agent discovers tickets by running `python3 scripts/mock-jira-client.py --list`. With Vikunja, the agent needs equivalent access.

### 8.2 Three AI Access Patterns

#### Pattern 1: File-Based (Recommended for Copilot)

The synced `architecture/metadata/tickets.yaml` file is automatically in the AI's context because it lives in the workspace. Copilot and Roo Code index workspace files and can read them without any API calls.

**Advantages:**
- Zero configuration — the file is just there
- Works offline — no Vikunja dependency during solutioning
- Version controlled — ticket state changes are tracked in git history
- The AI reads structured YAML natively

**Workflow:**
1. `sync-tickets.py` runs on a schedule or pre-commit hook
2. Commits `tickets.yaml` to the repository
3. AI agent reads `tickets.yaml` at the start of every session

#### Pattern 2: MCP Server (Advanced — For Real-Time Access)

Build a Model Context Protocol (MCP) server that wraps the Vikunja API, exposing tools like:

- `list_tickets(status?, capability?, service?)` — Filtered ticket listing
- `get_ticket(key)` — Full ticket detail with comments and history
- `search_tickets(query)` — Full-text search across all tickets
- `get_capability_tickets(capability_id)` — All tickets touching a capability

**Advantages:**
- Real-time data — no sync lag
- Rich filtering — AI can ask specific questions
- Comment history — AI sees the full conversation on a ticket

**Trade-offs:**
- Requires MCP server implementation and configuration
- Vikunja must be online during AI sessions
- More complex setup than file-based access

#### Pattern 3: Mock Script Upgrade (Transitional)

Keep the `mock-jira-client.py` pattern but point it at `tickets.yaml` instead of `tickets.json`, and add capability-aware commands:

```bash
# Current (mock JIRA)
python3 scripts/mock-jira-client.py --list
python3 scripts/mock-jira-client.py --ticket NTK-10003

# Upgraded (reads tickets.yaml)
python3 scripts/ticket-client.py --list
python3 scripts/ticket-client.py --ticket NTK-10003
python3 scripts/ticket-client.py --capability CAP-2.1          # NEW: filter by capability
python3 scripts/ticket-client.py --service svc-check-in        # NEW: filter by service
python3 scripts/ticket-client.py --impact extends              # NEW: filter by impact type
```

**Advantages:**
- Minimal change from current workflow
- No external dependencies
- AI already knows how to use CLI scripts from copilot-instructions.md

**Recommended approach:** Start with Pattern 1 (file-based) + Pattern 3 (script upgrade), graduate to Pattern 2 (MCP) when the platform matures.

### 8.3 Copilot Instructions Update

Add these commands to `.github/copilot-instructions.md`:

```markdown
### Ticket Commands

| Tool | Command | Purpose |
|------|---------|---------|
| Tickets — list all | `python3 scripts/ticket-client.py --list` | View all tickets |
| Tickets — by capability | `python3 scripts/ticket-client.py --capability CAP-2.1` | Tickets for a capability |
| Tickets — by service | `python3 scripts/ticket-client.py --service svc-check-in` | Tickets affecting a service |
| Tickets — ticket detail | `python3 scripts/ticket-client.py --ticket NTK-10003` | Full ticket with use cases |
```

### 8.4 AI Solutioning Workflow with Ticket Awareness

```
1. AI reads new ticket description
   │
2. AI reads architecture/metadata/tickets.yaml
   │  └── Identifies related tickets by capability or service overlap
   │
3. AI reads architecture/metadata/capabilities.yaml
   │  └── Finds the L1/L2 capabilities this ticket maps to
   │
4. AI checks existing solutions for related tickets
   │  └── Reads solution folders for prior art
   │
5. AI creates solution branch: solution/NTK-XXXXX-slug
   │  └── git checkout -b solution/NTK-XXXXX-slug
   │
6. AI drafts capability mapping (c.capabilities/capabilities.md)
   │  └── Declares EXTENDS/MODIFIES/CREATES with justification
   │
7. AI produces solution design (on the branch)
   │  └── References related tickets and decisions
   │
8. AI updates metadata YAML files (on the same branch)
   │  ├── capability-changelog.yaml — appends this ticket's impact
   │  ├── capabilities.yaml — adds new L3 capabilities
   │  └── cross-service-calls.yaml — if new integrations
   │
9. AI commits and pushes the branch
   │  └── Human architect opens PR for review
   │
10. PR reviewed, approved, merged → architecture grows
    └── The next ticket starts from a richer baseline
```

### 8.5 Ticket Status and Solution Branch Synchronization

Tickets in the ticketing system and solution branches in Git track related but distinct states. The mapping between them:

| Ticket Status | Solution Branch State | Portal Visibility |
|---------------|----------------------|-------------------|
| New | No branch exists | Ticket page only (no solution) |
| In Progress | Branch `solution/NTK-XXXXX-slug` exists, architect working | Ticket page only |
| In Review | PR open from solution branch | Ticket page only (PR preview via CI) |
| Done | PR merged to main, branch deleted | Ticket page + Solution page + capability rollup |
| Blocked | Branch may exist but work paused | Ticket page only |

This mapping is informational, not enforced by automation. The ticket system and Git are independent systems — the architect is responsible for keeping them synchronized. Future automation (webhooks from Git to the ticketing system, or vice versa) could automate status transitions:

- **On PR open**: Ticket status auto-updates to "In Review"
- **On PR merge**: Ticket status auto-updates to "Done"
- **On PR close without merge**: Ticket status reverts to "In Progress"

This automation is a Phase 3 enhancement (see Section 9.3). For Phase 1, manual synchronization is acceptable.

---

## 9. Migration Plan: Mock JIRA to Vikunja

### 9.1 Phase 1: Parallel Operation (No Vikunja Yet)

**Goal:** Adopt the structured ticket format and capability tagging without deploying Vikunja. Use `tickets.yaml` as the source of truth.

| Step | Task | Effort |
|------|------|--------|
| 1 | Create `architecture/metadata/tickets.yaml` with all 7 existing tickets migrated from `tickets.json` to the new schema (adding capability mappings, use cases) | Small |
| 2 | Rewrite `mock-jira-client.py` as `scripts/ticket-client.py` reading from `tickets.yaml` with capability/service filtering | Small |
| 3 | Create ticket page generator (`portal/scripts/generate-ticket-pages.py`) | Medium |
| 4 | Add User Stories section to `portal/mkdocs.yml` nav | Small |
| 5 | Update copilot-instructions.md with new ticket commands | Small |
| 6 | Publish to portal and validate cross-links | Small |

**Outcome:** Tickets are visible in the portal, tagged with capabilities, and the AI can query them — all without any external infrastructure.

### 9.2 Phase 2: Deploy Vikunja

**Goal:** Stand up Vikunja on Azure Container Apps as the authoritative ticket system.

| Step | Task | Effort |
|------|------|--------|
| 1 | Create `infra/modules/vikunja.bicep` container app definition | Medium |
| 2 | Add Vikunja parameters to `infra/parameters/prod.bicepparam` | Small |
| 3 | Wire the Vikunja module into `infra/main.bicep` | Small |
| 4 | Deploy and configure Vikunja (create project, set up labels for capabilities) | Medium |
| 5 | Seed Vikunja with all tickets from `tickets.yaml` via API | Small |
| 6 | Configure webhooks to trigger `sync-tickets.py` on ticket changes | Medium |

**Outcome:** Vikunja is the UI for ticket management. `sync-tickets.py` keeps `tickets.yaml` in sync. Portal pages are generated from `tickets.yaml` as before.

### 9.3 Phase 3: MCP Integration (Optional)

**Goal:** Give the AI agent real-time access to Vikunja.

| Step | Task | Effort |
|------|------|--------|
| 1 | Build MCP server wrapping Vikunja REST API (`scripts/mcp-vikunja-server.py`) | Medium |
| 2 | Register MCP server in VS Code settings | Small |
| 3 | Add MCP tool descriptions to copilot-instructions.md | Small |
| 4 | Test AI agent queries against live Vikunja data | Medium |

**Outcome:** AI agent can query tickets in real time, search by capability, and detect conflicts between in-flight tickets.

---

## 10. User Story Rollup to Capabilities — The Full Picture

### 10.1 Traceability Chain

```
User Story (ticket)
  └── Use Cases (structured in ticket description)
       └── Capability Mapping (labels + capabilities.md)
            └── L3 Capability (emergent from ticket work)
                 └── L2 Capability (stable business capability)
                      └── L1 Capability (strategic domain)
                           └── Service Impact (API/schema changes)
```

### 10.2 Example Rollup: NTK-10003

```
NTK-10003: "Support Unregistered Guest Self-Service Check-In"
│
├── UC-1: Reservation-Based Kiosk Lookup
│   └── CAP-2.1.4: Reservation-Based Guest Lookup (L3 — NEW)
│        └── CAP-2.1: Day-of-Adventure Check-In (L2)
│             └── CAP-2: Adventure Operations (L1)
│
├── UC-2: Walk-In Guest Registration
│   └── CAP-1.1.3: Temporary Guest Profile Lifecycle (L3 — NEW)
│        └── CAP-1.1: Guest Identity and Profile Management (L2)
│             └── CAP-1: Guest Experience (L1)
│
├── Services: svc-check-in (new endpoint), svc-guest-profiles (new endpoint)
├── Decisions: ADR-006, ADR-007, ADR-008
└── Solution: work-items/tickets/_NTK-10003-*/
```

### 10.3 Portal Views Enabled

| View | What It Shows | Who Benefits |
|------|--------------|--------------|
| Capability Map | Heatmap of L1/L2 with ticket count per capability | Architecture leadership |
| Capability Timeline | Chronological list of tickets that evolved a capability | Solution architects |
| Ticket Explorer | All tickets with capability tags, service links, status | All stakeholders |
| Service Impact History | Per-service list of all tickets and their changes | Service teams |
| Use Case Catalog | All use cases across all tickets, grouped by capability | Business analysts |
| Decision Traceability | ADRs linked to tickets linked to capabilities | Governance reviewers |

### 10.4 How This Prevents Architecture Amnesia

| Without Integration | With Integration |
|--------------------|-----------------|
| Ticket closes, solution design forgotten | Ticket closes, capability-changelog.yaml preserves the impact permanently |
| Next architect re-reads old specs from scratch | Next architect reads capability timeline showing all changes |
| No way to answer "what changed about check-in?" | Filter capability-changelog.yaml by CAP-2.1 — instant answer |
| Architecture documentation decays between releases | Architecture documentation grows with every ticket |
| AI agent has no memory between sessions | AI reads tickets.yaml and capability-changelog.yaml — full context |

---

## 11. Vikunja vs. Keeping Pure YAML (Decision Point)

Before committing to Vikunja, consider whether the YAML-only approach (Phase 1) might be sufficient for the POC:

### 11.1 YAML-Only Approach

```
architecture/metadata/tickets.yaml  ← Source of truth (hand-edited or AI-generated)
scripts/ticket-client.py           ← CLI for querying
portal/scripts/generate-ticket-pages.py  ← Portal page generator
```

**Pros:**
- Zero infrastructure cost
- Git-native — every change tracked, branching, PRs
- AI reads it natively from workspace
- No external dependency to maintain
- Fits the "everything-as-code" philosophy

**Cons:**
- No UI for non-technical stakeholders to browse/edit tickets
- No workflow automation (status transitions, notifications)
- No concurrent multi-user editing
- Manual ticket creation (YAML syntax required)
- No board/Kanban view

### 11.2 Decision Framework

| If... | Then... |
|-------|---------|
| Only architects use the system | YAML-only is sufficient |
| Stakeholders need a UI to browse and create tickets | Deploy Vikunja |
| The POC needs to demonstrate "real tooling" to leadership | Deploy Vikunja |
| Cost must stay at $0/month | YAML-only |
| AI integration is the primary concern | YAML-only (simplest path to AI awareness) |
| The team is larger than 3 people | Deploy Vikunja |

### 11.3 Recommended Path

**Start with YAML-only (Phase 1).** Get the ticket structure, capability tagging, and portal integration working. This validates the information architecture. Then deploy Vikunja (Phase 2) when a UI is needed for broader team adoption. The migration is seamless because `tickets.yaml` is the shared data model — Vikunja just becomes the UI that writes to it via `sync-tickets.py`.

---

## 12. Implementation Checklist

### Phase 1: YAML-First Ticketing (Recommended Starting Point)

- [ ] Create `architecture/metadata/tickets.yaml` — Migrate 7 tickets from mock JSON, add capability mappings and use cases
- [ ] Create `architecture/metadata/capabilities.yaml` — Formalize 34 L2 capabilities from CAPABILITY-MAP-ANALYSIS.md
- [ ] Write `scripts/ticket-client.py` — YAML-reading CLI with capability/service filtering
- [ ] Write `portal/scripts/generate-ticket-pages.py` — Index page + per-ticket pages
- [ ] Add ticket cross-references to capability page generator
- [ ] Add ticket cross-references to microservice page generator
- [ ] Update `portal/mkdocs.yml` nav with User Stories section
- [ ] Update `.github/copilot-instructions.md` with ticket commands, capability rollup checklist, and branching requirements
- [ ] Document branch naming convention (`solution/NTK-XXXXX-slug`) and solution branch workflow
- [ ] Publish to portal and validate all cross-links

### Phase 2: Vikunja Deployment

- [ ] Create `infra/modules/vikunja.bicep` and `infra/modules/container-apps-env.bicep`
- [ ] Add Vikunja parameters to `infra/parameters/prod.bicepparam`
- [ ] Wire modules into `infra/main.bicep`
- [ ] Deploy Vikunja to Azure Container Apps
- [ ] Create NovaTrek project and seed capability labels
- [ ] Import tickets from `tickets.yaml` via Vikunja API
- [ ] Write `portal/scripts/sync-tickets.py` for bidirectional sync
- [ ] Configure webhooks for automated sync on ticket changes
- [ ] Add Vikunja link to portal navigation

### Phase 3: Advanced Integration

- [ ] Build MCP server for real-time AI access to Vikunja
- [ ] Implement conflict detection (multiple tickets modifying same capability)
- [ ] Add capability health dashboard (churn analysis, staleness detection)
- [ ] Implement capability impact scoring (weighted by ticket priority and breadth)
- [ ] Add use case catalog generator (cross-ticket use case aggregation)
- [ ] Automate ticket-to-branch status synchronization (PR open → In Review, PR merge → Done) via Git webhooks to Vikunja API

---

## 13. Alternative Ticketing Solutions Not Recommended

For completeness, these were evaluated and rejected:

| Tool | Reason for Rejection |
|------|---------------------|
| **Redmine** | Ruby-based, heavy setup, dated UI, complex Docker deployment |
| **MantisBT** | PHP-based, limited API, legacy architecture |
| **Trac** | Python-based but effectively unmaintained since 2020 |
| **Kanboard** | PHP, minimal API, no custom fields |
| **GitLab Issues** | Requires full GitLab deployment ($500+/month on Azure for EE, CE is lighter but still heavy) |
| **GitHub Issues** | SaaS-only — violates self-hosted requirement for data isolation |
| **YouTrack** | Free for 10 users but proprietary — violates open-source requirement |
| **Linear** | SaaS-only, proprietary |

---

## 14. Summary

| Decision | Recommendation |
|----------|---------------|
| Ticketing tool | **Vikunja** — lightweight Go binary, SQLite, clean REST API, AGPL-3.0 |
| Starting approach | **YAML-first** — `tickets.yaml` as source of truth, deploy Vikunja when UI needed |
| Azure hosting | **Container Apps** (consumption plan) — $0-5/month, scale to zero |
| AI access model | **File-based** (tickets.yaml in workspace) + **CLI script** (ticket-client.py) |
| Ticket format | **Structured user stories** with use cases, capability mapping, service impact |
| Capability rollup | **Labels** in Vikunja + **capability mapping section** in every ticket |
| Portal integration | **Sync-and-generate** — Vikunja API syncs to YAML, generator builds MkDocs pages |
| Infrastructure as code | **Bicep module** for Vikunja Container App, wired into existing `main.bicep` |
