# 10. Quality Requirements

> **Help**: This section contains all quality requirements as a quality tree with scenarios. The most important ones have already been described in Section 1.2 (Quality Goals).
>
> Here you can also capture quality requirements with lesser priority, which will not create high risks when they are not fully achieved.
>
> **Motivation**: Since quality requirements will have a lot of influence on architectural decisions, you should know for every stakeholder what is really important to them, concrete and measurable.
>
> **Form**: Use a quality tree and quality scenarios following the ISO 25010 quality model or a similar quality model.

---

## 10.1 Quality Tree

> **Help**: The quality tree (as defined in ATAM -- Architecture Tradeoff Analysis Method) with quality/evaluation scenarios as leaves. The quality tree provides a high-level overview of the quality goals and requirements, using a tree structure with quality categories as roots and concrete quality scenarios as leaves.
>
> **Content**: The top-level quality attributes (from the ISO 25010 model or a custom model) with refinements and concrete quality scenarios.

```
Quality
├── Performance Efficiency
│   ├── Time Behavior
│   │   └── <Scenario P1>
│   ├── Resource Utilization
│   │   └── <Scenario P2>
│   └── Capacity
│       └── <Scenario P3>
├── Reliability
│   ├── Availability
│   │   └── <Scenario R1>
│   ├── Fault Tolerance
│   │   └── <Scenario R2>
│   └── Recoverability
│       └── <Scenario R3>
├── Security
│   ├── Confidentiality
│   │   └── <Scenario S1>
│   ├── Integrity
│   │   └── <Scenario S2>
│   └── Accountability
│       └── <Scenario S3>
├── Maintainability
│   ├── Modularity
│   │   └── <Scenario M1>
│   ├── Testability
│   │   └── <Scenario M2>
│   └── Modifiability
│       └── <Scenario M3>
├── Usability
│   ├── Learnability
│   │   └── <Scenario U1>
│   └── User Error Protection
│       └── <Scenario U2>
└── Portability
    ├── Adaptability
    │   └── <Scenario PT1>
    └── Installability
        └── <Scenario PT2>
```

---

## 10.2 Quality Scenarios

> **Help**: Concretization of (sometimes vague or implicit) quality requirements using quality scenarios.
>
> These scenarios describe what should happen when a stimulus arrives at the system:
> - **Source of stimulus**: Who or what generates the stimulus?
> - **Stimulus**: What is the event or condition?
> - **Environment**: Under what conditions does the stimulus occur?
> - **Artifact**: What part of the system is stimulated?
> - **Response**: What should the system do?
> - **Response measure**: How is the response measured?
>
> **Motivation**: Quality requirements tend to be abstract and vague. Scenarios make them concrete and communicable. They also serve as acceptance criteria for architecture evaluations.

### Performance Scenarios

| ID | Scenario | Stimulus | Response Measure | Priority |
|----|----------|----------|-----------------|----------|
| P1 | _\<e.g., Under normal load, the system responds to user requests\>_ | _\<1000 concurrent users\>_ | _\<95th percentile response time < 200ms\>_ | _\<High\>_ |
| P2 | _\<e.g., During peak load, the system continues to function\>_ | _\<5x normal traffic spike\>_ | _\<No errors, response time < 2s\>_ | _\<High\>_ |
| P3 | _\<e.g., Batch processing completes within the processing window\>_ | _\<1M records to process\>_ | _\<Complete within 4 hours\>_ | _\<Medium\>_ |

### Reliability Scenarios

| ID | Scenario | Stimulus | Response Measure | Priority |
|----|----------|----------|-----------------|----------|
| R1 | _\<e.g., System remains available during single-node failure\>_ | _\<One compute node crashes\>_ | _\<Zero downtime, automatic failover < 30s\>_ | _\<High\>_ |
| R2 | _\<e.g., System recovers from database failure\>_ | _\<Database becomes unavailable for 5 minutes\>_ | _\<Automatic reconnection, no data loss\>_ | _\<High\>_ |
| R3 | _\<e.g., System recovers from complete outage\>_ | _\<Full system restart required\>_ | _\<RTO < 15 minutes, RPO < 5 minutes\>_ | _\<Medium\>_ |

### Security Scenarios

| ID | Scenario | Stimulus | Response Measure | Priority |
|----|----------|----------|-----------------|----------|
| S1 | _\<e.g., Unauthorized access attempt is blocked\>_ | _\<Invalid credentials submitted\>_ | _\<Access denied, event logged, alert after 5 attempts\>_ | _\<High\>_ |
| S2 | _\<e.g., Sensitive data is protected in transit\>_ | _\<Network traffic intercepted\>_ | _\<All data encrypted with TLS 1.3\>_ | _\<High\>_ |
| S3 | _\<e.g., User actions are auditable\>_ | _\<Compliance audit requested\>_ | _\<Full audit trail available for past 12 months\>_ | _\<Medium\>_ |

### Maintainability Scenarios

| ID | Scenario | Stimulus | Response Measure | Priority |
|----|----------|----------|-----------------|----------|
| M1 | _\<e.g., Adding a new business rule\>_ | _\<New requirement from product owner\>_ | _\<Changes isolated to single service, < 2 days effort\>_ | _\<High\>_ |
| M2 | _\<e.g., Upgrading a dependency\>_ | _\<Security patch for library\>_ | _\<Update and deploy within 4 hours\>_ | _\<Medium\>_ |
| M3 | _\<e.g., New developer onboarding\>_ | _\<New team member joins\>_ | _\<Productive within 1 week using documentation\>_ | _\<Medium\>_ |

### Usability Scenarios

| ID | Scenario | Stimulus | Response Measure | Priority |
|----|----------|----------|-----------------|----------|
| U1 | _\<e.g., First-time user completes key task\>_ | _\<New user without training\>_ | _\<Task completed within 5 minutes\>_ | _\<Medium\>_ |
| U2 | _\<e.g., User makes input error\>_ | _\<Invalid form submission\>_ | _\<Clear error message, no data lost, easy correction\>_ | _\<Medium\>_ |

---

> Based on the arc42 architecture template (https://arc42.org).  
> Created by Dr. Peter Hruschka and Dr. Gernot Starke.  
> Licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
