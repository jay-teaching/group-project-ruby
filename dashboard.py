import requests
import streamlit as st

DEV_API = "http://127.0.0.1:8000/predict"
PROD_API = "https://predictingforjay.azurewebsit..."


def fetch_prediction(payload: dict) -> dict:
    """Call the prediction API and return the JSON response"""
    response = requests.post(DEV_API, json=payload, timeout=5)
    response.raise_for_status()
    return response.json()


def fetch_prediction_from_production(params: dict) -> dict:
    """Call the production API and return the response.

    Our serverless function doesnt support JSON in or out
    Plus we need to increase the timeout for cold starts.
    """
    url = PROD_API + "&" + "&".join(f"{k}={v}" for k, v in params.items())
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    return response

### Streamlit Dashboard for Telco Churn Prediction

st.set_page_config(page_title="Telco Churn Predictor", page_icon="📊")


st.title("Telco Churn Prediction")
st.write("Enter customer details and get a churn prediction.")

tenure = st.selectbox("Tenure (mths)", options=list(range(0, 121)))

monthly = st.number_input(
    "Monthly Charges", min_value=0, max_value=1000, step=10, value=70
)

# Binary / categorical inputs
TechSupport_yes = int(st.checkbox("Tech Support", value=False))
Contract_one_year = int(st.checkbox("Contract: One year", value=False))
Contract_two_year = int(st.checkbox("Contract: Two year", value=False))
PaperlessBilling_yes = int(st.checkbox("Paperless Billing", value=False))
InternetService_fiber_optic = int(st.checkbox("Internet Service: Fiber optic", value=False))
InternetService_no = int(st.checkbox("Internet Service: None", value=False))
Dependents_yes = int(st.checkbox("Has Dependents", value=False))

payload = {
    "tenure": int(tenure),
    "monthly": int(monthly),
    "TechSupport_yes": int(TechSupport_yes),
    "Contract_one_year": int(Contract_one_year),
    "Contract_two_year": int(Contract_two_year),
    "PaperlessBilling_yes": int(PaperlessBilling_yes),
    "InternetService_fiber_optic": int(InternetService_fiber_optic),
    "InternetService_no": int(InternetService_no),
    "Dependents_yes": int(Dependents_yes)
}

try:
    data = fetch_prediction(payload)
    prediction = data.get("prediction")

    st.subheader("Result")
    st.write(f"Model prediction: **{prediction}**")

    st.json(data)

except requests.RequestException as e:
    st.error(f"Error calling API: {e}")
