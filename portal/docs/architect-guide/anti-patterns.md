# Anti-Patterns

This page catalogs common architectural anti-patterns at NovaTrek. Flag these in reviews, avoid them in new designs.

---

## Data and Integration Anti-Patterns

### Shared Database

**Problem**: Multiple services read/write the same database tables, creating invisible coupling.

**Why it's harmful**: Changes to table structure by one service break other services silently. No service truly owns the data. Schema migrations become coordination nightmares.

**Recommended alternative**: API-mediated access. The owning service exposes read/write APIs. Other services call those APIs instead of hitting the database directly.

**Example**: If `svc-analytics` needs check-in data, it calls `svc-check-in`'s API — it does not query the check-in database.

---

### Distributed Monolith

**Problem**: Services are tightly coupled through long synchronous call chains. A request to Service A triggers calls to B, C, D, E in sequence.

**Why it's harmful**: A failure in any service in the chain fails the entire operation. Latency compounds across every hop. The services cannot be deployed or scaled independently.

**Recommended alternative**: Event-driven decoupling for cross-domain communication. Use the saga pattern or choreography for multi-service workflows. Only use synchronous calls within a bounded context for real-time reads.

---

### Entity Replacement (PUT Overwrite)

**Problem**: Using PUT semantics to update entities, sending the full entity and replacing everything — including fields owned by other services or set by other workflows.

**Why it's harmful**: Service A sends a reservation update. The PUT overwrites the `guide_assignment` field that Service B had just set. Data is silently lost.

**Recommended alternative**: PATCH semantics with field-level updates. Only modify the specific fields your operation owns. This is codified in [ADR-010](../decisions/ADR-010-patch-semantics-schedule-updates.md) for schedule updates.

---

### Missing Concurrency Control

**Problem**: No optimistic locking on mutable shared entities. Two concurrent updates both read version N, both write version N+1, and one silently overwrites the other.

**Why it's harmful**: Lost updates. In scheduling, this could mean double-booking a guide or overwriting an assignment.

**Recommended alternative**: `_rev` or `@Version` field with 409 Conflict on mismatch. The second writer gets a conflict response and must retry with the current version. See [ADR-011](../decisions/ADR-011-optimistic-locking-daily-schedule.md).

---

## Identity Anti-Patterns

### Shadow Guest Records

**Problem**: Services maintaining their own copy of guest identity data instead of delegating to `svc-guest-profiles`.

**Why it's harmful**: Guest profile updates (name change, contact info update) do not propagate to shadow copies. You end up with inconsistent guest data across services.

**Recommended alternative**: Always resolve guest identity through `svc-guest-profiles`. Cache for performance if needed, but the profile service is the single source of truth.

---

## Safety Anti-Patterns

### Unsafe Defaults

**Problem**: Unknown or unmapped inputs defaulting to the lowest safety level.

**Why it's harmful**: A new adventure category that hasn't been classified could default to Pattern 1 (self-service check-in). A guest goes rock climbing with no safety briefing and no gear check because the system assumed it was a nature walk.

**Recommended alternative**: Default to the highest safety level (Pattern 3 — Full Service). This ensures maximum safety protocols for any unrecognized activity. This is codified in [ADR-005](../decisions/ADR-005-pattern3-default-fallback.md).

---

## Code Anti-Patterns

### Hardcoded Classification

**Problem**: Business rules embedded in code constants or switch statements.

**Why it's harmful**: Adding a new adventure category requires a code change, a build, and a deployment. The business team cannot update classifications without developer involvement.

**Recommended alternative**: Configuration-driven approach. Adventure classifications live in `config/adventure-classification.yaml` and are read at runtime. See [ADR-004](../decisions/ADR-004-configuration-driven-classification.md).

---

### Missing Null Handling

**Problem**: Nullable fields added to API schemas without documenting what null means.

**Why it's harmful**: Consumer A interprets null elevation as "sea level". Consumer B interprets it as "unknown". Consumer C crashes on null. Each consumer handles it differently, creating inconsistent behavior.

**Recommended alternative**: Explicit `nullable: true` annotation with documented interpretation. See [ADR-003](../decisions/ADR-003-nullable-elevation-fields.md) for the nullable elevation fields decision.

---

### Full Entity Replacement in Code

**Problem**: Service code using `save(incomingEntity)` that replaces the entire database row with the incoming request body.

**Why it's harmful**: Fields that were set by other workflows (e.g., `guide_assignment`, `modified_by`, `last_verified`) are overwritten with null or stale values from the incoming request.

**Recommended alternative**: Field-level merge — read the existing entity, update only the changed fields, save.

---

### Direct Cross-Service Database Queries

**Problem**: Service A executes SQL queries against Service B's database.

**Why it's harmful**: Service B cannot change its schema without coordinating with Service A. The coupling is invisible — no API contract, no versioning, no backward compatibility guarantee.

**Recommended alternative**: Service B exposes an API. Service A calls the API. The API contract is versioned and tested.

---

### Unchecked Null Returns

**Problem**: Calling `repository.findById(id)` and using the result without checking for null/empty.

**Why it's harmful**: NullPointerException in production. Depending on the context, this could mean a 500 error to the guest during check-in or a silently failed safety check.

**Recommended alternative**: Use `Optional` return types. Handle the empty case explicitly — return a 404, use a default, or throw a domain-specific exception.

---

## How to Flag Anti-Patterns

When you encounter an anti-pattern during research or review:

1. **Note it in your analysis** with the specific file path and line number
2. **Reference the relevant ADR** if one exists (most common anti-patterns have corresponding decisions)
3. **Include it in the solution design's risk register** if the anti-pattern affects the current design
4. **Propose a remediation** in the impact assessment if the anti-pattern is in code you're modifying

Do not attempt to fix anti-patterns in code — that's the developer's responsibility. Document the finding and include it in the solution design's guidance if the fix is part of the approved changes.

---

## Source Code Analysis Guidelines

When reviewing Java source code in `services/`:

1. **Read the full file** before drawing conclusions — do not rely on method names alone
2. **Trace the data flow**: controller -> service -> repository
3. **Cross-reference with OpenAPI specs** — verify behavior matches the published contract
4. **Note line numbers** for all findings — cite specific lines in analysis documents
5. **Check for the patterns above** — especially entity replacement, missing locking, and cross-service database access
