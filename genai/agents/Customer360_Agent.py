# ============================================================
# Agent      : Customer360_Agent
# Domain     : Customer Relationship Management
# Purpose    : AI-powered Customer 360 Assistant
# Platform   : Azure OpenAI + Customer360 + RAG
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
# Transaction Summary
# ============================================================

def get_transaction_summary(customer_id):

    query = f"""

    SELECT

        count(*) as total_transactions,

        sum(transaction_amount) as total_spend,

        avg(transaction_amount) as average_spend,

        max(transaction_timestamp)
            as last_transaction_date

    FROM novabank_prod.transactions.transactions_silver

    WHERE customer_id = {customer_id}

    """

    return spark.sql(query).toPandas()

# ============================================================
# Fraud Summary
# ============================================================

def get_fraud_summary(customer_id):

    query = f"""

    SELECT

        fraud_risk_level,

        count(*) as case_count

    FROM novabank_prod.fraud.fact_fraud_cases

    WHERE customer_id = {customer_id}

    GROUP BY fraud_risk_level

    """

    return spark.sql(query).toPandas()

# ============================================================
# Risk Summary
# ============================================================

def get_risk_profile(customer_id):

    query = f"""

    SELECT *

    FROM novabank_prod.risk.fact_risk_scores

    WHERE customer_id = {customer_id}

    """

    return spark.sql(query).toPandas()

# ============================================================
# Product Holdings
# ============================================================

def get_customer_products(customer_id):

    query = f"""

    SELECT

        product_type,

        product_status,

        balance

    FROM novabank_prod.customer.customer_products

    WHERE customer_id = {customer_id}

    """

    return spark.sql(query).toPandas()

# ============================================================
# Knowledge Retrieval
# ============================================================

def retrieve_knowledge(question):

    documents = rag_pipeline.retrieve_documents(
        question,
        top_k=TOP_K_DOCUMENTS
    )

    return "\n".join(
        [doc.content for doc in documents]
    )

# ============================================================
# Prompt Builder
# ============================================================

def build_prompt(
    profile,
    transaction_summary,
    fraud_summary,
    risk_profile,
    products,
    context
):

    return f"""

You are a NovaBank Relationship Manager Assistant.

Create a professional customer summary.

Provide:

1. Executive Summary
2. Customer Profile
3. Product Holdings
4. Spending Behaviour
5. Risk Profile
6. Fraud Risk Assessment
7. Recommended Actions
8. Cross-Sell Opportunities

CUSTOMER PROFILE

{profile}

TRANSACTION SUMMARY

{transaction_summary}

FRAUD SUMMARY

{fraud_summary}

RISK PROFILE

{risk_profile}

PRODUCT HOLDINGS

{products}

REFERENCE CONTEXT

{context}

Use business-friendly language.

"""

# ============================================================
# Generate Customer Summary
# ============================================================

def generate_customer_summary(
    customer_id
):

    profile = get_customer_profile(
        customer_id
    )

    transactions = (
        get_transaction_summary(
            customer_id
        )
    )

    fraud = get_fraud_summary(
        customer_id
    )

    risk = get_risk_profile(
        customer_id
    )

    products = (
        get_customer_products(
            customer_id
        )
    )

    context = retrieve_knowledge(
        "customer relationship management"
    )

    prompt = build_prompt(
        profile,
        transactions,
        fraud,
        risk,
        products,
        context
    )

    response = azure_openai.chat.completions.create(

        model=LLM_MODEL,

        messages=[
            {
                "role": "system",
                "content":
                    "You are a banking relationship manager."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.1

    )

    return (
        response
        .choices[0]
        .message
        .content
    )

# ============================================================
# Audit Logging
# ============================================================

def log_interaction(customer_id):

    audit_df = spark.createDataFrame(

        [
            (
                customer_id,
                datetime.utcnow()
            )
        ],

        [
            "customer_id",
            "request_timestamp"
        ]

    )

    (
        audit_df.write
        .format("delta")
        .mode("append")
        .saveAsTable(
            "novabank_prod.genai.customer360_audit"
        )
    )

# ============================================================
# Example Execution
# ============================================================

if __name__ == "__main__":

    customer_id = 10001

    summary = generate_customer_summary(
        customer_id
    )

    print(summary)

    log_interaction(customer_id)
