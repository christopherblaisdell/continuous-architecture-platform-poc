---
tags:
  - standards
  - openapi
  - api-contracts
---

<div class="hero" markdown>

# OpenAPI Contracts

<p class="subtitle">Why we define every service API as a YAML specification — and how it powers the entire architecture platform</p>

</div>

## What Are the OpenAPI Specs?

The `architecture/specs/` directory contains an **OpenAPI 3.0 YAML file for every NovaTrek microservice** (22 services). Each file is a machine-readable contract that defines:

- **Endpoints** — every REST route, HTTP method, and operation ID
- **Request/response schemas** — exact field names, data types, nullable annotations, and enumerations
- **Security requirements** — authentication schemes (e.g., `BearerAuth`)
- **Server URLs** — base paths for each deployment environment
- **Contact metadata** — owning team and email for each service

Example (from `svc-analytics.yaml`):

```yaml
openapi: 3.0.3
info:
  title: NovaTrek Analytics Service
  version: 1.3.0
  contact:
    name: NovaTrek Data & Insights Team
paths:
  /analytics/bookings:
    get:
      operationId: getBookingAnalytics
      summary: Get booking analytics for a period
      parameters:
        - $ref: '#/components/parameters/Period'
      responses:
        '200':
          description: Booking analytics data
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BookingAnalytics'
```

---

## Why YAML?

**YAML is the standard format for OpenAPI specifications** because it offers the best balance of human readability and machine parseability for API contracts.

### Readability

YAML uses significant whitespace instead of braces and brackets, making deeply nested API schemas easy to scan. Engineers can read and review a YAML spec in a pull request without tooling — compare:

```yaml
# YAML — readable at a glance
BookingAnalytics:
  type: object
  properties:
    total_bookings:
      type: integer
      description: Total number of bookings in the period
    revenue:
      type: number
      format: double
      nullable: true
```

```json
{
  "BookingAnalytics": {
    "type": "object",
    "properties": {
      "total_bookings": {
        "type": "integer",
        "description": "Total number of bookings in the period"
      },
      "revenue": {
        "type": "number",
        "format": "double",
        "nullable": true
      }
    }
  }
}
```

Both are valid OpenAPI — but the YAML version is roughly 40% fewer characters and far easier to diff in a code review.

### References and reuse

YAML supports `$ref` pointers that let specs reference shared components without duplication. A parameter definition or schema defined once under `components/` can be referenced across every endpoint:

```yaml
parameters:
  - $ref: '#/components/parameters/Period'
  - $ref: '#/components/parameters/StartDate'
```

### Tooling ecosystem

OpenAPI YAML files are consumed by a wide ecosystem of tools that would require manual effort to replicate:

| Tool / Consumer | What It Does |
|----------------|--------------|
| **Swagger UI** | Interactive API documentation with "Try it out" capability |
| **Code generators** | Client SDKs and server stubs in any language (OpenAPI Generator) |
| **PlantUML diagram generator** | Sequence diagrams for every endpoint auto-rendered as SVGs |
| **Linters** (Spectral, Redocly) | Enforce naming conventions and schema completeness rules |
| **Contract testing** | Validate that running services match their published spec |
| **CALM topology generator** | Produces architecture-as-code topology from service contracts |

---

## Why Not Just Write Documentation?

Traditional API documentation is **prose maintained by hand** — it drifts from reality the moment a developer changes an endpoint without updating the docs. OpenAPI specs solve this by being:

| Property | Prose Documentation | OpenAPI Spec |
|----------|-------------------|--------------|
| **Machine-readable** | No | Yes — tools can parse, validate, generate from it |
| **Single source of truth** | Tends to duplicate | One file per service, everything derived from it |
| **Diffable in PRs** | Ambiguous changes | Structured changes reviewable field-by-field |
| **Generates UI automatically** | Manual upkeep | Swagger UI renders from the spec directly |
| **Validates at CI time** | Cannot | Linters catch breaking changes before merge |
| **Enforces contracts** | Honor system | Contract tests verify runtime matches spec |

The key insight: **the spec IS the documentation**. When a service changes, the spec is updated in the same pull request, and every downstream artifact (Swagger UI pages, sequence diagrams, microservice deep-dive pages, CALM topology) regenerates automatically.

---

## How NovaTrek Uses These Specs

### Architecture portal generation

The `generate-microservice-pages.py` script reads all 22 specs and produces:

1. **Microservice deep-dive pages** — one page per service with endpoint tables, schema details, and cross-service integration maps
2. **PlantUML sequence diagrams** — one diagram per endpoint (139 total), rendered as clickable SVGs with deep links to related services
3. **Swagger UI pages** — interactive API explorers served from `portal/docs/services/api/`

### Solution design workflow

When architects design solutions for tickets, they propose changes **to the OpenAPI spec**, not to prose documentation. This means:

- Reviewers see the exact fields being added, modified, or removed
- Impact is traceable — every spec change maps to a ticket and a solution design
- Backward compatibility is assessed structurally (new required fields break consumers)

### Cross-service integration

The specs define explicit contracts between services. When `svc-check-in` calls `svc-guest-profiles`, both sides reference the same schema definitions. This prevents:

- **Schema drift** — consumer and producer disagreeing on field types
- **Shadow records** — services inventing their own data models for data they do not own
- **Undocumented dependencies** — every integration point is visible in the spec

---

## NovaTrek OpenAPI Conventions

| Convention | Rule |
|-----------|------|
| **File naming** | `svc-{service-name}.yaml` — matches the service identifier exactly |
| **Version format** | Semantic versioning in `info.version` (e.g., `1.3.0`) |
| **Nullable fields** | Explicitly annotated with `nullable: true` — see ADR-003 (Nullable Elevation Fields) |
| **Operation IDs** | camelCase, unique across all specs (e.g., `getBookingAnalytics`) |
| **Tags** | Group endpoints by domain concern within the service |
| **Contact** | Every spec includes `info.contact` with owning team name and email |
| **$ref usage** | Shared schemas and parameters defined under `components/` and referenced throughout |

---

## Current Service Specs

All 22 service specifications live in `architecture/specs/`:

| Domain | Services |
|--------|----------|
| **Operations** | svc-check-in, svc-scheduling-orchestrator |
| **Guest Identity** | svc-guest-profiles |
| **Booking** | svc-reservations |
| **Product Catalog** | svc-trip-catalog, svc-trail-management |
| **Safety** | svc-safety-compliance, svc-emergency-response |
| **Logistics** | svc-transport-logistics, svc-gear-inventory |
| **Guide Management** | svc-guide-management |
| **External** | svc-partner-integrations |
| **Analytics** | svc-analytics |
| **Support** | svc-notifications, svc-payments, svc-loyalty-rewards, svc-media-gallery, svc-weather, svc-location-services, svc-inventory-procurement, svc-reviews, svc-wildlife-tracking |

Browse the interactive API documentation in the [Service Catalog](../../services/index.md), or explore the generated deep-dive pages under [Microservices](../../microservices/index.md).

---

!!! tip "Quick Reference"

    **Viewing a spec**: Open any file in `architecture/specs/` — it is both human-readable documentation and a machine-parseable contract.

    **Proposing a change**: Modify the YAML spec in a PR branch, run `python3 portal/scripts/generate-microservice-pages.py` to regenerate portal pages, then submit for review.

    **Understanding an endpoint**: Visit the [Service Catalog](../../services/index.md) for interactive Swagger UI, or the [Microservices](../../microservices/index.md) section for sequence diagrams and integration maps.
