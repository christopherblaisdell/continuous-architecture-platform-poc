# NTK-10004: User Stories

---

## US-001: As a guide, I want my manually entered schedule data to survive optimization cycles

**Priority**: Critical  
**Acceptance Criteria**:
1. When I enter a vacation block through the Guide Portal, it persists after any optimization run (nightly or on-demand)
2. When I add a medical restriction note, it remains visible after schedule optimization completes
3. When I set a max-group-size override for a specific date, it is not overwritten by the orchestrator

**Relates to**: ADR-NTK10004-001 (PATCH semantics)

---

## US-002: As an operations manager, I want concurrent regional optimizations to not corrupt guide data

**Priority**: High  
**Acceptance Criteria**:
1. When I trigger optimization for the Cascadia region while Sierra region optimization is running, a guide assigned to cross-region trails does not lose data from either optimization
2. If a write conflict occurs, the system detects it and retries automatically
3. If automatic retry fails, I receive a notification identifying the affected guide(s) so I can manually verify

**Relates to**: ADR-NTK10004-002 (Optimistic locking)

---

## US-003: As a guide, I want to be confident that my safety-critical notes are reliably stored

**Priority**: Critical  
**Acceptance Criteria**:
1. My medical restriction (e.g., "No high-altitude trails until medical clearance") is visible in the Guide Portal before and after any system process modifies my schedule
2. If any process attempts to remove or nullify my safety notes, the system prevents the change and logs a warning
3. I do not need to periodically check whether my restrictions are still in place

**Relates to**: Impact 2 (guide-management monitoring)

---

## US-004: As a solution architect, I want the PUT endpoint deprecated with a clear migration path

**Priority**: Medium  
**Acceptance Criteria**:
1. The PUT endpoint returns a `Sunset` header indicating the deprecation date
2. All PUT calls are logged with caller identity for migration tracking
3. The new PATCH endpoint is documented in the OpenAPI specification
4. Migration guide is provided to any identified callers of the PUT endpoint

**Relates to**: Impact 3 (API contract update), RISK-003 (client migration)
