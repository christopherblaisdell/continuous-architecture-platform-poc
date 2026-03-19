# Azure Wave 0 Go Live Checklist

Date: 2026-03-19
Status: Active
Scope: Wave 0 foundation only (shared infrastructure, no microservices)

Source references:
- [docs/AZURE-IMPLEMENTATION-PLAN.md](AZURE-IMPLEMENTATION-PLAN.md)
- [Wave 0 section](AZURE-IMPLEMENTATION-PLAN.md#wave-0--foundation-prerequisites)
- [Prerequisites and open items](AZURE-IMPLEMENTATION-PLAN.md#18-prerequisites-and-open-items)
- [Ready to Start Wave 0 checklist](AZURE-IMPLEMENTATION-PLAN.md#checklist-ready-to-start-wave-0)

Done condition:
- [x] `az containerapp env show -n cae-novatrek-dev -g rg-novatrek-dev` returns successfully.

## 1. External Prerequisites

### Azure subscription and guardrails
- [x] Azure subscription is active and billing is linked.
- [x] Monthly budgets are configured before deployment (recommended: dev $50, prod $200).
- [x] Resource providers are registered:
  - [x] `Microsoft.App`
  - [x] `Microsoft.DBforPostgreSQL`
  - [x] `Microsoft.ServiceBus`
  - [x] `Microsoft.KeyVault`
  - [x] `Microsoft.ContainerRegistry`

### DNS planning
- [ ] Cloudflare plan documented for `api.novatrek.cc`.
- [ ] Cloudflare plan documented for `api-dev.novatrek.cc`.
- [ ] Cloudflare wildcard strategy documented for `*.pr.novatrek.cc`.

## 2. GitHub and Identity Setup

### Environments and protection
- [x] GitHub environment `dev` exists.
- [x] GitHub environment `prod` exists.
- [x] `prod` has required reviewer approval rule.

### OIDC federation and secrets
- [x] Azure managed identity for GitHub OIDC exists.
- [x] Federated credential configured for `repo:{org}/{repo}:environment:dev`.
- [x] Federated credential configured for `repo:{org}/{repo}:environment:prod`.
- [x] Federated credential configured for `repo:{org}/{repo}:ref:refs/heads/main`.
- [x] Federated credential configured for `repo:{org}/{repo}:pull_request`.
- [x] Repository or environment secret `AZURE_CLIENT_ID` is set.
- [x] Repository or environment secret `AZURE_TENANT_ID` is set.
- [x] Repository or environment secret `AZURE_SUBSCRIPTION_ID` is set.
- [x] Repository or environment secret `POSTGRES_ADMIN_PASSWORD` is set.

## 3. Wave 0 Artifact Verification

Confirm all expected modules and workflows are present and in scope.

### Bicep modules (foundation stack)
- [x] [infra/modules/container-apps-env.bicep](../infra/modules/container-apps-env.bicep)
- [x] [infra/modules/container-registry.bicep](../infra/modules/container-registry.bicep)
- [x] [infra/modules/postgresql.bicep](../infra/modules/postgresql.bicep)
- [x] [infra/modules/key-vault.bicep](../infra/modules/key-vault.bicep)
- [x] [infra/modules/monitoring.bicep](../infra/modules/monitoring.bicep)
- [x] [infra/modules/service-bus.bicep](../infra/modules/service-bus.bicep)

### Parameter files
- [x] [infra/parameters/dev.platform.bicepparam](../infra/parameters/dev.platform.bicepparam)
- [x] [infra/parameters/prod.platform.bicepparam](../infra/parameters/prod.platform.bicepparam)

### Required workflows
- [x] [infra deploy workflow](../.github/workflows/infra-deploy.yml)
- [x] [service CI reusable workflow](../.github/workflows/service-ci.yml)
- [x] [service CD reusable workflow](../.github/workflows/service-cd.yml)
- [x] [nightly stop dev workflow](../.github/workflows/nightly-stop-dev.yml)
- [x] [nightly start dev workflow](../.github/workflows/nightly-start-dev.yml)
- [x] [ephemeral environment workflow](../.github/workflows/ephemeral-env.yml)
- [x] [database migration workflow](../.github/workflows/db-migrate.yml)

## 4. Preflight Validation

- [x] Bicep compiles locally for foundation template:

```bash
az bicep build --file infra/platform.bicep --stdout > /dev/null
```

- [x] Optional what-if runs for dev (if resource group exists):

```bash
az deployment group what-if \
  --resource-group rg-novatrek-dev \
  --template-file infra/platform.bicep \
  --parameters infra/parameters/dev.platform.bicepparam
```

## 5. Execute Wave 0 Deploy

### Option A: GitHub Actions (recommended)
- [x] Manually dispatch [infra deploy workflow](../.github/workflows/infra-deploy.yml) with `environment=dev`.
- [x] Confirm `Validate Bicep` job passed.
- [x] Confirm `Deploy Infrastructure` job passed.

### Option B: CLI deployment (fallback)
- [ ] Create resource group:

```bash
az group create --name rg-novatrek-dev --location eastus2 \
  --tags project=novatrek-adventures environment=dev managedBy=bicep
```

- [ ] Deploy template:

```bash
az deployment group create \
  --resource-group rg-novatrek-dev \
  --template-file infra/platform.bicep \
  --parameters infra/parameters/dev.platform.bicepparam \
  --name deploy-wave0-dev
```

## 6. Post Deploy Validation

- [x] Container Apps environment exists:

```bash
az containerapp env show -n cae-novatrek-dev -g rg-novatrek-dev \
  --query "{defaultDomain:properties.defaultDomain,provisioningState:properties.provisioningState}" -o table
```

- [x] PostgreSQL server is provisioned and reachable.
- [x] ACR exists and login works.
- [x] Key Vault exists and allows managed identity-based access.
- [x] Service Bus namespace exists.
- [x] Log Analytics workspace exists.
- [x] Application Insights exists.

## 7. Wave 0 Sign Off

- [x] Capture resource inventory (`az resource list -g rg-novatrek-dev -o table`).
- [ ] Capture deployment outputs and store in ticket/notes.
- [ ] Mark Wave 0 complete in roadmap tracking.
- [ ] Create Wave 1 kickoff issue (Guest Identity + Product Catalog).
