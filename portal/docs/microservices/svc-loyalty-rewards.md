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

---

## :material-database: Data Store

| Property | Detail |
|----------|--------|
| **Engine** | Couchbase 7 |
| **Schema** | `loyalty` |
| **Primary Tables** | `members`, `point_transactions`, `tiers`, `redemptions` |
| **Key Features** | Document-oriented member profiles with flexible reward schemas | N1QL queries for tier recalculation and point aggregation | Sub-document operations for atomic point balance updates |
| **Estimated Volume** | ~1,000 transactions/day |

---

## :material-api: Endpoints (5 total)

---

### GET `/members/{guest_id}/balance` -- Get loyalty member balance and tier info { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-loyalty-rewards.html#/Members/getMemberBalance){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-loyalty-rewards--get-members-guest_id-balance.svg" type="image/svg+xml" style="max-width: 100%;">GET /members/{guest_id}/balance sequence diagram</object></div>

---

### POST `/members/{guest_id}/earn` -- Award points to a member { .endpoint-post }

[:material-open-in-new: View in Swagger UI](../services/api/svc-loyalty-rewards.html#/Transactions/earnPoints){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-loyalty-rewards--post-members-guest_id-earn.svg" type="image/svg+xml" style="max-width: 100%;">POST /members/{guest_id}/earn sequence diagram</object></div>

---

### POST `/members/{guest_id}/redeem` -- Redeem points for a reward { .endpoint-post }

[:material-open-in-new: View in Swagger UI](../services/api/svc-loyalty-rewards.html#/Transactions/redeemPoints){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-loyalty-rewards--post-members-guest_id-redeem.svg" type="image/svg+xml" style="max-width: 100%;">POST /members/{guest_id}/redeem sequence diagram</object></div>

---

### GET `/members/{guest_id}/transactions` -- List point transactions for a member { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-loyalty-rewards.html#/Transactions/getMemberTransactions){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-loyalty-rewards--get-members-guest_id-transactions.svg" type="image/svg+xml" style="max-width: 100%;">GET /members/{guest_id}/transactions sequence diagram</object></div>

---

### GET `/tiers` -- List all loyalty tiers and their thresholds { .endpoint-get }

[:material-open-in-new: View in Swagger UI](../services/api/svc-loyalty-rewards.html#/Tiers/listTiers){ .md-button }

<div style="overflow-x: auto; width: 100%;"><object data="../svg/svc-loyalty-rewards--get-tiers.svg" type="image/svg+xml" style="max-width: 100%;">GET /tiers sequence diagram</object></div>

---

## :material-cellphone-link: Consuming Applications

| Application | Screens Using This Service |
|-------------|---------------------------|
| [Guest Portal](../applications/web-guest-portal/) | Guest Profile, Loyalty Dashboard |
| [Adventure App](../applications/app-guest-mobile/) | Earn Loyalty Points |
