# ============================================================
# Script     : Generate_Embeddings.py
# Domain     : Generative AI
# Purpose    : Generate embeddings for enterprise documents
# Platform   : Azure OpenAI + Databricks
# ============================================================

from datetime import datetime
import uuid

# ============================================================
# Configuration
# ============================================================

EMBEDDING_MODEL = "text-embedding-3-large"

DOCUMENT_TABLE = (
    "novabank_prod.genai.document_repository"
)

CHUNK_TABLE = (
    "novabank_prod.genai.document_chunks"
)

EMBEDDING_TABLE = (
    "novabank_prod.genai.document_embeddings"
)

MAX_CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

# ============================================================
# Chunking Function
# ============================================================

def split_text_into_chunks(
    text: str,
    chunk_size: int = MAX_CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(
            text[start:end]
        )

        start = end - overlap

    return chunks

# ============================================================
# Embedding Function
# ============================================================

def generate_embedding(
    text: str
):

    response = azure_openai.embeddings.create(

        model=EMBEDDING_MODEL,

        input=text

    )

    return response.data[0].embedding

# ============================================================
# Read Documents
# ============================================================

documents_df = spark.sql(
    f"""
    SELECT
        document_id,
        document_name,
        document_type,
        source_system,
        document_content
    FROM {DOCUMENT_TABLE}
    """
)

documents = documents_df.collect()

# ============================================================
# Process Documents
# ============================================================

embedding_records = []

chunk_records = []

for document in documents:

    chunks = split_text_into_chunks(
        document.document_content
    )

    chunk_number = 1

    for chunk in chunks:

        chunk_id = str(
            uuid.uuid4()
        )

        chunk_records.append(

            (
                chunk_id,
                document.document_id,
                chunk_number,
                chunk,
                datetime.utcnow()
            )

        )

        embedding = generate_embedding(
            chunk
        )

        embedding_records.append(

            (
                chunk_id,
                document.document_id,
                document.document_name,
                document.document_type,
                document.source_system,
                embedding,
                datetime.utcnow()
            )

        )

        chunk_number += 1

# ============================================================
# Store Chunks
# ============================================================

chunk_df = spark.createDataFrame(

    chunk_records,

    [
        "chunk_id",
        "document_id",
        "chunk_number",
        "chunk_text",
        "created_timestamp"
    ]

)

(
    chunk_df.write
    .format("delta")
    .mode("append")
    .saveAsTable(CHUNK_TABLE)
)

# ============================================================
# Store Embeddings
# ============================================================

embedding_df = spark.createDataFrame(

    embedding_records,

    [
        "chunk_id",
        "document_id",
        "document_name",
        "document_type",
        "source_system",
        "embedding_vector",
        "created_timestamp"
    ]

)

(
    embedding_df.write
    .format("delta")
    .mode("append")
    .saveAsTable(EMBEDDING_TABLE)
)

# ============================================================
# Processing Statistics
# ============================================================

document_count = len(documents)

chunk_count = len(chunk_records)

embedding_count = len(embedding_records)

print(
    f"Documents Processed : {document_count}"
)

print(
    f"Chunks Created      : {chunk_count}"
)

print(
    f"Embeddings Created  : {embedding_count}"
)

print(
    "Embedding Generation Completed Successfully"
)
