import azure.functions as func
import datetime
import json
import logging
import pandas as pd

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

@app.route(route="labsummary/{lab_order_id:int}", auth_level=func.AuthLevel.ANONYMOUS)
async def lab_summary(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    lab_order_id = int(req.route_params.get('lab_order_id'))
    print(lab_order_id)
    result = await hlp.get_lab_summary(lab_order_id)
        
    # return lab results as json
    return func.HttpResponse(result)