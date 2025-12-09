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
    #from sklearn.ensemble import RandomForestClassifier
    from xgboost import XGBClassifier


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

    SELECTED_FEATURES = ['Dependents_yes','TechSupport_yes','Contract_one year', 'Contract_two year', 'OnlineBackup_yes','OnlineSecurity_yes', 'InternetService_fiber optic',
                         'DeviceProtection_yes','tenure', 'MonthlyCharges']
    
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
def _(TEST_SIZE, X_scaled, y):  #C_VALUE,SOLVER, MAX_ITER,
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled,
        y,
        test_size=TEST_SIZE,
        stratify=y,
        random_state=42,
    )

    #model = LogisticRegression(
    #    solver=SOLVER, C=C_VALUE, class_weight="balanced", max_iter=MAX_ITER, random_state=42
    #)

    #model1 = RandomForestClassifier(class_weight="balanced", n_estimators=100, max_depth=10,
    #min_samples_split=20,random_state=42
    #) # LR is performing better

    model2 = XGBClassifier(
        scale_pos_weight=len(y_train[y_train==0]) / len(y_train[y_train==1]),  # Auto-balance
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        eval_metric='logloss'  
    )

    model2.fit(X_train, y_train)

    y_proba = model2.predict_proba(X_test)[:, 1]
    threshold = 0.4  # Lower = catch more churners, more false alarms
    y_pred = (y_proba >= threshold).astype(int)

    #y_pred = model2.predict(X_test)
    #y_proba = model2.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "confusion": confusion_matrix(y_test, y_pred),
        "report": classification_report(y_test, y_pred),
    }
    return metrics, model2, 


@app.cell
def _(metrics):
    print(metrics["confusion"])
    return


@app.cell
def _(metrics):
    print(metrics["report"])
    return

@app.cell #added for ROC-AUC
def _(metrics):
    print(f"ROC-AUC Score: {metrics['roc_auc']:.4f}")
    return


@app.cell
def _(MODEL_SAVE_PATH, SAVE_MODEL, model, scaler):
    if SAVE_MODEL:
        joblib.dump({"model": model, "scaler": scaler}, MODEL_SAVE_PATH)
    return


if __name__ == "__main__":
    app.run()
