"""API for making churn predictions using a FastAPI server.
Run with: uv run uvicorn api:app --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel
from prediction import make_prediction

# ---------------------------------------------------------
# FIX: Remove 'Field(alias=...)'
# Define the model exactly as the Streamlit app sends it.
# ---------------------------------------------------------
class Customer(BaseModel):
    tenure: int
    MonthlyCharges: float  # Changed to float (money is usually a float)
    TechSupport_yes: int
    Contract_one_year: int
    Contract_two_year: int
    PaperlessBilling_yes: int
    InternetService_fiber_optic: int
    internetserviceno: int
    Dependents_yes: int

app = FastAPI()

@app.post("/predict")
def predict(customer: Customer):
    """Make a churn prediction for a customer."""
    # Debug: Print received data to the terminal to see what's happening
    print(f"Received: {customer.model_dump()}")

    # Pass the data to the prediction function
    # model_dump() creates a dictionary: {"MonthlyCharges": 70.5, ...}
    prediction = make_prediction(**customer.model_dump())
    
    return {"prediction": prediction}