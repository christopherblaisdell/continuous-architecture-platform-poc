// ===========================================================================
// Azure Key Vault — NovaTrek
// Centralized secret management: DB connection strings, JWT signing keys,
// API keys, Service Bus connections. Managed identity access only.
// ===========================================================================

@description('Key Vault name (must be globally unique)')
param name string

@description('Azure region')
param location string

@description('Tags to apply')
param tags object = {}

@description('Enable soft delete')
param enableSoftDelete bool = true

@description('Soft delete retention in days')
param softDeleteRetentionInDays int = 7

@description('Enable purge protection (recommended for prod)')
param enablePurgeProtection bool = false

@description('Enable RBAC authorization (recommended over access policies)')
param enableRbacAuthorization bool = true

@description('Tenant ID for Azure AD')
param tenantId string = subscription().tenantId

// ---------------------------------------------------------------------------
// Key Vault
// ---------------------------------------------------------------------------

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: name
  location: location
  tags: tags
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: tenantId
    enableSoftDelete: enableSoftDelete
    softDeleteRetentionInDays: softDeleteRetentionInDays
    enablePurgeProtection: enablePurgeProtection ? true : null
    enableRbacAuthorization: enableRbacAuthorization
    enabledForDeployment: false
    enabledForDiskEncryption: false
    enabledForTemplateDeployment: false
  }
}

// ---------------------------------------------------------------------------
// Diagnostic Settings (audit secret access)
// ---------------------------------------------------------------------------

@description('Log Analytics workspace ID for audit logging (optional)')
param logAnalyticsWorkspaceId string = ''

resource diagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = if (!empty(logAnalyticsWorkspaceId)) {
  name: '${name}-diagnostics'
  scope: keyVault
  properties: {
    workspaceId: logAnalyticsWorkspaceId
    logs: [
      {
        categoryGroup: 'audit'
        enabled: true
        retentionPolicy: {
          enabled: false
          days: 0
        }
      }
    ]
  }
}

// ---------------------------------------------------------------------------
// Outputs
// ---------------------------------------------------------------------------

@description('Key Vault resource ID')
output id string = keyVault.id

@description('Key Vault name')
output name string = keyVault.name

@description('Key Vault URI')
output vaultUri string = keyVault.properties.vaultUri
