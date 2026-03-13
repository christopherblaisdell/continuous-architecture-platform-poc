---
tags:
  - handbook
  - openapi
  - api-contracts
---

<!-- PUBLISH -->

<div class="hero" markdown>

# API Contract Changes

<p class="subtitle">How to add endpoints, modify schemas, and manage backward compatibility in OpenAPI specs</p>

</div>

All NovaTrek API contracts are defined as OpenAPI 3.0.3 YAML files in `architecture/specs/`. These files are the **single source of truth** for every service's public interface. When the architect changes a spec and pushes to `main`, CI regenerates the Swagger UI pages and all sequence diagrams automatically.

---

## Overview

```
Architect edits architecture/specs/svc-xxx.yaml
     │
     ▼
CI runs generate-swagger-pages.py     → portal/docs/services/api/svc-xxx.html (Swagger UI)
CI runs generate-microservice-pages.py → portal/docs/microservices/svc-xxx.md  (service page)
                                         portal/docs/microservices/puml/*.puml   (sequence diagrams)
                                         portal/docs/microservices/svg/*.svg    (rendered diagrams)
```

---

## File Locations

| What | Where |
|---|---|
| OpenAPI specs (source of truth) | `architecture/specs/svc-{service-name}.yaml` |
| Swagger UI output (generated) | `portal/docs/services/api/svc-{service-name}.html` |
| Sequence diagram PUML (generated) | `portal/docs/microservices/puml/` |
| Sequence diagram SVG (generated) | `portal/docs/microservices/svg/` |

---

## Common Tasks

### Adding a New Endpoint

1. Open the spec file for the service: `architecture/specs/svc-{name}.yaml`
2. Add the path under `paths:` following the existing pattern:

```yaml
paths:
  /check-ins/{check_in_id}/wristband:
    put:
      operationId: assignWristband
      summary: Assign an RFID wristband to a check-in record
      description: |
        Associates an RFID wristband with an existing check-in record.
        The wristband must be unassigned. Returns 409 if already in use.
      tags: [Check-Ins]
      parameters:
        - name: check_in_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/WristbandAssignment'
      responses:
        '200':
          description: Wristband assigned
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CheckIn'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'
        '409':
          description: Wristband already assigned to another check-in
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
      security:
        - BearerAuth: []
```

Required fields for every operation:
- `operationId` — unique camelCase identifier across the entire spec
- `summary` — short one-line description
- `description` — full behavior description including edge cases
- `tags` — groups endpoints in Swagger UI; use the same tag as sibling endpoints
- `responses` — at minimum: success response, `400`, `401`, `404` (if applicable), `409` (if applicable)
- `security` — always include `BearerAuth: []`

### Adding a New Schema

Add schemas under `components/schemas:`:

```yaml
components:
  schemas:
    WristbandAssignment:
      type: object
      required:
        - wristband_id
      properties:
        wristband_id:
          type: string
          description: RFID wristband identifier (hex or UUID format)
          example: "A3F2-9C11"
```

Schema conventions:
- All properties have a `description`
- All properties have an `example` where possible
- Use `$ref` to reference shared schemas rather than inlining
- Mark nullable fields with `nullable: true` and document what null means
- Use `format: uuid` for UUID fields, `format: date-time` for timestamps

### Adding a Field to an Existing Schema

To add an optional field to an existing response schema:

```yaml
CheckIn:
  type: object
  properties:
    check_in_id:
      type: string
      format: uuid
    # ... existing fields ...
    wristband_id:          # ← new optional field
      type: string
      nullable: true
      description: |
        RFID wristband identifier assigned during check-in.
        Null if no wristband has been assigned yet.
      example: "A3F2-9C11"
```

Adding an optional field to a response is backward compatible. Consumers that do not expect the field will ignore it.

### Making a Field Required

!!! warning "Breaking change"
    Adding a new **required** field to a **request body schema** is a breaking change — existing consumers sending the old request format will receive `400` errors. Always provide a default value or a versioned migration path. See [Versioning Considerations](#versioning-considerations).

### Removing a Field

!!! warning "Breaking change"
    Removing a field from any published schema is a breaking change. Follow the deprecation process: mark the field as `deprecated: true` for one release cycle before removing it.

```yaml
properties:
  legacy_code:
    type: string
    deprecated: true
    description: |
      DEPRECATED — use confirmation_code instead.
      Will be removed in API version 2.0.
```

### Modifying an Existing Endpoint

Changing an existing endpoint's behavior without changing its signature (path, method, schema) is a non-breaking change. Document the behavior change in the `description` field.

Changing a path, removing a parameter, or changing a response schema is a breaking change — see [Versioning Considerations](#versioning-considerations).

---

## Versioning Considerations

NovaTrek uses **URI versioning** for breaking changes: `/v1/check-ins`, `/v2/check-ins`.

When a breaking change is unavoidable:

1. Add the new version path under `paths:` in the spec with a new `operationId`
2. Keep the old version path with a `deprecated: true` flag on the operation
3. Update `info.version` in the spec
4. Document the migration path in an impact assessment

```yaml
info:
  version: 2.0.0

paths:
  /v1/check-ins:
    post:
      deprecated: true
      summary: "[DEPRECATED] Initiate check-in (use /v2/check-ins)"
  /v2/check-ins:
    post:
      summary: Initiate check-in for a participant
```

---

## Registering Cross-Service Calls

If your new endpoint will be called by another service, register the integration in `architecture/metadata/cross-service-calls.yaml`:

```yaml
svc-check-in:
  calls:
    - target: svc-reservations
      method: GET
      path: /reservations/{reservation_id}
      purpose: Validate reservation before check-in
    - target: svc-guest-profiles      # ← new cross-service call
      method: GET
      path: /guests/{guest_id}
      purpose: Retrieve guest profile for wristband assignment
```

This ensures the sequence diagrams on the service page accurately reflect the integration topology.

---

## Updating the Service Version

After any spec change, bump `info.version` in the spec file to reflect the change:

```yaml
info:
  title: NovaTrek Check-In Service
  version: 1.2.0    # was 1.1.0
```

Use semantic versioning:
- **Patch** (1.0.x) — documentation changes, description improvements, no behavior change
- **Minor** (1.x.0) — new optional fields, new endpoints, backward compatible changes
- **Major** (x.0.0) — breaking changes, removed fields, changed required fields

---

## Running the Generators

After editing the spec, regenerate locally to verify:

```bash
# Full regeneration (recommended)
bash portal/scripts/generate-all.sh

# Swagger UI pages only (faster)
python3 portal/scripts/generate-swagger-pages.py

# Microservice pages + sequence diagrams (needed if endpoint structure changed)
python3 portal/scripts/generate-microservice-pages.py
```

Review the generated Swagger UI page to confirm the changes render correctly:

```
portal/docs/services/api/svc-{name}.html
```

---

## Spec Checklist

Before committing an OpenAPI spec change:

- [ ] `operationId` is unique within the spec
- [ ] All new parameters have `description` and `example`
- [ ] All new schemas have `description` on every property
- [ ] Nullable fields are marked `nullable: true` with documented null semantics
- [ ] New required request fields have a migration path documented
- [ ] Removed fields are marked `deprecated` first
- [ ] `info.version` bumped appropriately
- [ ] `cross-service-calls.yaml` updated for new integrations
- [ ] Generators run without errors

---

!!! tip "Related guides"
    - [Solution Design](solution-design.md) — when API changes are part of a full solution design
    - [Adding a Service](adding-a-service.md) — when you are creating a new spec from scratch
    - [Publishing](publishing.md) — how CI deploys spec changes to the portal
    - [Service Catalog](../services/index.md) — portal view of all published specs
