---
tags:
  - reference
  - technology
---

# Technology Stack

This page defines the standard technologies used across NovaTrek Adventures microservices and platform infrastructure.

---

## Application Runtime

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Java** | 21 (LTS) | Primary language for all microservices |
| **Spring Boot** | 3.3.5 | Web framework, dependency injection, auto-configuration |
| **Spring Data JPA** | (via Spring Boot) | Object-relational mapping and repository abstraction |
| **Gradle** | 8.x (Kotlin DSL) | Build system — all services use `build.gradle.kts` |
| **Flyway** | (via Spring Boot) | Database schema migrations — versioned SQL scripts |
| **Resilience4j** | 2.2.0 | Circuit breaker, retry, rate limiter, bulkhead patterns |

### Spring Boot

Spring Boot is the application framework for all NovaTrek microservices. It provides:

- **Embedded web server** — each service runs as a self-contained JAR with an embedded Tomcat server; no external application server required
- **Auto-configuration** — convention-over-configuration wiring for data sources, JPA, security, health checks, and metrics
- **Actuator endpoints** — standardized `/actuator/health`, `/actuator/info`, and `/actuator/metrics` endpoints used by Azure Container Apps health probes
- **Dependency injection** — constructor-based injection via Spring's IoC container
- **Profile-based configuration** — `application.yml` with environment-specific overrides (`application-dev.yml`, `application-prod.yml`)

Each service follows the standard Spring Boot project layout:

```
services/svc-{name}/
├── build.gradle.kts              # Dependencies, plugins, versions
├── Dockerfile                    # Multi-stage build → distroless JRE runtime
└── src/
    └── main/
        ├── java/.../
        │   ├── controller/       # REST endpoints (@RestController)
        │   ├── service/          # Business logic (@Service)
        │   ├── repository/       # Data access (@Repository, Spring Data JPA)
        │   ├── model/            # JPA entities (@Entity)
        │   ├── dto/              # Request/response DTOs
        │   └── config/           # Spring configuration (@Configuration)
        └── resources/
            ├── application.yml   # Spring Boot configuration
            └── db/migration/     # Flyway SQL migrations (V1__, V2__, ...)
```

---

## Data Persistence

| Technology | Version | Services | Purpose |
|-----------|---------|----------|---------|
| **PostgreSQL** | 15 | All 19 services | Primary relational database |
| **PostGIS** | (PostgreSQL extension) | svc-location-services, svc-wildlife-tracking | Geospatial queries and spatial indexing |
| **Valkey** | 8 | svc-trip-catalog, svc-scheduling-orchestrator, svc-notifications | In-memory cache layer |

Each service owns its own PostgreSQL database schema — no shared databases between services. Schema migrations are managed by Flyway with versioned SQL scripts.

**Hosting:** Azure Database for PostgreSQL Flexible Server with continuous WAL archiving and 7-day point-in-time recovery.

---

## Messaging and Events

| Technology | Purpose |
|-----------|---------|
| **Apache Kafka** | Asynchronous event-driven integration between services |
| **Azure Service Bus** | Queue-based messaging for specific workflows |

Event schemas are defined in [AsyncAPI specifications](../events/index.md) under `architecture/events/`. Services publish domain events (e.g., `checkin.completed`, `reservation.confirmed`) that other services consume without direct coupling.

---

## Containerization and Deployment

| Technology | Purpose |
|-----------|---------|
| **Docker** | Multi-stage builds producing distroless JRE runtime images |
| **Azure Container Apps** | Managed container orchestration (no Kubernetes management overhead) |
| **Azure Container Registry** | Private Docker image registry (`crnovatrekdev`, `crnovatrekprod`) |

Container Apps provides automatic scaling (0-2 replicas for dev, configurable for prod), built-in health probes against Spring Boot Actuator endpoints, and zero-downtime rolling deployments.

---

## Observability

| Technology | Purpose |
|-----------|---------|
| **OpenTelemetry** | Distributed tracing and metrics collection |
| **Micrometer** | Application metrics (via Spring Boot Actuator) |
| **Logstash Logback Encoder** | Structured JSON logging for all services |
| **Azure Application Insights** | Application performance monitoring (APM) |
| **Azure Log Analytics** | Centralized log aggregation and querying |

All services emit structured JSON logs and OpenTelemetry traces. Application Insights provides end-to-end request tracing across service boundaries.

---

## Infrastructure as Code

| Technology | Purpose |
|-----------|---------|
| **Bicep** | Azure resource provisioning (all infrastructure defined in `infra/`) |
| **GitHub Actions** | CI/CD pipeline orchestration (14 workflows) |
| **GitHub Secrets** | Credential management for deployments |

See [Platform Operations](platform-operations.md) for the full pipeline inventory and deployment flows.

---

## Security and Quality

| Technology | Purpose |
|-----------|---------|
| **OWASP Dependency Check** | CVE scanning of all Gradle dependencies in CI |
| **Trivy** | Container image vulnerability scanning in CI |
| **TestContainers** | Integration testing with disposable PostgreSQL containers |
| **Azure Key Vault** | Runtime secrets management (connection strings, API keys) |
| **Azure Managed Identity** | Passwordless authentication between Azure resources |

---

## Documentation and Architecture

| Technology | Purpose |
|-----------|---------|
| **MkDocs Material** | Architecture portal and presentation sites |
| **PlantUML** | C4 context diagrams, sequence diagrams, ERD diagrams |
| **Excalidraw** | UI/UX wireframes for applications |
| **OpenAPI 3.0** | REST API contract definitions for all services |
| **AsyncAPI 2.6** | Event schema definitions for Kafka topics |
| **YAML** | Architecture metadata (capabilities, data stores, cross-service calls, events) |
