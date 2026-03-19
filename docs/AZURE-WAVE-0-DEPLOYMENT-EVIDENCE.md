# Azure Wave 0 Deployment Evidence

Date: 2026-03-19
Status: Complete
Scope: Wave 0 foundation deployment evidence for rg-novatrek-dev

## Workflow Evidence

Deployment workflow:
- Name: Infrastructure Deploy
- Run ID: 23310894775
- URL: https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/runs/23310894775
- Status: completed
- Conclusion: success
- Created: 2026-03-19T18:35:46Z
- Updated: 2026-03-19T18:40:02Z

## Done Condition Evidence

Command:

```bash
az containerapp env show -n cae-novatrek-dev -g rg-novatrek-dev \
  --query '{name:name,defaultDomain:properties.defaultDomain,provisioningState:properties.provisioningState}' -o json
```

Observed result:
- name: `cae-novatrek-dev`
- defaultDomain: `blackwater-fd4bc06d.eastus2.azurecontainerapps.io`
- provisioningState: `Succeeded`

## Foundation Resources Verified

Core Wave 0 resources present:

- `Microsoft.App/managedEnvironments`: `cae-novatrek-dev`
- `Microsoft.ContainerRegistry/registries`: `crnovatrekdev`
- `Microsoft.DBforPostgreSQL/flexibleServers`: `pg-novatrek-dev-smwd6ded4e3so`
- `Microsoft.KeyVault/vaults`: `kv-novatrek-dev`
- `Microsoft.ServiceBus/namespaces`: `sb-novatrek-dev`
- `Microsoft.OperationalInsights/workspaces`: `log-novatrek-dev`
- `Microsoft.Insights/components`: `appi-novatrek-dev`
- `Microsoft.Storage/storageAccounts`: `stnovatrekdev`
- `Microsoft.ManagedIdentity/userAssignedIdentities`: `id-novatrek-dev`

## Budget Guardrails Verified

Budgets currently configured at subscription scope:

- `budget-novatrek-dev`: 50 monthly
- `novatrek-dev-monthly`: 50 monthly
- `novatrek-prod-monthly`: 200 monthly

## Notes

The resource group also contains container apps for services beyond strict Wave 0 scope. This does not invalidate Wave 0 completion criteria because the required shared foundation resources and done condition are present and healthy.
