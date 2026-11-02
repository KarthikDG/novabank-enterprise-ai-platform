# =====================================================
# Notebook: NB_Transaction_Bronze_Load
# Layer    : Bronze
# Domain   : Transactions
# Purpose  : Load raw transaction data into Delta Lake
# =====================================================

from pyspark.sql import functions as F
from pyspark.sql import SparkSession
from datetime import datetime

# =====================================================
# Configuration
# =====================================================

SOURCE_PATH = (
    "abfss://bronze@stnovabankdev.dfs.core.windows.net/"
    "transactions/"
)

TARGET_TABLE = (
    "novabank_prod.transactions.transactions_bronze"
)

AUDIT_TABLE = (
    "novabank_prod.audit.audit_pipeline_runs"
)

LOAD_TIMESTAMP = datetime.utcnow()

# =====================================================
# Read Raw Files
# =====================================================

transactions_df = (
    spark.read
         .option("header", "true")
         .option("inferSchema", "true")
         .csv(SOURCE_PATH)
)

# =====================================================
# Add Technical Columns
# =====================================================

transactions_df = (
    transactions_df
        .withColumn(
            "bronze_load_timestamp",
            F.current_timestamp()
        )
        .withColumn(
            "source_system",
            F.lit("CoreBanking")
        )
)

# =====================================================
# Data Quality Checks
# =====================================================

record_count = transactions_df.count()

print(f"Records Loaded: {record_count}")

required_columns = [
    "TransactionID",
    "CustomerID",
    "TransactionAmount",
    "TransactionDate"
]

for column_name in required_columns:

    null_count = (
        transactions_df
        .filter(F.col(column_name).isNull())
        .count()
    )

    print(
        f"{column_name} Null Count = {null_count}"
    )

# =====================================================
# Duplicate Analysis
# =====================================================

duplicate_count = (
    transactions_df
    .groupBy("TransactionID")
    .count()
    .filter(F.col("count") > 1)
    .count()
)

print(
    f"Duplicate Transaction IDs: {duplicate_count}"
)

# =====================================================
# Write Bronze Table
# =====================================================

(
    transactions_df.write
        .format("delta")
        .mode("append")
        .option("mergeSchema", "true")
        .saveAsTable(TARGET_TABLE)
)

# =====================================================
# Validation
# =====================================================

table_count = (
    spark.table(TARGET_TABLE)
         .count()
)

print(
    f"Bronze Transaction Count: {table_count}"
)

# =====================================================
# Audit Logging
# =====================================================

audit_df = spark.createDataFrame(
    [
        (
            "transactions",
            record_count,
            duplicate_count,
            LOAD_TIMESTAMP
        )
    ],
    [
        "domain",
        "records_loaded",
        "duplicate_records",
        "load_timestamp"
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

spark.sql(f"""
OPTIMIZE {TARGET_TABLE}
""")

# =====================================================
# Completion Status
# =====================================================

print(
    "Transaction Bronze Load Completed Successfully"
)
