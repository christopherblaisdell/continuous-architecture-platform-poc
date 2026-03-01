# 2. Architecture Constraints

> **Help**: Any requirement that constrains software architects in their freedom of design and implementation decisions or decisions about the development process. These constraints sometimes go beyond individual systems and are valid for whole organizations and companies.
>
> **Motivation**: Architects should know exactly where they are free in their design decisions and where they must adhere to constraints. Constraints must always be dealt with; they may be negotiable, though.
>
> **Form**: Simple tables of constraints with explanations. If needed, you can subdivide them into technical constraints, organizational and political constraints, and conventions.

---

## 2.1 Technical Constraints

> **Help**: List technical constraints here such as required operating systems, hardware, middleware, programming languages, frameworks, libraries, or specific versions of these.

| ID | Constraint | Description / Background |
|----|-----------|--------------------------|
| TC-01 | _\<e.g., Programming Language\>_ | _\<Must be implemented in Java 17+ due to corporate standard\>_ |
| TC-02 | _\<e.g., Operating System\>_ | _\<Must run on Linux (RHEL 8+) in production\>_ |
| TC-03 | _\<e.g., Database\>_ | _\<Must use PostgreSQL as the primary data store\>_ |
| TC-04 | _\<e.g., Cloud Provider\>_ | _\<Must be deployed on AWS (corporate cloud platform)\>_ |
| TC-05 | _\<e.g., API Standard\>_ | _\<All APIs must follow REST conventions and OpenAPI 3.0 spec\>_ |
| TC-06 | _\<e.g., Container Runtime\>_ | _\<Must be containerized with Docker / deployed via Kubernetes\>_ |
| TC-07 | _\<e.g., Browser Support\>_ | _\<Must support latest two versions of Chrome, Firefox, Safari, Edge\>_ |

---

## 2.2 Organizational Constraints

> **Help**: List organizational constraints such as team structure, schedule, budget, development process, or standards that the organization mandates.

| ID | Constraint | Description / Background |
|----|-----------|--------------------------|
| OC-01 | _\<e.g., Team Structure\>_ | _\<Development is distributed across two teams in different time zones\>_ |
| OC-02 | _\<e.g., Schedule\>_ | _\<MVP must be delivered by Q3 2026\>_ |
| OC-03 | _\<e.g., Budget\>_ | _\<Total infrastructure budget limited to $X/month\>_ |
| OC-04 | _\<e.g., Development Process\>_ | _\<Must follow SAFe agile methodology with 2-week sprints\>_ |
| OC-05 | _\<e.g., Approval Process\>_ | _\<Architecture decisions require Architecture Review Board approval\>_ |
| OC-06 | _\<e.g., Version Control\>_ | _\<All code must be managed in GitLab with merge request reviews\>_ |

---

## 2.3 Conventions

> **Help**: List conventions the team has agreed upon or that are mandated by the organization. These can include coding standards, documentation requirements, naming conventions, or architectural patterns.

| ID | Convention | Description / Background |
|----|-----------|--------------------------|
| CV-01 | _\<e.g., Coding Standards\>_ | _\<Follow corporate coding guidelines (link to standard)\>_ |
| CV-02 | _\<e.g., Architecture Documentation\>_ | _\<Use arc42 template for all architecture documentation\>_ |
| CV-03 | _\<e.g., Naming Conventions\>_ | _\<Services follow the pattern svc-{domain}-{function}\>_ |
| CV-04 | _\<e.g., Testing Standards\>_ | _\<Minimum 80% unit test coverage required for all services\>_ |
| CV-05 | _\<e.g., API Versioning\>_ | _\<APIs must be versioned using URL path versioning (e.g., /v1/)\>_ |
| CV-06 | _\<e.g., Logging\>_ | _\<Structured JSON logging with correlation IDs is mandatory\>_ |
| CV-07 | _\<e.g., Security\>_ | _\<OWASP Top 10 compliance required for all web-facing services\>_ |

---

> Based on the arc42 architecture template (https://arc42.org).  
> Created by Dr. Peter Hruschka and Dr. Gernot Starke.  
> Licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
