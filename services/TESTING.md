# NovaTrek Services — Testing and Verification Guide

This document describes how to build, test, and verify all 22 NovaTrek microservices.

## Prerequisites

- **Java 21** (OpenJDK recommended)
- **Gradle 8.14** (each service bundles its own Gradle wrapper — no global install required)

## Quick Start — Build All Services

From the repository root:

```bash
for svc in services/svc-*/; do
  name=$(basename "$svc")
  if [[ "$name" == "svc-guest-profiles" || "$name" == "svc-trail-management" || "$name" == "svc-trip-catalog" ]]; then
    result=$(cd "$svc" && ./gradlew clean build 2>&1 | tail -1)
  else
    result=$(cd "$svc" && ./gradlew clean build -x dependencyCheckAnalyze 2>&1 | tail -1)
  fi
  echo "$name: $result"
done
```

All 22 services should report `BUILD SUCCESSFUL`.

> **Note:** Three services (`svc-guest-profiles`, `svc-trail-management`, `svc-trip-catalog`) do not have the OWASP dependency-check plugin and must be built without the `-x dependencyCheckAnalyze` flag.

## Build a Single Service

```bash
cd services/svc-check-in
./gradlew clean build -x dependencyCheckAnalyze
```

## Run Tests Only

```bash
cd services/svc-check-in
./gradlew test
```

## Test Architecture

Each service follows a consistent test pattern:

| Test Type | Location | Framework | Purpose |
|-----------|----------|-----------|---------|
| Controller tests | `src/test/java/.../controller/` | `@WebMvcTest` + MockMvc | API endpoint behavior, HTTP status codes, JSON responses |
| Entity tests | `src/test/java/.../entity/` | JUnit 5 | Getter/setter coverage, lifecycle callbacks, enum validation |
| Repository tests | `src/test/java/.../repository/` | `@DataJpaTest` | JPA queries against H2 in-memory database |

### Controller Tests

Each controller test class uses `@WebMvcTest` with `@MockBean` for repository dependencies. Tests cover:

- **GET endpoints**: Empty list, populated list, filtering, not-found (404)
- **POST endpoints**: Successful creation with JSON body
- **PATCH endpoints**: All fields populated (true branch), empty body (false branch), not-found (404)
- **Unimplemented endpoints**: `assertThrows(ServletException.class, ...)` for methods that throw `UnsupportedOperationException`

### Entity Tests

Entity tests exercise:

- All getters and setters with assertEquals assertions
- JPA lifecycle callbacks (`@PrePersist` / `@PreUpdate`) setting `createdAt` and `updatedAt`
- Enum `values()` and `valueOf()` coverage

### Repository Tests

Repository tests use `@DataJpaTest` with an H2 in-memory database and verify custom query methods.

## JaCoCo Coverage Gates

All services enforce coverage gates via JaCoCo:

| Metric | Minimum |
|--------|---------|
| Line coverage | 80% |
| Branch coverage | 70% |

Coverage reports are generated at:

```
services/svc-{name}/build/reports/jacoco/test/html/index.html
```

To view a coverage report:

```bash
open services/svc-check-in/build/reports/jacoco/test/html/index.html
```

## Service Inventory

| Wave | Service | Domain | Test Classes |
|------|---------|--------|-------------|
| 1 | svc-guest-profiles | Guest Identity | Controller |
| 1 | svc-trip-catalog | Product Catalog | Controller |
| 1 | svc-trail-management | Product Catalog | Controller |
| 2 | svc-reservations | Booking | Controller, Entity |
| 2 | svc-check-in | Operations | Controller, Entity |
| 2 | svc-notifications | Support | Controller |
| 3 | svc-payments | Support | Controller, Entity |
| 3 | svc-gear-inventory | Logistics | Controller, Entity |
| 3 | svc-safety-compliance | Safety | Controller |
| 4 | svc-guide-management | Guide Management | Controller, Entity |
| 4 | svc-transport-logistics | Logistics | Controller |
| 4 | svc-location-services | Support | Controller |
| 5 | svc-analytics | Support | Controller |
| 5 | svc-loyalty-rewards | Support | Controller, Entity |
| 5 | svc-media-gallery | Support | Controller |
| 6 | svc-partner-integrations | External | Controller |
| 6 | svc-weather | Support | Controller |
| 6 | svc-inventory-procurement | Logistics | Controller, Entity |
| 6 | svc-emergency-response | Support | Controller, Entity |
| 6 | svc-wildlife-tracking | Support | Controller |
| 6 | svc-scheduling-orchestrator | Operations | Controller, Entity |
| 7 | svc-reviews | Guest Experience | Controller, Repository, Entity |

## Troubleshooting

### Build fails on `copyContracts`

All services have `failOnNoContracts = false` in their `contracts {}` block. If a new service is added without this setting, the build will fail with a `copyContracts` error.

### JaCoCo coverage too low

Check the HTML coverage report to identify uncovered classes. Common gaps:

- Entity classes without getter/setter tests — add an entity test class
- PATCH methods with `if (body.getField() != null)` branches — add tests with both full body and empty body
- Application main class — excluded from some services but may still count

### `UnsupportedOperationException` in test

Spring's `@WebMvcTest` wraps `UnsupportedOperationException` in `jakarta.servlet.ServletException`. Use `assertThrows(jakarta.servlet.ServletException.class, ...)` instead of asserting HTTP 500 status.

### OWASP dependency-check timeout

Three services lack the OWASP plugin. For the 19 services that have it, use `-x dependencyCheckAnalyze` to skip dependency analysis during local builds. CI runs the full analysis.
