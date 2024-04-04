param name string
param location string = resourceGroup().location
param tags object = {}
param keyVaultName string

@description('The email address of the owner of the service')
@minLength(1)
param publisherEmail string = 'noreply@microsoft.com'

@description('The name of the owner of the service')
@minLength(1)
param publisherName string = 'n/a'

@description('The pricing tier of this API Management service')
@allowed([
  'Consumption'
  'Developer'
  'Standard'
  'Premium'
])
param sku string = 'Consumption'

@description('The instance size of this API Management service.')
@allowed([ 0, 1, 2 ])
param skuCount int = 0

@description('Azure Application Insights Name')
param applicationInsightsName string

resource apimService 'Microsoft.ApiManagement/service@2021-08-01' = {
  name: name
  location: location
  tags: union(tags, { 'azd-service-name': name })
  sku: {
    name: sku
    capacity: (sku == 'Consumption') ? 0 : ((sku == 'Developer') ? 1 : skuCount)
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    publisherEmail: publisherEmail
    publisherName: publisherName
    // Custom properties are not supported for Consumption SKU
    customProperties: sku == 'Consumption' ? {} : {
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Ciphers.TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA': 'false'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Ciphers.TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA': 'false'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Ciphers.TLS_RSA_WITH_AES_128_GCM_SHA256': 'false'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Ciphers.TLS_RSA_WITH_AES_256_CBC_SHA256': 'false'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Ciphers.TLS_RSA_WITH_AES_128_CBC_SHA256': 'false'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Ciphers.TLS_RSA_WITH_AES_256_CBC_SHA': 'false'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Ciphers.TLS_RSA_WITH_AES_128_CBC_SHA': 'false'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Ciphers.TripleDes168': 'false'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Protocols.Tls10': 'false'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Protocols.Tls11': 'false'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Protocols.Ssl30': 'false'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Backend.Protocols.Tls10': 'false'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Backend.Protocols.Tls11': 'false'
      'Microsoft.WindowsAzure.ApiManagement.Gateway.Security.Backend.Protocols.Ssl30': 'false'
    }
  }
}

// Give APIM identity permissions to keyvault
module keyVaultAccess '../security/keyvault-access.bicep' = {
  name: 'keyVaultApimAccess'
  params: {
    keyVaultName: keyVaultName
    principalId: apimService.identity.principalId
  }
}

// Create default subscription
resource apimDefaultDeveloperSubscription 'Microsoft.ApiManagement/service/subscriptions@2023-05-01-preview' = {
  parent: apimService
  name: 'default-developer'
  properties: {
    scope: '/apis'
    displayName: 'default-developer'
    state: 'active'
    allowTracing: false
  }
}


resource apimLogger 'Microsoft.ApiManagement/service/loggers@2021-12-01-preview' = if (!empty(applicationInsightsName)) {
  name: 'app-insights-logger'
  parent: apimService
  properties: {
    credentials: {
      instrumentationKey: applicationInsights.properties.InstrumentationKey
    }
    description: 'Logger to Azure Application Insights'
    isBuffered: false
    loggerType: 'applicationInsights'
    resourceId: applicationInsights.id
  }
}

resource applicationInsights 'Microsoft.Insights/components@2020-02-02' existing = if (!empty(applicationInsightsName)) {
  name: applicationInsightsName
}

module keyVaultSecretEndpoint '../security/keyvault-secret.bicep' = {
  name: 'keyVaultSecret-apim-endpoint'
  params: {
    keyVaultName: keyVaultName
    name: 'AZURE-OPENAI-ENDPOINT'
    secretValue: apimService.properties.gatewayUrl
  }
}

module keyVaultSecretSubscriptionKey '../security/keyvault-secret.bicep' = {
  name: 'keyVaultSecret-apim-subscription-key'
  params: {
    keyVaultName: keyVaultName
    name: 'APIM-SUBSCRIPTION-KEY'
    secretValue: apimDefaultDeveloperSubscription.listSecrets(apimDefaultDeveloperSubscription.apiVersion).primaryKey
  }
}

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' existing = {
  name: keyVaultName
}

resource apim_openai_api_key 'Microsoft.ApiManagement/service/namedValues@2023-05-01-preview' = {
  parent: apimService
  dependsOn: [keyVaultAccess]
  name: 'openai-api-key'
  properties: {
    displayName: 'openai-api-key'
    keyVault: {
      secretIdentifier: '${keyVault.properties.vaultUri}secrets/AZURE-OPENAI-API-KEY'
    }
    secret: true
  }
}

output apimServiceName string = apimService.name
output apimServiceUrl string = apimService.properties.gatewayUrl
