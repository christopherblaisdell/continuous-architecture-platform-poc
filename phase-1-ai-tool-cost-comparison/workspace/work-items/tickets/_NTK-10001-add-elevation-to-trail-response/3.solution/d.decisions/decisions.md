# NTK-10001 - Decisions

## D1 - Use Nullable Fields for Elevation Data

### Context

When adding `elevation_gain_meters` and `elevation_loss_meters` to the trail response, we need to decide whether these fields should be required (always present with a value) or nullable (may be null for trails where elevation data has not been recorded).

Some trails in the database may not have elevation data populated, particularly older trail records or trails currently under survey. Making the fields required would mean either backfilling missing data before deployment or returning a default value (e.g., 0) which could be misleading.

### Decision

The new fields will be **nullable**. They will return `null` when elevation data is not available for a given trail, rather than a default numeric value.

### Consequences

**Positive:**
- No data backfill required before deployment
- Consumers can distinguish between "no data available" (null) and "flat trail" (0)
- Allows incremental data population without blocking the feature release

**Negative:**
- Consumers must handle null values when rendering elevation data
- API documentation must clearly state the fields are optional
