# =============================================================
# Notebook : NB_Customer360_Gold
# Layer    : Gold
# Domain   : Customer360
# Purpose  : Unified Customer360 Analytics Dataset
# =============================================================

from pyspark.sql import functions as F
from delta.tables import DeltaTable

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
# Helper Functions
# =============================================================

def validate_columns(
    dataframe,
    required_columns,
    table_name
):
    missing_columns = list(
        set(required_columns)
        - set(dataframe.columns)
    )

    if missing_columns:
        raise Exception(
            f"""
            Missing columns in {table_name}
            {missing_columns}
            """
        )


def standardise_columns(df):

    for col_name in df.columns:

        cleaned_name = (
            col_name
            .strip()
            .replace(" ", "")
        )

        df = (
            df.withColumnRenamed(
                col_name,
                cleaned_name
            )
        )

    return df

# =============================================================
# Read Tables
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
# Standardise Column Names
# =============================================================

customer_df = standardise_columns(
    customer_df
)

transaction_df = standardise_columns(
    transaction_df
)

fraud_case_df = standardise_columns(
    fraud_case_df
)

risk_df = standardise_columns(
    risk_df
)

# =============================================================
# Schema Validation
# =============================================================

validate_columns(
    customer_df,
    [
        "CustomerID"
    ],
    CUSTOMER_TABLE
)

validate_columns(
    transaction_df,
    [
        "CustomerID",
        "TransactionAmount",
        "TransactionDate"
    ],
    TRANSACTION_TABLE
)

validate_columns(
    fraud_case_df,
    [
        "CustomerID",
        "fraud_score"
    ],
    FRAUD_CASE_TABLE
)

validate_columns(
    risk_df,
    [
        "CustomerID",
        "RiskScore",
        "Exposure"
    ],
    RISK_SCORE_TABLE
)

# =============================================================
# Duplicate Validation
# =============================================================

duplicate_customer_df = (
    customer_df
    .groupBy("CustomerID")
    .count()
    .filter("count > 1")
)

if duplicate_customer_df.count() > 0:

    duplicate_customer_df.show(
        truncate=False
    )

    raise Exception(
        """
        Duplicate CustomerID detected
        in customer_silver
        """
    )

# =============================================================
# Transaction Aggregation
# =============================================================

txn_agg_df = (
    transaction_df
    .groupBy("CustomerID")
    .agg(

        F.count("*")
        .alias(
            "TotalTransactions"
        ),

        F.round(
            F.sum(
                "TransactionAmount"
            ),
            2
        )
        .alias(
            "TotalTransactionAmount"
        ),

        F.round(
            F.avg(
                "TransactionAmount"
            ),
            2
        )
        .alias(
            "AverageTransactionAmount"
        ),

        F.max(
            "TransactionDate"
        )
        .alias(
            "LastTransactionDate"
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

        F.count("*")
        .alias(
            "FraudCaseCount"
        ),

        F.max(
            "fraud_score"
        )
        .alias(
            "LatestFraudScore"
        )
    )
)

# =============================================================
# Customer360 Join
# =============================================================

customer360_df = (
    customer_df

    .join(
        txn_agg_df,
        "CustomerID",
        "left"
    )

    .join(
        fraud_agg_df,
        "CustomerID",
        "left"
    )

    .join(
        risk_df,
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
            "FraudCaseCount": 0,
            "LatestFraudScore": 0,
            "RiskScore": 0,
            "Exposure": 0
        }
    )
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
            F.col(
                "LatestFraudScore"
            ) >= 90,

            "CRITICAL"
        )

        .when(
            F.col(
                "LatestFraudScore"
            ) >= 75,

            "HIGH"
        )

        .when(
            F.col(
                "LatestFraudScore"
            ) >= 60,

            "MEDIUM"
        )

        .otherwise(
            "LOW"
        )
    )
)

# =============================================================
# Enterprise Risk Category
# =============================================================

customer360_df = (
    customer360_df
    .withColumn(
        "EnterpriseRiskCategory",

        F.when(
            F.col(
                "RiskScore"
            ) >= 70,

            "HIGH"
        )

        .when(
            F.col(
                "RiskScore"
            ) >= 30,

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
            (
                F.col(
                    "LatestFraudScore"
                ) >= 90
            )
            |
            (
                F.col(
                    "RiskScore"
                ) >= 90
            ),

            "CRITICAL"
        )

        .when(
            (
                F.col(
                    "LatestFraudScore"
                ) >= 75
            )
            |
            (
                F.col(
                    "RiskScore"
                ) >= 70
            ),

            "HIGH"
        )

        .when(
            F.col(
                "RiskScore"
            ) >= 30,

            "MEDIUM"
        )

        .otherwise(
            "LOW"
        )
    )
)

# =============================================================
# Data Quality Metrics
# =============================================================

null_customer_count = (
    customer360_df
    .filter(
        F.col(
            "CustomerID"
        ).isNull()
    )
    .count()
)

negative_amount_count = (
    customer360_df
    .filter(
        F.col(
            "TotalTransactionAmount"
        ) < 0
    )
    .count()
)

# =============================================================
# Metadata Columns
# =============================================================

customer360_df = (
    customer360_df
    .withColumn(
        "GoldLoadTimestamp",
        F.current_timestamp()
    )
)

# =============================================================
# Delta Merge
# =============================================================

if not spark.catalog.tableExists(
    TARGET_TABLE
):

    (
        customer360_df.write
        .format("delta")
        .saveAsTable(
            TARGET_TABLE
        )
    )

else:

    target = DeltaTable.forName(
        spark,
        TARGET_TABLE
    )

    (
        target.alias("t")
        .merge(
            customer360_df.alias("s"),

            """
            t.CustomerID =
            s.CustomerID
            """
        )

        .whenMatchedUpdateAll()

        .whenNotMatchedInsertAll()

        .execute()
    )

# =============================================================
# Optimize
# =============================================================

spark.sql(
    f"""
    OPTIMIZE {TARGET_TABLE}
    """
)

spark.sql(
    f"""
    OPTIMIZE {TARGET_TABLE}
    ZORDER BY (
        CustomerID,
        Customer360Tier,
        EnterpriseRiskCategory
    )
    """
)

# =============================================================
# Audit Metrics
# =============================================================

record_count = (
    customer360_df.count()
)

audit_df = spark.createDataFrame(
    [
        (
            "customer360_gold",
            record_count,
            null_customer_count,
            negative_amount_count
        )
    ],
    [
        "pipeline_name",
        "records_processed",
        "null_customer_count",
        "negative_amount_count"
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
# Validation Output
# =============================================================

print(
    f"""
Customer360 Records Processed :
{record_count}
"""
)

print(
    f"""
Null Customer IDs :
{null_customer_count}
"""
)

print(
    f"""
Negative Amount Records :
{negative_amount_count}
"""
)

print(
    "NB_Customer360_Gold Completed Successfully"
)
