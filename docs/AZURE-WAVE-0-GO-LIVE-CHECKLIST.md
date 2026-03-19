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
- [ ] `az containerapp env show -n cae-novatrek-dev -g rg-novatrek-dev` returns successfully.

## 1. External Prerequisites

### Azure subscription and guardrails
- [ ] Azure subscription is active and billing is linked.
- [ ] Monthly budgets are configured before deployment (recommended: dev $50, prod $200).
- [ ] Resource providers are registered:
  - [ ] `Microsoft.App`
  - [ ] `Microsoft.DBforPostgreSQL`
  - [ ] `Microsoft.ServiceBus`
  - [ ] `Microsoft.KeyVault`
  - [ ] `Microsoft.ContainerRegistry`

### DNS planning
- [ ] Cloudflare plan documented for `api.novatrek.cc`.
- [ ] Cloudflare plan documented for `api-dev.novatrek.cc`.
- [ ] Cloudflare wildcard strategy documented for `*.pr.novatrek.cc`.

## 2. GitHub and Identity Setup

### Environments and protection
- [ ] GitHub environment `dev` exists.
- [ ] GitHub environment `prod` exists.
- [ ] `prod` has required reviewer approval rule.

### OIDC federation and secrets
- [ ] Azure managed identity for GitHub OIDC exists.
- [ ] Federated credential configured for `repo:{org}/{repo}:environment:dev`.
- [ ] Federated credential configured for `repo:{org}/{repo}:environment:prod`.
- [ ] Repository or environment secret `AZURE_CLIENT_ID` is set.
- [ ] Repository or environment secret `AZURE_TENANT_ID` is set.
- [ ] Repository or environment secret `AZURE_SUBSCRIPTION_ID` is set.
- [ ] Repository or environment secret `POSTGRES_ADMIN_PASSWORD` is set.

## 3. Wave 0 Artifact Verification

Confirm all expected modules and workflows are present and in scope.

### Bicep modules (foundation stack)
- [ ] [infra/modules/container-apps-env.bicep](../infra/modules/container-apps-env.bicep)
- [ ] [infra/modules/container-registry.bicep](../infra/modules/container-registry.bicep)
- [ ] [infra/modules/postgresql.bicep](../infra/modules/postgresql.bicep)
- [ ] [infra/modules/key-vault.bicep](../infra/modules/key-vault.bicep)
- [ ] [infra/modules/monitoring.bicep](../infra/modules/monitoring.bicep)
- [ ] [infra/modules/service-bus.bicep](../infra/modules/service-bus.bicep)

### Parameter files
- [ ] [infra/parameters/dev.platform.bicepparam](../infra/parameters/dev.platform.bicepparam)
- [ ] [infra/parameters/prod.platform.bicepparam](../infra/parameters/prod.platform.bicepparam)

### Required workflows
- [ ] [infra deploy workflow](../.github/workflows/infra-deploy.yml)
- [ ] [service CI reusable workflow](../.github/workflows/service-ci.yml)
- [ ] [service CD reusable workflow](../.github/workflows/service-cd.yml)
- [ ] [nightly stop dev workflow](../.github/workflows/nightly-stop-dev.yml)
- [ ] [nightly start dev workflow](../.github/workflows/nightly-start-dev.yml)
- [ ] [ephemeral environment workflow](../.github/workflows/ephemeral-env.yml)
- [ ] [database migration workflow](../.github/workflows/db-migrate.yml)

## 4. Preflight Validation

- [ ] Bicep compiles locally for foundation template:

```bash
az bicep build --file infra/platform.bicep --stdout > /dev/null
```

- [ ] Optional what-if runs for dev (if resource group exists):

```bash
az deployment group what-if \
  --resource-group rg-novatrek-dev \
  --template-file infra/platform.bicep \
  --parameters infra/parameters/dev.platform.bicepparam
```

## 5. Execute Wave 0 Deploy

### Option A: GitHub Actions (recommended)
- [ ] Manually dispatch [infra deploy workflow](../.github/workflows/infra-deploy.yml) with `environment=dev`.
- [ ] Confirm `Validate Bicep` job passed.
- [ ] Confirm `Deploy Infrastructure` job passed.

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

- [ ] Container Apps environment exists:

```bash
az containerapp env show -n cae-novatrek-dev -g rg-novatrek-dev \
  --query "{defaultDomain:properties.defaultDomain,provisioningState:properties.provisioningState}" -o table
```

- [ ] PostgreSQL server is provisioned and reachable.
- [ ] ACR exists and login works.
- [ ] Key Vault exists and allows managed identity-based access.
- [ ] Service Bus namespace exists.
- [ ] Log Analytics workspace exists.
- [ ] Application Insights exists.

## 7. Wave 0 Sign Off

- [ ] Capture resource inventory (`az resource list -g rg-novatrek-dev -o table`).
- [ ] Capture deployment outputs and store in ticket/notes.
- [ ] Mark Wave 0 complete in roadmap tracking.
- [ ] Create Wave 1 kickoff issue (Guest Identity + Product Catalog).
