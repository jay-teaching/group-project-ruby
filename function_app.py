import azure.functions as func
import logging
from prediction import make_prediction

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="ruby_predict")
def ruby_predict(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing churn prediction request.')

    try:
        # FIX: Get data from JSON Body, not req.params
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    tenure = req.body.get('tenure')
    monthly = req.body.get('monthly')
    techsupport = req.body.get('techsupport')
    contractoneyear = req.body.get('contractoneyear')
    contracttwoyear = req.body.get('contracttwoyear')
    paperlessbilling = req.body.get('paperlessbilling')
    internetservicefiberoptic = req.body.get('internetservicefiberoptic')
    internetserviceno = req.body.get('internetserviceno')
    dependents = req.body.get('dependents')

    try:
        prediction = make_prediction(
            tenure=tenure,
            MonthlyCharges=monthly,
            TechSupport_yes=techsupport,
            # Add new features
            Contract_one_year=contractoneyear,        
            Contract_two_year=contracttwoyear,
            PaperlessBilling_yes=paperlessbilling,
            InternetService_fiber_optic=internetservicefiberoptic,
            internetserviceno=internetserviceno,
            Dependents_yes=dependents
        )
        
        # Return JSON response so Streamlit can parse it easily
        import json
        return func.HttpResponse(
            json.dumps({"prediction": prediction}), 
            mimetype="application/json",
            status_code=200
        )
        
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        return func.HttpResponse(f"Error: {e}", status_code=500)