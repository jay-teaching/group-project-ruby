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
    contractoneyear = req.params.get('contractoneyear')
    contracttwoyear = req.params.get('contracttwoyear')
    paperlessbilling = req.params.get('paperlessbilling')
    internetservicefiberoptic = req.params.get('internetservicefiberoptic')
    internetserviceno = req.params.get('internetserviceno')
    dependents = req.params.get('dependents')

    prediction = make_prediction(
        tenure=tenure,
        MonthlyCharges=monthly,
        TechSupport_yes=techsupport,
    # Add new features:
        Contract_one_year=contractoneyear,        
        Contract_two_year=contracttwoyear,
        PaperlessBilling_yes=paperlessbilling,
        InternetService_fiber_optic=internetservicefiberoptic,
        internetserviceno=internetserviceno,
        Dependents_yes=dependents
    )

    if tenure and monthly and techsupport:
        return func.HttpResponse(f"For the given inputs, the predicted churn is {prediction}.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully.",
             status_code=200
        )