# 7. Deployment View

> **Help**: The deployment view describes:
>
> 1. The technical infrastructure used to execute the system, with infrastructure elements like geographical locations, environments, computers, processors, channels, and net topologies as well as other infrastructure elements.
> 2. The mapping of (software) building blocks to that infrastructure elements.
>
> Often systems are executed in different environments, e.g., development, test, staging, production. In such cases, you should document all relevant environments.
>
> Especially document the deployment view when your software is executed as a distributed system with more than one computer, processor, server, or container, or when you design and construct your own hardware/infrastructure.
>
> **Motivation**: Software does not run without hardware. This underlying infrastructure can and will influence your system and/or some cross-cutting concepts. Therefore, you need to know the infrastructure.
>
> **Form**: UML deployment diagrams, C4 deployment diagrams, or similar infrastructure-aware notations. Use tables to map building blocks to infrastructure nodes.

---

## 7.1 Infrastructure Level 1

> **Help**: Describe (usually in a combination of diagrams, tables, and text):
>
> - The distribution of your system to multiple locations, environments, computers, processors, etc., as well as the physical connections between them
> - Important justification or motivation for this deployment structure
> - Quality and/or performance features of the infrastructure
> - The mapping of software artifacts to elements of the infrastructure

### Deployment Overview Diagram

_\<Insert a deployment diagram showing the production infrastructure. Consider using PlantUML, Mermaid, or C4 deployment notation.\>_

```
┌───────────────────────────────────────────────────────────────────┐
│                        Cloud Provider (AWS)                       │
│                                                                   │
│  ┌─────────────────────────┐  ┌─────────────────────────┐        │
│  │    Availability Zone A   │  │    Availability Zone B   │        │
│  │                         │  │                         │        │
│  │  ┌───────────────────┐  │  │  ┌───────────────────┐  │        │
│  │  │  K8s Node Pool    │  │  │  │  K8s Node Pool    │  │        │
│  │  │  ┌─────┐ ┌─────┐ │  │  │  │  ┌─────┐ ┌─────┐ │  │        │
│  │  │  │Svc A│ │Svc B│ │  │  │  │  │Svc A│ │Svc B│ │  │        │
│  │  │  └─────┘ └─────┘ │  │  │  │  └─────┘ └─────┘ │  │        │
│  │  └───────────────────┘  │  │  └───────────────────┘  │        │
│  │                         │  │                         │        │
│  │  ┌───────────────────┐  │  │  ┌───────────────────┐  │        │
│  │  │  Database (Primary)│  │  │  │  Database (Replica)│  │        │
│  │  └───────────────────┘  │  │  └───────────────────┘  │        │
│  └─────────────────────────┘  └─────────────────────────┘        │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │  CDN / WAF    │  │  Load        │  │  Object      │            │
│  │              │  │  Balancer    │  │  Storage     │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
└───────────────────────────────────────────────────────────────────┘
```

### Motivation

_\<Why was this deployment topology chosen? What are the key drivers (availability, cost, compliance, latency)?\>_

### Quality and Performance Features

| Feature | Specification | Notes |
|---------|--------------|-------|
| _\<Availability\>_ | _\<99.9% SLA\>_ | _\<Multi-AZ deployment\>_ |
| _\<Scalability\>_ | _\<Auto-scaling 2-20 pods\>_ | _\<CPU/memory-based HPA\>_ |
| _\<Network Latency\>_ | _\<< 50ms within region\>_ | _\<Same-region deployment\>_ |
| _\<Storage\>_ | _\<Encrypted at rest, AES-256\>_ | _\<Managed encryption keys\>_ |
| _\<Backup\>_ | _\<Daily automated backups\>_ | _\<30-day retention\>_ |

### Mapping of Building Blocks to Infrastructure

| Building Block | Infrastructure Element | Instance Count | Resources |
|---------------|----------------------|----------------|-----------|
| _\<Service A\>_ | _\<K8s Deployment\>_ | _\<2-10 replicas\>_ | _\<512Mi RAM, 0.5 CPU\>_ |
| _\<Service B\>_ | _\<K8s Deployment\>_ | _\<2-5 replicas\>_ | _\<1Gi RAM, 1 CPU\>_ |
| _\<Database\>_ | _\<RDS PostgreSQL\>_ | _\<1 primary + 1 replica\>_ | _\<db.r6g.large\>_ |
| _\<Cache\>_ | _\<ElastiCache Redis\>_ | _\<3-node cluster\>_ | _\<cache.r6g.large\>_ |
| _\<Message Broker\>_ | _\<Amazon MSK\>_ | _\<3 brokers\>_ | _\<kafka.m5.large\>_ |
| _\<Static Assets\>_ | _\<S3 + CloudFront\>_ | _\<1 bucket + CDN\>_ | _\<Standard tier\>_ |

---

## 7.2 Infrastructure Level 2

> **Help**: Here you can include the internal structure of (some) infrastructure elements from Level 1. Copy the structure from Level 1 for each selected element.

### 7.2.1 _\<Kubernetes Cluster Detail\>_

_\<Provide more detailed information about the Kubernetes cluster configuration, namespace strategy, resource quotas, network policies, etc.\>_

| Namespace | Services | Resource Quota | Network Policy |
|-----------|----------|---------------|----------------|
| _\<production\>_ | _\<Service A, Service B\>_ | _\<CPU: 8, Memory: 16Gi\>_ | _\<Ingress restricted\>_ |
| _\<monitoring\>_ | _\<Prometheus, Grafana\>_ | _\<CPU: 4, Memory: 8Gi\>_ | _\<Internal only\>_ |
| _\<ingress\>_ | _\<Nginx Ingress\>_ | _\<CPU: 2, Memory: 4Gi\>_ | _\<External facing\>_ |

---

## 7.3 Environments

> **Help**: Document the different environments if they differ significantly in structure or if the differences are architecturally relevant.

| Environment | Purpose | Infrastructure | Data | Access |
|-------------|---------|---------------|------|--------|
| _\<Development\>_ | _\<Local development and unit testing\>_ | _\<Docker Compose / Minikube\>_ | _\<Synthetic test data\>_ | _\<Developers\>_ |
| _\<Integration\>_ | _\<Integration testing\>_ | _\<Shared K8s cluster (reduced)\>_ | _\<Anonymized subset\>_ | _\<Dev + QA teams\>_ |
| _\<Staging\>_ | _\<Pre-production validation\>_ | _\<Production-mirror (scaled down)\>_ | _\<Anonymized production copy\>_ | _\<QA + Ops teams\>_ |
| _\<Production\>_ | _\<Live system\>_ | _\<Full HA infrastructure\>_ | _\<Real data\>_ | _\<Ops team only\>_ |

---

> Based on the arc42 architecture template (https://arc42.org).  
> Created by Dr. Peter Hruschka and Dr. Gernot Starke.  
> Licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
