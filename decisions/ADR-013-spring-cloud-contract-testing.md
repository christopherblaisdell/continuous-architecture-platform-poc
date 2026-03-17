# ADR-013: Select Spring Cloud Contract for Cross-Service Contract Testing

## Status

Accepted

## Date

2026-03-17

## Context and Problem Statement

NovaTrek Adventures maintains 19 microservices with 47 cross-service integration points documented in `architecture/metadata/cross-service-calls.yaml`. API contract changes introduced through solution designs can silently break downstream consumers. A contract testing strategy is needed to verify that provider API implementations match consumer expectations at every cross-service boundary, catching breaking changes before they reach production.

## Decision Drivers

- NovaTrek services use Spring Boot 3.3.5 with Gradle — the contract testing tool must integrate natively with the existing build pipeline
- OpenAPI specs in `architecture/specs/` are the authoritative API contracts — the tool should leverage these specs rather than requiring parallel contract definitions
- The team is small — the tool must minimize boilerplate and operational overhead (no separate broker infrastructure if avoidable)
- Contract tests must run in CI as a PR gate — fast execution is essential
- The solution must support both synchronous REST and asynchronous event contracts (NovaTrek uses Azure Service Bus for domain events)

## Considered Options

1. Pact (consumer-driven contracts with Pact Broker)
2. Spring Cloud Contract (provider-driven contracts with stub generation)
3. OpenAPI-driven validation only (Schemathesis / Spectral + custom assertions)

## Decision Outcome

**Chosen Option**: "Spring Cloud Contract", because it integrates natively with the Spring Boot and Gradle toolchain already in use, supports both REST and messaging contracts, generates executable stubs from provider contracts (avoiding the need for a separate Pact Broker), and aligns with the provider-first contract model where NovaTrek's OpenAPI specs define the authoritative contract shape.

### Confirmation

- Spring Cloud Contract verifier plugin added to the service build template
- Contract tests exist for all synchronous cross-service calls originating from svc-check-in (highest-traffic service)
- CI pipeline runs contract verification on every PR touching service code
- Contract stubs are published to a local Maven repository for consumer-side integration tests

## Consequences

### Positive

- Native Spring Boot integration — contracts written in Groovy DSL or YAML, verified as part of `./gradlew check`
- No external infrastructure required — stubs stored in local Maven repo or GitHub Packages (no Pact Broker to deploy and maintain)
- Provider-first model matches NovaTrek's architecture practice — OpenAPI specs define the contract, Spring Cloud Contract enforces it
- Generated WireMock stubs allow consumer services to test against realistic provider responses without running the provider
- Supports messaging contracts for Azure Service Bus event validation

### Negative

- Provider-first model means consumer teams must align to provider contracts — consumer-driven changes require coordination
- Groovy DSL or YAML contract files add a new artifact type to the repository
- Spring Cloud Contract version must stay aligned with Spring Boot BOM — version coupling

### Neutral

- Contract files live alongside the provider service in `src/test/resources/contracts/`
- Stub JAR artifacts follow Maven naming conventions (`{service}-stubs.jar`)
- Existing Testcontainers-based integration tests remain unchanged — contract tests are additive

## Pros and Cons of the Options

### Pact (Consumer-Driven Contracts)

Consumer services define expectations; provider services verify them against the Pact Broker.

- **Good**, because consumer-driven contracts catch provider changes that break actual consumer usage patterns
- **Good**, because Pact Broker provides a visual dashboard for contract compatibility
- **Good**, because language-agnostic — works across Java, Python, Node.js ecosystems
- **Bad**, because requires deploying and maintaining a Pact Broker (additional infrastructure cost and operational burden)
- **Bad**, because consumer-driven model conflicts with NovaTrek's provider-first architecture practice where OpenAPI specs are the source of truth
- **Neutral**, because Pact JVM integrates with JUnit 5 but requires separate consumer and provider test configurations

### Spring Cloud Contract

Provider services define contracts; consumers receive auto-generated stubs for integration testing.

- **Good**, because native Spring Boot and Gradle integration — contracts verified via `./gradlew contractTest`
- **Good**, because no external broker infrastructure — stubs published as Maven artifacts
- **Good**, because provider-first model aligns with NovaTrek's OpenAPI-driven architecture practice
- **Good**, because supports both REST (WireMock stubs) and messaging (Spring Cloud Stream) contracts
- **Bad**, because tightly coupled to Spring ecosystem — non-Spring consumers would need adapters
- **Neutral**, because contracts can be written in Groovy DSL, YAML, or Kotlin DSL

### OpenAPI-Driven Validation Only

Use OpenAPI specs directly with schema validation tools (Schemathesis, Spectral) without formal contract testing.

- **Good**, because leverages existing OpenAPI specs with zero new tooling
- **Good**, because Spectral linting catches schema issues at design time
- **Neutral**, because Schemathesis generates property-based API tests from specs automatically
- **Bad**, because validates schema shape only — does not verify business logic or response content
- **Bad**, because no consumer-side stub generation — consumers cannot test against realistic provider responses
- **Bad**, because no versioned contract history — breaking changes detected only when both services are running simultaneously

## More Information

- Cross-service integration map: `architecture/metadata/cross-service-calls.yaml` (47 integration points across 13 consumer services)
- OpenAPI specs: `architecture/specs/` (19 service specs)
- Test methodology ADR: `decisions/ADR-012-test-methodology-tdd-bdd-hybrid.md`
- Test standards config: `config/test-standards.yaml`
- Spring Cloud Contract docs: https://spring.io/projects/spring-cloud-contract
