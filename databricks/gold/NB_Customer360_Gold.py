# =============================================================
# Notebook : NB_Customer360_Gold
# Layer    : Gold
# Domain   : Customer 360
# Purpose  : Create Customer 360 analytics table
# =============================================================

from pyspark.sql import functions as F
from pyspark.sql.window import Window

# =============================================================
# Configuration
# =============================================================

CUSTOMER_TABLE = (
    "novabank_prod.customer.customer_silver"
)

TRANSACTION_TABLE = (
    "novabank_prod.transactions.transactions_silver"
)

TARGET_TABLE = (
    "novabank_prod.analytics.customer360_gold"
)

AUDIT_TABLE = (
    "novabank_prod.audit.audit_pipeline_runs"
)

# =============================================================
# Read Source Tables
# =============================================================

customer_df = spark.table(CUSTOMER_TABLE)

transaction_df = spark.table(TRANSACTION_TABLE)

# =============================================================
# Customer Level Aggregation
# =============================================================

txn_agg_df = (
    transaction_df
    .groupBy("CustomerID")
    .agg(
        F.count("*")
            .alias("TotalTransactions"),

        F.sum("TransactionAmount")
            .alias("TotalTransactionAmount"),

        F.avg("TransactionAmount")
            .alias("AverageTransactionAmount"),

        F.max("TransactionDate")
            .alias("LastTransactionDate"),

        F.sum(
            F.when(
                F.col("PotentialFraudFlag") == "Y",
                1
            ).otherwise(0)
        ).alias("FraudAlertCount")
    )
)

# =============================================================
# Customer 360 Creation
# =============================================================

customer360_df = (
    customer_df.alias("c")
    .join(
        txn_agg_df.alias("t"),
        "CustomerID",
        "left"
    )
)

# =============================================================
# Null Handling
# =============================================================

customer360_df = (
    customer360_df
    .fillna(
        {
            "TotalTransactions": 0,
            "TotalTransactionAmount": 0,
            "AverageTransactionAmount": 0,
            "FraudAlertCount": 0
        }
    )
)

# =============================================================
# Risk Segmentation
# =============================================================

customer360_df = (
    customer360_df
    .withColumn(
        "CustomerSegment",
        F.when(
            F.col("TotalTransactionAmount") >= 100000,
            "PREMIUM"
        )
        .when(
            F.col("TotalTransactionAmount") >= 25000,
            "GOLD"
        )
        .otherwise("STANDARD")
    )
)

# =============================================================
# Fraud Category
# =============================================================

customer360_df = (
    customer360_df
    .withColumn(
        "FraudRiskCategory",
        F.when(
            F.col("FraudAlertCount") >= 10,
            "HIGH"
        )
        .when(
            F.col("FraudAlertCount") >= 3,
            "MEDIUM"
        )
        .otherwise("LOW")
    )
)

# =============================================================
# Technical Columns
# =============================================================

customer360_df = (
    customer360_df
    .withColumn(
        "GoldLoadTimestamp",
        F.current_timestamp()
    )
)

# =============================================================
# Write Gold Table
# =============================================================

(
    customer360_df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(TARGET_TABLE)
)

# =============================================================
# Optimize Gold Table
# =============================================================

spark.sql(
    f"OPTIMIZE {TARGET_TABLE}"
)

# =============================================================
# Audit Logging
# =============================================================

record_count = customer360_df.count()

audit_df = spark.createDataFrame(
    [
        (
            "customer360_gold",
            record_count
        )
    ],
    [
        "pipeline_name",
        "records_processed"
    ]
)

(
    audit_df.write
        .format("delta")
        .mode("append")
        .saveAsTable(AUDIT_TABLE)
)

# =============================================================
# Validation
# =============================================================

print(
    f"Customer360 Records Created : {record_count}"
)

print(
    "NB_Customer360_Gold Completed Successfully"
)
