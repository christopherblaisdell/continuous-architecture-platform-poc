# NTK-10004: User Stories

---

## US-001: Guide Schedule Data Preserved After Optimization

**As a** guide,
**I want** my manually entered schedule information to survive whenever the system optimizes trail assignments,
**So that** I do not have to repeatedly re-enter vacation blocks, training days, medical restrictions, and group size preferences.

**Priority**: Critical

**Acceptance Criteria**:
1. When I enter a vacation block through the Guide Portal, it remains after any optimization run, whether nightly or on-demand
2. When I add a medical restriction note (e.g., "No high-altitude trails until medical clearance"), it persists after schedule optimization completes
3. When I set a max-group-size override for a specific date, it is preserved after optimization

---

## US-002: Concurrent Regional Optimizations Do Not Corrupt Guide Data

**As an** operations manager,
**I want** simultaneous schedule optimizations across different regions to not corrupt guide data,
**So that** guides assigned to cross-region trails retain their complete schedule information regardless of optimization timing.

**Priority**: High

**Acceptance Criteria**:
1. When I trigger optimization for the Cascadia region while Sierra region optimization is running, a guide assigned to cross-region trails does not lose data from either optimization
2. If a conflict occurs during simultaneous updates, the system detects it and resolves it automatically
3. If automatic resolution fails, I receive a notification identifying the affected guide so I can verify manually

---

## US-003: Safety Critical Notes Reliably Stored

**As a** guide with medical or safety restrictions,
**I want** to be confident that my safety-critical notes are never removed by any automated process,
**So that** I am not assigned to activities that conflict with my medical limitations or certification status.

**Priority**: Critical

**Acceptance Criteria**:
1. My medical restriction is visible in the Guide Portal before and after any system process modifies my schedule
2. No automated process can silently remove my safety notes — the system prevents such changes
3. I do not need to periodically check whether my restrictions are still in place

---

## US-004: Audit Trail for Schedule Changes

**As an** operations manager,
**I want** to see who or what modified a guide's schedule and when,
**So that** I can trace the source of any data discrepancy and hold the appropriate process accountable.

**Priority**: Medium

**Acceptance Criteria**:
1. Each schedule modification records the identity of the modifier (person or system process) and the timestamp
2. I can review the modification history to determine whether a change was made by a guide, an optimization process, or another system
3. Changes during the transition period are tracked to verify that the fix is working as expected
