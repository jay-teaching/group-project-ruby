"""API for making churn predictions using a FastAPI server.
Add fastapi and uvicorn to your environment with:
    uv add fastapi uvicorn
Run with: uv run uvicorn api:app --reload
"""
from fastapi import FastAPI
from pydantic import BaseModel
from prediction import make_prediction

class Customer(BaseModel):
    tenure: int
    # FIX: Remove aliases. Expect the exact Model names.
    MonthlyCharges: float
    TechSupport_yes: int
    Contract_one_year: int
    Contract_two_year: int
    PaperlessBilling_yes: int
    InternetService_fiber_optic: int
    InternetService_no: int
    Dependents_yes: int

app = FastAPI()

@app.post("/predict")
def predict(customer: Customer):
    """Make a churn prediction for a customer."""
    # model_dump() will now produce {"MonthlyCharges": 70.0, ...}
    prediction = make_prediction(**customer.model_dump())
    return {"prediction": prediction}