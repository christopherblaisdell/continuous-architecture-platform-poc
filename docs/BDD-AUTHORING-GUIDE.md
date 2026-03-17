# BDD Authoring Guide for NovaTrek Services

This guide covers how to write, organize, and maintain BDD (Behavior-Driven Development) scenarios for NovaTrek microservices using Cucumber-JVM.

## When to Write BDD Scenarios

BDD scenarios are written for **acceptance-level testing** — validating that user stories produce the correct business outcomes. They are derived directly from user story acceptance criteria in solution designs.

| Test Layer | Use BDD? | Use Instead |
|-----------|----------|-------------|
| Unit tests | No | JUnit 5 + AssertJ (TDD) |
| Integration tests | No | JUnit 5 + Testcontainers (TDD) |
| Contract tests | No | Spring Cloud Contract (spec-driven) |
| Acceptance tests | **Yes** | Cucumber-JVM (BDD) |
| E2E tests | No | Scripted test suites |

## From User Story to Gherkin

### Step 1: Identify the acceptance criteria

From a solution design user story:

> **As a** guest arriving for a rock climbing adventure  
> **I want to** check in with my reservation  
> **So that** the operations team can verify my waiver and assign safety gear
>
> **Acceptance Criteria:**
> 1. Guest provides reservation ID and is identified
> 2. System verifies an active waiver exists for the adventure category
> 3. If no waiver exists, check-in is blocked with a clear error message
> 4. If waiver is valid, check-in proceeds and gear verification is initiated

### Step 2: Translate to Gherkin scenarios

Each acceptance criterion becomes one or more scenarios:

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

### Step 3: Use Background for shared setup

When multiple scenarios share the same preconditions, use `Background`:

```gherkin
Feature: Guest Check-In

  Background:
    Given a guest "Alex Rivera" with guest ID "guest-001"
    And a confirmed reservation "res-5001" for trip "trip-100"

  Scenario: Successful check-in
    # ...build on shared preconditions

  Scenario: Failed check-in
    # ...build on shared preconditions
```

## File Organization

```
src/test/resources/features/
  check-in.feature              # One feature file per business capability
  reservation.feature
  guest-profile.feature
  safety-compliance.feature

src/test/java/com/novatrek/steps/
  CommonSteps.java              # Shared steps (guest identity, reservations, assertions)
  CheckInSteps.java             # Service-specific steps for svc-check-in
  ReservationSteps.java         # Service-specific steps for svc-reservations
```

## Writing Good Steps

### Do

- Write steps in **business language**, not technical language
- Keep steps **reusable** — parameterize with `{string}`, `{int}`, etc.
- Use `assertThat()` (AssertJ) for clear assertion messages
- Match step definitions to the domain vocabulary (guest, reservation, trip, waiver)

### Do Not

- Do not reference HTTP status codes, database tables, or JSON field names in Gherkin
- Do not create one-off step definitions — look for existing steps first
- Do not test implementation details (internal method calls, SQL queries)
- Do not use Scenario Outlines for trivially different cases — use separate scenarios for clarity

### Example: Good vs Bad Steps

```gherkin
# Good — business language
Given the guest has an active waiver for "rock_climbing"
When the guest checks in with reservation "res-5001"
Then the check-in is created successfully

# Bad — technical language
Given the database has a waiver row with category_code "rock_climbing" and status "ACTIVE"
When a POST is sent to /check-ins with body {"reservation_id": "res-5001"}
Then the response status is 201 and body contains "check_in_id"
```

## Running BDD Tests

```bash
# Run all BDD scenarios
./gradlew test --tests "com.novatrek.CucumberSuiteTest"

# Run specific feature file
./gradlew test -Dcucumber.features=src/test/resources/features/check-in.feature

# Run with specific tag
./gradlew test -Dcucumber.filter.tags="@smoke"
```

## Integration with CI

BDD scenarios run as part of the standard `./gradlew test` task. The Cucumber JUnit Platform engine discovers and executes all feature files automatically. Reports are generated at `build/reports/cucumber/`.

## Tagging Strategy

Use tags to categorize scenarios for selective execution:

| Tag | Purpose |
|-----|---------|
| `@smoke` | Critical path scenarios — run on every commit |
| `@regression` | Full regression — run on PR |
| `@wip` | Work in progress — excluded from CI |
| `@slow` | Performance-sensitive — run nightly only |

## Related Documents

- ADR-012: Test Methodology (TDD/BDD Hybrid)
- `config/test-standards.yaml`: Coverage thresholds and tooling standards
- Solution design template: Test Plan section maps user stories to BDD scenarios
- `services/template/src/test/resources/features/`: Example feature files
