# System Map

Domain-level topology for NovaTrek Adventures — 22 services across 9 domains.

!!! info "Everything on this portal is entirely fictional"
    NovaTrek Adventures is a completely fictitious company used as a synthetic workspace for the Continuous Architecture Platform proof of concept.

---

## Domain Overview

Each node represents a domain (bounded context) containing one or more microservices. Arrows show **cross-domain** communication with connection counts.

<div class="diagram-wrap">
  <a href="../svg/topology-domain-overview.svg" target="_blank" class="diagram-expand" title="Open in new tab">&#x2922;</a>
  <object data="../svg/topology-domain-overview.svg" type="image/svg+xml" style="max-width: 100%;">
    Domain Overview C4 Diagram
  </object>
</div>

---

## Domains

Click a domain in the diagram or table to see its service-level topology with individual connections.

| Domain | Services | REST Out | Events Out |
|--------|----------|----------|------------|
| [Booking](domain-views.md#booking) | 1 | 4 | 3 |
| [External](domain-views.md#external) | 1 | 5 | 0 |
| [Guest Identity](domain-views.md#guest-identity) | 1 | 2 | 2 |
| [Guide Management](domain-views.md#guide-management) | 1 | 0 | 0 |
| [Logistics](domain-views.md#logistics) | 2 | 6 | 0 |
| [Operations](domain-views.md#operations) | 2 | 13 | 4 |
| [Product Catalog](domain-views.md#product-catalog) | 2 | 4 | 0 |
| [Safety](domain-views.md#safety) | 3 | 11 | 9 |
| [Support](domain-views.md#support) | 9 | 5 | 1 |

---

## Legend

| Element | Meaning |
|---------|---------|
| Blue box | Domain (bounded context) containing one or more services |
| Solid arrow with label | Synchronous REST calls (count shown) |
| Dashed purple arrow | Asynchronous Kafka events (count shown) |

## How to Read This Diagram

1. **Each box is a domain** — a bounded context owning a group of related microservices
2. **Arrows between domains** show cross-boundary communication with the number of distinct service-to-service connections
3. **High fan-in domains** (many arrows pointing in) provide shared platform capabilities — Guest Identity, Support
4. **Dashed lines** indicate event-driven decoupling — the source domain publishes events without knowing the consumers
5. **Drill down** into any domain via the [Domain Views](domain-views.md) page to see individual service connections

## Data Source

Generated from `architecture/calm/novatrek-topology.json` by `portal/scripts/generate-topology-pages.py`.
