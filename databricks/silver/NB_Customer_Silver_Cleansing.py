# =====================================================
# Notebook: NB_Customer_Silver_Cleansing
# Layer    : Silver
# Domain   : Customer
# Purpose  : Clean and standardize customer data
# =====================================================

from pyspark.sql import functions as F
from pyspark.sql.window import Window

# =====================================================
# Configuration
# =====================================================

BRONZE_TABLE = (
    "novabank_prod.customer.customer_bronze"
)

SILVER_TABLE = (
    "novabank_prod.customer.customer_silver"
)

AUDIT_TABLE = (
    "novabank_prod.audit.audit_pipeline_runs"
)

# =====================================================
# Read Bronze Layer
# =====================================================

customer_df = spark.table(BRONZE_TABLE)

# =====================================================
# Standardization
# =====================================================

customer_df = (
    customer_df
        .withColumn(
            "FirstName",
            F.initcap(F.trim(F.col("FirstName")))
        )
        .withColumn(
            "LastName",
            F.initcap(F.trim(F.col("LastName")))
        )
        .withColumn(
            "EmailAddress",
            F.lower(F.trim(F.col("EmailAddress")))
        )
        .withColumn(
            "CountryCode",
            F.upper(F.trim(F.col("CountryCode")))
        )
)

# =====================================================
# Remove Invalid Records
# =====================================================

customer_df = (
    customer_df
        .filter(F.col("CustomerID").isNotNull())
        .filter(F.col("CustomerNumber").isNotNull())
)

# =====================================================
# Email Validation
# =====================================================

customer_df = (
    customer_df.withColumn(
        "ValidEmail",
        F.when(
            F.col("EmailAddress").rlike(
                "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$"
            ),
            "Y"
        ).otherwise("N")
    )
)

# =====================================================
# Deduplication
# =====================================================

window_spec = Window.partitionBy(
    "CustomerID"
).orderBy(
    F.col("bronze_load_timestamp").desc()
)

customer_df = (
    customer_df
        .withColumn(
            "row_num",
            F.row_number().over(window_spec)
        )
        .filter(F.col("row_num") == 1)
        .drop("row_num")
)

# =====================================================
# Data Enrichment
# =====================================================

customer_df = (
    customer_df
        .withColumn(
            "CustomerFullName",
            F.concat_ws(
                " ",
                F.col("FirstName"),
                F.col("LastName")
            )
        )
)

customer_df = (
    customer_df
        .withColumn(
            "RecordSource",
            F.lit("CoreBanking")
        )
)

customer_df = (
    customer_df
        .withColumn(
            "SilverLoadTimestamp",
            F.current_timestamp()
        )
)

# =====================================================
# Data Quality Metrics
# =====================================================

record_count = customer_df.count()

invalid_email_count = (
    customer_df
        .filter(F.col("ValidEmail") == "N")
        .count()
)

print(
    f"Valid Customer Records : {record_count}"
)

print(
    f"Invalid Emails : {invalid_email_count}"
)

# =====================================================
# Persist Silver Layer
# =====================================================

(
    customer_df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(SILVER_TABLE)
)

# =====================================================
# Audit Logging
# =====================================================

audit_df = spark.createDataFrame(
    [
        (
            "customer_silver",
            record_count,
            invalid_email_count
        )
    ],
    [
        "pipeline_name",
        "records_processed",
        "data_quality_issues"
    ]
)

(
    audit_df.write
            .format("delta")
            .mode("append")
            .saveAsTable(AUDIT_TABLE)
)

# =====================================================
# Optimization
# =====================================================

spark.sql(
    f"OPTIMIZE {SILVER_TABLE}"
)

# =====================================================
# Completion
# =====================================================

print(
    "Customer Silver Cleansing Completed Successfully"
)
