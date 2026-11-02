# =====================================================
# Notebook: NB_Transaction_Silver_Cleansing
# Layer    : Silver
# Domain   : Transactions
# Purpose  : Clean, validate and enrich transactions
# =====================================================

from pyspark.sql import functions as F
from pyspark.sql.window import Window

# =====================================================
# Configuration
# =====================================================

BRONZE_TABLE = (
    "novabank_prod.transactions.transactions_bronze"
)

SILVER_TABLE = (
    "novabank_prod.transactions.transactions_silver"
)

AUDIT_TABLE = (
    "novabank_prod.audit.audit_pipeline_runs"
)

# =====================================================
# Read Bronze Data
# =====================================================

transaction_df = spark.table(BRONZE_TABLE)

# =====================================================
# Initial Record Count
# =====================================================

source_count = transaction_df.count()

print(f"Source Record Count: {source_count}")

# =====================================================
# Data Standardization
# =====================================================

transaction_df = (
    transaction_df
    .withColumn(
        "CountryCode",
        F.upper(F.trim(F.col("CountryCode")))
    )
    .withColumn(
        "Channel",
        F.upper(F.trim(F.col("Channel")))
    )
    .withColumn(
        "MerchantCategory",
        F.upper(F.trim(F.col("MerchantCategory")))
    )
)

# =====================================================
# Data Validation
# =====================================================

transaction_df = (
    transaction_df
    .filter(F.col("TransactionID").isNotNull())
    .filter(F.col("CustomerID").isNotNull())
    .filter(F.col("TransactionDate").isNotNull())
)

transaction_df = (
    transaction_df
    .filter(F.col("TransactionAmount") > 0)
)

# =====================================================
# Duplicate Removal
# =====================================================

window_spec = (
    Window
    .partitionBy("TransactionID")
    .orderBy(F.col("bronze_load_timestamp").desc())
)

transaction_df = (
    transaction_df
    .withColumn(
        "row_num",
        F.row_number().over(window_spec)
    )
    .filter(F.col("row_num") == 1)
    .drop("row_num")
)

# =====================================================
# Fraud Indicator Enrichment
# =====================================================

transaction_df = (
    transaction_df
    .withColumn(
        "HighValueTransaction",
        F.when(
            F.col("TransactionAmount") >= 5000,
            "Y"
        ).otherwise("N")
    )
)

transaction_df = (
    transaction_df
    .withColumn(
        "PotentialFraudFlag",
        F.when(
            (
                (F.col("TransactionAmount") > 10000)
                &
                (F.col("Channel") == "ONLINE")
            ),
            "Y"
        ).otherwise("N")
    )
)

# =====================================================
# Business Attributes
# =====================================================

transaction_df = (
    transaction_df
    .withColumn(
        "TransactionYear",
        F.year("TransactionDate")
    )
    .withColumn(
        "TransactionMonth",
        F.month("TransactionDate")
    )
    .withColumn(
        "TransactionDay",
        F.dayofmonth("TransactionDate")
    )
)

transaction_df = (
    transaction_df
    .withColumn(
        "SilverLoadTimestamp",
        F.current_timestamp()
    )
)

# =====================================================
# Data Quality Metrics
# =====================================================

valid_count = transaction_df.count()

fraud_candidate_count = (
    transaction_df
    .filter(F.col("PotentialFraudFlag") == "Y")
    .count()
)

print(
    f"Valid Transactions: {valid_count}"
)

print(
    f"Fraud Candidates: {fraud_candidate_count}"
)

# =====================================================
# Write Silver Layer
# =====================================================

(
    transaction_df.write
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
            "transactions_silver",
            valid_count,
            fraud_candidate_count
        )
    ],
    [
        "pipeline_name",
        "records_processed",
        "fraud_candidates"
    ]
)

(
    audit_df.write
    .format("delta")
    .mode("append")
    .saveAsTable(AUDIT_TABLE)
)

# =====================================================
# Optimize Table
# =====================================================

spark.sql(
    f"OPTIMIZE {SILVER_TABLE}"
)

# =====================================================
# Completion
# =====================================================

print(
    "Transaction Silver Cleansing Completed Successfully"
)
