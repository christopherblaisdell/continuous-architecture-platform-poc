# NTK-10002: Architecture Decisions

---

## ADR-NTK10002-001: Configuration-Driven Classification over Database-Driven

### Status

Accepted

### Date

2024-08-14

### Context and Problem Statement

The adventure category classification system requires a mapping from 25 adventure categories to 3 check-in UI patterns. This mapping must be maintainable by the team, performant at runtime (no per-request latency penalty), and auditable over time. How should the category-to-pattern mapping be stored and maintained?

### Decision Drivers

- Change frequency is low (less than once per sprint)
- Mapping changes must be auditable and reviewable
- Runtime lookup must add near-zero latency to the check-in request
- Implementation scope should be minimized
- Operations team needs visibility into current mapping

### Considered Options

1. **Database-driven** -- Store mapping in a database table with an admin UI
2. **Configuration-driven** -- Define mapping in YAML via Spring Cloud Config
3. **Code-driven** -- Hardcode the mapping in the Java source code

### Decision Outcome

**Chosen Option**: "Configuration-driven", because it provides version-controlled, reviewable mapping changes with sub-millisecond runtime performance and minimal implementation scope.

#### Confirmation

- Classification config file exists in Spring Cloud Config repository
- `ClassificationService` loads config at startup and refreshes on TTL expiry
- `/actuator/refresh` endpoint triggers immediate reload

### Consequences

#### Positive

- YAML config is version-controlled in Git, providing full audit trail and PR-based review
- No new database table, schema migration, or admin UI required
- In-memory `ConcurrentHashMap` provides sub-millisecond lookup performance
- Spring `@Cacheable` with configurable TTL (default 5 min) handles refresh transparently

#### Negative

- Configuration changes require a commit, push, and service refresh -- not self-service
- Operations staff must request changes through the development team
- If change frequency increases beyond once per sprint, this approach should be revisited

#### Neutral

- Requires Spring Cloud Config infrastructure (already in place)

### Pros and Cons of the Options

#### Database-driven

- **Good**, because operations can modify mappings through an admin UI without developer involvement
- **Good**, because changes are immediate (no cache TTL)
- **Neutral**, because requires database connection for every lookup (mitigated by application-level caching)
- **Bad**, because introduces new database table, migration, and admin UI development effort
- **Bad**, because changes bypass code review -- no audit trail in Git

#### Configuration-driven

- **Good**, because changes are version-controlled and require PR review
- **Good**, because no additional infrastructure required
- **Good**, because sub-millisecond in-memory lookup with automatic refresh
- **Neutral**, because requires Spring Cloud Config refresh for changes to take effect
- **Bad**, because not self-service for operations staff

#### Code-driven

- **Good**, because simplest implementation -- just a Java Map constant
- **Bad**, because mapping changes require a code deployment
- **Bad**, because mixes configuration data with application logic

### More Information

- Solution Design Section 7: Architecture Decision
- Comment thread: Comments 6-7 in ticket NTK-10002

---

## ADR-NTK10002-002: Pattern 3 as Default Fallback for Unknown Categories

### Status

Accepted

### Date

2024-08-19

### Context and Problem Statement

Edge cases exist where the `adventure_category` field may be null, empty, or contain a value not recognized by the classification table. This could occur with legacy reservations predating the feature, or when a new category is added to `svc-trip-catalog` before the classification config is updated. What should the system do when it encounters an unknown or missing category?

### Decision Drivers

- Guest safety is the highest priority
- Operational staff prefer to over-service rather than under-service
- Unknown categories are expected to occur occasionally during the transition period
- The fallback must be deterministic and predictable

### Considered Options

1. **Default to Pattern 3 (Full Service)** -- safety-first, provide all check-in steps
2. **Default to Pattern 1 (Basic)** -- minimal friction, assume low-complexity
3. **Return an error** -- reject the check-in and require manual classification

### Decision Outcome

**Chosen Option**: "Default to Pattern 3 (Full Service)", because guest safety takes precedence over convenience, and over-servicing creates only minor inconvenience while under-servicing could create safety risks.

#### Confirmation

- Unit tests verify fallback to Pattern 3 for null, empty, and unrecognized category values
- `checkin.classification.fallback.count` metric is tracked and alerted on

### Consequences

#### Positive

- No guest will miss critical safety steps due to a classification gap
- Operational alignment: confirmed with operations team as the preferred approach
- Deterministic behavior: logs and monitoring clearly show when fallback is triggered

#### Negative

- Guests with unmapped low-complexity categories experience an unnecessarily long check-in flow
- May cause minor guest frustration if fallback occurs frequently

#### Neutral

- Monitoring via `checkin.classification.fallback.count` metric identifies categories needing mapping

### Pros and Cons of the Options

#### Default to Pattern 3 (Full Service)

- **Good**, because no guest misses safety-critical steps
- **Good**, because aligned with operational safety-first principles
- **Neutral**, because adds a few minutes to check-in for misclassified guests
- **Bad**, because may cause minor frustration for simple-activity guests

#### Default to Pattern 1 (Basic)

- **Good**, because minimal friction for guests -- fastest possible check-in
- **Bad**, because could skip gear verification, safety briefing, or medical clearance for high-risk activities
- **Bad**, because creates safety liability if a guest on a complex activity bypasses safety steps

#### Return an error

- **Good**, because forces correct classification before check-in proceeds
- **Bad**, because blocks the guest from checking in -- creates a hard failure at the kiosk
- **Bad**, because requires staff intervention for every unmapped category

### More Information

- Ticket comment thread: Comments 11-13 in NTK-10002
- Product owner confirmation: Morgan Chen, 2024-08-19

---

## ADR-NTK10002-003: Additive API Contract Changes for Classification Response

### Status

Accepted

### Date

2026-03-03

### Context and Problem Statement

The check-in API must convey the determined classification pattern to the calling client (kiosk, mobile app) so the client can render the correct UI flow. How should the classification result be communicated in the API response, and how should the svc-trip-catalog schema be extended to carry the adventure category?

### Decision Drivers

- Backward compatibility with existing API consumers
- Client applications need to know which UI flow to render
- The adventure category must originate from svc-trip-catalog and flow through svc-reservations
- Existing consumers of svc-trip-catalog Trip responses must not break

### Considered Options

1. **Additive fields on existing schemas** -- Add `determined_pattern` and `pattern_name` to the CheckIn response; add `adventure_category` to the Trip schema
2. **New dedicated endpoint** -- Create a separate `GET /check-ins/{id}/classification` endpoint
3. **Header-based response** -- Return classification data in custom HTTP response headers

### Decision Outcome

**Chosen Option**: "Additive fields on existing schemas", because it minimizes API surface area growth, maintains backward compatibility through optional fields, and aligns with the tolerant reader pattern already used across NovaTrek services.

#### Confirmation

- `POST /check-ins` response includes `determined_pattern` (integer) and `pattern_name` (string)
- svc-trip-catalog `Trip` schema includes `adventure_category` (nullable string enum)
- Both additions are optional/nullable fields that do not break existing consumers

### Consequences

#### Positive

- No new endpoints required -- existing API surface remains stable
- Backward compatible -- consumers ignoring the new fields continue to work
- Classification result is co-located with the check-in data, avoiding extra lookups
- adventure_category on Trip schema enables future features beyond check-in classification

#### Negative

- CheckIn response grows slightly larger (two additional fields)
- Consumers must be updated to read the new fields if they want classification-aware behavior

#### Neutral

- Swagger specification updates required for both svc-check-in and svc-trip-catalog

### Pros and Cons of the Options

#### Additive fields on existing schemas

- **Good**, because minimal API changes and backward compatible
- **Good**, because follows existing tolerant reader pattern
- **Good**, because classification data is immediately available in the check-in response
- **Neutral**, because requires Swagger spec updates for documentation

#### New dedicated endpoint

- **Good**, because separates classification concerns from check-in data
- **Bad**, because requires an additional API call from clients to get classification
- **Bad**, because increases API surface area and maintenance burden

#### Header-based response

- **Good**, because does not modify the response body at all
- **Bad**, because headers are harder to discover, document, and debug
- **Bad**, because violates NovaTrek API design conventions (data in response body, not headers)

### More Information

- Source code analysis: `CheckInRecord.java` already has `uiPattern` field (line 43), confirming the entity is ready for this data
- svc-trip-catalog Swagger spec: `Trip` schema to be extended with `adventure_category` field
