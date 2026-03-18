# System Map

Domain-level topology for NovaTrek Adventures — 22 services across 9 domains.

!!! info "Everything on this portal is entirely fictional"
    NovaTrek Adventures is a completely fictitious company used as a synthetic workspace for the Continuous Architecture Platform proof of concept.

---

## Domain Overview

Each node represents a domain (bounded context) containing one or more microservices. Arrows show **cross-domain** communication — internal connections within a domain are noted on each node.

**Solid arrows** = synchronous REST calls (HTTPS)
**Dashed arrows** = asynchronous event flows (Kafka)

```mermaid
flowchart TB

    Booking["Booking\n1 service"]
    External["External\n1 service"]
    Guest_Identity["Guest Identity\n1 service"]
    Guide_Management["Guide Management\n1 service"]
    Logistics["Logistics\n2 services"]
    Operations["Operations\n2 services"]
    Product_Catalog["Product Catalog\n2 services"]
    Safety["Safety\n3 services\n2 internal connections"]
    Support["Support\n9 services\n7 internal connections"]

    %% Cross-domain REST calls
    Booking -->|1 REST| Guest_Identity
    Booking -->|1 REST| Product_Catalog
    Booking -->|1 REST| Support
    External -->|1 REST| Booking
    External -->|1 REST| Guest_Identity
    External -->|1 REST| Product_Catalog
    External -->|1 REST| Support
    Guest_Identity -->|1 REST| Booking
    Guest_Identity -->|1 REST| Support
    Logistics -->|2 REST| Booking
    Logistics -->|1 REST| Guest_Identity
    Logistics -->|1 REST| Safety
    Logistics -->|1 REST| Support
    Operations -->|1 REST| Booking
    Operations -->|1 REST| Guest_Identity
    Operations -->|1 REST| Guide_Management
    Operations -->|1 REST| Logistics
    Operations -->|3 REST| Product_Catalog
    Operations -->|1 REST| Safety
    Operations -->|2 REST| Support
    Product_Catalog -->|1 REST| Safety
    Product_Catalog -->|2 REST| Support
    Safety -->|2 REST| Guest_Identity
    Safety -->|2 REST| Guide_Management
    Safety -->|1 REST| Operations
    Safety -->|1 REST| Product_Catalog
    Safety -->|2 REST| Support
    Support -->|2 REST| Booking
    Support -->|2 REST| Guest_Identity
    Support -->|1 REST| Logistics

    %% Cross-domain event flows
    Booking -.->|1 events| Operations
    Booking -.->|2 events| Support
    External -.->|1 events| Support
    Guest_Identity -.->|2 events| Support
    Logistics -.->|1 events| Support
    Operations -.->|1 events| Guide_Management
    Operations -.->|4 events| Support
    Product_Catalog -.->|1 events| Support
    Safety -.->|2 events| Operations
    Safety -.->|1 events| Product_Catalog
    Safety -.->|6 events| Support
    Support -.->|1 events| Booking

    %% Styling
    style Operations fill:#1B5E2020,stroke:#1B5E20,stroke-width:2px,color:#fff
    style Guest_Identity fill:#0D47A120,stroke:#0D47A1,stroke-width:2px,color:#fff
    style Booking fill:#E6510020,stroke:#E65100,stroke-width:2px,color:#fff
    style Product_Catalog fill:#4A148C20,stroke:#4A148C,stroke-width:2px,color:#fff
    style Safety fill:#B71C1C20,stroke:#B71C1C,stroke-width:2px,color:#fff
    style Logistics fill:#00606420,stroke:#006064,stroke-width:2px,color:#fff
    style Guide_Management fill:#33691E20,stroke:#33691E,stroke-width:2px,color:#fff
    style External fill:#37474F20,stroke:#37474F,stroke-width:2px,color:#fff
    style Support fill:#4E342E20,stroke:#4E342E,stroke-width:2px,color:#fff
```
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/calm/novatrek-topology.json" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from architecture/calm/novatrek-topology.json</a>

---

## Domains

Click a domain to see its service-level topology diagram with individual service connections.

| Domain | Services | REST Out | Events Out |
|--------|----------|----------|------------|
| [Booking](domain-views.md#booking) | 1 | 3 | 3 |
| [External](domain-views.md#external) | 1 | 4 | 1 |
| [Guest Identity](domain-views.md#guest-identity) | 1 | 2 | 2 |
| [Guide Management](domain-views.md#guide-management) | 1 | 0 | 0 |
| [Logistics](domain-views.md#logistics) | 2 | 5 | 1 |
| [Operations](domain-views.md#operations) | 2 | 10 | 5 |
| [Product Catalog](domain-views.md#product-catalog) | 2 | 3 | 1 |
| [Safety](domain-views.md#safety) | 3 | 8 | 9 |
| [Support](domain-views.md#support) | 9 | 5 | 1 |

---

## Legend

| Element | Meaning |
|---------|---------|
| Domain node | Bounded context containing one or more services |
| Solid arrow with count | Cross-domain synchronous REST calls |
| Dashed arrow with count | Cross-domain asynchronous Kafka events |
| Internal connections note | Intra-domain service-to-service calls |

## How to Read This Diagram

1. **Each box is a domain** — a bounded context owning a group of related microservices
2. **Arrows between domains** show cross-boundary communication with the number of distinct service-to-service connections
3. **High fan-in domains** (many arrows pointing in) provide shared platform capabilities — Guest Identity, Support
4. **Dashed lines** indicate event-driven decoupling — the source domain publishes events without knowing the consumers
5. **Drill down** into any domain via the [Domain Views](domain-views.md) page to see individual service connections

## Data Source

Generated from `architecture/calm/novatrek-topology.json` by `portal/scripts/generate-topology-pages.py`.
