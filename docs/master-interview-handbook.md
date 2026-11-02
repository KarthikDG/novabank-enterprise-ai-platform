# NovaBank Enterprise AI Platform
# Master Interview Handbook

Version: 1.0

---

# Purpose

This handbook serves as a complete interview preparation guide covering:

```text
Azure Data Engineering

Databricks Engineering

Analytics Engineering

Data Architecture

Solution Architecture

MLOps

Generative AI

Power BI

Terraform

CI/CD

Security

Governance
```

---

# Table of Contents

1. Executive Introduction
2. Project Overview
3. Architecture Walkthrough
4. Azure Data Factory
5. Azure Event Hub
6. Azure Data Lake
7. Azure Databricks
8. Delta Lake
9. Unity Catalog
10. Analytics Engineering with dbt
11. Customer 360
12. Fraud Analytics
13. Risk Analytics
14. Machine Learning
15. MLflow
16. MLOps
17. Generative AI
18. RAG
19. Vector Search
20. AI Agents
21. Power BI
22. Terraform
23. Security
24. Monitoring
25. CI/CD
26. STAR Stories
27. Scenario-Based Questions
28. Architect-Level Questions

---

# SECTION 1
# Executive Introduction

## Interview Introduction (30 Seconds)

> I designed a cloud-native Azure Enterprise AI Platform using Azure Data Factory, Azure Databricks, Delta Lake, dbt, MLflow, Azure OpenAI, Terraform, and Power BI. The platform supports Customer 360, Fraud Analytics, Risk Management, MLOps, and Generative AI capabilities while providing enterprise-grade security, monitoring, governance, and CI/CD.

---

## Interview Introduction (60 Seconds)

> The platform ingests data from banking, payments, CRM, and regulatory systems using Azure Data Factory and Event Hub. Data is stored in Azure Data Lake using a Medallion Architecture and transformed with Databricks and dbt. Gold-layer datasets support executive reporting, machine learning models, and Generative AI assistants. Infrastructure is deployed through Terraform and Azure DevOps, while governance is implemented using Unity Catalog, Key Vault, RBAC, and monitoring frameworks.

---

# SECTION 2
# Architecture Questions

## Q1. Describe the architecture.

### Answer

```text
Source Systems
      │
      ▼
ADF + Event Hub
      │
      ▼
ADLS Gen2
      │
      ▼
Bronze Layer
      │
      ▼
Databricks
      │
      ▼
Silver Layer
      │
      ▼
dbt
      │
      ▼
Gold Layer
      │
 ┌────┼───────────┐
 ▼    ▼           ▼

Power BI
MLflow
Azure OpenAI
```

---

## Q2. Why choose a Lakehouse architecture?

### Answer

Benefits:

```text
Open Architecture

Lower Cost

Unified Analytics

ACID Compliance

Machine Learning Support

Real-Time Processing
```

---

## Q3. Why combine Databricks and dbt?

### Answer

Databricks handles:

```text
Engineering Transformations

Streaming

Feature Engineering
```

dbt handles:

```text
Business Logic

Testing

Documentation

Lineage
```

---

# SECTION 3
# Azure Data Factory

## Q4. Explain your ADF design.

### Answer

ADF provides:

```text
Metadata-Driven Pipelines

Incremental Loads

CDC

Scheduling

Pipeline Orchestration
```

---

## Q5. What is a metadata-driven framework?

### Answer

A control table stores:

```text
Source System

Source Object

Load Type

Watermark Column

Active Flag
```

One generic pipeline dynamically processes many sources.

---

## Q6. How would you load 500 tables?

### Answer

Not with 500 pipelines.

Use:

```text
Metadata Table

Lookup

ForEach Activity

Dynamic Parameters
```

---

## Q7. Explain watermark processing.

### Answer

Last loaded timestamp is stored.

Query:

```sql
SELECT *
FROM Transactions
WHERE LastModifiedDate >
      WatermarkValue
```

---

## Q8. How do you handle failures?

### Answer

Implemented:

```text
Retries

Error Logging

Quarantine Zone

Alerting
```

---

# SECTION 4
# Databricks

## Q9. Why Databricks?

### Answer

Provides:

```text
Spark

Delta Lake

Streaming

MLflow

Unity Catalog
```

---

## Q10. Explain Bronze Layer.

### Answer

Stores raw source data.

Characteristics:

```text
Immutable

Historical

Audit Ready
```

---

## Q11. Explain Silver Layer.

### Answer

Performs:

```text
Data Cleansing

Standardisation

Enrichment

Validation
```

---

## Q12. Explain Gold Layer.

### Answer

Creates:

```text
Customer360

Fraud Analytics

Risk Analytics
```

for business users.

---

# SECTION 5
# Delta Lake

## Q13. What problems does Delta Lake solve?

### Answer

Provides:

```text
ACID Transactions

Time Travel

Schema Evolution

Concurrent Writes
```

---

## Q14. What is Time Travel?

### Answer

Query historical versions:

```sql
SELECT *
FROM customer_silver
VERSION AS OF 10
```

---

## Q15. What is OPTIMIZE?

### Answer

Compacts small files.

Improves performance.

---

## Q16. What is ZORDER?

### Answer

Improves data skipping.

Example:

```sql
OPTIMIZE transactions
ZORDER BY(customer_id)
```

---

# SECTION 6
# Unity Catalog

## Q17. Why Unity Catalog?

### Answer

Provides:

```text
Governance

Lineage

Security

Discovery
```

---

## Q18. What security levels exist?

### Answer

```text
Catalog

Schema

Table

Column

Row
```

---

# SECTION 7
# dbt

## Q19. What is dbt?

### Answer

Analytics engineering framework used for:

```text
Transformations

Testing

Documentation

Lineage
```

---

## Q20. Difference between view and table materialisation?

### Answer

View:

```text
Computed At Runtime
```

Table:

```text
Persisted Results
```

---

## Q21. What is ref()?

### Answer

Creates model dependencies.

Example:

```sql
{{ ref('dim_customer') }}
```

---

## Q22. What tests did you implement?

### Answer

```text
Unique

Not Null

Accepted Values

Relationships
```

---

# SECTION 8
# Customer 360

## Q23. What is Customer360?

### Answer

Unified profile containing:

```text
Customer

Products

Transactions

Risk

Fraud
```

---

## Q24. Why is Customer360 important?

### Answer

Supports:

```text
Personalization

Cross-Sell

Risk Analysis

Customer Service
```

---

# SECTION 9
# Fraud Analytics

## Q25. Explain fraud scoring.

### Answer

Inputs:

```text
Transaction Amount

Fraud History

Customer Behaviour

Transaction Patterns
```

Output:

```text
Risk Score
```

---

## Q26. Explain fraud workflow.

### Answer

```text
Transactions

▼

Fraud Features

▼

ML Scoring

▼

Investigation Queue
```

---

# SECTION 10
# Risk Analytics

## Q27. How is risk calculated?

### Answer

Combines:

```text
Exposure

Fraud Signals

Customer Behaviour

Risk Profile
```

---

## Q28. Risk classification example?

### Answer

```text
LOW

MEDIUM

HIGH
```

based on calculated risk scores.

---

# SECTION 11
# MLOps

## Q29. Why MLflow?

### Answer

Supports:

```text
Experiment Tracking

Model Registry

Deployment

Monitoring
```

---

## Q30. Explain model lifecycle.

### Answer

```text
Development

▼

Staging

▼

Production
```

---

## Q31. What is model drift?

### Answer

Production data differs from training data.

Can reduce model accuracy.

---

# SECTION 12
# Generative AI

## Q32. What is RAG?

### Answer

Retrieval Augmented Generation.

Combines:

```text
Search

Context Retrieval

LLM Generation
```

---

## Q33. Why use RAG?

### Answer

Benefits:

```text
Grounded Responses

Reduced Hallucinations

Enterprise Knowledge
```

---

## Q34. What are embeddings?

### Answer

Vector representations of text.

Used for:

```text
Similarity Matching

Vector Search
```

---

## Q35. What is vector search?

### Answer

Searching by meaning rather than keywords.

---

# SECTION 13
# AI Agents

## Q36. Describe the Fraud Agent.

### Answer

Uses:

```text
Fraud Cases

Transactions

Customer360

Knowledge Base
```

to create investigation reports.

---

## Q37. Describe the Customer360 Agent.

### Answer

Generates:

```text
Customer Summary

Product Insights

Cross-Sell Opportunities
```

---

## Q38. Describe the Risk Agent.

### Answer

Provides:

```text
Risk Assessments

Exposure Analysis

Recommendations
```

---

# SECTION 14
# Terraform

## Q39. Why Terraform?

### Answer

Provides:

```text
Infrastructure As Code

Version Control

Repeatable Deployments
```

---

## Q40. Resources deployed?

### Answer

```text
ADF

Databricks

Storage

Networking

Key Vault

Monitoring
```

---

# SECTION 15
# Security

## Q41. Explain security architecture.

### Answer

Implemented:

```text
Entra ID

RBAC

Managed Identity

Key Vault

Unity Catalog

Private Endpoints
```

---

## Q42. Why Managed Identity?

### Answer

Eliminates:

```text
Passwords

Credential Rotation Problems
```

---

## Q43. How is PII protected?

### Answer

```text
Encryption

Masking

RBAC

Private Networks
```

---

# SECTION 16
# Monitoring

## Q44. What is monitored?

### Answer

```text
ADF

Databricks

dbt

ML Models

AI Services
```

---

## Q45. What is model monitoring?

### Answer

Tracks:

```text
Accuracy

Drift

Latency

Prediction Volume
```

---

# SECTION 17
# CI/CD

## Q46. Explain deployment flow.

### Answer

```text
Developer

▼

GitHub

▼

Azure DevOps

▼

Terraform

▼

Deploy
```

---

# SECTION 18
# STAR STORIES

## STAR Story 1
### Fraud Analytics

Situation:

Fraud detection was delayed.

Task:

Create faster fraud monitoring.

Action:

Implemented:

```text
Event Hub

Streaming

Fraud Scoring

Dashboards
```

Result:

Improved visibility and reduced latency.

---

## STAR Story 2
### Customer360

Situation:

Customer data fragmented across systems.

Task:

Create unified customer profile.

Action:

Implemented Customer360 model.

Result:

Improved customer insights and reporting.

---

## STAR Story 3
### Generative AI

Situation:

Employees struggled finding policies.

Task:

Build knowledge assistant.

Action:

Implemented:

```text
RAG

Embeddings

Vector Search

Azure OpenAI
```

Result:

Faster information retrieval.

---

# Architect-Level Questions

## How would this platform scale to 100 TB?

Answer:

```text
Partitioning

Streaming

Auto Scaling Clusters

Optimized Delta Tables

Incremental Processing
```

---

## How would you make architecture multi-region?

Answer:

```text
Geo Replication

Cross Region Storage

Secondary Event Hub

DR Environment
```

---

# Ultimate Closing Answer

If the interviewer says:

"Tell me about your strongest project."

Answer:

> NovaBank is an enterprise-scale Azure Data & AI platform that I designed using Azure Data Factory, Databricks, Delta Lake, dbt, MLflow, Azure OpenAI, Terraform, and Power BI. The platform supports Customer360, Fraud Analytics, Risk Analytics, MLOps, and Generative AI while implementing CI/CD, security, governance, monitoring, and enterprise architecture best practices.
