"""
Minimal Azure Functions predictor for the Telco churn model.

Expect only the features defined in the model built by `telco_marimo.py`.


"""

import joblib
import pandas as pd

# Edit this list to match the features used in your model
FEATURE_ORDER = ['Dependents_yes','TechSupport_yes','Contract_one year', 'Contract_two year', 'OnlineBackup_yes','OnlineSecurity_yes', 'InternetService_fiber optic',
                         'DeviceProtection_yes','tenure', 'MonthlyCharges']


BUNDLE = joblib.load("models/telco_logistic_regression.joblib")
MODEL, SCALER = BUNDLE["model"], BUNDLE["scaler"]


def make_prediction(**kwargs: float) -> float:
    """Make a churn prediction given the input features.

    Adjust FEATURE_ORDER above according to the model definition.
    """
    # Extract features in the correct order
    try:
        args = [kwargs[feature] for feature in FEATURE_ORDER]
    except KeyError as e:
        raise ValueError(f"Missing feature: {e.args[0]}") from e
    
    # Format features for scaling
    features = pd.DataFrame([args], columns=FEATURE_ORDER) # type: ignore

    # Scale features with saved scaler
    scaled = SCALER.transform(features)

    # Predict with saved model
    prob = float(MODEL.predict_proba(scaled)[0, 1])

    # Output the probability
    print(f"Churn probability: {prob:.4f}")
    return prob
