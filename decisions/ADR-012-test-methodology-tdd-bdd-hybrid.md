# ADR-012: Adopt TDD/BDD Hybrid Test Methodology

## Status

Accepted

## Date

2026-03-17

## Context and Problem Statement

The NovaTrek Continuous Architecture Platform produces solution designs, API contracts, and implementation guidance for 19 microservices — but the delivery practice has no defined testing standards. The arc42 templates reference coverage targets (80% line coverage) and the risk register flags test gaps, yet no enforcement mechanism, methodology, or tooling exists. As services evolve through solution designs, untested changes compound risk across service boundaries.

## Decision Drivers

- The platform already maintains 19 OpenAPI specs and a cross-service integration map (`architecture/metadata/cross-service-calls.yaml`) that define every contract boundary — these should drive contract tests automatically
- User stories in solution designs include acceptance criteria that map naturally to executable BDD scenarios
- The service template (`services/template/build.gradle.kts`) already includes JaCoCo, JUnit 5, and Testcontainers — the tooling foundation exists but is not consistently applied across all services
- Cross-service integration points are the highest-risk boundaries — a failing contract between svc-check-in and svc-reservations directly impacts guest experience
- The team is small and needs fast feedback — heavy process or ceremony will not be adopted

## Considered Options

1. TDD-only (Test-Driven Development across all layers)
2. BDD-only (Behavior-Driven Development with Gherkin scenarios for everything)
3. TDD/BDD hybrid (TDD for unit and integration tests, BDD for acceptance tests, spec-driven for contract tests)

## Decision Outcome

**Chosen Option**: "TDD/BDD hybrid", because it applies the right methodology at each layer of the testing pyramid — TDD for fast, developer-focused feedback at the unit and integration levels; BDD for stakeholder-readable acceptance validation derived from user story criteria; and spec-driven contract testing that leverages the OpenAPI specs already maintained as the architecture source of truth.

### Confirmation

- Every new service build file includes JaCoCo with coverage thresholds configured per `config/test-standards.yaml`
- CI pipeline (`validate-solution.yml`) enforces coverage gates on PRs affecting service code
- Solution design reviews verify that a test plan exists in `3.solution/g.guidance/test-plan.md`
- Cross-service contract tests exist for every entry in `cross-service-calls.yaml`

## Consequences

### Positive

- Consistent test expectations across all 19 services — no ambiguity about what "tested" means
- Acceptance criteria in user stories become executable — BDD scenarios serve as living documentation
- Contract tests catch breaking API changes before they reach production — critical for the 47 cross-service integration points
- TDD at the unit level forces clean API design and prevents gold-plating
- Coverage thresholds provide an objective quality gate — PRs blocked below minimum

### Negative

- BDD requires Gherkin authoring discipline — poorly written scenarios become maintenance overhead
- Initial velocity reduction as teams adopt TDD habits and write test-first
- Mutation testing (PITest) adds CI execution time — starts as advisory to manage build duration

### Neutral

- Existing services without tests require a retrofit effort proportional to their codebase size
- Coverage thresholds will be tuned over time — starting values are informed by industry practice, not NovaTrek-specific data
- Contract testing tool selection (Pact vs Spring Cloud Contract) is deferred to Phase B (see TEST-METHODOLOGY-ROADMAP.md)

## Pros and Cons of the Options

### TDD-Only

Test-Driven Development applied to all layers — red-green-refactor for unit, integration, and acceptance tests.

- **Good**, because it enforces a test-first discipline at every level
- **Good**, because it keeps all tests in the same framework (JUnit 5)
- **Neutral**, because developers already familiar with JUnit need no new tooling
- **Bad**, because acceptance-level tests written in JUnit are not stakeholder-readable — acceptance criteria lose traceability to user stories
- **Bad**, because it does not leverage the natural mapping from user story Gherkin to executable scenarios

### BDD-Only

All tests written as Gherkin scenarios executed by Cucumber-JVM, from unit-level to end-to-end.

- **Good**, because every test is human-readable and maps to business behavior
- **Good**, because stakeholders can review test scenarios without reading Java
- **Neutral**, because Cucumber-JVM integrates with the existing Spring Boot test infrastructure
- **Bad**, because unit-level Gherkin scenarios add boilerplate (step definitions, feature files) for tests that are faster and clearer as plain JUnit
- **Bad**, because BDD at the unit level fights the natural grain of TDD — the red-green-refactor cycle does not map well to Given/When/Then for low-level logic

### TDD/BDD Hybrid

TDD for unit and integration tests (JUnit 5), BDD for acceptance tests (Cucumber-JVM), spec-driven for contract tests (OpenAPI-derived).

- **Good**, because each test layer uses the methodology that fits its purpose
- **Good**, because acceptance criteria in user stories have a direct, traceable path to Gherkin scenarios
- **Good**, because contract tests leverage the 19 OpenAPI specs already maintained — no manual test authoring for API shape validation
- **Bad**, because two test authoring paradigms (JUnit + Cucumber) increase the learning surface
- **Neutral**, because the boundary between TDD and BDD layers is clearly defined by the testing pyramid — no ambiguity about which methodology applies where

## More Information

- Test Methodology Roadmap: `roadmap/TEST-METHODOLOGY-ROADMAP.md`
- Testing pyramid and coverage thresholds: `config/test-standards.yaml`
- Cross-service integration map: `architecture/metadata/cross-service-calls.yaml`
- Service template with JaCoCo: `services/template/build.gradle.kts`
- Solution design template (test plan section): `portal/docs/standards/solution-design/solution-design-template.md`
