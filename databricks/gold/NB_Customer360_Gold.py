# =============================================================
# Notebook : NB_Customer360_Gold
# Layer    : Gold
# Domain   : Customer360
# Purpose  : Unified Customer360 Gold Dataset
# =============================================================

from pyspark.sql import functions as F

# =============================================================
# Configuration
# =============================================================

CUSTOMER_TABLE = (
    "novabank_prod.customer.customer_silver"
)

TRANSACTION_TABLE = (
    "novabank_prod.transactions.transactions_silver"
)

FRAUD_CASE_TABLE = (
    "novabank_prod.fraud.fraud_cases_silver"
)

RISK_SCORE_TABLE = (
    "novabank_prod.risk.risk_scores_silver"
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

customer_df = spark.table(
    CUSTOMER_TABLE
)

transaction_df = spark.table(
    TRANSACTION_TABLE
)

fraud_case_df = spark.table(
    FRAUD_CASE_TABLE
)

risk_df = spark.table(
    RISK_SCORE_TABLE
)

# =============================================================
# Transaction Aggregation
# =============================================================

txn_agg_df = (
    transaction_df
    .groupBy("CustomerID")
    .agg(
        F.count("*")
            .alias("TotalTransactions"),

        F.round(
            F.sum("TransactionAmount"), 2
        ).alias(
            "TotalTransactionAmount"
        ),

        F.round(
            F.avg("TransactionAmount"), 2
        ).alias(
            "AverageTransactionAmount"
        ),

        F.max("TransactionDate")
            .alias("LastTransactionDate"),

        F.sum(
            F.when(
                F.col(
                    "PotentialFraudFlag"
                ) == "Y",
                1
            ).otherwise(0)
        ).alias(
            "FraudAlertCount"
        )
    )
)

# =============================================================
# Fraud Aggregation
# =============================================================

fraud_agg_df = (
    fraud_case_df
    .groupBy("CustomerID")
    .agg(
        F.max("fraud_score")
            .alias("LatestFraudScore"),

        F.count("*")
            .alias("FraudCaseCount"),

        F.max("status")
            .alias("LatestFraudStatus")
    )
)

# =============================================================
# Customer360 Join
# =============================================================

customer360_df = (
    customer_df.alias("c")

    .join(
        txn_agg_df.alias("t"),
        "CustomerID",
        "left"
    )

    .join(
        fraud_agg_df.alias("f"),
        "CustomerID",
        "left"
    )

    .join(
        risk_df.alias("r"),
        "CustomerID",
        "left"
    )
)

# =============================================================
# Null Handling
# =============================================================

customer360_df = (
    customer360_df.fillna({
        "TotalTransactions": 0,
        "TotalTransactionAmount": 0,
        "AverageTransactionAmount": 0,
        "FraudAlertCount": 0,
        "LatestFraudScore": 0,
        "FraudCaseCount": 0,
        "Exposure": 0,
        "RiskScore": 0
    })
)

# =============================================================
# Customer Spend Segment
# =============================================================

customer360_df = (
    customer360_df
    .withColumn(
        "CustomerSpendSegment",

        F.when(
            F.col(
                "TotalTransactionAmount"
            ) >= 100000,

            "PREMIUM"
        )

        .when(
            F.col(
                "TotalTransactionAmount"
            ) >= 50000,

            "GOLD"
        )

        .otherwise(
            "STANDARD"
        )
    )
)

# =============================================================
# Fraud Risk Category
# =============================================================

customer360_df = (
    customer360_df
    .withColumn(
        "FraudRiskCategory",

        F.when(
            F.col("LatestFraudScore") >= 90,

            "CRITICAL"
        )

        .when(
            F.col("LatestFraudScore") >= 75,

            "HIGH"
        )

        .when(
            F.col("LatestFraudScore") >= 60,

            "MEDIUM"
        )

        .otherwise(
            "LOW"
        )
    )
)

# =============================================================
# Risk Category
# =============================================================

customer360_df = (
    customer360_df
    .withColumn(
        "EnterpriseRiskCategory",

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

# =============================================================
# Customer360 Tier
# =============================================================

customer360_df = (
    customer360_df
    .withColumn(
        "Customer360Tier",

        F.when(
            (F.col(
                "LatestFraudScore"
            ) >= 90)

            |

            (F.col(
                "RiskScore"
            ) >= 90),

            "CRITICAL"
        )

        .when(
            (F.col(
                "LatestFraudScore"
            ) >= 75)

            |

            (F.col(
                "RiskScore"
            ) >= 70),

            "HIGH"
        )

        .when(
            (F.col(
                "RiskScore"
            ) >= 30),

            "MEDIUM"
        )

        .otherwise(
            "LOW"
        )
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
        .option(
            "overwriteSchema",
            "true"
        )
        .saveAsTable(
            TARGET_TABLE
        )
)

# =============================================================
# Performance Optimisation
# =============================================================

spark.sql(
    f"OPTIMIZE {TARGET_TABLE}"
)

# Optional

spark.sql(
    f"""
    OPTIMIZE {TARGET_TABLE}
    ZORDER BY (
        CustomerID,
        Customer360Tier
    )
    """
)

# =============================================================
# Audit Logging
# =============================================================

record_count = (
    customer360_df.count()
)

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
        .saveAsTable(
            AUDIT_TABLE
        )
)

# =============================================================
# Validation
# =============================================================

print(
    f"""
Customer360 Records Created:
{record_count}
"""
)

print(
    "NB_Customer360_Gold Completed Successfully"
)
