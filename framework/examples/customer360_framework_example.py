# ============================================================
# Customer360 Gold Example
# Framework Usage Example
# ============================================================

from pyspark.sql import functions as F

from framework.NB_Audit_Framework import AuditFramework
from framework.NB_DQ_Framework import DataQualityFramework
from framework.NB_Quarantine_Framework import QuarantineFramework

# ============================================================
# Configuration
# ============================================================

CUSTOMER_TABLE = (
    "novabank_prod.customer.customer_silver"
)

TARGET_TABLE = (
    "novabank_prod.analytics.customer360_gold"
)

AUDIT_TABLE = (
    "novabank_prod.audit.audit_pipeline_runs"
)

QUARANTINE_TABLE = (
    "novabank_prod.audit.quarantine_records"
)

# ============================================================
# Framework Initialisation
# ============================================================

dq = DataQualityFramework()

audit = AuditFramework(
    spark,
    AUDIT_TABLE
)

quarantine = QuarantineFramework(
    QUARANTINE_TABLE
)

# ============================================================
# Read Data
# ============================================================

customer_df = spark.table(
    CUSTOMER_TABLE
)

# ============================================================
# Data Quality Checks
# ============================================================

dq.validate_required_columns(
    customer_df,
    [
        "CustomerID"
    ]
)

duplicate_count = (
    dq.check_duplicates(
        customer_df,
        "CustomerID"
    )
)

if duplicate_count > 0:

    raise Exception(
        "Duplicate CustomerID Found"
    )

# ============================================================
# Quarantine Invalid Data
# ============================================================

valid_df, invalid_df = (
    quarantine.filter_valid_records(
        customer_df,
        F.col("CustomerID").isNotNull()
    )
)

quarantine.quarantine_records(
    invalid_df,
    "CustomerID Missing"
)

# ============================================================
# Gold Processing
# ============================================================

customer360_df = (
    valid_df
    .withColumn(
        "GoldLoadTimestamp",
        F.current_timestamp()
    )
)

# ============================================================
# Write Gold
# ============================================================

(
    customer360_df.write
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
    pipeline_name="NB_Customer360_Gold",
    layer="GOLD",
    source_table=CUSTOMER_TABLE,
    target_table=TARGET_TABLE,
    records_processed=customer360_df.count(),
    status="SUCCESS"
)
