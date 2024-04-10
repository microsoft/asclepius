import azure.functions as func
import datetime
import json
import logging
import pandas as pd
from semantic_kernel import KernelArguments

import helpers as hlp

app = func.FunctionApp()


@app.route(route="patient", auth_level=func.AuthLevel.ANONYMOUS)
def patient_list(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # load patient data patient csv file using pandas
    patients = pd.read_csv('./data/patient_enh_no_PHI.csv').to_dict(orient='records')
    # remove NaN values from patients
    patients = [{k: v for k, v in patient.items() if pd.notna(v)} for patient in patients]
    # return patients as json
    return func.HttpResponse(json.dumps(patients), mimetype="application/json")

@app.route(route="laborder", auth_level=func.AuthLevel.ANONYMOUS)
def lab_order_list(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # load lab result data from csv file using pandas
    lab_results = pd.read_csv('./data/lab_ord_rslt_no_PHI.csv').to_dict(orient='records')
    # remove NaN values from lab results
    lab_results = [{k: v for k, v in lab_result.items() if pd.notna(v)} for lab_result in lab_results]
        
    # return lab results as json
    return func.HttpResponse(json.dumps(lab_results), mimetype="application/json")

@app.route(route="labresult/{lab_order_id:int}", auth_level=func.AuthLevel.ANONYMOUS)
def lab_result_list(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    lab_order_id = req.route_params.get('lab_order_id')

    # load lab result data from csv file using pandas
    lab_results = pd.read_csv('./data/lab_rslt_component_no_PHI.csv').to_dict(orient='records')
    # remove NaN values from lab results
    lab_results = [{k: v for k, v in lab_result.items() if pd.notna(v)} for lab_result in lab_results]
    
    if lab_order_id is not None:
        lab_results = [lab_result for lab_result in lab_results if lab_result['ORD_ID'] == int(lab_order_id)]
        
    # return lab results as json
    return func.HttpResponse(json.dumps(lab_results), mimetype="application/json")

@app.route(route="labsummary", auth_level=func.AuthLevel.ANONYMOUS, methods=['POST'])
async def lab_summary(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Generating lab summary.')

    # get lab data json from body
    lab_data = req.get_json()
    
    visit_id = lab_data['PAT_ENC_CSN_ID']
    
    lab_notes = pd.read_csv('./data/notes_no_PHI.csv')
    lab_notes = lab_notes.loc[lab_notes['PAT_ENC_CSN_ID'] == visit_id]
    visit_note = lab_notes['NOTE_TEXT']
    
    kernel = hlp.KernelFactory.create_kernel()
    
    note_functions = [
        kernel.plugins["summarize_note"]["summarize_chief_complaint"], 
        kernel.plugins["summarize_note"]["summarize_lab_history"],
        kernel.plugins["summarize_note"]["summarize_assessment"]
    ]
    
    arguments = KernelArguments(input=visit_note)
    response = await kernel.invoke(note_functions, arguments)

    sum_chief_complaint = response[0].value[0].content
    sum_lab_history = response[1].value[0].content
    sum_assessment = response[2].value[0].content

    lab_summary_function = kernel.plugins['summarize_labs']['summarize_labs']
    
    lab_summary_response = await kernel.invoke(lab_summary_function, KernelArguments(
        lab_results_input=lab_data['lab_results'], 
        hpi_input=sum_chief_complaint, 
        previous_labs_input=sum_lab_history, 
        assessment_plan_input=sum_assessment)
    )
    
    if lab_summary_response:
        return func.HttpResponse(lab_summary_response.value[0].content)
    else:
        return func.HttpResponse(None)
    