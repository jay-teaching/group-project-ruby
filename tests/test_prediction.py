import prediction


def test_make_prediction_simple():
    """A simple test to check if make_prediction returns a float.

    This test must be modified as per the actual model used.

    """
    payload = { 'tenure':2,
                'MonthlyCharges':12.3,
                'TechSupport_yes':0,
                'Contract_one year':1, 
                'Contract_two year':0, 
                'PaperlessBilling_yes':1,
                'InternetService_fiber_optic':1,
                'InternetService_no':0,
                'Dependents_yes':1
    }

    result = prediction.make_prediction(**payload)
    assert isinstance(result, float)
