import azure.functions as func
import logging
import json
from prediction import make_prediction

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="ruby_predict", methods=["POST"]) # Explicitly allow POST
def ruby_predict(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing churn prediction request.')

    try:
        # 1. Parse JSON Body
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON body. Please send a POST request with a JSON payload.", 
            status_code=400
        )

    # 2. Extract Data using the EXACT keys sent by Streamlit
    try:
        input_data = {
            "tenure": req_body.get('tenure'),
            "MonthlyCharges": req_body.get('MonthlyCharges'), # Matches Streamlit
            "TechSupport_yes": req_body.get('TechSupport_yes'), # Matches Streamlit
            "Contract_one_year": req_body.get('Contract_one_year'),
            "Contract_two_year": req_body.get('Contract_two_year'),
            "PaperlessBilling_yes": req_body.get('PaperlessBilling_yes'),
            "InternetService_fiber_optic": req_body.get('InternetService_fiber_optic'),
            "internetserviceno": req_body.get('internetserviceno'),
            "Dependents_yes": req_body.get('Dependents_yes')
        }
        
        # Check for missing values (optional safety step)
        if None in input_data.values():
            missing = [k for k, v in input_data.items() if v is None]
            return func.HttpResponse(f"Missing required fields: {missing}", status_code=400)

        # 3. Call Prediction
        prediction = make_prediction(**input_data)

        return func.HttpResponse(
            json.dumps({"prediction": prediction}), 
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Prediction error: {e}")
        return func.HttpResponse(f"Server Error: {e}", status_code=500)