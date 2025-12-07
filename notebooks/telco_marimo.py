import marimo

__generated_with = "0.17.8"
app = marimo.App(width="medium")

with app.setup:
    from pathlib import Path

    import joblib
    import marimo as mo
    import pandas as pd
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import (accuracy_score, classification_report,
                                 confusion_matrix, f1_score, roc_auc_score)
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler


@app.cell(hide_code=True)
def _():
    mo.md("""
    # Telco churn – baseline logistic regression

    Edit the constants below, run the notebook top-to-bottom, and inspect the metrics.
    """)
    return


@app.cell
def _():
    DATA_PATH = Path("input/WA_Fn-UseC_-Telco-Customer-Churn.csv")
    MODEL_SAVE_PATH = Path("models/telco_logistic_regression.joblib")

    SAVE_MODEL = False

    SELECTED_FEATURES = ["tenure", 
                         "MonthlyCharges", 
                         "TechSupport_yes",
                         "InternetService_fiber optic",
                         'Contract_one year', 
                         'Contract_two year',
                         "PaymentMethod_electronic check",
                         "TotalCharges"]
    TEST_SIZE = 0.20
    C_VALUE = 1.0
    MAX_ITER = 1000
    SOLVER = "liblinear"
    return (
        C_VALUE,
        DATA_PATH,
        MAX_ITER,
        MODEL_SAVE_PATH,
        SAVE_MODEL,
        SELECTED_FEATURES,
        SOLVER,
        TEST_SIZE,
    )


@app.cell
def _(DATA_PATH):
    telco_df = pd.read_csv(DATA_PATH)
    telco_df.head()
    return (telco_df,)


@app.cell
def _(SELECTED_FEATURES):
    def preprocess_telco(df: pd.DataFrame):
        cleaned = df.copy()
        if "customerID" in cleaned.columns:
            cleaned = cleaned.drop(columns=["customerID"])
        cleaned["TotalCharges"] = pd.to_numeric(
            cleaned["TotalCharges"], errors="coerce"
        )
        cleaned = cleaned.dropna()

        for column in cleaned.select_dtypes(include="object"):
            cleaned[column] = cleaned[column].str.lower().str.strip()

        X = pd.get_dummies(cleaned.drop(columns=["Churn"]), drop_first=True, dtype=int)

        print("Available features after encoding:", X.columns.tolist())
        print("Selected features for modeling:", SELECTED_FEATURES)

        # Choose features
        X = X[SELECTED_FEATURES]
        y = cleaned["Churn"].map({"yes": 1, "no": 0}).to_numpy()

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        return cleaned, X_scaled, y, scaler, X.columns.tolist()

    return (preprocess_telco,)


@app.cell
def _(preprocess_telco, telco_df):
    cleaned_df, X_scaled, y, scaler, feature_names = preprocess_telco(telco_df)
    print("Chosen features:", feature_names)
    cleaned_df.head()
    return X_scaled, scaler, y


@app.cell
def _(C_VALUE, MAX_ITER, SOLVER, TEST_SIZE, X_scaled, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled,
        y,
        test_size=TEST_SIZE,
        stratify=y,
        random_state=42,
    )

    model = LogisticRegression(
        solver=SOLVER, C=C_VALUE, max_iter=MAX_ITER, random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "confusion": confusion_matrix(y_test, y_pred),
        "report": classification_report(y_test, y_pred),
    }
    return metrics, model


@app.cell
def _(metrics):
    print(metrics["confusion"])
    return


@app.cell
def _(metrics):
    print(metrics["report"])
    return


@app.cell
def _(MODEL_SAVE_PATH, SAVE_MODEL, model, scaler):
    if SAVE_MODEL:
        joblib.dump({"model": model, "scaler": scaler}, MODEL_SAVE_PATH)
    return


if __name__ == "__main__":
    app.run()
