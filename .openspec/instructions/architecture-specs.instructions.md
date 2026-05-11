## OpenAPI Specification Design Rules

When creating or modifying OpenAPI specs in this directory, follow these REST API design patterns:

### Resource Naming

- Resources are nouns, plural, lowercase, kebab-case: `/reservations`, `/check-ins`, `/guest-profiles`
- Sub-resources for relationships: `/guests/{guest_id}/reservations`
- Actions that do not map to CRUD use verbs sparingly: `/check-ins/{id}/complete`
- Query parameters for filtering: `?status=active&adventure_type=kayaking`

### HTTP Methods and Status Codes

| Method | Use For | Success Code |
|--------|---------|-------------|
| GET | Retrieve resources | 200 OK |
| POST | Create resources, trigger actions | 201 Created (include Location header) |
| PUT | Full replacement (avoid — prefer PATCH per ADR-010) | 200 OK |
| PATCH | Partial update | 200 OK |
| DELETE | Remove a resource | 204 No Content |

Error codes: 400 (validation), 401 (unauthenticated), 403 (unauthorized), 404 (not found), 409 (conflict/optimistic lock per ADR-011), 422 (unprocessable), 429 (rate limited), 500 (server error)

### Schema Completeness Checklist

For every schema in a spec, verify:
- [ ] All fields have `type` specified
- [ ] All fields have `description` with business meaning, not just the field name restated
- [ ] Nullable fields have `nullable: true` with documented null semantics (what does null mean?)
- [ ] Enum fields use validated domain values from `config/adventure-classification.yaml` or service-specific constants
- [ ] Required vs optional fields are correctly annotated
- [ ] Date fields use ISO 8601 format (`date-time` or `date`)
- [ ] ID fields specify format (e.g., `format: uuid`)

### Backward Compatibility

When modifying an existing spec:
- Adding a new **optional** field: safe
- Adding a new **required** field: BREAKING — existing consumers will fail
- Removing a field: BREAKING — deprecate first, remove in next major version
- Changing a field type: BREAKING
- Adding a new enum value: safe for servers, potentially breaking for clients with strict validation
- Removing an enum value: BREAKING

### Pagination

List endpoints returning collections MUST support pagination:
```yaml
parameters:
  - name: page
    in: query
    schema: { type: integer, default: 1, minimum: 1 }
  - name: page_size
    in: query
    schema: { type: integer, default: 20, minimum: 1, maximum: 100 }
```

### NovaTrek-Specific Patterns

- Optimistic locking: include `_rev` or `version` field in mutable entities (ADR-011)
- PATCH semantics: prefer partial updates over full replacement (ADR-010)
- Cross-service references: use the target service's published ID format, never internal database IDs
- Service version: `info.version` should reflect the service's last documented change
