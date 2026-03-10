// ===========================================================================
// Azure Container Apps Environment
// Provides the managed environment for running containerized workloads.
// ===========================================================================

@description('Name of the Container Apps Environment')
param name string

@description('Azure region')
param location string

@description('Tags to apply')
param tags object = {}

@description('Log Analytics workspace name (used to retrieve shared key)')
param logAnalyticsWorkspaceName string

// ---------------------------------------------------------------------------
// Reference existing Log Analytics workspace to retrieve keys
// ---------------------------------------------------------------------------

resource logAnalyticsRef 'Microsoft.OperationalInsights/workspaces@2023-09-01' existing = {
  name: logAnalyticsWorkspaceName
}

// ---------------------------------------------------------------------------
// Container Apps Environment
// ---------------------------------------------------------------------------

resource containerAppsEnv 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: name
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalyticsRef.properties.customerId
        sharedKey: logAnalyticsRef.listKeys().primarySharedKey
      }
    }
  }
}

// ---------------------------------------------------------------------------
// Outputs
// ---------------------------------------------------------------------------

@description('Container Apps Environment resource ID')
output id string = containerAppsEnv.id

@description('Container Apps Environment name')
output name string = containerAppsEnv.name

@description('Default domain for the Container Apps Environment')
output defaultDomain string = containerAppsEnv.properties.defaultDomain

@description('Log Analytics workspace ID used')
output logAnalyticsWorkspaceId string = logAnalyticsRef.id
