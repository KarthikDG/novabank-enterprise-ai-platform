# ============================================================
# Risk Analytics Example
# Framework Usage Example
# ============================================================

from pyspark.sql import functions as F

from framework.NB_Audit_Framework import AuditFramework
from framework.NB_DQ_Framework import DataQualityFramework
from framework.NB_Quarantine_Framework import QuarantineFramework
from framework.NB_Watermark_Framework import WatermarkFramework

# ============================================================
# Configuration
# ============================================================

RISK_TABLE = (
    "novabank_prod.risk.risk_scores_silver"
)

TARGET_TABLE = (
    "novabank_prod.analytics.risk_scores_gold"
)

AUDIT_TABLE = (
    "novabank_prod.audit.audit_pipeline_runs"
)

QUARANTINE_TABLE = (
    "novabank_prod.audit.quarantine_records"
)

WATERMARK_TABLE = (
    "novabank_prod.control.pipeline_watermarks"
)

# ============================================================
# Framework Setup
# ============================================================

dq = DataQualityFramework()

audit = AuditFramework(
    spark,
    AUDIT_TABLE
)

quarantine = QuarantineFramework(
    QUARANTINE_TABLE
)

watermark = WatermarkFramework(
    spark,
    WATERMARK_TABLE
)

# ============================================================
# Read Risk Data
# ============================================================

risk_df = spark.table(
    RISK_TABLE
)

# ============================================================
# Schema Validation
# ============================================================

dq.validate_required_columns(
    risk_df,
    [
        "CustomerID",
        "RiskScore",
        "Exposure"
    ]
)

# ============================================================
# Quarantine Invalid Risk Scores
# ============================================================

valid_df, invalid_df = (
    quarantine.filter_valid_records(

        risk_df,

        (
            F.col("RiskScore") >= 0
        )
        &
        (
            F.col("RiskScore") <= 100
        )
    )
)

quarantine.quarantine_records(
    invalid_df,
    "Invalid Risk Score"
)

# ============================================================
# Risk Categorisation
# ============================================================

risk_gold_df = (
    valid_df
    .withColumn(
        "RiskCategory",

        F.when(
            F.col("RiskScore") >= 70,
            "HIGH"
        )
        .when(
            F.col("RiskScore") >= 30,
            "MEDIUM"
        )
        .otherwise(
            "LOW"
        )
    )
)

# ============================================================
# Save Gold Layer
# ============================================================

(
    risk_gold_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(
        TARGET_TABLE
    )
)

# ============================================================
# Audit Logging
# ============================================================

audit.write_audit_record(
    pipeline_name="NB_Risk_Gold",
    layer="GOLD",
    source_table=RISK_TABLE,
    target_table=TARGET_TABLE,
    records_processed=risk_gold_df.count(),
    status="SUCCESS"
)

# ============================================================
# Watermark Example
# ============================================================

watermark.update_watermark(
    pipeline_name="NB_Risk_Gold",
    watermark_value="2026-11-02"
)
