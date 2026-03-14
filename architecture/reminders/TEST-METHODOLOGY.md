# Comprehensive Test Methodology and Practice

**Date**: 2026-03-11
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

- [x] Define a test methodology document covering unit, integration, contract, and end-to-end testing layers — see [ADR-012](../../decisions/ADR-012-test-methodology.md)
- [x] Evaluate TDD (Test-Driven Development) as the standard practice for service implementation — selected for unit and integration layers
- [x] Evaluate BDD (Behavior-Driven Development) with Gherkin/Cucumber for acceptance criteria validation — selected for acceptance layer
- [x] Establish minimum coverage thresholds per service (unit, branch, mutation) — see [config/test-standards.yaml](../../config/test-standards.yaml)
- [x] Add JaCoCo coverage enforcement to service build templates — updated services/template and all existing services
- [x] Add PITest mutation testing to service build templates — advisory in Phase A
- [x] Add test requirements to the solution design template (test plan section in guidance) — added to solution-design-template.md
- [ ] Add automated regression test suites to CI pipelines (run on every PR) — Phase D
- [ ] Define contract testing strategy for cross-service API boundaries (e.g., Pact, Spring Cloud Contract) — Phase B
- [ ] Add test coverage validation to `validate-solution.yml` CI workflow — Phase D
- [ ] Create an ADR for contract testing tool selection (Pact vs Spring Cloud Contract) — Phase B (ADR-013)
- [ ] Document test data management strategy (synthetic test data generation, fixture conventions) — Phase B/C

## Delivery Practice Integration Points

| Artifact | Test Impact |
|----------|-------------|
| Solution Design Template | Test plan section added to `3.solution/g.guidance/` |
| PR Review Checklist | Test coverage and test plan criteria added |
| CI Pipeline | Coverage reporting and threshold enforcement — Phase D |
| Impact Assessments | Include "test impact" — which test suites need updating |
| User Stories | Acceptance criteria become BDD scenario candidates |
| OpenAPI Specs | Contract tests auto-generated from spec definitions — Phase B |

## Related

- ADR-012 (test methodology decision): `decisions/ADR-012-test-methodology.md`
- Coverage thresholds: `config/test-standards.yaml`
- Detailed roadmap: `roadmap/TEST-METHODOLOGY-ROADMAP.md` (phased rollout plan)
- Main roadmap: `roadmap/ROADMAP.md` Section 7 — Future Initiatives
- Architecture review checklist: `roadmap/ROADMAP.md` Section 8
- CI validation workflow: `.github/workflows/validate-solution.yml`
- Solution design template: `portal/docs/standards/solution-design/`
