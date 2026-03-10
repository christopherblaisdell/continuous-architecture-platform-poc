// ===========================================================================
// Azure Container App — NovaTrek Microservice Template
// Generic module for deploying any of the 22 NovaTrek microservices.
// All services follow this exact same pattern — no special snowflakes.
// ===========================================================================

@description('Service name (e.g., svc-check-in)')
param name string

@description('Azure region')
param location string

@description('Container Apps Environment resource ID')
param environmentId string

@description('Container Registry login server')
param registryServer string

@description('Full image reference (registry/repo:tag)')
param image string

@description('Tags to apply')
param tags object = {}

@description('CPU cores (e.g., 0.25, 0.5, 1.0)')
param cpu string = '0.25'

@description('Memory allocation (e.g., 0.5Gi, 1.0Gi)')
param memory string = '0.5Gi'

@description('Minimum replicas (0 = scale to zero)')
param minReplicas int = 0

@description('Maximum replicas for burst capacity')
param maxReplicas int = 3

@description('Target port the container listens on')
param targetPort int = 8080

@description('Enable external ingress')
param externalIngress bool = true

@description('Environment variables for the container')
param env array = []

@description('Secret references for the container')
param secrets array = []

@description('User-assigned managed identity resource ID')
param managedIdentityId string = ''

@description('Concurrent requests threshold for HTTP scaling')
param httpScaleConcurrency int = 50

// ---------------------------------------------------------------------------
// Container App
// ---------------------------------------------------------------------------

resource containerApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: 'ca-${name}'
  location: location
  tags: union(tags, { service: name })
  identity: !empty(managedIdentityId) ? {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${managedIdentityId}': {}
    }
  } : {
    type: 'None'
  }
  properties: {
    managedEnvironmentId: environmentId
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: externalIngress ? {
        external: true
        targetPort: targetPort
        transport: 'auto'
        allowInsecure: false
      } : null
      registries: !empty(managedIdentityId) ? [
        {
          server: registryServer
          identity: managedIdentityId
        }
      ] : []
      secrets: secrets
    }
    template: {
      containers: [
        {
          name: name
          image: image
          resources: {
            cpu: json(cpu)
            memory: memory
          }
          env: env
          probes: [
            {
              type: 'Liveness'
              httpGet: {
                path: '/actuator/health/liveness'
                port: targetPort
              }
              initialDelaySeconds: 30
              periodSeconds: 10
              failureThreshold: 3
            }
            {
              type: 'Readiness'
              httpGet: {
                path: '/actuator/health/readiness'
                port: targetPort
              }
              initialDelaySeconds: 15
              periodSeconds: 5
              failureThreshold: 3
            }
          ]
        }
      ]
      scale: {
        minReplicas: minReplicas
        maxReplicas: maxReplicas
        rules: [
          {
            name: 'http-scaling'
            http: {
              metadata: {
                concurrentRequests: string(httpScaleConcurrency)
              }
            }
          }
        ]
      }
    }
  }
}

// ---------------------------------------------------------------------------
// Outputs
// ---------------------------------------------------------------------------

@description('Container App resource ID')
output id string = containerApp.id

@description('Container App name')
output name string = containerApp.name

@description('Container App FQDN')
output fqdn string = externalIngress ? containerApp.properties.configuration.ingress.fqdn : ''

@description('Container App latest revision name')
output latestRevision string = containerApp.properties.latestRevisionName
