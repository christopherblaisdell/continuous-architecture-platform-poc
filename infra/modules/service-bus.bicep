// ===========================================================================
// Azure Service Bus — NovaTrek Event Bus
// Hosts all AsyncAPI-defined event topics for inter-service communication.
// ===========================================================================

@description('Namespace name')
param name string

@description('Azure region')
param location string

@description('Tags to apply')
param tags object = {}

@description('SKU tier (Basic for dev, Standard for prod topics/subscriptions)')
@allowed(['Basic', 'Standard', 'Premium'])
param sku string = 'Basic'

@description('Event topic names to create')
param topics array = []

// ---------------------------------------------------------------------------
// Service Bus Namespace
// ---------------------------------------------------------------------------

resource namespace 'Microsoft.ServiceBus/namespaces@2022-10-01-preview' = {
  name: name
  location: location
  tags: tags
  sku: {
    name: sku
    tier: sku
  }
}

// ---------------------------------------------------------------------------
// Topics (Standard/Premium tier only — Basic uses queues)
// ---------------------------------------------------------------------------

resource sbTopics 'Microsoft.ServiceBus/namespaces/topics@2022-10-01-preview' = [for topic in topics: if (sku != 'Basic') {
  parent: namespace
  name: topic
  properties: {
    maxSizeInMegabytes: 1024
    defaultMessageTimeToLive: 'P14D'
    enablePartitioning: false
    enableBatchedOperations: true
  }
}]

// ---------------------------------------------------------------------------
// Queues (Basic tier alternative — one queue per event type)
// ---------------------------------------------------------------------------

resource sbQueues 'Microsoft.ServiceBus/namespaces/queues@2022-10-01-preview' = [for topic in topics: if (sku == 'Basic') {
  parent: namespace
  name: topic
  properties: {
    maxSizeInMegabytes: 1024
    defaultMessageTimeToLive: 'P14D'
    deadLetteringOnMessageExpiration: true
    maxDeliveryCount: 3
  }
}]

// ---------------------------------------------------------------------------
// Authorization Rules
// ---------------------------------------------------------------------------

resource sendRule 'Microsoft.ServiceBus/namespaces/authorizationRules@2022-10-01-preview' = {
  parent: namespace
  name: 'SendOnly'
  properties: {
    rights: ['Send']
  }
}

resource listenRule 'Microsoft.ServiceBus/namespaces/authorizationRules@2022-10-01-preview' = {
  parent: namespace
  name: 'ListenOnly'
  properties: {
    rights: ['Listen']
  }
}

// ---------------------------------------------------------------------------
// Outputs
// ---------------------------------------------------------------------------

@description('Service Bus namespace resource ID')
output id string = namespace.id

@description('Service Bus namespace name')
output name string = namespace.name

@description('Service Bus namespace FQDN')
output fqdn string = '${namespace.name}.servicebus.windows.net'

@description('Send authorization rule resource ID')
output sendRuleId string = sendRule.id

@description('Listen authorization rule resource ID')
output listenRuleId string = listenRule.id
