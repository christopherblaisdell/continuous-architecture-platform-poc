# ADR-012: Test Methodology for NovaTrek Services

| | |
|-----------|-------|
| **Status** | ACCEPTED |
| **Date** | 2026-03-14 |
| **Last Updated** | 2026-03-14 |
| **Decision Makers** | Christopher Blaisdell, Architecture Practice |
| **Initiative** | Test Methodology and Practice |

## Context and Problem Statement

The Continuous Architecture Platform produces solution designs, API contracts, and implementation guidance across 19+ microservices — but has no defined testing standards or enforcement mechanism. The arc42 templates reference an 80% unit test coverage target as a quality constraint, and the risk register flags test coverage gaps as a known risk. Without a defined testing approach, capability rollup may introduce breaking changes silently across service boundaries.

**Which testing methodology should NovaTrek Services adopt for unit, integration, contract, and acceptance testing — and what coverage thresholds should be enforced in CI?**

## Decision Drivers

- **Service boundary safety** — Cross-service API contracts must be validated automatically; breaking changes must be caught before merge
- **Existing constraint compliance** — arc42 templates document 80% line coverage as a quality constraint for all services
- **Traceability** — User story acceptance criteria should map to executable test scenarios that prove business behavior
- **Developer ergonomics** — The methodology must integrate naturally with the existing Java/Spring Boot/Gradle service stack
- **CI enforcement** — Coverage gates must run on every PR with no manual intervention; failure must block merge
- **Incremental adoption** — The methodology must be adoptable service by service without requiring a full-fleet migration before any value is realized

## Considered Options

### Option A: TDD-Only (Unit and Integration)

All test layers use Test-Driven Development exclusively. Developers write failing tests before implementation. No BDD adoption.

**Strengths:**
- Consistent single methodology across all test layers
- Well-understood in Java ecosystem (JUnit 5, Mockito, AssertJ)
- Forces clean API design and modular code
- Fast feedback loop at the unit level

**Weaknesses:**
- TDD at the acceptance layer is difficult — business stakeholders cannot read or write JUnit tests
- No bridge between user story acceptance criteria and executable scenarios
- Contract testing requires a separate discipline with no overlap to TDD practices
- Acceptance criteria traceability requires manual mapping

### Option B: BDD-Only (Gherkin for All Layers)

All test layers use Behavior-Driven Development. Every scenario is written in Gherkin (Given/When/Then) and executed by Cucumber-JVM.

**Strengths:**
- Human-readable test scenarios — business stakeholders can review and contribute
- Direct traceability from user stories to executable acceptance tests
- Living documentation — Gherkin scenarios serve as always-current specification

**Weaknesses:**
- BDD at the unit level adds Gherkin overhead for low-level tests that have no business audience
- Step definition boilerplate increases maintenance burden significantly
- Slower feedback at unit layer due to Cucumber execution overhead
- More complex setup than JUnit for developer-owned unit tests
- Not standard practice in most Java service teams — high learning curve

### Option C: TDD + BDD Hybrid (Recommended)

Apply TDD at the unit and integration layers for fast, developer-owned feedback. Apply BDD at the acceptance layer to connect user story acceptance criteria to executable scenarios. Use spec-driven contract testing auto-generated from OpenAPI specs for cross-service boundaries.

| Layer | Methodology | Rationale |
|-------|-------------|-----------|
| Unit | TDD | Fast feedback, forces clean design, standard practice in Java |
| Integration | TDD | Validates data access and service composition; no business audience |
| Contract | Spec-driven (OpenAPI) | Auto-generated from existing specs; no manual authoring; CI-validated |
| Acceptance | BDD (Cucumber-JVM) | User stories produce Gherkin scenarios; acceptance criteria become executable |
| E2E | Scripted | Small set of critical path scripts; not TDD or BDD |

**Strengths:**
- Each layer uses the most appropriate methodology for its audience and feedback speed
- Acceptance criteria traceability from user stories to Gherkin scenarios
- Contract testing leverages existing OpenAPI specs — no new authoring required
- Standard tools in each layer reduce the learning curve
- Coverage thresholds enforced at unit and integration layers where they are meaningful

**Weaknesses:**
- Two methodologies to learn and maintain (TDD and BDD)
- Requires Cucumber-JVM setup in addition to JUnit 5 for services with BDD scenarios
- Step definition library grows over time and requires maintenance

## Decision Outcome

**Selected option:** Option C — TDD + BDD Hybrid

The hybrid approach applies the right tool to each test layer: TDD where speed and design feedback matter (unit, integration), BDD where business traceability matters (acceptance), and spec-driven validation where API contracts define the boundary (contract tests). This matches the existing solution design workflow — user story acceptance criteria are already written per the solution design template, and BDD provides the natural executable bridge.

### Coverage Thresholds (CI-Enforced)

All thresholds are defined in `config/test-standards.yaml` and applied via JaCoCo in each service build.

| Metric | Minimum Threshold | Target | CI Behavior |
|--------|-------------------|--------|-------------|
| Line coverage | 80% | 90% | PR blocked below minimum |
| Branch coverage | 70% | 80% | PR blocked below minimum |
| Mutation score | 60% | 75% | Advisory report (gate in Phase D) |
| Contract test coverage | 100% of cross-service calls | 100% | PR blocked below 100% |

### Tooling

| Layer | Tool | Version |
|-------|------|---------|
| Unit + Integration | JUnit 5, Mockito, AssertJ | Spring Boot 3.x managed |
| Coverage measurement | JaCoCo | Gradle plugin |
| Mutation testing | PITest | 1.15.x |
| Contract testing | Spring Cloud Contract (pending ADR-013) | Spring Cloud managed |
| BDD acceptance | Cucumber-JVM | 7.x |
| E2E | JUnit 5 + REST-assured | — |

### Consequences

**Positive:**
- Every service has CI-enforced coverage gates — no regression without coverage
- User story acceptance criteria are executable via Gherkin scenarios
- Contract tests auto-generated from OpenAPI specs catch breaking changes before merge
- Coverage thresholds are centrally defined in `config/test-standards.yaml` — one change updates all services

**Negative:**
- Services without BDD setup require a one-time Cucumber-JVM configuration step
- Step definition libraries must be maintained as services evolve
- Mutation testing adds build time — advised to run nightly rather than on every PR

**Neutral:**
- Existing tests in all services remain valid; this ADR does not require rewrites
- PITest mutation score is advisory until Phase D of the rollout; build times are unaffected initially
- Contract test infrastructure (Pact Broker or Spring Cloud Contract) requires a separate ADR for tool selection

## Phased Rollout

| Phase | Description | Deliverables |
|-------|-------------|-------------|
| A — Standards and Tooling | This ADR, coverage config, build template updates, solution design template update | ADR-012, `config/test-standards.yaml`, updated `build.gradle.kts` templates |
| B — Contract Testing | Evaluate Pact vs Spring Cloud Contract; ADR for tool selection; set up broker; write first contracts for svc-check-in boundaries | ADR-013, Pact Broker or Spring Cloud Contract infrastructure |
| C — BDD Adoption | Set up Cucumber-JVM; convert existing acceptance criteria to Gherkin; write step definitions for common patterns | Feature files derived from NTK-10003 and NTK-10006 user stories |
| D — Coverage Enforcement | Enable JaCoCo coverage gate in CI; promote mutation score to gate | Updated `validate-solution.yml`, coverage dashboard |

## Links

- [Test Methodology Roadmap](../roadmap/TEST-METHODOLOGY-ROADMAP.md)
- [Architecture Review Checklist](../roadmap/ROADMAP.md#8-architecture-review-checklist)
- [cross-service-calls.yaml](../architecture/metadata/cross-service-calls.yaml) — contract test boundary source
- [config/test-standards.yaml](../config/test-standards.yaml) — coverage thresholds
- [services/template/build.gradle.kts](../services/template/build.gradle.kts) — service build template
