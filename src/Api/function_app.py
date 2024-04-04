import azure.functions as func
import datetime
import json
import logging
import pandas as pd

app = func.FunctionApp()


@app.route(route="patient/{patient_id:alpha?}", auth_level=func.AuthLevel.ANONYMOUS)
def patient_list(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    patient_id = req.route_params.get('patient_id')
    # load patient data patient csv file using pandas
    patients = pd.read_csv('./data/patient_enh_no_PHI.csv').to_dict(orient='records')
    # remove NaN values from patients
    patients = [{k: v for k, v in patient.items() if pd.notna(v)} for patient in patients]
    # filter patients by patient_id
    if patient_id is not None:
        patients = [patient for patient in patients if patient['PAT_ID'] == patient_id]
    # return patients as json
    return func.HttpResponse(json.dumps(patients), mimetype="application/json")

@app.route(route="labresult", auth_level=func.AuthLevel.ANONYMOUS)
def lab_result_list(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # load lab result data from csv file using pandas
    lab_results = pd.read_csv('./data/lab_ord_rslt_no_PHI.csv').to_dict(orient='records')
    # remove NaN values from lab results
    lab_results = [{k: v for k, v in lab_result.items() if pd.notna(v)} for lab_result in lab_results]
        
    # return lab results as json
    return func.HttpResponse(json.dumps(lab_results), mimetype="application/json")