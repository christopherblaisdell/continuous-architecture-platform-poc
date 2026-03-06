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

@description('Log Analytics workspace ID for diagnostics (optional)')
param logAnalyticsWorkspaceId string = ''

// ---------------------------------------------------------------------------
// Log Analytics Workspace (created if not provided)
// ---------------------------------------------------------------------------

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = if (empty(logAnalyticsWorkspaceId)) {
  name: '${name}-logs'
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

var effectiveLogAnalyticsId = !empty(logAnalyticsWorkspaceId) ? logAnalyticsWorkspaceId : logAnalytics.id

// Need to retrieve the shared key for the Container Apps Environment
resource logAnalyticsRef 'Microsoft.OperationalInsights/workspaces@2023-09-01' existing = if (empty(logAnalyticsWorkspaceId)) {
  name: '${name}-logs'
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
        customerId: empty(logAnalyticsWorkspaceId) ? logAnalytics.properties.customerId : ''
        sharedKey: empty(logAnalyticsWorkspaceId) ? logAnalytics.listKeys().primarySharedKey : ''
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
output logAnalyticsWorkspaceId string = effectiveLogAnalyticsId
