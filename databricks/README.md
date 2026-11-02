# Databricks Lakehouse Platform

## Overview

Azure Databricks is the core data engineering, analytics, machine learning, and AI platform for the NovaBank Enterprise AI Platform.

The platform processes data from Azure Data Factory and Event Hub and transforms it into trusted business datasets for analytics, machine learning, and GenAI workloads.

---

# Core Responsibilities

Databricks supports:

- Data Engineering
- Batch Processing
- Streaming Processing
- Data Quality
- Fraud Detection
- Risk Analytics
- Feature Engineering
- Machine Learning
- MLOps
- GenAI

---

# Medallion Architecture

The platform follows the Databricks Lakehouse Medallion Architecture.

```text
                  Raw Sources
                        |
                        ▼
                 BRONZE LAYER
                        |
                        ▼
                 SILVER LAYER
                        |
                        ▼
                  GOLD LAYER
                        |
            ┌───────────┼───────────┐
            ▼           ▼           ▼

        Power BI     ML Models    GenAI
```

---

# Bronze Layer

Purpose:

```text
Raw Data Ingestion
```

Examples:

```text
Customer Data
Transactions
Loans
Mortgages
CRM Data
AML Data
```

Source Location:

```text
abfss://bronze@stnovabankdev.dfs.core.windows.net/
```

Characteristics:

- Raw Data
- No Business Transformations
- Historical Retention
- Audit Ready

---

# Silver Layer

Purpose:

```text
Data Cleansing
Data Validation
Standardisation
Enrichment
```

Examples:

```text
Customer Standardisation

Transaction Validation

Fraud Enrichment

Risk Reference Data
```

Processes:

- Remove Duplicates
- Handle Null Values
- Validate Data Types
- Data Quality Checks

---

# Gold Layer

Purpose:

```text
Business Consumption
```

Examples:

```text
Customer 360

Fraud Analytics

Risk Analytics

Executive Dashboards

AI Features
```

Consumers:

```text
Power BI
Databricks SQL
Machine Learning
GenAI Applications
```

---

# Folder Structure

```text
databricks/

├── README.md

├── bronze/

├── silver/

├── gold/

├── notebooks/

├── utilities/

├── shared/
```

---

# Unity Catalog Structure

```text
novabank_prod

├── customer

├── transactions

├── fraud

├── risk

└── analytics
```

---

# Example Tables

## Customer Domain

```text
customer_bronze

customer_silver

dim_customer
```

## Transactions

```text
transactions_bronze

transactions_silver

fact_transactions
```

## Fraud

```text
fraud_events

fraud_scores

fact_fraud_cases
```

---

# Delta Lake Features

The platform uses Delta Lake for:

```text
ACID Transactions

Time Travel

Schema Evolution

Data Versioning

Scalable Storage
```

---

# Batch Processing

Executed by:

```text
Azure Data Factory
```

Workflow:

```text
ADF
    │
    ▼

Databricks Notebook

    │
    ▼

Bronze → Silver → Gold
```

---

# Real-Time Streaming

Source:

```text
Azure Event Hub
```

Workflow:

```text
Event Hub
      │
      ▼

Structured Streaming
      │
      ▼

Silver Layer
```

Use Cases:

```text
Transaction Monitoring

Fraud Detection

Customer Activity Tracking
```

---

# Machine Learning

Supported Use Cases:

```text
Fraud Prediction

Customer Churn

Risk Scoring

Credit Risk
```

Tools:

```text
MLflow

Databricks ML

Feature Store
```

---

# GenAI

The platform supports:

```text
Azure OpenAI

RAG

Vector Search

AI Agents
```

Examples:

```text
Relationship Manager Assistant

Fraud Investigation Assistant

Policy Search Assistant
```

---

# Security

Implemented Controls:

```text
Unity Catalog

RBAC

Data Lineage

Column Level Security

Row Level Security

Secret Scopes
```

---

# Monitoring

Monitor:

```text
Job Failures

Cluster Utilisation

Data Quality

ML Drift

Streaming Performance
```

---

# Development Standards

Languages:

```text
Python

PySpark

SQL
```

Preferred Notebook Structure:

```text
Configuration

Read Data

Transformation

Validation

Write Data

Logging
```

---

# Next Deliverables

The next notebooks to be created are:

```text
bronze/

NB_Customer_Bronze_Load.py

NB_Transaction_Bronze_Load.py

silver/

NB_Customer_Silver_Cleansing.py

NB_Transaction_Silver_Cleansing.py

gold/

NB_Customer360_Gold.py

NB_FraudAnalytics_Gold.py
```

These notebooks implement the complete Bronze → Silver → Gold processing framework.
