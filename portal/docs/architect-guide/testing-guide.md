# Testing Guide

This page covers how architecture drives test design at NovaTrek. Architects do not write tests, but they produce the artifacts that tests are derived from.

---

## Test Methodology Overview

NovaTrek uses a hybrid TDD/BDD approach (ADR-012) with four distinct test layers:

| Layer | Method | Written By | Derived From | Framework |
|-------|--------|-----------|--------------|-----------|
| **Unit tests** | TDD | Developer | Implementation logic | JUnit 5 + AssertJ |
| **Integration tests** | TDD | Developer | Data store interactions | JUnit 5 + Testcontainers |
| **Contract tests** | Spec-driven | Generated | OpenAPI specs | Spring Cloud Contract |
| **Acceptance tests** | BDD | Developer | User story acceptance criteria | Cucumber-JVM |

### What the Architect Influences

- **User stories** with acceptance criteria -> drive BDD scenarios
- **OpenAPI specs** -> drive contract test generation
- **Data store schemas** (`data-stores.yaml`) -> inform integration test scope
- **Test standards** (`config/test-standards.yaml`) -> define coverage thresholds and conventions

---

## BDD: From User Stories to Test Scenarios

### The Architect's Output

When you write user stories in `3.solution/u.user.stories/`, include specific acceptance criteria:

```
As a guest arriving for a rock climbing adventure
I want to check in with my reservation
So that the operations team can verify my waiver and assign safety gear

Acceptance Criteria:
1. Guest provides reservation ID and is identified
2. System verifies an active waiver exists for the adventure category
3. If no waiver exists, check-in is blocked with a clear error message
4. If waiver is valid, check-in proceeds and gear verification is initiated
```

### The Developer's Translation

Each acceptance criterion becomes one or more Gherkin scenarios:

```gherkin
Feature: Rock Climbing Check-In

  Scenario: Successful check-in with valid waiver
    Given a guest "Alex Rivera" with guest ID "guest-001"
    And a confirmed reservation "res-5001" for trip "trip-100"
    And the trip "trip-100" has adventure category "rock_climbing"
    And the guest has an active waiver for "rock_climbing"
    When the guest checks in with reservation "res-5001"
    Then the check-in is created successfully
    And gear verification is initiated

  Scenario: Check-in blocked without waiver
    Given a guest "Alex Rivera" with guest ID "guest-001"
    And a confirmed reservation "res-5001" for trip "trip-100"
    And the trip "trip-100" has adventure category "rock_climbing"
    And the guest does not have an active waiver
    When the guest checks in with reservation "res-5001"
    Then the check-in is rejected
    And the error message contains "active waiver required"
```

### Quality Rules for Acceptance Criteria

Write acceptance criteria that translate cleanly to BDD scenarios:

- **Use business language**, not technical language. Say "check-in is blocked" not "API returns 403"
- **Be specific about outcomes**. Say "error message contains 'active waiver required'" not "an error is shown"
- **Cover the happy path AND failure paths**. Every acceptance criterion should have at least one positive and one negative scenario
- **Keep criteria independent**. Each criterion should be testable in isolation

### BDD File Organization

Developers organize feature files by business capability:

```
src/test/resources/features/
  check-in.feature           # One feature file per capability
  reservation.feature
  guest-profile.feature
  safety-compliance.feature
```

### Tagging Strategy

| Tag | Purpose | Runs |
|-----|---------|------|
| `@smoke` | Critical path scenarios | Every commit |
| `@regression` | Full regression | Every PR |
| `@wip` | Work in progress | Excluded from CI |
| `@slow` | Performance-sensitive | Nightly only |

---

## Contract Testing (ADR-013)

### How Architecture Drives Contract Tests

1. **You write the OpenAPI spec** — this is the contract
2. **Spring Cloud Contract auto-generates tests** from the spec
3. **Producer tests** verify the service correctly implements the contract
4. **Consumer stubs** verify consumers correctly call the API
5. **CI catches drift** before it reaches production

### What This Means for Your Spec Work

Every change to an OpenAPI spec triggers contract test regeneration. If you add a required field to a response, the producer's contract test will fail until the developer adds it. If you remove a field, consumer stubs will fail until those consumers update.

This is intentional — the contract is enforced, not advisory.

---

## Test Standards Configuration

Test standards are centralized in `config/test-standards.yaml`:

- Coverage thresholds per test layer
- Tooling versions (JUnit, Cucumber, Testcontainers)
- Naming conventions for test classes and feature files
- Exclusion rules (what doesn't need tests)

As an architect, you may propose changes to test standards. Update the YAML and create an ADR if the change is significant.

---

## How Tests Map to Solution Design Components

When creating a solution design, consider the test implications for each component:

| Solution Component | Generates Tests |
|-------------------|----------------|
| New API endpoint | Contract test (auto-generated from spec) |
| Modified request schema | Contract test update (auto-generated) |
| New user story | BDD acceptance scenario (developer writes) |
| New database table | Integration test (developer writes) |
| New cross-service call | Contract test for both producer and consumer |
| New event | AsyncAPI contract test (auto-generated) |

You do not need to write a test plan in the solution design. The test coverage is implicit in the artifacts you produce:

- OpenAPI spec changes -> contract tests
- User story acceptance criteria -> BDD scenarios
- Data store changes -> integration tests

---

## Running Tests

Developers run tests with:

```bash
# All tests
./gradlew test

# BDD scenarios only
./gradlew test --tests "com.novatrek.CucumberSuiteTest"

# Specific feature file
./gradlew test -Dcucumber.features=src/test/resources/features/check-in.feature
```

---

## Reference

- [ADR-012: TDD/BDD Hybrid](../decisions/ADR-012-test-methodology-tdd-bdd-hybrid.md) — why this methodology
- [ADR-013: Spring Cloud Contract](../decisions/ADR-013-spring-cloud-contract-testing.md) — contract testing decision
- `config/test-standards.yaml` — coverage thresholds and conventions
