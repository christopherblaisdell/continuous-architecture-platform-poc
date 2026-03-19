---
tags:
  - microservice
  - svc-loyalty-rewards
  - support
---

# svc-loyalty-rewards

**NovaTrek Loyalty Rewards Service** &nbsp;|&nbsp; <span style="background: #64748b15; color: #64748b; border: 1px solid #64748b40; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 600;">Support</span> &nbsp;|&nbsp; `v1.0.0` &nbsp;|&nbsp; *NovaTrek Platform Team*

> Manages the NovaTrek Adventures loyalty program including points accrual,

[:material-api: Swagger UI](../services/api/svc-loyalty-rewards.html){ .md-button .md-button--primary }
[:material-file-download: Download OpenAPI Spec](../specs/svc-loyalty-rewards.yaml){ .md-button }
[:material-rocket-launch: Live Service (Dev)](https://ca-svc-loyalty-rewards.blackwater-fd4bc06d.eastus2.azurecontainerapps.io/actuator/health){ .md-button }
[:material-microsoft-azure: Azure Portal](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-loyalty-rewards){ .md-button }
[:material-pipe: CI/CD Pipeline](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/service-ci.yml){ .md-button }
[:material-source-branch: Source Code](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/services/svc-loyalty-rewards){ .md-button }
[:material-language-java: Technology Stack](../technologies.md){ .md-button }

## :material-truck-delivery: Delivery Status

**Delivery Wave:** 5 -- Analytics, Loyalty, and Media

| Stage | Status |
|-------|--------|
| Infrastructure (Bicep) | :white_check_mark: complete |
| Database Schema (Flyway) | :white_check_mark: complete |
| Deployed to Dev | :white_check_mark: complete |
| Smoke Tested | :white_check_mark: complete |
| Deployed to Prod | :material-circle-outline: not-started |


| Pipeline | Status |
|----------|--------|
| CI Pipeline | :white_check_mark: complete |
| CD Pipeline | :white_check_mark: complete |

**Azure Resources (Dev):**

- [:material-microsoft-azure: Container App](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.App/containerApps/ca-svc-loyalty-rewards)
- [:material-database: PostgreSQL Server](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.DBforPostgreSQL/flexibleServers/pg-novatrek-dev-smwd6ded4e3so)
- [:material-text-search: Log Analytics](https://portal.azure.com/#@/resource/subscriptions/19e4c997-f9c1-46a9-b66b-1ad5a8260b8b/resourceGroups/rg-novatrek-dev/providers/Microsoft.OperationalInsights/workspaces/log-novatrek-dev/logs)

---

## :material-map: Integration Context

<div class="diagram-wrap"><a href="../svg/svc-loyalty-rewards--c4-context.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-loyalty-rewards--c4-context.svg" type="image/svg+xml" style="max-width: 100%;">svc-loyalty-rewards C4 context diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-loyalty-rewards.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-loyalty-rewards.yaml` + `cross-service-calls.yaml`</a>


## :material-database: Data Store { #data-store }

### Entity Relationship Diagram

<div class="diagram-wrap"><a href="../svg/svc-loyalty-rewards--erd.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-loyalty-rewards--erd.svg" type="image/svg+xml" style="max-width: 100%;">svc-loyalty-rewards entity relationship diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/metadata/data-stores.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/metadata/data-stores.yaml`</a>

### Overview

| Property | Detail |
|----------|--------|
| **Engine** | Couchbase 7 |
| **Schema** | `loyalty` |
| **Tables** | `members`, `point_transactions`, `tiers`, `redemptions` |
| **Estimated Volume** | ~1,000 transactions/day |
| **Connection Pool** | min 5 / max 15 / idle timeout 30s |
| **Backup Strategy** | XDCR to standby cluster, daily cbbackupmgr |

### Key Features

- Document-oriented member profiles with flexible reward schemas
- N1QL queries for tier recalculation and point aggregation
- Sub-document operations for atomic point balance updates

### Table Reference

#### `members`

*Loyalty member documents with point balances and tier status*

| Column | Type | Constraints |
|--------|------|-------------|
| `document_key` | `String` | members::{guest_id} |
| `guest_id` | `String` | NOT NULL |
| `tier` | `String` | NOT NULL (bronze/silver/gold/platinum) |
| `points_balance` | `Number` | NOT NULL |
| `lifetime_points` | `Number` | NOT NULL |
| `tier_qualified_at` | `ISO8601 String` | NOT NULL |
| `enrolled_at` | `ISO8601 String` | NOT NULL |

**Indexes:**

- `idx_member_tier` on `tier` (N1QL GSI)
- `idx_member_points` on `points_balance DESC` (N1QL GSI)

#### `point_transactions`

*Point earn and redeem transaction ledger*

| Column | Type | Constraints |
|--------|------|-------------|
| `document_key` | `String` | txn::{transaction_id} |
| `transaction_id` | `String` | NOT NULL |
| `guest_id` | `String` | NOT NULL |
| `type` | `String` | NOT NULL (earn/redeem/expire/adjust) |
| `points` | `Number` | NOT NULL |
| `description` | `String` | NOT NULL |
| `reference_id` | `String` | NULL (reservation or trip ID) |
| `created_at` | `ISO8601 String` | NOT NULL |

**Indexes:**

- `idx_txn_guest` on `guest_id, created_at DESC` (N1QL GSI)

#### `redemptions`

*Reward redemption records against point balances*

| Column | Type | Constraints |
|--------|------|-------------|
| `document_key` | `String` | redemption::{redemption_id} |
| `redemption_id` | `String` | NOT NULL |
| `guest_id` | `String` | NOT NULL |
| `reward_type` | `String` | NOT NULL |
| `points_spent` | `Number` | NOT NULL |
| `status` | `String` | NOT NULL |
| `redeemed_at` | `ISO8601 String` | NOT NULL |

**Indexes:**

- `idx_redeem_guest` on `guest_id` (N1QL GSI)


---

## :material-api: Endpoints (5 total)

---

### GET `/members/{guest_id}/balance` -- Get loyalty member balance and tier info { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-loyalty-rewards.html#/Members/getMemberBalance){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-loyalty-rewards--get-members-guest_id-balance.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-loyalty-rewards--get-members-guest_id-balance.svg" type="image/svg+xml" style="max-width: 100%;">GET /members/{guest_id}/balance sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-loyalty-rewards.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-loyalty-rewards.yaml`</a>
<span class="diagram-source-subtitle">Auto-generated baseline — shows standard request flow. For detailed behavioral sequences, see the relevant <a href="/solutions/">solution design</a>.</span>

---

### POST `/members/{guest_id}/earn` -- Award points to a member { .endpoint-post }

[:material-open-in-new: View in Swagger UI](../services/api/svc-loyalty-rewards.html#/Transactions/earnPoints){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-loyalty-rewards--post-members-guest_id-earn.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-loyalty-rewards--post-members-guest_id-earn.svg" type="image/svg+xml" style="max-width: 100%;">POST /members/{guest_id}/earn sequence diagram</object></div>
<span class="diagram-source diagram-source--override"><span class="diagram-source-icon">&#x270E;</span> Architect-authored — overrides auto-generated baseline</span>
<span class="diagram-source-subtitle">Source: <a href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/diagrams/endpoints/svc-loyalty-rewards--post-members-guest_id-earn.puml"><code>architecture/diagrams/endpoints/svc-loyalty-rewards--post-members-guest_id-earn.puml</code></a></span>

---

### POST `/members/{guest_id}/redeem` -- Redeem points for a reward { .endpoint-post }

[:material-open-in-new: View in Swagger UI](../services/api/svc-loyalty-rewards.html#/Transactions/redeemPoints){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-loyalty-rewards--post-members-guest_id-redeem.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-loyalty-rewards--post-members-guest_id-redeem.svg" type="image/svg+xml" style="max-width: 100%;">POST /members/{guest_id}/redeem sequence diagram</object></div>
<span class="diagram-source diagram-source--override"><span class="diagram-source-icon">&#x270E;</span> Architect-authored — overrides auto-generated baseline</span>
<span class="diagram-source-subtitle">Source: <a href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/diagrams/endpoints/svc-loyalty-rewards--post-members-guest_id-redeem.puml"><code>architecture/diagrams/endpoints/svc-loyalty-rewards--post-members-guest_id-redeem.puml</code></a></span>

---

### GET `/members/{guest_id}/transactions` -- List point transactions for a member { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-loyalty-rewards.html#/Transactions/getMemberTransactions){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-loyalty-rewards--get-members-guest_id-transactions.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-loyalty-rewards--get-members-guest_id-transactions.svg" type="image/svg+xml" style="max-width: 100%;">GET /members/{guest_id}/transactions sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-loyalty-rewards.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-loyalty-rewards.yaml`</a>
<span class="diagram-source-subtitle">Auto-generated baseline — shows standard request flow. For detailed behavioral sequences, see the relevant <a href="/solutions/">solution design</a>.</span>

---

### GET `/tiers` -- List all loyalty tiers and their thresholds { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-loyalty-rewards.html#/Tiers/listTiers){ .md-button }

<div class="diagram-wrap"><a href="../svg/svc-loyalty-rewards--get-tiers.svg" target="_blank" class="diagram-expand" title="Open in new tab">⤢</a><object data="../svg/svc-loyalty-rewards--get-tiers.svg" type="image/svg+xml" style="max-width: 100%;">GET /tiers sequence diagram</object></div>
<a class="diagram-source" href="https://github.com/christopherblaisdell/continuous-architecture-platform-poc/blob/main/architecture/specs/svc-loyalty-rewards.yaml" title="View data source"><span class="diagram-source-icon">&#x2699;</span> Generated from `architecture/specs/svc-loyalty-rewards.yaml`</a>
<span class="diagram-source-subtitle">Auto-generated baseline — shows standard request flow. For detailed behavioral sequences, see the relevant <a href="/solutions/">solution design</a>.</span>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Guest Portal](../../applications/web-guest-portal/) | Guest Profile, Loyalty Dashboard |
| [Adventure App](../../applications/app-guest-mobile/) | Earn Loyalty Points |

---

## :material-broadcast-off: Events Consumed

| Event | Producer | Channel |
|-------|----------|---------|
| [`guest.registered`](/events/#guestregistered) | [svc-guest-profiles](../svc-guest-profiles/) | `novatrek.guest-identity.guest.registered` |
