# =====================================================
# Notebook: NB_Customer_Bronze_Load
# Layer    : Bronze
# Domain   : Customer
# Purpose  : Load raw customer data into Delta Lake
# =====================================================

from pyspark.sql import functions as F
from pyspark.sql.types import *
from pyspark.sql import SparkSession
from datetime import datetime

# =====================================================
# Configuration
# =====================================================

SOURCE_PATH = (
    "abfss://bronze@stnovabankdev.dfs.core.windows.net/"
    "customer/"
)

TARGET_TABLE = (
    "novabank_prod.customer.customer_bronze"
)

LOAD_TIMESTAMP = datetime.utcnow()

# =====================================================
# Load Raw Data
# =====================================================

customer_df = (
    spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(SOURCE_PATH)
)

# =====================================================
# Technical Columns
# =====================================================

customer_df = (
    customer_df
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

record_count = customer_df.count()

print(f"Records Loaded : {record_count}")

required_columns = [
    "CustomerID",
    "CustomerNumber",
    "FirstName",
    "LastName"
]

for column_name in required_columns:
    null_count = (
        customer_df
        .filter(F.col(column_name).isNull())
        .count()
    )

    print(
        f"{column_name} Null Records : {null_count}"
    )

# =====================================================
# Persist Bronze Data
# =====================================================

(
    customer_df.write
    .format("delta")
    .mode("append")
    .option("mergeSchema", "true")
    .saveAsTable(TARGET_TABLE)
)

# =====================================================
# Validation
# =====================================================

validation_count = (
    spark.table(TARGET_TABLE)
         .count()
)

print(
    f"Customer Bronze Table Count : "
    f"{validation_count}"
)

# =====================================================
# Audit Logging
# =====================================================

audit_df = spark.createDataFrame(
    [
        (
            "customer",
            record_count,
            LOAD_TIMESTAMP
        )
    ],
    [
        "domain",
        "records_loaded",
        "load_timestamp"
    ]
)

(
    audit_df.write
    .format("delta")
    .mode("append")
    .saveAsTable(
        "novabank_prod.audit.audit_pipeline_runs"
    )
)

print(
    "NB_Customer_Bronze_Load completed successfully"
)
