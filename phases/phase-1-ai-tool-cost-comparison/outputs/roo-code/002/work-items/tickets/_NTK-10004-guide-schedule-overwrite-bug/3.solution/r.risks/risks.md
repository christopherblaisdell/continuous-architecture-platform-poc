# NTK-10004: Risk Assessment

## RISK-001: Data Already Lost Cannot Be Recovered

**Likelihood**: CONFIRMED
**Impact**: HIGH

**Description**: Guide enrichment data (certifications, medical notes, availability exceptions, language skills) that has already been overwritten by past optimization cycles cannot be automatically recovered. There is no audit log of previous values, no event history, and no backup of individual field-level changes.

**Mitigation**: After deploying the fix, conduct a manual data recovery effort. Contact affected guides (identified from Elastic logs: G-4821, G-5190, G-3302, and others) and ask them to re-enter their enrichment data through the Guide Portal. Prioritize guides with safety-critical data (medical restrictions, certification requirements).

## RISK-002: Optimistic Locking Retry Storms Under High Contention

**Likelihood**: LOW
**Impact**: MEDIUM

**Description**: Adding `@Version` optimistic locking means concurrent writes will fail with `OptimisticLockingFailureException`. During the nightly batch optimization when multiple regions run simultaneously, cross-region guides could experience repeated version conflicts. If retry logic is aggressive, this could cause retry storms.

**Mitigation**: Implement exponential back-off with jitter on retry (e.g., 100ms, 200ms, 400ms + random jitter). Set a maximum retry count of 3. Log and alert on version conflicts exceeding the retry limit. Consider serializing optimization for guides assigned to multiple regions.

## RISK-003: Incomplete Field Ownership Documentation

**Likelihood**: MEDIUM
**Impact**: MEDIUM

**Description**: The fix depends on the orchestrator knowing which fields it owns and only updating those fields. If field ownership is not clearly documented and enforced, future developers may add new fields to `DailySchedule` without specifying ownership, potentially recreating the same overwrite pattern.

**Mitigation**: Document field ownership in the entity class using annotations or comments. Add a code review checklist item: "New DailySchedule fields must have documented ownership." Consider adding a `@OwnedBy` custom annotation for compile-time documentation.

## RISK-004: PUT Endpoint Removal May Break Unknown Consumers

**Likelihood**: LOW
**Impact**: MEDIUM

**Description**: The PUT endpoint at `/api/v1/schedules/{id}` is not documented in the OpenAPI contract, but undocumented endpoints can still have consumers (e.g., scripts, internal tools, monitoring). Deprecating or removing it could break these unknown consumers.

**Mitigation**: Deprecate the PUT endpoint with a `Sunset` response header and a `Deprecation` response header before removing it. Log all PUT requests with the caller identity for 30 days to identify any consumers. Only remove after confirming no active consumers remain.

## RISK-005: Guide Safety During Fix Rollout

**Likelihood**: MEDIUM
**Impact**: CRITICAL

**Description**: Until the fix is deployed, guide safety data continues to be at risk. Every optimization cycle that runs before the fix is deployed could silently remove medical restrictions, certification requirements, or safety notes from guide profiles.

**Mitigation**: As an immediate interim measure before the code fix, pause nightly optimization runs or exclude guides with safety-critical enrichment data from the optimization scope. Notify operations managers to manually verify guide safety data after any optimization run until the fix is deployed.
