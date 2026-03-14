# Comprehensive Test Methodology and Practice

**Date**: 2026-03-11
**Last Updated**: 2026-03-14
**Priority**: High
**Status**: In Progress — Phase A complete

## Summary

Establish a comprehensive testing methodology across the NovaTrek platform delivery practice. The current architecture practice produces solution designs, capability rollups, and portal publishing — but has no defined testing standards, coverage requirements, or quality gates for the services themselves.

## Why This Matters

- No testing standards documented across the 19 microservices
- arc42 templates reference "80% unit test coverage" as a constraint, but no enforcement mechanism exists
- arc42 risk register identifies "gaps in test coverage" as a known risk — currently unmitigated
- Solution designs produce API contract changes and implementation guidance without corresponding test expectations
- Without regression coverage, capability rollup (the core value of the platform) risks introducing breaking changes silently

## Action Items

- [x] Define a test methodology document covering unit, integration, contract, and end-to-end testing layers — [TEST-METHODOLOGY-ROADMAP.md](../docs/roadmap/TEST-METHODOLOGY-ROADMAP.md)
- [x] Evaluate TDD (Test-Driven Development) as the standard practice for service implementation — ADR-012: TDD at unit and integration layers
- [x] Evaluate BDD (Behavior-Driven Development) with Gherkin/Cucumber for acceptance criteria validation — ADR-012: BDD at acceptance layer
- [x] Establish minimum coverage thresholds per service (unit, branch, mutation) — [config/test-standards.yaml](../config/test-standards.yaml)
- [x] Create an ADR for the chosen testing approach (TDD vs BDD vs hybrid) — [ADR-012](../decisions/ADR-012-test-methodology.md)
- [x] Add test requirements to the solution design template (test plan section in guidance) — [solution-design-template.md](../portal/docs/standards/solution-design/solution-design-template.md)
- [ ] Add automated regression test suites to CI pipelines (run on every PR)
- [ ] Define contract testing strategy for cross-service API boundaries (e.g., Pact, Spring Cloud Contract)
- [ ] Add test coverage validation to `validate-solution.yml` CI workflow
- [ ] Document test data management strategy (synthetic test data generation, fixture conventions)

## Delivery Practice Integration Points

| Artifact | Test Impact |
|----------|-------------|
| Solution Design Template | Add test plan section to `3.solution/g.guidance/` |
| PR Review Checklist | Add "test coverage meets threshold" criterion |
| CI Pipeline | Add coverage reporting and threshold enforcement |
| Impact Assessments | Include "test impact" — which test suites need updating |
| User Stories | Acceptance criteria become BDD scenario candidates |
| OpenAPI Specs | Contract tests auto-generated from spec definitions |

## Related

- arc42 constraints template: references 80% coverage target
- arc42 risk register: test coverage gaps listed as known risk
- Detailed roadmap: `roadmap/TEST-METHODOLOGY-ROADMAP.md` (phased rollout plan)
- Main roadmap: `roadmap/ROADMAP.md` Section 7 — Future Initiatives
- Architecture review checklist: `roadmap/ROADMAP.md` Section 8
- CI validation workflow: `.github/workflows/validate-solution.yml`
- Solution design template: `portal/docs/standards/solution-design/`
