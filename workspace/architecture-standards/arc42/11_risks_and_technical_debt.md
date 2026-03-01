# 11. Risks and Technical Debt

> **Help**: A list of identified technical risks or technical debts, ordered by priority. The term "risk management" is already used in project management (a]though often with different focus). In our context, we highlight risks and technical debt related to architecture and development.
>
> **Motivation**: "Risk management is project management for grown-ups" (Tim Lister, Atlantic Systems Guild).
>
> This should be your wake-up call: What could go wrong? What keeps you awake at night? What could derail the project or make the architecture fail? Documenting risks and technical debt is the first step toward managing them.
>
> **Form**: List of risks and/or technical debt, probably including suggested measures to minimize, mitigate, or avoid risks, or reduce technical debt.

---

## 11.1 Risks

> **Help**: Identify and document technical risks that could threaten the success of the project or the quality of the architecture. For each risk, assess likelihood and impact, and propose mitigation strategies.

| ID | Risk | Likelihood | Impact | Mitigation Strategy | Owner | Status |
|----|------|-----------|--------|---------------------|-------|--------|
| R-01 | _\<e.g., Third-party API becomes unavailable\>_ | _\<Medium\>_ | _\<High\>_ | _\<Implement circuit breaker, cache responses, define SLA with provider\>_ | _\<Architect\>_ | _\<Open\>_ |
| R-02 | _\<e.g., Performance degrades under peak load\>_ | _\<Medium\>_ | _\<High\>_ | _\<Load testing, auto-scaling, caching strategy\>_ | _\<Tech Lead\>_ | _\<Open\>_ |
| R-03 | _\<e.g., Key team member leaves\>_ | _\<Low\>_ | _\<High\>_ | _\<Knowledge sharing, documentation, pair programming\>_ | _\<Manager\>_ | _\<Open\>_ |
| R-04 | _\<e.g., Security vulnerability in dependencies\>_ | _\<High\>_ | _\<High\>_ | _\<Automated dependency scanning, regular updates\>_ | _\<Security Lead\>_ | _\<Open\>_ |
| R-05 | _\<e.g., Data migration fails\>_ | _\<Low\>_ | _\<Critical\>_ | _\<Rehearsal migrations, rollback plan, data validation\>_ | _\<Data Engineer\>_ | _\<Open\>_ |
| R-06 | _\<e.g., Cloud provider lock-in\>_ | _\<Medium\>_ | _\<Medium\>_ | _\<Abstract cloud services behind interfaces, use Terraform\>_ | _\<Architect\>_ | _\<Open\>_ |

### Risk Matrix

```
                    Impact
                Low    Medium    High    Critical
Likelihood  ┌────────┬─────────┬────────┬──────────┐
            │        │         │        │          │
  High      │        │         │ R-04   │          │
            │        │         │        │          │
  Medium    │        │ R-06    │ R-01   │          │
            │        │         │ R-02   │          │
  Low       │        │         │ R-03   │ R-05     │
            │        │         │        │          │
            └────────┴─────────┴────────┴──────────┘
```

---

## 11.2 Technical Debt

> **Help**: Document known technical debt -- shortcuts, workarounds, or suboptimal solutions that were accepted for pragmatic reasons but should be addressed in the future. Track the reason the debt was incurred, its impact, and a plan for resolution.

| ID | Description | Category | Incurred Date | Reason | Impact | Remediation Plan | Priority | Estimated Effort |
|----|------------|----------|---------------|--------|--------|-----------------|----------|-----------------|
| TD-01 | _\<e.g., Shared database between Service A and Service B\>_ | _\<Architecture\>_ | _\<YYYY-MM-DD\>_ | _\<Timeline pressure for MVP\>_ | _\<Tight coupling, deployment dependency\>_ | _\<Introduce API layer, migrate to separate databases\>_ | _\<High\>_ | _\<3 sprints\>_ |
| TD-02 | _\<e.g., Missing integration tests for payment flow\>_ | _\<Testing\>_ | _\<YYYY-MM-DD\>_ | _\<Team capacity\>_ | _\<Regression risk in critical path\>_ | _\<Add Testcontainers-based integration tests\>_ | _\<High\>_ | _\<1 sprint\>_ |
| TD-03 | _\<e.g., Hardcoded configuration values\>_ | _\<Code Quality\>_ | _\<YYYY-MM-DD\>_ | _\<Prototype carried to production\>_ | _\<Deployment inflexibility\>_ | _\<Move to config service / environment variables\>_ | _\<Medium\>_ | _\<0.5 sprint\>_ |
| TD-04 | _\<e.g., No structured logging in legacy service\>_ | _\<Observability\>_ | _\<YYYY-MM-DD\>_ | _\<Legacy codebase\>_ | _\<Difficult debugging, no correlation\>_ | _\<Implement structured JSON logging\>_ | _\<Medium\>_ | _\<1 sprint\>_ |
| TD-05 | _\<e.g., Outdated API documentation\>_ | _\<Documentation\>_ | _\<YYYY-MM-DD\>_ | _\<Documentation not in CI pipeline\>_ | _\<Developer confusion, integration errors\>_ | _\<Generate docs from OpenAPI specs in CI\>_ | _\<Low\>_ | _\<0.5 sprint\>_ |

### Technical Debt Categories

| Category | Description | Examples |
|----------|-------------|---------|
| **Architecture** | Structural issues in system design | Tight coupling, missing abstractions, shared databases |
| **Code Quality** | Code-level issues affecting maintainability | Duplication, complexity, lack of patterns |
| **Testing** | Gaps in test coverage or test quality | Missing tests, flaky tests, no performance tests |
| **Infrastructure** | Issues in deployment, CI/CD, or operations | Manual deployments, missing monitoring, no IaC |
| **Documentation** | Missing or outdated documentation | Stale API docs, missing runbooks, no onboarding guide |
| **Security** | Known security gaps or compliance issues | Unpatched dependencies, weak authentication |
| **Observability** | Gaps in monitoring, logging, or tracing | No distributed tracing, unstructured logs |

---

## 11.3 Tracking and Review

> **Help**: Define how risks and technical debt will be tracked and reviewed over time.

| Process | Frequency | Participants | Output |
|---------|-----------|-------------|--------|
| _\<Risk Review\>_ | _\<Monthly\>_ | _\<Architect, Tech Lead, Product Owner\>_ | _\<Updated risk register\>_ |
| _\<Technical Debt Review\>_ | _\<Per sprint planning\>_ | _\<Tech Lead, Development Team\>_ | _\<Prioritized remediation backlog\>_ |
| _\<Architecture Assessment\>_ | _\<Quarterly\>_ | _\<Architecture Review Board\>_ | _\<Architecture fitness report\>_ |

---

> Based on the arc42 architecture template (https://arc42.org).  
> Created by Dr. Peter Hruschka and Dr. Gernot Starke.  
> Licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
