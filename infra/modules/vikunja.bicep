// ===========================================================================
// Vikunja — Open-Source Task Management on Azure Container Apps
// Deploys Vikunja as a single container with SQLite storage.
// ===========================================================================
// Vikunja image: vikunja/vikunja (all-in-one: API + frontend)
// Docs: https://vikunja.io/docs/
// ===========================================================================

@description('Name of the Container App')
param name string

@description('Azure region')
param location string

@description('Container Apps Environment resource ID')
param containerAppsEnvId string

@description('Tags to apply')
param tags object = {}

@description('Vikunja Docker image and tag')
param vikunjaImage string = 'docker.io/vikunja/vikunja:latest'

@description('CPU cores to allocate (0.25, 0.5, 1.0, 2.0)')
@allowed([
  '0.25'
  '0.5'
  '1.0'
  '2.0'
])
param cpu string = '0.25'

@description('Memory in Gi to allocate')
@allowed([
  '0.5Gi'
  '1.0Gi'
  '2.0Gi'
  '4.0Gi'
])
param memory string = '0.5Gi'

@description('Vikunja service URL (for CORS and frontend config)')
param serviceUrl string = ''

@description('Enable external ingress')
param externalIngress bool = true

@description('Target port for Vikunja')
param targetPort int = 3456

// ---------------------------------------------------------------------------
// Vikunja Container App
// ---------------------------------------------------------------------------

resource vikunja 'Microsoft.App/containerApps@2024-03-01' = {
  name: name
  location: location
  tags: union(tags, {
    component: 'ticketing'
    application: 'vikunja'
  })
  properties: {
    managedEnvironmentId: containerAppsEnvId
    configuration: {
      ingress: {
        external: externalIngress
        targetPort: targetPort
        transport: 'http'
        allowInsecure: false
      }
      // Vikunja uses SQLite by default — no external DB needed for POC
    }
    template: {
      containers: [
        {
          name: 'vikunja'
          image: vikunjaImage
          resources: {
            cpu: json(cpu)
            memory: memory
          }
          env: [
            {
              name: 'VIKUNJA_SERVICE_FRONTENDURL'
              value: serviceUrl
            }
            {
              name: 'VIKUNJA_SERVICE_ENABLEREGISTRATION'
              value: 'false'
            }
            {
              name: 'VIKUNJA_SERVICE_ENABLEEMAILREMINDERS'
              value: 'false'
            }
          ]
          volumeMounts: [
            {
              volumeName: 'vikunja-data'
              mountPath: '/app/vikunja/files'
            }
            {
              volumeName: 'vikunja-db'
              mountPath: '/db'
            }
          ]
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 1
      }
      volumes: [
        {
          name: 'vikunja-data'
          storageType: 'EmptyDir'
        }
        {
          name: 'vikunja-db'
          storageType: 'EmptyDir'
        }
      ]
    }
  }
}

// ---------------------------------------------------------------------------
// Outputs
// ---------------------------------------------------------------------------

@description('Vikunja Container App FQDN')
output fqdn string = vikunja.properties.configuration.ingress.fqdn

@description('Vikunja URL')
output url string = 'https://${vikunja.properties.configuration.ingress.fqdn}'

@description('Vikunja Container App resource ID')
output id string = vikunja.id
