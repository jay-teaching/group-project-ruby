import prediction


def test_make_prediction_simple():
    """A simple test to check if make_prediction returns a float.

    This test must be modified as per the actual model used.

    """
    payload = {
        "Dependents_yes": 0,
        "TechSupport_yes": 0,
        "Contract_one year": 1,
        "Contract_two year": 0,
        "OnlineBackup_yes": 1,
        "OnlineSecurity_yes": 0,
        "InternetService_fiber optic": 0,
        "DeviceProtection_yes": 1,
        "tenure": 2,
        "MonthlyCharges": 12.3,
    }
    result = prediction.make_prediction(**payload)
    assert isinstance(result, float)
