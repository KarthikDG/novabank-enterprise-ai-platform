# ============================================================
# Agent      : Fraud_Investigation_Agent
# Domain     : Fraud Operations
# Purpose    : AI-powered fraud investigation assistant
# Platform   : Azure OpenAI + RAG + Lakehouse
# ============================================================

from datetime import datetime

# ============================================================
# Configuration
# ============================================================

LLM_MODEL = "gpt-4o"

TOP_K_DOCUMENTS = 5

# ============================================================
# Customer Profile Retrieval
# ============================================================

def get_customer_profile(customer_id):

    query = f"""

    SELECT *

    FROM novabank_prod.analytics.customer360_gold

    WHERE customer_id = {customer_id}

    """

    return spark.sql(query).toPandas()

# ============================================================
# Transaction History
# ============================================================

def get_transaction_history(customer_id):

    query = f"""

    SELECT *

    FROM novabank_prod.transactions.transactions_silver

    WHERE customer_id = {customer_id}

    ORDER BY transaction_timestamp DESC

    LIMIT 50

    """

    return spark.sql(query).toPandas()

# ============================================================
# Fraud Case Information
# ============================================================

def get_fraud_case(transaction_id):

    query = f"""

    SELECT *

    FROM novabank_prod.fraud.fact_fraud_cases

    WHERE transaction_id = '{transaction_id}'

    """

    return spark.sql(query).toPandas()

# ============================================================
# Knowledge Retrieval (RAG)
# ============================================================

def retrieve_knowledge(question):

    documents = rag_pipeline.retrieve_documents(
        question,
        top_k=TOP_K_DOCUMENTS
    )

    context = "\n".join(
        [d.content for d in documents]
    )

    return context

# ============================================================
# Investigation Prompt
# ============================================================

def build_prompt(
    customer_profile,
    fraud_case,
    transaction_history,
    knowledge_context
):

    return f"""

You are a Senior Fraud Investigator.

Review the information below and generate:

1. Executive Summary
2. Fraud Indicators
3. Risk Assessment
4. Recommended Actions
5. Policy References

CUSTOMER PROFILE

{customer_profile}

FRAUD CASE

{fraud_case}

TRANSACTION HISTORY

{transaction_history}

KNOWLEDGE CONTEXT

{knowledge_context}

Provide a professional fraud investigation report.

"""

# ============================================================
# Generate Investigation Report
# ============================================================

def investigate_fraud_case(
    customer_id,
    transaction_id
):

    profile = get_customer_profile(
        customer_id
    )

    history = get_transaction_history(
        customer_id
    )

    case = get_fraud_case(
        transaction_id
    )

    context = retrieve_knowledge(
        "Fraud investigation procedures"
    )

    prompt = build_prompt(
        profile,
        case,
        history,
        context
    )

    response = azure_openai.chat.completions.create(

        model=LLM_MODEL,

        messages=[
            {
                "role": "system",
                "content":
                    "You are a fraud investigation expert."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.1

    )

    return response.choices[0].message.content

# ============================================================
# Audit
# ============================================================

def log_investigation(
    customer_id,
    transaction_id
):

    audit_record = [

        (
            customer_id,
            transaction_id,
            datetime.utcnow()
        )

    ]

    audit_df = spark.createDataFrame(
        audit_record,
        [
            "customer_id",
            "transaction_id",
            "investigation_timestamp"
        ]
    )

    (
        audit_df.write
        .format("delta")
        .mode("append")
        .saveAsTable(
            "novabank_prod.genai.investigation_audit"
        )
    )

# ============================================================
# Example Execution
# ============================================================

if __name__ == "__main__":

    customer_id = 10001

    transaction_id = "TXN-982734"

    report = investigate_fraud_case(
        customer_id,
        transaction_id
    )

    print(report)

    log_investigation(
        customer_id,
        transaction_id
    )
