# NTK-10002: Risks

## RISK-001: Category Proliferation Without Classification Updates

**Likelihood**: Medium
**Impact**: Medium

**Description**: New adventure categories may be added to `svc-trip-catalog` by the catalog team without a corresponding update to the classification configuration in `svc-check-in`. When this happens, the new category will not be found in the classification table and will fall back to Pattern 3 (Full Service). While the fallback is safe per ADR-NTK10002-002, it means guests on potentially simple activities could be subjected to an unnecessarily long check-in process.

**Mitigation**: Establish a process requirement that any new adventure category added to the catalog must include a corresponding classification config update. Add the `checkin.classification.fallback.count` metric and set up an alert when fallback rate exceeds 5% of total classifications, indicating unmapped categories are in use.

## RISK-002: Cache Staleness

**Likelihood**: Low
**Impact**: Low

**Description**: The classification configuration is cached in memory with a 5-minute TTL. If a configuration change is pushed to Spring Cloud Config, there is a window of up to 5 minutes where some service instances may serve stale classification data. During this window, guests could receive the wrong check-in pattern.

**Mitigation**: For planned config changes, use the `/actuator/refresh` endpoint to force an immediate cache reload across all instances. For urgent corrections, the same endpoint can be called via the deployment pipeline. The 5-minute window is acceptable for routine updates.

## RISK-003: Override Rule Complexity Growth

**Likelihood**: Medium
**Impact**: Medium

**Description**: The current design includes 2 booking source overrides (PARTNER_API and WALK_IN). Over time, business stakeholders may request additional override rules based on other booking sources, guest tiers, promotional campaigns, or seasonal adjustments. Unchecked growth in override rules will make the classification logic harder to understand, test, and maintain.

**Mitigation**: Treat override rules as architectural decisions requiring formal review. Any new override must be documented in the decisions log with business justification. If the number of overrides exceeds 5, consider refactoring to a rules engine approach.

## RISK-004: Guest Confusion from Pattern Changes

**Likelihood**: Low
**Impact**: Medium

**Description**: If the classification mapping is updated between the time a guest books their trip and the time they check in, the guest may see a different check-in experience than what pre-trip communications described. For example, a guest told to "allow 10 minutes for check-in" might arrive and find only a 30-second confirmation screen, or vice versa.

**Mitigation**: Classification changes should be communicated to the guest communications team so that pre-trip emails reflect current patterns. Consider caching the determined pattern at booking time and storing it on the reservation so the check-in experience is locked in when the booking is made. This optimization is deferred to a future iteration.

## RISK-005: Current Code Safety Gap During Transition

**Likelihood**: High
**Impact**: High

**Description**: The current `AdventureCategoryClassifier.java` defaults to Pattern 1 (Basic) for unknown categories (line 74). This means that until the new `ClassificationService` is deployed and the feature flag is enabled, any guest with an unrecognized adventure category receives only a confirmation screen -- bypassing all safety steps. This is a live safety gap.

**Mitigation**: Prioritize the deployment of the new `ClassificationService` with the Pattern 3 fallback. As an interim measure, consider a hotfix to change the default in the existing `AdventureCategoryClassifier` from `PATTERN_1` to `PATTERN_3` before the full feature is ready. The feature flag approach ensures that the rollout is controlled.
