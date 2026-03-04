# 12. Glossary

> **Help**: The most important domain and technical terms that your stakeholders use when discussing the system.
>
> You can also see the glossary as a source for translations if you work in multi-language teams.
>
> **Motivation**: You should clearly define your terms so that all stakeholders:
> - Have an identical understanding of these terms
> - Do not use synonyms and homonyms
> - Can communicate effectively without misunderstanding
>
> **Form**: A table with columns for Term and Definition. Potentially more columns for translations into other languages and for references to definitions in external resources.
>
> **Tips**:
> - Keep the glossary sorted alphabetically
> - Include both domain-specific and technical terms
> - Reference authoritative sources where applicable
> - Update the glossary as new terms emerge during the project
> - Consider creating separate sections for domain terms and technical terms

---

## Domain Terms

| Term | Definition | Synonyms | Reference |
|------|-----------|----------|-----------|
| _\<Term A\>_ | _\<Clear, concise definition of this domain term\>_ | _\<Any synonyms used\>_ | _\<Link to authoritative source\>_ |
| _\<Term B\>_ | _\<Clear, concise definition of this domain term\>_ | _\<Any synonyms used\>_ | _\<Link to authoritative source\>_ |
| _\<Term C\>_ | _\<Clear, concise definition of this domain term\>_ | _\<Any synonyms used\>_ | _\<Link to authoritative source\>_ |
| _\<Term D\>_ | _\<Clear, concise definition of this domain term\>_ | _\<Any synonyms used\>_ | _\<Link to authoritative source\>_ |
| _\<Term E\>_ | _\<Clear, concise definition of this domain term\>_ | _\<Any synonyms used\>_ | _\<Link to authoritative source\>_ |

---

## Technical Terms

| Term | Definition | Context |
|------|-----------|---------|
| _\<ADR\>_ | _\<Architecture Decision Record - a document capturing an important architectural decision along with its context and consequences\>_ | _\<Section 9\>_ |
| _\<API Gateway\>_ | _\<A server that acts as a single entry point for API requests, providing cross-cutting concerns like authentication, rate limiting, and routing\>_ | _\<Section 5, 7\>_ |
| _\<ATAM\>_ | _\<Architecture Tradeoff Analysis Method - a systematic approach for evaluating software architectures relative to quality attribute goals\>_ | _\<Section 10\>_ |
| _\<Bounded Context\>_ | _\<A central pattern in Domain-Driven Design that defines the boundary within which a particular domain model is defined and applicable\>_ | _\<Section 8\>_ |
| _\<Circuit Breaker\>_ | _\<A design pattern that prevents cascading failures by monitoring for failures and temporarily stopping calls to a failing service\>_ | _\<Section 6, 8\>_ |
| _\<CQRS\>_ | _\<Command Query Responsibility Segregation - a pattern that separates read and write operations into different models\>_ | _\<Section 4\>_ |
| _\<Event Sourcing\>_ | _\<A pattern where state changes are stored as a sequence of events, allowing reconstruction of state at any point in time\>_ | _\<Section 4, 8\>_ |
| _\<HPA\>_ | _\<Horizontal Pod Autoscaler - a Kubernetes resource that automatically scales the number of pods based on observed metrics\>_ | _\<Section 7\>_ |
| _\<ISO 25010\>_ | _\<International standard for software product quality models, defining quality characteristics like performance, security, and maintainability\>_ | _\<Section 10\>_ |
| _\<RPO\>_ | _\<Recovery Point Objective - the maximum acceptable amount of data loss measured in time\>_ | _\<Section 10\>_ |
| _\<RTO\>_ | _\<Recovery Time Objective - the maximum acceptable duration of time to restore a system after a disruption\>_ | _\<Section 10\>_ |
| _\<SLA\>_ | _\<Service Level Agreement - a formal agreement defining the expected level of service\>_ | _\<Section 7, 10\>_ |

---

## Abbreviations

| Abbreviation | Full Form |
|-------------|-----------|
| _\<API\>_ | _\<Application Programming Interface\>_ |
| _\<CI/CD\>_ | _\<Continuous Integration / Continuous Delivery\>_ |
| _\<DDD\>_ | _\<Domain-Driven Design\>_ |
| _\<HA\>_ | _\<High Availability\>_ |
| _\<IaC\>_ | _\<Infrastructure as Code\>_ |
| _\<JWT\>_ | _\<JSON Web Token\>_ |
| _\<K8s\>_ | _\<Kubernetes\>_ |
| _\<OIDC\>_ | _\<OpenID Connect\>_ |
| _\<PII\>_ | _\<Personally Identifiable Information\>_ |
| _\<RBAC\>_ | _\<Role-Based Access Control\>_ |
| _\<REST\>_ | _\<Representational State Transfer\>_ |
| _\<TLS\>_ | _\<Transport Layer Security\>_ |

---

> Based on the arc42 architecture template (https://arc42.org).  
> Created by Dr. Peter Hruschka and Dr. Gernot Starke.  
> Licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
