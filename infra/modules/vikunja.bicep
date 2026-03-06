// ===========================================================================
// Vikunja — Open-Source Task Management on Azure Container Apps
// Deploys Vikunja as a single container with SQLite on Azure Files.
// ===========================================================================
// Vikunja image: vikunja/vikunja (all-in-one: API + frontend)
// Docs: https://vikunja.io/docs/
//
// Storage: SQLite database persisted to Azure Files via init container
// that sets correct permissions (Vikunja runs as uid=1000).
// ===========================================================================

@description('Name of the Container App')
param name string

@description('Azure region')
param location string

@description('Container Apps Environment resource ID')
param containerAppsEnvId string

@description('Name of the Container Apps Environment (used for storage mount)')
param containerAppsEnvName string

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

@description('Fixed JWT secret to survive container restarts')
@secure()
param jwtSecret string

// ---------------------------------------------------------------------------
// Storage Account + File Share for persistent SQLite database
// ---------------------------------------------------------------------------

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: 'stcapticketing'
  location: location
  tags: union(tags, { component: 'ticketing-storage' })
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
  }
}

resource fileService 'Microsoft.Storage/storageAccounts/fileServices@2023-05-01' = {
  parent: storageAccount
  name: 'default'
}

resource fileShare 'Microsoft.Storage/storageAccounts/fileServices/shares@2023-05-01' = {
  parent: fileService
  name: 'vikunja-data'
  properties: {
    shareQuota: 1
  }
}

// ---------------------------------------------------------------------------
// Register Azure Files storage in Container Apps Environment
// ---------------------------------------------------------------------------

resource envStorage 'Microsoft.App/managedEnvironments/storages@2024-03-01' = {
  name: '${containerAppsEnvName}/vikunjafiles'
  properties: {
    azureFile: {
      accountName: storageAccount.name
      accountKey: storageAccount.listKeys().keys[0].value
      shareName: fileShare.name
      accessMode: 'ReadWrite'
    }
  }
}

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
  dependsOn: [envStorage]
  properties: {
    managedEnvironmentId: containerAppsEnvId
    configuration: {
      ingress: {
        external: externalIngress
        targetPort: targetPort
        transport: 'http'
        allowInsecure: false
      }
    }
    template: {
      initContainers: [
        {
          name: 'fix-perms'
          image: 'docker.io/busybox:latest'
          command: ['/bin/sh', '-c', 'chmod -R 777 /db && touch /db/vikunja.db && chmod 666 /db/vikunja.db']
          resources: {
            cpu: json(cpu)
            memory: memory
          }
          volumeMounts: [
            {
              volumeName: 'vikunja-db'
              mountPath: '/db'
            }
          ]
        }
      ]
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
              name: 'VIKUNJA_SERVICE_PUBLICURL'
              value: serviceUrl
            }
            {
              name: 'VIKUNJA_SERVICE_FRONTENDURL'
              value: serviceUrl
            }
            {
              name: 'VIKUNJA_CORS_ENABLE'
              value: 'false'
            }
            {
              name: 'VIKUNJA_SERVICE_ENABLEREGISTRATION'
              value: 'false'
            }
            {
              name: 'VIKUNJA_SERVICE_ENABLEEMAILREMINDERS'
              value: 'false'
            }
            {
              name: 'VIKUNJA_DATABASE_PATH'
              value: '/db/vikunja.db'
            }
            {
              name: 'VIKUNJA_SERVICE_JWTSECRET'
              value: jwtSecret
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
        minReplicas: 1
        maxReplicas: 1
      }
      volumes: [
        {
          name: 'vikunja-data'
          storageType: 'EmptyDir'
        }
        {
          name: 'vikunja-db'
          storageName: 'vikunjafiles'
          storageType: 'AzureFile'
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
