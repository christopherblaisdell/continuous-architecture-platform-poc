// ===========================================================================
// NovaTrek Adventures — Platform Infrastructure Orchestrator
// ===========================================================================
// Composes all Bicep modules to deploy the full NovaTrek microservices
// platform: ACA environment, PostgreSQL, Service Bus, Key Vault, Redis,
// ACR, monitoring, managed identity, and all microservices.
//
// Usage:
//   az deployment group create \
//     --resource-group rg-novatrek-{env} \
//     --template-file infra/platform.bicep \
//     --parameters infra/parameters/{env}.platform.bicepparam
// ===========================================================================

targetScope = 'resourceGroup'

// ---------------------------------------------------------------------------
// Core Parameters
// ---------------------------------------------------------------------------

@description('Environment identifier')
@allowed(['prod', 'dev', 'ephemeral'])
param environment string

@description('Azure region')
param location string = resourceGroup().location

@description('Services to deploy (incremental delivery — empty = infra only)')
param servicesToDeploy array = []

@description('PostgreSQL administrator password')
@secure()
param postgresAdminPassword string

@description('Budget start date (ISO 8601, first of month)')
param budgetStartDate string = '2026-04-01'

@description('Monthly budget amount in USD')
param budgetAmount int = 50

@description('Deploy Redis cache (required by svc-scheduling-orchestrator)')
param deployRedis bool = false

@description('Deploy Azure Service Bus')
param deployServiceBus bool = true

@description('Deploy budget alert')
param deployBudget bool = true

@description('Location override for PostgreSQL (some subscriptions restrict certain regions)')
param postgresLocation string = location

// ---------------------------------------------------------------------------
// Variables
// ---------------------------------------------------------------------------

var defaultTags = {
  project: 'novatrek-adventures'
  environment: environment
  managedBy: 'bicep'
}

var acrName = 'crnovatrek${environment}'
var envSuffix = 'novatrek-${environment}'

// NovaTrek event topics (from AsyncAPI specs)
var eventTopics = [
  'novatrek.operations.checkin.completed'
  'novatrek.booking.reservation.created'
  'novatrek.booking.reservation.status-changed'
  'novatrek.support.payment.processed'
  'novatrek.identity.guest.updated'
  'novatrek.safety.waiver.signed'
  'novatrek.safety.emergency.activated'
  'novatrek.operations.wildlife.sighted'
]

// Database names — one per microservice schema
var allDatabases = [
  'checkin'
  'scheduling'
  'guests'
  'reservations'
  'payments'
  'catalog'
  'trails'
  'safety'
  'gear'
  'guides'
  'transport'
  'notifications'
  'loyalty'
  'media'
  'analytics'
  'weather'
  'location'
  'partners'
  'procurement'
]

// Blob containers
var blobContainers = [
  'media-assets'
  'db-backups'
  'exports'
]

// ---------------------------------------------------------------------------
// Monitoring (deploy first — other modules reference Log Analytics)
// ---------------------------------------------------------------------------

module monitoring 'modules/monitoring.bicep' = {
  name: 'deploy-monitoring'
  params: {
    environment: environment
    location: location
    tags: defaultTags
    retentionInDays: environment == 'prod' ? 90 : 30
  }
}

// ---------------------------------------------------------------------------
// Container Registry
// ---------------------------------------------------------------------------

module acr 'modules/container-registry.bicep' = {
  name: 'deploy-acr'
  params: {
    name: acrName
    location: location
    tags: defaultTags
    sku: 'Basic'
  }
}

// ---------------------------------------------------------------------------
// Container Apps Environment
// ---------------------------------------------------------------------------

module acaEnv 'modules/container-apps-env.bicep' = {
  name: 'deploy-aca-env'
  params: {
    name: 'cae-${envSuffix}'
    location: location
    tags: defaultTags
    logAnalyticsWorkspaceName: monitoring.outputs.logAnalyticsName
  }
}

// ---------------------------------------------------------------------------
// Key Vault
// ---------------------------------------------------------------------------

module keyVault 'modules/key-vault.bicep' = {
  name: 'deploy-kv'
  params: {
    name: 'kv-${envSuffix}'
    location: location
    tags: defaultTags
    enablePurgeProtection: environment == 'prod'
    logAnalyticsWorkspaceId: monitoring.outputs.logAnalyticsId
  }
}

// ---------------------------------------------------------------------------
// PostgreSQL Flexible Server
// ---------------------------------------------------------------------------

var postgresName = 'pg-${envSuffix}-${uniqueString(resourceGroup().id)}'

module postgresql 'modules/postgresql.bicep' = {
  name: 'deploy-psql'
  params: {
    name: postgresName
    location: postgresLocation
    tags: defaultTags
    skuName: environment == 'prod' ? 'Standard_B2s' : 'Standard_B1ms'
    skuTier: 'Burstable'
    storageSizeGB: environment == 'prod' ? 64 : 32
    backupRetentionDays: environment == 'prod' ? 35 : 7
    administratorLoginPassword: postgresAdminPassword
    databases: allDatabases
  }
}

// ---------------------------------------------------------------------------
// Azure Service Bus
// ---------------------------------------------------------------------------

module serviceBus 'modules/service-bus.bicep' = if (deployServiceBus) {
  name: 'deploy-sb'
  params: {
    name: 'sb-${envSuffix}'
    location: location
    tags: defaultTags
    sku: environment == 'prod' ? 'Standard' : 'Basic'
    topics: eventTopics
  }
}

// ---------------------------------------------------------------------------
// Azure Cache for Redis (conditional — Wave 3+)
// ---------------------------------------------------------------------------

module redis 'modules/redis.bicep' = if (deployRedis) {
  name: 'deploy-redis'
  params: {
    name: 'redis-${envSuffix}'
    location: location
    tags: defaultTags
    skuName: environment == 'prod' ? 'Standard' : 'Basic'
    skuCapacity: environment == 'prod' ? 1 : 0
  }
}

// ---------------------------------------------------------------------------
// Azure Blob Storage
// ---------------------------------------------------------------------------

module storage 'modules/storage-account.bicep' = {
  name: 'deploy-storage'
  params: {
    name: 'stnovatrek${environment}'
    location: location
    tags: defaultTags
    containers: blobContainers
    enableLifecyclePolicy: environment == 'prod'
  }
}

// ---------------------------------------------------------------------------
// Managed Identity (shared by all microservices)
// ---------------------------------------------------------------------------

module identity 'modules/managed-identity.bicep' = {
  name: 'deploy-identity'
  params: {
    name: 'id-${envSuffix}'
    location: location
    tags: defaultTags
    acrId: acr.outputs.id
    keyVaultId: keyVault.outputs.id
    serviceBusId: ''
  }
}

// ---------------------------------------------------------------------------
// Budget Alert
// ---------------------------------------------------------------------------

module budget 'modules/budget.bicep' = if (deployBudget) {
  name: 'deploy-budget'
  params: {
    environment: environment
    amount: budgetAmount
    startDate: budgetStartDate
  }
}

// ---------------------------------------------------------------------------
// Microservices (conditionally deployed based on servicesToDeploy)
// ---------------------------------------------------------------------------

module services 'modules/container-app.bicep' = [for svc in servicesToDeploy: {
  name: 'deploy-${svc}'
  params: {
    name: svc
    location: location
    tags: defaultTags
    environmentId: acaEnv.outputs.id
    registryServer: acr.outputs.loginServer
    image: '${acr.outputs.loginServer}/${svc}:latest'
    managedIdentityId: identity.outputs.id
    minReplicas: 0
    maxReplicas: environment == 'prod' ? 5 : 2
    env: [
      { name: 'SPRING_PROFILES_ACTIVE', value: environment }
      { name: 'APPLICATIONINSIGHTS_CONNECTION_STRING', value: monitoring.outputs.appInsightsConnectionString }
      { name: 'DATABASE_HOST', value: postgresql.outputs.fqdn }
      { name: 'DATABASE_NAME', value: replace(replace(svc, 'svc-', ''), '-', '_') }
    ]
  }
}]

// ---------------------------------------------------------------------------
// Outputs
// ---------------------------------------------------------------------------

@description('Container Apps Environment default domain')
output acaDefaultDomain string = acaEnv.outputs.defaultDomain

@description('Container Registry login server')
output acrLoginServer string = acr.outputs.loginServer

@description('PostgreSQL server FQDN')
output postgresqlFqdn string = postgresql.outputs.fqdn

@description('Key Vault URI')
output keyVaultUri string = keyVault.outputs.vaultUri

@description('Service Bus namespace name')
output serviceBusName string = deployServiceBus ? 'sb-${envSuffix}' : ''

@description('Log Analytics workspace name')
output logAnalyticsName string = monitoring.outputs.logAnalyticsName

@description('Application Insights name')
output appInsightsName string = monitoring.outputs.appInsightsName

@description('Managed Identity client ID')
output managedIdentityClientId string = identity.outputs.clientId

@description('Blob storage endpoint')
output blobEndpoint string = storage.outputs.blobEndpoint

@description('Deployed service FQDNs')
output serviceFqdns array = [for (svc, i) in servicesToDeploy: {
  service: svc
  fqdn: services[i].outputs.fqdn
}]
