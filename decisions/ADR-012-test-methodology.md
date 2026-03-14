# ADR-012: Test Methodology — TDD and BDD Hybrid Approach

| | |
|-----------|-------|
| **Status** | Accepted |
| **Date** | 2026-03-14 |
| **Decision Makers** | Christopher Blaisdell, Architecture Practice |
| **Companion** | [TEST-METHODOLOGY-ROADMAP.md](../docs/roadmap/TEST-METHODOLOGY-ROADMAP.md) |
| **Config** | [config/test-standards.yaml](../config/test-standards.yaml) |

## Context and Problem Statement

The Continuous Architecture Platform produces solution designs, API contracts, and implementation guidance for 22 NovaTrek microservices. The delivery practice has no defined testing standards, coverage requirements, or quality gates. As services evolve through solution designs, untested changes compound risk across service boundaries.

The arc42 constraint templates already reference an 80% unit test coverage target, and the arc42 risk register identifies test coverage gaps as a known risk — but no enforcement mechanism, methodology, or tooling exists to make these constraints operational.

**Which testing methodology should the NovaTrek Architecture Practice adopt to enforce quality standards across all 22 microservices?**

## Decision Drivers

- **Coverage enforcement** — Coverage thresholds must be machine-enforced in CI, not advisory only
- **Cross-service safety** — 146 cross-service relationships (per CALM topology) require contract-level validation
- **Architecture traceability** — User story acceptance criteria must map to executable test scenarios
- **Tooling maturity** — Java microservices require a well-established, production-grade testing stack
- **Incremental adoption** — Standard must be adoptable per-service without disrupting the existing delivery practice
- **Minimal authoring overhead** — Contract tests should be auto-generated from existing OpenAPI specs where possible

## Considered Options

### Option A: TDD Only

Apply Test-Driven Development (red-green-refactor) at all test layers: unit, integration, contract, and acceptance.

| Aspect | Assessment |
|--------|-----------|
| Strengths | Consistent methodology across all layers; forces clean API design; immediate regression safety |
| Weaknesses | TDD at the acceptance layer is unnatural — Gherkin scenarios are not written test-first; user stories do not map cleanly to unit-style TDD |
| Contract testing | Manual — no automatic derivation from OpenAPI specs |
| Stakeholder readability | Low — JUnit tests are not readable by product owners or architects |

### Option B: BDD Only

Apply Behavior-Driven Development (Given/When/Then) at all test layers using Cucumber-JVM.

| Aspect | Assessment |
|--------|-----------|
| Strengths | Stakeholder-readable scenarios; direct traceability from user stories to tests |
| Weaknesses | BDD at the unit layer is overhead-heavy; step definitions for simple logic are boilerplate; slower feedback loop than JUnit |
| Contract testing | Indirect — possible but not the natural fit for Cucumber |
| Maintenance cost | High — Gherkin step definitions require ongoing synchronization with scenario text |

### Option C: Hybrid TDD and BDD (Recommended)

Apply TDD at unit and integration layers, BDD at the acceptance layer, and spec-driven generation at the contract layer.

| Layer | Methodology | Rationale |
|-------|-------------|-----------|
| Unit | TDD | Fast feedback; forces clean class-level design; natural fit for JUnit 5 |
| Integration | TDD | Validates data access and service composition with real databases |
| Contract | Spec-driven | Auto-generated from OpenAPI specs in `architecture/specs/`; no manual authoring |
| Acceptance | BDD | User stories produce Gherkin scenarios; acceptance criteria become executable |
| E2E | Scripted | Small set of critical path scripts; not TDD or BDD overhead |

## Decision Outcome

**Chosen option: Option C — Hybrid TDD and BDD**, because it applies the right methodology at each test layer, minimizes authoring overhead at each layer, and provides the strongest traceability path from OpenAPI specs through contract tests to user story acceptance criteria.

### Coverage Thresholds

Defined in `config/test-standards.yaml`:

| Metric | Minimum | Target | Enforcement |
|--------|---------|--------|-------------|
| Line coverage | 80% | 90% | CI gate — PR blocked |
| Branch coverage | 70% | 80% | CI gate — PR blocked |
| Mutation score | 60% | 75% | Advisory initially; promoted to gate in Phase D |
| Contract coverage | 100% of cross-service calls | 100% | CI gate — PR blocked |

### Tooling Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| Unit / Integration | JUnit 5, Mockito, AssertJ | Standard Java testing stack |
| Coverage | JaCoCo | Line, branch, instruction coverage |
| Mutation | PITest | Mutation testing — identifies weak assertions |
| Contract | Pact (preferred) | Consumer-driven contract testing |
| Acceptance | Cucumber-JVM | BDD scenario execution from Gherkin |
| E2E | REST Assured | HTTP-level critical path testing |

Contract tool selection (Pact vs Spring Cloud Contract) is addressed in the companion roadmap Phase B evaluation step.

### Solution Design Integration

Every solution design that touches service logic must include a test plan at `3.solution/g.guidance/test-plan.md` covering:

- Which test layers are affected (unit, integration, contract, acceptance)
- New test scenarios required
- Existing tests that need updating
- BDD scenarios derived from user stories (Gherkin format, where applicable)
- Contract test additions for new cross-service integrations

## Consequences

### Positive

- Coverage thresholds are enforced in CI, eliminating silent regression risk
- Every cross-service boundary in `architecture/metadata/cross-service-calls.yaml` has a corresponding contract test
- User story acceptance criteria become executable scenarios, closing the loop between architecture and delivery
- The 80% line coverage target already referenced in arc42 constraints is now enforced rather than aspirational

### Negative

- Initial setup effort: JaCoCo, PITest, Cucumber-JVM, and Pact integration across 22 service build files
- BDD step definition maintenance overhead when Gherkin scenarios change
- Pact Broker infrastructure required for contract test result storage and verification

### Neutral

- Existing services that already meet coverage thresholds are unaffected
- Adoption is incremental — new solutions apply the standard; existing services migrate progressively
- The mutation score gate starts advisory to allow calibration before enforcement
