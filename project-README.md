# Telco Customer Churn Prediction

This project is using machine learning to predict customer churn for a telecommunications companies using the IBM Telco Customer Churn dataset. The current model achieves 82% recall for identifying at-risk customers.

This customer churn prediction helps the telecom company identify customers who are likely to leave, so they can take action to retain them. This project uses XGBoost to build a churn prediction model that can be deployed as an Azure Function for real-time predictions.

## Why XGBoost?

We switched from logistic regression to **XGBoost** for a few important reasons:

- **Better performance** - XGBoost can capture non-linear relationships between features that logistic regression misses
- **Handles complex interactions** - Automatically finds patterns between different features (like how contract type and monthly charges interact)
- **More robust** - Deals better with outliers and doesn't require as much feature preprocessing
- **Feature importance** - Gives us insights into which factors matter most for churn

## Features

The model uses 9 features selected based on their predictive power:

**Customer Information**
- `tenure` - How many months the customer has been with the company
- `MonthlyCharges` - Monthly bill amount

**Services**
- `TechSupport_yes` - Whether they have tech support
- `InternetService_fiber_optic` - Has fiber optic internet
- `InternetService_no` - No internet service

**Contract Details**
- `Contract_one_year` - One year contract
- `Contract_two_year` - Two year contract
- `PaperlessBilling_yes` - Uses paperless billing

**Household**
- `Dependents_yes` - Has dependents

## Performance
```
              precision    recall  f1-score   support
           0       0.91      0.65      0.76      1033
           1       0.46      0.82      0.59       374

    accuracy                           0.70      1407
ROC-AUC Score: 0.8259
```

**Confusion Matrix:**
```
[[672 361]
 [ 67 307]]
```

**What this means:**
- We correctly identify **82%** of customers who will churn (307 out of 374)
- The model catches most at-risk customers, which is what we optimized for
- The precision is lower (46%) which means we also flag some customers who wouldn't actually churn
- ROC-AUC of 0.83 shows the model has good overall discrimination ability

The high recall is intentional - it's better to reach out to some customers who might not churn than to miss customers who will leave. Retention campaigns are usually cheaper than acquiring new customers.

## Getting Started

### Install dependencies
```bash
uv sync
```

## CI/CD

GitHub Actions runs tests automatically on every push and pull request.

## Deployment

The model can be deployed as an Azure Function for real-time predictions. See the deployment section in the full documentation for step-by-step instructions.

## What Could Be Better

- Add more feature engineering (interaction terms, aggregations)
- Tune XGBoost hyperparameters more systematically
- Try ensemble methods or stacking

## Tech Stack

- XGBoost, scikit-learn
- Marimo for notebooks
- uv for package management
- pytest for testing
- Azure Functions for deployment