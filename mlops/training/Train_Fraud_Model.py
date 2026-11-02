# ============================================================
# Script     : Train_Fraud_Model.py
# Domain     : Fraud Detection
# Purpose    : Train and register fraud detection model
# Platform   : Databricks + MLflow
# ============================================================

import mlflow
import mlflow.sklearn

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from xgboost import XGBClassifier

# ============================================================
# Configuration
# ============================================================

EXPERIMENT_NAME = "/NovaBank/FraudDetection"

REGISTERED_MODEL_NAME = (
    "NovaBank_Fraud_Detection_Model"
)

# ============================================================
# Load Features
# ============================================================

query = """

SELECT

    transaction_amount,

    fraud_signal_count,

    total_transactions,

    fraud_score,

    CASE
        WHEN fraud_risk_level = 'HIGH'
        THEN 1
        ELSE 0
    END AS label

FROM novabank_prod.fraud.fact_fraud_cases

"""

fraud_df = spark.sql(query).toPandas()

# ============================================================
# Feature Selection
# ============================================================

features = [

    "transaction_amount",

    "fraud_signal_count",

    "total_transactions",

    "fraud_score"

]

target = "label"

X = fraud_df[features]

y = fraud_df[target]

# ============================================================
# Train Test Split
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42

)

# ============================================================
# MLflow Experiment
# ============================================================

mlflow.set_experiment(EXPERIMENT_NAME)

with mlflow.start_run():

    model = XGBClassifier(

        n_estimators=200,

        max_depth=6,

        learning_rate=0.10,

        subsample=0.80,

        colsample_bytree=0.80,

        random_state=42

    )

    # ========================================================
    # Training
    # ========================================================

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    probabilities = model.predict_proba(X_test)[:, 1]

    # ========================================================
    # Metrics
    # ========================================================

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions
    )

    recall = recall_score(
        y_test,
        predictions
    )

    f1 = f1_score(
        y_test,
        predictions
    )

    auc = roc_auc_score(
        y_test,
        probabilities
    )

    # ========================================================
    # Log Parameters
    # ========================================================

    mlflow.log_param(
        "n_estimators",
        200
    )

    mlflow.log_param(
        "max_depth",
        6
    )

    mlflow.log_param(
        "learning_rate",
        0.10
    )

    # ========================================================
    # Log Metrics
    # ========================================================

    mlflow.log_metric(
        "accuracy",
        accuracy
    )

    mlflow.log_metric(
        "precision",
        precision
    )

    mlflow.log_metric(
        "recall",
        recall
    )

    mlflow.log_metric(
        "f1_score",
        f1
    )

    mlflow.log_metric(
        "auc",
        auc
    )

    # ========================================================
    # Log Model
    # ========================================================

    mlflow.sklearn.log_model(

        sk_model=model,

        artifact_path="fraud_model"

    )

    # ========================================================
    # Register Model
    # ========================================================

    run_id = mlflow.active_run().info.run_id

    model_uri = (

        f"runs:/{run_id}/fraud_model"

    )

    result = mlflow.register_model(

        model_uri=model_uri,

        name=REGISTERED_MODEL_NAME

    )

    print(
        f"Registered Model: "
        f"{REGISTERED_MODEL_NAME}"
    )

    print(
        f"Version: {result.version}"
    )

# ============================================================
# Summary
# ============================================================

print("\nModel Training Complete")

print(f"Accuracy : {accuracy:.4f}")

print(f"Precision: {precision:.4f}")

print(f"Recall   : {recall:.4f}")

print(f"F1 Score : {f1:.4f}")

print(f"AUC      : {auc:.4f}")
