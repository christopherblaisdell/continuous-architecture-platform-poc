// ===========================================================================
// Managed Identity + Role Assignments — NovaTrek
// User-assigned managed identity for microservices with RBAC to
// ACR, Key Vault, Service Bus, and PostgreSQL.
// ===========================================================================

@description('Identity name')
param name string

@description('Azure region')
param location string

@description('Tags to apply')
param tags object = {}

@description('Container Registry resource ID for AcrPull role')
param acrId string = ''

@description('Key Vault resource ID for Key Vault Secrets User role')
param keyVaultId string = ''

@description('Service Bus namespace resource ID for data sender/receiver roles')
param serviceBusId string = ''

// ---------------------------------------------------------------------------
// Role Definition IDs (built-in Azure roles)
// ---------------------------------------------------------------------------

var acrPullRoleId = '7f951dda-4ed3-4680-a7ca-43fe172d538d'
var keyVaultSecretsUserRoleId = '4633458b-17de-408a-b874-0445c86b69e6'
var serviceBusDataSenderRoleId = '69a216fc-b8fb-44d8-bc22-1f3c2cd27a39'
var serviceBusDataReceiverRoleId = '4f6d3b9b-027b-4f4c-9142-0e5a2a2247e0'

// ---------------------------------------------------------------------------
// User-Assigned Managed Identity
// ---------------------------------------------------------------------------

resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: name
  location: location
  tags: tags
}

// ---------------------------------------------------------------------------
// ACR Pull Role Assignment
// ---------------------------------------------------------------------------

resource acrPull 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(acrId)) {
  name: guid(acrId, identity.id, acrPullRoleId)
  scope: resourceGroup()
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', acrPullRoleId)
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// ---------------------------------------------------------------------------
// Key Vault Secrets User Role Assignment
// ---------------------------------------------------------------------------

resource kvSecretsUser 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(keyVaultId)) {
  name: guid(keyVaultId, identity.id, keyVaultSecretsUserRoleId)
  scope: resourceGroup()
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', keyVaultSecretsUserRoleId)
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// ---------------------------------------------------------------------------
// Service Bus Data Sender Role Assignment
// ---------------------------------------------------------------------------

resource sbSender 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(serviceBusId)) {
  name: guid(serviceBusId, identity.id, serviceBusDataSenderRoleId)
  scope: resourceGroup()
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', serviceBusDataSenderRoleId)
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// ---------------------------------------------------------------------------
// Service Bus Data Receiver Role Assignment
// ---------------------------------------------------------------------------

resource sbReceiver 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(serviceBusId)) {
  name: guid(serviceBusId, identity.id, serviceBusDataReceiverRoleId)
  scope: resourceGroup()
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', serviceBusDataReceiverRoleId)
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// ---------------------------------------------------------------------------
// Outputs
// ---------------------------------------------------------------------------

@description('Managed identity resource ID')
output id string = identity.id

@description('Managed identity name')
output name string = identity.name

@description('Managed identity principal ID')
output principalId string = identity.properties.principalId

@description('Managed identity client ID')
output clientId string = identity.properties.clientId
