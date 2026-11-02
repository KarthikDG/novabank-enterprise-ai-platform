# =============================================================
# Notebook : NB_FraudAnalytics_Gold
# Layer    : Gold
# Domain   : Fraud Analytics
# Purpose  : Build fraud analytics fact table and KPIs
# =============================================================

from pyspark.sql import functions as F
from pyspark.sql.window import Window

# =============================================================
# Configuration
# =============================================================

TRANSACTION_SILVER = (
    "novabank_prod.transactions.transactions_silver"
)

FRAUD_GOLD = (
    "novabank_prod.fraud.fact_fraud_analytics"
)

AUDIT_TABLE = (
    "novabank_prod.audit.audit_pipeline_runs"
)

# =============================================================
# Read Source Data
# =============================================================

transactions_df = spark.table(TRANSACTION_SILVER)

# =============================================================
# Fraud Scoring Logic
# =============================================================

fraud_df = (
    transactions_df
    .withColumn(
        "FraudScore",
        F.when(
            F.col("TransactionAmount") >= 10000,
            90
        )
        .when(
            F.col("TransactionAmount") >= 5000,
            70
        )
        .when(
            F.col("TransactionAmount") >= 1000,
            40
        )
        .otherwise(10)
    )
)

# =============================================================
# Fraud Risk Classification
# =============================================================

fraud_df = (
    fraud_df
    .withColumn(
        "FraudRiskLevel",
        F.when(
            F.col("FraudScore") >= 80,
            "HIGH"
        )
        .when(
            F.col("FraudScore") >= 50,
            "MEDIUM"
        )
        .otherwise("LOW"
        )
    )
)

# =============================================================
# High-Risk Countries
# =============================================================

high_risk_countries = [
    "XX",
    "YY",
    "ZZ"
]

fraud_df = (
    fraud_df
    .withColumn(
        "HighRiskCountryFlag",
        F.when(
            F.col("CountryCode").isin(
                high_risk_countries
            ),
            "Y"
        ).otherwise("N")
    )
)

# =============================================================
# Business KPIs
# =============================================================

fraud_df = (
    fraud_df
    .withColumn(
        "FraudReviewRequired",
        F.when(
            (
                (F.col("FraudRiskLevel") == "HIGH")
                |
                (F.col("HighRiskCountryFlag") == "Y")
            ),
            "Y"
        ).otherwise("N")
    )
)

fraud_df = (
    fraud_df
    .withColumn(
        "FraudDetectionDate",
        F.current_timestamp()
    )
)

# =============================================================
# Fraud Analytics Fact Table
# =============================================================

fact_fraud_df = fraud_df.select(
    "TransactionID",
    "CustomerID",
    "TransactionAmount",
    "TransactionDate",
    "CountryCode",
    "Channel",
    "FraudScore",
    "FraudRiskLevel",
    "HighRiskCountryFlag",
    "FraudReviewRequired",
    "FraudDetectionDate"
)

# =============================================================
# Write Gold Layer
# =============================================================

(
    fact_fraud_df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(FRAUD_GOLD)
)

# =============================================================
# Optimize Table
# =============================================================

spark.sql(
    f"OPTIMIZE {FRAUD_GOLD}"
)

# =============================================================
# KPI Reporting
# =============================================================

total_transactions = fact_fraud_df.count()

high_risk_count = (
    fact_fraud_df
    .filter(
        F.col("FraudRiskLevel") == "HIGH"
    )
    .count()
)

review_required_count = (
    fact_fraud_df
    .filter(
        F.col("FraudReviewRequired") == "Y"
    )
    .count()
)

# =============================================================
# Audit Logging
# =============================================================

audit_df = spark.createDataFrame(
    [
        (
            "fraud_analytics_gold",
            total_transactions,
            high_risk_count,
            review_required_count
        )
    ],
    [
        "pipeline_name",
        "records_processed",
        "high_risk_records",
        "review_required_records"
    ]
)

(
    audit_df.write
        .format("delta")
        .mode("append")
        .saveAsTable(AUDIT_TABLE)
)

# =============================================================
# Summary
# =============================================================

print(
    f"Total Transactions: {total_transactions}"
)

print(
    f"High Risk Transactions: {high_risk_count}"
)

print(
    f"Transactions Requiring Review: "
    f"{review_required_count}"
)

print(
    "NB_FraudAnalytics_Gold Completed Successfully"
)
