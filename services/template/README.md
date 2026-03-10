# NovaTrek Adventures — Service Template

This directory contains the template for bootstrapping any of the 22 NovaTrek microservices. Copy this template and customize for each service.

## Usage

```bash
# Copy template for a new service
cp -r services/template services/svc-my-service

# Update service name in build.gradle.kts and application.yaml
# Create Flyway baseline migration for the service schema
# Create per-service CI workflow from the example
```

## Contents

| File | Purpose |
|------|---------|
| `build.gradle.kts` | Gradle build with Spring Boot 3, Java 21, all standard dependencies |
| `Dockerfile` | Multi-stage build: JDK build → JRE distroless runtime |
| `src/main/resources/application.yaml` | Shared config (all environments) |
| `src/main/resources/application-dev.yaml` | Dev environment overrides |
| `src/main/resources/application-prod.yaml` | Production overrides |
| `src/main/resources/application-local.yaml` | Local development (Docker Compose) |
| `src/main/resources/db/migration/V1__baseline.sql` | Flyway baseline migration template |

## Spring Boot Dependencies (standard for all services)

- **Spring Web** — REST controllers
- **Spring Data JPA** — Database access
- **Flyway** — Database migrations
- **Spring Boot Actuator** — Health checks, metrics
- **Micrometer + OpenTelemetry** — Distributed tracing
- **Spring Cloud Azure Key Vault** — Secret management
- **Spring Cloud Azure Service Bus** — Event pub/sub
- **Resilience4j** — Circuit breakers, retries
- **Logback JSON** — Structured JSON logging
