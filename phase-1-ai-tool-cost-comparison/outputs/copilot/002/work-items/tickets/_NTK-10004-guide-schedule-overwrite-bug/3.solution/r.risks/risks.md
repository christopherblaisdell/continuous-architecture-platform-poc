# NTK-10004: Risks

## RISK-001 Migration of Existing PUT Callers

**Likelihood**: High
**Impact**: Medium

**Description**: Internal callers of the `PUT /api/v1/schedules/{id}` endpoint must be identified and migrated to use the new PATCH endpoint. If any caller is missed, the deprecated PUT endpoint (now delegating to PATCH logic) will handle the request safely, but the caller will not benefit from providing selective field updates.

**Mitigation**: Audit all consumers of the PUT endpoint through API gateway logs and service dependency graphs. The deprecated PUT endpoint is implemented as a safe delegation to PATCH, so missed callers will not cause data loss but will receive deprecation warnings in response headers and logs.

## RISK-002 Optimistic Lock Retry Storms

**Likelihood**: Low
**Impact**: Medium

**Description**: During nightly optimization of multiple regions, if many guides are assigned to cross-region trails, the optimistic locking mechanism could cause retry storms where multiple optimization processes repeatedly conflict on the same guide's schedule.

**Mitigation**: Implement exponential backoff with jitter on retry logic. Maximum 3 retries per schedule update. If retries are exhausted, log an error and skip the conflicting guide (the existing schedule remains intact). Monitor `schedule.version.conflict.count` metric to detect if retry frequency exceeds acceptable thresholds.

## RISK-003 Data Already Lost in Production

**Likelihood**: High
**Impact**: Medium

**Description**: Guide enrichment data that has already been lost in production cannot be recovered by this fix. The fix prevents future data loss but does not restore previously deleted notes, preferences, or certifications.

**Mitigation**: After deploying the fix, communicate to all guides through the Guide Portal that they should review and re-enter any missing schedule information. Provide a re-entry period and operational support to facilitate data restoration.

## RISK-004 Incomplete Field Ownership Documentation

**Likelihood**: Medium
**Impact**: Medium

**Description**: The PATCH endpoint approach requires explicit documentation of which fields are owned by which service. If field ownership is not clearly documented, future developers may inadvertently update fields they do not own by adding them to the DTO.

**Mitigation**: Document field ownership boundaries in the service's README and in code comments on the `DailyScheduleUpdateRequest` DTO. Add a code review checklist item requiring field ownership verification when new fields are added to the schedule entity.

## RISK-005 Regression During Deployment

**Likelihood**: Low
**Impact**: High

**Description**: The transition from PUT to PATCH changes the update behavior of a safety-critical system. A regression during deployment could either revert to the data loss behavior or introduce a new failure mode.

**Mitigation**: Deploy behind a feature flag that allows instant rollback to PUT behavior. Run comprehensive integration tests in staging that simulate the full optimization cycle with concurrent regional runs. Monitor enrichment field integrity for 48 hours post-deployment before marking the flag as permanently enabled.
