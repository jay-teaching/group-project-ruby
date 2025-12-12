import requests
import streamlit as st
from PIL import Image
import os
import json

#TODO: import dataset for analysis charts later

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(
    page_title="Project-Ruby Churn Predictor",
    page_icon=":diamonds:",
    layout="wide",
    initial_sidebar_state="auto" #discuss if we want that
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
    """
    Call the API and return JSON.
    For now we ALWAYS use DEV_API so nothing breaks.
    Later you can switch to PROD_API logic.
    """
    url = DEV_API 
    if use_prod and PROD_API:
        url = PROD_API
    response = requests.post(url, json=payload, timeout=5)
    response.raise_for_status()
    return response.json()


# ---------------------------
# SIDEBAR (future toggles)
# ---------------------------
with st.sidebar:
    st.markdown("### Settings")
    st.caption("API mode etc. can be configured here later.")
    use_prod = st.checkbox("Use PROD API (requires config.json)", value=False)
    # Just a placeholder for now


# ---------------------------
# HEADER (Logo + Title)
# ---------------------------
col1, col2 = st.columns([1, 6])

with col1:
    if logo:
        st.image(logo, width=120)

with col2:
    st.markdown(
        """
        # **Ruby Churn Prediction**
        Helping telecom companies understand customer behavior
        """,
        unsafe_allow_html=True
    )


# ---------------------------
# INPUT CARD
# ---------------------------
st.markdown("### Customer Information")

with st.container():
    st.markdown(
        "Enter the customer's details below to estimate the likelihood of churn."
    )

    colA, colB, colC = st.columns(3)

    with colA:
        tenure = st.slider(
            "Tenure (months)", min_value=0, max_value=120, value=0, step=1
        )

    with colB:
        monthly = st.slider(
            "Monthly Charges ($)", min_value=0, max_value=300, value=70, step=5
        )

    with colC:
        techsupport = int(st.toggle("Tech Support Active?", value=False))

# Prepare payload
payload = {
    "tenure": int(tenure),
    "monthly": int(monthly),
    "techsupport": int(techsupport),
}

# ---------------------------
# PREDICTION BUTTON
# ---------------------------
center = st.columns([3, 1, 3])[1]

with center:
    predict_btn = st.button("✨ Predict Churn", use_container_width=True)

# ---------------------------
# RESULT CARD
# ---------------------------
if predict_btn:
    try:
        data = fetch_prediction(payload, use_prod=use_prod)
        prediction = data.get("prediction", "No prediction returned")

        st.markdown("---")
        st.markdown("## 📌 Prediction Result")

        if prediction == 1:
            st.error("🚨 **This customer is likely to churn.**")
        else:
            st.success("💗 **This customer is unlikely to churn.**")

        # Debug JSON
        st.markdown("### Full Model Output")
        st.json(data)

    except requests.RequestException as e:
        st.error(f"❌ Error calling API: {e}")

# ---------------------------
# PLACEHOLDER FOR CHARTS (future)
# ---------------------------
st.markdown("---")
st.markdown("## Insights & Analytics (Coming Soon)")
st.info("Future charts will visualize customer patterns, churn correlations, and trends.")
