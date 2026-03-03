# ADR-003: Use Nullable Fields for Elevation Data

## Status

Accepted

## Date

2026-02-15

## Context and Problem Statement

When adding `elevation_gain_meters` and `elevation_loss_meters` to the trail response in svc-trail-management, we need to decide whether these fields should be required (always present with a value) or nullable (may be null for trails where elevation data has not been recorded).

Some trails in the database may not have elevation data populated, particularly older trail records or trails currently under survey. Making the fields required would mean either backfilling missing data before deployment or returning a default value (e.g., 0) which could be misleading.

## Decision Drivers

- Avoid blocking feature deployment on a data backfill exercise
- API consumers must distinguish between "no data available" and "flat trail with zero elevation change"
- Incremental data population should be supported without schema changes
- Backward compatibility with existing API consumers

## Considered Options

1. **Nullable fields** — Return `null` when elevation data is not available
2. **Required fields with default** — Return `0` for unknown elevation data
3. **Required fields with backfill** — Populate all records before deployment

## Decision Outcome

**Chosen Option**: "Nullable fields", because it avoids a data backfill dependency, allows consumers to distinguish between "no data" and "flat trail", and supports incremental data population.

### Confirmation

- OpenAPI spec updated with `nullable: true` on both fields
- Unit tests verify null handling in serialization and deserialization
- API documentation clearly states the fields are optional

## Consequences

### Positive

- No data backfill required before deployment
- Consumers can distinguish between "no data available" (`null`) and "flat trail" (`0`)
- Allows incremental data population without blocking the feature release

### Negative

- Consumers must handle null values when rendering elevation data
- API documentation must clearly state the fields are optional

## More Information

- Origin: [NTK-10001 Solution Design](../phase-1-ai-tool-cost-comparison/workspace/work-items/tickets/_NTK-10001-add-elevation-to-trail-response/NTK-10001-solution-design.md)
- Service: [svc-trail-management](../services/svc-trail-management.md)
