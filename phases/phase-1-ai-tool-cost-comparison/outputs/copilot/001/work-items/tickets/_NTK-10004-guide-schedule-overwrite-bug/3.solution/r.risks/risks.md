# NTK-10004: Risks

---

## RISK-001: Incomplete Field Ownership Mapping

**Likelihood**: Medium
**Impact**: High
**Risk Level**: HIGH

**Description**: The current fix addresses `guideNotes` and `guidePreferences`, but there may be additional fields on the `DailySchedule` entity (or on related entities accessed via the same API) that are not owned by the scheduling orchestrator. If the field ownership mapping is incomplete, the PATCH DTO may still inadvertently include fields owned by other services.

**Mitigation**: Conduct a comprehensive audit of all fields in the `DailySchedule` entity and the `daily_schedules` table. Document the owner of each field explicitly. Review with svc-guide-management team before implementation.

---

## RISK-002: Optimistic Lock Retry Exhaustion Under Peak Load

**Likelihood**: Low
**Impact**: Medium
**Risk Level**: MEDIUM

**Description**: During peak scheduling periods (e.g., nightly batch optimization across all regions), concurrent writes to the same guide's schedule may exceed the retry limit (3 attempts). If all retries are exhausted, the optimization result for that guide is lost and must be recovered manually or by re-running the optimization.

**Mitigation**:
- Implement exponential backoff with jitter on retries
- Add a dead-letter mechanism: if all retries fail, write the failed update to a retry queue for manual review
- Monitor `schedule.patch.retry.exhausted` metric and alert on occurrences

---

## RISK-003: PUT Endpoint Deprecation and Client Migration

**Likelihood**: Medium
**Impact**: Medium
**Risk Level**: MEDIUM

**Description**: The existing PUT endpoint may be called by undiscovered internal clients (scheduled jobs, admin tools, migration scripts). Deprecating PUT without identifying all callers risks breaking unknown integrations.

**Mitigation**:
- Add structured logging to the PUT endpoint (caller identity, source IP, user-agent)
- Run in observation mode for 2 sprints before sunset
- Search all repositories for references to `PUT /api/v1/schedules/` or `updateSchedule`
- Announce deprecation through architecture guild and service catalog

---

## RISK-004: Historical Data Corruption Recovery

**Likelihood**: High
**Impact**: Medium
**Risk Level**: HIGH

**Description**: Guide enrichment data that has already been lost cannot be automatically recovered by the fix -- the fix only prevents future data loss. Guides who have lost vacation blocks, medical notes, or certification data may not realize their information is missing until they receive a conflicting assignment.

**Mitigation**:
- Notify all guides to review and re-enter their schedule metadata after the fix is deployed
- Provide an Operations Manager report listing all guides whose `guideNotes` or `guidePreferences` are currently null but had non-null values in past audit logs (if available)
- Prioritize guides with safety-critical notes (medical restrictions, altitude limits)
