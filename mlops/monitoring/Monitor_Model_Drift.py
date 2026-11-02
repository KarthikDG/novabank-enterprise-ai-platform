# ============================================================
# Script     : Monitor_Model_Drift.py
# Domain     : MLOps Monitoring
# Purpose    : Monitor model drift and performance degradation
# Platform   : Databricks + MLflow
# ============================================================

import mlflow
import pandas as pd
import numpy as np

from scipy.stats import ks_2samp
from datetime import datetime

# ============================================================
# Configuration
# ============================================================

MODEL_NAME = "NovaBank_Fraud_Detection_Model"

FEATURE_DRIFT_THRESHOLD = 0.15

PREDICTION_DRIFT_THRESHOLD = 0.20

ACCURACY_THRESHOLD = 0.90

# ============================================================
# Reference Dataset
# ============================================================

reference_query = """

SELECT

    transaction_amount,
    fraud_signal_count,
    total_transactions,
    fraud_score

FROM novabank_prod.ml.training_features

"""

reference_df = spark.sql(
    reference_query
).toPandas()

# ============================================================
# Production Dataset
# ============================================================

production_query = """

SELECT

    transaction_amount,
    fraud_signal_count,
    total_transactions,
    fraud_score

FROM novabank_prod.ml.production_features

"""

production_df = spark.sql(
    production_query
).toPandas()

# ============================================================
# Feature Drift Calculation
# ============================================================

feature_results = []

feature_columns = [
    "transaction_amount",
    "fraud_signal_count",
    "total_transactions",
    "fraud_score"
]

for feature in feature_columns:

    statistic, p_value = ks_2samp(
        reference_df[feature],
        production_df[feature]
    )

    drift_detected = (
        statistic > FEATURE_DRIFT_THRESHOLD
    )

    feature_results.append({

        "feature": feature,

        "ks_statistic": round(
            statistic,
            4
        ),

        "drift_detected": drift_detected

    })

# ============================================================
# Drift Summary
# ============================================================

feature_drift_df = pd.DataFrame(
    feature_results
)

total_drifted_features = len(
    feature_drift_df[
        feature_drift_df["drift_detected"]
    ]
)

# ============================================================
# Prediction Drift Check
# ============================================================

prediction_query = """

SELECT

    prediction_probability

FROM novabank_prod.ml.predictions

WHERE prediction_date >= date_sub(
    current_date(),
    7
)

"""

prediction_df = spark.sql(
    prediction_query
).toPandas()

baseline_probability = 0.50

current_probability = (
    prediction_df[
        "prediction_probability"
    ].mean()
)

prediction_drift = abs(
    current_probability
    - baseline_probability
)

prediction_drift_detected = (
    prediction_drift
    > PREDICTION_DRIFT_THRESHOLD
)

# ============================================================
# Production Performance Metrics
# ============================================================

performance_query = """

SELECT

    accuracy,
    recall,
    precision,
    f1_score

FROM novabank_prod.ml.model_metrics

ORDER BY evaluation_timestamp DESC

LIMIT 1

"""

performance_df = spark.sql(
    performance_query
).toPandas()

accuracy = float(
    performance_df["accuracy"][0]
)

performance_issue = (
    accuracy < ACCURACY_THRESHOLD
)

# ============================================================
# Alert Generation
# ============================================================

alerts = []

if total_drifted_features > 0:

    alerts.append(
        f"{total_drifted_features} "
        f"features show drift"
    )

if prediction_drift_detected:

    alerts.append(
        "Prediction drift threshold exceeded"
    )

if performance_issue:

    alerts.append(
        "Model accuracy below threshold"
    )

# ============================================================
# Monitoring Summary
# ============================================================

summary = {

    "monitoring_timestamp":
        datetime.utcnow(),

    "drifted_features":
        total_drifted_features,

    "prediction_drift":
        round(
            prediction_drift,
            4
        ),

    "accuracy":
        accuracy,

    "alert_count":
        len(alerts)
}

summary_df = pd.DataFrame(
    [summary]
)

spark.createDataFrame(
    summary_df
).write \
 .format("delta") \
 .mode("append") \
 .saveAsTable(
    "novabank_prod.ml.model_drift_monitoring"
 )

# ============================================================
# Retraining Recommendation
# ============================================================

if len(alerts) > 0:

    print(
        "RETRAINING RECOMMENDED"
    )

    for alert in alerts:

        print(
            f"ALERT: {alert}"
        )

else:

    print(
        "Model Performance Normal"
    )

# ============================================================
# Completion
# ============================================================

print(
    "Model Drift Monitoring Completed"
)
