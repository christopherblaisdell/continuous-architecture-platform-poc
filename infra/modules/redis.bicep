// ===========================================================================
// Azure Cache for Redis — NovaTrek
// Schedule locks, session cache, rate limiting.
// ===========================================================================

@description('Redis cache name')
param name string

@description('Azure region')
param location string

@description('Tags to apply')
param tags object = {}

@description('SKU name')
@allowed(['Basic', 'Standard', 'Premium'])
param skuName string = 'Basic'

@description('SKU family')
@allowed(['C', 'P'])
param skuFamily string = 'C'

@description('Cache capacity (C0=250MB, C1=1GB, C2=2.5GB)')
@allowed([0, 1, 2, 3, 4, 5, 6])
param skuCapacity int = 0

@description('Minimum TLS version')
param minTlsVersion string = '1.2'

@description('Enable non-SSL port (should always be false)')
param enableNonSslPort bool = false

// ---------------------------------------------------------------------------
// Redis Cache
// ---------------------------------------------------------------------------

resource redis 'Microsoft.Cache/redis@2023-08-01' = {
  name: name
  location: location
  tags: tags
  properties: {
    sku: {
      name: skuName
      family: skuFamily
      capacity: skuCapacity
    }
    enableNonSslPort: enableNonSslPort
    minimumTlsVersion: minTlsVersion
    redisConfiguration: {
      'maxmemory-policy': 'allkeys-lru'
    }
  }
}

// ---------------------------------------------------------------------------
// Outputs
// ---------------------------------------------------------------------------

@description('Redis cache resource ID')
output id string = redis.id

@description('Redis cache name')
output name string = redis.name

@description('Redis cache hostname')
output hostName string = redis.properties.hostName

@description('Redis SSL port')
output sslPort int = redis.properties.sslPort
