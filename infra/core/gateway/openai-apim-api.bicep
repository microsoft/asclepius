param apiManagementServiceName string
param apiName string = 'azure-openai-service-api'
param apiPath string = '/openai'
param openAIEndpoint string

resource apiManagementService 'Microsoft.ApiManagement/service@2022-08-01' existing = {
  name: apiManagementServiceName
}

resource api 'Microsoft.ApiManagement/service/apis@2023-03-01-preview' = {
  name: apiName
  parent: apiManagementService
  properties: {
    format: 'openapi'
    value: loadTextContent('inference.json')
    serviceUrl: '${openAIEndpoint}openai'
    path: apiPath
    subscriptionRequired: true
    subscriptionKeyParameterNames: {
      header: 'api-key'
      query: 'api-key'
    }
  }
}

resource policy 'Microsoft.ApiManagement/service/apis/policies@2023-03-01-preview' = {
  name: 'policy'
  parent: api
  properties: {
    format: 'xml'
    value: loadTextContent('policy.xml')
  }
}

