import azure.functions as func
import datetime
import json
import logging
import pandas as pd

app = func.FunctionApp()



@app.route(route="name", auth_level=func.AuthLevel.ANONYMOUS)
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
        
@app.route(route="weather", auth_level=func.AuthLevel.ANONYMOUS)
def weather(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # load weather data from utf-8-sig encoded json file
    with open('data/weather.json', 'r', encoding='utf-8-sig') as file:
        weather = json.load(file)
        
    # return weather as json
    return func.HttpResponse(json.dumps(weather), mimetype="application/json")

@app.route(route="patient", auth_level=func.AuthLevel.ANONYMOUS)
def patient_list(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # load patient data patient csv file using pandas
    patients = pd.read_csv('./data/patient_enh_no_PHI.csv').to_dict(orient='records')
    # remove NaN values from patients
    patients = [{k: v for k, v in patient.items() if pd.notna(v)} for patient in patients]
        
    # return patients as json
    return func.HttpResponse(json.dumps(patients), mimetype="application/json")