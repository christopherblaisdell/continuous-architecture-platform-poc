# NTK-10004: Risk Assessment

## RISK-001: Ongoing Data Loss Until Fix is Deployed

**Likelihood**: CERTAIN
**Impact**: HIGH
**Status**: ACTIVE

**Description**: The bug continues to silently overwrite guide enrichment data on every optimization cycle. Every nightly batch run and every on-demand regional optimization destroys manually-entered guide notes, availability exceptions, and preferences. Each occurrence creates safety risk (removed medical restrictions) and operational overhead (guides must re-enter data).

**Mitigation**: Expedite the PATCH semantics fix to Sprint 19 or 20. As an immediate interim measure, communicate to operations managers that optimization runs will overwrite guide data and that guides should verify their profiles after any optimization event. Consider temporarily disabling nightly optimization in the most impacted regions until the fix is deployed.

## RISK-002: Incomplete Data Field Identification

**Likelihood**: Medium
**Impact**: Medium

**Description**: The investigation identified `guideNotes` and `guidePreferences` as the two overwritten fields. However, there may be additional fields or related entities that are also affected by the full-entity replacement that were not captured in the investigation. If the PATCH fix only protects the known fields, other data may continue to be lost.

**Mitigation**: Conduct a thorough field-by-field audit of the `DailySchedule` entity and the `daily_schedules` table to identify ALL fields not owned by the scheduling orchestrator. The PATCH DTO must explicitly enumerate ONLY orchestrator-owned fields, ensuring that any field NOT in the DTO is automatically protected.

## RISK-003: Optimistic Locking Contention During Peak Optimization

**Likelihood**: Medium
**Impact**: Medium

**Description**: Adding `@Version` optimistic locking will cause concurrent optimization writes to fail with `OptimisticLockException`. During the nightly batch when all regions optimize simultaneously, guides assigned to cross-region trails may experience high contention and repeated retry failures.

**Mitigation**: Implement exponential backoff retry (3 retries, 100ms initial delay, 2x multiplier). Monitor conflict rate after deployment. If contention is consistently high, consider scheduling regional optimizations in staggered windows rather than simultaneously.

## RISK-004: Regression Through New PUT Callers

**Likelihood**: Low
**Impact**: HIGH

**Description**: If the PUT endpoint is deprecated but not removed, a future developer could inadvertently use it, reintroducing the overwrite bug. The undocumented nature of the current PUT endpoint increases this risk, as there is no formal API governance preventing its use.

**Mitigation**: Remove the PUT endpoint entirely in a follow-up sprint. Until then, add a WARNING log and a deprecation header to any PUT request. Document the PATCH endpoint in the OpenAPI specification and mark PUT as deprecated in the spec if it must be retained temporarily.

## RISK-005: Guide Retention Impact During Fix Window

**Likelihood**: Medium
**Impact**: Medium

**Description**: The ticket comments indicate that guides have already escalated to HR. Until the fix is deployed, continued data loss events damage trust in the system and may contribute to guide attrition during the peak season preparation period.

**Mitigation**: Communicate directly with affected guides that the root cause has been identified and a fix is in progress with a target deployment date. Provide a manual workaround (export/re-import guide profiles after optimization) during the interim period.
