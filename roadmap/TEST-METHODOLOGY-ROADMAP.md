# Test Methodology and Practice Roadmap

| | |
|-----------|-------|
| **Author** | Christopher Blaisdell |
| **Date** | 2026-03-11 |
| **Status** | In Progress |
| **Purpose** | Define a comprehensive testing methodology for NovaTrek Adventures — establishing TDD/BDD practices, coverage standards, automated regression, and contract testing as integral parts of the delivery practice |

---

## 1. Problem Statement

The Continuous Architecture Platform produces solution designs, API contracts, and implementation guidance — but the delivery practice currently has no defined testing standards. The arc42 templates reference coverage targets and flag test gaps as risks, yet no enforcement mechanism, methodology, or tooling exists. As the platform grows and more services evolve through solution designs, untested changes compound risk across service boundaries.

---

## 2. Goals

1. **Full coverage** — Every service meets defined minimum thresholds for unit, branch, and integration test coverage
2. **Automated regression** — Every PR runs the full regression suite; no merge without green tests
3. **Contract testing** — Cross-service API boundaries are validated automatically against OpenAPI specs
4. **Test-first culture** — TDD and/or BDD adopted as standard practice, not an afterthought
5. **Traceability** — User story acceptance criteria map directly to executable test scenarios

---

## 3. Testing Pyramid

```
         ┌─────────┐
         │  E2E    │   Few — critical happy paths only
         ├─────────┤
        │ Contract  │   Per cross-service boundary
        ├───────────┤
       │ Integration │   Service + database + dependencies
       ├─────────────┤
      │    Unit       │   Fast, isolated, high volume
      └───────────────┘
```

| Layer | Scope | Speed | Count | Owner |
|-------|-------|-------|-------|-------|
| Unit | Single class/function | Milliseconds | Highest | Developer |
| Integration | Service + data store | Seconds | Medium | Developer |
| Contract | API boundary between services | Seconds | Per integration point | Service team |
| End-to-End | Full user journey across services | Minutes | Lowest (critical paths) | QA / Platform team |

---

## 4. Methodology Options

### 4.1 TDD (Test-Driven Development)

Write tests before implementation code. Red-green-refactor cycle.

| Aspect | Assessment |
|--------|-----------|
| Strengths | Forces clean API design, prevents gold-plating, immediate regression safety |
| Challenges | Requires discipline and team buy-in, slower initial velocity |
| Best fit | Unit tests, service-layer logic, data validation rules |
| Java tooling | JUnit 5, Mockito, AssertJ |

### 4.2 BDD (Behavior-Driven Development)

Write human-readable scenarios (Given/When/Then) derived from acceptance criteria.

| Aspect | Assessment |
|--------|-----------|
| Strengths | Bridges user stories to executable tests, stakeholder-readable, living documentation |
| Challenges | Gherkin maintenance overhead, step definition boilerplate |
| Best fit | Acceptance criteria validation, cross-service workflows, business rule verification |
| Java tooling | Cucumber-JVM, JBehave |

### 4.3 Recommended Hybrid Approach

| Layer | Methodology | Rationale |
|-------|-------------|-----------|
| Unit | TDD | Fast feedback, forces clean design at the class level |
| Integration | TDD | Validates data access and service composition |
| Contract | Spec-driven | Auto-generated from OpenAPI specs — no manual test authoring |
| Acceptance | BDD | User stories produce Gherkin scenarios; acceptance criteria become executable |
| E2E | Scripted | Small set of critical path scripts; not TDD or BDD |

---

## 5. Coverage Standards

| Metric | Minimum Threshold | Target | Enforcement |
|--------|-------------------|--------|-------------|
| Line coverage | 80% | 90% | CI gate — PR blocked below minimum |
| Branch coverage | 70% | 80% | CI gate |
| Mutation score | 60% | 75% | CI report — advisory initially, gate later |
| Contract test coverage | 100% of cross-service calls | 100% | CI gate |

### Coverage Tooling

| Tool | Purpose |
|------|---------|
| JaCoCo | Java code coverage (line, branch, instruction) |
| PITest | Mutation testing for Java |
| Pact / Spring Cloud Contract | Consumer-driven contract testing |
| Cucumber-JVM | BDD scenario execution |
| SonarQube / SonarCloud | Aggregated quality dashboard (optional) |

---

## 6. Contract Testing Strategy

Every entry in `architecture/metadata/cross-service-calls.yaml` represents a contract boundary that requires a contract test.

```
Consumer Service ──── Pact Contract ──── Provider Service
       │                                        │
       └── Consumer test generates pact ──┐     │
                                          │     │
                                   Pact Broker   │
                                          │     │
                        Provider test verifies ──┘
```

### OpenAPI-Driven Contracts

NovaTrek already maintains 19 OpenAPI specs in `architecture/specs/`. These specs can drive contract test generation:

1. **Provider verification** — validate that service implementation matches its OpenAPI spec
2. **Consumer contract** — validate that consumer expectations align with the published spec
3. **Breaking change detection** — diff OpenAPI specs on PR to flag backward-incompatible changes

---

## 7. Integration with Delivery Practice

### Solution Design Template Changes

Add a test plan section to `3.solution/g.guidance/`:

```
3.solution/
  g.guidance/
    implementation-guidance.md   (existing)
    test-plan.md                 (new — required)
```

Test plan contents:
- Which test layers are affected (unit, integration, contract, acceptance)
- New test scenarios required
- Existing tests that need updating
- BDD scenarios derived from user stories (Gherkin format)
- Contract test additions for new cross-service integrations

### PR Review Checklist Additions

- [ ] Test plan included in guidance folder
- [ ] Coverage thresholds met for affected services
- [ ] Contract tests added for new cross-service integrations
- [ ] BDD scenarios correspond to acceptance criteria in user stories
- [ ] No test gaps flagged by mutation testing

### CI Pipeline Additions

| Stage | Gate | Tool |
|-------|------|------|
| Build | Compile + unit tests | Maven / Gradle |
| Coverage | Line >= 80%, Branch >= 70% | JaCoCo |
| Mutation | Score >= 60% (advisory) | PITest |
| Contract | All pacts verified | Pact / Spring Cloud Contract |
| Acceptance | All BDD scenarios pass | Cucumber-JVM |

---

## 8. Phased Rollout

### Phase A: Standards and Tooling (Foundation)

| Step | Task | Effort |
|------|------|--------|
| A.1 | COMPLETE -- Created ADR-012 for test methodology (TDD + BDD hybrid) | Small |
| A.2 | COMPLETE -- Defined coverage thresholds in `config/test-standards.yaml` | Small |
| A.3 | COMPLETE -- Added JaCoCo coverage verification (80% line, 70% branch gates), PITest mutation testing (advisory), and Cucumber-JVM BDD to service build template | Small |
| A.4 | COMPLETE -- Added test plan section to solution design template | Small |
| A.5 | COMPLETE -- Updated PR review checklist with test criteria | Small |

### Phase B: Contract Testing (Cross-Service Safety)

| Step | Task | Effort |
|------|------|--------|
| B.1 | Evaluate Pact vs Spring Cloud Contract for NovaTrek services | Small |
| B.2 | Create ADR for contract testing tool selection | Small |
| B.3 | Set up Pact Broker (or equivalent) infrastructure | Medium |
| B.4 | Write contract tests for highest-traffic cross-service calls (svc-check-in boundaries) | Medium |
| B.5 | Add contract verification to CI pipeline | Small |

### Phase C: BDD Adoption (Acceptance Testing)

| Step | Task | Effort |
|------|------|--------|
| C.1 | Set up Cucumber-JVM in service build templates | Small |
| C.3 | Write step definitions for common patterns (API calls, database assertions) | Medium |
| C.4 | Add BDD scenario execution to CI pipeline | Small |
| C.5 | Document BDD authoring guide for architects and developers | Small |

### Phase D: Coverage Enforcement (Quality Gates)

| Step | Task | Effort |
|------|------|--------|
| D.1 | Enable JaCoCo coverage gate in CI (fail PR below 80% line coverage) | Small |
| D.2 | Enable mutation testing reports in CI (advisory) | Small |
| D.3 | Create coverage dashboard (SonarCloud or custom) | Medium |
| D.4 | Promote mutation score to gate (fail PR below 60%) | Small |
| D.5 | Quarterly coverage review and threshold adjustment | Ongoing |

---

## 9. Success Criteria

Six months after adoption:

1. Every service has >= 80% line coverage with automated enforcement
2. Every cross-service integration point has a contract test
3. Every solution design includes a test plan in the guidance folder
4. User story acceptance criteria are executable as BDD scenarios
5. No production regression escapes that would have been caught by the defined test layers
6. Mutation testing identifies dead code and weak assertions across all services

---

## 10. Related Documents

| Document | Relevance |
|----------|-----------|
| [ROADMAP.md](ROADMAP.md) | Parent roadmap — this document extends the delivery practice (see Future Initiatives section) |
| [architecture/reminders/TEST-METHODOLOGY.md](../architecture/reminders/TEST-METHODOLOGY.md) | Reminder tracking this initiative |
| arc42 constraints template | References 80% coverage target |
| arc42 risk register | Lists test coverage gaps as known risk |
| `architecture/metadata/cross-service-calls.yaml` | Defines every contract boundary requiring tests |
| [ROADMAP.md Future Initiatives](ROADMAP.md#future-initiatives-summary) | Consolidated view of all planned and proposed work |
