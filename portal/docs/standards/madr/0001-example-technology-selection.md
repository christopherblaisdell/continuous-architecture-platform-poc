# ADR-0001: Choose REST Framework for Microservices

## Status

Accepted

## Date

2026-02-28

## Context and Problem Statement

Our platform is transitioning from a monolithic architecture to microservices. We need to select a standard JVM-based REST framework that all new microservices will use. The framework must support our operational requirements for high availability, observability, and cloud-native deployment on Kubernetes. Standardizing on a single framework reduces cognitive overhead and enables shared libraries.

## Decision Drivers

- Team expertise and existing skill set (predominantly Java/Spring developers)
- Ecosystem maturity and availability of production-grade libraries
- Startup time and memory footprint for containerized deployment
- Community size, documentation quality, and long-term viability
- Integration with existing CI/CD pipelines and observability stack (Datadog, ELK)
- Enterprise support availability

## Considered Options

1. Spring Boot 3.x
2. Quarkus 3.x
3. Micronaut 4.x

## Decision Outcome

**Chosen Option**: "Spring Boot 3.x", because it provides the best balance of team familiarity, ecosystem maturity, and enterprise support. While Quarkus and Micronaut offer better startup performance, the productivity gains from existing team expertise and the breadth of the Spring ecosystem outweigh the performance advantages for our use case.

### Confirmation

- First two microservices will be built with Spring Boot 3.x and deployed to staging
- Startup time and memory usage will be measured and documented
- Developer onboarding time for the new service template will be tracked
- Review after 6 months of production use

## Consequences

### Positive

- Minimal ramp-up time: 80% of the team already has Spring Boot experience
- Extensive ecosystem: Spring Security, Spring Data, Spring Cloud, Micrometer
- Strong enterprise support through VMware Tanzu
- Largest community and most comprehensive documentation

### Negative

- Higher memory footprint compared to Quarkus/Micronaut (typically 150-300MB vs 50-100MB)
- Slower cold start time, which affects scaling responsiveness
- GraalVM native compilation support exists but is less mature than Quarkus

### Neutral

- Spring Boot 3.x requires Java 17+, aligning with our JDK upgrade plan
- Virtual threads (Project Loom) support is available for reactive-style concurrency

## Pros and Cons of the Options

### Spring Boot 3.x

Spring Boot is the most widely adopted Java microservices framework, backed by VMware.

- **Good**, because the team has 5+ years of collective Spring Boot experience
- **Good**, because the ecosystem covers virtually every integration need (messaging, caching, security, data access)
- **Good**, because VMware offers commercial support and LTS releases
- **Good**, because Micrometer provides first-class Datadog and Prometheus integration
- **Neutral**, because Spring Boot 3.x requires Java 17 minimum
- **Bad**, because memory consumption is higher than alternatives (JVM overhead)
- **Bad**, because cold start time of 3-8 seconds is slower than Quarkus native

### Quarkus 3.x

Quarkus is a Kubernetes-native Java framework by Red Hat, optimized for GraalVM native images.

- **Good**, because native compilation produces sub-second startup times
- **Good**, because memory footprint is significantly lower (50-80MB native)
- **Good**, because it supports most popular Java libraries (Hibernate, RESTEasy, Vert.x)
- **Good**, because Red Hat provides enterprise support
- **Neutral**, because the developer experience is different from traditional Spring
- **Bad**, because team has no production Quarkus experience (estimated 4-6 week ramp-up)
- **Bad**, because the ecosystem is smaller, with fewer community extensions
- **Bad**, because native compilation has longer build times and some library restrictions

### Micronaut 4.x

Micronaut is a modern JVM framework using compile-time dependency injection.

- **Good**, because compile-time DI eliminates reflection overhead
- **Good**, because startup time and memory are competitive with Quarkus
- **Good**, because it has good GraalVM native image support
- **Neutral**, because documentation quality is adequate but less extensive than Spring
- **Bad**, because it has the smallest community of the three options
- **Bad**, because team has no Micronaut experience
- **Bad**, because enterprise support options are more limited (Object Computing)
- **Bad**, because fewer third-party integrations available out of the box

## More Information

- Spring Boot documentation: [https://docs.spring.io/spring-boot/docs/current/reference/html/](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- Quarkus guides: [https://quarkus.io/guides/](https://quarkus.io/guides/)
- Micronaut documentation: [https://docs.micronaut.io/latest/guide/](https://docs.micronaut.io/latest/guide/)
- Internal benchmark results: See `docs/spikes/framework-benchmark-2026Q1.md`
