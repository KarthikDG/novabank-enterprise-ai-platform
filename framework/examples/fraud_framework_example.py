# ============================================================
# Fraud Analytics Example
# Framework Usage Example
# ============================================================

from pyspark.sql import functions as F

from framework.NB_Audit_Framework import AuditFramework
from framework.NB_DQ_Framework import DataQualityFramework
from framework.NB_Quarantine_Framework import QuarantineFramework

FRAUD_TABLE = (
    "novabank_prod.fraud.fraud_cases_silver"
)

TARGET_TABLE = (
    "novabank_prod.analytics.fraud_scores_gold"
)

AUDIT_TABLE = (
    "novabank_prod.audit.audit_pipeline_runs"
)

QUARANTINE_TABLE = (
    "novabank_prod.audit.quarantine_records"
)

dq = DataQualityFramework()

audit = AuditFramework(
    spark,
    AUDIT_TABLE
)

quarantine = QuarantineFramework(
    QUARANTINE_TABLE
)

fraud_df = spark.table(
    FRAUD_TABLE
)

# ============================================================
# Schema Validation
# ============================================================

dq.validate_required_columns(
    fraud_df,
    [
        "CustomerID",
        "fraud_score"
    ]
)

# ============================================================
# Quarantine Invalid Scores
# ============================================================

valid_df, invalid_df = (
    quarantine.filter_valid_records(
        fraud_df,

        (
            F.col("fraud_score") >= 0
        )
        &
        (
            F.col("fraud_score") <= 100
        )
    )
)

quarantine.quarantine_records(
    invalid_df,
    "Invalid Fraud Score"
)

# ============================================================
# Fraud Analytics
# ============================================================

fraud_gold_df = (
    valid_df
    .groupBy("CustomerID")
    .agg(
        F.max(
            "fraud_score"
        ).alias(
            "LatestFraudScore"
        ),

        F.count("*")
        .alias(
            "FraudCaseCount"
        )
    )
)

(
    fraud_gold_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(
        TARGET_TABLE
    )
)

audit.write_audit_record(
    "NB_Fraud_Analytics_Gold",
    "GOLD",
    FRAUD_TABLE,
    TARGET_TABLE,
    fraud_gold_df.count(),
    "SUCCESS"
)
