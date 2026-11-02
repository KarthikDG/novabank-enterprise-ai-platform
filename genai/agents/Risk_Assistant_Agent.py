# ============================================================
# Agent      : Risk_Assistant_Agent
# Domain     : Risk Management
# Purpose    : AI-powered enterprise risk assistant
# Platform   : Azure OpenAI + RAG + Lakehouse
# ============================================================

from datetime import datetime

# ============================================================
# Configuration
# ============================================================

LLM_MODEL = "gpt-4o"

TOP_K_DOCUMENTS = 5

# ============================================================
# Customer Risk Profile
# ============================================================

def get_customer_risk_profile(customer_id):

    query = f"""

    SELECT *

    FROM novabank_prod.risk.fact_risk_scores

    WHERE customer_id = {customer_id}

    """

    return spark.sql(query).toPandas()

# ============================================================
# Customer360 Information
# ============================================================

def get_customer_360(customer_id):

    query = f"""

    SELECT *

    FROM novabank_prod.analytics.customer360_gold

    WHERE customer_id = {customer_id}

    """

    return spark.sql(query).toPandas()

# ============================================================
# Fraud Exposure
# ============================================================

def get_fraud_exposure(customer_id):

    query = f"""

    SELECT

        fraud_risk_level,

        count(*) as fraud_cases,

        sum(transaction_amount)
            as fraud_exposure

    FROM novabank_prod.fraud.fact_fraud_cases

    WHERE customer_id = {customer_id}

    GROUP BY fraud_risk_level

    """

    return spark.sql(query).toPandas()

# ============================================================
# Portfolio Risk Summary
# ============================================================

def get_portfolio_risk_summary():

    query = """

    SELECT

        enterprise_risk_level,

        count(*) as customers,

        sum(total_exposure)
            as exposure

    FROM novabank_prod.risk.fact_risk_scores

    GROUP BY enterprise_risk_level

    """

    return spark.sql(query).toPandas()

# ============================================================
# RAG Knowledge Retrieval
# ============================================================

def retrieve_knowledge(question):

    docs = rag_pipeline.retrieve_documents(
        question,
        top_k=TOP_K_DOCUMENTS
    )

    return "\n".join(
        [d.content for d in docs]
    )

# ============================================================
# Prompt Creation
# ============================================================

def build_prompt(
    customer_profile,
    customer360,
    fraud_exposure,
    portfolio_summary,
    context
):

    return f"""

You are a Senior Enterprise Risk Analyst.

Provide:

1. Executive Summary
2. Risk Assessment
3. Risk Drivers
4. Exposure Analysis
5. Fraud Exposure
6. Regulatory Considerations
7. Recommendations

CUSTOMER RISK PROFILE

{customer_profile}

CUSTOMER 360

{customer360}

FRAUD EXPOSURE

{fraud_exposure}

PORTFOLIO SUMMARY

{portfolio_summary}

KNOWLEDGE BASE

{context}

Generate a professional
risk assessment report.

"""

# ============================================================
# Generate Risk Report
# ============================================================

def generate_risk_assessment(customer_id):

    customer_profile = (
        get_customer_risk_profile(
            customer_id
        )
    )

    customer360 = (
        get_customer_360(
            customer_id
        )
    )

    fraud_exposure = (
        get_fraud_exposure(
            customer_id
        )
    )

    portfolio_summary = (
        get_portfolio_risk_summary()
    )

    context = retrieve_knowledge(
        "risk management policy"
    )

    prompt = build_prompt(
        customer_profile,
        customer360,
        fraud_exposure,
        portfolio_summary,
        context
    )

    response = azure_openai.chat.completions.create(

        model=LLM_MODEL,

        messages=[
            {
                "role": "system",
                "content":
                    "You are a banking risk expert."
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

def log_assessment(customer_id):

    audit_df = spark.createDataFrame(

        [
            (
                customer_id,
                datetime.utcnow()
            )
        ],

        [
            "customer_id",
            "assessment_timestamp"
        ]

    )

    (
        audit_df.write
        .format("delta")
        .mode("append")
        .saveAsTable(
            "novabank_prod.genai.risk_assessment_audit"
        )
    )

# ============================================================
# Example Execution
# ============================================================

if __name__ == "__main__":

    customer_id = 10001

    report = generate_risk_assessment(
        customer_id
    )

    print(report)

    log_assessment(customer_id)
