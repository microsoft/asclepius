# AI Generated Lab Results Summary Template
This project provides an example template to illustrate the use of Azure OpenAI to generate a patient-facing summary of incoming lab results, including explanation of what the results mean and the implications on the patient's health. The intent is to simulate an integration with an EHR, intercepting the incoming lab results from the in-basket and passing those results along with the notes from the last encounter to the Azure OpenAI LLM to create an explanation to the patient - reducing cognitive load an time spent by clinicians and getting result information to patients more quickly.

## Solution Description
This solution includes an API defined and deployed to an Azure Function App, developed on Python with the Semantic Kernal SDK to define and orchestration prompt function calls to Azure OpenAI. 

**ToDo: create app flow illustration of data inputs, prompt functions and plugin call to OpenAI**

## Architecture
This template deploys an API built and hosted by an Azure Function App, with a Static Web App Blazor front end to illustrate a user selecting a lab result from an in-basket and requesting patient-facing summary from AI. 

![Template Architecture](./docs/LabSum_Template_Architecture.png)

This template includes the reading of sample data from a local sample data file for simplicity. This could be extended with Databricks or other mechanism to pull near-real-time data, or other integration pattern, as in the example below.

![Example Integration Pattern with Databricks](./docs/LabSum_Extension_Example.png)

# Deployment Instructions
To deploy to Azure, you can follow these steps:

1. Install the Azure CLI: [How to install the Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)

2. Install the Azure DevOps (azd) extension for the Azure CLI. You can do this by running the following command in your terminal:

    `az extension add --name azure-devops`

3. Log in to your Azure account by running the following command and following the prompts:
    `az login`

4. Run the azd up command, specifying the main.bicep file and the main.parameters.json file. Here's an example:

    ```az deployment group create --resource-group myResourceGroup --template-uri https://github.com/microsoft/asclepius/tree/main/infra/main.bicep --parameters @main.parameters.json```

6. Follow the prompts to indicate the subscription, region and resource group to deploy to

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
