import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

from prediction import make_prediction

@app.route(route="ruby_predict")
def ruby_predict(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    tenure = req.params.get('tenure')
    monthly = req.params.get('monthly')
    techsupport = req.params.get('techsupport')

    prediction = make_prediction(
    tenure=tenure,
    MonthlyCharges=monthly,
    TechSupport_yes=techsupport
    )

    if tenure and monthly and techsupport:
        return func.HttpResponse(f"For the given tenure, monthly and techsupport, the predicted churn is {prediction}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. tenure, monthly and techsupport.",
             status_code=200
        )