# ============================================================
# Script     : Create_Vector_Index.py
# Domain     : Generative AI
# Purpose    : Create and maintain vector search index
# Platform   : Databricks Vector Search
# ============================================================

from datetime import datetime

# ============================================================
# Configuration
# ============================================================

CATALOG = "novabank_prod"

SCHEMA = "genai"

EMBEDDING_TABLE = (
    "novabank_prod.genai.document_embeddings"
)

VECTOR_INDEX_NAME = (
    "policy_vector_index"
)

PRIMARY_KEY = "chunk_id"

EMBEDDING_COLUMN = "embedding_vector"

SYNC_MODE = "TRIGGERED"

# ============================================================
# Read Embedding Source
# ============================================================

embedding_df = spark.sql(
    f"""
    SELECT *
    FROM {EMBEDDING_TABLE}
    """
)

record_count = embedding_df.count()

print(
    f"Embedding Records Found: {record_count}"
)

# ============================================================
# Databricks Vector Search Endpoint
# ============================================================

endpoint_name = (
    "novabank-vector-search-endpoint"
)

print(
    f"Endpoint: {endpoint_name}"
)

# ============================================================
# Create Index Configuration
# ============================================================

index_configuration = {

    "index_name":
        VECTOR_INDEX_NAME,

    "source_table":
        EMBEDDING_TABLE,

    "primary_key":
        PRIMARY_KEY,

    "embedding_column":
        EMBEDDING_COLUMN,

    "pipeline_type":
        "TRIGGERED"

}

print(
    "Vector Index Configuration Created"
)

# ============================================================
# Metadata Validation
# ============================================================

required_columns = [

    "chunk_id",

    "document_id",

    "document_name",

    "document_type",

    "embedding_vector"

]

for column_name in required_columns:

    if column_name not in embedding_df.columns:

        raise Exception(
            f"Missing Column: {column_name}"
        )

# ============================================================
# Index Statistics
# ============================================================

document_count = (

    embedding_df
    .select("document_id")
    .distinct()
    .count()

)

print(
    f"Unique Documents: {document_count}"
)

# ============================================================
# Audit Information
# ============================================================

audit_df = spark.createDataFrame(

    [

        (
            VECTOR_INDEX_NAME,

            record_count,

            document_count,

            datetime.utcnow()
        )

    ],

    [

        "vector_index_name",

        "embedding_records",

        "documents",

        "created_timestamp"

    ]

)

(
    audit_df.write
    .format("delta")
    .mode("append")
    .saveAsTable(
        "novabank_prod.genai.vector_index_audit"
    )
)

# ============================================================
# Example Search Payload
# ============================================================

example_search = {

    "query":
        "What is the KYC process?",

    "top_k":
        5

}

print(
    f"Sample Search Query: "
    f"{example_search['query']}"
)

# ============================================================
# Completion
# ============================================================

print(
    "Vector Index Creation Completed Successfully"
)
