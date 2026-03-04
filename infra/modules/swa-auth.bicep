// ===========================================================================
// Azure AD Authentication for Static Web App (Optional)
// ===========================================================================
// Deploy this ONLY when you need private documentation behind Azure AD.
//
// Usage:
//   az deployment group create \
//     --resource-group rg-cap-docs-prod \
//     --template-file infra/modules/swa-auth.bicep \
//     --parameters staticWebAppName=swa-cap-docs-prod \
//                   tenantId=<your-azure-ad-tenant-id> \
//                   clientId=<your-app-registration-client-id>
// ===========================================================================

targetScope = 'resourceGroup'

@description('Name of the existing Static Web App')
param staticWebAppName string

@description('Azure AD Tenant ID')
param tenantId string

@description('Azure AD App Registration Client ID')
param clientId string

// Reference the existing Static Web App
resource staticWebApp 'Microsoft.Web/staticSites@2023-12-01' existing = {
  name: staticWebAppName
}

// Configure Azure AD authentication
resource authSettings 'Microsoft.Web/staticSites/config@2023-12-01' = {
  parent: staticWebApp
  name: 'authsettings'
  properties: {
    enabled: true
    runtimeVersion: '~1'
    unauthenticatedClientAction: 'RedirectToLoginPage'
    tokenStoreEnabled: true
    defaultProvider: 'AzureActiveDirectory'
    clientId: clientId
    issuer: 'https://login.microsoftonline.com/${tenantId}/v2.0'
  }
}
