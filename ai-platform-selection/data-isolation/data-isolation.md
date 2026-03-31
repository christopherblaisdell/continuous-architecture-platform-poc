# Data Isolation

## Zero Corporate Data Policy

This evaluation contains **zero corporate data**. Every artifact, tool response, and data point is synthetic. This page documents the isolation guarantees and verification mechanisms.

---

## The NovaTrek Adventures Domain

NovaTrek Adventures is a **fictional outdoor adventure tourism company** created specifically for this evaluation. Nothing about NovaTrek corresponds to any real company, product, or service.

### Synthetic Assets

| Asset | Count | Description |
|-------|-------|-------------|
| Microservice OpenAPI specs | 19 | Fictional services (svc-check-in, svc-reservations, etc.) |
| Java source code files | Multiple | Synthetic controllers, services, repositories |
| Architecture decision records | 14 | ADR-001 through ADR-014, all fictional |
| JIRA tickets | 6 | NTK-10001 through NTK-10006, synthetic feature/bug tickets |
| Elasticsearch logs | 50+ | Fabricated error logs with synthetic trace IDs |
| GitLab merge requests | Multiple | Synthetic MR diffs and code changes |
| Guest profiles | Synthetic | Fictional guest names, IDs, and reservation data |

### Service Domains

| Domain | Services |
|--------|----------|
| Operations | svc-check-in, svc-scheduling-orchestrator |
| Guest Identity | svc-guest-profiles |
| Booking | svc-reservations |
| Product Catalog | svc-trip-catalog, svc-trail-management |
| Safety | svc-safety-compliance |
| Logistics | svc-transport-logistics, svc-gear-inventory |
| Guide Management | svc-guide-management |
| External | svc-partner-integrations |
| Support | svc-notifications, svc-payments, svc-loyalty-rewards, svc-media-gallery, svc-analytics, svc-weather, svc-location-services, svc-inventory-procurement |

---

## Mock Tool Architecture

All tool integrations are **local Python scripts** reading JSON files from disk. No network calls are made. No credentials are used. No corporate systems are accessed.

| Tool | Implementation | Data Source |
|------|---------------|-------------|
| JIRA | `python3 scripts/mock-jira-client.py` | `scripts/mock-data/tickets.json` |
| Elasticsearch | `python3 scripts/mock-elastic-searcher.py` | `scripts/mock-data/logs.json` |
| GitLab | `python3 scripts/mock-gitlab-client.py` | `scripts/mock-data/merge-requests.json` |

### What the Mock Tools Do NOT Do

- Make HTTP requests to any external service
- Use API credentials or tokens
- Import `requests`, `urllib`, or any networking library
- Access corporate JIRA, Elasticsearch, or GitLab instances
- Transmit data outside the local filesystem

The scripts use **Python standard library only** (`json`, `argparse`, `sys`). No external dependencies are installed or required.

---

## Data Isolation Rules

1. **Never imply real corporate connections.** When referencing JIRA, Elastic, or GitLab tools, always clarify they are local mock scripts
2. **Never fabricate data.** Only use data returned by the mock scripts or present in workspace files
3. **Never introduce corporate identifiers.** All identifiers use the NovaTrek namespace
4. **Always use the NovaTrek Adventures domain** for any new synthetic data
5. **Never reference real company names, products, or internal systems** in generated content
6. **Never generate fake URLs** that resolve to real domains -- use `*.novatrek.example.com` exclusively

---

## Verification

An automated audit script verifies data isolation before every commit:

```bash
./portal/scripts/utilities/audit-data-isolation.sh
```

This script scans all workspace files for:

- Corporate identifiers (company names, product names, internal system references)
- Real domain names that should not appear in synthetic data
- API credentials or tokens that may have been accidentally committed
- References to corporate JIRA, Confluence, or GitLab instances

---

## Why This Matters

Data isolation serves two purposes:

1. **Evaluation integrity:** The AI toolchains are evaluated on their ability to process architecture problems, not on their access to proprietary data. Using synthetic data ensures the evaluation measures the toolchain, not the dataset.

2. **Publishability:** Every artifact produced by this evaluation can be shared publicly, presented to stakeholders, or published to documentation portals without data classification review. There is nothing to redact because there is nothing corporate to protect.
