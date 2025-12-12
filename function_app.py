import azure.functions as func
import logging
from prediction import make_prediction

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="ruby_predict", methods=["POST"])
def ruby_predict(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing churn prediction request.')

    tenure = req.params.get('tenure')
    monthly = req.params.get('monthly')
    techsupport = req.params.get('techsupport')

    prediction = make_prediction(
        tenure=tenure,
        MonthlyCharges=monthly,
        TechSupport_yes=techsupport,
    # Add new features:
        Contract_one_year=0,        
        Contract_two_year=0,
        PaperlessBilling_yes=0,
        InternetService_fiber_optic=0,
        internetserviceno=0,
        Dependents_yes=0
    )

    if tenure and monthly and techsupport:
        return func.HttpResponse(f"For the given inputs, the predicted churn is {prediction}.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully.",
             status_code=200
        )