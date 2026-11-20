// AZ-900 Week 6: Declarative Infrastructure as Code (Bicep)
// Deploys a PaaS Web App (Azure App Service) + Storage Account with Governance Tags

@description('Azure region for all resources (must comply with allowed-locations policy)')
param location string = 'centralindia'

@description('Unique prefix for naming resources')
param appPrefix string = 'az900toolkit'

@description('Mandatory cost-allocation tags')
param commonTags object = {
  Environment: 'dev'
  CostCenter: 'CU-AIML-24BAI70160'
  Owner: 'Nalam Srinivasa Moorty'
}

var storageAccountName = toLower('${appPrefix}${uniqueString(resourceGroup().id)}')
var appServicePlanName = '${appPrefix}-plan'
var webAppName = '${appPrefix}-web-${uniqueString(resourceGroup().id)}'

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: take(storageAccountName, 24)
  location: location
  tags: commonTags
  sku: {
    name: 'Standard_ZRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
  }
}

resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: appServicePlanName
  location: location
  tags: commonTags
  sku: {
    name: 'B1'
    tier: 'Basic'
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

resource webApp 'Microsoft.Web/sites@2023-12-01' = {
  name: webAppName
  location: location
  tags: commonTags
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      minTlsVersion: '1.2'
    }
  }
}

output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
output storageName string = storageAccount.name
