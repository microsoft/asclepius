import logging
import os
import uuid
import pandas as pd

import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion


def generate_uuid() -> str:
    return str(uuid.uuid4())


class KernelFactory:
    @staticmethod
    def create_kernel() -> sk.Kernel:
        kernel = sk.Kernel()

        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

        #deployment, api_key, endpoint = sk.azure_openai_settings_from_dot_env()

        script_directory = os.path.dirname(__file__)
        plugins_directory = os.path.join(script_directory, "plugins")

        service_id = None

        plugin_names = [
            plugin for plugin in os.listdir(plugins_directory) if os.path.isdir(os.path.join(plugins_directory, plugin))
        ]

        # for each plugin, add the plugin to the kernel
        try:
            for plugin_name in plugin_names:
                kernel.import_plugin_from_prompt_directory(plugins_directory, plugin_name)
        except ValueError:
            logging.exception(f"Plugin {plugin_name} not found")

        # add the chat service
        service = AzureChatCompletion(
            service_id=service_id,
            deployment_name=deployment,
            endpoint=endpoint,
            api_key=api_key,
            #   api_version="2024-02-15-preview"
        )

        kernel.add_service(service)

        return kernel

    def __str__(self):
        return self.name
    
async def get_lab_summary(lab_order_id: int) -> str:
    kernel = KernelFactory.create_kernel()
    
    sk_function = kernel.plugins['summarize_labs']['summarize_labs']
    
    # load lab result data from csv file using pandas
    lab_results = pd.read_csv('./data/lab_rslt_component_no_PHI.csv')
    lab_results = lab_results.loc[lab_results['ORD_ID'] == 279149741]
    visit_id = lab_results['PAT_ENC_CSN_ID'][0]
    print(visit_id)
    cols = ['CMPNT_NM', 'RSLT_VALUE_TXT', 'REFER_UNIT', 'REFER_VALUE']
    lab_results = lab_results[cols]
    
    lab_notes = pd.read_csv('./data/notes_no_PHI.csv')
    lab_notes = lab_notes.loc[lab_notes['PAT_ENC_CSN_ID'] == visit_id]
    
    functions = [
        kernel.plugins["summarize_note"]["summarize_chief_complaint"], 
        kernel.plugins["summarize_note"]["summarize_lab_history"],
        kernel.plugins["summarize_note"]["summarize_assessment"]
    ]
    
    visit_note = lab_notes['NOTE_TEXT']

    
    arguments = sk.KernelArguments(input=visit_note)
    response = await kernel.invoke(functions, arguments)

    sum_chief_complaint = response[0].value[0].content
    sum_lab_history = response[1].value[0].content
    sum_assessment = response[2].value[0].content
    
    print("Lenght of lab notes:" + str(len(lab_notes)))
    arguments = sk.KernelArguments(
        lab_results_input=lab_results.to_json(orient='records'), 
        hpi_input=sum_chief_complaint, 
        previous_labs_input=sum_lab_history, 
        assessment_plan_input=sum_assessment)
    
    result = await kernel.invoke(sk_function, arguments=arguments)
    
    if result:
        return result.value[0].content
    else:
        return None
    