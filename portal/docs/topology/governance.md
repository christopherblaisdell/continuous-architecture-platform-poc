---
tags:
  - topology
  - governance
  - compliance
---

# Architecture Governance Dashboard

Auto-generated from the [CALM topology](../../calm/) — validates every service against the
[NovaTrek Organizational Architecture Standard](../../../architecture/calm/standards/novatrek-org-standard.json).

---

## Compliance Summary

| Metric | Count |
|--------|-------|
| Services assessed | 22 |
| Total rule checks | 111 |
| Passing | 111 |
| Failing (error) | 0 |
| Warnings | 0 |

All services are compliant with NovaTrek architecture governance rules.

---

## Governance Rules

| Rule | ID | Severity | Description |
|------|----|----------|-------------|
| Domain metadata | novatrek-003 | Error | Every service must declare its bounded context domain |
| Team metadata | novatrek-003 | Error | Every service must declare its owning team |
| Single database | novatrek-001 | Warning | Each service should own exactly one database |
| API-mediated access | novatrek-002 | Error | No JDBC connections between services |
| No orphan services | novatrek-003 | Warning | Every service should participate in at least one relationship |
| PCI scope | novatrek-004 | Error | PCI-scoped services must declare pci-in-scope: true |

---

## Per-Service Compliance

Legend: ✓ Pass | ✗ Fail | ! Warning | — Not applicable

| Service | Domain | R1 Domain | R2 Team | R3 Single DB | R4 API Only | R5 Connected | R6 PCI |
|---------|--------|-----------|---------|--------------|-------------|--------------|--------|
| [svc-analytics](../microservices/svc-analytics/) | Support | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| [svc-check-in](../microservices/svc-check-in/) | Operations | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| [svc-emergency-response](../microservices/svc-emergency-response/) | Safety | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| [svc-gear-inventory](../microservices/svc-gear-inventory/) | Logistics | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| [svc-guest-profiles](../microservices/svc-guest-profiles/) | Guest Identity | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| [svc-guide-management](../microservices/svc-guide-management/) | Guide Management | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| [svc-inventory-procurement](../microservices/svc-inventory-procurement/) | Support | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| [svc-location-services](../microservices/svc-location-services/) | Support | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| [svc-loyalty-rewards](../microservices/svc-loyalty-rewards/) | Support | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| [svc-media-gallery](../microservices/svc-media-gallery/) | Support | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| [svc-notifications](../microservices/svc-notifications/) | Support | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| [svc-partner-integrations](../microservices/svc-partner-integrations/) | External | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| [svc-payments](../microservices/svc-payments/) | Support | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| [svc-reservations](../microservices/svc-reservations/) | Booking | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| [svc-reviews](../microservices/svc-reviews/) | Support | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| [svc-safety-compliance](../microservices/svc-safety-compliance/) | Safety | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| [svc-scheduling-orchestrator](../microservices/svc-scheduling-orchestrator/) | Operations | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| [svc-trail-management](../microservices/svc-trail-management/) | Product Catalog | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| [svc-transport-logistics](../microservices/svc-transport-logistics/) | Logistics | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| [svc-trip-catalog](../microservices/svc-trip-catalog/) | Product Catalog | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| [svc-weather](../microservices/svc-weather/) | Support | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| [svc-wildlife-tracking](../microservices/svc-wildlife-tracking/) | Safety | ✓ | ✓ | ✓ | ✓ | ✓ | — |

---

## Data Source

Generated from `architecture/calm/novatrek-topology.json` by `portal/scripts/generate-governance-dashboard.py`.

Governance rules defined in `architecture/calm/standards/novatrek-org-standard.json`.

To regenerate:
```bash
python3 scripts/generate-calm.py
python3 portal/scripts/generate-governance-dashboard.py
```
