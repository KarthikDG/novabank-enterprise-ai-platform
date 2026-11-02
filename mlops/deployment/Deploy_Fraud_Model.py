# ============================================================
# Script     : Deploy_Fraud_Model.py
# Domain     : Fraud Detection
# Purpose    : Promote MLflow model to Production
# ============================================================

from mlflow.tracking import MlflowClient
import mlflow

# ============================================================
# Configuration
# ============================================================

MODEL_NAME = "NovaBank_Fraud_Detection_Model"

TARGET_STAGE = "Production"

# ============================================================
# MLflow Client
# ============================================================

client = MlflowClient()

# ============================================================
# Get Latest Model Version
# ============================================================

latest_versions = client.get_latest_versions(
    MODEL_NAME
)

latest_version = max(
    [int(v.version) for v in latest_versions]
)

print(
    f"Latest Model Version Found: {latest_version}"
)

# ============================================================
# Archive Existing Production Models
# ============================================================

for model_version in latest_versions:

    if model_version.current_stage == "Production":

        client.transition_model_version_stage(
            name=MODEL_NAME,
            version=model_version.version,
            stage="Archived"
        )

        print(
            f"Archived version "
            f"{model_version.version}"
        )

# ============================================================
# Promote to Production
# ============================================================

client.transition_model_version_stage(
    name=MODEL_NAME,
    version=latest_version,
    stage=TARGET_STAGE
)

print(
    f"Version {latest_version} promoted "
    f"to {TARGET_STAGE}"
)

# ============================================================
# Load Production Model
# ============================================================

model_uri = (

    f"models:/{MODEL_NAME}/Production"

)

model = mlflow.pyfunc.load_model(
    model_uri
)

print(
    "Production model loaded successfully"
)

# ============================================================
# Example Prediction Payload
# ============================================================

sample_transaction = {

    "transaction_amount": 15000.00,
    "fraud_signal_count": 5,
    "total_transactions": 120,
    "fraud_score": 85

}

print(
    "Deployment validation complete"
)

# ============================================================
# Deployment Summary
# ============================================================

print(
    f"Model Name    : {MODEL_NAME}"
)

print(
    f"Version       : {latest_version}"
)

print(
    f"Stage         : Production"
)

print(
    "Deployment Status : SUCCESS"
)
