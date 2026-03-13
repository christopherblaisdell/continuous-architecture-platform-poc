---
tags:
  - handbook
  - workflow
  - tickets
---

<!-- PUBLISH -->

<div class="hero" markdown>

# Working a Ticket

<p class="subtitle">How to triage, investigate, and respond to architecture tickets on the NovaTrek platform</p>

</div>

This guide covers the full lifecycle of an architecture ticket — from the moment it arrives to the moment a solution design is ready for review (or the ticket is resolved without one).

---

## Overview

Not every ticket requires a full solution design. The first job of a solution architect is **triage**: reading the ticket carefully and deciding what level of architectural response is warranted.

```
Ticket arrives
     │
     ▼
  Triage
  ├── No architecture work needed → comment and close/reassign
  ├── Minor investigation only → run tools, document findings, no solution design
  └── Solution required → create solution design (see Solution Design guide)
```

---

## Step 1 — Read the Ticket

Open the ticket using the JIRA mock client (in the Phase 1 workspace) or the ticket client (in the architecture workspace).

=== "Architecture workspace (ticket-client)"

    ```bash
    # Run from architecture/ or root
    python3 architecture/scripts/ticket-client.py --ticket NTK-10005
    ```

=== "Phase 1 workspace (mock-jira-client)"

    ```bash
    # Run from the Phase 1 workspace directory
    python3 scripts/mock-jira-client.py --ticket NTK-10005
    ```

Read the full ticket body including all comments. Pay attention to:

- **Reported symptoms** — what is broken or missing from the user's perspective
- **Affected services** — which services are mentioned
- **Business context** — what capability is at stake
- **Priority and urgency** — how quickly a response is needed

---

## Step 2 — List All Open Tickets

Before diving into a single ticket, check what else is open. New tickets may be related to existing ones.

=== "Architecture workspace"

    ```bash
    python3 architecture/scripts/ticket-client.py --list --status "New"
    python3 architecture/scripts/ticket-client.py --list --status "In Progress"
    ```

=== "Phase 1 workspace"

    ```bash
    python3 scripts/mock-jira-client.py --list --status "New"
    ```

---

## Step 3 — Determine Architectural Relevance

Ask these questions to assess relevance:

| Question | If yes, then... |
|---|---|
| Does it change a public API contract? | Architecture work needed — [update OpenAPI spec](api-contracts.md) |
| Does it change a database schema or add an index? | Architecture work needed — [database changes](database-changes.md) |
| Does it require a new service? | Architecture work needed — [adding a service](adding-a-service.md) |
| Does it add or change a domain event? | Architecture work needed — [events](events.md) |
| Does it change a UI flow or screen? | Consider a [wireframe](wireframes.md) |
| Does it cross service domain boundaries? | An ADR is likely needed |
| Does it introduce a new integration pattern? | An ADR is likely needed |
| Is it purely a bug fix within a single service? | May not require architecture work |
| Is it a configuration or ops change only? | May not require architecture work |

---

## Step 4 — Run Investigations

For tickets that show symptoms (errors, performance degradation, incorrect behavior), investigate before proposing solutions.

### Run production logs first

Always run Elastic before GitLab. Logs establish the symptom timeline before you look at code.

=== "Architecture workspace"

    The architecture workspace does not have an Elastic mock. Review any attached log snippets in the ticket, then check the relevant OpenAPI spec and source code.

=== "Phase 1 workspace"

    ```bash
    # Search logs for a specific service
    python3 scripts/mock-elastic-searcher.py --service svc-scheduling-orchestrator --level ERROR

    # Search logs for a keyword
    python3 scripts/mock-elastic-searcher.py --query "timeout"

    # Search logs across all services for a specific error pattern
    python3 scripts/mock-elastic-searcher.py --query "NullPointerException"
    ```

### Check recent MRs

After reviewing logs, check for recent merge requests that may be related to the symptoms.

=== "Phase 1 workspace"

    ```bash
    # List MRs for a service
    python3 scripts/mock-gitlab-client.py --project svc-scheduling-orchestrator --mrs

    # Read a specific MR with diff
    python3 scripts/mock-gitlab-client.py --mr 5001
    ```

### Review the OpenAPI spec

Cross-reference observed behavior with the published API contract.

```bash
# OpenAPI specs live in architecture/specs/
cat architecture/specs/svc-scheduling-orchestrator.yaml
```

### Review source code

Source code lives in `source-code/` (Phase 1 workspace) or `services/` (production services).

When reading source code:

1. Read the **full file** before drawing conclusions
2. Trace the request lifecycle: controller → service → repository
3. Look for [common anti-patterns](../index.md#platform-principles) — entity replacement, missing concurrency control, hardcoded classification, shadow guest records

---

## Step 5 — Discover Prior Art

Before starting any design work, check whether previous solutions have already addressed the same capabilities.

```bash
# Find tickets that touched a specific capability
python3 architecture/scripts/ticket-client.py --list --capability CAP-2.1

# Find tickets affecting a specific service
python3 architecture/scripts/ticket-client.py --list --service svc-check-in
```

Then read the capability changelog to understand what L3 capabilities already exist:

```bash
cat architecture/metadata/capability-changelog.yaml
```

And browse existing solution folders:

```
architecture/solutions/
  _NTK-10001-add-elevation-to-trail-response/
  _NTK-10002-adventure-category-classification/
  _NTK-10003-unregistered-guest-self-checkin/
  ...
```

Read the master document (e.g., `NTK-10003-solution-design.md`) and the capabilities summary (`3.solution/c.capabilities/capabilities.md`) for related work.

Document any prior art you find in the **Prior Art** section of your solution design's master document.

---

## Step 6 — Decide on Response Type

Based on your investigation, choose the appropriate response:

=== "No architecture work needed"

    - Comment on the ticket explaining why no architecture change is required
    - Route to the appropriate engineering team if it is a bug fix or configuration change
    - Close or reassign the ticket

=== "Investigation findings only"

    - Document your findings in a brief investigation note (can be a comment or a minimal `2.analysis/` document)
    - If the findings reveal a previously unknown risk, create a risk note in the relevant solution's `3.solution/r.risks/` directory
    - No solution design folder needed

=== "Full solution design required"

    - Follow the [Solution Design](solution-design.md) guide to create a complete solution design
    - Branch, folder structure, master document, capability changelog entry, portal generation, and PR

---

## Step 7 — Scope Check

Before writing anything, verify scope:

- **Architect scope**: assess, design, document. Not: debug code, write implementation, configure infrastructure.
- **Cross-domain changes**: any change touching multiple bounded contexts needs an ADR.
- **Safety-critical paths**: any change that could affect the adventure classification system (ADR-005) requires explicit safety review.

---

## Reference — Ticket Statuses

| Status | Meaning |
|---|---|
| `New` | Arrived, not yet triaged |
| `In Triage` | Being assessed by architecture |
| `In Progress` | Solution design under development |
| `In Review` | Solution design submitted as PR, awaiting review |
| `Approved` | Solution design accepted |
| `Implemented` | Development complete |
| `Closed` | No architecture action needed |

---

!!! tip "Related guides"
    - [Solution Design](solution-design.md) — full workflow for creating a solution design
    - [Metadata Registry](../standards/metadata-registry/index.md) — how tickets are registered in `tickets.yaml`
