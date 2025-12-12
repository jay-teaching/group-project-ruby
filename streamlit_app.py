import requests
import streamlit as st
from PIL import Image
import os
import json

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(
    page_title="Project-Ruby Churn Predictor",
    page_icon=":diamonds:",
    layout="wide",
    initial_sidebar_state="auto"
)

logo = Image.open("Logo1_.png")

# ---------------------------
# API ENDPOINTS
# ---------------------------
DEV_API = "http://127.0.0.1:8000/predict"

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
_prod_api_key = None
if os.path.isfile(CONFIG_PATH):
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            _cfg = json.load(f)
            _prod_api_key = _cfg.get("prod_api_key")
    except Exception:
        _prod_api_key = None

PROD_API = None
if _prod_api_key:
    PROD_API = f"https://predictingforruby.azurewebsites.net/api/ruby_predict?code={_prod_api_key}"

def fetch_prediction(payload: dict, use_prod: bool = False) -> dict:
    url = DEV_API
    if use_prod and PROD_API:
        url = PROD_API
    response = requests.post(url, json=payload, timeout=5)
    response.raise_for_status()
    return response.json()

# ---------------------------
# SIDEBAR
# ---------------------------
with st.sidebar:
    st.markdown("### Settings")
    use_prod = st.checkbox("Use PROD API", value=False)

# ---------------------------
# HEADER
# ---------------------------
col1, col2 = st.columns([1, 6])

with col1:
    st.image(logo, width=120)

with col2:
    st.markdown(
        """
        # **Ruby Churn Prediction**
        Helping telecom companies understand customer behavior
        """
    )

# ---------------------------
# INPUTS
# ---------------------------
st.markdown("### Customer Information")

colA, colB, colC = st.columns(3)

with colA:
    tenure = st.slider("Tenure (months)", 0, 120, 10)
    dependents_choice = st.selectbox("Has Dependents?", ["No", "Yes"])
    paperless_choice = st.selectbox("Paperless Billing?", ["No", "Yes"])

with colB:
    monthly = st.slider("Monthly Charges ($)", 0, 300, 70)
    techsupport_choice = st.selectbox("Tech Support", ["No", "Yes"])
    internet_service = st.selectbox("Internet Service", ["Fiber optic", "No internet"])

with colC:
    contract_type = st.selectbox(
        "Contract Type",
        ["Month-to-month", "One year", "Two years"]
    )

# ---------------------------
# DROPDOWN → MODEL MAPPING
# ---------------------------
Dependents_yes = 1 if dependents_choice == "Yes" else 0
PaperlessBilling_yes = 1 if paperless_choice == "Yes" else 0
TechSupport_yes = 1 if techsupport_choice == "Yes" else 0

Contract_one_year = 1 if contract_type == "One year" else 0
Contract_two_year = 1 if contract_type == "Two years" else 0

InternetService_fiber_optic = 1 if internet_service == "Fiber optic" else 0
internetserviceno = 1 if internet_service == "No internet" else 0

# ---------------------------
# PAYLOAD (BACKEND CONTRACT)
# ---------------------------
payload = {
    "tenure": int(tenure),
    "MonthlyCharges": float(monthly),
    "TechSupport_yes": TechSupport_yes,
    "Contract_one_year": Contract_one_year,
    "Contract_two_year": Contract_two_year,
    "PaperlessBilling_yes": PaperlessBilling_yes,
    "InternetService_fiber_optic": InternetService_fiber_optic,
    "internetserviceno": internetserviceno,
    "Dependents_yes": Dependents_yes,
}

# ---------------------------
# PREDICT BUTTON
# ---------------------------
center = st.columns([3, 1, 3])[1]
with center:
    predict_btn = st.button("✨ Predict Churn", use_container_width=True)

# ---------------------------
# RESULT
# ---------------------------
if predict_btn:
    try:
        data = fetch_prediction(payload, use_prod=use_prod)
        st.markdown("## 📌 Prediction Result")
        st.json(data)
    except requests.RequestException as e:
        st.error(f"❌ Error calling API: {e}")

