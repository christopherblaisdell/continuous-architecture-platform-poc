// ===========================================================================
// Azure Database for PostgreSQL — Flexible Server
// Hosts all NovaTrek microservice schemas in a single instance (dev)
// or dedicated instances for critical services (prod).
// ===========================================================================

@description('Server name')
param name string

@description('Azure region')
param location string

@description('Tags to apply')
param tags object = {}

@description('SKU name (e.g., Standard_B1ms, Standard_B2s)')
param skuName string = 'Standard_B1ms'

@description('SKU tier')
@allowed(['Burstable', 'GeneralPurpose', 'MemoryOptimized'])
param skuTier string = 'Burstable'

@description('Storage size in GB')
param storageSizeGB int = 32

@description('PostgreSQL version')
@allowed(['14', '15', '16'])
param version string = '15'

@description('Administrator login name')
param administratorLogin string = 'novatrekadmin'

@description('Administrator login password')
@secure()
param administratorLoginPassword string

@description('Enable high availability (prod only)')
param highAvailability bool = false

@description('Backup retention days')
param backupRetentionDays int = 7

@description('Enable geo-redundant backup')
param geoRedundantBackup bool = false

@description('Database names to create (one per microservice schema)')
param databases array = []

@description('Enable Azure AD authentication')
param enableAadAuth bool = false

// ---------------------------------------------------------------------------
// PostgreSQL Flexible Server
// ---------------------------------------------------------------------------

resource server 'Microsoft.DBforPostgreSQL/flexibleServers@2023-12-01-preview' = {
  name: name
  location: location
  tags: tags
  sku: {
    name: skuName
    tier: skuTier
  }
  properties: {
    version: version
    administratorLogin: administratorLogin
    administratorLoginPassword: administratorLoginPassword
    storage: {
      storageSizeGB: storageSizeGB
    }
    backup: {
      backupRetentionDays: backupRetentionDays
      geoRedundantBackup: geoRedundantBackup ? 'Enabled' : 'Disabled'
    }
    highAvailability: {
      mode: highAvailability ? 'ZoneRedundant' : 'Disabled'
    }
    authConfig: {
      activeDirectoryAuth: enableAadAuth ? 'Enabled' : 'Disabled'
      passwordAuth: 'Enabled'
    }
  }
}

// ---------------------------------------------------------------------------
// Firewall Rule — Allow Azure Services
// ---------------------------------------------------------------------------

resource allowAzure 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2023-12-01-preview' = {
  parent: server
  name: 'AllowAzureServices'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

// ---------------------------------------------------------------------------
// PostGIS Extension (required by svc-trail-management)
// ---------------------------------------------------------------------------

resource postgisExtension 'Microsoft.DBforPostgreSQL/flexibleServers/configurations@2023-12-01-preview' = {
  parent: server
  name: 'azure.extensions'
  properties: {
    value: 'POSTGIS,UUID-OSSP'
    source: 'user-override'
  }
}

// ---------------------------------------------------------------------------
// Databases (one per microservice schema)
// ---------------------------------------------------------------------------

resource dbs 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2023-12-01-preview' = [for db in databases: {
  parent: server
  name: db
  properties: {
    charset: 'UTF8'
    collation: 'en_US.utf8'
  }
}]

// ---------------------------------------------------------------------------
// Outputs
// ---------------------------------------------------------------------------

@description('PostgreSQL server resource ID')
output id string = server.id

@description('PostgreSQL server name')
output name string = server.name

@description('PostgreSQL server FQDN')
output fqdn string = server.properties.fullyQualifiedDomainName
