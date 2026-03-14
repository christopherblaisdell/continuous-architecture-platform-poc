# System Map

Interactive service topology for NovaTrek Adventures — 23 services across 9 domains.

!!! info "Everything on this portal is entirely fictional"
    NovaTrek Adventures is a completely fictitious company used as a synthetic workspace for the Continuous Architecture Platform proof of concept.

---

## Full System Topology

**Solid arrows** = synchronous REST calls (HTTPS)
**Dashed arrows** = asynchronous event flows (Kafka)

```mermaid
flowchart LR

    %% Domain subgraphs
    subgraph Booking["Booking"]
        svc-reservations["Reservations"]
    end

    subgraph External["External"]
        svc-partner-integrations["Partner Integrations"]
    end

    subgraph Guest_Identity["Guest Identity"]
        svc-guest-profiles["Guest Profiles"]
    end

    subgraph Guide_Management["Guide Management"]
        svc-guide-management["Guide Management"]
    end

    subgraph Logistics["Logistics"]
        svc-gear-inventory["Gear Inventory"]
        svc-transport-logistics["Transport Logistics"]
    end

    subgraph Operations["Operations"]
        svc-adventure-tracking["Adventure Tracking"]
        svc-check-in["Check In"]
        svc-scheduling-orchestrator["Scheduling Orchestrator"]
    end

    subgraph Product_Catalog["Product Catalog"]
        svc-trail-management["Trail Management"]
        svc-trip-catalog["Trip Catalog"]
    end

    subgraph Safety["Safety"]
        svc-emergency-response["Emergency Response"]
        svc-safety-compliance["Safety Compliance"]
        svc-wildlife-tracking["Wildlife Tracking"]
    end

    subgraph Support["Support"]
        svc-analytics["Analytics"]
        svc-inventory-procurement["Inventory Procurement"]
        svc-location-services["Location Services"]
        svc-loyalty-rewards["Loyalty Rewards"]
        svc-media-gallery["Media Gallery"]
        svc-notifications["Notifications"]
        svc-payments["Payments"]
        svc-reviews["Reviews"]
        svc-weather["Weather"]
    end

    %% REST calls (HTTPS)
    svc-adventure-tracking --> svc-location-services
    svc-check-in --> svc-gear-inventory
    svc-check-in --> svc-guest-profiles
    svc-check-in --> svc-reservations
    svc-check-in --> svc-safety-compliance
    svc-check-in --> svc-trip-catalog
    svc-emergency-response --> svc-adventure-tracking
    svc-emergency-response --> svc-guest-profiles
    svc-emergency-response --> svc-guide-management
    svc-emergency-response --> svc-location-services
    svc-gear-inventory --> svc-guest-profiles
    svc-gear-inventory --> svc-reservations
    svc-gear-inventory --> svc-safety-compliance
    svc-guest-profiles --> svc-analytics
    svc-guest-profiles --> svc-reservations
    svc-inventory-procurement --> svc-gear-inventory
    svc-inventory-procurement --> svc-payments
    svc-loyalty-rewards --> svc-guest-profiles
    svc-loyalty-rewards --> svc-payments
    svc-loyalty-rewards --> svc-reservations
    svc-partner-integrations --> svc-guest-profiles
    svc-partner-integrations --> svc-payments
    svc-partner-integrations --> svc-reservations
    svc-partner-integrations --> svc-trip-catalog
    svc-reservations --> svc-guest-profiles
    svc-reservations --> svc-payments
    svc-reservations --> svc-trip-catalog
    svc-reviews --> svc-guest-profiles
    svc-reviews --> svc-reservations
    svc-safety-compliance --> svc-guest-profiles
    svc-safety-compliance --> svc-guide-management
    svc-scheduling-orchestrator --> svc-guide-management
    svc-scheduling-orchestrator --> svc-location-services
    svc-scheduling-orchestrator --> svc-trail-management
    svc-scheduling-orchestrator --> svc-trip-catalog
    svc-scheduling-orchestrator --> svc-weather
    svc-trail-management --> svc-location-services
    svc-trail-management --> svc-safety-compliance
    svc-trail-management --> svc-weather
    svc-transport-logistics --> svc-location-services
    svc-transport-logistics --> svc-reservations
    svc-wildlife-tracking --> svc-scheduling-orchestrator
    svc-wildlife-tracking --> svc-trail-management
    svc-wildlife-tracking --> svc-weather

    %% Event flows (Kafka)
    svc-adventure-tracking -.-> svc-emergency-response
    svc-adventure-tracking -.-> svc-notifications
    svc-check-in -.-> svc-analytics
    svc-check-in -.-> svc-notifications
    svc-emergency-response -.-> svc-analytics
    svc-emergency-response -.-> svc-notifications
    svc-emergency-response -.-> svc-safety-compliance
    svc-emergency-response -.-> svc-scheduling-orchestrator
    svc-guest-profiles -.-> svc-analytics
    svc-guest-profiles -.-> svc-loyalty-rewards
    svc-inventory-procurement -.-> svc-notifications
    svc-loyalty-rewards -.-> svc-notifications
    svc-media-gallery -.-> svc-notifications
    svc-partner-integrations -.-> svc-notifications
    svc-payments -.-> svc-notifications
    svc-payments -.-> svc-reservations
    svc-reservations -.-> svc-analytics
    svc-reservations -.-> svc-notifications
    svc-reservations -.-> svc-scheduling-orchestrator
    svc-safety-compliance -.-> svc-analytics
    svc-safety-compliance -.-> svc-notifications
    svc-scheduling-orchestrator -.-> svc-analytics
    svc-scheduling-orchestrator -.-> svc-guide-management
    svc-scheduling-orchestrator -.-> svc-notifications
    svc-trail-management -.-> svc-notifications
    svc-transport-logistics -.-> svc-notifications
    svc-weather -.-> svc-notifications
    svc-wildlife-tracking -.-> svc-analytics
    svc-wildlife-tracking -.-> svc-notifications
    svc-wildlife-tracking -.-> svc-safety-compliance
    svc-wildlife-tracking -.-> svc-scheduling-orchestrator
    svc-wildlife-tracking -.-> svc-trail-management

    %% Styling
    style Operations fill:#1B5E2015,stroke:#1B5E20,stroke-width:2px
    style Guest_Identity fill:#0D47A115,stroke:#0D47A1,stroke-width:2px
    style Booking fill:#E6510015,stroke:#E65100,stroke-width:2px
    style Product_Catalog fill:#4A148C15,stroke:#4A148C,stroke-width:2px
    style Safety fill:#B71C1C15,stroke:#B71C1C,stroke-width:2px
    style Logistics fill:#00606415,stroke:#006064,stroke-width:2px
    style Guide_Management fill:#33691E15,stroke:#33691E,stroke-width:2px
    style External fill:#37474F15,stroke:#37474F,stroke-width:2px
    style Support fill:#4E342E15,stroke:#4E342E,stroke-width:2px
```

---

## Legend

| Element | Meaning |
|---------|---------|
| Solid box | Microservice |
| Colored subgraph | Domain boundary |
| Solid arrow (-->) | Synchronous REST call |
| Dashed arrow (-.->) | Asynchronous Kafka event |

## How to Read This Diagram

1. **Domains** are grouped as colored subgraphs — services within the same subgraph belong to the same bounded context
2. **High fan-in services** (many arrows pointing in) are shared platform services — `Guest Profiles`, `Notifications`, `Reservations`
3. **High fan-out services** (many arrows pointing out) are orchestrators — `Check In`, `Scheduling Orchestrator`, `Emergency Response`
4. **Dashed lines** indicate event-driven decoupling — the source publishes an event without knowing the consumer

## Data Source

Generated from `architecture/calm/novatrek-topology.json` by `portal/scripts/generate-topology-pages.py`.
