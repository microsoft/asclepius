targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name which is used to generate a short unique hash for each resource')
param name string

@minLength(1)
@description('Primary location for all resources')
param location string

@description('Id of the user or app to assign application roles')
param principalId string = ''

param aoaiEndpointUrl string
@secure()
param aoaiApiKey string

var resourceToken = toLower(uniqueString(subscription().id, name, location))
var tags = { 'azd-env-name': name }

resource resourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: '${name}-rg'
  location: location
  tags: tags
}

var prefix = '${name}-${resourceToken}'

module monitoring './core/monitor/monitoring.bicep' = {
  name: 'monitoring'
  scope: resourceGroup
  params: {
    location: location
    tags: tags
    logAnalyticsName: '${prefix}-logworkspace'
    applicationInsightsName: '${prefix}-appinsights'
    applicationInsightsDashboardName: '${prefix}-appinsights-dashboard'
  }
}

module storageAccount 'core/storage/storage-account.bicep' = {
  name: 'storage'
  scope: resourceGroup
  params: {
    name: '${toLower(take(replace(prefix, '-', ''), 17))}storage'
    location: location
    tags: tags
  }
}

module appServicePlan './core/host/appserviceplan.bicep' = {
  name: 'appserviceplan'
  scope: resourceGroup
  params: {
    name: '${prefix}-plan'
    location: location
    tags: tags
    sku: {
      name: 'Y1'
      tier: 'Dynamic'
    }
  }
}

module functionApp 'core/host/functions.bicep' = {
  name: 'function'
  scope: resourceGroup
  params: {
    name: '${prefix}-function-app'
    location: location
    tags: union(tags, { 'azd-service-name': 'api' })
    alwaysOn: false
    appSettings: {
      AzureWebJobsFeatureFlags: 'EnableWorkerIndexing'
    }
    applicationInsightsName: monitoring.outputs.applicationInsightsName
    appServicePlanId: appServicePlan.outputs.id
    runtimeName: 'python'
    runtimeVersion: '3.11'
    storageAccountName: storageAccount.outputs.name
    keyVaultName: keyVault.outputs.name
    openAIEndpoint: aoaiEndpointUrl
  }
}

module webKeyVaultAccess './core/security/keyvault-access.bicep' = {
  name: 'web-keyvault-access'
  scope: resourceGroup
  params: {
    keyVaultName: keyVault.name
    principalId: functionApp.outputs.identityPrincipalId
  }
}

module keyVault './core/security/keyvault.bicep' = {
  name: 'keyvault'
  scope: resourceGroup
  params: {
    name: '${take(replace(prefix, '-', ''), 17)}-vault'
    location: location
    tags: tags
    principalId: principalId
  }
}

module apim 'core/gateway/apim.bicep' = {
  name: 'apim'
  scope: resourceGroup
  params: {
    name: '${prefix}-apim'
    location: location
    tags: tags
    applicationInsightsName: monitoring.outputs.applicationInsightsName
    keyVaultName: keyVault.outputs.name
  }
}

module apimapi './core/gateway/openai-apim-api.bicep' = {
  name: 'apim-api'
  scope: resourceGroup
  params: {
    apiManagementServiceName: apim.outputs.apimServiceName
    openAIEndpoint: aoaiEndpointUrl
  }
}

module aoaiApiKeySecret 'core/security/keyvault-secret.bicep' = {
  name: 'aoaiApiKeySecret'
  scope: resourceGroup
  params: {
    keyVaultName: keyVault.outputs.name
    name: 'AZURE-OPENAI-API-KEY'
    secretValue: aoaiApiKey
  }
}

module aoaiEndpointUrlSecret 'core/security/keyvault-secret.bicep' = {
  name: 'aoaiEndpointUrlSecret'
  scope: resourceGroup
  params: {
    keyVaultName: keyVault.outputs.name
    name: 'AZURE-OPENAI-ENDPOINT-URL'
    secretValue: aoaiEndpointUrl
  }
}
